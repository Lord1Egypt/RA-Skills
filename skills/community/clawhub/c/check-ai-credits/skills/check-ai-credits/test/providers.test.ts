import { describe, expect, test } from "bun:test";
import { parseDeepseek } from "../src/providers/deepseek";
import { calcDeepinfra } from "../src/providers/deepinfra";
import { baseSnapshot, errorSnapshot } from "../src/core/snapshot";
import { registry } from "../src/registry";

describe("parseDeepseek", () => {
  test("maps balance_infos[0]", () => {
    const snap = parseDeepseek({
      is_available: true,
      balance_infos: [
        { currency: "USD", total_balance: "3.25", granted_balance: "1.00", topped_up_balance: "2.25" },
      ],
    });
    expect(snap.provider).toBe("deepseek");
    expect(snap.source).toBe("api");
    expect(snap.currency).toBe("USD");
    expect(snap.balance).toBe(3.25);
    expect(snap.error).toBeNull();
    expect(snap.details).toMatchObject({
      isAvailable: true,
      grantedBalance: 1.0,
      toppedUpBalance: 2.25,
    });
    expect(typeof snap.timestamp).toBe("string");
  });

  test("empty response -> null balance, no crash", () => {
    const snap = parseDeepseek({});
    expect(snap.balance).toBeNull();
    expect(snap.currency).toBe("USD");
  });
});

describe("calcDeepinfra", () => {
  test("credit pool minus unbilled = spendable; usage cents -> USD", () => {
    // mirrors the verified 2026-09 numbers: pool $27.19, month usage $17.99
    const snap = calcDeepinfra(
      { stripe_balance: -27.19, recent: 17.99, suspended: false, topup: false },
      { months: [{ total_cost: 1799, period: "2026-09-01/2026-09-30", invoice_id: "in_1" }] },
      { limit: 0 },
    );
    expect(snap.balance).toBeCloseTo(9.2, 6);
    expect(snap.currency).toBe("USD");
    expect(snap.monthCost).toBeCloseTo(17.99, 6);
    expect(snap.monthPeriod).toBe("2026-09-01/2026-09-30");
    expect(snap.details).toMatchObject({ creditUsd: 27.19, unbilledUsd: 17.99, owedUsd: 0, limitUsd: null });
  });

  test("positive stripe_balance is money owed, spendable floors at credit=0", () => {
    const snap = calcDeepinfra({ stripe_balance: 3.5, recent: 1.0 }, null, null);
    expect(snap.details).toMatchObject({ owedUsd: 3.5, creditUsd: 0, spendableUsd: -1 });
    // negative spendable keeps honest (owed money, no credit) — assert we didn't fake 0
    expect(snap.balance).toBeLessThan(0);
  });

  test("topup cents conversion + models breakdown", () => {
    const snap = calcDeepinfra(
      { stripe_balance: -10, recent: 0, topup: true, topup_amount: 500, topup_threshold: 500 },
      {
        months: [
          {
            total_cost: 300,
            period: "2026-09",
            items: [
              { model: { model_name: "big-model" }, cost: 250 },
              { model: { model_name: "small-model" }, cost: 50 },
            ],
          },
        ],
      },
      null,
      true,
    );
    expect(snap.details).toMatchObject({
      topup: { enabled: true, amountUsd: 5, thresholdUsd: 5, failed: false },
    });
    expect((snap.details as { models: { model: string; costUsd: number }[] }).models).toEqual([
      { model: "big-model", costUsd: 2.5 },
      { model: "small-model", costUsd: 0.5 },
    ]);
  });

  test("monthCost from cents with no usage endpoint", () => {
    const snap = calcDeepinfra({ stripe_balance: -5, recent: 0 }, null, { limit: -1 });
    expect(snap.monthCost).toBeNull();
    expect(snap.details).toMatchObject({ limitUsd: null });
  });
});

describe("snapshot schema guarantees", () => {
  test("errorSnapshot carries all required keys", () => {
    const snap = errorSnapshot("x", "boom", "api", "https://example.com");
    for (const key of ["provider", "source", "timestamp", "balance", "usedPercent", "resetsAt", "monthCost", "monthPeriod", "error"]) {
      expect(key in snap).toBe(true);
    }
    expect(snap.authHint).toBe("https://example.com");
  });

  test("baseSnapshot carries all required keys", () => {
    const snap = baseSnapshot("y", "api");
    expect(snap.error).toBeNull();
    expect(typeof snap.timestamp).toBe("string");
    expect(snap.balance).toBeNull();
  });
});

describe("registry", () => {
  test("exactly 10 unique provider ids", () => {
    expect(registry.length).toBe(10);
    const ids = registry.map((p) => p.id);
    expect(new Set(ids).size).toBe(10);
    expect(ids).toEqual([
      "deepseek", "deepinfra", "codex", "grok", "mimo",
      "claude", "gemini", "kimi", "openrouter", "apikeyfun",
    ]);
  });

  test("every provider has a label and detect()", () => {
    for (const p of registry) {
      expect(p.label.length).toBeGreaterThan(0);
      expect(typeof p.detect).toBe("function");
      expect(typeof p.fetch).toBe("function");
    }
  });
});
