import type { Address } from "viem";
import { appConfig } from "../config.js";
import { getNativeToken } from "../chains/index.js";
import type { BridgeQuote, BridgeStatus, ChainName } from "../types.js";
import { formatTokenAmount } from "../utils/formatting.js";
import { BridgeService } from "./bridgeService.js";
import { TokenService } from "./tokenService.js";
import { WalletService } from "./walletService.js";

interface DepositQuoteResult {
  routeType: "direct_arbitrum" | "bridge_then_deposit";
  depositTokenSymbol: "USDC";
  estimatedReceivedOnArbitrum: string;
  minimumReceivedOnArbitrum?: string;
  bridgeQuote?: BridgeQuote;
  gasTopUpQuote?: BridgeQuote;
  gasTopUpSourceAmount?: string;
  gasTopUpDestinationAmount?: string;
  gasStatus: {
    sourceChain: {
      chain: ChainName;
      currentBalance: string;
      estimatedRequired?: string;
      ready: boolean;
    };
    destinationChain: {
      chain: "arbitrum";
      currentBalance: string;
      estimatedRequired: string;
      readyBeforeTopUp: boolean;
      readyAfterTopUp: boolean;
    };
  };
  destination: Address;
}

export class HyperliquidService {
  public constructor(
    private readonly walletService: WalletService,
    private readonly tokenService: TokenService,
    private readonly bridgeService: BridgeService
  ) {}

