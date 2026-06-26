-- Restructure images_cache:
--   • sha256, phash, local_path become nullable (NULL = URL registered but not yet fetched)
--   • unique constraint changes from (listing_id, sha256) → (listing_id, source_url)
--   • image URLs are migrated from listings.images → images_cache
--   • listings.images column is dropped (images_cache is the source of truth)

CREATE TABLE images_cache_new (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    listing_id    INTEGER NOT NULL REFERENCES listings(id),
    source_url    TEXT    NOT NULL,
    sha256        TEXT,
    phash         INTEGER,
    local_path    TEXT,
    UNIQUE(listing_id, source_url)
);

-- Preserve already-downloaded images (keep their hashes and local paths).
INSERT INTO images_cache_new (listing_id, source_url, sha256, phash, local_path)
SELECT listing_id, source_url, sha256, phash, local_path FROM images_cache;

-- Register all image URLs from listings.images that aren't already tracked.
-- json_each() available since SQLite 3.9 (2015).
INSERT OR IGNORE INTO images_cache_new (listing_id, source_url)
SELECT l.id, j.value
FROM   listings l, json_each(l.images) j
WHERE  json_valid(l.images) AND j.value != '';

DROP TABLE images_cache;
ALTER TABLE images_cache_new RENAME TO images_cache;

-- listings no longer owns the image URL list; images_cache is the source of truth.
ALTER TABLE listings DROP COLUMN images;
