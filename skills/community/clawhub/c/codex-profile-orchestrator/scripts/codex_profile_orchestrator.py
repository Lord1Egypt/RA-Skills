#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

USAGE_URL = 'https://chatgpt.com/backend-api/wham/usage'
TRANSPORT_ERRORS = {'timeout', 'url_error', 'os_error', 'network_down'}
INVALID_ERRORS = {'http_400', 'http_401', 'http_403', 'missing_token', 'token_expired'}


def now_ms() -> int:
    return int(time.time() * 1000)


def deep_copy(value: Any) -> Any:
    return json.loads(json.dumps(value, ensure_ascii=False))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def backup_file(path: Path) -> Path:
    backup_path = path.with_suffix(path.suffix + f'.bak-{int(time.time())}')
    if path.exists():
        shutil.copy2(path, backup_path)
    return backup_path


def decode_token(token: str | None) -> dict[str, Any]:
    if not isinstance(token, str) or token.count('.') < 2:
        return {}
    payload = token.split('.')[1]
    payload += '=' * (-len(payload) % 4)
    try:
        return json.loads(base64.urlsafe_b64decode(payload.encode()).decode())
    except Exception:
        return {}


def extract_identity(profile_id: str, profile: dict[str, Any]) -> dict[str, Any]:
    token = profile.get('access') or profile.get('token')
    decoded = decode_token(token)
    auth_payload = decoded.get('https://api.openai.com/auth') or {}
    profile_payload = decoded.get('https://api.openai.com/profile') or {}
    return {
        'profileId': profile_id,
        'profileBlob': deep_copy(profile),
        'token': token,
        'email': (profile.get('email') or profile_payload.get('email') or '').lower() or None,
        'userId': auth_payload.get('chatgpt_user_id') or auth_payload.get('user_id'),
        'accountId': auth_payload.get('chatgpt_account_id'),
        'provider': profile.get('provider'),
        'type': profile.get('type'),
    }


