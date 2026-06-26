import { SignalResult, TradeSide } from '../types.js';

export function decide(signal: SignalResult, buyThreshold: number, sellThreshold: number, minConf: number): { side?: TradeSide; why: string } {
  if (signal.confidence < minConf) return { why: `confidence too low ${signal.confidence}` };
  const x = signal.sentiment * signal.impact;
  if (x >= buyThreshold) return { side: 'BUY_WBNB', why: `x=${x} >= buyThreshold` };
  if (x <= -sellThreshold) return { side: 'SELL_WBNB', why: `x=${x} <= -sellThreshold` };
  return { why: `neutral x=${x}` };
}
