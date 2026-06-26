-- SQLite does not allow non-constant expressions in ALTER TABLE ADD COLUMN DEFAULT.
-- Add the column nullable, then back-fill existing rows.
ALTER TABLE images_cache ADD COLUMN created_at TEXT;
UPDATE images_cache SET created_at = datetime('now') WHERE created_at IS NULL;
