# Config reference

This skill now uses a centralized app config module plus two data layers:

- `scripts/config.py`: centralized app-owned configuration and shared config loading
- `references/configs.defaults.json`: mutable user defaults shipped with the skill
- `~/.apple-health-sync/config/config.json`: generated and mutable per-user user config

Required local state:

- The default state root is `~/.apple-health-sync`.
- Passing `--state-dir <path>` moves all required local artifacts under that custom root instead.
- State, config, and secrets directories are restricted to mode `0700`.
- Private keys, user config, onboarding artifacts, SQLite/NDJSON health storage, and saved summaries are restricted to mode `0600`; public key files may use `0644`.
- `config/config.json` is created by `scripts/onboarding.py`.
- Protocol `v4` uses `config/secrets/private_key.pem`.
- Protocol `v5` uses `config/secrets/signing_private_key_v5.pem` and `config/secrets/encryption_private_key_v5.pem`.
- `onboarding.py --rotate` archives the current identity under `config/key-backups/<UTC timestamp>/`, then always creates new keys and a new user ID. Keeping the previous user ID during rotation is not supported.

Legacy note:

- `~/.apple-health-sync/config/runtime.json` is still read as a fallback for older installs, but new writes go to `config.json`.

Effective config order:

1. app-owned values from `scripts/config.py`
2. `references/configs.defaults.json`
3. `config.json` (or legacy `runtime.json`)

App-owned values are centralized in `scripts/config.py`, including:

- `onboarding_version`
- `ios_app_link`
- `supabase_region`
- `supabase_get_data_url`
- `supabase_qr_code_generator_url`
- `supabase_unlink_device_url`
- `supabase_publishable_key`

## Skill-shipped config

`references/configs.defaults.json` contains mutable user defaults:

```json
{
  "storage": "sqlite"
}
```

## User Config

User config defaults to `~/.apple-health-sync`, or the `--state-dir` path when provided:

- SQLite DB: `~/.apple-health-sync/health_data.db`
- User config: `~/.apple-health-sync/config/config.json`
- Private key: `~/.apple-health-sync/config/secrets/private_key.pem`

Typical user config fields:

```json
{
  "user_id": "ahs_...",
  "protocol_version": 5,
  "algorithm": "RSA-2048",
  "state_dir": "/Users/<user>/.apple-health-sync",
  "config_dir": "/Users/<user>/.apple-health-sync/config",
  "secrets_dir": "/Users/<user>/.apple-health-sync/config/secrets",
  "private_key_path": "/Users/<user>/.apple-health-sync/config/secrets/private_key.pem",
  "public_key_path": "/Users/<user>/.apple-health-sync/config/public_key.pem",
  "public_key_base64": "<base64-spki-public-key>",
  "signing_algorithm": "Ed25519",
  "signing_private_key_path": "/Users/<user>/.apple-health-sync/config/secrets/signing_private_key_v5.pem",
  "signing_public_key_path": "/Users/<user>/.apple-health-sync/config/signing_public_key_v5.pem",
  "signing_public_key_base64": "<base64-raw-ed25519-public-key>",
  "encryption_algorithm": "X25519",
  "box_algorithm": "X25519-ChaCha20Poly1305",
  "encryption_private_key_path": "/Users/<user>/.apple-health-sync/config/secrets/encryption_private_key_v5.pem",
  "encryption_public_key_path": "/Users/<user>/.apple-health-sync/config/encryption_public_key_v5.pem",
  "encryption_public_key_base64": "<base64-raw-x25519-public-key>",
  "onboarding_fingerprint": "<sha256-hex>",
  "onboarding_payload_json": "<compact-json>",
  "onboarding_payload_hex": "<hex-encoded-json>",
  "storage": "sqlite",
  "sqlite_path": "/Users/<user>/.apple-health-sync/health_data.db",
  "json_path": "/Users/<user>/.apple-health-sync/config/health_data.ndjson",
  "qr_payload_path": "/Users/<user>/.apple-health-sync/config/registration-qr.json",
  "qr_png_path": "/Users/<user>/.apple-health-sync/config/registration-qr.png",
  "last_rotation_at": "<UTC timestamp>",
  "last_rotation_backup_path": "/Users/<user>/.apple-health-sync/config/key-backups/<UTC timestamp>",
  "last_fetch_attempt_at": "<UTC timestamp>",
  "last_fetch_success_at": "<UTC timestamp>",
  "last_unlink_attempt_at": "<UTC timestamp>",
  "last_unlink_success_at": "<UTC timestamp>",
  "last_validation_raw_days": 7,
  "last_validation_stored_days": 7,
  "last_validation_dropped_days": 0
}
```

Onboarding writes user-owned fields only. App-owned keys such as `onboarding_version`, `ios_app_link`, and the Supabase settings are centralized in `scripts/config.py` and are not persisted back into `config.json`.

