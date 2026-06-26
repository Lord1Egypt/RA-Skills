<div align="center">

# AIWorkFlow

**Full-cycle AI development automation.**
**6 Skills. Autopilot Engine. Intelligent Orchestration.**

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Shell](https://img.shields.io/badge/Shell-Bash-blue.svg)](scripts/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Codex](https://img.shields.io/badge/Codex-Autopilot-orange.svg)](scripts/watchdog.sh)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Orchestration-red.svg)](https://github.com/openclaw/openclaw)

English · [中文](README_zh.md)

</div>

---

A complete development toolchain for AI startup teams: **6 Development Workflow Skills** + **Codex Autopilot Multi-Project Engine** + **OpenClaw Intelligent Orchestration Layer**.

## 🏗 System Overview

| Module | What It Does |
|--------|-------------|
| **Workflow Skills** (v1.5.0) | 6 skills covering the full dev cycle — requirement research → doc writing → review → development → testing → code review |
| **Codex Autopilot** | Multi-project 24/7 Codex CLI automation via tmux + launchd — status detection, smart nudge, task queue, auto-recovery |
| **OpenClaw Layer** | Cron scheduling, Claude sub-agent reviews, Telegram/Discord channels, cross-engine orchestration |

## 📋 Development Workflow Skills

```
Requirement → Doc Writing → Doc Review → Development ←→ Testing → Code Review → Release
```

| Skill | Purpose | Trigger |
|-------|---------|---------|
| **requirement-discovery** | RICE scoring, AI feasibility | "Research this requirement" |
| **doc-writing** | PRDs, tech specs, API design | "Write a requirements doc" |
| **doc-review** | Gap & risk identification | "Review this PRD" |
| **development** | Implementation, 5 Whys bug fix | "Implement this feature" |
| **testing** | Test strategy & case design | "Design test cases" |
| **code-review** | 3-layer defense review | "Review this code" |

**Core Principles:** Startup-friendly (MoSCoW MVP) · AI-native (token cost controls) · SOLID-driven · Doc-closed-loop

<details>
<summary>📌 Installation</summary>

```bash
# Gemini
ln -sf /path/to/AIWorkFlowSkill/development ~/.gemini/skills/development

# Codex — reference in AGENTS.md
# Claude — add to Skills directory
```

</details>

---

## 🤖 Codex Autopilot Engine

```
  Trigger          Detection         Decision          Execution
┌──────────┐    ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│ launchd  │───→│codex-status │──→│ watchdog.sh │──→│ tmux-send.sh│
│  (10s)   │    │    .sh      │   │ (~1700 LOC) │   │ (3-layer)   │
└──────────┘    │ JSON output │   │ State machine│   └─────────────┘
│  cron    │───→│working/idle/│   │ Exp backoff  │──→│ task-queue  │
│ (10min)  │    │perm/shell   │   │ Lock/compact │   │    .sh      │
└──────────┘    └─────────────┘   └─────────────┘   └─────────────┘
```

### Typical Flow

```
User (Telegram) → "Fix white-screen bug"
  → Claude (OpenClaw) writes to task-queue
  → Watchdog detects Codex idle → dispatches task
  → Codex fixes → commit → triggers Claude code review
  → Review clean → Discord notification "✅ Bug fixed"
```

### Multi-Model Task Routing

```
Task Queue
├─ type: frontend/ui/h5  → 🎨 Gemini tmux window (design-optimized)
├─ type: bugfix/feature   → 🔧 Codex tmux window (code-optimized)
├─ Codex limit exhausted  → 🤖 Claude AgentTeam fallback
└─ Gemini unavailable     → 🔧 Codex fallback (graceful degradation)
```

| Role | Model | Method | Best At |
|------|-------|--------|---------|
| **Orchestrator** | Claude (OpenClaw) | Direct | Planning, reviews, communication |
| **Backend Dev** | Codex (GPT-5.4) | tmux persistent | APIs, databases, deployment |
| **Frontend Dev** | Gemini CLI (`gemini-3.1-pro-preview`) | tmux persistent session | UI, components, 1M context, visual design |

Frontend tasks do **not** go through ACP for now. Direct tmux persistent sessions are more stable in current production runs.

**Configuration:**

```yaml
# config.yaml
gemini:
  default_window: "gemini-h5"    # Default Gemini tmux window
  project_windows:               # Per-project mapping
    youxin: "gemini-youxin"
```

**Usage:**

```bash
# Frontend tasks route to Gemini automatically
task-queue.sh add myproject "Build login page" normal --type frontend

# Backend tasks still go to Codex
task-queue.sh add myproject "Fix auth API" high --type bugfix
```

Frontend tasks include Anti-AI-Slop prompt injection: layout checks, design system consistency, interaction state coverage (loading/empty/error/success).

### CI/CD: Test Agent

Trigger points:
- `on_commit_evaluate`: evaluate test/coverage right after commit detection
- `on_review_clean`: run coverage-gap analysis and enqueue test tasks after review is clean
- `nightly`: scheduled coverage evaluation window

Flow:

```
commit
  → watchdog (detect new commit)
  → test-agent evaluate (run tests + collect coverage)
  → pass: continue workflow, then on review clean run coverage-gap enqueue
  → fail: auto-parse test logs
          → extract failed test files + error summary
          → task-queue add "fix tests" bugfix tasks (high priority)
```

Coverage ratchet policy:
- Weekly ratchet: `+1%`
- Cap: `90%`

Auto-enqueue on failure (introduced in `386a682`):
- Parse `$HOME/.autopilot/logs/test-agent-run-*.log` and package run logs
- Extract failed test file and key error line
- Enqueue bugfix task via `task-queue.sh add <project> ... high --type bugfix`
- 1-hour cooldown dedupe per failed target to avoid retry loops

Config example:

```yaml
test_agent:
  enabled: true
  trigger:
    on_commit_evaluate: true
    on_review_clean: true
    nightly: "02:30"
  queue:
    max_tasks_per_round: 3
  coverage:
    changed_files_min: 80
    ratchet_weekly: 1
    ratchet_cap: 90
```

### Smart Nudge Decision Tree

```
Codex idle
├─ Queue has tasks? → consume queue (bypass cooldown)
│   ├─ type=frontend? → route to Gemini window
│   └─ type=other?    → route to Codex window
├─ Review has issues? → nudge #N/5 (5-attempt cap, backoff)
├─ Compact just finished? → resume with context snapshot
├─ PRD has issues? → nudge fix
├─ Nothing pending → 💤 stay quiet (zero token waste)
└─ Dirty tree? → prompt commit
```

### Core Scripts

| Script | LOC | Function |
|--------|:---:|----------|
| `watchdog.sh` | ~1700 | Main daemon — detection, nudge, recovery, queue, tracking |
| `codex-status.sh` | ~200 | BFS process tree → JSON status |
| `tmux-send.sh` | ~480 | 3-layer send + task tracking |
| `monitor-all.sh` | ~450 | 10-min global report → Telegram |
| `task-queue.sh` | ~350 | Queue CRUD — priority, locks, timeout recovery |
| `test-agent.sh` | ~790 | Test/coverage orchestration, coverage-gap enqueue, and auto-enqueue bugfix tasks on test failures |
| `consume-review-trigger.sh` | ~450 | Trigger-file code review consumer |
| `discord-notify.sh` | ~180 | Project→channel notification mapping |
| `prd_verify_engine.py` | ~500 | PRD checker plugin system |
| `codex-token-daily.py` | ~380 | Token usage from JSONL sessions |

<details>
<summary>🛡 Safety Mechanisms</summary>

| Mechanism | Description |
|-----------|-------------|
| Smart Nudge | No nudge without tasks; review issues capped at 5 |
| Exponential Backoff | 300→600→…→9600s; stops after 6 + alert |
| 3× Idle Confirmation | Prevents API latency false positives |
| 90s Work Inertia | No nudge within 90s of "working" |
| Manual Task Protection | Human tasks protected for 300s |
| Task Tracking | Auto-notify on completion or timeout |
| Queue Concurrency Lock | Atomic mkdir; prevents corruption |
| Queue Timeout Recovery | >3600s auto-fail and re-queue |
| Compact Context Snapshot | Precise state recovery after compact |
| Runtime File Isolation | gitignored to prevent dirty repo |

</details>

### Quick Start

```bash
# 1. Configure projects
cat > watchdog-projects.conf << EOF
ProjectA:/path/to/project-a:Default nudge message
EOF

# 2. Configure Telegram (config.yaml)
# 3. Create tmux session + start Codex
tmux new-session -s autopilot -n ProjectA
codex --full-auto

# 4. Start watchdog
nohup bash scripts/watchdog.sh &

# 5. Submit tasks
bash scripts/task-queue.sh add myproject "Fix bug" high
```

---

## 📁 Project Structure

<details>
<summary>Click to expand</summary>

```
AIWorkFlowSkill/
├── README.md
├── CONVENTIONS.md
├── CONTRIBUTING.md
├── LICENSE
├── requirement-discovery/    # Skill: Requirement Research
├── doc-writing/              # Skill: Doc Writing
├── doc-review/               # Skill: Doc Review
├── development/              # Skill: Development
├── testing/                  # Skill: Test Design
├── code-review/              # Skill: Code Review
├── scripts/                  # Autopilot Engine
│   ├── watchdog.sh
│   ├── codex-status.sh
│   ├── tmux-send.sh
│   ├── monitor-all.sh
│   ├── task-queue.sh
│   └── ...
├── watchdog-projects.conf
├── config.yaml
└── prd-items.yaml
```

</details>

## 📦 Version History

| Version | Date | Highlights |
|---------|------|------------|
| **0.7.0** | 2026-03-24 | Test-agent auto-enqueue bugfix on failure, discord-notify retry, Gemini tmux as primary (not ACP transition) |
| **0.6.0** | 2026-03-22 | Multi-model routing (Gemini frontend + Codex backend), Anti-AI-Slop prompt, test agent, branch isolation |
| **0.5.0** | 2026-03-03 | Smart nudge, task tracking, Discord routing, queue locks |
| **0.4.0** | 2026-03-01 | ClawHub release, Discord→Autopilot routing |
| **2.0.0** | 2026-02-12 | Autopilot engine v6, task queue, compact snapshot, PRD verification |
| 1.5.0 | 2026-01-19 | Integrated guo-yu/skills; dangerous command blocklist |
| 1.4.1 | 2026-01-18 | Testing skill; session persistence |
| 1.0.0 | 2025-01-17 | Initial release: 4 core skills |

## 📜 License

[MIT](LICENSE)

## 🙏 Acknowledgments

Built on [OpenClaw](https://github.com/openclaw/openclaw) and [Codex CLI](https://github.com/openai/codex).
