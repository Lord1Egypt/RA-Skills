---
name: context-assembler
description: Dynamic context preprocessor for OpenClaw agents. Selects relevant memory, collapses timelines, detects forbidden patterns, and injects task-specific context before agent reasoning. Reduces context noise by up to 89% while improving output quality. Use when you want smarter, more focused agent behavior without changing any prompts.
version: 1.0.0
tags: [context, memory, optimization, agent-infra]
---

# Context Assembler

**Not a tool for agents — a preprocessor for their context window.**

OpenClaw injects ~3700 tokens of static bootstrap context into every session, regardless of the task. Context Assembler reduces that to ~400 tokens of task-relevant information, achieving 89% context compression without quality loss.

## What It Does

```
Task arrives → Classify → Semantic Projection → Timeline Collapse → Forbidden Patterns → Pack → Agent reasons
```

1. **Classifies** the task type (nas_ops, coding, research, evolution_check, etc.)
2. **Semantically projects** relevant memory from MEMORY.md and daily notes — only what matters
3. **Collapses timelines** — repeated failures become single entries, noise gets filtered
4. **Detects forbidden patterns** — paths that failed ≥2 times get marked "do not retry"
5. **Packs** everything into a compact context block within token budget

## Why This Matters

Karpathy's "Context Engineering > Prompt Engineering" principle applied to OpenClaw. The quality bottleneck isn't how you write prompts — it's what the agent sees in its context window before reasoning.

## Quick Start

### Manual invocation (agent calls it)

```bash
python3 scripts/assembler.py --task "check NAS disk health" --max-tokens 1500
```

### Cron pre-turn hook

In your OpenClaw cron job, run assembler first:

```bash
# The agent's first action: get optimized context
python3 skills/context-assembler/scripts/assembler.py \
  --task "daily evolution check" \
  --max-tokens 1800
```

### Agent-assisted mode

Tell your agent: `"optimize my context"` — it will call assembler and use the output.

## Configuration

Edit `genome.yml` to customize:
- **Source weights**: which memory sources matter most
- **Task profiles**: per-task token budgets and source preferences
- **Synonym map**: lightweight semantic expansion (e.g., "shrimp" → "aquaculture, water quality")
- **Noise patterns**: timeline events to filter out
- **Staleness decay**: how fast old information loses relevance

The `genome.yml` is the "mutable kernel" — you tune it, the assembler engine stays fixed.

## Requirements

- Python 3.8+
- PyYAML (`pip install pyyaml`)
- Read access to OpenClaw workspace (`MEMORY.md`, `memory/*.md`)

## Architecture

```
skills/context-assembler/
├── SKILL.md              # This file
├── genome.yml            # ★ Mutable kernel (tune this)
├── scripts/
│   └── assembler.py      # Fixed engine (~510 lines)
├── index/                # Future: pre-built search indices
└── feedback/             # Selection → outcome log
```

## Design Principles

1. **Offload decisions**: don't teach the agent to judge — encode judgment as a checklist
2. **Compress output space**: templates > free-form writing
3. **Absence as signal**: tell the agent what NOT to include
4. **Embed domain knowledge**: your expertise encoded as correlation rules
5. **Graceful degradation**: missing data is normal, not an error

## Notes

- Phase 1 uses keyword matching with synonym expansion (zero-latency, zero-extra-memory)
- Phase 2+ will add embedding-based semantic search as memory corpus grows
- The genome is designed to be optimizable — feedback logging enables self-tuning
- Does NOT modify OpenClaw core — installs as a regular skill
- Contains no credentials, tokens, or personal identifiers — safe to publish
