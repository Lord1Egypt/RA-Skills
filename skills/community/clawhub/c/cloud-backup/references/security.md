# Security — threat model, restore safety, incident response

## Threat model (what the encryption is for)

Archive encryption protects your backups **at rest in the bucket and in
leak scenarios**: bucket compromise, provider insiders, a mislaid archive
file. It does **not** protect against host compromise — anyone with a shell
on your host already reads `~/.openclaw` directly.

That asymmetry drives the credential policy:

- Host-side secrets in mode-600 files (`~/.aws/credentials`, the passphrase
  file) are acceptable: they add no exposure beyond the host itself.
- Secrets inside `openclaw.json` are NOT acceptable: **this skill archives
  that file.** A credential stored there is replicated into every backup it
  protects — exposure multiplied by retention count × destinations. This is
  why v2 deprecates `skills.entries.cloud-backup.env.*` and why the docs
  never suggest it.

## Enforcement in the script (v2)

- **Sensitivity verdict**: before every backup, the script detects whether
  the archive scope contains real secret material (file-provider secret
  stores, `credentials/`, legacy auth files, plaintext values in
  openclaw.json). If it does, encryption is **forced** — plaintext output for
  that scope fails with exit 14. `config.excludeSecrets=true` excludes the
  detected stores instead (restores from such archives need secrets
  re-provisioned — pair with an encrypted `backup settings`).
- **No durable plaintext**: archives are produced inside a per-run mode-700
  staging directory that is removed on any exit (and swept on the next run
  after a hard kill). v1 could leave unencrypted tarballs behind when a step
  failed; v2 cannot.
- **No passphrase on command lines**: gpg receives the passphrase over a file
  descriptor. v1 passed `--passphrase <value>` on argv, visible in
  `ps`/`/proc/*/cmdline` for the duration of every run.
- **Verified uploads**: sha256 sidecars, decrypt-and-list verification after
  encryption, and a HEAD check (size + sha metadata) after upload.

## Credential rules

- Least-privilege, **bucket-scoped** keys (see the provider guides). Never
  account-wide or root keys.
- Storage: AWS named profile or operator-managed process env for S3; a
  mode-600 passphrase file or OpenClaw SecretRef for GPG. Details and
  resolution order: `references/credentials.md`.
- Never commit credentials to git. `~/.openclaw/openclaw.json` should be
  mode 600 regardless.
- Rotate keys every ~90 days and immediately on any suspicion.

## Restore safety

1. Always `restore --dry-run` first — lists contents without extracting.
2. Checksums are verified before anything else; decryption before listing.
3. Tar member paths are validated — absolute paths and `..` traversal are
   rejected before extraction.
4. Restores are **staged by default** (a fresh mode-700 directory, with
   printed next steps). `--in-place` overwrites live state and requires an
   interactive typed confirmation, or `--yes --force` for automation.
5. Cross-host caution: native archives record their original state dir; an
   in-place restore onto a host with a different state dir is refused — go
   through `--target`.

## Troubleshooting

- **`Unable to locate credentials`** — no profile/env configured. Set
  `config.profile` (recommended) — see `references/credentials.md`.
- **`AccessDenied`** — the key lacks `ListBucket` / `GetObject` / `PutObject`
  / `DeleteObject` on the target bucket.
- **`SignatureDoesNotMatch`** — region/endpoint mismatch (check provider
  guide), or system clock skew.
- **`Could not connect to the endpoint URL`** — AWS: leave `endpoint` unset;
  every other provider: `endpoint` is required.
- **Checksum mismatch on restore** — re-download; if persistent, treat the
  remote object as corrupted and restore an older set.
- **exit 14** — the scope contains secret material and no passphrase is
  configured. Set `config.passphraseFile`; do not bypass.

## Incident response (key suspected leaked)

Rotate-first, revoke-last — never leave a window with zero working backups:

1. Create a NEW bucket-scoped key in the provider console (old key stays
   valid for now).
2. Update the AWS profile (`aws configure --profile openclaw-backup`).
3. Run `backup full` + `verify --latest` to prove the new chain works.
4. Audit recent bucket activity for unexpected reads/writes/deletes.
5. Revoke the OLD key.
6. If the key ever lived in openclaw.json: archives made during that period
   contain it. Prune them (`prune`, plus manual `aws s3 rm` for anything
   outside retention) or treat the data they protect as exposed.
7. If the passphrase leaked: pick a new one, keep the old labeled by date
   range (old archives still need it), and re-create current backups under
   the new passphrase.
