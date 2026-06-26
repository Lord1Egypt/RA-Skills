#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import LogisticsOptimizer, handle


def test_priority_detection_fastest():
    tool = LogisticsOptimizer('Need the fastest route from China to Germany for electronics')
    assert tool.priority == 'fastest'


def test_country_extraction():
    tool = LogisticsOptimizer('Compare lanes from China to Germany for cosmetics')
    assert tool.origin == 'China'
    assert tool.destination == 'Germany'


def test_risk_flags_for_brazil_cosmetics():
    tool = LogisticsOptimizer('Safest route from China to Brazil for cosmetics with customs delay concerns')
    joined = ' '.join(tool.risk_flags).lower()
    assert 'brazil' in joined
    assert 'cosmetics' in joined or 'ingredient' in joined or 'leak' in joined


def test_render_contains_sections():
    output = handle('Cheapest way to ship accessories from US to Canada at 0.5kg and 30x20x10cm')
    assert output.startswith('# Cross-border Logistics Decision Brief')
    assert '## Route Comparison' in output
    assert '## Packaging Checklist' in output


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
