# Secrets and configuration

## What to verify in review

1. **No literals in application code** — API keys, tokens, database URLs, and private keys must not appear as string literals in `.ex` files shipped to production.

2. **Runtime configuration** — Prefer `config/runtime.exs` (or release-time env) for values that differ per environment. `Application.get_env/2` should read secrets supplied via environment or secret stores, not checked-in files.

3. **Committed config** — `config/*.exs` may set non-secret defaults; deployment secrets belong in env vars or external secret managers, not in git history.

4. **`.env` and similar** — Ensure `.env*` is in `.gitignore` when used locally; never commit files that contain real credentials.

## Useful checks

- Search for common patterns: `api_key`, `secret`, `password`, `BEGIN PRIVATE KEY`, connection strings with embedded credentials.
- Confirm `Mix.env()` does not accidentally enable dev-only shortcuts that log or return secrets in production paths.

## Valid patterns (do not flag without evidence)

- Placeholders like `System.get_env("DATABASE_URL")` with documentation that ops sets the var.
- Test fixtures with obviously fake credentials in `test/support` only.