  public async quoteDeposit(input: {
    sourceChain: ChainName;
    token: string;
    amount: string;
    destination: Address;
  }): Promise<DepositQuoteResult> {
    const treasuryAddress = this.walletService.getTreasuryAddress();
    if (input.destination.toLowerCase() !== treasuryAddress.toLowerCase()) {
      throw new Error(
        "Hyperliquid deposits are only supported when destination matches the treasury signer address. Hyperliquid credits the sending EOA."
      );
    }

    if (input.token.trim().toUpperCase() !== "USDC") {
      throw new Error("Hyperliquid deposit currently supports USDC only.");
    }

    const arbitrumUsdc = await this.tokenService.resolveToken("arbitrum", "USDC");
    const minDeposit = appConfig.hyperliquid.minUsdcDeposit;
    if (Number(input.amount) < minDeposit) {
      throw new Error(`Hyperliquid minimum supported deposit is ${minDeposit} USDC.`);
    }

    if (input.sourceChain === "arbitrum") {
      const amountRaw = this.tokenService.amountToRaw(input.amount, arbitrumUsdc);
      const depositGas = await this.tokenService.estimateTransferGas(
        "arbitrum",
        treasuryAddress,
        appConfig.hyperliquid.bridgeAddress,
        arbitrumUsdc,
        amountRaw
      );
      const gasPrice = await this.walletService.getGasPrice("arbitrum");
      const requiredArbitrumGas = this.addGasBuffer(depositGas * gasPrice);
      const currentArbitrumGas = await this.walletService.getNativeBalance("arbitrum", treasuryAddress);
      return {
        routeType: "direct_arbitrum",
        depositTokenSymbol: "USDC",
        estimatedReceivedOnArbitrum: input.amount,
        minimumReceivedOnArbitrum: input.amount,
        gasStatus: {
          sourceChain: {
            chain: "arbitrum",
            currentBalance: formatTokenAmount(currentArbitrumGas, getNativeToken("arbitrum").decimals),
            estimatedRequired: formatTokenAmount(requiredArbitrumGas, getNativeToken("arbitrum").decimals),
            ready: currentArbitrumGas >= requiredArbitrumGas
          },
          destinationChain: {
            chain: "arbitrum",
            currentBalance: formatTokenAmount(currentArbitrumGas, getNativeToken("arbitrum").decimals),
            estimatedRequired: formatTokenAmount(requiredArbitrumGas, getNativeToken("arbitrum").decimals),
            readyBeforeTopUp: currentArbitrumGas >= requiredArbitrumGas,
            readyAfterTopUp: currentArbitrumGas >= requiredArbitrumGas
          }
        },
        destination: input.destination
      };
    }

    if (!["polygon", "base"].includes(input.sourceChain)) {
      throw new Error("Hyperliquid deposit currently supports sourceChain = arbitrum, polygon, or base.");
    }

    const sourceUsdc = await this.tokenService.resolveToken(input.sourceChain, "USDC");
    const sourceTokenAmountRaw = this.tokenService.amountToRaw(input.amount, sourceUsdc);
    const currentArbitrumGas = await this.walletService.getNativeBalance("arbitrum", treasuryAddress);

    let gasTopUpQuote: BridgeQuote | undefined;
    let gasTopUpSourceAmountRaw = 0n;
    let gasTopUpDestinationAmountRaw = 0n;

    const estimatedDepositGas = await this.tokenService.estimateTransferGas(
      "arbitrum",
      treasuryAddress,
      appConfig.hyperliquid.bridgeAddress,
      arbitrumUsdc,
      1n
    );
    const arbitrumGasPrice = await this.walletService.getGasPrice("arbitrum");
    const requiredArbitrumGas = this.addGasBuffer(estimatedDepositGas * arbitrumGasPrice);
    const hasArbitrumGasAlready = currentArbitrumGas >= requiredArbitrumGas;

    if (!hasArbitrumGasAlready && appConfig.hyperliquid.autoGasTopUpEnabled) {
      const gasSuggestion = await this.bridgeService.getGasSuggestion("arbitrum", input.sourceChain, sourceUsdc);
      if (!gasSuggestion) {
        throw new Error("Unable to obtain Arbitrum gas top-up suggestion for Hyperliquid deposit.");
      }

      gasTopUpSourceAmountRaw = gasSuggestion.requiredSourceAmountRaw;
      gasTopUpDestinationAmountRaw = gasSuggestion.recommendedDestinationAmountRaw;

      const gasTopUpSourceAmount = Number(formatTokenAmount(gasTopUpSourceAmountRaw, sourceUsdc.decimals));
      if (gasTopUpSourceAmount > appConfig.hyperliquid.maxAutoGasTopUpSourceAmount) {
        throw new Error(
          `Automatic gas top-up would consume ${gasTopUpSourceAmount} ${sourceUsdc.symbol}, exceeding configured limit ${appConfig.hyperliquid.maxAutoGasTopUpSourceAmount}.`
        );
      }

      gasTopUpQuote = await this.bridgeService.quoteTransfer({
        sourceChain: input.sourceChain,
        destinationChain: "arbitrum",
        sourceToken: sourceUsdc,
        destinationToken: getNativeToken("arbitrum"),
        amount: gasTopUpSourceAmountRaw,
        fromAddress: treasuryAddress,
        toAddress: treasuryAddress
      });
    }

    const bridgeAmountRaw = sourceTokenAmountRaw - gasTopUpSourceAmountRaw;
    if (bridgeAmountRaw <= 0n) {
      throw new Error("Amount is too small after reserving source funds for destination gas top-up.");
    }

    const bridgeQuote = await this.bridgeService.quoteTransfer({
      sourceChain: input.sourceChain,
      destinationChain: "arbitrum",
      sourceToken: sourceUsdc,
      destinationToken: arbitrumUsdc,
      amount: bridgeAmountRaw,
      fromAddress: treasuryAddress,
      toAddress: treasuryAddress
    });

    const currentSourceGas = await this.walletService.getNativeBalance(input.sourceChain, treasuryAddress);
    const estimatedSourceGas = this.estimateSourceGasCost(bridgeQuote, gasTopUpQuote);

    return {
      routeType: "bridge_then_deposit",
      depositTokenSymbol: "USDC",
      estimatedReceivedOnArbitrum: formatTokenAmount(bridgeQuote.toAmountRaw, arbitrumUsdc.decimals),
      minimumReceivedOnArbitrum: bridgeQuote.minReceivedRaw
        ? formatTokenAmount(bridgeQuote.minReceivedRaw, arbitrumUsdc.decimals)
        : undefined,
      bridgeQuote,
      gasTopUpQuote,
      gasTopUpSourceAmount: gasTopUpSourceAmountRaw > 0n
        ? formatTokenAmount(gasTopUpSourceAmountRaw, sourceUsdc.decimals)
        : undefined,
      gasTopUpDestinationAmount: gasTopUpDestinationAmountRaw > 0n
        ? formatTokenAmount(gasTopUpDestinationAmountRaw, getNativeToken("arbitrum").decimals)
        : undefined,
      gasStatus: {
        sourceChain: {
          chain: input.sourceChain,
          currentBalance: formatTokenAmount(currentSourceGas, getNativeToken(input.sourceChain).decimals),
          estimatedRequired: formatTokenAmount(estimatedSourceGas, getNativeToken(input.sourceChain).decimals),
          ready: currentSourceGas >= estimatedSourceGas
        },
        destinationChain: {
          chain: "arbitrum",
          currentBalance: formatTokenAmount(currentArbitrumGas, getNativeToken("arbitrum").decimals),
          estimatedRequired: formatTokenAmount(requiredArbitrumGas, getNativeToken("arbitrum").decimals),
          readyBeforeTopUp: hasArbitrumGasAlready,
          readyAfterTopUp: hasArbitrumGasAlready || gasTopUpDestinationAmountRaw >= requiredArbitrumGas
        }
      },
      destination: input.destination
    };
  }

