# Credentials — where each secret lives, and why

This skill needs up to three secrets: an S3 access key id, an S3 secret key,
and a GPG passphrase. **None of them belong in openclaw.json.** Backups
archive that file — a credential stored there rides along inside every
archive it protects.

The recommended setup is two chmod-600 files:

| Secret | Home | How |
|---|---|---|
| S3 key pair | AWS named profile (`~/.aws/credentials`) | `aws configure --profile openclaw-backup && chmod 600 ~/.aws/credentials`, then set `config.profile` |
| GPG passphrase | passphrase file | `umask 077 && openssl rand -base64 32 > ~/.openclaw/credentials/cloud-backup.passphrase`, then set `config.passphraseFile` |

## Resolution order (what the script actually does)

**S3 credentials** (highest first):

1. Process env `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` /
   `AWS_SESSION_TOKEN` — operator-injected (systemd `EnvironmentFile=`,
   gateway environment). Never overridden.
2. **OpenClaw secret refs** — `config.accessKeyRef` + `config.secretKeyRef`
   (+ optional `config.sessionTokenRef`). See "Using the OpenClaw secret
   store" below. A configured-but-unresolvable ref aborts the run (exit 13) —
   never a silent fallthrough to a weaker tier.
3. `config.profile` → named profile in `~/.aws/credentials` (mode 600).
   **Recommended simple default.** The skill passes `--profile`; the aws CLI
   reads its own standard store. The secret never touches OpenClaw config or
   this chat — and `~/.aws` is OUTSIDE the backup scope, so the key never
   travels inside the archives it protects.
4. DEPRECATED: `skills.entries.cloud-backup.env.ACCESS_KEY_ID` /
   `.SECRET_ACCESS_KEY` / `.SESSION_TOKEN` plaintext in openclaw.json.
   Still works in v2; warns loudly on every run; removed in v3.

**GPG passphrase** (highest first):

1. Process env `GPG_PASSPHRASE` — operator-injected.
2. Process env `CLOUD_BACKUP_GPG_PASSPHRASE` — injected by OpenClaw from
   `skills.entries.cloud-backup.apiKey` (which may itself be a SecretRef).
   Resolves only inside the OpenClaw agent runtime, so a bare-shell
   `cloud-backup.sh backup` won't see it — prefer `passphraseRef` below.
3. **OpenClaw secret ref** — `config.passphraseRef` (below). Works from any
   shell; aborts with exit 14 if configured but unresolvable.
4. `config.passphraseFile` — path to a mode-600 file. **Recommended simple
   default.** The script refuses world-readable files and warns on group
   access. The passphrase is passed to gpg over a file descriptor — never on
   a command line (v1 leaked it into `ps`/`/proc/*/cmdline`).
5. DEPRECATED: `skills.entries.cloud-backup.env.GPG_PASSPHRASE` plaintext in
   openclaw.json. Warns on every run; removed in v3.

`status` always prints where each secret resolved from — check it whenever
you are unsure which tier is active.

## Using the OpenClaw secret store (config.*Ref)

If you already run OpenClaw's secret system (`openclaw secrets configure`,
`.secrets.providers` in openclaw.json), the skill hooks straight into it —
one credential model for the whole instance, 1Password-style backends
included. The `*Ref` keys accept the same shapes OpenClaw uses everywhere:
a SecretRef object `{source, provider, id}` or a `$NAME` / `${NAME}` env
template.

```json
{ "skills": { "entries": { "cloud-backup": { "config": {
  "accessKeyRef":  { "source": "file", "provider": "default", "id": "/cloudBackup/accessKeyId" },
  "secretKeyRef":  { "source": "file", "provider": "default", "id": "/cloudBackup/secretAccessKey" },
  "passphraseRef": { "source": "file", "provider": "default", "id": "/cloudBackup/gpgPassphrase" }
} } } } }
```

Supported sources (resolved with the gateway's own semantics):

- **file** — provider `{source: "file", path, mode: "json"|"singleValue"}`;
  in json mode (the default) `id` is a JSON pointer into the chmod-600 store
  file, e.g. `/cloudBackup/gpgPassphrase`.
- **env** — `id` is the environment variable name.
- **exec** — provider `{source: "exec", command, args?, jsonOnly?}`; the
  skill speaks the protocolVersion-1 contract (request object on stdin,
  `values` map on stdout), so the same resolver you use for the gateway —
  e.g. a 1Password `op read` wrapper — works unchanged. Plugin-integration
  exec providers resolve only inside the gateway and are rejected with a
  clear error.

Notes:

- Configured refs that fail to resolve abort instead of falling back;
  `status` shows `UNRESOLVABLE` with the reason.
- Archive-scope trade-off: a file-provider store under `~/.openclaw` travels
  inside every (encrypted) archive; an AWS profile never travels at all.
  Both are fine — just know which you picked.
- A literal secret string in a `*Ref` key technically works but is plaintext
  in config — the sensitivity verdict will flag it. Use a real ref.

## Generating a passphrase

```bash
umask 077
mkdir -p ~/.openclaw/credentials
openssl rand -base64 32 > ~/.openclaw/credentials/cloud-backup.passphrase
openclaw config patch 'skills.entries.cloud-backup.config.passphraseFile="~/.openclaw/credentials/cloud-backup.passphrase"'
```

**Immediately store a copy in your password manager.** Without the
passphrase, encrypted backups are unrecoverable — that is the point of them.
If you ever rotate it, keep the old one labeled with its date range: older
archives still need it until they age out of retention.

## Migrating from v1 (plaintext in openclaw.json)

```bash
# 1. S3 keys → profile (run yourself; do not paste keys into agent chat)
aws configure --profile openclaw-backup
chmod 600 ~/.aws/credentials
openclaw config patch 'skills.entries.cloud-backup.config.profile="openclaw-backup"'

# 2. Passphrase → file (see above). If you keep the SAME passphrase, just move
#    it; if you pick a new one, save BOTH in your password manager.

# 3. Remove the plaintext block, then verify
openclaw config patch 'skills.entries.cloud-backup.env=null'
jq '.skills.entries["cloud-backup"]' ~/.openclaw/openclaw.json   # no "env" block
bash scripts/cloud-backup.sh status                              # no DEPRECATED warnings
```

Consider the old key exposed (it lived in config, which earlier backups
archived): rotate it at the provider after the new chain is verified.
