import { appConfig } from "../config.js";
import { readLogEvents } from "../utils/logging.js";
import type { BalanceChainName, SafetyDecision, ToolName } from "../types.js";
import { WalletService } from "./walletService.js";

interface SafetyEvaluationRequest {
  operationType: ToolName;
  chain: BalanceChainName;
  tokenSymbol: string;
  amount: string;
  destination?: string;
  feeBps?: number;
  slippageBps?: number;
  approval?: boolean;
  requireDestinationAllowlist?: boolean;
  requireGasReserve?: boolean;
}

export class RiskService {
  public constructor(private readonly walletService: WalletService) {}

  public async evaluate(request: SafetyEvaluationRequest): Promise<SafetyDecision> {
    const reasons: string[] = [];
    const warnings: string[] = [];
    const symbol = request.tokenSymbol.toUpperCase();
    const amount = Number(request.amount);
    const destination = request.destination?.toLowerCase();
    const treasuryAddress = this.walletService.getTreasuryAddress().toLowerCase();
    const allowlist = new Set([
      ...appConfig.safety.allowlist.map((address) => address.toLowerCase()),
      treasuryAddress,
      appConfig.hyperliquid.bridgeAddress.toLowerCase()
    ]);

    const maxSingle = appConfig.safety.maxSingleTransferByToken[symbol];
    if (typeof maxSingle === "number" && Number.isFinite(maxSingle) && amount > maxSingle) {
      reasons.push(`Amount ${request.amount} ${symbol} exceeds max single transfer limit of ${maxSingle} ${symbol}.`);
    }

    const dailyLimit = appConfig.safety.maxDailyTransferByToken[symbol];
    const dailyUsed = this.getDailyAmountUsed(symbol);
    if (typeof dailyLimit === "number" && Number.isFinite(dailyLimit) && dailyUsed + amount > dailyLimit) {
      reasons.push(
        `Daily transfer limit would be exceeded for ${symbol}. Used ${dailyUsed}, requested ${amount}, limit ${dailyLimit}.`
      );
    }

    const confirmationThreshold = appConfig.safety.confirmationThresholdByToken[symbol];
    if (
      typeof confirmationThreshold === "number" &&
      Number.isFinite(confirmationThreshold) &&
      amount > confirmationThreshold &&
      !request.approval
    ) {
      reasons.push(
        `Amount ${request.amount} ${symbol} exceeds confirmation threshold ${confirmationThreshold} ${symbol}. Explicit approval=true is required.`
      );
    }

    if (
      request.requireDestinationAllowlist !== false &&
      destination &&
      appConfig.safety.strictAllowlist &&
      !allowlist.has(destination)
    ) {
      reasons.push("Destination is not allowlisted.");
    }

    if (
      typeof request.feeBps === "number" &&
      request.feeBps > appConfig.safety.maxFeeBps
    ) {
      reasons.push(
        `Estimated fees ${request.feeBps} bps exceed configured limit ${appConfig.safety.maxFeeBps} bps.`
      );
    }

    if (
      typeof request.slippageBps === "number" &&
      request.slippageBps > appConfig.safety.maxSlippageBps
    ) {
      reasons.push(
        `Estimated slippage ${request.slippageBps} bps exceeds configured limit ${appConfig.safety.maxSlippageBps} bps.`
      );
    }

    if (request.requireGasReserve) {
      const requiredReserve = appConfig.safety.minGasReserveByChain[request.chain];
      if (requiredReserve !== undefined) {
        if (request.chain === "solana") {
          warnings.push("Solana source gas reserve checks are not yet enforced by RiskService.");
        } else {
          const balance = Number(
            await this.walletService.getNativeBalanceFormatted(request.chain, this.walletService.getTreasuryAddress())
          );
          if (balance < requiredReserve) {
            reasons.push(
              `Native gas balance ${balance} on ${request.chain} is below reserve requirement ${requiredReserve}.`
            );
          } else if (balance < requiredReserve * 2) {
            warnings.push(
              `Native gas balance on ${request.chain} is above reserve but still low relative to policy.`
            );
          }
        }
      }
    }

    return {
      approved: reasons.length === 0,
      decision: reasons.length === 0 ? "approve" : "reject",
      reasons,
      warnings,
      policySnapshot: {
        strictAllowlist: appConfig.safety.strictAllowlist,
        maxSingle,
        dailyLimit,
        dailyUsed,
        confirmationThreshold,
        maxFeeBps: appConfig.safety.maxFeeBps,
        maxSlippageBps: appConfig.safety.maxSlippageBps,
        gasReserve: appConfig.safety.minGasReserveByChain[request.chain]
      }
    };
  }

  private getDailyAmountUsed(symbol: string): number {
    const today = new Date().toISOString().slice(0, 10);
    return readLogEvents()
      .filter((event) => event.timestamp.startsWith(today))
      .filter((event) =>
        ["transfer_token", "swap_token", "bridge_token", "deposit_to_hyperliquid"].includes(event.action)
      )
      .filter((event) => ["success", "submitted"].includes(event.status))
      .filter((event) => {
        const loggedSymbol = event.details.tokenSymbol;
        return typeof loggedSymbol === "string" && loggedSymbol.toUpperCase() === symbol;
      })
      .reduce((sum, event) => {
        const amount = Number(event.details.amount ?? 0);
        return Number.isFinite(amount) ? sum + amount : sum;
      }, 0);
  }
}
