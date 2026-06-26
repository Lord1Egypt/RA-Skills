-- ============================================================
-- 003_bot_tables.sql — ASGAgentBot + Owner Cabinet
-- 5 tables for Telegram binding, event processing, audit
-- ============================================================

-- 1. Owner <-> Telegram binding
CREATE TABLE IF NOT EXISTS owner_telegram_links (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  owner_wallet    TEXT NOT NULL,
  telegram_user_id BIGINT NOT NULL,
  chat_id         BIGINT NOT NULL,
  linked_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
  revoked_at      TIMESTAMPTZ,
  status          TEXT NOT NULL DEFAULT 'active'
    CHECK (status IN ('active','revoked')),
  UNIQUE (owner_wallet, telegram_user_id)
);

-- 2. One-time link tokens (stored hashed)
CREATE TABLE IF NOT EXISTS telegram_link_tokens (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  token_hash      TEXT NOT NULL UNIQUE,
  owner_wallet    TEXT NOT NULL,
  scope           TEXT NOT NULL DEFAULT 'telegram_link',
  expires_at      TIMESTAMPTZ NOT NULL,
  consumed_at     TIMESTAMPTZ,
  created_by_ip   TEXT,
  status          TEXT NOT NULL DEFAULT 'pending'
    CHECK (status IN ('pending','consumed','expired','revoked'))
);

-- 3. Bot event processing (idempotency + replay control)
CREATE TABLE IF NOT EXISTS bot_events (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  source          TEXT NOT NULL,
  event_type      TEXT NOT NULL,
  payload_hash    TEXT NOT NULL,
  idempotency_key TEXT NOT NULL UNIQUE,
  processed_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
  delivery_status TEXT NOT NULL DEFAULT 'pending'
    CHECK (delivery_status IN ('pending','delivered','failed','skipped'))
);

-- 4. Bot message delivery log (correlation + tracking)
CREATE TABLE IF NOT EXISTS bot_messages (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  chat_id         BIGINT NOT NULL,
  template_key    TEXT NOT NULL,
  correlation_id  TEXT,
  telegram_msg_id BIGINT,
  sent_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
  status          TEXT NOT NULL DEFAULT 'pending'
    CHECK (status IN ('pending','sent','failed'))
);

-- 5. Authz audit trail
CREATE TABLE IF NOT EXISTS authz_audit_log (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  actor_type  TEXT NOT NULL,
  actor_id    TEXT NOT NULL,
  action      TEXT NOT NULL,
  resource_id TEXT,
  decision    TEXT NOT NULL CHECK (decision IN ('allow','deny')),
  reason      TEXT,
  ip_address  TEXT,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ── Indexes ──────────────────────────────────────────────────
CREATE INDEX IF NOT EXISTS idx_links_wallet ON owner_telegram_links(owner_wallet) WHERE status = 'active';
CREATE INDEX IF NOT EXISTS idx_links_tg ON owner_telegram_links(telegram_user_id) WHERE status = 'active';
CREATE INDEX IF NOT EXISTS idx_tokens_hash ON telegram_link_tokens(token_hash);
CREATE INDEX IF NOT EXISTS idx_tokens_wallet ON telegram_link_tokens(owner_wallet) WHERE status = 'pending';
CREATE INDEX IF NOT EXISTS idx_bot_events_key ON bot_events(idempotency_key);
CREATE INDEX IF NOT EXISTS idx_bot_messages_chat ON bot_messages(chat_id, sent_at DESC);
CREATE INDEX IF NOT EXISTS idx_bot_messages_corr ON bot_messages(correlation_id) WHERE correlation_id IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_audit_actor ON authz_audit_log(actor_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_audit_action ON authz_audit_log(action, created_at DESC);

-- ── RLS (tables owned by service role, no direct user access) ──
ALTER TABLE owner_telegram_links ENABLE ROW LEVEL SECURITY;
ALTER TABLE telegram_link_tokens ENABLE ROW LEVEL SECURITY;
ALTER TABLE bot_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE bot_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE authz_audit_log ENABLE ROW LEVEL SECURITY;
