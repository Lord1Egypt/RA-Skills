---
name: adaptive-brain
description: Adaptive self-improving agent brain that learns, evolves, and optimizes itself over time. Use when you need: performance tracking, error pattern detection, automatic behavior adaptation, skill evolution, confidence-weighted learning, rollback on bad changes, metrics dashboards, proactive failure prediction, or cross-session memory synthesis. Triggers on "self improve", "learn from mistakes", "track performance", "evolve behavior", "adaptive agent", "improve yourself", "what did you learn", "learning dashboard", or when errors/corrections are detected.
---

# Adaptive Brain

A self-improving agent system that doesn't just log — it **learns, adapts, and evolves**.

## Core Philosophy

The existing self-improving-agent skill logs to markdown. That's a diary. This is an **immune system** — it detects patterns, builds antibodies, prevents recurring failures, and gets smarter with every interaction.

## Quick Start

```bash
python3 scripts/brain.py init          # Initialize brain system
python3 scripts/brain.py learn         # Log a learning
python3 scripts/brain.py error         # Log an error
python3 scripts/brain.py adapt         # Run adaptation cycle
python3 scripts/brain.py dashboard     # Show improvement metrics
python3 scripts/brain.py predict "task description"  # Predict failure risk
python3 scripts/brain.py evolve        # Auto-evolve skill configs
```

## What Makes This Different

| Feature | Basic Logger | Adaptive Brain |
|---------|-------------|----------------|
| Log entries | ✅ | ✅ |
| Pattern detection | ❌ | ✅ Recurring error clustering |
| Confidence scoring | ❌ | ✅ Weighted by success rate |
| Auto-adaptation | ❌ | ✅ Changes behavior automatically |
| Failure prediction | ❌ | ✅ Risk scoring before tasks |
| Skill evolution | ❌ | ✅ Rewrites SKILL.md based on learnings |
| Rollback | ❌ | ✅ Reverts bad adaptations |
| Performance metrics | ❌ | ✅ Tracks improvement over time |
| Cross-pattern links | ❌ | ✅ Connects related errors |
| Behavioral DNA | ❌ | ✅ Encodes successful patterns |
| Outcome tracking | ❌ | ✅ Tracks prediction accuracy |
| Skill mutation | ❌ | ✅ Auto-generates prevention rules |
| Context awareness | ❌ | ✅ Weighs learnings by recency & area |
| Feedback loop | ❌ | ✅ Confirms/contradicts based on outcomes |

## Architecture

```
~/.adaptive-brain/
├── brain.json          # Core state: DNA, confidence, metrics
├── learnings.json      # All learnings with scores and links
├── patterns.json       # Detected recurring patterns
├── evolution.json      # History of adaptations and rollbacks
├── metrics.json        # Performance tracking over time
└── predictions.json    # Failure predictions and outcomes
```

## Commands

### `learn` — Log a learning with auto-classification

```bash
python3 scripts/brain.py learn \
  --type correction \
  --summary "User corrected: weather defaults to UTC not local" \
  --area config \
  --context "Asked for Dhaka weather, got UTC time" \
  --fix "Always check USER.md timezone before reporting weather"
```

### `error` — Log an error with pattern detection

```bash
python3 scripts/brain.py error \
  --command "pip install pandas" \
  --error "externally-managed-environment" \
  --fix "Use venv or --break-system-packages" \
  --files "signal_engine.py"
```

The brain automatically checks for similar past errors and links them.

### `adapt` — Run adaptation cycle

Scans recent learnings and errors, then:
1. Detects recurring patterns (same error 3+ times)
2. Updates behavioral DNA
3. Generates prevention rules
4. Optionally promotes to workspace files

### `predict` — Predict failure risk before a task

```bash
python3 scripts/brain.py predict "deploy to production"
```

Returns risk score based on:
- Past errors in similar tasks
- Confidence level in relevant skills
- Historical success rate for task type

### `evolve` — Auto-evolve based on accumulated learnings

```bash
python3 scripts/brain.py evolve
```

The brain reviews all learnings and:
1. Identifies patterns that should become permanent rules
2. Generates optimized SKILL.md patches
3. Creates behavioral DNA mutations
4. Tracks evolution history (for rollback)

### `dashboard` — Learning metrics

Shows:
- Total learnings by category
- Error recurrence rate
- Adaptation success rate
- Improvement trend (getting better or worse?)
- Top patterns
- Confidence score over time

### `rollback` — Undo a bad adaptation

```bash
python3 scripts/brain.py rollback --to 3
```

Reverts to a previous evolution state.

## Behavioral DNA

The brain maintains a "DNA" string encoding successful behavioral patterns:

```json
{
  "dna": {
    "always_use_venv": true,
    "check_prices_before_trade": true,
    "write_files_then_execute": true,
    "test_before_publish": true,
    "default_timezone": "UTC"
  },
  "mutations": [
    {"timestamp": "...", "gene": "always_use_venv", "reason": "3 pip errors in a row"}
  ]
}
```

Each gene is backed by learnings. When a gene's backing learnings are resolved, it can be retired.

## Pattern Detection

The brain clusters errors and learnings into patterns:

```json
{
  "patterns": [
    {
      "id": "P001",
      "name": "Package install failures",
      "keywords": ["pip", "externally-managed", "venv"],
      "count": 4,
      "first_seen": "2026-03-30",
      "last_seen": "2026-03-31",
      "prevention": "Always use venv or --break-system-packages",
      "confidence": 0.95
    }
  ]
}
```

## Integration with OpenClaw

The brain reads and writes to workspace files:

| Brain Action | Target File | When |
|-------------|-------------|------|
| Behavioral rule | SOUL.md | Confidence > 0.9, seen 3+ times |
| Tool gotcha | TOOLS.md | Error pattern for specific tool |
| Workflow | AGENTS.md | Process improvement confirmed |
| Long-term | MEMORY.md | Major insight or decision |

## Learning Confidence

Every learning has a confidence score (0-1) that changes over time:

- **New learning**: 0.5 (neutral)
- **Confirmed correct**: +0.2 per successful application
- **Contradicted**: -0.3
- **Resolves error**: +0.1
- **Older than 30 days**: decays by 0.1

Only high-confidence learnings (>0.8) get promoted to workspace files.

## Automatic Triggers

After each session, the brain should run:

```bash
python3 scripts/brain.py adapt
```

Or set up a cron job:

```
Schedule: daily at 23:00
Command: python3 scripts/brain.py adapt
```

## See Also

For basic markdown logging (complementary to this skill), see the `self-improving-agent` skill. This skill is an enhanced superset with adaptation, prediction, and evolution capabilities.
