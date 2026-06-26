import { describe, it, expect, vi, beforeEach } from "vitest";
import {
  parseLLMResponse,
  buildChurnPrompt,
  analyzeChurn,
  fallbackDecision,
} from "../src/llm-analyzer";
import type { ChurnContext } from "../src/types";

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

describe("parseLLMResponse", () => {
  it("parses valid CREATE_DISCOUNT response", () => {
    const raw = JSON.stringify({
      action: "CREATE_DISCOUNT",
      reason: "High-value customer worth retaining",
      confidence: 0.9,
      params: { percentage: 30, durationMonths: 3 },
    });
    const result = parseLLMResponse(raw);
    expect(result).toEqual({
      action: "CREATE_DISCOUNT",
      reason: "High-value customer worth retaining",
      confidence: 0.9,
      params: { percentage: 30, durationMonths: 3 },
    });
  });

  it("parses valid SUGGEST_PAUSE response", () => {
    const raw = JSON.stringify({
      action: "SUGGEST_PAUSE",
      reason: "Medium-value, might return",
      confidence: 0.7,
      params: {},
    });
    const result = parseLLMResponse(raw);
    expect(result?.action).toBe("SUGGEST_PAUSE");
    expect(result?.params).toEqual({});
  });

  it("parses valid NO_ACTION response", () => {
    const raw = JSON.stringify({
      action: "NO_ACTION",
      reason: "Low tenure, low value",
      confidence: 0.95,
      params: {},
    });
    const result = parseLLMResponse(raw);
    expect(result?.action).toBe("NO_ACTION");
  });

  it("returns null for invalid JSON", () => {
    expect(parseLLMResponse("not json at all")).toBeNull();
  });

  it("returns null for JSON with invalid action", () => {
    const raw = JSON.stringify({ action: "INVALID", reason: "test", confidence: 0.5, params: {} });
    expect(parseLLMResponse(raw)).toBeNull();
  });

  it("returns null for JSON missing required fields", () => {
    const raw = JSON.stringify({ action: "CREATE_DISCOUNT" });
    expect(parseLLMResponse(raw)).toBeNull();
  });

  it("extracts JSON from markdown code block", () => {
    const raw = '```json\n{"action":"NO_ACTION","reason":"test","confidence":0.8,"params":{}}\n```';
    const result = parseLLMResponse(raw);
    expect(result?.action).toBe("NO_ACTION");
  });

  it("clamps negative confidence to 0", () => {
    const raw = JSON.stringify({
      action: "NO_ACTION",
      reason: "test",
      confidence: -0.5,
      params: {},
    });
    const result = parseLLMResponse(raw);
    expect(result?.confidence).toBe(0);
  });

  it("passes through valid confidence unchanged", () => {
    const raw = JSON.stringify({
      action: "NO_ACTION",
      reason: "test",
      confidence: 0.5,
      params: {},
    });
    const result = parseLLMResponse(raw);
    expect(result?.confidence).toBe(0.5);
  });

  it("clamps confidence above 1 to 1", () => {
    const raw = JSON.stringify({
      action: "CREATE_DISCOUNT",
      reason: "test",
      confidence: 1.5,
      params: { percentage: 20, durationMonths: 1 },
    });
    const result = parseLLMResponse(raw);
    expect(result?.confidence).toBe(1);
  });
});

