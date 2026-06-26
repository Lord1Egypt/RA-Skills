#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import CommerceBICopilot, handle


def test_mode_detection_anomaly():
    copilot = CommerceBICopilot('Why did GMV drop yesterday after our promotion?')
    assert copilot.mode == 'Anomaly Diagnosis'


def test_metric_detection_refund_and_inventory():
    copilot = CommerceBICopilot('Need a weekly review of refunds, returns, and stockout issues')
    assert 'Refund Rate' in copilot.metrics
    assert 'Inventory Health' in copilot.metrics


def test_channel_detection_meta_and_shopify():
    copilot = CommerceBICopilot('Turn our Shopify and Meta notes into an executive summary')
    assert 'Shopify' in copilot.channels
    assert 'Meta Ads' in copilot.channels


def test_render_contains_key_sections():
    output = handle('Create a weekly ecommerce review for GMV, ROAS, refunds, and inventory')
    assert output.startswith('# Commerce BI Brief')
    assert '## KPI Snapshot' in output
    assert '## Next Best Actions' in output
    assert '## Executive-Ready Brief' in output


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
