#!/usr/bin/env bash
# 检查 CareMax token 状态
# 输出: JSON { "status": "valid|expired|missing", "access_token"?: "...", "base_url"?: "..." }

set -euo pipefail

CREDS_FILE="$HOME/.caremax/credentials.json"

if [ ! -f "$CREDS_FILE" ]; then
  echo '{"status":"missing"}'
  exit 0
fi

python3 -c "
import json, sys
from datetime import datetime

creds = json.load(open('$CREDS_FILE'))
expires_at = creds.get('expires_at', '')

try:
    exp = datetime.fromisoformat(expires_at.replace('Z', '+00:00'))
    now = datetime.now(exp.tzinfo)
    if now < exp:
        print(json.dumps({
            'status': 'valid',
            'access_token': creds['access_token'],
            'base_url': creds.get('base_url', 'https://api.caremax.ai'),
            'expires_at': expires_at,
            'scope': creds.get('scope', '')
        }))
    else:
        print(json.dumps({
            'status': 'expired',
            'refresh_token': creds.get('refresh_token', ''),
            'base_url': creds.get('base_url', 'https://api.caremax.ai')
        }))
except Exception as e:
    print(json.dumps({'status': 'expired', 'refresh_token': creds.get('refresh_token', ''), 'base_url': creds.get('base_url', 'https://api.caremax.ai')}))
"
