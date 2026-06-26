-- Places table (canonical verified places)
CREATE TABLE IF NOT EXISTS places (
	id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
	google_place_id TEXT UNIQUE,
	name TEXT NOT NULL,
	address TEXT,
	city TEXT,
	region TEXT,
	country TEXT,
	latitude REAL,
	longitude REAL,
	content_type TEXT NOT NULL DEFAULT 'restaurant' CHECK(content_type IN ('restaurant', 'bar', 'cafe', 'event')),
	google_types TEXT DEFAULT '[]',
	price_level INTEGER CHECK(price_level BETWEEN 1 AND 4),
	embedding BLOB,
	source_url TEXT,
	source_platform TEXT,
	confidence REAL,
	extraction_source TEXT,
	event_date TEXT,
	expires_at TEXT,
	user_notes TEXT,
	status TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active', 'archived', 'visited', 'expired')),
	save_count INTEGER NOT NULL DEFAULT 1,
	created_at TEXT NOT NULL DEFAULT (datetime('now')),
	updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- FTS5 virtual table for full-text search
CREATE VIRTUAL TABLE IF NOT EXISTS places_fts USING fts5(
	name,
	city,
	address,
	user_notes,
	content='places',
	content_rowid='rowid'
);

-- Triggers to keep FTS in sync
CREATE TRIGGER IF NOT EXISTS places_ai AFTER INSERT ON places BEGIN
	INSERT INTO places_fts(rowid, name, city, address, user_notes)
	VALUES (new.rowid, new.name, new.city, new.address, new.user_notes);
END;

CREATE TRIGGER IF NOT EXISTS places_ad AFTER DELETE ON places BEGIN
	INSERT INTO places_fts(places_fts, rowid, name, city, address, user_notes)
	VALUES ('delete', old.rowid, old.name, old.city, old.address, old.user_notes);
END;

CREATE TRIGGER IF NOT EXISTS places_au AFTER UPDATE ON places BEGIN
	INSERT INTO places_fts(places_fts, rowid, name, city, address, user_notes)
	VALUES ('delete', old.rowid, old.name, old.city, old.address, old.user_notes);
	INSERT INTO places_fts(rowid, name, city, address, user_notes)
	VALUES (new.rowid, new.name, new.city, new.address, new.user_notes);
END;

-- Metadata table for schema versioning
CREATE TABLE IF NOT EXISTS metadata (
	key TEXT PRIMARY KEY,
	value TEXT NOT NULL
);

INSERT OR IGNORE INTO metadata (key, value) VALUES ('schema_version', '1');

-- Indexes
CREATE INDEX IF NOT EXISTS idx_places_content_type ON places(content_type);
CREATE INDEX IF NOT EXISTS idx_places_status ON places(status);
CREATE INDEX IF NOT EXISTS idx_places_city ON places(city);
CREATE INDEX IF NOT EXISTS idx_places_google_place_id ON places(google_place_id);
