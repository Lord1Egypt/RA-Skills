import type { LLMDecision, ChurnContext, ActionResult } from "./types.js";

interface CreemClient {
  discounts: {
    create(params: {
      name: string;
      type: string;
      percentage: number;
      duration: string;
      durationInMonths: number;
      appliesToProducts: string[];
    }): Promise<{ id: string; code: string }>;
  };
  subscriptions: {
    pause(id: string): Promise<{ id: string; status: string }>;
  };
}

export async function executeAction(
  decision: LLMDecision,
  ctx: ChurnContext,
  creem: CreemClient,
): Promise<ActionResult> {
  try {
    switch (decision.action) {
      case "CREATE_DISCOUNT": {
        const percentage = decision.params.percentage ?? 20;
        const months = decision.params.durationMonths ?? 3;

        const discount = await creem.discounts.create({
          name: `Retention ${percentage}% off`,
          type: "percentage",
          percentage,
          duration: "repeating",
          durationInMonths: months,
          appliesToProducts: [ctx.productId],
        });

        return {
          success: true,
          action: "CREATE_DISCOUNT",
          details: `Created ${percentage}% discount for ${months} months (code: ${discount.code})`,
        };
      }

      case "SUGGEST_PAUSE": {
        await creem.subscriptions.pause(ctx.subscriptionId);

        return {
          success: true,
          action: "SUGGEST_PAUSE",
          details: "Subscription paused successfully",
        };
      }

      case "NO_ACTION": {
        return {
          success: true,
          action: "NO_ACTION",
          details: "No action taken — customer will churn naturally",
        };
      }
    }
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    return {
      success: false,
      action: decision.action,
      details: `Failed to execute ${decision.action}: ${message}`,
    };
  }
}

export function formatActionResult(result: ActionResult, ctx: ChurnContext): string {
  const lines: string[] = [];

  if (!result.success) {
    lines.push(`❌ Action Failed: ${result.action}`);
    lines.push(`Customer: ${ctx.customerEmail}`);
    lines.push(`Error: ${result.details}`);
    return lines.join("\n");
  }

  switch (result.action) {
    case "CREATE_DISCOUNT":
      lines.push(`✅ Discount Created`);
      lines.push(`Customer: ${ctx.customerEmail}`);
      lines.push(`${result.details}`);
      break;
    case "SUGGEST_PAUSE":
      lines.push(`✅ Subscription Paused`);
      lines.push(`Customer: ${ctx.customerEmail}`);
      lines.push(`${result.details}`);
      break;
    case "NO_ACTION":
      lines.push(`ℹ️ No Action Taken`);
      lines.push(`Customer: ${ctx.customerEmail}`);
      lines.push(`${result.details}`);
      break;
  }

  return lines.join("\n");
}
