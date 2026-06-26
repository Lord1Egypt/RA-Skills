-- ASG Card — Database Migration 001: Core Tables
-- Applies to: PostgreSQL / Supabase
-- Created: 2026-02-27
-- Ticket: PLAT-003

-- ── Enable required extensions ─────────────────────────────
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- ── Cards ──────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS cards (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  card_id         TEXT UNIQUE NOT NULL,
  wallet_address  TEXT NOT NULL,
  name_on_card    TEXT NOT NULL,
  email           TEXT NOT NULL,
  balance         NUMERIC(12, 2) NOT NULL DEFAULT 0,
  initial_amount  NUMERIC(12, 2) NOT NULL,
  status          TEXT NOT NULL DEFAULT 'active'
                    CHECK (status IN ('active', 'frozen')),
  details_encrypted BYTEA,  -- AES-256-GCM encrypted card details
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_cards_wallet ON cards (wallet_address);
CREATE INDEX idx_cards_status ON cards (status);

-- ── Payments ───────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS payments (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tx_hash     TEXT UNIQUE NOT NULL,
  payer       TEXT NOT NULL,
  amount      TEXT NOT NULL,       -- atomic USDC (string to avoid floating point)
  tier_amount INTEGER NOT NULL,
  status      TEXT NOT NULL DEFAULT 'proof_received'
                CHECK (status IN (
                  'proof_received', 'verified', 'settled',
                  'settle_failed', 'verify_failed'
                )),
  settle_id   TEXT,
  card_id     TEXT REFERENCES cards(card_id),
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_payments_payer ON payments (payer);
CREATE INDEX idx_payments_status ON payments (status);
CREATE INDEX idx_payments_card ON payments (card_id);

-- ── Webhook Events ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS webhook_events (
  id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  idempotency_key  TEXT UNIQUE NOT NULL,
  event_type       TEXT NOT NULL,
  payload          JSONB NOT NULL,
  processed_at     TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_webhook_events_type ON webhook_events (event_type);

-- ── Updated-at trigger ─────────────────────────────────────
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_updated_at_cards
  BEFORE UPDATE ON cards
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER set_updated_at_payments
  BEFORE UPDATE ON payments
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
