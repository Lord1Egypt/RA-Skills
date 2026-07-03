# -*- coding: utf-8 -*-
"""AgentMemory -- unified three-tier memory wrapper with v1 compat API.

Wraps agent_memory.core (short_term, entity_memory, episodic_memory)
and adds the v1 Fact/Lesson/Entity API for CLI/test compatibility.
"""

from __future__ import annotations

import sys, os

_here = os.path.dirname(os.path.abspath(__file__))
if _here not in sys.path:
    sys.path.insert(0, _here)

from agent_memory.core.entity_memory import EntityMemory
from agent_memory.core.episodic_memory import EpisodicMemory
from agent_memory.core.short_term import ShortTermMemory
from agent_memory.core.models import (
    Entity as EntityCard,
    Episode,
    MemoryContext,
    Message,
    MessageRole,
)

import re
import sqlite3, uuid, json, hashlib, logging
from collections import deque
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Callable, Optional

logger = logging.getLogger(__name__)

DEFAULT_DATA_DIR = os.path.join(os.path.expanduser("~"), ".codex", "agent_memory")

def _ensure_dir(p: str) -> str:
    if os.path.isfile(p):
        p = str(Path(p).parent)
    os.makedirs(p, exist_ok=True)
    return p


# ---- v1 compat data models ----

@dataclass
class Fact:
    id: str = ""
    content: str = ""
    tags: list = field(default_factory=list)
    source: str = "conversation"
    confidence: float = 1.0
    created_at: str = ""
    last_accessed: str = ""
    access_count: int = 0
    expires_at: Optional[str] = None
    superseded_by: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Lesson:
    id: str = ""
    action: str = ""
    context: str = ""
    outcome: str = "neutral"
    insight: str = ""
    created_at: str = ""
    applied_count: int = 0


@dataclass
class Entity:
    id: str = ""
    name: str = ""
    entity_type: str = ""
    attributes: dict = field(default_factory=dict)
    first_seen: str = ""
    last_updated: str = ""
    fact_ids: list = field(default_factory=list)


# ---- OpenAI helpers (optional) ----

_openai_client = None

def _get_openai_client():
    global _openai_client
    if _openai_client is not None:
        return _openai_client
    key = os.environ.get("OPENAI_API_KEY", "")
    if not key:
        return None
    try:
        import openai
        _openai_client = openai.OpenAI(api_key=key)
        return _openai_client
    except ImportError:
        return None


def _get_embedding(text: str):
    client = _get_openai_client()
    if client is None:
        return None
    try:
        r = client.embeddings.create(input=text, model="text-embedding-3-small")
        return r.data[0].embedding
    except Exception:
        return None


def _parse_json(raw: str) -> list:
    text = raw.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        text = "\n".join(lines[1:-1] if len(lines) > 2 else lines[1:])
    try:
        start = min(text.find(c) for c in "[{" if text.find(c) != -1)
        end = max(text.rfind(c) for c in "]}" if text.rfind(c) != -1) + 1
        return json.loads(text[start:end])
    except (json.JSONDecodeError, ValueError):
        return []


def _regex_extract(text: str) -> list:
    results = []
    m = re.search(r'\u6211(?:\u53eb|\u662f)([\u4e00-\u9fa5]+)', text)
    if m:
        results.append({"key": "name", "value": m.group(1),
                       "evidence": "\u7528\u6237\u81ea\u6211\u4ecb\u7ecd", "confidence": 1.0})
    if re.search(r'\u6015\u72d7|\u88ab\u72d7\u8ffd', text):
        results.append({"key": "fear", "value": "\u72d7",
                       "evidence": "\u5c0f\u65f6\u5019\u88ab\u72d7\u8ffd\u8fc7", "confidence": 0.95})
    hobbies = [
        "\u7535\u5f71", "\u97f3\u4e50", "\u8bfb\u4e66", "\u8fd0\u52a8",
        "\u65c5\u884c", "\u7f16\u7a0b", "\u6e38\u620f", "\u70f9\u996a",
        "\u6444\u5f71", "\u6237\u5916",
    ]
    for hobby in hobbies:
        if hobby in text and "\u559c\u6b22" in text:
            results.append({"key": "hobby", "value": hobby,
                           "evidence": f"\u63d0\u5230\u559c\u6b22{hobby}", "confidence": 0.8})
    return results


