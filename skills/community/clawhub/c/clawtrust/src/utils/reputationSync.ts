import { ChainId } from "../config/chains.js";

export interface ReputationSyncResult {
  score: number;
  syncedAt: string;
  fromChain: ChainId;
  toChain: ChainId;
  success: boolean;
  txHash?: string;
  error?: string;
}

export interface CrossChainReputation {
  base: number | null;
  skale: number | null;
  mostActive: ChainId | null;
  errors: string[];
}

const API_BASE = "https://clawtrust.org/api";

async function apiGet(path: string, agentId?: string): Promise<unknown> {
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (agentId) headers["x-agent-id"] = agentId;
  const res = await fetch(`${API_BASE}${path}`, { headers });
  if (!res.ok) throw new Error(`API ${res.status}: ${await res.text()}`);
  return res.json();
}

async function apiPost(path: string, body: unknown, agentId?: string): Promise<unknown> {
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (agentId) headers["x-agent-id"] = agentId;
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers,
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`API ${res.status}: ${await res.text()}`);
  return res.json();
}

export async function syncReputation(
  agentId: string,
  fromChain: ChainId,
  toChain: ChainId
): Promise<ReputationSyncResult> {
  if (toChain !== ChainId.SKALE) {
    throw new Error("syncReputation currently supports syncing to SKALE only");
  }

  try {
    const data = await apiPost(`/agents/${agentId}/sync-to-skale`, {
      fromChain,
      toChain,
    }, agentId) as {
      score?: number;
      syncedAt?: string;
      txHash?: string;
    };

    return {
      score: data.score ?? 0,
      syncedAt: data.syncedAt ?? new Date().toISOString(),
      fromChain,
      toChain,
      success: true,
      txHash: data.txHash,
    };
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : String(err);
    return {
      score: 0,
      syncedAt: new Date().toISOString(),
      fromChain,
      toChain,
      success: false,
      error: message,
    };
  }
}

export async function getReputationAcrossChains(
  agentId: string
): Promise<CrossChainReputation> {
  const result: CrossChainReputation = {
    base: null,
    skale: null,
    mostActive: null,
    errors: [],
  };

  try {
    const rep = await apiGet(`/reputation/${agentId}`) as {
      breakdown?: { fusedScore?: number };
    };
    result.base = rep.breakdown?.fusedScore ?? null;
  } catch (err: unknown) {
    result.errors.push(`Base: ${err instanceof Error ? err.message : String(err)}`);
  }

  try {
    const skaleScore = await apiGet(`/agents/${agentId}/skale-score`) as {
      score?: number;
    };
    result.skale = skaleScore.score ?? null;
  } catch (err: unknown) {
    result.errors.push(`SKALE: ${err instanceof Error ? err.message : String(err)}`);
  }

  if (result.base !== null && result.skale !== null) {
    result.mostActive = result.skale >= result.base ? ChainId.SKALE : ChainId.BASE;
  } else if (result.base !== null) {
    result.mostActive = ChainId.BASE;
  } else if (result.skale !== null) {
    result.mostActive = ChainId.SKALE;
  }

  return result;
}

export async function hasReputationOnChain(
  agentId: string,
  chain: ChainId
): Promise<boolean> {
  try {
    if (chain === ChainId.SKALE) {
      const data = await apiGet(`/agents/${agentId}/skale-score`) as { score?: number };
      return (data.score ?? 0) > 0;
    }
    const data = await apiGet(`/reputation/${agentId}`) as {
      breakdown?: { fusedScore?: number };
    };
    return (data.breakdown?.fusedScore ?? 0) > 0;
  } catch {
    return false;
  }
}
