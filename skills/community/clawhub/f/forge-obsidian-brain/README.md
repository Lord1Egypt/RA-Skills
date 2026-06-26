# ForgeObsidianBrain

A local-first CLI tool for managing an AI's Obsidian vault. No network access. No external APIs. Just your notes, your way.

## What It Does

- **Auto-discovers** your Obsidian vault (or creates one)
- **Captures** thoughts, research URLs, and conversations
- **Syncs** bidirectionally between OpenClaw memory and your vault
- **Searches** with fuzzy matching, regex patterns, and case-insensitive matching
- **Resurfaces** stale and forgotten notes

## Quick Start

```bash
# Discover your vault
brain discover

# Initialize folder structure
brain init

# Capture a thought
brain capture thought "Kubernetes selectors are just labels as queries"

# Search with typo tolerance
brain search "kuberntes" --fuzzy

# Sync memory to vault
brain sync
```

## Security

**This skill operates entirely locally:**

- ✅ No network requests
- ✅ No external APIs
- ✅ No data upload or exfiltration
- ✅ Plain, readable JavaScript source code
- ✅ `grep` command execution with sanitized input only

See [SECURITY.md](SECURITY.md) for complete documentation.

## Commands

| Command | Description |
|---------|-------------|
| `discover` | Auto-detect vault location |
| `init` | Create Brain folder structure |
| `sync` | Bidirectional sync with memory |
| `capture thought <text>` | Quick thought capture |
| `capture research --url <url>` | Save research reference |
| `search <query>` | Case-insensitive search (default) |
| `search <query> --fuzzy` | Typo-tolerant fuzzy search |
| `search <query> --regex` | Regex pattern search |
| `resurface topic <query>` | Find relevant notes |
| `resurface stale --days <n>` | Find untouched notes |

## Installation

```bash
# Copy to OpenClaw skills folder
cp -r skills/forge-obsidian-brain ~/.openclaw/workspace/skills/

# Optional: Add alias to your shell profile
alias brain="node ~/.openclaw/workspace/skills/forge-obsidian-brain/scripts/brain.js"
```

## Requirements

- Node.js (built-in modules only — no npm install needed)
- `grep` command (standard on Linux/macOS/WSL)
- Obsidian vault (auto-created if missing)

## License

MIT — See LICENSE file
