-- Add explicit position column to images_cache to preserve the ordering
-- of images as returned by the listing parser.
ALTER TABLE images_cache ADD COLUMN position INTEGER NOT NULL DEFAULT 0;

-- Backfill: assign 0-based positions ordered by insertion id within each listing.
UPDATE images_cache
SET position = (
    SELECT COUNT(*)
    FROM images_cache ic2
    WHERE ic2.listing_id = images_cache.listing_id AND ic2.id < images_cache.id
);