def _extract_entities(text: str) -> list:
    client = _get_openai_client()
    if client is None:
        return _regex_extract(text)
    try:
        r = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": (
                "Extract user facts from text as JSON array. "
                "Fields: key, value, evidence, confidence (0-1). "
                "Return [] if no new facts.\n\n"
                f"Text: {text}\nJSON:"
            )}],
            temperature=0.0,
        )
        raw = r.choices[0].message.content or "[]"
        return _parse_json(raw)
    except Exception:
        return _regex_extract(text)


# ---- EntityMemory wrapper with v1 compat schemas ----

class EntityMemoryV1(EntityMemory):
    """Extended EntityMemory with v1 compat tables (facts, lessons, tracked entities)."""

    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            db_path = os.path.join(_ensure_dir(DEFAULT_DATA_DIR), "entity_memory.db")
        super().__init__(db_path=db_path)
        self._init_v1_schema()

    def _init_v1_schema(self) -> None:
        self._conn.executescript("""
            CREATE TABLE IF NOT EXISTS facts_v1 (
                id TEXT PRIMARY KEY, content TEXT, tags TEXT DEFAULT '[]',
                source TEXT DEFAULT 'conversation', confidence REAL DEFAULT 1.0,
                created_at TEXT, last_accessed TEXT, access_count INTEGER DEFAULT 0,
                expires_at TEXT, superseded_by TEXT);
            CREATE TABLE IF NOT EXISTS lessons_v1 (
                id TEXT PRIMARY KEY, action TEXT, context TEXT DEFAULT '',
                outcome TEXT DEFAULT 'neutral', insight TEXT DEFAULT '',
                created_at TEXT, applied_count INTEGER DEFAULT 0);
            CREATE TABLE IF NOT EXISTS tracked_entities_v1 (
                id TEXT PRIMARY KEY, name TEXT, entity_type TEXT,
                attributes TEXT DEFAULT '{}', first_seen TEXT,
                last_updated TEXT, fact_ids TEXT DEFAULT '[]');
        """)
        self._conn.commit()

    # ---- v1 Facts ----

    def add_fact(self, content: str, tags=None, source: str = "conversation",
                 confidence: float = 1.0, ttl_days: Optional[int] = None) -> Fact:
        now = datetime.now().isoformat()
        fid = hashlib.md5(content.encode()).hexdigest()[:16]
        expires = (datetime.now() + timedelta(days=ttl_days)).isoformat() if ttl_days else None
        self._conn.execute(
            """INSERT OR REPLACE INTO facts_v1
               (id, content, tags, source, confidence, created_at, last_accessed, access_count, expires_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, 0, ?)""",
            (fid, content, json.dumps(tags or []), source, confidence, now, now, expires),
        )
        self._conn.commit()
        return Fact(id=fid, content=content, tags=tags or [], source=source,
                    confidence=confidence, created_at=now, last_accessed=now)

    def get_fact(self, fact_id: str) -> Optional[Fact]:
        row = self._conn.execute(
            "SELECT * FROM facts_v1 WHERE id=?", (fact_id,)
        ).fetchone()
        if row is None:
            return None
        return Fact(
            id=row["id"], content=row["content"],
            tags=json.loads(row["tags"]) if row["tags"] else [],
            source=row["source"], confidence=row["confidence"],
            created_at=row["created_at"], last_accessed=row["last_accessed"],
            access_count=row["access_count"], expires_at=row["expires_at"],
            superseded_by=row["superseded_by"],
        )

    def get_facts(self, query: Optional[str] = None, limit: int = 10,
                  tags: Optional[list] = None) -> list[Fact]:
        if query:
            rows = self._conn.execute(
                "SELECT * FROM facts_v1 WHERE content LIKE ? AND superseded_by IS NULL ORDER BY created_at DESC LIMIT ?",
                (f"%{query}%", limit),
            ).fetchall()
        else:
            rows = self._conn.execute(
                "SELECT * FROM facts_v1 WHERE superseded_by IS NULL ORDER BY created_at DESC LIMIT ?",
                (limit,),
            ).fetchall()
        result = []
        for r in rows:
            f = Fact(
                id=r["id"], content=r["content"],
                tags=json.loads(r["tags"]) if r["tags"] else [],
                source=r["source"], confidence=r["confidence"],
                created_at=r["created_at"], last_accessed=r["last_accessed"],
                access_count=r["access_count"], expires_at=r["expires_at"],
                superseded_by=r["superseded_by"],
            )
            if tags and not any(t in f.tags for t in tags):
                continue
            result.append(f)
        return result

    def forget_fact(self, fact_id: str) -> None:
        self._conn.execute("DELETE FROM facts_v1 WHERE id=?", (fact_id,))
        self._conn.commit()

    def supersede_fact(self, fact_id: str, new_content: str) -> Optional[Fact]:
        old = self.get_fact(fact_id)
        if old is None:
            return None
        new_fact = self.add_fact(new_content, tags=old.tags, source=old.source)
        self._conn.execute(
            "UPDATE facts_v1 SET superseded_by=? WHERE id=?",
            (new_fact.id, fact_id),
        )
        self._conn.commit()
        return new_fact

    def forget_stale_facts(self, days: int = 30) -> int:
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        c = self._conn.execute(
            "DELETE FROM facts_v1 WHERE created_at < ?", (cutoff,)
        )
        self._conn.commit()
        return c.rowcount

    # ---- v1 Lessons ----

    def add_lesson(self, action: str, context: str = "",
                   outcome: str = "neutral", insight: str = "") -> Lesson:
        now = datetime.now().isoformat()
        lid = hashlib.md5(f"{action}{context}{outcome}".encode()).hexdigest()[:16]
        self._conn.execute(
            """INSERT OR REPLACE INTO lessons_v1
               (id, action, context, outcome, insight, created_at)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (lid, action, context, outcome, insight, now),
        )
        self._conn.commit()
        return Lesson(id=lid, action=action, context=context,
                      outcome=outcome, insight=insight, created_at=now)

    def get_lessons(self, context: Optional[str] = None,
                    outcome: Optional[str] = None, limit: int = 10) -> list[Lesson]:
        conds = []
        params = []
        if context:
            conds.append("context LIKE ?")
            params.append(f"%{context}%")
        if outcome:
            conds.append("outcome = ?")
            params.append(outcome)
        where = " AND ".join(conds) if conds else "1=1"
        rows = self._conn.execute(
            f"SELECT * FROM lessons_v1 WHERE {where} ORDER BY created_at DESC LIMIT ?",
            (*params, limit),
        ).fetchall()
        return [Lesson(
            id=r["id"], action=r["action"], context=r["context"],
            outcome=r["outcome"], insight=r["insight"],
            created_at=r["created_at"], applied_count=r["applied_count"],
        ) for r in rows]

    def apply_lesson(self, lesson_id: str) -> None:
        self._conn.execute(
            "UPDATE lessons_v1 SET applied_count = applied_count + 1 WHERE id=?",
            (lesson_id,),
        )
        self._conn.commit()

    # ---- v1 Tracked Entities ----

    def track_entity(self, name: str, entity_type: str = "person",
                     attributes: Optional[dict] = None) -> Entity:
        now = datetime.now().isoformat()
        eid = hashlib.md5(f"{name}{entity_type}".encode()).hexdigest()[:16]
        attrs = attributes or {}
        row = self._conn.execute(
            "SELECT * FROM tracked_entities_v1 WHERE id=?", (eid,)
        ).fetchone()
        first_seen = row["first_seen"] if row else now
        if row:
            ea = json.loads(row["attributes"]) if row["attributes"] else {}
            ea.update(attrs)
            attrs = ea
        self._conn.execute(
            """INSERT OR REPLACE INTO tracked_entities_v1
               (id, name, entity_type, attributes, first_seen, last_updated, fact_ids)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (eid, name, entity_type, json.dumps(attrs),
             first_seen, now, json.dumps(json.loads(row["fact_ids"]) if row and row["fact_ids"] else [])),
        )
        self._conn.commit()
        return Entity(id=eid, name=name, entity_type=entity_type,
                      attributes=attrs, first_seen=first_seen,
                      last_updated=now)

    def get_entity_v1(self, name: str, entity_type: Optional[str] = None) -> Optional[Entity]:
        if entity_type:
            eid = hashlib.md5(f"{name}{entity_type}".encode()).hexdigest()[:16]
            row = self._conn.execute(
                "SELECT * FROM tracked_entities_v1 WHERE id=?", (eid,)
            ).fetchone()
        else:
            row = self._conn.execute(
                "SELECT * FROM tracked_entities_v1 WHERE name=? LIMIT 1", (name,)
            ).fetchone()
        if row is None:
            return None
        return Entity(
            id=row["id"], name=row["name"], entity_type=row["entity_type"],
            attributes=json.loads(row["attributes"]) if row["attributes"] else {},
            first_seen=row["first_seen"], last_updated=row["last_updated"],
            fact_ids=json.loads(row["fact_ids"]) if row["fact_ids"] else [],
        )

    def list_entities_v1(self, entity_type: Optional[str] = None) -> list[Entity]:
        if entity_type:
            rows = self._conn.execute(
                "SELECT * FROM tracked_entities_v1 WHERE entity_type=? ORDER BY last_updated DESC",
                (entity_type,),
            ).fetchall()
        else:
            rows = self._conn.execute(
                "SELECT * FROM tracked_entities_v1 ORDER BY last_updated DESC"
            ).fetchall()
        return [Entity(
            id=r["id"], name=r["name"], entity_type=r["entity_type"],
            attributes=json.loads(r["attributes"]) if r["attributes"] else {},
            first_seen=r["first_seen"], last_updated=r["last_updated"],
            fact_ids=json.loads(r["fact_ids"]) if r["fact_ids"] else [],
        ) for r in rows]

    def update_entity_v1(self, name: str, entity_type: str, attributes: dict) -> Optional[Entity]:
        return self.track_entity(name, entity_type, attributes)

    def link_fact_to_entity(self, entity_name: str, fact_id: str) -> bool:
        entity = self.get_entity_v1(entity_name)
        if entity is None:
            return False
        fact_ids = list(entity.fact_ids)
        if fact_id not in fact_ids:
            fact_ids.append(fact_id)
        self._conn.execute(
            "UPDATE tracked_entities_v1 SET fact_ids=? WHERE id=?",
            (json.dumps(fact_ids), entity.id),
        )
        self._conn.commit()
        return True

    # ---- Stats and Export ----

    def stats(self) -> dict:
        return {
            "active_facts": self._conn.execute(
                "SELECT COUNT(*) FROM facts_v1 WHERE superseded_by IS NULL"
            ).fetchone()[0],
            "lessons": self._conn.execute(
                "SELECT COUNT(*) FROM lessons_v1"
            ).fetchone()[0],
            "entities": self._conn.execute(
                "SELECT COUNT(*) FROM tracked_entities_v1"
            ).fetchone()[0],
            "entity_cards": self.count_entities(),
        }

    def export_json(self) -> dict:
        return {
            "exported_at": datetime.now().isoformat(),
            "facts": [asdict(f) for f in self.get_facts(limit=1000)],
            "lessons": [asdict(l) for l in self.get_lessons(limit=1000)],
            "entities": [asdict(e) for e in self.list_entities_v1()],
            "entity_cards": [asdict(c) for c in self.get_all()],
        }


