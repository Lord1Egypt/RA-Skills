# DashPass CLI Command Reference

All commands follow the pattern:

```bash
node dashpass-cli.mjs <command> [options]
```

**Global options:**

| Option | Description |
|--------|-------------|
| `--identity-id <id>` | Override `DASHPASS_IDENTITY_ID` env var for this invocation |

---

## `put` — Store a Credential

Encrypts a value and stores it on the Dash blockchain.

**Syntax:**

```bash
echo "<secret>" | node dashpass-cli.mjs put \
  --service <service-name> \
  --type <credential-type> \
  --level <security-level> \
  --label "<description>" \
  --value-stdin \
  [--expires-in <duration>]
```

**Parameters:**

| Parameter | Required | Description |
|-----------|:--------:|-------------|
| `--service` | Yes | Unique name for this credential (e.g., `anthropic-api`, `github-deploy`). Used as the lookup key. Max 63 characters. |
| `--type` | Yes | Credential type. One of: `api-key`, `oauth-token`, `ssh-key`, `wif`, `db-cred`, `tls-cert`, `service-token`, `encryption-key` |
| `--level` | Yes | Security level. One of: `critical` (highest), `sensitive`, `normal` |
| `--label` | Yes | Human-readable description. Max 63 characters. |
| `--value-stdin` | Recommended | Read the secret value from stdin (pipe it in). Prevents the value from appearing in shell history. |
| `--value` | Alternative | Pass the value directly (WARNING: visible in shell history and `ps` output). |
| `--expires-in` | No | Set an expiry. Format: `30m`, `12h`, `7d`, `90d`. Omit for no expiry. |

**Examples:**

```bash
# Store an API key (recommended: pipe via stdin)
echo "sk-ant-api03-xxxxx" | node dashpass-cli.mjs put \
  --service anthropic-api \
  --type api-key \
  --level sensitive \
  --label "Anthropic production key" \
  --value-stdin

# Store an OAuth token that expires in 90 days
echo "gho_xxxxxxxxxxxx" | node dashpass-cli.mjs put \
  --service github-oauth \
  --type oauth-token \
  --level sensitive \
  --label "GitHub OAuth token" \
  --value-stdin \
  --expires-in 90d

# Store a database password
echo "s3cur3p4ss" | node dashpass-cli.mjs put \
  --service postgres-prod \
  --type db-cred \
  --level critical \
  --label "PostgreSQL production password" \
  --value-stdin
```

---

## `get` — Retrieve a Credential

Fetches a credential from the blockchain and decrypts it locally.

**Syntax:**

```bash
node dashpass-cli.mjs get --service <service-name> [--json] [--pipe]
```

**Parameters:**

| Parameter | Required | Description |
|-----------|:--------:|-------------|
| `--service` | Yes | The service name used when storing the credential. |
| `--json` | No | Output as formatted JSON (includes metadata). |
| `--pipe` | No | Output only the raw value, no formatting, no newline. Ideal for `$(...)` substitution in scripts. |

**Examples:**

```bash
# Human-readable output (default)
node dashpass-cli.mjs get --service anthropic-api

# Pipe-friendly — use in scripts
API_KEY=$(node dashpass-cli.mjs get --service anthropic-api --pipe)
echo "Got key: ${API_KEY:0:10}..."

# JSON output — for programmatic consumption
node dashpass-cli.mjs get --service anthropic-api --json
```

**JSON output format:**

```json
{
  "id": "7Hk9xYz...",
  "service": "anthropic-api",
  "label": "Anthropic production key",
  "credType": "api-key",
  "level": "sensitive",
  "status": "active",
  "version": 1,
  "expiresAt": 0,
  "decrypted": {
    "value": "sk-ant-api03-xxxxx"
  }
}
```

**Behavior notes:**
- If the credential exists in the local cache (less than 5 minutes old), the cached copy is used (faster).
- If multiple versions exist (after rotation), the latest version is returned.
- Exit code `1` if the credential is not found.

---

## `list` — List All Credentials

Shows a table of all your credentials (metadata only, not decrypted values).

**Syntax:**

```bash
node dashpass-cli.mjs list [--type <type>] [--level <level>]
```

**Parameters:**

| Parameter | Required | Description |
|-----------|:--------:|-------------|
| `--type` | No | Filter by credential type (e.g., `api-key`, `ssh-key`). |
| `--level` | No | Filter by security level (e.g., `critical`). |

If neither filter is given, lists all `active` credentials.

**Examples:**

```bash
# List everything
node dashpass-cli.mjs list

# Only API keys
node dashpass-cli.mjs list --type api-key

# Only critical credentials
node dashpass-cli.mjs list --level critical
```

