-- Rename searches/search_criteria_id to search_profiles/search_profile_id.

ALTER TABLE searches RENAME TO search_profiles;
ALTER TABLE listings RENAME COLUMN search_criteria_id TO search_profile_id;

DROP TRIGGER IF EXISTS listings_search_criteria_id_notnull_insert;
DROP TRIGGER IF EXISTS listings_search_criteria_id_notnull_update;

CREATE TRIGGER listings_search_profile_id_notnull_insert
BEFORE INSERT ON listings
BEGIN
    SELECT RAISE(ABORT, 'search_profile_id may not be NULL')
    WHERE NEW.search_profile_id IS NULL;
END;

CREATE TRIGGER listings_search_profile_id_notnull_update
BEFORE UPDATE OF search_profile_id ON listings
BEGIN
    SELECT RAISE(ABORT, 'search_profile_id may not be NULL')
    WHERE NEW.search_profile_id IS NULL;
END;
