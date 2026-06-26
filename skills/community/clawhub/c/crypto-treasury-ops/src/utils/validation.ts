import { z } from "zod";
import { getAddress, isAddress, type Address } from "viem";
import type { ChainName } from "../types.js";

const evmChainEnum = z.enum(["ethereum", "polygon", "arbitrum", "base"]);
const balanceChainEnum = z.enum(["ethereum", "polygon", "arbitrum", "base", "solana"]);
const bridgeSourceChainEnum = z.enum(["ethereum", "polygon", "arbitrum", "base", "solana"]);
const hyperliquidOrderSideEnum = z.enum(["buy", "sell"]);
const hyperliquidOrderTypeEnum = z.enum(["market", "limit"]);
const hyperliquidTimeInForceEnum = z.enum(["gtc", "ioc", "alo"]);
const hyperliquidMarginModeEnum = z.enum(["cross", "isolated"]);
const percentageSchema = z.number().finite().positive().max(10_000);

const addressSchema = z
  .string()
  .refine((value) => isAddress(value), "Invalid EVM address.")
  .transform((value) => getAddress(value));

const positiveDecimalSchema = z
  .string()
  .trim()
  .refine((value) => /^\d+(\.\d+)?$/.test(value), "Amount must be a positive decimal string.")
  .refine((value) => Number(value) > 0, "Amount must be greater than zero.");

const executionFlagsSchema = z.object({
  dryRun: z.boolean().optional(),
  approval: z.boolean().optional()
});

export const getBalancesInputSchema = z.object({
  walletAddress: z.string().trim().optional(),
  chain: balanceChainEnum,
  solanaAddress: z.string().trim().optional()
}).superRefine((value, context) => {
  if (value.chain === "solana") {
    if (!value.solanaAddress && !value.walletAddress) {
      context.addIssue({
        code: z.ZodIssueCode.custom,
        message: "solanaAddress or walletAddress is required for Solana balance checks."
      });
    }
    return;
  }

  if (!value.walletAddress || !isAddress(value.walletAddress)) {
    context.addIssue({
      code: z.ZodIssueCode.custom,
      message: "walletAddress must be a valid EVM address."
    });
  }
});

export const transferTokenInputSchema = executionFlagsSchema.extend({
  chain: evmChainEnum,
  token: z.string().trim().min(1, "Token is required."),
  recipient: addressSchema,
  amount: positiveDecimalSchema
});

export const swapTokenInputSchema = executionFlagsSchema.extend({
  chain: evmChainEnum,
  sellToken: z.string().trim().min(1, "sellToken is required."),
  buyToken: z.string().trim().min(1, "buyToken is required."),
  amount: positiveDecimalSchema,
  recipient: addressSchema.optional(),
  slippageBps: z.number().int().positive().max(10_000).optional()
});

export const bridgeTokenInputSchema = executionFlagsSchema.extend({
  sourceChain: bridgeSourceChainEnum,
  destinationChain: evmChainEnum,
  token: z.string().trim().min(1, "Token is required."),
  amount: positiveDecimalSchema
});

export const depositToHyperliquidInputSchema = executionFlagsSchema.extend({
  sourceChain: evmChainEnum,
  token: z.string().trim().min(1, "Token is required."),
  amount: positiveDecimalSchema,
  destination: addressSchema
});

export const getHyperliquidMarketStateInputSchema = z.object({
  market: z.string().trim().min(1).optional().transform((value) => value?.toUpperCase())
});

export const getHyperliquidAccountStateInputSchema = z.object({
  user: addressSchema.optional(),
  dex: z.string().trim().min(1).optional()
});

