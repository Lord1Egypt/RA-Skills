# Credentials

Read this before backing up or restoring anything under `~/.ssh`, `~/.aws`,
`~/.config/gh`, or their kin.

Copying these is your job. Knowing what is in them is not.

## The handling rules

- **Copy, do not read.** `scripts/stage_copy.py` moves the bytes without ever
  putting a private key in your context. Never `cat`, `head`, `grep`, or
  `file` a credential file — not to check a key's type, not to count keys,
  not to confirm a file is what its name says.
- **Do not name files in conversation.** `~/.ssh` is a path.
  `~/.ssh/id_ed25519_acme_prod` names a key and an employer. Directory-level
  discussion is enough for every decision the user has to make.
  `test -d ~/.aws` is a fine existence check; `ls ~/.aws` is not necessary.
- **Ask before the backup, not after.** Step 2 of the backup is where the user
  decides whether their work AWS keys are going onto a file that will live on a
  USB stick. Name each credential directory on its own line and let them strike
  any of them. Do not fold them into a summary count.
- **Restore at `0600` / `0700`, and never overwrite.** Details below.
- **Never fabricate coverage.** If you did not check whether a directory
  exists, say so rather than assuming.

`stage_copy.py` keeps modes and symlinks on the way into staging. Credentials
get `--hash` and `--hash-prefix` like every other entry:

```sh
python3 scripts/stage_copy.py ~/.ssh staging/credentials/ssh \
    --hash --hash-prefix credentials/ssh
```

## Where they live

| Location | What it is | Holds a long-term secret? | Note for the user |
|---|---|---|---|
| `~/.ssh` | Private/public keys, `config`, `known_hosts` | Yes | The one nearly everybody wants. Modes matter — see below |
| `~/.gnupg` | GPG keyrings, trustdb, agent config | Yes | Carry the whole directory. Version-sensitive; see below |
| `~/.aws` | `config` and `credentials` | Yes with static access keys; no with SSO | If they use SSO, `aws sso login` on the new machine is cleaner than carrying anything |
| `~/.config/gh` | GitHub CLI hosts and OAuth token | Yes | Or just `gh auth login` again — it takes 20 seconds |
| `~/.config/gcloud` | gcloud config and credential DB | Yes, refresh tokens | Re-authenticating is usually quicker than debugging a stale token cache |
| `~/.azure` | Azure CLI profile and token cache | Yes | Token caches often need refreshing anyway |
| `~/.kube` | Cluster configs and contexts | Often — embedded tokens or client certs | Carry it, and expect some tokens to have expired |
| `~/.docker/config.json` | Registry auth | Yes | Or `docker login` again. Do not carry the rest of `~/.docker` |
| `~/.netrc` | Machine/password pairs, plaintext | Yes | Say "plaintext by design" out loud when proposing it |
| `~/.npmrc` | npm registry auth token | Yes | Small file, always worth carrying |
| `~/.pypirc` | PyPI upload credentials | Yes | Same |
| `~/.cargo/credentials.toml` | crates.io token | Yes | Carry the file; leave the rest of `~/.cargo` behind |
| `~/.m2/settings.xml` | Maven server passwords | Sometimes | Carry the file, not `~/.m2/repository` |
| `~/.gradle/gradle.properties` | Signing keys, repo passwords | Sometimes | Carry the file, not `~/.gradle/caches` |
| `~/.config/*/credentials`, `~/.config/*/config.json`, `~/.config/*/auth.json` | Assorted CLI tools — Fly, Railway, Supabase, Doppler, Vercel, Stripe, Cloudflare | Usually | Enumerate with `ls -d ~/.config/*/` and ask about the ones you recognise |
| `~/.config/op`, `~/.1password` | Password manager CLI state | Device-bound | Usually needs re-authorising on the new machine regardless |
| `~/.terraform.d/credentials.tfrc.json` | Terraform Cloud token | Yes | |
| `~/.claude` | Claude Code settings, skills — and, on Linux, `.credentials.json` | Yes, the token file | Settings and skills go in `files/`; the token file follows the rules on this page. On macOS the OAuth token is in the login Keychain instead and cannot travel |
| `~/.codex/auth.json`, `~/.gemini/oauth_creds.json`, `~/.qwen/oauth_creds.json`, `~/.local/share/opencode/auth.json` | AI coding agent logins | Yes | Every one of these agents has a login command; re-authenticating beats carrying the token. See `ai-agents.md` |
| `~/.claude.json`, `~/.codex/config.toml`, `~/.cursor/mcp.json`, `~/.gemini/config/mcp_config.json`, any repo `.mcp.json` | Agent config — **and MCP `env` blocks** | Whenever a server sets a key inline | A config file with an inline `env` key is a credential file, whatever its name. `scripts/agent_inventory.py` reports the key *names*; that is enough to classify it without reading the value |
| `~/.databrickscfg`, `~/.snowflake`, `~/.dbt/profiles.yml` | Data tooling | Yes | `profiles.yml` often has database passwords |

