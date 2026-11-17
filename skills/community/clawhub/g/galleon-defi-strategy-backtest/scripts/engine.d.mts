export class BacktestError extends Error { code: string; constructor(code: string); }
export type Strategy = { type: 'buy-and-hold' } | { type: 'dca'; amountUsd: number; everyBars: number } | { type: 'sma'; period: number };
export interface Contribution { timestamp: string; amountUsd: number; }
export interface StrategySpec { schemaVersion: 1; initialCashUsd: number; feeBps: number; slippageBps: number; strategy: Strategy; contributions?: Contribution[]; }
export interface DailyDataset {
  schemaVersion: 1; identity: { namespace: string; id: string }; unit: 'USD'; intervalSeconds: 86400;
  priceType: 'aggregate-snapshot' | 'venue-close';
  provenance: { provider: string; source: string; retrievedAt: string; synthetic: boolean; rawSha256?: string };
  candles: { timestamp: string; close: number }[];
}
export interface Metrics {
  initialCashUsd: number; totalContributedUsd: number; endingEquityUsd: number; netProfitUsd: number;
  contributionAdjustedProfitPct: number; timeWeightedReturnPct: number; maxDrawdownPct: number;
  totalFeesUsd: number; totalSlippageUsd: number; tradeCount: number; endingCashUsd: number; endingAssetUnits: number;
}
export interface Trade {
  side: 'buy' | 'sell'; decisionAt: string; executedAt: string; markUsd: number; fillUsd: number;
  quantity: number; notionalUsd: number; feeUsd: number; slippageUsd: number; cashDeltaUsd: number;
}
export interface EquityPoint { timestamp: string; closeUsd: number; cashUsd: number; assetUnits: number; equityUsd: number; contributionUsd: number; returnIndex: number; drawdownPct: number; }
export interface Period { firstObservation: string; lastObservation: string; observations: number; }
export interface Simulation { metrics: Metrics; equityCurve: EquityPoint[]; trades: Trade[]; }
export interface BacktestReport extends Simulation {
  ok: true; schemaVersion: 1; model: 'daily-long-only-next-observation-v1'; identity: DailyDataset['identity']; unit: 'USD';
  priceType: DailyDataset['priceType']; provenance: DailyDataset['provenance']; period: Period; spec: StrategySpec;
  benchmark: Simulation & { strategy: 'buy-and-hold' };
  comparison: { timeWeightedReturnDifferencePct: number; endingEquityDifferenceUsd: number }; assumptions: string[]; limitations: string[];
}
export interface StrategyTemplate {
  readonly id: string; readonly label: string; readonly strategy: Readonly<{ type: 'buy-and-hold' } | { type: 'dca'; everyBars: number } | { type: 'sma'; period: number }>;
  readonly requiredParameters: readonly string[];
  readonly horizon: Readonly<{ intervalSeconds: 86400; minimumObservationsPerPeriod: number; minimumValidationObservations: number; recommendedValidationObservations: number }>;
  readonly requiredData: readonly string[];
}
export const STRATEGY_TEMPLATES: readonly StrategyTemplate[];
export interface TemplateParameters { initialCashUsd: number; feeBps: number; slippageBps: number; amountUsd?: number; contributions?: Contribution[]; }
export interface ValidationOptions { splitIndex?: number; stressFeeBps?: number; stressSlippageBps?: number; }
export interface ValidationPeriod {
  period: Period; baseline: BacktestReport; higherCosts: BacktestReport;
  costSensitivity: { endingEquityDifferenceUsd: number; timeWeightedReturnDifferencePct: number; maxDrawdownDifferencePct: number; modeledCostDifferenceUsd: number };
}
export interface StrategyValidationReport {
  ok: true; schemaVersion: 1; model: 'daily-frozen-rule-validation-v1'; evidence: 'historical-simulation';
  identity: DailyDataset['identity']; provenance: DailyDataset['provenance']; frozenSpec: StrategySpec;
  partition: { splitIndex: number; firstHeldOutObservation: string; inputObservations: number; minimumObservationsPerPeriod: number };
  costScenarios: { baseline: { feeBps: number; slippageBps: number }; higherCosts: { feeBps: number; slippageBps: number } };
  accounting: { mode: 'independent-restarts'; initialCashUsdPerPeriod: number; convention: string };
  periods: { reference: ValidationPeriod; heldOut: ValidationPeriod }; assumptions: string[]; limitations: string[];
}
export function validateDataset(dataset: unknown): DailyDataset;
export function validateSpec(spec: unknown, dataset: DailyDataset): StrategySpec;
export function runBacktest(dataset: DailyDataset, spec: StrategySpec): BacktestReport;
export function createStrategySpec(templateId: string, parameters: TemplateParameters): StrategySpec;
export function runStrategyValidation(dataset: DailyDataset, spec: StrategySpec, options?: ValidationOptions): StrategyValidationReport;
