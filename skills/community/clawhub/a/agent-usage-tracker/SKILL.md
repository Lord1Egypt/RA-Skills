---
name: agent-usage-tracker
description: Track AI agent token usage, model costs, and budget thresholds with a TypeScript and SQLite workflow. Use when the user wants to instrument agent runs, calculate token spend, enforce per-session or time-window budgets, or analyze usage by model, session, or time range.
---

# Agent Usage Tracker

Use this skill when you need local token accounting for AI agents.

## What it provides

- Real-time token usage persistence in SQLite
- Cost calculation based on per-model pricing
- Budget thresholds with persisted warning and blocking states
- Usage statistics grouped by time window, session, or model

## Files to use

- `src/UsageTracker.ts`: ingestion, storage, and reporting
- `src/CostCalculator.ts`: pricing catalog and cost math
- `src/BudgetManager.ts`: budget policy evaluation
- `examples/basic-usage.ts`: end-to-end usage example
- `tests/`: reference behavior for tracking, budgeting, and aggregation

## Recommended workflow

1. Instantiate `UsageTracker` with a SQLite path or `:memory:` for tests.
2. Register model pricing with `CostCalculator`.
3. Record each agent interaction with prompt tokens, completion tokens, session id, and timestamp.
4. Save reusable budgets with `BudgetManager.setBudget`, then call `evaluateBudget` before or after new work to warn or stop when a limit is exceeded.
5. Use `UsageTracker.getUsageSummary` or `getTimeSeries` for reporting.

## Integration notes

- Store token counts at the moment the provider returns usage metadata.
- Keep model ids normalized. Pricing lookup is exact by model id.
- Use `metadata` for provider-specific fields such as request id or tool name.
- For sliding-window budgets, query usage by `startTime` and `endTime` before dispatching new work.

## Output expectations

This skill ships as a local Node.js package with tests and examples. Extend `CostCalculator` if your provider pricing changes.
