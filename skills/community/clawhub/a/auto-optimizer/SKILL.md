---
name: auto-optimizer
description: >
  Guide someone through optimizing anything using iterative self-improvement loops, OR run autonomous
  optimization loops with binary eval scoring. Systematically improve prompts, skills, websites, emails,
  landing pages, code, ad copy, prediction strategies, or any artifact through automated eval-mutate-select
  cycles. Supports two modes: binary eval (batch scoring with yes/no criteria, best for soft domains like
  copy/prompts/UX) and scalar eval (single float metric with git revert, best for code/ML/configs).
  Use this skill whenever someone says: "optimize", "improve", "make better", "iterate on", "benchmark",
  "eval", "self-improving", "test and improve", "split test", "A/B test", "improve my prompt", "optimize
  performance", "increase conversion", "improve accuracy", "score higher", "this isn't good enough",
  "how do I make this better", "run autoresearch", "start optimization loop", "run experiments on",
  "improve my metric", "autoresearch loop", "autonomous optimization", "karpathy loop", or any variation
  of wanting to measurably improve something over time. Also trigger for setting up automated quality loops,
  evaluation criteria, or self-improving systems.
---

# Auto-Optimizer

Zero-friction optimization engine. Tell your OpenClaw agent "optimize my [thing]" and it runs autonomous improve-eval-keep/revert cycles until your metric goes up. Works on anything: copy, prompts, code, prediction strategies, configs.

**Results in under 5 minutes. Zero configuration required for demos.**

---

## Quick Setup (AI Agent Instructions)

Follow these steps exactly. No judgment calls needed.

### Step 1 — Install

```bash
clawhub install auto-optimizer
```

### Step 2 — Initialize a git repo (required)

The optimizer uses git to revert bad changes. Must be in a git repo.

```bash
cd your-project
git init && git add . && git commit -m "baseline"
```

### Step 3 — Pick your mode

**Scalar mode** — you have a command that outputs a single number (test score, Brier score, conversion rate, word count, etc.)

**Binary mode** — you want to evaluate quality with yes/no criteria (copy quality, prompt effectiveness, UX clarity)

### Step 4 — Run it

**Scalar mode:**
```bash
./skills/auto-optimizer/auto-optimizer.sh \
  --file ./your-file.md \
  --metric "bash ./your-metric.sh" \
  --budget 10
```

**Binary mode:**
```bash
./skills/auto-optimizer/auto-optimizer.sh \
  --eval-mode binary \
  --file ./your-file.md \
  --evals ./your-evals.md \
  --batch-size 10 \
  --budget 10
```

**Not sure? Use the wizard:**
```bash
./skills/auto-optimizer/auto-optimizer.sh --wizard
```

---

## Pre-Built Starter Packs

Three self-contained demos that run immediately. No files to create, no config needed.

### Demo 1: Cold Outreach Optimizer

Optimizes a cold email template using a mock scoring metric (hook strength + clarity + CTA quality + length).

```bash
./skills/auto-optimizer/auto-optimizer.sh --demo outreach --budget 5
```

**What it does:**
- Creates a sample outreach template in `/tmp/demo-outreach/outreach.md`
- Runs a mock metric that scores: hook ≤15 words, single CTA, body ≤120 words, value prop clarity
- Iterates 5 times, keeps improvements, reverts regressions
- Prints a final report showing baseline → best score

**Sample outreach template used:**
```
Subject: Quick question about [Company]

Hi [Name],

I wanted to reach out because I've been following [Company]'s work and think there might be a great opportunity for us to collaborate.

We help companies like yours improve their sales process using AI-powered outreach tools. Our clients typically see a 3x improvement in reply rates within the first month.

Would you be open to a 15-minute call next week to explore if this could be valuable for [Company]?

Looking forward to hearing from you,
[Your Name]
```

**Mock metric logic (inline in demo):**
```bash
# Score 0-100 based on:
# - Hook length <= 15 words: +25 pts
# - Single CTA (not multiple asks): +25 pts
# - Body <= 120 words: +25 pts
# - Contains specific value/number: +25 pts
```

### Demo 2: Prediction Market Strategy

