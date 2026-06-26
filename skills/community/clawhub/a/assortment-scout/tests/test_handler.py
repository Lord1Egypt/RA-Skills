#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import AssortmentScout, handle


def test_objective_detection_cleanup():
    scout = AssortmentScout('We need to prune SKU clutter, rationalize duplicates, and retire weak long-tail products.')
    assert scout.objective == 'SKU Cleanup'


def test_signal_detection_margin_reviews_and_variants():
    scout = AssortmentScout('Review margin, return rate, product ratings, and size-color variant coverage for our fashion line.')
    assert 'Margin / Cost' in scout.signals
    assert 'Returns / Reviews' in scout.signals
    assert 'Variants / Coverage' in scout.signals


def test_dict_input_supported():
    output = handle({
        'objective': 'find assortment gaps',
        'signals': ['revenue', 'margin', 'inventory'],
        'constraints': ['warehouse capacity'],
        'notes': 'Need a category review before our seasonal cleanup.',
    })
    assert '# Assortment Scout Brief' in output
    assert '## Coverage and Gap Map' in output


def test_render_contains_sections():
    output = handle('Audit our catalog for hero dependence, duplicate-risk SKUs, price-band gaps, and long-tail bloat.')
    assert output.startswith('# Assortment Scout Brief')
    assert '## Assortment Health Summary' in output
    assert '## Action Recommendations' in output
    assert '## 30-Day Execution Brief' in output


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
