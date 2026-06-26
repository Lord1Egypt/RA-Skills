#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import handle


def test_boundary_scenario_detects_goal():
    output = handle('I need to set a boundary with a coworker who keeps messaging me late at night')
    assert '# Conversation Rehearsal Brief' in output
    assert '- Conversation goal: Setting a boundary' in output


def test_dict_input_preserves_requested_outcome():
    output = handle({
        'purpose': 'Requesting a change',
        'message': 'I need clearer turnaround times on edits',
        'outcome': 'A more predictable workflow next week'
    })
    assert 'I need clearer turnaround times on edits' in output
    assert 'A more predictable workflow next week' in output


def test_output_contains_boundary_sentence_and_close():
    output = handle('I need to tell a friend I cannot keep cancelling my own plans for them')
    assert '- My boundary sentence:' in output
    assert '## Close' in output


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
