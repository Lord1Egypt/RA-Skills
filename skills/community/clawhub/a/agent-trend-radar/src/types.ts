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

// --- TrendRadar 전용 타입 ---

export interface TrendRadarInput {
  keywords: string[];
  timeframe?: '1d' | '7d' | '30d';
  region?: string;
}

export type TrendSignal = 'Rising' | 'Peaking' | 'Declining' | 'Insufficient_Data';

export interface TrendResult {
  keyword: string;
  signal: TrendSignal;
  score: number; // 0~100
  reason: string;
  evidence: string[]; // URL 목록
}

export interface TrendRadarOutput {
  timeframe: string;
  region: string;
  trends: TrendResult[];
  brief: string;
}
