# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.1.0] - 2026-03-31

### Security Fixes
- Removed `STOCKAI_JWT_TOKEN` support — skill is now API-key only, no user credential flows
- Removed `DSE_API_EMAIL`/`DSE_API_PASSWORD` auto-login — credential-based auth was undocumented and risky
- Added `STOCKAI_API_BASE` domain validation — only `stock-ai.live` domains allowed, prevents redirect attacks

### Removed
- `--token` CLI flag
- `get_token()` function
- `AUTH_COMMANDS` set
- Bearer token header injection in requests

### Changed
- `portfolio` command now uses API key auth instead of JWT token
- `make_request()` simplified — single `X-API-Key` header, no optional Bearer token
- Renamed env var `API_BASE` → `STOCKAI_API_BASE` (avoids conflicts with other tools)
- `optional_env` in `_meta.json` updated to `["STOCKAI_API_BASE"]`

## [1.0.0] - 2026-03-26

### Added
- Initial release
- Free tier commands: `price`, `search`, `market`, `news`
- Pro tier commands: `gainers`, `losers`, `history`
- Enterprise tier commands: `signal`, `vegas`, `ema`, `fib`, `sectors`, `portfolio`
- Multi-dimensional trading system documentation (Vegas Tunnel, Fibonacci, EMA channels)
- Tier-based pricing documentation
- OpenClaw and local .env configuration
