import { NewsItem, SignalResult } from '../types.js';
import { ISignalModel } from './interface.js';

const bullish = ['binance', 'bnb burn', 'listing', 'partnership', 'upgrade', 'etf', 'adoption', 'recovery'];
const bearish = ['hack', 'exploit', 'breach', 'fine', 'lawsuit', 'ban', 'freeze', 'delist', 'regulation', 'congestion'];

export class RuleSignalModel implements ISignalModel {
  async analyze(news: NewsItem): Promise<SignalResult> {
    const text = `${news.title} ${news.body}`.toLowerCase();
    let score = 0;
    const tags: string[] = [];
    for (const k of bullish) if (text.includes(k)) { score += 0.25; tags.push(k); }
    for (const k of bearish) if (text.includes(k)) { score -= 0.25; tags.push(k); }

    const rel = ['bnb', 'bsc', 'binance', 'cz', 'usdt', 'busd'].some((k) => text.includes(k));
    const impact = Math.min(1, Math.abs(score) + (rel ? 0.3 : 0.1));
    const sentiment = Math.max(-1, Math.min(1, score));
    const confidence = Math.min(1, 0.45 + tags.length * 0.1 + (rel ? 0.15 : 0));

    return {
      sentiment,
      confidence,
      tags,
      impact,
      reason: rel ? `RuleModel relevant tags=${tags.join(',') || 'none'}` : 'RuleModel low relevance'
    };
  }
}
