import type { Address, Hex } from "viem";

export type EvmChainName = "ethereum" | "polygon" | "arbitrum" | "base";
export type ChainName = EvmChainName;
export type BalanceChainName = EvmChainName | "solana";
export type BridgeSourceChainName = EvmChainName | "solana";
export type BridgeDestinationChainName = EvmChainName;

export type ToolName =
  | "get_balances"
  | "transfer_token"
  | "swap_token"
  | "bridge_token"
  | "deposit_to_hyperliquid"
  | "get_hyperliquid_market_state"
  | "get_hyperliquid_account_state"
  | "place_hyperliquid_order"
  | "protect_hyperliquid_position"
  | "cancel_hyperliquid_order"
  | "safety_check"
  | "quote_operation";

export interface TokenInfo {
  chain: BalanceChainName;
  symbol: string;
  decimals: number;
  address?: string;
  name: string;
  isNative: boolean;
  isBridged?: boolean;
}

export interface TokenBalance {
  token: TokenInfo;
  rawAmount: string;
  amount: string;
}

export interface FeeQuote {
  name: string;
  amount: string;
  amountUsd?: string;
  tokenSymbol?: string;
  percentageBps?: number;
  included?: boolean;
}

export interface SafetyDecision {
  approved: boolean;
  decision: "approve" | "reject";
  reasons: string[];
  warnings: string[];
  policySnapshot: Record<string, unknown>;
}

export interface ToolResponse<T = unknown> {
  ok: boolean;
  tool: ToolName;
  status: "success" | "submitted" | "dry_run" | "rejected" | "error";
  requestId: string;
  timestamp: string;
  data?: T;
  warnings?: string[];
  errors?: string[];
}

export interface ExecutionFlags {
  dryRun?: boolean;
  approval?: boolean;
}

export interface TransferInput extends ExecutionFlags {
  chain: ChainName;
  token: string;
  recipient: Address;
  amount: string;
}

export interface SwapInput extends ExecutionFlags {
  chain: ChainName;
  sellToken: string;
  buyToken: string;
  amount: string;
  recipient?: Address;
  slippageBps?: number;
}

export interface BridgeInput extends ExecutionFlags {
  sourceChain: BridgeSourceChainName;
  destinationChain: BridgeDestinationChainName;
  token: string;
  amount: string;
}

export interface DepositToHyperliquidInput extends ExecutionFlags {
  sourceChain: ChainName;
  token: string;
  amount: string;
  destination: Address;
}

export interface HyperliquidMarketStateInput {
  market?: string;
}

export interface HyperliquidAccountStateInput {
  user?: Address;
  dex?: string;
}

export type HyperliquidOrderSide = "buy" | "sell";
export type HyperliquidOrderType = "market" | "limit";
export type HyperliquidTimeInForce = "gtc" | "ioc" | "alo";
export type HyperliquidMarginMode = "cross" | "isolated";
export type HyperliquidTriggerKind = "tp" | "sl";

export interface PlaceHyperliquidOrderInput extends ExecutionFlags {
  accountAddress?: Address;
  market: string;
  side: HyperliquidOrderSide;
  size: string;
  orderType: HyperliquidOrderType;
  price?: string;
  slippageBps?: number;
  reduceOnly?: boolean;
  leverage?: number;
  marginMode?: HyperliquidMarginMode;
  timeInForce?: HyperliquidTimeInForce;
  enableDexAbstraction?: boolean;
}

export interface ProtectHyperliquidPositionInput extends ExecutionFlags {
  accountAddress?: Address;
  market: string;
  takeProfitRoePercent?: number;
  stopLossRoePercent?: number;
  replaceExisting?: boolean;
  liquidationBufferBps?: number;
  enableDexAbstraction?: boolean;
}

export interface CancelHyperliquidOrderInput extends ExecutionFlags {
  market: string;
  orderId: number;
}

export interface SafetyCheckInput extends ExecutionFlags {
  operationType: ToolName;
  chain: ChainName;
  token: string;
  amount: string;
  destination?: Address;
  feeBps?: number;
  slippageBps?: number;
}

export interface QuoteOperationInput extends ExecutionFlags {
  operationType: ToolName;
  walletAddress?: Address;
  chain?: ChainName;
  sourceChain?: BridgeSourceChainName;
  destinationChain?: BridgeDestinationChainName;
  token?: string;
  sellToken?: string;
  buyToken?: string;
  recipient?: Address;
  destination?: Address;
  amount?: string;
  market?: string;
  accountAddress?: Address;
  side?: HyperliquidOrderSide;
  size?: string;
  orderType?: HyperliquidOrderType;
  price?: string;
  leverage?: number;
  reduceOnly?: boolean;
  timeInForce?: HyperliquidTimeInForce;
  slippageBps?: number;
  takeProfitRoePercent?: number;
  stopLossRoePercent?: number;
  replaceExisting?: boolean;
  liquidationBufferBps?: number;
  enableDexAbstraction?: boolean;
}

export interface SwapQuote {
  provider: string;
  chain: ChainName;
  sellToken: TokenInfo;
  buyToken: TokenInfo;
  sellAmountRaw: bigint;
  buyAmountRaw: bigint;
  minBuyAmountRaw?: bigint;
  price?: string;
  gas?: string;
  gasPrice?: string;
  totalNetworkFee?: string;
  allowanceTarget?: Address;
  liquidityAvailable: boolean;
  transactionRequest?: {
    to?: Address;
    data?: Hex;
    value?: string;
    gas?: string;
    gasPrice?: string;
  };
  routeSummary?: Record<string, unknown>;
  raw: Record<string, unknown>;
}

export interface BridgeQuote {
  provider: string;
  routeId?: string;
  tool?: string;
  sourceChain: BridgeSourceChainName;
  destinationChain: BridgeDestinationChainName;
  sourceToken: TokenInfo;
  destinationToken: TokenInfo;
  fromAmountRaw: bigint;
  toAmountRaw: bigint;
  minReceivedRaw?: bigint;
  approvalAddress?: Address;
  transactionRequest?: {
    to?: Address;
    data?: Hex;
    value?: string;
    gasLimit?: string;
    gasPrice?: string;
  };
  feeQuotes: FeeQuote[];
  raw: Record<string, unknown>;
}

export interface BridgeStatus {
  provider: string;
  status: "NOT_FOUND" | "INVALID" | "PENDING" | "DONE" | "FAILED";
  substatus?: string;
  substatusMessage?: string;
  tool?: string;
  txHash: string;
  explorerUrl?: string;
  receivingTxHash?: string;
  receivedAmountRaw?: bigint;
  raw: Record<string, unknown>;
}

export interface GasSuggestion {
  destinationChain: ChainName;
  destinationToken: TokenInfo;
  recommendedDestinationAmountRaw: bigint;
  sourceToken: TokenInfo;
  requiredSourceAmountRaw: bigint;
  raw: Record<string, unknown>;
}

export interface RuntimeLogEvent {
  requestId: string;
  action: ToolName;
  status: string;
  timestamp: string;
  details: Record<string, unknown>;
}
