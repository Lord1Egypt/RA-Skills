import type { LLMDecision, LLMAction, ChurnContext, TelegramBot } from "./types.js";

interface InlineButton {
  text: string;
  callback_data: string;
}

export function formatChurnAlert(ctx: ChurnContext, decision: LLMDecision): string {
  const confidencePct = Math.round(decision.confidence * 100);
  const lines: string[] = [];

  lines.push("🔔 Churn Alert — AI Analysis");
  lines.push("─".repeat(30));
  lines.push(`Customer: ${ctx.customerEmail}`);
  lines.push(`Plan: ${ctx.productName} ($${ctx.price}/mo)`);
  lines.push(`Tenure: ${ctx.tenureMonths} months`);
  lines.push(`Total Revenue: $${ctx.totalRevenue}`);
  lines.push(`Cancel Reason: ${ctx.cancelReason || "not provided"}`);
  lines.push("");
  lines.push(`🤖 Recommendation: ${decision.action}`);
  lines.push(`Confidence: ${confidencePct}%`);
  lines.push(`Reason: ${decision.reason}`);

  if (decision.action === "CREATE_DISCOUNT" && decision.params.percentage) {
    lines.push(`Discount: ${decision.params.percentage}% for ${decision.params.durationMonths ?? 3} months`);
  }

  return lines.join("\n");
}

export function buildInlineKeyboard(subscriptionId: string, action: LLMAction): InlineButton[][] {
  switch (action) {
    case "CREATE_DISCOUNT":
      return [[
        { text: "✅ Apply Discount", callback_data: `apply:${subscriptionId}` },
        { text: "⏭️ Skip", callback_data: `skip:${subscriptionId}` },
      ]];
    case "SUGGEST_PAUSE":
      return [[
        { text: "⏸️ Pause Subscription", callback_data: `pause:${subscriptionId}` },
        { text: "⏭️ Skip", callback_data: `skip:${subscriptionId}` },
      ]];
    case "NO_ACTION":
      return [];
  }
}

interface RawTelegramBot {
  sendMessage(chatId: string, text: string, options?: Record<string, unknown>): Promise<unknown>;
  on(event: string, handler: (...args: unknown[]) => void): void;
  onText(pattern: RegExp, handler: (msg: { chat: { id: number } }) => void): void;
}

export function createTelegramBot(rawBot: RawTelegramBot, chatId: string): TelegramBot {
  return {
    async sendMessage(text, options) {
      await rawBot.sendMessage(chatId, text, options);
    },
    onCallbackQuery(handler) {
      rawBot.on("callback_query", handler as (...args: unknown[]) => void);
    },
    onText(pattern, handler) {
      rawBot.onText(pattern, handler);
    },
  };
}
