import { AsterClient } from "@asterdex/aster-skills-hub";
import { OpenNewsClient } from "opennews-mcp";
import OpenAI from "openai";

/**
 * ============================================================
 * CONFIG
 * ============================================================
 */
const CONFIG = {
  WATCH_COINS: ["BTC", "ETH", "SOL", "BNB"],

  SYMBOL_MAP: {
    BTC: "BTCUSDT",
    ETH: "ETHUSDT",
    SOL: "SOLUSDT",
    BNB: "BNBUSDT"
  },

  NEWS: {
    sources: ["twitter", "coindesk", "cointelegraph", "theblock", "decrypt", "bloomberg"],
    timeRange: "1h",
    limit: 10,
    language: "en"
  },

  TRADE: {
    leverage: 5,
    positionSizeUSDT: 100,
    stopLossPct: 0.02,
    takeProfitPct: 0.04,
    orderType: "MARKET"
  },

  SENTIMENT: {
    minConfidence: 0.7,
    bullishThreshold: 0.65,
    bearishThreshold: 0.65
  },

  COOLDOWN_MS: 30 * 60 * 1000
};

/**
 * ============================================================
 * PROMPT — Bullish/Bearish classification
 * ============================================================
 */
const SENTIMENT_ANALYSIS_PROMPT = `
You are a professional cryptocurrency market analyst specializing in short-term price impact (1–4 hours).

Task: Determine whether the following news is bullish, bearish, or neutral for {COIN}.

News batch:
{NEWS_CONTENT}

Rules:
- If news is NOT directly related to {COIN}, return "neutral" and recommended_action "skip".
- If the source is unverified/anonymous rumor, cap confidence at 0.55 and likely "skip".
- Prefer official sources and major media over KOL commentary.
- Prefer fundamental/market-structure events over price predictions.

Bullish examples:
- Institutional buying / ETF inflows
- Regulatory approval / clear positive guidance
- Major successful upgrade / adoption / Tier-1 listing
- Major partnerships or integrations
- Strong on-chain accumulation signals

Bearish examples:
- Regulatory crackdown / lawsuit / delisting
- Hack/exploit/outage
- Whale/institutional sell-off signals
- Hawkish macro shock (rate hikes, liquidity tightening)
- Large token unlock / supply shock

Score (0-10) each:
1) source_credibility
2) event_importance
3) timeliness
4) market_sensitivity

Compute confidence (0..1) from weighted score:
confidence = (source_credibility*0.30 + event_importance*0.35 + timeliness*0.20 + market_sensitivity*0.15) / 10

Output STRICT JSON ONLY:
{
  "coin": "{COIN}",
  "sentiment": "bullish | bearish | neutral",
  "confidence": 0.0,
  "signal_strength": "strong | medium | weak",
  "scores": {
    "source_credibility": 0,
    "event_importance": 0,
    "timeliness": 0,
    "market_sensitivity": 0
  },
  "reasoning": {
    "key_factors": ["..."],
    "bullish_points": ["..."],
    "bearish_points": ["..."],
    "risk_factors": ["..."]
  },
  "recommended_action": "open_long | open_short | wait | skip",
  "urgency": "immediate | within_1h | within_4h | no_action",
  "summary": "One sentence summary"
}
`;

/**
 * ============================================================
 * News Monitor (OpenNews MCP)
 * ============================================================
 */
class NewsMonitor {
  constructor() {
    this.client = new OpenNewsClient({
      twitterBearerToken: process.env.TWITTER_BEARER_TOKEN
    });
    this.dedup = new Map(); // id -> timestamp
  }

  buildKeywords(coin) {
    const map = {
      BTC: ["Bitcoin", "BTC", "#Bitcoin", "$BTC", "Satoshi"],
      ETH: ["Ethereum", "ETH", "#Ethereum", "$ETH", "Vitalik", "EIP", "EVM"],
      SOL: ["Solana", "SOL", "#Solana", "$SOL", "Solana network"],
      BNB: ["BNB", "Binance", "#BNB", "$BNB", "BNBChain", "BSC", "CZ"]
    };
    return map[coin] || [coin];
  }

