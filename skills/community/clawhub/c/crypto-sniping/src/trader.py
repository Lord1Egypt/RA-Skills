"""Trading execution and risk management."""
import logging
import sqlite3
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import json

from .binance_client import BinanceClient
from .signals import Signal, SignalType

@dataclass
class Position:
    symbol: str
    entry_price: float
    quantity: float
    side: str  # "BUY" or "SELL"
    stop_loss: float
    take_profits: List[Dict]  # [{"price": float, "sell_percent": float}]
    timestamp: int
    order_id: Optional[int] = None

@dataclass
class Trade:
    id: int
    symbol: str
    side: str
    entry_price: float
    exit_price: Optional[float]
    quantity: float
    pnl: Optional[float]
    pnl_percent: Optional[float]
    timestamp: int
    status: str  # "OPEN", "CLOSED", "CANCELLED"

class RiskManager:
    """Manage position sizing and risk."""
    
    def __init__(self, max_daily_trades: int = 5, max_daily_loss: float = 500.0,
                 default_position_size: float = 100.0, stop_loss_percent: float = 5.0,
                 take_profit_tiers: Optional[List[Dict]] = None):
        self.max_daily_trades = max_daily_trades
        self.max_daily_loss = max_daily_loss
        self.default_position_size = default_position_size
        self.stop_loss_percent = stop_loss_percent
        
        # Default take profit tiers: 50% at 2x, 25% at 5x, 25% at 10x
        self.take_profit_tiers = take_profit_tiers or [
            {"percent": 100, "sell": 50},
            {"percent": 400, "sell": 25},
            {"percent": 900, "sell": 25}
        ]
    
    def calculate_position_size(self, signal_confidence: int, account_balance: float) -> float:
        """Calculate position size based on confidence and balance."""
        # Base size adjusted by confidence (1-5 scale)
        confidence_multiplier = signal_confidence / 3.0  # 0.33x to 1.67x
        size = self.default_position_size * confidence_multiplier
        
        # Cap at 10% of account
        max_size = account_balance * 0.10
        return min(size, max_size)
    
    def calculate_stop_loss(self, entry_price: float, side: str) -> float:
        """Calculate stop loss price."""
        if side == "BUY":
            return entry_price * (1 - self.stop_loss_percent / 100)
        else:
            return entry_price * (1 + self.stop_loss_percent / 100)
    
    def calculate_take_profits(self, entry_price: float, side: str) -> List[Dict]:
        """Calculate take profit levels."""
        take_profits = []
        for tier in self.take_profit_tiers:
            profit_percent = tier["percent"]
            sell_percent = tier["sell"]
            
            if side == "BUY":
                price = entry_price * (1 + profit_percent / 100)
            else:
                price = entry_price * (1 - profit_percent / 100)
            
            take_profits.append({
                "price": round(price, 2),
                "sell_percent": sell_percent,
                "hit": False
            })
        return take_profits
    
    def check_daily_limits(self, trades_today: int, pnl_today: float) -> bool:
        """Check if we can trade today."""
        if trades_today >= self.max_daily_trades:
            logging.warning(f"Daily trade limit reached: {trades_today}/{self.max_daily_trades}")
            return False
        
        if pnl_today <= -self.max_daily_loss:
            logging.warning(f"Daily loss limit hit: ${pnl_today:.2f}")
            return False
        
        return True

