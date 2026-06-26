#!/usr/bin/env python3
"""
Crypto Portfolio Analyzer
Tracks multiple wallets, calculates P&L, and generates portfolio reports
"""

import json
import sys
import os
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class PortfolioTracker:
    def __init__(self, config_file: str = None):
        self.config = self.load_config(config_file)
        self.wallets = self.config.get('wallets', {})
        self.watchlist = self.config.get('watchlist', ['BTC', 'ETH', 'SOL'])
        self.cost_basis = self.config.get('cost_basis', {})
        
    def load_config(self, config_file: str) -> Dict:
        """Load configuration from JSON file"""
        if not config_file:
            # Look for config in current directory or skill directory
            possible_paths = [
                './portfolio-config.json',
                '../references/config-example.json',
                os.path.expanduser('~/.openclaw/workspace/crypto-portfolio-config.json')
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    config_file = path
                    break
        
        if config_file and os.path.exists(config_file):
            with open(config_file, 'r') as f:
                return json.load(f)
        
        # Default config
        return {
            'wallets': {},
            'watchlist': ['BTC', 'ETH', 'SOL', 'DOGE', 'XRP'],
            'cost_basis': {},
            'target_allocation': {}
        }
    
    def get_prices(self, coins: List[str] = None) -> Dict[str, float]:
        """Get current prices from CoinGecko"""
        if not coins:
            coins = self.watchlist
            
        # CoinGecko ID mapping
        coin_ids = {
            'BTC': 'bitcoin', 'ETH': 'ethereum', 'SOL': 'solana', 
            'DOGE': 'dogecoin', 'XRP': 'ripple', 'ADA': 'cardano',
            'AVAX': 'avalanche-2', 'LINK': 'chainlink', 'DOT': 'polkadot',
            'UNI': 'uniswap', 'NEAR': 'near', 'ATOM': 'cosmos'
        }
        
        ids = [coin_ids.get(coin, coin.lower()) for coin in coins if coin in coin_ids]
        
        if not ids:
            return {}
            
        try:
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={','.join(ids)}&vs_currencies=usd&include_24hr_change=true&include_market_cap=true"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            # Map back to symbols
            prices = {}
            for coin in coins:
                coin_id = coin_ids.get(coin)
                if coin_id and coin_id in data:
                    prices[coin] = {
                        'price': data[coin_id]['usd'],
                        'change_24h': data[coin_id].get('usd_24h_change', 0),
                        'market_cap': data[coin_id].get('usd_market_cap', 0)
                    }
            return prices
        except Exception as e:
            print(f"Error fetching prices: {e}", file=sys.stderr)
            return {}
    
    def calculate_portfolio_value(self, holdings: Dict[str, float]) -> Dict:
        """Calculate total portfolio value and breakdown"""
        if not holdings:
            return {'total_value': 0, 'breakdown': {}, 'total_pnl': 0, 'total_pnl_pct': 0}
            
        coins = list(holdings.keys())
        prices = self.get_prices(coins)
        
        breakdown = {}
        total_value = 0
        total_cost = 0
        
        for coin, amount in holdings.items():
            if coin in prices:
                current_price = prices[coin]['price']
                position_value = amount * current_price
                cost_basis = self.cost_basis.get(coin, current_price) * amount
                
                breakdown[coin] = {
                    'amount': amount,
                    'price': current_price,
                    'value': position_value,
                    'cost_basis': cost_basis,
                    'pnl': position_value - cost_basis,
                    'pnl_pct': ((position_value - cost_basis) / cost_basis * 100) if cost_basis > 0 else 0,
                    'change_24h': prices[coin].get('change_24h', 0),
                    'allocation_pct': 0  # Will calculate after total
                }
                
                total_value += position_value
                total_cost += cost_basis
        
        # Calculate allocations
        for coin in breakdown:
            breakdown[coin]['allocation_pct'] = (breakdown[coin]['value'] / total_value * 100) if total_value > 0 else 0
        
        return {
            'total_value': total_value,
            'total_cost': total_cost,
            'total_pnl': total_value - total_cost,
            'total_pnl_pct': ((total_value - total_cost) / total_cost * 100) if total_cost > 0 else 0,
            'breakdown': breakdown,
            'timestamp': datetime.now().isoformat()
        }
    
    def generate_report(self, portfolio_data: Dict, format: str = 'text') -> str:
        """Generate portfolio report"""
        if format == 'json':
            return json.dumps(portfolio_data, indent=2, default=str)
        
        # Text format
        lines = []
        lines.append("📊 CRYPTO PORTFOLIO REPORT")
        lines.append("=" * 50)
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        
        # Summary
        total_value = portfolio_data['total_value']
        total_pnl = portfolio_data['total_pnl']
        total_pnl_pct = portfolio_data['total_pnl_pct']
        
        pnl_emoji = "🟢" if total_pnl >= 0 else "🔴"
        lines.append(f"💰 Total Value: ${total_value:,.2f}")
        lines.append(f"{pnl_emoji} Total P&L: ${total_pnl:,.2f} ({total_pnl_pct:+.2f}%)")
        lines.append("")
        
        # Breakdown
        lines.append("📈 POSITION BREAKDOWN:")
        lines.append("-" * 50)
        
        breakdown = portfolio_data['breakdown']
        
        # Sort by value (largest first)
        sorted_positions = sorted(breakdown.items(), key=lambda x: x[1]['value'], reverse=True)
        
        for coin, data in sorted_positions:
            value = data['value']
            pnl = data['pnl']
            pnl_pct = data['pnl_pct']
            allocation = data['allocation_pct']
            change_24h = data['change_24h']
            
            pnl_emoji = "🟢" if pnl >= 0 else "🔴"
            change_emoji = "🟢" if change_24h >= 0 else "🔴"
            
            lines.append(f"{coin}:")
            lines.append(f"  💵 Value: ${value:,.2f} ({allocation:.1f}% of portfolio)")
            lines.append(f"  {pnl_emoji} P&L: ${pnl:,.2f} ({pnl_pct:+.2f}%)")
            lines.append(f"  {change_emoji} 24h: {change_24h:+.2f}%")
            lines.append("")
        
        return "\n".join(lines)
    
    def track_wallet(self, address: str, name: str = None):
        """Add wallet to tracking (placeholder - would integrate with blockchain APIs)"""
        if not name:
            name = f"Wallet {address[:8]}..."
        
        self.wallets[name] = {
            'address': address,
            'added_date': datetime.now().isoformat()
        }
        print(f"✅ Added wallet: {name} ({address})")
    
    def get_market_overview(self) -> Dict:
        """Get market overview for watchlist"""
        prices = self.get_prices(self.watchlist)
        
        if not prices:
            return {'error': 'Failed to fetch market data'}
        
        # Calculate market metrics
        total_mcap = sum(data.get('market_cap', 0) for data in prices.values())
        avg_change = sum(data.get('change_24h', 0) for data in prices.values()) / len(prices)
        
        return {
            'timestamp': datetime.now().isoformat(),
            'total_market_cap': total_mcap,
            'average_24h_change': avg_change,
            'coins': prices,
            'market_sentiment': 'Bullish' if avg_change > 2 else 'Bearish' if avg_change < -2 else 'Neutral'
        }

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Crypto Portfolio Tracker')
    parser.add_argument('--config', '-c', help='Config file path')
    parser.add_argument('--format', '-f', choices=['text', 'json'], default='text', help='Output format')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Portfolio command
    portfolio_parser = subparsers.add_parser('portfolio', help='Analyze portfolio')
    portfolio_parser.add_argument('--holdings', help='Holdings as JSON string or file')
    
    # Market command
    market_parser = subparsers.add_parser('market', help='Market overview')
    
    # Wallet command
    wallet_parser = subparsers.add_parser('wallet', help='Add wallet to track')
    wallet_parser.add_argument('address', help='Wallet address')
    wallet_parser.add_argument('--name', help='Wallet name')
    
    args = parser.parse_args()
    
    tracker = PortfolioTracker(args.config)
    
    if args.command == 'portfolio':
        if args.holdings:
            try:
                if args.holdings.startswith('{'):
                    holdings = json.loads(args.holdings)
                else:
                    with open(args.holdings, 'r') as f:
                        holdings = json.load(f)
                
                portfolio_data = tracker.calculate_portfolio_value(holdings)
                print(tracker.generate_report(portfolio_data, args.format))
                
            except Exception as e:
                print(f"Error: {e}", file=sys.stderr)
                sys.exit(1)
        else:
            print("Error: --holdings required for portfolio command", file=sys.stderr)
            sys.exit(1)
            
    elif args.command == 'market':
        market_data = tracker.get_market_overview()
        if args.format == 'json':
            print(json.dumps(market_data, indent=2, default=str))
        else:
            print("🌍 CRYPTO MARKET OVERVIEW")
            print("=" * 30)
            print(f"Sentiment: {market_data.get('market_sentiment', 'Unknown')}")
            print(f"Avg 24h Change: {market_data.get('average_24h_change', 0):+.2f}%")
            print("\nTop Coins:")
            for coin, data in market_data.get('coins', {}).items():
                emoji = "🟢" if data.get('change_24h', 0) >= 0 else "🔴"
                print(f"  {emoji} {coin}: ${data['price']:,.2f} ({data.get('change_24h', 0):+.2f}%)")
                
    elif args.command == 'wallet':
        tracker.track_wallet(args.address, args.name)
        
    else:
        parser.print_help()

if __name__ == '__main__':
    main()