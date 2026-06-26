import { getNativeToken } from "../chains/index.js";
import { appConfig } from "../config.js";
import { parseUnits } from "viem";
import { BridgeService } from "../services/bridgeService.js";
import { RiskService } from "../services/riskService.js";
import { SolanaTokenService } from "../services/solanaTokenService.js";
import { SolanaWalletService } from "../services/solanaWalletService.js";
import { TokenService } from "../services/tokenService.js";
import { WalletService } from "../services/walletService.js";
import type { TokenInfo, ToolResponse } from "../types.js";
import { buildFailure, buildSuccess, formatTokenAmount } from "../utils/formatting.js";
import { createRequestId, logEvent } from "../utils/logging.js";
import { bridgeTokenInputSchema } from "../utils/validation.js";

function resolveSolanaDestinationToken(
  destinationChain: "ethereum" | "polygon" | "arbitrum" | "base",
  sourceToken: TokenInfo
): TokenInfo {
  if (sourceToken.symbol === "SOL") {
    return getNativeToken(destinationChain);
  }

  throw new Error(`Unsupported Solana destination mapping for ${sourceToken.symbol}.`);
}

export async function bridgeTokenTool(
  input: unknown,
  walletService: WalletService,
  solanaWalletService: SolanaWalletService,
  tokenService: TokenService,
  solanaTokenService: SolanaTokenService,
  bridgeService: BridgeService,
  riskService: RiskService
): Promise<ToolResponse<Record<string, unknown>>> {
  const requestId = createRequestId();
  const parsed = bridgeTokenInputSchema.parse(input);

  const sourceToken = parsed.sourceChain === "solana"
    ? solanaTokenService.resolveToken(parsed.token)
    : await tokenService.resolveToken(parsed.sourceChain, parsed.token);
  const destinationToken = parsed.sourceChain === "solana"
    ? (sourceToken.symbol === "SOL"
        ? resolveSolanaDestinationToken(parsed.destinationChain, sourceToken)
        : await tokenService.resolveToken(parsed.destinationChain, sourceToken.symbol))
    : await tokenService.resolveToken(parsed.destinationChain, sourceToken.symbol);

  const amountRaw = parsed.sourceChain === "solana"
    ? parseUnits(parsed.amount, sourceToken.decimals)
    : tokenService.amountToRaw(parsed.amount, sourceToken);

  const sourceTreasuryAddress = parsed.sourceChain === "solana"
    ? solanaWalletService.getTreasuryAddress()
    : walletService.getTreasuryAddress();

  const balance = parsed.sourceChain === "solana"
    ? await solanaTokenService.getTokenBalance(sourceTreasuryAddress, sourceToken)
    : await tokenService.getTokenBalance(parsed.sourceChain, walletService.getTreasuryAddress(), sourceToken);

  if (BigInt(balance.rawAmount) < amountRaw) {
    return buildFailure("bridge_token", requestId, "rejected", [
      `Insufficient ${sourceToken.symbol} balance. Available ${balance.amount}, requested ${parsed.amount}.`
    ]);
  }

  const destinationAddress = walletService.getTreasuryAddress();
  const quote = await bridgeService.quoteTransfer({
    sourceChain: parsed.sourceChain,
      destinationChain: parsed.destinationChain,
      sourceToken,
      destinationToken,
      amount: amountRaw,
      fromAddress: sourceTreasuryAddress,
      toAddress: destinationAddress
    });

  const feeBps = quote.fromAmountRaw > 0n
    ? Math.round(quote.feeQuotes.reduce((sum, fee) => sum + Number(fee.percentageBps ?? 0), 0))
    : 0;
  const slippageBps =
    quote.minReceivedRaw && quote.toAmountRaw > 0n
      ? Math.round(Number((quote.toAmountRaw - quote.minReceivedRaw) * 10_000n / quote.toAmountRaw))
      : 0;

  const safety = await riskService.evaluate({
    operationType: "bridge_token",
    chain: parsed.sourceChain,
    tokenSymbol: sourceToken.symbol,
    amount: parsed.amount,
    destination: destinationAddress,
    feeBps,
    slippageBps,
    approval: parsed.approval,
    requireGasReserve: parsed.sourceChain !== "solana"
  });

  if (!safety.approved) {
    logEvent(requestId, "bridge_token", "rejected", {
      sourceChain: parsed.sourceChain,
      destinationChain: parsed.destinationChain,
      tokenSymbol: sourceToken.symbol,
      amount: parsed.amount
    });
    return buildFailure("bridge_token", requestId, "rejected", safety.reasons, {
      quote,
      safety
    }, safety.warnings);
  }

  const quoteSummary = {
    provider: quote.provider,
    routeId: quote.routeId,
    tool: quote.tool,
    sourceChain: parsed.sourceChain,
    destinationChain: parsed.destinationChain,
    token: sourceToken.symbol,
    destinationToken: destinationToken.symbol,
    amount: parsed.amount,
    expectedReceived: formatTokenAmount(quote.toAmountRaw, destinationToken.decimals),
    minimumReceived: quote.minReceivedRaw
      ? formatTokenAmount(quote.minReceivedRaw, destinationToken.decimals)
      : undefined,
    destinationAddress,
    fees: quote.feeQuotes
  };

  const dryRun = parsed.dryRun ?? appConfig.safety.dryRunDefault;
  if (dryRun) {
    logEvent(requestId, "bridge_token", "dry_run", {
      sourceChain: parsed.sourceChain,
      destinationChain: parsed.destinationChain,
      tokenSymbol: sourceToken.symbol,
      amount: parsed.amount
    });
    return buildSuccess("bridge_token", requestId, "dry_run", {
      quote: quoteSummary,
      safety
    }, safety.warnings);
  }

  const execution = await bridgeService.executeBridge(quote);
  const status = await bridgeService.waitForBridgeCompletion(quote, execution.sourceTxHash);
  const responseStatus = status.status === "DONE" ? "success" : "submitted";

  logEvent(requestId, "bridge_token", responseStatus, {
    sourceChain: parsed.sourceChain,
    destinationChain: parsed.destinationChain,
    tokenSymbol: sourceToken.symbol,
    amount: parsed.amount,
    txHash: execution.sourceTxHash,
    bridgeStatus: status.status
  });

  return buildSuccess("bridge_token", requestId, responseStatus, {
    quote: quoteSummary,
    safety,
    execution: {
      approvalTxHash: execution.approvalTxHash,
      sourceTxHash: execution.sourceTxHash,
      bridgeStatus: status
    }
  }, safety.warnings);
}