def collect_profiles(auth: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for profile_id, profile in (auth.get('profiles') or {}).items():
        if not str(profile_id).startswith('openai-codex:') or not isinstance(profile, dict):
            continue
        rows.append(extract_identity(str(profile_id), profile))
    rows.sort(key=lambda row: row['profileId'])
    return rows


def identity_key(email: str | None, user_id: str | None, account_id: str | None) -> str:
    return f'{(email or "").lower()}|{user_id or ""}|{account_id or ""}'


def email_user_key(email: str | None, user_id: str | None) -> str:
    return f'{(email or "").lower()}|{user_id or ""}'


def slug_email(email: str | None) -> str:
    base = ((email or 'account').split('@')[0]).strip().lower()
    slug = ''.join(ch if ch.isalnum() else '-' for ch in base).strip('-')
    return slug or 'account'


def next_ws_alias(email: str | None, identities: dict[str, Any], auth_profiles: dict[str, Any]) -> str:
    prefix = f'openai-codex:{slug_email(email)}-ws'
    used_numbers: set[int] = set()
    for record in identities.values():
        canonical = str(record.get('canonicalId') or '')
        if canonical.startswith(prefix):
            try:
                used_numbers.add(int(canonical.split('-ws')[-1]))
            except Exception:
                pass
    for profile_id in auth_profiles:
        pid = str(profile_id)
        if pid.startswith(prefix):
            try:
                used_numbers.add(int(pid.split('-ws')[-1]))
            except Exception:
                pass
    next_number = 2
    while next_number in used_numbers:
        next_number += 1
    return f'{prefix}{next_number}'


def remaining_percent(window: dict[str, Any] | None) -> float | None:
    if not isinstance(window, dict) or window.get('used_percent') is None:
        return None
    try:
        return max(0.0, 100.0 - float(window.get('used_percent') or 0.0))
    except Exception:
        return None


def pick_window(section: dict[str, Any], seconds: int) -> dict[str, Any] | None:
    for key in ('primary_window', 'secondary_window'):
        window = section.get(key) or {}
        if window.get('limit_window_seconds') == seconds:
            return window
    return None


def compute_usage_summary(usage: dict[str, Any]) -> dict[str, Any]:
    rate_limit = usage.get('rate_limit') or {}
    code_review = usage.get('code_review_rate_limit') or {}
    five = remaining_percent(pick_window(rate_limit, 18000) or rate_limit.get('primary_window'))
    week = remaining_percent(pick_window(rate_limit, 604800) or rate_limit.get('secondary_window'))
    candidates = [value for value in [five, week, remaining_percent(pick_window(code_review, 18000)), remaining_percent(pick_window(code_review, 604800))] if value is not None]
    effective = min(candidates) if candidates else None
    unusable = None
    if usage.get('error'):
        unusable = usage.get('error')
    elif rate_limit.get('allowed') is False:
        unusable = 'rate_limit_disallowed'
    elif rate_limit.get('limit_reached') is True:
        unusable = str((usage.get('rate_limit_reached_type') or {}).get('type') or 'rate_limit_reached')
    elif week is not None and week <= 0:
        unusable = 'weekly_exhausted'
    elif five is not None and five <= 0:
        unusable = 'five_hour_exhausted'
    return {
        'fiveHourRemaining': five,
        'weekRemaining': week,
        'effectiveRemaining': effective,
        'unusableReason': unusable,
    }


def probe_connectivity(url: str, timeout_seconds: int) -> dict[str, Any]:
    req = urllib.request.Request(url, headers={'User-Agent': 'codex-profile-orchestrator/2.0'})
    try:
        with urllib.request.urlopen(req, timeout=timeout_seconds) as response:
            return {'ok': True, 'status': getattr(response, 'status', None)}
    except urllib.error.HTTPError as exc:
        return {'ok': True, 'status': exc.code, 'error': f'http_{exc.code}'}
    except urllib.error.URLError as exc:
        return {'ok': False, 'error': f'url_error:{exc.reason}'}
    except socket.timeout:
        return {'ok': False, 'error': 'timeout'}
    except OSError as exc:
        return {'ok': False, 'error': f'os_error:{exc.__class__.__name__}'}


def load_fixtures(fixtures_path: str | None) -> dict[str, Any]:
    if not fixtures_path:
        return {}
    return json.loads(Path(fixtures_path).read_text(encoding='utf-8'))


def fetch_usage(profile: dict[str, Any], timeout_seconds: int, fixtures: dict[str, Any], network_ok: bool) -> dict[str, Any]:
    if not network_ok:
        return {'error': 'network_down'}
    fixture = fixtures.get(profile['profileId'])
    if fixture is not None:
        return fixture
    token = profile.get('token')
    if not token:
        return {'error': 'missing_token'}
    headers = {
        'Authorization': f'Bearer {token}',
        'User-Agent': 'codex-profile-orchestrator/2.0',
        'Accept': 'application/json',
    }
    if profile.get('accountId'):
        headers['ChatGPT-Account-Id'] = str(profile['accountId'])
    req = urllib.request.Request(USAGE_URL, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout_seconds) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as exc:
        return {'error': f'http_{exc.code}'}
    except urllib.error.URLError:
        return {'error': 'url_error'}
    except socket.timeout:
        return {'error': 'timeout'}
    except OSError:
        return {'error': 'os_error'}


def build_profile_statuses(profiles: list[dict[str, Any]], registry: dict[str, Any], timeout_seconds: int, fixtures_path: str | None, network_ok: bool) -> list[dict[str, Any]]:
    fixtures = load_fixtures(fixtures_path)
    out = []
    identity_index = registry.setdefault('identities', {})
    for profile in profiles:
        usage = fetch_usage(profile, timeout_seconds, fixtures, network_ok)
        summary = compute_usage_summary(usage)
        key = identity_key(profile.get('email'), profile.get('userId'), profile.get('accountId'))
        record = identity_index.get(key) or {}
        out.append({
            **profile,
            'identityKey': key,
            'canonicalId': record.get('canonicalId') or profile['profileId'],
            'kind': record.get('kind') or 'primary',
            'usage': usage,
            **summary,
            'invalid': str(usage.get('error') or '') in INVALID_ERRORS,
            'transportError': str(usage.get('error') or '') in TRANSPORT_ERRORS,
            'usable': not summary['unusableReason'] and str(usage.get('error') or '') not in INVALID_ERRORS,
        })
    return out


def ensure_registry(path: Path) -> dict[str, Any]:
    registry = load_json(path)
    registry.setdefault('version', 2)
    registry.setdefault('identities', {})
    registry.setdefault('notificationState', {})
    registry.setdefault('invalidStreaks', {})
    registry.setdefault('lastPreferredProfileId', None)
    return registry


def reconcile_profiles(auth: dict[str, Any], registry: dict[str, Any], apply: bool) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], bool]:
    auth_profiles = auth.setdefault('profiles', {})
    identities = registry.setdefault('identities', {})
    rows = collect_profiles(auth)
    discovered = []
    duplicates = []
    auth_changed = False
    exact_seen: dict[str, str] = {}
    email_user_seen: dict[str, list[str]] = {}

    for row in rows:
        key = identity_key(row.get('email'), row.get('userId'), row.get('accountId'))
        if key in identities:
            record = identities[key]
            record['lastSeenAt'] = now_ms()
            record['profileBlob'] = deep_copy(row['profileBlob'])
            canonical = record['canonicalId']
        else:
            same_exact = exact_seen.get(key)
            same_email_user = email_user_seen.get(email_user_key(row.get('email'), row.get('userId')), [])
            if same_exact:
                canonical = same_exact
                kind = 'duplicate'
                duplicates.append({'profileId': row['profileId'], 'canonicalId': canonical, 'reason': 'same-email-user-account'})
            elif same_email_user:
                canonical = next_ws_alias(row.get('email'), identities, auth_profiles)
                kind = 'workspace_variant'
                discovered.append({'profileId': row['profileId'], 'canonicalId': canonical, 'kind': kind, 'email': row.get('email')})
            else:
                canonical = f'openai-codex:{slug_email(row.get("email"))}'
                kind = 'primary'
                if canonical in auth_profiles and canonical != row['profileId']:
                    canonical = next_ws_alias(row.get('email'), identities, auth_profiles)
                    kind = 'workspace_variant'
                discovered.append({'profileId': row['profileId'], 'canonicalId': canonical, 'kind': kind, 'email': row.get('email')})
            identities[key] = {
                'email': row.get('email'),
                'userId': row.get('userId'),
                'accountId': row.get('accountId'),
                'canonicalId': canonical,
                'kind': kind,
                'firstSeenAt': now_ms(),
                'lastSeenAt': now_ms(),
                'profileBlob': deep_copy(row['profileBlob']),
            }
        exact_seen.setdefault(key, identities[key]['canonicalId'])
        email_user_seen.setdefault(email_user_key(row.get('email'), row.get('userId')), []).append(identities[key]['canonicalId'])

    if apply:
        for record in identities.values():
            canonical = record.get('canonicalId')
            profile_blob = record.get('profileBlob') or {}
            if canonical and canonical not in auth_profiles and profile_blob:
                auth_profiles[canonical] = deep_copy(profile_blob)
                auth_changed = True
        for row in rows:
            key = identity_key(row.get('email'), row.get('userId'), row.get('accountId'))
            canonical = (identities.get(key) or {}).get('canonicalId')
            if canonical and row['profileId'] != canonical and key in exact_seen:
                auth_profiles.pop(row['profileId'], None)
                auth_changed = True
    rows = collect_profiles(auth)
    return rows, discovered, duplicates, auth_changed


