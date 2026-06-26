#!/usr/bin/env python3
"""
Bollinger Bands Auto-Trade
Safe export version - uses env vars only
"""
import requests
import json
import time
import os
import hmac
import hashlib
from datetime import datetime

BASE_URL = "https://fapi.binance.com"
SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XAUUSDT", "XAGUSDT"]
FEE = 0.0004

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

POSITION_PCT = 0.20
MIN_POSITION = 20
MAX_POSITION = 50

def get_signature(query_string):
    return hmac.new(API_SECRET.encode(), query_string.encode(), hashlib.sha256).hexdigest()

def futures_request(method, endpoint, params=None):
    params = params or {}
    params['timestamp'] = int(time.time() * 1000)
    params['recvWindow'] = 5000
    query = '&'.join([f"{k}={v}" for k, v in params.items()])
    signature = get_signature(query)
    url = f"{BASE_URL}{endpoint}?{query}&signature={signature}"
    headers = {'X-MBX-APIKEY': API_KEY}
    if method == 'GET':
        r = requests.get(url, headers=headers, timeout=10)
    elif method == 'POST':
        r = requests.post(url, headers=headers, timeout=10)
    elif method == 'DELETE':
        r = requests.delete(url, headers=headers, timeout=10)
    return r.json()

def get_balance():
    data = futures_request('GET', '/fapi/v2/account')
    return float(data.get('availableBalance', 0))

def get_positions():
    data = futures_request('GET', '/fapi/v2/account')
    positions = []
    for pos in data.get('positions', []):
        if float(pos.get('notional', 0)) != 0:
            positions.append(pos)
    return positions

def send_telegram(message):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print(f"📱 {message}")
        return False
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}
        requests.post(url, data=data, timeout=10)
        return True
    except:
        print(f"📱 {message}")
        return False

def place_order(symbol, side, quantity):
    return futures_request('POST', '/fapi/v1/order', {
        'symbol': symbol,
        'side': side,
        'type': 'MARKET',
        'quantity': str(quantity),
    })

def close_position(symbol, quantity):
    return futures_request('POST', '/fapi/v1/order', {
        'symbol': symbol,
        'side': 'SELL' if quantity > 0 else 'BUY',
        'type': 'MARKET',
        'quantity': str(abs(quantity)),
    })

def fetch_klines(symbol, interval="5m", limit=100):
    url = f"{BASE_URL}/fapi/v1/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    r = requests.get(url, params=params, timeout=10)
    data = r.json()
    ohlc = []
    for k in data:
        ohlc.append({
            "open": float(k[1]), "high": float(k[2]), "low": float(k[3]),
            "close": float(k[4]), "volume": float(k[5]), "time": int(k[0])
        })
    return ohlc

def calc_bollinger(data, period=20, std_dev=2):
    upper, middle, lower = [], [], []
    for i in range(len(data)):
        if i < period - 1:
            upper.append(None); middle.append(None); lower.append(None)
        else:
            window = data[i-period+1:i+1]
            sma = sum(window) / period
            variance = sum((x - sma) ** 2 for x in window) / period
            std = variance ** 0.5
            middle.append(sma)
            upper.append(sma + std_dev * std)
            lower.append(sma - std_dev * std)
    return upper, middle, lower

def calc_atr(highs, lows, closes, period=14):
    tr = []
    for i in range(1, len(highs)):
        high, low, close_prev = highs[i], lows[i], closes[i-1]
        tr.append(max(high - low, abs(high - close_prev), abs(low - close_prev)))
    if len(tr) < period:
        return [0] * len(tr)
    atr = []
    for i in range(len(tr)):
        if i < period - 1:
            atr.append(sum(tr[:i+1]) / (i+1) if i > 0 else tr[0])
        else:
            atr.append(sum(tr[i-period+1:i+1]) / period)
    return atr

def get_signal(closes, highs, lows, upper_bb, lower_bb, atr):
    price = closes[-1]
    upper = upper_bb[-1]
    lower = lower_bb[-1]
    atr_val = atr[-1] if atr and atr[-1] else 0
    
    bb_range = upper - lower
    touch_threshold_lower = lower + bb_range * 0.05
    touch_threshold_upper = upper - bb_range * 0.05
    
    if price <= touch_threshold_lower:
        sl = price - 1.5 * atr_val if atr_val else price * 0.98
        tp = price + 2.0 * atr_val if atr_val else price * 1.04
        return "BUY", {"sl": sl, "tp": tp, "reason": f"Price ${price:.2f} at lower BB ${lower:.2f}"}
    
    elif price >= touch_threshold_upper:
        sl = price + 1.5 * atr_val if atr_val else price * 1.02
        tp = price - 2.0 * atr_val if atr_val else price * 0.96
        return "SELL", {"sl": sl, "tp": tp, "reason": f"Price ${price:.2f} at upper BB ${upper:.2f}"}
    
    return None, None

