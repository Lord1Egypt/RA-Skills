"""
工单数据库 — SQLite 工单管理
"""
import sqlite3
import os
import uuid
from datetime import datetime, timedelta
from typing import Optional
from .config_loader import get_config


class TicketDB:
    """工单数据库管理"""

    def __init__(self, config: dict = None):
        cfg = config or get_config()
        db_path = cfg.get("database", {}).get("path", "data/tickets.db")
        # 确保目录存在
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self._init_db()

    def _get_conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        return conn

    def _init_db(self):
        """初始化数据库表"""
        with self._get_conn() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS tickets (
                    id TEXT PRIMARY KEY,
                    ticket_id TEXT UNIQUE NOT NULL,
                    email_uid TEXT,
                    message_id TEXT,
                    from_addr TEXT NOT NULL,
                    from_name TEXT,
                    subject TEXT,
                    body_preview TEXT,
                    category TEXT,
                    confidence REAL,
                    sentiment TEXT,
                    urgency_level INTEGER,
                    urgency_score INTEGER,
                    language TEXT,
                    entities_json TEXT,
                    summary TEXT,
                    status TEXT DEFAULT 'PENDING',
                    escalation_level TEXT,
                    escalation_reason TEXT,
                    rma_number TEXT,
                    reply_subject TEXT,
                    reply_body TEXT,
                    reply_sent_at TEXT,
                    sla_deadline TEXT,
                    sla_breached INTEGER DEFAULT 0,
                    created_at TEXT DEFAULT (datetime('now', 'localtime')),
                    updated_at TEXT DEFAULT (datetime('now', 'localtime')),
                    resolved_at TEXT
                );

                CREATE TABLE IF NOT EXISTS email_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ticket_id TEXT NOT NULL,
                    direction TEXT NOT NULL,  -- INBOUND / OUTBOUND
                    subject TEXT,
                    body_preview TEXT,
                    timestamp TEXT DEFAULT (datetime('now', 'localtime')),
                    FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id)
                );

                CREATE TABLE IF NOT EXISTS spam_features (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    domain TEXT,
                    keyword TEXT,
                    hit_count INTEGER DEFAULT 1,
                    first_seen TEXT DEFAULT (datetime('now', 'localtime')),
                    last_seen TEXT DEFAULT (datetime('now', 'localtime'))
                );

                CREATE TABLE IF NOT EXISTS daily_stats (
                    date TEXT PRIMARY KEY,
                    total_received INTEGER DEFAULT 0,
                    auto_replied INTEGER DEFAULT 0,
                    escalated INTEGER DEFAULT 0,
                    archived INTEGER DEFAULT 0,
                    avg_frt_seconds REAL DEFAULT 0,
                    avg_urgency REAL DEFAULT 0,
                    csat_avg REAL DEFAULT 0,
                    csat_count INTEGER DEFAULT 0
                );

                CREATE INDEX IF NOT EXISTS idx_tickets_status ON tickets(status);
                CREATE INDEX IF NOT EXISTS idx_tickets_from_addr ON tickets(from_addr);
                CREATE INDEX IF NOT EXISTS idx_tickets_created ON tickets(created_at);
                CREATE INDEX IF NOT EXISTS idx_tickets_category ON tickets(category);
                CREATE INDEX IF NOT EXISTS idx_email_log_ticket ON email_log(ticket_id);
            """)

    def create_ticket(self, email, classification, urgency, ticket_id: str = None) -> str:
        """创建工单，返回 ticket_id"""
        if ticket_id is None:
            ticket_id = self._generate_ticket_id()

        import json
        with self._get_conn() as conn:
            conn.execute("""
                INSERT INTO tickets (id, ticket_id, email_uid, message_id, from_addr, from_name,
                    subject, body_preview, category, confidence, sentiment, urgency_level,
                    urgency_score, language, entities_json, summary, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'PENDING')
            """, (
                str(uuid.uuid4()), ticket_id, email.uid, email.message_id,
                email.from_addr, email.from_name, email.subject[:200],
                email.body_plain[:500], classification.category, classification.confidence,
                classification.sentiment, urgency.level, urgency.score,
                classification.language, json.dumps(classification.entities, ensure_ascii=False),
                classification.summary,
            ))

        # 记录收件日志
        self._log_email(ticket_id, "INBOUND", email.subject, email.body_plain[:200])

        return ticket_id

    def update_reply(self, ticket_id: str, reply_subject: str, reply_body: str):
        """记录已发送的回复"""
        now = datetime.now().isoformat()
        with self._get_conn() as conn:
            conn.execute("""
                UPDATE tickets SET
                    reply_subject = ?, reply_body = ?, reply_sent_at = ?,
                    status = 'AUTO_REPLIED', updated_at = ?
                WHERE ticket_id = ?
            """, (reply_subject, reply_body, now, now, ticket_id))

        self._log_email(ticket_id, "OUTBOUND", reply_subject, reply_body[:200])

    def escalate(self, ticket_id: str, level: str, reason: str):
        """升级工单"""
        now = datetime.now().isoformat()
        with self._get_conn() as conn:
            conn.execute("""
                UPDATE tickets SET
                    status = 'ESCALATED', escalation_level = ?, escalation_reason = ?,
                    updated_at = ?
                WHERE ticket_id = ?
            """, (level, reason, now, ticket_id))

    def resolve(self, ticket_id: str):
        """标记工单已解决"""
        now = datetime.now().isoformat()
        with self._get_conn() as conn:
            conn.execute("""
                UPDATE tickets SET status = 'RESOLVED', resolved_at = ?, updated_at = ?
                WHERE ticket_id = ?
            """, (now, now, ticket_id))

    def archive(self, ticket_id: str, reason: str = "SPAM"):
        """归档工单"""
        with self._get_conn() as conn:
            conn.execute("""
                UPDATE tickets SET status = 'ARCHIVED', escalation_reason = ?, updated_at = datetime('now', 'localtime')
                WHERE ticket_id = ?
            """, (reason, ticket_id))

    def get_ticket(self, ticket_id: str) -> Optional[dict]:
        """查询单个工单"""
        with self._get_conn() as conn:
            row = conn.execute("SELECT * FROM tickets WHERE ticket_id = ?", (ticket_id,)).fetchone()
            return dict(row) if row else None

    def get_recent_email_count(self, from_addr: str, hours: int = 24) -> int:
        """获取某发件人最近 N 小时内的邮件数"""
        cutoff = (datetime.now() - timedelta(hours=hours)).isoformat()
        with self._get_conn() as conn:
            row = conn.execute(
                "SELECT COUNT(*) as cnt FROM tickets WHERE from_addr = ? AND created_at >= ?",
                (from_addr, cutoff)
            ).fetchone()
            return row["cnt"] if row else 0

    def get_reply_rounds(self, from_addr: str) -> int:
        """获取与某发件人的对话轮数 (OUTBOUND 数量)"""
        with self._get_conn() as conn:
            row = conn.execute(
                """SELECT COUNT(DISTINCT t.ticket_id) as cnt
                   FROM tickets t JOIN email_log e ON t.ticket_id = e.ticket_id
                   WHERE t.from_addr = ? AND e.direction = 'OUTBOUND'""",
                (from_addr,)
            ).fetchone()
            return row["cnt"] if row else 0

    def add_spam_feature(self, domain: str = "", keyword: str = ""):
        """记录垃圾邮件特征"""
        with self._get_conn() as conn:
            if domain:
                conn.execute("""
                    INSERT INTO spam_features (domain, hit_count) VALUES (?, 1)
                    ON CONFLICT(domain) DO UPDATE SET hit_count = hit_count + 1, last_seen = datetime('now', 'localtime')
                """, (domain,))
            if keyword:
                conn.execute("""
                    INSERT INTO spam_features (keyword, hit_count) VALUES (?, 1)
                    ON CONFLICT(keyword) DO UPDATE SET hit_count = hit_count + 1, last_seen = datetime('now', 'localtime')
                """, (keyword,))

    def get_stats(self) -> dict:
        """获取今日统计"""
        today = datetime.now().strftime("%Y-%m-%d")
        with self._get_conn() as conn:
            # 今日概览
            stats = {}
            row = conn.execute("""
                SELECT
                    COUNT(*) as total,
                    SUM(CASE WHEN status = 'AUTO_REPLIED' THEN 1 ELSE 0 END) as auto_replied,
                    SUM(CASE WHEN status = 'ESCALATED' THEN 1 ELSE 0 END) as escalated,
                    SUM(CASE WHEN status = 'ARCHIVED' THEN 1 ELSE 0 END) as archived,
                    SUM(CASE WHEN status = 'PENDING' THEN 1 ELSE 0 END) as pending
                FROM tickets WHERE date(created_at) = ?
            """, (today,)).fetchone()
            stats["overview"] = dict(row)

            # 分类分布
            rows = conn.execute("""
                SELECT category, COUNT(*) as cnt
                FROM tickets WHERE date(created_at) = ?
                GROUP BY category
            """, (today,)).fetchall()
            stats["category_dist"] = {r["category"]: r["cnt"] for r in rows}

            # 情感分布
            rows = conn.execute("""
                SELECT sentiment, COUNT(*) as cnt
                FROM tickets WHERE date(created_at) = ?
                GROUP BY sentiment
            """, (today,)).fetchall()
            stats["sentiment_dist"] = {r["sentiment"]: r["cnt"] for r in rows}

            # 升级列表
            rows = conn.execute("""
                SELECT ticket_id, from_addr, from_name, subject, category,
                       sentiment, urgency_level, escalation_level, escalation_reason, created_at
                FROM tickets WHERE status = 'ESCALATED' AND date(created_at) = ?
                ORDER BY urgency_level DESC
            """, (today,)).fetchall()
            stats["escalated_list"] = [dict(r) for r in rows]

            # SLA 健康度
            row = conn.execute("""
                SELECT
                    COUNT(*) as total_tickets,
                    SUM(CASE WHEN sla_breached = 1 THEN 1 ELSE 0 END) as breached,
                    SUM(CASE WHEN sla_breached = 0 AND status IN ('AUTO_REPLIED', 'RESOLVED') THEN 1 ELSE 0 END) as met
                FROM tickets WHERE date(created_at) = ?
            """, (today,)).fetchone()
            sla = dict(row)
            total = sla.get("total_tickets", 1) or 1
            stats["sla_health"] = {
                "total": total,
                "met_pct": round(sla.get("met", 0) / total * 100, 1),
                "breached_pct": round(sla.get("breached", 0) / total * 100, 1),
            }

        return stats

    def get_trend(self, days: int = 7) -> list[dict]:
        """获取最近 N 天的趋势数据"""
        with self._get_conn() as conn:
            rows = conn.execute("""
                SELECT date(created_at) as day,
                       COUNT(*) as total,
                       SUM(CASE WHEN status = 'AUTO_REPLIED' THEN 1 ELSE 0 END) as auto_replied,
                       SUM(CASE WHEN status = 'ESCALATED' THEN 1 ELSE 0 END) as escalated,
                       AVG(urgency_score) as avg_urgency
                FROM tickets
                WHERE created_at >= datetime('now', ? || ' days')
                GROUP BY day ORDER BY day
            """, (f"-{days}",)).fetchall()
            return [dict(r) for r in rows]

    @staticmethod
    def _generate_ticket_id() -> str:
        """生成工单编号 TK-YYYYMMDD-NNNN"""
        today = datetime.now().strftime("%Y%m%d")
        # 简单随机后缀
        suffix = uuid.uuid4().hex[:4].upper()
        return f"TK-{today}-{suffix}"

    def _log_email(self, ticket_id: str, direction: str, subject: str, body: str):
        """记录邮件日志"""
        with self._get_conn() as conn:
            conn.execute("""
                INSERT INTO email_log (ticket_id, direction, subject, body_preview)
                VALUES (?, ?, ?, ?)
            """, (ticket_id, direction, subject[:200], body[:200]))