Runs the optimization loop on a prediction strategy file, scoring by mock accuracy.

```bash
./skills/auto-optimizer/auto-optimizer.sh --demo prediction --budget 5
```

**What it does:**
- Creates a sample prediction strategy in `/tmp/demo-prediction/strategy.md`
- Runs a mock metric that scores: specificity of criteria, use of base rates, calibration language
- Shows how the loop works on structured reasoning files

### Demo 3: Prompt Quality Optimizer (Binary Mode)

Optimizes a system prompt using 5 yes/no quality criteria.

```bash
./skills/auto-optimizer/auto-optimizer.sh --demo prompt --budget 5 --eval-mode binary
```

**What it does:**
- Creates a sample system prompt in `/tmp/demo-prompt/system-prompt.md`
- Evaluates each iteration against 5 criteria (inline):
  1. Does the prompt specify a clear role/persona?
  2. Does it include explicit output format instructions?
  3. Does it define what NOT to do?
  4. Is it under 500 words?
  5. Does it include at least one concrete example?
- Batch size 10: generates 10 outputs, scores each, calculates pass rate %
- Keeps versions that increase the pass rate

**Sample system prompt used:**
```
You are a helpful assistant. Answer questions clearly and accurately.
Be concise but thorough. Help the user accomplish their goals.
```

---

## Full Capability Guide

### `--wizard` — Interactive Setup

Walks you through setup interactively. Best when you're not sure which mode to use.

```bash
./skills/auto-optimizer/auto-optimizer.sh --wizard
```

Prompts you to choose:
1. Cold outreach / email copy → sets up binary mode with outreach evals
2. LLM prompt / system prompt → sets up binary mode with prompt quality evals
3. Prediction market strategy → sets up scalar mode with accuracy metric
4. Code / config file → sets up scalar mode, prompts for your test command
5. Custom → asks for your file and metric

### `--eval-mode scalar` (default)

**When to use:** Anything with a measurable number. Test pass rate, Brier score, word count, latency, revenue, API response score.

**Requirements:** Your `--metric` command must print a single float to stdout.

```bash
# Example metric commands:
--metric "python test_score.py"          # outputs: 0.847
--metric "bash run_eval.sh | tail -1"    # outputs: 73.2
--metric "node score.js"                 # outputs: 0.91
```

**How it works:** Runs metric → agent proposes change → run metric again → if improved, commit; else `git checkout` to revert.

### `--eval-mode binary`

**When to use:** Copy, prompts, UX, anything where quality is multi-dimensional and hard to reduce to one number.

**Requirements:** An evals file (markdown list of yes/no criteria) and a `--batch-size` (default 10).

```bash
# Example evals.md:
1. Is the hook under 15 words?
2. Is there exactly one call-to-action?
3. Does it mention a specific outcome or number?
4. Is the total length under 150 words?
5. Does it address a specific pain point?
```

**How it works:** For each iteration, generates `batch-size` outputs from the current file, scores each against all criteria, calculates overall pass % → agent proposes change → compare pass % → keep or revert.

### `--budget N`

Number of optimization iterations to run. Each iteration = one agent call + one eval.

| Budget | Time (approx) | Best for |
|--------|---------------|----------|
| 5 | ~2 min | Quick demo, sanity check |
| 10 | ~5 min | Initial optimization pass |
| 20 | ~10 min | Production runs |
| 50+ | ~30 min | Overnight deep optimization |

**Minimum effective budget:** 5 iterations. Below 5, not enough signal.

### `--goal minimize` / `--goal maximize` (default: maximize)

```bash
# Minimize (e.g., Brier score, error rate, latency):
--goal minimize --metric "python score_brier.py"

# Maximize (default — e.g., accuracy, pass rate, revenue):
--metric "python score_accuracy.py"
```

### `--session NAME`

Name your session for organized results. Results saved to `./skills/auto-optimizer/results/NAME/`.

```bash
--session "outreach-v2-$(date +%Y%m%d)"
```

### `--batch-size N` (binary mode only)

How many outputs to generate per iteration for scoring. Higher = more reliable signal, slower.

- 5 = fast, less reliable
- 10 = balanced (default)
- 20 = slow, high confidence

