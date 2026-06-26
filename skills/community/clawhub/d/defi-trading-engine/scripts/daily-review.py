#!/usr/bin/env python3
"""
Daily Review - Analyze trade performance and suggest improvements
Calculates P&L, win rate, identifies patterns, and generates recommendations.
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from collections import defaultdict

def load_trades(trades_dir: str, start_date: str = None, end_date: str = None) -> List[Dict]:
    """Load trades within date range"""
    trades = []
    trades_path = Path(trades_dir)
    
    if not trades_path.exists():
        return []
    
    # Parse date range
    if start_date:
        start = datetime.fromisoformat(start_date).date()
    else:
        start = None
    
    if end_date:
        end = datetime.fromisoformat(end_date).date()
    else:
        end = datetime.now().date()
    
    # Load all trade files
    for trade_file in sorted(trades_path.glob("*.json")):
        # Extract date from filename (YYYY-MM-DD.json)
        try:
            file_date = datetime.strptime(trade_file.stem, '%Y-%m-%d').date()
        except ValueError:
            continue
        
        # Check if in range
        if start and file_date < start:
            continue
        if end and file_date > end:
            continue
        
        # Load trades from file
        try:
            with open(trade_file, 'r') as f:
                file_trades = json.load(f)
                if isinstance(file_trades, list):
                    trades.extend(file_trades)
        except (json.JSONDecodeError, IOError):
            continue
    
    return trades

def calculate_pnl(trades: List[Dict], initial_balance: float = 1000.0) -> Dict:
    """Calculate profit/loss metrics"""
    balance = initial_balance
    peak_balance = initial_balance
    max_drawdown = 0.0
    
    total_pnl = 0.0
    realized_pnl = 0.0
    
    # Track positions
    positions = defaultdict(lambda: {'quantity': 0, 'cost_basis': 0})
    
    winning_trades = []
    losing_trades = []
    
    for trade in trades:
        if trade.get('status') != 'success':
            continue
        
        symbol = trade.get('symbol')
        action = trade.get('action', '').lower()
        amount = trade.get('amount_usd', 0)
        price = trade.get('price', 0)
        quantity = trade.get('quantity', 0)
        
        if action in ['buy', 'limit_buy']:
            # Open/add to position
            positions[symbol]['quantity'] += quantity
            positions[symbol]['cost_basis'] += amount
            balance -= amount
            
        elif action in ['sell', 'limit_sell']:
            # Close/reduce position
            if positions[symbol]['quantity'] > 0:
                # Calculate P&L for this sell
                avg_cost = positions[symbol]['cost_basis'] / positions[symbol]['quantity']
                pnl = (price - avg_cost) * quantity
                
                realized_pnl += pnl
                balance += amount
                
                # Track as winning or losing trade
                trade_with_pnl = {**trade, 'pnl': pnl}
                if pnl > 0:
                    winning_trades.append(trade_with_pnl)
                else:
                    losing_trades.append(trade_with_pnl)
                
                # Update position
                positions[symbol]['quantity'] -= quantity
                positions[symbol]['cost_basis'] -= avg_cost * quantity
            else:
                # Selling without position (shouldn't happen normally)
                balance += amount
        
        # Update peak and drawdown
        if balance > peak_balance:
            peak_balance = balance
        
        if peak_balance > 0:
            current_drawdown = ((peak_balance - balance) / peak_balance) * 100
            max_drawdown = max(max_drawdown, current_drawdown)
    
    # Calculate unrealized P&L (positions still open)
    # Note: This requires current prices, which we don't have here
    # In production, fetch current prices for open positions
    unrealized_pnl = 0.0
    
    total_pnl = realized_pnl + unrealized_pnl
    
    # Win rate
    total_closed_trades = len(winning_trades) + len(losing_trades)
    win_rate = (len(winning_trades) / total_closed_trades * 100) if total_closed_trades > 0 else 0
    
    # Average win/loss
    avg_win = sum(t['pnl'] for t in winning_trades) / len(winning_trades) if winning_trades else 0
    avg_loss = sum(t['pnl'] for t in losing_trades) / len(losing_trades) if losing_trades else 0
    
    return {
        'initial_balance': initial_balance,
        'final_balance': balance,
        'realized_pnl': realized_pnl,
        'unrealized_pnl': unrealized_pnl,
        'total_pnl': total_pnl,
        'total_pnl_pct': (total_pnl / initial_balance * 100) if initial_balance > 0 else 0,
        'max_drawdown': max_drawdown,
        'win_rate': win_rate,
        'total_trades': len(trades),
        'winning_trades': len(winning_trades),
        'losing_trades': len(losing_trades),
        'avg_win': avg_win,
        'avg_loss': avg_loss,
        'best_trades': sorted(winning_trades, key=lambda t: t.get('pnl', 0), reverse=True)[:3],
        'worst_trades': sorted(losing_trades, key=lambda t: t.get('pnl', 0))[:3],
        'open_positions': {k: v for k, v in positions.items() if v['quantity'] > 0.0001}
    }

def analyze_patterns(trades: List[Dict]) -> Dict:
    """Identify patterns in winning/losing trades"""
    patterns = {
        'by_symbol': defaultdict(lambda: {'wins': 0, 'losses': 0, 'total_pnl': 0}),
        'by_action': defaultdict(lambda: {'wins': 0, 'losses': 0, 'total_pnl': 0}),
        'by_hour': defaultdict(lambda: {'wins': 0, 'losses': 0, 'total_pnl': 0}),
        'observations': []
    }
    
    # Track positions to calculate P&L
    positions = defaultdict(lambda: {'quantity': 0, 'cost_basis': 0})
    
    for trade in trades:
        if trade.get('status') != 'success':
            continue
        
        symbol = trade.get('symbol')
        action = trade.get('action', '').lower()
        amount = trade.get('amount_usd', 0)
        price = trade.get('price', 0)
        quantity = trade.get('quantity', 0)
        timestamp_str = trade.get('timestamp')
        
        # Extract hour
        try:
            timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            hour = timestamp.hour
        except (ValueError, AttributeError):
            hour = None
        
        if action in ['buy', 'limit_buy']:
            positions[symbol]['quantity'] += quantity
            positions[symbol]['cost_basis'] += amount
            
        elif action in ['sell', 'limit_sell']:
            if positions[symbol]['quantity'] > 0:
                avg_cost = positions[symbol]['cost_basis'] / positions[symbol]['quantity']
                pnl = (price - avg_cost) * quantity
                
                # Update patterns
                patterns['by_symbol'][symbol]['total_pnl'] += pnl
                patterns['by_action'][action]['total_pnl'] += pnl
                
                if hour is not None:
                    patterns['by_hour'][hour]['total_pnl'] += pnl
                
                if pnl > 0:
                    patterns['by_symbol'][symbol]['wins'] += 1
                    patterns['by_action'][action]['wins'] += 1
                    if hour is not None:
                        patterns['by_hour'][hour]['wins'] += 1
                else:
                    patterns['by_symbol'][symbol]['losses'] += 1
                    patterns['by_action'][action]['losses'] += 1
                    if hour is not None:
                        patterns['by_hour'][hour]['losses'] += 1
                
                # Update position
                positions[symbol]['quantity'] -= quantity
                positions[symbol]['cost_basis'] -= avg_cost * quantity
    
    # Generate observations
    for symbol, stats in patterns['by_symbol'].items():
        total = stats['wins'] + stats['losses']
        if total >= 3:  # Only report on symbols with 3+ trades
            win_rate = (stats['wins'] / total * 100) if total > 0 else 0
            if win_rate >= 70:
                patterns['observations'].append(f"✅ {symbol}: strong performer ({stats['wins']}/{total} wins, ${stats['total_pnl']:.2f} P&L)")
            elif win_rate <= 30:
                patterns['observations'].append(f"❌ {symbol}: underperformer ({stats['wins']}/{total} wins, ${stats['total_pnl']:.2f} P&L)")
    
    # Check for time-of-day patterns
    if patterns['by_hour']:
        best_hour = max(patterns['by_hour'].items(), key=lambda x: x[1]['total_pnl'])
        worst_hour = min(patterns['by_hour'].items(), key=lambda x: x[1]['total_pnl'])
        
        if best_hour[1]['total_pnl'] > 10:
            patterns['observations'].append(f"⏰ Best trading hour: {best_hour[0]}:00 (${best_hour[1]['total_pnl']:.2f} P&L)")
        
        if worst_hour[1]['total_pnl'] < -10:
            patterns['observations'].append(f"⚠️ Avoid trading around {worst_hour[0]}:00 (${worst_hour[1]['total_pnl']:.2f} P&L)")
    
    return patterns

def generate_recommendations(pnl: Dict, patterns: Dict, config: Dict) -> List[Dict]:
    """Generate parameter adjustment recommendations"""
    recommendations = []
    risk = config.get('risk', {})
    
    # 1. Win rate too low
    if pnl['win_rate'] < 50 and pnl['total_trades'] >= 10:
        recommendations.append({
            'parameter': 'data_sources.min_liquidity_usd',
            'current': config.get('data_sources', {}).get('min_liquidity_usd', 50000),
            'suggested': config.get('data_sources', {}).get('min_liquidity_usd', 50000) * 2,
            'reason': f"Win rate {pnl['win_rate']:.1f}% is low. Tighten entry filters.",
            'priority': 'high'
        })
    
    # 2. Average loss exceeds stop-loss target
    stop_loss_pct = risk.get('stop_loss_pct', 8)
    if pnl['avg_loss'] < -(stop_loss_pct * 0.8):  # If avg loss is 80%+ of stop-loss
        recommendations.append({
            'parameter': 'risk.stop_loss_pct',
            'current': stop_loss_pct,
            'suggested': max(4, stop_loss_pct - 2),
            'reason': f"Average loss ${pnl['avg_loss']:.2f} is close to stop-loss limit. Tighten stop.",
            'priority': 'high'
        })
    
    # 3. Max drawdown too high
    if pnl['max_drawdown'] > 10:
        recommendations.append({
            'parameter': 'risk.max_position_size_usd',
            'current': risk.get('max_position_size_usd', 40),
            'suggested': int(risk.get('max_position_size_usd', 40) * 0.75),
            'reason': f"Max drawdown {pnl['max_drawdown']:.1f}% is high. Reduce position size.",
            'priority': 'medium'
        })
    
    # 4. Win rate good but average win is small
    if pnl['win_rate'] > 60 and pnl['avg_win'] < 5:
        recommendations.append({
            'parameter': 'risk.take_profit_pct',
            'current': risk.get('take_profit_pct', 4),
            'suggested': risk.get('take_profit_pct', 4) + 2,
            'reason': f"High win rate but small avg win ${pnl['avg_win']:.2f}. Let winners run.",
            'priority': 'low'
        })
    
    # 5. Specific symbols underperforming
    for obs in patterns['observations']:
        if '❌' in obs and 'underperformer' in obs:
            symbol = obs.split(':')[0].replace('❌', '').strip()
            recommendations.append({
                'parameter': 'exclusions',
                'current': [],
                'suggested': [symbol],
                'reason': f"Add {symbol} to exclusion list due to poor performance.",
                'priority': 'medium'
            })
    
    return recommendations

def write_review(
    pnl: Dict,
    patterns: Dict,
    recommendations: List[Dict],
    output_path: Path,
    start_date: str,
    end_date: str
):
    """Write markdown review report"""
    
    # Format date range for title
    if start_date:
        date_range = f"{start_date} to {end_date}"
    else:
        date_range = end_date
    
    report = f"""# Trading Review — {date_range}

