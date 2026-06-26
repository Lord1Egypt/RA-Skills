import { describe, expect, it } from "vitest";

import { CostCalculator } from "../src/CostCalculator.js";

describe("CostCalculator", () => {
  it("calculates prompt and completion cost from per-million rates", () => {
    const calculator = new CostCalculator({
      "gpt-4.1-mini": {
        inputCostPerMillion: 0.4,
        outputCostPerMillion: 1.6
      }
    });

    const result = calculator.calculateCost("gpt-4.1-mini", 250_000, 100_000);

    expect(result.inputCostUsd).toBeCloseTo(0.1);
    expect(result.outputCostUsd).toBeCloseTo(0.16);
    expect(result.totalCostUsd).toBeCloseTo(0.26);
  });

  it("returns zero for unknown model pricing", () => {
    const calculator = new CostCalculator();
    expect(calculator.calculateCost("unknown", 1000, 1000).totalCostUsd).toBe(0);
  });
});
