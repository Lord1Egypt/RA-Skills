"""Cross-system integrations for Communication DNA — CRM + Knowledge Base."""

import os
import re
import sqlite3
from datetime import datetime

from db import get_conn, DB_PATH

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CRM_DB = os.path.join(BASE_DIR, "..", "personal-crm", "crm.db")
KB_DB = os.path.join(BASE_DIR, "..", "knowledge-base", "knowledge.db")

# ── Schema ────────────────────────────────────────────────────

LINKS_SCHEMA = """
CREATE TABLE IF NOT EXISTS speaker_links (
    speaker_id INTEGER REFERENCES speakers(id),
    link_type TEXT,
    external_id INTEGER,
    external_db TEXT,
    confidence REAL DEFAULT 1.0,
    linked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (speaker_id, link_type, external_id)
);
"""


def init_links(conn=None):
    """Ensure speaker_links table exists."""
    c = conn or get_conn()
    c.executescript(LINKS_SCHEMA)
    if not conn:
        c.close()


# ── Fuzzy name matching ──────────────────────────────────────

def _normalize(name):
    return re.sub(r'\s+', ' ', (name or '').lower().strip())


def _name_parts(name):
    return [p for p in _normalize(name).split() if p]


def fuzzy_name_match(name_a, name_b):
    """Return confidence 0-1 for name match."""
    a, b = _normalize(name_a), _normalize(name_b)
    if not a or not b:
        return 0.0
    if a == b:
        return 1.0
    # one contains the other
    if a in b or b in a:
        return 0.8
    # check part overlap
    pa, pb = set(_name_parts(name_a)), set(_name_parts(name_b))
    if not pa or not pb:
        return 0.0
    overlap = pa & pb
    if overlap:
        return 0.6 * len(overlap) / max(len(pa), len(pb))
    return 0.0


# ── CRM Integration ──────────────────────────────────────────

def _crm_conn():
    if not os.path.isfile(CRM_DB):
        return None
    conn = sqlite3.connect(CRM_DB)
    conn.row_factory = sqlite3.Row
    return conn


def auto_link_crm(conn=None):
    """Match speakers to CRM contacts. Returns list of matches."""
    c = conn or get_conn()
    init_links(c)
    crm = _crm_conn()
    if not crm:
        return []

    speakers = c.execute("SELECT id, name, aliases FROM speakers").fetchall()
    contacts = crm.execute("SELECT id, name, email, company FROM contacts WHERE is_noise = 0").fetchall()
    crm.close()

    matches = []
    for s in speakers:
        names = [s["name"]] + (s["aliases"].split(",") if s["aliases"] else [])
        for contact in contacts:
            best = 0.0
            for n in names:
                score = fuzzy_name_match(n, contact["name"])
                best = max(best, score)
            if best >= 0.5:
                c.execute("""
                    INSERT OR REPLACE INTO speaker_links (speaker_id, link_type, external_id, external_db, confidence)
                    VALUES (?, 'crm_contact', ?, ?, ?)
                """, (s["id"], contact["id"], CRM_DB, best))
                matches.append({
                    "speaker_id": s["id"], "speaker_name": s["name"],
                    "contact_id": contact["id"], "contact_name": contact["name"],
                    "contact_email": contact["email"], "confidence": best,
                })
    c.commit()
    if not conn:
        c.close()
    return matches


def get_crm_info(speaker_id, conn=None):
    """Get CRM contact info for a linked speaker."""
    c = conn or get_conn()
    init_links(c)
    links = c.execute("""
        SELECT external_id FROM speaker_links
        WHERE speaker_id = ? AND link_type = 'crm_contact'
    """, (speaker_id,)).fetchall()
    if not conn:
        c.close()
    if not links:
        return []

    crm = _crm_conn()
    if not crm:
        return []
    results = []
    for lnk in links:
        contact = crm.execute("""
            SELECT id, name, email, company, role, health_score, last_seen, interaction_count
            FROM contacts WHERE id = ?
        """, (lnk["external_id"],)).fetchone()
        if contact:
            last_interaction = crm.execute("""
                SELECT type, subject, date FROM interactions
                WHERE contact_id = ? ORDER BY date DESC LIMIT 1
            """, (contact["id"],)).fetchone()
            results.append({
                **dict(contact),
                "last_interaction": dict(last_interaction) if last_interaction else None,
            })
    crm.close()
    return results


