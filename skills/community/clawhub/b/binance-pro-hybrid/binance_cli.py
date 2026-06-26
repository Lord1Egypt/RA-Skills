#!/usr/bin/env python3
"""
Binance Pro CLI - Complete Binance integration for spot and futures trading.
Check balances, open/close positions, set stop loss and take profit.
"""

import json
import os
import sys
import hmac
import hashlib
import time
import urllib.request
from datetime import datetime

BINANCE_SPOT = "https://api.binance.com"
BINANCE_FUTURES = "https://fapi.binance.com"

CREDS_FILE = os.path.expanduser("~/.openclaw/credentials/binance.json")

def get_credentials():
    """Load API credentials from file or environment."""
    # Try environment first
    api_key = os.environ.get("BINANCE_API_KEY")
    secret_key = os.environ.get("BINANCE_SECRET")
    
    if api_key and secret_key:
        return api_key, secret_key
    
    # Try file
    if os.path.exists(CREDS_FILE):
        with open(CREDS_FILE, 'r') as f:
            creds = json.load(f)
            return creds.get("apiKey"), creds.get("secretKey")
    
    print("❌ No credentials found")
    print(f"   Set env vars: BINANCE_API_KEY, BINANCE_SECRET")
    print(f"   Or create: {CREDS_FILE}")
    sys.exit(1)

def generate_signature(query_string, secret_key):
    """Generate HMAC SHA256 signature."""
    return hmac.new(secret_key.encode(), query_string.encode(), hashlib.sha256).hexdigest()

def make_request(url, params=None, method="GET", signed=False):
    """Make authenticated request to Binance API."""
    api_key, secret_key = get_credentials()
    
    headers = {
        "X-MBX-APIKEY": api_key,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    if params is None:
        params = {}
    
    # Add timestamp
    timestamp = int(time.time() * 1000)
    params["timestamp"] = timestamp
    
    # Build query string
    query_string = "&".join(f"{k}={v}" for k, v in params.items())
    
    # Sign if required
    if signed:
        signature = generate_signature(query_string, secret_key)
        query_string += f"&signature={signature}"
    
    # Build full URL
    if query_string and method == "GET":
        url = f"{url}?{query_string}"
    
    req = urllib.request.Request(url, method=method, headers=headers)
    
    if method == "POST" and query_string:
        req.data = query_string.encode()
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"❌ HTTP Error {e.code}: {e.reason}")
        print(f"   Details: {error_body}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Request failed: {e}")
        sys.exit(1)

def get_spot_balance():
    """Get spot account balance."""
    url = f"{BINANCE_SPOT}/api/v3/account"
    result = make_request(url, signed=True)
    
    if "balances" in result:
        # Filter non-zero balances
        balances = [b for b in result["balances"] if float(b.get("free", 0)) > 0]
        
        print("\n💰 Spot Balance\n")
        print(f"{'Asset':<15} {'Free':>20} {'Locked':>20}")
        print("-" * 60)
        
        for bal in sorted(balances, key=lambda x: float(x["free"]), reverse=True)[:20]:
            free = float(bal["free"])
            locked = float(bal["locked"])
            print(f"{bal['asset']:<15} {free:>20,.8f} {locked:>20,.8f}")
    else:
        print(json.dumps(result, indent=2))

def get_futures_positions():
    """Get all futures positions."""
    url = f"{BINANCE_FUTURES}/fapi/v2/positionRisk"
    result = make_request(url, signed=True)
    
    if isinstance(result, list):
        # Filter non-zero positions
        positions = [p for p in result if float(p.get("positionAmt", 0)) != 0]
        
        if not positions:
            print("\n📊 No open futures positions\n")
            return
        
        print("\n📊 Futures Positions\n")
        print(f"{'Symbol':<12} {'Size':>12} {'Entry Price':>15} {'Mark Price':>15} {'PnL':>15} {'Liq Price':>15}")
        print("-" * 90)
        
        total_pnl = 0
        for pos in positions:
            symbol = pos["symbol"]
            size = float(pos["positionAmt"])
            entry = float(pos["entryPrice"])
            mark = float(pos["markPrice"])
            pnl = float(pos["unRealizedProfit"])
            liq = float(pos.get("liquidationPrice", 0))
            
            total_pnl += pnl
            
            side = "LONG" if size > 0 else "SHORT"
            size_str = f"{abs(size):.4f} {side}"
            
            print(f"{symbol:<12} {size_str:>12} ${entry:>14,.2f} ${mark:>14,.2f} ${pnl:>14,.2f} ${liq:>14,.2f}")
        
        print("-" * 90)
        print(f"Total Unrealized PnL: ${total_pnl:,.2f}")
    else:
        print(json.dumps(result, indent=2))

