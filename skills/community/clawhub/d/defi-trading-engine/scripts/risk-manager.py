#!/usr/bin/env python3
"""
Risk Manager - Gatekeeper for all trades
Enforces position limits, trade frequency, drawdown limits, and correlation checks.
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional

DEFAULTS = {
    "trade_size_usd": 40,
    "max_active_positions": 5,
    "max_daily_trades": 8,
    "cooldown_minutes": 30,
    "max_drawdown_pct": 20.0,
    "max_correlated_positions": 2,
    "dry_run": True,
}

def load_config(config_path: str = "trading-config.json") -> Dict:
    """Load trading configuration, fall back to defaults if missing"""
    try:
        with open(config_path, 'r') as f:
            return {**DEFAULTS, **json.load(f)}
    except FileNotFoundError:
        print(f"⚠️  Config not found: {config_path}, using defaults", file=sys.stderr)
        return DEFAULTS.copy()
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in config: {e}", file=sys.stderr)
        sys.exit(1)

def load_trades(trades_dir: str = "trades") -> List[Dict]:
    """Load all trade history"""
    trades = []
    trades_path = Path(trades_dir)
    
    if not trades_path.exists():
        return []
    
    for trade_file in trades_path.glob("*.json"):
        try:
            with open(trade_file, 'r') as f:
                file_trades = json.load(f)
                if isinstance(file_trades, list):
                    trades.extend(file_trades)
        except (json.JSONDecodeError, IOError):
            continue
    
    return trades

def get_open_positions(trades: List[Dict]) -> List[Dict]:
    """Get all currently open positions"""
    open_positions = []
    
    # Group trades by symbol
    symbols = {}
    for trade in trades:
        symbol = trade.get('symbol')
        if not symbol:
            continue
        if symbol not in symbols:
            symbols[symbol] = []
        symbols[symbol].append(trade)
    
    # Check which symbols have open positions
    for symbol, symbol_trades in symbols.items():
        total_quantity = 0
        total_cost = 0
        
        for trade in symbol_trades:
            if trade.get('status') != 'success':
                continue
            
            action = trade.get('action', '').lower()
            quantity = trade.get('quantity', 0)
            amount = trade.get('amount_usd', 0)
            
            if action in ['buy', 'limit_buy']:
                total_quantity += quantity
                total_cost += amount
            elif action in ['sell', 'limit_sell']:
                total_quantity -= quantity
                total_cost -= amount
        
        # If we still hold this position
        if total_quantity > 0.0001:
            open_positions.append({
                'symbol': symbol,
                'quantity': total_quantity,
                'cost_usd': total_cost,
                'trades': symbol_trades
            })
    
    return open_positions

def get_todays_trades(trades: List[Dict]) -> List[Dict]:
    """Get trades from today"""
    today = datetime.now().date()
    todays_trades = []
    
    for trade in trades:
        timestamp_str = trade.get('timestamp')
        if not timestamp_str:
            continue
        
        try:
            trade_date = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00')).date()
            if trade_date == today:
                todays_trades.append(trade)
        except (ValueError, AttributeError):
            continue
    
    return todays_trades

def get_last_trade_time(trades: List[Dict]) -> Optional[datetime]:
    """Get timestamp of most recent trade"""
    if not trades:
        return None
    
    sorted_trades = sorted(trades, key=lambda t: t.get('timestamp', ''), reverse=True)
    
    for trade in sorted_trades:
        timestamp_str = trade.get('timestamp')
        if timestamp_str:
            try:
                return datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                continue
    
    return None

def calculate_drawdown(trades: List[Dict], initial_balance: float = 1000.0) -> float:
    """Calculate current portfolio drawdown percentage"""
    if not trades:
        return 0.0
    
    # Sort trades by timestamp
    sorted_trades = sorted(trades, key=lambda t: t.get('timestamp', ''))
    
    balance = initial_balance
    peak_balance = initial_balance
    
    for trade in sorted_trades:
        if trade.get('status') != 'success':
            continue
        
        action = trade.get('action', '').lower()
        amount = trade.get('amount_usd', 0)
        
        # Simplified P&L calculation
        # In production, track realized/unrealized separately
        if action in ['buy', 'limit_buy']:
            balance -= amount
        elif action in ['sell', 'limit_sell']:
            balance += amount
    
    # Update peak
    if balance > peak_balance:
        peak_balance = balance
    
    # Calculate drawdown
    if peak_balance == 0:
        return 0.0
    
    drawdown = ((peak_balance - balance) / peak_balance) * 100
    return max(0, drawdown)

def count_similar_positions(open_positions: List[Dict], symbol: str, correlation_tags: Dict[str, List[str]]) -> int:
    """Count positions in the same correlation group"""
    # Get correlation group for this symbol
    symbol_group = None
    for group, symbols in correlation_tags.items():
        if symbol.upper() in [s.upper() for s in symbols]:
            symbol_group = group
            break
    
    if not symbol_group:
        return 0
    
    # Count positions in same group
    count = 0
    group_symbols = [s.upper() for s in correlation_tags[symbol_group]]
    
    for pos in open_positions:
        if pos['symbol'].upper() in group_symbols:
            count += 1
    
    return count

def check_trade(
    symbol: str,
    amount: float,
    config: Dict,
    trades: List[Dict]
) -> tuple[bool, str]:
    """
    Check if trade passes all risk limits.
    Returns (approved: bool, reason: str)
    """
    risk = config.get('risk', {})
    
    # 1. Position size check
    max_position = risk.get('max_position_size_usd', 40)
    if amount > max_position:
        return False, f"Position size ${amount} exceeds limit ${max_position}"
    
    # 2. Active positions check
    open_positions = get_open_positions(trades)
    max_positions = risk.get('max_active_positions', 5)
    
    # Don't count selling an existing position against the limit
    if len(open_positions) >= max_positions:
        # Check if we already have this symbol (then it's a sell)
        has_position = any(pos['symbol'].upper() == symbol.upper() for pos in open_positions)
        if not has_position:
            return False, f"Max active positions reached ({len(open_positions)}/{max_positions})"
    
    # 3. Daily trade limit
    todays_trades = get_todays_trades(trades)
    max_daily = risk.get('max_daily_trades', 8)
    
    if len(todays_trades) >= max_daily:
        return False, f"Daily trade limit reached ({len(todays_trades)}/{max_daily})"
    
    # 4. Cooldown period
    last_trade = get_last_trade_time(trades)
    cooldown_min = risk.get('cooldown_minutes', 30)
    
    if last_trade:
        time_since = datetime.now(last_trade.tzinfo) - last_trade
        cooldown_delta = timedelta(minutes=cooldown_min)
        
        if time_since < cooldown_delta:
            minutes_left = int((cooldown_delta - time_since).total_seconds() / 60)
            return False, f"Cooldown period active ({minutes_left} minutes remaining)"
    
    # 5. Max drawdown check
    max_drawdown = risk.get('max_drawdown_pct', 20)
    current_drawdown = calculate_drawdown(trades)
    
    if current_drawdown >= max_drawdown:
        return False, f"Max drawdown exceeded ({current_drawdown:.1f}% >= {max_drawdown}%) - TRADING HALTED"
    
    # 6. Correlation limit (optional)
    correlation_tags = config.get('correlation_tags', {
        'memecoins': ['DOGE', 'SHIB', 'PEPE', 'FLOKI'],
        'defi_blue_chip': ['UNI', 'AAVE', 'COMP', 'MKR'],
        'layer1': ['ETH', 'SOL', 'AVAX', 'MATIC']
    })
    
    max_correlated = risk.get('max_correlated_positions', 3)
    similar_count = count_similar_positions(open_positions, symbol, correlation_tags)
    
    if similar_count >= max_correlated:
        return False, f"Too many correlated positions ({similar_count}/{max_correlated})"
    
    # All checks passed
    return True, "All risk checks passed"

def print_risk_status(config: Dict, trades: List[Dict]):
    """Print current risk status"""
    risk = config.get('risk', {})
    open_positions = get_open_positions(trades)
    todays_trades = get_todays_trades(trades)
    last_trade = get_last_trade_time(trades)
    drawdown = calculate_drawdown(trades)
    
    print("\n📊 Risk Status")
    print("=" * 50)
    print(f"  Active positions: {len(open_positions)}/{risk.get('max_active_positions', 5)}")
    print(f"  Daily trades: {len(todays_trades)}/{risk.get('max_daily_trades', 8)}")
    
    if last_trade:
        time_since = datetime.now(last_trade.tzinfo) - last_trade
        minutes = int(time_since.total_seconds() / 60)
        print(f"  Last trade: {minutes} minutes ago")
    else:
        print(f"  Last trade: Never")
    
    print(f"  Current drawdown: {drawdown:.1f}% (limit: {risk.get('max_drawdown_pct', 20)}%)")
    
    if open_positions:
        print(f"\n  Open Positions:")
        for pos in open_positions:
            print(f"    - {pos['symbol']}: {pos['quantity']:.4f} (cost: ${pos['cost_usd']:.2f})")
    
    print("=" * 50)

def main():
    parser = argparse.ArgumentParser(description='Risk Manager - Check trade approval')
    parser.add_argument('--action', choices=['check', 'status'], default='check',
                      help='Action to perform')
    parser.add_argument('--symbol', help='Trading symbol (e.g. SOL)')
    parser.add_argument('--amount', type=float, help='Trade amount in USD')
    parser.add_argument('--config', default='trading-config.json',
                      help='Config file path')
    parser.add_argument('--trades-dir', default='trades',
                      help='Trades directory')
    
    args = parser.parse_args()
    
    # Load config and trades
    config = load_config(args.config)
    trades = load_trades(args.trades_dir)
    
    if args.action == 'status':
        print_risk_status(config, trades)
        sys.exit(0)
    
    # Check action requires symbol and amount
    if not args.symbol or args.amount is None:
        print("❌ --symbol and --amount required for check action", file=sys.stderr)
        parser.print_help()
        sys.exit(1)
    
    # Run risk check
    approved, reason = check_trade(args.symbol, args.amount, config, trades)
    
    if approved:
        print(f"✅ Risk check passed")
        print(f"  Symbol: {args.symbol}")
        print(f"  Amount: ${args.amount}")
        print(f"  Reason: {reason}")
        
        # Print current status for context
        risk = config.get('risk', {})
        open_positions = get_open_positions(trades)
        todays_trades = get_todays_trades(trades)
        drawdown = calculate_drawdown(trades)
        
        print(f"\n  Active positions: {len(open_positions)}/{risk.get('max_active_positions', 5)}")
        print(f"  Daily trades: {len(todays_trades)}/{risk.get('max_daily_trades', 8)}")
        print(f"  Current drawdown: {drawdown:.1f}%")
        
        sys.exit(0)
    else:
        print(f"❌ Risk check failed")
        print(f"  Symbol: {args.symbol}")
        print(f"  Amount: ${args.amount}")
        print(f"  Reason: {reason}")
        sys.exit(1)

if __name__ == '__main__':
    main()
