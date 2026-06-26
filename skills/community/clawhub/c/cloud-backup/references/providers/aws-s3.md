# AWS S3

## 1. Create a private bucket

1. AWS Console → S3 → **Create bucket**
2. Keep **Block Public Access** enabled (all four checkboxes)
3. Enable **Bucket Versioning** (recommended — protects against overwrites)
4. Use **SSE-S3** encryption (default, free)

## 2. Create a least-privilege key

Create a dedicated IAM user with programmatic access. Never use root keys.
Attach this policy (replace `YOUR_BUCKET`):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    { "Sid": "ListBucket", "Effect": "Allow",
      "Action": ["s3:ListBucket"], "Resource": "arn:aws:s3:::YOUR_BUCKET" },
    { "Sid": "ObjectAccess", "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:PutObject", "s3:DeleteObject"],
      "Resource": "arn:aws:s3:::YOUR_BUCKET/*" }
  ]
}
```

IAM → Users → Create user → attach policy → Create access key.

## 3. Store the credentials (run this yourself — keep keys out of the chat)

```bash
aws configure --profile openclaw-backup
chmod 600 ~/.aws/credentials
```

On EC2/ECS, prefer an instance/task role and skip stored keys entirely.

## 4. Configure the skill (non-secret keys only)

```bash
openclaw config patch 'skills.entries.cloud-backup.config.bucket="YOUR_BUCKET"'
openclaw config patch 'skills.entries.cloud-backup.config.region="us-east-1"'
openclaw config patch 'skills.entries.cloud-backup.config.profile="openclaw-backup"'
```

**No `endpoint`** — AWS S3 is the one provider where it stays unset.

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

- Common regions: `us-east-1`, `us-west-2`, `eu-west-1`, `eu-central-1`.
- If using S3 Object Lock or Glacier, extend the IAM policy accordingly.

## Deprecated (v1): keys in OpenClaw config — do not use

v1 documented `skills.entries.cloud-backup.env.ACCESS_KEY_ID/SECRET_ACCESS_KEY`.
It still works in v2 with loud warnings and is removed in v3. Migration:
`references/credentials.md`.
