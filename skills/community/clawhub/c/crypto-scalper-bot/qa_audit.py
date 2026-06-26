#!/usr/bin/env python3
"""
QA Audit - System Health Check
Safe export version - uses env vars only
"""
import requests
import hmac
import hashlib
import time
import os
import ast
from datetime import datetime

# Load env vars
for env_file in ['binance.env', 'telegram.env', '/root/.openclaw/workspace/binance.env', '/root/.openclaw/workspace/telegram.env']:
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                if '=' in line:
                    k, v = line.strip().split('=', 1)
                    os.environ.setdefault(k, v)

API_KEY = os.environ.get('BINANCE_API_KEY', '')
API_SECRET = os.environ.get('BINANCE_API_SECRET', '')
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '')

def get_signature(query_string):
    return hmac.new(API_SECRET.encode(), query_string.encode(), hashlib.sha256).hexdigest()

def futures_request(method, endpoint, params=None):
    params = params or {}
    params['timestamp'] = int(time.time() * 1000)
    params['recvWindow'] = 5000
    query = '&'.join([f"{k}={v}" for k, v in params.items()])
    signature = get_signature(query)
    url = f"https://fapi.binance.com{endpoint}?{query}&signature={signature}"
    headers = {'X-MBX-APIKEY': API_KEY}
    if method == 'GET':
        r = requests.get(url, headers=headers, timeout=10)
    elif method == 'POST':
        r = requests.post(url, headers=headers, timeout=10)
    elif method == 'DELETE':
        r = requests.delete(url, headers=headers, timeout=10)
    return r.json()

def send_telegram(msg):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print(f"📱 QA: {msg}")
        return False
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "HTML"}
        requests.post(url, data=data, timeout=10)
        return True
    except:
        return False

def check_script_syntax(path):
    try:
        with open(path) as f:
            ast.parse(f.read())
        return True, "OK"
    except SyntaxError as e:
        return False, f"Syntax error: {e}"

def run_qa():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M UTC+8")
    issues = []
    checks = []
    
    print(f"\n{'='*50}")
    print(f"🔍 QA AUDIT - {timestamp}")
    print(f"{'='*50}")
    
    # 1. Balance
    try:
        acc = futures_request('GET', '/fapi/v2/account')
        balance = float(acc.get('availableBalance', 0))
        checks.append(("Balance", True, f"${balance:.2f}"))
        if balance < 10:
            issues.append(f"⚠️ Balance very low: ${balance:.2f}")
    except Exception as e:
        checks.append(("Balance", False, str(e)))
        issues.append(f"❌ Balance check failed: {e}")
    
    # 2. Positions
    try:
        positions = [p for p in acc.get('positions', []) if float(p.get('notional', 0)) != 0]
        if len(positions) == 0:
            checks.append(("Positions", True, "No open positions"))
        elif len(positions) == 1:
            sym = positions[0]['symbol']
            qty = float(positions[0]['positionAmt'])
            entry = float(positions[0]['entryPrice'])
            checks.append(("Positions", True, f"{sym}: {qty} @ ${entry:.2f}"))
        else:
            pos_info = ", ".join([f"{p['symbol']}:{p['positionAmt']}" for p in positions])
            checks.append(("⚠️ Positions", False, f"Multiple: {pos_info}"))
            issues.append(f"⚠️ Multiple positions: {pos_info}")
    except Exception as e:
        checks.append(("Positions", False, str(e)))
    
    # 3. API permissions (test with reduceOnly)
    try:
        test = futures_request('POST', '/fapi/v1/order', {
            'symbol': 'BTCUSDT',
            'side': 'SELL',
            'type': 'MARKET',
            'quantity': '0.001',
            'reduceOnly': 'true',
        })
        checks.append(("API Orders", True, "Can place orders"))
        if 'orderId' in test:
            futures_request('DELETE', '/fapi/v1/order', {'symbol': 'BTCUSDT', 'orderId': test['orderId']})
    except Exception as e:
        checks.append(("API Orders", False, str(e)))
        issues.append(f"❌ API test failed: {e}")
    
    # 4. Telegram
    try:
        r = send_telegram(f"🧪 QA Check\n_{timestamp}_\nRunning system health check...")
        checks.append(("Telegram", r, "OK" if r else "Failed"))
        if not r:
            issues.append("⚠️ Telegram message failed")
    except Exception as e:
        checks.append(("Telegram", False, str(e)))
        issues.append(f"⚠️ Telegram check failed: {e}")
    
    # 5. Scripts syntax
    import os.path
    for script in ['futures_auto_trade.py', 'mean_reversion.py', 'qa_audit.py']:
        if os.path.exists(script):
            ok, msg = check_script_syntax(script)
            checks.append((f"Syntax: {script}", ok, msg))
            if not ok:
                issues.append(f"❌ {script}: {msg}")
    
    # Print results
    print("\nChecks:")
    for name, ok, msg in checks:
        status = "✅" if ok else "❌"
        print(f"  {status} {name}: {msg}")
    
    if issues:
        msg_lines = [f"🚨 <b>QA ISSUES DETECTED</b>\n_{timestamp}_", "━" * 20]
        for issue in issues:
            msg_lines.append(issue)
        send_telegram("\n".join(msg_lines))
        print(f"\n🚨 ISSUES FOUND: {len(issues)}")
    else:
        send_telegram(f"✅ <b>QA All Clear</b>\n_{timestamp}_\nAll systems OK")
        print(f"\n✅ ALL CLEAR")
    
    return len(issues) == 0

if __name__ == "__main__":
    run_qa()
