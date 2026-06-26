# Benchmark Schema

## Purpose

This file defines the canonical structure for benchmark inputs, run metadata, raw outputs, and derived artifacts used by the `benchmark-model-provider` skill.

---

## 1. Benchmark spec

A benchmark spec should normally be stored as YAML and include these top-level sections.

```yaml
name: finance-daily-benchmark
version: v1
mode: prompt_only
base_url: https://api.example.com/v1
auth_env: BENCHMARK_API_KEY
context_profile:
  purpose: market research and daily decision support
  domain: finance
  usage_frequency: multiple times per day
providers_available:
  - openai:gpt-5.4
  - anthropic:claude-sonnet-4-6
models:
  - gpt-5.4
  - claude-sonnet-4-6
questions:
  - id: q1
    title: Macro impact summary
    task_type: analysis
    weight: 1.0
    prompt: |
      Summarize the top three macro developments affecting Vietnam today.
scoring:
  overall_weights:
    quality: 0.45
    depth: 0.35
    cost: 0.20
  include_speed_in_overall: false
outputs:
  markdown: true
  html: true
  pdf: false
  publish_default: ask
```

---

## 2. Required top-level fields

- `name`: logical benchmark name
- `version`: spec version tag
- `mode`: `prompt_only` or `agent_context`
- `models`: list of model identifiers to benchmark
- `questions`: list of benchmark questions

## 3. Recommended top-level fields

- `base_url`: OpenAI-compatible API base URL
- `auth_env`: environment variable containing the API key
- `context_profile`: normalized user benchmark context
- `providers_available`: optional trusted provider/model list captured from local OpenClaw context for verification UX
- `scoring`: weight configuration and scoring flags
- `outputs`: desired local output types
- `metadata`: free-form notes, provenance, language, owner, etc.

---

## 4. Question structure

Each question should include:

- `id`: stable unique identifier
- `title`: short human-readable title
- `prompt`: the exact prompt sent to the model

Recommended optional fields:

- `task_type`: e.g. analysis, coding, summary, recommendation
- `weight`: per-question weight
- `expected_strength`: what the question is meant to reveal
- `language`: question language

---

## 5. Mode-specific rules

### `prompt_only`
- Send only the raw prompt text.
- Do not inject memory, few-shot examples, hidden scaffolding, or benchmark-only system prompts.

### `agent_context`
- Use the same fixed shared system/context layer for all models in the run.
- Record that context in the run metadata or benchmark spec.
- Keep the run reproducible.

---

## 6. Run artifacts

A benchmark run should preserve at least these artifact types.

### Raw answer files
Suggested path pattern:

- `test_results/<run-id>/<model-slug>.md`

### Raw metrics
Suggested path pattern:

- `test_results/<run-id>/raw_metrics.json`

### Score breakdown
Suggested path pattern:

- `test_results/<run-id>/score_breakdown.json`

### Rendered reports
Suggested path patterns:

- `test_results/<run-id>/summary.md`
- `landingpage/index.html`
- `test_results/<run-id>/report.pdf`

---

## 7. Raw metrics structure

Suggested JSON shape:

```json
{
  "run_id": "2026-04-01T21-00-00Z",
  "benchmark_name": "finance-daily-benchmark",
  "benchmark_version": "v1",
  "mode": "prompt_only",
  "models": [
    {
      "model": "cliproxy/gpt-5.4",
      "questions": [
        {
          "id": "q1",
          "input_tokens": 123,
          "output_tokens": 456,
          "total_tokens": 579,
          "latency_sec": 8.4,
          "cost_usd": 0.0042,
          "cost_source": "official",
          "usage_is_estimated": false
        }
      ],
      "totals": {
        "input_tokens": 1000,
        "output_tokens": 2000,
        "total_tokens": 3000,
        "latency_sec": 44.8,
        "cost_usd": 0.028,
        "cost_source": "estimated"
      }
    }
  ]
}
```

---

## 8. Score breakdown structure

Suggested JSON shape:

```json
{
  "run_id": "2026-04-01T21-00-00Z",
  "weights": {
    "quality": 0.45,
    "depth": 0.35,
    "cost": 0.20,
    "speed_included": false
  },
  "rankings": [
    {
      "rank": 1,
      "model": "cliproxy/gpt-5.4",
      "quality_raw": 43,
      "depth_raw": 41,
      "quality_score": 92.0,
      "depth_score": 88.0,
      "cost_score": 61.0,
      "speed_score": 74.0,
      "overall_score": 84.15
    }
  ]
}
```

---

## 9. Metadata requirements

Every run should preserve:

- benchmark name
- benchmark version
- run timestamp
- benchmark mode
- execution strategy
- model list
- pricing provenance where applicable
- estimated vs actual flags for uncertain values

---

## 10. Design rule

Always keep raw data separate from derived scores. This is required for reranking, auditing, and report regeneration.