The table is a prompt for the conversation, not a boundary. If the user names
something that is not here, it travels on the same terms.

## What cannot travel in a file

Say so plainly and do not attempt a workaround.

- **macOS Keychain, Windows DPAPI, TPM-sealed secrets.** Bound to the machine
  or the login. Copying the store yields bytes that will not decrypt on the far
  side. Between two Macs, Apple's own Setup Assistant migrates the Keychain.
- **Hardware tokens.** A YubiKey or smartcard holds a key that cannot be
  exported by design. The user carries the device.
- **Agent sockets.** `SSH_AUTH_SOCK` and the GPG agent socket are live kernel
  objects, not files. Whatever is in them is not in the backup.
- **Biometric-gated secrets.** Touch ID-protected SSH keys, Secure
  Enclave-backed certificates. The key never left the machine and will not now.
- **Agent OAuth tokens in the macOS Keychain.** Claude Code stores its token
  there rather than in `~/.claude` on macOS; there is no file to carry. The
  new machine logs in again. Record it in the manifest entry's
  `machine_bound` so the restore says so instead of looking for a file that
  was never there.

## Restoring

### Modes

```sh
chmod 700 ~/.ssh ~/.gnupg ~/.aws ~/.config/gh
find ~/.ssh -type f -exec chmod 600 {} +
chmod 644 ~/.ssh/known_hosts ~/.ssh/config 2>/dev/null   # optional; 600 also works
```

`ssh` refuses to use a private key that is group- or world-readable, so `0600`
is not a precaution here — it is what makes the key usable. `0700` on the
directory is the same story.

These recipes sweep the whole directory, which also touches files the new
machine already owned (the ones you skipped rather than overwrote). For `~/.ssh`
and `~/.gnupg` that is what the tools demand anyway; still, say what the sweep
will re-mode before running it, and if the user has deliberately loosened
something, chmod only the files you actually restored instead.

`~/.gnupg` is stricter than the rest and needs its whole tree tightened:

```sh
chmod 700 ~/.gnupg
find ~/.gnupg -type d -exec chmod 700 {} +
find ~/.gnupg -type f -exec chmod 600 {} +
```

If `gpg` on the new machine is a different major version, run `gpg --list-keys`
once after restoring: it migrates the keyring format and will tell you if it
cannot.

### Never overwriting

If a file already exists at the target path, **skip it and record the skip**.
Do not merge, do not replace, do not rename the incoming one into place.

On any machine the user has already touched, expect skips: `ssh-keygen` may
have run during setup, `gh auth login` may have written a token,
`known_hosts` may already have entries. Every one of those is the new
machine's own state, and it is more current than the backup's.

Collect the skips and put them in the restore report as a list the user can
act on — "these five files were already here, so I left them alone" is
actionable; a silent skip is not.

### Afterwards

- `ls -la` each restored directory, and fix any mode that is not what it
  should be.
- `ssh-add ~/.ssh/id_ed25519` (or let the agent pick it up on first use). On
  macOS, `ssh-add --apple-use-keychain` if they used the Keychain before.
- `ssh -T git@github.com` is a quick end-to-end check that the restore worked
  before you start cloning repositories with it.
- Restore credentials **before** git repositories. Every SSH clone in the git
  step depends on this one having finished.
