#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import FocusSessionPlanner, handle


def test_deep_work_mode_for_heavy_task():
    planner = FocusSessionPlanner('I need to write a strategy memo and I can protect a full hour this morning.')
    assert planner.mode['label'] == 'Deep Work Block'


def test_quick_sprint_for_light_task():
    planner = FocusSessionPlanner('Help me focus on email cleanup for 15 minutes before a meeting.')
    assert planner.mode['label'] == 'Quick Sprint'


def test_output_sections():
    output = handle('I want a focused study session for calculus, but I get interrupted by my kids.')
    assert output.startswith('# Focus Session Card')
    assert '## During Session' in output
    assert '## Break Plan' in output
    assert '## End Review' in output


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
