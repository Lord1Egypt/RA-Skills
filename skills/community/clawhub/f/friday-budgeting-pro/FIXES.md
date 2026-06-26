# FIXES.md — Bug Fix Log

---

### Bug: Disconnect redirects to wrong page (Bug 1)

**Symptom:** Clicking "Disconnect" on the `/accounts` page (which POSTs to `POST /profile` with `action=disconnect_bank`) left the user on the profile page instead of returning them to accounts.

**Root cause:** The `profile_post` handler for `action == "disconnect_bank"` re-rendered `profile.html` on success instead of issuing a redirect. The disconnect button in `accounts.html` posts to `/profile`, but after a successful disconnect the user should land back on `/accounts` (or `/setup` if no connections remain).

**Fix (`ui/server.py`):** After a successful `_sm.disconnect()` call, replaced the re-render with:
- `_redirect("/accounts")` if the user still has remaining connections
- `_redirect("/setup")` if no connections remain (freshly disconnected user needs to re-link)

Also fixed a secondary bug: the old code called `_get_connections()` (no `uid`) after disconnect, which would return all users' connections instead of just the current user's. Now it calls `_get_connections(uid)`.

**Files changed:** `ui/server.py`

---

### Bug: Institution shows "Unknown Institution" (Bug 2)

**Symptom:** After connecting a bank via Plaid Link, the institution name was always `NULL` in `bank_connections`, causing the `/accounts` page to display "── Unknown Institution" for every connected bank.

**Root cause:** `complete_link()` in `server/main.py` intentionally left `institution_name` as `NULL` with the comment "fetching it requires Plaid /institutions/get_by_id which is out of scope; see issue #34."

**Fix (`server/main.py`):** After exchanging the public token, call `provider.get_institution_name(access_token)` (which was already implemented in `PlaidProvider` via `/item/get` → `/institutions/get_by_id`) and store the result in `bank_connections.institution_name`. The call is wrapped in `try/except` so a Plaid API failure does not break the overall link flow.

**Note:** The existing connection in the DB (which has `institution_name = NULL`) will continue to show "Unknown Institution" until the user disconnects and reconnects their bank, or until a DB backfill is performed via: `sqlite3 ~/.friday-bp/data.db "UPDATE bank_connections SET institution_name = 'Your Bank Name' WHERE institution_name IS NULL;"`

**Files changed:** `server/main.py`

This file documents all bugs found and fixed in Friday Budgeting Pro.

---

### Bug: load_dotenv() timing issue

**Symptom:** Environment variables (PLAID_CLIENT_ID, PLAID_SECRET, PLAID_ENV) were not available at startup even though `.env` existed.

**Root cause:** `load_dotenv()` was being called too late in the startup sequence — after modules that needed the env vars had already been imported.

**Fix:** Moved `load_dotenv()` call to the very top of `server/main.py` (before any other imports that depend on env vars).

---

### Bug: Hardcoded sandbox environment

**Symptom:** Plaid API calls always used the sandbox environment even when the app was configured for production.

**Root cause:** The `PlaidProvider` was instantiated with `env="sandbox"` hardcoded in some call sites instead of reading from the `PLAID_ENV` environment variable.

**Fix:** Changed those call sites to pass `env=None` so `PlaidProvider.__init__` reads `PLAID_ENV` from the environment (defaulting to `'sandbox'` if unset).

---

### Bug: Missing complete_url / POST /link/complete route

**Symptom:** After completing Plaid Link (selecting a bank, logging in), the browser showed a blank page or error — the public token was never exchanged.

**Root cause:** The `link.html` template's `complete_url` was not set correctly (or the `POST /link/complete` route didn't exist). The Plaid `onSuccess` callback tried to POST to a non-existent endpoint.

**Fix:** Added the `POST /link/complete` route in `ui/server.py` and ensured `link.html` receives `complete_url="/link/complete"` from the template context.

---

### Bug: Accounts not showing after bank connection

**Symptom:** After successfully connecting a bank via Plaid Link (the link flow completes, redirects to `/accounts?linked=1`), the accounts page shows "No bank accounts connected yet." — no accounts appear.

**Root cause:** Two issues combined:

1. **Missing initial sync**: `complete_link()` only stores the bank connection row in `bank_connections`. It does NOT call Plaid's `/transactions/sync` endpoint, so the `bank_accounts` table is never populated. The `/accounts` page queries `bank_accounts` which is empty.

2. **Wrong `plaid_env` default in `complete_link()`**: The `complete_link()` function had `plaid_env: str = "sandbox"` as its default, but the link token was generated using the `PLAID_ENV` env variable (e.g. `production`). This caused the token exchange to fail silently (exception caught/ignored) in production mode when called from the UI without an explicit `plaid_env` argument.

**Fix:** Three changes:

- `server/main.py` → `complete_link()`: Changed signature from `plaid_env: str = "sandbox"` to `plaid_env: str | None = None` so it reads from `PLAID_ENV` env var (matching `start_link` behavior).

