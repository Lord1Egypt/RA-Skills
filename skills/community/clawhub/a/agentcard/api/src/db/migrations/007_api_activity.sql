-- Migration: Add daily active agents tracking
-- Lightweight table to track unique API callers per day for DAA metric.

CREATE TABLE IF NOT EXISTS api_activity (
    id            SERIAL PRIMARY KEY,
    wallet_address TEXT NOT NULL,
    request_date  DATE NOT NULL DEFAULT CURRENT_DATE,
    request_count INT NOT NULL DEFAULT 1,
    first_seen_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_seen_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (wallet_address, request_date)
);

-- Index for fast DAA lookups
CREATE INDEX IF NOT EXISTS idx_api_activity_date ON api_activity (request_date);

-- Upsert function: call on each API request to track activity
-- Usage: SELECT upsert_api_activity('GWALLET...');
CREATE OR REPLACE FUNCTION upsert_api_activity(p_wallet TEXT)
RETURNS VOID AS $$
BEGIN
  INSERT INTO api_activity (wallet_address, request_date, request_count)
  VALUES (p_wallet, CURRENT_DATE, 1)
  ON CONFLICT (wallet_address, request_date)
  DO UPDATE SET request_count = api_activity.request_count + 1,
                last_seen_at = NOW();
END;
$$ LANGUAGE plpgsql;
