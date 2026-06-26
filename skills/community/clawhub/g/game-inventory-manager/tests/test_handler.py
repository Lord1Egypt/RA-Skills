#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import handle


def test_inventory_sections_and_classification():
    result = handle({
        'skill_name': 'game-inventory-manager',
        'input': {
            'items': ['daily planner', 'expired coupons', 'duplicate cable', 'draft notes about summer plan']
        },
    })['result']
    assert 'Equipped Now' in result
    assert 'Discard / Archive' in result
    assert 'expired coupons' in result
    assert 'draft notes about summer plan' in result


def test_cleanup_move_exists():
    result = handle({'skill_name': 'game-inventory-manager', 'input': 'Items: broken charger, weekly checklist, seasonal coat'})['result']
    assert '15-Minute Cleanup Move' in result
    assert 'broken charger' in result


def test_prompt_mode_returns_template():
    result = handle({'skill_name': 'game-inventory-manager', 'mode': 'prompt'})['result']
    assert 'inventory' in result.lower()
    assert '10 to 20 minutes' in result


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
