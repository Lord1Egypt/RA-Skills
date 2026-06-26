import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import ProductResearchEngine, handle

def test_market_extraction():
    e = ProductResearchEngine('portable neck stretcher, US market, price $29-$49')
    assert e.market == 'US'
    print('✓ test_market_extraction passed')

def test_price_band_extraction():
    e = ProductResearchEngine('pet glove UK market $19-$35')
    assert e.price_low == 19 and e.price_high == 35
    print('✓ test_price_band_extraction passed')

def test_competition_saturated():
    e = ProductResearchEngine('galaxy projector germany market')
    assert e.score_competition() >= 75
    print('✓ test_competition_saturated passed')

def test_risk_detection():
    e = ProductResearchEngine('medical liquid product for baby')
    assert e.score_risk() >= 60
    print('✓ test_risk_detection passed')

def test_recommendation_present():
    out = handle('portable pet grooming glove UK market $19-$35 demo content')
    assert 'Recommendation: **' in out
    print('✓ test_recommendation_present passed')

def test_output_has_all_dimensions():
    out = handle('portable organizer US market $25-$49')
    for key in ['Demand potential', 'Competition saturation', 'Margin potential', 'Creative angle potential', 'Logistics / compliance risk']:
        assert key in out
    print('✓ test_output_has_all_dimensions passed')

def test_output_markdown():
    out = handle('neck stretcher US $29-$49')
    assert out.startswith('# Dropshipping Product Research Memo')
    print('✓ test_output_markdown passed')

if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
