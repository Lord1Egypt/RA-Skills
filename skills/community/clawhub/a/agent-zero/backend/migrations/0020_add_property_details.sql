-- Parser-extracted property metadata fields.
ALTER TABLE listings ADD COLUMN property_type   TEXT;     -- e.g. "Townhouse", "Single Family Residential"
ALTER TABLE listings ADD COLUMN listed_date     TEXT;     -- ISO date when the listing was posted (YYYY-MM-DD)
ALTER TABLE listings ADD COLUMN mls_number      TEXT;     -- MLS® listing number (e.g. "R3086230")
ALTER TABLE listings ADD COLUMN laundry_in_unit INTEGER;  -- boolean: in-suite washer/dryer
