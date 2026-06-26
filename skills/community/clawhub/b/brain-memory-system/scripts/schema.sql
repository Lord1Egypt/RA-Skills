-- Brain: Unified Cognitive Memory System
-- Inspired by human brain architecture
-- Schema v1.0 — March 15, 2026

PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

-- ============================================================
-- EPISODIC MEMORY (Hippocampus → Neocortex)
-- Time-stamped events, experiences, decisions
-- ============================================================
CREATE TABLE IF NOT EXISTS episodes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,              -- YYYY-MM-DD
    time TEXT,                       -- HH:MM (24h)
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    -- Emotional tagging (Amygdala)
    emotion TEXT,                    -- feeling word (e.g., frustrated, proud, electric)
    emotion_intensity TEXT,          -- low, medium, high
    -- Consolidation metadata
    importance INTEGER DEFAULT 5,   -- 1-10 scale
    novelty INTEGER DEFAULT 5,      -- 1-10 how new/surprising
    rehearsal_count INTEGER DEFAULT 0, -- times recalled
    consolidated BOOLEAN DEFAULT 0, -- has been processed into long-term
    consolidated_at TEXT,            -- when consolidation happened
    -- Source tracking
    source TEXT DEFAULT 'manual',   -- manual, migration, consolidation, agent
    agent TEXT DEFAULT 'margot',    -- which agent created this
    -- Timestamps
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_episodes_date ON episodes(date);
CREATE INDEX IF NOT EXISTS idx_episodes_emotion ON episodes(emotion);
CREATE INDEX IF NOT EXISTS idx_episodes_importance ON episodes(importance);
CREATE INDEX IF NOT EXISTS idx_episodes_consolidated ON episodes(consolidated);
CREATE INDEX IF NOT EXISTS idx_episodes_agent ON episodes(agent);

-- Full-text search on episodes
CREATE VIRTUAL TABLE IF NOT EXISTS episodes_fts USING fts5(
    title, content, emotion,
    content='episodes',
    content_rowid='id'
);

-- Triggers to keep FTS in sync
CREATE TRIGGER IF NOT EXISTS episodes_ai AFTER INSERT ON episodes BEGIN
    INSERT INTO episodes_fts(rowid, title, content, emotion)
    VALUES (new.id, new.title, new.content, new.emotion);
END;

CREATE TRIGGER IF NOT EXISTS episodes_ad AFTER DELETE ON episodes BEGIN
    INSERT INTO episodes_fts(episodes_fts, rowid, title, content, emotion)
    VALUES ('delete', old.id, old.title, old.content, old.emotion);
END;

CREATE TRIGGER IF NOT EXISTS episodes_au AFTER UPDATE ON episodes BEGIN
    INSERT INTO episodes_fts(episodes_fts, rowid, title, content, emotion)
    VALUES ('delete', old.id, old.title, old.content, old.emotion);
    INSERT INTO episodes_fts(rowid, title, content, emotion)
    VALUES (new.id, new.title, new.content, new.emotion);
END;

-- ============================================================
-- SEMANTIC MEMORY (Neocortex — long-term facts)
-- Consolidated knowledge, preferences, relationships
-- Extends existing facts.db concept
-- ============================================================
CREATE TABLE IF NOT EXISTS facts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entity TEXT NOT NULL,            -- who/what this is about
    key TEXT NOT NULL,               -- attribute name
    value TEXT NOT NULL,             -- the fact
    confidence REAL DEFAULT 1.0,    -- 0.0-1.0
    source_episode_id INTEGER,      -- which episode taught us this
    -- Consolidation
    times_confirmed INTEGER DEFAULT 1,
    last_confirmed TEXT,
    superseded_by INTEGER,          -- if this fact was updated
    -- Timestamps
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    UNIQUE(entity, key),
    FOREIGN KEY (source_episode_id) REFERENCES episodes(id),
    FOREIGN KEY (superseded_by) REFERENCES facts(id)
);

