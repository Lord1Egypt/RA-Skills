"""Wiki 结构化数据存储层。

每个 wiki 目录下维护一个 data.db（SQLite），存储所有结构化数据。
Markdown 页面只负责叙事分析，不在 frontmatter 中存储 data/history。

用法：
    from store import WikiStore

    store = WikiStore(".wiki/my-research/")
    store.upsert_data("alpha-corp", "管理规模", 1200, "亿元", "2025-12", "2026-04-policy-doc")
    store.add_relation("alpha-corp", "受托人市场格局", "part_of")

    # 查询
    rows = store.query_data(page_slug="alpha-corp")
    timeline = store.query_timeline(field="管理规模")

CLI:
    python store.py init .wiki/my-research/
    python store.py dump .wiki/my-research/
"""

from __future__ import annotations

import sqlite3
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any, Optional


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS pages (
    slug        TEXT PRIMARY KEY,
    title       TEXT NOT NULL,
    type        TEXT NOT NULL CHECK(type IN ('source','entity','concept','analysis','mental-model')),
    confidence  TEXT NOT NULL DEFAULT 'medium' CHECK(confidence IN ('high','medium','low','contested')),
    created     TEXT NOT NULL,
    updated     TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS data_points (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    page_slug   TEXT NOT NULL REFERENCES pages(slug),
    field       TEXT NOT NULL,
    value       REAL NOT NULL,
    unit        TEXT NOT NULL,
    period      TEXT NOT NULL,
    source_slug TEXT NOT NULL,
    scope       TEXT,
    verified    INTEGER,              -- NULL=unknown, 0=false, 1=true
    confidence  TEXT DEFAULT 'high' CHECK(confidence IN ('high','medium','low','contested')),
    created_at  TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE(page_slug, field, period)  -- 同一页面同一字段同一时段只留一条（upsert 覆盖）
);

CREATE TABLE IF NOT EXISTS history (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    page_slug   TEXT NOT NULL REFERENCES pages(slug),
    field       TEXT NOT NULL,
    old_value   REAL NOT NULL,
    old_unit    TEXT NOT NULL,
    old_source  TEXT NOT NULL,
    new_source  TEXT,
    reason      TEXT NOT NULL,
    date        TEXT NOT NULL,
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS relations (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    from_slug   TEXT NOT NULL,
    to_slug     TEXT NOT NULL,
    type        TEXT NOT NULL,
    created_at  TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE(from_slug, to_slug, type)
);

CREATE INDEX IF NOT EXISTS idx_dp_page ON data_points(page_slug);
CREATE INDEX IF NOT EXISTS idx_dp_field ON data_points(field);
CREATE INDEX IF NOT EXISTS idx_dp_period ON data_points(period);
CREATE INDEX IF NOT EXISTS idx_rel_from ON relations(from_slug);
CREATE INDEX IF NOT EXISTS idx_rel_to ON relations(to_slug);
CREATE INDEX IF NOT EXISTS idx_hist_page ON history(page_slug);
"""


class WikiStore:
    """单个 wiki 的 SQLite 存储接口。"""

    def __init__(self, wiki_dir: str | Path):
        self.wiki_dir = Path(wiki_dir)
        self.db_path = self.wiki_dir / "data.db"
        self._conn: Optional[sqlite3.Connection] = None

    @property
    def conn(self) -> sqlite3.Connection:
        if self._conn is None:
            self._conn = sqlite3.connect(str(self.db_path))
            self._conn.row_factory = sqlite3.Row
            self._conn.execute("PRAGMA journal_mode=WAL")
            self._conn.execute("PRAGMA foreign_keys=ON")
        return self._conn

    def init_db(self) -> None:
        """创建表结构（幂等）。"""
        self.conn.executescript(SCHEMA_SQL)
        self.conn.commit()

    def close(self) -> None:
        if self._conn:
            self._conn.close()
            self._conn = None

    # ── Pages ──

    def upsert_page(self, slug: str, title: str, page_type: str,
                    confidence: str = "medium",
                    created: str = "", updated: str = "") -> None:
        today = date.today().isoformat()
        self.conn.execute("""
            INSERT INTO pages (slug, title, type, confidence, created, updated)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(slug) DO UPDATE SET
                title=excluded.title, type=excluded.type,
                confidence=excluded.confidence, updated=excluded.updated
        """, (slug, title, page_type, confidence, created or today, updated or today))
        self.conn.commit()

    # ── Data Points ──

    def upsert_data(self, page_slug: str, field: str, value: float,
                    unit: str, period: str, source_slug: str,
                    scope: str = None, verified: bool = None,
                    confidence: str = "high") -> Optional[dict]:
        """写入数据点。如果同字段同时段已有旧值，自动写入 history 并返回旧记录。"""
        # 查旧值
        old = self.conn.execute(
            "SELECT value, unit, source_slug FROM data_points WHERE page_slug=? AND field=? AND period=?",
            (page_slug, field, period)
        ).fetchone()

        old_record = None
        if old and old["value"] != value:
            old_record = dict(old)
            # 写 history
            self.conn.execute("""
                INSERT INTO history (page_slug, field, old_value, old_unit, old_source, new_source, reason, date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (page_slug, field, old["value"], old["unit"], old["source_slug"],
                  source_slug, f"{field}: {old['value']} → {value}", date.today().isoformat()))

        # upsert data point
        v_int = None if verified is None else (1 if verified else 0)
        self.conn.execute("""
            INSERT INTO data_points (page_slug, field, value, unit, period, source_slug, scope, verified, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(page_slug, field, period) DO UPDATE SET
                value=excluded.value, unit=excluded.unit,
                source_slug=excluded.source_slug, scope=excluded.scope,
                verified=excluded.verified, confidence=excluded.confidence
        """, (page_slug, field, value, unit, period, source_slug, scope, v_int, confidence))
        self.conn.commit()
        return old_record

    # ── Relations ──

    def add_relation(self, from_slug: str, to_slug: str, rel_type: str) -> None:
        self.conn.execute("""
            INSERT OR IGNORE INTO relations (from_slug, to_slug, type)
            VALUES (?, ?, ?)
        """, (from_slug, to_slug, rel_type))
        self.conn.commit()

    # ── Queries ──

    def query_data(self, page_slug: str = None, field: str = None) -> list[dict]:
        """查询数据点。可按页面或字段过滤。"""
        sql = "SELECT * FROM data_points WHERE 1=1"
        params: list = []
        if page_slug:
            sql += " AND page_slug=?"
            params.append(page_slug)
        if field:
            sql += " AND field=?"
            params.append(field)
        sql += " ORDER BY period DESC"
        return [dict(r) for r in self.conn.execute(sql, params).fetchall()]

    def query_timeline(self, field: str, page_slug: str = None) -> list[dict]:
        """查询某字段的时间线（含历史值）。"""
        # 当前值
        sql = "SELECT page_slug, field, value, unit, period, source_slug, 'current' as status FROM data_points WHERE field=?"
        params: list = [field]
        if page_slug:
            sql += " AND page_slug=?"
            params.append(page_slug)

        # 历史值
        sql2 = "SELECT page_slug, field, old_value as value, old_unit as unit, date as period, old_source as source_slug, 'superseded' as status FROM history WHERE field=?"
        params2: list = [field]
        if page_slug:
            sql2 += " AND page_slug=?"
            params2.append(page_slug)

        rows = [dict(r) for r in self.conn.execute(sql, params).fetchall()]
        rows += [dict(r) for r in self.conn.execute(sql2, params2).fetchall()]
        rows.sort(key=lambda r: r.get("period", ""), reverse=True)
        return rows

    def query_relations(self, slug: str = None, rel_type: str = None) -> list[dict]:
        sql = "SELECT * FROM relations WHERE 1=1"
        params: list = []
        if slug:
            sql += " AND (from_slug=? OR to_slug=?)"
            params += [slug, slug]
        if rel_type:
            sql += " AND type=?"
            params.append(rel_type)
        return [dict(r) for r in self.conn.execute(sql, params).fetchall()]

    def get_page(self, slug: str) -> Optional[dict]:
        row = self.conn.execute("SELECT * FROM pages WHERE slug=?", (slug,)).fetchone()
        return dict(row) if row else None

    def list_pages(self, page_type: str = None) -> list[dict]:
        sql = "SELECT * FROM pages"
        params: list = []
        if page_type:
            sql += " WHERE type=?"
            params.append(page_type)
        sql += " ORDER BY updated DESC"
        return [dict(r) for r in self.conn.execute(sql, params).fetchall()]

    def stats(self) -> dict:
        """返回 wiki 数据库统计。"""
        s: dict[str, Any] = {}
        s["pages"] = self.conn.execute("SELECT COUNT(*) FROM pages").fetchone()[0]
        s["data_points"] = self.conn.execute("SELECT COUNT(*) FROM data_points").fetchone()[0]
        s["relations"] = self.conn.execute("SELECT COUNT(*) FROM relations").fetchone()[0]
        s["contested"] = self.conn.execute("SELECT COUNT(*) FROM data_points WHERE confidence='contested'").fetchone()[0]
        for row in self.conn.execute("SELECT type, COUNT(*) as cnt FROM pages GROUP BY type").fetchall():
            s[f"pages_{row['type']}"] = row["cnt"]
        return s

    def dump(self) -> str:
        """输出人类可读的数据库摘要。"""
        st = self.stats()
        lines = [
            f"Wiki Store: {self.wiki_dir.name}",
            f"{'='*50}",
            f"Pages: {st['pages']} | Data Points: {st['data_points']} | Relations: {st['relations']} | Contested: {st['contested']}",
            "",
        ]
        # pages by type
        for pt in ["entity", "concept", "source", "analysis", "mental-model"]:
            key = f"pages_{pt}"
            if st.get(key):
                lines.append(f"  {pt}: {st[key]}")

        # recent data points
        recent = self.conn.execute(
            "SELECT page_slug, field, value, unit, period FROM data_points ORDER BY created_at DESC LIMIT 10"
        ).fetchall()
        if recent:
            lines += ["", "Recent Data Points:"]
            for r in recent:
                lines.append(f"  {r['page_slug']}.{r['field']} = {r['value']} {r['unit']} ({r['period']})")

        # relations
        rels = self.conn.execute("SELECT * FROM relations ORDER BY created_at DESC LIMIT 10").fetchall()
        if rels:
            lines += ["", "Recent Relations:"]
            for r in rels:
                lines.append(f"  {r['from_slug']} --{r['type']}--> {r['to_slug']}")

        return "\n".join(lines)


# ── CLI ──

def main():
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python store.py init <wiki_dir>   — initialize data.db")
        print("  python store.py dump <wiki_dir>   — dump database summary")
        sys.exit(1)

    cmd, target = sys.argv[1], Path(sys.argv[2])
    store = WikiStore(target)

    if cmd == "init":
        store.init_db()
        print(f"Initialized: {store.db_path}")
    elif cmd == "dump":
        if not store.db_path.exists():
            print(f"No data.db found in {target}")
            sys.exit(1)
        print(store.dump())
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)

    store.close()


if __name__ == "__main__":
    main()
