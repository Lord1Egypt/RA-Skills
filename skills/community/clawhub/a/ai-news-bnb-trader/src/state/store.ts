import fs from 'fs';
import path from 'path';

export type TradeRecord = {
  id: string;
  ts: number;
  side: 'BUY_WBNB' | 'SELL_WBNB';
  amountInUsd: number;
  px: number;
  txHash?: string;
  gasUsd?: number;
  reason: string;
};

export type BotState = {
  newsSeen: string[];
  trades: TradeRecord[];
  panic: boolean;
  safeMode: boolean;
  consecutiveFailures: number;
  lastTradeTs: number;
};

const initial: BotState = { newsSeen: [], trades: [], panic: false, safeMode: false, consecutiveFailures: 0, lastTradeTs: 0 };

export class JsonStore {
  private file: string;
  state: BotState;

  constructor(dir: string) {
    fs.mkdirSync(dir, { recursive: true });
    this.file = path.join(dir, 'bot-state.json');
    this.state = fs.existsSync(this.file) ? JSON.parse(fs.readFileSync(this.file, 'utf8')) : initial;
  }

  save() { fs.writeFileSync(this.file, JSON.stringify(this.state, null, 2)); }

  markNews(id: string) {
    this.state.newsSeen.push(id);
    if (this.state.newsSeen.length > 50000) this.state.newsSeen = this.state.newsSeen.slice(-20000);
    this.save();
  }

  hasNews(id: string) { return this.state.newsSeen.includes(id); }

  addTrade(t: TradeRecord) { this.state.trades.push(t); this.state.lastTradeTs = t.ts; this.save(); }
}
