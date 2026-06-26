# Cloudflare R2

## 1. Create a private bucket

1. Cloudflare Dashboard → **R2 Object Storage** → **Create bucket**
2. Pick a name (lowercase, no dots); location hint "Automatic" is fine
3. Recommended: add a lifecycle rule **Abort incomplete multipart uploads
   after 1 day** (cleans up interrupted uploads)

## 2. Create a least-privilege key

1. R2 → **Manage R2 API Tokens** → **Create API token**
2. Permissions: **Object Read & Write**
3. Scope: **restrict to your backup bucket only**
4. Note the **Access Key ID** and **Secret Access Key** for the next step

## 3. Store the credentials (run this yourself — keep keys out of the chat)

```bash
aws configure --profile openclaw-backup   # paste key id + secret; region: auto
chmod 600 ~/.aws/credentials
```

## 4. Configure the skill (non-secret keys only)

```bash
openclaw config patch 'skills.entries.cloud-backup.config.bucket="my-backup-bucket"'
openclaw config patch 'skills.entries.cloud-backup.config.region="auto"'
openclaw config patch 'skills.entries.cloud-backup.config.endpoint="https://<ACCOUNT_ID>.r2.cloudflarestorage.com"'
openclaw config patch 'skills.entries.cloud-backup.config.profile="openclaw-backup"'
```

Find your Account ID in the dashboard sidebar or the R2 overview page.

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

- R2 region is always `auto` — single global namespace.
- Zero egress fees; free tier: 10 GB storage, 10M reads / 1M writes per month.
- Signature errors usually mean a wrong Account ID in the endpoint URL.

## Deprecated (v1): keys in OpenClaw config — do not use

v1 documented `skills.entries.cloud-backup.env.ACCESS_KEY_ID/SECRET_ACCESS_KEY`.
It still works in v2 with loud warnings and is removed in v3. Migration:
`references/credentials.md`.
