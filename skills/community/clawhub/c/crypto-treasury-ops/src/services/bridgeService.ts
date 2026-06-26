import { URL } from "node:url";
import { fetchQuote, fetchTokenList, swapFromSolana, type Quote as MayanQuote, type Token as MayanToken } from "@mayanfinance/swap-sdk";
import type { Transaction, VersionedTransaction } from "@solana/web3.js";
import { getAddress, type Address, type Hex } from "viem";
import { getNativeToken } from "../chains/index.js";
import { appConfig } from "../config.js";
import type {
  BridgeDestinationChainName,
  BridgeQuote,
  BridgeSourceChainName,
  BridgeStatus,
  FeeQuote,
  GasSuggestion,
  TokenInfo
} from "../types.js";
import { SolanaWalletService } from "./solanaWalletService.js";
import { TokenService } from "./tokenService.js";
import { WalletService } from "./walletService.js";

interface BridgeRequest {
  sourceChain: BridgeSourceChainName;
  destinationChain: BridgeDestinationChainName;
  sourceToken: TokenInfo;
  destinationToken: TokenInfo;
  amount: bigint;
  fromAddress: string;
  toAddress: string;
  slippageBps?: number;
}

interface BridgeProvider {
  quote(request: BridgeRequest): Promise<BridgeQuote>;
  execute(quote: BridgeQuote): Promise<{
    sourceTxHash: string;
    approvalTxHash?: string;
  }>;
  waitForCompletion(quote: BridgeQuote, sourceTxHash: string): Promise<BridgeStatus>;
}

function normaliseBaseUrl(baseUrl: string): string {
  return baseUrl.endsWith("/") ? baseUrl.slice(0, -1) : baseUrl;
}

function parseFeeQuotes(rawFees: unknown): FeeQuote[] {
  if (!Array.isArray(rawFees)) {
    return [];
  }

  return rawFees.map((fee) => {
    const feeRecord = fee as Record<string, unknown>;
    return {
      name: String(feeRecord.name ?? "unknown"),
      amount: String(feeRecord.amount ?? "0"),
      amountUsd: feeRecord.amountUSD ? String(feeRecord.amountUSD) : undefined,
      tokenSymbol:
        typeof feeRecord.token === "object" && feeRecord.token
          ? String((feeRecord.token as Record<string, unknown>).symbol ?? "")
          : undefined,
      percentageBps: feeRecord.percentage ? Math.round(Number(feeRecord.percentage) * 100) : undefined,
      included: typeof feeRecord.included === "boolean" ? feeRecord.included : undefined
    };
  });
}

function formatExplorerUrl(txHash: string): string {
  return `https://explorer.mayan.finance/swap/${txHash}`;
}

class LifiBridgeProvider implements BridgeProvider {
  public constructor(
    private readonly walletService: WalletService,
    private readonly tokenService: TokenService
  ) {}

