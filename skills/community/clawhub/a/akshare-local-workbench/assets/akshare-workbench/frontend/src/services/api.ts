import type {
  AIChatMessage,
  AIConfigPublic,
  AIPlanResponse,
  ExportFormat,
  Indicator,
  IndicatorSummary,
  RunResponse,
  Sector,
  SectorSnapshot,
  SectorSummary,
  SourceSummary
} from "../types";

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...options?.headers
    },
    ...options
  });

  if (!response.ok) {
    let message = "请求失败，请稍后重试。";
    try {
      const payload = await response.json();
      message = payload.detail ?? message;
    } catch {
      message = response.statusText || message;
    }
    throw new Error(message);
  }

  return response.json() as Promise<T>;
}

export function fetchSectors(signal?: AbortSignal): Promise<SectorSummary[]> {
  return request<SectorSummary[]>("/api/sectors", { signal });
}

export function fetchSector(sectorId: string, signal?: AbortSignal): Promise<Sector> {
  return request<Sector>(`/api/sectors/${sectorId}`, { signal });
}

export function fetchSectorSnapshot(
  sectorId: string,
  refresh = false,
  signal?: AbortSignal
): Promise<SectorSnapshot> {
  const query = refresh ? "?refresh=true" : "";
  return request<SectorSnapshot>(`/api/sectors/${sectorId}/snapshot${query}`, { signal });
}

export function fetchIndicators(
  params?: {
    source?: string;
    q?: string;
  },
  signal?: AbortSignal
): Promise<IndicatorSummary[]> {
  const searchParams = new URLSearchParams();
  if (params?.source) searchParams.set("source", params.source);
  if (params?.q) searchParams.set("q", params.q);
  const query = searchParams.toString();
  return request<IndicatorSummary[]>(`/api/indicators${query ? `?${query}` : ""}`, { signal });
}

export function fetchSources(): Promise<SourceSummary[]> {
  return request<SourceSummary[]>("/api/sources");
}

export function fetchIndicator(indicatorId: string): Promise<Indicator> {
  return request<Indicator>(`/api/indicators/${indicatorId}`);
}

export function runExtraction(
  indicatorId: string,
  params: Record<string, string | number | boolean | null>,
  refresh = false
): Promise<RunResponse> {
  return request<RunResponse>("/api/tasks/run", {
    method: "POST",
    body: JSON.stringify({
      indicator_id: indicatorId,
      params,
      refresh
    })
  });
}

export async function clearTask(taskId: string): Promise<void> {
  await fetch(`${API_BASE}/api/tasks/${taskId}`, { method: "DELETE" });
}

export async function clearAllTasks(): Promise<void> {
  await fetch(`${API_BASE}/api/tasks`, { method: "DELETE" });
}

export async function clearResultCache(): Promise<void> {
  await fetch(`${API_BASE}/api/cache/results`, { method: "DELETE" });
}

export function buildExportUrl(taskId: string, format: ExportFormat): string {
  return `${API_BASE}/api/tasks/${taskId}/export?format=${format}`;
}

export function getAIConfig(): Promise<AIConfigPublic> {
  return request<AIConfigPublic>("/api/ai/config");
}

export function saveAIConfig(payload: {
  base_url: string;
  model: string;
  api_key: string;
}): Promise<AIConfigPublic> {
  return request<AIConfigPublic>("/api/ai/config", {
    method: "PUT",
    body: JSON.stringify(payload)
  });
}

export function aiPlan(messages: AIChatMessage[]): Promise<AIPlanResponse> {
  return request<AIPlanResponse>("/api/ai/plan", {
    method: "POST",
    body: JSON.stringify({ messages })
  });
}
