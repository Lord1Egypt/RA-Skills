-- Migration 0019: Add Zillow URL support

ALTER TABLE listings ADD COLUMN zillow_url TEXT;

CREATE INDEX idx_listings_zillow_url ON listings(zillow_url);
