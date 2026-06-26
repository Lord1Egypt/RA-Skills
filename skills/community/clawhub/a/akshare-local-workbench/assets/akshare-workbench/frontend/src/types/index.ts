export type ParamType = "string" | "date" | "select" | "integer" | "number" | "boolean";
export type ExportFormat = "csv" | "json" | "xlsx";

export interface IndicatorParam {
  name: string;
  label: string;
  type: ParamType;
  required: boolean;
  default?: string | number | boolean | null;
  placeholder?: string | null;
  description?: string | null;
  options?: string[] | null;
}

export interface IndicatorSummary {
  id: string;
  level1: string;
  level2: string;
  level3: string;
  name: string;
  source: string;
  source_name: string;
  update_frequency: string;
  description: string;
  docs_url: string;
}

export interface Indicator extends IndicatorSummary {
  ak_function: string;
  params: IndicatorParam[];
  result_notes?: string | null;
}

export interface SourceSummary {
  source: string;
  source_name: string;
  indicator_count: number;
}

export interface SectorSummary {
  id: string;
  name: string;
  short_name: string;
  description: string;
  accent: string;
  indicator_count: number;
}

export interface Sector extends SectorSummary {
  indicator_ids: string[];
}

export interface SnapshotCard {
  title: string;
  value: number | null;
  value_display: string;
  change: number | null;
  change_display: string | null;
  unit: string;
  decimals: number;
  description: string | null;
  error: string | null;
}

export interface SectorSnapshot {
  sector_id: string;
  generated_at: string;
  cards: SnapshotCard[];
}

export interface RunResponse {
  task_id: string;
  indicator_id: string;
  indicator_name: string;
  row_count: number;
  column_count: number;
  columns: string[];
  preview: Record<string, unknown>[];
  created_at: string;
  expires_at: string;
}

export interface AIConfigPublic {
  configured: boolean;
  base_url: string;
  model: string;
  has_key: boolean;
}

export type AIPlanAction =
  | "run"
  | "collect"
  | "clarify"
  | "reject"
  | "not_configured"
  | "error";

export interface AICandidate {
  id: string;
  name: string;
  level1: string;
  description: string;
}

export interface AIChatMessage {
  role: "user" | "assistant";
  content: string;
}

export interface AIPlanResponse {
  action: AIPlanAction;
  reply: string;
  indicator_id: string | null;
  indicator_name: string | null;
  params: Record<string, string | number | boolean | null>;
  candidates: AICandidate[];
  form: IndicatorParam[];
  quick_replies: string[];
}