  public async quote(request: BridgeRequest): Promise<BridgeQuote> {
    if (request.sourceChain === "solana") {
      throw new Error("LI.FI provider does not support Solana source chains.");
    }

    const endpoint = new URL(`${normaliseBaseUrl(appConfig.bridge.lifiApiUrl)}/quote`);
    endpoint.searchParams.set("fromChain", this.toChainId(request.sourceChain));
    endpoint.searchParams.set("toChain", this.toChainId(request.destinationChain));
    endpoint.searchParams.set("fromToken", request.sourceToken.address!);
    endpoint.searchParams.set("toToken", request.destinationToken.address!);
    endpoint.searchParams.set("fromAmount", request.amount.toString());
    endpoint.searchParams.set("fromAddress", request.fromAddress);
    endpoint.searchParams.set("toAddress", request.toAddress);
    if (!request.sourceToken.isNative && !request.destinationToken.isNative) {
      endpoint.searchParams.set("preset", "stablecoin");
    }
    endpoint.searchParams.set("integrator", appConfig.bridge.integrator);
    endpoint.searchParams.set(
      "slippage",
      String((request.slippageBps ?? appConfig.safety.maxSlippageBps) / 10_000)
    );

    const response = await fetch(endpoint, {
      headers: appConfig.bridge.lifiApiKey
        ? {
            "x-lifi-api-key": appConfig.bridge.lifiApiKey
          }
        : undefined
    });

    if (!response.ok) {
      const body = await response.text();
      throw new Error(`LI.FI quote failed: ${response.status} ${body}`);
    }

    const payload = (await response.json()) as Record<string, unknown>;
    const estimate = (payload.estimate ?? {}) as Record<string, unknown>;
    const transactionRequest = (payload.transactionRequest ?? {}) as Record<string, unknown>;

    return {
      provider: "lifi",
      routeId: typeof payload.id === "string" ? payload.id : undefined,
      tool: typeof payload.tool === "string" ? payload.tool : undefined,
      sourceChain: request.sourceChain,
      destinationChain: request.destinationChain,
      sourceToken: request.sourceToken,
      destinationToken: request.destinationToken,
      fromAmountRaw: request.amount,
      toAmountRaw: BigInt(String(estimate.toAmount ?? "0")),
      minReceivedRaw: estimate.toAmountMin ? BigInt(String(estimate.toAmountMin)) : undefined,
      approvalAddress: estimate.approvalAddress ? getAddress(String(estimate.approvalAddress)) : undefined,
      transactionRequest: {
        to: transactionRequest.to ? getAddress(String(transactionRequest.to)) : undefined,
        data: transactionRequest.data ? (String(transactionRequest.data) as Hex) : undefined,
        value: transactionRequest.value ? String(transactionRequest.value) : undefined,
        gasLimit: transactionRequest.gasLimit ? String(transactionRequest.gasLimit) : undefined,
        gasPrice: transactionRequest.gasPrice ? String(transactionRequest.gasPrice) : undefined
      },
      feeQuotes: parseFeeQuotes(estimate.feeCosts),
      raw: payload
    };
  }

  public async execute(quote: BridgeQuote): Promise<{ sourceTxHash: string; approvalTxHash?: string }> {
    const sender = this.walletService.getTreasuryAddress();

    let approvalTxHash: string | undefined;
    if (quote.approvalAddress) {
      approvalTxHash = await this.tokenService.ensureAllowance(
        quote.sourceChain as Exclude<BridgeSourceChainName, "solana">,
        quote.sourceToken,
        sender,
        quote.approvalAddress,
        quote.fromAmountRaw
      );
    }

    const txRequest = quote.transactionRequest;
    if (!txRequest?.to) {
      throw new Error("Bridge quote did not include transaction request data.");
    }

    const sourceTxHash = await this.walletService.sendTransaction(
      quote.sourceChain as Exclude<BridgeSourceChainName, "solana">,
      {
        to: txRequest.to,
        data: txRequest.data,
        value: txRequest.value ? BigInt(txRequest.value) : 0n,
        gas: txRequest.gasLimit ? BigInt(txRequest.gasLimit) : undefined
      }
    );

    await this.walletService.waitForReceipt(
      quote.sourceChain as Exclude<BridgeSourceChainName, "solana">,
      sourceTxHash
    );
    return { sourceTxHash, approvalTxHash };
  }

