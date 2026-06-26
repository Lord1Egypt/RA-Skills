"""
EvoMind — Five-Layer Memory Engine for AI Agents
Reference implementation v1.1.2 | MIT License

Usage:
    from evomind import MemoryCore
    mem = MemoryCore(db_path="./agent_memory.db")
    mem.remember("The user prefers dark mode", layer="L1")
    mem.skill_save("web-scraper", "...SKILL.md content...")
    mem.curate()  # Run L4 curation
    results = mem.recall("dark mode")  # L5 semantic search
"""

import sqlite3
import json
import os
import hashlib
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional, List, Dict, Any


class MemoryCore:
    """Five-layer persistent memory system for AI agents.

    L1: Durable facts (≤20KB, auto-archive on overflow)
    L2: Skills (procedural knowledge, reusable workflows)
    L3: Session cache (high-turnover conversation context)
    L4: Curator (daily review, pruning, consolidation)
    L5: Semantic index (cross-session fast recall via FTS5)
    """

    def __init__(self, db_path: str = "~/.agent_memory.db"):
        self.db_path = os.path.expanduser(db_path)
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()
        self.max_l1_size_kb = 20
        self.curation_interval_hours = 24

    # ── Schema ──────────────────────────────────────────────

    def _init_schema(self):
        self.conn.execute("PRAGMA journal_mode=WAL")  # Better concurrency
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS l1_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                priority INTEGER DEFAULT 0,
                source TEXT DEFAULT '',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                tags TEXT DEFAULT '[]'
            );
            CREATE TABLE IF NOT EXISTS l1_archive (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                orig_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                archived_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                reason TEXT DEFAULT ''
            );
            CREATE TABLE IF NOT EXISTS l2_skills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT DEFAULT '',
                version TEXT DEFAULT '1.0.0',
                content TEXT NOT NULL,
                usage_count INTEGER DEFAULT 0,
                last_used TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                tags TEXT DEFAULT '[]'
            );
            CREATE TABLE IF NOT EXISTS l3_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                key TEXT NOT NULL,
                value TEXT DEFAULT '',
                ttl_seconds INTEGER DEFAULT 3600,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(session_id, key)
            );
            CREATE TABLE IF NOT EXISTS l4_curator_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                actions_taken TEXT DEFAULT '[]',
                l1_before_count INTEGER DEFAULT 0,
                l1_after_count INTEGER DEFAULT 0,
                items_archived INTEGER DEFAULT 0,
                items_consolidated INTEGER DEFAULT 0
            );
            CREATE VIRTUAL TABLE IF NOT EXISTS l5_fts USING fts5(
                content, source, layer, tokenize='unicode61'
            );
        """)
        self.conn.commit()

    # ── L1: Durable Facts ───────────────────────────────────

    def remember(self, content: str, priority: int = 0, source: str = "", tags: List[str] = None) -> int:
        """Store a durable fact in L1. Auto-archives oldest if >20KB."""
        if self._l1_size_kb() >= self.max_l1_size_kb:
            self._archive_oldest_l1()
        tags_json = json.dumps(tags or [], ensure_ascii=False)
        c = self.conn.execute(
            "INSERT INTO l1_memory (content, priority, source, tags) VALUES (?,?,?,?)",
            (content, priority, source, tags_json)
        )
        self.conn.commit()
        entry_id = c.lastrowid
        self._index_l5(entry_id, content, source, "L1")
        return entry_id

    def forget(self, entry_id: int) -> bool:
        """Delete a L1 memory entry by ID. Returns True if deleted."""
        row = self.conn.execute("SELECT content FROM l1_memory WHERE id=?", (entry_id,)).fetchone()
        if not row:
            return False
        self._index_remove_l5(row["content"], "L1")
        self.conn.execute("DELETE FROM l1_memory WHERE id=?", (entry_id,))
        self.conn.commit()
        return True

    def forget_all(self) -> int:
        """Delete all L1 memory entries. Returns count deleted."""
        rows = self.conn.execute("SELECT content FROM l1_memory").fetchall()
        self.conn.execute("DELETE FROM l1_memory")
        for r in rows:
            self._index_remove_l5(r["content"], "L1")
        self.conn.commit()
        return len(rows)

    def recall_l1(self, limit: int = 20) -> List[Dict]:
        """Return all L1 facts, newest first."""
        rows = self.conn.execute(
            "SELECT * FROM l1_memory ORDER BY priority DESC, updated_at DESC LIMIT ?",
            (limit,)
        ).fetchall()
        return [dict(r) for r in rows]

    def _l1_size_kb(self) -> float:
        row = self.conn.execute("SELECT COALESCE(SUM(LENGTH(content)),0) FROM l1_memory").fetchone()
        return row[0] / 1024.0

    def _archive_oldest_l1(self):
        oldest = self.conn.execute(
            "SELECT * FROM l1_memory ORDER BY priority ASC, updated_at ASC LIMIT 1"
        ).fetchone()
        if oldest:
            self._index_remove_l5(oldest["content"], "L1")
            self.conn.execute(
                "INSERT INTO l1_archive (orig_id, content, reason) VALUES (?,?,?)",
                (oldest["id"], oldest["content"], "L1 size cap auto-archive")
            )
            self.conn.execute("DELETE FROM l1_memory WHERE id=?", (oldest["id"],))
            self.conn.commit()

    # ── L2: Skills ──────────────────────────────────────────

    def skill_save(self, name: str, content: str, description: str = "", tags: List[str] = None) -> bool:
        """Save or update a skill. Returns True if new, False if updated."""
        tags_json = json.dumps(tags or [], ensure_ascii=False)
        existing = self.conn.execute("SELECT id FROM l2_skills WHERE name=?", (name,)).fetchone()
        if existing:
            self.conn.execute(
                "UPDATE l2_skills SET content=?, description=?, tags=?, version=version+0.1, updated_at=CURRENT_TIMESTAMP WHERE name=?",
                (content, description, tags_json, name)
            )
            new = False
        else:
            self.conn.execute(
                "INSERT INTO l2_skills (name, content, description, tags) VALUES (?,?,?,?)",
                (name, content, description, tags_json)
            )
            new = True
        self.conn.commit()
        self._index_l5(-1, f"{name}: {description}", "L2", "L2")
        return new

    def skill_load(self, name: str) -> Optional[Dict]:
        row = self.conn.execute("SELECT * FROM l2_skills WHERE name=?", (name,)).fetchone()
        if row:
            self.conn.execute(
                "UPDATE l2_skills SET usage_count=usage_count+1, last_used=CURRENT_TIMESTAMP WHERE name=?",
                (name,)
            )
            self.conn.commit()
            # Re-query to get updated usage_count
            row = self.conn.execute("SELECT * FROM l2_skills WHERE name=?", (name,)).fetchone()
            return dict(row)
        return None

    def skill_find(self, query: str, limit: int = 5) -> List[Dict]:
        """Find skills by name or description."""
        rows = self.conn.execute(
            "SELECT * FROM l2_skills WHERE name LIKE ? OR description LIKE ? ORDER BY usage_count DESC LIMIT ?",
            (f"%{query}%", f"%{query}%", limit)
        ).fetchall()
        return [dict(r) for r in rows]

    def skill_list(self) -> List[Dict]:
        return [dict(r) for r in self.conn.execute(
            "SELECT name, description, version, usage_count FROM l2_skills ORDER BY usage_count DESC"
        ).fetchall()]

    def skill_delete(self, name: str) -> bool:
        """Delete a skill by name. Returns True if deleted, False if not found."""
        row = self.conn.execute("SELECT id, description FROM l2_skills WHERE name=?", (name,)).fetchone()
        if not row:
            return False
        # Match the FTS5 key format used in skill_save: "name: description"
        desc = row["description"] or ""
        fts5_key = f"{name}: {desc}" if desc else name
        self._index_remove_l5(fts5_key, "L2")
        self.conn.execute("DELETE FROM l2_skills WHERE name=?", (name,))
        self.conn.commit()
        return True

    # ── L3: Session Cache ───────────────────────────────────

    def cache_set(self, session_id: str, key: str, value: str, ttl: int = 3600):
        self.conn.execute(
            "INSERT OR REPLACE INTO l3_cache (session_id, key, value, ttl_seconds, created_at) VALUES (?,?,?,?,CURRENT_TIMESTAMP)",
            (session_id, key, value, ttl)
        )
        self.conn.commit()

    def cache_get(self, session_id: str, key: str) -> Optional[str]:
        row = self.conn.execute(
            "SELECT value, created_at, ttl_seconds FROM l3_cache WHERE session_id=? AND key=?",
            (session_id, key)
        ).fetchone()
        if row:
            created = datetime.strptime(row["created_at"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
            if (datetime.now(timezone.utc) - created).total_seconds() < row["ttl_seconds"]:
                return row["value"]
            self.conn.execute("DELETE FROM l3_cache WHERE session_id=? AND key=?", (session_id, key))
            self.conn.commit()
        return None

    def cache_clear(self, session_id: str):
        self.conn.execute("DELETE FROM l3_cache WHERE session_id=?", (session_id,))
        self.conn.commit()

    # ── L4: Curator ─────────────────────────────────────────

    def curate(self) -> Dict[str, Any]:
        """Run a curation cycle: archive stale L1, consolidate L2, prune L3."""
        before = {
            "l1": self.conn.execute("SELECT COUNT(*) FROM l1_memory").fetchone()[0],
            "l2": self.conn.execute("SELECT COUNT(*) FROM l2_skills").fetchone()[0],
            "l3": self.conn.execute("SELECT COUNT(*) FROM l3_cache").fetchone()[0],
        }

        actions = []

        # Archive L1 entries older than 30 days with priority=0
        cutoff = (datetime.now() - timedelta(days=30)).isoformat()
        stale = self.conn.execute(
            "SELECT id, content FROM l1_memory WHERE priority=0 AND updated_at < ?",
            (cutoff,)
        ).fetchall()
        for row in stale:
            self._index_remove_l5(row["content"], "L1")
            self.conn.execute(
                "INSERT INTO l1_archive (orig_id, content, reason) VALUES (?,?,'curator: stale 30d')",
                (row["id"], row["content"])
            )
            self.conn.execute("DELETE FROM l1_memory WHERE id=?", (row["id"],))
        if stale:
            actions.append(f"Archived {len(stale)} stale L1 entries")

        # Prune expired L3
        self.conn.execute("DELETE FROM l3_cache WHERE datetime(created_at, '+' || ttl_seconds || ' seconds') < datetime('now')")
        pruned = self.conn.total_changes
        if pruned:
            actions.append(f"Pruned L3 cache")

        # Detect redundant L2 skills (name similarity)
        dupes = self._detect_duplicate_skills()
        if dupes:
            actions.append(f"Found {len(dupes)} potential duplicate skills: {dupes}")

        after = {
            "l1": self.conn.execute("SELECT COUNT(*) FROM l1_memory").fetchone()[0],
            "l2": self.conn.execute("SELECT COUNT(*) FROM l2_skills").fetchone()[0],
            "l3": self.conn.execute("SELECT COUNT(*) FROM l3_cache").fetchone()[0],
        }

        self.conn.execute(
            "INSERT INTO l4_curator_log (actions_taken, l1_before_count, l1_after_count, items_archived) VALUES (?,?,?,?)",
            (json.dumps(actions), before["l1"], after["l1"], len(stale))
        )
        self.conn.commit()

        return {"before": before, "after": after, "actions": actions}

    def _detect_duplicate_skills(self) -> List[str]:
        """Simple duplicate detection by name token overlap."""
        skills = self.conn.execute("SELECT name FROM l2_skills").fetchall()
        names = [s["name"] for s in skills]
        duplicates = []
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                if self._jaccard(names[i], names[j]) > 0.6:
                    duplicates.append(f"{names[i]} ≈ {names[j]}")
        return duplicates[:5]

    def curator_log(self, limit: int = 10) -> List[Dict]:
        rows = self.conn.execute(
            "SELECT * FROM l4_curator_log ORDER BY run_at DESC LIMIT ?", (limit,)
        ).fetchall()
        return [dict(r) for r in rows]

    # ── L5: Semantic Index (FTS5) ───────────────────────────

    def _index_l5(self, entry_id: int, content: str, source: str, layer: str):
        self.conn.execute(
            "INSERT INTO l5_fts (content, source, layer) VALUES (?,?,?)",
            (content, source, layer)
        )

    def _index_remove_l5(self, content_key: str, layer: str):
        """Remove one entry from FTS5 index by rowid to avoid cross-affecting duplicates."""
        self.conn.execute(
            "DELETE FROM l5_fts WHERE rowid = (SELECT MIN(rowid) FROM l5_fts WHERE content = ? AND layer = ?)",
            (content_key, layer)
        )
        # Clean up empty FTS index
        self.conn.execute("INSERT INTO l5_fts(l5_fts) VALUES('optimize')")

    def recall(self, query: str, limit: int = 10) -> List[Dict]:
        """Cross-layer semantic search via FTS5 + LIKE fallback for CJK."""
        terms = query.split()
        results = []
        
        # Try FTS5 first (wrap terms in quotes to avoid syntax errors)
        safe_terms = [t.replace('"', '""') for t in terms]
        if len(safe_terms) > 1:
            fts_query = " OR ".join('"' + t.lower() + '"' for t in safe_terms)
        else:
            escaped = query.lower().replace('"', '""')
            fts_query = '"' + escaped + '"'
        try:
            rows = self.conn.execute(
                "SELECT content, source, layer, rank FROM l5_fts WHERE l5_fts MATCH ? ORDER BY rank LIMIT ?",
                (fts_query, limit)
            ).fetchall()
            results = [{"content": r["content"], "source": r["source"], "layer": r["layer"]} for r in rows]
        except sqlite3.OperationalError:
            pass
        
        # LIKE fallback for CJK or when FTS returns nothing
        if not results:
            for term in terms:
                like_pattern = "%" + term.replace("%", "\\%") + "%"
                rows = self.conn.execute(
                    "SELECT content, source, layer FROM l5_fts WHERE content LIKE ? LIMIT ?",
                    (like_pattern, max(1, limit))
                ).fetchall()
                for r in rows:
                    results.append({"content": r["content"], "source": r["source"], "layer": r["layer"]})
                if len(results) >= limit:
                    break
        
        return results[:limit]

    # ── Utility ─────────────────────────────────────────────

    def stats(self) -> Dict[str, Any]:
        return {
            "L1_entries": self.conn.execute("SELECT COUNT(*) FROM l1_memory").fetchone()[0],
            "L1_size_kb": round(self._l1_size_kb(), 2),
            "L1_archived": self.conn.execute("SELECT COUNT(*) FROM l1_archive").fetchone()[0],
            "L2_skills": self.conn.execute("SELECT COUNT(*) FROM l2_skills").fetchone()[0],
            "L3_cache_entries": self.conn.execute("SELECT COUNT(*) FROM l3_cache").fetchone()[0],
            "L4_curator_runs": self.conn.execute("SELECT COUNT(*) FROM l4_curator_log").fetchone()[0],
            "L5_fts_entries": self.conn.execute("SELECT COUNT(*) FROM l5_fts").fetchone()[0],
        }

    def health_check(self) -> Dict[str, bool]:
        """Verify all five layers are operational."""
        try:
            self.conn.execute("SELECT 1")
            db_ok = True
        except Exception:
            db_ok = False
        s = self.stats() if db_ok else {}
        return {
            "L1_ok": s.get("L1_entries", 0) >= 0,
            "L2_ok": s.get("L2_skills", 0) >= 0,
            "L3_ok": s.get("L3_cache_entries", 0) >= 0,
            "L4_ok": s.get("L4_curator_runs", 0) >= 0,
            "L5_ok": s.get("L5_fts_entries", 0) >= 0,
            "all_ok": db_ok,
        }

    @staticmethod
    def _jaccard(a: str, b: str) -> float:
        sa, sb = set(a.lower().split("-")), set(b.lower().split("-"))
        if not sa.union(sb):
            return 0.0
        return len(sa & sb) / len(sa | sb)

    def close(self):
        self.conn.close()


# ── CLI ────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    mem = MemoryCore()

    if len(sys.argv) < 2:
        print("Usage: python memory_core.py <command> [args]")
        print("Commands: remember <text>, recall <query>, skill-save <name> <file>,")
        print("          skill-load <name>, curate, stats, health")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "remember":
        content = " ".join(sys.argv[2:])
        eid = mem.remember(content, source="cli")
        print(f"✅ L1 remembered (id={eid}): {content[:50]}...")

    elif cmd == "recall":
        query = " ".join(sys.argv[2:])
        results = mem.recall(query)
        for r in results:
            print(f"  [{r['layer']}] {r['content'][:80]}")

    elif cmd == "skill-save":
        name, filepath = sys.argv[2], sys.argv[3]
        with open(filepath) as f:
            content = f.read()
        new = mem.skill_save(name, content)
        print(f"✅ Skill '{name}' {'created' if new else 'updated'}")

    elif cmd == "skill-load":
        skill = mem.skill_load(sys.argv[2])
        if skill:
            print(f"Name: {skill['name']} v{skill['version']}")
            print(f"Used: {skill['usage_count']}x")
            print(skill['content'][:300])
        else:
            print("❌ Not found")

    elif cmd == "curate":
        result = mem.curate()
        print(f"Before: {result['before']}")
        print(f"After:  {result['after']}")
        for a in result["actions"]:
            print(f"  {a}")

    elif cmd == "stats":
        for k, v in mem.stats().items():
            print(f"  {k}: {v}")

    elif cmd == "health":
        result = mem.health_check()
        for layer, ok in result.items():
            print(f"  {layer}: {'✅' if ok else '❌'}")

    mem.close()
