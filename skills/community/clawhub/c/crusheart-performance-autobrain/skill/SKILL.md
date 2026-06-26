---
name: crusheart-autobrain-turbo
description: Long-term memory, anti-hallucination, self-evolution, and workflow orchestration for OpenClaw. 68+ Python engines, 12 groups/subsystems, zero config. Plus memory/skill auto-scan, config reader, correction data init.
homepage: https://github.com/crusheart/crusheart-autobrain-turbo
metadata:
  {
    "openclaw":
      {
        "emoji": "🦞",
        "tags": ["memory", "self-evolution", "anti-hallucination", "workflow", "orchestrator", "plugin", "health-check", "engine"],
        "requires": { "openclaw": ">=2026.5.0" }
      }
  }
---

# 灵枢AutoBrain v6.3.1

Give your OpenClaw agent long-term memory, anti-hallucination, self-evolution, and workflow orchestration. 68+ Python engines across 8 engine groups + 4 subsystems, deployed automatically.

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
| **🔄 Self-Evolution** | LLM-as-Judge self-scoring + Reflexion reflection with full triplet (pattern, root cause, fix) |
| **🎯 Dual-Mode + R-CCAM** | Fast path for simple Q&A, deep reasoning for complex tasks |
| **🔍 Enhanced Retrieval** | Query rewriting + RRF fusion + retrieval confidence evaluation |
| **🩺 Daily Maintenance** | 01:00 unified cron: health check + cleanup + memory + dream + replay |
| **🔀 Workflow Engine** | Multi-skill coordination, conflict detection, task routing, rule engine |
| **📋 Context Capsule (DAG)** | DAG-based session handoff with SQLite-backed context graph |
| **📁 Auto-Scan** | First-install: memory scan + skill classification + correction init |
| **🔄 Version Check** | One-time check against clawhub.ai on install |

## Architecture

```
plugin (index.js) ──► 68+ Python engines ──► 10-stage message pipeline
  8 engine groups: init/memory/quality/operations/workflow/hooks/tools/compat
  + 4 subsystems: pipeline/planner/learning_loop/capability
  + 7 auto-deployed scripts

Plugin slot: exclusive (.crusheart-slot.json lock)
Compat layer: compat/ engine group
Cron: health (00:00), maintenance (01:00), dreaming (03:00),
       engine init (05:00), memory (23:00), distill (23:30)
```

## Resources

- **Architecture Reference**: `bundle/ARCHITECTURE.md`
- **Readme (EN)**: `README.md`
- **Readme (CN)**: `readme_cn.md`
- **Skill (CN)**: `skill_cn.md`

---

**Feedback**: HIM603070@gmail.com
