---
name: clawqueue
description: "Turn GitHub Issues into a local agent queue. GitHub issues in, agent work out."
homepage: https://github.com/ClawQueue/ClawQueue
metadata:
  {
    "openclaw":
      {
        "emoji": "🤖",
        "requires": { "bins": ["python3", "git"] },
      },
  }
---

# ClawQueue (CQ)

![ClawQueue Logo](https://raw.githubusercontent.com/ClawQueue/ClawQueue/main/docs/public/brand/png/ClawQueue-alpha-small.png)

> **GitHub issues in · agent work out**
> 
> Turn GitHub Issues into a local agent queue. ClawQueue is a local, git-backed and issue-tracked multi-agent queue manager designed for seamless human-agent collaboration.

---

## 🌟 Core Value Proposition

ClawQueue replaces complex, centralized workflow orchestrators with a lightweight, git-native task queue. By using GitHub Issues and Project Boards as your control surface, you get full visibility, easy human-in-the-loop oversight, and standard Git auditing for free.

### Why Local-First?
- **No Agent Lock-In**: Run your workers locally, in isolated Docker containers, or as native OpenClaw subagents.
- **Standard Git Backing**: Every action, attempt, and deliverable is logged, tracked, and stored in standard Markdown and Mermaid files.
- **Zero Heavy Infra**: You don't need a heavy database or complex API endpoints. All state is modeled natively using Git branches, commits, and GitHub project columns.

---

## 🏢 The ClawQueue Organization Ecosystem

The complete ClawQueue suite is organized into specialized repositories under the [github.com/ClawQueue](https://github.com/ClawQueue) organization:

### ⚙️ [ClawQueue/ClawQueue](https://github.com/ClawQueue/ClawQueue) (Core)
The main Python-based scheduler, dispatcher, and worker runtime. It polls your target project boards, matches unassigned issues in active column states (like "Todo"), triggers matching worker roles (e.g., `cto`, `cmo`), manages execution attempts, and commits results.

### 📝 [ClawQueue/ClawQueue-reports](https://github.com/ClawQueue/ClawQueue-reports) (The Worklog)
The standardized repository where completed task deliverables, automated reports, and execution artifacts live. Files are saved dynamically under `boards/<board_name>/<slug>.md` as structured Markdown files, ensuring your agent outputs are clean and public/private separated.

### 🐳 [ClawQueue/openclaw-balena](https://github.com/ClawQueue/openclaw-balena) (Edge Deployment)
Shell scripts and container deployment configurations designed to run lightweight OpenClaw agent and node runtimes on [balenaOS](https://www.balena.io/). Perfect for deploying resilient agent worker nodes on physical edge devices and gateways.

### 📖 [ClawQueue/ClawQueue.github.io](https://github.com/ClawQueue/ClawQueue.github.io) (Documentation)
The official open-source documentation site. Hosted via GitHub Pages at [clawqueue.github.io/ClawQueue](https://clawqueue.github.io/ClawQueue/), it provides comprehensive guides, architecture overviews, and tutorials on starting your first dispatcher profile.

---

## 🚀 How It Works

```
[ GitHub Project Board ]
       │
       ▼ (Polls columns: "Todo", "Ready")
┌─────────────────────────────────┐
│       ClawQueue Scheduler       │
└─────────────────────────────────┘
       │
       ▼ (Spawns isolated workers / subagents)
┌─────────────────────────────────┐
│     OpenClaw Worker Agents      │
└─────────────────────────────────┘
       │
       ▼ (Generates deliverables and summaries)
[ ClawQueue-reports / Worklog Repo ]
       │
       ▼ (Updates board & closes issue)
[ Completed Issue / Board Column ]
```

---

## Common CLI Commands

Run these commands from your local ClawQueue repository root:

### View Status and Active Workers
Show active tasks, current PID, remaining attempts per issue, recent dispatch decisions, and matching queued items:
```bash
python3 scripts/status.py --profile <your-profile>
```

### Diagnostics and Verification
Diagnose local profile settings and verify that your configured repository pointers, scheduler service environment, and secret parameters are mapped correctly:
```bash
/cq diagnose
```

### Trigger Scheduler Runs
Trigger an immediate evaluation/run of the queue to process pending dispatches:
```bash
/cq run
```

### Resume or Retry Tasks
Retry a failed issue after clearing its attempt counts, or resume paused tickets:
```bash
/cq retry
```

### Pause or Block
Temporarily pause task board scheduling or suspend dispatches:
```bash
/cq pause
```

## Directory and File Mapping

- **Core Repository**: `~/ClawQueue` (or your chosen checkout path)
- **Reports and Deliverables**: `~/clawqueue-worklog`
- **Profile Configurations**: `./profiles/<profile>/config/`
  - `workflow_policy.md` - Behavioral constraints and column mapping policies.
  - `clawqueue.private.json` - Private API credentials, LLM keys, and local endpoint overrides.
- **Service Logs**: `~/.local/share/clawqueue/`
- **Scheduler State**: `~/.openclaw/tmp/clawqueue/`
