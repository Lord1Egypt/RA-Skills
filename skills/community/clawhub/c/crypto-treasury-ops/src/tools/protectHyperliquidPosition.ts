import { appConfig } from "../config.js";
import { HyperliquidTradingService } from "../services/hyperliquidTradingService.js";
import type { ToolResponse } from "../types.js";
import { buildFailure, buildSuccess } from "../utils/formatting.js";
import { createRequestId, logEvent } from "../utils/logging.js";
import { protectHyperliquidPositionInputSchema } from "../utils/validation.js";

export async function protectHyperliquidPositionTool(
  input: unknown,
  hyperliquidTradingService: HyperliquidTradingService
): Promise<ToolResponse<Record<string, unknown>>> {
  const requestId = createRequestId();
  const parsed = protectHyperliquidPositionInputSchema.parse(input);
  const quote = await hyperliquidTradingService.quoteProtection(parsed);

  if (!quote.safety.approved) {
    logEvent(requestId, "protect_hyperliquid_position", "rejected", {
      market: quote.market,
      positionSide: quote.position.side,
      size: quote.position.absoluteSize
    });
    return buildFailure("protect_hyperliquid_position", requestId, "rejected", quote.safety.reasons, {
      quote,
      safety: quote.safety
    }, quote.safety.warnings);
  }

  const dryRun = parsed.dryRun ?? appConfig.safety.dryRunDefault;
  if (dryRun) {
    logEvent(requestId, "protect_hyperliquid_position", "dry_run", {
      market: quote.market,
      positionSide: quote.position.side,
      size: quote.position.absoluteSize
    });
    return buildSuccess("protect_hyperliquid_position", requestId, "dry_run", {
      quote,
      safety: quote.safety
    }, quote.safety.warnings);
  }

  const execution = await hyperliquidTradingService.protectPosition(parsed);
  logEvent(requestId, "protect_hyperliquid_position", "success", {
    market: quote.market,
    positionSide: quote.position.side,
    size: quote.position.absoluteSize
  });

  return buildSuccess("protect_hyperliquid_position", requestId, "success", {
    quote,
    safety: quote.safety,
    execution
  }, quote.safety.warnings);
}
