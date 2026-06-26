export type NewsItem = {
  id: string;
  ts: number;
  source: string;
  title: string;
  body: string;
  url: string;
  lang: string;
};

export type SignalResult = {
  sentiment: number;
  confidence: number;
  tags: string[];
  impact: number;
  reason: string;
};

export type TradeSide = 'BUY_WBNB' | 'SELL_WBNB';
