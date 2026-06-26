export interface BillingResult {
  success: boolean;
  payment_url?: string;
  error?: string;
  balance?: number;
}

export interface ChargeParams {
  userId: string;
  apiKey: string;
  priceUsdt: number;
  skillId: string;
  fetchFn?: typeof fetch;
}

export interface SkillResponse<T = unknown> {
  success: boolean;
  data?: T;
  error?: string;
  payment_url?: string;
}
