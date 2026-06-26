export const PLAN_LIMITS = {
  free: {
    semanticScans: false,
    semanticPreview: true,
    semanticPreviewCount: 2,
    apiScansPerMonth: 8,
    webhooks: 0,
    scanHistoryDays: 7,
    apiKeys: 1,
  },
  pro: {
    semanticScans: true,
    semanticPreview: false,
    semanticPreviewCount: Infinity,
    apiScansPerMonth: Infinity,
    webhooks: 5,
    scanHistoryDays: Infinity,
    apiKeys: 3,
  },
  team: {
    semanticScans: true,
    semanticPreview: false,
    semanticPreviewCount: Infinity,
    apiScansPerMonth: Infinity,
    webhooks: Infinity,
    scanHistoryDays: Infinity,
    apiKeys: 10,
  },
} as const;

export type Plan = keyof typeof PLAN_LIMITS;

export function getPlanLimits(plan: string) {
  return PLAN_LIMITS[plan as Plan] || PLAN_LIMITS.free;
}

export function getCurrentPeriodStart(): Date {
  const now = new Date();
  return new Date(now.getFullYear(), now.getMonth(), 1);
}
