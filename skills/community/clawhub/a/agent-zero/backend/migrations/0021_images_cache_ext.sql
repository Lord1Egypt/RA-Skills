-- Replace local_path with ext in images_cache.
-- local_path was derived (IMAGES_URL_PREFIX + "/" + listing_id + "/" + sha256 + "." + ext)
-- and is fully reconstructable from the other columns; only ext needs storing.
ALTER TABLE images_cache ADD COLUMN ext TEXT;

UPDATE images_cache
SET ext = SUBSTR(local_path, INSTR(local_path, '.') + 1)
WHERE local_path IS NOT NULL;

ALTER TABLE images_cache DROP COLUMN local_path;
