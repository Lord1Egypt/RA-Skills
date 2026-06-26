---
name: free-scaling
version: 3.3.1
description: "$0 test-time scaling with online learning. Classify, generate, and verify using free model ensembles. Models self-select via ELO scoring + A/B testing from deployment data. 13 NIM models + optional Copilot backend."
---

# Free Scaling

$0 test-time scaling infrastructure using NVIDIA NIM free tier.

Three patterns, one API key:

```python
from free_scaling import scale, generate, health

# Classify — vote on labels
result = scale("Is this safe?", context=code, k=3,
               answer_patterns=["SAFE", "VULNERABLE"])

# Generate — best-of-k with cross-evaluation
result = generate("Summarize this paper.", context=paper, k=3)

# Verify — just scale() with source+output as context
check = scale("Any hallucinated claims?",
              context=f"Source:\n{src}\n\nOutput:\n{draft}",
              k=3, answer_patterns=["YES", "NO"])
```

## Setup

1. Get a free API key at [build.nvidia.com](https://build.nvidia.com)
2. `export NVIDIA_API_KEY="nvapi-..."`
3. No pip install — stdlib only (Python 3.10+)

## Core API

### `scale(question, context, k, answer_patterns)` → CascadeResult

Classification via ensemble voting. Ask k models, majority wins.

```python
result = scale(
    "Is this email urgent? Answer URGENT, NORMAL, or IGNORE.",
    context=email_body,
    k=3,
    answer_patterns=["URGENT", "NORMAL", "IGNORE"]
)
result.answer       # "NORMAL"
result.confidence   # 1.0
result.calls_made   # 3
result.elapsed_s    # 1.8
```

**Parameters:**
- `question` — what to judge (should end with "Answer X or Y")
- `context` — material to evaluate (placed in system message)
- `k` — models to query: 1, 3, 5, or `"auto"` (smart cascade)
- `answer_patterns` — expected answers (e.g. `["YES", "NO"]`)
- `models` — override model selection (list of aliases)

### `generate(question, context, k)` → GenerateResult

Best-of-k generation with cross-evaluation. Round 1: k models generate. Round 2: k different models judge which is best.

```python
result = generate(
    "Summarize this email in 2 sentences.",
    context=email_text,
    k=3,
    max_tokens=200,
)
result.output          # winning summary
result.all_outputs     # all 3 summaries
result.winner_model    # "llama-3.3"
result.judge_votes     # ["2", "2", "2"]
result.total_calls     # 6 (3 gen + 3 judge)
```

### `scale_batch(items, k)` / `generate_batch(items, k)`

Parallel batch versions. Each item is a dict with `question`, `context`, `answer_patterns`.

```python
results = scale_batch([
    {"question": "Urgent?", "context": e, "answer_patterns": ["YES", "NO"]}
    for e in emails
], k=3)
```

### `health(models=None)` → dict

Probe models. Returns status per model (ok/dead/slow/error + latency).

```python
status = health()  # all models
status = health(models=["llama-3.3", "gemma-27b"])  # specific
```

Dead models are auto-skipped in subsequent calls and retried after 5 minutes.

## Online Learning (v3.3)

Models self-select through deployment data. No manual benchmarking needed.

```python
from free_scaling import elo, feedback
from free_scaling.evolve import evolve, report

# Every scale() call automatically:
# 1. Logs votes to ELO tracker
# 2. Runs 1 shadow challenger for A/B data
# 3. Logs result for user feedback resolution

# Check current rankings
print(elo.summary())

# User feedback (4× stronger than consensus signal)
feedback.resolve_by_reaction("discord-msg-id", "👍")   # confirm
feedback.resolve_by_reaction("discord-msg-id", "🅱️")   # Panel B wins
feedback.resolve_by_reaction("discord-msg-id", "🔴")   # override to URGENT

# Weekly panel evolution
result = evolve(dry_run=True)   # check if panel should change
result = evolve(dry_run=False)  # apply the change
```

**How it works:**
- Consensus: models that agree with majority get +ELO (K=16)
- Override: user feedback is 4× stronger (K=64)
- Shadow challenger: 1 extra model per call for free A/B data
- Evolution: top-3 by ELO become champion panel (requires 30+ calls/model)

## Smart Features

- **Online learning**: ELO-based model scoring from deployment data (see above)
- **A/B testing**: shadow challengers run alongside panel for competitive signal
- **Auto-heal**: 404/410 models get marked dead, substituted with same-tier alternatives, retried after 5min TTL
- **Context routing**: `context` goes in system message, `question` stays in user message
- **Parallel short-circuit**: submits all k models in parallel, cancels remaining when first 2 agree
- **Task classification**: `k="auto"` classifies the question type and routes to the best expert
- **Copilot integration**: `cp-*` aliases route automatically through GitHub Copilot API
- **User feedback loop**: Discord reaction → ELO update (👍 confirm, 🅰️🅱️ A/B, 🔴🟡⚪ override)
- **Error isolation**: batch functions catch per-item failures without killing the batch

## 13 Models Included

| Tier | Models | Latency |
|------|--------|---------|
| Fast | llama-3.3 70B, gemma-27b, nemotron-super-49b, dracarys-70b, jamba-mini | <1s |
| Medium | mistral-large 675B, kimi-k2, qwen-397b, llama-405b, mistral-medium | 1-3s |
| Thinking | deepseek-v3.1, minimax-m2.5 🧠, kimi-k2.5 🧠 | 3s+ |

All free via NVIDIA NIM. One API key covers everything.

## CLI

```bash
python3 -m nim_ensemble.cli scale "Is this safe?" -k 3 --answers "SAFE,VULNERABLE"
python3 -m nim_ensemble.cli models     # list available models
python3 -m nim_ensemble.cli panels     # list panels
```

## Capability Profiling (optional)

Profile models on your tasks for data-driven routing:

```bash
python3 -m nim_ensemble.capability_map --models llama-3.3 gemma-27b mistral-large --trials 3
```

Generates `capability_map.json` — the cascade loads it automatically.

## Architecture

```
nim_ensemble/
├── __init__.py       # Exports: scale, generate, health, scale_batch, generate_batch
├── cascade.py        # scale(), scale_batch(), smart cascade
├── generate.py       # generate(), generate_batch(), best-of-k
├── voter.py          # Core voting engine, NIM + Copilot backends
├── health.py         # Model probing, dead-model tracking, substitution
├── models.py         # Model registry, panels
├── parser.py         # Answer extraction (thinking models, negation, word boundaries)
├── elo.py            # Online ELO scoring, model ranking
├── feedback.py       # User feedback loop (reactions → ELO updates)
├── evolve.py         # Weekly panel evolution (promote/demote by ELO)
├── cli.py            # CLI interface
├── benchmark.py      # Single-trial profiling
└── capability_map.py # Multi-trial profiling with error correlation
```

## Requirements

- `NVIDIA_API_KEY` environment variable (free at build.nvidia.com)
- Python 3.10+ (stdlib only, no pip dependencies)
- Optional: GitHub Copilot token for `cp-*` model aliases
