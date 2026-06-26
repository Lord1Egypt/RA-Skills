import { URL } from "node:url";
import { getAddress, type Address, type Hex } from "viem";
import { appConfig } from "../config.js";
import type { ChainName, SwapQuote, TokenInfo } from "../types.js";
import { TokenService } from "./tokenService.js";
import { WalletService } from "./walletService.js";

interface SwapRequest {
  chain: ChainName;
  sellToken: TokenInfo;
  buyToken: TokenInfo;
  sellAmountRaw: bigint;
  takerAddress: Address;
  recipient?: Address;
  slippageBps?: number;
}

interface SwapExecutionResult {
  approvalTxHash?: Hex;
  txHash: Hex;
}

interface SwapProvider {
  quote(request: SwapRequest): Promise<SwapQuote>;
  execute(quote: SwapQuote): Promise<SwapExecutionResult>;
}

function normaliseBaseUrl(baseUrl: string): string {
  return baseUrl.endsWith("/") ? baseUrl.slice(0, -1) : baseUrl;
}

class ZeroExSwapProvider implements SwapProvider {
  public constructor(
    private readonly walletService: WalletService,
    private readonly tokenService: TokenService
  ) {}

  public async quote(request: SwapRequest): Promise<SwapQuote> {
    if (!appConfig.swap.zeroExApiKey) {
      throw new Error("ZEROX_API_KEY is required for swap_token and swap quotes.");
    }

    if (request.sellToken.isNative || request.buyToken.isNative) {
      throw new Error(
        "swap_token currently supports ERC-20 swaps only. Use wrapped gas tokens such as WETH instead of native ETH/POL."
      );
    }

    const endpoint = new URL(`${normaliseBaseUrl(appConfig.swap.zeroExApiUrl)}/swap/allowance-holder/quote`);
    endpoint.searchParams.set("chainId", this.toChainId(request.chain));
    endpoint.searchParams.set("sellToken", request.sellToken.address!);
    endpoint.searchParams.set("buyToken", request.buyToken.address!);
    endpoint.searchParams.set("sellAmount", request.sellAmountRaw.toString());
    endpoint.searchParams.set("taker", request.takerAddress);
    endpoint.searchParams.set("slippageBps", String(request.slippageBps ?? appConfig.safety.maxSlippageBps));
    if (request.recipient) {
      endpoint.searchParams.set("recipient", request.recipient);
    }

    const response = await fetch(endpoint, {
      headers: {
        "0x-api-key": appConfig.swap.zeroExApiKey,
        "0x-version": appConfig.swap.zeroExVersion
      }
    });

    if (!response.ok) {
      const body = await response.text();
      throw new Error(`0x swap quote failed: ${response.status} ${body}`);
    }

    const payload = (await response.json()) as Record<string, unknown>;
    const transaction = (payload.transaction ?? {}) as Record<string, unknown>;
    const issues = (payload.issues ?? {}) as Record<string, unknown>;
    const allowance = (issues.allowance ?? {}) as Record<string, unknown>;
    const route = (payload.route ?? {}) as Record<string, unknown>;

    return {
      provider: "0x",
      chain: request.chain,
      sellToken: request.sellToken,
      buyToken: request.buyToken,
      sellAmountRaw: request.sellAmountRaw,
      buyAmountRaw: BigInt(String(payload.buyAmount ?? "0")),
      minBuyAmountRaw: payload.minBuyAmount ? BigInt(String(payload.minBuyAmount)) : undefined,
      price: payload.price ? String(payload.price) : undefined,
      gas: payload.gas ? String(payload.gas) : undefined,
      gasPrice: payload.gasPrice ? String(payload.gasPrice) : undefined,
      totalNetworkFee: payload.totalNetworkFee ? String(payload.totalNetworkFee) : undefined,
      allowanceTarget: allowance.spender ? getAddress(String(allowance.spender)) : undefined,
      liquidityAvailable: payload.liquidityAvailable !== false,
      transactionRequest: {
        to: transaction.to ? getAddress(String(transaction.to)) : undefined,
        data: transaction.data ? (String(transaction.data) as Hex) : undefined,
        value: transaction.value ? String(transaction.value) : undefined,
        gas: transaction.gas ? String(transaction.gas) : undefined,
        gasPrice: transaction.gasPrice ? String(transaction.gasPrice) : undefined
      },
      routeSummary: route,
      raw: payload
    };
  }

  public async execute(quote: SwapQuote): Promise<SwapExecutionResult> {
    const sender = this.walletService.getTreasuryAddress();

    let approvalTxHash: Hex | undefined;
    if (quote.allowanceTarget) {
      approvalTxHash = await this.tokenService.ensureAllowance(
        quote.chain,
        quote.sellToken,
        sender,
        quote.allowanceTarget,
        quote.sellAmountRaw
      );
    }

    if (!quote.transactionRequest?.to) {
      throw new Error("Swap quote did not include transaction request data.");
    }

    const txHash = await this.walletService.sendTransaction(quote.chain, {
      to: quote.transactionRequest.to,
      data: quote.transactionRequest.data,
      value: quote.transactionRequest.value ? BigInt(quote.transactionRequest.value) : 0n,
      gas: quote.transactionRequest.gas ? BigInt(quote.transactionRequest.gas) : undefined
    });

    await this.walletService.waitForReceipt(quote.chain, txHash);
    return {
      approvalTxHash,
      txHash
    };
  }

  private toChainId(chain: ChainName): string {
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

export class SwapService {
  private readonly provider: SwapProvider;

  public constructor(
    walletService: WalletService,
    tokenService: TokenService
  ) {
    switch (appConfig.swap.provider) {
      case "0x":
        this.provider = new ZeroExSwapProvider(walletService, tokenService);
        break;
      default:
        throw new Error(`Unsupported swap provider "${appConfig.swap.provider}".`);
    }
  }

  public quoteSwap(request: SwapRequest): Promise<SwapQuote> {
    return this.provider.quote(request);
  }

  public executeSwap(quote: SwapQuote): Promise<SwapExecutionResult> {
    return this.provider.execute(quote);
  }
}
