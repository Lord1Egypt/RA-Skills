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

// --- CompeteScope 전용 타입 ---

export interface CompeteScopeInput {
  my_product: string;
  competitors: string[];
  focus?: 'pricing' | 'features' | 'positioning' | 'all';
}

export interface CompetitorProfile {
  name: string;
  description: string;
  key_features: string[];
  pricing_model: string;
  positioning: string;
  sources: string[];
}

export interface MatrixRow {
  dimension: string;
  my_product: string;
  competitors: Record<string, string>;
}

export interface CompeteScopeOutput {
  my_product: string;
  focus: string;
  competitor_profiles: CompetitorProfile[];
  comparison_matrix: MatrixRow[];
  whitespace: string[];
  recommendation: string;
}
