/** Pure daily spot simulation. No network, signer, storage or host dependencies. */
export class BacktestError extends Error {
  constructor(code) { super(code); this.name = 'BacktestError'; this.code = code; }
}
const fail = code => { throw new BacktestError(code); };
const object = value => value !== null && typeof value === 'object' && !Array.isArray(value);
const finite = (value, minimum, maximum) => typeof value === 'number' && Number.isFinite(value) && value >= minimum && value <= maximum;
function keys(value, allowed, code) {
  if (!object(value) || Object.keys(value).some(key => !allowed.includes(key))) fail(code);
}
function timestamp(value) {
  if (typeof value !== 'string' || !/^\d{4}-\d{2}-\d{2}T00:00:00\.000Z$/.test(value)) fail('invalid_timestamp');
  const parsed = Date.parse(value);
  if (!Number.isSafeInteger(parsed) || new Date(parsed).toISOString() !== value) fail('invalid_timestamp');
  return parsed;
}
export function validateDataset(dataset) {
  keys(dataset, ['schemaVersion', 'identity', 'unit', 'intervalSeconds', 'priceType', 'provenance', 'candles'], 'invalid_dataset');
  if (dataset.schemaVersion !== 1 || dataset.unit !== 'USD' || dataset.intervalSeconds !== 86400 || !['aggregate-snapshot', 'venue-close'].includes(dataset.priceType)) fail('unsupported_dataset');
  keys(dataset.identity, ['namespace', 'id'], 'invalid_identity');
  if (![dataset.identity.namespace, dataset.identity.id].every(value => typeof value === 'string' && /^[a-z0-9][a-z0-9:._-]{0,127}$/.test(value))) fail('invalid_identity');
  keys(dataset.provenance, ['provider', 'source', 'retrievedAt', 'synthetic', 'rawSha256'], 'invalid_provenance');
  if (typeof dataset.provenance.provider !== 'string' || !/^[a-z0-9][a-z0-9-]{0,63}$/.test(dataset.provenance.provider) || typeof dataset.provenance.synthetic !== 'boolean') fail('invalid_provenance');
  const retrieved = Date.parse(dataset.provenance.retrievedAt);
  if (!Number.isSafeInteger(retrieved) || typeof dataset.provenance.retrievedAt !== 'string' || new Date(retrieved).toISOString() !== dataset.provenance.retrievedAt) fail('invalid_provenance');
  if (typeof dataset.provenance.source !== 'string') fail('invalid_provenance');
  if (dataset.provenance.synthetic) {
    if (!/^fixture:[a-z0-9-]+$/.test(dataset.provenance.source)) fail('invalid_provenance');
  } else {
    let url;
    try { url = new URL(dataset.provenance.source); } catch { fail('invalid_provenance'); }
    if (url.protocol !== 'https:' || url.username || url.password || url.search || url.hash) fail('invalid_provenance');
  }
  if (dataset.provenance.rawSha256 !== undefined && !/^[a-f0-9]{64}$/.test(dataset.provenance.rawSha256)) fail('invalid_provenance');
  if (!Array.isArray(dataset.candles) || dataset.candles.length < 2 || dataset.candles.length > 10000) fail('invalid_candle_count');
  let previous;
  for (const row of dataset.candles) {
    keys(row, ['timestamp', 'close'], 'invalid_candle');
    const instant = timestamp(row.timestamp);
    if (!finite(row.close, 1e-12, 1e12)) fail('invalid_price');
    if (instant > retrieved) fail('observation_after_retrieval');
    if (previous !== undefined && instant - previous !== 86400000) fail('nonconsecutive_daily_candles');
    previous = instant;
  }
  return dataset;
}
export function validateSpec(spec, dataset) {
  keys(spec, ['schemaVersion', 'initialCashUsd', 'feeBps', 'slippageBps', 'strategy', 'contributions'], 'invalid_spec');
  if (spec.schemaVersion !== 1 || !finite(spec.initialCashUsd, 0.01, 1e12) || !finite(spec.feeBps, 0, 1000) || !finite(spec.slippageBps, 0, 1000)) fail('invalid_spec');
  const strategy = spec.strategy;
  if (!object(strategy)) fail('invalid_strategy');
  if (strategy.type === 'buy-and-hold') keys(strategy, ['type'], 'invalid_strategy');
  else if (strategy.type === 'dca') {
    keys(strategy, ['type', 'amountUsd', 'everyBars'], 'invalid_strategy');
    if (!finite(strategy.amountUsd, 0.01, 1e12) || !Number.isSafeInteger(strategy.everyBars) || strategy.everyBars < 1 || strategy.everyBars > dataset.candles.length) fail('invalid_strategy');
  } else if (strategy.type === 'sma') {
    keys(strategy, ['type', 'period'], 'invalid_strategy');
    if (!Number.isSafeInteger(strategy.period) || strategy.period < 2 || strategy.period >= dataset.candles.length) fail('invalid_strategy');
  } else fail('unsupported_strategy');
  const rows = spec.contributions ?? [];
  if (!Array.isArray(rows) || rows.length > dataset.candles.length) fail('invalid_contributions');
  const dates = new Set(dataset.candles.map(row => row.timestamp)), seen = new Set();
  for (const row of rows) {
    keys(row, ['timestamp', 'amountUsd'], 'invalid_contributions');
    timestamp(row.timestamp);
    if (!dates.has(row.timestamp) || seen.has(row.timestamp) || !finite(row.amountUsd, 0.01, 1e12)) fail('invalid_contributions');
    seen.add(row.timestamp);
  }
  return spec;
}
function simulate(dataset, spec, strategy) {
  const feeRate = spec.feeBps / 10000, slipRate = spec.slippageBps / 10000;
  const flows = new Map((spec.contributions ?? []).map(row => [row.timestamp, row.amountUsd]));
  let cash = spec.initialCashUsd, units = 0, pending;
  let previousEquity = spec.initialCashUsd, index = 1, peak = 1, maxDrawdown = 0;
  let contributed = spec.initialCashUsd, totalFees = 0, totalSlippage = 0;
  const equityCurve = [], trades = [];
  for (let i = 0; i < dataset.candles.length; i++) {
    const row = dataset.candles[i], preFlowEquity = cash + units * row.close;
    const marketFactor = i === 0 ? 1 : preFlowEquity / previousEquity;
    const flow = flows.get(row.timestamp) ?? 0;
    cash += flow; contributed += flow;
    const preTradeEquity = preFlowEquity + flow;
    if (pending?.side === 'buy' && cash >= 1e-10) {
      const budget = Math.min(cash, pending.budget ?? cash), fill = row.close * (1 + slipRate);
      const notional = budget / (1 + feeRate), quantity = notional / fill, fee = notional * feeRate;
      const slippage = quantity * (fill - row.close);
      cash -= budget; units += quantity; totalFees += fee; totalSlippage += slippage;
      trades.push({ side: 'buy', decisionAt: pending.decisionAt, executedAt: row.timestamp, markUsd: row.close, fillUsd: fill, quantity, notionalUsd: notional, feeUsd: fee, slippageUsd: slippage, cashDeltaUsd: -budget });
    } else if (pending?.side === 'sell' && units > 0) {
      const quantity = units, fill = row.close * (1 - slipRate), notional = quantity * fill;
      const fee = notional * feeRate, slippage = quantity * (row.close - fill);
      cash += notional - fee; units = 0; totalFees += fee; totalSlippage += slippage;
      trades.push({ side: 'sell', decisionAt: pending.decisionAt, executedAt: row.timestamp, markUsd: row.close, fillUsd: fill, quantity, notionalUsd: notional, feeUsd: fee, slippageUsd: slippage, cashDeltaUsd: notional - fee });
    }
    const equity = cash + units * row.close;
    index *= marketFactor * (equity / preTradeEquity);
    peak = Math.max(peak, index);
    const drawdown = Math.max(0, 1 - index / peak);
    maxDrawdown = Math.max(maxDrawdown, drawdown);
    if (![equity, index, drawdown].every(Number.isFinite)) fail('numeric_overflow');
    equityCurve.push({ timestamp: row.timestamp, closeUsd: row.close, cashUsd: cash, assetUnits: units, equityUsd: equity, contributionUsd: flow, returnIndex: index, drawdownPct: drawdown * 100 });
    previousEquity = equity;
    pending = undefined;
    if (strategy.type === 'buy-and-hold') pending = { side: 'buy', decisionAt: row.timestamp };
    else if (strategy.type === 'dca' && i % strategy.everyBars === 0) pending = { side: 'buy', budget: strategy.amountUsd, decisionAt: row.timestamp };
    else if (strategy.type === 'sma' && i >= strategy.period - 1) {
      let sum = 0;
      for (let j = i - strategy.period + 1; j <= i; j++) sum += dataset.candles[j].close;
      const bullish = row.close > sum / strategy.period;
      if (bullish) pending = { side: 'buy', decisionAt: row.timestamp };
      else pending = { side: 'sell', decisionAt: row.timestamp };
    }
  }
  const endingEquityUsd = previousEquity, netProfitUsd = endingEquityUsd - contributed;
  return {
    metrics: { initialCashUsd: spec.initialCashUsd, totalContributedUsd: contributed, endingEquityUsd, netProfitUsd, contributionAdjustedProfitPct: netProfitUsd / contributed * 100, timeWeightedReturnPct: (index - 1) * 100, maxDrawdownPct: maxDrawdown * 100, totalFeesUsd: totalFees, totalSlippageUsd: totalSlippage, tradeCount: trades.length, endingCashUsd: cash, endingAssetUnits: units },
    equityCurve, trades,
  };
}
export function runBacktest(dataset, spec) {
  validateDataset(dataset); validateSpec(spec, dataset);
  const result = simulate(dataset, spec, spec.strategy);
  const benchmark = simulate(dataset, spec, { type: 'buy-and-hold' });
  return {
    ok: true, schemaVersion: 1, model: 'daily-long-only-next-observation-v1',
    identity: { ...dataset.identity }, unit: dataset.unit, priceType: dataset.priceType,
    provenance: { ...dataset.provenance },
    period: { firstObservation: dataset.candles[0].timestamp, lastObservation: dataset.candles.at(-1).timestamp, observations: dataset.candles.length },
    spec: JSON.parse(JSON.stringify(spec)),
    ...result, benchmark: { strategy: 'buy-and-hold', ...benchmark },
    comparison: { timeWeightedReturnDifferencePct: result.metrics.timeWeightedReturnPct - benchmark.metrics.timeWeightedReturnPct, endingEquityDifferenceUsd: result.metrics.endingEquityUsd - benchmark.metrics.endingEquityUsd },
    assumptions: [
      'Signals use only observations through decisionAt; execution uses the next daily observation.',
      'The next observed price is a simulation mark, not a guaranteed venue fill; fixed adverse slippage and fees apply to every trade.',
      'Long-only fractional spot units; no leverage, shorting, funding, borrow, staking yield, taxes, liquidity constraints or cash interest.',
      'Positive contributions enter cash at the observation after market movement and before pending orders; withdrawals are unsupported.',
      'Returns and drawdown use a flow-neutral index, split before the contribution and after trading costs; final assets are marked without forced liquidation.',
      'Benchmark has identical dates, contributions and costs; its first buy also executes on the second observation.',
      'Floating-point arithmetic is for research simulation, not token base-unit reconciliation or transaction construction.',
    ],
    limitations: [
      ...(dataset.provenance.synthetic ? ['Synthetic fixture: results describe an invented price path.'] : []),
      ...(dataset.priceType === 'aggregate-snapshot' ? ['Aggregated daily prices are not venue candle closes or executable quotes.'] : []),
      'No intraday stop, order-book, latency, partial-fill, capacity or venue-specific cost model.',
      'Historical fit and a benchmark comparison do not establish future performance or authorize trading.',
    ],
  };
}

