#!/usr/bin/env bash
set -euo pipefail

STATE_DIR="${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"
MAIN_AUTH="$STATE_DIR/agents/main/agent/auth-profiles.json"
SNAPSHOT_DIR="$STATE_DIR/auth-snapshots"
BACKUP_DIR="$SNAPSHOT_DIR/backups"
PENDING_FILE="$STATE_DIR/cs-add.pending.json"
CLIENT_ID="${CS_OAUTH_CLIENT_ID:-app_EMoamEEZ73f0CkXaXp7hrann}"
AUTHORIZE_URL="${CS_OAUTH_AUTHORIZE_URL:-https://auth.openai.com/oauth/authorize}"
TOKEN_URL="${CS_OAUTH_TOKEN_URL:-https://auth.openai.com/oauth/token}"
REDIRECT_URI="${CS_OAUTH_REDIRECT_URI:-http://localhost:1455/auth/callback}"
SCOPE="${CS_OAUTH_SCOPE:-openid profile email offline_access}"
ORIGINATOR="${CS_OAUTH_ORIGINATOR:-pi}"
mkdir -p "$SNAPSHOT_DIR" "$BACKUP_DIR"

usage() {
    cat <<'EOF'
Usage: cs [command] [args]
  switch <alias>              Switch active creds to snapshot <alias>
  list                        List snapshots with email + expiry
  current                     Show current active email
  quota                       Check usage quota for current email
  refresh <alias>             Force refresh a specific snapshot
  refresh-all                 Auto-refresh snapshots expiring within 24h
  add                         Start OAuth login flow, alias auto-derived from email on apply
  add <alias>                 Start OAuth login flow for a new account using explicit alias
  add --apply <callback> [alias]
                              Finish OAuth login and save new snapshot
EOF
}

backup_file() {
    local src="$1"
    [ -f "$src" ] || return 0
    local ts base out
    ts="$(date +%Y%m%d-%H%M%S)"
    base="$(basename "$src")"
    out="$BACKUP_DIR/${base}.${ts}.bak"
    cp "$src" "$out"
    echo "$out"
}

