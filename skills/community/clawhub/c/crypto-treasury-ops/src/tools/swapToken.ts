import { appConfig } from "../config.js";
import type { ToolResponse } from "../types.js";
import { buildFailure, buildSuccess } from "../utils/formatting.js";
import { createRequestId, logEvent } from "../utils/logging.js";
import { swapTokenInputSchema } from "../utils/validation.js";
import { RiskService } from "../services/riskService.js";
import { SwapService } from "../services/swapService.js";
import { TokenService } from "../services/tokenService.js";
import { WalletService } from "../services/walletService.js";

export async function swapTokenTool(
  input: unknown,
  walletService: WalletService,
  tokenService: TokenService,
  swapService: SwapService,
  riskService: RiskService
): Promise<ToolResponse<Record<string, unknown>>> {
  const requestId = createRequestId();
  const parsed = swapTokenInputSchema.parse(input);
  const treasuryAddress = walletService.getTreasuryAddress();
  const recipient = parsed.recipient ?? treasuryAddress;
  const sellToken = await tokenService.resolveToken(parsed.chain, parsed.sellToken);
  const buyToken = await tokenService.resolveToken(parsed.chain, parsed.buyToken);

  if (
    sellToken.symbol.toUpperCase() === buyToken.symbol.toUpperCase() &&
    sellToken.address?.toLowerCase() === buyToken.address?.toLowerCase()
  ) {
    return buildFailure("swap_token", requestId, "rejected", [
      "sellToken and buyToken must be different."
    ]);
  }

  const sellAmountRaw = tokenService.amountToRaw(parsed.amount, sellToken);
  const balance = await tokenService.getTokenBalance(parsed.chain, treasuryAddress, sellToken);
  if (BigInt(balance.rawAmount) < sellAmountRaw) {
    return buildFailure("swap_token", requestId, "rejected", [
      `Insufficient ${sellToken.symbol} balance. Available ${balance.amount}, requested ${parsed.amount}.`
    ]);
  }

  const quote = await swapService.quoteSwap({
    chain: parsed.chain,
    sellToken,
    buyToken,
    sellAmountRaw,
    takerAddress: treasuryAddress,
    recipient,
    slippageBps: parsed.slippageBps
  });

  if (!quote.liquidityAvailable) {
    return buildFailure("swap_token", requestId, "rejected", [
      "Swap route has no available liquidity."
    ], { quote });
  }

  const slippageBps =
    quote.minBuyAmountRaw && quote.buyAmountRaw > 0n
      ? Math.round(Number((quote.buyAmountRaw - quote.minBuyAmountRaw) * 10_000n / quote.buyAmountRaw))
      : parsed.slippageBps ?? 0;

  const safety = await riskService.evaluate({
    operationType: "swap_token",
    chain: parsed.chain,
    tokenSymbol: sellToken.symbol,
    amount: parsed.amount,
    destination: recipient,
    slippageBps,
    approval: parsed.approval,
    requireGasReserve: true
  });

  if (!safety.approved) {
    logEvent(requestId, "swap_token", "rejected", {
      chain: parsed.chain,
      sellTokenSymbol: sellToken.symbol,
      buyTokenSymbol: buyToken.symbol,
      amount: parsed.amount,
      recipient
    });
    return buildFailure("swap_token", requestId, "rejected", safety.reasons, {
      quote,
      safety
    }, safety.warnings);
  }

  const quoteSummary = {
    provider: quote.provider,
    chain: quote.chain,
    sellToken: sellToken.symbol,
    buyToken: buyToken.symbol,
    amountIn: parsed.amount,
    expectedAmountOut: tokenService.formatRawAmount(quote.buyAmountRaw, buyToken),
    minimumAmountOut: quote.minBuyAmountRaw
      ? tokenService.formatRawAmount(quote.minBuyAmountRaw, buyToken)
      : undefined,
    gas: quote.gas,
    gasPrice: quote.gasPrice,
    totalNetworkFee: quote.totalNetworkFee,
    allowanceTarget: quote.allowanceTarget,
    recipient
  };

  const dryRun = parsed.dryRun ?? appConfig.safety.dryRunDefault;
  if (dryRun) {
    logEvent(requestId, "swap_token", "dry_run", {
      chain: parsed.chain,
      sellTokenSymbol: sellToken.symbol,
      buyTokenSymbol: buyToken.symbol,
      amount: parsed.amount,
      recipient
    });
    return buildSuccess("swap_token", requestId, "dry_run", {
      quote: quoteSummary,
      safety
    }, safety.warnings);
  }

  const execution = await swapService.executeSwap(quote);
  logEvent(requestId, "swap_token", "success", {
    chain: parsed.chain,
    sellTokenSymbol: sellToken.symbol,
    tokenSymbol: sellToken.symbol,
    buyTokenSymbol: buyToken.symbol,
    amount: parsed.amount,
    recipient,
    txHash: execution.txHash
  });

  return buildSuccess("swap_token", requestId, "success", {
    quote: quoteSummary,
    safety,
    execution
  }, safety.warnings);
}
