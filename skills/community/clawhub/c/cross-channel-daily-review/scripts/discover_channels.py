#!/usr/bin/env python3
import argparse
import glob
import json
import re
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

CHANNEL_PATTERNS = {
    'telegram': [r'"channel"\s*:\s*"telegram"', r'"chat_id"\s*:\s*"telegram:[^"]+"', r'"to"\s*:\s*"telegram:[^"]+"', r'agent:main:telegram:(direct|group|thread):'],
    'feishu': [r'"channel"\s*:\s*"feishu"', r'"chat_id"\s*:\s*"feishu:[^"]+"', r'"to"\s*:\s*"feishu:[^"]+"', r'agent:main:feishu:(direct|group|thread):'],
    'qq': [r'"channel"\s*:\s*"qqbot"', r'"chat_id"\s*:\s*"qqbot:[^"]+"', r'"to"\s*:\s*"qqbot:[^"]+"', r'agent:main:qqbot:(direct|group|thread):'],
    'web': [r'"channel"\s*:\s*"web"', r'"surface"\s*:\s*"web"', r'"chat_id"\s*:\s*"web:[^"]+"'],
    'discord': [r'"channel"\s*:\s*"discord"', r'"chat_id"\s*:\s*"discord:[^"]+"', r'"to"\s*:\s*"discord:[^"]+"', r'agent:main:discord:(direct|group|thread):'],
    'slack': [r'"channel"\s*:\s*"slack"', r'"chat_id"\s*:\s*"slack:[^"]+"', r'"to"\s*:\s*"slack:[^"]+"', r'agent:main:slack:(direct|group|thread):'],
}
LABELS = {
    'telegram': 'Telegram', 'feishu': 'Feishu', 'qq': 'QQ', 'web': 'Web', 'discord': 'Discord', 'slack': 'Slack'
}
SCOPE_PATTERNS = {
    'telegram': [r'(agent:main:telegram:(direct|group|thread):[^\s"`]+)', r'(telegram:[^\s"`]+)'],
    'feishu': [r'(agent:main:feishu:(direct|group|thread):[^\s"`]+)', r'(ou_[A-Za-z0-9_]+)'],
    'qq': [r'(agent:main:qqbot:(direct|group|thread):[^\s"`]+)', r'(qqbot:(?:c2c|group):[^\s"`]+)'],
    'web': [r'(web:[^\s"`]+)'],
    'discord': [r'(agent:main:discord:(direct|group|thread):[^\s"`]+)', r'(discord:[^\s"`]+)'],
    'slack': [r'(agent:main:slack:(direct|group|thread):[^\s"`]+)', r'(slack:[^\s"`]+)'],
}


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--sessions-dir', required=True)
    p.add_argument('--date', required=True)
    p.add_argument('--window-hours', type=int, default=24)
    p.add_argument('--expected', default='web,telegram,feishu,qq')
    p.add_argument('--sessions-list-json')
    p.add_argument('--output', required=True)
    return p.parse_args()


def file_mtime_in_window(path: str, start_ts: float):
    try:
        return Path(path).stat().st_mtime >= start_ts
    except FileNotFoundError:
        return False


def uniq_keep_order(items):
    out = []
    seen = set()
    for x in items:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def scope_type_from_ref(ref: str) -> str:
    if ':direct:' in ref or ':c2c:' in ref or ref.startswith('telegram:'):
        return 'dm'
    if ':group:' in ref:
        return 'group'
    if ':thread:' in ref:
        return 'thread'
    if ref.startswith('ou_'):
        return 'dm'
    return 'unknown'


def participant_shape(scope_type: str, bot_count: int, session_count: int) -> str:
    if bot_count > 1:
        return 'multi-bot-scope'
    if scope_type == 'group' and session_count > 1:
        return 'workflow-group'
    if scope_type == 'dm' and bot_count == 1:
        return 'single-bot-dm'
    if scope_type == 'thread' and session_count > 1:
        return 'thread-workflow'
    return 'unknown'


def bot_count_for_channel(channel: str, session_count: int, scopes_count: int) -> int:
    if scopes_count <= 0:
        return 0
    if session_count > 1 and scopes_count > 1:
        return min(scopes_count, session_count)
    return 1


