---
name: forge-obsidian-brain
description: CLI tool for managing an AI's Obsidian vault with note CRUD, bidirectional sync, capture commands, and intelligent resurface. Local-only — no network access. Triggers on brain commands, vault management, note capture, fuzzy search, regex search, case-insensitive search, resurface stale/topic, or Obsidian-related operations.
---

# ForgeObsidianBrain

Analytics and capture layer for an AI's Obsidian vault. Auto-discovers vaults, manages note CRUD operations, captures fleeting thoughts, resurfaces forgotten knowledge, with fuzzy matching, regex patterns, and case-insensitive search.

**Security Note:** See [SECURITY.md](SECURITY.md) for full security model. This skill operates entirely locally with no network access.

---

## Installation

```bash
# Clone or copy to your OpenClaw skills folder
cp -r skills/forge-obsidian-brain ~/.openclaw/workspace/skills/

# Make executable
chmod +x ~/.openclaw/workspace/skills/forge-obsidian-brain/scripts/brain.js

# Set up alias (optional)
alias brain="node ~/.openclaw/workspace/skills/forge-obsidian-brain/scripts/brain.js"
```

---

## Configuration

Set the default vault path via environment variable:

```bash
export OBSIDIAN_VAULT="$HOME/obsidian-vault"
```

Or specify `--vault <path>` for any command.

The skill auto-discovers vaults by:
1. Checking `OBSIDIAN_VAULT` environment variable
2. Reading Obsidian's config (`~/.config/obsidian/obsidian.json`)
3. Falling back to `~/obsidian-vault`

---

## Commands

### Core Commands

| Command | Description |
|---------|-------------|
| `discover` | Auto-detect vault location |
| `config` | Show Obsidian configuration |
| `init` | Create Brain folder structure |
| `sync` | Bidirectional sync with memory folder |

### Note CRUD

| Command | Usage |
|---------|-------|
| `read <path>` | Read a note |
| `create <path> [content]` | Create a new note |
| `update <path> [content]` | Update existing note |
| `delete <path>` | Delete a note |
| `list [folder]` | List notes in folder |
| `search <query>` | Search notes by content (case-insensitive by default) |
| `search <query> --fuzzy` | Fuzzy search (typo-tolerant) |
| `search <query> --regex` | Regex pattern search |
| `exists <path>` | Check if note exists |

### Capture Commands

Capture content to structured folders:

| Command | Description |
|---------|-------------|
| `capture thought <text>` | Quick thought → `Brain/Thoughts/` |
| `capture research --url <url> --title <title>` | Research ref → `Brain/Research/` |
| `capture conversation --source <src> --id <id>` | Chat log → `Brain/Conversations/` |

**Examples:**

```bash
# Fleeting thought
brain capture thought "I should refactor the auth module"

# Research capture
brain capture research \
  --url "https://martinfowler.com/articles/microservices.html" \
  --title "Microservices Guide" \
  --text "Key points about service boundaries"

# Conversation log
brain capture conversation \
  --source telegram \
  --id "12345" \
  --text "User asked about distributed systems"
```

### Resurface Commands

Find relevant or neglected notes:

| Command | Description |
|---------|-------------|
| `resurface topic <query>` | Fuzzy search with relevance scoring |
| `resurface stale --days <n>` | Find notes untouched in N days |

**Examples:**

```bash
# Find notes about microservices
brain resurface topic "microservices"

# Find all notes older than 30 days
brain resurface stale --days 30 --limit 20
```

---

## Options

| Flag | Description |
|------|-------------|
| `--vault <path>` | Override vault location |
| `--frontmatter '<json>'` | Add frontmatter to note |
| `--merge` | Merge instead of replace frontmatter |
| `--overwrite` | Allow overwriting existing notes |
| `--limit <n>` | Limit results (default: 5) |
| `--dry-run` | Preview sync without writing |
| `--days <n>` | Days threshold for stale search |
| `--fuzzy` | Use fuzzy matching for search |
| `--regex` | Use regex pattern for search |
| `--case-sensitive` | Force case-sensitive search |

---

## Workflow Examples

### Daily Brain Maintenance

```bash
# 1. Initialize structure (once)
brain init

# 2. Capture a thought
brain capture thought "Kubernetes selectors are just labels as queries"

# 3. Save research for later
brain capture research \
  --url "https://distcc.github.io/" \
  --title "Distributed Compilation"

# 4. Check for stale notes to review
brain resurface stale --days 14

# 5. Sync to memory folder
brain sync
```

### Search and Resurface

```bash
# Case-insensitive search (new default)
brain search "OpenClaw"

# Fuzzy search - matches "opneclaw" to "openclaw"
brain search "opneclaw" --fuzzy

# Regex search
brain search "^# .* Title" --regex

# Case-sensitive search
brain search "OpenClaw" --case-sensitive

# Resurface topic with fuzzy matching
brain resurface topic distributed --limit 10

# Output:
# {
#   "success": true,
#   "query": "distributed",
#   "totalMatches": 3,
#   "shown": 3,
#   "searchMode": "fuzzy",
#   "results": [
#     { "relativePath": "Brain/Research/...", "relevance": 5, "rank": 1, "matches": [...] },
#     ...
#   ]
# }
```

---

## Folder Structure

After `brain init`, your vault gets these folders:

```
vault/
├── Brain/
│   ├── Thoughts/          # Quick captures
│   ├── Research/          # URL references
│   ├── Conversations/     # Chat logs
│   ├── Entities/          # Structured data
│   └── Relations/         # Connections
└── .obsidian/
    └── ...
```

---

## Implementation Details

- **Vault Discovery**: Cross-platform (Linux, macOS, Windows)
- **Note Format**: Markdown with YAML frontmatter
- **Search**: Uses grep for fast content matching
- **Sync**: Bidirectional between `~/.openclaw/workspace/memory` and vault Inbox
- **IDs**: Base36 timestamps for collision-resistant filenames

---

## Security

This skill operates entirely on the local filesystem with **no network access**:

- **No external APIs** — No network requests are made
- **No data exfiltration** — All data stays on your machine
- **No arbitrary code execution** — `execSync` is used only for `grep` text search with strictly validated input
- **Plain source code** — No obfuscation, all JavaScript is readable

See [SECURITY.md](SECURITY.md) for complete security documentation including data access patterns, credentials, and execution details.

---

## Related

- [Obsidian](https://obsidian.md) - The knowledge base
- [OpenClaw](../README.md) - Parent project
