"""
claw-reliability: SQLite storage layer for agent metrics.
"""

import sqlite3
import json
import os
from datetime import datetime, timezone
from pathlib import Path


class MetricsStore:
    def __init__(self, db_path: str = "data/metrics.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
        self._init_tables()

    def _init_tables(self):
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS tool_invocations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                session_id TEXT,
                agent_id TEXT,
                tool_name TEXT NOT NULL,
                success INTEGER NOT NULL,
                duration_ms REAL,
                error_message TEXT,
                params_summary TEXT,
                created_at TEXT DEFAULT (datetime('now'))
            );
            CREATE TABLE IF NOT EXISTS llm_calls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                session_id TEXT,
                agent_id TEXT,
                model TEXT NOT NULL,
                tokens_in INTEGER,
                tokens_out INTEGER,
                latency_ms REAL,
                estimated_cost_usd REAL,
                created_at TEXT DEFAULT (datetime('now'))
            );
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT UNIQUE NOT NULL,
                agent_id TEXT,
                started_at TEXT,
                ended_at TEXT,
                message_count INTEGER DEFAULT 0,
                tool_call_count INTEGER DEFAULT 0,
                total_tokens INTEGER DEFAULT 0,
                total_cost_usd REAL DEFAULT 0.0
            );
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                severity TEXT NOT NULL,
                alert_type TEXT NOT NULL,
                message TEXT NOT NULL,
                details TEXT,
                acknowledged INTEGER DEFAULT 0,
                created_at TEXT DEFAULT (datetime('now'))
            );
            CREATE TABLE IF NOT EXISTS tool_history (
                tool_name TEXT PRIMARY KEY,
                first_seen TEXT NOT NULL,
                total_calls INTEGER DEFAULT 0,
                total_failures INTEGER DEFAULT 0
            );
            CREATE INDEX IF NOT EXISTS idx_tool_inv_timestamp ON tool_invocations(timestamp);
            CREATE INDEX IF NOT EXISTS idx_tool_inv_tool ON tool_invocations(tool_name);
            CREATE INDEX IF NOT EXISTS idx_llm_timestamp ON llm_calls(timestamp);
            CREATE INDEX IF NOT EXISTS idx_alerts_timestamp ON alerts(timestamp);
            CREATE INDEX IF NOT EXISTS idx_alerts_type ON alerts(alert_type);
        """)
        self.conn.commit()

    def record_tool_invocation(self, tool_name, success, duration_ms=None,
                                session_id=None, agent_id=None,
                                error_message=None, params_summary=None):
        now = datetime.now(timezone.utc).isoformat()
        self.conn.execute("""
            INSERT INTO tool_invocations
            (timestamp, session_id, agent_id, tool_name, success, duration_ms, error_message, params_summary)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (now, session_id, agent_id, tool_name, int(success), duration_ms,
              error_message, params_summary))
        self.conn.execute("""
            INSERT INTO tool_history (tool_name, first_seen, total_calls, total_failures)
            VALUES (?, ?, 1, ?)
            ON CONFLICT(tool_name) DO UPDATE SET
                total_calls = total_calls + 1,
                total_failures = total_failures + ?
        """, (tool_name, now, 0 if success else 1, 0 if success else 1))
        self.conn.commit()

    def get_tool_stats(self, hours=24):
        cur = self.conn.execute("""
            SELECT tool_name,
                COUNT(*) as total_calls,
                SUM(CASE WHEN success=1 THEN 1 ELSE 0 END) as successes,
                SUM(CASE WHEN success=0 THEN 1 ELSE 0 END) as failures,
                AVG(duration_ms) as avg_duration_ms,
                MIN(timestamp) as first_call, MAX(timestamp) as last_call
            FROM tool_invocations
            WHERE timestamp > datetime('now', ?)
            GROUP BY tool_name ORDER BY total_calls DESC
        """, (f'-{hours} hours',))
        return [dict(r) for r in cur.fetchall()]

    def get_recent_tool_failures(self, tool_name, limit=10):
        cur = self.conn.execute("""
            SELECT * FROM tool_invocations
            WHERE tool_name=? AND success=0
            ORDER BY timestamp DESC LIMIT ?
        """, (tool_name, limit))
        return [dict(r) for r in cur.fetchall()]

    def get_consecutive_failures(self, tool_name):
        cur = self.conn.execute("""
            SELECT success FROM tool_invocations
            WHERE tool_name=? ORDER BY timestamp DESC LIMIT 20
        """, (tool_name,))
        count = 0
        for row in cur.fetchall():
            if row['success'] == 0:
                count += 1
            else:
                break
        return count

    def record_llm_call(self, model, tokens_in=None, tokens_out=None,
                         latency_ms=None, estimated_cost_usd=None,
                         session_id=None, agent_id=None):
        now = datetime.now(timezone.utc).isoformat()
        self.conn.execute("""
            INSERT INTO llm_calls
            (timestamp, session_id, agent_id, model, tokens_in, tokens_out, latency_ms, estimated_cost_usd)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (now, session_id, agent_id, model, tokens_in, tokens_out,
              latency_ms, estimated_cost_usd))
        self.conn.commit()

    def get_cost_summary(self, hours=24):
        cur = self.conn.execute("""
            SELECT model, COUNT(*) as call_count,
                SUM(tokens_in) as total_tokens_in,
                SUM(tokens_out) as total_tokens_out,
                SUM(estimated_cost_usd) as total_cost,
                AVG(latency_ms) as avg_latency_ms
            FROM llm_calls WHERE timestamp > datetime('now', ?)
            GROUP BY model
        """, (f'-{hours} hours',))
        rows = [dict(r) for r in cur.fetchall()]
        total_cost = sum(r['total_cost'] or 0 for r in rows)
        total_tokens = sum((r['total_tokens_in'] or 0) + (r['total_tokens_out'] or 0) for r in rows)
        return {"by_model": rows, "total_cost_usd": round(total_cost, 4),
                "total_tokens": total_tokens, "period_hours": hours}

    def get_hourly_cost(self, hours=1):
        cur = self.conn.execute("""
            SELECT COALESCE(SUM(estimated_cost_usd), 0) as cost
            FROM llm_calls WHERE timestamp > datetime('now', ?)
        """, (f'-{hours} hours',))
        return cur.fetchone()['cost']

    def upsert_session(self, session_id, agent_id=None, started_at=None, ended_at=None):
        now = datetime.now(timezone.utc).isoformat()
        self.conn.execute("""
            INSERT INTO sessions (session_id, agent_id, started_at)
            VALUES (?, ?, ?)
            ON CONFLICT(session_id) DO UPDATE SET
                ended_at = COALESCE(?, ended_at),
                agent_id = COALESCE(?, agent_id)
        """, (session_id, agent_id, started_at or now, ended_at, agent_id))
        self.conn.commit()

    def get_session_summary(self):
        cur = self.conn.execute("""
            SELECT s.session_id, s.agent_id, s.started_at, s.ended_at,
                COUNT(DISTINCT t.id) as tool_calls,
                COUNT(DISTINCT l.id) as llm_calls,
                COALESCE(SUM(l.estimated_cost_usd), 0) as total_cost
            FROM sessions s
            LEFT JOIN tool_invocations t ON t.session_id = s.session_id
            LEFT JOIN llm_calls l ON l.session_id = s.session_id
            GROUP BY s.session_id ORDER BY s.started_at DESC LIMIT 20
        """)
        return [dict(r) for r in cur.fetchall()]

    def record_alert(self, severity, alert_type, message, details=None):
        now = datetime.now(timezone.utc).isoformat()
        self.conn.execute("""
            INSERT INTO alerts (timestamp, severity, alert_type, message, details)
            VALUES (?, ?, ?, ?, ?)
        """, (now, severity, alert_type, message,
              json.dumps(details) if details else None))
        self.conn.commit()

    def get_recent_alerts(self, limit=50):
        cur = self.conn.execute(
            "SELECT * FROM alerts ORDER BY timestamp DESC LIMIT ?", (limit,))
        return [dict(r) for r in cur.fetchall()]

    def get_last_alert_time(self, alert_type):
        cur = self.conn.execute(
            "SELECT MAX(timestamp) as last_time FROM alerts WHERE alert_type=?",
            (alert_type,))
        row = cur.fetchone()
        return row['last_time'] if row else None

    def is_tool_known(self, tool_name):
        cur = self.conn.execute(
            "SELECT 1 FROM tool_history WHERE tool_name=?", (tool_name,))
        return cur.fetchone() is not None

    def get_activity_timeline(self, hours=24, bucket_minutes=30):
        cur = self.conn.execute("""
            SELECT
                strftime('%%Y-%%m-%%dT%%H:', timestamp) ||
                    CAST((CAST(strftime('%%M', timestamp) AS INTEGER) / ?) * ? AS TEXT) ||
                    ':00' as bucket,
                COUNT(*) as event_count,
                SUM(CASE WHEN success=1 THEN 1 ELSE 0 END) as successes,
                SUM(CASE WHEN success=0 THEN 1 ELSE 0 END) as failures
            FROM tool_invocations WHERE timestamp > datetime('now', ?)
            GROUP BY bucket ORDER BY bucket
        """, (bucket_minutes, bucket_minutes, f'-{hours} hours'))
        return [dict(r) for r in cur.fetchall()]

    def get_dashboard_summary(self):
        return {
            "tool_stats_24h": self.get_tool_stats(24),
            "cost_summary_24h": self.get_cost_summary(24),
            "recent_alerts": self.get_recent_alerts(10),
            "activity_timeline": self.get_activity_timeline(24),
            "sessions": self.get_session_summary()
        }

    def close(self):
        self.conn.close()