def collect_from_sessions_list(path: str, expected: list[str]):
    found = defaultdict(list)
    scopes = defaultdict(list)
    if not path:
        return found, scopes
    p = Path(path)
    if not p.exists():
        return found, scopes
    payload = json.loads(p.read_text(encoding='utf-8'))
    sessions = payload.get('sessions') or []
    for sess in sessions:
        ch = (sess.get('channel') or sess.get('deliveryContext', {}).get('channel') or sess.get('lastChannel') or '').strip().lower()
        if ch == 'qqbot':
            ch = 'qq'
        if ch in expected:
            ref = sess.get('transcriptPath') or sess.get('key') or sess.get('sessionId') or 'sessions_list'
            found[ch].append(ref)
            scope = sess.get('lastTo') or sess.get('deliveryContext', {}).get('to') or sess.get('key') or sess.get('sessionId')
            if scope:
                scopes[ch].append(scope)
    return found, scopes


def collect_from_transcripts(sessions_dir: str, start_ts: float, expected: list[str]):
    found = defaultdict(list)
    scopes = defaultdict(list)
    files = glob.glob(str(Path(sessions_dir) / '*.jsonl'))
    for path in files:
        if not file_mtime_in_window(path, start_ts):
            continue
        try:
            text = Path(path).read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue
        for channel in expected:
            patterns = CHANNEL_PATTERNS.get(channel, [])
            if any(re.search(p, text, re.I) for p in patterns):
                found[channel].append(path)
                for sp in SCOPE_PATTERNS.get(channel, []):
                    m = re.search(sp, text, re.I)
                    if m:
                        scopes[channel].append(m.group(1))
                        break
    return found, scopes


def main() -> int:
    args = parse_args()
    end = datetime.fromisoformat(args.date + 'T23:59:59+08:00')
    start = end - timedelta(hours=args.window_hours)
    start_ts = start.timestamp()
    expected = [x.strip().lower() for x in args.expected.split(',') if x.strip()]

    found_meta, scopes_meta = collect_from_sessions_list(args.sessions_list_json, expected)
    found_text, scopes_text = collect_from_transcripts(args.sessions_dir, start_ts, expected)

    results = []
    for channel in expected:
        refs_meta = found_meta.get(channel, [])
        refs_text = found_text.get(channel, [])
        refs = uniq_keep_order(refs_meta + refs_text)[:5]
        scopes = uniq_keep_order(scopes_meta.get(channel, []) + scopes_text.get(channel, []))
        primary_scope = scopes[0] if scopes else f'{channel}:unknown'
        scope_type = scope_type_from_ref(primary_scope)
        session_count = len(refs)
        bots = bot_count_for_channel(channel, session_count, len(scopes))
        pshape = participant_shape(scope_type, bots, session_count)

        status = 'active' if refs_meta else ('configured' if refs_text else 'missing')
        if status == 'active':
            summary = f'基于 sessions_list 元数据确认 {len(refs_meta)} 个相关会话，识别到 {len(scopes)} 个 scope'
            note_mode = 'discovery_mode=sessions_metadata+transcript_fallback'
            missing_reason = ''
        elif status == 'configured':
            summary = f'仅从 transcript 结构化痕迹检出 {len(refs_text)} 个候选会话，识别到 {len(scopes)} 个候选 scope，尚未拿到 sessions 元数据确认'
            note_mode = 'discovery_mode=transcript_only_candidate'
            missing_reason = '发现候选转录痕迹，但缺少 sessions 元数据确认，属于 discoverability gap'
        else:
            summary = ''
            note_mode = 'discovery_mode=no_signal'
            missing_reason = f'未发现可确认的近期 {LABELS.get(channel, channel)} 会话转录或 sessions 元数据'

        results.append({
            'channel': channel,
            'channel_label': LABELS.get(channel, channel.title()),
            'scope_key': primary_scope,
            'scope_type': scope_type,
            'participant_shape': pshape,
            'bot_count': bots,
            'session_count': session_count,
            'status': status,
            'date': args.date,
            'time_window': f"{start.strftime('%Y-%m-%d %H:%M')} ~ {end.strftime('%Y-%m-%d %H:%M')} Asia/Shanghai",
            'source_refs': refs if refs else [f'scan:{args.sessions_dir}'],
            'summary_points': [summary] if summary else [],
            'issues': [],
            'wins': [],
            'missing_reason': missing_reason,
            'notes': [f'expected={channel}', note_mode, f'scopes={len(scopes)}']
        })

    Path(args.output).write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'channels': results}, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
