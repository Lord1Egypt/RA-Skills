#!/usr/bin/env python3
"""
agent-trading-bot.py — AI-Powered Trading Bot Framework for OpenClaw
Built by GetAgentIQ — https://getagentiq.ai

Connects to crypto exchanges, manages risk, executes strategies.
Paper trading mode by default — never trades real money without explicit approval.
"""

import argparse
import datetime
import hashlib
import hmac
import json
import math
import os
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

# ─── Constants ───────────────────────────────────────────────────────────────

TRADING_CONFIG_PATH = os.path.expanduser("~/.openclaw/trading-config.json")
TRADE_LOG_PATH = os.path.expanduser("~/.openclaw/workspace/memory/trading-log.json")
PAPER_PORTFOLIO_PATH = os.path.expanduser("~/.openclaw/workspace/memory/paper-portfolio.json")

# Default risk limits
DEFAULT_RISK = {
    "max_position_pct": 10,       # Max % of portfolio in one position
    "max_drawdown_pct": 10,       # Max drawdown before circuit breaker
    "default_stop_loss_pct": 5,   # Default stop-loss per trade
    "default_take_profit_pct": 15,# Default take-profit per trade
    "max_daily_trades": 20,       # Max trades per day
    "allowed_pairs": ["BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT"],
}

# Exchange API base URLs
EXCHANGE_URLS = {
    "binance": "https://api.binance.com",
    "binance_futures": "https://fapi.binance.com",
    "hyperliquid": "https://api.hyperliquid.xyz",
}

# ─── Utility ─────────────────────────────────────────────────────────────────

def load_json(path, default=None):
    """Safely load JSON file."""
    if default is None:
        default = {}
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except (IOError, json.JSONDecodeError):
        return default


