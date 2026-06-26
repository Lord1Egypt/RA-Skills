-- Index on listings.status to speed up status-filtered queries.
CREATE INDEX IF NOT EXISTS idx_listings_status ON listings(status);
