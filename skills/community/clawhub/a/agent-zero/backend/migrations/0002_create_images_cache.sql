CREATE TABLE IF NOT EXISTS images_cache (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    listing_id INTEGER NOT NULL REFERENCES listings(id),
    source_url TEXT    NOT NULL,
    sha256     TEXT    NOT NULL,
    phash      INTEGER NOT NULL,
    local_path TEXT    NOT NULL,
    UNIQUE(listing_id, sha256)
);