  public async executeDeposit(input: {
    sourceChain: ChainName;
    token: string;
    amount: string;
    destination: Address;
  }): Promise<{
    routeType: "direct_arbitrum" | "bridge_then_deposit";
    gasTopUp?: {
      sourceTxHash: string;
      approvalTxHash?: string;
      status: BridgeStatus;
    };
    bridge?: {
      sourceTxHash: string;
      approvalTxHash?: string;
      status: BridgeStatus;
    };
    depositTxHash: string;
    depositedAmount: string;
  }> {
    const quote = await this.quoteDeposit(input);
    const arbitrumUsdc = await this.tokenService.resolveToken("arbitrum", "USDC");
    const treasuryAddress = this.walletService.getTreasuryAddress();

    if (quote.routeType === "direct_arbitrum") {
      if (!quote.gasStatus.destinationChain.readyAfterTopUp) {
        throw new Error("Arbitrum gas balance is too low for Hyperliquid deposit and no automatic top-up route is available.");
      }

      const amountRaw = this.tokenService.amountToRaw(input.amount, arbitrumUsdc);
      const depositTxHash = await this.tokenService.transferToken(
        "arbitrum",
        appConfig.hyperliquid.bridgeAddress,
        arbitrumUsdc,
        amountRaw
      );
      await this.walletService.waitForReceipt("arbitrum", depositTxHash);

      return {
        routeType: quote.routeType,
        depositTxHash,
        depositedAmount: input.amount
      };
    }

    const bridgeQuote = quote.bridgeQuote;
    if (!bridgeQuote) {
      throw new Error("Missing bridge quote for Hyperliquid deposit flow.");
    }

    if (!quote.gasStatus.sourceChain.ready) {
      throw new Error(`Source-chain gas is too low on ${quote.gasStatus.sourceChain.chain} to execute the deposit flow.`);
    }

    let gasTopUpExecution:
      | {
          sourceTxHash: string;
          approvalTxHash?: string;
          status: BridgeStatus;
        }
      | undefined;

    if (quote.gasTopUpQuote) {
      const requiredArbitrumGas = this.tokenService.amountToRaw(
        quote.gasStatus.destinationChain.estimatedRequired,
        getNativeToken("arbitrum")
      );
      const gasTopUp = await this.bridgeService.executeBridge(quote.gasTopUpQuote);
      const gasTopUpStatus = await this.waitForArbitrumGasReadiness(
        quote.gasTopUpQuote,
        gasTopUp.sourceTxHash,
        treasuryAddress,
        requiredArbitrumGas
      );
      if (gasTopUpStatus.status !== "DONE") {
        throw new Error(
          `Gas top-up leg did not complete. Status: ${gasTopUpStatus.status}${gasTopUpStatus.substatus ? ` (${gasTopUpStatus.substatus})` : ""}.`
        );
      }

      gasTopUpExecution = {
        sourceTxHash: gasTopUp.sourceTxHash,
        approvalTxHash: gasTopUp.approvalTxHash,
        status: gasTopUpStatus
      };
    }

    const balanceBeforeBridge = BigInt(
      (await this.tokenService.getTokenBalance("arbitrum", treasuryAddress, arbitrumUsdc)).rawAmount
    );

    const execution = await this.bridgeService.executeBridge(bridgeQuote);
    const status = await this.waitForArbitrumUsdcArrival(
      bridgeQuote,
      execution.sourceTxHash,
      treasuryAddress,
      arbitrumUsdc,
      balanceBeforeBridge
    );
    if (status.status !== "DONE") {
      throw new Error(
        `Bridge leg did not complete. Status: ${status.status}${status.substatus ? ` (${status.substatus})` : ""}.`
      );
    }

    // Hyperliquid credits the sending Arbitrum EOA after the bridged USDC reaches Arbitrum.
    const depositedAmountRaw = status.receivedAmountRaw ?? bridgeQuote.toAmountRaw;
    const depositTxHash = await this.tokenService.transferToken(
      "arbitrum",
      appConfig.hyperliquid.bridgeAddress,
      arbitrumUsdc,
      depositedAmountRaw
    );
    await this.walletService.waitForReceipt("arbitrum", depositTxHash);

    return {
      routeType: quote.routeType,
      gasTopUp: gasTopUpExecution,
      bridge: {
        sourceTxHash: execution.sourceTxHash,
        approvalTxHash: execution.approvalTxHash,
        status
      },
      depositTxHash,
      depositedAmount: formatTokenAmount(depositedAmountRaw, arbitrumUsdc.decimals)
    };
  }

