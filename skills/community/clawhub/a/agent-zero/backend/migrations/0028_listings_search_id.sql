-- Add search_id FK to listings and seed the first search.
-- Step 1: Insert the default search.
INSERT INTO searches (title, description) VALUES (
    'East Van House',
    'Single Family House in East Vancouver; ideally with a good rental unit for mortgage helper; minimum 3 beds, ideally 6 beds with the additional beds in a separate isolated rental unit; close to public transit, sky train station within walking distance; ideally with garage, 2 is the best, if not 1 is ok. If not, it would be great to have the potential to build garage in the backyard, therefore, lane access is ideal. Budget targeting for 2m, over 2.5m is absolutely no.'
);

-- Step 2: Add the search_id column (nullable for now).
ALTER TABLE listings ADD COLUMN search_id INTEGER REFERENCES searches(id);

-- Step 3: Backfill all existing listings into the first search.
UPDATE listings SET search_id = (SELECT id FROM searches ORDER BY id LIMIT 1);
