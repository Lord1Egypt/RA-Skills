import { getNativeToken } from "../chains/index.js";
import { parseUnits } from "viem";
import { formatTokenAmount } from "../utils/formatting.js";
import { buildFailure, buildSuccess } from "../utils/formatting.js";
import { createRequestId, logEvent } from "../utils/logging.js";
import { quoteOperationInputSchema } from "../utils/validation.js";
import type { ToolResponse } from "../types.js";
import { BridgeService } from "../services/bridgeService.js";
import { HyperliquidService } from "../services/hyperliquidService.js";
import { HyperliquidTradingService } from "../services/hyperliquidTradingService.js";
import { SolanaTokenService } from "../services/solanaTokenService.js";
import { SolanaWalletService } from "../services/solanaWalletService.js";
import { SwapService } from "../services/swapService.js";
import { TokenService } from "../services/tokenService.js";
import { WalletService } from "../services/walletService.js";

export async function quoteOperationTool(
  input: unknown,
  walletService: WalletService,
  tokenService: TokenService,
  solanaWalletService: SolanaWalletService,
  solanaTokenService: SolanaTokenService,
  swapService: SwapService,
  bridgeService: BridgeService,
  hyperliquidService: HyperliquidService,
  hyperliquidTradingService: HyperliquidTradingService
): Promise<ToolResponse<Record<string, unknown>>> {
  const requestId = createRequestId();
  const parsed = quoteOperationInputSchema.parse(input);

  if (parsed.operationType === "transfer_token") {
    if (!parsed.chain || !parsed.token || !parsed.recipient || !parsed.amount) {
      return buildFailure("quote_operation", requestId, "error", [
        "transfer_token quote requires chain, token, recipient, and amount."
      ]);
    }

    const treasuryAddress = parsed.walletAddress ?? walletService.getTreasuryAddress();
    const token = await tokenService.resolveToken(parsed.chain, parsed.token);
    const amountRaw = tokenService.amountToRaw(parsed.amount, token);
    const gasEstimate = await tokenService.estimateTransferGas(
      parsed.chain,
      treasuryAddress,
      parsed.recipient,
      token,
      amountRaw
    );
    const gasPrice = await walletService.getGasPrice(parsed.chain);

    logEvent(requestId, "quote_operation", "success", {
      operationType: parsed.operationType
    });
    return buildSuccess("quote_operation", requestId, "success", {
      operationType: parsed.operationType,
      quote: {
        chain: parsed.chain,
        sender: treasuryAddress,
        recipient: parsed.recipient,
        token: token.symbol,
        amount: parsed.amount,
        gasEstimate: gasEstimate.toString(),
        estimatedGasCostRaw: (gasEstimate * gasPrice).toString()
      }
    });
  }

  if (parsed.operationType === "bridge_token") {
    if (!parsed.sourceChain || !parsed.destinationChain || !parsed.token || !parsed.amount) {
      return buildFailure("quote_operation", requestId, "error", [
        "bridge_token quote requires sourceChain, destinationChain, token, and amount."
      ]);
    }

    const sourceToken = parsed.sourceChain === "solana"
      ? solanaTokenService.resolveToken(parsed.token)
      : await tokenService.resolveToken(parsed.sourceChain, parsed.token);
    const destinationToken = parsed.sourceChain === "solana"
      ? (sourceToken.symbol === "SOL"
          ? getNativeToken(parsed.destinationChain)
          : await tokenService.resolveToken(parsed.destinationChain, sourceToken.symbol))
      : await tokenService.resolveToken(parsed.destinationChain, sourceToken.symbol);
    const sourceAddress = parsed.sourceChain === "solana"
      ? solanaWalletService.getTreasuryAddress()
      : (parsed.walletAddress ?? walletService.getTreasuryAddress());
    const destinationAddress = parsed.walletAddress ?? walletService.getTreasuryAddress();
    const quote = await bridgeService.quoteTransfer({
      sourceChain: parsed.sourceChain,
      destinationChain: parsed.destinationChain,
      sourceToken,
      destinationToken,
      amount: parsed.sourceChain === "solana"
        ? parseUnits(parsed.amount, sourceToken.decimals)
        : tokenService.amountToRaw(parsed.amount, sourceToken),
      fromAddress: sourceAddress,
      toAddress: destinationAddress
    });

    logEvent(requestId, "quote_operation", "success", {
      operationType: parsed.operationType
    });
    return buildSuccess("quote_operation", requestId, "success", {
      operationType: parsed.operationType,
      quote: {
        provider: quote.provider,
        routeId: quote.routeId,
        sourceChain: parsed.sourceChain,
        destinationChain: parsed.destinationChain,
        token: sourceToken.symbol,
        amount: parsed.amount,
        expectedReceived: formatTokenAmount(quote.toAmountRaw, destinationToken.decimals),
        minimumReceived: quote.minReceivedRaw
          ? formatTokenAmount(quote.minReceivedRaw, destinationToken.decimals)
          : undefined,
        fees: quote.feeQuotes
      }
    });
  }

  if (parsed.operationType === "swap_token") {
    if (!parsed.chain || !parsed.sellToken || !parsed.buyToken || !parsed.amount) {
      return buildFailure("quote_operation", requestId, "error", [
        "swap_token quote requires chain, sellToken, buyToken, and amount."
      ]);
    }

    const treasuryAddress = parsed.walletAddress ?? walletService.getTreasuryAddress();
    const sellToken = await tokenService.resolveToken(parsed.chain, parsed.sellToken);
    const buyToken = await tokenService.resolveToken(parsed.chain, parsed.buyToken);
    const quote = await swapService.quoteSwap({
      chain: parsed.chain,
      sellToken,
      buyToken,
      sellAmountRaw: tokenService.amountToRaw(parsed.amount, sellToken),
      takerAddress: treasuryAddress,
      recipient: parsed.recipient,
      slippageBps: parsed.slippageBps
    });

    logEvent(requestId, "quote_operation", "success", {
      operationType: parsed.operationType
    });
    return buildSuccess("quote_operation", requestId, "success", {
      operationType: parsed.operationType,
      quote: {
        provider: quote.provider,
        chain: parsed.chain,
        sellToken: sellToken.symbol,
        buyToken: buyToken.symbol,
        amountIn: parsed.amount,
        expectedAmountOut: formatTokenAmount(quote.buyAmountRaw, buyToken.decimals),
        minimumAmountOut: quote.minBuyAmountRaw
          ? formatTokenAmount(quote.minBuyAmountRaw, buyToken.decimals)
          : undefined,
        gas: quote.gas,
        gasPrice: quote.gasPrice,
        totalNetworkFee: quote.totalNetworkFee,
        allowanceTarget: quote.allowanceTarget,
        recipient: parsed.recipient ?? treasuryAddress
      }
    });
  }

  if (parsed.operationType === "deposit_to_hyperliquid") {
    if (!parsed.sourceChain || !parsed.token || !parsed.amount || !parsed.destination) {
      return buildFailure("quote_operation", requestId, "error", [
        "deposit_to_hyperliquid quote requires sourceChain, token, amount, and destination."
      ]);
    }
    if (parsed.sourceChain === "solana") {
      return buildFailure("quote_operation", requestId, "error", [
        "deposit_to_hyperliquid does not support Solana source chains."
      ]);
    }

    const quote = await hyperliquidService.quoteDeposit({
      sourceChain: parsed.sourceChain,
      token: parsed.token,
      amount: parsed.amount,
      destination: parsed.destination
    });

    logEvent(requestId, "quote_operation", "success", {
      operationType: parsed.operationType
    });
    return buildSuccess("quote_operation", requestId, "success", {
      operationType: parsed.operationType,
      quote
    });
  }

  if (parsed.operationType === "place_hyperliquid_order") {
    if (!parsed.market || !parsed.side || !parsed.size || !parsed.orderType) {
      return buildFailure("quote_operation", requestId, "error", [
        "place_hyperliquid_order quote requires market, side, size, and orderType."
      ]);
    }

    const quote = await hyperliquidTradingService.quoteOrder({
      accountAddress: parsed.accountAddress ?? parsed.walletAddress,
      market: parsed.market,
      side: parsed.side,
      size: parsed.size,
      orderType: parsed.orderType,
      price: parsed.price,
      slippageBps: parsed.slippageBps,
      leverage: parsed.leverage,
      reduceOnly: parsed.reduceOnly,
      timeInForce: parsed.timeInForce,
      enableDexAbstraction: parsed.enableDexAbstraction,
      approval: parsed.approval,
      dryRun: parsed.dryRun
    });

    logEvent(requestId, "quote_operation", "success", {
      operationType: parsed.operationType
    });
    return buildSuccess("quote_operation", requestId, "success", {
      operationType: parsed.operationType,
      quote
    }, quote.safety.warnings);
  }

  if (parsed.operationType === "protect_hyperliquid_position") {
    if (!parsed.market) {
      return buildFailure("quote_operation", requestId, "error", [
        "protect_hyperliquid_position quote requires market."
      ]);
    }

    const quote = await hyperliquidTradingService.quoteProtection({
      accountAddress: parsed.accountAddress ?? parsed.walletAddress,
      market: parsed.market,
      takeProfitRoePercent: parsed.takeProfitRoePercent,
      stopLossRoePercent: parsed.stopLossRoePercent,
      replaceExisting: parsed.replaceExisting,
      liquidationBufferBps: parsed.liquidationBufferBps,
      enableDexAbstraction: parsed.enableDexAbstraction,
      approval: parsed.approval,
      dryRun: parsed.dryRun
    });

    logEvent(requestId, "quote_operation", "success", {
      operationType: parsed.operationType
    });
    return buildSuccess("quote_operation", requestId, "success", {
      operationType: parsed.operationType,
      quote
    }, quote.safety.warnings);
  }

  return buildFailure("quote_operation", requestId, "error", [
    "quote_operation currently supports transfer_token, swap_token, bridge_token, deposit_to_hyperliquid, place_hyperliquid_order, and protect_hyperliquid_position."
  ]);
}
