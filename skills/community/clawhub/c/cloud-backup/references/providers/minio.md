# MinIO

## 1. Create a private bucket

1. MinIO Console → **Buckets** → **Create Bucket**
2. Set access to **Private**

## 2. Create a least-privilege key

Never use the admin credentials (`minioadmin`) for backups.

1. MinIO Console → **Access Keys** → **Create Access Key**
2. Attach a policy restricted to the one bucket:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    { "Effect": "Allow", "Action": ["s3:ListBucket"],
      "Resource": "arn:aws:s3:::YOUR_BUCKET" },
    { "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:PutObject", "s3:DeleteObject"],
      "Resource": "arn:aws:s3:::YOUR_BUCKET/*" }
  ]
}
```

## 3. Store the credentials (run this yourself — keep keys out of the chat)

```bash
aws configure --profile openclaw-backup
chmod 600 ~/.aws/credentials
```

## 4. Configure the skill (non-secret keys only)

```bash
openclaw config patch 'skills.entries.cloud-backup.config.bucket="my-backup-bucket"'
openclaw config patch 'skills.entries.cloud-backup.config.region="us-east-1"'
openclaw config patch 'skills.entries.cloud-backup.config.endpoint="https://minio.example.com:9000"'
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

- Region can be anything; `us-east-1` is conventional.
- Self-signed TLS: set `AWS_CA_BUNDLE=/path/to/ca.pem` in the environment.
- Non-standard port goes in the endpoint URL.

## Deprecated (v1): keys in OpenClaw config — do not use

v1 documented `skills.entries.cloud-backup.env.ACCESS_KEY_ID/SECRET_ACCESS_KEY`.
It still works in v2 with loud warnings and is removed in v3. Migration:
`references/credentials.md`.
