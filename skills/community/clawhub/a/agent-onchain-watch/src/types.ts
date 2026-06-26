// src/types.ts

// --- Master Spec 공통 타입 ---

export interface AcpJobResult {
  success: boolean;
  agent_id: string;
  job_id: string;
  generated_at: string;
  data: unknown;
  error?: string;
}

export function makeSuccess(agentId: string, jobId: string, data: unknown): AcpJobResult {
  return {
    success: true,
    agent_id: agentId,
    job_id: jobId,
    generated_at: new Date().toISOString(),
    data,
  };
}

export function makeError(agentId: string, jobId: string, error: string): AcpJobResult {
  return {
    success: false,
    agent_id: agentId,
    job_id: jobId,
    generated_at: new Date().toISOString(),
    data: null,
    error,
  };
}

// --- OnchainWatch 전용 타입 ---

export interface OnchainWatchInput {
  address: string;
  chain?: 'ethereum' | 'base';
  event_types?: Array<'tx' | 'token_transfer'>;
}

export interface TxRecord {
  hash: string;
  from: string;
  to: string;
  value_eth: number;
  timestamp: string;
  type: 'in' | 'out';
}

export interface TokenTransferRecord {
  token_name: string;
  token_symbol: string;
  from: string;
  to: string;
  value: string;
  timestamp: string;
}

export interface OnchainWatchOutput {
  address: string;
  chain: string;
  balance_eth: number | null;
  transactions: TxRecord[];
  token_transfers: TokenTransferRecord[];
  risk_flags: string[];
  summary: string;
}
