# DigitalOcean Spaces

## 1. Create a private Space

1. DigitalOcean Console → **Spaces Object Storage** → **Create a Space**
2. Choose a datacenter region (`nyc3`, `sfo3`, `ams3`, `sgp1`, `fra1`, …)
3. Restrict file listing: **Private**

## 2. Create a key — read the warning first

> **WARNING: Spaces keys are account-wide.** DigitalOcean does not support
> per-Space scoping — this key can read, write, and delete EVERY Space in
> your account. Prefer a dedicated team/project for backups, and rotate more
> aggressively than usual (30–60 days). If account-wide blast radius is
> unacceptable, pick a provider with bucket-scoped keys (R2, B2, AWS).

1. **API** → **Spaces Keys** → **Generate New Key**
2. Note the **Key** (= access key) and **Secret** (= secret key)

## 3. Store the credentials (run this yourself — keep keys out of the chat)

```bash
aws configure --profile openclaw-backup
chmod 600 ~/.aws/credentials
```

## 4. Configure the skill (non-secret keys only)

```bash
openclaw config patch 'skills.entries.cloud-backup.config.bucket="my-backup-space"'
openclaw config patch 'skills.entries.cloud-backup.config.region="nyc3"'
openclaw config patch 'skills.entries.cloud-backup.config.endpoint="https://nyc3.digitaloceanspaces.com"'
openclaw config patch 'skills.entries.cloud-backup.config.profile="openclaw-backup"'
```

## Credential safety (read me)

- This key can read, write, and DELETE your backups. Treat it like a password.
- Never commit it to git. Never store it in openclaw.json: **backups archive
  openclaw.json itself** — a key stored there rides along inside every archive
  it protects.
- Scope the key to this one bucket where the provider supports it. An
  account-wide key turns one leaked archive into an account takeover.
- Rotate every ~90 days and immediately on any suspicion: create new key →
  update the profile → verify a backup → revoke the old key.

## Notes

- Region in the endpoint and `config.region` must match.
- No free tier (Spaces starts at $5/mo for 250 GB).
- `SignatureDoesNotMatch` → endpoint region doesn't match the Space's region.

## Deprecated (v1): keys in OpenClaw config — do not use

v1 documented `skills.entries.cloud-backup.env.ACCESS_KEY_ID/SECRET_ACCESS_KEY`.
It still works in v2 with loud warnings and is removed in v3. Migration:
`references/credentials.md`.
