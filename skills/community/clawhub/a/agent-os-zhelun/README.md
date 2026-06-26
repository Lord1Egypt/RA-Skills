# Agent OS

A lightweight collaboration layer for multi-agent systems. File-based protocols for audit findings, context packs, mission control, flight recording, and experience promotion.

轻量级多 Agent 协作层。基于文件协议的审计发现、上下文包、健康视图、运行记录和经验沉淀。

---

## Why Agent OS? / 为什么需要它？

**The problem**: Multiple AI agents (Claude Code, Codex, WorkBuddy, Cursor) work on the same project, but they don't share state. Each starts from scratch, reading long chat logs or repo histories. Findings get lost in memos. The human must read scattered logs to understand project health.

**The solution**: A single file protocol (`.agent-os/`) that all agents read and write. No database, no server, no new tool. Just auditable plain-text files that give every agent the same starting context.

**核心痛点**: 多个 AI Agent（Claude Code、Codex、WorkBuddy、Cursor）在同一个项目上工作时彼此不共享状态。审计发现消失在 memo 里，人类需要翻阅分散的日志才能了解项目状况。

**解决方式**: 一个所有 Agent 共同读写的文件协议（`.agent-os/`）。不需要数据库、服务器或新工具。可审计的纯文本文件，让每个 Agent 都从同样的上下文开始。

| Without Agent OS / 没有它 | With Agent OS / 有它 |
|---|---|
| 每个 Agent 从零理解项目 | Context Pack 一键载入 |
| 审计发现消失在 memo 里 | Findings 状态机追踪到关闭 |
| 人类翻日志看项目健康 | Mission Control 一页看完 |
| 不知道 Agent 做了什么决定 | Flight Recorder 回放决策 |

---

## Features / 特性

- **Audit Finding Lifecycle** — Track issues through `open → accepted → fixed → verified → closed` status machine
- **Context Pack Compiler** — Give each agent run a compact starting context instead of full chat history
- **Mission Control** — One-page project health view the human can scan in seconds
- **Flight Recorder** — Record agent decisions for post-hoc replay and debugging
- **Decision Compressor** — Filter human-actionable items into 1-3 real decisions
- **Experience Promotion** — Classify learnings as rule/test/gate/prompt/doc

## v0.1.0 MVP Scope / MVP 范围

**Scripts (fully functional):**

| Script | Purpose |
|---|---|
| `scripts/upsert_finding.py` | Create/update audit findings |
| `scripts/compile_context_pack.py` | Generate context packs |
| `scripts/mission_control.py` | Generate health view |

**Workflows/Templates only (scripts planned for v0.2.0):**

- `record flight`
- `compress decisions`
- `promote learning`

## Installation / 安装

### Option 1: Install as a WorkBuddy Skill

Copy the `agent-os/` directory to your user-level skills path:

```bash
# User-level (available in all projects)
cp -r agent-os/ ~/.workbuddy/skills/agent-os/

# Or project-level (available in one project)
cp -r agent-os/ <project>/.workbuddy/skills/agent-os/
```

### Option 2: Use Scripts Standalone

The scripts in `scripts/` are self-contained (Python 3.10+, zero external deps) and can be used outside the skill:

```bash
python scripts/upsert_finding.py --help
python scripts/compile_context_pack.py --help
python scripts/mission_control.py --help
```

## Directory Protocol / 目录协议

Agent OS creates and reads from `<project-root>/.agent-os/`:

```
.agent-os/
├── findings.jsonl                  # Audit finding registry (JSONL)
├── experience-log.jsonl            # Promoted learnings (JSONL)
├── context-packs/
│   └── YYYY-MM-DD-<label>.md      # Task-scoped context summaries
├── mission-control/
│   └── YYYY-MM-DD.md              # Daily health view
└── flight-recorder/
    └── YYYY-MM-DD.jsonl            # Agent run records (JSONL)
```

**No other directories are required.** This is the single protocol root.

## Quick Start / 快速开始

### 1. Initialize the directory structure

```bash
mkdir -p .agent-os/{context-packs,mission-control,flight-recorder}
touch .agent-os/findings.jsonl
```

### 2. Create your first finding

```bash
python scripts/upsert_finding.py create \
  --title "Missing test coverage for auth module" \
  --severity P1 \
  --owner "primary-agent"
```

### 3. Generate a context pack

```bash
python scripts/compile_context_pack.py \
  --task "refactor-auth" \
  --label "auth-refactor"
```

### 4. Generate mission control

```bash
python scripts/mission_control.py
```

## Agent Onboarding / Agent 接入

A new agent joining the workspace should:

1. Read the latest context pack (`.agent-os/context-packs/`)
2. Query open findings (`.agent-os/findings.jsonl` where status = `open`)
3. Read the latest mission control (`.agent-os/mission-control/`)
4. After work: update findings or append a flight record

## Security Boundaries / 安全边界

- Agent OS only reads and writes within `<project-root>/.agent-os/`
- It does NOT access `.workbuddy/`, home directories, or system paths
- No network calls, no external dependencies, no database
- All data is plain text (JSONL + Markdown) — fully auditable
- Scripts support `--dry-run` to preview actions without writing

## License

MIT
