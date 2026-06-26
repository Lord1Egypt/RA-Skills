import { getAddress, type Address } from "viem";
import type { Chain } from "viem/chains";
import { arbitrum, base, mainnet, polygon } from "viem/chains";
import type { ChainName, TokenInfo } from "../types.js";

interface ChainTokenConfig {
  symbol: string;
  name: string;
  address: Address;
  decimals: number;
  isBridged?: boolean;
  trackBalance?: boolean;
}

interface ChainConfig {
  key: ChainName;
  label: string;
  chainId: number;
  nativeSymbol: string;
  nativeName: string;
  decimals: number;
  viemChain: Chain;
  stablecoins: ChainTokenConfig[];
}

const TOKEN_ZERO = "0x0000000000000000000000000000000000000000" as Address;
const addr = (value: string): Address => getAddress(value);

export const SUPPORTED_CHAINS: Record<ChainName, ChainConfig> = {
  ethereum: {
    key: "ethereum",
    label: "Ethereum",
    chainId: 1,
    nativeSymbol: "ETH",
    nativeName: "Ether",
    decimals: 18,
    viemChain: mainnet,
    stablecoins: [
      {
        symbol: "USDC",
        name: "USD Coin",
        address: addr("0xA0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"),
        decimals: 6,
        trackBalance: true
      },
      {
        symbol: "USDT",
        name: "Tether USD",
        address: addr("0xdAC17F958D2ee523a2206206994597C13D831ec7"),
        decimals: 6,
        trackBalance: true
      },
      {
        symbol: "DAI",
        name: "Dai Stablecoin",
        address: addr("0x6B175474E89094C44Da98b954EedeAC495271d0F"),
        decimals: 18,
        trackBalance: true
      },
      {
        symbol: "WETH",
        name: "Wrapped Ether",
        address: addr("0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"),
        decimals: 18
      },
      {
        symbol: "WBTC",
        name: "Wrapped BTC",
        address: addr("0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599"),
        decimals: 8
      }
    ]
  },
  polygon: {
    key: "polygon",
    label: "Polygon",
    chainId: 137,
    nativeSymbol: "POL",
    nativeName: "Polygon Ecosystem Token",
    decimals: 18,
    viemChain: polygon,
    stablecoins: [
      {
        symbol: "USDC",
        name: "USD Coin",
        address: addr("0x3c499c542cef5e3811e1192ce70d8cc03d5c3359"),
        decimals: 6,
        trackBalance: true
      },
      {
        symbol: "USDC.E",
        name: "Bridged USDC (PoS)",
        address: addr("0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"),
        decimals: 6,
        isBridged: true,
        trackBalance: true
      },
      {
        symbol: "USDT",
        name: "Tether USD",
        address: addr("0xc2132D05D31c914a87C6611C10748AEb04B58e8F"),
        decimals: 6,
        trackBalance: true
      },
      {
        symbol: "DAI",
        name: "Dai Stablecoin",
        address: addr("0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063"),
        decimals: 18,
        trackBalance: true
      },
      {
        symbol: "WETH",
        name: "Wrapped Ether",
        address: addr("0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619"),
        decimals: 18
      },
      {
        symbol: "WBTC",
        name: "Wrapped BTC",
        address: addr("0x1BFD67037B42Cf73acF2047067bd4F2C47D9BfD6"),
        decimals: 8
      }
    ]
  },
  arbitrum: {
    key: "arbitrum",
    label: "Arbitrum",
    chainId: 42161,
    nativeSymbol: "ETH",
    nativeName: "Ether",
    decimals: 18,
    viemChain: arbitrum,
    stablecoins: [
      {
        symbol: "USDC",
        name: "USD Coin",
        address: addr("0xaf88d065e77c8cC2239327C5EDb3A432268e5831"),
        decimals: 6,
        trackBalance: true
      },
      {
        symbol: "USDC.E",
        name: "Bridged USDC",
        address: addr("0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8"),
        decimals: 6,
        isBridged: true,
        trackBalance: true
      },
      {
        symbol: "USDT",
        name: "Tether USD",
        address: addr("0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9"),
        decimals: 6,
        trackBalance: true
      },
      {
        symbol: "DAI",
        name: "Dai Stablecoin",
        address: addr("0xda10009cbd5d07dd0cecc66161fc93d7c9000da1"),
        decimals: 18,
        trackBalance: true
      },
      {
        symbol: "WETH",
        name: "Wrapped Ether",
        address: addr("0x82af49447d8a07e3bd95bd0d56f35241523fbab1"),
        decimals: 18
      },
      {
        symbol: "WBTC",
        name: "Wrapped BTC",
        address: addr("0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f"),
        decimals: 8
      },
      {
        symbol: "ARB",
        name: "Arbitrum",
        address: addr("0x912CE59144191C1204E64559FE8253a0e49E6548"),
        decimals: 18
      }
    ]
  },
  base: {
    key: "base",
    label: "Base",
    chainId: 8453,
    nativeSymbol: "ETH",
    nativeName: "Ether",
    decimals: 18,
    viemChain: base,
    stablecoins: [
      {
        symbol: "USDC",
        name: "USD Coin",
        address: addr("0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"),
        decimals: 6,
        trackBalance: true
      },
      {
        symbol: "DAI",
        name: "Dai Stablecoin",
        address: addr("0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb"),
        decimals: 18,
        trackBalance: true
      },
      {
        symbol: "WETH",
        name: "Wrapped Ether",
        address: addr("0x4200000000000000000000000000000000000006"),
        decimals: 18
      },
      {
        symbol: "CBBTC",
        name: "Coinbase Wrapped BTC",
        address: addr("0xcbb7c0000ab88b473b1f5afd9ef808440eed33bf"),
        decimals: 8
      }
    ]
  }
};

