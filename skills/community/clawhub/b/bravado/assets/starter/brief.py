"""Validate the fixed seven-scene starter's inputs before generating any frames.

Product-specific renderers may define a different schema; this describes render.py.
"""
import json
import math
import re
from pathlib import Path

TEXT_FIELDS = {
    'brand': 'name tagline closing_subline eyebrow footer url cta rail_label',
    'example': 'interval_unit currency_symbol unit network',
    'story.opening': 'headline subline',
    'story.wait': 'line1 line2 count_label timeline_label end_label payoff',
    'story.shift': 'line1 line2 source_label source_note destination_label destination_state status payoff',
    'story.cadence': 'line1 line2 metric_label caption1 caption2 card_label card_footer',
    'story.flow': 'line1 line2 subline source',
    'story.proof': 'line1 line2 subline1 subline2 record_label record_item payoff',
}
PALETTE_KEYS = 'forest dark clay cream sun stone line muted'.split()


def validate_brief(raw):
    """Return the unchanged valid brief, or raise ValueError with a field path."""
    def value(path):
        node = raw
        for part in path.split('.'):
            if not isinstance(node, dict) or part not in node:
                raise ValueError(f'Missing brief field: {path}')
            node = node[part]
        return node

    def text(item, path):
        if not isinstance(item, str) or not item.strip():
            raise ValueError(f'{path} must be a non-empty string')

    if not isinstance(raw, dict):
        raise ValueError('Brief must be a JSON object')
    for group, fields in TEXT_FIELDS.items():
        for field in fields.split():
            path = f'{group}.{field}'
            text(value(path), path)
    for key in PALETTE_KEYS:
        path = f'palette.{key}'
        item = value(path)
        if not isinstance(item, str) or re.fullmatch(r'#[0-9a-fA-F]{6}', item) is None:
            raise ValueError(f'{path} must be a six-digit hex color')
    for field, upper in [('period_days', 14), ('interval_seconds', 3600)]:
        item = value(f'example.{field}')
        if type(item) is not int or not 1 <= item <= upper:
            raise ValueError(f'example.{field} must be an integer in 1..{upper}')
    for field in ['weekly_total', 'starting_amount']:
        item = value(f'example.{field}')
        if isinstance(item, bool) or not isinstance(item, (int, float)):
            raise ValueError(f'example.{field} must be a finite nonnegative number')
        try:
            valid = math.isfinite(item) and item >= 0
        except OverflowError:
            valid = False
        if not valid:
            raise ValueError(f'example.{field} must be a finite nonnegative number')
    audiences = value('story.flow.audiences')
    if not isinstance(audiences, list) or len(audiences) != 3:
        raise ValueError('story.flow.audiences must contain three [title, subtitle] pairs')
    for index, pair in enumerate(audiences):
        path = f'story.flow.audiences[{index}]'
        if not isinstance(pair, list) or len(pair) != 2:
            raise ValueError(f'{path} must be a [title, subtitle] pair')
        for index2, item in enumerate(pair):
            text(item, f'{path}[{index2}]')
    verbs = value('story.proof.verbs')
    if not isinstance(verbs, list) or len(verbs) != 3:
        raise ValueError('story.proof.verbs must contain three labels')
    for index, item in enumerate(verbs):
        text(item, f'story.proof.verbs[{index}]')
    if 'monogram' in raw['brand']:
        text(raw['brand']['monogram'], 'brand.monogram')
    return raw


def load_brief(path):
    return validate_brief(json.loads(Path(path).read_text(encoding='utf-8')))
