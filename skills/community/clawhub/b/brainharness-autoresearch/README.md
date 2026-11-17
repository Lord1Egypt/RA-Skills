# brainharness-autoresearch

> Previously named `brainforge-autoresearch`; earlier names include `openclaw-autoresearch` and `autoresearch`. Use the current installation commands below.

Autonomous skill prompt optimizer based on Karpathy's autoresearch methodology.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![ClawHub](https://img.shields.io/badge/ClawHub-brainharness--autoresearch-blue)](https://clawhub.ai/zning1994/brainharness-autoresearch)
[![brainharness](https://img.shields.io/badge/brainharness-marketplace-purple)](https://github.com/zning1994/brainharness)

## What it does

Define what "good" means as binary evals, then let an agent loop to optimize your skill prompt automatically. The optimizer reads your current prompt, runs it against eval cases, analyzes failures, mutates the prompt, tests the mutation, and keeps or discards it -- repeating until evals pass or the experiment budget is exhausted.

Based on [Andrej Karpathy's autoresearch](https://github.com/karpathy/autoresearch) and [Ole Lehmann's Claude Code adaptation](https://github.com/olelehmann100kMRR/autoresearch-skill). Works with any AI coding agent: OpenClaw, Claude Code, Cursor, Cline.

## Quick Start

```bash
# Claude Code (via brainharness marketplace)
/plugin marketplace add zning1994/brainharness
/plugin install brainharness-autoresearch@brainharness

# Universal (npx skills)
npx skills add zning1994/brainharness-autoresearch

# OpenClaw ClawHub
npx clawhub@0.23.3 install brainharness-autoresearch

# Standalone
git clone https://github.com/zning1994/brainharness-autoresearch
cd brainharness-autoresearch
python autoresearch.py --target ./my-skill/SKILL.md --evals eval.json
```

## How it works

```
                        +------------------+
                        |  Read SKILL.md   |
                        +--------+---------+
                                 |
                        +--------v---------+
                   +--->|  Run baseline    |
                   |    +--------+---------+
                   |             |
                   |    +--------v---------+
                   |    | Analyze failures |
                   |    +--------+---------+
                   |             |
                   |    +--------v---------+
                   |    |  Mutate prompt   |
                   |    +--------+---------+
                   |             |
                   |    +--------v---------+
                   |    |   Test mutation  |
                   |    +--------+---------+
                   |             |
                   |    +--------v---------+
                   +----+ Keep or discard  |
                        +------------------+
```

## Creating eval.json

Minimal example with one rule eval and one LLM eval:

```json
[
  {
    "name": "includes_greeting",
    "input": "Say hello to the user",
    "type": "rule",
    "rule": "contains",
    "expected": "hello"
  },
  {
    "name": "tone_is_professional",
    "input": "Draft a project update email",
    "type": "llm",
    "criteria": "The output uses a professional tone with no slang or emojis"
  }
]
```

See [eval-guide.md](eval-guide.md) for details.

## Eval types

| Type | Rule | Description |
|------|------|-------------|
| `rule` | `regex` | Match output against a regex pattern |
| `rule` | `contains` | Output must contain the expected string |
| `rule` | `not_contains` | Output must not contain the string |
| `rule` | `banned_phrases` | Output must not contain any listed phrase |
| `rule` | `word_count` | Output word count within min/max range |
| `llm` | -- | LLM judges output against freeform criteria |

## CLI Reference

| Flag | Default | Description |
|------|---------|-------------|
| `--target` | `./SKILL.md` | Path to the skill prompt file to optimize |
| `--evals` | `./eval.json` | Path to the eval definitions file |
| `--provider` | auto-detect | LLM provider: `minimax`, `openai`, `anthropic` |
| `--runs` | `3` | Number of runs per eval case per experiment |
| `--max-experiments` | `10` | Maximum optimization iterations |
| `--dashboard` | off | Generate an HTML dashboard of results |
| `--output-dir` | `./results` | Directory for output artifacts |
| `--verbose` | off | Print detailed logs to stderr |

## LLM Providers

Auto-detection order:

1. `MINIMAX_API_KEY`
2. `OPENAI_API_KEY`
3. `ANTHROPIC_API_KEY`

Custom endpoint support via `OPENAI_BASE_URL` (works with any OpenAI-compatible API).

## Output

| File | Description |
|------|-------------|
| `results.tsv` | Tab-separated eval scores per experiment |
| `changelog.md` | Human-readable log of each mutation and its effect |
| `results.json` | Full structured results for programmatic use |
| `dashboard.html` | Visual dashboard (when `--dashboard` is set) |
| `SKILL.md.baseline` | Backup of the original prompt before optimization |

## Credits

- [Andrej Karpathy's autoresearch](https://github.com/karpathy/autoresearch) -- the original methodology
- [Ole Lehmann's Claude Code adaptation](https://github.com/olelehmann100kMRR/autoresearch-skill) -- adapted for prompt optimization with coding agents

## License

[MIT](LICENSE)
