import { appConfig } from "../config.js";
import type { ToolResponse } from "../types.js";
import { buildFailure, buildSuccess } from "../utils/formatting.js";
import { createRequestId, logEvent } from "../utils/logging.js";
import { depositToHyperliquidInputSchema } from "../utils/validation.js";
import { HyperliquidService } from "../services/hyperliquidService.js";
import { RiskService } from "../services/riskService.js";
import { WalletService } from "../services/walletService.js";

export async function depositToHyperliquidTool(
  input: unknown,
  walletService: WalletService,
  hyperliquidService: HyperliquidService,
  riskService: RiskService
): Promise<ToolResponse<Record<string, unknown>>> {
  const requestId = createRequestId();
  const parsed = depositToHyperliquidInputSchema.parse(input);
  const treasuryAddress = walletService.getTreasuryAddress();

  const quote = await hyperliquidService.quoteDeposit(parsed);
  const safety = await riskService.evaluate({
    operationType: "deposit_to_hyperliquid",
    chain: parsed.sourceChain,
    tokenSymbol: "USDC",
    amount: parsed.amount,
    destination: appConfig.hyperliquid.bridgeAddress,
    approval: parsed.approval,
    requireGasReserve: false
  });

  const gasReasons: string[] = [];
  const gasWarnings: string[] = [];
  if (!quote.gasStatus.sourceChain.ready) {
    gasReasons.push(
      `Source-chain gas on ${quote.gasStatus.sourceChain.chain} is below estimated requirement ${quote.gasStatus.sourceChain.estimatedRequired}. Current balance: ${quote.gasStatus.sourceChain.currentBalance}.`
    );
  }
  if (!quote.gasStatus.destinationChain.readyAfterTopUp) {
    gasReasons.push(
      `Destination-chain gas on arbitrum is insufficient for Hyperliquid deposit. Current balance: ${quote.gasStatus.destinationChain.currentBalance}, estimated required: ${quote.gasStatus.destinationChain.estimatedRequired}.`
    );
  } else if (!quote.gasStatus.destinationChain.readyBeforeTopUp && quote.gasTopUpQuote) {
    gasWarnings.push(
      `Automatic gas top-up is planned before deposit because Arbitrum gas balance is below the estimated deposit requirement.`
    );
  }

  const combinedReasons = [...safety.reasons, ...gasReasons];
  const combinedWarnings = [...safety.warnings, ...gasWarnings];

  if (!safety.approved || gasReasons.length > 0) {
    logEvent(requestId, "deposit_to_hyperliquid", "rejected", {
      sourceChain: parsed.sourceChain,
      amount: parsed.amount,
      destination: parsed.destination
    });
    return buildFailure("deposit_to_hyperliquid", requestId, "rejected", combinedReasons, {
      quote,
      safety
    }, combinedWarnings);
  }

  const dryRun = parsed.dryRun ?? appConfig.safety.dryRunDefault;
  if (dryRun) {
    logEvent(requestId, "deposit_to_hyperliquid", "dry_run", {
      sourceChain: parsed.sourceChain,
      amount: parsed.amount,
      destination: parsed.destination
    });
    return buildSuccess("deposit_to_hyperliquid", requestId, "dry_run", {
      treasuryAddress,
      hyperliquidBridgeAddress: appConfig.hyperliquid.bridgeAddress,
      quote,
      safety
    }, combinedWarnings);
  }

  const execution = await hyperliquidService.executeDeposit(parsed);
  logEvent(requestId, "deposit_to_hyperliquid", "success", {
    sourceChain: parsed.sourceChain,
    amount: parsed.amount,
    destination: parsed.destination,
    depositTxHash: execution.depositTxHash
  });

  return buildSuccess("deposit_to_hyperliquid", requestId, "success", {
    treasuryAddress,
    hyperliquidBridgeAddress: appConfig.hyperliquid.bridgeAddress,
    execution,
    safety
  }, combinedWarnings);
}
