#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import CRMSegmentWinback, handle


def test_business_detection_dtc():
    crm = CRMSegmentWinback('DTC skincare brand CRM segmentation')
    assert crm.business == 'DTC Brand'


def test_segment_detection_lapsed():
    crm = CRMSegmentWinback('Winback strategy for customers who have not purchased in 90 days')
    assert 'Lapsed Customer' in crm.segments


def test_segment_detection_vip():
    crm = CRMSegmentWinback('VIP loyalty program for top-spending customers')
    assert 'VIP / Loyal' in crm.segments


def test_channel_detection_email_sms():
    crm = CRMSegmentWinback('Email and SMS winback campaign for lapsed customers')
    assert 'Email' in crm.channels
    assert 'SMS' in crm.channels


def test_goal_detection_winback():
    crm = CRMSegmentWinback('Reactivate churned subscribers with email and SMS sequence')
    assert crm.goal == 'Winback / Re-engagement'


def test_render_contains_sections():
    output = handle('Build a winback strategy for customers who have not purchased in 90 days')
    assert output.startswith('# CRM Segment & Winback Brief')
    assert '## Segment Framework' in output
    assert '## Winback Trigger Library' in output
    assert '## Campaign Sequence Ideas' in output


def test_dict_input_supported():
    output = handle({
        'business': 'DTC Brand',
        'segments': ['New Customer', 'Lapsed Customer', 'VIP / Loyal'],
        'channels': ['Email', 'SMS'],
        'campaign_goal': 'Winback / Re-engagement'
    })
    assert '# CRM Segment & Winback Brief' in output
    assert 'Winback' in output


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