# ── Knowledge Base Integration ────────────────────────────────

def _kb_conn():
    if not os.path.isfile(KB_DB):
        return None
    conn = sqlite3.connect(KB_DB)
    conn.row_factory = sqlite3.Row
    return conn


def auto_link_kb(conn=None):
    """Match DNA topics/extractions to KB entities. Returns matches."""
    c = conn or get_conn()
    init_links(c)
    kb = _kb_conn()
    if not kb:
        return []

    kb_entities = kb.execute("SELECT id, name, entity_type, mention_count FROM entities").fetchall()
    kb.close()

    # Get all topics from extractions
    topics = c.execute("""
        SELECT DISTINCT e.content, e.speaker_id
        FROM extractions e WHERE e.type = 'topic'
    """).fetchall()

    matches = []
    for ent in kb_entities:
        ent_norm = _normalize(ent["name"])
        for topic in topics:
            topic_norm = _normalize(topic["content"])
            score = fuzzy_name_match(ent_norm, topic_norm)
            if score >= 0.5 and topic["speaker_id"]:
                c.execute("""
                    INSERT OR REPLACE INTO speaker_links (speaker_id, link_type, external_id, external_db, confidence)
                    VALUES (?, 'kb_entity', ?, ?, ?)
                """, (topic["speaker_id"], ent["id"], KB_DB, score))
                matches.append({
                    "speaker_id": topic["speaker_id"],
                    "topic": topic["content"],
                    "kb_entity": ent["name"],
                    "kb_entity_type": ent["entity_type"],
                    "confidence": score,
                })
    c.commit()
    if not conn:
        c.close()
    return matches


def get_kb_links(speaker_id, conn=None):
    """Get KB entities linked to a speaker."""
    c = conn or get_conn()
    init_links(c)
    links = c.execute("""
        SELECT external_id, confidence FROM speaker_links
        WHERE speaker_id = ? AND link_type = 'kb_entity'
    """, (speaker_id,)).fetchall()
    if not conn:
        c.close()
    if not links:
        return []

    kb = _kb_conn()
    if not kb:
        return []
    results = []
    for lnk in links:
        ent = kb.execute("SELECT * FROM entities WHERE id = ?", (lnk["external_id"],)).fetchone()
        if ent:
            results.append({**dict(ent), "link_confidence": lnk["confidence"]})
    kb.close()
    return results


def push_to_kb(transcription_id, conn=None):
    """Push a transcription into the Knowledge Base as a source."""
    c = conn or get_conn()
    t = c.execute("SELECT * FROM transcriptions WHERE id = ?", (transcription_id,)).fetchone()
    if not t:
        if not conn:
            c.close()
        return {"error": f"Transcription {transcription_id} not found"}

    text = t["raw_text"] or ""
    if not text.strip():
        # Reconstruct from segments
        segs = c.execute("SELECT text FROM segments WHERE transcription_id = ? ORDER BY sequence_order", (transcription_id,)).fetchall()
        text = "\n".join(s["text"] for s in segs)
    if not conn:
        c.close()

    if not text.strip():
        return {"error": "No text content to push"}

    # Use a synthetic URL for transcription sources
    url = f"dna://transcription/{transcription_id}"
    title = t["title"] or f"Transcription #{transcription_id}"
    summary = text[:500]
    word_count = len(text.split())

    kb = _kb_conn()
    if not kb:
        return {"error": "Knowledge Base database not found"}

    try:
        # Check if already pushed
        existing = kb.execute("SELECT id FROM sources WHERE url = ?", (url,)).fetchone()
        if existing:
            kb.close()
            return {"status": "already_exists", "source_id": existing["id"]}

        # We need to insert with source_type. KB schema restricts to article/youtube/twitter/pdf
        # so we'll add 'transcription' check or just use 'article' as closest match
        # Actually the CHECK constraint won't allow it. Let's use the KB's own functions.
        # Import from KB
        import sys
        kb_path = os.path.join(BASE_DIR, "..", "knowledge-base")
        if kb_path not in sys.path:
            sys.path.insert(0, kb_path)

        from ingest import chunk_text, store_source_and_entities
        from entities import extract_entities
        kb.close()

        entities = extract_entities(text)
        source_id = store_source_and_entities(
            url=url, title=title, source_type="article",  # closest match
            content_text=text, summary=summary,
            metadata={"origin": "communication_dna", "transcription_id": transcription_id, "date": t["date"]},
            entities=entities,
        )
        return {"status": "pushed", "source_id": source_id, "word_count": word_count}
    except Exception as e:
        kb.close()
        return {"error": str(e)}


