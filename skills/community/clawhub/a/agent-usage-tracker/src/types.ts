export interface ModelPricing {
  inputCostPerMillion: number;
  outputCostPerMillion: number;
}

export interface UsageEventInput {
  sessionId: string;
  model: string;
  promptTokens: number;
  completionTokens: number;
  timestamp?: string;
  metadata?: Record<string, unknown>;
}

export interface UsageRecord extends UsageEventInput {
  id: number;
  totalTokens: number;
  inputCostUsd: number;
  outputCostUsd: number;
  totalCostUsd: number;
  timestamp: string;
}

export interface UsageQuery {
  sessionId?: string;
  model?: string;
  startTime?: string;
  endTime?: string;
}

export interface UsageSummary {
  totalRequests: number;
  promptTokens: number;
  completionTokens: number;
  totalTokens: number;
  totalCostUsd: number;
  byModel: Array<{
    model: string;
    requests: number;
    promptTokens: number;
    completionTokens: number;
    totalTokens: number;
    totalCostUsd: number;
  }>;
  bySession: Array<{
    sessionId: string;
    requests: number;
    promptTokens: number;
    completionTokens: number;
    totalTokens: number;
    totalCostUsd: number;
  }>;
}

export interface TimeSeriesPoint {
  bucket: string;
  requests: number;
  promptTokens: number;
  completionTokens: number;
  totalTokens: number;
  totalCostUsd: number;
}

export interface UsageTrackerOptions {
  dbPath?: string;
  costCalculator?: {
    calculateCost(model: string, promptTokens: number, completionTokens: number): {
      inputCostUsd: number;
      outputCostUsd: number;
      totalCostUsd: number;
    };
  };
}

export interface BudgetPolicy {
  name: string;
  limitUsd: number;
  warningThreshold?: number;
  sessionId?: string;
  model?: string;
  startTime?: string;
  endTime?: string;
}

export interface StoredBudgetPolicy extends BudgetPolicy {
  createdAt: string;
  updatedAt: string;
}

export interface BudgetEvaluation {
  budgetName: string;
  limitUsd: number;
  spentUsd: number;
  remainingUsd: number;
  usageRatio: number;
  status: "ok" | "warning" | "exceeded";
}
