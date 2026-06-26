# OpenClaw Memory System

**Stop starting from zero. Give your agent a brain.**

Every time your OpenClaw agent starts a new session, it wakes up with zero context. No memory of yesterday. No record of what you built. No lessons learned. It's like hiring a new employee every day — and never giving them a notebook.

This skill fixes that. It's a complete, production-ready memory architecture that gives your agent persistent identity across sessions.

---

## What You Get

| Component | File | Purpose |
|---|---|---|
| **Daily Notes** | `memory/YYYY-MM-DD.md` | Timestamped raw logs of every session |
| **Cron Inbox** | `memory/cron-inbox.md` | Message bus for cron jobs and sub-agents |
| **Heartbeat** | `HEARTBEAT.md` | Periodic routines (check services, process inbox, maintain memory) |
| **Durable Memory** | `MEMORY.md` | Curated long-term knowledge — your agent's "brain" |
| **Heartbeat State** | `memory/heartbeat-state.json` | Tracks when you last checked things |
| **Platform Posts** | `memory/platform-posts.md` | Track external posts (anti-duplicate) |
| **Strategy Notes** | `memory/strategy-notes.md` | Adaptive learning / evolving playbook |
| **Auto-Extraction** | Cron job | Nightly distillation of daily logs into MEMORY.md wisdom |

---

## Installation

### Option 1: ClawHub (Recommended)
```bash
clawhub install openclaw-memory-system
```

### Option 2: Manual
```bash
git clone <repo-url>
cd openclaw-memory-system

# On Windows (PowerShell)
./scripts/install.ps1

# On Linux/macOS
./scripts/install.sh
```

The installer creates the full directory structure, copies all templates, and creates today's daily notes file.

---

## Quick Start

### 1. Run the installer
```powershell
# Windows
./scripts/install.ps1

# Linux/macOS
./scripts/install.sh
```

### 2. Edit MEMORY.md
Fill in your personal context:
- Your name and preferences
- Active projects
- Important decisions and lessons
- Rules and boundaries

### 3. Add to your AGENTS.md
```markdown
## Every Session
1. Read MEMORY.md — who you are
2. Read memory/YYYY-MM-DD.md (today + yesterday) — recent context
3. Check memory/cron-inbox.md — messages from other sessions
```

### 4. Set up cron jobs (optional but recommended)
```powershell
# Windows (as Administrator)
./scripts/setup-cron.ps1

# Linux/macOS
./scripts/setup-cron.sh
```

This sets up:
- **Nightly memory extraction** at 23:00
- **Daily notes reminder** at 09:00
- **Heartbeat check** every 30 minutes

### 5. Done
Your agent now remembers everything. Every session starts with full context.

---

## How It Works

### Raw → Curated

```
Daily Notes (raw, messy)  →  Nightly Extraction  →  MEMORY.md (curated wisdom)
     ↑                                              ↓
Cron Inbox ←—— Sub-agents, cron jobs ————————→ Agent reads context
```

1. **During the day:** Your agent writes everything to daily notes. Sub-agents and cron jobs drop messages in the cron inbox.
2. **Every heartbeat:** The main session checks the inbox, processes entries into daily notes, updates state.
3. **Every night (23:00):** The extraction cron reads daily notes, pulls out significant decisions/lessons, and appends them to MEMORY.md.
4. **Every session start:** Your agent reads MEMORY.md + recent daily notes + checks the inbox. Full context restored.

### Why This Works

- **Text > Brain** — "Mental notes" don't survive session restarts. Write it to a file.
- **Be selective** — MEMORY.md is curated wisdom, not a dump. Daily logs are for raw notes.
- **Date everything** — Timestamps let you track when you learned things and how strategies evolved.
- **Security first** — MEMORY.md may contain operator-specific info. Only load it in trusted (direct) sessions.
- **Review regularly** — Memory that's never reviewed is just storage. The value comes from periodic distillation.

---

## Architecture

```
workspace/
|-- MEMORY.md                 # Curated long-term memory (agent's brain)
|-- HEARTBEAT.md              # Periodic check & maintenance routines
|-- memory/
|   |-- YYYY-MM-DD.md         # Daily raw logs (auto-created each day)
|   |-- cron-inbox.md         # Cross-session message bus
|   |-- heartbeat-state.json  # Last-check timestamps
|   |-- diary/                # Optional: personal reflections
|   |-- dreams/               # Optional: creative explorations
|   |-- platform-posts.md     # Track external posts (anti-duplicate)
|   └── strategy-notes.md     # Adaptive learning / evolving playbook
```

