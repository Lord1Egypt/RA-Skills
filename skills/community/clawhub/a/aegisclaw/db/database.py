"""
数据库模块 - SQLite 数据存储
"""

import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path


class Database:
    """SQLite 数据库管理"""

    def __init__(self, db_path: str = "db/aegisclaw.db"):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        """初始化数据库表"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # 余额快照表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS balance_snapshots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    bnb_amount REAL NOT NULL,
                    usdt_amount REAL NOT NULL,
                    total_assets INTEGER NOT NULL,
                    timestamp DATETIME NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # 交易记录表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS trades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT NOT NULL,
                    symbol TEXT,
                    side TEXT,
                    quantity REAL NOT NULL,
                    price REAL,
                    order_id TEXT,
                    status TEXT NOT NULL,
                    profit REAL,
                    details TEXT,
                    timestamp DATETIME NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # 安全检查记录表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS security_checks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    account_type TEXT NOT NULL,
                    security_score INTEGER NOT NULL,
                    permissions TEXT,
                    warnings TEXT,
                    timestamp DATETIME NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # 套利机会记录表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS arbitrage_opportunities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    funding_rate REAL NOT NULL,
                    spot_price REAL NOT NULL,
                    mark_price REAL NOT NULL,
                    estimated_profit_pct REAL NOT NULL,
                    executed BOOLEAN DEFAULT 0,
                    timestamp DATETIME NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # 操作日志表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS operation_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    operation_type TEXT NOT NULL,
                    status TEXT NOT NULL,
                    message TEXT,
                    details TEXT,
                    timestamp DATETIME NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            conn.commit()

    # ========== 余额快照 ==========

    def save_balance_snapshot(self, snapshot: Dict) -> int:
        """保存余额快照"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO balance_snapshots
                (bnb_amount, usdt_amount, total_assets, timestamp)
                VALUES (?, ?, ?, ?)
            """, (
                snapshot["bnb_amount"],
                snapshot["usdt_amount"],
                snapshot["total_assets"],
                snapshot["timestamp"]
            ))
            conn.commit()
            return cursor.lastrowid

    def get_balance_history(self, start_time: datetime, end_time: datetime) -> List[Dict]:
        """获取余额历史"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT bnb_amount, usdt_amount, total_assets, timestamp
                FROM balance_snapshots
                WHERE timestamp BETWEEN ? AND ?
                ORDER BY timestamp ASC
            """, (start_time, end_time))
            rows = cursor.fetchall()

        return [{
            "bnb_amount": r[0],
            "usdt_amount": r[1],
            "total_assets": r[2],
            "timestamp": r[3]
        } for r in rows]

    # ========== 交易记录 ==========

    def save_trade(self, trade: Dict) -> int:
        """保存交易记录"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO trades
                (type, symbol, side, quantity, price, order_id, status, profit, details, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                trade["type"],
                trade.get("symbol"),
                trade.get("side"),
                trade["quantity"],
                trade.get("price"),
                trade.get("order_id"),
                trade["status"],
                trade.get("profit"),
                json.dumps(trade.get("details", {})),
                trade.get("timestamp", datetime.now())
            ))
            conn.commit()
            return cursor.lastrowid

    def get_trades(self, start_time: datetime, end_time: datetime) -> List[Dict]:
        """获取交易记录"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT type, symbol, side, quantity, price, order_id, status, profit, details, timestamp
                FROM trades
                WHERE timestamp BETWEEN ? AND ?
                ORDER BY timestamp DESC
            """, (start_time, end_time))
            rows = cursor.fetchall()

        return [{
            "type": r[0],
            "symbol": r[1],
            "side": r[2],
            "quantity": r[3],
            "price": r[4],
            "order_id": r[5],
            "status": r[6],
            "profit": r[7],
            "details": json.loads(r[8]) if r[8] else {},
            "timestamp": r[9]
        } for r in rows]

    # ========== 安全检查 ==========

    def save_security_check(self, check: Dict) -> int:
        """保存安全检查结果"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # 添加 timestamp 字段
            timestamp = check.get("timestamp", datetime.now())
            cursor.execute("""
                INSERT INTO security_checks
                (account_type, security_score, permissions, warnings, timestamp)
                VALUES (?, ?, ?, ?, ?)
            """, (
                check["account_type"],
                check["security_score"],
                json.dumps(check["permissions"]),
                json.dumps(check["warnings"]),
                timestamp
            ))
            conn.commit()
            return cursor.lastrowid

    # ========== 套利机会 ==========

    def save_arbitrage_opportunity(self, opportunity: Dict) -> int:
        """保存套利机会"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO arbitrage_opportunities
                (symbol, funding_rate, spot_price, mark_price, estimated_profit_pct, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                opportunity["symbol"],
                opportunity["funding_rate"],
                opportunity["spot_price"],
                opportunity["mark_price"],
                opportunity["estimated_profit_pct"],
                opportunity.get("timestamp", datetime.now())
            ))
            conn.commit()
            return cursor.lastrowid

    # ========== 操作日志 ==========

    def log_operation(self, operation_type: str, status: str, message: str, details: Dict = None):
        """记录操作日志"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO operation_logs
                (operation_type, status, message, details, timestamp)
                VALUES (?, ?, ?, ?, ?)
            """, (
                operation_type,
                status,
                message,
                json.dumps(details) if details else None,
                datetime.now()
            ))
            conn.commit()

    def get_recent_logs(self, limit: int = 50) -> List[Dict]:
        """获取最近的操作日志"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT operation_type, status, message, details, timestamp
                FROM operation_logs
                ORDER BY timestamp DESC
                LIMIT ?
            """, (limit,))
            rows = cursor.fetchall()

        return [{
            "operation_type": r[0],
            "status": r[1],
            "message": r[2],
            "details": json.loads(r[3]) if r[3] else {},
            "timestamp": r[4]
        } for r in rows]