def sort_key(profile: dict[str, Any], current_profile_id: str | None) -> tuple[float, float, int, int]:
    return (
        float(profile.get('fiveHourRemaining') or 0.0),
        float(profile.get('weekRemaining') or 0.0),
        1 if profile.get('kind') == 'primary' else 0,
        1 if profile.get('profileId') == current_profile_id else 0,
    )


def choose_preferred(statuses: list[dict[str, Any]], current_profile_id: str | None, threshold: float, network_ok: bool) -> dict[str, Any] | None:
    if not statuses:
        return None
    current = next((row for row in statuses if row['profileId'] == current_profile_id), None)
    if not network_ok:
        return current or statuses[0]
    healthy = [row for row in statuses if row.get('usable') and not row.get('invalid')]
    if current and current in healthy and (current.get('fiveHourRemaining') or 0.0) > threshold:
        return current
    above = [row for row in healthy if (row.get('fiveHourRemaining') or 0.0) > threshold]
    if above:
        above.sort(key=lambda row: sort_key(row, current_profile_id), reverse=True)
        return above[0]
    if current and current in healthy:
        return current
    if healthy:
        healthy.sort(key=lambda row: sort_key(row, current_profile_id), reverse=True)
        return healthy[0]
    return current or statuses[0]


def resolve_session_targets(sessions: dict[str, Any], configured_targets: list[str], agent_name: str) -> list[str]:
    seen = set()
    out = []

    def add(key: str) -> None:
        if key not in seen and isinstance(sessions.get(key), dict):
            seen.add(key)
            out.append(key)

    for key in configured_targets:
        add(key)
    prefix = f'agent:{agent_name}:'
    for key, entry in sessions.items():
        if not isinstance(entry, dict) or not key.startswith(prefix):
            continue
        if 'authProfileOverride' in entry or any(token in key for token in (':telegram:', ':signal:', ':discord:', ':whatsapp:', ':slack:', ':webchat:')):
            add(key)
    return out


