-- EduClaw IELTS Planner — SQLite Schema
-- Database file: workspace/tracker/educlaw.db
-- Created by: educlaw-ielts-planner v1.1.0

PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

------------------------------------------------------------
-- 1. sessions — study session tracker (single source of truth)
------------------------------------------------------------
CREATE TABLE IF NOT EXISTS sessions (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    date        TEXT    NOT NULL,                          -- YYYY-MM-DD
    phase       INTEGER NOT NULL,                          -- 1-4
    session     INTEGER NOT NULL,                          -- session number within phase
    skill       TEXT    NOT NULL,                          -- Listening / Reading / Writing / Speaking
    topic       TEXT    NOT NULL,                          -- e.g. "Section 1-2 Gap Fill"
    event_id    TEXT    NOT NULL UNIQUE,                   -- calendar event title (used for delete/update)
    status      TEXT    NOT NULL DEFAULT 'Planned',        -- Planned/Completed/Missed/Rescheduled/Deleted/Replaced
    score       REAL,                                      -- score after session (nullable)
    duration_min INTEGER NOT NULL DEFAULT 90,              -- session duration in minutes
    vocab_count INTEGER NOT NULL DEFAULT 10,               -- number of vocab words in this session
    weak_areas  TEXT    NOT NULL DEFAULT '',                -- comma-separated weak areas
    materials_used TEXT NOT NULL DEFAULT '',                -- materials actually used
    notes       TEXT    NOT NULL DEFAULT '',                -- free-form notes
    created_at  TEXT    NOT NULL DEFAULT (datetime('now')), -- row creation timestamp
    updated_at  TEXT    NOT NULL DEFAULT (datetime('now'))  -- last update timestamp
);

CREATE INDEX IF NOT EXISTS idx_sessions_date ON sessions(date);
CREATE INDEX IF NOT EXISTS idx_sessions_status ON sessions(status);
CREATE INDEX IF NOT EXISTS idx_sessions_event_id ON sessions(event_id);

------------------------------------------------------------
-- 2. vocabulary — word bank with spaced repetition tracking
------------------------------------------------------------
CREATE TABLE IF NOT EXISTS vocabulary (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    word         TEXT    NOT NULL,
    ipa          TEXT    NOT NULL DEFAULT '',               -- IPA pronunciation
    pos          TEXT    NOT NULL DEFAULT '',               -- part of speech
    meaning      TEXT    NOT NULL DEFAULT '',               -- meaning in user_lang
    collocations TEXT    NOT NULL DEFAULT '',               -- common collocations
    example      TEXT    NOT NULL DEFAULT '',               -- example sentence
    topic        TEXT    NOT NULL DEFAULT '',               -- IELTS topic category
    session_id   INTEGER,                                   -- FK to sessions.id (which session introduced this word)
    date_added   TEXT    NOT NULL DEFAULT (date('now')),    -- YYYY-MM-DD
    review_count INTEGER NOT NULL DEFAULT 0,                -- times reviewed
    mastered     INTEGER NOT NULL DEFAULT 0,                -- 0=false, 1=true
    created_at   TEXT    NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (session_id) REFERENCES sessions(id)
);

CREATE INDEX IF NOT EXISTS idx_vocabulary_word ON vocabulary(word);
CREATE INDEX IF NOT EXISTS idx_vocabulary_topic ON vocabulary(topic);
CREATE INDEX IF NOT EXISTS idx_vocabulary_mastered ON vocabulary(mastered);

------------------------------------------------------------
-- 3. materials — resource library
------------------------------------------------------------
CREATE TABLE IF NOT EXISTS materials (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    title     TEXT    NOT NULL,
    type      TEXT    NOT NULL DEFAULT 'Book',              -- Book / Website / Video / App
    reference TEXT    NOT NULL DEFAULT '',                   -- page/section/URL
    skill     TEXT    NOT NULL DEFAULT '',                   -- Listening / Reading / Writing / Speaking / General
    phase     INTEGER,                                       -- phase number
    status    TEXT    NOT NULL DEFAULT 'Not Started',        -- Not Started / In Progress / Completed
    rating    INTEGER,                                       -- 1-5 user rating (nullable)
    notes     TEXT    NOT NULL DEFAULT '',
    created_at TEXT   NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_materials_skill ON materials(skill);
CREATE INDEX IF NOT EXISTS idx_materials_status ON materials(status);

------------------------------------------------------------
-- 4. weekly_summaries — weekly progress snapshots
------------------------------------------------------------
CREATE TABLE IF NOT EXISTS weekly_summaries (
    id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    week               INTEGER NOT NULL,                    -- week number (1-16)
    phase              INTEGER NOT NULL,                    -- phase 1-4
    sessions_planned   INTEGER NOT NULL DEFAULT 0,
    sessions_completed INTEGER NOT NULL DEFAULT 0,
    completion_rate    REAL    NOT NULL DEFAULT 0,           -- 0.0-100.0
    vocab_learned      INTEGER NOT NULL DEFAULT 0,
    mock_score         REAL,                                -- nullable
    weak_focus         TEXT    NOT NULL DEFAULT '',
    adjustments        TEXT    NOT NULL DEFAULT '',
    created_at         TEXT    NOT NULL DEFAULT (datetime('now')),
    updated_at         TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_weekly_week_phase ON weekly_summaries(week, phase);

------------------------------------------------------------
-- Useful views for reports & cron jobs
------------------------------------------------------------

-- Current week completion summary
CREATE VIEW IF NOT EXISTS v_current_week AS
SELECT
    COUNT(*)                                                    AS total_sessions,
    SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END)      AS completed,
    SUM(CASE WHEN status = 'Missed' THEN 1 ELSE 0 END)         AS missed,
    SUM(CASE WHEN status = 'Planned' THEN 1 ELSE 0 END)        AS planned,
    ROUND(100.0 * SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) / MAX(COUNT(*), 1), 1) AS completion_pct
FROM sessions
WHERE date >= date('now', 'weekday 1', '-7 days')
  AND date <  date('now', 'weekday 1');

-- Vocabulary stats
CREATE VIEW IF NOT EXISTS v_vocab_stats AS
SELECT
    COUNT(*)                                              AS total_words,
    SUM(CASE WHEN mastered = 1 THEN 1 ELSE 0 END)        AS mastered_count,
    SUM(CASE WHEN mastered = 0 THEN 1 ELSE 0 END)        AS learning_count,
    COUNT(DISTINCT topic)                                  AS topics_covered
FROM vocabulary;

-- Words due for review (reviewed < 3 times, not mastered)
CREATE VIEW IF NOT EXISTS v_words_to_review AS
SELECT word, ipa, meaning, collocations, example, topic, review_count
FROM vocabulary
WHERE mastered = 0 AND review_count < 3
ORDER BY review_count ASC, date_added ASC
LIMIT 20;

-- Session history (last 7 days)
CREATE VIEW IF NOT EXISTS v_recent_sessions AS
SELECT date, phase, session, skill, topic, status, score, duration_min, notes
FROM sessions
WHERE date >= date('now', '-7 days')
ORDER BY date DESC;

-- Materials usage
CREATE VIEW IF NOT EXISTS v_materials_unused AS
SELECT title, type, reference, skill, phase
FROM materials
WHERE status = 'Not Started'
ORDER BY phase ASC, skill ASC;
