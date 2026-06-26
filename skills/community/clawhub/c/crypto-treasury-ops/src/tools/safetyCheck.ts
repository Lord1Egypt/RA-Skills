import type { ToolResponse } from "../types.js";
import { buildFailure, buildSuccess } from "../utils/formatting.js";
import { createRequestId, logEvent } from "../utils/logging.js";
import { safetyCheckInputSchema } from "../utils/validation.js";
import { RiskService } from "../services/riskService.js";

export async function safetyCheckTool(
  input: unknown,
  riskService: RiskService
): Promise<ToolResponse<Record<string, unknown>>> {
  const requestId = createRequestId();
  const parsed = safetyCheckInputSchema.parse(input);
  const decision = await riskService.evaluate({
    operationType: parsed.operationType,
    chain: parsed.chain,
    tokenSymbol: parsed.token,
    amount: parsed.amount,
    destination: parsed.destination,
    feeBps: parsed.feeBps,
    slippageBps: parsed.slippageBps,
    approval: parsed.approval,
    requireGasReserve: parsed.operationType === "bridge_token" || parsed.operationType === "deposit_to_hyperliquid"
  });

  logEvent(requestId, "safety_check", decision.approved ? "success" : "rejected", {
    operationType: parsed.operationType,
    chain: parsed.chain,
    tokenSymbol: parsed.token,
    amount: parsed.amount,
    destination: parsed.destination
  });

  if (!decision.approved) {
    return buildFailure("safety_check", requestId, "rejected", decision.reasons, {
      safety: decision
    }, decision.warnings);
  }

  return buildSuccess("safety_check", requestId, "success", {
    safety: decision
  }, decision.warnings);
}