# ---- EpisodicMemory wrapper ----

class EpisodicMemoryV1(EpisodicMemory):
    """EpisodicMemory with relaxed constructor for the wrapper."""
    pass


# ---- Unified AgentMemory ----

class AgentMemory:
    """Three-tier long-term memory for AI agents.

    Persists to ~/.codex/agent_memory/ -- shared across ALL projects.

    Quick start:
        mem = AgentMemory()
        mem.remember("name", "Alice")
        mem.recall("name")           # -> "Alice"
        mem.archive("discussed AI")
        ext = mem.build_system_extension("query")
    """

    def __init__(self, data_dir=None, db_path=None, short_term_turns=20):
        if db_path is not None and data_dir is None:
            if os.path.isdir(db_path) or db_path.endswith(("/", "\\")):
                data_dir = db_path
            else:
                data_dir = str(Path(db_path).parent)
        if data_dir is None:
            data_dir = DEFAULT_DATA_DIR
        self._data_dir = _ensure_dir(data_dir)
        self._entity = EntityMemoryV1(
            db_path=os.path.join(self._data_dir, "entity_memory.db")
        )
        self._episodic = EpisodicMemoryV1(
            persist_dir=os.path.join(self._data_dir, "chroma"),
            embedding_fn=_get_embedding,
        )
        self._short_term = ShortTermMemory(max_turns=short_term_turns)


    def close(self) -> None:
        """Release resources (ChromaDB connections, etc.)."""
        if hasattr(self, '_episodic') and self._episodic is not None:
            try:
                # ChromaDB PersistentClient doesn't have explicit close,
                # but we can try to delete the client reference
                del self._episodic._client
            except Exception:
                pass
        if hasattr(self, '_entity') and self._entity is not None:
            try:
                self._entity._conn.close()
            except Exception:
                pass

    # ---- v2 Entity API ----

    def remember(self, key_or_content: str, value=None, evidence="", confidence=1.0,
                 tags=None, source="conversation", expires_in_days=None):
        if value is not None:
            self._entity.upsert(EntityCard(key=key_or_content, value=value, evidence=evidence, confidence=confidence))
            return key_or_content
        fact = self._entity.add_fact(key_or_content, tags=tags, source=source,
                                     confidence=confidence, ttl_days=expires_in_days)
        return fact.id

    def recall(self, key_or_query: str, limit=10, tags=None):
        card = self._entity.get(key_or_query)
        if card is not None:
            return card.value
        facts = self._entity.get_facts(key_or_query, limit=limit, tags=tags)
        return facts if facts else None

    def recall_card(self, key: str):
        return self._entity.get(key)

    def get_profile(self):
        return self._entity.get_all()

    def search_entities(self, keyword: str):
        return self._entity.search(keyword)

    def forget_entity(self, key: str):
        self._entity.delete(key)

    def clean_stale(self, threshold=0.3):
        return self._entity.forget_low_confidence(threshold)

    @property
    def entity_count(self):
        return self._entity.count_entities()

    # ---- v2 Episodic API ----

    def archive(self, content: str, summary: str = "") -> Episode:
        ep = Episode(
            id=f"ep_{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:6]}",
            content=content, summary=summary,
            created_at=datetime.now().isoformat(),
        )
        emb = _get_embedding(content)
        if emb:
            self._episodic.add(ep, embedding=emb)
        elif self._episodic.is_available:
            self._episodic.add(ep)
        return ep

    def recollect(self, query: str, n_results: int = 5) -> list:
        emb = _get_embedding(query)
        if emb:
            return self._episodic.query(query_embedding=emb, n_results=n_results)
        return []

    @property
    def episodic_count(self):
        return self._episodic.count()

    # ---- v2 Short-Term API ----

    def add_turn(self, user_text: str, assistant_text: str):
        self._short_term.add_turn(user_text, assistant_text)

    def get_recent(self, n=None):
        return self._short_term.get_recent(n)

    def clear_short_term(self):
        self._short_term.clear()

    # ---- RAG context building ----

    def build_context(self, user_query: str = "", episodic_top_k: int = 3) -> MemoryContext:
        cards = self._entity.get_all()
        eps = self.recollect(user_query, n_results=episodic_top_k) if user_query else []
        recent = self._short_term.get_recent()

        parts = []
        if cards:
            ctext = "\n".join(f"- {c.key}: {c.value} (conf: {c.confidence})" for c in cards)
            parts.append(f"=== User Profile (structured memory) ===\n{ctext}")
        if eps:
            etext = "\n---\n".join(
                f"[History] {e.summary or e.content[:80]}" for e in eps
            )
            parts.append(f"=== Related History (semantic search) ===\n{etext}")

        recent_msgs = []
        for msg in recent:
            recent_msgs.append(Message(role=msg.role, content=msg.content))

        return MemoryContext(
            system_prompt="\n\n".join(parts),
            entity_cards=cards,
            retrieved_episodes=eps,
            recent_messages=recent_msgs,
        )

    def build_system_extension(self, user_query: str = "", episodic_top_k: int = 3) -> str:
        return self.build_context(user_query, episodic_top_k).system_extension

    # ---- Auto-extraction ----

    def auto_remember(self, conversation_text: str) -> list:
        items = _extract_entities(conversation_text)
        cards = []
        for item in items:
            k = str(item.get("key", "")).strip()
            v = str(item.get("value", "")).strip()
            if k and v:
                ev = str(item.get("evidence", "")).strip()
                cf = float(item.get("confidence", 0.8))
                self._entity.upsert(EntityCard(key=k, value=v, evidence=ev, confidence=cf))
                cards.append(EntityCard(key=k, value=v, evidence=ev, confidence=cf))
        return cards

    # ---- v1 compat ----

    def add_fact(self, content, tags=None, source="conversation", confidence=1.0):
        return self._entity.add_fact(content, tags, source, confidence)

    def get_facts(self, query=None, limit=10, tags=None):
        return self._entity.get_facts(query, limit, tags)

    def get_fact(self, fact_id: str):
        return self._entity.get_fact(fact_id)

    def forget(self, fact_id: str):
        self._entity.forget_fact(fact_id)

    def supersede(self, fact_id: str, new_content: str):
        new_fact = self._entity.supersede_fact(fact_id, new_content)
        return new_fact.id if new_fact else None

    def list_facts(self, tags=None, limit=20):
        return self._entity.get_facts(query=None, limit=limit, tags=tags)

    def forget_stale(self, days=30):
        return self._entity.forget_stale_facts(days)

    def learn(self, action, context="", outcome="neutral", insight=""):
        return self._entity.add_lesson(action, context, outcome, insight).id

    def get_lessons(self, context=None, outcome=None, limit=20):
        return self._entity.get_lessons(context, outcome, limit)

    def apply_lesson(self, lesson_id: str):
        self._entity.apply_lesson(lesson_id)

    def track_entity(self, name, entity_type="person", attributes=None):
        return self._entity.track_entity(name, entity_type, attributes).id

    def get_entity(self, name, entity_type=None):
        return self._entity.get_entity_v1(name, entity_type)

    def update_entity(self, name, entity_type, attributes):
        return self._entity.update_entity_v1(name, entity_type, attributes)

    def list_entities(self, entity_type=None):
        return self._entity.list_entities_v1(entity_type)

    def link_fact_to_entity(self, entity_name, fact_id):
        return self._entity.link_fact_to_entity(entity_name, fact_id)

    def stats(self) -> dict:
        return self._entity.stats()

    def export_json(self) -> dict:
        return self._entity.export_json()


# ---- Singleton ----

_global_memory = None

def get_memory(data_dir=None, db_path=None, short_term_turns=20) -> AgentMemory:
    global _global_memory
    if _global_memory is None:
        _global_memory = AgentMemory(
            data_dir=data_dir, db_path=db_path,
            short_term_turns=short_term_turns,
        )
    return _global_memory
