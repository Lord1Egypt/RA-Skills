import { getJson } from "../api/http";

export const RPC_CONF_API_URL = "https://api.element.market/v1/quote/rpcConfInfo";

export interface RpcConfInfo {
  chainMId: number;
  rpcUrl: string;
  isWalletPriority: boolean;
}

interface RpcConfResponse {
  code: number;
  status: string;
  data: RpcConfInfo[];
}

const STATIC_RPC_URLS: Record<number, string> = {
  1: "https://api.zan.top/node/v1/eth/mainnet/6e96cfbcaff949bfbdaeb5fbc554ac7c"
};

let cachedRpcConfigs: Map<number, RpcConfInfo> | null = null;
let lastFetchTime = 0;
const CACHE_DURATION_MS = 5 * 60 * 1000;

export async function fetchRpcConfigs(): Promise<RpcConfInfo[]> {
  const result = await getJson<RpcConfResponse>(RPC_CONF_API_URL);
  if (result.code !== 0) {
    throw new Error(`Failed to fetch rpc configs: ${result.status}`);
  }

  return result.data;
}

export async function getCachedRpcConfigs(): Promise<Map<number, RpcConfInfo>> {
  const now = Date.now();
  if (cachedRpcConfigs && now - lastFetchTime < CACHE_DURATION_MS) {
    return cachedRpcConfigs;
  }

  const configs = await fetchRpcConfigs();
  const filtered = configs.filter((config) => !config.isWalletPriority);
  cachedRpcConfigs = new Map(filtered.map((config) => [config.chainMId, config]));

  Object.entries(STATIC_RPC_URLS).forEach(([chainMId, rpcUrl]) => {
    const numericChainMId = Number(chainMId);
    if (!cachedRpcConfigs?.has(numericChainMId)) {
      cachedRpcConfigs?.set(numericChainMId, {
        chainMId: numericChainMId,
        rpcUrl,
        isWalletPriority: false
      });
    }
  });

  lastFetchTime = now;
  return cachedRpcConfigs;
}

export async function getRpcUrlForChainMId(chainMId: number): Promise<string> {
  const configs = await getCachedRpcConfigs();
  const rpcUrl = configs.get(chainMId)?.rpcUrl;
  if (!rpcUrl) {
    throw new Error(`Unsupported chainMId for rpc resolution: ${chainMId}`);
  }
  return rpcUrl;
}

export function __resetRpcConfigCacheForTests(): void {
  cachedRpcConfigs = null;
  lastFetchTime = 0;
}
