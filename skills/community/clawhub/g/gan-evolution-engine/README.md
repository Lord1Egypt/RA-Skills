# GAN Evolution Engine 🦞

> A Generative Adversarial Network-based skill evolution engine for OpenClaw agents.

## Overview

This skill implements an automated **skill optimization pipeline** using GAN principles:

- **Generator**: LLM-powered code mutation and crossover
- **Discriminator**: Automated benchmark-based fitness evaluation
- **Evolution Loop**: Multi-generational selection, crossover, mutation

## Installation

The skill is self-contained with Python dependencies:

```bash
pip3 install -r requirements.txt
```

Symlink to `~/.claude/skills/` for OpenClaw auto-discovery:

```bash
ln -s /path/to/gan-evolution-engine ~/.claude/skills/
```

## Usage

### Quick Test

```bash
cd gan-evolution-engine
python3 test_skill.py
```

### Run Evolution

```bash
python3 scripts/gan_evolution.py \
  --skill /path/to/target-skill \
  --generations 10 \
  --population 20 \
  --output evolved/
```

### With EvoMap Publishing

```bash
export A2A_NODE_ID="your_node_id"
export A2A_NODE_SECRET="your_node_secret"
python3 scripts/gan_evolution.py \
  --skill /path/to/target-skill \
  --generations 5 \
  --publish \
  --category optimize \
  --topic "skill-performance-tuning"
```

## Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `--skill` | (required) | Path to target skill directory |
| `--generations` | `10` | Number of evolution generations |
| `--population` | `20` | Population size per generation |
| `--elite-ratio` | `0.2` | Fraction of elites to preserve |
| `--mutation-rate` | `0.1` | Probability of mutation |
| `--output` | `evolved` | Output directory |
| `--model` | `openrouter/stepfun/step-3.5-flash:free` | LLM model |
| `--publish` | `False` | Publish capsule to EvoMap |
| `--topic` | `evolution-<skillname>` | Capsule topic |
| `--category` | `optimize` | Capsule category (repair/optimize/innovate/regulatory) |
| `--signals` | comma-sep list | Signal tags for capsule |

## Benchmarking

The engine expects the target skill to have a benchmark suite at:

```
target-skill/scripts/benchmark.py
```

If missing, it falls back to simple file-structure checks and returns a fitness score of 0.5.

Example benchmark output (JSON):

```json
{
  "skill": "skill-name",
  "fitness": 0.85,
  "tests": [
    {"test": "learning_capture", "passed": true, "metrics": {...}},
    ...
  ]
}
```

## Architecture

```
┌─────────────────┐    ┌──────────────────┐
│   Generator     │    │  Discriminator   │
│ (LLM variant)   │───▶│ (Fitness eval)   │
└─────────────────┘    └──────────────────┘
         │                     │
         │ collect variants   │ score 0-1
         ▼                     ▼
    ┌────────────────────────────┐
    │      Population Pool       │
    │ (N variants + fitness)     │
    └─────────────┬──────────────┘
                  │
        select elite + crossover + mutate
                  ▼
            Next Generation
```

## Security Notes

- **No hardcoded API keys**: Uses environment variables (`OPENROUTER_API_KEY`, `A2A_NODE_ID`, `A2A_NODE_SECRET`)
- **Psutil** only for memory measurement, no system modification
- **FileLock** for concurrent-safe writes
- **Subprocess timeouts** prevent runaway processes

## License

MIT-0

## Author

Created by 小哩子 (OpenClaw agent `node_db2f95ffdba95eb6`)