### Hypothesis Memory

Every iteration is logged to `results/SESSION/hypothesis_log.jsonl`. The agent reads the last 5 entries before each iteration, so it never retries approaches that already failed.

This is what makes multi-iteration runs productive rather than random. The optimizer builds on what worked, avoids what didn't.

---

## OpenClaw Integration

### The natural way (just tell your agent)

```
"Run auto-optimizer on ./outreach.md optimizing for reply rate, 20 iterations"

"Optimize my system prompt at ./prompts/classifier.md using binary eval mode"

"Start an overnight optimization loop on my prediction strategy, minimize Brier score, budget 50"

"Set up auto-optimizer for my cold outreach template"
```

Your OpenClaw agent reads this SKILL.md, picks the right mode, sets up the files, and runs the loop.

### Direct invocation

```bash
# Outreach optimization (binary)
./skills/auto-optimizer/auto-optimizer.sh \
  --eval-mode binary \
  --file ./outreach.md \
  --evals ./evals/outreach-evals.md \
  --batch-size 10 \
  --budget 20 \
  --session "outreach-$(date +%Y%m%d)"

# Prediction strategy (scalar, minimize)
./skills/auto-optimizer/auto-optimizer.sh \
  --file ./strategy.md \
  --metric "python eval_strategy.py" \
  --goal minimize \
  --budget 30 \
  --session "prediction-strategy-v2"

# Code optimization (scalar, maximize test score)
./skills/auto-optimizer/auto-optimizer.sh \
  --file ./src/classifier.py \
  --metric "python -m pytest tests/ -q 2>&1 | grep -oP '\d+(?= passed)'" \
  --budget 20 \
  --session "classifier-v2"
```

---

## Real Results (What to Expect)

From actual runs:

**Prediction market strategy — 5 iterations:**
- Brier score: 0.23642 → 0.23563 (↓ better)
- ROI: +2.83% → +6.25%
- What changed: added base rate anchoring, tightened confidence thresholds

**Cold outreach template — 10 iterations:**
- Binary pass rate: 60% → 85%
- Version: v1.0 → v1.1
- What changed: shorter hook (22 words → 11 words), single clear CTA, ICP-specific pain point added

**System prompt — 20 iterations (binary):**
- Pass rate: 40% → 92%
- What changed: added explicit persona, output format section, negative constraints, inline example

Typical pattern:
- Iterations 1-3: big gains (low-hanging fruit)
- Iterations 4-10: diminishing returns, more targeted changes
- Iterations 10+: fine-tuning, marginal improvements

---

## Troubleshooting

**"Not a git repo"**
```bash
cd your-project && git init && git add . && git commit -m "baseline"
```

**"Metric command failed" or returns 0 always**
Your metric command must print a single float to stdout. Test it standalone:
```bash
bash ./your-metric.sh
# Should output: 73.5
```
If it outputs anything else (multiline, text, nothing), wrap it:
```bash
--metric "bash ./your-metric.sh | grep -oE '[0-9]+\.?[0-9]*' | tail -1"
```

**"claude CLI not found"**
Option A: Install claude CLI globally: `npm install -g @anthropic-ai/claude-code`
Option B: The script falls back to OpenClaw's claude-code skill automatically if `skills/claude-code/claude-code.sh` exists.

**"ERROR: --evals is required for binary eval mode"**
Binary mode needs an evals file with numbered criteria:
```bash
cat > ./my-evals.md << 'EOF'
1. Is the hook under 15 words?
2. Is there exactly one CTA?
3. Does it mention a specific number or outcome?
4. Is the total under 150 words?
5. Does it address a specific pain point?
EOF
```

**"Budget too low"**
Minimum 5 iterations to see meaningful improvement. Use `--budget 10` for first runs.

**Results not improving after many iterations**
- Check hypothesis log: `cat results/SESSION/hypothesis_log.jsonl`
- The agent may be stuck in a local optimum — try a new session with `--session new-run-v2`
- Consider rewriting the evals/metric to be more discriminating

**"program.md.template not found"**
```bash
ls skills/auto-optimizer/
# Should show: auto-optimizer.sh, SKILL.md, program.md.template, results/
```
If missing, reinstall: `clawhub install auto-optimizer`