def sync_sessions(sessions_path: Path, sessions: dict[str, Any], targets: list[str], preferred_profile_id: str | None, apply: bool) -> list[dict[str, Any]]:
    updates = []
    changed = False
    if not preferred_profile_id:
        return updates
    for key in targets:
        entry = sessions.get(key)
        if not isinstance(entry, dict):
            continue
        old = entry.get('authProfileOverride')
        if old == preferred_profile_id:
            continue
        updates.append({'sessionKey': key, 'oldProfileId': old, 'newProfileId': preferred_profile_id})
        if apply:
            entry['authProfileOverride'] = preferred_profile_id
            entry['authProfileOverrideSource'] = 'codex-profile-orchestrator'
            entry['updatedAt'] = now_ms()
            changed = True
    if changed:
        backup_file(sessions_path)
        write_json(sessions_path, sessions)
    return updates


def update_auth_order(auth_path: Path, auth: dict[str, Any], preferred_profile_id: str | None, statuses: list[dict[str, Any]], apply: bool) -> bool:
    if not preferred_profile_id:
        return False
    valid_profile_ids = [row['profileId'] for row in statuses if not row.get('invalid')]
    order = auth.setdefault('order', {})
    new_order = [pid for pid in order.get('openai-codex', []) if pid in valid_profile_ids and pid != preferred_profile_id]
    for pid in valid_profile_ids:
        if pid != preferred_profile_id and pid not in new_order:
            new_order.append(pid)
    new_order.insert(0, preferred_profile_id)
    if new_order == order.get('openai-codex', []):
        return False
    if apply:
        backup_file(auth_path)
        order['openai-codex'] = new_order
        write_json(auth_path, auth)
    return True


def cleanup_invalid(auth_path: Path, auth: dict[str, Any], registry: dict[str, Any], statuses: list[dict[str, Any]], preferred_profile_id: str | None, delete_after: int, apply: bool, network_ok: bool) -> tuple[list[dict[str, Any]], list[str]]:
    invalid_profiles = []
    removed = []
    streaks = registry.setdefault('invalidStreaks', {})
    if not network_ok:
        registry['lastNetworkIncidentAt'] = now_ms()
        return invalid_profiles, removed
    auth_profiles = auth.setdefault('profiles', {})
    for row in statuses:
        profile_id = row['profileId']
        error = str((row.get('usage') or {}).get('error') or '')
        if row.get('invalid'):
            streaks[profile_id] = int(streaks.get(profile_id, 0) or 0) + 1
            invalid_profiles.append({'profileId': profile_id, 'reason': error, 'streak': streaks[profile_id]})
            if apply and streaks[profile_id] >= delete_after and profile_id != preferred_profile_id and profile_id in auth_profiles:
                auth_profiles.pop(profile_id, None)
                removed.append(profile_id)
        elif row.get('transportError'):
            continue
        else:
            streaks[profile_id] = 0
    if removed:
        backup_file(auth_path)
        write_json(auth_path, auth)
    return invalid_profiles, removed


def short_profile_name(profile_id: str | None) -> str:
    return str(profile_id or '-').removeprefix('openai-codex:')


def fmt_percent(value: float | None) -> str:
    if value is None:
        return '?'
    return f'%{int(value)}'


