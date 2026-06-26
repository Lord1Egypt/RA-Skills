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

// --- NewsDigest 전용 타입 ---

export interface NewsDigestInput {
  topic: string;
  period?: '1d' | '3d' | '7d';
  max_items?: number;
}

export interface NewsArticle {
  title: string;
  url: string;
  summary: string;
  published_date: string;
  importance_score: number;
}

export interface NewsDigestOutput {
  topic: string;
  period: string;
  total_found: number;
  articles: NewsArticle[];
  brief: string;
}
