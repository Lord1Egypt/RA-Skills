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

PURPOSE_RULES = {
'Setting a boundary': ['boundary', 'stop', 'too much', 'late at night', 'need space', 'not okay'],
'Requesting a change': ['ask', 'request', 'need you to', 'can we', 'change'],
'Repairing': ['repair', 'apologize', 'sorry', 'reconnect', 'fix this'],
'Informing clearly': ['tell', 'inform', 'update', 'let you know'],
}

RELATION_RULES = {
'Manager or coworker': ['boss', 'manager', 'coworker', 'colleague', 'team'],
'Partner': ['partner', 'husband', 'wife', 'girlfriend', 'boyfriend', 'spouse'],
'Parent or family member': ['parent', 'mom', 'dad', 'family', 'relative'],
'Friend': ['friend', 'buddy'],
}

SAFETY_KEYWORDS = ['abuse', 'unsafe', 'threat', 'violence', 'coercion']


def _purpose(text: str) -> str:
    return _detect_one(text, PURPOSE_RULES, 'Informing clearly')


def _relationship(text: str) -> str:
    return _detect_one(text, RELATION_RULES, 'Important relationship')


def _default_outcome(purpose: str) -> str:
    mapping = {
        'Setting a boundary': 'A clear limit is heard and the next expectation is explicit.',
        'Requesting a change': 'The other person understands the request and the next step is concrete.',
        'Repairing': 'The conversation moves toward repair without erasing accountability.',
        'Informing clearly': 'The message is delivered directly, with less guessing and less over-explaining.',
    }
    return mapping.get(purpose, 'The message lands clearly and calmly.')


def _opening_line(purpose: str, key_message: str) -> str:
    if purpose == 'Setting a boundary':
        return f'I want to say this clearly because it matters: {key_message}. Going forward, I need a different pattern.'
    if purpose == 'Requesting a change':
        return f'I want to talk about one specific change that would help: {key_message}.'
    if purpose == 'Repairing':
        return f'I want to own my part and say this clearly: {key_message}. I care more about repair than winning the point.'
    return f'I want to say this directly so there is less guessing between us: {key_message}.'


def _responses(purpose: str) -> List[Dict[str, str]]:
    base = [
        {
            'if_they_say': 'You are overreacting.',
            'reply': 'You may see it differently, and I still need to be clear about the impact on me.',
        },
        {
            'if_they_say': 'I did not mean it that way.',
            'reply': 'I hear that, and I am talking about the effect and the change I need now.',
        },
        {
            'if_they_say': 'Let us do this later.',
            'reply': 'If now is not workable, let us set a specific time so it does not drift.',
        },
    ]
    if purpose == 'Repairing':
        base[0] = {
            'if_they_say': 'I am still hurt.',
            'reply': 'I understand that, and I am not asking you to skip the impact. I want to understand it and repair what I can.',
        }
    if purpose == 'Requesting a change':
        base[1] = {
            'if_they_say': 'This is just how I do things.',
            'reply': 'I hear that it is familiar, and I am still asking for a different pattern going forward.',
        }
    return base


def _boundary_focus(purpose: str) -> str:
    if purpose == 'Setting a boundary':
        return 'Whether the limit is allowed to stay in place.'
    if purpose == 'Repairing':
        return 'A circular argument about intentions with no ownership or next step.'
    return 'Repeating the same point without moving toward a decision or next step.'


def _boundary_sentence(purpose: str) -> str:
    if purpose == 'Setting a boundary':
        return 'I am willing to discuss next steps, but I am not willing to keep discussing whether this boundary should exist.'
    if purpose == 'Repairing':
        return 'I am open to repair, and I am not willing to keep turning this into a fight about who is more wrong.'
    return 'I am happy to keep this respectful, and I am not going to keep circling the same argument.'


def _close_line(purpose: str) -> str:
    if purpose == 'Requesting a change':
        return 'Thanks for hearing me. The next thing I want is one concrete agreement about what changes after this conversation.'
    if purpose == 'Repairing':
        return 'Thank you for staying in this. I would like us to leave with one repair step or one follow-up time.'
    return 'Thank you for hearing me. I wanted to be clear, and I want the next step to match what we just discussed.'


def handle(inputs):
    meta = _load_skill_meta('difficult-conversation-rehearser')
    data = _coerce_dict(inputs)
    text = _normalize_inputs(inputs)
    key_message = _pick_text(data, ['message', 'what_i_need_to_say', 'issue', 'topic'], _shorten(text, 140) or 'Say the important thing clearly and briefly.')
    purpose = _pick_text(data, ['purpose', 'goal'], _purpose(text))
    relationship = _pick_text(data, ['relationship', 'person'], _relationship(text))
    outcome = _pick_text(data, ['outcome', 'desired_outcome'], _default_outcome(purpose))
    responses = _responses(purpose)
    note = ''
    if any(keyword in text.lower() for keyword in SAFETY_KEYWORDS):
        note = 'If safety, threats, or coercion are involved, prioritize support, documentation, and protection over rehearsal alone.'

    lines: List[str] = []
    lines.append('# Conversation Rehearsal Brief')
    lines.append('')
    if note:
        lines.append(f'> {note}')
        lines.append('')
    lines.append('## Purpose')
    lines.append(f'- What I need to say: {key_message}')
    lines.append(f'- What outcome I want: {outcome}')
    lines.append(f'- Conversation goal: {purpose}')
    lines.append(f'- Relationship context: {relationship}')
    lines.append('')
    lines.append('## Opening')
    lines.append(f'- {_opening_line(purpose, key_message)}')
    lines.append('')
    lines.append('## Likely Responses and My Replies')
    for idx, item in enumerate(responses[:3], 1):
        lines.append(f'{idx}. If they say: {item["if_they_say"]}')
        lines.append(f'   - I can reply: {item["reply"]}')
    lines.append('')
    lines.append('## Boundaries')
    lines.append(f'- What I will not keep debating: {_boundary_focus(purpose)}')
    lines.append(f'- My boundary sentence: {_boundary_sentence(purpose)}')
    lines.append('')
    lines.append('## Close')
    lines.append(f'- How I will end the conversation: {_close_line(purpose)}')
    return '\n'.join(lines)

if __name__ == "__main__":
    payload = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    print(handle(payload))