class Trader:
    """Execute trades and manage positions."""
    
    def __init__(self, client: BinanceClient, risk_manager: RiskManager, 
                 db_path: str = "trades.db", paper_mode: bool = True):
        self.client = client
        self.risk_manager = risk_manager
        self.db_path = db_path
        self.paper_mode = paper_mode
        self.positions: Dict[str, Position] = {}
        
        self._init_db()
        self._load_open_positions()
    
    def _init_db(self):
        """Initialize SQLite database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                side TEXT NOT NULL,
                entry_price REAL NOT NULL,
                exit_price REAL,
                quantity REAL NOT NULL,
                stop_loss REAL NOT NULL,
                take_profits TEXT NOT NULL,
                pnl REAL,
                pnl_percent REAL,
                timestamp INTEGER NOT NULL,
                status TEXT NOT NULL,
                order_id INTEGER,
                paper_mode BOOLEAN NOT NULL
            )
        """)
        
        conn.commit()
        conn.close()
    
    def _load_open_positions(self):
        """Load open positions from database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT symbol, entry_price, quantity, side, stop_loss, 
                   take_profits, timestamp, order_id
            FROM trades WHERE status = 'OPEN'
        """)
        
        for row in cursor.fetchall():
            position = Position(
                symbol=row[0],
                entry_price=row[1],
                quantity=row[2],
                side=row[3],
                stop_loss=row[4],
                take_profits=json.loads(row[5]),
                timestamp=row[6],
                order_id=row[7]
            )
            self.positions[position.symbol] = position
        
        conn.close()
    
    def execute_signal(self, signal: Signal) -> Optional[Trade]:
        """Execute a trading signal."""
        if signal.type == SignalType.HOLD:
            return None
        
        symbol = signal.symbol
        side = "BUY" if signal.type == SignalType.BUY else "SELL"
        
        # Check if we already have a position
        if symbol in self.positions:
            logging.info(f"Already have position in {symbol}, skipping signal")
            return None
        
        # Get account info for position sizing
        try:
            account = self.client.get_account()
            usdt_balance = float([b for b in account["balances"] if b["asset"] == "USDT"][0]["free"])
        except Exception as e:
            logging.error(f"Failed to get account balance: {e}")
            return None
        
        # Check daily limits
        trades_today, pnl_today = self._get_daily_stats()
        if not self.risk_manager.check_daily_limits(trades_today, pnl_today):
            return None
        
        # Calculate position size
        position_size = self.risk_manager.calculate_position_size(signal.confidence, usdt_balance)
        if position_size < 10:  # Minimum $10 trade
            logging.info(f"Position size too small: ${position_size:.2f}")
            return None
        
        # Calculate stop loss and take profits
        stop_loss = self.risk_manager.calculate_stop_loss(signal.price, side)
        take_profits = self.risk_manager.calculate_take_profits(signal.price, side)
        
        # Execute trade
        try:
            if self.paper_mode:
                order_id = self._paper_trade(symbol, side, position_size, signal.price)
            else:
                order = self.client.place_order(
                    symbol=symbol,
                    side=side,
                    order_type="MARKET",
                    quote_quantity=position_size
                )
                order_id = order["orderId"]
            
            # Record position
            position = Position(
                symbol=symbol,
                entry_price=signal.price,
                quantity=position_size / signal.price,
                side=side,
                stop_loss=stop_loss,
                take_profits=take_profits,
                timestamp=signal.timestamp,
                order_id=order_id
            )
            self.positions[symbol] = position
            self._save_position(position)
            
            logging.info(f"Opened {side} position in {symbol} at ${signal.price:.2f}")
            
            return Trade(
                id=0,  # Will be set by DB
                symbol=symbol,
                side=side,
                entry_price=signal.price,
                exit_price=None,
                quantity=position.quantity,
                pnl=None,
                pnl_percent=None,
                timestamp=signal.timestamp,
                status="OPEN"
            )
            
        except Exception as e:
            logging.error(f"Failed to execute trade: {e}")
            return None
    
    def _paper_trade(self, symbol: str, side: str, quantity: float, price: float) -> int:
        """Simulate a trade in paper mode."""
        import random
        return random.randint(1000000, 9999999)
    
    def _save_position(self, position: Position):
        """Save position to database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO trades (symbol, side, entry_price, quantity, stop_loss,
                              take_profits, timestamp, status, order_id, paper_mode)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            position.symbol, position.side, position.entry_price, position.quantity,
            position.stop_loss, json.dumps(position.take_profits), position.timestamp,
            "OPEN", position.order_id, self.paper_mode
        ))
        
        conn.commit()
        conn.close()
    
    def check_positions(self):
        """Check open positions for exit conditions."""
        for symbol, position in list(self.positions.items()):
            try:
                current_price = self.client.get_symbol_price(symbol)
                self._evaluate_position(position, current_price)
            except Exception as e:
                logging.error(f"Failed to check position {symbol}: {e}")
    
    def _evaluate_position(self, position: Position, current_price: float):
        """Evaluate if position should be closed."""
        # Check stop loss
        if position.side == "BUY" and current_price <= position.stop_loss:
            self._close_position(position, current_price, "STOP_LOSS")
            return
        elif position.side == "SELL" and current_price >= position.stop_loss:
            self._close_position(position, current_price, "STOP_LOSS")
            return
        
        # Check take profits
        for tier in position.take_profits:
            if tier["hit"]:
                continue
            
            tp_price = tier["price"]
            if (position.side == "BUY" and current_price >= tp_price) or \
               (position.side == "SELL" and current_price <= tp_price):
                
                # In real trading, this would partially close the position
                tier["hit"] = True
                logging.info(f"Take profit hit for {position.symbol} at ${tp_price:.2f}")
                
                # If all TPs hit, close position
                if all(t["hit"] for t in position.take_profits):
                    self._close_position(position, current_price, "TAKE_PROFIT")
    
    def _close_position(self, position: Position, exit_price: float, reason: str):
        """Close a position."""
        # Calculate P&L
        if position.side == "BUY":
            pnl = (exit_price - position.entry_price) * position.quantity
            pnl_percent = (exit_price - position.entry_price) / position.entry_price * 100
        else:
            pnl = (position.entry_price - exit_price) * position.quantity
            pnl_percent = (position.entry_price - exit_price) / position.entry_price * 100
        
        # Update database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE trades 
            SET exit_price = ?, pnl = ?, pnl_percent = ?, status = 'CLOSED'
            WHERE symbol = ? AND status = 'OPEN'
        """, (exit_price, pnl, pnl_percent, position.symbol))
        
        conn.commit()
        conn.close()
        
        # Remove from active positions
        del self.positions[position.symbol]
        
        logging.info(f"Closed {position.symbol} at ${exit_price:.2f} ({reason}). P&L: ${pnl:.2f} ({pnl_percent:.2f}%)")
    
    def _get_daily_stats(self) -> tuple:
        """Get today's trade count and P&L."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        today_start = int(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp() * 1000)
        
        cursor.execute("""
            SELECT COUNT(*), COALESCE(SUM(pnl), 0)
            FROM trades 
            WHERE timestamp >= ?
        """, (today_start,))
        
        result = cursor.fetchone()
        conn.close()
        
        return result[0], result[1]
    
    def get_open_positions(self) -> List[Position]:
        """Get all open positions."""
        return list(self.positions.values())
    
    def get_trade_history(self, days: int = 7) -> List[Trade]:
        """Get recent trade history."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        since = int((datetime.now().timestamp() - days * 86400) * 1000)
        
        cursor.execute("""
            SELECT id, symbol, side, entry_price, exit_price, quantity,
                   pnl, pnl_percent, timestamp, status
            FROM trades 
            WHERE timestamp >= ?
            ORDER BY timestamp DESC
        """, (since,))
        
        trades = []
        for row in cursor.fetchall():
            trades.append(Trade(
                id=row[0], symbol=row[1], side=row[2], entry_price=row[3],
                exit_price=row[4], quantity=row[5], pnl=row[6],
                pnl_percent=row[7], timestamp=row[8], status=row[9]
            ))
        
        conn.close()
        return trades
