-- Friday Budgeting Pro — SQLite schema
-- Design principles:
--   • Store raw values exactly as received (never overwrite Plaid data)
--   • amount = original currency, amount_home = converted to home currency
--   • All timestamps are UTC Unix seconds; display layer handles timezone
--   • entry_type drives whether a transaction counts in spending/income/savings totals
--   • classification_rules replaces routing_rules (natural language, priority-ordered)

-- ---------------------------------------------------------------------------
-- Auth
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS users (
  id TEXT PRIMARY KEY,
  username TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,     -- argon2id hash
  created_at INTEGER NOT NULL,
  home_currency TEXT DEFAULT 'CAD',            -- ISO 4217; used for all totals and display
  timezone TEXT DEFAULT 'America/Toronto'      -- IANA timezone; used for date-boundary queries
);

CREATE TABLE IF NOT EXISTS sessions (
  id TEXT PRIMARY KEY,             -- session token (random 32 bytes hex)
  user_id TEXT REFERENCES users(id),
  created_at INTEGER NOT NULL,
  last_seen_at INTEGER NOT NULL,
  expires_at INTEGER NOT NULL,     -- unused; kept for backward compat
  user_agent TEXT
);

-- ---------------------------------------------------------------------------
-- Bank connections
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS bank_connections (
  id TEXT PRIMARY KEY,
  plaid_item_id TEXT UNIQUE,
  plaid_access_token_encrypted TEXT NOT NULL,  -- Fernet-encrypted
  institution_name TEXT,
  status TEXT DEFAULT 'active',                -- active | needs_reauth
  last_synced_at INTEGER,                      -- UTC Unix seconds
  user_id TEXT REFERENCES users(id),
  plaid_env TEXT NOT NULL DEFAULT 'sandbox'    -- sandbox | development | production
);

CREATE TABLE IF NOT EXISTS bank_accounts (
  id TEXT PRIMARY KEY,
  connection_id TEXT REFERENCES bank_connections(id),
  plaid_account_id TEXT UNIQUE,
  name TEXT,                                   -- Plaid account name (e.g. "RBC Day to Day")
  mask TEXT,                                   -- last 4 digits
  type TEXT,                                   -- depository | credit | investment
  subtype TEXT,                                -- checking | savings | credit card etc.
  currency TEXT DEFAULT 'CAD',                 -- native currency of this account (ISO 4217)
  balance_current REAL,                        -- current balance from last sync
  balance_available REAL,                      -- available balance from last sync
  description TEXT,                            -- user-set context for classifier
  default_ledger_id TEXT REFERENCES ledgers(id) -- transactions from this account route here by default
);

-- ---------------------------------------------------------------------------
-- Ledger structure
-- ---------------------------------------------------------------------------

-- A ledger is a financial entity: personal household, a rental property, or investments.
-- Transactions are classified into line items within a ledger.
CREATE TABLE IF NOT EXISTS ledgers (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  user_id TEXT REFERENCES users(id),
  type TEXT NOT NULL DEFAULT 'personal',       -- personal | property | investment
  description TEXT                             -- optional label (e.g. property address)
);

-- Line items are categories within a ledger (e.g. Mortgage, Rent income, Groceries).
CREATE TABLE IF NOT EXISTS line_items (
  id TEXT PRIMARY KEY,
  ledger_id TEXT REFERENCES ledgers(id),
  name TEXT NOT NULL,
  item_type TEXT DEFAULT 'expense'             -- income | expense
);

-- ---------------------------------------------------------------------------
-- Transactions (raw from Plaid — never modified after insert)
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS transactions (
  id TEXT PRIMARY KEY,
  bank_account_id TEXT REFERENCES bank_accounts(id),
  plaid_transaction_id TEXT UNIQUE,
  date TEXT NOT NULL,                          -- YYYY-MM-DD (Plaid-localised, no conversion needed)
  authorized_datetime TEXT,                    -- ISO-8601 datetime with time (e.g. 2024-01-15T14:23:00Z); NULL when Plaid omits it
  merchant TEXT,
  amount REAL NOT NULL,                        -- original amount in account's native currency
  currency TEXT DEFAULT 'CAD',                 -- ISO 4217 (from Plaid iso_currency_code)
  amount_home REAL,                            -- converted to home currency at sync time (NULL if FX unavailable)
  plaid_category TEXT,                         -- Plaid personal_finance_category primary
  plaid_category_detailed TEXT,                -- Plaid personal_finance_category detailed
  pending INTEGER DEFAULT 0                    -- 1 = pending, do not classify
);

-- ---------------------------------------------------------------------------
-- Classification results
-- ---------------------------------------------------------------------------

