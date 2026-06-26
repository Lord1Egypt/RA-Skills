# agent-usage-tracker

`agent-usage-tracker` is an OpenClaw skill package for tracking AI agent token usage, computing spend, enforcing budgets, and generating usage analytics from SQLite-backed history.

## Features

- Persist prompt, completion, and total token usage
- Calculate per-request and aggregate cost from model pricing
- Persist budget policies with warning and blocking thresholds
- Summarize usage by model, session, and time range
- Generate daily time-series data for reporting

## Project layout

- `SKILL.md`: skill trigger metadata and operating guidance
- `src/`: implementation
- `tests/`: Vitest coverage
- `examples/`: runnable sample

## Install

```bash
npm install
```

## Build

```bash
npm run build
```

## Test

```bash
npm test
```

## Example

```bash
npm run example
```

## Usage

```ts
import { BudgetManager, CostCalculator, UsageTracker } from "./src/index.js";

const pricing = new CostCalculator({
  "gpt-4.1-mini": { inputCostPerMillion: 0.4, outputCostPerMillion: 1.6 }
});

const tracker = new UsageTracker({
  dbPath: "usage.db",
  costCalculator: pricing
});

await tracker.recordUsage({
  sessionId: "session-1",
  model: "gpt-4.1-mini",
  promptTokens: 1200,
  completionTokens: 300
});

const budgetManager = new BudgetManager(tracker);
await budgetManager.setBudget({
  name: "daily-dev-budget",
  limitUsd: 5,
  warningThreshold: 0.8
});
const result = await budgetManager.evaluateBudget("daily-dev-budget");

console.log(result.status);
```