describe("buildChurnPrompt", () => {
  it("includes customer email", () => {
    const prompt = buildChurnPrompt(SAMPLE_CONTEXT);
    expect(prompt).toContain("alice@example.com");
  });

  it("includes product name and price", () => {
    const prompt = buildChurnPrompt(SAMPLE_CONTEXT);
    expect(prompt).toContain("Pro Plan");
    expect(prompt).toContain("$49");
  });

  it("includes tenure and total revenue", () => {
    const prompt = buildChurnPrompt(SAMPLE_CONTEXT);
    expect(prompt).toContain("8 months");
    expect(prompt).toContain("$392");
  });

  it("includes cancel reason", () => {
    const prompt = buildChurnPrompt(SAMPLE_CONTEXT);
    expect(prompt).toContain("too expensive");
  });

  it("mentions all 3 available actions", () => {
    const prompt = buildChurnPrompt(SAMPLE_CONTEXT);
    expect(prompt).toContain("CREATE_DISCOUNT");
    expect(prompt).toContain("SUGGEST_PAUSE");
    expect(prompt).toContain("NO_ACTION");
  });

  it("requests JSON output", () => {
    const prompt = buildChurnPrompt(SAMPLE_CONTEXT);
    expect(prompt).toContain("JSON");
  });

  it("requests confidence field", () => {
    const prompt = buildChurnPrompt(SAMPLE_CONTEXT);
    expect(prompt).toContain("confidence");
  });
});

describe("fallbackDecision", () => {
  it("recommends CREATE_DISCOUNT for high-tenure customer (>6 months)", () => {
    const result = fallbackDecision({ ...SAMPLE_CONTEXT, tenureMonths: 7, totalRevenue: 600 });
    expect(result.action).toBe("CREATE_DISCOUNT");
    expect(result.params.percentage).toBe(20);
    expect(result.params.durationMonths).toBe(3);
  });

  it("recommends CREATE_DISCOUNT for high-revenue customer (>$500)", () => {
    const result = fallbackDecision({ ...SAMPLE_CONTEXT, tenureMonths: 3, totalRevenue: 600 });
    expect(result.action).toBe("CREATE_DISCOUNT");
  });

  it("recommends NO_ACTION for low-tenure low-value customer", () => {
    const result = fallbackDecision({ ...SAMPLE_CONTEXT, tenureMonths: 1, totalRevenue: 49 });
    expect(result.action).toBe("NO_ACTION");
  });

  it("sets confidence to 0.5 for rule-based fallback", () => {
    const result = fallbackDecision(SAMPLE_CONTEXT);
    expect(result.confidence).toBe(0.5);
  });
});

describe("analyzeChurn", () => {
  let mockAnthropicClient: any;

  beforeEach(() => {
    mockAnthropicClient = {
      messages: {
        create: vi.fn(),
      },
    };
  });

  it("returns parsed LLM decision on success", async () => {
    const llmResponse = {
      action: "CREATE_DISCOUNT",
      reason: "Valuable customer",
      confidence: 0.85,
      params: { percentage: 25, durationMonths: 3 },
    };
    mockAnthropicClient.messages.create.mockResolvedValue({
      content: [{ type: "text", text: JSON.stringify(llmResponse) }],
    });

    const result = await analyzeChurn(SAMPLE_CONTEXT, mockAnthropicClient);

    expect(result.action).toBe("CREATE_DISCOUNT");
    expect(result.confidence).toBe(0.85);
    expect(result.params.percentage).toBe(25);
  });

  it("uses claude-haiku-4-5 model", async () => {
    mockAnthropicClient.messages.create.mockResolvedValue({
      content: [{ type: "text", text: JSON.stringify({ action: "NO_ACTION", reason: "test", confidence: 0.9, params: {} }) }],
    });

    await analyzeChurn(SAMPLE_CONTEXT, mockAnthropicClient);

    expect(mockAnthropicClient.messages.create).toHaveBeenCalledWith(
      expect.objectContaining({ model: "claude-haiku-4-5" })
    );
  });

  it("falls back to rule-based on API error", async () => {
    mockAnthropicClient.messages.create.mockRejectedValue(new Error("API timeout"));

    const result = await analyzeChurn(SAMPLE_CONTEXT, mockAnthropicClient);

    expect(result.action).toBe("CREATE_DISCOUNT");
    expect(result.confidence).toBe(0.5);
  });

  it("falls back to rule-based on unparseable response", async () => {
    mockAnthropicClient.messages.create.mockResolvedValue({
      content: [{ type: "text", text: "I cannot make a decision in JSON format sorry" }],
    });

    const result = await analyzeChurn(SAMPLE_CONTEXT, mockAnthropicClient);

    expect(result.confidence).toBe(0.5);
  });
});
