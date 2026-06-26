import { afterEach, describe, expect, it } from "vitest";

import { BudgetManager } from "../src/BudgetManager.js";
import { CostCalculator } from "../src/CostCalculator.js";
import { UsageTracker } from "../src/UsageTracker.js";

describe("BudgetManager", () => {
  let tracker: UsageTracker | undefined;

  afterEach(() => {
    tracker?.close();
    tracker = undefined;
  });

  it("returns warning when spend crosses threshold", async () => {
    tracker = new UsageTracker({
      dbPath: ":memory:",
      costCalculator: new CostCalculator({
        expensive: { inputCostPerMillion: 10, outputCostPerMillion: 20 }
      })
    });

    await tracker.recordUsage({
      sessionId: "budget-session",
      model: "expensive",
      promptTokens: 40_000,
      completionTokens: 20_000
    });

    const manager = new BudgetManager(tracker);
    await manager.setBudget({
      name: "session-budget",
      limitUsd: 1,
      warningThreshold: 0.75
    });
    const evaluation = await manager.evaluateBudget("session-budget");

    expect(evaluation.status).toBe("warning");
    expect(evaluation.spentUsd).toBeCloseTo(0.8);
  });

  it("returns exceeded when spend is above limit", async () => {
    tracker = new UsageTracker({
      dbPath: ":memory:",
      costCalculator: new CostCalculator({
        expensive: { inputCostPerMillion: 20, outputCostPerMillion: 40 }
      })
    });

    await tracker.recordUsage({
      sessionId: "budget-session",
      model: "expensive",
      promptTokens: 60_000,
      completionTokens: 30_000
    });

    const manager = new BudgetManager(tracker);
    await manager.setBudget({
      name: "session-budget",
      limitUsd: 1
    });
    const evaluation = await manager.evaluateBudget("session-budget");

    expect(evaluation.status).toBe("exceeded");
    expect(evaluation.remainingUsd).toBe(0);
  });

  it("stores and lists budget policies", async () => {
    tracker = new UsageTracker({ dbPath: ":memory:" });
    const manager = new BudgetManager(tracker);

    const stored = await manager.setBudget({
      name: "daily-team-budget",
      limitUsd: 25,
      warningThreshold: 0.5,
      model: "gpt-4.1-mini"
    });

    expect(stored.name).toBe("daily-team-budget");

    const loaded = await manager.getBudget("daily-team-budget");
    const all = await manager.listBudgets();

    expect(loaded?.model).toBe("gpt-4.1-mini");
    expect(all).toHaveLength(1);
  });
});