def build_notifications(discovered: list[dict[str, Any]], duplicates: list[dict[str, Any]], invalids: list[dict[str, Any]], removed: list[str], previous_preferred: str | None, preferred_profile_id: str | None, session_updates: list[dict[str, Any]], statuses: list[dict[str, Any]], threshold: float, network: dict[str, Any], registry: dict[str, Any]) -> list[dict[str, str]]:
    notes = []
    threshold_state = registry.setdefault('thresholdState', {})
    if not network.get('ok'):
        notes.append({'code': 'network', 'text': '🌐 Ağ veya ChatGPT erişimi sorunlu görünüyor. Profiller karantinaya alınmadı.'})
    for row in discovered:
        emoji = '🆕'
        label = 'Yeni WS' if row.get('kind') == 'workspace_variant' else 'Yeni hesap'
        notes.append({'code': f'discovered:{row.get("canonicalId")}', 'text': f'{emoji} {label}: {row.get("canonicalId")} | {row.get("email") or "-"}'})
    for row in duplicates:
        notes.append({'code': f'duplicate:{row["profileId"]}', 'text': f'🧹 Duplicate görmezden gelindi: {row["profileId"]} -> {row["canonicalId"]}'})
    for row in invalids:
        notes.append({'code': f'invalid:{row["profileId"]}', 'text': f'⚠️ Profil karantinada: {short_profile_name(row["profileId"])} ({row["reason"]})'})
    for profile_id in removed:
        notes.append({'code': f'removed:{profile_id}', 'text': f'🗑️ Profil silindi: {short_profile_name(profile_id)}'})
    rows_by_id = {row['profileId']: row for row in statuses}
    if preferred_profile_id and preferred_profile_id != previous_preferred:
        new_row = rows_by_id.get(preferred_profile_id) or {}
        if previous_preferred:
            old_row = rows_by_id.get(previous_preferred) or {}
            notes.append({'code': 'switch', 'text': f'🔁 Profil değişti: {short_profile_name(previous_preferred)} -> {short_profile_name(preferred_profile_id)} | 5h {fmt_percent(new_row.get("fiveHourRemaining"))} | week {fmt_percent(new_row.get("weekRemaining"))}'})
        else:
            notes.append({'code': 'switch', 'text': f'✅ Aktif profil: {short_profile_name(preferred_profile_id)} | 5h {fmt_percent(new_row.get("fiveHourRemaining"))} | week {fmt_percent(new_row.get("weekRemaining"))}'})
    for row in statuses:
        profile_id = str(row['profileId'])
        profile_state = threshold_state.setdefault(profile_id, {})
        five = row.get('fiveHourRemaining')
        week = row.get('weekRemaining')
        five_low = five is not None and five < threshold
        week_low = week is not None and week < threshold
        if five_low and not profile_state.get('fiveHourLow'):
            notes.append({'code': f'threshold5:{profile_id}', 'text': f'⚠️ {short_profile_name(profile_id)} için 5 saatlik limit %25 altına indi.'})
        if week_low and not profile_state.get('weekLow'):
            notes.append({'code': f'threshold7:{profile_id}', 'text': f'⚠️ {short_profile_name(profile_id)} için weekly limit %25 altına indi.'})
        profile_state['fiveHourLow'] = five_low
        profile_state['weekLow'] = week_low
    if session_updates:
        notes.append({'code': f'sessions:{preferred_profile_id}', 'text': f'🔄 Oturum senkronu tamam: {len(session_updates)} session -> {short_profile_name(preferred_profile_id)}'})
    return notes


def notify_openclaw(cfg: dict[str, Any], registry: dict[str, Any], notifications: list[dict[str, str]], apply: bool) -> list[dict[str, str]]:
    notify_cfg = cfg.get('notify') or {}
    if not apply or not notify_cfg.get('enabled'):
        return []
    target = str(notify_cfg.get('target') or '').strip()
    if not target:
        return []
    dedupe_seconds = int(notify_cfg.get('dedupeSeconds', 300))
    sent = []
    state = registry.setdefault('notificationState', {})
    now = int(time.time())
    for note in notifications:
        key = hashlib.sha256(f"{note['code']}|{note['text']}".encode()).hexdigest()
        if now - int(state.get(key, 0) or 0) < dedupe_seconds:
            continue
        openclaw_bin = shutil.which('openclaw') or shutil.which('openclaw.cmd') or shutil.which('openclaw.ps1') or 'openclaw.cmd'
        cmd = [openclaw_bin, 'message', 'send', '--channel', str(notify_cfg.get('channel') or 'telegram'), '--target', target, '-m', note['text']]
        account = str(notify_cfg.get('account') or '').strip()
        if account:
            cmd.extend(['--account', account])
        result = subprocess.run(cmd, check=False, capture_output=True, text=True, timeout=90)
        if result.returncode == 0:
            state[key] = now
            sent.append(note)
    return sent


def summary_lines(statuses: list[dict[str, Any]], preferred_profile_id: str | None) -> list[str]:
    lines = [f'preferred: {preferred_profile_id or "-"}']
    for row in statuses:
        marker = ' *' if row['profileId'] == preferred_profile_id else ''
        lines.append(f'- {row["profileId"]}{marker} | 5h {fmt_percent(row.get("fiveHourRemaining"))} | week {fmt_percent(row.get("weekRemaining"))} | eff {fmt_percent(row.get("effectiveRemaining"))} | error {(row.get("usage") or {}).get("error") or "-"}')
    return lines


