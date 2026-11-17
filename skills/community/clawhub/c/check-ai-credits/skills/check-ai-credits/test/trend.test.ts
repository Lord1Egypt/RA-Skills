import { describe, expect, test } from "bun:test";
import {
  LOW_BALANCE_USD,
  calculateTrend,
  clipAfterReset,
  slopePerHour,
} from "../src/core/trend";
import type { Snapshot } from "../src/types";

function iso(hoursAgo: number): string {
  return new Date(Date.now() - hoursAgo * 3_600_000).toISOString();
}

function snap(partial: Partial<Snapshot> & { provider: string; timestamp: string }): Snapshot {
  return {
    source: "test",
    error: null,
    ...partial,
  } as Snapshot;
}

describe("slopePerHour", () => {
  test("linear decline -> exact negative slope", () => {
    const points = [
      { t: 0, v: 100 },
      { t: 3_600_000, v: 90 },
      { t: 7_200_000, v: 80 },
    ];
    expect(slopePerHour(points)).toBeCloseTo(-10, 6);
  });

  test("fewer than 2 points -> 0", () => {
    expect(slopePerHour([{ t: 0, v: 5 }])).toBe(0);
  });
});

describe("clipAfterReset", () => {
  test("drops everything before the last reset (percent drop)", () => {
    const points = [
      { t: 0, v: 40 },
      { t: 1, v: 95 }, // climbing
      { t: 2, v: 5 }, // reset happened here
      { t: 3, v: 15 },
    ];
    const clipped = clipAfterReset(points);
    expect(clipped.map((p) => p.v)).toEqual([5, 15]);
  });

  test("no reset -> unchanged", () => {
    const points = [
      { t: 0, v: 10 },
      { t: 1, v: 20 },
    ];
    expect(clipAfterReset(points)).toEqual(points);
  });
});

describe("calculateTrend — balance basis", () => {
  test("linear burn: 10/day from 60 -> days-left 6.0", () => {
    const entries = [96, 72, 48, 24, 0].map((h, i) =>
      snap({
        provider: "deepseek",
        timestamp: iso(h),
        currency: "USD",
        balance: 100 - i * 10,
      }),
    );
    const t = calculateTrend(entries, "deepseek")!;
    expect(t.basis).toBe("balance");
    expect(t.balance).toBe(60);
    expect(t.dailyRate).toBeCloseTo(10, 1);
    expect(t.estimatedDaysLeft).toBeCloseTo(6, 1);
    expect(t.lowBalance).toBe(false);
    expect(t.samples).toBe(5);
  });

  test("USD wallet under threshold -> lowBalance", () => {
    const entries = [
      snap({ provider: "deepinfra", timestamp: iso(48), currency: "USD", balance: 6 }),
      snap({ provider: "deepinfra", timestamp: iso(0), currency: "USD", balance: LOW_BALANCE_USD - 1 }),
    ];
    const t = calculateTrend(entries, "deepinfra")!;
    expect(t.lowBalance).toBe(true);
  });

  test("non-USD wallet never flags lowBalance on USD rule", () => {
    const entries = [
      snap({ provider: "grok", timestamp: iso(48), currency: "CREDITS", balance: 3 }),
      snap({ provider: "grok", timestamp: iso(0), currency: "CREDITS", balance: 1 }),
    ];
    const t = calculateTrend(entries, "grok")!;
    expect(t.lowBalance).toBe(false);
  });

  test("span under 0.5h -> no rate (noise rule)", () => {
    const entries = [
      snap({ provider: "deepseek", timestamp: iso(0.1), currency: "USD", balance: 50 }),
      snap({ provider: "deepseek", timestamp: iso(0), currency: "USD", balance: 49.99 }),
    ];
    const t = calculateTrend(entries, "deepseek")!;
    expect(t.samples).toBe(2);
    expect(t.dailyRate).toBeNull();
    expect(t.estimatedDaysLeft).toBeNull();
  });

  test("error snapshots are excluded from the series", () => {
    const entries = [
      snap({ provider: "codex", timestamp: iso(48), balance: 10, error: "boom" }),
      snap({ provider: "codex", timestamp: iso(24), balance: 10 }),
      snap({ provider: "codex", timestamp: iso(0), balance: 10 }),
    ];
    const t = calculateTrend(entries, "codex")!;
    expect(t.samples).toBe(2);
    expect(t.dailyRate).toBe(0); // flat -> noise-suppressed burn
    expect(t.estimatedDaysLeft).toBeNull();
  });

  test("single snapshot -> trend exists but no rate", () => {
    const t = calculateTrend(
      [snap({ provider: "mimo", timestamp: iso(0), currency: "CNY", balance: 12.5 })],
      "mimo",
    )!;
    expect(t.samples).toBe(1);
    expect(t.dailyRate).toBeNull();
  });

  test("unknown provider -> null", () => {
    expect(calculateTrend([], "nope")).toBeNull();
  });
});

describe("calculateTrend — percent basis", () => {
  test("clips before reset, reports remaining % and days-left", () => {
    const entries = [
      snap({ provider: "codex", timestamp: iso(72), usedPercent: 40 }),
      snap({ provider: "codex", timestamp: iso(48), usedPercent: 95 }),
      snap({ provider: "codex", timestamp: iso(24), usedPercent: 5 }), // reset
      snap({ provider: "codex", timestamp: iso(0), usedPercent: 15 }),
    ];
    const t = calculateTrend(entries, "codex")!;
    expect(t.basis).toBe("percent");
    expect(t.remainingPercent).toBe(85);
    expect(t.dailyRate).toBeCloseTo(10, 1); // 10%/day after reset
    expect(t.estimatedDaysLeft).toBeCloseTo(8.5, 1);
    expect(t.lowBalance).toBe(false);
  });

  test("remaining under 20% -> lowBalance on percent basis", () => {
    const entries = [
      snap({ provider: "claude", timestamp: iso(48), usedPercent: 50 }),
      snap({ provider: "claude", timestamp: iso(0), usedPercent: 85 }),
    ];
    const t = calculateTrend(entries, "claude")!;
    expect(t.remainingPercent).toBe(15);
    expect(t.lowBalance).toBe(true);
  });

  test("points outside the 7-day window are ignored", () => {
    const entries = [
      snap({ provider: "codex", timestamp: iso(24 * 30), usedPercent: 100 }), // stale, must drop
      snap({ provider: "codex", timestamp: iso(48), usedPercent: 10 }),
      snap({ provider: "codex", timestamp: iso(24), usedPercent: 20 }),
      snap({ provider: "codex", timestamp: iso(0), usedPercent: 30 }),
    ];
    const t = calculateTrend(entries, "codex")!;
    expect(t.samples).toBe(3);
    expect(t.dailyRate).toBeCloseTo(10, 1);
  });
});
