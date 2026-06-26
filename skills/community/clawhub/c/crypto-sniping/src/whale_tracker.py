"""Whale tracking and large order monitoring."""
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta

from .binance_client import BinanceClient

@dataclass
class WhaleAlert:
    symbol: str
    type: str  # "LARGE_ORDER", "LIQUIDATION", "FUNDING_SPIKE"
    side: str  # "BUY" or "SELL"
    size: float
    price: float
    total_value: float
    timestamp: int
    details: str

class WhaleTracker:
    """Track whale movements and large market events."""
    
    def __init__(self, client: BinanceClient, 
                 min_order_size: float = 1_000_000,
                 liquidation_threshold: float = 10_000_000,
                 funding_rate_alert: float = 0.01):
        self.client = client
        self.min_order_size = min_order_size
        self.liquidation_threshold = liquidation_threshold
        self.funding_rate_alert = funding_rate_alert
        self.recent_alerts: List[WhaleAlert] = []
    
    def scan_orderbook(self, symbol: str) -> List[WhaleAlert]:
        """Scan orderbook for large orders."""
        alerts = []
        
        try:
            orderbook = self.client.get_orderbook(symbol, limit=100)
            current_price = self.client.get_symbol_price(symbol)
            
            # Check bids (buy orders)
            for bid in orderbook.get("bids", [])[:20]:
                price, quantity = float(bid[0]), float(bid[1])
                value = price * quantity
                
                if value >= self.min_order_size:
                    alert = WhaleAlert(
                        symbol=symbol,
                        type="LARGE_ORDER",
                        side="BUY",
                        size=quantity,
                        price=price,
                        total_value=value,
                        timestamp=int(datetime.now().timestamp() * 1000),
                        details=f"Large bid: {quantity:.4f} @ ${price:,.2f} (${value:,.0f})"
                    )
                    alerts.append(alert)
                    self.recent_alerts.append(alert)
            
            # Check asks (sell orders)
            for ask in orderbook.get("asks", [])[:20]:
                price, quantity = float(ask[0]), float(ask[1])
                value = price * quantity
                
                if value >= self.min_order_size:
                    alert = WhaleAlert(
                        symbol=symbol,
                        type="LARGE_ORDER",
                        side="SELL",
                        size=quantity,
                        price=price,
                        total_value=value,
                        timestamp=int(datetime.now().timestamp() * 1000),
                        details=f"Large ask: {quantity:.4f} @ ${price:,.2f} (${value:,.0f})"
                    )
                    alerts.append(alert)
                    self.recent_alerts.append(alert)
        
        except Exception as e:
            logging.error(f"Failed to scan orderbook for {symbol}: {e}")
        
        return alerts
    
    def check_liquidations(self, symbol: str) -> List[WhaleAlert]:
        """Check for recent liquidations."""
        alerts = []
        
        try:
            # Get liquidations from last hour
            end_time = int(datetime.now().timestamp() * 1000)
            start_time = end_time - (60 * 60 * 1000)  # 1 hour ago
            
            liquidations = self.client.get_liquidations(symbol, start_time, end_time, limit=100)
            
            for liq in liquidations:
                value = float(liq.get("executedQty", 0)) * float(liq.get("avgPrice", 0))
                
                if value >= self.liquidation_threshold:
                    alert = WhaleAlert(
                        symbol=symbol,
                        type="LIQUIDATION",
                        side=liq.get("side", "UNKNOWN"),
                        size=float(liq.get("executedQty", 0)),
                        price=float(liq.get("avgPrice", 0)),
                        total_value=value,
                        timestamp=liq.get("time", int(datetime.now().timestamp() * 1000)),
                        details=f"Liquidation: {liq.get('side')} {value:,.0f} USDT"
                    )
                    alerts.append(alert)
                    self.recent_alerts.append(alert)
        
        except Exception as e:
            logging.error(f"Failed to check liquidations for {symbol}: {e}")
        
        return alerts
    
    def check_funding_rate(self, symbol: str) -> Optional[WhaleAlert]:
        """Check for unusual funding rates."""
        try:
            funding_rate = self.client.get_funding_rate(symbol)
            
            if abs(funding_rate) >= self.funding_rate_alert:
                direction = "positive" if funding_rate > 0 else "negative"
                
                alert = WhaleAlert(
                    symbol=symbol,
                    type="FUNDING_SPIKE",
                    side="LONGS_PAY" if funding_rate > 0 else "SHORTS_PAY",
                    size=0,
                    price=0,
                    total_value=abs(funding_rate),
                    timestamp=int(datetime.now().timestamp() * 1000),
                    details=f"High funding rate: {funding_rate:.4%} ({direction}) - {symbol}"
                )
                self.recent_alerts.append(alert)
                return alert
        
        except Exception as e:
            logging.error(f"Failed to check funding rate for {symbol}: {e}")
        
        return None
    
    def get_recent_alerts(self, minutes: int = 60) -> List[WhaleAlert]:
        """Get alerts from last N minutes."""
        cutoff = int((datetime.now() - timedelta(minutes=minutes)).timestamp() * 1000)
        return [a for a in self.recent_alerts if a.timestamp >= cutoff]
    
    def analyze_whale_activity(self, symbol: str) -> Dict:
        """Analyze overall whale activity for a symbol."""
        alerts = self.get_recent_alerts(minutes=60)
        symbol_alerts = [a for a in alerts if a.symbol == symbol]
        
        buy_pressure = sum(a.total_value for a in symbol_alerts if a.side == "BUY")
        sell_pressure = sum(a.total_value for a in symbol_alerts if a.side == "SELL")
        
        return {
            "symbol": symbol,
            "buy_pressure": buy_pressure,
            "sell_pressure": sell_pressure,
            "net_pressure": buy_pressure - sell_pressure,
            "alert_count": len(symbol_alerts),
            "dominant_side": "BUY" if buy_pressure > sell_pressure else "SELL",
            "significant": max(buy_pressure, sell_pressure) > 5_000_000
        }
