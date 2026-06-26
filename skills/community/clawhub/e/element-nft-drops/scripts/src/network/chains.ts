import type { ChainListPaymentToken, ChainListWithGasItem, ElementApiResponse, GetChainsWithGasResponse } from "../types";

export interface ElementChainMetadata {
  chainMId: number;
  chain: string;
  chainId: number;
  chainName: string;
  aliases: string[];
}

export const ELEMENT_CHAIN_METADATA_BY_CHAIN_MID: Record<number, ElementChainMetadata> = {
  1: { chainMId: 1, chain: "eth", chainId: 1, chainName: "ethereum", aliases: ["ethereum", "mainnet", "eth"] },
  101: { chainMId: 101, chain: "polygon", chainId: 137, chainName: "polygon", aliases: ["polygon", "matic"] },
  201: { chainMId: 201, chain: "bsc", chainId: 56, chainName: "bsc", aliases: ["bsc", "bnb", "binance", "binance smart chain"] },
  401: { chainMId: 401, chain: "avalanche", chainId: 43114, chainName: "avalanche", aliases: ["avalanche", "avax"] },
  601: { chainMId: 601, chain: "arbitrum", chainId: 42161, chainName: "arbitrum", aliases: ["arbitrum", "arbitrum one"] },
  701: { chainMId: 701, chain: "zksync", chainId: 324, chainName: "zksync", aliases: ["zksync", "zksync era"] },
  901: { chainMId: 901, chain: "linea", chainId: 59144, chainName: "linea", aliases: ["linea"] },
  1101: { chainMId: 1101, chain: "opbnb", chainId: 204, chainName: "opbnb", aliases: ["opbnb"] },
  1201: { chainMId: 1201, chain: "base", chainId: 8453, chainName: "base", aliases: ["base"] },
  1301: { chainMId: 1301, chain: "scroll", chainId: 534352, chainName: "scroll", aliases: ["scroll"] },
  1401: { chainMId: 1401, chain: "manta_pacific", chainId: 169, chainName: "manta", aliases: ["manta", "manta pacific"] },
  1501: { chainMId: 1501, chain: "optimism", chainId: 10, chainName: "optimism", aliases: ["optimism", "op"] },
  1601: { chainMId: 1601, chain: "mantle", chainId: 5000, chainName: "mantle", aliases: ["mantle"] },
  1701: { chainMId: 1701, chain: "zkfair", chainId: 42766, chainName: "zkfair", aliases: ["zkfair"] },
  1801: { chainMId: 1801, chain: "blast", chainId: 81457, chainName: "blast", aliases: ["blast"] },
  1901: { chainMId: 1901, chain: "merlin", chainId: 4200, chainName: "merlin", aliases: ["merlin", "merlin chain"] },
  2001: { chainMId: 2001, chain: "mode", chainId: 34443, chainName: "mode", aliases: ["mode"] },
  2101: { chainMId: 2101, chain: "cyber", chainId: 7560, chainName: "cyber", aliases: ["cyber", "cyberconnect"] },
  2201: { chainMId: 2201, chain: "bob", chainId: 60808, chainName: "bob", aliases: ["bob"] },
  2301: { chainMId: 2301, chain: "lightlink", chainId: 1890, chainName: "lightlink", aliases: ["lightlink"] },
  2501: { chainMId: 2501, chain: "nanon", chainId: 2748, chainName: "nanon", aliases: ["nanon"] },
  2601: { chainMId: 2601, chain: "bera", chainId: 80094, chainName: "berachain", aliases: ["bera", "berachain"] },
  2701: { chainMId: 2701, chain: "zeta", chainId: 7000, chainName: "zetachain", aliases: ["zeta", "zetachain"] },
  2801: { chainMId: 2801, chain: "nibiru", chainId: 6900, chainName: "nibiru", aliases: ["nibiru"] },
  2901: { chainMId: 2901, chain: "abstract", chainId: 2741, chainName: "abstract", aliases: ["abstract"] },
  3001: { chainMId: 3001, chain: "monad", chainId: 143, chainName: "monad", aliases: ["monad"] },
  3101: { chainMId: 3101, chain: "bitlayer", chainId: 200901, chainName: "bitlayer", aliases: ["bitlayer"] },
  3201: { chainMId: 3201, chain: "mantra", chainId: 5888, chainName: "mantra", aliases: ["mantra"] }
};

const CHAIN_MID_BY_ALIAS = new Map(
  Object.values(ELEMENT_CHAIN_METADATA_BY_CHAIN_MID).flatMap((metadata) =>
    metadata.aliases.map((alias) => [normalizeChainName(alias), metadata.chainMId] as const)
  )
);

let cachedChainsWithGas: ChainListWithGasItem[] | null = null;

function normalizeChainName(input: string): string {
  return input.toLowerCase().replace(/[_-]+/g, " ").replace(/\s+/g, " ").trim();
}