CREATE INDEX IF NOT EXISTS idx_facts_entity ON facts(entity);
CREATE INDEX IF NOT EXISTS idx_facts_key ON facts(key);

CREATE VIRTUAL TABLE IF NOT EXISTS facts_fts USING fts5(
    entity, key, value,
    content='facts',
    content_rowid='id'
);

CREATE TRIGGER IF NOT EXISTS facts_ai AFTER INSERT ON facts BEGIN
    INSERT INTO facts_fts(rowid, entity, key, value)
    VALUES (new.id, new.entity, new.key, new.value);
END;

CREATE TRIGGER IF NOT EXISTS facts_ad AFTER DELETE ON facts BEGIN
    INSERT INTO facts_fts(facts_fts, rowid, entity, key, value)
    VALUES ('delete', old.id, old.entity, old.key, old.value);
END;

CREATE TRIGGER IF NOT EXISTS facts_au AFTER UPDATE ON facts BEGIN
    INSERT INTO facts_fts(facts_fts, rowid, entity, key, value)
    VALUES ('delete', old.id, old.entity, old.key, old.value);
    INSERT INTO facts_fts(rowid, entity, key, value)
    VALUES (new.id, new.entity, new.key, new.value);
END;

-- ============================================================
-- PROCEDURAL MEMORY (Cerebellum)
-- Versioned workflows with error-driven evolution
-- ============================================================
CREATE TABLE IF NOT EXISTS procedures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    description TEXT,
    version INTEGER DEFAULT 1,
    tags TEXT,                       -- comma-separated
    -- Stats
    success_count INTEGER DEFAULT 0,
    failure_count INTEGER DEFAULT 0,
    last_run TEXT,
    last_outcome TEXT,               -- success, failure
    -- Content
    steps TEXT NOT NULL,             -- JSON array of step objects
    -- Timestamps
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS procedure_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    procedure_id INTEGER NOT NULL,
    version INTEGER NOT NULL,
    event_type TEXT NOT NULL,        -- success, failure, evolved
    failed_step INTEGER,
    description TEXT,
    fix_applied TEXT,
    occurred_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (procedure_id) REFERENCES procedures(id)
);

CREATE INDEX IF NOT EXISTS idx_procedures_slug ON procedures(slug);
CREATE INDEX IF NOT EXISTS idx_proc_history_proc ON procedure_history(procedure_id);

-- ============================================================
-- WORKING MEMORY (Prefrontal Cortex)
-- Current context, active goals, task state
-- Capacity-limited (enforced by application)
-- ============================================================
CREATE TABLE IF NOT EXISTS working_memory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent TEXT NOT NULL DEFAULT 'margot',
    slot_type TEXT NOT NULL,         -- goal, context, task, note
    content TEXT NOT NULL,
    priority INTEGER DEFAULT 5,     -- 1-10
    expires_at TEXT,                 -- auto-decay
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_wm_agent ON working_memory(agent);

-- ============================================================
-- CONSOLIDATION LOG (Hippocampal replay tracking)
-- ============================================================
CREATE TABLE IF NOT EXISTS consolidation_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_type TEXT NOT NULL,       -- episode, fact, procedure
    source_id INTEGER NOT NULL,
    action TEXT NOT NULL,            -- consolidated, merged, archived, forgotten
    destination TEXT,                -- where it went (facts, long_term, etc.)
    reason TEXT,
    occurred_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_consolidation_source ON consolidation_log(source_type, source_id);
CREATE INDEX IF NOT EXISTS idx_consolidation_occurred ON consolidation_log(occurred_at);

-- ============================================================
-- SYSTEM METADATA
-- ============================================================
CREATE TABLE IF NOT EXISTS brain_meta (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at TEXT DEFAULT (datetime('now'))
);

INSERT OR IGNORE INTO brain_meta(key, value) VALUES
    ('schema_version', '1.0'),
    ('created_at', datetime('now')),
    ('agent', 'margot');