export const placeHyperliquidOrderInputSchema = executionFlagsSchema.extend({
  accountAddress: addressSchema.optional(),
  market: z.string().trim().min(1, "market is required."),
  side: hyperliquidOrderSideEnum,
  size: positiveDecimalSchema,
  orderType: hyperliquidOrderTypeEnum,
  price: positiveDecimalSchema.optional(),
  slippageBps: z.number().int().positive().max(10_000).optional(),
  reduceOnly: z.boolean().optional(),
  leverage: z.number().finite().positive().max(100).optional(),
  marginMode: hyperliquidMarginModeEnum.optional(),
  timeInForce: hyperliquidTimeInForceEnum.optional(),
  enableDexAbstraction: z.boolean().optional()
}).superRefine((value, context) => {
  if (value.orderType === "limit" && !value.price) {
    context.addIssue({
      code: z.ZodIssueCode.custom,
      message: "price is required for limit orders."
    });
  }

  if (value.orderType === "market" && value.timeInForce && value.timeInForce !== "ioc") {
    context.addIssue({
      code: z.ZodIssueCode.custom,
      message: "Market orders only support timeInForce=ioc."
    });
  }
});

export const protectHyperliquidPositionInputSchema = executionFlagsSchema.extend({
  accountAddress: addressSchema.optional(),
  market: z.string().trim().min(1, "market is required."),
  takeProfitRoePercent: percentageSchema.optional(),
  stopLossRoePercent: percentageSchema.optional(),
  replaceExisting: z.boolean().optional(),
  liquidationBufferBps: z.number().finite().positive().max(5_000).optional(),
  enableDexAbstraction: z.boolean().optional()
});

export const cancelHyperliquidOrderInputSchema = executionFlagsSchema.extend({
  market: z.string().trim().min(1, "market is required."),
  orderId: z.number().int().positive()
});

export const safetyCheckInputSchema = executionFlagsSchema.extend({
  operationType: z.enum([
    "get_balances",
    "transfer_token",
    "swap_token",
    "bridge_token",
    "deposit_to_hyperliquid",
    "safety_check",
    "quote_operation"
  ]),
  chain: evmChainEnum,
  token: z.string().trim().min(1),
  amount: positiveDecimalSchema,
  destination: addressSchema.optional(),
  feeBps: z.number().finite().nonnegative().optional(),
  slippageBps: z.number().finite().nonnegative().optional()
});

export const quoteOperationInputSchema = executionFlagsSchema.extend({
  operationType: z.enum([
    "get_balances",
    "transfer_token",
    "swap_token",
    "bridge_token",
    "deposit_to_hyperliquid",
    "place_hyperliquid_order",
    "protect_hyperliquid_position",
    "safety_check",
    "quote_operation"
  ]),
  walletAddress: addressSchema.optional(),
  chain: evmChainEnum.optional(),
  sourceChain: bridgeSourceChainEnum.optional(),
  destinationChain: evmChainEnum.optional(),
  token: z.string().optional(),
  sellToken: z.string().optional(),
  buyToken: z.string().optional(),
  recipient: addressSchema.optional(),
  destination: addressSchema.optional(),
  amount: positiveDecimalSchema.optional(),
  market: z.string().trim().min(1).optional(),
  accountAddress: addressSchema.optional(),
  side: hyperliquidOrderSideEnum.optional(),
  size: positiveDecimalSchema.optional(),
  orderType: hyperliquidOrderTypeEnum.optional(),
  price: positiveDecimalSchema.optional(),
  leverage: z.number().finite().positive().max(100).optional(),
  reduceOnly: z.boolean().optional(),
  timeInForce: hyperliquidTimeInForceEnum.optional(),
  enableDexAbstraction: z.boolean().optional(),
  slippageBps: z.number().int().positive().max(10_000).optional()
  ,
  takeProfitRoePercent: percentageSchema.optional(),
  stopLossRoePercent: percentageSchema.optional(),
  replaceExisting: z.boolean().optional(),
  liquidationBufferBps: z.number().finite().positive().max(5_000).optional()
});

export function parseAddress(value: string): Address {
  if (!isAddress(value)) {
    throw new Error("Invalid EVM address.");
  }

  return getAddress(value);
}

export function parseChain(value: string): ChainName {
  return evmChainEnum.parse(value.toLowerCase());
}

export function safeParseJsonInput(rawInput: string | undefined): unknown {
  if (!rawInput) {
    return {};
  }

  try {
    return JSON.parse(rawInput);
  } catch {
    throw new Error("Input must be valid JSON.");
  }
}
