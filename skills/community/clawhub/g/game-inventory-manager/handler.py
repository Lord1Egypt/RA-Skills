#!/usr/bin/env python3
import json
import os
import re
from typing import Any, Dict, List, Tuple

SKILL_SLUG = 'game-inventory-manager'
PROMPT_TEMPLATE = """Sort the user's clutter like a game inventory.
Classify items into equipped, quick access, storage, sell or delegate, discard or archive, and craft or combine. Explain the logic and end with one cleanup move that fits inside 10 to 20 minutes."""

CATEGORY_LABELS = [
    ('equip', 'Equipped Now', 'High current value or direct support for active goals.'),
    ('quick', 'Quick Access', 'Useful often enough to keep near the surface.'),
    ('storage', 'Storage', 'Worth keeping, but not worth active attention right now.'),
    ('sell', 'Sell / Delegate', 'Still has value, but should leave your active backpack.'),
    ('discard', 'Discard / Archive', 'Expired, duplicate, broken, or no longer worth carrying.'),
    ('craft', 'Craft / Combine', 'Fragments that become more valuable if batched or merged.'),
]

KEYWORDS = {
    'discard': ['expired', 'broken', 'duplicate', 'trash', 'stale', 'useless', 'old', 'delete', 'empty', 'outdated'],
    'sell': ['sell', 'donate', 'delegate', 'outsource', 'return', 'swap', 'extra', 'loan'],
    'craft': ['draft', 'note', 'idea', 'receipt', 'snippet', 'fragment', 'batch', 'merge', 'combine', 'outline'],
    'equip': ['daily', 'urgent', 'must', 'current', 'active', 'important', 'health', 'today', 'key', 'passport', 'charger'],
    'quick': ['weekly', 'often', 'favorite', 'routine', 'template', 'reference'],
    'storage': ['seasonal', 'backup', 'archive', 'later', 'someday', 'memory', 'keepsake'],
}


def _load_skill_meta(skill_name):
    path = os.path.join(os.path.dirname(__file__), 'SKILL.md')
    with open(path, 'r', encoding='utf-8') as handle:
        content = handle.read()
    match = re.search(r'^---\s*\n(.*?)\n---\s*', content, re.DOTALL | re.MULTILINE)
    meta = {}
    if match:
        for line in match.group(1).splitlines():
            if ':' in line:
                key, value = line.split(':', 1)
                meta[key.strip()] = value.strip()
    meta['skill_name'] = skill_name or meta.get('name', SKILL_SLUG)
    return meta


def _load_prompt_template(skill_name):
    return PROMPT_TEMPLATE


def _clean_text(value: Any) -> str:
    if value is None:
        return ''
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, (int, float)):
        return str(value)
    return json.dumps(value, ensure_ascii=False)


def _parse_text_map(raw: str) -> Dict[str, str]:
    data: Dict[str, str] = {}
    for line in raw.splitlines():
        if re.search(r'[:：]', line):
            key, value = re.split(r'[:：]', line, maxsplit=1)
            normalized = re.sub(r'\s+', '_', key.strip().lower())
            data[normalized] = value.strip()
    return data


def _coerce_input(user_input: Any) -> Tuple[str, Dict[str, Any]]:
    if isinstance(user_input, dict):
        return json.dumps(user_input, ensure_ascii=False), dict(user_input)
    raw = _clean_text(user_input)
    if raw.startswith('{') and raw.endswith('}'):
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, dict):
                return raw, parsed
        except json.JSONDecodeError:
            pass
    return raw, _parse_text_map(raw)


def _split_items(value: Any) -> List[str]:
    if isinstance(value, list):
        return [_clean_text(item) for item in value if _clean_text(item)]
    text = _clean_text(value)
    if not text:
        return []
    items = [re.sub(r'^[\-•\d.\s]+', '', part).strip() for part in re.split(r'[\n,;，；]+', text)]
    return [item for item in items if item]


def _extract_items(raw: str, data: Dict[str, Any]) -> List[str]:
    for key in ['items', 'objects', 'tasks', 'scope', 'list']:
        if key in data:
            items = _split_items(data[key])
            if items:
                return items
    raw_items = _split_items(raw)
    if raw_items:
        return raw_items
    return ['current obligations', 'stored clutter', 'unfinished fragments']


def _classify_item(item: str) -> Tuple[str, str]:
    lowered = item.lower()
    for category in ['discard', 'sell', 'craft', 'equip', 'quick', 'storage']:
        for word in KEYWORDS[category]:
            if word in lowered:
                if category == 'discard':
                    return category, 'low value, duplicate, expired, or no longer functional'
                if category == 'sell':
                    return category, 'valuable enough to leave through delegation, donation, or sale'
                if category == 'craft':
                    return category, 'fragmented material that becomes better when merged into one batch'
                if category == 'equip':
                    return category, 'actively supports today or a live priority'
                if category == 'quick':
                    return category, 'used often enough to stay near the surface'
                if category == 'storage':
                    return category, 'worth keeping, but not worth active attention right now'
    if len(item.split()) <= 2:
        return 'quick', 'small, reusable item that may deserve easy access'
    return 'storage', 'not urgent enough for active loadout, but not obviously discardable'


