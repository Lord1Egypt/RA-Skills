# Reference — Models

Choose the **cheapest model that meets the quality bar**. Default to Haiku; escalate deliberately.

---

## Families

| Model ID | Family / tier | Strengths | Typical use | Relative cost |
|----------|---------------|-----------|-------------|---------------|
| `claude-opus-4-8` | Opus — most capable | Deepest reasoning, complex agents, hard coding, nuanced analysis | High-stakes/complex tasks where quality dominates | $$$ |
| `claude-opus-4-7` | Opus — previous | Very strong reasoning | When 4.8 isn't required but you want Opus-class quality | $$$ |
| `claude-sonnet-4-6` | Sonnet — balanced | Strong quality at moderate cost; fast enough for production | Most production workloads | $$ |
| `claude-haiku-4-5` | Haiku — fast & cheap | Low latency, low cost, solid for well-scoped tasks | Classification, extraction, routing, short chat, high volume — **default** | $ |

> Verification needed: confirm exact model IDs, pricing tiers, and context-window sizes at https://docs.anthropic.com/en/docs/about-claude/models

---

## Quality vs. cost

```
Quality:  Haiku  <  Sonnet  <  Opus
Cost:     Haiku  <  Sonnet  <  Opus
Latency:  Haiku (fastest)  <  Sonnet  <  Opus (slowest)
```

The right choice is the **lowest tier that still produces acceptable output** for your task.

---

## Context windows

All current Claude 4 models support large context windows (long documents, multi-file code, extended conversations). Exact token limits vary by model and may differ for input vs. output.

> Verification needed: confirm per-model context window and max output tokens at https://docs.anthropic.com/en/docs/about-claude/models

Use `anthropic_count_tokens` to confirm your prompt fits before sending.

---

## When to use each

| Task | Recommended | Why |
|------|-------------|-----|
| Bulk classification / tagging | Haiku | Cheap, fast, sufficient. |
| Data extraction to JSON (with tool forcing) | Haiku → Sonnet | Start cheap; escalate if accuracy lags. |
| Customer-facing chat | Sonnet | Good quality/cost balance. |
| Complex multi-step agent | Sonnet → Opus | Escalate if reasoning fails. |
| Hard math / proofs / deep planning | Opus + extended thinking | Needs the strongest reasoning. |
| Large codebase refactor / review | Opus or Sonnet | Quality matters; pick by budget. |
| High-volume, latency-sensitive | Haiku | Throughput and cost. |

---

## Escalation strategy

1. Try **Haiku**.
2. If quality is insufficient on a representative sample, try **Sonnet**.
3. If still insufficient, use **Opus** (add extended thinking only if needed).

Measure on a sample before committing an expensive model to a large run.

---

## Discovering models at runtime

Call `anthropic_models` (no args) to list available models, or pass `{ "model": "<id>" }` to validate one. Re-check periodically as new models ship and old ones retire.
