#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path
from urllib import request
from card_snapshot_store import find_snapshot_by_card_key, patch_subscribe_button

ENQUEUE = Path('/root/.openclaw/workspace-dev/skills/feishu-card-sender/scripts/enqueue_callback.py')

SCRIPT_DIR = Path(__file__).resolve().parent
HANDLER = SCRIPT_DIR / "subscribe_callback_handler.py"
OPENCLAW_CONFIG = Path('/root/.openclaw/openclaw.json')
TOKEN_CACHE = Path('/root/.openclaw/workspace-dev/skills/feishu-card-sender/tmp/tenant_token_cache.json')


def load_app_credentials(account_id: str | None):
    cfg = json.loads(OPENCLAW_CONFIG.read_text(encoding='utf-8'))
    accounts = (((cfg.get('channels') or {}).get('feishu') or {}).get('accounts') or [])
    if not accounts:
        return None, None
    if account_id is not None:
        for a in accounts:
            if str(a.get('id')) == str(account_id):
                return a.get('appId'), a.get('appSecret')
        if str(account_id).isdigit():
            idx = int(str(account_id))
            if 0 <= idx < len(accounts):
                a = accounts[idx]
                return a.get('appId'), a.get('appSecret')
    a = accounts[0]
    return a.get('appId'), a.get('appSecret')


def get_tenant_token(app_id: str, app_secret: str):
    body = json.dumps({'app_id': app_id, 'app_secret': app_secret}).encode('utf-8')
    req = request.Request('https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal', data=body, method='POST', headers={'Content-Type': 'application/json'})
    with request.urlopen(req, timeout=20) as resp:
        data = json.loads(resp.read().decode('utf-8'))
    return data.get('tenant_access_token'), int(data.get('expire', 7200))


def get_tenant_token_cached(app_id: str, app_secret: str):
    now = __import__('time').time()
    try:
        if TOKEN_CACHE.exists():
            c = json.loads(TOKEN_CACHE.read_text(encoding='utf-8'))
            if c.get('app_id') == app_id and c.get('token') and float(c.get('exp_at', 0)) - now > 120:
                return c['token']
    except Exception:
        pass

    token, ttl = get_tenant_token(app_id, app_secret)
    if token:
        TOKEN_CACHE.parent.mkdir(parents=True, exist_ok=True)
        TOKEN_CACHE.write_text(json.dumps({'app_id': app_id, 'token': token, 'exp_at': now + max(300, ttl - 60)}), encoding='utf-8')
    return token


def update_message_card_by_id(message_id: str, tenant_token: str, raw_card_json: str):
    card = json.loads(raw_card_json)
    payload = {
        'msg_type': 'interactive',
        'content': json.dumps(card, ensure_ascii=False),
    }
    req = request.Request(
        f'https://open.feishu.cn/open-apis/im/v1/messages/{message_id}',
        data=json.dumps(payload, ensure_ascii=False).encode('utf-8'),
        method='PATCH',
        headers={'Authorization': f'Bearer {tenant_token}', 'Content-Type': 'application/json'},
    )
    with request.urlopen(req, timeout=20) as resp:
        body = resp.read().decode('utf-8', errors='replace')
        try:
            return json.loads(body)
        except Exception:
            return {'raw': body}


def main():
    p = argparse.ArgumentParser(description='Route Feishu card callback payloads')
    p.add_argument('--payload', required=True, help='raw callback payload json')
    p.add_argument('--channel', default='feishu')
    p.add_argument('--user-id', required=True)
    p.add_argument('--message-id', help='Inbound message_id, e.g. card-action-c-xxx')
    p.add_argument('--account-id', help='Feishu account id/index for app credentials')
    args = p.parse_args()

    try:
        payload = json.loads(args.payload)
    except Exception:
        print(json.dumps({'success': False, 'error': 'invalid_json'}, ensure_ascii=False))
        return 2

    action = payload.get('action')
    if action != 'subscribe':
        print(json.dumps({'success': False, 'error': 'unsupported_action', 'action': action}, ensure_ascii=False))
        return 2

    callback_token = None
    if args.message_id:
        mid = args.message_id.strip()
        if mid.startswith('card-action-'):
            callback_token = mid[len('card-action-'):]

    tenant_token = None
    app_id, app_secret = load_app_credentials(args.account_id)
    if app_id and app_secret:
        try:
            tenant_token = get_tenant_token_cached(app_id, app_secret)
        except Exception:
            tenant_token = None

    card_key = str(payload.get('card_key') or '')
    snapshot = None
    if card_key:
        snapshot = find_snapshot_by_card_key(card_key)

    message_id_for_update = (snapshot or {}).get('message_id') if isinstance(snapshot, dict) else None

    processing_update = None
    processing_update_error = None
    if message_id_for_update and tenant_token and snapshot:
        try:
            processing_card = patch_subscribe_button(snapshot['raw_card_json'], text='处理中...', disabled=True)
            processing_update = update_message_card_by_id(message_id_for_update, tenant_token, processing_card)
        except Exception as ex:
            processing_update_error = str(ex)

    # Queue finalize job (subscribe + final patch)
    enqueue_res = subprocess.run([
        'python3', str(ENQUEUE),
        '--channel', args.channel,
        '--user-id', args.user_id,
        '--account-id', str(args.account_id or '1'),
        '--message-id', args.message_id or '',
        '--payload', json.dumps(payload, ensure_ascii=False),
    ], capture_output=True, text=True)

    out = {
        'success': True,
        'status': 'processing',
        'message': '正在处理中，请稍候',
        'debug_update': {
            'processing': processing_update,
            'processing_error': processing_update_error,
            'has_snapshot': bool(snapshot),
            'callback_token': bool(callback_token),
            'message_id': message_id_for_update,
            'enqueued': enqueue_res.returncode == 0,
            'enqueue_stdout': (enqueue_res.stdout or '').strip(),
            'enqueue_stderr': (enqueue_res.stderr or '').strip(),
        }
    }
    print(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
