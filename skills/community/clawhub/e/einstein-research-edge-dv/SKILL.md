---
id: 'einstein-research-edge'
name: 'einstein-research-edge'
description: 'Generate and prioritize US equity long-side edge research tickets from
  EOD observations, then export pipeline-ready candidate specs for trade-strategy-pipeline
  Phase I. Use when users ask to turn hypotheses/anomalies into reproducible research
  tickets, convert validated ideas into `strategy.yaml` + `metadata.json`, or preflight-check
  interface compatibility (`edge-finder-candidate/v1`) before running pipeline backtests.'
version: '1.0.0'
author: 'DaVinci'
last_amended_at: null
trigger_patterns: []
pre_conditions:
  git_repo_required: false
  tools_available: []
expected_output_format: 'natural_language'
---

# Edge Research Ticket Generator

This skill formalizes the process of turning a trading hypothesis or anomaly into a structured, reproducible research ticket. It's the first step in the quantitative research pipeline, ensuring that ideas are well-defined and testable before any backtesting code is written.

## When to Use This Skill

- User has a trading idea or hypothesis (e.g., "I think stocks that do X tend to go up").
- User observes a market anomaly and wants to investigate it systematically.
- User wants to create a new candidate for the `trade-strategy-pipeline`.
- Triggers: "research ticket," "new strategy idea," "test this hypothesis," "is this an edge?".

## Workflow: From Idea to Pipeline-Ready Spec

### Step 1: Idea Ingestion

The skill prompts the user for the core components of their idea:

- **Hypothesis**: A clear, one-sentence statement of the proposed edge.
- **Entry Signal**: The specific conditions that trigger a buy.
- **Exit Signal**: The conditions that trigger a sell (e.g., target profit, stop-loss, time-based).
- **Universe**: The group of stocks to test this on (e.g., S&P 500, Nasdaq 100).
- **Rationale**: *Why* should this edge exist? (Behavioral, structural, etc.).

### Step 2: Ticket Generation

The `edge-generator` CLI tool takes these inputs and creates a structured research ticket in Markdown format.

```bash
edge-generator create \
  --hypothesis "Stocks hitting a 52-week high with high volume have momentum." \
  --entry "Price > 52-week high AND Volume > 2x 50-day avg volume" \
  --exit "5-day hold OR 10% profit target OR 5% stop-loss" \
  --universe "sp500" \
  --rationale "Breakout momentum, high volume confirms institutional interest."
```

This generates a file like `tickets/ER-2026-015_52_week_high_momentum.md`.

**Ticket Structure:**
- **ID**: `ER-YYYY-NNN`
- **Title**: Short description of the idea.
- **Hypothesis**: As provided.
- **Entry/Exit/Universe/Rationale**: As provided.
- **Data Requirements**: Lists the data needed (e.g., daily OHLCV, 52-week high, 50-day avg volume).
- **Priority Score**: An initial score (0-100) based on uniqueness, rationale strength, and testability.

### Step 3: Prioritization

The skill can rank all open tickets in the `tickets/` directory to help decide what to research next.

```bash
edge-generator prioritize
```

This updates the priority scores based on factors like:
- **Novelty**: How similar is this to previously tested (and failed) ideas?
- **Data Availability**: Can this be tested with our current data sources?
- **Computational Cost**: Is the backtest likely to be fast or slow?

### Step 4: Export to Pipeline Spec

Once a ticket is prioritized and approved for research, this skill exports it to the format required by the `trade-strategy-pipeline`.

```bash
edge-generator export ER-2026-015
```

This creates a directory `pipeline-candidates/ER-2026-015/` containing:

-   **`strategy.yaml`**: The machine-readable definition of the strategy.
    ```yaml
    version: edge-finder-candidate/v1
    name: 52-Week High Momentum
    hypothesis: Stocks hitting a 52-week high with high volume have momentum.
    entry:
      - "price > high_52w"
      - "volume > 2 * avg_volume_50d"
    exit:
      - "hold_days == 5"
      - "pct_change >= 0.10"
      - "pct_change <= -0.05"
    universe: "sp500"
    ```
-   **`metadata.json`**: Additional context for the pipeline runner.
    ```json
    {
      "ticketId": "ER-2026-015",
      "rationale": "Breakout momentum, high volume confirms institutional interest.",
      "priority": 85,
      "dataRequirements": ["daily_ohlcv", "high_52w", "avg_volume_50d"]
    }
    ```

### Step 5: Handoff to Backtest Engine

The generated directory is now ready to be processed by the `einstein-research-backtest-engine` skill, which will execute the backtest based on the `strategy.yaml` spec.

## Why This Is Important

- **Reproducibility**: Every research effort starts with a formal, version-controlled definition.
- **Efficiency**: Prevents wasted time on ill-defined ideas.
- **Systematic Process**: Ensures a consistent and rigorous approach to alpha research.
- **Automation**: The `strategy.yaml` format allows the backtesting process to be fully automated.

This skill is the gateway to the entire quantitative research pipeline, turning qualitative ideas into testable, machine-readable artifacts.