def normalize_profile_id(profile_id: str | None, statuses: list[dict[str, Any]]) -> str | None:
    raw = str(profile_id or '').strip()
    if not raw:
        return None
    by_id = {str(row.get('profileId') or ''): row for row in statuses}
    if raw in by_id:
        return raw
    suffix = raw.removeprefix('openai-codex:').lower()
    for row in statuses:
        pid = str(row.get('profileId') or '')
        email = str(row.get('email') or '').lower()
        local = email.split('@')[0] if '@' in email else email
        if suffix in {pid.removeprefix('openai-codex:').lower(), email, local}:
            return pid
    return raw if raw in by_id else None


def sync_auth_state(auth_state_path: Path, auth_state: dict[str, Any], preferred_profile_id: str | None, statuses: list[dict[str, Any]], apply: bool) -> bool:
    if not preferred_profile_id:
        return False
    valid_profile_ids = [str(row.get('profileId') or '') for row in statuses if str(row.get('profileId') or '')]
    if not valid_profile_ids:
        return False
    changed = False
    order = auth_state.setdefault('order', {})
    current_order = [normalize_profile_id(pid, statuses) for pid in (order.get('openai-codex', []) or [])]
    current_order = [pid for pid in current_order if pid and pid in valid_profile_ids and pid != preferred_profile_id]
    for pid in valid_profile_ids:
        if pid != preferred_profile_id and pid not in current_order:
            current_order.append(pid)
    new_order = [preferred_profile_id, *current_order]
    if new_order != (order.get('openai-codex', []) or []):
        order['openai-codex'] = new_order
        changed = True

    last_good = auth_state.setdefault('lastGood', {})
    if last_good.get('openai-codex') != preferred_profile_id:
        last_good['openai-codex'] = preferred_profile_id
        changed = True

    usage_stats = auth_state.setdefault('usageStats', {})
    normalized_usage: dict[str, Any] = {}
    for key, value in list(usage_stats.items()):
        normalized_key = normalize_profile_id(key, statuses)
        target_key = normalized_key or key
        if target_key not in normalized_usage:
            normalized_usage[target_key] = value
    if usage_stats != normalized_usage:
        auth_state['usageStats'] = normalized_usage
        changed = True

    if changed and apply:
        backup_file(auth_state_path)
        write_json(auth_state_path, auth_state)
    return changed


def run_once(config_path: Path, apply: bool) -> dict[str, Any]:
    cfg = load_json(config_path)
    agent_name = str(cfg.get('agent') or 'main')
    state_dir = Path(cfg.get('stateDir') or Path.home() / '.openclaw')
    auth_path = state_dir / 'agents' / agent_name / 'agent' / 'auth-profiles.json'
    auth_state_path = state_dir / 'agents' / agent_name / 'agent' / 'auth-state.json'
    sessions_path = state_dir / 'agents' / agent_name / 'sessions' / 'sessions.json'
    registry_path = Path(cfg.get('registryPath') or (config_path.resolve().parent.parent / 'state' / 'codex-profile-orchestrator-state.json'))
    auth = load_json(auth_path)
    auth_state = load_json(auth_state_path)
    sessions = load_json(sessions_path)
    registry = ensure_registry(registry_path)
    profiles, discovered, duplicates, auth_changed = reconcile_profiles(auth, registry, apply)
    if apply and auth_changed:
        backup_file(auth_path)
        write_json(auth_path, auth)
    if not profiles:
        payload = {
            'generatedAt': now_ms(),
            'safeMode': True,
            'notifications': [{'code': 'no-profiles', 'text': '⚠️ hiç codex profili bulunamadı.'}],
            'profiles': [],
            'preferredProfileId': None,
        }
        if apply:
            write_json(registry_path, registry)
        return payload
    network = probe_connectivity(str(cfg.get('probeUrl') or 'https://chatgpt.com/'), int(cfg.get('probeTimeoutSeconds', 8) or 8))
    statuses = build_profile_statuses(profiles, registry, int(cfg.get('usageTimeoutSeconds', 15) or 15), cfg.get('usageFixturesPath'), bool(network.get('ok')))
    main_entry = sessions.get(f'agent:{agent_name}:main') or sessions.get('agent:main:main') or {}
    current_profile_id = normalize_profile_id(main_entry.get('authProfileOverride') if isinstance(main_entry, dict) else None, statuses)
    auth_state_current = normalize_profile_id(((auth_state.get('lastGood') or {}).get('openai-codex')), statuses)
    if not current_profile_id:
        current_profile_id = auth_state_current
    threshold = float(cfg.get('thresholdPercent', 25) or 25)
    preferred = choose_preferred(statuses, current_profile_id, threshold, bool(network.get('ok')))
    preferred_profile_id = preferred['profileId'] if preferred else current_profile_id
    invalids, removed = cleanup_invalid(auth_path, auth, registry, statuses, preferred_profile_id, int(cfg.get('invalidStreakBeforeDelete', 3) or 3), apply, bool(network.get('ok')))
    if removed:
        profiles = collect_profiles(auth)
        statuses = build_profile_statuses(profiles, registry, int(cfg.get('usageTimeoutSeconds', 15) or 15), cfg.get('usageFixturesPath'), bool(network.get('ok')))
        preferred = choose_preferred(statuses, current_profile_id, threshold, bool(network.get('ok')))
        preferred_profile_id = preferred['profileId'] if preferred else current_profile_id
    targets = resolve_session_targets(sessions, list(cfg.get('sessionTargets') or []), agent_name)
    session_updates = sync_sessions(sessions_path, sessions, targets, preferred_profile_id, apply)
    order_updated = update_auth_order(auth_path, auth, preferred_profile_id, statuses, apply)
    auth_state_updated = sync_auth_state(auth_state_path, auth_state, preferred_profile_id, statuses, apply)
    previous_preferred = registry.get('lastPreferredProfileId')
    notifications = build_notifications(discovered, duplicates, invalids, removed, previous_preferred, preferred_profile_id, session_updates, statuses, threshold, network, registry)
    sent_notifications = notify_openclaw(cfg, registry, notifications, apply)
    registry['lastPreferredProfileId'] = preferred_profile_id
    registry['updatedAt'] = now_ms()
    write_json(registry_path, registry) if apply else None
    return {
        'generatedAt': now_ms(),
        'apply': apply,
        'network': network,
        'currentProfileId': current_profile_id,
        'preferredProfileId': preferred_profile_id,
        'profiles': statuses,
        'discovered': discovered,
        'duplicates': duplicates,
        'invalidProfiles': invalids,
        'removedProfiles': removed,
        'sessionUpdates': session_updates,
        'authOrderUpdated': order_updated,
        'authStateUpdated': auth_state_updated,
        'notifications': notifications,
        'sentNotifications': sent_notifications,
    }