export function getElementChainNameByChainMId(chainMId: number): string {
  const metadata = ELEMENT_CHAIN_METADATA_BY_CHAIN_MID[chainMId];
  if (!metadata) {
    throw new Error(`Unsupported chainMId for Element chain resolution: ${chainMId}`);
  }
  return metadata.chainName;
}

function sortSupportedChainNames(chainMIds: number[]): string[] {
  return chainMIds
    .map((chainMId) => ELEMENT_CHAIN_METADATA_BY_CHAIN_MID[chainMId]?.chainName)
    .filter((name): name is string => Boolean(name))
    .sort((a, b) => a.localeCompare(b));
}

export interface ResolveElementChainInput {
  chainName?: string;
  chainMId?: number;
}

export interface ResolveElementChainResult {
  chainMId: number;
  chainName: string;
  paymentTokens: ChainListPaymentToken[];
  currency: string;
}

function normalizePaymentTokenSelector(input: string): string {
  return input.trim().toLowerCase();
}

export function resolvePaymentToken(input: {
  paymentToken?: string;
  availablePaymentTokens?: ChainListPaymentToken[];
}): ChainListPaymentToken | null {
  if (!input.paymentToken) {
    return null;
  }

  const availablePaymentTokens = input.availablePaymentTokens ?? [];
  const selector = normalizePaymentTokenSelector(input.paymentToken);
  return (
    availablePaymentTokens.find((token) => {
      return (
        normalizePaymentTokenSelector(token.name) === selector ||
        (token.symbol ? normalizePaymentTokenSelector(token.symbol) === selector : false) ||
        normalizePaymentTokenSelector(token.TokenAddress) === selector
      );
    }) ?? null
  );
}

function formatSupportedPaymentTokens(paymentTokens: ChainListPaymentToken[]): string {
  return paymentTokens
    .map((token) => {
      const symbol = token.symbol ? `/${token.symbol}` : "";
      return `${token.name}${symbol} (${token.TokenAddress})`;
    })
    .join(", ");
}

export function resolveMintingTypeFromPaymentToken(input: {
  paymentToken?: string;
  availablePaymentTokens?: ChainListPaymentToken[];
  fallbackMintingType?: number;
}): number {
  if (!input.paymentToken) {
    return input.fallbackMintingType ?? 0;
  }

  const availablePaymentTokens = input.availablePaymentTokens ?? [];
  const matchedToken = resolvePaymentToken({
    paymentToken: input.paymentToken,
    availablePaymentTokens
  });

  if (!matchedToken) {
    throw new Error(
      `Unsupported paymentToken: ${input.paymentToken}. Supported payment tokens: ${formatSupportedPaymentTokens(
        availablePaymentTokens
      )}`
    );
  }

  return matchedToken.SerId << 4;
}

export function resolvePaymentTokenFromMintingType(input: {
  mintingType?: number;
  availablePaymentTokens?: ChainListPaymentToken[];
}): ChainListPaymentToken | null {
  if (!Number.isFinite(input.mintingType) || (input.mintingType ?? 0) <= 0) {
    return null;
  }

  const serId = Math.floor((input.mintingType as number) / 16);
  if (serId <= 0) {
    return null;
  }

  return (input.availablePaymentTokens ?? []).find((token) => token.SerId === serId) ?? null;
}

export async function resolveElementChain(
  input: ResolveElementChainInput,
  deps: {
    getChainsWithGas: () => Promise<ElementApiResponse<GetChainsWithGasResponse>>;
  }
): Promise<ResolveElementChainResult> {
  if (!cachedChainsWithGas) {
    const response = await deps.getChainsWithGas();
    cachedChainsWithGas = response.data.chains;
  }

  const supportedChainIds = cachedChainsWithGas.map((item) => item.chainMId);
  let chainMId = input.chainMId;

  if (input.chainName) {
    chainMId = CHAIN_MID_BY_ALIAS.get(normalizeChainName(input.chainName));
    if (!chainMId) {
      throw new Error(
        `Unsupported chainName: ${input.chainName}. Supported chains: ${sortSupportedChainNames(supportedChainIds).join(", ")}`
      );
    }
  }

  if (!chainMId) {
    throw new Error("chainName is required");
  }

  const supportedChain = cachedChainsWithGas.find((item) => item.chainMId === chainMId);
  if (!supportedChain) {
    throw new Error(
      `Unsupported chain for Element Drop: ${getElementChainNameByChainMId(chainMId)}. Supported chains: ${sortSupportedChainNames(
        supportedChainIds
      ).join(", ")}`
    );
  }

  return {
    chainMId,
    chainName: getElementChainNameByChainMId(chainMId),
    paymentTokens: supportedChain.paymentTokens,
    currency: supportedChain.currency
  };
}
