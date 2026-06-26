---
name: bitwarden-credential
description: Store or retrieve credentials in Bitwarden via CLI. Use when asked to save, store, or add a password/API key/OAuth token/secret/credential to Bitwarden. Triggered by phrases like "save to bitwarden", "store credential", "add api key to bitwarden", "save password", or when given a name/username/password triplet to persist. Requires user to have run `bw unlock` first and provide BW_SESSION env var.
metadata:
  openclaw:
    homepage: https://bitwarden.com
---

# Bitwarden Credential Skill

Store credentials (passwords, API keys, OAuth tokens, etc.) in Bitwarden via the CLI.

## Workflow

### Step 1: Ensure Vault is Unlocked

The user must unlock their Bitwarden vault **once per session** in their terminal:

```bash
bw unlock
```

After unlocking, the user gets a session key. There are two ways to provide it:

**Option A — Export the session (user does in their terminal):**
```bash
export BW_SESSION="<session-key-from-unlock>"
```
Then just tell me "unlocked" and I can run commands directly.

**Option B — Pass session directly to script:**
```bash
BW_SESSION="<session-key>" ./bitwarden-credential.sh <name> <username> <password> [notes]
```

### Step 2: Store a Credential

Once vault is unlocked, provide me with:
- **Name** — identifier for this credential (e.g., "GitHub API Key", "MiniMax API")
- **Username** — often the client_id or key name
- **Password/Secret** — the actual secret value
- **Notes** *(optional)* — extra context (scope, grant_type, etc.)

Example user message:
> "Save to Bitwarden: name=Grafana, username=admin, password=xyz123, notes=prod server"

### Step 3: Execute

Use the bundled script or run directly:

```bash
# With BW_SESSION set
./scripts/bitwarden-credential.sh "<name>" "<username>" "<password>" "[notes]"

# Or via bw CLI directly
echo -n '{"name":"...","login":{"username":"...","password":"..."},"type":1}' | bw create item
```

## Notes

- **Bitwarden CLI must be installed**: `brew install bitwarden-cli`
- **API key auth**: Use `bw login --apikey` with client_id + client_secret, but vault still requires master password to unlock
- **I cannot unlock the vault for you** — the master password never leaves your terminal
- Session token (`BW_SESSION`) is session-scoped; it expires when the vault locks again
