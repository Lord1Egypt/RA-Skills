#!/usr/bin/env python3
import json
import os
import re
from typing import Any, Dict, Sequence, Tuple


def _load_skill_meta(slug):
    path = os.path.join(os.path.dirname(__file__), 'SKILL.md')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    meta = re.search(r'^---$(.*?)^---$', content, re.DOTALL | re.MULTILINE)
    return meta.group(1).strip() if meta else ''


def _normalize_inputs(inputs: Any) -> str:
    if inputs is None:
        return ''
    if isinstance(inputs, str):
        return inputs.strip()
    if isinstance(inputs, dict):
        parts = []
        for key, value in inputs.items():
            if value in (None, '', [], {}, ()):  # type: ignore[comparison-overlap]
                continue
            if isinstance(value, (list, tuple, set)):
                rendered = ', '.join(str(item) for item in value)
            else:
                rendered = str(value)
            parts.append(f"{key}: {rendered}")
        return ' | '.join(parts)
    if isinstance(inputs, (list, tuple, set)):
        return ' | '.join(str(item) for item in inputs)
    try:
        return json.dumps(inputs, ensure_ascii=False, sort_keys=True)
    except TypeError:
        return str(inputs)


def _coerce_dict(inputs: Any) -> Dict[str, Any]:
    return inputs if isinstance(inputs, dict) else {}


def _pick_text(data: Dict[str, Any], keys: Sequence[str], default: str = '') -> str:
    for key in keys:
        value = data.get(key)
        if value is None:
            continue
        text = str(value).strip()
        if text:
            return text
    return default


def _detect_one(text: str, rules: Dict[str, Sequence[str]], default: str) -> str:
    lower = text.lower()
    for label, keywords in rules.items():
        if any(keyword in lower for keyword in keywords):
            return label
    return default


PURPOSE_RULES = {
    'Rest': ['rest', 'tired', 'exhausted', 'overstimulated', 'quiet', 'need a break'],
    'Clarity': ['clarity', 'decision', 'think', 'clear my head', 'mental clutter', 'brain fog'],
    'Play': ['play', 'fun', 'joy', 'lightness', 'explore'],
    'Recovery': ['recover', 'healing', 'burnout', 'after conflict', 'tender'],
    'Creative space': ['create', 'write', 'draw', 'sketch', 'idea', 'deep work', 'project'],
}

ENERGY_RULES = {
    'Low': ['tired', 'drained', 'overwhelmed', 'burned out', 'burnt out'],
    'High': ['energized', 'curious', 'restless', 'ready'],
}


def _extract_duration(data: Dict[str, Any], raw: str) -> str:
    explicit = _pick_text(data, ['available_time', 'time', 'duration'])
    if explicit:
        return explicit
    lowered = raw.lower()
    match = re.search(r'(\d+)\s*(minutes?|mins?|hours?)', lowered)
    if match:
        unit = match.group(2)
        if unit.startswith('hour'):
            return f"{match.group(1)} hour" + ('' if match.group(1) == '1' else 's')
        return f"{match.group(1)} minutes"
    return '30 minutes'


def _default_location(purpose: str) -> str:
    return {
        'Rest': 'A quiet room, shaded bench, or another low-stimulation place',
        'Clarity': 'A walkable route or a table with a notebook and no chatter',
        'Play': 'A light, low-pressure place that feels a little fresh',
        'Recovery': 'A protected, gentle space where you do not need to perform',
        'Creative space': 'A desk, library table, studio corner, or café with minimal interruption',
    }[purpose]


def _activity_palette(purpose: str) -> Tuple[str, str, str]:
    palettes = {
        'Rest': (
            'Tea, stretching, closed-eye rest, or lying down without input',
            'A slow walk or a few pages of quiet reading without multitasking',
            'Ten minutes of silence and breathing before writing one simple line about what you need',
        ),
        'Clarity': (
            'A brain-dump list of everything crowding your mind',
            'A solo walk with one question and no podcast',
            'Sit with one notebook page and ask what matters most right now',
        ),
        'Play': (
            'Flip through an art book, playlist, or playful prompt',
            'Sketch, doodle, wander, or make something with no outcome pressure',
            'Let yourself explore one small curiosity without turning it into a project',
        ),
        'Recovery': (
            'Warm tea, gentle stretching, or sitting somewhere soft and quiet',
            'A slow walk, soothing music, or a very light tidy reset',
            'A full protected block with no obligation except settling your nervous system',
        ),
        'Creative space': (
            'Freewrite or sketch fragments without judging them',
            'Read a few pages, collect notes, or outline one idea thread',
            'One uninterrupted making block with the phone out of reach',
        ),
    }
    return palettes[purpose]


def handle(inputs):
    meta = _load_skill_meta('skill')
    data = _coerce_dict(inputs)
    raw = _normalize_inputs(inputs)

    purpose = _pick_text(data, ['purpose', 'need'], _detect_one(raw, PURPOSE_RULES, 'Clarity'))
    energy = _pick_text(data, ['energy_level', 'energy'], _detect_one(raw, ENERGY_RULES, 'Medium'))
    available_time = _extract_duration(data, raw)
    location = _pick_text(data, ['location'], _default_location(purpose))
    phone_rule = _pick_text(
        data,
        ['phone_rule'],
        'Put the phone on Do Not Disturb, keep it out of reach, and only check it at the planned end of the block.',
    )
    interruptions_rule = _pick_text(
        data,
        ['interruptions_rule'],
        'Only break the block for genuine emergencies; everything else can wait until re-entry.',
    )
    low, medium, high = _activity_palette(purpose)
    if energy == 'Low':
        medium = 'Keep the medium option gentle: a slow walk, easy reading, or a notebook check-in with no pressure.'

    notice_after = {
        'Rest': 'Notice whether your body feels softer, slower, or less defended.',
        'Clarity': 'Notice whether the next step feels more obvious than it did before the block.',
        'Play': 'Notice whether you feel lighter, more curious, or less heavy.',
        'Recovery': 'Notice whether the solitude calmed you rather than numbed you out.',
        'Creative space': 'Notice whether one idea thread feels alive enough to continue later.',
    }[purpose]
    return_to_day = 'Take two slower breaths, name one sentence about what helped, and choose one simple next action before rejoining people or tasks.'

    return f"""# Alone Time Blueprint
## Purpose
- What I need from this solitude: {purpose}
- Available time: {available_time}

## Boundaries
- Location: {location}
- Phone rule: {phone_rule}
- Interruptions rule: {interruptions_rule}

## Activity Palette
- Low-energy option: {low}
- Medium-energy option: {medium}
- High-presence option: {high}

## Re-entry
- How I will return to the day: {return_to_day}
- What to notice after: {notice_after}
"""