  cleanDedup() {
    const cutoff = Date.now() - 24 * 60 * 60 * 1000;
    for (const [id, ts] of this.dedup.entries()) {
      if (ts < cutoff) this.dedup.delete(id);
    }
  }

  formatForLLM(articles) {
    return articles
      .map(
        (a, i) => `
[Article ${i + 1}]
Source: ${a.source}
Author: ${a.author || "Unknown"}
PublishedAt: ${new Date(a.publishedAt).toISOString()}
Title: ${a.title || ""}
Content: ${(a.content || a.description || "").slice(0, 700)}
URL: ${a.url || ""}
Engagement: likes=${a.likes || 0} retweets=${a.retweets || 0} replies=${a.replies || 0}
`.trim()
      )
      .join("\n\n---\n\n");
  }

  async fetch(coin) {
    try {
      const keywords = this.buildKeywords(coin);
      const articles = await this.client.search({
        keywords,
        sources: CONFIG.NEWS.sources,
        timeRange: CONFIG.NEWS.timeRange,
        limit: CONFIG.NEWS.limit,
        language: CONFIG.NEWS.language,
        sortBy: "publishedAt"
      });

      const fresh = (articles || []).filter((a) => {
        if (!a?.id) return false;
        if (this.dedup.has(a.id)) return false;
        this.dedup.set(a.id, Date.now());
        return true;
      });

      this.cleanDedup();
      return fresh;
    } catch (e) {
      console.error(`[News] Fetch error for ${coin}:`, e?.message || e);
      return [];
    }
  }
}

/**
 * ============================================================
 * Sentiment Analyzer (OpenAI)
 * ============================================================
 */
class SentimentAnalyzer {
  constructor() {
    this.openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
  }

  async analyze(coin, formattedNews) {
    const prompt = SENTIMENT_ANALYSIS_PROMPT
      .replaceAll("{COIN}", coin)
      .replace("{NEWS_CONTENT}", formattedNews);

    const resp = await this.openai.chat.completions.create({
      model: "gpt-4o",
      temperature: 0.1,
      max_tokens: 1200,
      response_format: { type: "json_object" },
      messages: [
        {
          role: "system",
          content: "Return strict JSON only. No markdown. No extra text."
        },
        { role: "user", content: prompt }
      ]
    });

    return JSON.parse(resp.choices[0].message.content);
  }

  getTradeSignal(analysis) {
    const { sentiment, confidence, signal_strength, recommended_action } = analysis;

    if (recommended_action === "skip") return null;
    if (confidence < CONFIG.SENTIMENT.minConfidence) return null;
    if (signal_strength === "weak") return null;

    if (sentiment === "bullish" && confidence >= CONFIG.SENTIMENT.bullishThreshold) {
      return { side: "BUY", action: "open_long" };
    }
    if (sentiment === "bearish" && confidence >= CONFIG.SENTIMENT.bearishThreshold) {
      return { side: "SELL", action: "open_short" };
    }
    return null;
  }
}

/**
 * ============================================================
 * Aster Trader
 * ============================================================
 */
class AsterTrader {
  constructor() {
    this.client = new AsterClient({
      apiKey: process.env.ASTER_API_KEY,
      apiSecret: process.env.ASTER_API_SECRET,
      baseUrl: process.env.ASTER_BASE_URL || "https://api.asterdex.com"
    });
    this.cooldown = new Map(); // coin -> last trade timestamp
  }

  inCooldown(coin) {
    const last = this.cooldown.get(coin);
    return last && Date.now() - last < CONFIG.COOLDOWN_MS;
  }