  public async waitForCompletion(quote: BridgeQuote, sourceTxHash: string): Promise<BridgeStatus> {
    const startedAt = Date.now();

    while (Date.now() - startedAt < appConfig.bridge.statusTimeoutMs) {
      const endpoint = new URL(`${normaliseBaseUrl(appConfig.bridge.lifiApiUrl)}/status`);
      endpoint.searchParams.set("txHash", sourceTxHash);
      endpoint.searchParams.set("fromChain", this.toChainId(quote.sourceChain as Exclude<BridgeSourceChainName, "solana">));
      endpoint.searchParams.set("toChain", this.toChainId(quote.destinationChain));
      if (quote.tool) {
        endpoint.searchParams.set("bridge", quote.tool);
      }

      const response = await fetch(endpoint, {
        headers: appConfig.bridge.lifiApiKey
          ? {
              "x-lifi-api-key": appConfig.bridge.lifiApiKey
            }
          : undefined
      });

      if (!response.ok) {
        const body = await response.text();
        throw new Error(`LI.FI status lookup failed: ${response.status} ${body}`);
      }

      const payload = (await response.json()) as Record<string, unknown>;
      const status = String(payload.status ?? "NOT_FOUND") as BridgeStatus["status"];

      if (status === "DONE" || status === "FAILED" || status === "INVALID") {
        const receiving = (payload.receiving ?? {}) as Record<string, unknown>;
        return {
          provider: "lifi",
          status,
          substatus: payload.substatus ? String(payload.substatus) : undefined,
          substatusMessage: payload.substatusMessage ? String(payload.substatusMessage) : undefined,
          tool: payload.tool ? String(payload.tool) : quote.tool,
          txHash: sourceTxHash,
          explorerUrl: payload.lifiExplorerLink ? String(payload.lifiExplorerLink) : undefined,
          receivingTxHash: receiving.txHash ? String(receiving.txHash) : undefined,
          receivedAmountRaw: receiving.amount ? BigInt(String(receiving.amount)) : undefined,
          raw: payload
        };
      }

      await new Promise((resolve) => setTimeout(resolve, appConfig.bridge.statusPollMs));
    }

    return {
      provider: "lifi",
      status: "PENDING",
      txHash: sourceTxHash,
      tool: quote.tool,
      raw: {
        timeoutMs: appConfig.bridge.statusTimeoutMs
      }
    };
  }

  private toChainId(chain: Exclude<BridgeSourceChainName, "solana"> | BridgeDestinationChainName): string {
    switch (chain) {
      case "ethereum":
        return "1";
      case "polygon":
        return "137";
      case "arbitrum":
        return "42161";
      case "base":
        return "8453";
    }
  }
}

class MayanSolanaBridgeProvider implements BridgeProvider {
  private readonly tokenCache = new Map<string, Promise<MayanToken[]>>();

  public constructor(
    private readonly walletService: WalletService,
    private readonly solanaWalletService: SolanaWalletService
  ) {}

  public async quote(request: BridgeRequest): Promise<BridgeQuote> {
    if (request.sourceChain !== "solana") {
      throw new Error("Mayan Solana bridge provider only supports Solana source chains.");
    }

    const [fromToken, toToken] = await Promise.all([
      this.resolveMayanToken("solana", request.sourceToken),
      this.resolveMayanToken(request.destinationChain, request.destinationToken)
    ]);

    const quotes = await fetchQuote(
      {
        amountIn64: request.amount.toString(),
        fromToken: fromToken.contract,
        fromChain: "solana",
        toToken: toToken.contract,
        toChain: this.toMayanChainName(request.destinationChain),
        slippageBps: request.slippageBps ?? "auto",
        destinationAddress: request.toAddress
      },
      {
        apiKey: appConfig.bridge.mayanApiKey
      }
    );

    const selectedQuote = quotes[0];
    if (!selectedQuote) {
      throw new Error(`Mayan did not return a route for ${request.sourceToken.symbol} from Solana to ${request.destinationChain}.`);
    }

    return {
      provider: "mayan",
      routeId: selectedQuote.quoteId,
      tool: selectedQuote.type,
      sourceChain: request.sourceChain,
      destinationChain: request.destinationChain,
      sourceToken: request.sourceToken,
      destinationToken: request.destinationToken,
      fromAmountRaw: request.amount,
      toAmountRaw: BigInt(selectedQuote.expectedAmountOutBaseUnits),
      minReceivedRaw: BigInt(selectedQuote.minReceivedBaseUnits),
      feeQuotes: this.toFeeQuotes(selectedQuote),
      raw: {
        quote: selectedQuote,
        destinationAddress: request.toAddress,
        sourceAddress: request.fromAddress
      }
    };
  }