def get_futures_balance():
    """Get futures account balance."""
    url = f"{BINANCE_FUTURES}/fapi/v2/balance"
    result = make_request(url, signed=True)
    
    if isinstance(result, list):
        print("\n💰 Futures Balance\n")
        print(f"{'Asset':<15} {'Available':>20} {'Balance':>20}")
        print("-" * 60)
        
        for bal in result:
            available = float(bal.get("availableBalance", 0))
            balance = float(bal.get("balance", 0))
            if available > 0 or balance > 0:
                print(f"{bal['asset']:<15} {available:>20,.2f} {balance:>20,.2f}")
    else:
        print(json.dumps(result, indent=2))

def open_futures_order(symbol, side, quantity, order_type="MARKET"):
    """Open a futures order."""
    url = f"{BINANCE_FUTURES}/fapi/v1/order"
    params = {
        "symbol": symbol.upper(),
        "side": side.upper(),
        "type": order_type.upper(),
        "quantity": quantity
    }
    
    print(f"\n📦 Opening {side.upper()} order for {quantity} {symbol}...")
    result = make_request(url, params, "POST", signed=True)
    
    if "orderId" in result:
        print(f"✅ Order placed!")
        print(f"   Order ID: {result['orderId']}")
        print(f"   Symbol: {result['symbol']}")
        print(f"   Side: {result['side']}")
        print(f"   Type: {result['type']}")
        print(f"   Quantity: {result['origQty']}")
        print(f"   Status: {result['status']}")
    else:
        print(json.dumps(result, indent=2))

def close_position(symbol):
    """Close a futures position (reduce only)."""
    # First get current position
    positions = get_futures_positions_raw(symbol)
    
    if not positions:
        print(f"\nℹ️  No open position for {symbol}")
        return
    
    for pos in positions:
        size = float(pos.get("positionAmt", 0))
        if size != 0:
            side = "SELL" if size > 0 else "BUY"
            quantity = abs(size)
            
            print(f"\n🔒 Closing {symbol} position ({side} {quantity})...")
            
            url = f"{BINANCE_FUTURES}/fapi/v1/order"
            params = {
                "symbol": symbol.upper(),
                "side": side,
                "type": "MARKET",
                "quantity": quantity,
                "reduceOnly": "true"
            }
            
            result = make_request(url, params, "POST", signed=True)
            
            if "orderId" in result:
                print(f"✅ Position closed! Order ID: {result['orderId']}")
            else:
                print(json.dumps(result, indent=2))

def get_futures_positions_raw(symbol=None):
    """Get raw position data."""
    url = f"{BINANCE_FUTURES}/fapi/v2/positionRisk"
    params = {}
    if symbol:
        params["symbol"] = symbol.upper()
    
    return make_request(url, params, signed=True)

def set_stop_loss(symbol, stop_price, side=None):
    """Set stop loss order."""
    # Auto-detect side if not provided
    if side is None:
        positions = get_futures_positions_raw(symbol)
        for pos in positions:
            if pos["symbol"] == symbol.upper():
                size = float(pos.get("positionAmt", 0))
                side = "SELL" if size > 0 else "BUY"
                break
    
    if not side:
        print("❌ No position found to set stop loss")
        return
    
    url = f"{BINANCE_FUTURES}/fapi/v1/order"
    params = {
        "symbol": symbol.upper(),
        "side": side,
        "type": "STOP_MARKET",
        "stopPrice": stop_price,
        "closePosition": "true"
    }
    
    print(f"\n🛡️  Setting stop loss for {symbol} at ${stop_price:,.2f}...")
    result = make_request(url, params, "POST", signed=True)
    
    if "orderId" in result:
        print(f"✅ Stop loss set! Order ID: {result['orderId']}")
    else:
        print(json.dumps(result, indent=2))