  calcQty(price) {
    const notional = CONFIG.TRADE.positionSizeUSDT * CONFIG.TRADE.leverage;
    const raw = notional / price;
    return Math.floor(raw * 1000) / 1000; // 3 decimals
  }

  calcSLTP(price, side) {
    const { stopLossPct, takeProfitPct } = CONFIG.TRADE;
    if (side === "BUY") {
      return {
        stopLoss: +(price * (1 - stopLossPct)).toFixed(2),
        takeProfit: +(price * (1 + takeProfitPct)).toFixed(2)
      };
    }
    return {
      stopLoss: +(price * (1 + stopLossPct)).toFixed(2),
      takeProfit: +(price * (1 - takeProfitPct)).toFixed(2)
    };
  }

  async place(coin, side, analysis) {
    if (this.inCooldown(coin)) {
      console.log(`[Trade] ${coin} in cooldown, skip.`);
      return null;
    }

    const symbol = CONFIG.SYMBOL_MAP[coin];
    if (!symbol) throw new Error(`No symbol mapping for ${coin}`);

    await this.client.setLeverage({ symbol, leverage: CONFIG.TRADE.leverage });

    const ticker = await this.client.getTicker({ symbol });
    const price = Number(ticker.lastPrice);
    const quantity = this.calcQty(price);
    const { stopLoss, takeProfit } = this.calcSLTP(price, side);

    const order = {
      symbol,
      side,
      type: CONFIG.TRADE.orderType,
      quantity,
      leverage: CONFIG.TRADE.leverage,
      stopLoss,
      takeProfit,
      reduceOnly: false,
      metadata: {
        strategy: "crypto-news-trader",
        coin,
        sentiment: analysis.sentiment,
        confidence: analysis.confidence,
        signal_strength: analysis.signal_strength,
        summary: analysis.summary,
        executed_at: new Date().toISOString()
      }
    };

    console.log(`[Trade] Placing order:`, {
      symbol,
      side,
      quantity,
      price,
      stopLoss,
      takeProfit,
      summary: analysis.summary
    });

    const res = await this.client.createOrder(order);
    this.cooldown.set(coin, Date.now());
    console.log(`[Trade] Order placed. orderId=${res.orderId}`);
    return res;
  }
}

/**
 * ============================================================
 * Main
 * ============================================================
 */
async function runOnce() {
  const monitor = new NewsMonitor();
  const analyzer = new SentimentAnalyzer();
  const trader = new AsterTrader();

  for (const coin of CONFIG.WATCH_COINS) {
    console.log(`\n=== ${coin} ===`);

    // Step 1
    const articles = await monitor.fetch(coin);
    if (!articles.length) {
      console.log(`[News] No new articles.`);
      continue;
    }
    console.log(`[News] ${articles.length} new article(s).`);

    // Step 2
    const formatted = monitor.formatForLLM(articles);
    let analysis;
    try {
      analysis = await analyzer.analyze(coin, formatted);
    } catch (e) {
      console.error(`[Analyzer] Failed:`, e?.message || e);
      continue;
    }

    console.log(`[Analyzer]`, {
      sentiment: analysis.sentiment,
      confidence: analysis.confidence,
      signal_strength: analysis.signal_strength,
      action: analysis.recommended_action,
      summary: analysis.summary
    });

    const signal = analyzer.getTradeSignal(analysis);
    if (!signal) {
      console.log(`[Decision] No trade.`);
      continue;
    }

    // Step 3
    try {
      await trader.place(coin, signal.side, analysis);
    } catch (e) {
      console.error(`[Trade] Failed:`, e?.message || e);
    }
  }
}

/**
 * Clawhub entry: default export
 * If Clawhub provides its own scheduler, this runs per schedule.
 */
export default async function main() {
  // Basic env checks
  for (const k of ["ASTER_API_KEY", "ASTER_API_SECRET", "OPENAI_API_KEY"]) {
    if (!process.env[k]) throw new Error(`Missing required env var: ${k}`);
  }
  await runOnce();
}