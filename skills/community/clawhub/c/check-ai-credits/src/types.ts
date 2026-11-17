/** Uniform snapshot schema — kept identical to the legacy Python logger.
 *  `timestamp` is mandatory: trend ordering depends on it. */
export interface Snapshot {
  provider: string;
  source: string;
  timestamp: string;
  currency?: string;
  balance?: number | null;
  usedPercent?: number | null;
  resetsAt?: string | null;
  monthCost?: number | null;
  monthPeriod?: string | null;
  details?: Record<string, unknown> | null;
  error?: string | null;
  /** login/setup URL attached when credentials are expired or missing */
  authHint?: string;
}

export interface DetectResult {
  configured: boolean;
  source?: string;
  reason?: string;
}

export interface FetchOptions {
  /** include per-model month breakdown where supported (DeepInfra) */
  models?: boolean;
}

/** One provider adapter: credential detection separate from data fetch. */
export interface Provider {
  id: string;
  label: string;
  loginUrl?: string;
  /** Resolve credentials without network I/O. Never prompts, never refreshes. */
  detect(): Promise<DetectResult>;
  /** Fetch a snapshot. Returns error snapshots instead of throwing. */
  fetch(opts?: FetchOptions): Promise<Snapshot>;
}

export interface Trend {
  provider: string;
  basis: "percent" | "balance";
  balance?: number;
  currency?: string;
  remainingPercent?: number;
  dailyRate: number | null;
  estimatedDaysLeft: number | null;
  lowBalance: boolean;
  samples: number;
  spanHours: number;
}
