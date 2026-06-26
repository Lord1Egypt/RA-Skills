---
name: continuous-agent-loop
description: "Canonical patterns for continuous autonomous agent loops with quality gates, evals, and recovery controls. Supports sequential, RFC, CI/PR, and exploratory loops. Trigger phrases: autonomous loop, continuous agent, quality gates, agent loop recovery, eval loop, session persistence. Adapted from everything-claude-code by @affaan-m (MIT)"
metadata: {"clawdbot":{"emoji":"🔄","requires":{"bins":[],"env":["AUDIT_ROOT"]},"os":["linux","darwin","win32"]}}
---

# Continuous Agent Loop

Patterns for autonomous agent loops with quality gates and recovery.

## Loop Selection

Choose your loop type based on requirements:

```text
Need strict CI/PR control? 
  → continuous-pr

Need RFC decomposition?
  → rfc-dag

Need exploratory parallel generation?
  → infinite

Default → sequential
```

## Production Stack (Recommended)

1. **RFC decomposition** — break large requests into a DAG of sub-tasks before looping
2. **Quality gates** — define explicit pass/fail criteria before starting each loop iteration
3. **Eval loop** — run automated checks after each iteration to verify progress
4. **Session persistence** — checkpoint state between iterations so you can resume on failure

## Key Patterns

**Sequential Loop:**
- Single task → execute → verify → repeat
- Best for: stable, incremental work
- Recovery: freeze, audit, reduce scope

**RFC-DAG Loop:**
- Decompose request → parallel branches → merge results
- Best for: complex multi-part features
- Recovery: replay failing unit

**CI/PR Loop:**
- Generate → test → push PR → merge on pass
- Best for: code-heavy deliverables
- Recovery: fail fast, surface root cause

**Infinite/Exploratory:**
- Generate variants in parallel, filter winners
- Best for: creative or search-heavy work
- Recovery: cap iterations, tighten criteria

## Failure Modes & Recovery

| Problem | Root Cause | Fix |
|---------|-----------|-----|
| Loop churn | Vague acceptance criteria | Freeze & redefine criteria |
| Repeated retries | Same root cause ignored | Run harness audit (see `scripts/harness-audit.js`), fix root |
| Merge queue stalls | Test flakes or deps | Isolate failing unit |
| Cost drift | Unbounded escalation | Cap token budget per loop |

**Recovery checklist:**
- Freeze loop
- Run `node scripts/harness-audit.js` — scores 7 categories (tool coverage, quality gates, evals, security, cost efficiency, memory, context)
- Reduce scope to failing unit
- Replay with explicit criteria

## References
- `scripts/harness-audit.js` — deterministic audit script, scores repo 0-70 across 7 categories
- `references/harness-audit.md` — full command usage and output contract
