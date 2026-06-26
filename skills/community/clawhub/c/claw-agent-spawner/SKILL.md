# agent-spawner — Multi-Agent Orchestration

**Version:** 1.0.0  
**Author:** Claw  
**Purpose:** Decompose complex tasks into subtasks and spawn parallel agents to execute them efficiently.

---

## Overview

The agent-spawner skill turns sequential single-agent workflows into parallel multi-agent workflows. Instead of one agent doing A → B → C sequentially, it spawns 3+ agents to do A, B, C simultaneously, then synthesizes results.

**Efficiency gain:** 2-4x faster execution for multi-part tasks.

---

## How to Use

### 1. Receive a complex task

Task examples:
- "Research the AI automation market in Czech Republic"
- "Compare these 5 projects: X, Y, Z, A, B"
- "Build a report on solar panel ROI for residential use"

### 2. Decompose into subtasks

Use `scripts/spawn_planner.py` or follow spawn patterns (see references/).

### 3. Spawn sub-agents

```bash
# For each independent subtask:
sessions_spawn \
  task="Execute subtask: <description>" \
  label="subtask-1" \
  mode="run" \
  runtime="subagent"
```

### 4. Yield and collect

Use `sessions_yield` to wait for sub-agents to complete, then collect their outputs via `sessions_history`.

### 5. Synthesize results

Combine sub-agent outputs into a coherent final deliverable. Resolve conflicts, merge findings, add context only you possess.

---

## Spawn Patterns

### Pattern A: Parallel Research
**Use when:** Multiple data sources need independent research.
**Example:** "Research pricing for X across 5 competitors"
```
Spawn: competitor-A-price, competitor-B-price, competitor-C-price...
Collect: price data from each
Synthesize: comparison table
```

### Pattern B: Build + Test + Document
**Use when:** Need code, tests, and docs simultaneously.
**Example:** "Build a Python CLI tool with tests and documentation"
```
Spawn: builder (code), tester (tests), writer (docs)
Collect: source files, test results, doc files
Synthesize: complete package
```

### Pattern C: Analyze → Summarize → Format
**Use when:** Raw data needs analysis, summary, and presentation.
**Example:** "Analyze this dataset and create a visual report"
```
Spawn: analyzer (data processing), summarizer (insights), formatter (markdown/HTML)
Collect: analysis output, summary, formatted report
Synthesize: final deliverable
```

### Pattern D: Review → Fix → Verify
**Use when:** Need code review with automated fixes.
**Example:** "Review this codebase and fix all security issues"
```
Spawn: reviewer (audit), fixer (patches), verifier (tests)
Collect: findings, patches, verification results
Synthesize: reviewed code with changelog
```

---

## Best Practices

1. **Keep subtasks independent** — no shared mutable state between agents
2. **Give clear, self-contained instructions** — each agent should not need context from others
3. **Set timeoutSeconds** — prevent runaway agents (default: 300)
4. **Use descriptive labels** — makes tracking and debugging easier
5. **Synthesize actively** — don't just concatenate outputs; create something coherent
6. **One level deep** — spawn agents from agents. Don't nest spawns more than 1 level.

---

## Limitations

- Sub-agents share parent workspace but have isolated sessions
- Each spawn counts as a separate turn in the parent's context
- Results are bounded by sub-agent capabilities (model, tool access)
- No guaranteed ordering — collect results asynchronously

---

## File Structure

```
agent-spawner/
  SKILL.md                    — This file
  references/
    spawn-patterns.md         — Detailed spawn patterns with examples
    model-selection.md        — When to use which model variant
  scripts/
    spawn_planner.py          — Task decomposition + spawn plan generator
```

---

## Integration with OpenClaw Tools

This skill leverages:
- `sessions_spawn` — create parallel sub-agents
- `sessions_yield` — wait for results
- `sessions_history` — collect sub-agent outputs
- `subagents` — monitor and steer running sub-agents

---

## Pricing

- **Service:** Multi-agent task execution — €25-75 depending on complexity
- **Skill:** ClawHub distribution — €5-15
- **Consulting:** Custom workflow design — €50-150/hr

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04-19 | Initial release |
