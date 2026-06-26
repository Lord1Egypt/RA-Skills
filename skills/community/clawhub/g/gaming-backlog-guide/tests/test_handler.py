#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import handle


def test_low_friction_profile_for_tired_short_session():
    result = handle({
        'skill_name': 'gaming-backlog-guide',
        'input': {
            'mood': 'tired and want to decompress',
            'time': 25,
            'platform': 'Switch',
            'budget': 'low',
            'recent_types': 'long RPGs',
        },
    })['result']
    assert 'Low-friction decompression' in result
    assert "Tonight's Easiest Start" in result
    assert 'Avoid for Now' in result


def test_social_case_is_supported():
    result = handle({
        'skill_name': 'gaming-backlog-guide',
        'input': 'Mood: playful\nTime: 60 minutes\nPlatform: PC\nWith whom: family on the couch\nBudget: low',
    })['result']
    assert 'Best-Fit Directions' in result
    assert ('Shared couch or co-op energy' in result) or ('Comfort companion' in result)


def test_prompt_mode_returns_template():
    result = handle({'skill_name': 'gaming-backlog-guide', 'mode': 'prompt'})['result']
    assert 'mood, time, energy' in result.lower()
    assert 'weekend option' in result.lower()


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
