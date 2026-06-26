#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import EnergyPeakFinder, handle


def test_best_window_detection():
    finder = EnergyPeakFinder('Late morning is when I feel sharp and focused, but I crash in the early afternoon after lunch.')
    assert finder.best_window == 'late morning'
    assert finder.lowest_window == 'early afternoon'


def test_disruptor_detection():
    finder = EnergyPeakFinder('I get a good 10am burst, then coffee and after lunch make me foggy.')
    joined = ' '.join(finder.disruptors)
    assert 'caffeine' in joined or 'lunch' in joined or 'meal' in joined


def test_output_sections():
    output = handle('My energy is best in the late morning, but meetings and messages kill the afternoon.')
    assert output.startswith('# Energy Pattern Review')
    assert '## Observation Summary' in output
    assert '## Task Matching' in output
    assert '## Next Experiment' in output


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