  private addGasBuffer(rawAmount: bigint): bigint {
    return (rawAmount * 120n) / 100n;
  }

  private estimateSourceGasCost(mainBridge: BridgeQuote, gasTopUpQuote?: BridgeQuote): bigint {
    const quotes = [mainBridge, gasTopUpQuote].filter((quote): quote is BridgeQuote => Boolean(quote));
    return quotes.reduce((total, quote) => {
      const gasLimit = quote.transactionRequest?.gasLimit ? BigInt(quote.transactionRequest.gasLimit) : 0n;
      const gasPrice = quote.transactionRequest?.gasPrice ? BigInt(quote.transactionRequest.gasPrice) : 0n;
      if (gasLimit === 0n || gasPrice === 0n) {
        return total;
      }

      return total + this.addGasBuffer(gasLimit * gasPrice);
    }, 0n);
  }

  private async waitForArbitrumGasReadiness(
    quote: BridgeQuote,
    sourceTxHash: string,
    treasuryAddress: Address,
    requiredArbitrumGas: bigint
  ): Promise<BridgeStatus> {
    try {
      const status = await this.bridgeService.waitForBridgeCompletion(quote, sourceTxHash);
      if (status.status === "DONE") {
        return status;
      }
    } catch (error) {
      return this.waitForMinimumNativeBalance(
        "arbitrum",
        treasuryAddress,
        requiredArbitrumGas,
        sourceTxHash,
        quote.provider,
        error
      );
    }

    return this.waitForMinimumNativeBalance(
      "arbitrum",
      treasuryAddress,
      requiredArbitrumGas,
      sourceTxHash,
      quote.provider
    );
  }

