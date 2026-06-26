#!/usr/bin/env python3
"""
Futures Auto-Trade - Scalper Strategy
Safe export version - uses env vars only
"""
import asyncio
import os
import sys
import traceback

# Load env vars from files
for env_file in ['binance.env', 'telegram.env', '/root/.openclaw/workspace/binance.env', '/root/.openclaw/workspace/telegram.env']:
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                if '=' in line:
                    k, v = line.strip().split('=', 1)
                    os.environ.setdefault(k, v)

# Use environment variables
API_KEY = os.environ.get('BINANCE_API_KEY', '')
API_SECRET = os.environ.get('BINANCE_API_SECRET', '')
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '')

# Validate credentials
if not API_KEY or not API_SECRET:
    print("❌ Missing BINANCE_API_KEY or BINANCE_API_SECRET")
    print("   Create binance.env file with your credentials")
    sys.exit(1)

import requests
import hmac
import hashlib
import time
from datetime import datetime
from typing import List, Dict, Tuple, Optional

# ============ CONFIG ============
BINANCE_FUTURES_API = "https://fapi.binance.com"

SYMBOLS = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'BNBUSDT', 'XAUUSDT', 'XAGUSDT']
POSITION_PCT = 0.20
MIN_POSITION = 20
MAX_POSITION = 50
SL_PCT = 0.5
TP_PCT = 2.0
RSI_OVERSOLD = 30
RSI_OVERBOUGHT = 70
EMA_FAST = 9
EMA_SLOW = 21
VOLUME_MULTIPLIER = 2.0
FEE = 0.0004

# ============ BINANCE API ============
def get_signature(query_string):
    return hmac.new(API_SECRET.encode(), query_string.encode(), hashlib.sha256).hexdigest()

def futures_api_request(method, endpoint, params=None):
    params = params or {}
    params['timestamp'] = int(time.time() * 1000)
    params['recvWindow'] = 5000
    query = '&'.join([f"{k}={v}" for k, v in params.items()])
    signature = get_signature(query)
    url = f"{BINANCE_FUTURES_API}{endpoint}?{query}&signature={signature}"
    headers = {'X-MBX-APIKEY': API_KEY}
    if method == 'GET':
        r = requests.get(url, headers=headers, timeout=10)
    elif method == 'POST':
        r = requests.post(url, headers=headers, timeout=10)
    elif method == 'DELETE':
        r = requests.delete(url, headers=headers, timeout=10)
    return r.json()

def get_balance():
    data = futures_api_request('GET', '/fapi/v2/account')
    return float(data.get('availableBalance', 0))

def get_positions():
    data = futures_api_request('GET', '/fapi/v2/account')
    positions = []
    for pos in data.get('positions', []):
        if float(pos.get('notional', 0)) != 0:
            positions.append(pos)
    return positions

def place_order(symbol, side, quantity):
    return futures_api_request('POST', '/fapi/v1/order', {
        'symbol': symbol,
        'side': side,
        'type': 'MARKET',
        'quantity': str(quantity),
    })

def close_position(symbol, quantity):
    return futures_api_request('POST', '/fapi/v1/order', {
        'symbol': symbol,
        'side': 'SELL' if quantity > 0 else 'BUY',
        'type': 'MARKET',
        'quantity': str(abs(quantity)),
    })

def set_leverage(symbol, leverage=5):
    return futures_api_request('POST', '/fapi/v1/leverage', {
        'symbol': symbol,
        'leverage': leverage,
    })

def send_telegram(message):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print(f"📱 Telegram: {message}")
        return False
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}
        r = requests.post(url, data=data, timeout=10)
        return r.json().get('ok', False)
    except:
        print(f"📱 Telegram: {message}")
        return False

# ============ DATA ============
def get_futures_klines(symbol, interval="5m", limit=100):
    url = f"{BINANCE_FUTURES_API}/fapi/v1/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    return r.json()

def get_current_price(symbol):
    url = f"{BINANCE_FUTURES_API}/fapi/v1/ticker/price"
    params = {"symbol": symbol}
    r = requests.get(url, params=params, timeout=10)
    return float(r.json()['price'])

def calc_rsi(closes: List[float], period: int = 14) -> Optional[float]:
    if len(closes) < period + 1:
        return None
    deltas = [closes[i] - closes[i-1] for i in range(1, len(closes))]
    gains = [d if d > 0 else 0 for d in deltas[-period:]]
    losses = [-d if d < 0 else 0 for d in deltas[-period:]]
    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period
    if avg_loss == 0:
        return 100
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def calc_ema(closes: List[float], period: int) -> float:
    if len(closes) < period:
        return 0
    k = 2 / (period + 1)
    ema = sum(closes[:period]) / period
    for price in closes[period:]:
        ema = price * k + ema * (1 - k)
    return ema

def calc_avg_volume(volumes: List[float], period: int = 20) -> float:
    if len(volumes) < period:
        return sum(volumes) / len(volumes) if volumes else 0
    return sum(volumes[-period:]) / period

