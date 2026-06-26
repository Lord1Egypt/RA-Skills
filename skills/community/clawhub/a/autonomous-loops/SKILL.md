---
name: autonomous-loops
description: "Autonomous Claude Code loop patterns: sequential pipelines, persistent REPL sessions, parallel spec-driven generation, PR automation, cleanup passes, and RFC-driven DAG orchestration. Choose pattern by complexity: simple (sequential) → medium (PR loop, infinite agents) → advanced (DAG with merge queue). Trigger phrases: autonomous loop, agent loop, continuous development, parallel agents, multi-pass refinement."
metadata: {"clawdbot":{"emoji":"🔄","requires":{"bins":["gh","git","node"],"env":["CLAW_SESSION","CLAW_SKILLS"]},"os":["linux","darwin","win32"]}}
---

# Autonomous Loops — Patterns for Claude Code Automation

Running Claude in loops enables spec-driven development, CI/CD-style pipelines, and iterative refinement without human intervention between steps.

## Quick Start

**Choose your pattern by complexity:**

1. **Sequential Pipeline** (simple) — Chain `claude -p` calls for linear workflows
2. **Persistent REPL** (simple) — Interactive sessions with history
3. **Spec-Driven Parallel** (medium) — Deploy N agents from spec, manage waves
4. **PR Automation Loop** (medium) — PR creation, CI fix, auto-merge
5. **De-Sloppify Pass** (add-on) — Cleanup step after any implementation
6. **RFC-Driven DAG** (advanced) — Multi-unit parallel work with dependency graph

## Pattern Spectrum

| Pattern | Setup | Complexity | Best For |
|---------|-------|-----------|----------|
| Sequential Pipeline | Bash script | Low | Daily tasks, scripted workflows |
| REPL | Node/CLI | Low | Interactive development |
| Parallel Agents | Claude Code loop | Medium | Content generation, spec variations |
| PR Loop | Shell script | Medium | Iterative multi-day projects |
| De-Sloppify | Add-on to any | Optional | Quality cleanup after implementation |
| DAG Orchestration | Python/Node | High | Large features, parallel units, merge coordination |

## References

- `references/sequential-pipeline.md` — Basic `claude -p` loops with examples
- `references/persistent-repl.md` — NanoClaw-style session persistence
- `references/parallel-agents.md` — Spec-driven deployment with wave management
- `references/pr-automation.md` — Continuous Claude PR loop with CI gates
- `references/de-sloppify.md` — Quality cleanup pattern
- `references/dag-orchestration.md` — RFC-driven multi-unit coordination

## Key Principles

1. **Isolation** — Each loop iteration gets fresh context (no bleed-through)
2. **Context Persistence** — Use files (SHARED_TASK_NOTES.md) to bridge iterations
3. **Exit Conditions** — Always set max-runs, max-cost, max-duration, or completion signal
4. **No Blind Retries** — Capture error context for next iteration
5. **Separate Concerns** — Different loop patterns for different problem sizes

## Decision Matrix

```text
Is this a single focused change?
├─ Yes → Sequential Pipeline
└─ No → Do you have a spec/RFC?
         ├─ Yes → Do you need parallel work?
         │        ├─ Yes → DAG Orchestration
         │        └─ No → PR Automation Loop
         └─ No → Do you need many variations?
                  ├─ Yes → Parallel Agents + Spec
                  └─ No → Sequential Pipeline + De-Sloppify
```

## Anti-Patterns

❌ Infinite loops without exit conditions
❌ No context bridge between iterations
❌ Retrying the same failure without capturing error context
❌ Negative instructions instead of cleanup passes
❌ All agents in one context window (reviewer should never be the author)
❌ Ignoring file overlap in parallel work

---

**Adapted from everything-claude-code by @affaan-m (MIT)**