def _bucket_items(items: List[str]) -> Dict[str, List[Tuple[str, str]]]:
    buckets: Dict[str, List[Tuple[str, str]]] = {name: [] for name, _, _ in CATEGORY_LABELS}
    for item in items:
        category, reason = _classify_item(item)
        buckets[category].append((item, reason))
    return buckets


def _biggest_load(buckets: Dict[str, List[Tuple[str, str]]]) -> str:
    ordered = sorted(buckets.items(), key=lambda pair: len(pair[1]), reverse=True)
    top_name, top_items = ordered[0]
    label = next(label for name, label, _ in CATEGORY_LABELS if name == top_name)
    return f'{label} ({len(top_items)} item(s))'


def _first_slot_to_clear(buckets: Dict[str, List[Tuple[str, str]]]) -> str:
    priority = ['discard', 'sell', 'craft', 'quick', 'storage', 'equip']
    for category in priority:
        if buckets[category]:
            label = next(label for name, label, _ in CATEGORY_LABELS if name == category)
            target = buckets[category][0][0]
            return f'Start with **{label}** by processing `{target}` first. That unlocks visible relief fastest.'
    return 'Start with the smallest visible category and clear one complete slot.'


def _craft_suggestions(buckets: Dict[str, List[Tuple[str, str]]]) -> List[str]:
    suggestions: List[str] = []
    if len(buckets['craft']) >= 2:
        craft_names = ', '.join(item for item, _ in buckets['craft'][:3])
        suggestions.append(f'Combine fragmented materials into one named batch, for example: {craft_names}.')
    if len(buckets['sell']) >= 2:
        suggestions.append('Create one delegate, donate, or resale batch instead of deciding item by item.')
    if len(buckets['quick']) >= 3:
        suggestions.append('Move truly recurring items into one quick-access list so they stop resurfacing as random reminders.')
    if not suggestions:
        suggestions.append('If no obvious combination exists, create one short “process later” batch so your backpack stops carrying loose fragments.')
    return suggestions


def _cleanup_move(buckets: Dict[str, List[Tuple[str, str]]]) -> str:
    if buckets['discard']:
        return 'Set a 15-minute timer and clear the discard or archive pile completely before touching anything else.'
    if buckets['sell']:
        return 'Spend 15 minutes making one delegate, donate, or resale batch with a single exit plan.'
    if buckets['craft']:
        return 'Use 15 minutes to merge the top fragments into one named checklist, folder, or note.'
    return 'Use 10 minutes to move active items into one visible quick-access slot and park the rest.'


def _build_result(raw: str, data: Dict[str, Any], template: str) -> str:
    items = _extract_items(raw, data)
    buckets = _bucket_items(items)
    friction_candidates = [item for category in ['discard', 'sell', 'craft'] for item, _ in buckets[category]][:3]
    lines: List[str] = []
    lines.append('# Game Inventory Review')
    lines.append('')
    lines.append('## Backpack Status')
    lines.append(f'- Total items reviewed: {len(items)}')
    lines.append(f'- Biggest current load: {_biggest_load(buckets)}')
    lines.append(f'- Sorting frame: {template.splitlines()[0]}')
    if friction_candidates:
        lines.append(f"- Most attention-draining items: {', '.join(friction_candidates)}")
    else:
        lines.append('- Most attention-draining items: No obvious clutter sink was stated, so start with whichever slot feels heaviest.')
    lines.append('')
    lines.append('## Sorted Inventory')
    for name, label, summary in CATEGORY_LABELS:
        lines.append(f'### {label}')
        if buckets[name]:
            for item, reason in buckets[name]:
                lines.append(f'- {item} — {reason}')
        else:
            lines.append('- No clear items in this slot right now.')
        lines.append(f'- Why this slot exists: {summary}')
        lines.append('')
    lines.append('## First Slot to Clear')
    lines.append(f'- {_first_slot_to_clear(buckets)}')
    lines.append('')
    lines.append('## Craft Suggestions')
    for suggestion in _craft_suggestions(buckets):
        lines.append(f'- {suggestion}')
    lines.append('')
    lines.append('## 15-Minute Cleanup Move')
    lines.append(f'- {_cleanup_move(buckets)}')
    return '\n'.join(lines)


def handle(args):
    skill_name = args.get('skill_name', SKILL_SLUG) or SKILL_SLUG
    user_input = args.get('input', '')
    mode = args.get('mode', 'guide')
    meta = _load_skill_meta(skill_name)
    template = _load_prompt_template(skill_name)
    if mode == 'meta':
        return {'result': json.dumps(meta, ensure_ascii=False, indent=2)}
    if mode == 'prompt':
        return {'result': template}
    raw, data = _coerce_input(user_input)
    return {'result': _build_result(raw, data, template)}
