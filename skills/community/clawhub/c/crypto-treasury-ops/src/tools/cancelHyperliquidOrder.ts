import { appConfig } from "../config.js";
import type { ToolResponse } from "../types.js";
import { HyperliquidTradingService } from "../services/hyperliquidTradingService.js";
import { buildSuccess } from "../utils/formatting.js";
import { createRequestId, logEvent } from "../utils/logging.js";
import { cancelHyperliquidOrderInputSchema } from "../utils/validation.js";

export async function cancelHyperliquidOrderTool(
  input: unknown,
  hyperliquidTradingService: HyperliquidTradingService
): Promise<ToolResponse<Record<string, unknown>>> {
  const requestId = createRequestId();
  const parsed = cancelHyperliquidOrderInputSchema.parse(input);
  const preview = await hyperliquidTradingService.previewCancel(parsed);
  const dryRun = parsed.dryRun ?? appConfig.safety.dryRunDefault;

  if (dryRun) {
    logEvent(requestId, "cancel_hyperliquid_order", "dry_run", {
      market: parsed.market,
      orderId: parsed.orderId
    });
    return buildSuccess("cancel_hyperliquid_order", requestId, "dry_run", {
      preview
    });
  }

  const execution = await hyperliquidTradingService.cancelOrder(parsed);
  logEvent(requestId, "cancel_hyperliquid_order", "success", {
    market: parsed.market,
    orderId: parsed.orderId
  });

  return buildSuccess("cancel_hyperliquid_order", requestId, "success", {
    execution
  });
}
