CREATE TABLE open_houses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    listing_id INTEGER NOT NULL REFERENCES listings(id) ON DELETE CASCADE,
    start_time TEXT NOT NULL,
    end_time TEXT,
    visited INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE(listing_id, start_time)
);

CREATE INDEX idx_open_houses_listing_id ON open_houses(listing_id);
