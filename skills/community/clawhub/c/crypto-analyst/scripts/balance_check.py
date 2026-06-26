#!/usr/bin/env python3
"""
OKX Account Balance Checker
Requires OKX API Key with read permissions. Uses only public endpoints (no trading).
.env 需要: OKX_API_KEY, OKX_API_SECRET, OKX_API_PASSPHRASE
"""

import sys
import os
import requests
import hmac
import base64
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

def load_env():
    """Load OKX credentials from .env (优先项目根目录，其次脚本目录）"""
    for env_path in [
        os.path.join(PROJECT_ROOT, '.env'),
        os.path.join(SCRIPT_DIR, '.env'),
    ]:
        if os.path.exists(env_path):
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if '=' in line and not line.startswith('#'):
                        k, v = line.split('=', 1)
                        os.environ.setdefault(k.strip(), v.strip())

def get_sign(timestamp: str, method: str, path: str, body: str, secret_key: str) -> str:
    message = timestamp + method + path + body
    mac = hmac.new(secret_key.encode(), message.encode(), digestmod='sha256')
    return base64.b64encode(mac.digest()).decode()

def get_balance(api_key: str, secret_key: str, passphrase: str):
    timestamp = datetime.utcnow().isoformat() + 'Z'
    method = 'GET'
    path = '/api/v5/account/balance'

    headers = {
        'OK-ACCESS-KEY': api_key,
        'OK-ACCESS-SIGN': get_sign(timestamp, method, path, '', secret_key),
        'OK-ACCESS-TIMESTAMP': timestamp,
        'OK-ACCESS-PASSPHRASE': passphrase,
        'Content-Type': 'application/json',
    }

    url = 'https://www.okx.com' + path
    try:
        r = requests.get(url, headers=headers, timeout=15)
        return r.json()
    except Exception as e:
        return {'msg': str(e)}

def main():
    load_env()

    api_key = os.environ.get('OKX_API_KEY')
    secret_key = os.environ.get('OKX_API_SECRET')
    passphrase = os.environ.get('OKX_API_PASSPHRASE', '')

    if not api_key or not secret_key:
        print('请在 .env 文件中配置 OKX_API_KEY、OKX_API_SECRET 和 OKX_API_PASSPHRASE', file=sys.stderr)
        print('（复制 .env.example 为 .env 后填入）', file=sys.stderr)
        sys.exit(1)

    if not passphrase:
        print('请在 .env 中配置 OKX_API_PASSPHRASE', file=sys.stderr)
        sys.exit(1)

    result = get_balance(api_key, secret_key, passphrase)

    if 'msg' in result:
        print(f'错误: {result["msg"]}', file=sys.stderr)
        sys.exit(1)

    data = result.get('data', [])
    if not data:
        print('无账户数据')
        sys.exit(1)

    for acct in data:
        total_equity = float(acct.get('totalEq', 0))
        print(f'╔══════════════════════════════════════════╗')
        print(f'║           OKX 账户概览                    ║')
        print(f'╠══════════════════════════════════════════╣')
        print(f'║  总权益: ${total_equity:,.2f}                    ║')
        print(f'╠══════════════════════════════════════════╣')

        details = acct.get('details', [])
        if not details:
            print('║  无持仓详情                              ║')
        else:
            for d in details:
                ccy = d.get('ccy', '')
                avail = float(d.get('availBal', 0))
                frozen = float(d.get('frozenBal', 0))
                eq = float(d.get('eq', 0))
                if avail > 0 or frozen > 0 or eq > 0:
                    print(f'║  {ccy:>4} 余额: {avail:.6f}  冻结: {frozen:.6f}    ║')

        print('╚══════════════════════════════════════════╝')

if __name__ == '__main__':
    main()
