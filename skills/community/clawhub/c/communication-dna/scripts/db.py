"""Database initialization and connection management for Communication DNA."""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "communication_dna.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS speakers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    aliases TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS transcriptions (
    id INTEGER PRIMARY KEY,
    title TEXT,
    source_file TEXT,
    source_type TEXT,
    duration_seconds INTEGER,
    date TEXT,
    context TEXT,
    raw_text TEXT,
    word_count INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS transcription_speakers (
    transcription_id INTEGER REFERENCES transcriptions(id),
    speaker_id INTEGER REFERENCES speakers(id),
    role TEXT,
    PRIMARY KEY (transcription_id, speaker_id)
);

CREATE TABLE IF NOT EXISTS segments (
    id INTEGER PRIMARY KEY,
    transcription_id INTEGER REFERENCES transcriptions(id),
    speaker_id INTEGER,
    start_time REAL,
    end_time REAL,
    text TEXT NOT NULL,
    word_count INTEGER,
    sequence_order INTEGER
);

CREATE TABLE IF NOT EXISTS extractions (
    id INTEGER PRIMARY KEY,
    segment_id INTEGER REFERENCES segments(id),
    transcription_id INTEGER REFERENCES transcriptions(id),
    speaker_id INTEGER,
    type TEXT,
    content TEXT,
    confidence REAL DEFAULT 1.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

FTS_SCHEMA = """
CREATE VIRTUAL TABLE IF NOT EXISTS segments_fts USING fts5(text, content=segments, content_rowid=id);
"""

FTS_TRIGGERS = """
CREATE TRIGGER IF NOT EXISTS segments_ai AFTER INSERT ON segments BEGIN
    INSERT INTO segments_fts(rowid, text) VALUES (new.id, new.text);
END;
CREATE TRIGGER IF NOT EXISTS segments_ad AFTER DELETE ON segments BEGIN
    INSERT INTO segments_fts(segments_fts, rowid, text) VALUES('delete', old.id, old.text);
END;
CREATE TRIGGER IF NOT EXISTS segments_au AFTER UPDATE ON segments BEGIN
    INSERT INTO segments_fts(segments_fts, rowid, text) VALUES('delete', old.id, old.text);
    INSERT INTO segments_fts(rowid, text) VALUES (new.id, new.text);
END;
"""


def get_conn(db_path=None):
    """Get a database connection, initializing schema if needed."""
    path = db_path or DB_PATH
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA)
    conn.executescript(FTS_SCHEMA)
    conn.executescript(FTS_TRIGGERS)
    return conn