# ── Cross-search ──────────────────────────────────────────────

def cross_search(query, limit=20):
    """Search across Communication DNA segments and Knowledge Base chunks."""
    results = []

    # Search DNA segments
    conn = get_conn()
    try:
        rows = conn.execute("""
            SELECT s.id, s.transcription_id, s.speaker_id, s.text,
                   sp.name as speaker_name, t.title, t.date
            FROM segments_fts fts JOIN segments s ON fts.rowid = s.id
            LEFT JOIN speakers sp ON s.speaker_id = sp.id
            LEFT JOIN transcriptions t ON s.transcription_id = t.id
            WHERE segments_fts MATCH ? ORDER BY rank LIMIT ?
        """, (query, limit)).fetchall()
        for r in rows:
            results.append({
                "source": "communication_dna", "type": "segment",
                "text": r["text"], "speaker": r["speaker_name"],
                "title": r["title"], "date": r["date"],
                "transcription_id": r["transcription_id"],
            })
    except Exception:
        pass
    finally:
        conn.close()

    # Search KB chunks
    kb = _kb_conn()
    if kb:
        try:
            rows = kb.execute("""
                SELECT c.id, c.chunk_text, c.source_id, s.title, s.source_type, s.url
                FROM chunks_fts fts JOIN chunks c ON fts.rowid = c.id
                LEFT JOIN sources s ON c.source_id = s.id
                WHERE chunks_fts MATCH ? ORDER BY rank LIMIT ?
            """, (query, limit)).fetchall()
            for r in rows:
                results.append({
                    "source": "knowledge_base", "type": r["source_type"] or "chunk",
                    "text": r["chunk_text"], "title": r["title"],
                    "url": r["url"], "source_id": r["source_id"],
                })
        except Exception:
            pass
        finally:
            kb.close()

    # Also search KB sources
    if kb:
        kb = _kb_conn()
        if kb:
            try:
                rows = kb.execute("""
                    SELECT s.id, s.title, s.summary, s.source_type, s.url, s.author
                    FROM sources_fts fts JOIN sources s ON fts.rowid = s.id
                    WHERE sources_fts MATCH ? ORDER BY rank LIMIT ?
                """, (query, limit)).fetchall()
                for r in rows:
                    results.append({
                        "source": "knowledge_base", "type": r["source_type"],
                        "text": r["summary"] or "", "title": r["title"],
                        "url": r["url"], "source_id": r["id"],
                    })
            except Exception:
                pass
            finally:
                kb.close()

    return results


# ── Stats ─────────────────────────────────────────────────────

def integration_stats(conn=None):
    """Get integration statistics."""
    c = conn or get_conn()
    init_links(c)
    linked_crm = c.execute("SELECT COUNT(DISTINCT speaker_id) as c FROM speaker_links WHERE link_type = 'crm_contact'").fetchone()["c"]
    linked_kb = c.execute("SELECT COUNT(DISTINCT speaker_id) as c FROM speaker_links WHERE link_type = 'kb_entity'").fetchone()["c"]
    total_links = c.execute("SELECT COUNT(*) as c FROM speaker_links").fetchone()["c"]
    total_speakers = c.execute("SELECT COUNT(*) as c FROM speakers").fetchone()["c"]
    if not conn:
        c.close()
    return {
        "linked_crm": linked_crm,
        "linked_kb": linked_kb,
        "total_links": total_links,
        "total_speakers": total_speakers,
        "crm_available": os.path.isfile(CRM_DB),
        "kb_available": os.path.isfile(KB_DB),
    }
