import { config as loadDotenv } from "dotenv";
import path from "node:path";
import { getAddress, isAddress, type Address, type Hex } from "viem";
import type { BalanceChainName, ChainName } from "./types.js";
import { DEFAULT_EVM_RPC_URLS, DEFAULT_SOLANA_RPC_URLS } from "./constants/rpcs.js";

loadDotenv();

function parseBoolean(value: string | undefined, fallback: boolean): boolean {
  if (value === undefined) {
    return fallback;
  }

  return ["1", "true", "yes", "on"].includes(value.trim().toLowerCase());
}

function parseSymbolAmountMap(value: string | undefined): Record<string, number> {
  if (!value) {
    return {};
  }

  return value.split(",").reduce<Record<string, number>>((accumulator, item) => {
    const [rawKey, rawValue] = item.split(":");
    if (!rawKey || !rawValue) {
      return accumulator;
    }

    const numericValue = Number(rawValue);
    if (!Number.isFinite(numericValue)) {
      return accumulator;
    }

    accumulator[rawKey.trim().toUpperCase()] = numericValue;
    return accumulator;
  }, {});
}

function parseChainAmountMap(value: string | undefined): Partial<Record<BalanceChainName, number>> {
  if (!value) {
    return {};
  }

  return value.split(",").reduce<Partial<Record<BalanceChainName, number>>>((accumulator, item) => {
    const [rawKey, rawValue] = item.split(":");
    if (!rawKey || !rawValue) {
      return accumulator;
    }

    const chain = rawKey.trim().toLowerCase() as BalanceChainName;
    const numericValue = Number(rawValue);
    if (!Number.isFinite(numericValue)) {
      return accumulator;
    }

    accumulator[chain] = numericValue;
    return accumulator;
  }, {});
}

function parseAddressList(value: string | undefined): Address[] {
  if (!value) {
    return [];
  }

  return value
    .split(",")
    .map((entry) => entry.trim())
    .filter(Boolean)
    .filter((entry) => isAddress(entry))
    .map((entry) => getAddress(entry));
}

function parseStringList(value: string | undefined): string[] {
  if (!value) {
    return [];
  }

  return value
    .split(",")
    .map((entry) => entry.trim())
    .filter(Boolean);
}

function parseRpcUrlList(value: string | undefined, defaults: string[]): string[] {
  const customUrls = value
    ?.split(",")
    .map((item) => item.trim())
    .filter(Boolean) ?? [];

  return Array.from(new Set([...customUrls, ...defaults]));
}

function parseSolanaTrackedTokens(value: string | undefined): Array<{
  symbol: string;
  mint: string;
  decimals: number;
}> {
  const fallback =
    value ??
    "USDC:EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v:6,USDT:Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB:6";

  return fallback.split(",").reduce<Array<{ symbol: string; mint: string; decimals: number }>>((items, entry) => {
    const [symbol, mint, decimals] = entry.split(":").map((part) => part?.trim());
    const parsedDecimals = Number(decimals);
    if (!symbol || !mint || !Number.isFinite(parsedDecimals)) {
      return items;
    }

    items.push({
      symbol: symbol.toUpperCase(),
      mint,
      decimals: parsedDecimals
    });
    return items;
  }, []);
}

const defaultHyperliquidBridge = getAddress(
  process.env.HYPERLIQUID_BRIDGE_ADDRESS ?? "0x2df1c51e09aecf9cacb7bc98cb1742757f163df7"
);

