#!/usr/bin/env python3
import argparse, json, subprocess, time
from pathlib import Path
from urllib import request
from card_snapshot_store import find_snapshot_by_card_key, patch_subscribe_button

OPENCLAW_CONFIG = Path('/root/.openclaw/openclaw.json')
HANDLER = Path('/root/.openclaw/workspace-dev/skills/feishu-card-sender/scripts/subscribe_callback_handler.py')
METRIC_LOG = Path('/root/.openclaw/workspace-dev/skills/feishu-card-sender/tmp/callback-metrics.jsonl')


def load_app_credentials(account_id):
    cfg = json.loads(OPENCLAW_CONFIG.read_text(encoding='utf-8'))
    accounts = (((cfg.get('channels') or {}).get('feishu') or {}).get('accounts') or [])
    if not accounts:
        return None, None
    if account_id is not None:
        for a in accounts:
            if str(a.get('id')) == str(account_id):
                return a.get('appId'), a.get('appSecret')
        if str(account_id).isdigit():
            idx = int(account_id)
            if 0 <= idx < len(accounts):
                a = accounts[idx]
                return a.get('appId'), a.get('appSecret')
    a = accounts[0]
    return a.get('appId'), a.get('appSecret')


def get_tenant_token(app_id, app_secret):
    body = json.dumps({'app_id': app_id, 'app_secret': app_secret}).encode()
    req = request.Request('https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal', data=body, method='POST', headers={'Content-Type':'application/json'})
    with request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode()).get('tenant_access_token')


def patch_message(message_id, token, raw_card_json):
    payload = {'msg_type':'interactive','content':json.dumps(json.loads(raw_card_json), ensure_ascii=False)}
    req = request.Request(f'https://open.feishu.cn/open-apis/im/v1/messages/{message_id}', data=json.dumps(payload, ensure_ascii=False).encode(), method='PATCH', headers={'Authorization':f'Bearer {token}','Content-Type':'application/json'})
    with request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode())


def log_metric(d):
    METRIC_LOG.parent.mkdir(parents=True, exist_ok=True)
    with METRIC_LOG.open('a', encoding='utf-8') as f:
        f.write(json.dumps(d, ensure_ascii=False) + '\n')


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--payload', required=True)
    ap.add_argument('--channel', default='feishu')
    ap.add_argument('--user-id', required=True)
    ap.add_argument('--account-id', default='1')
    args=ap.parse_args()

    t0=time.time()
    p=json.loads(args.payload)
    card_key=str(p.get('card_key') or '')
    snap=find_snapshot_by_card_key(card_key)
    if not snap:
        log_metric({'ok':False,'stage':'snapshot_missing','card_key':card_key,'t':time.time()})
        return 1

    app_id, app_secret = load_app_credentials(args.account_id)
    token = get_tenant_token(app_id, app_secret)

    t1=time.time()
    res=subprocess.run(['python3', str(HANDLER), '--channel', args.channel, '--user-id', args.user_id, '--payload', args.payload], capture_output=True, text=True)
    out={}
    try:
        out=json.loads((res.stdout or '').strip() or '{}')
    except Exception:
        out={'success':False}
    t2=time.time()

    ok=bool(out.get('success'))
    final=patch_subscribe_button(snap['raw_card_json'], text='✅ 已订阅' if ok else '订阅失败，重试', disabled=True if ok else False)
    patch_resp=patch_message(snap['message_id'], token, final)
    t3=time.time()

    log_metric({
        'ok':ok,
        'card_key':card_key,
        'tmdb_id':p.get('tmdb_id'),
        'media_type':p.get('media_type'),
        't_click':t0,
        't_subscribe_done':t2,
        't_final_patch_done':t3,
        'dt_subscribe_ms':int((t2-t1)*1000),
        'dt_total_ms':int((t3-t0)*1000),
        'patch_resp':patch_resp,
    })
    return 0

if __name__=='__main__':
    raise SystemExit(main())
