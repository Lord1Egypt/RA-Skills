#!/usr/bin/env python3
import argparse
import json
import os
import time
import subprocess
from pathlib import Path
from urllib import parse, request, error

ROOT = Path(__file__).resolve().parent.parent
IDEMPOTENT_PATH = ROOT / "tmp" / "subscribe-callback-dedupe.json"
DEFAULT_BASE = "http://home.dobby.lol:1001"


def mk_toast(t: str, content: str):
    return {"toast": {"type": t, "content": content}}


def pack_result(*, success: bool, status: str, message: str, subscribe_id=None, deduped=False, ui=None, error=None):
    data = {
        "success": success,
        "status": status,
        "message": message,
        "deduped": deduped,
        "subscribe_id": subscribe_id,
        "ui": ui or {},
        "callbackResponse": mk_toast("info", "处理中..."),
        "delayedUpdate": {
            "toast": mk_toast("success" if success else "error", message)["toast"],
            "ui": ui or {},
        },
    }
    if error:
        data["error"] = error
    return data


def load_cred(channel: str, user_id: str):
    p = Path('/root/.openclaw/workspace-dev/skills/movipilot-api-foundation/scripts/mp_credential_store.py')
    raw = subprocess.check_output(['python3', str(p), 'get', '--channel', channel, '--user-id', user_id], text=True).strip()
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except Exception:
        return {}


def _ensure_store():
    IDEMPOTENT_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not IDEMPOTENT_PATH.exists():
        IDEMPOTENT_PATH.write_text('{}', encoding='utf-8')


def _load_store():
    _ensure_store()
    try:
        return json.loads(IDEMPOTENT_PATH.read_text(encoding='utf-8') or '{}')
    except Exception:
        return {}


def _save_store(data):
    _ensure_store()
    IDEMPOTENT_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def dedupe_key(payload: dict):
    return f"subscribe:{payload.get('media_type')}:{payload.get('tmdb_id')}"


def get_recent(key: str, window_sec: int = 60):
    db = _load_store()
    item = db.get(key)
    if not item:
        return None
    if time.time() - item.get('ts', 0) <= window_sec:
        return item
    return None


def mark_state(key: str, result: dict):
    db = _load_store()
    db[key] = {'ts': int(time.time()), **result}
    _save_store(db)


def mp_get(url: str):
    req = request.Request(url, headers={'User-Agent': 'OpenClaw/subscribe-callback'})
    with request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode('utf-8', errors='replace'))


def mp_post(url: str, data: dict):
    body = json.dumps(data, ensure_ascii=False).encode('utf-8')
    req = request.Request(url, data=body, method='POST', headers={'Content-Type': 'application/json', 'User-Agent': 'OpenClaw/subscribe-callback'})
    with request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode('utf-8', errors='replace'))


def main():
    ap = argparse.ArgumentParser(description='Handle Feishu card subscribe callback -> MoviePilot subscription')
    ap.add_argument('--payload', required=True, help='JSON payload from callback')
    ap.add_argument('--channel', default='feishu')
    ap.add_argument('--user-id', required=True)
    args = ap.parse_args()

    payload = json.loads(args.payload)
    if payload.get('action') != 'subscribe':
        raise SystemExit('unsupported action')

    media_type = payload.get('media_type')
    tmdb_id = str(payload.get('tmdb_id') or '').strip()
    if media_type not in ('movie', 'tv') or not tmdb_id.isdigit():
        raise SystemExit('invalid payload: need media_type(movie|tv) and numeric tmdb_id')

    key = dedupe_key(payload)
    item = get_recent(key, window_sec=60)
    if item:
        status = item.get('status')
        if status == 'processing':
            print(json.dumps(pack_result(success=True, deduped=True, status='processing', message='正在处理中，请稍候', ui={'subscribe_disabled': True, 'subscribe_button_text': '处理中...'}), ensure_ascii=False))
            return
        print(json.dumps(pack_result(success=True, deduped=True, status=status, message='重复点击已忽略', subscribe_id=item.get('subscribe_id'), ui={'subscribe_disabled': True, 'subscribe_button_text': '✅ 已订阅' if status in ('created','exists') else '处理中...'}), ensure_ascii=False))
        return

    mark_state(key, {'success': True, 'status': 'processing', 'message': '正在处理中'})

    cred = load_cred(args.channel, args.user_id)
    token = cred.get('token')
    base = cred.get('base_url') or os.getenv('MP_DEFAULT_BASE_URL') or DEFAULT_BASE
    if not token:
        raise SystemExit('missing movipilot token')

    mediaid = f'tmdb:{tmdb_id}'
    sub = mp_get(f"{base}/api/v1/subscribe/media/{parse.quote(mediaid)}?token={parse.quote(token)}")
    if sub and sub.get('id'):
        result = pack_result(success=True, deduped=False, status='exists', subscribe_id=sub.get('id'), message='已存在订阅', ui={'subscribe_disabled': True, 'subscribe_button_text': '✅ 已订阅'})
        mark_state(key, result)
        print(json.dumps(result, ensure_ascii=False))
        return

    type_name = '电影' if media_type == 'movie' else '电视剧'

    # Fast path: create subscription directly from callback payload (avoid extra media lookup latency)
    create_payload = {
        'name': payload.get('title') or '',
        'year': '',
        'type': type_name,
        'tmdbid': int(tmdb_id),
        'mediaid': mediaid,
        'season': None,
    }
    resp = mp_post(f"{base}/api/v1/subscribe/?token={parse.quote(token)}", create_payload)

    # Fallback path: if direct create rejected, fetch media details then retry once
    if not resp.get('success'):
        media = mp_get(f"{base}/api/v1/media/{parse.quote(mediaid)}?type_name={parse.quote(type_name)}&token={parse.quote(token)}")
        create_payload = {
            'name': media.get('title') or payload.get('title') or '',
            'year': str(media.get('year') or ''),
            'type': type_name,
            'tmdbid': int(tmdb_id),
            'mediaid': mediaid,
            'season': None,
        }
        resp = mp_post(f"{base}/api/v1/subscribe/?token={parse.quote(token)}", create_payload)
        if not resp.get('success'):
            raise RuntimeError(f'create subscribe failed: {resp}')

    sid = (resp.get('data') or {}).get('id')
    result = pack_result(success=True, deduped=False, status='created', subscribe_id=sid, message='新增订阅成功', ui={'subscribe_disabled': True, 'subscribe_button_text': '✅ 已订阅'})
    mark_state(key, result)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    try:
        main()
    except error.HTTPError as ex:
        raw = ex.read().decode('utf-8', errors='replace')
        print(json.dumps(pack_result(success=False, status='failed', message='订阅失败，可重试', ui={'subscribe_disabled': False, 'subscribe_button_text': '订阅失败，重试'}, error=f'HTTP {ex.code}: {raw[:200]}'), ensure_ascii=False))
        raise
    except Exception as ex:
        print(json.dumps(pack_result(success=False, status='failed', message='订阅失败，可重试', ui={'subscribe_disabled': False, 'subscribe_button_text': '订阅失败，重试'}, error=str(ex)), ensure_ascii=False))
        raise
