import type { ChurnContext, LLMDecision, LLMAction } from "./types.js";

const VALID_ACTIONS: LLMAction[] = ["CREATE_DISCOUNT", "SUGGEST_PAUSE", "NO_ACTION"];

export function parseLLMResponse(raw: string): LLMDecision | null {
  try {
    let jsonStr = raw;
    const codeBlockMatch = raw.match(/```(?:json)?\s*\n?([\s\S]*?)\n?```/);
    if (codeBlockMatch) {
      jsonStr = codeBlockMatch[1].trim();
    }

    const parsed = JSON.parse(jsonStr);

    if (
      !parsed.action ||
      !VALID_ACTIONS.includes(parsed.action) ||
      typeof parsed.reason !== "string" ||
      typeof parsed.confidence !== "number" ||
      typeof parsed.params !== "object"
    ) {
      return null;
    }

    return {
      action: parsed.action,
      reason: parsed.reason,
      confidence: Math.max(0, Math.min(1, parsed.confidence)),
      params: parsed.params ?? {},
    };
  } catch {
    return null;
  }
}

export function buildChurnPrompt(ctx: ChurnContext): string {
  return `You are a SaaS retention analyst. A customer is about to churn. Analyze and recommend ONE action.

Customer: ${ctx.customerEmail}
Plan: ${ctx.productName} ($${ctx.price}/mo)
Tenure: ${ctx.tenureMonths} months
Total Revenue: $${ctx.totalRevenue}
Cancel Reason: ${ctx.cancelReason || "not provided"}

Available actions (pick exactly one):
- CREATE_DISCOUNT: Create a retention discount. Params: { percentage: 10-50, durationMonths: 1-6 }
- SUGGEST_PAUSE: Pause subscription instead of cancel. Params: {}
- NO_ACTION: Let the customer go. Params: {}

Rules:
- High-value customers (>$500 total or >6 months): prefer CREATE_DISCOUNT with 20-40%
- Low-tenure (<2 months) or low-value: prefer NO_ACTION
- Medium cases: consider SUGGEST_PAUSE
- Include confidence (0-1) in your assessment

Respond in JSON only:
{"action": "CREATE_DISCOUNT|SUGGEST_PAUSE|NO_ACTION", "reason": "one sentence", "confidence": 0.0-1.0, "params": {...}}`;
}

export function fallbackDecision(ctx: ChurnContext): LLMDecision {
  const isHighValue = ctx.totalRevenue > 500 || ctx.tenureMonths > 6;

  if (isHighValue) {
    return {
      action: "CREATE_DISCOUNT",
      reason: "Rule-based: high-value customer retention attempt",
      confidence: 0.5,
      params: { percentage: 20, durationMonths: 3 },
    };
  }

  return {
    action: "NO_ACTION",
    reason: "Rule-based: low-tenure or low-value customer",
    confidence: 0.5,
    params: {},
  };
}

interface AnthropicClient {
  messages: {
    create(params: {
      model: string;
      max_tokens: number;
      messages: Array<{ role: string; content: string }>;
    }): Promise<{
      content: Array<{ type: string; text: string }>;
    }>;
  };
}

export async function analyzeChurn(
  ctx: ChurnContext,
  client: AnthropicClient,
): Promise<LLMDecision> {
  try {
    const response = await client.messages.create({
      model: "claude-haiku-4-5",
      max_tokens: 256,
      messages: [{ role: "user", content: buildChurnPrompt(ctx) }],
    });

    const text = response.content[0]?.text ?? "";
    const parsed = parseLLMResponse(text);

    if (parsed) return parsed;

    return fallbackDecision(ctx);
  } catch {
    return fallbackDecision(ctx);
  }
}
