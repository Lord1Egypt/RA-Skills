#!/usr/bin/env python3
"""Main trading bot runner."""
import os
import sys
import time
import logging
import argparse
import yaml
from typing import Dict, List
from datetime import datetime

from binance_client import BinanceClient
from signals import TechnicalAnalyzer, SignalType
from trader import Trader, RiskManager
from whale_tracker import WhaleTracker
from notifier import Notifier

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('trading_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TradingBot:
    """Main trading bot orchestrator."""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config = self._load_config(config_path)
        self.client = BinanceClient()
        self.analyzer = TechnicalAnalyzer(
            rsi_period=self.config['entry'].get('rsi_period', 14),
            macd_fast=self.config['entry'].get('macd_fast', 12),
            macd_slow=self.config['entry'].get('macd_slow', 26)
        )
        self.risk_manager = RiskManager(
            max_daily_trades=self.config['risk'].get('max_daily_trades', 5),
            max_daily_loss=self.config['risk'].get('max_daily_loss', 500),
            default_position_size=self.config['trading'].get('default_position_size', 100),
            stop_loss_percent=self.config['risk'].get('stop_loss_percent', 5),
            take_profit_tiers=self.config['risk'].get('take_profit_tiers', [
                {"percent": 100, "sell": 50},
                {"percent": 400, "sell": 25},
                {"percent": 900, "sell": 25}
            ])
        )
        self.trader = Trader(
            client=self.client,
            risk_manager=self.risk_manager,
            paper_mode=self.config['trading'].get('mode', 'paper') == 'paper'
        )
        self.whale_tracker = WhaleTracker(
            client=self.client,
            min_order_size=self.config['whale'].get('min_order_size', 1_000_000),
            liquidation_threshold=self.config['whale'].get('liquidation_threshold', 10_000_000),
            funding_rate_alert=self.config['whale'].get('funding_rate_alert', 0.01)
        )
        self.notifier = Notifier()
        self.symbols = self.config['trading'].get('assets', ['BTCUSDT', 'ETHUSDT', 'SOLUSDT'])
        self.running = False
    
    def _load_config(self, path: str) -> Dict:
        """Load configuration from YAML."""
        if not os.path.exists(path):
            logger.warning(f"Config file not found: {path}, using defaults")
            return self._default_config()
        
        with open(path, 'r') as f:
            return yaml.safe_load(f)
    
    def _default_config(self) -> Dict:
        """Return default configuration."""
        return {
            'trading': {
                'mode': 'paper',
                'assets': ['BTCUSDT', 'ETHUSDT', 'SOLUSDT'],
                'default_position_size': 100,
                'max_daily_trades': 5,
                'max_daily_loss': 500
            },
            'entry': {
                'rsi_oversold': 30,
                'rsi_period': 14,
                'macd_fast': 12,
                'macd_slow': 26,
                'volume_spike_threshold': 2.0,
                'min_confidence': 2
            },
            'risk': {
                'stop_loss_percent': 5,
                'take_profit_tiers': [
                    {'percent': 100, 'sell': 50},
                    {'percent': 400, 'sell': 25},
                    {'percent': 900, 'sell': 25}
                ],
                'trailing_stop': True,
                'trailing_stop_percent': 10
            },
            'whale': {
                'min_order_size': 1_000_000,
                'liquidation_threshold': 10_000_000,
                'funding_rate_alert': 0.01
            },
            'notifications': {
                'telegram': {'enabled': False},
                'log_level': 'INFO'
            }
        }
    
    def scan_signals(self) -> List[Dict]:
        """Scan all symbols for trading signals."""
        signals = []
        
        for symbol in self.symbols:
            try:
                # Get kline data
                klines = self.client.get_klines(symbol, interval='1h', limit=100)
                
                # Analyze
                signal = self.analyzer.analyze(klines)
                signal.symbol = symbol  # Attach symbol
                
                if signal.type != SignalType.HOLD and signal.confidence >= self.config['entry'].get('min_confidence', 2):
                    signals.append({
                        'symbol': symbol,
                        'signal': signal,
                        'indicators': self.analyzer.get_indicator_values(klines)
                    })
                    self.notifier.notify_signal(signal)
            
            except Exception as e:
                logger.error(f"Error scanning {symbol}: {e}")
        
        return signals
    
    def check_whale_activity(self):
        """Check for whale activity."""
        for symbol in self.symbols:
            try:
                # Scan orderbook
                alerts = self.whale_tracker.scan_orderbook(symbol)
                for alert in alerts:
                    self.notifier.notify_whale_alert(alert)
                
                # Check liquidations
                liq_alerts = self.whale_tracker.check_liquidations(symbol)
                for alert in liq_alerts:
                    self.notifier.notify_whale_alert(alert)
                
                # Check funding rates
                funding_alert = self.whale_tracker.check_funding_rate(symbol)
                if funding_alert:
                    self.notifier.notify_whale_alert(funding_alert)
            
            except Exception as e:
                logger.error(f"Error checking whale activity for {symbol}: {e}")
    
    def run(self):
        """Run the trading bot loop."""
        logger.info(f"Starting trading bot in {self.config['trading'].get('mode', 'paper')} mode")
        logger.info(f"Monitoring: {', '.join(self.symbols)}")
        
        self.running = True
        
        while self.running:
            try:
                # Check open positions
                self.trader.check_positions()
                
                # Scan for signals
                signals = self.scan_signals()
                
                # Execute trades for high-confidence signals
                for sig_data in signals:
                    signal = sig_data['signal']
                    if signal.confidence >= 4:  # Only auto-trade high confidence
                        trade = self.trader.execute_signal(signal)
                        if trade:
                            self.notifier.notify_trade_opened(trade)
                
                # Check whale activity every 5 minutes
                if int(time.time()) % 300 < 60:
                    self.check_whale_activity()
                
                # Sleep before next iteration
                time.sleep(60)  # Check every minute
                
            except KeyboardInterrupt:
                logger.info("Shutting down...")
                self.running = False
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                self.notifier.notify_error(str(e))
                time.sleep(60)
    
    def get_status(self) -> Dict:
        """Get current bot status."""
        open_positions = self.trader.get_open_positions()
        recent_trades = self.trader.get_trade_history(days=1)
        
        return {
            'mode': self.config['trading'].get('mode', 'paper'),
            'symbols': self.symbols,
            'open_positions': len(open_positions),
            'positions': [{'symbol': p.symbol, 'side': p.side, 'entry': p.entry_price} for p in open_positions],
            'today_trades': len(recent_trades),
            'today_pnl': sum(t.pnl or 0 for t in recent_trades)
        }

def main():
    parser = argparse.ArgumentParser(description='Crypto Sniping Bot')
    parser.add_argument('--config', default='config.yaml', help='Config file path')
    parser.add_argument('--scan', action='store_true', help='Scan signals only (no trading)')
    parser.add_argument('--status', action='store_true', help='Show bot status')
    parser.add_argument('--whales', action='store_true', help='Check whale activity')
    args = parser.parse_args()
    
    bot = TradingBot(args.config)
    
    if args.scan:
        print("Scanning for signals...")
        signals = bot.scan_signals()
        for sig in signals:
            print(f"\n{sig['symbol']}: {sig['signal'].type.value.upper()} (confidence: {sig['signal'].confidence})")
            print(f"  Indicators: {', '.join(sig['signal'].indicators)}")
            print(f"  Current indicators: {sig['indicators']}")
    
    elif args.status:
        status = bot.get_status()
        print(f"\nMode: {status['mode']}")
        print(f"Symbols: {', '.join(status['symbols'])}")
        print(f"Open positions: {status['open_positions']}")
        for pos in status['positions']:
            print(f"  - {pos['symbol']} {pos['side']} @ ${pos['entry']:.2f}")
        print(f"Today's trades: {status['today_trades']}")
        print(f"Today's P&L: ${status['today_pnl']:.2f}")
    
    elif args.whales:
        print("Checking whale activity...")
        bot.check_whale_activity()
        alerts = bot.whale_tracker.get_recent_alerts(minutes=60)
        for alert in alerts:
            print(f"\n{alert.type}: {alert.symbol} {alert.side} ${alert.total_value:,.0f}")
            print(f"  {alert.details}")
    
    else:
        bot.run()

if __name__ == "__main__":
    main()
