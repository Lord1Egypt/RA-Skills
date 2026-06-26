# Config reference

This skill now uses a centralized app config module plus two data layers:

- `scripts/config.py`: centralized app-owned configuration and shared config loading
- `references/configs.defaults.json`: mutable user defaults shipped with the skill
- `~/.apple-health-sync/config/config.json`: generated and mutable per-user user config

Required local state:

- The default state root is `~/.apple-health-sync`.
- Passing `--state-dir <path>` moves all required local artifacts under that custom root instead.
- `config/config.json` is created by `scripts/onboarding.py`.
- Protocol `v4` uses `config/secrets/private_key.pem`.
- Protocol `v5` uses `config/secrets/signing_private_key_v5.pem` and `config/secrets/encryption_private_key_v5.pem`.

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
  "last_validation_raw_days": 7,
  "last_validation_stored_days": 7,
  "last_validation_dropped_days": 0
}
```

Onboarding writes user-owned fields only. App-owned keys such as `onboarding_version`, `ios_app_link`, and the Supabase settings are centralized in `scripts/config.py` and are not persisted back into `config.json`.

Protocol behavior:

- `v4` keeps the legacy RSA keypair and RSA-OAEP encrypted server rows.
- `v5` uses Ed25519 for challenge signatures and X25519 + ChaCha20-Poly1305 for encrypted day payloads.
- `fetch_health_data.py` can read mixed history: legacy RSA rows from the old tables plus `v5` rows from `*_v2`.

## Storage behavior

- `storage=sqlite`: upsert decrypted day payloads into `health_data`
- `storage=json`: append decrypted envelopes to NDJSON

`storage` remains a mutable user field. Existing installs with the removed legacy value `custom` are migrated to `sqlite` when the config is loaded.

## Relay behavior

- `fetch_health_data.py` reads `supabase_region`, `supabase_get_data_url`, and `supabase_publishable_key` from `scripts/config.py`
- `onboarding.py` reads `supabase_region`, `supabase_qr_code_generator_url`, and `supabase_publishable_key` from `scripts/config.py`
- `unlink_device.py` reads `supabase_region`, `supabase_unlink_device_url`, and `supabase_publishable_key` from `scripts/config.py`

## Validation behavior in `fetch_health_data.py`

- Accept only date keys in `YYYY-MM-DD`
- Accept only safe metric keys matching `^[A-Za-z0-9_.:-]{1,64}$`
- Accept only JSON values `null`, `bool`, finite numbers, lists, and objects
- Drop all string values to prevent persisted prompt-style instructions
- Enforce depth, node, list, dict, and payload-size limits
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
