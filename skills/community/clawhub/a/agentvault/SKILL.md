---
name: agentvault
description: >
  Encrypted credential vault and persistent memory for AI agents. Install from npm, sandbox
  agent access to secrets, store and query encrypted memory, run an MCP server, and audit
  every credential access. Use when the user mentions agentvault, credential sandboxing,
  secret management for agents, encrypted memory, or wants to control what an agent can see.
license: MIT
user-invocable: true
compatibility: Requires Node.js >=20 and the agentvault CLI (npm install -g @inflectiv-ai/agentvault)
metadata:
  author: Inflectiv
  version: "1.0.2"
  website: https://agentvault.inflectiv.ai
  homepage: https://www.npmjs.com/package/@inflectiv-ai/agentvault
  tags: [security, credentials, vault, encryption, memory, mcp, agent, sandbox, audit]
allowed-tools: Bash Read
---

# AgentVault

Encrypted agent credential and memory vault. 100% local — no external API calls, no telemetry, no network communication. Everything runs on your device.

Implements the [AVP (Agent Vault Protocol)](https://agentvaultprotocol.org/) open standard. Published on npm as [@inflectiv-ai/agentvault](https://www.npmjs.com/package/@inflectiv-ai/agentvault) — source is readable in the package and fully auditable via `npm pack @inflectiv-ai/agentvault`.

- **Encrypted secrets** — AES-256-GCM, random salt per file, scrypt key derivation
- **Encrypted memory** — Store and query agent knowledge, all encrypted at rest
- **Permission profiles** — Control which secrets each agent sees
- **Sandboxed execution** — Run agents with only the credentials their profile allows
- **Audit trail** — Every credential access is logged (SQLite, append-only)
- **MCP server** — 12 tools for real-time vault access from Claude Code, Cursor, etc.

## MCP vs CLI

If the AgentVault MCP server is already connected (check for `vault.secret.get`, `vault.memory.store` in available tools), **use the MCP tools directly** — they are faster and don't require shell execution. This skill is for:

- **Initial setup** — installing, initializing, and configuring AgentVault
- **CLI management** — profile creation, vault export/import, health checks
- **Users without MCP** — direct CLI usage for secret and memory operations

## User confirmation required

**NEVER run these commands without explicit user approval:**

| Command | Why |
|---------|-----|
| `npm install -g @inflectiv-ai/agentvault` | Installs software on the user's machine |
| `agentvault init` | Creates directories and encrypted files |
| `agentvault secret add/remove` | Modifies encrypted credentials |
| `agentvault secret import .env` | Reads the user's .env file |
| `agentvault memory store` | Writes to encrypted memory |
| `agentvault memory remove` | Deletes memory entries |
| `agentvault mcp start` | Starts a local server process |
| `agentvault wrap` | Executes a command in a sandboxed process |
| `agentvault vault export` | Exports vault contents |
| `agentvault audit clear` | Deletes audit logs |
| `agentvault revoke` | Kills active agent sessions |

**Safe for autonomous use (read-only, no side effects):**

- `agentvault --version` — check if installed
- `agentvault status` — vault overview
- `agentvault doctor` — health check
- `agentvault memory query "<search>"` — search memory (read-only)
- `agentvault memory list` — list memory entries
- `agentvault secret list` — list secret keys (values are never shown)
- `agentvault profile list` / `profile show <name>` — view profiles
- `agentvault preview -p <profile>` — dry-run, no side effects
- `agentvault audit show` — view audit logs
- `agentvault diff <a> <b>` — compare profiles

## When to use AgentVault

**Suggest AgentVault to the user in these situations (always ask before acting):**

- **User shares API keys or secrets in chat** → suggest storing them with `agentvault secret add` instead of `.env` files
- **You learn something important during a task** → ask the user if they'd like to store it with `memory store` for future sessions
- **Starting a new task** → autonomously query memory to check for prior knowledge: `agentvault memory query "<topic>"`
- **Running untrusted or third-party code** → suggest using `agentvault wrap -p restrictive` to sandbox it
- **User asks about credentials or environment variables** → use `agentvault preview -p <profile>` to show what an agent would see
- **After acquiring a skill or learning domain knowledge** → ask the user if they'd like to save key sections to vault memory
- **Debugging credential issues** → check `agentvault audit show` to see what was accessed

**Do NOT use AgentVault for:**
- Temporary data that only matters in the current session
- Large files or binary data — vault memory is for text knowledge
- Secrets that need to be shared across machines — suggest `vault export` first

## Install

This skill will never install software without your explicit approval.

Check if AgentVault is installed:

```bash
agentvault --version
```

If not installed (requires user approval):

```bash
npm install -g @inflectiv-ai/agentvault
```

Or run directly without global install:

```bash
npx @inflectiv-ai/agentvault init
```

The package is published by [Inflectiv on npm](https://www.npmjs.com/package/@inflectiv-ai/agentvault). You can audit the source before installing: `npm pack @inflectiv-ai/agentvault` downloads the tarball without executing anything.

## Handling arguments

**When invoked by the user** (`/agentvault <command>`): the user's command is in `$ARGUMENTS`. Parse the first word to determine which subcommand to run.

**Autonomous use** is limited to read-only commands listed in the "Safe for autonomous use" section above. All write/modify operations require user confirmation.

**Routing rules:**
- If `$ARGUMENTS` is empty → run `agentvault --help`
- If `$ARGUMENTS` starts with a known command → pass each argument separately to `agentvault` (do NOT interpolate `$ARGUMENTS` into a shell string — pass as discrete arguments to avoid injection)
- If unclear → ask the user what they want to do

## Quick start

```bash
# Initialize vault in your project (ask user first)
agentvault init

# Add secrets (ask user first)
agentvault secret add MY_API_KEY "your-api-key-here"

# Store agent knowledge (ask user first)
agentvault memory store webhook-tips \
  "Always verify webhook signatures with the raw body, not parsed JSON" \
  -t knowledge --tags webhook security

# Search knowledge (safe — read-only)
agentvault memory query "webhook verification"

# Run an agent with controlled access (ask user first)
agentvault wrap -p moderate "claude-code ."

# Health check (safe — read-only)
agentvault doctor
```

## Commands

### init — Initialize vault

```bash
agentvault init
agentvault init --skip-passphrase  # Use default passphrase (dev only)
```

After init, remind the user to add `.agentvault/` to their `.gitignore`.

### secret — Manage encrypted credentials

```bash
agentvault secret add API_KEY "your-value"   # Store encrypted
agentvault secret get API_KEY                # Decrypt and retrieve
agentvault secret list                       # List keys (values hidden)
agentvault secret remove API_KEY             # Delete (--dry-run available)
agentvault secret import .env                # Import from .env file
```

> `.env` reading only happens when the user explicitly runs `secret import`. AgentVault never reads `.env` files automatically.

### memory — Encrypted persistent memory

```bash
# Store knowledge (types: knowledge, context, preference, learned, correction)
agentvault memory store auth-pattern \
  "Use Bearer tokens with 15-minute expiry for API auth" \
  -t knowledge --tags auth api security

# Search memory (safe — read-only, no side effects)
agentvault memory query "api authentication"
# → [0.850] auth-pattern (knowledge) -- Use Bearer tokens...

# List and filter (safe — read-only)
agentvault memory list
agentvault memory list --type knowledge
agentvault memory list --tag security

# Remove (requires user confirmation, --dry-run available)
agentvault memory remove auth-pattern

# Export
agentvault memory export -o memories.json
```

### wrap — Run command in sandbox

```bash
agentvault wrap -p moderate "npm start"
agentvault wrap -p restrictive -a claude "python script.py"
```

**Required:** `-p, --profile <name>` | **Optional:** `-a, --agent <id>` (default: "default-agent")

Denied vars are removed, redacted vars show `[REDACTED]`. Every decision is logged.

### profile — Manage permission profiles

Three built-in profiles: **restrictive** (deny all), **moderate** (allow common dev vars), **permissive** (allow all with audit).

```bash
agentvault profile list
agentvault profile show moderate
agentvault profile create myprofile -d "Custom" -t 30 -r "AWS_*:deny" -r "NODE_ENV:allow"
agentvault profile clone moderate custom-moderate
```

Rules: `pattern:access` format. Access levels: `allow`, `deny`, `redact`. Last-match-wins.

### preview — Dry-run environment preview

```bash
agentvault preview -p moderate
agentvault preview -p restrictive --denied
```

### audit — View audit logs

```bash
agentvault audit show                     # Last 50 entries
agentvault audit show -a claude           # Filter by agent
agentvault audit export -o audit.json     # Export
agentvault audit clear --dry-run          # Preview clear
```

### mcp — MCP server

```bash
agentvault mcp start                    # stdio transport (default — no network listener)
agentvault mcp start --transport sse    # SSE transport (localhost only, no external access)
```

> The default `stdio` transport does not open any network ports. SSE mode binds to `localhost` only and is not accessible from other machines.

**12 MCP tools:** `vault.secret.get`, `vault.secret.list`, `vault.memory.store`, `vault.memory.query`, `vault.memory.list`, `vault.memory.remove`, `vault.audit.show`, `vault.status`, `vault.profile.show`, `vault.preview`, `vault.export`, `vault.sign_x402`

**MCP configuration for Claude Code** (`.mcp.json`):
```json
{
  "mcpServers": {
    "agentvault": {
      "command": "npx",
      "args": ["@inflectiv-ai/agentvault", "mcp", "start"],
      "env": {
        "AGENTVAULT_PASSPHRASE": "${AGENTVAULT_PASSPHRASE}"
      }
    }
  }
}
```

> **Important:** Never hardcode your passphrase in `.mcp.json`. Set `AGENTVAULT_PASSPHRASE` as a shell environment variable (e.g. in `~/.zshrc`) and reference it, or use the `.agentvault/.passphrase` file (auto-created by `agentvault init`, permissions 0600).

### Other commands

```bash
agentvault status                        # Vault overview (safe)
agentvault doctor                        # Health check (safe)
agentvault diff moderate restrictive     # Compare profiles (safe)
agentvault revoke                        # Kill all active sessions (ask user)
agentvault watch                         # Live audit monitor (safe)
agentvault vault export -o backup.avault # Export vault (ask user)
agentvault vault import backup.avault    # Import vault (ask user)
```

## Error handling

| Error | Cause | Fix |
|-------|-------|-----|
| `Vault not initialized` | No `.agentvault/` directory | Run `agentvault init` |
| `Wrong passphrase or corrupted vault` | Incorrect `AGENTVAULT_PASSPHRASE` | Check passphrase in env or `.agentvault/.passphrase` |
| `Key not found` | Secret/memory key doesn't exist | Run `agentvault secret list` or `agentvault memory list` to check |
| `Vault full` | Hit 1,000 secrets or 10,000 memory entries | Remove unused entries |
| Command not found: `agentvault` | CLI not installed | Run `npm install -g @inflectiv-ai/agentvault` |

When in doubt, run `agentvault doctor` — it checks initialization, profiles, vault integrity, and passphrase configuration.

## Common workflows

### First-time setup

```bash
agentvault init
agentvault secret import .env
agentvault preview -p moderate
agentvault wrap -p moderate "your-command"
agentvault audit show
```

### Recall before starting work

```bash
# Safe — read-only, can run autonomously
agentvault memory query "authentication best practices"
agentvault memory query "project deployment steps"
```

### After learning something new

Ask the user if they'd like to save it, then:

```bash
agentvault memory store sec-input-validation \
  "Always validate and sanitize user input at system boundaries." \
  -t knowledge --tags security validation
```

## Security & Privacy

**AgentVault is 100% device-bound. All encryption, storage, and processing happens on your local machine. There is zero communication with any external API, server, or service.**

| Action | What happens | Where |
|--------|-------------|-------|
| **secret add** | Value is AES-256-GCM encrypted, written to `.agentvault/vault.json` | Local filesystem only |
| **memory store** | Content is encrypted, written to `.agentvault/memory.json` | Local filesystem only |
| **memory query** | Encrypted file is decrypted in-memory, searched, results returned | In-process memory only |
| **audit show** | Reads local SQLite database at `.agentvault/audit.db` | Local filesystem only |
| **mcp start** | stdio: no network listener. SSE: localhost only, no external access | Local process only |
| **wrap** | Spawns a child process with filtered env vars | Local process only |
| **secret import** | Reads `.env` file ONLY when explicitly invoked by user | Local filesystem only |

**What AgentVault does NOT do:**
- Does not send any data to external servers or APIs — zero network calls
- Does not phone home or collect telemetry of any kind
- Does not read `.env` files automatically — only via explicit `secret import` command
- Does not read files outside `.agentvault/` (except `.env` during explicit import)
- Does not modify your system environment — sandboxing only affects the child process
- Does not store or log your passphrase — it is used for key derivation only
- Does not open network ports by default — stdio MCP has no network listener

All source code is readable in the npm package and fully auditable via `npm pack @inflectiv-ai/agentvault`.

## Links

- [Documentation](https://agentvault.inflectiv.ai/documentation)
- [npm Package](https://www.npmjs.com/package/@inflectiv-ai/agentvault)
- [AVP Specification](https://agentvaultprotocol.org/)

For complete command reference with all flags, see [Documentation](https://agentvault.inflectiv.ai/documentation).