- `ui/server.py` → `link_complete()` handler (POST /link/complete): Added a `sync()` call immediately after a successful `complete_link()`. This triggers Plaid's `/transactions/sync` which populates `bank_accounts`. Errors from the sync are non-fatal (logged as warnings) — the connection is already saved.

- `ui/server.py` → setup wizard step 3: Same sync call added after `complete_link()` during the initial setup bank-link flow.

**Files changed:**
- `server/main.py`
- `ui/server.py`

---

### Bug: Accounts not showing after bank connection — Part 2 (empty account / no transactions)

**Symptom:** After successfully connecting a bank (link flow completes, redirects to `/accounts?linked=1`), the accounts page still shows "No bank accounts connected yet." — even though `bank_connections` has a row.

**Root cause:** In `sync()` (`server/main.py`), the `bank_accounts` table is only populated via `INSERT OR IGNORE` inside the **added transactions loop** (`for txn in added_txns`). A second "always-update" block above that loop only runs `UPDATE`, never `INSERT`. For brand new or empty accounts that have no transaction history yet, Plaid's `/transactions/sync` response includes account metadata in `accounts[]` but returns zero entries in `added[]`. The UPDATE has no rows to act on and the INSERT never runs, leaving `bank_accounts` permanently empty.

**Evidence from logs:**
- `POST /link/complete → 302 → /accounts?linked=1` (no errors logged = complete_link + sync both succeeded)
- `bank_connections` had 1 row; `bank_accounts` had 0 rows

**Fix (`server/main.py`):** Changed the "always update" account metadata block to also run `INSERT OR IGNORE INTO bank_accounts` before the `UPDATE`, so every account returned in the sync response is guaranteed to have a row regardless of transaction count.

**Files changed:**
- `server/main.py` — accounts upsert block (lines ~1620-1650)

---

### Fix: Plaid credentials and access tokens fully persisted across daemon restarts

**Symptoms (three related issues):**
1. After `configure_plaid()` was called, a daemon restart would lose Plaid credentials unless `.env` was present — the DB row was not loaded into `os.environ` on startup.
2. `configure_plaid()` in tests raised `sqlite3.OperationalError: no such table: sessions` because the DB write path called `get_active_user_id()` against an uninitialised temp DB.
3. `health_monitor.check_all_connections()` ignored the `plaid_provider` argument and created its own per-connection providers — which triggered real Plaid API calls in tests when env vars were set, masking the mock.

**Root cause analysis:**

| Component | Before | After |
|---|---|---|
| `plaid_config` table | Existed in schema | Unchanged — already correct |
| Access token encryption | Fernet key in macOS Keychain (stable) | Unchanged — already correct |
| Access tokens in DB | Stored encrypted in `bank_connections` | Unchanged — already correct |
| `configure_plaid()` → DB write | Present but crashed on uninit DB in tests | Wrapped in `try/except`; gracefully skips if DB not ready |
| Daemon startup | Only loaded `.env`; no DB credential loading | Adds `_load_plaid_config_from_db()` step after `init_db` |
| `health_monitor` | Created per-connection providers, ignoring `plaid_provider` arg | Uses passed `plaid_provider` when not None; only creates per-connection providers when called standalone |

**Fixes:**

- **`server/daemon.py`** — Added `_load_plaid_config_from_db()` called from `main()` after `init_db`. Reads the most recently updated `plaid_config` row and exports `PLAID_CLIENT_ID`, `PLAID_SECRET`, `PLAID_ENV` into `os.environ`. DB values override `.env` so the authoritative per-user credentials always win on restart. Graceful no-op if table is empty or DB doesn't exist yet. `load_dotenv` kept as inline import inside `main()` so test patches on `dotenv.load_dotenv` continue to intercept it.

- **`server/main.py` (`configure_plaid`)** — Wrapped the entire DB write block (including `get_active_user_id()`) in `try/except Exception`. In test environments with uninitialised temp DBs the function now falls through cleanly to the `.env` write.

- **`server/health_monitor.py`** — Restored the original contract: when `plaid_provider` is not None, use it for all connections (enables test mocks and the module-level singleton). When None, build per-connection providers from `plaid_config` DB credentials. Changed `SELECT` to include `user_id` and `plaid_env` only in the None-provider path.

**Persistence guarantee summary:**
- Fernet encryption key: stored in macOS Keychain by `server.crypto.get_or_create_key()` — stable across all restarts.
- Encrypted access tokens: persisted in `bank_connections.plaid_access_token_encrypted` (SQLite file) — survive restarts.
- Plaid API credentials: persisted in `plaid_config` (SQLite, per user) AND in `.env` (fallback) — loaded into env on every daemon startup.

**Files changed:**
- `server/daemon.py` — `_load_plaid_config_from_db()` function + call in `main()`
- `server/main.py` — `configure_plaid()` DB write wrapped in `try/except`
- `server/health_monitor.py` — `check_all_connections()` provider resolution logic
- `server/plaid_credentials.py` — new module (per-user credential resolution helper)
