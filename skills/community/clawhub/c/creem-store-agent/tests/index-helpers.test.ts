import { describe, it, expect, vi } from "vitest";
import { extractChurnContext, shouldAutoExecute } from "../src/index-helpers";
import type { CreemWebhookPayload, LLMDecision } from "../src/types";

describe("extractChurnContext", () => {
  function makeCreemMock(overrides: Record<string, any> = {}) {
    return {
      subscriptions: {
        get: vi.fn().mockResolvedValue({
          id: "sub_123",
          product: { id: "prod_789", name: "Pro Plan", price: 4900 },
          customer: { id: "cus_456", email: "alice@example.com" },
          createdAt: new Date("2025-07-17"),
          status: "canceled",
          ...overrides.subscription,
        }),
      },
      transactions: {
        search: vi.fn().mockResolvedValue({
          items: [
            { amount: 4900 },
            { amount: 4900 },
            { amount: 4900 },
          ],
          ...overrides.transactions,
        }),
      },
    };
  }

  it("extracts complete churn context from Creem SDK responses", async () => {
    const creem = makeCreemMock();
    const payload: CreemWebhookPayload = {
      eventType: "subscription.canceled",
      id: "evt_1",
      created_at: 1742198400,
      object: { id: "sub_123", customerId: "cus_456", cancelReason: "too expensive" },
    };

    const ctx = await extractChurnContext(payload, creem as any);

    expect(ctx.subscriptionId).toBe("sub_123");
    expect(ctx.customerId).toBe("cus_456");
    expect(ctx.productId).toBe("prod_789");
    expect(ctx.customerEmail).toBe("alice@example.com");
    expect(ctx.productName).toBe("Pro Plan");
    expect(ctx.price).toBe(49);
    expect(ctx.tenureMonths).toBeGreaterThan(0);
    expect(ctx.totalRevenue).toBe(147);
    expect(ctx.cancelReason).toBe("too expensive");
  });

  it("calls creem.subscriptions.get with subscriptionId string", async () => {
    const creem = makeCreemMock();
    const payload: CreemWebhookPayload = {
      eventType: "subscription.canceled",
      id: "evt_2",
      created_at: 1742198400,
      object: { id: "sub_abc", customerId: "cus_def" },
    };

    await extractChurnContext(payload, creem as any);

    expect(creem.subscriptions.get).toHaveBeenCalledWith("sub_abc");
  });

  it("calls creem.transactions.search with customerId from subscription entity", async () => {
    const creem = makeCreemMock();
    const payload: CreemWebhookPayload = {
      eventType: "subscription.canceled",
      id: "evt_3",
      created_at: 1742198400,
      object: { id: "sub_123", customerId: "cus_456" },
    };

    await extractChurnContext(payload, creem as any);

    expect(creem.transactions.search).toHaveBeenCalledWith("cus_456");
  });

  it("handles missing cancelReason gracefully", async () => {
    const creem = makeCreemMock();
    const payload: CreemWebhookPayload = {
      eventType: "subscription.canceled",
      id: "evt_5",
      created_at: 1742198400,
      object: { id: "sub_123", customerId: "cus_456" },
    };

    const ctx = await extractChurnContext(payload, creem as any);

    expect(ctx.cancelReason).toBe("not provided");
  });

  it("handles empty transactions list", async () => {
    const creem = makeCreemMock({ transactions: { items: [] } });
    const payload: CreemWebhookPayload = {
      eventType: "subscription.canceled",
      id: "evt_6",
      created_at: 1742198400,
      object: { id: "sub_123", customerId: "cus_456" },
    };

    const ctx = await extractChurnContext(payload, creem as any);

    expect(ctx.totalRevenue).toBe(0);
  });

  it("handles missing customer email", async () => {
    const creem = makeCreemMock({ subscription: { customer: { id: "cus_456" } } });
    const payload: CreemWebhookPayload = {
      eventType: "subscription.canceled",
      id: "evt_7",
      created_at: 1742198400,
      object: { id: "sub_123", customerId: "cus_456" },
    };

    const ctx = await extractChurnContext(payload, creem as any);

    expect(ctx.customerEmail).toBe("unknown");
  });

  it("handles string (non-expanded) product and customer", async () => {
    const creem = makeCreemMock({
      subscription: {
        product: "prod_def",
        customer: "cust_ghi",
        createdAt: new Date("2026-02-01"),
      },
    });
    const payload: CreemWebhookPayload = {
      eventType: "subscription.canceled",
      id: "evt_8",
      created_at: 1742198400,
      object: { id: "sub_123" },
    };

    const ctx = await extractChurnContext(payload, creem as any);

    expect(ctx.productId).toBe("prod_def");
    expect(ctx.productName).toBe("Unknown Plan");
    expect(ctx.price).toBe(0);
    expect(ctx.customerEmail).toBe("unknown");
  });
});

describe("shouldAutoExecute", () => {
  it("returns true when confidence equals threshold (0.8)", () => {
    const decision: LLMDecision = {
      action: "CREATE_DISCOUNT",
      reason: "test",
      confidence: 0.8,
      params: { percentage: 20, durationMonths: 3 },
    };
    expect(shouldAutoExecute(decision, 0.8)).toBe(true);
  });

  it("returns false when confidence is below threshold (0.79)", () => {
    const decision: LLMDecision = {
      action: "CREATE_DISCOUNT",
      reason: "test",
      confidence: 0.79,
      params: { percentage: 20, durationMonths: 3 },
    };
    expect(shouldAutoExecute(decision, 0.8)).toBe(false);
  });

  it("returns true when confidence is above threshold (0.81)", () => {
    const decision: LLMDecision = {
      action: "CREATE_DISCOUNT",
      reason: "test",
      confidence: 0.81,
      params: { percentage: 20, durationMonths: 3 },
    };
    expect(shouldAutoExecute(decision, 0.8)).toBe(true);
  });

  it("returns true for SUGGEST_PAUSE above threshold", () => {
    const decision: LLMDecision = {
      action: "SUGGEST_PAUSE",
      reason: "test",
      confidence: 0.9,
      params: {},
    };
    expect(shouldAutoExecute(decision, 0.8)).toBe(true);
  });

  it("never auto-executes NO_ACTION regardless of confidence", () => {
    const decision: LLMDecision = {
      action: "NO_ACTION",
      reason: "Let them go",
      confidence: 0.99,
      params: {},
    };
    expect(shouldAutoExecute(decision, 0.8)).toBe(false);
  });

  it("never auto-executes NO_ACTION even with confidence 1.0", () => {
    const decision: LLMDecision = {
      action: "NO_ACTION",
      reason: "test",
      confidence: 1.0,
      params: {},
    };
    expect(shouldAutoExecute(decision, 0.5)).toBe(false);
  });

  it("works with custom threshold", () => {
    const decision: LLMDecision = {
      action: "CREATE_DISCOUNT",
      reason: "test",
      confidence: 0.6,
      params: { percentage: 20, durationMonths: 3 },
    };
    expect(shouldAutoExecute(decision, 0.5)).toBe(true);
    expect(shouldAutoExecute(decision, 0.7)).toBe(false);
  });
});