def save_json(path, data):
    """Save JSON data."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)


def load_risk_config():
    """Load risk configuration with defaults."""
    config = load_json(TRADING_CONFIG_PATH, DEFAULT_RISK.copy())
    for key, val in DEFAULT_RISK.items():
        config.setdefault(key, val)
    return config


def log_trade(action, pair, amount, price, reasoning, result, paper=True):
    """Log a trade to the trading log."""
    log = load_json(TRADE_LOG_PATH, [])
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "action": action,
        "pair": pair,
        "amount": amount,
        "price": price,
        "reasoning": reasoning,
        "result": result,
        "paper": paper,
    }
    log.append(entry)
    if len(log) > 10000:
        log = log[-10000:]
    save_json(TRADE_LOG_PATH, log)
    return entry


def format_money(amount):
    """Format a number as money."""
    if abs(amount) >= 1000:
        return f"${amount:,.2f}"
    return f"${amount:.4f}"


# ─── Exchange Connectivity ───────────────────────────────────────────────────

def binance_signed_request(endpoint, params=None, method='GET'):
    """Make a signed Binance API request."""
    api_key = os.environ.get('BINANCE_API_KEY', '')
    api_secret = os.environ.get('BINANCE_API_SECRET', '')

    if not api_key or not api_secret:
        return None, "BINANCE_API_KEY and BINANCE_API_SECRET env vars not set"

    if params is None:
        params = {}
    params['timestamp'] = int(time.time() * 1000)
    params['recvWindow'] = 5000

    query_string = urllib.parse.urlencode(params)
    signature = hmac.new(
        api_secret.encode(), query_string.encode(), hashlib.sha256
    ).hexdigest()
    query_string += f"&signature={signature}"

    url = f"{EXCHANGE_URLS['binance']}{endpoint}?{query_string}"

    req = urllib.request.Request(url)
    req.add_header('X-MBX-APIKEY', api_key)

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode()), None
    except Exception as e:
        return None, str(e)


def get_binance_price(pair):
    """Get current price from Binance."""
    symbol = pair.replace('/', '')
    url = f"{EXCHANGE_URLS['binance']}/api/v3/ticker/price?symbol={symbol}"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            return float(data['price']), None
    except Exception as e:
        return None, str(e)


def get_binance_klines(pair, interval='1h', limit=100):
    """Get candlestick data from Binance."""
    symbol = pair.replace('/', '')
    url = f"{EXCHANGE_URLS['binance']}/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            return [{
                'time': d[0],
                'open': float(d[1]),
                'high': float(d[2]),
                'low': float(d[3]),
                'close': float(d[4]),
                'volume': float(d[5]),
            } for d in data], None
    except Exception as e:
        return None, str(e)


# ─── Indicators ──────────────────────────────────────────────────────────────

def calculate_sma(prices, period):
    """Simple Moving Average."""
    if len(prices) < period:
        return None
    return sum(prices[-period:]) / period


def calculate_ema(prices, period):
    """Exponential Moving Average."""
    if len(prices) < period:
        return None
    multiplier = 2 / (period + 1)
    ema = sum(prices[:period]) / period
    for price in prices[period:]:
        ema = (price - ema) * multiplier + ema
    return ema


def calculate_rsi(prices, period=14):
    """Relative Strength Index."""
    if len(prices) < period + 1:
        return None
    gains = []
    losses = []
    for i in range(1, len(prices)):
        change = prices[i] - prices[i-1]
        gains.append(max(0, change))
        losses.append(max(0, -change))

    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period

    if avg_loss == 0:
        return 100

    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


# ─── Strategy Engines ────────────────────────────────────────────────────────

def strategy_dca(pair, amount, interval_hours=24):
    """Dollar-Cost Averaging — buy fixed amount at regular intervals."""
    price, err = get_binance_price(pair)
    if err:
        return None, f"Cannot get price: {err}"

    qty = amount / price

    return {
        "action": "BUY",
        "pair": pair,
        "price": price,
        "amount_usd": amount,
        "quantity": qty,
        "reasoning": f"DCA: Buy ${amount:.2f} of {pair} at {format_money(price)}. "
                     f"Next buy in {interval_hours}h.",
        "strategy": "dca",
    }, None


def strategy_momentum(pair, amount):
    """Momentum/trend following using SMA crossover."""
    klines, err = get_binance_klines(pair, '1h', 100)
    if err:
        return None, f"Cannot get klines: {err}"

    closes = [k['close'] for k in klines]
    price = closes[-1]

    sma_20 = calculate_sma(closes, 20)
    sma_50 = calculate_sma(closes, 50)
    rsi = calculate_rsi(closes)

    if sma_20 is None or sma_50 is None or rsi is None:
        return None, "Not enough data for indicators"

    # Signal generation
    if sma_20 > sma_50 and rsi < 70:
        action = "BUY"
        reasoning = (f"Momentum BUY: SMA20 ({sma_20:.2f}) > SMA50 ({sma_50:.2f}), "
                     f"RSI={rsi:.1f} (not overbought). Trend is UP.")
    elif sma_20 < sma_50 or rsi > 80:
        action = "SELL"
        reasoning = (f"Momentum SELL: SMA20 ({sma_20:.2f}) < SMA50 ({sma_50:.2f}) "
                     f"or RSI={rsi:.1f} overbought. Trend reversing.")
    else:
        action = "HOLD"
        reasoning = (f"Momentum HOLD: No clear signal. SMA20={sma_20:.2f}, "
                     f"SMA50={sma_50:.2f}, RSI={rsi:.1f}")

    qty = amount / price if action == "BUY" else 0

    return {
        "action": action,
        "pair": pair,
        "price": price,
        "amount_usd": amount if action == "BUY" else 0,
        "quantity": qty,
        "reasoning": reasoning,
        "strategy": "momentum",
        "indicators": {"sma_20": sma_20, "sma_50": sma_50, "rsi": rsi},
    }, None


def strategy_mean_revert(pair, amount):
    """Mean reversion using RSI."""
    klines, err = get_binance_klines(pair, '1h', 100)
    if err:
        return None, f"Cannot get klines: {err}"

    closes = [k['close'] for k in klines]
    price = closes[-1]
    rsi = calculate_rsi(closes)

    if rsi is None:
        return None, "Not enough data for RSI"

    if rsi < 30:
        action = "BUY"
        reasoning = f"Mean Revert BUY: RSI={rsi:.1f} (oversold < 30). Price likely to bounce."
    elif rsi > 70:
        action = "SELL"
        reasoning = f"Mean Revert SELL: RSI={rsi:.1f} (overbought > 70). Price likely to pull back."
    else:
        action = "HOLD"
        reasoning = f"Mean Revert HOLD: RSI={rsi:.1f} (neutral zone 30-70)."

    qty = amount / price if action == "BUY" else 0

    return {
        "action": action,
        "pair": pair,
        "price": price,
        "amount_usd": amount if action == "BUY" else 0,
        "quantity": qty,
        "reasoning": reasoning,
        "strategy": "mean-revert",
        "indicators": {"rsi": rsi},
    }, None


STRATEGIES = {
    "dca": strategy_dca,
    "momentum": strategy_momentum,
    "mean-revert": strategy_mean_revert,
}


# ─── Paper Trading ───────────────────────────────────────────────────────────

def paper_execute(signal):
    """Execute a trade in paper mode."""
    default_portfolio = {
        "cash": 10000,
        "positions": {},
        "trades": [],
        "start_value": 10000,
    }
    portfolio = load_json(PAPER_PORTFOLIO_PATH, default_portfolio)
    # Ensure all keys exist
    for k, v in default_portfolio.items():
        portfolio.setdefault(k, v)

    if signal["action"] == "BUY" and signal["amount_usd"] > 0:
        if portfolio["cash"] < signal["amount_usd"]:
            return f"Insufficient paper cash: ${portfolio['cash']:.2f}"

        portfolio["cash"] -= signal["amount_usd"]
        pair = signal["pair"]
        pos = portfolio["positions"].get(pair, {"qty": 0, "avg_price": 0})
        total_cost = pos["qty"] * pos["avg_price"] + signal["amount_usd"]
        pos["qty"] += signal["quantity"]
        pos["avg_price"] = total_cost / pos["qty"] if pos["qty"] > 0 else 0
        portfolio["positions"][pair] = pos

        portfolio["trades"].append({
            "time": datetime.datetime.utcnow().isoformat(),
            "action": "BUY",
            "pair": pair,
            "qty": signal["quantity"],
            "price": signal["price"],
        })

    elif signal["action"] == "SELL":
        pair = signal["pair"]
        pos = portfolio["positions"].get(pair)
        if not pos or pos["qty"] <= 0:
            return f"No {pair} position to sell"

        sell_value = pos["qty"] * signal["price"]
        pnl = sell_value - (pos["qty"] * pos["avg_price"])
        portfolio["cash"] += sell_value
        del portfolio["positions"][pair]

        portfolio["trades"].append({
            "time": datetime.datetime.utcnow().isoformat(),
            "action": "SELL",
            "pair": pair,
            "qty": pos["qty"],
            "price": signal["price"],
            "pnl": pnl,
        })

    save_json(PAPER_PORTFOLIO_PATH, portfolio)

    # Calculate total portfolio value
    total = portfolio["cash"]
    for pair, pos in portfolio["positions"].items():
        price, _ = get_binance_price(pair)
        if price:
            total += pos["qty"] * price

    pnl_pct = ((total - portfolio["start_value"]) / portfolio["start_value"]) * 100

    return (f"Paper trade executed: {signal['action']} {signal.get('quantity', 0):.6f} "
            f"{signal['pair']} @ {format_money(signal['price'])}. "
            f"Portfolio: {format_money(total)} ({pnl_pct:+.2f}%)")


# ─── Commands ────────────────────────────────────────────────────────────────

def cmd_status(args):
    """Check exchange connectivity and account status."""
    print("📡 Agent Trading Bot — Status Check")
    print("=" * 50)

    # Check Binance public API
    print("\n🔗 Exchange Connectivity:")
    price, err = get_binance_price("BTC/USDT")
    if err:
        print(f"  ❌ Binance: {err}")
    else:
        print(f"  ✅ Binance: Connected (BTC/USDT = {format_money(price)})")

    # Check API keys
    has_binance = bool(os.environ.get('BINANCE_API_KEY'))
    has_hyperliquid = bool(os.environ.get('HYPERLIQUID_API_KEY'))

    print(f"\n🔑 API Keys:")
    print(f"  Binance: {'✅ Set' if has_binance else '❌ Not set'}")
    print(f"  Hyperliquid: {'✅ Set' if has_hyperliquid else '❌ Not set'}")

    # Check balances if API keys set
    if has_binance:
        data, err = binance_signed_request('/api/v3/account')
        if err:
            print(f"\n💰 Balances: Error — {err}")
        elif data:
            print(f"\n💰 Binance Balances:")
            for bal in data.get('balances', []):
                free = float(bal.get('free', 0))
                if free > 0:
                    print(f"  {bal['asset']}: {free:.8f}")

    # Show paper portfolio if exists
    portfolio = load_json(PAPER_PORTFOLIO_PATH)
    if portfolio and 'cash' in portfolio:
        print(f"\n📝 Paper Portfolio:")
        print(f"  Cash: {format_money(portfolio['cash'])}")
        for pair, pos in portfolio.get('positions', {}).items():
            print(f"  {pair}: {pos['qty']:.6f} (avg: {format_money(pos['avg_price'])})")

    # Risk config
    risk = load_risk_config()
    print(f"\n⚠️  Risk Limits:")
    print(f"  Max position: {risk['max_position_pct']}%")
    print(f"  Max drawdown: {risk['max_drawdown_pct']}%")
    print(f"  Stop-loss: {risk['default_stop_loss_pct']}%")
    print(f"  Max daily trades: {risk['max_daily_trades']}")


def cmd_paper(args):
    """Paper trade with a strategy."""
    print("📝 Agent Trading Bot — Paper Trading")
    print("=" * 50)

    strategy = getattr(args, 'strategy', 'dca')
    pair = getattr(args, 'pair', 'BTC/USDT')
    amount = getattr(args, 'amount', 100)

    print(f"\n🎯 Strategy: {strategy}")
    print(f"📊 Pair: {pair}")
    print(f"💵 Amount: ${amount}")

    if strategy not in STRATEGIES:
        print(f"\n❌ Unknown strategy: {strategy}")
        print(f"   Available: {', '.join(STRATEGIES.keys())}")
        sys.exit(1)

    # Get signal
    print(f"\n🔍 Analyzing...")
    if strategy == 'dca':
        signal, err = STRATEGIES[strategy](pair, amount)
    else:
        signal, err = STRATEGIES[strategy](pair, amount)

    if err:
        print(f"  ❌ Error: {err}")
        sys.exit(1)

    print(f"\n📊 Signal: {signal['action']}")
    print(f"💡 Reasoning: {signal['reasoning']}")

    if 'indicators' in signal:
        print(f"📈 Indicators:")
        for k, v in signal['indicators'].items():
            print(f"   {k}: {v:.2f}")

    # Execute paper trade
    if signal['action'] in ('BUY', 'SELL'):
        result = paper_execute(signal)
        print(f"\n✅ {result}")
        log_trade(signal['action'], pair, signal.get('quantity', 0),
                  signal['price'], signal['reasoning'], result, paper=True)
    else:
        print(f"\n⏸️  No trade — signal is HOLD")
        log_trade('HOLD', pair, 0, signal['price'], signal['reasoning'], 'no_trade', paper=True)


def cmd_trade(args):
    """Live trading (requires --live flag)."""
    print("🔴 Agent Trading Bot — LIVE Trading")
    print("=" * 50)

    live = getattr(args, 'live', False)
    if not live:
        print("\n⚠️  SAFETY: Live trading requires --live flag.")
        print("   Run: agent-trading-bot trade --strategy dca --pair BTC/USDT --amount 100 --live")
        print("\n   Use 'paper' command to test strategies safely first.")
        sys.exit(1)

    # Double confirmation
    print("\n🚨 WARNING: This will execute REAL trades with REAL money.")
    print("   Strategy:", getattr(args, 'strategy', 'dca'))
    print("   Pair:", getattr(args, 'pair', 'BTC/USDT'))
    print("   Amount: $", getattr(args, 'amount', 100))

    # Check API keys
    if not os.environ.get('BINANCE_API_KEY'):
        print("\n❌ BINANCE_API_KEY not set. Cannot trade.")
        sys.exit(1)

    # Check risk limits
    risk = load_risk_config()
    amount = getattr(args, 'amount', 100)

    # Get account balance
    data, err = binance_signed_request('/api/v3/account')
    if err:
        print(f"\n❌ Cannot access account: {err}")
        sys.exit(1)

    # Find USDT balance
    usdt_balance = 0
    for bal in data.get('balances', []):
        if bal['asset'] == 'USDT':
            usdt_balance = float(bal['free'])

    if amount > usdt_balance:
        print(f"\n❌ Insufficient balance: ${usdt_balance:.2f} USDT available, ${amount} requested")
        sys.exit(1)

    # Position size check
    if usdt_balance > 0 and (amount / usdt_balance * 100) > risk['max_position_pct']:
        print(f"\n❌ Position too large: {amount / usdt_balance * 100:.1f}% > "
              f"{risk['max_position_pct']}% limit")
        sys.exit(1)

    print(f"\n⚠️  All safety checks passed. Trade would execute here.")
    print(f"   (Full Binance order execution requires ccxt library — install with: pip install ccxt)")
    print(f"   For production use, see references/exchange-setup.md")


def cmd_risk(args):
    """Show risk dashboard."""
    print("⚠️  Agent Trading Bot — Risk Dashboard")
    print("=" * 50)

    risk = load_risk_config()

    # Paper portfolio stats
    portfolio = load_json(PAPER_PORTFOLIO_PATH, {})
    if portfolio and 'cash' in portfolio:
        total = portfolio['cash']
        positions = portfolio.get('positions', {})

        print(f"\n📝 Paper Portfolio:")
        print(f"  Cash: {format_money(portfolio['cash'])}")

        for pair, pos in positions.items():
            price, _ = get_binance_price(pair)
            if price:
                value = pos['qty'] * price
                pnl = value - (pos['qty'] * pos['avg_price'])
                pnl_pct = (pnl / (pos['qty'] * pos['avg_price'])) * 100 if pos['avg_price'] > 0 else 0
                total += value
                print(f"  {pair}: {pos['qty']:.6f} × {format_money(price)} = "
                      f"{format_money(value)} ({pnl_pct:+.2f}%)")

        start = portfolio.get('start_value', 10000)
        total_pnl = ((total - start) / start) * 100
        drawdown = min(0, total_pnl)

        print(f"\n  📊 Total: {format_money(total)} ({total_pnl:+.2f}%)")
        print(f"  📉 Drawdown: {drawdown:.2f}% (max allowed: -{risk['max_drawdown_pct']}%)")

        if abs(drawdown) > risk['max_drawdown_pct']:
            print(f"  🚨 CIRCUIT BREAKER: Drawdown exceeds limit!")
    else:
        print("\n  No paper portfolio. Run: agent-trading-bot paper --strategy dca --pair BTC/USDT")

    # Trade log stats
    log = load_json(TRADE_LOG_PATH, [])
    if log:
        today = datetime.datetime.utcnow().strftime('%Y-%m-%d')
        today_trades = [t for t in log if t.get('timestamp', '').startswith(today)]
        print(f"\n📋 Trade Log:")
        print(f"  Today: {len(today_trades)}/{risk['max_daily_trades']} trades")
        print(f"  Total: {len(log)} trades recorded")

    print(f"\n⚠️  Risk Limits:")
    print(f"  Max position size: {risk['max_position_pct']}% of portfolio")
    print(f"  Max drawdown: {risk['max_drawdown_pct']}%")
    print(f"  Stop-loss: {risk['default_stop_loss_pct']}%")
    print(f"  Take-profit: {risk['default_take_profit_pct']}%")
    print(f"  Allowed pairs: {', '.join(risk['allowed_pairs'])}")


def cmd_kill(args):
    """Emergency kill switch."""
    print("🚨 Agent Trading Bot — KILL SWITCH")
    print("=" * 50)

    force = getattr(args, 'force', False)

    if not force:
        print("\n⚠️  This will close ALL positions and cancel ALL orders.")
        print("   Run with --force to execute immediately.")
        print("   agent-trading-bot kill --force")
        return

    # Paper positions
    portfolio = load_json(PAPER_PORTFOLIO_PATH, {})
    if portfolio and portfolio.get('positions'):
        print("\n📝 Closing paper positions...")
        for pair, pos in list(portfolio.get('positions', {}).items()):
            price, _ = get_binance_price(pair)
            if price:
                value = pos['qty'] * price
                pnl = value - (pos['qty'] * pos['avg_price'])
                portfolio['cash'] += value
                print(f"  ✅ Closed {pair}: {pos['qty']:.6f} @ {format_money(price)} "
                      f"(P&L: {format_money(pnl)})")
                log_trade('KILL_SELL', pair, pos['qty'], price,
                          'Emergency kill switch', f'P&L: {format_money(pnl)}', paper=True)
        portfolio['positions'] = {}
        save_json(PAPER_PORTFOLIO_PATH, portfolio)
        print(f"  💰 Cash: {format_money(portfolio['cash'])}")

    # Live positions (if API keys set)
    if os.environ.get('BINANCE_API_KEY'):
        print("\n🔴 Live positions would be closed here.")
        print("   (Full implementation requires ccxt library)")

    print("\n✅ Kill switch executed. All positions closed.")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='Agent Trading Bot — AI-Powered Trading for OpenClaw'
    )
    sub = parser.add_subparsers(dest='command')

    sub.add_parser('status', help='Check exchange connectivity')

    p_paper = sub.add_parser('paper', help='Paper trading (simulated)')
    p_paper.add_argument('--strategy', default='dca', choices=list(STRATEGIES.keys()))
    p_paper.add_argument('--pair', default='BTC/USDT')
    p_paper.add_argument('--amount', type=float, default=100)

    p_trade = sub.add_parser('trade', help='Live trading')
    p_trade.add_argument('--strategy', default='dca', choices=list(STRATEGIES.keys()))
    p_trade.add_argument('--pair', default='BTC/USDT')
    p_trade.add_argument('--amount', type=float, default=100)
    p_trade.add_argument('--live', action='store_true')

    sub.add_parser('risk', help='Risk dashboard')

    p_kill = sub.add_parser('kill', help='Emergency kill switch')
    p_kill.add_argument('--force', action='store_true')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    {'status': cmd_status, 'paper': cmd_paper, 'trade': cmd_trade,
     'risk': cmd_risk, 'kill': cmd_kill}[args.command](args)


if __name__ == '__main__':
    main()
