-- Rename search_id → search_criteria_id and enforce NOT NULL.

-- Step 1: Backfill any NULL values (e.g. listings added before the constraint).
UPDATE listings
SET search_id = (SELECT id FROM searches ORDER BY position ASC, id ASC LIMIT 1)
WHERE search_id IS NULL;

-- Step 2: Rename the column (SQLite 3.25+).
ALTER TABLE listings RENAME COLUMN search_id TO search_criteria_id;

-- Step 3: Enforce NOT NULL at the DB level via triggers (SQLite can't add NOT NULL
--         via ALTER TABLE without recreating the whole table).
CREATE TRIGGER listings_search_criteria_id_notnull_insert
BEFORE INSERT ON listings
BEGIN
    SELECT RAISE(ABORT, 'search_criteria_id may not be NULL')
    WHERE NEW.search_criteria_id IS NULL;
END;

CREATE TRIGGER listings_search_criteria_id_notnull_update
BEFORE UPDATE OF search_criteria_id ON listings
BEGIN
    SELECT RAISE(ABORT, 'search_criteria_id may not be NULL')
    WHERE NEW.search_criteria_id IS NULL;
END;
