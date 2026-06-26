from __future__ import annotations

import re
from typing import Any, Dict, List

from .common import load_reference_json


KEYWORDS_MAP = {
    '科技': '科技博主', '数码': '科技博主', 'AI': '科技博主',
    '亲子': '亲子博主', '育儿': '亲子博主', '宝妈': '亲子博主',
    '美妆': '美妆博主', '护肤': '美妆博主', '化妆': '美妆博主',
    '健身': '健身博主', '运动': '健身博主', '减脂': '健身博主',
    '美食': '美食博主', '烹饪': '美食博主', '做菜': '美食博主',
    '学习': '学习博主', '教育': '学习博主', '考研': '学习博主',
    '旅行': '旅行博主', '旅游': '旅行博主',
    '职场': '职场博主', '工作': '职场博主', '办公': '职场博主',
    '漫画': '漫画博主', '动漫': '漫画博主', '二次元': '漫画博主', '国漫': '漫画博主', '番剧': '漫画博主',
    '摄影': '摄影博主', '拍照': '摄影博主',
    '穿搭': '穿搭博主', '时尚': '穿搭博主',
    '游戏': '游戏博主', '电竞': '游戏博主',
    '音乐': '音乐博主', '歌手': '音乐博主',
}


def load_style_presets() -> Dict[str, Any]:
    raw = load_reference_json('style-presets.json', default={}) or {}
    if not isinstance(raw, dict):
        return {}
    preset_value = raw.get('presets')
    if isinstance(preset_value, dict):
        return raw
    if not isinstance(preset_value, list):
        return raw
    preset_map: Dict[str, Any] = {}
    for item in preset_value:
        if not isinstance(item, dict):
            continue
        account_type = str(item.get('style') or '').strip()
        if not account_type:
            continue
        content_length = item.get('content_length') if isinstance(item.get('content_length'), dict) else {}
        emojis = item.get('emoji')
        emoji_value = emojis[0] if isinstance(emojis, list) and emojis else item.get('emoji')
        colors = item.get('colors')
        color_value = '、'.join([str(c) for c in colors[:3]]) if isinstance(colors, list) and colors else item.get('colors')
        preset_map[account_type] = {
            'style': account_type,
            'colors': str(color_value or '干净、统一、适合图文阅读'),
            'tone': str(item.get('tone') or '自然、真诚、口语化'),
            'emoji': str(emoji_value or '✨'),
            'content_min': int(content_length.get('min', 35)) if isinstance(content_length, dict) else 35,
            'content_max': int(content_length.get('max', 70)) if isinstance(content_length, dict) else 70,
        }
    fallback = raw.get('fallback')
    if not isinstance(fallback, dict):
        fallback = {
            'style': '通用',
            'colors': '干净、统一、适合图文阅读',
            'tone': '自然、真诚、口语化',
            'emoji': '✨',
            'content_min': 35,
            'content_max': 70,
        }
    return {**raw, 'presets': preset_map, 'fallback': fallback}



def load_hashtag_library() -> Dict[str, Any]:
    return load_reference_json('hashtag-library.json', default={}) or {}



def match_style_preset(account_type: str, presets: Dict[str, Any]) -> Dict[str, Any]:
    account_type = (account_type or '').strip()
    preset_map = presets.get('presets', {}) if isinstance(presets, dict) else {}
    fallback = presets.get('fallback', {}) if isinstance(presets, dict) else {}

    if account_type in preset_map:
        return preset_map[account_type]

    lowered = account_type.lower()
    for keyword, mapped in KEYWORDS_MAP.items():
        if keyword.lower() in lowered and mapped in preset_map:
            return preset_map[mapped]

    return fallback



def recommend_hashtags(topic: str, content_direction: str, target_audience: str, limit: int = 10) -> List[str]:
    library = load_hashtag_library()
    candidates: List[str] = []
    lookup_text = ' '.join(filter(None, [topic, content_direction, target_audience]))

    if isinstance(library, dict):
        for key, value in library.items():
            if key in lookup_text and isinstance(value, list):
                candidates.extend([str(v).strip() for v in value if str(v).strip()])

    if not candidates:
        words = [w for w in re.split(r'[\s,，、/]+', lookup_text) if w]
        candidates.extend([f'#{w}' if not w.startswith('#') else w for w in words[:limit]])

    seen = set()
    result: List[str] = []
    for tag in candidates:
        normalized = tag if tag.startswith('#') else f'#{tag}'
        if normalized not in seen:
            seen.add(normalized)
            result.append(normalized)
        if len(result) >= limit:
            break
    return result
