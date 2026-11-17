import { describe, expect, test } from "bun:test";
import { extractPluginSnapshot, extractUsageSnapshot } from "../src/core/codexbar";
import { detectAuthError, LOGIN_URLS } from "../src/core/auth";

const usageItem = {
  provider: "claude",
  source: "web",
  error: null,
  pace: { primary: { summary: "steady", willLastToReset: true, etaSeconds: 3600 } },
  usage: {
    primary: { usedPercent: 42.5, resetsAt: "2026-09-25T00:00:00Z", windowMinutes: 10080, resetDescription: "weekly" },
  },
};

describe("extractUsageSnapshot", () => {
  test("maps primary usage into schema", () => {
    const snap = extractUsageSnapshot(usageItem);
    expect(snap.provider).toBe("claude");
    expect(snap.usedPercent).toBe(42.5);
    expect(snap.resetsAt).toBe("2026-09-25T00:00:00Z");
    expect(snap.error).toBeNull();
    expect(typeof snap.timestamp).toBe("string");
    expect(snap.details).toMatchObject({
      resetDescription: "weekly",
      windowMinutes: 10080,
      paceSummary: "steady",
    });
  });

  test("mimo wallet fields surface as balance/currency", () => {
    const snap = extractUsageSnapshot({
      provider: "mimo",
      source: "web",
      usage: { primary: { usedPercent: null }, mimoUsage: { balance: 6.38, currency: "CNY", tokenUsed: 100 } },
    });
    expect(snap.balance).toBe(6.38);
    expect(snap.currency).toBe("CNY");
  });

  test("auth-expired error attaches login URL", () => {
    const snap = extractUsageSnapshot({
      provider: "gemini",
      error: "browser session expired",
      usage: {},
    });
    expect(snap.error).toBe("browser session expired");
    expect(snap.authHint).toBe(LOGIN_URLS.gemini);
  });

  test("object-shaped CodexBar error is normalized to its message", () => {
    const snap = extractUsageSnapshot({
      provider: "openrouter",
      source: "auto",
      error: { kind: "provider", message: "OpenRouter API error: HTTP 401", code: 1 },
    });
    expect(snap.error).toBe("OpenRouter API error: HTTP 401");
    expect(snap.authHint).toBe(LOGIN_URLS.openrouter);
  });
});

describe("extractPluginSnapshot", () => {
  test("apikey.fun shape: providerCost + details rows", () => {
    const snap = extractPluginSnapshot(
      {
        providerCost: { balance: 12.34, currencyCode: "USD", used: 1.5, period: "2026-09" },
        details: [
          {
            rows: [
              { label: "Balance", value: "$12.34 (shared)" },
              { label: "Today", value: "$0.42" },
              { label: "All time", value: "$310.55" },
            ],
          },
        ],
      },
      "apikeyfun",
    );
    expect(snap.balance).toBe(12.34);
    expect(snap.currency).toBe("USD");
    expect(snap.details).toMatchObject({
      windowSpend: 1.5,
      windowPeriod: "2026-09",
      todayCost: 0.42,
      allTimeCost: 310.55,
    });
    expect(snap.error).toBeNull();
  });

  test("null plugin payload -> error snapshot", () => {
    const snap = extractPluginSnapshot(null, "apikeyfun");
    expect(snap.error).toContain("plugin fetch");
    expect(snap.provider).toBe("apikeyfun");
  });
});

describe("detectAuthError", () => {
  test("pattern match returns provider login URL", () => {
    expect(detectAuthError({ provider: "codex", error: "auth token is invalid" })).toBe(
      LOGIN_URLS.codex ?? null,
    );
  });

  test("case-insensitive", () => {
    expect(detectAuthError({ provider: "grok", error: "Login Required" })).toBe(LOGIN_URLS.grok ?? null);
  });

  test("unrelated error -> null", () => {
    expect(detectAuthError({ provider: "codex", error: "rate limited" })).toBeNull();
  });

  test("identity.loginMethod expired -> login URL", () => {
    expect(
      detectAuthError({ provider: "kimi", usage: { identity: { loginMethod: "expired" } } }),
    ).toBe(LOGIN_URLS.kimi ?? null);
  });
});
