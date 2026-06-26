-- User's intended offer price for mortgage calculations.
-- Defaults to null; the application falls back to the listing `price` when unset.
ALTER TABLE listings ADD COLUMN offer_price INTEGER;
