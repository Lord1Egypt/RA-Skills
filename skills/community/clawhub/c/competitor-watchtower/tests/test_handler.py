#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import CompetitorWatchtower, handle


def test_watch_mode_detection_pricing():
    tower = CompetitorWatchtower('Run a pricing scan because the competitor launched heavy discount coupons.')
    assert tower.watch_mode == 'Pricing and Promo Scan'


def test_surface_detection_amazon_tiktok():
    tower = CompetitorWatchtower('Monitor Amazon and TikTok Shop competitors this week.')
    assert 'Amazon' in tower.surfaces
    assert 'TikTok Shop / Douyin' in tower.surfaces


def test_signal_detection_reviews_and_service():
    tower = CompetitorWatchtower('Watch reviews, ratings, refunds, and shipping complaints from the rival brand.')
    assert 'Reviews and proof' in tower.signals
    assert 'Service and fulfillment' in tower.signals


def test_render_contains_sections():
    output = handle('Build a weekly competitor watchlist for Amazon and our DTC site.')
    assert output.startswith('# Competitor Watchtower Brief')
    assert '## Signal Grid' in output
    assert '## Response Options' in output
    assert '## Assumptions and Limits' in output


def test_dict_input_supported():
    output = handle({
        'surfaces': ['Amazon', 'DTC site'],
        'watch_mode': 'pricing and promo scan',
        'signals': ['price', 'reviews'],
        'notes': 'competitor has aggressive discounting',
    })
    assert '# Competitor Watchtower Brief' in output
    assert 'Pricing and Promo Scan' in output


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
