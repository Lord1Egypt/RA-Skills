import { describe, it, expect } from 'vitest';
import { riskCheck } from '../src/risk/risk-manager.js';

const store: any = { state: { panic: false, safeMode: false, trades: [], lastTradeTs: 0 } };

describe('riskCheck', () => {
  it('rejects large order', () => {
    const r = riskCheck(store, {
      nowTs: 1, usdBalance: 1000, wbnbUsdValue: 0, orderUsd: 1000, estSlippageBps: 10, dailyPnlUsd: 0,
      cooldownSeconds: 10, maxTradesPerDay: 10, maxDailyLossUsd: 100, maxPositionPct: 0.5, maxTradeUsd: 200, maxSlippageBps: 50
    });
    expect(r.ok).toBe(false);
  });
});
