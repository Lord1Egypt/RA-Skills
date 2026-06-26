# agent-config-sync v1.5

**Keep configuration consistent across multiple OpenClaw agents** — zero-touch setup, interactive wizard, version tracking, and automatic sync dispatch.

[![Version](https://img.shields.io/badge/version-1.5.0-blue)](_meta.json)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-enabled-green)](https://openclaw.ai)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Bash](https://img.shields.io/badge/pure-bash-orange)](scripts/)

---

## 🎯 What It Does

When you run 2+ OpenClaw agents, keeping their configurations in sync is painful. `agent-config-sync` automates this:

```
Master Agent detects change
        │
        ▼
  Reads CHANGELOG.md
        │
        ▼
  Generates sync manifest
        │
        ├─→ Agent 1: pending_sync_v3.1_a1b2c3.md
        ├─→ Agent 2: pending_sync_v3.1_a1b2c3.md
        └─→ Agent 3: pending_sync_v3.1_a1b2c3.md
                │
                ▼
       Agents apply → verify → cleanup
```

**Syncs**: System code · Agent configs (SOUL/IDENTITY/TOOLS) · OpenClaw config · Task configs · API keys

---

## ⚡ Quick Start (30 seconds)

```bash
# 1. Install
clawhub install agent-config-sync

# 2. Run wizard (interactive, auto-detects everything)
cd ~/.openclaw/skills/agent-config-sync
bash scripts/wizard.sh

# 3. Done! 🎉
#    All agents now have sync infrastructure.
#    Changes are auto-dispatched on next Master heartbeat.
```

**Prefer non-interactive?**
```bash
bash scripts/wizard.sh --auto     # Zero prompts
bash scripts/init_sync.sh --auto  # Even faster
```

---

## ✨ Features

| Feature | Description |
|:--------|:------------|
| 🧙 **Interactive Wizard** | 5-step guided setup with auto-detection — no manual file editing |
| 🤖 **--auto Mode** | One-command setup that detects workspaces, generates registry, and initializes everything |
| 📊 **Version Tracking** | Sentinel files (`.current_system_version`, `.last_sync_version`) for monotonic versioning |
| 🔄 **Auto Dispatch** | Master HEARTBEAT detects version mismatch → dispatches to all agents via `sessions_send` or file fallback |
| 📝 **CHANGELOG-driven** | Structured `CHANGELOG.md` — read only latest section, not entire history |
| 🗄️ **Two-Phase Commit** | `.sync_journal.jsonl` ensures atomicity — PREPARE → DISPATCH → COMMIT |
| 🔍 **Offline Catch-Up** | Agents that miss sync cycles get cumulative catch-up packages |
| 🛡️ **Rollback** | Pre-sync snapshots + SHA256 verification for safe rollbacks |
| 🔒 **Dispatch Lock** | Prevents concurrent sync dispatch (< 2min window) |
| 🔁 **Loop Detection** | 3+ consecutive same-version → block and alert |
| 📦 **Batch Mode** | Merges rapid consecutive changes into single dispatch |
| 🏝️ **Self-Upgrade Isolation** | agent-config-sync's own files use isolated upgrade flow |
| 🌐 **Bilingual** | Full Chinese + English output (`--lang en|zh`) |
| 🎭 **Demo Mode** | `--demo` creates a full temp deployment for learning |
| 🔐 **Path Validation** | Only writes to `~/.openclaw/workspace-*` — no external access |

---

## 📋 Requirements

- **OpenClaw** running with 2+ agents
- One designated "master" coordination agent
- `clawhub` CLI installed
- Bash 4.0+ (no Python/Perl required)

---

## 🏗️ Architecture

```
skills/agent-config-sync/
├── SKILL.md                    # Full documentation
├── SECURITY.md                 # Security model & permissions
├── README.md                   # This file
├── _meta.json                  # Package metadata
├── scripts/
│   ├── wizard.sh               # 🆕 Interactive setup wizard (v1.5)
│   ├── init_sync.sh            # Infrastructure initialization
│   ├── force_sync.sh           # Trigger immediate sync detection
│   └── revert_sync.sh          # Version rollback trigger
├── references/
│   ├── agent-registry.json     # Single source of truth (agent IDs, paths)
│   ├── sync-setup.md           # HEARTBEAT item 12 + CHANGELOG spec
│   ├── sync-journal.md         # Two-phase commit mechanism
│   ├── pending-sync-template.md # Sync file template
│   └── quickstart.md           # Quickstart for new users
└── reports/
    └── ...                     # Evaluation reports & repair logs
```

---

## 🚀 Usage

### Daily Operations

```bash
# Record a change (master agent)
echo "v1.1" > ~/.openclaw/workspace-amaster/memory/.current_system_version

# Or use the force_sync helper
bash scripts/force_sync.sh --confirm ~/.openclaw/workspace-amaster/memory v1.0 v1.1
```

### Check Status

```bash
# Master version
cat ~/.openclaw/workspace-amaster/memory/.current_system_version
cat ~/.openclaw/workspace-amaster/memory/.last_sync_version

# Pending syncs on an agent
ls ~/.openclaw/workspace-acode/pending_sync_*.md
```

### Rollback

```bash
bash scripts/revert_sync.sh --dry-run ~/.openclaw/workspace-amaster/memory v1.0
bash scripts/revert_sync.sh --confirm ~/.openclaw/workspace-amaster/memory v1.0
```

### Demo / Learning

```bash
bash scripts/init_sync.sh --demo --lang en
```

---

## ⚙️ Configuration

The wizard auto-generates `references/agent-registry.json`. To customize manually:

```json
{
  "vars": {
    "workspace_root": "~/.openclaw",
    "master_agent": "amaster"
  },
  "agents": {
    "acode": { "name": "Coding Agent", "role": "Development", "workspace": "..." },
    "ainvest": { "name": "Investment Agent", "role": "Finance", "workspace": "..." }
  }
}
```

---

## 🔒 Security

All scripts enforce:
- `--confirm` required for writes (use `--dry-run` first)
- Path whitelist: only `~/.openclaw/workspace-*` allowed
- Cross-agent isolation: each agent accesses only its own workspace
- Atomic writes: `tempfile → sync → mv` (no partial sentinel files)
- No network, no API calls, no credential access

Full details: [SECURITY.md](SECURITY.md)

---

## 🌐 Internationalization

```bash
# English output
bash scripts/wizard.sh --lang en
bash scripts/init_sync.sh --lang en

# Chinese output (default)
bash scripts/wizard.sh --lang zh
```

---

## 📄 License

MIT

---

## 🙋 FAQ

**Q: How is this different from just copying files?**
A: It's event-driven (version mismatch → dispatch), journaled (two-phase commit), and handles edge cases (offline agents, conflicts, rollbacks).

**Q: Do I need to run this on every agent?**
A: No. Only the Master agent dispatches. Other agents receive `pending_sync_*.md` files and check for them on startup/heartbeat (automatically set up by `init_sync.sh`).

**Q: What if an agent is offline?**
A: The Master writes a `pending_sync_<VERSION>.md` file to the agent's workspace. On next startup, the agent detects and applies it. If multiple versions piled up, version collapse jumps to the latest.

**Q: Can I use this without `clawhub`?**
A: Yes — just clone or copy the skill directory to `~/.openclaw/skills/agent-config-sync/` and run `scripts/wizard.sh`.
