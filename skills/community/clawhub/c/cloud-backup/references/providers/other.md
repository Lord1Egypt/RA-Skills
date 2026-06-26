# Other / Custom S3-Compatible Provider

Any storage service with an S3-compatible API works. You need three things:
a **private bucket**, the **S3 endpoint URL**, and a **key pair** — scoped to
the one bucket if your provider supports scoping (use it if so).

## 1. Finding the endpoint

Always a full URL. Common patterns:

- `https://s3.<region>.<provider>.com`
- `https://<account-id>.r2.cloudflarestorage.com`
- `https://<region>.digitaloceanspaces.com`
- `https://minio.your-server.com:9000`

Look for "S3 API endpoint" in your provider's compatibility docs.

## 2. Create a least-privilege key

Look for "API keys", "access keys", "S3 credentials", or "application keys"
in the console. If the provider supports key scoping, restrict to the backup
bucket with list/read/write/delete only.

## 3. Store the credentials (run this yourself — keep keys out of the chat)

```bash
aws configure --profile openclaw-backup
chmod 600 ~/.aws/credentials
```

## 4. Configure the skill (non-secret keys only)

```bash
openclaw config patch 'skills.entries.cloud-backup.config.bucket="my-bucket"'
openclaw config patch 'skills.entries.cloud-backup.config.endpoint="https://s3.your-provider.com"'
openclaw config patch 'skills.entries.cloud-backup.config.region="us-east-1"'
openclaw config patch 'skills.entries.cloud-backup.config.profile="openclaw-backup"'
```

If unsure about region, use `us-east-1` or `auto`.

## Credential safety (read me)

- This key can read, write, and DELETE your backups. Treat it like a password.
- Never commit it to git. Never store it in openclaw.json: **backups archive
  openclaw.json itself** — a key stored there rides along inside every archive
  it protects.
- Scope the key to this one bucket where the provider supports it. An
  account-wide key turns one leaked archive into an account takeover.
- Rotate every ~90 days and immediately on any suspicion: create new key →
  update the profile → verify a backup → revoke the old key.

## Verifying compatibility

The skill uses only basic operations: `aws s3 cp/ls/rm` plus a
`head-object` check. No presigned URLs, no bucket creation, no ACLs. If
`aws s3 ls s3://your-bucket/ --endpoint-url https://... --profile openclaw-backup`
works, you're good. (Custom object metadata is used for upload verification;
providers that drop it just skip the sha check, size is still verified.)

## Troubleshooting

- **`SignatureDoesNotMatch`** — region/endpoint mismatch; try `region=auto`.
- **SSL errors** — self-signed certs: `AWS_CA_BUNDLE=/path/to/ca.pem`.
- **Connection refused** — include the port in the endpoint.
- **Bucket-name DNS errors** — set `AWS_S3_FORCE_PATH_STYLE=true` in the env.

## Deprecated (v1): keys in OpenClaw config — do not use

v1 documented `skills.entries.cloud-backup.env.ACCESS_KEY_ID/SECRET_ACCESS_KEY`.
It still works in v2 with loud warnings and is removed in v3. Migration:
`references/credentials.md`.