**Example output:**

```
Found 5 credential(s):

SERVICE                  TYPE           LEVEL       VER  STATUS    LABEL
--------------------------------------------------------------------------------
anthropic-api            api-key        sensitive   3    active    Anthropic production key
github-deploy            ssh-key        critical    1    active    GitHub deploy key
postgres-prod            db-cred        critical    1    active    PostgreSQL production
slack-webhook            service-token  normal      1    active    Slack notification webhook
xai-api                  api-key        sensitive   2    active    xAI Grok API key
```

---

## `rotate` — Rotate a Credential

Stores a new value for an existing credential, incrementing the version number. The old version remains on-chain (archived) and the new version becomes the active one returned by `get`.

**Syntax:**

```bash
echo "<new-secret>" | node dashpass-cli.mjs rotate \
  --service <service-name> \
  --value-stdin
```

**Parameters:**

| Parameter | Required | Description |
|-----------|:--------:|-------------|
| `--service` | Yes | The service name of the credential to rotate. |
| `--value-stdin` | Recommended | Read the new value from stdin. |
| `--new-value` | Alternative | Pass the new value directly (WARNING: visible in shell history). |

**Example:**

```bash
# Rotate the Anthropic API key to a new value
echo "sk-ant-api03-NEW-KEY-HERE" | node dashpass-cli.mjs rotate \
  --service anthropic-api \
  --value-stdin
```

**Expected output:**

```
[rotate] Current version: 1, doc: 7Hk9x...
[rotate] Creating new version: 2
[rotate] OK
  New Document ID: 9Abc3...
  Version: 2
  Previous: 7Hk9x...
```

**Behavior notes:**
- The old version document stays on-chain (for audit purposes).
- `get` always returns the highest version number.
- The local cache is invalidated after rotation.

---

## `check` — Check for Expiring Credentials

Scans your credentials and reports any that are expired or about to expire.

**Syntax:**

```bash
node dashpass-cli.mjs check --expiring-within <duration>
```

**Parameters:**

| Parameter | Required | Description |
|-----------|:--------:|-------------|
| `--expiring-within` | Yes | Time window to check. Format: `30m`, `12h`, `7d`. |

**Example:**

```bash
# Check for anything expiring within the next 7 days
node dashpass-cli.mjs check --expiring-within 7d
```

**Example output:**

```
[check] Window: 7d (until 2026-04-14T00:00:00.000Z)
[check] Total active: 5
[check] Already expired: 0
[check] Expiring within window: 1

EXPIRING SOON:
  - github-oauth (expires 2026-04-12T15:30:00.000Z, 5d 3h left)
```

---

## `status` — Vault Status

Shows your vault configuration, credit balance, and credential count.

**Syntax:**

```bash
node dashpass-cli.mjs status
```

**No parameters.** Just run it.

**Example output:**

```
[status] DashPass Vault v2
  Contract: ATamKoznYgWsQGP6JBpmVuFGiqAXTVWdjpeSGeEVSikq
  Identity: 36SxvpAKXeBJByUdJ364Hnhp2NfVDe6Gkj7xtTRZj6hh
  Balance:  965669809292 credits
  Doc types: credential, accessLog
  Active credentials: 5
[status] OK
```

> **How do I know if I have enough credits?** A balance above 100,000,000 is plenty for normal use. If your balance is below 10,000,000, consider topping up.

---

## `delete` — Delete a Credential

Permanently removes a credential (all versions) from the blockchain.

**Syntax:**

```bash
node dashpass-cli.mjs delete --service <service-name>
```

**Parameters:**

| Parameter | Required | Description |
|-----------|:--------:|-------------|
| `--service` | Yes | The service name of the credential to delete. |

**Example:**

```bash
node dashpass-cli.mjs delete --service old-unused-service
```

**Expected output:**

```
[delete] Found 3 document(s) for service="old-unused-service"
[delete] Deleting document 7Hk9x...
[delete] Deleted: 7Hk9x...
[delete] Deleting document 9Abc3...
[delete] Deleted: 9Abc3...
[delete] Deleting document Bdef5...
[delete] Deleted: Bdef5...
[delete] OK — removed 3 document(s)
```

**Warning:** Deletion is permanent. All versions of the credential are removed from the blockchain. There is no undo.

---

## `env` — Export Credentials as Environment Variables

Fetches one or more credentials and outputs `export VAR="value"` lines, suitable for `eval $(...)`.

**Syntax:**

```bash
eval $(node dashpass-cli.mjs env --services <svc1,svc2,...> [--prefix <pfx>] [--null-if-missing])
```