validate_alias() {
    local alias="$1"
    [ -n "$alias" ] || { echo "[ERR] alias is empty" >&2; return 1; }
    case "$alias" in
        *..*|*/*|*.json|*.bak|.*)
            echo "[ERR] invalid alias: $alias" >&2; return 1 ;;
    esac
    if ! printf '%s' "$alias" | grep -Eq '^[a-zA-Z0-9._-]+$'; then
        echo "[ERR] invalid alias: $alias" >&2; return 1
    fi
}

normalize_alias() {
    python3 - "$1" <<'PY'
import re, sys
s=sys.argv[1].strip().lower()
s=s.replace('@','-').replace(' ','-')
s=re.sub(r'[^a-z0-9._-]+','-',s)
s=re.sub(r'-+','-',s).strip('-')
print(s or 'account')
PY
}

start_add() {
    local alias="${1:-}"
    python3 - "$PENDING_FILE" "$alias" "$CLIENT_ID" "$AUTHORIZE_URL" "$REDIRECT_URI" "$SCOPE" "$ORIGINATOR" <<'PY'
import base64, hashlib, json, secrets, sys, time
from urllib.parse import urlencode
pending_path, alias, client_id, auth_url, redirect_uri, scope, originator = sys.argv[1:8]
raw = secrets.token_urlsafe(64)
verifier = raw.replace('=', '')
challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).decode().rstrip('=')
state = secrets.token_hex(16)
params = {
  'response_type': 'code',
  'client_id': client_id,
  'redirect_uri': redirect_uri,
  'scope': scope,
  'code_challenge': challenge,
  'code_challenge_method': 'S256',
  'state': state,
  'id_token_add_organizations': 'true',
  'codex_cli_simplified_flow': 'true',
  'originator': originator,
}
obj = {
  'alias': alias,
  'client_id': client_id,
  'redirect_uri': redirect_uri,
  'verifier': verifier,
  'state': state,
  'created_at': int(time.time() * 1000),
}
with open(pending_path, 'w', encoding='utf-8') as f:
  json.dump(obj, f, ensure_ascii=False, indent=2)
  f.write('\n')
print(auth_url + '?' + urlencode(params))
PY
}

finish_add() {
    local callback="$1"
    local explicit_alias="${2:-}"
    python3 - "$PENDING_FILE" "$callback" "$explicit_alias" "$TOKEN_URL" "$SNAPSHOT_DIR" <<'PY'
import base64, json, os, re, sys, tempfile, time
from urllib.parse import parse_qs, urlparse, urlencode
from urllib.request import Request, urlopen
pending_path, callback_input, explicit_alias, token_url, snapdir = sys.argv[1:6]
pending=json.load(open(pending_path, encoding='utf-8'))

def parse_callback(value):
    s=value.strip()
    u=urlparse(s)
    q=parse_qs(u.query)
    code=(q.get('code') or [None])[0]
    state=(q.get('state') or [None])[0]
    return code, state

def normalize_alias(value):
    s=(value or '').strip().lower().replace('@','-')
    s=re.sub(r'[^a-z0-9._-]+','-', s)
    s=re.sub(r'-+','-', s).strip('-')
    return s or 'account'

code, state = parse_callback(callback_input)
if not code:
    raise SystemExit('[ERR] callback missing authorization code')
if state != pending.get('state'):
    raise SystemExit('[ERR] oauth state mismatch')
body=urlencode({
    'grant_type':'authorization_code',
    'client_id':pending['client_id'],
    'code':code,
    'code_verifier':pending['verifier'],
    'redirect_uri':pending['redirect_uri'],
}).encode()
req=Request(token_url, data=body, method='POST', headers={
    'Content-Type':'application/x-www-form-urlencoded',
    'Accept':'application/json',
    'User-Agent':'cs/1.0'
})
with urlopen(req, timeout=30) as resp:
    data=json.loads(resp.read().decode('utf-8','replace'))
access=str(data.get('access_token','')).strip()
refresh=str(data.get('refresh_token','')).strip()
expires_in=int(data.get('expires_in',0) or 0)
if not access or not refresh or not expires_in:
    raise SystemExit('[ERR] token exchange response missing fields')
payload_b64 = access.split('.')[1]
payload_b64 += '=' * (-len(payload_b64) % 4)
payload = json.loads(base64.urlsafe_b64decode(payload_b64.encode()).decode())
auth_claim = payload.get('https://api.openai.com/auth', {}) if isinstance(payload, dict) else {}
profile_claim = payload.get('https://api.openai.com/profile', {}) if isinstance(payload, dict) else {}
account_id = str(auth_claim.get('chatgpt_account_id', '')).strip()
email = str(profile_claim.get('email', '')).strip()
alias = explicit_alias.strip() if explicit_alias.strip() else (pending.get('alias') or '').strip()
if not alias:
    alias = normalize_alias(email)
minimal = {
    'access': access,
    'refresh': refresh,
    'expires': int(time.time() * 1000 + expires_in * 1000),
    'accountId': account_id,
}
os.makedirs(snapdir, exist_ok=True)
out=os.path.join(snapdir, alias + '.json')
fd, tmp = tempfile.mkstemp(prefix='snapshot.', suffix='.json', dir=snapdir)
os.close(fd)
with open(tmp,'w',encoding='utf-8') as f:
    json.dump(minimal, f, ensure_ascii=False, indent=2)
    f.write('\n')
os.replace(tmp, out)
print(json.dumps({'path': out, 'alias': alias, 'email': email}, ensure_ascii=False))
PY
    rm -f "$PENDING_FILE"
}

case "${1:-}" in
    switch)
        [ -z "${2:-}" ] && { echo "Usage: cs switch <alias>"; exit 1; }
        alias="$2"
        validate_alias "$alias"
        [ ! -f "$SNAPSHOT_DIR/$alias.json" ] && { echo "[ERR] Snapshot $alias not found"; exit 1; }
        backup_file "$MAIN_AUTH" >/dev/null
        python3 - "$MAIN_AUTH" "$SNAPSHOT_DIR/$alias.json" <<'PY'
import json, sys, tempfile, os
main, snap = sys.argv[1:3]
data = json.load(open(main, 'r', encoding='utf-8'))
snap_data = json.load(open(snap, 'r', encoding='utf-8'))
prof = data.setdefault('profiles', {}).setdefault('openai-codex:default', {'type': 'oauth', 'provider': 'openai-codex'})
prof.update(snap_data)
data.setdefault('lastGood', {})['openai-codex'] = 'openai-codex:default'
fd, tmp = tempfile.mkstemp(prefix='auth-profiles.', suffix='.json', dir=os.path.dirname(main))
os.close(fd)
with open(tmp, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write('\n')
os.replace(tmp, main)
print(f'[OK] Switched: {snap}')
PY
        echo '---'
        "$0" current
        echo '---'
        "$0" quota
        ;;
    list)
        python3 - "$SNAPSHOT_DIR" <<'PY'
import json, os, sys, time, base64
snapdir = sys.argv[1]
now = int(time.time() * 1000)
print('{:<24} {:<28} {:<12}'.format('ALIAS', 'EMAIL', 'EXPIRES IN'))
print('-' * 70)
for f in sorted(os.listdir(snapdir)):
    if not f.endswith('.json'):
        continue
    path=os.path.join(snapdir,f)
    try:
        data=json.load(open(path,'r',encoding='utf-8'))
        access=data.get('access','')
        exp=data.get('expires',0) or 0
        email='-'
        if access.count('.') >= 2:
            payload=access.split('.')[1]
            payload += '=' * (-len(payload) % 4)
            obj=json.loads(base64.urlsafe_b64decode(payload.encode()).decode())
            email=((obj.get('https://api.openai.com/profile') or {}).get('email') or '-')
        diff=(int(exp)-now)/3600000 if exp else None
        status=f'{diff:.1f}h' if diff is not None and diff > 0 else 'EXPIRED'
        print(f'{f[:-5]:<24} {email:<28} {status:<12}')
    except Exception:
        print('{:<24} {:<28} {:<12}'.format(f[:-5], '-', 'BROKEN'))
PY
        ;;
    current)
        python3 - "$MAIN_AUTH" <<'PY'
import json, sys, base64
try:
    data = json.load(open(sys.argv[1], 'r', encoding='utf-8'))
    prof = data.get('profiles', {}).get('openai-codex:default', {})
    email = 'None'
    access = prof.get('access','')
    if access.count('.') >= 2:
        payload = access.split('.')[1]
        payload += '=' * (-len(payload) % 4)
        obj = json.loads(base64.urlsafe_b64decode(payload.encode()).decode())
        email = ((obj.get('https://api.openai.com/profile') or {}).get('email') or '-')
    print(f'Current active: {email}')
except Exception as e:
    print(f'Error: {e}')
PY
        ;;
    quota)
        python3 - "$MAIN_AUTH" <<'PY'
import json, sys, requests, base64
try:
    data = json.load(open(sys.argv[1], 'r', encoding='utf-8'))
    prof = data.get('profiles', {}).get('openai-codex:default', {})
    access = prof.get('access','')
    if not access:
        raise Exception('No active token')
    email = 'Unknown'
    if access.count('.') >= 2:
        payload = access.split('.')[1]
        payload += '=' * (-len(payload) % 4)
        obj = json.loads(base64.urlsafe_b64decode(payload.encode()).decode())
        email = ((obj.get('https://api.openai.com/profile') or {}).get('email') or '-')
    headers = {
        'Authorization': f'Bearer {access}',
        'ChatGPT-Account-Id': prof.get('accountId', '')
    }
    resp = requests.get('https://chatgpt.com/backend-api/wham/usage', headers=headers, timeout=10)
    resp.raise_for_status()
    res = resp.json()
    print(f"Account: {email}")
    print(f"Plan: {res.get('plan_type', 'FREE').upper()}")
    primary = (res.get('rate_limit') or {}).get('primary_window') or {}
    secondary = (res.get('rate_limit') or {}).get('secondary_window') or {}
    print(f"Hourly: {100 - primary.get('used_percent', 0)}% remaining")
    print(f"Weekly: {100 - secondary.get('used_percent', 0)}% remaining")
except Exception as e:
    print(f'Quota Check Failed: {e}')
PY
        ;;
    refresh)
        [ -z "${2:-}" ] && { echo "Usage: cs refresh <alias>"; exit 1; }
        alias="$2"
        validate_alias "$alias"
        [ -f "$SNAPSHOT_DIR/$alias.json" ] || { echo "[ERR] Snapshot $alias not found"; exit 1; }
        backup_file "$SNAPSHOT_DIR/$alias.json" >/dev/null
        python3 - "$SNAPSHOT_DIR/$alias.json" "$TOKEN_URL" "$CLIENT_ID" <<'PY'
import json, requests, sys, time, tempfile, os
path, token_url, client_id = sys.argv[1:4]
data = json.load(open(path, 'r', encoding='utf-8'))
if not data.get('refresh'):
    raise SystemExit('[ERR] no refresh token')
resp = requests.post(token_url, data={
    'grant_type': 'refresh_token',
    'refresh_token': data['refresh'],
    'client_id': client_id,
}, timeout=15)
resp.raise_for_status()
res = resp.json()
if 'access_token' not in res:
    raise SystemExit(f'[ERR] refresh failed: {res}')
data.update({
    'access': res['access_token'],
    'refresh': res.get('refresh_token', data['refresh']),
    'expires': int(time.time() * 1000) + int(res.get('expires_in', 3600)) * 1000,
})
fd, tmp = tempfile.mkstemp(prefix='snapshot.', suffix='.json', dir=os.path.dirname(path))
os.close(fd)
with open(tmp, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write('\n')
os.replace(tmp, path)
print(f'[OK] Refreshed: {path}')
PY
        ;;
    refresh-all)
        python3 - "$SNAPSHOT_DIR" "$TOKEN_URL" "$CLIENT_ID" "$BACKUP_DIR" <<'PY'
import json, os, sys, time, requests, shutil, tempfile
snapdir, token_url, client_id, backup_dir = sys.argv[1:5]
now = int(time.time() * 1000)
threshold = 24 * 3600 * 1000
os.makedirs(backup_dir, exist_ok=True)
for f in sorted(os.listdir(snapdir)):
    if not f.endswith('.json'):
        continue
    path = os.path.join(snapdir, f)
    alias = f[:-5]
    try:
        data = json.load(open(path, 'r', encoding='utf-8'))
        exp = int(data.get('expires', 0) or 0)
        remaining = exp - now
        if remaining >= threshold:
            print(f'OK {alias} ({remaining // 3600000}h left)')
            continue
        refresh = data.get('refresh')
        if not refresh:
            print(f'FAILED {alias} (no refresh token)')
            continue
        ts=time.strftime('%Y%m%d-%H%M%S', time.localtime())
        shutil.copy2(path, os.path.join(backup_dir, f + '.' + ts + '.bak'))
        resp = requests.post(token_url, data={
            'grant_type': 'refresh_token',
            'refresh_token': refresh,
            'client_id': client_id,
        }, timeout=15)
        resp.raise_for_status()
        res = resp.json()
        access = res.get('access_token')
        if not access:
            print(f'FAILED {alias} (no access_token in response)')
            continue
        data.update({
            'access': access,
            'refresh': res.get('refresh_token', refresh),
            'expires': int(time.time() * 1000) + int(res.get('expires_in', 3600)) * 1000,
        })
        fd, tmp = tempfile.mkstemp(prefix='snapshot.', suffix='.json', dir=os.path.dirname(path))
        os.close(fd)
        with open(tmp, 'w', encoding='utf-8') as fp:
            json.dump(data, fp, ensure_ascii=False, indent=2)
            fp.write('\n')
        os.replace(tmp, path)
        new_remaining = (int(data['expires']) - int(time.time() * 1000)) // 3600000
        print(f'REFRESHED {alias} ({new_remaining}h left)')
    except Exception as e:
        print(f'FAILED {alias} ({e})')
PY
        ;;
    add)
        if [ "${2:-}" = "--apply" ]; then
            [ -z "${3:-}" ] && { echo "Usage: cs add --apply <callback-url> [alias]"; exit 1; }
            alias="${4:-}"
            if [ -n "$alias" ]; then validate_alias "$alias"; fi
            # backup if explicit alias target exists
            if [ -n "$alias" ] && [ -f "$SNAPSHOT_DIR/$alias.json" ]; then backup_file "$SNAPSHOT_DIR/$alias.json" >/dev/null; fi
            finish_add "$3" "$alias"
        else
            alias="${2:-}"
            if [ -n "$alias" ]; then validate_alias "$alias"; fi
            start_add "$alias"
        fi
        ;;
    *)
        usage
        ;;
esac
