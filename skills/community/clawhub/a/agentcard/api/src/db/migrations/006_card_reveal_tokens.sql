-- ============================================================
-- 006_card_reveal_tokens.sql — Secure one-time card reveal links
-- P0-2 FIX: Table was referenced in myCards.ts but never created
-- ============================================================

-- One-time reveal tokens for secure PAN/CVV display
CREATE TABLE IF NOT EXISTS card_reveal_tokens (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  token           TEXT NOT NULL UNIQUE,
  card_id         TEXT NOT NULL,
  wallet_address  TEXT NOT NULL,
  expires_at      TIMESTAMPTZ NOT NULL,
  consumed_at     TIMESTAMPTZ,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  status          TEXT NOT NULL DEFAULT 'pending'
    CHECK (status IN ('pending','consumed','expired'))
);

-- ── Indexes ──────────────────────────────────────────────────
CREATE INDEX IF NOT EXISTS idx_reveal_token ON card_reveal_tokens(token) WHERE status = 'pending';
CREATE INDEX IF NOT EXISTS idx_reveal_card ON card_reveal_tokens(card_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_reveal_expires ON card_reveal_tokens(expires_at) WHERE status = 'pending';

-- ── RLS ──────────────────────────────────────────────────────
ALTER TABLE card_reveal_tokens ENABLE ROW LEVEL SECURITY;

-- ── Also fix bot_events: add created_at column alias for metrics queries (P1-4) ──
-- The table uses 'processed_at' but metricsService.ts queries 'created_at'
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name = 'bot_events' AND column_name = 'created_at'
  ) THEN
    ALTER TABLE bot_events ADD COLUMN created_at TIMESTAMPTZ NOT NULL DEFAULT now();
  END IF;
END $$;

CREATE INDEX IF NOT EXISTS idx_bot_events_created ON bot_events(created_at);
