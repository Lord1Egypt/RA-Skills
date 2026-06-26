# AgentVault Command Reference

Complete reference for all AgentVault CLI commands, flags, and options.

## Global

```
agentvault [command] [options]
```

Install: `npm install -g @inflectiv-ai/agentvault`
Version: 1.0.1

---

## init

Initialize AgentVault in the current project. Creates `.agentvault/` directory with default profiles, encrypted vault, and audit database.

```
agentvault init [options]
```

| Flag | Description |
|------|-------------|
| `--skip-passphrase` | Skip passphrase prompt and use default (development only) |

**Default profiles created:**
- `restrictive` — Denies all non-system vars
- `moderate` — Allows common dev vars, denies cloud credentials
- `permissive` — Allows most vars, redacts known secrets

---

## wrap

Run a command inside a sandboxed environment. Filters environment variables based on the selected profile.

```
agentvault wrap -p <profile> [options] "<command>"
```

| Flag | Description | Required |
|------|-------------|----------|
| `-p, --profile <name>` | Permission profile to use | Yes |
| `-a, --agent <id>` | Agent identifier for audit trail | No (default: "default-agent") |

**Behavior:**
1. Loads the specified profile
2. Evaluates every environment variable against profile rules
3. Builds a filtered environment (allowed vars pass through, denied vars removed, redacted vars show `[REDACTED]`)
4. Logs every access decision to audit trail
5. Spawns child process with filtered environment
6. On exit: revokes the session

---

## secret

Manage secrets in the AES-256-GCM encrypted vault.

### secret list

```
agentvault secret list
```

### secret add

```
agentvault secret add <key> <value>
```

### secret get

```
agentvault secret get <key>
```

### secret remove

```
agentvault secret remove <key>
agentvault secret remove <key> --dry-run
```

### secret rename

```
agentvault secret rename <oldKey> <newKey>
```

### secret import

```
agentvault secret import <file>
```

Import secrets from a `.env` file. Each `KEY=VALUE` line becomes a vault entry.

---

## memory

Manage encrypted persistent memory.

### memory store

```
agentvault memory store <key> "<content>" [options]
```

| Flag | Description | Default |
|------|-------------|---------|
| `-t, --type <type>` | Memory type | `knowledge` |
| `--tags <tags...>` | Searchable tags | None |
| `--confidence <n>` | Confidence score 0.0-1.0 | `0.8` |
| `--ttl <hours>` | Time-to-live in hours | None (no expiry) |
| `--source <source>` | Source identifier | None |

**Memory types:** `knowledge`, `context`, `preference`, `learned`, `correction`

### memory query

```
agentvault memory query "<search terms>" [options]
```

| Flag | Description | Default |
|------|-------------|---------|
| `-n, --limit <n>` | Max results | `10` |
| `--min-score <n>` | Minimum score threshold | `0.1` |

### memory list

```
agentvault memory list [options]
```

| Flag | Description |
|------|-------------|
| `--type <type>` | Filter by memory type |
| `--tag <tag>` | Filter by tag |

### memory remove

```
agentvault memory remove <key> [options]
```

| Flag | Description |
|------|-------------|
| `--dry-run` | Preview removal without deleting |

### memory export

```
agentvault memory export -o <file>
```

---

## profile

Manage permission profiles.

### profile list

```
agentvault profile list
```

### profile show

```
agentvault profile show <name>
```

### profile create

```
agentvault profile create <name> [options]
```

| Flag | Description | Default |
|------|-------------|---------|
| `-d, --description <desc>` | Profile description | `""` |
| `-t, --trust <level>` | Trust level 0-100 | `50` |
| `--ttl <seconds>` | Token TTL in seconds | `3600` |
| `-r, --rule <rules...>` | Rules as `"pattern:access"` | None |

### profile delete

```
agentvault profile delete <name>
```

### profile clone

```
agentvault profile clone <from> <to>
```

---

## preview

Preview what environment variables an agent would see under a given profile.

```
agentvault preview -p <profile> [options]
```

| Flag | Description | Required |
|------|-------------|----------|
| `-p, --profile <name>` | Permission profile to use | Yes |
| `--allowed` | Show only allowed variables | No |
| `--redacted` | Show only redacted variables | No |
| `--denied` | Show only denied variables | No |

---

## audit

### audit show

```
agentvault audit show [options]
```

| Flag | Description | Default |
|------|-------------|---------|
| `-s, --session <id>` | Filter by session ID | All sessions |
| `-a, --agent <id>` | Filter by agent ID | All agents |
| `-n, --limit <n>` | Number of entries to show | 50 |

### audit export

```
agentvault audit export [options]
```

| Flag | Description | Default |
|------|-------------|---------|
| `-o, --output <file>` | Output file path | Required |
| `-f, --format <format>` | Output format: `json` or `csv` | `json` |

### audit clear

```
agentvault audit clear
agentvault audit clear --dry-run
```

---

## mcp

### mcp start

```
agentvault mcp start [options]
```

| Flag | Description | Default |
|------|-------------|---------|
| `--transport <type>` | Transport: `stdio` or `sse` | `stdio` |
| `--port <n>` | Port for SSE transport | `3100` |

**12 MCP tools:** `vault.secret.get`, `vault.secret.list`, `vault.memory.store`, `vault.memory.query`, `vault.memory.list`, `vault.memory.remove`, `vault.audit.show`, `vault.status`, `vault.profile.show`, `vault.preview`, `vault.export`, `vault.sign_x402`

---

## vault

### vault export

```
agentvault vault export -o <file> [options]
```

| Flag | Description |
|------|-------------|
| `-o, --output <file>` | Output .avault file path |
| `--decrypted` | Export as plaintext JSON |
| `--confirm-plaintext` | Required with --decrypted |

### vault import

```
agentvault vault import <file>
```

---

## status

```
agentvault status
```

---

## doctor

```
agentvault doctor
```

---

## diff

```
agentvault diff <profileA> <profileB>
```

---

## revoke

```
agentvault revoke [options]
```

| Flag | Description |
|------|-------------|
| `-s, --session <id>` | Revoke specific session (optional) |

---

## watch

```
agentvault watch [options]
```

| Flag | Description | Default |
|------|-------------|---------|
| `-i, --interval <ms>` | Poll interval in milliseconds | `1000` |

---

## wallet (optional — requires ethers)

```
agentvault wallet init              # Generate new wallet
agentvault wallet show              # Show wallet address
agentvault wallet import <key>      # Import existing private key
```

---

## Profile Rule Semantics

- **Last-match-wins**: Rules are evaluated in order; the last matching rule determines access
- **System vars bypass**: `PATH`, `HOME`, `SHELL`, `USER`, `LANG`, `TERM`, `TMPDIR`, `LOGNAME`, `EDITOR`, `VISUAL`, `DISPLAY`, `XDG_*` always pass through
- **Pattern types**:
  - `"*"` — Match all variables
  - `"AWS_*"` — Prefix glob
  - `"NODE_ENV"` — Exact match
- **Access levels**:
  - `allow` — Variable passes through unchanged
  - `deny` — Variable is removed from the environment
  - `redact` — Variable is set to `[REDACTED]`
