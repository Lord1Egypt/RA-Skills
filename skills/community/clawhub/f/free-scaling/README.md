# Free Scaling

$0 test-time scaling infrastructure using [NVIDIA NIM](https://build.nvidia.com) free tier.

Three patterns, one API key, zero cost:

```python
from free_scaling import scale, generate, health

# Classify — 3 models vote on labels
result = scale("Is this code safe?", context=code, k=3,
               answer_patterns=["SAFE", "VULNERABLE"])
# → VULNERABLE (100%, 3 calls, 1.2s)

# Generate — best-of-k with cross-evaluation
result = generate("Summarize this paper.", context=paper, k=3)
# → best summary picked by 3 independent judges

# Verify — just scale() with source+output as context
check = scale("Any hallucinated claims? Answer YES or NO.",
              context=f"Source:\n{source}\n\nOutput:\n{draft}", k=3)
```

## Why

Single models hallucinate. Ensembles don't (as much). NIM gives you 13 models for free. This library turns them into reliable infrastructure with one parameter: **k**.

**Zero cost. Zero dependencies. Just stdlib Python + a free API key.**

## Setup

```bash
# 1. Get a free key at build.nvidia.com (one key works for all 13 models)
export NVIDIA_API_KEY="nvapi-..."

# 2. Clone
git clone https://github.com/isotrivial/free-scaling.git
cd free-scaling
```

No pip install needed — stdlib only (Python 3.10+).

## Quick Start

### CLI
```bash
# Classify
python3 -m nim_ensemble.cli scale "Is eval(input()) safe?" -k 3 --answers "SAFE,VULNERABLE"

# Auto-scale (smart cascade — 1 call if confident, up to 5 if uncertain)
python3 -m nim_ensemble.cli scale "Is this compliant?" -k auto

# Check model health
python3 -m nim_ensemble.cli models
```

### Python
```python
from free_scaling import scale, scale_batch, generate, generate_batch, health

# ── Classify ──────────────────────────────────────────
result = scale("Is this urgent?", context=email, k=3,
               answer_patterns=["URGENT", "NORMAL", "IGNORE"])

# Batch classify (parallel)
results = scale_batch([
    {"question": "Urgent?", "context": e, "answer_patterns": ["YES", "NO"]}
    for e in emails
], k=3)

# ── Generate ──────────────────────────────────────────
result = generate("Summarize this.", context=paper, k=3)
print(result.output)       # best of 3 summaries
print(result.winner_model) # which model won

# ── Health ────────────────────────────────────────────
status = health()
for model, h in status.items():
    print(f"{model}: {h.status} ({h.latency_s:.1f}s)")
```

## How It Works

### `scale(question, context, k)` — Classification

Ask k models the same question, majority vote. Context goes in system message so the question stays clean.

| k | Behavior | Calls |
|---|----------|-------|
| 1 | Single best model for task type | 1 |
| 3 | 3 diverse models, majority vote | 3 |
| 5 | 5 models for maximum confidence | 5 |
| `"auto"` | Smart cascade: start with 1, escalate on uncertainty | 1-5 |

### `generate(question, context, k)` — Generation

Round 1: k models generate independently (parallel).
Round 2: k *different* models judge which output is best.
Returns the winner. Judges use different model families to avoid self-evaluation bias.

### `health()` — Model Probing

Probes all models with a trivial question. Reports ok/dead/slow/error + latency.
Dead models (404/410) are auto-skipped in subsequent calls and retried after 5 minutes.

## Online Learning (v3.3)

Models self-select through deployment data. No manual benchmarking.

```python
from free_scaling import elo, feedback
from free_scaling.evolve import evolve, report

# Every scale() call automatically:
# 1. Logs votes to ELO tracker
# 2. Runs 1 shadow challenger for A/B data

# Check rankings after deployment
print(elo.summary())

# User feedback — 4× stronger than consensus
feedback.resolve_by_reaction(msg_id, "👍")   # confirm
feedback.resolve_by_reaction(msg_id, "🅱️")   # Panel B wins
feedback.resolve_by_reaction(msg_id, "🔴")   # override to URGENT

# Weekly: check if panel should evolve
result = evolve(dry_run=True)
if result["changed"]:
    evolve(dry_run=False)  # apply
```

**Signal sources:**
- **Consensus** (automatic): models agreeing/disagreeing with majority → K=16
- **Shadow challenger**: 1 extra model per call for free competitive data
- **User feedback**: reactions on output → K=64 (4× stronger)
- **A/B splits**: when panels disagree, user picks winner

After ~30 calls/model, ELO data replaces static panel selection.

## Smart Features

- **Online learning**: ELO-based model scoring from deployment data
- **A/B testing**: shadow challengers run alongside panel for competitive signal
- **Auto-heal**: Dead models get substituted with same-tier alternatives automatically
- **Parallel short-circuit**: Submits all k in parallel, cancels when first 2 agree
- **Task routing** (`k="auto"`): Classifies question type, routes to best expert
- **Copilot integration**: `cp-*` aliases route through GitHub Copilot API
- **User feedback loop**: Discord reactions → ELO updates (👍 🅰️🅱️ 🔴🟡⚪)
- **Error isolation**: Batch functions catch per-item failures without killing the batch
- **Thinking model support**: Handles MiniMax `<think>` blocks and Kimi `reasoning_content`

## 13 Models

| Tier | Models |
|------|--------|
| Fast (<1s) | llama-3.3 70B, gemma-27b, nemotron-super-49b, dracarys-70b, jamba-mini |
| Medium (1-3s) | mistral-large 675B, kimi-k2, qwen-397b, llama-405b, mistral-medium |
| Thinking (3s+) | deepseek-v3.1, minimax-m2.5 🧠, kimi-k2.5 🧠 |

All free via NVIDIA NIM. One API key covers everything.

## Model Selection

**Default**: panels are data-driven via ELO scoring from deployment. Start with static defaults, evolve automatically.

**Manual profiling** (optional): for a quick snapshot before ELO accumulates data:

```bash
python3 -m nim_ensemble.capability_map --models llama-3.3 gemma-27b mistral-large --trials 3
```

**ELO state**: stored at `~/.cache/free-scaling/elo.json`. View with `elo.summary()`. Reset by deleting the file.

## Use Cases

- **Email triage** — classify priority across 20 emails in one batch
- **Code review** — "Is this vulnerable?" with 3-model consensus
- **Content moderation** — TOXIC/BORDERLINE/CLEAN at scale
- **Fact-checking** — consensus answers from diverse architectures
- **Agent self-evaluation** — verify behavior against specs
- **Summarization** — best-of-3 summaries, judged by 3 different models
- **CI gates** — automated judgment with JSON output

## Also an OpenClaw Skill

```bash
clawhub install free-scaling
```

See [SKILL.md](SKILL.md) for the full agent skill reference.

## License

MIT — see [LICENSE](LICENSE).
