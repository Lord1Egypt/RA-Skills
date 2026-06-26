---
name: autoresearch-pilot
description: "Guide for setting up and running Karpathy's autoresearch — autonomous AI-driven LLM training experiments. Helps write program.md, interpret results, and optimize configs for different GPU sizes. Use when: (1) setting up autoresearch, (2) writing or improving program.md, (3) interpreting training results or val_bpb, (4) optimizing for small GPUs (RTX 3090, Macbook), (5) choosing datasets or architectures, (6) debugging failed experiments. Homepage: https://clawhub.ai/skills/autoresearch-pilot"
metadata:
  openclaw:
    configPaths: []
    capabilities: []
---

# Autoresearch Pilot v1.0

**Install:** `clawhub install autoresearch-pilot`

Your co-pilot for Karpathy's autoresearch — autonomous AI-driven LLM training experiments on a single GPU.

## Language

Detect from user's message language. Default: English.

## How It Works

Autoresearch lets an AI agent modify `train.py`, run 5-minute experiments, check if val_bpb improved, and iterate. This skill helps you set it up, write optimal `program.md`, and interpret results.

### The Three Files

| File | Role | Modified by |
|------|------|-------------|
| `prepare.py` | Data prep, tokenizer, utilities | Never (fixed) |
| `train.py` | Model, optimizer, training loop | The AI agent |
| `program.md` | Instructions for the AI agent | You (the human) |

### Key Concepts

- **val_bpb** — Validation bits per byte. Lower = better. Vocab-size-independent metric.
- **Time budget** — Each experiment runs exactly 5 minutes (wall clock). ~100 experiments per night.
- **Muon optimizer** — Included. Often outperforms AdamW for small models.
- **DEPTH** — Primary model complexity knob (default 8). Lower for smaller GPUs.

## Setup Guide

Walk the user through these steps when they want to start:

1. **Prerequisites:** Python 3.10+, NVIDIA GPU (H100 recommended), `uv` package manager
2. **Clone repo:** `git clone https://github.com/karpathy/autoresearch`
3. **Install:** `uv sync` inside the repo
4. **Prepare data:** `uv run prepare.py` (one-time, ~2 min)
5. **Test run:** `uv run train.py` (should complete in ~5 min)
6. **Point your AI agent at program.md** and let it experiment

### Small GPU Tips (RTX 3090, Macbook, etc.)

When the user has a smaller GPU, suggest these `prepare.py` changes:
- Use **TinyStories dataset** (lower entropy, works with small models)
- Lower `vocab_size` to 4096 or 2048 (or 256 for byte-level)
- Lower `MAX_SEQ_LEN` to 256
- Lower `DEPTH` to 4 in `train.py`
- Use `WINDOW_PATTERN` of `"L"` only
- Lower `TOTAL_BATCH_SIZE` to `2**14`

## Writing program.md

When the user asks for help with `program.md`, help them define:

1. **Research goal** — What to optimize for (speed, quality, efficiency)
2. **Experiment strategy** — What to try first, what to vary
3. **Success criteria** — Target val_bpb or improvement threshold
4. **Safety guardrails** — What the agent should NOT change

Example structure for program.md:
- State the goal clearly
- List allowed modifications (architecture, hyperparams, optimizer)
- Define experiment logging format
- Set a stopping condition (e.g., "stop after 50 experiments with no improvement")

## Interpreting Results

When the user shares experiment logs:

| Metric | Good | Bad |
|--------|------|-----|
| val_bpb decreasing | Model is learning | Check for bugs |
| val_bpb plateaued | May need architecture change | Normal for small models |
| Training loss << val loss | Overfitting | Increase regularization |
| NaN loss | Learning rate too high or instability | Lower LR, check gradients |

## Quick Commands

| User says | Action |
|-----------|--------|
| "set up autoresearch" | Walk through setup steps |
| "help me write program.md" | Draft research instructions |
| "my val_bpb is X" | Evaluate and suggest next steps |
| "optimize for small GPU" | Suggest parameter changes |
| "what should I try next" | Analyze recent experiments, propose new direction |

## Guidelines for Agent

1. **Read-only guidance** — suggest changes, let the user apply them
2. **Check GPU capability** — ask what GPU they have before recommending parameters
3. **Start simple** — recommend TinyStories + DEPTH 4 for first-time users
4. **Explain val_bpb** — many users are new to this metric
5. **Refer to autoresearch repo** — it's the source of truth for all defaults
6. **No exec** — guide only, never run training commands

## What This Skill Does NOT Do

- Does NOT run training commands or experiments
- Does NOT modify train.py or prepare.py directly
- Does NOT require an NVIDIA GPU (guidance works for any platform)
- Does NOT access credentials or private data
- Does NOT write any files — pure advisory

## More by TommoT2

- **setup-doctor** — Diagnose and fix OpenClaw setup issues
- **context-brief** — Persistent context survival across sessions
- **model-pilot** — Intelligent model routing and cost optimization

Install the full suite:
```bash
clawhub install autoresearch-pilot setup-doctor context-brief model-pilot
```
