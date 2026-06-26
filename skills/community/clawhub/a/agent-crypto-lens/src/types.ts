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

// --- CryptoLens 전용 타입 ---

export interface CryptoLensInput {
  token: string;
  analysis_type?: 'market' | 'sentiment' | 'full';
}

export interface MarketData {
  current_price_usd: number | null;
  price_change_24h_pct: number | null;
  market_cap_usd: number | null;
  volume_24h_usd: number | null;
  data_source: string;
}

export interface SentimentData {
  score: number;
  label: 'Bullish' | 'Neutral' | 'Bearish';
  summary: string;
}

export interface ScoreData {
  momentum: number;
  sentiment: number;
  risk: number;
}

export interface CryptoLensOutput {
  token: string;
  analysis_type: string;
  market: MarketData;
  sentiment: SentimentData;
  report: string;
  scores: ScoreData;
}