Protocol behavior:

- Both versions require the pinned Python `cryptography` package and keep cryptographic operations in memory without invoking OpenSSL.
- `v4` keeps the legacy RSA keypair and RSA-OAEP encrypted server rows.
- `v5` uses Ed25519 for challenge signatures and X25519 + ChaCha20-Poly1305 for encrypted day payloads.
- `fetch_health_data.py` can read mixed history: legacy RSA rows from the old tables plus `v5` rows from `*_v2`.

## Rotation backups

`onboarding.py --rotate` creates a private identity archive before replacing any keys. The archive contains:

- the previous `config.json` and legacy `runtime.json` when present;
- all recognized RSA, Ed25519, and X25519 public/private key files that exist;
- the previous QR JSON/PNG artifacts when present;
- a manifest with the previous and replacement user IDs, protocol version, fingerprint, file list, and SHA-256 checksums.

The backup directory uses mode `0700`; every archived file uses `0600`, including public keys, because the archive also contains private identity material. A configured identity must have its complete protocol-specific key set before rotation. Missing required artifacts or any copy-verification failure aborts rotation. Backups are never pruned automatically.

Rotation always starts a new server identity. Existing encrypted rows remain bound to the archived user ID and require the archived encryption private key. The active SQLite database is retained and may therefore continue to contain locally decrypted rows for previous user IDs.

## Operation timestamps

- `last_fetch_attempt_at` and `last_unlink_attempt_at` record the most recent invocation, including failed calls.
- `last_fetch_success_at` and `last_unlink_success_at` change only after a successful operation.
- Deprecated `last_fetch_at` and `last_unlink_at` remain as success-only compatibility aliases.
- `last_fetch_status`, `last_fetch_error`, `last_unlink_status`, and `last_unlink_error` describe the most recent attempt.
- On the next operation, a legacy `last_*_at` value is migrated to `last_*_success_at` only when its stored status is `ok`; an error-associated legacy timestamp is discarded because no successful time can be inferred from it.

## Storage behavior

- `storage=sqlite`: upsert decrypted day payloads into `health_data`
- `storage=json`: append decrypted envelopes to NDJSON

`storage` remains a mutable user field. Existing installs with the removed legacy value `custom` are migrated to `sqlite` when the config is loaded.

## Relay behavior

- Every request URL is checked against an exact allowlist before transmission; other hosts, schemes, paths, and query strings are rejected.
- `fetch_health_data.py` uses only `https://snpiylxajnxpklpwdtdg.supabase.co/functions/v1/get-data-v2` and sends the user ID, public key, and challenge signature. It receives ciphertext and decrypts health data locally.
- `onboarding.py` uses only `https://snpiylxajnxpklpwdtdg.supabase.co/functions/v1/qr-code-generator` and sends public onboarding material plus a challenge signature. It never sends private keys or health records.
- `unlink_device.py` uses only `https://snpiylxajnxpklpwdtdg.supabase.co/functions/v1/unlink-device` and sends the user ID, public key, and challenge signature.

## Validation behavior in `fetch_health_data.py`

- Accept only date keys in `YYYY-MM-DD`
- Accept only safe metric keys matching `^[A-Za-z0-9_.:-]{1,64}$`
- Accept only JSON values `null`, `bool`, finite numbers, lists, and objects
- Drop all string values to prevent persisted prompt-style instructions
- Enforce depth, node, list, dict, and payload-size limits
- Accept the `workouts[*].heart_rate_samples` array through a dedicated strict validator; each point contains only `start_offset_ms`, `end_offset_ms`, and `bpm`, and valid arrays are never silently truncated at the generic 512-item limit
- Accept `workout_timing`, `workout_events`, `speed_samples`, and `distance_intervals` only through dedicated all-or-nothing validators with fixed fields, enumerated event/source values, finite numbers, and valid time ranges; always discard the retired `workout_activities` field
- Accept `workouts[*].route_points` only through a dedicated all-or-nothing validator; coordinates must be in range and optional altitude, accuracy, speed, and course values must be finite and valid
- Permit up to 65,536 points in each high-resolution workout series; oversized or malformed series are rejected instead of partially truncated
- Merge overlapping v5 scopes with `history` as the base and `recent` winning per day category
- Fail closed when all decrypted day payloads are rejected

## SQLite schema

```sql
create table health_data (
  id integer primary key autoincrement,
  user_id text not null,
  date text not null,
  data text not null,
  created_at text not null,
  updated_at text not null
);
```

CronJobs are created and managed in OpenClaw, not by scripts in this skill.
They must be created only after an explicit user request and confirmation.

Saved summaries require `--save <path> --confirm-sensitive-save`, write a new regular `0600` file, reject symbolic links and existing targets, and expose `record_count` instead of user/record identifiers.