-- One row per classified transaction. A transaction has at most one entry
-- (no splits in v1). entry_type drives totals:
--   spending  → counts toward expense total in the ledger
--   income    → counts toward income total
--   transfer  → excluded from all totals (neutral move between accounts)
--   savings   → counts toward savings total (e.g. investment contribution)
--   skip      → ignored entirely (e.g. pending, credit card payment already tracked)
CREATE TABLE IF NOT EXISTS transaction_entries (
  id TEXT PRIMARY KEY,
  transaction_id TEXT UNIQUE REFERENCES transactions(id),
  ledger_id TEXT REFERENCES ledgers(id),
  line_item_id TEXT REFERENCES line_items(id),
  amount REAL NOT NULL,                        -- original currency amount
  amount_home REAL,                            -- home currency amount (copied from transaction)
  entry_type TEXT NOT NULL DEFAULT 'spending', -- spending | income | transfer | savings | skip
  source TEXT,                                 -- rule | llm | manual | manual_retroactive
  confidence REAL,                             -- 0.0–1.0, from LLM
  uncertain INTEGER DEFAULT 0,                 -- 1 = below confidence threshold, user should review
  reasoning TEXT,                              -- LLM explanation
  reviewed INTEGER DEFAULT 0,                  -- 1 = user confirmed this classification
  corrected_from_line_item_id TEXT REFERENCES line_items(id),  -- set when manually corrected
  corrected_at INTEGER                         -- UTC Unix seconds of correction
);

-- ---------------------------------------------------------------------------
-- Classification rules (replaces routing_rules)
-- ---------------------------------------------------------------------------

-- Natural language rules evaluated by the LLM in priority order.
-- is_default=1 rules ship with the app and cannot be deleted (only disabled).
CREATE TABLE IF NOT EXISTS classification_rules (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,                          -- short display name
  description TEXT NOT NULL,                   -- natural language: what this rule matches and does
  rule_type TEXT NOT NULL,                     -- transfer | savings | spending | income | skip
  line_item_id TEXT REFERENCES line_items(id), -- optional target line item
  priority INTEGER NOT NULL DEFAULT 100,       -- lower = evaluated first
  is_default INTEGER NOT NULL DEFAULT 0,       -- 1 = built-in, cannot delete
  enabled INTEGER NOT NULL DEFAULT 1,
  created_at INTEGER NOT NULL
);

-- Default rules (seeded on first setup):
-- priority 1:  Pending skip
-- priority 10: Internal transfer (same amount cross-account within 3 days)
-- priority 20: Investment contribution (outflow to investment platform)
-- priority 30: Credit card payment (chequing→credit matches balance)
-- priority 40: Salary/payroll (Plaid INCOME_SALARY tag)
-- priority 50: Bank fees (Plaid BANK_FEES tag)

-- Legacy substring rules — kept for backward compat, no longer written to
CREATE TABLE IF NOT EXISTS routing_rules (
  id TEXT PRIMARY KEY,
  merchant_pattern TEXT,
  line_item_id TEXT REFERENCES line_items(id)
);

-- Natural language hints (supplementary context for LLM, not priority-ordered)
CREATE TABLE IF NOT EXISTS classification_hints (
  id TEXT PRIMARY KEY,
  text TEXT NOT NULL,
  user_id TEXT REFERENCES users(id)
);

-- ---------------------------------------------------------------------------
-- FX rates cache
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS fx_rates (
  base TEXT NOT NULL,                          -- source currency, e.g. 'USD'
  quote TEXT NOT NULL,                         -- target currency, e.g. 'CAD'
  rate REAL NOT NULL,                          -- 1 base = rate quote
  fetched_at INTEGER NOT NULL,                 -- UTC Unix seconds; reuse if < 24h old
  PRIMARY KEY (base, quote)
);

-- ---------------------------------------------------------------------------
-- Sync
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS sync_cursors (
  connection_id TEXT PRIMARY KEY REFERENCES bank_connections(id),
  cursor TEXT,
  last_synced_at INTEGER
);

-- ---------------------------------------------------------------------------
-- App config (single row, id always = 1)
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS app_config (
  id INTEGER PRIMARY KEY CHECK (id = 1),
  username TEXT,
  ui_password_hash TEXT,                       -- argon2id hash
  ui_password_set_at INTEGER,
  notification_channel TEXT DEFAULT 'in_ui',   -- openclaw_chat | macos | in_ui
  home_currency TEXT DEFAULT 'CAD',            -- ISO 4217; used for all totals and display
  timezone TEXT DEFAULT 'America/Toronto'      -- IANA timezone; used for date-boundary queries
);

-- ---------------------------------------------------------------------------
-- Notifications
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS notifications (
  id TEXT PRIMARY KEY,
  message TEXT NOT NULL,
  urgency TEXT DEFAULT 'normal',               -- normal | high
  created_at INTEGER NOT NULL,
  delivered_via TEXT,
  read INTEGER DEFAULT 0
);

-- ---------------------------------------------------------------------------
-- Plaid credentials (per-user, supersedes .env at runtime)
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS plaid_config (
  id INTEGER PRIMARY KEY,
  user_id TEXT NOT NULL REFERENCES users(id),
  client_id TEXT NOT NULL,
  secret TEXT NOT NULL,
  plaid_env TEXT NOT NULL DEFAULT 'production',
  created_at INTEGER NOT NULL DEFAULT (unixepoch()),
  updated_at INTEGER NOT NULL DEFAULT (unixepoch()),
  UNIQUE(user_id)
);

-- ---------------------------------------------------------------------------
-- Audit logs
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS auto_promoted_rules_log (
  id TEXT PRIMARY KEY,
  rule_id TEXT NOT NULL REFERENCES routing_rules(id) ON DELETE CASCADE,
  merchant TEXT NOT NULL,
  line_item_id TEXT NOT NULL,
  source_transaction_ids TEXT NOT NULL,        -- JSON array
  created_at INTEGER NOT NULL
);
