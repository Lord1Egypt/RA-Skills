-- Add a partial unique index on mls_number to prevent duplicate listings
-- for the same property. NULLs are excluded (listings without MLS are allowed).
CREATE UNIQUE INDEX IF NOT EXISTS idx_listings_mls_number
    ON listings(mls_number) WHERE mls_number IS NOT NULL;