def run_self_test() -> dict[str, Any]:
    def make_token(email: str, user_id: str, account_id: str) -> str:
        header = base64.urlsafe_b64encode(json.dumps({'alg': 'none'}).encode()).decode().rstrip('=')
        payload = base64.urlsafe_b64encode(json.dumps({'https://api.openai.com/auth': {'chatgpt_user_id': user_id, 'chatgpt_account_id': account_id}, 'https://api.openai.com/profile': {'email': email}}).encode()).decode().rstrip('=')
        return f'{header}.{payload}.sig'

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        state_dir = root / '.openclaw'
        workspace = root / 'workspace'
        auth_path = state_dir / 'agents' / 'main' / 'agent' / 'auth-profiles.json'
        sessions_path = state_dir / 'agents' / 'main' / 'sessions' / 'sessions.json'
        cfg_path = workspace / 'config' / 'codex-profile-orchestrator.json'
        registry_path = workspace / 'state' / 'codex-profile-orchestrator-state.json'
        fixtures_path = workspace / 'fixtures.json'
        auth_path.parent.mkdir(parents=True, exist_ok=True)
        sessions_path.parent.mkdir(parents=True, exist_ok=True)
        cfg_path.parent.mkdir(parents=True, exist_ok=True)
        registry_path.parent.mkdir(parents=True, exist_ok=True)
        write_json(auth_path, {'profiles': {
            'openai-codex:one': {'access': make_token('same@example.com', 'u1', 'a1')},
            'openai-codex:dup': {'access': make_token('same@example.com', 'u1', 'a1')},
            'openai-codex:variant': {'access': make_token('same@example.com', 'u1', 'a2')},
            'openai-codex:other': {'access': make_token('other@example.com', 'u2', 'a3')},
        }})
        write_json(sessions_path, {
            'agent:main:main': {'authProfileOverride': 'openai-codex:one'},
            'agent:main:telegram:direct:123': {'authProfileOverride': 'openai-codex:one'},
        })
        write_json(fixtures_path, {
            'openai-codex:one': {'rate_limit': {'allowed': True, 'limit_reached': False, 'primary_window': {'used_percent': 90, 'limit_window_seconds': 18000}, 'secondary_window': {'used_percent': 10, 'limit_window_seconds': 604800}}},
            'openai-codex:dup': {'rate_limit': {'allowed': True, 'limit_reached': False, 'primary_window': {'used_percent': 80, 'limit_window_seconds': 18000}, 'secondary_window': {'used_percent': 10, 'limit_window_seconds': 604800}}},
            'openai-codex:variant': {'rate_limit': {'allowed': True, 'limit_reached': False, 'primary_window': {'used_percent': 20, 'limit_window_seconds': 18000}, 'secondary_window': {'used_percent': 5, 'limit_window_seconds': 604800}}},
            'openai-codex:other': {'rate_limit': {'allowed': True, 'limit_reached': False, 'primary_window': {'used_percent': 15, 'limit_window_seconds': 18000}, 'secondary_window': {'used_percent': 15, 'limit_window_seconds': 604800}}},
        })
        write_json(cfg_path, {
            'agent': 'main',
            'stateDir': str(state_dir),
            'registryPath': str(registry_path),
            'usageFixturesPath': str(fixtures_path),
            'probeUrl': 'https://chatgpt.com/',
            'thresholdPercent': 25,
            'sessionTargets': ['agent:main:main'],
            'notify': {'enabled': False},
        })
        payload = run_once(cfg_path, apply=True)
        assert payload['preferredProfileId'] == 'openai-codex:other'
        assert any(item['canonicalId'].endswith('-ws2') for item in payload['discovered'] if item['kind'] == 'workspace_variant')
        auth_after = load_json(auth_path)
        assert 'openai-codex:dup' not in (auth_after.get('profiles') or {})
        sessions_after = load_json(sessions_path)
        assert (sessions_after.get('agent:main:telegram:direct:123') or {}).get('authProfileOverride') == 'openai-codex:other'
        # network outage should not quarantine
        write_json(cfg_path, {
            'agent': 'main',
            'stateDir': str(state_dir),
            'registryPath': str(registry_path),
            'usageFixturesPath': str(fixtures_path),
            'probeUrl': 'http://127.0.0.1:9',
            'thresholdPercent': 25,
            'sessionTargets': ['agent:main:main'],
            'notify': {'enabled': False},
        })
        payload2 = run_once(cfg_path, apply=False)
        assert payload2['network']['ok'] is False
        assert not payload2['invalidProfiles']
        return {'ok': True, 'testedAt': now_ms()}


