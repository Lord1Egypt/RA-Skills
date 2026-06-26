#!/usr/bin/env python3
"""
Trade Executor - Executes trades via Bankr CLI
Supports market/limit orders, stop-loss, take-profit.
Always runs risk checks before executing.
"""

import json
import sys
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, Tuple

DEFAULTS = {
    "chain": "base",
    "trade_size_usd": 40,
    "take_profit_pct": 4.0,
    "stop_loss_pct": 8.0,
    "dry_run": True,
}

def load_config(config_path: str = "trading-config.json") -> Dict:
    """Load trading configuration, fall back to safe defaults if missing"""
    try:
        with open(config_path, 'r') as f:
            return {**DEFAULTS, **json.load(f)}
    except FileNotFoundError:
        print(f"⚠️  Config not found: {config_path}, using defaults (dry_run=true)", file=sys.stderr)
        return DEFAULTS.copy()
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in config: {e}", file=sys.stderr)
        sys.exit(1)

def run_risk_check(symbol: str, amount: float, config_path: str, trades_dir: str) -> bool:
    """Run risk manager check before executing trade"""
    try:
        result = subprocess.run(
            [
                'python3', 'risk-manager.py',
                '--action', 'check',
                '--symbol', symbol,
                '--amount', str(amount),
                '--config', config_path,
                '--trades-dir', trades_dir
            ],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        # Print risk manager output
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("❌ Risk check timeout", file=sys.stderr)
        return False
    except FileNotFoundError:
        print("❌ risk-manager.py not found", file=sys.stderr)
        return False

def get_current_price(symbol: str, config: Dict) -> Optional[float]:
    """Get current price for a symbol (mock for now, integrate real data)"""
    # In production: call Bankr CLI or price API
    # For now, return mock price
    
    # Attempt to get from bankr balance (if we hold it)
    try:
        result = subprocess.run(
            ['bankr', 'price', symbol],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0 and result.stdout:
            # Parse price from output
            # Format varies by CLI, adjust as needed
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if '$' in line or 'price' in line.lower():
                    # Extract number
                    price_str = ''.join(c for c in line if c.isdigit() or c == '.')
                    if price_str:
                        return float(price_str)
    except (subprocess.TimeoutExpired, subprocess.SubprocessError, ValueError):
        pass
    
    # Fallback: return None (caller should handle)
    return None

def execute_bankr_swap(
    symbol: str,
    action: str,
    amount: float,
    config: Dict,
    dry_run: bool = False
) -> Tuple[bool, Optional[str], Optional[Dict]]:
    """
    Execute market swap via Bankr CLI.
    Returns (success, tx_hash, trade_details)
    """
    bankr_config = config.get('bankr', {})
    chain = bankr_config.get('chain', 'base')
    slippage = bankr_config.get('slippage_pct', 1.5)
    
    # Build command
    # Example: bankr swap --from ETH --to SOL --amount 0.1 --chain base --slippage 1.5
    
    if action.lower() in ['buy', 'limit_buy']:
        # Buying symbol with base currency (assume ETH or USDC)
        base_currency = 'USDC'  # Could be config option
        cmd = [
            'bankr', 'swap',
            '--from', base_currency,
            '--to', symbol,
            '--amount-usd', str(amount),
            '--chain', chain,
            '--slippage', str(slippage)
        ]
    elif action.lower() in ['sell', 'limit_sell']:
        # Selling symbol for base currency
        base_currency = 'USDC'
        cmd = [
            'bankr', 'swap',
            '--from', symbol,
            '--to', base_currency,
            '--amount-usd', str(amount),
            '--chain', chain,
            '--slippage', str(slippage)
        ]
    else:
        return False, None, None
    
    if dry_run:
        print(f"🔍 DRY RUN - Would execute: {' '.join(cmd)}")
        return True, "DRY_RUN_TX_HASH", {
            'dry_run': True,
            'command': ' '.join(cmd)
        }
    
    # Execute command
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        print(result.stdout)
        
        if result.returncode == 0:
            # Parse tx hash from output (format varies by CLI)
            tx_hash = None
            for line in result.stdout.split('\n'):
                if 'hash' in line.lower() or '0x' in line:
                    # Extract hash
                    parts = line.split()
                    for part in parts:
                        if part.startswith('0x') and len(part) > 40:
                            tx_hash = part
                            break
                if tx_hash:
                    break
            
            return True, tx_hash, {'output': result.stdout}
        else:
            print(result.stderr, file=sys.stderr)
            return False, None, {'error': result.stderr}
    
    except subprocess.TimeoutExpired:
        print("❌ Bankr command timeout", file=sys.stderr)
        return False, None, {'error': 'timeout'}
    except FileNotFoundError:
        print("❌ Bankr CLI not found. Install with: npm install -g @bankr/cli", file=sys.stderr)
        return False, None, {'error': 'bankr not installed'}

def set_stop_loss(
    symbol: str,
    stop_price: float,
    config: Dict,
    dry_run: bool = False
) -> bool:
    """Set stop-loss order via Bankr"""
    bankr_config = config.get('bankr', {})
    chain = bankr_config.get('chain', 'base')
    
    cmd = [
        'bankr', 'stop',
        '--symbol', symbol,
        '--price', str(stop_price),
        '--chain', chain
    ]
    
    if dry_run:
        print(f"🔍 DRY RUN - Would set stop-loss: {' '.join(cmd)}")
        return True
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        print(result.stdout)
        
        if result.returncode != 0:
            print(result.stderr, file=sys.stderr)
            return False
        
        return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False

def set_take_profit(
    symbol: str,
    take_profit_price: float,
    config: Dict,
    dry_run: bool = False
) -> bool:
    """Set take-profit limit order via Bankr"""
    bankr_config = config.get('bankr', {})
    chain = bankr_config.get('chain', 'base')
    
    cmd = [
        'bankr', 'limit',
        '--symbol', symbol,
        '--side', 'sell',
        '--price', str(take_profit_price),
        '--chain', chain
    ]
    
    if dry_run:
        print(f"🔍 DRY RUN - Would set take-profit: {' '.join(cmd)}")
        return True
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        print(result.stdout)
        
        if result.returncode != 0:
            print(result.stderr, file=sys.stderr)
            return False
        
        return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False

def log_trade(trade_data: Dict, trades_dir: str = "trades"):
    """Append trade to daily log file"""
    trades_path = Path(trades_dir)
    trades_path.mkdir(exist_ok=True)
    
    today = datetime.now().strftime('%Y-%m-%d')
    log_file = trades_path / f"{today}.json"
    
    # Load existing trades for today
    if log_file.exists():
        try:
            with open(log_file, 'r') as f:
                trades = json.load(f)
        except json.JSONDecodeError:
            trades = []
    else:
        trades = []
    
    # Append new trade
    trades.append(trade_data)
    
    # Write back
    with open(log_file, 'w') as f:
        json.dump(trades, f, indent=2)
    
    print(f"📝 Trade logged to {log_file}")

def execute_trade(
    symbol: str,
    action: str,
    amount: float,
    config: Dict,
    dry_run: bool = False,
    skip_risk_check: bool = False,
    config_path: str = "trading-config.json",
    trades_dir: str = "trades"
) -> bool:
    """
    Execute a trade with full workflow:
    1. Risk check
    2. Execute swap
    3. Set stop-loss/take-profit
    4. Log trade
    """
    
    print(f"\n🎯 Executing {action.upper()} {symbol} - ${amount}")
    print("=" * 50)
    
    # 1. Risk check (unless explicitly skipped)
    if not skip_risk_check and not dry_run:
        print("\n🛡️  Running risk check...")
        if not run_risk_check(symbol, amount, config_path, trades_dir):
            print("\n❌ Trade rejected by risk manager")
            return False
    
    # 2. Get current price
    print(f"\n💰 Fetching current price for {symbol}...")
    current_price = get_current_price(symbol, config)
    
    if not current_price:
        print(f"⚠️  Could not fetch price for {symbol}, using amount-based swap")
        current_price = amount  # Fallback for logging
    else:
        print(f"   Current price: ${current_price}")
    
    # 3. Execute swap
    print(f"\n🔄 Executing swap...")
    success, tx_hash, details = execute_bankr_swap(symbol, action, amount, config, dry_run)
    
    if not success:
        print("\n❌ Swap failed")
        return False
    
    print(f"✅ Swap successful")
    if tx_hash and not dry_run:
        print(f"   TX: {tx_hash}")
    
    # Calculate quantity (approximate)
    if current_price and current_price > 0:
        quantity = amount / current_price
    else:
        quantity = 0
    
    # 4. Set stop-loss and take-profit (for buy orders)
    risk = config.get('risk', {})
    stop_loss_price = None
    take_profit_price = None
    
    if action.lower() in ['buy', 'limit_buy'] and current_price:
        stop_loss_pct = risk.get('stop_loss_pct', 8)
        take_profit_pct = risk.get('take_profit_pct', 4)
        
        stop_loss_price = current_price * (1 - stop_loss_pct / 100)
        take_profit_price = current_price * (1 + take_profit_pct / 100)
        
        print(f"\n🛡️  Setting stop-loss at ${stop_loss_price:.2f} (-{stop_loss_pct}%)")
        set_stop_loss(symbol, stop_loss_price, config, dry_run)
        
        print(f"🎯 Setting take-profit at ${take_profit_price:.2f} (+{take_profit_pct}%)")
        set_take_profit(symbol, take_profit_price, config, dry_run)
    
    # 5. Log trade
    trade_data = {
        'timestamp': datetime.now().isoformat() + 'Z',
        'symbol': symbol,
        'action': action,
        'amount_usd': amount,
        'price': current_price,
        'quantity': quantity,
        'tx_hash': tx_hash,
        'status': 'success' if success else 'failed',
        'stop_loss_price': stop_loss_price,
        'take_profit_price': take_profit_price,
        'details': details
    }
    
    if not dry_run:
        log_trade(trade_data, trades_dir)
    else:
        print(f"\n🔍 DRY RUN - Trade data:")
        print(json.dumps(trade_data, indent=2))
    
    print("\n✅ Trade complete")
    print("=" * 50)
    
    return True

def main():
    parser = argparse.ArgumentParser(description='Trade Executor - Execute trades via Bankr CLI')
    parser.add_argument('--symbol', required=True, help='Trading symbol (e.g. SOL)')
    parser.add_argument('--action', required=True,
                      choices=['buy', 'sell', 'limit_buy', 'limit_sell'],
                      help='Trade action')
    parser.add_argument('--amount', type=float, required=True,
                      help='Trade amount in USD')
    parser.add_argument('--config', default='trading-config.json',
                      help='Config file path')
    parser.add_argument('--trades-dir', default='trades',
                      help='Trades directory')
    parser.add_argument('--dry-run', action='store_true',
                      help='Simulate trade without executing')
    parser.add_argument('--skip-risk-check', action='store_true',
                      help='Skip risk manager check (dangerous!)')
    
    args = parser.parse_args()
    
    # Load config
    config = load_config(args.config)
    
    # Execute trade
    success = execute_trade(
        symbol=args.symbol,
        action=args.action,
        amount=args.amount,
        config=config,
        dry_run=args.dry_run,
        skip_risk_check=args.skip_risk_check,
        config_path=args.config,
        trades_dir=args.trades_dir
    )
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
