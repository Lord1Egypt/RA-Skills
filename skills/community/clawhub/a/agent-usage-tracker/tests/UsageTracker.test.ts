import { afterEach, describe, expect, it } from "vitest";

import { CostCalculator } from "../src/CostCalculator.js";
import { UsageTracker } from "../src/UsageTracker.js";

describe("UsageTracker", () => {
  let tracker: UsageTracker | undefined;

  afterEach(() => {
    tracker?.close();
    tracker = undefined;
  });

  it("records usage and includes computed cost", async () => {
    tracker = new UsageTracker({
      dbPath: ":memory:",
      costCalculator: new CostCalculator({
        "gpt-4.1-mini": {
          inputCostPerMillion: 0.4,
          outputCostPerMillion: 1.6
        }
      })
    });

    const record = await tracker.recordUsage({
      sessionId: "session-a",
      model: "gpt-4.1-mini",
      promptTokens: 10_000,
      completionTokens: 5_000,
      metadata: { requestId: "req_123" }
    });

    expect(record.totalTokens).toBe(15_000);
    expect(record.totalCostUsd).toBeCloseTo(0.012);

    const stored = await tracker.listUsage();
    expect(stored).toHaveLength(1);
    expect(stored[0]?.metadata).toEqual({ requestId: "req_123" });
  });

  it("aggregates by model, session, and day", async () => {
    tracker = new UsageTracker({
      dbPath: ":memory:",
      costCalculator: new CostCalculator({
        modelA: { inputCostPerMillion: 1, outputCostPerMillion: 2 },
        modelB: { inputCostPerMillion: 0.5, outputCostPerMillion: 1 }
      })
    });

    await tracker.recordUsage({
      sessionId: "s1",
      model: "modelA",
      promptTokens: 1000,
      completionTokens: 500,
      timestamp: "2026-03-07T10:00:00.000Z"
    });
    await tracker.recordUsage({
      sessionId: "s1",
      model: "modelB",
      promptTokens: 2000,
      completionTokens: 1000,
      timestamp: "2026-03-07T11:00:00.000Z"
    });
    await tracker.recordUsage({
      sessionId: "s2",
      model: "modelA",
      promptTokens: 4000,
      completionTokens: 2000,
      timestamp: "2026-03-08T09:00:00.000Z"
    });

    const summary = await tracker.getUsageSummary();
    expect(summary.totalRequests).toBe(3);
    expect(summary.totalTokens).toBe(10_500);
    expect(summary.byModel).toHaveLength(2);
    expect(summary.bySession).toHaveLength(2);

    const series = await tracker.getTimeSeries();
    expect(series).toEqual([
      expect.objectContaining({ bucket: "2026-03-07", requests: 2, totalTokens: 4500 }),
      expect.objectContaining({ bucket: "2026-03-08", requests: 1, totalTokens: 6000 })
    ]);
  });
});