**Parameters:**

| Parameter | Required | Description |
|-----------|:--------:|-------------|
| `--services` | Yes | Comma-separated list of service names to fetch. |
| `--prefix` | No | Prefix to prepend to all env var names. |
| `--null-if-missing` | No | Output `unset VAR` for missing services instead of a warning. |

**Built-in service → env var mappings:**

| Service | Env Var |
|---------|---------|
| `anthropic-api` | `ANTHROPIC_API_KEY` |
| `xai-api` | `XAI_API_KEY` |
| `openai-api` | `OPENAI_API_KEY` |
| `brave-search-api` | `BRAVE_API_KEY` |
| `github-token` | `GITHUB_TOKEN` |
| `slack-token` | `SLACK_TOKEN` |
| `discord-token` | `DISCORD_TOKEN` |
| `aws-access-key` | `AWS_ACCESS_KEY_ID` |
| `aws-secret-key` | `AWS_SECRET_ACCESS_KEY` |
| `database-url` | `DATABASE_URL` |
| `redis-url` | `REDIS_URL` |

Unknown services are mapped to uppercase with hyphens replaced by underscores.

**Examples:**

```bash
# Single service
eval $(node dashpass-cli.mjs env --services anthropic-api)
echo $ANTHROPIC_API_KEY

# Multiple services at once
eval $(node dashpass-cli.mjs env --services anthropic-api,brave-search-api,xai-api)

# With prefix
eval $(node dashpass-cli.mjs env --services anthropic-api --prefix DASHPASS_)
# Sets DASHPASS_ANTHROPIC_API_KEY
```

---

## Environment Variables Reference

| Variable | Required | Description | Example |
|----------|:--------:|-------------|---------|
| `CRITICAL_WIF` | **Yes** | Your private key in WIF format. Used to encrypt/decrypt all credentials. This is the master key — if you lose it, you lose access to all stored credentials. | `cVt4o7BGAig1UX...` (testnet WIF starts with `c`) |
| `DASHPASS_IDENTITY_ID` | **Yes** | Your Dash Platform Identity ID (base58). Determines which identity signs transactions and which credentials you can access. | `36SxvpAKXeBJByUdJ364Hnhp2NfVDe6Gkj7xtTRZj6hh` |
| `DASHPASS_CONTRACT_ID` | No | The Data Contract ID to use. Defaults to the shared testnet contract `GCeh2gnvtiHrujq37ZcKnhZ64xpzDC1LMCLhrUJzKDQF`. Set this if you deploy your own contract. | `ATamKoznYgWsQGP6JBpmVuFGiqAXTVWdjpeSGeEVSikq` |
| `DASHPASS_CACHE` | No | Set to `none` to disable local caching entirely. Every `get` will fetch directly from the blockchain. Default: caching enabled. | `none` |

### Setting Variables Persistently

Add these to your shell profile (`~/.bashrc`, `~/.zshrc`, or equivalent):

```bash
# DashPass configuration
export CRITICAL_WIF="your-wif-here"
export DASHPASS_IDENTITY_ID="your-identity-id-here"
# export DASHPASS_CONTRACT_ID="your-contract-id"  # uncomment if using own contract
```

Then reload: `source ~/.bashrc`

> **Security tip:** Never commit these values to git. Add them to `.gitignore` if they're in a file. Consider using a dedicated `.env` file that's excluded from version control, or a secrets manager for the WIF itself.

---

## Credential Types

| Type | Use For | Examples |
|------|---------|---------|
| `api-key` | API authentication keys | Anthropic, OpenAI, xAI, Brave Search keys |
| `oauth-token` | OAuth access/refresh tokens | GitHub, Google, Slack tokens |
| `ssh-key` | SSH private keys | VPS access keys, Git deploy keys |
| `wif` | Blockchain private keys | Dash WIFs, other cryptocurrency keys |
| `db-cred` | Database credentials | PostgreSQL, Redis, MongoDB passwords |
| `tls-cert` | TLS/SSL certificates | Server certs, client certs |
| `service-token` | Generic service tokens | Webhook secrets, internal auth tokens |
| `encryption-key` | Encryption passphrases | Backup encryption keys, SEED passphrases |

## Security Levels

| Level | Meaning | When to Use |
|-------|---------|-------------|
| `critical` | Highest protection. Compromise = severe damage. | Mainnet private keys, primary API keys, database root passwords |
| `sensitive` | Standard protection. Compromise = moderate impact. | Most API keys, OAuth tokens, deploy keys |
| `normal` | Basic encryption. Compromise = low impact. | Webhook secrets, non-sensitive tokens, test credentials |
