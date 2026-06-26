# Changelog

## 1.2.1 — 2026-04-01

### Fixed
- `references/troubleshooting.md`: removed stale `--url` flag example, stopped instructing agent to ask user for webhook URL — now directs to administrator
- `SKILL.md` Rule 2: removed stale `config.json` reference

## 1.2.0 — 2026-03-31

### Breaking
- Webhook URL now read exclusively from `BITRIX24_WEBHOOK_URL` env var — no file-based storage. OpenClaw users configure it as `apiKey` in `openclaw.json`.
- Removed `save_webhook.py` script — webhook is no longer accepted via chat or CLI
- Removed `--url` and `--config-file` flags from all scripts
- Removed `BITRIX24_KEYRING_PASSWORD` env var — no longer needed
- Removed pip dependencies: `keyring`, `keyrings.alt`, `pycryptodome`

### Changed
- `bitrix24_config.py` rewritten: removed all keyring/encryption code (~150 lines), reads webhook from env var only
- Cache file renamed from `config.json` to `cache_user_timezone.json` — stores only non-secret user_id and timezone
- SKILL.md: new Security Model, updated frontmatter (`primaryEnv`, `requires.env`), rewritten Setup section
- `agents/openai.yaml`: env var changed to `BITRIX24_WEBHOOK_URL`
- `references/access.md`: setup instructions updated for env var approach

### Security
- Addresses ClawHub review: declared `primaryEnv`, removed `/etc/machine-id` access, removed plaintext fallback, removed metadata mismatches

## 1.1.9 — 2026-03-31

### Fixed
- Removed `requires.config` from SKILL.md and `agents/openai.yaml` — OpenClaw treats `config` entries as dotted keys in `openclaw.json`, not filesystem paths; `~/.config/bitrix24-skill/config.json` was always failing validation, leaving the skill permanently in "needs setup" state

## 1.1.8 — 2026-03-31

### Fixed
- Migrated SKILL.md frontmatter to official ClawHub schema (`requires.env`, `requires.config`, `install` with `kind: uv`) — fixes registry summary showing "none" for env vars and config paths
- Agent pip install in Setup section now requires explicit user consent
- Cleaned up `agents/openai.yaml` to match registry schema

## 1.1.7 — 2026-03-31

### Fixed
- Added `primary_credential` to registry metadata for correct summary display
- Credential description now explicitly documents fallback chain security limitations
- Added `env_vars` and `primary_credential` to `agents/openai.yaml` for registry visibility

## 1.1.6 — 2026-03-31

### Security
- Removed silent runtime `pip install` from code — package installation now only via visible shell commands in agent instructions
- Declared `BITRIX24_KEYRING_PASSWORD` env var in skill metadata (`requires.env_vars`) with fallback behavior description

## 1.1.5 — 2026-03-31

### Security
- Three-level encrypted storage for webhook:
  1. OS keychain (macOS Keychain, Windows Credential Vault, Linux SecretService) — webhook never on disk
  2. AES-256 encrypted file via `keyrings.alt` EncryptedKeyring — for containers and headless servers
  3. Plaintext config with permissions 600 — fallback when encryption packages unavailable
- Agent auto-installs `keyring`, `keyrings.alt`, `pycryptodome` when falling back to plaintext
- OS keyring probe correctly rejects file-based backends (PlaintextKeyring) in containers
- Encryption password derived from env var `BITRIX24_KEYRING_PASSWORD`, `/etc/machine-id`, or built-in default

### Changed
- `bitrix24_config.py`: removed hard dependency on `keyring` — all crypto packages are now optional
- Updated Security Model in SKILL.md with three-level storage description
- Added auto-install instructions for agent in Setup section
- Updated credential metadata: `storage: "auto"` instead of `"os-keychain"`

## 1.1.2 — 2026-03-30

### Fixed
- Added rule: do not use im.*/imbot.* methods for replying to users — the channel plugin handles delivery
- Clarified references/chat.md and references/files.md to separate "reply to user" vs "manage other chats" scenarios

## 1.1.1 — 2026-03-27

### Fixed
- Declared webhook credential in skill metadata (credentials.webhook_url with storage path)
- Softened Rule 2: transparent about connecting to Bitrix24, hides only implementation details
- Rule 1: clarified that user authorized access by providing webhook

## 1.1.0 — 2026-03-27

### Changed
- Switched from Vibe Platform to direct webhook integration
- New scripts: bitrix24_call.py, bitrix24_batch.py, bitrix24_config.py, check_webhook.py, save_webhook.py
- Updated all reference files for webhook-based API
- Landing page updated for webhook setup flow

### Removed
- Vibe Platform scripts (vibe.py, vibe_config.py, check_connection.py)
- Reference files: bots, telephony, workflows, ecommerce, duplicates, timeline-logs

## 1.0.0 — 2026-03-26

Initial release — Bitrix24 REST API skill for OpenClaw.
