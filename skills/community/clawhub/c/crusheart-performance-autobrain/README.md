<p align="center">
  <img src="https://img.shields.io/badge/OpenClaw-2026.5.0%2B-blueviolet" alt="OpenClaw">
  <img src="https://img.shields.io/badge/version-6.3.1-green" alt="Version">
  <img src="https://img.shields.io/badge/status-stable-brightgreen" alt="Status">
</p>

<h1 align="center">🦞 灵枢AutoBrain</h1>
<p align="center">
  <em>Give your OpenClaw agent a brain — long-term memory, anti-hallucination, self-evolution, and workflow orchestration, out of the box.</em>
</p>

---

## ✨ What It Does

AutoBrain is a **plugin + skill hybrid pack** that upgrades any OpenClaw agent from a stateless chatbot to a persistent, self-improving AI companion. It hooks into the agent lifecycle and deploys 90+ Python engines across 8 engine groups + 3 subsystems — no manual setup required.

| Capability | What You Get |
|------------|-------------|
| 🧠 **Long-term Memory** | 5-layer memory (session → short-term → dream consolidation → archive → vector retrieval). Remembers who you are between sessions. |
| 🛡️ **Anti-Hallucination** | Authority domain whitelist, knowledge assertion validation, multi-source cross-verification (16 engines). |
| 🔄 **Self-Evolution** | LLM-as-Judge self-scoring + Reflexion reflection (failure pattern, root cause, fix strategy). |
| 🎯 **Dual-Mode + R-CCAM** | Fast path for simple Q&A, deep reasoning for complex tasks. R-CCAM classifier for query complexity routing. |
| 🩺 **Health Check** | Daily cron — engine status, disk space, gateway health, anomaly detection (0-100 scoring). |
| 🔌 **Failover + Error Isolation** | Auto-switch to backup model when primary fails. Circuit breaker with timeout protection, auto-retry, and checkpoint resume. |
| 🔀 **Workflow Orchestration** | Multi-skill coordination, conflict detection, task routing, rule engine. |
| 📋 **Context Capsule (DAG)** | DAG-based context management with incremental summarization. SQLite-backed, retains message dependencies. |
| 🔍 **Enhanced Retrieval** | Query rewriting + RRF fusion + retrieval confidence evaluation for higher recall accuracy. |
| 🧵 **Background Sub-Agents** | Async task dispatch + subagent spawn with heartbeat, timeout recovery, and SQLite persistence. |

## 🚀 Quick Start

### Prerequisites

- **OpenClaw** ≥ 2026.5.0
- **Node.js** ≥ 18
- **Python** ≥ 3.10

### Install

```bash
# Quick Install

openclaw plugins install --dangerously-force-unsafe-install ./crusheart-pack/

# Restart gateway
supervisorctl restart openclaw-gateway
```

> **Why `--dangerously-force-unsafe-install`?** The plugin's `index.js` calls `child_process` to execute Python engines during bootstrap. This is a false positive — the code is local, not remote.

### Verify

```bash
openclaw plugins list | grep crusheart
# Bootstrap log should show:
#   ✅ Engine deployment complete
#   ✅ Init wizard: 8 steps passed
#   ✅ 2 cron jobs registered
```

## 🏗️ Architecture

```
openclaw-gateway
  │
  ├── crusheart-autobrain-turbo (plugin)
  │     ├── index.js                    ← Node.js bridge to 4 lifecycle hooks
  │     ├── bundle/crusheart-core.tar.gz  ← 90+ Python engines (deployed at bootstrap)
  │     └── skill/                       ← OpenClaw skill metadata
  │
  ├── core/engines/                     ← Deployed to workspace (8 groups)
  │     ├── init/      (12)  — Config, session, context capsule, auto-loader
  │     ├── memory/     (7)  — 5-layer memory, vector index, user portrait
  │     ├── quality/   (11)  — Anti-hallucination, judge engine, anomaly detection
  │     ├── operations/ (7)  — Health check, decision core, autonomy cycle
  │     ├── workflow/   (7)  — Orchestrator, rule engine, serial lanes, goal compiler
  │     ├── tools/     (12)  — Failover, DB, template library, trace timeline
  │     ├── hooks/      (4)  — Dual-mode classifier, self-evolution v3/v4
  │     └── compat/     (2)  — Third-party engine registry
  │
  ├── core/pipeline/    (10)  — 10-stage message pipeline
  ├── core/planner/     (6)   — Goal parsing & task decomposition
  └── core/capability/  (1)   — Task graph models
```

## 📦 What's Included

| Artifact | Path | Purpose |
|----------|------|---------|
| Plugin entry | `index.js` | Bridges Python engines into OpenClaw lifecycle hooks |
| Plugin manifest | `openclaw.plugin.json` | OpenClaw plugin registration |
| Engine bundle | `bundle/crusheart-core.tar.gz` | 90+ Python engines + pipeline + planner |
| Skill metadata | `skill/_meta.json` | Skill marketplace registration |
| Skill doc | `skill/SKILL.md` | Skill documentation |
| Readme (this file) | `README.md` | English readme |
| Readme (Chinese) | `readme_cn.md` | Chinese readme |
| Skill doc (Chinese) | `skill_cn.md` | Chinese skill documentation |
| Architecture reference | `bundle/ARCHITECTURE.md` | Full architecture with file lookup |
| System rules | `bundle/SOUL.md` | Iron rules for agent behavior (deployed to workspace) |
| Install guide | `bundle/INSTALL_GUIDE.md` | Installation wizard documentation |
| Auto-deployed scripts | `bundle/*.py`, `bundle/*.sh` | 8 scripts deployed to workspace scripts/ |

## 🔧 Configuration

### Environment Variables (optional)

| Variable | Purpose | Default |
|----------|---------|---------|
| `EMBEDDING_API_URL` | Remote embedding service URL | _(local TF-IDF fallback)_ |
| `EMBEDDING_API_KEY` | Bearer token for embedding API | _(none)_ |
| `FALLBACK_MODEL` | Backup model when primary fails | _(user-configured)_ |
| `CRUSHEART_PYTHON` | Python interpreter path | `python3` |

Without these, the system falls back to local TF-IDF vector search — slightly less accurate but fully functional.

### Cron Jobs (auto-registered)

| Time | Name | Description |
|------|------|-------------|
| `0 1 * * *` | Unified maintenance + memory maintenance | Health check + memory consolidation + system cleanup + dream scan + replay distill + execution review + memory scan/archive/index rebuild + skill scan |
| `0 5 * * *` | Engine re-init + version check | `init_engines.py --bootstrap` + `version_check.py` check for new release |


---

The current version is under development and testing. If you have any suggestions or questions about this plugin, please send them to the email address HIM603070@gmail.com
