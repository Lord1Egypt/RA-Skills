import type { ToolResponse } from "../types.js";
import { HyperliquidTradingService } from "../services/hyperliquidTradingService.js";
import { buildSuccess } from "../utils/formatting.js";
import { createRequestId, logEvent } from "../utils/logging.js";
import { getHyperliquidMarketStateInputSchema } from "../utils/validation.js";

export async function getHyperliquidMarketStateTool(
  input: unknown,
  hyperliquidTradingService: HyperliquidTradingService
): Promise<ToolResponse<Record<string, unknown>>> {
  const requestId = createRequestId();
  const parsed = getHyperliquidMarketStateInputSchema.parse(input);
  const data = await hyperliquidTradingService.getMarketState(parsed);

  logEvent(requestId, "get_hyperliquid_market_state", "success", {
    market: parsed.market
  });

  return buildSuccess("get_hyperliquid_market_state", requestId, "success", data);
}