def set_take_profit(symbol, take_profit_price, side=None):
    """Set take profit order."""
    if side is None:
        positions = get_futures_positions_raw(symbol)
        for pos in positions:
            if pos["symbol"] == symbol.upper():
                size = float(pos.get("positionAmt", 0))
                side = "SELL" if size > 0 else "BUY"
                break
    
    if not side:
        print("❌ No position found to set take profit")
        return
    
    url = f"{BINANCE_FUTURES}/fapi/v1/order"
    params = {
        "symbol": symbol.upper(),
        "side": side,
        "type": "TAKE_PROFIT_MARKET",
        "stopPrice": take_profit_price,
        "closePosition": "true"
    }
    
    print(f"\n🎯 Setting take profit for {symbol} at ${take_profit_price:,.2f}...")
    result = make_request(url, params, "POST", signed=True)
    
    if "orderId" in result:
        print(f"✅ Take profit set! Order ID: {result['orderId']}")
    else:
        print(json.dumps(result, indent=2))

def get_price(symbol):
    """Get current price for a symbol."""
    url = f"{BINANCE_SPOT}/api/v3/ticker/price"
    params = {"symbol": symbol.upper()}
    
    result = make_request(url, params)
    
    if "price" in result:
        print(f"\n💹 {symbol.upper()}: ${float(result['price']):,.2f}")
    else:
        print(json.dumps(result, indent=2))

def main():
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print("""Binance Pro CLI - Spot & Futures Trading

Usage: binance_cli.py <command> [args]

Commands:
  balance                     Show spot balance
  futures-balance             Show futures balance
  positions                   Show open futures positions
  price <symbol>              Get current price
  
  buy <symbol> <quantity>     Open LONG position (futures)
  sell <symbol> <quantity>    Open SHORT position (futures)
  close <symbol>              Close position (futures)
  
  stop-loss <symbol> <price>  Set stop loss
  take-profit <symbol> <price> Set take profit
  
  spot-buy <symbol> <qty>     Buy on spot market
  spot-sell <symbol> <qty>    Sell on spot market

Credentials:
  Set BINANCE_API_KEY and BINANCE_SECRET env vars
  Or create ~/.openclaw/credentials/binance.json

Examples:
  ./binance_cli.py balance
  ./binance_cli.py positions
  ./binance_cli.py buy BTCUSDT 0.001
  ./binance_cli.py stop-loss BTCUSDT 75000
  ./binance_cli.py price ETHUSDT
""")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "balance":
        get_spot_balance()
    
    elif command == "futures-balance":
        get_futures_balance()
    
    elif command == "positions":
        get_futures_positions()
    
    elif command == "price" and len(sys.argv) >= 3:
        get_price(sys.argv[2])
    
    elif command == "buy" and len(sys.argv) >= 4:
        symbol = sys.argv[2]
        quantity = sys.argv[3]
        open_futures_order(symbol, "BUY", quantity)
    
    elif command == "sell" and len(sys.argv) >= 4:
        symbol = sys.argv[2]
        quantity = sys.argv[3]
        open_futures_order(symbol, "SELL", quantity)
    
    elif command == "close" and len(sys.argv) >= 3:
        close_position(sys.argv[2])
    
    elif command == "stop-loss" and len(sys.argv) >= 4:
        symbol = sys.argv[2]
        price = float(sys.argv[3])
        set_stop_loss(symbol, price)
    
    elif command == "take-profit" and len(sys.argv) >= 4:
        symbol = sys.argv[2]
        price = float(sys.argv[3])
        set_take_profit(symbol, price)
    
    elif command == "spot-buy" and len(sys.argv) >= 4:
        symbol = sys.argv[2]
        quantity = sys.argv[3]
        # Implement spot buy if needed
        print("⚠️  Spot trading not yet implemented")
    
    elif command == "spot-sell" and len(sys.argv) >= 4:
        symbol = sys.argv[2]
        quantity = sys.argv[3]
        # Implement spot sell if needed
        print("⚠️  Spot trading not yet implemented")
    
    else:
        print(f"❌ Unknown command or missing arguments: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