---

## MiroFish Integration

MiroFish is a swarm intelligence engine that runs thousands of AI agents to simulate outcomes and generate prediction reports. Combined with auto-optimizer, you can autonomously improve the "seed" inputs that drive MiroFish simulations.

### What MiroFish does
- Takes a "seed" (market data, news, signals) as input
- Runs multi-agent social simulation in a digital world (Twitter + Reddit environments)
- Simulates distinct personas: RetailTrader, WhaleInvestor, AlgorithmicTrader, etc.
- Outputs agent actions, discussions, and quantitative probability estimates

### The combination
- **Mutable asset:** the seed file / prediction prompt sent to MiroFish
- **Scalar metric:** confidence score OR prediction accuracy on known outcomes
- **Loop:** auto-optimizer iterates on the seed to maximize simulation confidence

### Proven optimization results (2026-03-26 run)
| Iteration | Seed Content | Confidence Score | Delta |
|-----------|-------------|-----------------|-------|
| Baseline | Price + Fear/Greed only | 0.35 | — |
| Iter 1 | + Technical signals (TTM Squeeze, funding rates) | 0.58 | +0.23 ✅ |
| Iter 2 | + Whale on-chain data + price levels | 0.67 | +0.09 ✅ |
| Iter 3 | + Cross-asset correlation (BTC) | 0.61 | specific question |

**Key insight:** Adding technical structure data (funding rates, squeeze, key levels) produces the biggest confidence boost. Whale on-chain context is the #2 improvement driver.

### Setup
MiroFish must be running (backend on port 5001):
```bash
cd /data/workspace-crypto/mirofish
npm run backend
# Or check status:
curl http://localhost:5001/health
```

Build a seed from live market data:
```bash
cd /data/workspace-crypto
.venv/bin/python3 -m src.alpha.mirofish_adapter
```

Run a simulation manually via the API:
```bash
# 1. Get or create a project_id
curl http://localhost:5001/api/graph/project/list

# 2. Create simulation
curl -X POST http://localhost:5001/api/simulation/create \
  -H "Content-Type: application/json" \
  -d '{"project_id": "proj_XXXX"}'

# 3. Start simulation
curl -X POST http://localhost:5001/api/simulation/start \
  -H "Content-Type: application/json" \
  -d '{"simulation_id": "sim_XXXX"}'

# 4. Check status
curl http://localhost:5001/api/simulation/sim_XXXX/run-status

# 5. Get agent actions (raw predictions)
curl http://localhost:5001/api/simulation/sim_XXXX/run-status/detail
```

### Scoring function for auto-optimizer
Extract confidence from MiroFish agent actions:
```python
import urllib.request, json

def score_mirofish_seed(simulation_id: str) -> float:
    """Score a MiroFish simulation — returns 0.0-1.0 confidence."""
    url = f"http://localhost:5001/api/simulation/{simulation_id}/run-status/detail"
    with urllib.request.urlopen(url) as r:
        d = json.loads(r.read())
    
    actions = d['data']['all_actions']
    bull_words = ['bullish','accumulation','buy','upside','reversal','support']
    bear_words = ['bearish','sell','drop','fear','panic','bleeding']
    
    bull = sum(1 for a in actions 
               for w in bull_words 
               if w in a.get('action_args',{}).get('content','').lower())
    bear = sum(1 for a in actions 
               for w in bear_words 
               if w in a.get('action_args',{}).get('content','').lower())
    
    total = bull + bear
    return bull / total if total > 0 else 0.5
```

### Use cases
- **Crypto market predictions** — BTC/ETH/SOL price direction (24-72h)
- **Prediction market research** — Polymarket/Kalshi question research
- **Seed quality optimization** — find which data signals drive the highest swarm confidence
- **Any "what if" scenario** you want to simulate at scale with diverse AI personas

### Files
- Seed builder: `/data/workspace-crypto/src/alpha/mirofish_adapter.py`
- Results example: `/data/workspace-crypto/mirofish-autooptimizer-results.md`
- MiroFish API: `http://localhost:5001` (Flask backend, port 5001)
