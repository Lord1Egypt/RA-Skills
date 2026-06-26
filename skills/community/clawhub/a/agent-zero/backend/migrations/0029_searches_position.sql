-- Add position column to searches for user-defined ordering.
ALTER TABLE searches ADD COLUMN position INTEGER NOT NULL DEFAULT 0;

-- Backfill: assign positions based on existing id order (oldest = 0).
UPDATE searches SET position = (
    SELECT cnt FROM (
        SELECT id, ROW_NUMBER() OVER (ORDER BY id) - 1 AS cnt FROM searches
    ) AS ranked WHERE ranked.id = searches.id
);
