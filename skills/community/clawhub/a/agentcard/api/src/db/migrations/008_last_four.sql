-- Migration: Add last_four column to cards table
-- Stores unencrypted last 4 digits for display (non-sensitive).

ALTER TABLE cards ADD COLUMN IF NOT EXISTS last_four TEXT;

-- Index for potential future lookups
CREATE INDEX IF NOT EXISTS idx_cards_last_four ON cards (last_four);
