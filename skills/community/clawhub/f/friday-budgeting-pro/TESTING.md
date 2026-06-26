# Testing — Friday Budgeting Pro

This document describes how tests are structured, isolated, and run locally
and in CI.

---

## Quick start

```bash
# Install dependencies (once)
pip install -r requirements.txt

# Run unit tests (no server, no Plaid needed)
pytest -q --ignore=tests/test_plaid_e2e.py

# Run all tests including integration
pytest -q
```

---

## Test database isolation

**Every test uses an isolated, throwaway database.**  The production DB at
`~/.friday-bp/data.db` is **never** read or written by the test suite.

### How it works

`tests/conftest.py` defines an `autouse=True` fixture called
`_isolated_app_dir` that runs for every test automatically:

1. Creates a fresh temp directory via pytest's `tmp_path`.
2. Sets `FRIDAY_BP_APP_DIR` in the process environment to point at that dir.
3. Patches `server.paths.APP_DIR`, `DB_PATH`, `SYNC_LOCK_PATH`, and
   `EXPORTS_DIR` to resolve under the temp dir.

Individual test fixtures (e.g. `db_path` in many test files) layer on top of
this by calling `init_db()` or `migrate_db()` to set up the schema.

### CI safety check

`scripts/check_test_isolation.py` scans every file in `tests/` for
hard-coded production paths (`~/.friday-bp/` or `.friday-bp/data.db`) in
executable code (not comments or docstrings).  It runs as part of the
`security-lint` CI job:

```bash
python3 scripts/check_test_isolation.py
# → OK — no production paths in tests
```

---

## UI tests (Playwright)

```bash
# Install Playwright and the Chromium binary (once)
pip install playwright
playwright install chromium

# Run all Playwright UI tests
pytest tests/ui/ -v
```

The `server_url` fixture in `tests/ui/conftest.py` starts a fresh server
subprocess with `FRIDAY_BP_DB_PATH` set to a temp file — it never touches
`~/.friday-bp/data.db`.

---

## Plaid sandbox tests

Tests that require Plaid credentials are **skipped automatically** unless the
relevant environment variables are set:

```bash
# Run Plaid sandbox tests
PLAID_CLIENT_ID=xxx PLAID_SANDBOX_SECRET=xxx PLAID_ENV=sandbox \
    pytest tests/integration/ -v
```

Sandbox institutions (pre-seeded by Plaid):
- First Platypus Bank
- First Gingham Credit Union

**Never** use production Plaid credentials in tests.  CI uses
`PLAID_ENV=sandbox` exclusively.

---

## What must NOT happen

| ❌ Never | ✅ Always |
|---------|---------|
| Read from `~/.friday-bp/data.db` | Use a temp dir via `_isolated_app_dir` |
| Write to a production Plaid connection | Use sandbox or mock Plaid |
| Use production Plaid credentials | Use `PLAID_ENV=sandbox` + sandbox secret |
| Playwright tests without `FRIDAY_BP_APP_DIR` set | `server_url` fixture sets it |

---

## CI jobs

| Job | What it checks |
|-----|---------------|
| `unit` | All unit tests (temp DB, no Plaid) |
| `lint` | `ruff` + `black` formatting |
| `security-lint` | `lint_security.py` + `check_test_isolation.py` |
| `integration` | Integration tests with temp DB |
| `mcp-smoke` | Server imports + `setup_status()` sanity check |