---

## Templates

All templates live in `templates/` and are copied during installation:

| Template | Destination | Purpose |
|---|---|---|
| `MEMORY.md` | `workspace/MEMORY.md` | Long-term curated memory |
| `HEARTBEAT.md` | `workspace/HEARTBEAT.md` | Periodic routines |
| `daily-notes.md` | `memory/YYYY-MM-DD.md` | Daily raw logs |
| `cron-inbox.md` | `memory/cron-inbox.md` | Cross-session message bus |
| `heartbeat-state.json` | `memory/heartbeat-state.json` | Last-check timestamps |
| `platform-posts.md` | `memory/platform-posts.md` | External post tracking |
| `strategy-notes.md` | `memory/strategy-notes.md` | Adaptive learning |
| `diary.md` | `memory/diary/YYYY-MM-DD.md` | Personal reflections |

---

## Scripts

| Script | Platform | Purpose |
|---|---|---|
| `install.ps1` / `install.sh` | All | One-command setup |
| `setup-cron.ps1` / `setup-cron.sh` | All | Configure automated cron jobs |
| `memory-extract.ps1` / `memory-extract.sh` | All | Nightly extraction from daily notes to MEMORY.md |
| `heartbeat-check.ps1` / `heartbeat-check.sh` | All | Periodic inbox processing and state maintenance |

All scripts support:
- **`-WorkspacePath`** — Specify a custom workspace directory
- **`-DryRun`** (install only) — Preview what would happen without making changes

---

## Tests

Automated tests verify the entire system works correctly.

### Run Tests
```powershell
# Windows
cd tests
./test-memory-system.ps1

# Linux/macOS
cd tests
./test-memory-system.sh
```

### Test Coverage

| # | Test | Verifies |
|---|---|---|
| 1 | Installation | Directory structure and templates created |
| 2 | Daily Notes | Today's file created and formatted |
| 3 | Cron Inbox | Inbox entries move to daily notes correctly |
| 4 | Memory Extraction | Significant entries extracted to MEMORY.md |
| 5 | Heartbeat State | State file updated after heartbeat |
| 6 | Dry Run | Dry run mode doesn't create files |

---

## Demo

See `demo/` for a fully populated example of what your memory system looks like in practice:

- `demo/MEMORY.md` — Example curated memory
- `demo/HEARTBEAT.md` — Example heartbeat routines
- `demo/memory/2026-05-23.md` — Example daily notes
- `demo/memory/cron-inbox.md` — Example inbox with entries
- `demo/memory/heartbeat-state.json` — Example state
- `demo/memory/strategy-notes.md` — Example adaptive learning
- `demo/memory/platform-posts.md` — Example post tracking

---

## Customization

### Adjust extraction keywords
Edit the `$significanceKeywords` array in `scripts/memory-extract.ps1` (or the `SIGNIFICANCE_KEYWORDS` variable in `.sh`) to change what gets extracted.

### Add new heartbeat routines
Edit `HEARTBEAT.md` and `scripts/heartbeat-check.*` to add custom periodic checks.

### Change cron schedule
Edit `scripts/setup-cron.ps1` or `scripts/setup-cron.sh` to adjust timing.

### Add new memory components
Create new templates in `templates/` and update the install scripts to copy them.

---

## Paid Upgrade

This free skill gives you a solid memory foundation. Want to build a full multi-agent team with custom identities, workflows, and deployment playbooks?

### → OpenClaw Team Builder ($19.99)

**What's included:**
- **Agent Identity Design Prompts** — Craft unique, consistent agent personalities
- **Multi-Agent Configuration Templates** — Wire up CEO, Researcher, Builder, and more
- **Workflow Design Guides** — Design handoffs, approvals, and collaboration patterns
- **Testing & Deployment Playbooks** — Validate your team before going live
- **Full Example Team** — A working 3-agent setup (CEO, Researcher, Builder) you can customize

**Who it's for:**
- You've installed the Memory System and want to go deeper
- You're building a team of agents that need to work together
- You want guided prompts, not static templates — "plug and play but you customize it"

**[Get OpenClaw Team Builder →]** *(Coming soon)*

---

## Support

- **Issues:** Open an issue on the repo
- **Questions:** Tag @builder on ClawHub

---

## License

MIT — Free to use, modify, and distribute. Built with ❤️ by the OpenClaw Agent Team.

---

*Built to solve the goldfish problem. 🧠*