  public async execute(quote: BridgeQuote): Promise<{ sourceTxHash: string; approvalTxHash?: string }> {
    if (quote.sourceChain !== "solana") {
      throw new Error("Mayan Solana bridge provider only supports Solana source chains.");
    }

    const mayanQuote = (quote.raw.quote ?? null) as MayanQuote | null;
    const destinationAddress = String(quote.raw.destinationAddress ?? this.walletService.getTreasuryAddress());
    const sourceAddress = this.solanaWalletService.getTreasuryAddress();
    if (!mayanQuote) {
      throw new Error("Mayan quote payload is missing from raw bridge data.");
    }

    const signSolanaTransaction = ((
      transaction: Transaction | VersionedTransaction
    ) => ("version" in transaction
      ? this.solanaWalletService.signVersionedTransaction(transaction)
      : this.solanaWalletService.signLegacyTransaction(transaction))) as Parameters<typeof swapFromSolana>[4];

    const swap = await swapFromSolana(
      mayanQuote,
      sourceAddress,
      destinationAddress,
      undefined,
      signSolanaTransaction,
      this.solanaWalletService.getPrimaryConnection(),
      this.solanaWalletService.getExtraRpcUrls(),
      undefined,
      undefined,
      undefined,
      {
        onTransactionSigned: () => undefined,
        apiKey: appConfig.bridge.mayanApiKey
      }
    );

    await this.solanaWalletService.confirmSignature(swap.signature);
    return {
      sourceTxHash: swap.signature
    };
  }

  public async waitForCompletion(quote: BridgeQuote, sourceTxHash: string): Promise<BridgeStatus> {
    return {
      provider: "mayan",
      status: "PENDING",
      tool: quote.tool,
      txHash: sourceTxHash,
      explorerUrl: formatExplorerUrl(sourceTxHash),
      raw: {
        routeId: quote.routeId,
        note: "Mayan status polling is not yet integrated; use explorerUrl or re-check the destination balance."
      }
    };
  }

  private async resolveMayanToken(
    chain: BridgeSourceChainName | BridgeDestinationChainName,
    token: TokenInfo
  ): Promise<MayanToken> {
    const chainName = chain === "solana" ? "solana" : this.toMayanChainName(chain);
    const tokens = await this.fetchTokens(chainName);
    const matched = token.isNative
      ? tokens.find((item) => item.standard === "native")
      : tokens.find((item) => item.symbol.toUpperCase() === token.symbol.toUpperCase());

    if (!matched) {
      throw new Error(`Mayan does not support ${token.symbol} on ${chainName}.`);
    }

    return matched;
  }

  private fetchTokens(chain: string): Promise<MayanToken[]> {
    const cached = this.tokenCache.get(chain);
    if (cached) {
      return cached;
    }

    const pending = fetchTokenList(chain as Parameters<typeof fetchTokenList>[0], false, undefined, appConfig.bridge.mayanApiKey);
    this.tokenCache.set(chain, pending);
    return pending;
  }

  private toFeeQuotes(quote: MayanQuote): FeeQuote[] {
    return [
      {
        name: "bridge_fee",
        amount: String(quote.bridgeFee),
        tokenSymbol: quote.fromToken.symbol
      },
      {
        name: "swap_relayer_fee",
        amount: String(quote.swapRelayerFee),
        tokenSymbol: quote.fromToken.symbol
      },
      {
        name: "redeem_relayer_fee",
        amount: String(quote.redeemRelayerFee),
        tokenSymbol: quote.toToken.symbol
      },
      {
        name: "solana_relayer_fee",
        amount: String(quote.solanaRelayerFee),
        tokenSymbol: quote.fromToken.symbol
      }
    ].filter((fee) => Number(fee.amount) > 0);
  }

  private toMayanChainName(chain: BridgeDestinationChainName): "ethereum" | "polygon" | "arbitrum" | "base" {
    switch (chain) {
      case "ethereum":
      case "polygon":
      case "arbitrum":
      case "base":
        return chain;
    }
  }
}

class AcrossBridgeProvider implements BridgeProvider {
  public async quote(): Promise<BridgeQuote> {
    // TODO: integrate Across quote and execution APIs when provider selection is switched to "across".
    throw new Error("Across bridge provider is not implemented yet.");
  }