export const appConfig = {
  wallet: {
    privateKey: process.env.TREASURY_PRIVATE_KEY as Hex | undefined,
    treasuryAddressOverride: process.env.TREASURY_WALLET_ADDRESS
      ? getAddress(process.env.TREASURY_WALLET_ADDRESS)
      : undefined
  },
  rpcUrls: {
    ethereum: parseRpcUrlList(process.env.ETHEREUM_RPC_URL, DEFAULT_EVM_RPC_URLS.ethereum),
    polygon: parseRpcUrlList(process.env.POLYGON_RPC_URL, DEFAULT_EVM_RPC_URLS.polygon),
    arbitrum: parseRpcUrlList(process.env.ARBITRUM_RPC_URL, DEFAULT_EVM_RPC_URLS.arbitrum),
    base: parseRpcUrlList(process.env.BASE_RPC_URL, DEFAULT_EVM_RPC_URLS.base)
  } satisfies Record<ChainName, string[]>,
  solana: {
    rpcUrls: parseRpcUrlList(process.env.SOLANA_RPC_URL, DEFAULT_SOLANA_RPC_URLS),
    trackedTokens: parseSolanaTrackedTokens(process.env.SOLANA_TRACKED_TOKENS),
    privateKey: process.env.SOLANA_TREASURY_PRIVATE_KEY,
    treasuryAddressOverride: process.env.SOLANA_TREASURY_ADDRESS
  },
  bridge: {
    provider: (process.env.BRIDGE_PROVIDER ?? "lifi").toLowerCase(),
    lifiApiUrl: process.env.LIFI_API_URL ?? "https://li.quest/v1",
    lifiApiKey: process.env.LIFI_API_KEY,
    mayanApiKey: process.env.MAYAN_API_KEY,
    integrator: process.env.BRIDGE_INTEGRATOR ?? "crypto-treasury-ops",
    statusTimeoutMs: Number(process.env.BRIDGE_STATUS_TIMEOUT_MS ?? 900_000),
    statusPollMs: Number(process.env.BRIDGE_STATUS_POLL_MS ?? 15_000)
  },
  swap: {
    provider: (process.env.SWAP_PROVIDER ?? "0x").toLowerCase(),
    zeroExApiUrl: process.env.ZEROX_API_URL ?? "https://api.0x.org",
    zeroExApiKey: process.env.ZEROX_API_KEY,
    zeroExVersion: process.env.ZEROX_API_VERSION ?? "v2"
  },
  safety: {
    allowlist: parseAddressList(process.env.TREASURY_ALLOWLIST),
    strictAllowlist: parseBoolean(process.env.STRICT_ALLOWLIST, true),
    dryRunDefault: parseBoolean(process.env.DRY_RUN_DEFAULT, true),
    maxSingleTransferByToken: parseSymbolAmountMap(process.env.MAX_SINGLE_TRANSFER_BY_TOKEN),
    maxDailyTransferByToken: parseSymbolAmountMap(process.env.MAX_DAILY_TRANSFER_BY_TOKEN),
    confirmationThresholdByToken: parseSymbolAmountMap(process.env.CONFIRMATION_THRESHOLD_BY_TOKEN),
    minGasReserveByChain: parseChainAmountMap(process.env.MIN_GAS_RESERVE_BY_CHAIN),
    maxFeeBps: Number(process.env.MAX_FEE_BPS ?? 100),
    maxSlippageBps: Number(process.env.MAX_SLIPPAGE_BPS ?? 50)
  },
  runtime: {
    logPath: path.resolve(process.cwd(), process.env.RUNTIME_LOG_PATH ?? ".runtime/treasury-ops.log")
  },
  hyperliquid: {
    apiUrl: process.env.HYPERLIQUID_API_URL ?? "https://api.hyperliquid.xyz",
    dex: process.env.HYPERLIQUID_DEX ?? undefined,
    bridgeAddress: defaultHyperliquidBridge,
    minUsdcDeposit: Number(process.env.HYPERLIQUID_MIN_USDC_DEPOSIT ?? 5),
    autoGasTopUpEnabled: parseBoolean(process.env.HYPERLIQUID_AUTO_GAS_TOPUP_ENABLED, true),
    maxAutoGasTopUpSourceAmount: Number(process.env.HYPERLIQUID_MAX_AUTO_GAS_TOPUP_SOURCE_AMOUNT ?? 5)
  },
  hyperliquidTrading: {
    enabled: parseBoolean(process.env.HYPERLIQUID_TRADING_ENABLED, true),
    allowedMarkets: parseStringList(process.env.HYPERLIQUID_TRADING_ALLOW_MARKETS).map((market) =>
      market.toUpperCase()
    ),
    maxOrderNotionalUsd: Number(process.env.HYPERLIQUID_TRADING_MAX_ORDER_NOTIONAL_USD ?? 10_000),
    maxDailyOrderNotionalUsd: Number(process.env.HYPERLIQUID_TRADING_MAX_DAILY_NOTIONAL_USD ?? 25_000),
    confirmationThresholdUsd: Number(process.env.HYPERLIQUID_TRADING_CONFIRMATION_THRESHOLD_USD ?? 2_000),
    maxLeverage: Number(process.env.HYPERLIQUID_TRADING_MAX_LEVERAGE ?? 5),
    defaultSlippageBps: Number(process.env.HYPERLIQUID_TRADING_DEFAULT_SLIPPAGE_BPS ?? 50)
  }
};
