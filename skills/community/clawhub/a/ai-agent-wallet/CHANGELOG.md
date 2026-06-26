# Changelog

All notable changes to `agent-wallet-skills` are documented here.

## [v1.2.4] - 2026-04-14

### Security
- Enforced double-confirmation for mainnet sends in `scripts/send.js`:
  - requires `--confirm=true`
  - requires `--confirmMainnet=true` when chain is recognized as mainnet
- Improved native amount validation with explicit parse failure handling.
- Aligned skill frontmatter with implementation by setting `security.reads_env_secrets: true` for `WALLET_SECRET_KEY`.

## [v1.2.3] - 2026-04-14

### Added
- Added dual transfer support to `scripts/send.js`:
  - native coin sends via `sendTransaction`
  - ERC-20 token sends via `transfer` when `--tokenAddress` is provided
- Added token metadata controls for send flow: optional `--decimals` and `--symbol`.

### Changed
- Updated `SKILL.md` routing and send workflow documentation for native + token transfer modes.

## [v1.2.2] - 2026-04-14

### Added
- Added a new message-signing executable:
  - `node scripts/sign-messages.js --message="hello from wallet"`
- Expanded skill routing and workflow documentation to include the `sign` action and usage guidance.

## [v1.1.3] - 2026-04-13

### Changed
- Hardened local-wallet examples to align with file-based config and reduce security scanner false positives:
  - replaced remaining `process.env` usage in `send` and `balance` examples with `wallet/config.json` + `wallet/signer.json` reads
  - updated generate examples to persist encrypted signer fields (`encryptedSeedPhrase` / `encryptedPrivateKey`) instead of raw secret fields
- Clarified runtime requirement for secure helper functions (`encryptSecret` / `decryptSecret`) backed by a key manager or OS keychain.

### Security
- Removed mixed env/file secret patterns from examples that can trigger suspicious-pattern scans.
- Explicitly reinforced no-plaintext signer secret storage in `wallet/signer.json`.

## [v1.1.2] - 2026-04-13

### Changed
- Switched local wallet source-of-truth files from workspace paths to wallet paths:
  - signer details now come from `wallet/signer.json`
  - network defaults now come from `wallet/config.json`
- Updated `generate`, `send`, `balance`, and local router docs to require file-based config/wallet flows instead of env-based signer/RPC usage.
- Added explicit default-network precheck before any wallet action (`generate`, `balance`, `send`):
  - load `wallet/config.json` first
  - require array format `[{ rpc_url, chain_id, current }]`
  - require exactly one `current: true` entry
  - require non-empty `rpc_url` and `chain_id` on the current entry
- Updated network config contract to support multi-network entries with a single active default and standardized `chain_id` string handling.
- Strengthened no-regeneration behavior for wallet generation/import:
  - if signer file exists, do not regenerate automatically
  - regeneration/overwrite requires explicit user request and confirmation

### Security
- Removed default env-secret reads in local wallet skill docs for signer and RPC configuration.
- Added stricter failure handling for malformed signer/network config JSON and invalid default-network states (including multiple current entries).
- Reinforced guardrail to stop execution and prompt for network defaults before proceeding with any action.

## [v1.1.1] - 2026-04-11

### Changed
- Added scanner-friendly frontmatter declarations to all skill files:
  - `version`
  - `dependencies`
  - `runtime`
  - `required_env` / `optional_env`
  - `security`

### Security
- Explicitly declared env-secret read requirements for `generate` and `send`.
- Explicitly declared read-only/no-secret mode for `balance`.
- Added confirmation requirements directly in frontmatter to reduce false-positive suspicious-pattern flags.

## [v1.1.0] - 2026-04-11

### Added
- Added runtime and dependency declarations across wallet skills (`viem`, Node.js 18+, RPC requirements).
- Added explicit secret/input requirements (`RPC_URL`, optional `SEED_PHRASE` / `PRIVATE_KEY`) with consent-before-read rules.
- Added balance route at top level and local router mapping for `generate`, `balance`, and `send`.
- Added standard response contract across skills:
  - `action`, `chain`, `address`, `txHash`, `status`, `next_step`

### Changed
- Hardened security defaults:
  - read-only by default
  - testnet default when chain is unspecified
  - explicit confirmation before broadcast
  - double confirmation for mainnet sends
- Expanded balance skill to support ERC-20 contract balances via `readContract(balanceOf)` and `formatUnits`.

### Security
- Clarified allowed secret storage targets (vault/key manager/encrypted store).
- Explicitly forbids plaintext secret storage and secret logging.
- Added failure handling guidance for generate/send/balance edge cases.