# ============ SIGNALS ============
def get_signal(symbol: str) -> Tuple[Optional[str], Optional[dict]]:
    klines = get_futures_klines(symbol, "5m", 100)
    if len(klines) < 30:
        return None, None
    
    opens = [float(k[1]) for k in klines]
    closes = [float(k[4]) for k in klines]
    volumes = [float(k[5]) for k in klines]
    
    current_price = closes[-1]
    current_rsi = calc_rsi(closes)
    ema_fast = calc_ema(closes, EMA_FAST)
    ema_slow = calc_ema(closes, EMA_SLOW)
    avg_vol = calc_avg_volume(volumes)
    current_vol = volumes[-1]
    
    # Long signal
    if (current_rsi and current_rsi < RSI_OVERSOLD and
        current_price < ema_slow and
        current_vol > avg_vol * VOLUME_MULTIPLIER):
        
        sl_price = current_price * (1 - SL_PCT / 100)
        tp_price = current_price * (1 + TP_PCT / 100)
        return "BUY", {
            'entry': current_price,
            'sl': sl_price,
            'tp': tp_price,
            'rsi': current_rsi
        }
    
    # Short signal
    if (current_rsi and current_rsi > RSI_OVERBOUGHT and
        current_price > ema_slow and
        current_vol > avg_vol * VOLUME_MULTIPLIER):
        
        sl_price = current_price * (1 + SL_PCT / 100)
        tp_price = current_price * (1 - TP_PCT / 100)
        return "SELL", {
            'entry': current_price,
            'sl': sl_price,
            'tp': tp_price,
            'rsi': current_rsi
        }
    
    return None, None

def check_and_close_position(symbol: str, entry_price: float, sl_price: float, tp_price: float, quantity: float):
    current_price = get_current_price(symbol)
    
    # Long position
    if entry_price < current_price:
        if current_price >= tp_price:
            return 'TP', close_position(symbol, quantity)
        if current_price <= sl_price:
            return 'SL', close_position(symbol, quantity)
    
    # Short position
    else:
        if current_price <= tp_price:
            return 'TP', close_position(symbol, abs(quantity))
        if current_price >= sl_price:
            return 'SL', close_position(symbol, abs(quantity))
    
    return None, None

# ============ MAIN ============
async def run_auto_trade_cycle():
    print(f"\n{'='*60}")
    print(f"🤖 FUTURES AUTO-TRADE CYCLE")
    print(f"{'='*60}")
    
    balance = get_balance()
    positions = get_positions()
    
    print(f"💰 Balance: ${balance:.2f}")
    print(f"📊 Open Positions: {len(positions)}")
    
    # Set leverage
    for symbol in SYMBOLS:
        try:
            set_leverage(symbol, 5)
        except:
            pass
    
    # Check existing positions
    for pos in positions:
        sym = pos['symbol']
        qty = float(pos['positionAmt'])
        entry = float(pos['entryPrice'])
        
        current_price = get_current_price(sym)
        print(f"\n📍 {sym}: ${entry:.2f} → Current ${current_price:.2f}")
        
        # Calculate SL/TP
        if qty > 0:
            sl = entry * (1 - SL_PCT / 100)
            tp = entry * (1 + TP_PCT / 100)
        else:
            sl = entry * (1 + SL_PCT / 100)
            tp = entry * (1 - TP_PCT / 100)
        
        reason, result = check_and_close_position(sym, entry, sl, tp, qty)
        
        if reason == 'TP':
            pnl = balance * POSITION_PCT * TP_PCT / 100
            send_telegram(f"🎯 <b>TAKE PROFIT!</b>\n{sym}\nEntry: ${entry:.2f}\nTP: ${tp:.2f}\nP&L: +${pnl:.2f}")
            print(f"  🎯 TP HIT! Closed @ ${current_price:.2f}")
        elif reason == 'SL':
            pnl = -balance * POSITION_PCT * SL_PCT / 100
            send_telegram(f"🛡️ <b>STOP LOSS!</b>\n{sym}\nEntry: ${entry:.2f}\nSL: ${sl:.2f}\nP&L: ${pnl:.2f}")
            print(f"  🛡️ SL HIT! Closed @ ${current_price:.2f}")
    
    # Scan for new signals
    if not positions:
        print(f"\n🔍 Scanning for signals...")
        for symbol in SYMBOLS:
            try:
                side, params = get_signal(symbol)
                if side:
                    price = params['entry']
                    rsi = params['rsi']
                    print(f"  ✅ {symbol}: {side} @ ${price:.2f} (RSI {rsi:.1f})")
                    
                    # Execute
                    position_size = max(MIN_POSITION, min(MAX_POSITION, balance * POSITION_PCT))
                    quantity = round(position_size / price, 3)
                    
                    if quantity >= 0.001:
                        result = place_order(symbol, side, quantity)
                        if 'orderId' in result:
                            send_telegram(f"🚀 <b>NEW TRADE</b>\n{symbol} {side}\nEntry: ${price:.4f}\nQty: {quantity}")
                            print(f"  ✅ Executed {side} {quantity} {symbol}")
                        else:
                            print(f"  ❌ Order failed: {result}")
            except Exception as e:
                print(f"  ⚠️ {symbol}: {e}")
    else:
        print(f"\n⏳ Already have position, waiting...")
    
    print(f"\n✅ Cycle complete")

if __name__ == "__main__":
    asyncio.run(run_auto_trade_cycle())
