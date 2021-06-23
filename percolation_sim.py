from random import random


class Percolator:
    """A time based simulation of percolation type flow through a network."""
    """Enum of cell states"""
    NAIVE = 0
    INFECTED = 1
    RECOVERED = 2
    VACCINATED = 3
    TRANSMISSION_PROBABILITY = 0.4
    _cells = list(list())
    _length = 0
    _width = 0
    _has_changed = True


    def __init__(self, row_length, col_length):
        self._length = col_length
        self._width = row_length
        self._cells = [self._length * [self.NAIVE] for j in range(self._width)]


    def set_state(self, cell_id, state):
        if cell_id >= self._length * self._width or cell_id < 0:
            raise Exception('Cell ID {} out of range'.format(cell_id))
        i = cell_id // self._length 
        j = cell_id % self._length
        self._cells[i][j] = state


    def cell_state(self, cell_id):
        if cell_id >= self._length * self._width or cell_id < 0:
            raise Exception('Cell ID {} out of range'.format(cell_id))
        i = cell_id // self._length 
        j = cell_id % self._length
        return self._cells[i][j]


    def get_neighbors(self, cell_id):
        if cell_id >= self._length * self._width or cell_id < 0:
            raise Exception('Cell ID {} out of range'.format(cell_id))
        i = cell_id // self._length 
        j = cell_id % self._length
        neighbors = list()
        if i - 1 >= 0:
            neighbors.append((i - 1) * self._length + j)
        if i + 1 < self._width:
            neighbors.append((i + 1) * self._length + j)
        if j - 1 >= 0:
            neighbors.append(i * self._length + j - 1)
        if j + 1 < self._length:
            neighbors.append(i * self._length + j + 1)
        return neighbors


    def percolate(self):
        next_recovered = set()
        next_infected = set()
        self._has_changed = False
        for cell in range(self._length * self._width):
            if self.cell_state(cell) == self.INFECTED:
                next_recovered.add(cell)
                neighbors = self.get_neighbors(cell)
                for n in neighbors:
                    if self.cell_state(n) == self.NAIVE and self.TRANSMISSION_PROBABILITY > random(): 
                        next_infected.add(n)
        for cell in next_recovered:
            self.set_state(cell, self.RECOVERED)
        for cell in next_infected:
            self.set_state(cell, self.INFECTED)
        if len(next_infected) > 0:
            self._has_changed = True


    def has_changed(self):
        return self._has_changed


    def print(self):
        for row in self._cells:
            print(row)
        print()


def main():
    p = Percolator(4, 6)
    p.set_state(12, p.INFECTED)
    p.print()
    while p.has_changed():
        p.percolate()
        p.print()


if __name__ == "__main__":
    main()