def redact_output(value: Any) -> Any:
    if isinstance(value, dict):
        out: dict[str, Any] = {}
        for key, item in value.items():
            if key in {'token', 'access', 'refresh'}:
                out[key] = '<redacted>' if item else item
            elif key == 'profileBlob' and isinstance(item, dict):
                blob = dict(item)
                for sensitive in ('access', 'refresh'):
                    if sensitive in blob:
                        blob[sensitive] = '<redacted>' if blob.get(sensitive) else blob.get(sensitive)
                out[key] = {k: redact_output(v) for k, v in blob.items()}
            else:
                out[key] = redact_output(item)
        return out
    if isinstance(value, list):
        return [redact_output(item) for item in value]
    return value


def emit_text(text: str) -> None:
    try:
        sys.stdout.write(text + '\n')
    except UnicodeEncodeError:
        sys.stdout.buffer.write((text + '\n').encode('utf-8', errors='backslashreplace'))


def main() -> int:
    parser = argparse.ArgumentParser(description='codex profile orchestrator')
    sub = parser.add_subparsers(dest='cmd', required=False)
    parser.add_argument('--config')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--daemon', action='store_true')
    parser.add_argument('--json', action='store_true')
    sub.add_parser('self-test')
    sub.add_parser('report')
    args = parser.parse_args()

    if args.cmd == 'self-test':
        payload = run_self_test()
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    if not args.config:
        raise SystemExit('--config is required unless using self-test')

    def emit(payload: dict[str, Any], *, force_summary: bool = False) -> None:
        if force_summary or args.cmd == 'report':
            emit_text('\n'.join(summary_lines(payload.get('profiles') or [], payload.get('preferredProfileId'))))
        elif args.json or args.dry_run or args.apply:
            emit_text(json.dumps(redact_output(payload), ensure_ascii=False, indent=2))
        else:
            emit_text('\n'.join(summary_lines(payload.get('profiles') or [], payload.get('preferredProfileId'))))

    apply = bool(args.apply and not args.dry_run)
    if args.daemon:
        cfg = load_json(Path(args.config))
        loop_seconds = int(cfg.get('loopSeconds', 60) or 60)
        while True:
            emit(run_once(Path(args.config), apply=apply), force_summary=True)
            time.sleep(loop_seconds)
    else:
        emit(run_once(Path(args.config), apply=apply))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