  private async waitForArbitrumUsdcArrival(
    quote: BridgeQuote,
    sourceTxHash: string,
    treasuryAddress: Address,
    arbitrumUsdc: Awaited<ReturnType<TokenService["resolveToken"]>>,
    balanceBeforeBridge: bigint
  ): Promise<BridgeStatus> {
    try {
      const status = await this.bridgeService.waitForBridgeCompletion(quote, sourceTxHash);
      if (status.status === "DONE") {
        return status;
      }
    } catch (error) {
      return this.waitForMinimumTokenDelta(
        "arbitrum",
        treasuryAddress,
        arbitrumUsdc,
        balanceBeforeBridge,
        quote.minReceivedRaw ?? quote.toAmountRaw,
        sourceTxHash,
        quote.provider,
        error
      );
    }

    return this.waitForMinimumTokenDelta(
      "arbitrum",
      treasuryAddress,
      arbitrumUsdc,
      balanceBeforeBridge,
      quote.minReceivedRaw ?? quote.toAmountRaw,
      sourceTxHash,
      quote.provider
    );
  }

  private async waitForMinimumNativeBalance(
    chain: ChainName,
    address: Address,
    minimumRaw: bigint,
    sourceTxHash: string,
    provider: string,
    recoveryError?: unknown
  ): Promise<BridgeStatus> {
    const startedAt = Date.now();

    while (Date.now() - startedAt < appConfig.bridge.statusTimeoutMs) {
      const currentBalance = await this.walletService.getNativeBalance(chain, address);
      if (currentBalance >= minimumRaw) {
        return {
          provider,
          status: "DONE",
          txHash: sourceTxHash,
          substatus: "BALANCE_CONFIRMED",
          substatusMessage: `Observed native balance on ${chain} is sufficient to continue.`,
          receivedAmountRaw: currentBalance,
          raw: {
            observedBalance: currentBalance.toString(),
            minimumRequired: minimumRaw.toString(),
            recoveredFromError: recoveryError instanceof Error ? recoveryError.message : undefined
          }
        };
      }

      await new Promise((resolve) => setTimeout(resolve, appConfig.bridge.statusPollMs));
    }

    return {
      provider,
      status: "PENDING",
      txHash: sourceTxHash,
      substatus: "BALANCE_WAIT_TIMEOUT",
      substatusMessage: `Timed out waiting for native balance on ${chain} to reach the required threshold.`,
      raw: {
        minimumRequired: minimumRaw.toString(),
        recoveredFromError: recoveryError instanceof Error ? recoveryError.message : undefined
      }
    };
  }

  private async waitForMinimumTokenDelta(
    chain: ChainName,
    address: Address,
    token: Awaited<ReturnType<TokenService["resolveToken"]>>,
    balanceBefore: bigint,
    minimumDelta: bigint,
    sourceTxHash: string,
    provider: string,
    recoveryError?: unknown
  ): Promise<BridgeStatus> {
    const startedAt = Date.now();

    while (Date.now() - startedAt < appConfig.bridge.statusTimeoutMs) {
      const currentBalance = BigInt((await this.tokenService.getTokenBalance(chain, address, token)).rawAmount);
      const delta = currentBalance - balanceBefore;
      if (delta >= minimumDelta) {
        return {
          provider,
          status: "DONE",
          txHash: sourceTxHash,
          substatus: "BALANCE_CONFIRMED",
          substatusMessage: `Observed ${token.symbol} arrival on ${chain}; continuing with deposit.`,
          receivedAmountRaw: delta,
          raw: {
            observedBalance: currentBalance.toString(),
            balanceBefore: balanceBefore.toString(),
            observedDelta: delta.toString(),
            minimumDelta: minimumDelta.toString(),
            recoveredFromError: recoveryError instanceof Error ? recoveryError.message : undefined
          }
        };
      }

      await new Promise((resolve) => setTimeout(resolve, appConfig.bridge.statusPollMs));
    }

    return {
      provider,
      status: "PENDING",
      txHash: sourceTxHash,
      substatus: "BALANCE_WAIT_TIMEOUT",
      substatusMessage: `Timed out waiting for ${token.symbol} to arrive on ${chain}.`,
      raw: {
        balanceBefore: balanceBefore.toString(),
        minimumDelta: minimumDelta.toString(),
        recoveredFromError: recoveryError instanceof Error ? recoveryError.message : undefined
      }
    };
  }
}
