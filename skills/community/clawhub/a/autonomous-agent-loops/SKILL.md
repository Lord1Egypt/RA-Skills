---
name: autonomous-loops
description: "Autonomous agent loop patterns: sequential pipelines, persistent REPL sessions, parallel spec-driven generation, PR automation, cleanup passes, and RFC-driven DAG orchestration. Choose pattern by complexity: simple (sequential) → medium (PR loop, infinite agents) → advanced (DAG with merge queue). Trigger phrases: 'autonomous loop', 'agent loop', 'parallel agents', 'multi-pass refinement', 'continuous integration loop'."
metadata: {"clawdbot":{"emoji":"🔄","requires":{"bins":["gh","git","node"],"env":["CLAW_SESSION","CLAW_SKILLS"]},"os":["linux","darwin","win32"]}}
---

# Autonomous Loops — Patterns for Agent Automation

> ## ⚠️ Security & Consent — READ FIRST
>
> **This skill teaches unattended repository automation.** It can create branches, open pull requests, retry CI failures, and merge code without a human in the loop. That power is dangerous in the wrong hands and on the wrong target.
>
> **Before using any pattern in this skill, you MUST:**
>
> 1. **Get explicit, informed consent from the repository owner.** "I want to automate PRs" is not consent for "merge my production code at 3 AM without review."
> 2. **Default to dry-run.** All patterns below start in `--disable-commits` / no-write mode. Only flip the switch when you understand what each flag does.
> 3. **Use protected branches + least-privileged credentials.** The GitHub token this loop uses must not have admin/org-owner scopes. A scoped fine-grained PAT scoped to one repo is the minimum.
> 4. **Set hard limits.** Every loop must have `--max-runs`, `--max-cost`, and `--max-duration`. Without these, a runaway loop will burn budget or destroy state.
> 5. **Never loop on production.** Run on a fork, a scratch repo, or a clearly-labeled branch. The main branch should be merged by a human.
> 6. **Audit your inputs.** Specs, directory listings, and captured diffs may contain secrets, customer data, internal paths, or proprietary code. Never pipe those into an external agent command without scrubbing them first.
>
> **Patterns in this skill that touch the network, filesystem, or git remotes will refuse to run unless the corresponding safety flags are explicitly set.** If a pattern silently merges or pushes, that is a bug — file an issue.
>
> See `references/security-checklist.md` for the full audit before first use.

---

Running agents in loops enables spec-driven development, CI/CD-style pipelines, and iterative refinement without human intervention between steps. **Used correctly**, this is a productivity multiplier. **Used carelessly**, it can drain a bank account, leak secrets, or rewrite a production codebase.

## Quick Start

**Choose your pattern by complexity:**

1. **Sequential Pipeline** (simple) — Chain `claude -p` calls for linear workflows
2. **Persistent REPL** (simple) — Interactive sessions with history
3. **Spec-Driven Parallel** (medium) — Deploy N agents from spec, manage waves
4. **PR Automation Loop** (medium) — PR creation, CI fix, auto-merge
5. **De-Sloppify Pass** (add-on) — Cleanup step after any implementation
6. **RFC-Driven DAG** (advanced) — Multi-unit parallel work with dependency graph

## Pattern Spectrum

| Pattern | Setup | Complexity | Default Mode | Best For |
|---------|-------|-----------|--------------|----------|
| Sequential Pipeline | Bash script | Low | Dry-run | Daily tasks, scripted workflows |
| REPL | Node/CLI | Low | Read-only | Interactive development |
| Parallel Agents | Agent loop | Medium | Dry-run | Content generation, spec variations |
| PR Loop | Shell script | Medium | `--disable-commits` | Iterative multi-day projects |
| De-Sloppify | Add-on to any | Optional | Dry-run | Quality cleanup after implementation |
| DAG Orchestration | Python/Node | High | Dry-run | Large features, parallel units, merge coordination |

## References

- `references/security-checklist.md` — **Read before any first use**
- `references/sequential-pipeline.md` — Basic `claude -p` loops with examples
- `references/persistent-repl.md` — Session persistence + secrets-handling rules
- `references/parallel-agents.md` — Spec-driven deployment with worktree isolation
- `references/pr-automation.md` — Continuous PR loop with consent gates and CI gates
- `references/de-sloppify.md` — Quality cleanup pattern
- `references/dag-orchestration.md` — RFC-driven multi-unit coordination + merge-conflict recovery

## Key Principles

1. **Isolation** — Each loop iteration gets fresh context (no bleed-through)
2. **Context Persistence** — Use files (SHARED_TASK_NOTES.md) to bridge iterations
3. **Exit Conditions** — Always set max-runs, max-cost, max-duration, or completion signal
4. **No Blind Retries** — Capture error context for next iteration (and redact secrets first)
5. **Separate Concerns** — Different loop patterns for different problem sizes
6. **Default Deny** — Network writes, git pushes, and merges require explicit opt-in flags

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
❌ Auto-merge without explicit human approval on every merge
❌ Skipping the security checklist before first use

---

**Adapted from everything-claude-code by @affaan-m (MIT)**