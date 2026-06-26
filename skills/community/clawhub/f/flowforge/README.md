# FlowForge

```
  ███████╗██╗      ██████╗ ██╗    ██╗
  ██╔════╝██║     ██╔═══██╗██║    ██║
  █████╗  ██║     ██║   ██║██║ █╗ ██║
  ██╔══╝  ██║     ██║   ██║██║███╗██║
  ██║     ███████╗╚██████╔╝╚███╔███╔╝
  ╚═╝     ╚══════╝ ╚═════╝  ╚══╝╚══╝
       ███████╗ ██████╗ ██████╗  ██████╗ ███████╗
       ██╔════╝██╔═══██╗██╔══██╗██╔════╝ ██╔════╝
       █████╗  ██║   ██║██████╔╝██║  ███╗█████╗
       ██╔══╝  ██║   ██║██╔══██╗██║   ██║██╔══╝
       ██║     ╚██████╔╝██║  ██║╚██████╔╝███████╗
       ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝
```

> *Spec it. Plan it. Build it. Ship it.*

**FlowForge** is an autonomous AI coding pipeline for [OpenClaw](https://github.com/openclaw/openclaw). Drop in a GitHub issue or task description — FlowForge breaks it into a structured implementation plan and executes every subtask via Claude Code, automatically rotating across multiple Claude Max subscriptions so you never hit a rate limit.

---

## 🎯 The Problem

Claude Code is the best coding agent available — but it has rate limits. One account runs out, your agent stops. And without a structured plan, even a fresh Claude Code session wastes tokens re-discovering the codebase before writing a single line.

**Without FlowForge:**
```
  You → Claude Code → hits rate limit → ❌ stopped
         ↑
    (re-discovers codebase every session, no structured plan)
```

**With FlowForge:**
```
  You → FlowForge → Spec → Plan → Code → QA → ✅ shipped
                      ↑      ↑      ↑      ↑
                  Claude  Claude  Claude  Claude
                  Code 1  Code 1  Code 2  Code 3
                              (auto-rotates on rate limit)
```

---

## 🔄 How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                        FLOWFORGE PIPELINE                        │
└─────────────────────────────────────────────────────────────────┘

  GitHub Issue / Task Description
          │
          ▼
  ┌───────────────┐
  │  SPEC AGENT   │  Claude Code — High Thinking
  │               │  → spec.md
  │  • Overview   │    Full feature specification
  │  • Scope      │    Acceptance criteria
  │  • Files      │    Verification commands
  └───────┬───────┘
          │
          ▼
  ┌───────────────┐
  │  PLAN AGENT   │  Claude Code — High Thinking
  │               │  → implementation_plan.json
  │  • Investigate│    Phases with dependencies
  │  • Classify   │    Subtasks with file targets
  │  • Decompose  │    Verification per subtask
  └───────┬───────┘
          │
          ▼
  ┌───────────────────────────────────────┐
  │           CODER AGENT LOOP            │  Claude Code — Medium Thinking
  │                                       │
  │  For each subtask:                    │
  │  ┌──────────────────────────────┐     │
  │  │ Read pattern files           │     │
  │  │ Write code changes           │     │
  │  │ Run verification command     │──┐  │
  │  │ Pass? → mark complete, next  │  │  │
  │  │ Fail? → fix, retry (3x max)  │◄─┘  │
  │  └──────────────────────────────┘     │
  │                                       │
  │  Rate limit? → auto-rotate account ↓  │
  └───────┬───────────────────────────────┘
          │
          ▼
  ┌───────────────┐
  │   QA AGENT    │  Claude Code — High Thinking
  │               │  → qa_report.md
  │  • Score spec │    Pass/fail per criterion
  │  • Run tests  │    Gaps with fix guidance
  │  • Verdict    │    Ship / needs work / retry
  └───────┬───────┘
          │
          ▼
      📬 Report delivered via OpenClaw → Telegram
```

---

## ⚡ Account Rotation

FlowForge rotates across multiple Claude Max subscriptions automatically. When one account hits its rate limit, the pipeline switches credentials and continues — no manual intervention needed.

```
┌──────────────────────────────────────────────────┐
│              ACCOUNT ROTATION                     │
│                                                   │
│  Account 1 ████████████████████░  rate limit hit  │
│     ↓ auto-switch                                 │
│  Account 2 ░░░░░░░░░░░░░░░░░░░░░  fresh → go      │
│     ↓ if also limited                             │
│  Account 3 ░░░░░░░░░░░░░░░░░░░░░  fresh → go      │
│                                                   │
│  All limited? → wait for earliest reset ⏳        │
└──────────────────────────────────────────────────┘
```

Add as many Claude Max accounts as you have. FlowForge cycles through them in order, storing credentials at `~/.claude/accounts/<email>.json`.

---

## 🗂 Workflow Types

FlowForge classifies every task before planning — each type produces a different phase structure:

| Type | When to Use | Phase Structure |
|------|-------------|----------------|
| `feature` | New capability | Backend → Worker → Frontend → Integration |
| `refactor` | Restructure existing code | Add New → Migrate → Remove Old → Cleanup |
| `investigation` | Bug hunt | Reproduce → Investigate → Fix (blocked) → Harden |
| `migration` | Move data or infrastructure | Prepare → Test → Execute → Cleanup |
| `simple` | Single-file or small change | Subtasks only, no phases |

---

## 🚀 Quick Start

### 1. Install

FlowForge is an OpenClaw skill. Add it to your workspace:

```bash
# Clone into your OpenClaw skills directory
git clone https://github.com/windseeker1111/FlowForge ~/clawd/skills/flowforge
```

### 2. Save your Claude Code accounts

```bash
mkdir -p ~/.claude/accounts

# For each Claude Max account, authenticate and save credentials:
claude auth login   # sign in with account 1
cp ~/.claude/.credentials.json ~/.claude/accounts/you@example.com.json

claude auth login   # sign in with account 2
cp ~/.claude/.credentials.json ~/.claude/accounts/you2@example.com.json
```

### 3. Run a task

```bash
# From a GitHub issue
gh issue view 42 --repo owner/repo --json title,body | \
  jq -r '"# " + .title + "\n\n" + .body' > /tmp/task.md

bash ~/clawd/skills/flowforge/scripts/init_forge.sh "$(cat /tmp/task.md)" ~/Dev/my-repo
bash ~/clawd/skills/flowforge/scripts/run_forge.sh ~/.forge/<timestamp>/
```

Or just tell OpenClaw:

> *"FlowForge issue #42 in owner/my-repo"*

---

## 📁 Output

Every forge run creates a timestamped workspace at `~/.forge/<timestamp>/`:

```
~/.forge/20260222_143201/
├── task.md                    # Input task
├── spec.md                    # Generated specification
├── implementation_plan.json   # Phases + subtasks with status
├── implementation_plan_done.json  # Updated after coding
├── qa_report.md               # Final QA score and verdict
└── progress.log               # Timestamped execution log
```

---

## 🏗 Architecture

```
flowforge/
├── SKILL.md                        # OpenClaw skill definition
├── scripts/
│   ├── init_forge.sh               # Workspace initialization
│   ├── run_forge.sh                # Main pipeline runner
│   └── rotate_account.sh           # Claude Code account switcher
└── references/
    ├── spec-prompt.md              # Spec writer system prompt
    ├── planner-prompt.md           # Planner system prompt
    ├── coder-prompt.md             # Coder agent system prompt
    └── qa-prompt.md                # QA reviewer system prompt
```

**Token strategy:** OpenClaw (Flo) handles orchestration only — workspace setup, monitoring, Telegram delivery. Every heavy AI step runs through `claude --print` via Claude Code, consuming your Max subscription allocation rather than the API budget.

---

## 🔧 Configuration

Edit `run_forge.sh` to set your account rotation order:

```bash
# In rotate_account.sh
ACCOUNTS=(
  "you@example.com"
  "you2@example.com"
  "you3@example.com"
)
```

---

## 🤝 Contributing

FlowForge is open source under MIT. PRs welcome — especially:
- New workflow type templates
- Language-specific verification patterns
- Tighter GitHub/Linear integration

---

## 📦 Part of the Flowverse

FlowForge is part of the [Flowverse](https://flowverse.io) open-source toolkit:

| Tool | What it does |
|------|-------------|
| [FlowClaw](https://github.com/windseeker1111/flowclaw) | LLM usage monitor + load balancer |
| **FlowForge** | Autonomous coding pipeline via Claude Code |

---

## License

MIT — free to use, modify, and distribute.