const template = (id, label, strategy, minimumObservationsPerPeriod, requiredParameters = []) => Object.freeze({
  id, label, strategy: Object.freeze(strategy), requiredParameters: Object.freeze(requiredParameters),
  horizon: Object.freeze({ intervalSeconds: 86400, minimumObservationsPerPeriod, minimumValidationObservations: minimumObservationsPerPeriod * 2, recommendedValidationObservations: 180 }),
  requiredData: Object.freeze(['One resolved asset identity and USD prices.', 'Consecutive daily UTC observations with provider, source, retrieval time and price type.', 'Explicit positive contributions for new funding; no assumed deposits.']),
});
/** Fixed research starting points, not optimized parameters or recommendations. */
export const STRATEGY_TEMPLATES = Object.freeze([
  template('buy-and-hold', 'Buy and hold', { type: 'buy-and-hold' }, 3),
  template('weekly-dca', 'Funded weekly DCA', { type: 'dca', everyBars: 7 }, 9, ['amountUsd']),
  template('sma-10', '10-day moving average', { type: 'sma', period: 10 }, 12),
  template('sma-30', '30-day moving average', { type: 'sma', period: 30 }, 32),
]);
export function createStrategySpec(templateId, parameters) {
  const selected = STRATEGY_TEMPLATES.find(value => value.id === templateId);
  if (!selected) fail('unknown_template');
  keys(parameters, ['initialCashUsd', 'feeBps', 'slippageBps', 'amountUsd', 'contributions'], 'invalid_template_parameters');
  if (!finite(parameters.initialCashUsd, 0.01, 1e12) || !finite(parameters.feeBps, 0, 1000) || !finite(parameters.slippageBps, 0, 1000)) fail('invalid_template_parameters');
  if (selected.strategy.type === 'dca' ? !finite(parameters.amountUsd, 0.01, 1e12) : parameters.amountUsd !== undefined) fail('invalid_template_parameters');
  if (parameters.contributions !== undefined && !Array.isArray(parameters.contributions)) fail('invalid_template_parameters');
  const spec = { schemaVersion: 1, initialCashUsd: parameters.initialCashUsd, feeBps: parameters.feeBps, slippageBps: parameters.slippageBps,
    strategy: { ...selected.strategy, ...(selected.strategy.type === 'dca' ? { amountUsd: parameters.amountUsd } : {}) },
    ...(parameters.contributions !== undefined ? { contributions: parameters.contributions.map(row => ({ ...row })) } : {}) };
  // Date membership is checked against the supplied dataset by the runner.
  for (const row of spec.contributions ?? []) {
    keys(row, ['timestamp', 'amountUsd'], 'invalid_contributions'); timestamp(row.timestamp);
    if (!finite(row.amountUsd, 0.01, 1e12)) fail('invalid_contributions');
  }
  return spec;
}
function minimumValidationSamples(strategy) {
  if (strategy.type === 'sma') return strategy.period + 2; // Warmup, a possible fill, then a later mark.
  if (strategy.type === 'dca') return Math.max(3, strategy.everyBars + 2); // Two possible scheduled fills.
  return 3;
}
/** Chronological frozen-rule comparison. Each period starts independently in cash. */
export function runStrategyValidation(dataset, spec, options = {}) {
  validateDataset(dataset); validateSpec(spec, dataset);
  keys(options, ['splitIndex', 'stressFeeBps', 'stressSlippageBps'], 'invalid_validation_options');
  const splitIndex = options.splitIndex === undefined ? Math.floor(dataset.candles.length / 2) : options.splitIndex;
  if (!Number.isSafeInteger(splitIndex) || splitIndex <= 0 || splitIndex >= dataset.candles.length) fail('invalid_split');
  const minimumObservationsPerPeriod = minimumValidationSamples(spec.strategy);
  if (splitIndex < minimumObservationsPerPeriod || dataset.candles.length - splitIndex < minimumObservationsPerPeriod) fail('insufficient_validation_samples');
  const stressFeeBps = options.stressFeeBps === undefined ? Math.min(1000, Math.max(spec.feeBps * 2, spec.feeBps + 10)) : options.stressFeeBps;
  const stressSlippageBps = options.stressSlippageBps === undefined ? Math.min(1000, Math.max(spec.slippageBps * 2, spec.slippageBps + 10)) : options.stressSlippageBps;
  if (!finite(stressFeeBps, spec.feeBps, 1000) || !finite(stressSlippageBps, spec.slippageBps, 1000) || stressFeeBps + stressSlippageBps <= spec.feeBps + spec.slippageBps) fail('invalid_stress_costs');
  function evaluate(candles) {
    const periodDataset = { ...dataset, candles };
    const dates = new Set(candles.map(row => row.timestamp));
    const periodSpec = { ...spec, contributions: (spec.contributions ?? []).filter(row => dates.has(row.timestamp)) };
    const baseline = runBacktest(periodDataset, periodSpec);
    const higherCosts = runBacktest(periodDataset, { ...periodSpec, feeBps: stressFeeBps, slippageBps: stressSlippageBps });
    return { period: baseline.period, baseline, higherCosts, costSensitivity: {
      endingEquityDifferenceUsd: higherCosts.metrics.endingEquityUsd - baseline.metrics.endingEquityUsd,
      timeWeightedReturnDifferencePct: higherCosts.metrics.timeWeightedReturnPct - baseline.metrics.timeWeightedReturnPct,
      maxDrawdownDifferencePct: higherCosts.metrics.maxDrawdownPct - baseline.metrics.maxDrawdownPct,
      modeledCostDifferenceUsd: higherCosts.metrics.totalFeesUsd + higherCosts.metrics.totalSlippageUsd - baseline.metrics.totalFeesUsd - baseline.metrics.totalSlippageUsd,
    } };
  }
  const reference = evaluate(dataset.candles.slice(0, splitIndex));
  const heldOut = evaluate(dataset.candles.slice(splitIndex));
  return {
    ok: true, schemaVersion: 1, model: 'daily-frozen-rule-validation-v1', evidence: 'historical-simulation',
    identity: { ...dataset.identity }, provenance: { ...dataset.provenance }, frozenSpec: JSON.parse(JSON.stringify(spec)),
    partition: { splitIndex, firstHeldOutObservation: dataset.candles[splitIndex].timestamp, inputObservations: dataset.candles.length, minimumObservationsPerPeriod },
    costScenarios: { baseline: { feeBps: spec.feeBps, slippageBps: spec.slippageBps }, higherCosts: { feeBps: stressFeeBps, slippageBps: stressSlippageBps } },
    accounting: { mode: 'independent-restarts', initialCashUsdPerPeriod: spec.initialCashUsd,
      convention: 'Each period starts with zero asset units, declared initial cash, its own dated contributions, fresh indicator warmup and no pending order. Final reference positions and decisions do not carry into held-out balances.' },
    periods: { reference, heldOut },
    assumptions: [
      'One supplied rule is frozen for both periods and both cost scenarios; no parameter search, ranking or optimization occurs.',
      'The split is chronological. This runner cannot prove that the user had not inspected or tuned on held-out observations before supplying the rule.',
      'Higher costs apply to both the rule and its same-flow buy-and-hold benchmark; fixed cost assumptions are not measured venue fills.',
      'Balances and returns are per-period independent experiments; they are not combined into a continuous account or live performance.',
    ],
    limitations: [
      ...(dataset.provenance.synthetic ? ['Synthetic fixture: no real asset performance evidence.'] : []),
      ...(Math.min(splitIndex, dataset.candles.length - splitIndex) < 90 ? ['At least one period has fewer than 90 daily observations; short samples limit inference.'] : []),
      ...(reference.baseline.metrics.tradeCount === 0 || heldOut.baseline.metrics.tradeCount === 0 ? ['At least one period has no modeled strategy fills; cash-only performance cannot establish trading behavior.'] : []),
      'Sample minimums permit accounting checks; they do not establish statistical significance, profitability or future performance.',
      'A historical replay is separate from live paper observation, execution readiness, wallet balances and permission to trade.',
      'The daily spot engine excludes intraday stops, leverage, funding, liquidity, venue depth and partial fills.',
    ],
  };
}
