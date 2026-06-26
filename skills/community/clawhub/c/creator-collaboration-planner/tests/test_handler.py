#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import CreatorCollaborationPlanner, handle


def test_channel_detection_tiktok_xiaohongshu():
    planner = CreatorCollaborationPlanner('Build a creator plan for TikTok and Xiaohongshu.')
    assert 'TikTok / Douyin' in planner.channels
    assert 'Xiaohongshu' in planner.channels


def test_program_type_detection_affiliate():
    planner = CreatorCollaborationPlanner('We want an affiliate program with commission payouts for creators.')
    assert planner.program_type == 'Affiliate / Commission Program'


def test_creator_mix_detection_expert_and_ugc():
    planner = CreatorCollaborationPlanner('Need expert creators plus UGC content creators for a trust-building beauty launch.')
    assert 'Expert creators' in planner.creator_mix
    assert 'UGC creators' in planner.creator_mix


def test_render_contains_sections():
    output = handle('Create a creator outreach and brief plan for a product launch on Xiaohongshu.')
    assert output.startswith('# Creator Collaboration Plan')
    assert '## Creator Mix and Selection Rubric' in output
    assert '## Outreach and Negotiation Plan' in output
    assert '## Measurement and Debrief' in output


def test_dict_input_supported():
    output = handle({
        'channels': ['TikTok', 'Instagram'],
        'objective': 'awareness',
        'creator_types': ['micro creators', 'ugc'],
        'program': 'paid sponsored deliverables',
    })
    assert '# Creator Collaboration Plan' in output
    assert 'Paid Campaign Brief' in output


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
