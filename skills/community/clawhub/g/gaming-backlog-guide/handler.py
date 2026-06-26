#!/usr/bin/env python3
import json
import os
import re
from typing import Any, Dict, List, Tuple

SKILL_SLUG = 'gaming-backlog-guide'
PROMPT_TEMPLATE = """Match the user's current mood, time, energy, and platform habits to the right kind of game experience.
Recommend the best-fit directions, separate a play-now option from a weekend option, flag one type to avoid for now, and end with the easiest possible start."""

PROFILES = {
    'low_friction': {
        'label': 'Low-friction decompression',
        'fit': 'Short, low-energy windows where starting matters more than mastery.',
        'entry': 'Choose sessions that reset cleanly in 10 to 30 minutes, such as short runs, puzzle bursts, or bite-size matches.',
        'example_direction': 'short roguelite runs, puzzle slices, racing laps, or quick arcade loops',
        'avoid_when': 'you are hoping for a giant emotional journey tonight but only have scraps of attention',
    },
    'comfort': {
        'label': 'Comfort companion',
        'fit': 'Moments when the user wants something familiar, warm, and emotionally safe.',
        'entry': 'Return to a known world, low-stakes sim, or familiar progression loop that does not need a fresh tutorial.',
        'example_direction': 'cozy management, life sim check-ins, familiar RPG side content, or soft routine games',
        'avoid_when': 'you are clearly bored by your existing habits and need novelty instead of emotional safety',
    },
    'novelty': {
        'label': 'Fresh novelty sampler',
        'fit': 'When the user is bored, stale, or curious and needs a new flavor without a giant commitment.',
        'entry': 'Sample one new genre, demo, short indie, or self-contained first hour before committing to a major campaign.',
        'example_direction': 'demo-first exploration, a short indie experiment, or one unfamiliar genre with a low entry cost',
        'avoid_when': 'the user is exhausted enough that even learning a new control scheme feels expensive',
    },
    'immersion': {
        'label': 'Deep immersion weekend arc',
        'fit': 'Longer windows with enough energy for story, systems, or campaign depth.',
        'entry': 'Open a title that rewards 90 minutes or more, ideally with one clear chapter or objective to finish.',
        'example_direction': 'story RPG arcs, strategy campaigns, long-form survival crafting, or open-world quest blocks',
        'avoid_when': 'the available time is short or the user is already mentally drained',
    },
    'social': {
        'label': 'Shared couch or co-op energy',
        'fit': 'Moments when play is really about connection, not solo optimization.',
        'entry': 'Pick something with quick onboarding, short rounds, and room for conversation or teamwork.',
        'example_direction': 'couch co-op, party co-op, family-friendly challenge runs, or asymmetrical shared play',
        'avoid_when': 'the current mood is private recovery and the user does not want extra coordination',
    },
}


def _load_skill_meta(skill_name: str) -> Dict[str, str]:
    path = os.path.join(os.path.dirname(__file__), 'SKILL.md')
    with open(path, 'r', encoding='utf-8') as handle:
        content = handle.read()
    match = re.search(r'^---\s*\n(.*?)\n---\s*', content, re.DOTALL | re.MULTILINE)
    meta: Dict[str, str] = {}
    if match:
        for line in match.group(1).splitlines():
            if ':' in line:
                key, value = line.split(':', 1)
                meta[key.strip()] = value.strip()
    meta['skill_name'] = skill_name or meta.get('name', SKILL_SLUG)
    return meta


def _load_prompt_template(skill_name: str) -> str:
    del skill_name
    return PROMPT_TEMPLATE


def _normalize_key(key: Any) -> str:
    return re.sub(r'[^a-z0-9_\u4e00-\u9fff]+', '_', str(key).strip().lower()).strip('_')


def _clean_text(value: Any) -> str:
    if value is None:
        return ''
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, (int, float)):
        return str(value)
    return json.dumps(value, ensure_ascii=False)


