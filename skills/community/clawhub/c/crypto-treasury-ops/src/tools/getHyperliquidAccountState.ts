import type { ToolResponse } from "../types.js";
import { HyperliquidTradingService } from "../services/hyperliquidTradingService.js";
import { buildSuccess } from "../utils/formatting.js";
import { createRequestId, logEvent } from "../utils/logging.js";
import { getHyperliquidAccountStateInputSchema } from "../utils/validation.js";

export async function getHyperliquidAccountStateTool(
  input: unknown,
  hyperliquidTradingService: HyperliquidTradingService
): Promise<ToolResponse<Record<string, unknown>>> {
  const requestId = createRequestId();
  const parsed = getHyperliquidAccountStateInputSchema.parse(input);
  const data = await hyperliquidTradingService.getAccountState(parsed);

  logEvent(requestId, "get_hyperliquid_account_state", "success", {
    user: data.user
  });

  return buildSuccess("get_hyperliquid_account_state", requestId, "success", data);
}
