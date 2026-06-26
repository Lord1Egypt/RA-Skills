import { describe, it, expect, vi, beforeEach } from "vitest";
import { executeAction, formatActionResult } from "../src/action-executor";
import type { LLMDecision, ChurnContext, ActionResult } from "../src/types";

const SAMPLE_CONTEXT: ChurnContext = {
  subscriptionId: "sub_123",
  customerId: "cus_456",
  productId: "prod_789",
  customerEmail: "alice@example.com",
  productName: "Pro Plan",
  price: 49,
  tenureMonths: 8,
  totalRevenue: 392,
  cancelReason: "too expensive",
};

describe("executeAction", () => {
  let mockCreem: any;

  beforeEach(() => {
    mockCreem = {
      discounts: {
        create: vi.fn().mockResolvedValue({ id: "disc_new", code: "RETAIN30" }),
      },
      subscriptions: {
        pause: vi.fn().mockResolvedValue({ id: "sub_123", status: "paused" }),
      },
    };
  });

  it("creates discount for CREATE_DISCOUNT action", async () => {
    const decision: LLMDecision = {
      action: "CREATE_DISCOUNT",
      reason: "Retain high-value customer",
      confidence: 0.9,
      params: { percentage: 30, durationMonths: 3 },
    };

    const result = await executeAction(decision, SAMPLE_CONTEXT, mockCreem);

    expect(mockCreem.discounts.create).toHaveBeenCalledWith({
      name: "Retention 30% off",
      type: "percentage",
      percentage: 30,
      duration: "repeating",
      durationInMonths: 3,
      appliesToProducts: ["prod_789"],
    });
    expect(result.success).toBe(true);
    expect(result.action).toBe("CREATE_DISCOUNT");
    expect(result.details).toContain("30%");
  });

  it("uses default discount params when not provided", async () => {
    const decision: LLMDecision = {
      action: "CREATE_DISCOUNT",
      reason: "test",
      confidence: 0.8,
      params: {},
    };

    await executeAction(decision, SAMPLE_CONTEXT, mockCreem);

    expect(mockCreem.discounts.create).toHaveBeenCalledWith(
      expect.objectContaining({
        percentage: 20,
        durationInMonths: 3,
      })
    );
  });

  it("pauses subscription for SUGGEST_PAUSE action", async () => {
    const decision: LLMDecision = {
      action: "SUGGEST_PAUSE",
      reason: "Customer might return",
      confidence: 0.7,
      params: {},
    };

    const result = await executeAction(decision, SAMPLE_CONTEXT, mockCreem);

    expect(mockCreem.subscriptions.pause).toHaveBeenCalledWith(SAMPLE_CONTEXT.subscriptionId);
    expect(result.success).toBe(true);
    expect(result.action).toBe("SUGGEST_PAUSE");
  });

  it("returns success with no SDK calls for NO_ACTION", async () => {
    const decision: LLMDecision = {
      action: "NO_ACTION",
      reason: "Low value customer",
      confidence: 0.95,
      params: {},
    };

    const result = await executeAction(decision, SAMPLE_CONTEXT, mockCreem);

    expect(result.success).toBe(true);
    expect(result.action).toBe("NO_ACTION");
    expect(mockCreem.discounts.create).not.toHaveBeenCalled();
    expect(mockCreem.subscriptions.pause).not.toHaveBeenCalled();
  });

  it("returns failure when Creem SDK throws", async () => {
    mockCreem.discounts.create.mockRejectedValue(new Error("Product not found"));

    const decision: LLMDecision = {
      action: "CREATE_DISCOUNT",
      reason: "test",
      confidence: 0.8,
      params: { percentage: 20, durationMonths: 1 },
    };

    const result = await executeAction(decision, SAMPLE_CONTEXT, mockCreem);

    expect(result.success).toBe(false);
    expect(result.details).toContain("Product not found");
  });

  it("returns failure when pause throws", async () => {
    mockCreem.subscriptions.pause.mockRejectedValue(new Error("Subscription not found"));

    const decision: LLMDecision = {
      action: "SUGGEST_PAUSE",
      reason: "test",
      confidence: 0.7,
      params: {},
    };

    const result = await executeAction(decision, SAMPLE_CONTEXT, mockCreem);

    expect(result.success).toBe(false);
    expect(result.details).toContain("Subscription not found");
  });
});

describe("formatActionResult", () => {
  it("formats successful discount creation", () => {
    const result: ActionResult = {
      success: true,
      action: "CREATE_DISCOUNT",
      details: "Created 30% discount for 3 months",
    };
    const msg = formatActionResult(result, SAMPLE_CONTEXT);
    expect(msg).toContain("✅");
    expect(msg).toContain("30%");
    expect(msg).toContain("alice@example.com");
  });

  it("formats successful pause", () => {
    const result: ActionResult = {
      success: true,
      action: "SUGGEST_PAUSE",
      details: "Subscription paused",
    };
    const msg = formatActionResult(result, SAMPLE_CONTEXT);
    expect(msg).toContain("✅");
    expect(msg).toContain("paused");
  });

  it("formats no action taken", () => {
    const result: ActionResult = {
      success: true,
      action: "NO_ACTION",
      details: "No action taken",
    };
    const msg = formatActionResult(result, SAMPLE_CONTEXT);
    expect(msg).toContain("ℹ️");
    expect(msg).toContain("No action");
  });

  it("formats failure with error details", () => {
    const result: ActionResult = {
      success: false,
      action: "CREATE_DISCOUNT",
      details: "Error: Product not found",
    };
    const msg = formatActionResult(result, SAMPLE_CONTEXT);
    expect(msg).toContain("❌");
    expect(msg).toContain("Product not found");
  });
});