def _normalize_map(data: Dict[str, Any]) -> Dict[str, Any]:
    return {_normalize_key(key): value for key, value in data.items()}


def _parse_text_map(raw: str) -> Dict[str, Any]:
    data: Dict[str, Any] = {}
    for line in raw.splitlines():
        if re.search(r'[:：]', line):
            key, value = re.split(r'[:：]', line, maxsplit=1)
            data[_normalize_key(key)] = value.strip()
    return data


def _coerce_input(user_input: Any) -> Tuple[str, Dict[str, Any]]:
    if isinstance(user_input, dict):
        return json.dumps(user_input, ensure_ascii=False), _normalize_map(user_input)
    raw = _clean_text(user_input)
    if raw.startswith('{') and raw.endswith('}'):
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, dict):
                return raw, _normalize_map(parsed)
        except json.JSONDecodeError:
            pass
    return raw, _parse_text_map(raw)


def _pick(data: Dict[str, Any], keys: List[str], default: str = '') -> str:
    for key in keys:
        normalized = _normalize_key(key)
        if normalized in data:
            text = _clean_text(data[normalized])
            if text:
                return text
    return default


def _to_int(value: Any, default: int = 0) -> int:
    if isinstance(value, int):
        return value
    text = _clean_text(value)
    match = re.search(r'(\d+)', text)
    return int(match.group(1)) if match else default


def _contains_any(text: str, keywords: List[str]) -> bool:
    lowered = text.lower()
    return any(word in lowered for word in keywords)


def _score_profiles(raw: str, data: Dict[str, Any]) -> Tuple[Dict[str, int], int, str, str, str]:
    mood = _pick(data, ['mood', 'energy', 'emotion', '心情'])
    time_text = _pick(data, ['time', 'minutes', 'available_time', '空闲时间'])
    platform = _pick(data, ['platform', 'device', '平台'], 'not specified')
    budget = _pick(data, ['budget', 'price_limit', '预算'], 'not specified')
    recent = _pick(data, ['recent_games', 'recent_types', 'genres', '最近在玩'])
    desired = _pick(data, ['desired_experience', 'want', 'goal', '想要的体验'])
    together = _pick(data, ['with_whom', 'co_op', 'group', '一起玩'])
    minutes = _to_int(time_text, 0)
    context = ' '.join([raw, mood, platform, budget, recent, desired, together]).lower()

    scores = {name: 0 for name in PROFILES}
    if minutes:
        if minutes <= 30:
            scores['low_friction'] += 5
            scores['comfort'] += 2
            scores['immersion'] -= 2
        elif minutes <= 90:
            scores['comfort'] += 2
            scores['novelty'] += 2
        else:
            scores['immersion'] += 5
            scores['comfort'] += 1
    if _contains_any(context, ['tired', 'drained', 'low energy', 'decompress', 'unwind', '疲惫', '放松']):
        scores['low_friction'] += 4
        scores['comfort'] += 2
        scores['immersion'] -= 1
    if _contains_any(context, ['cozy', 'warm', 'familiar', 'safe', 'comfort', '治愈', '熟悉']):
        scores['comfort'] += 4
    if _contains_any(context, ['bored', 'stale', 'fresh', 'new', 'curious', 'novelty', '腻了', '新鲜感']):
        scores['novelty'] += 4
    if _contains_any(context, ['story', 'immersive', 'epic', 'campaign', 'deep', '沉浸', '主线']):
        scores['immersion'] += 4
    if _contains_any(context, ['friend', 'family', 'partner', 'co-op', 'coop', 'couch', 'together', '亲子', '一起']):
        scores['social'] += 5
    if _contains_any(context, ['budget', 'cheap', 'free', 'backlog', 'already own', '低成本', '库存']) or 'low' in budget.lower():
        scores['comfort'] += 1
        scores['novelty'] += 1
    if all(score == 0 for score in scores.values()):
        scores['comfort'] = 2
        scores['low_friction'] = 1

    return scores, minutes, platform, budget, recent or 'not specified'


