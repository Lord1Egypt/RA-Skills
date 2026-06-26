import { appConfig } from "../config.js";
import type { ToolResponse } from "../types.js";
import { HyperliquidTradingService } from "../services/hyperliquidTradingService.js";
import { buildFailure, buildSuccess } from "../utils/formatting.js";
import { createRequestId, logEvent } from "../utils/logging.js";
import { placeHyperliquidOrderInputSchema } from "../utils/validation.js";

export async function placeHyperliquidOrderTool(
  input: unknown,
  hyperliquidTradingService: HyperliquidTradingService
): Promise<ToolResponse<Record<string, unknown>>> {
  const requestId = createRequestId();
  const parsed = placeHyperliquidOrderInputSchema.parse(input);
  const quote = await hyperliquidTradingService.quoteOrder(parsed);

  if (!quote.safety.approved) {
    logEvent(requestId, "place_hyperliquid_order", "rejected", {
      market: quote.market,
      side: quote.side,
      size: quote.size,
      orderType: quote.orderType,
      notionalUsd: Number(quote.notionalUsd),
      reduceOnly: quote.reduceOnly
    });
    return buildFailure("place_hyperliquid_order", requestId, "rejected", quote.safety.reasons, {
      quote,
      safety: quote.safety
    }, quote.safety.warnings);
  }

  const dryRun = parsed.dryRun ?? appConfig.safety.dryRunDefault;
  if (dryRun) {
    logEvent(requestId, "place_hyperliquid_order", "dry_run", {
      market: quote.market,
      side: quote.side,
      size: quote.size,
      orderType: quote.orderType,
      notionalUsd: Number(quote.notionalUsd),
      reduceOnly: quote.reduceOnly
    });
    return buildSuccess("place_hyperliquid_order", requestId, "dry_run", {
      quote,
      safety: quote.safety
    }, quote.safety.warnings);
  }

  const execution = await hyperliquidTradingService.placeOrder(parsed);
  logEvent(requestId, "place_hyperliquid_order", "success", {
    market: quote.market,
    side: quote.side,
    size: quote.size,
    orderType: quote.orderType,
    notionalUsd: Number(quote.notionalUsd),
    reduceOnly: quote.reduceOnly
  });

  return buildSuccess("place_hyperliquid_order", requestId, "success", {
    quote,
    safety: quote.safety,
    execution
  }, quote.safety.warnings);
}
