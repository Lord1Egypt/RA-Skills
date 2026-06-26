-- Add rew_url column for rew.ca listings.
-- Simple ALTER TABLE since there are no NOT NULL constraints to change.

ALTER TABLE listings ADD COLUMN rew_url TEXT;

CREATE UNIQUE INDEX idx_listings_rew_url
    ON listings(rew_url) WHERE rew_url IS NOT NULL;
