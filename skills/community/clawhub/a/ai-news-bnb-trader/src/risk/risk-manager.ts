import { JsonStore } from '../state/store.js';

export type RiskInput = {
  nowTs: number;
  usdBalance: number;
  wbnbUsdValue: number;
  orderUsd: number;
  estSlippageBps: number;
  dailyPnlUsd: number;
  cooldownSeconds: number;
  maxTradesPerDay: number;
  maxDailyLossUsd: number;
  maxPositionPct: number;
  maxTradeUsd: number;
  maxSlippageBps: number;
};

export function riskCheck(store: JsonStore, i: RiskInput): { ok: boolean; reason?: string } {
  if (store.state.panic) return { ok: false, reason: 'panic=true' };
  if (store.state.safeMode) return { ok: false, reason: 'safeMode=true' };
  if (i.orderUsd > i.maxTradeUsd) return { ok: false, reason: 'order > MAX_TRADE_USD' };
  if (i.estSlippageBps > i.maxSlippageBps) return { ok: false, reason: 'slippage too high' };
  if (i.dailyPnlUsd <= -Math.abs(i.maxDailyLossUsd)) return { ok: false, reason: 'daily loss hit' };

  const dayStart = new Date(); dayStart.setUTCHours(0,0,0,0);
  const todayTrades = store.state.trades.filter(t => t.ts >= Math.floor(dayStart.getTime()/1000)).length;
  if (todayTrades >= i.maxTradesPerDay) return { ok: false, reason: 'max trades/day reached' };

  if (store.state.lastTradeTs && i.nowTs - store.state.lastTradeTs < i.cooldownSeconds) return { ok: false, reason: 'cooldown' };

  const total = i.usdBalance + i.wbnbUsdValue;
  if (total > 0 && (i.wbnbUsdValue / total) > i.maxPositionPct) return { ok: false, reason: 'position pct too high' };

  return { ok: true };
}
