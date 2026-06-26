#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import SustainabilityAdvisor, handle


def test_hotspot_detection_packaging():
    advisor = SustainabilityAdvisor('We use oversized boxes with plastic bubble wrap for home goods')
    assert 'packaging' in advisor.hotspots


def test_claim_risk_detection():
    advisor = SustainabilityAdvisor('Our site says we are eco-friendly and carbon neutral across every order')
    assert advisor.claim_risk is True


def test_render_contains_sections():
    output = handle('Beauty brand with high returns, express shipping, and vague sustainable messaging')
    assert output.startswith('# E-commerce Sustainability Action Brief')
    assert '## 90-Day Action Roadmap' in output
    assert '## Claim Wording Cautions' in output


def test_kpi_section_present():
    output = handle('Review packaging waste and sustainability claims for our ecommerce brand')
    assert '## KPI Starter Pack' in output


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