## Performance Summary

- **Total P&L:** ${pnl['total_pnl']:+.2f} ({pnl['total_pnl_pct']:+.1f}%)
- **Realized P&L:** ${pnl['realized_pnl']:+.2f}
- **Trades:** {pnl['total_trades']} ({pnl['winning_trades']} wins, {pnl['losing_trades']} losses)
- **Win Rate:** {pnl['win_rate']:.1f}%
- **Avg Win:** ${pnl['avg_win']:.2f}
- **Avg Loss:** ${pnl['avg_loss']:.2f}
- **Max Drawdown:** {pnl['max_drawdown']:.1f}%

"""
    
    # Best/worst trades
    if pnl['best_trades']:
        report += "## Top Performers\n\n"
        for i, trade in enumerate(pnl['best_trades'], 1):
            report += f"{i}. {trade['symbol']}: ${trade['pnl']:+.2f}\n"
        report += "\n"
    
    if pnl['worst_trades']:
        report += "## Worst Performers\n\n"
        for i, trade in enumerate(pnl['worst_trades'], 1):
            report += f"{i}. {trade['symbol']}: ${trade['pnl']:+.2f}\n"
        report += "\n"
    
    # Open positions
    if pnl['open_positions']:
        report += "## Open Positions\n\n"
        for symbol, pos in pnl['open_positions'].items():
            report += f"- {symbol}: {pos['quantity']:.4f} (cost basis: ${pos['cost_basis']:.2f})\n"
        report += "\n"
    
    # Pattern analysis
    if patterns['observations']:
        report += "## Pattern Analysis\n\n"
        for obs in patterns['observations']:
            report += f"- {obs}\n"
        report += "\n"
    
    # Recommendations
    if recommendations:
        report += "## Recommended Adjustments\n\n"
        for rec in sorted(recommendations, key=lambda r: {'high': 0, 'medium': 1, 'low': 2}[r['priority']]):
            report += f"### {rec['priority'].upper()}: {rec['parameter']}\n\n"
            report += f"- **Current:** {rec['current']}\n"
            report += f"- **Suggested:** {rec['suggested']}\n"
            report += f"- **Reason:** {rec['reason']}\n\n"
    
    # Next actions
    report += """## Next Actions