def analyze_all():
    results = {}
    for sym in SYMBOLS:
        klines = fetch_klines(sym)
        closes = [k["close"] for k in klines]
        highs = [k["high"] for k in klines]
        lows = [k["low"] for k in klines]
        
        upper_bb, middle_bb, lower_bb = calc_bollinger(closes)
        atr = calc_atr(highs, lows, closes)
        
        signal, params = get_signal(closes, highs, lows, upper_bb, lower_bb, atr)
        price = closes[-1]
        
        results[sym] = {
            "price": price,
            "bb_upper": upper_bb[-1] if upper_bb[-1] else 0,
            "bb_lower": lower_bb[-1] if lower_bb[-1] else 0,
            "bb_middle": middle_bb[-1] if middle_bb[-1] else 0,
            "atr": atr[-1] if atr and atr[-1] else 0,
            "signal": signal,
            "sl": params["sl"] if params else None,
            "tp": params["tp"] if params else None,
            "reason": params["reason"] if params else None,
        }
    return results

def run_cycle():
    balance = get_balance()
    positions = get_positions()
    
    print(f"\n{'='*60}")
    print(f"📊 BOLLINGER BANDS AUTO-TRADE")
    print(f"{'='*60}")
    print(f"💰 Balance: ${balance:.2f}")
    print(f"📊 Positions: {len(positions)}")
    
    # Check existing positions
    for pos in positions:
        sym = pos['symbol']
        qty = float(pos['positionAmt'])
        entry = float(pos['entryPrice'])
        
        try:
            ticker = requests.get(f"{BASE_URL}/fapi/v1/ticker/price", 
                params={"symbol": sym}, timeout=10).json()
            current_price = float(ticker['price'])
        except:
            current_price = entry
        
        if qty > 0:  # LONG
            sl_price = entry * 0.995
            tp_price = entry * 1.02
            pnl_pct = (current_price / entry - 1) * 100
            
            closed = False
            reason = ""
            if current_price <= sl_price:
                reason = f"SL HIT (${sl_price:.2f})"
                closed = True
            elif current_price >= tp_price:
                reason = f"TP HIT (${tp_price:.2f})"
                closed = True
            
            if closed:
                close_position(sym, qty)
                send_telegram(f"🎯 <b>POSITION CLOSED</b>\n{sym} LONG\nEntry: ${entry:.2f}\nExit: ${current_price:.2f}\nReason: {reason}\nP&L: {pnl_pct:+.2f}%")
                print(f"  🎯 Closed {sym} LONG @ ${current_price:.2f} ({pnl_pct:+.2f}%)")
            else:
                print(f"  📍 {sym} LONG: Entry ${entry:.2f} | Current ${current_price:.2f} | P&L {pnl_pct:+.2f}%")
        else:  # SHORT
            sl_price = entry * 1.005
            tp_price = entry * 0.98
            pnl_pct = (1 - current_price / entry) * 100
            
            closed = False
            reason = ""
            if current_price >= sl_price:
                reason = f"SL HIT (${sl_price:.2f})"
                closed = True
            elif current_price <= tp_price:
                reason = f"TP HIT (${tp_price:.2f})"
                closed = True
            
            if closed:
                close_position(sym, abs(qty))
                send_telegram(f"🎯 <b>POSITION CLOSED</b>\n{sym} SHORT\nEntry: ${entry:.2f}\nExit: ${current_price:.2f}\nReason: {reason}\nP&L: {pnl_pct:+.2f}%")
                print(f"  🎯 Closed {sym} SHORT @ ${current_price:.2f} ({pnl_pct:+.2f}%)")
            else:
                print(f"  📍 {sym} SHORT: Entry ${entry:.2f} | Current ${current_price:.2f} | P&L {pnl_pct:+.2f}%")
    
    # Scan for new signals
    if not positions:
        results = analyze_all()
        signals_found = [(sym, r) for sym, r in results.items() if r['signal']]
        
        print(f"\n🔍 Scanning...")
        for sym, r in results.items():
            if r['signal']:
                print(f"  ✅ {sym}: {r['signal']} — {r['reason']}")
            else:
                print(f"  ⚪ {sym}: ${r['price']:.2f} (BB middle zone)")
        
        if signals_found:
            sym, r = signals_found[0]
            position_size = max(MIN_POSITION, min(MAX_POSITION, balance * POSITION_PCT))
            quantity = round(position_size / r['price'], 3)
            
            if quantity >= 0.001:
                result = place_order(sym, r['signal'], quantity)
                if 'orderId' in result:
                    msg = f"🚀 <b>BOLLINGER BANDS SIGNAL</b>\n\n"
                    msg += f"{sym} {r['signal']}\n"
                    msg += f"Entry: ${r['price']:.4f}\n"
                    msg += f"SL: ${r['sl']:.4f}\n"
                    msg += f"TP: ${r['tp']:.4f}\n"
                    msg += f"Qty: {quantity}\n"
                    msg += f"Reason: {r['reason']}"
                    send_telegram(msg)
                    print(f"  ✅ Executed {r['signal']} {sym} @ ${r['price']:.2f}")
    
    print(f"\n✅ Cycle complete")

if __name__ == "__main__":
    try:
        run_cycle()
    except Exception as e:
        print(f"Error: {e}")
