"""状态持久化 - SQLite（含安全防护）"""
from __future__ import annotations
import json, logging, os, sqlite3, stat
from contextlib import contextmanager
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional
from .config import get_config
from .models import SignalType, TradeSignal

logger = logging.getLogger(__name__)


def _protect_database(db_path: str) -> None:
    """设置数据库文件权限，仅 owner 可读写"""
    try:
        db_file = Path(db_path)
        if db_file.exists():
            # 设置文件权限为 600 (rw-------)
            os.chmod(db_path, stat.S_IRUSR | stat.S_IWUSR)
            logger.debug(f"已设置数据库文件权限: {db_path}")
        
        # 设置目录权限为 700 (rwx------)
        db_dir = db_file.parent
        if db_dir.exists():
            os.chmod(str(db_dir), stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
            logger.debug(f"已设置数据库目录权限: {db_dir}")
    except Exception as e:
        logger.warning(f"设置数据库权限失败: {e}")


class StateStore:
    def __init__(self, db_path: str | None = None):
        self._db_path = db_path or get_config().db_path
        self._ensure_directory()
        self._init_db()
        _protect_database(self._db_path)

    def _ensure_directory(self):
        """确保数据库目录存在并设置安全权限"""
        db_dir = Path(self._db_path).parent
        if not db_dir.exists():
            db_dir.mkdir(parents=True, mode=0o700, exist_ok=True)
            logger.info(f"创建数据库目录: {db_dir}")

    @contextmanager
    def _conn(self):
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        try: yield conn; conn.commit()
        except: conn.rollback(); raise
        finally: conn.close()

    def _init_db(self):
        with self._conn() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS signals (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, code TEXT, name TEXT, signal_type TEXT, price REAL, support REAL, resistance REAL, stop_loss REAL, target_price REAL, position_pct REAL, confidence REAL, strategy_name TEXT, reason TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP);
                CREATE TABLE IF NOT EXISTS positions (code TEXT PRIMARY KEY, name TEXT, entry_price REAL, entry_date TEXT, shares INTEGER DEFAULT 0, stop_loss REAL, target_price REAL, status TEXT DEFAULT 'open', updated_at TEXT DEFAULT CURRENT_TIMESTAMP);
                CREATE TABLE IF NOT EXISTS reports (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, report_json TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP);
                CREATE INDEX IF NOT EXISTS idx_signals_date ON signals(date);
            """)

    def save_signal(self, signal: TradeSignal):
        with self._conn() as conn:
            conn.execute("INSERT INTO signals (date,code,name,signal_type,price,support,resistance,stop_loss,target_price,position_pct,confidence,strategy_name,reason) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (signal.timestamp, signal.code, signal.name, signal.signal_type.value, signal.price, signal.support, signal.resistance, signal.stop_loss, signal.target_price, signal.position_pct, signal.confidence, signal.strategy_name, signal.reason))

    def get_signals(self, code=None, start_date=None, end_date=None, limit=50):
        clauses, params = [], []
        if code: clauses.append("code=?"); params.append(code)
        if start_date: clauses.append("date>=?"); params.append(start_date)
        if end_date: clauses.append("date<=?"); params.append(end_date)
        where = " WHERE " + " AND ".join(clauses) if clauses else ""
        params.append(limit)
        with self._conn() as conn:
            return [dict(r) for r in conn.execute(f"SELECT * FROM signals{where} ORDER BY date DESC LIMIT ?", params).fetchall()]

    def save_position(self, code, name, entry_price, shares, stop_loss, target_price):
        with self._conn() as conn:
            conn.execute("INSERT OR REPLACE INTO positions (code,name,entry_price,entry_date,shares,stop_loss,target_price,status,updated_at) VALUES (?,?,?,?,?,?,?,'open',?)",
                (code, name, entry_price, date.today().isoformat(), shares, stop_loss, target_price, datetime.now().isoformat()))

    def get_open_positions(self):
        with self._conn() as conn:
            return [dict(r) for r in conn.execute("SELECT * FROM positions WHERE status='open'").fetchall()]

    def close_position(self, code):
        with self._conn() as conn:
            conn.execute("UPDATE positions SET status='closed',updated_at=? WHERE code=?", (datetime.now().isoformat(), code))

    def save_report(self, report_json):
        with self._conn() as conn:
            conn.execute("INSERT INTO reports (date,report_json) VALUES (?,?)", (date.today().isoformat(), report_json))

    def get_signal_stats(self, days=30):
        with self._conn() as conn:
            row = conn.execute("SELECT COUNT(*) as total, SUM(CASE WHEN signal_type='买入' THEN 1 ELSE 0 END) as buy_count, AVG(confidence) as avg_confidence FROM signals WHERE date>=date('now',?)", (f"-{days} days",)).fetchone()
            return dict(row) if row else {}

    # ===================== 信号绩效追踪 =====================

    def _init_performance_table(self):
        with self._conn() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS signal_performance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    signal_id INTEGER,
                    code TEXT,
                    signal_date TEXT,
                    signal_type TEXT,
                    entry_price REAL,
                    strategy_name TEXT,
                    check_date TEXT,
                    return_1d REAL,
                    return_3d REAL,
                    return_5d REAL,
                    return_10d REAL,
                    hit_target INTEGER DEFAULT 0,
                    hit_stop INTEGER DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (signal_id) REFERENCES signals(id)
                );
                CREATE INDEX IF NOT EXISTS idx_perf_code ON signal_performance(code);
                CREATE INDEX IF NOT EXISTS idx_perf_date ON signal_performance(signal_date);
                CREATE INDEX IF NOT EXISTS idx_perf_strategy ON signal_performance(strategy_name);
            """)

    def save_signal_performance(self, signal_id: int, code: str, signal_date: str,
                                signal_type: str, entry_price: float,
                                strategy_name: str, returns: Dict[str, float],
                                hit_target: bool = False, hit_stop: bool = False):
        """保存信号绩效数据"""
        self._init_performance_table()
        with self._conn() as conn:
            conn.execute(
                """INSERT INTO signal_performance
                   (signal_id, code, signal_date, signal_type, entry_price,
                    strategy_name, check_date, return_1d, return_3d, return_5d, return_10d,
                    hit_target, hit_stop)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (signal_id, code, signal_date, signal_type, entry_price,
                 strategy_name, date.today().isoformat(),
                 returns.get("1d", 0), returns.get("3d", 0),
                 returns.get("5d", 0), returns.get("10d", 0),
                 int(hit_target), int(hit_stop)),
            )

    def get_strategy_performance(self, strategy_name: str = None, days: int = 90):
        """获取策略历史绩效统计"""
        self._init_performance_table()
        clauses, params = [], []
        if strategy_name:
            clauses.append("strategy_name=?")
            params.append(strategy_name)
        clauses.append("signal_date>=date('now',?)")
        params.append(f"-{days} days")
        where = " WHERE " + " AND ".join(clauses)

        with self._conn() as conn:
            rows = conn.execute(
                f"""SELECT strategy_name,
                        COUNT(*) as total,
                        AVG(return_5d) as avg_ret_5d,
                        SUM(CASE WHEN return_5d > 0 THEN 1 ELSE 0 END) as wins,
                        SUM(CASE WHEN hit_target = 1 THEN 1 ELSE 0 END) as target_hits,
                        SUM(CASE WHEN hit_stop = 1 THEN 1 ELSE 0 END) as stop_hits
                    FROM signal_performance{where}
                    GROUP BY strategy_name""",
                params,
            ).fetchall()
            return [dict(r) for r in rows]

    def get_pending_performance_checks(self, days_back: int = 10):
        """获取需要回填绩效的历史信号"""
        with self._conn() as conn:
            cutoff = (date.today() - timedelta(days=days_back)).isoformat()
            rows = conn.execute(
                """SELECT s.id, s.code, s.date as signal_date, s.signal_type,
                          s.price as entry_price, s.strategy_name
                   FROM signals s
                   WHERE s.date >= ? AND s.date < ?
                     AND NOT EXISTS (
                         SELECT 1 FROM signal_performance sp
                         WHERE sp.signal_id = s.id
                     )
                   ORDER BY s.date""",
                (cutoff, date.today().isoformat()),
            ).fetchall()
            return [dict(r) for r in rows]

    def get_signal_win_rate_by_strategy(self, days: int = 90) -> Dict[str, float]:
        """获取各策略信号胜率，用于动态权重调整"""
        perf = self.get_strategy_performance(days=days)
        result = {}
        for p in perf:
            total = p.get("total", 0)
            wins = p.get("wins", 0)
            if total >= 5:
                result[p["strategy_name"]] = wins / total
        return result
