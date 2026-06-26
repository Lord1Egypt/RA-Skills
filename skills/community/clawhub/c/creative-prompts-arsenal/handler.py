#!/usr/bin/env python3
import json
import os
import re
import sys
from typing import Any, Dict, List, Sequence


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
        parts: List[str] = []
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
        if isinstance(value, (list, tuple, set)):
            text = ', '.join(str(item) for item in value if str(item).strip())
        else:
            text = str(value).strip()
        if text:
            return text
    return default


def _listify(value: Any) -> List[str]:
    if value in (None, '', [], {}, ()):  # type: ignore[comparison-overlap]
        return []
    if isinstance(value, str):
        clean = value.replace(';', '\n').replace(',', '\n')
        return [chunk.strip() for chunk in clean.splitlines() if chunk.strip()]
    if isinstance(value, (list, tuple, set)):
        return [str(item).strip() for item in value if str(item).strip()]
    return [str(value).strip()]


def _detect_one(text: str, rules: Dict[str, Sequence[str]], default: str) -> str:
    lower = text.lower()
    for label, keywords in rules.items():
        if any(keyword in lower for keyword in keywords):
            return label
    return default


def _detect_many(text: str, rules: Dict[str, Sequence[str]], default: List[str], limit: int = 4) -> List[str]:
    lower = text.lower()
    found = [label for label, keywords in rules.items() if any(keyword in lower for keyword in keywords)]
    ordered: List[str] = []
    for item in found + default:
        if item not in ordered:
            ordered.append(item)
    return ordered[:limit]


def _shorten(text: str, limit: int = 140) -> str:
    clean = ' '.join(text.split())
    if len(clean) <= limit:
        return clean
    return clean[: limit - 3].rstrip() + '...'

DOMAIN_RULES = {
'Writing': ['write', 'essay', 'article', 'story', 'book', 'blog', 'newsletter', 'script'],
'Design': ['design', 'ui', 'ux', 'layout', 'brand', 'logo', 'poster', 'visual'],
'Parenting': ['parent', 'child', 'kid', 'family activity', 'homeschool'],
'Teaching': ['teach', 'lesson', 'class', 'student', 'curriculum', 'workshop'],
'Business': ['business', 'offer', 'marketing', 'campaign', 'product', 'sales', 'service'],
}

STUCKNESS_RULES = {
'Blank page': ['blank page', 'stuck', 'start', 'nothing', 'empty', 'first line'],
'Too many ideas': ['too many ideas', 'too many directions', 'too many options', 'scattered'],
'Weak direction': ['direction', 'unclear', 'not sure where to go', 'weak idea'],
'Stale style': ['stale', 'same', 'boring', 'flat', 'predictable'],
'Fear of judgment': ['judged', 'cringe', 'embarrassed', 'not good enough', 'fear'],
}

DOMAIN_FRAMES = {
'Writing': {'artifact': 'piece', 'audience': 'reader', 'raw_material': 'scene, argument, or paragraph'},
'Design': {'artifact': 'concept', 'audience': 'user', 'raw_material': 'layout, flow, or visual system'},
'Parenting': {'artifact': 'idea', 'audience': 'child or family', 'raw_material': 'routine, activity, or conversation'},
'Teaching': {'artifact': 'lesson', 'audience': 'student', 'raw_material': 'example, explanation, or activity'},
'Business': {'artifact': 'offer', 'audience': 'customer or team', 'raw_material': 'message, test, or customer problem'},
'General': {'artifact': 'project', 'audience': 'intended audience', 'raw_material': 'core material'},
}


def _context_text(data: Dict[str, Any], text: str) -> str:
    return _pick_text(data, ['project', 'topic', 'idea', 'brief', 'context'], _shorten(text, 100) or 'this project')


def _prompt_sets(domain: str, stuckness: str, context: str) -> Dict[str, List[str]]:
    frame = DOMAIN_FRAMES.get(domain, DOMAIN_FRAMES['General'])
    artifact = frame['artifact']
    audience = frame['audience']
    raw_material = frame['raw_material']
    return {
        'Expand': [
            f'List 10 possible angles for {context} without judging them yet.',
            f'What would make this {artifact} 20% more vivid, useful, or surprising for the {audience}?',
        ],
        'Invert': [
            f'If the obvious approach is wrong, what opposite move would you try with the {raw_material}?',
            f'What would you remove, mute, or simplify so the core of {context} becomes easier to feel?',
        ],
        'Remix': [
            f'Borrow one pattern from an unrelated field and apply it to this {artifact}.',
            f'Reframe {context} for a completely different audience, age group, or setting, then steal one useful insight back.',
        ],
        'Refine': [
            f'Choose one promising direction and state the single effect it should create for the {audience}.',
            f'Name the next draft, sketch, or test you can finish in 15 minutes.',
        ],
    }


def _best_first_prompt(stuckness: str, prompts: Dict[str, List[str]]) -> Dict[str, str]:
    if stuckness == 'Blank page':
        return {
            'prompt': prompts['Expand'][0],
            'why': 'It removes the pressure to be good and replaces it with immediate motion.',
        }
    if stuckness == 'Too many ideas':
        return {
            'prompt': prompts['Refine'][0],
            'why': 'It narrows the field so the best direction becomes easier to test.',
        }
    if stuckness == 'Stale style':
        return {
            'prompt': prompts['Remix'][0],
            'why': 'A fresh borrowed pattern often breaks sameness faster than more polishing.',
        }
    if stuckness == 'Fear of judgment':
        return {
            'prompt': prompts['Expand'][0],
            'why': 'Quantity lowers the stakes and helps you move before your inner critic takes over.',
        }
    return {
        'prompt': prompts['Invert'][0],
        'why': 'A clean perspective shift usually restores direction when the problem feels muddy.',
    }


def handle(inputs):
    meta = _load_skill_meta('creative-prompts-arsenal')
    data = _coerce_dict(inputs)
    text = _normalize_inputs(inputs)
    domain = _pick_text(data, ['domain'], _detect_one(text, DOMAIN_RULES, 'General'))
    stuckness = _pick_text(data, ['stuckness', 'block', 'what_feels_stuck'], _detect_one(text, STUCKNESS_RULES, 'Weak direction'))
    context = _context_text(data, text)
    prompts = _prompt_sets(domain, stuckness, context)
    best = _best_first_prompt(stuckness, prompts)

    lines: List[str] = []
    lines.append('# Creative Prompt Kit')
    lines.append('')
    lines.append('## Context')
    lines.append(f'- Domain: {domain}')
    lines.append(f'- What feels stuck: {stuckness}')
    lines.append('')
    lines.append('## Prompt Set')
    for section in ['Expand', 'Invert', 'Remix', 'Refine']:
        lines.append(f'### {section}')
        for idx, prompt in enumerate(prompts[section], 1):
            lines.append(f'{idx}. {prompt}')
        lines.append('')
    lines.append('## Best First Prompt')
    lines.append(f'- Start with: {best["prompt"]}')
    lines.append(f'- Why this one first: {best["why"]}')
    lines.append('- Suggested order: Expand -> Invert -> Remix -> Refine')
    return '\n'.join(lines)

if __name__ == "__main__":
    payload = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    print(handle(payload))
