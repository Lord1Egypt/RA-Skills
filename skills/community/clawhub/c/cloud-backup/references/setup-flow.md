# First-time setup — guided flow (for the agent)

Principles: the user understands every consequence before it happens; secrets
never transit the conversation; every config write is shown verbatim and
confirmed first; nothing is scheduled without an explicit opt-in.

## Step 0 — Preflight

Run `setup`. It prints the checklist, current config, dependency status, and
(if cloud is configured) a connection test. It never writes anything.

## Step 1 — Provider

Ask which provider: AWS S3, Cloudflare R2, Backblaze B2, DigitalOcean Spaces,
MinIO, or another S3-compatible service. Read the matching
`references/providers/<provider>.md`.

## Step 2 — Bucket + least-privilege key

Echo the provider guide's bucket and key steps. The user performs them in the
provider console: private bucket, then a key scoped to that one bucket (where
the provider supports scoping).

## Step 3 — Credential home

Offer exactly two options (never a third):

1. **AWS profile (recommended)** — the user runs, themselves:
   ```bash
   aws configure --profile openclaw-backup
   chmod 600 ~/.aws/credentials
   ```
   The key never appears in this chat.
2. **Process env** — for operators who manage gateway env (systemd
   `EnvironmentFile=`): `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY`.

Plaintext in openclaw.json is not offered. If the user asks for it, explain
the amplifier (backups archive the config) and point to
`references/credentials.md`.

## Step 4 — Config write (GATE)

Show every patch verbatim, wait for an explicit yes, then run:

```bash
openclaw config patch 'skills.entries.cloud-backup.config.bucket="<bucket>"'
openclaw config patch 'skills.entries.cloud-backup.config.endpoint="<endpoint>"'   # non-AWS only
openclaw config patch 'skills.entries.cloud-backup.config.region="<region>"'
openclaw config patch 'skills.entries.cloud-backup.config.profile="openclaw-backup"'
```

## Step 5 — Connection test

Run `setup` again (or `status`) and confirm "Connected / Reachable ✓".

## Step 6 — Encryption (GATE on the config writes)

Tell the user:

> "Backups of this scope contain your OpenClaw config, credential store, and
> agent databases, so encryption is required. Generate a strong passphrase
> into a 600-mode file (run it yourself), then store a copy in your password
> manager — without it, backups are unrecoverable:"

```bash
umask 077 && mkdir -p ~/.openclaw/credentials
openssl rand -base64 32 > ~/.openclaw/credentials/cloud-backup.passphrase
```

Then (after confirmation) set:

```bash
openclaw config patch 'skills.entries.cloud-backup.config.passphraseFile="~/.openclaw/credentials/cloud-backup.passphrase"'
```

(`config.encrypt` already defaults to true in v2.) Advanced alternative —
SecretRef via `apiKey`: see `references/credentials.md`.

## Step 7 — First backup (GATE)

1. Run `backup full --dry-run`; show the user the scope, excludes, sensitivity
   verdict, and destination.
2. On yes: run `backup full`, then `verify --latest`.
3. Report: archive name, size, encrypted ✓, uploaded ✓, verified ✓.

## Step 8 — Scheduling offer (only now, only once)

Per SKILL.md "Scheduling — strictly opt-in": offer once, show the exact
`openclaw cron add` command from `schedule`, and create nothing without an
explicit yes. "No" is a complete answer — do not re-offer.