def _rank_profiles(scores: Dict[str, int]) -> List[Tuple[str, int]]:
    return sorted(scores.items(), key=lambda item: (item[1], PROFILES[item[0]]['label']), reverse=True)


def _tonight_start(profile_id: str, minutes: int, budget: str) -> str:
    if profile_id == 'low_friction':
        return 'Pick something you can launch in under 2 minutes and finish or pause cleanly inside one short sitting.'
    if profile_id == 'comfort':
        return 'Reopen a familiar save or a known cozy loop so the first five minutes feel frictionless.'
    if profile_id == 'novelty':
        return 'Try one demo, one short indie, or one new genre sample, but cap the experiment at the first 30 to 45 minutes.'
    if profile_id == 'immersion':
        return 'Open the campaign only if you can protect a real block of time and stop after one chapter or objective.'
    note = 'Keep setup and explanation light so the social energy goes into play instead of logistics.'
    if 'low' in budget.lower() or 'not specified' in budget.lower():
        note += ' Prefer something already in the library or available at low cost.'
    return note


def _build_result(raw: str, data: Dict[str, Any], template: str) -> str:
    scores, minutes, platform, budget, recent = _score_profiles(raw, data)
    ranked = _rank_profiles(scores)
    top_ids = [item[0] for item in ranked[:3]]
    avoid_id = ranked[-1][0]
    play_now = top_ids[0]
    weekend = next((profile_id for profile_id in top_ids if profile_id == 'immersion'), top_ids[1] if len(top_ids) > 1 else top_ids[0])

    lines: List[str] = []
    lines.append('# Gaming Backlog Match')
    lines.append('')
    lines.append('## Current Need Profile')
    lines.append(f'- Platform read: {platform}')
    if minutes:
        lines.append(f'- Available time: about {minutes} minutes')
    else:
        lines.append('- Available time: not fully specified, so the guide defaults to lower-friction choices first.')
    lines.append(f'- Budget pressure: {budget}')
    lines.append(f'- Recent pattern: {recent}')
    lines.append(f"- Decision frame: {template.splitlines()[0]}")
    lines.append('')
    lines.append('## Best-Fit Directions')
    for index, profile_id in enumerate(top_ids, start=1):
        profile = PROFILES[profile_id]
        lines.append(f"### {index}. {profile['label']}")
        lines.append(f"- Why it fits: {profile['fit']}")
        lines.append(f"- Entry advice: {profile['entry']}")
        lines.append(f"- Example direction: {profile['example_direction']}")
        lines.append('')
    lines.append('## Start Here')
    lines.append(f"- Play now: {PROFILES[play_now]['label']} — {_tonight_start(play_now, minutes, budget)}")
    lines.append(f"- Weekend slot: {PROFILES[weekend]['label']} — {PROFILES[weekend]['entry']}")
    if 'low' in budget.lower() or 'tight' in budget.lower() or 'not specified' in budget.lower():
        lines.append('- Budget note: start with backlog, free, or already-owned options before adding purchase pressure.')
    else:
        lines.append('- Budget note: still prefer the experience match first, then decide whether new spending is justified.')
    lines.append('')
    lines.append('## Avoid for Now')
    lines.append(f"- {PROFILES[avoid_id]['label']} — avoid this if {PROFILES[avoid_id]['avoid_when']}.")
    lines.append('')
    lines.append("## Tonight's Easiest Start")
    lines.append(f"- {_tonight_start(play_now, minutes, budget)}")
    return '\n'.join(lines)


def handle(args: Dict[str, Any]) -> Dict[str, str]:
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


if __name__ == '__main__':
    demo = {
        'mood': 'tired and want to decompress',
        'time': 25,
        'platform': 'Switch',
        'budget': 'low',
        'recent_types': 'long RPGs',
    }
    print(json.dumps(handle({'skill_name': SKILL_SLUG, 'input': demo}), ensure_ascii=False, indent=2))
