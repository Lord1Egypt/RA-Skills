#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import EcommercePulseBoard, handle


def test_window_detection_weekly():
    pulse = EcommercePulseBoard('Give me a weekly pulse check on our Shopify and Amazon operations')
    assert pulse.window == 'Weekly'


def test_window_detection_monthly():
    pulse = EcommercePulseBoard('Monthly ecommerce health brief from these KPI notes')
    assert pulse.window == 'Monthly'


def test_channel_detection_shopify_amazon():
    pulse = EcommercePulseBoard('Pulse check for Shopify and Amazon this week')
    assert 'Shopify' in pulse.channels
    assert 'Amazon' in pulse.channels


def test_concern_detection_gmv():
    pulse = EcommercePulseBoard('GMV dropped this week — what is happening?')
    assert pulse.concern == 'GMV / Revenue'


def test_pillar_detection_traffic_conversion():
    pulse = EcommercePulseBoard('Weekly review of traffic and conversion metrics')
    assert 'Traffic' in pulse.pillars
    assert 'Conversion' in pulse.pillars


def test_render_contains_sections():
    output = handle('Give me a pulse check on our Shopify and Amazon operations this week')
    assert output.startswith('# Ecommerce Pulse Brief')
    assert '## Pillar Health Grid' in output
    assert '## Signal of the Week' in output
    assert '## Risk Watchlist' in output
    assert '## Priority Actions' in output


def test_dict_input_supported():
    output = handle({
        'window': 'Weekly',
        'channels': ['Shopify', 'Amazon', 'TikTok Shop'],
        'concern': 'Overall Health',
        'kpis': {'GMV': 'down 5%', 'ROAS': 'stable'}
    })
    assert '# Ecommerce Pulse Brief' in output
    assert 'Weekly' in output


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