- [ ] Review recommendations and update `trading-config.json`
- [ ] Monitor performance for 7 days with new parameters
- [ ] Run backtest if available
- [ ] Check open positions for exit opportunities

---

*Generated by daily-review.py*
"""
    
    # Write to file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(report)
    
    print(f"📄 Review written to {output_path}")

def main():
    parser = argparse.ArgumentParser(description='Daily Review - Analyze trading performance')
    parser.add_argument('--start-date', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end-date', help='End date (YYYY-MM-DD), default: today')
    parser.add_argument('--trades-dir', default='trades', help='Trades directory')
    parser.add_argument('--config', default='trading-config.json', help='Config file')
    parser.add_argument('--output-dir', default='reviews', help='Output directory for reviews')
    
    args = parser.parse_args()
    
    # Default end date to today
    if not args.end_date:
        args.end_date = datetime.now().strftime('%Y-%m-%d')
    
    # Load config
    try:
        with open(args.config, 'r') as f:
            config = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        config = {}
    
    # Load trades
    print(f"📊 Loading trades from {args.trades_dir}...")
    trades = load_trades(args.trades_dir, args.start_date, args.end_date)
    
    if not trades:
        print("❌ No trades found in date range")
        sys.exit(1)
    
    print(f"   Found {len(trades)} trades")
    
    # Calculate P&L
    print("\n💰 Calculating P&L...")
    pnl = calculate_pnl(trades)
    
    # Analyze patterns
    print("🔍 Analyzing patterns...")
    patterns = analyze_patterns(trades)
    
    # Generate recommendations
    print("💡 Generating recommendations...")
    recommendations = generate_recommendations(pnl, patterns, config)
    
    # Write review
    output_filename = f"review-{args.end_date}.md"
    output_path = Path(args.output_dir) / output_filename
    
    print("\n📝 Writing review...")
    write_review(pnl, patterns, recommendations, output_path, args.start_date, args.end_date)
    
    # Also write recommendations as JSON
    rec_path = Path(args.output_dir) / f"recommendations-{args.end_date}.json"
    with open(rec_path, 'w') as f:
        json.dump({
            'date': args.end_date,
            'pnl_summary': {
                'total_pnl': pnl['total_pnl'],
                'win_rate': pnl['win_rate'],
                'max_drawdown': pnl['max_drawdown']
            },
            'recommendations': recommendations
        }, f, indent=2)
    
    print(f"📊 Recommendations JSON: {rec_path}")
    
    # Print summary
    print("\n" + "=" * 50)
    print("📈 PERFORMANCE SUMMARY")
    print("=" * 50)
    print(f"Total P&L: ${pnl['total_pnl']:+.2f} ({pnl['total_pnl_pct']:+.1f}%)")
    print(f"Win Rate: {pnl['win_rate']:.1f}%")
    print(f"Max Drawdown: {pnl['max_drawdown']:.1f}%")
    print(f"Trades: {pnl['total_trades']}")
    print("=" * 50)

if __name__ == '__main__':
    main()