  public async execute(): Promise<{ sourceTxHash: string; approvalTxHash?: string }> {
    throw new Error("Across bridge provider is not implemented yet.");
  }

  public async waitForCompletion(): Promise<BridgeStatus> {
    throw new Error("Across bridge provider is not implemented yet.");
  }
}

class RelayBridgeProvider implements BridgeProvider {
  public async quote(): Promise<BridgeQuote> {
    // TODO: integrate Relay API credentials and response parsing when provider selection is switched to "relay".
    throw new Error("Relay bridge provider is not implemented yet.");
  }

  public async execute(): Promise<{ sourceTxHash: string; approvalTxHash?: string }> {
    throw new Error("Relay bridge provider is not implemented yet.");
  }

  public async waitForCompletion(): Promise<BridgeStatus> {
    throw new Error("Relay bridge provider is not implemented yet.");
  }
}

export class BridgeService {
  private readonly evmProvider: BridgeProvider;
  private readonly solanaProvider: BridgeProvider;

  public constructor(
    walletService: WalletService,
    tokenService: TokenService,
    solanaWalletService: SolanaWalletService
  ) {
    switch (appConfig.bridge.provider) {
      case "lifi":
        this.evmProvider = new LifiBridgeProvider(walletService, tokenService);
        break;
      case "across":
        this.evmProvider = new AcrossBridgeProvider();
        break;
      case "relay":
        this.evmProvider = new RelayBridgeProvider();
        break;
      default:
        throw new Error(`Unsupported bridge provider "${appConfig.bridge.provider}".`);
    }

    this.solanaProvider = new MayanSolanaBridgeProvider(walletService, solanaWalletService);
  }

  public quoteTransfer(request: BridgeRequest): Promise<BridgeQuote> {
    return this.getProvider(request.sourceChain).quote(request);
  }

  public executeBridge(quote: BridgeQuote): Promise<{ sourceTxHash: string; approvalTxHash?: string }> {
    return this.getProvider(quote.sourceChain).execute(quote);
  }

  public waitForBridgeCompletion(quote: BridgeQuote, sourceTxHash: string): Promise<BridgeStatus> {
    return this.getProvider(quote.sourceChain).waitForCompletion(quote, sourceTxHash);
  }

  public async getGasSuggestion(
    destinationChain: BridgeDestinationChainName,
    sourceChain: Exclude<BridgeSourceChainName, "solana">,
    sourceToken: TokenInfo
  ): Promise<GasSuggestion | undefined> {
    const endpoint = new URL(`${normaliseBaseUrl(appConfig.bridge.lifiApiUrl)}/gas/suggestion/${this.toChainId(destinationChain)}`);
    endpoint.searchParams.set("fromChain", this.toChainId(sourceChain));
    endpoint.searchParams.set("fromToken", sourceToken.address ?? sourceToken.symbol);

    const response = await fetch(endpoint, {
      headers: appConfig.bridge.lifiApiKey
        ? {
            "x-lifi-api-key": appConfig.bridge.lifiApiKey
          }
        : undefined
    });

    if (!response.ok) {
      return undefined;
    }

    const payload = (await response.json()) as Record<string, unknown>;
    const recommended = (payload.recommended ?? {}) as Record<string, unknown>;
    if (!recommended.amount || !payload.fromAmount) {
      return undefined;
    }

    return {
      destinationChain,
      destinationToken: getNativeToken(destinationChain),
      recommendedDestinationAmountRaw: BigInt(String(recommended.amount)),
      sourceToken,
      requiredSourceAmountRaw: BigInt(String(payload.fromAmount)),
      raw: payload
    };
  }

  private getProvider(sourceChain: BridgeSourceChainName): BridgeProvider {
    return sourceChain === "solana" ? this.solanaProvider : this.evmProvider;
  }

  private toChainId(chain: Exclude<BridgeSourceChainName, "solana"> | BridgeDestinationChainName): string {
    switch (chain) {
      case "ethereum":
        return "1";
      case "polygon":
        return "137";
      case "arbitrum":
        return "42161";
      case "base":
        return "8453";
    }
  }
}
