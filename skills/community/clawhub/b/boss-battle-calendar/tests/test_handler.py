#!/usr/bin/env python3
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from handler import _load_prompt_template, _load_skill_meta, handle


SKILL_DIR = Path(__file__).resolve().parents[1]
SKILL_NAME = SKILL_DIR.name


def test_load_skill_meta():
    meta = _load_skill_meta(SKILL_NAME)
    assert meta['name'] == SKILL_NAME
    assert meta['description']


def test_prompt_template_sections_exist():
    template = _load_prompt_template(SKILL_NAME)
    for heading in ['## Purpose', '## Workflow', '## Output Format', '## Quality bar']:
        assert heading in template


def test_handle_returns_descriptive_card():
    payload = {
        'skill_name': SKILL_NAME,
        'input': 'Need help turning this into a playable plan.',
        'mode': 'guide',
    }
    result = handle(payload)
    assert isinstance(result, dict)
    text = result['result']
    assert f'- Skill slug: {SKILL_NAME}' in text
    assert '## Workflow' in text
    assert '## Output format' in text
    assert 'Need help turning this into a playable plan.' in text
    assert 'Loaded from SKILL.md' in text


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_') and callable(fn):
            fn()
    print('All tests passed.')
