import { describe, it, expect, vi, beforeEach } from "vitest";
import {
  createTelegramBot,
  formatChurnAlert,
  buildInlineKeyboard,
} from "../src/telegram";
import type { LLMDecision, ChurnContext } from "../src/types";

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

describe("formatChurnAlert", () => {
  it("includes LLM reasoning and recommendation", () => {
    const decision: LLMDecision = {
      action: "CREATE_DISCOUNT",
      reason: "High-value 8-month customer",
      confidence: 0.9,
      params: { percentage: 30, durationMonths: 3 },
    };
    const msg = formatChurnAlert(SAMPLE_CONTEXT, decision);
    expect(msg).toContain("alice@example.com");
    expect(msg).toContain("Pro Plan");
    expect(msg).toContain("8 months");
    expect(msg).toContain("$392");
    expect(msg).toContain("CREATE_DISCOUNT");
    expect(msg).toContain("High-value 8-month customer");
    expect(msg).toContain("90%");
    expect(msg).toContain("30%");
  });

  it("shows NO_ACTION recommendation", () => {
    const decision: LLMDecision = {
      action: "NO_ACTION",
      reason: "Low value",
      confidence: 0.8,
      params: {},
    };
    const msg = formatChurnAlert(SAMPLE_CONTEXT, decision);
    expect(msg).toContain("NO_ACTION");
    expect(msg).toContain("Low value");
  });

  it("shows SUGGEST_PAUSE recommendation", () => {
    const decision: LLMDecision = {
      action: "SUGGEST_PAUSE",
      reason: "Might return later",
      confidence: 0.65,
      params: {},
    };
    const msg = formatChurnAlert(SAMPLE_CONTEXT, decision);
    expect(msg).toContain("SUGGEST_PAUSE");
    expect(msg).toContain("65%");
  });
});

describe("buildInlineKeyboard", () => {
  it("returns Apply and Skip buttons for CREATE_DISCOUNT", () => {
    const keyboard = buildInlineKeyboard("sub_123", "CREATE_DISCOUNT");
    expect(keyboard).toHaveLength(1);
    expect(keyboard[0]).toHaveLength(2);
    expect(keyboard[0][0].text).toContain("Apply");
    expect(keyboard[0][0].callback_data).toBe("apply:sub_123");
    expect(keyboard[0][1].text).toContain("Skip");
    expect(keyboard[0][1].callback_data).toBe("skip:sub_123");
  });

  it("returns Pause and Skip buttons for SUGGEST_PAUSE", () => {
    const keyboard = buildInlineKeyboard("sub_456", "SUGGEST_PAUSE");
    expect(keyboard[0][0].text).toContain("Pause");
    expect(keyboard[0][0].callback_data).toBe("pause:sub_456");
    expect(keyboard[0][1].callback_data).toBe("skip:sub_456");
  });

  it("returns empty keyboard for NO_ACTION", () => {
    const keyboard = buildInlineKeyboard("sub_789", "NO_ACTION");
    expect(keyboard).toHaveLength(0);
  });
});

describe("createTelegramBot", () => {
  let mockBot: any;

  beforeEach(() => {
    mockBot = {
      sendMessage: vi.fn().mockResolvedValue({}),
      on: vi.fn(),
      onText: vi.fn(),
    };
  });

  it("sendMessage delegates to underlying bot with chat ID", async () => {
    const bot = createTelegramBot(mockBot, "12345");
    await bot.sendMessage("Hello");
    expect(mockBot.sendMessage).toHaveBeenCalledWith("12345", "Hello", undefined);
  });

  it("sendMessage passes options through", async () => {
    const bot = createTelegramBot(mockBot, "12345");
    const opts = { parse_mode: "HTML" as const };
    await bot.sendMessage("Test", opts);
    expect(mockBot.sendMessage).toHaveBeenCalledWith("12345", "Test", opts);
  });
});
