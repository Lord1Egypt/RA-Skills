---
name: evolution-dashboard
description: Generate performance metrics dashboard for EvoMap evolution cycles — success rates, gene performance, signal trends. Use when you need to audit evolution health or report on evolver progress.
---

# Evolution Dashboard

Generates a performance metrics report from EvoMap evolution data.

## Quick Start

```bash
# Generate full dashboard
node skills/evolution-dashboard/scripts/dashboard.js

# Or use the main entry programmatically
node -e "const d = require('./skills/evolution-dashboard'); console.log(JSON.stringify(d.generate(), null, 2))"
```

## Metrics Reported

- **Overview**: Total cycles, success/fail counts, overall success rate
- **Gene Performance**: Per-gene stats (successes, attempts, success rate)
- **Signal Trends**: Most frequent signals and their frequency
- **Timeline**: Recent cycle outcomes with timestamps and scores

## Data Sources

Reads from (in priority order):
- `.evolver/gep/events.jsonl` — Primary: EvolutionEvent and ValidationReport records
- `.evolver/gep/genes.json` — Gene definitions and stats
- `.evolver/gep/capsules.json` — Solidified capsule outcomes
- `memory/evolution/memory_graph.jsonl` — Fallback legacy data
- `memory/evolution/evolution_state.json` — Cycle counters

## Notes

- All metrics are computed locally, no external API calls
- Dashboard output is plain text, suitable for chat display
- Use during heartbeats to track evolution health over time
- Enhanced in cycle #0015 to read from `.evolver/gep/` as primary source
