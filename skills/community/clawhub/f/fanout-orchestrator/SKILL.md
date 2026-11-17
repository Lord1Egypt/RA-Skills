---
name: fanout-orchestrator
description: "Dispatch parallel sub-tasks across specialized agents (researcher/analyst/writer/coder) instead of serializing through one loop. Use when a task naturally decomposes into 2+ independent streams — multi-angle research, parallel reviews, multi-source synthesis, fan-out investigation, batch analysis. Backed by OpenProse VM. Triggers: 'fan out', 'parallel', 'in parallel', 'split this across', 'have X and Y both look at', 'multi-angle review', 'research N things at once'."
metadata:
  emoji: "🌐"
  pattern_key: "fanout-orchestrator"
  first_authored: "2026-07-03"
---

# Fan-Out Orchestrator

Run multiple sub-tasks in parallel across specialized agents, then synthesize. Avoids the single-loop serialization trap where everything waits on one slow step.

## When to use

- ✅ Task naturally decomposes into 2+ **independent** streams
- ✅ Each stream benefits from a specialist's perspective
- ✅ You can describe the synthesis step clearly
- ❌ Streams depend on each other's output (use sequential instead)
- ❌ Streams are trivial (just do them yourself)

## How

### Layer 1 — Lean on OpenProse directly

OpenProse (already installed via `open-prose` plugin) is the engine. For ad-hoc fan-outs, write a `.prose` file and run it. Pattern template:

```prose
# parallel-research.prose
agent researcher:
  prompt: "You are a research specialist. Gather, verify, synthesize. Cite sources."

parallel:
  stream_a = session: researcher
    prompt: "Research X — return sources + 200-word brief"
  stream_b = session: researcher
    prompt: "Research Y — return sources + 200-word brief"
  stream_c = session: researcher
    prompt: "Research Z — return sources + 200-word brief"

session "Synthesize streams A, B, C into a unified answer for Daniel"
  context: { stream_a, stream_b, stream_c }
```

Run with: `prose run parallel-research.prose`

### Layer 2 — `sessions_spawn` for inline fan-outs

For shorter fan-outs that don't need a full prose file, dispatch via `sessions_spawn` in parallel:

```
# Pseudo-pattern (run all in one assistant turn to maximize parallelism):
- spawn researcher → "look up X"
- spawn analyst    → "evaluate Y"
- spawn writer     → "draft Z"
- wait for all three, aggregate, return synthesis
```

Each call returns independently. Run them in the same tool-call block so they execute concurrently rather than sequentially.

### Layer 3 — Specialist routing

When specialists exist in the agent topology (researcher/analyst/writer/coder — currently blocked on config unlock), pick the right one for each stream:

| Stream type | Specialist |
|---|---|
| Web search, source synthesis, fact-finding | researcher |
| Markets, prices, decision analysis, predictions | analyst |
| Polished prose, X drafts, articles, copy | writer |
| Code generation, debugging, review | coder |

## Anti-patterns

- **False parallelism**: spawning streams that immediately need each other's output. Just run them sequentially.
- **Over-decomposition**: 10 tiny streams cost more in coordination than they save in time.
- **Fan-out without synthesis**: parallel work that returns raw streams is worse than one good answer.
- **Serial spawning**: calling `sessions_spawn` one at a time across multiple turns. Always batch.

## Output shape

Return:
1. Per-stream result (concise)
2. Synthesis (what the streams together imply)
3. Tradeoffs / contradictions between streams
4. Practical read for the user

---

<!-- Patterns from real use get appended below as they emerge -->