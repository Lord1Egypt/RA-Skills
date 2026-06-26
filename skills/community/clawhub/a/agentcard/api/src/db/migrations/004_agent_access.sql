-- Migration 004: Agent access control
-- REALIGN-005: Owner can revoke agent access to card details
-- REALIGN-003: Nonce dedup table for anti-replay

-- ── Agent nonce dedup table ────────────────────────────────
CREATE TABLE IF NOT EXISTS agent_nonces (
  nonce       TEXT PRIMARY KEY,
  wallet      TEXT NOT NULL,
  card_id     TEXT NOT NULL,
  created_at  TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_nonces_created ON agent_nonces(created_at);
CREATE INDEX IF NOT EXISTS idx_nonces_wallet ON agent_nonces(wallet);

-- ── Add details_revoked column to cards ────────────────────
ALTER TABLE cards ADD COLUMN IF NOT EXISTS details_revoked BOOLEAN DEFAULT false;

-- ── Enable RLS on new table ────────────────────────────────
ALTER TABLE agent_nonces ENABLE ROW LEVEL SECURITY;
