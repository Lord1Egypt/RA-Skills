CREATE TABLE listing_history (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    listing_id  INTEGER NOT NULL REFERENCES listings(id) ON DELETE CASCADE,
    field_name  TEXT NOT NULL,
    old_value   TEXT,
    new_value   TEXT,
    changed_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_listing_history_listing_id ON listing_history(listing_id);