export const NATIVE_TOKEN_SENTINEL = TOKEN_ZERO;

export function getChainConfig(chain: ChainName): ChainConfig {
  return SUPPORTED_CHAINS[chain];
}

export function getNativeToken(chain: ChainName): TokenInfo {
  const config = getChainConfig(chain);
  return {
    chain,
    symbol: config.nativeSymbol,
    name: config.nativeName,
    decimals: config.decimals,
    address: NATIVE_TOKEN_SENTINEL,
    isNative: true
  };
}

export function getConfiguredStablecoins(chain: ChainName): TokenInfo[] {
  return getChainConfig(chain).stablecoins
    .filter((token) => token.trackBalance !== false)
    .map((token) => ({
      chain,
      symbol: token.symbol,
      name: token.name,
      decimals: token.decimals,
      address: token.address,
      isNative: false,
      isBridged: token.isBridged
    }));
}

export function getConfiguredTokens(chain: ChainName): TokenInfo[] {
  return getChainConfig(chain).stablecoins.map((token) => ({
    chain,
    symbol: token.symbol,
    name: token.name,
    decimals: token.decimals,
    address: token.address,
    isNative: false,
    isBridged: token.isBridged
  }));
}

export function findConfiguredTokenBySymbol(chain: ChainName, symbol: string): TokenInfo | undefined {
  const normalizedSymbol = symbol.trim().toUpperCase();
  if (normalizedSymbol === getChainConfig(chain).nativeSymbol.toUpperCase() || normalizedSymbol === "NATIVE") {
    return getNativeToken(chain);
  }

  return getConfiguredTokens(chain).find(
    (token) => token.symbol.toUpperCase() === normalizedSymbol
  );
}

export function findConfiguredTokenByAddress(chain: ChainName, address: Address): TokenInfo | undefined {
  const normalized = address.toLowerCase();
  return getConfiguredTokens(chain).find(
    (token) => token.address?.toLowerCase() === normalized
  );
}
