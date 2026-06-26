<p align="center">
  <img src="https://img.shields.io/badge/OpenClaw-2026.5.0%2B-blueviolet" alt="OpenClaw">
  <img src="https://img.shields.io/badge/version-6.3.1-green" alt="Version">
  <img src="https://img.shields.io/badge/status-stable-brightgreen" alt="Status">
</p>

<h1 align="center">🦞 灵枢AutoBrain — Skill Page</h1>
<p align="center">
  <em>Long-term memory, anti-hallucination, self-evolution, and workflow orchestration for OpenClaw. 90+ Python engines across 8 engine groups + 3 subsystems.</em>
</p>

---

## Quick Install

```bash
openclaw plugins install --dangerously-force-unsafe-install ./crusheart-pack/
# Then restart gateway
```

## Features

| Feature | Description |
|---------|-------------|
| **🧠 Long-term Memory** | 5-layer memory + DAG context management + memory consolidation engine |
| **🛡️ Anti-Hallucination** | Authority whitelist + multi-source cross-verification (16 engines) |
| **🔄 Self-Evolution** | LLM-as-Judge self-scoring + Reflexion reflection (pattern, root cause, fix) |
| **🎯 Dual-Mode + R-CCAM** | Fast path for simple Q&A, deep reasoning for complex tasks |
| **🔍 Enhanced Retrieval** | Query rewriting + RRF fusion + retrieval confidence evaluation |
| **🩺 Daily Maintenance** | 01:00 unified cron: health check + cleanup + memory + dream + replay + memory scan |
| **🔀 Workflow Engine** | Multi-skill coordination, conflict detection, task routing, rule engine |
| **📋 Context Capsule** | DAG-based session handoff with SQLite-backed context graph |
| **📁 Auto-Scan** | First-install: memory scan + skill classification + correction init |
| **🔄 Version Check** | One-time check against clawhub.ai on install, daily re-check at 05:00 |

## Architecture

```
plugin (index.js) ──► 90+ Python engines ──► 10-stage message pipeline
  8 engine groups: init/memory/quality/operations/workflow/hooks/tools/compat
  + 3 subsystems: pipeline/planner/capability
  + 8 auto-deployed scripts

Plugin slot: exclusive — detects any overlapping plugin and blocks install
Cron: unified maintenance (01:00), engine init + version check (05:00)
```

## Resources

- **Architecture Reference**: `bundle/ARCHITECTURE.md` — full file lookup guide
- **Readme (English)**: `README.md`
- **Readme (Chinese)**: `readme_cn.md`
- **Skill (Chinese)**: `skill_cn.md`
- **Install Guide**: `bundle/INSTALL_GUIDE.md`

---

**Feedback**: HIM603070@gmail.com
