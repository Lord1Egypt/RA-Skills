import { appConfig } from "../config.js";
import type { ToolResponse } from "../types.js";
import { buildFailure, buildSuccess } from "../utils/formatting.js";
import { createRequestId, logEvent } from "../utils/logging.js";
import { transferTokenInputSchema } from "../utils/validation.js";
import { RiskService } from "../services/riskService.js";
import { TokenService } from "../services/tokenService.js";
import { WalletService } from "../services/walletService.js";

export async function transferTokenTool(
  input: unknown,
  walletService: WalletService,
  tokenService: TokenService,
  riskService: RiskService
): Promise<ToolResponse<Record<string, unknown>>> {
  const requestId = createRequestId();
  const parsed = transferTokenInputSchema.parse(input);
  const sender = walletService.getTreasuryAddress();
  const token = await tokenService.resolveToken(parsed.chain, parsed.token);
  const amountRaw = tokenService.amountToRaw(parsed.amount, token);

  const balance = await tokenService.getTokenBalance(parsed.chain, sender, token);
  if (BigInt(balance.rawAmount) < amountRaw) {
    return buildFailure("transfer_token", requestId, "rejected", [
      `Insufficient ${token.symbol} balance. Available ${balance.amount}, requested ${parsed.amount}.`
    ]);
  }

  const gasEstimate = await tokenService.estimateTransferGas(parsed.chain, sender, parsed.recipient, token, amountRaw);
  const gasPrice = await walletService.getGasPrice(parsed.chain);
  const estimatedGasCostRaw = gasEstimate * gasPrice;

  // Native transfers spend balance on both the send amount and gas, so reserve both up front.
  if (token.isNative && BigInt(balance.rawAmount) < amountRaw + estimatedGasCostRaw) {
    return buildFailure("transfer_token", requestId, "rejected", [
      `Insufficient ${token.symbol} balance after reserving gas. Available ${balance.amount}, requested ${parsed.amount}, estimated gas cost raw ${estimatedGasCostRaw.toString()}.`
    ]);
  }

  const feeBps = token.isNative ? Math.round((Number(estimatedGasCostRaw) / Number(amountRaw)) * 10_000) : 0;

  const safety = await riskService.evaluate({
    operationType: "transfer_token",
    chain: parsed.chain,
    tokenSymbol: token.symbol,
    amount: parsed.amount,
    destination: parsed.recipient,
    feeBps,
    approval: parsed.approval,
    requireGasReserve: true
  });

  if (!safety.approved) {
    logEvent(requestId, "transfer_token", "rejected", {
      chain: parsed.chain,
      tokenSymbol: token.symbol,
      amount: parsed.amount,
      recipient: parsed.recipient
    });
    return buildFailure("transfer_token", requestId, "rejected", safety.reasons, {
      safety,
      balance,
      gasEstimate: gasEstimate.toString(),
      estimatedGasCostRaw: estimatedGasCostRaw.toString()
    }, safety.warnings);
  }

  const dryRun = parsed.dryRun ?? appConfig.safety.dryRunDefault;
  if (dryRun) {
    logEvent(requestId, "transfer_token", "dry_run", {
      chain: parsed.chain,
      tokenSymbol: token.symbol,
      amount: parsed.amount,
      recipient: parsed.recipient
    });
    return buildSuccess("transfer_token", requestId, "dry_run", {
      summary: {
        chain: parsed.chain,
        sender,
        recipient: parsed.recipient,
        token: token.symbol,
        amount: parsed.amount,
        gasEstimate: gasEstimate.toString(),
        estimatedGasCostRaw: estimatedGasCostRaw.toString(),
        safety
      }
    }, safety.warnings);
  }

  const txHash = await tokenService.transferToken(parsed.chain, parsed.recipient, token, amountRaw);
  await walletService.waitForReceipt(parsed.chain, txHash);

  logEvent(requestId, "transfer_token", "success", {
    chain: parsed.chain,
    tokenSymbol: token.symbol,
    amount: parsed.amount,
    recipient: parsed.recipient,
    txHash
  });

  return buildSuccess("transfer_token", requestId, "success", {
    summary: {
      chain: parsed.chain,
      sender,
      recipient: parsed.recipient,
      token: token.symbol,
      amount: parsed.amount,
      txHash,
      gasEstimate: gasEstimate.toString(),
      estimatedGasCostRaw: estimatedGasCostRaw.toString()
    },
    safety
  }, safety.warnings);
}
