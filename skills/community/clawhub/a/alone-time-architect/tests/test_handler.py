#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import handle


def test_overstimulated_context_detects_rest_need():
    output = handle('I feel overstimulated after a busy family day and need 30 minutes alone')
    assert '# Alone Time Blueprint' in output
    assert '- What I need from this solitude: Rest' in output
    assert '- Available time: 30 minutes' in output


def test_dict_input_preserves_location_and_time():
    output = handle({
        'purpose': 'Creative space',
        'available_time': '1 hour',
        'location': 'Library table near a window'
    })
    assert 'Creative space' in output
    assert '1 hour' in output
    assert 'Library table near a window' in output


def test_output_contains_phone_rule_and_reentry():
    output = handle('Need some solitude to clear my head without wasting it on my phone')
    assert '- Phone rule:' in output
    assert '## Re-entry' in output


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
