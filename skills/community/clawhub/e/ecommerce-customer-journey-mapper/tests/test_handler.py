import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import JourneyAnalyzer, handle

def test_mode_detection():
    a = JourneyAnalyzer('Please run a full audit for my checkout flow')
    assert a.mode == 'deep'
    print('✓ test_mode_detection passed')

def test_goal_detection_checkout():
    a = JourneyAnalyzer('Our checkout completion is weak and payment confidence is low')
    assert a.goal == 'checkout'
    print('✓ test_goal_detection_checkout passed')

def test_goal_detection_retention():
    a = JourneyAnalyzer('We have low repeat purchase and weak retention after first order')
    assert a.goal == 'retention'
    print('✓ test_goal_detection_retention passed')

def test_stage_mapping_awareness():
    a = JourneyAnalyzer('Meta ads click-through is okay but landing page messaging is weak')
    assert 'meta' in a.matched['Awareness']
    print('✓ test_stage_mapping_awareness passed')

def test_stage_mapping_checkout():
    a = JourneyAnalyzer('Shipping fees show too late during checkout payment step')
    assert 'checkout' in a.matched['Checkout']
    print('✓ test_stage_mapping_checkout passed')

def test_handle_returns_markdown():
    out = handle('Map my ecommerce journey from ads to checkout')
    assert out.startswith('# E-commerce Customer Journey Map')
    assert '## Journey Stage Map' in out
    print('✓ test_handle_returns_markdown passed')

def test_contains_five_plus_stages():
    out = handle('journey audit for DTC brand')
    assert out.count('### ') >= 5
    print('✓ test_contains_five_plus_stages passed')

def test_contains_priority_actions():
    out = handle('checkout dropoff analysis')
    assert '## Prioritized Action Brief' in out
    assert '1. **' in out
    print('✓ test_contains_priority_actions passed')

if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
