// DealPilot 类型定义

export type Platform = "taobao" | "pdd" | "jd" | "yhd" | "vip";

export interface PriceRange {
  min?: number;
  max?: number;
}

export interface ShoppingRequest {
  product?: string;
  productUrl?: string;
  category?: string;
  budget?: PriceRange;
  priorities?: string[];
  quantity?: number;
  scenario?: "personal" | "gift" | "resale";
  urgency?: "low" | "medium" | "high";
  platforms?: Platform[];
  mustHave?: string[];
  mustAvoid?: string[];
}

export interface RiskItem {
  level: "low" | "medium" | "high";
  description: string;
  mitigation?: string;
}

export interface AltPlatform {
  platform: Platform;
  score: number;
  price?: number;
  keyReason: string;
}

export interface TimingAdvice {
  verdict: "buy_now" | "wait" | "compare_first";
  reason: string;
  waitDays?: number;
  betterPeriod?: string;
}

export interface PlatformSummary {
  platform: Platform;
  price?: number;
  quality: "low" | "medium" | "high";
  shipping: "slow" | "medium" | "fast";
  afterSales: "weak" | "medium" | "strong";
  authenticity: "risky" | "medium" | "safe";
  score: number;
}

export interface DecisionReport {
  recommendedPlatform: Platform;
  recommendedUrl?: string;
  recommendedPrice?: number;
  reasons: string[];
  risks: RiskItem[];
  alternatives: AltPlatform[];
  timingAdvice: TimingAdvice;
  comparison: PlatformSummary[];
  conclusion: string;
}

export interface SearchOptions {
  category?: string;
  minPrice?: number;
  maxPrice?: number;
  sortBy?: "price" | "sales" | "rating";
}

export interface FinalPrice {
  rawPrice: number;
  finalPrice: number;
  discountDesc: string[];
  isSubsidized: boolean;
}

export interface PlatformTraits {
  strength: string[];
  weakness: string[];
  bestFor: string[];
  worstFor: string[];
}
