import type { Address } from "viem";
import type { ToolResponse } from "../types.js";
import { buildSuccess } from "../utils/formatting.js";
import { createRequestId, logEvent } from "../utils/logging.js";
import { getBalancesInputSchema } from "../utils/validation.js";
import { SolanaBalanceService } from "../services/solanaBalanceService.js";
import { TokenService } from "../services/tokenService.js";

export async function getBalancesTool(
  input: unknown,
  tokenService: TokenService,
  solanaBalanceService: SolanaBalanceService
): Promise<ToolResponse<Record<string, unknown>>> {
  const requestId = createRequestId();
  const parsed = getBalancesInputSchema.parse(input);

  if (parsed.chain === "solana") {
    const solanaAddress = parsed.solanaAddress ?? parsed.walletAddress ?? "";
    const balances = await solanaBalanceService.getConfiguredBalances(solanaAddress);
    const response = buildSuccess("get_balances", requestId, "success", {
      chain: parsed.chain,
      walletAddress: solanaAddress,
      nativeBalance: balances.nativeBalance,
      stablecoinBalances: balances.stablecoinBalances
    });

    logEvent(requestId, "get_balances", "success", {
      chain: parsed.chain,
      walletAddress: solanaAddress
    });
    return response;
  }

  const walletAddress = parsed.walletAddress as Address;

  const balances = await tokenService.getConfiguredBalances(parsed.chain, walletAddress);
  const response = buildSuccess("get_balances", requestId, "success", {
    chain: parsed.chain,
    walletAddress,
    nativeBalance: balances.nativeBalance,
    stablecoinBalances: balances.stablecoinBalances
  });

  logEvent(requestId, "get_balances", "success", {
    chain: parsed.chain,
    walletAddress
  });
  return response;
}
