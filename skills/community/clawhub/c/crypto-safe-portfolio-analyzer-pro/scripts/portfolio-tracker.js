#!/usr/bin/env node
/**
 * Crypto Opportunity Scanner (US-friendly)
 * Uses CoinGecko (free, no key) + Coinbase public API
 * Outputs structured alerts for Discord #crypto channel
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

const CONFIG = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'config.json'), 'utf-8'));

// ─── Helpers ───────────────────────────────────────────────

function httpsGet(url) {
  return new Promise((resolve) => {
    const req = https.get(url, {
      timeout: 15000,
      headers: { 'User-Agent': 'OpenClaw-CryptoScanner/1.0', 'Accept': 'application/json' }
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try { resolve(JSON.parse(data)); }
        catch { resolve(null); }
      });
    });
    req.on('error', () => resolve(null));
    req.on('timeout', () => { req.destroy(); resolve(null); });
  });
}

// ─── CoinGecko Market Data ─────────────────────────────────

const COINGECKO_IDS = {
  BTC: 'bitcoin', ETH: 'ethereum', SOL: 'solana', XRP: 'ripple',
  DOGE: 'dogecoin', AVAX: 'avalanche-2', LINK: 'chainlink', ADA: 'cardano',
  DOT: 'polkadot', MATIC: 'matic-network', ATOM: 'cosmos', UNI: 'uniswap',
  NEAR: 'near', APT: 'aptos', SUI: 'sui', ARB: 'arbitrum',
  OP: 'optimism', INJ: 'injective-protocol', PEPE: 'pepe', SHIB: 'shiba-inu',
  RENDER: 'render-token', FET: 'fetch-ai', ONDO: 'ondo-finance', WIF: 'dogwifcoin'
};

async function getMarketData() {
  const ids = CONFIG.watchlist.map(c => COINGECKO_IDS[c]).filter(Boolean).join(',');
  const url = `https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=${ids}&order=market_cap_desc&per_page=50&sparkline=false&price_change_percentage=1h,24h,7d`;
  const data = await httpsGet(url);
  if (!data || !Array.isArray(data)) return [];
  return data;
}

// ─── Fear & Greed ──────────────────────────────────────────

async function getFearGreed() {
  const data = await httpsGet('https://api.alternative.me/fng/?limit=1');
  if (!data || !data.data || !data.data[0]) return null;
  const fg = data.data[0];
  const v = parseInt(fg.value);
  return {
    value: v,
    label: fg.value_classification,
    emoji: v <= 25 ? '😱' : v <= 45 ? '😰' : v <= 55 ? '😐' : v <= 75 ? '😊' : '🤑'
  };
}

// ─── Coinbase BTC Price (backup) ───────────────────────────

async function getCoinbasePrice(pair = 'BTC-USD') {
  const data = await httpsGet(`https://api.coinbase.com/v2/prices/${pair}/spot`);
  if (!data || !data.data) return null;
  return parseFloat(data.data.amount);
}

// ─── Analysis Engine ───────────────────────────────────────

function analyzeOpportunities(markets, fg) {
  const opps = [];

  for (const coin of markets) {
    const symbol = Object.keys(COINGECKO_IDS).find(k => COINGECKO_IDS[k] === coin.id) || coin.symbol.toUpperCase();
    const change24h = coin.price_change_percentage_24h || 0;
    const change7d = coin.price_change_percentage_7d_in_currency || 0;
    const change1h = coin.price_change_percentage_1h_in_currency || 0;
    const price = coin.current_price;
    const volume = coin.total_volume;
    const mcap = coin.market_cap;
    const ath = coin.ath;
    const athDrop = ath ? ((price - ath) / ath * 100) : 0;

    // ─── DIP BUY: Down big in 24h, high volume ───
    if (change24h <= -8 && volume > 50000000) {
      opps.push({
        type: 'DIP_BUY', coin: symbol, price, emoji: '🟢',
        action: 'BUY THE DIP',
        reason: `Down ${change24h.toFixed(1)}% in 24h with $${(volume/1e6).toFixed(0)}M volume — oversold bounce setup`,
        risk: 'HIGH', potential: '10-20% recovery bounce',
        score: Math.abs(change24h) * 1.5
      });
    }

    // ─── BREAKOUT: Up big with momentum ───
    if (change24h >= 8 && change1h >= 1 && volume > 50000000) {
      opps.push({
        type: 'BREAKOUT', coin: symbol, price, emoji: '🚀',
        action: 'RIDE BREAKOUT',
        reason: `Up ${change24h.toFixed(1)}% and still pushing (+${change1h.toFixed(1)}% last hour)`,
        risk: 'HIGH', potential: 'Continuation to next resistance',
        score: change24h * 1.2
      });
    }

    // ─── REVERSAL SETUP: Down 7d but bouncing today ───
    if (change7d <= -15 && change24h >= 3) {
      opps.push({
        type: 'REVERSAL', coin: symbol, price, emoji: '🔄',
        action: 'REVERSAL PLAY',
        reason: `Down ${change7d.toFixed(1)}% this week but bouncing +${change24h.toFixed(1)}% today — possible trend reversal`,
        risk: 'HIGH', potential: '15-30% recovery if reversal confirms',
        score: Math.abs(change7d) * 0.8
      });
    }

    // ─── VALUE BUY: Way below ATH with signs of life ───
    if (athDrop <= -70 && change24h >= 2 && mcap > 500000000) {
      opps.push({
        type: 'VALUE', coin: symbol, price, emoji: '💎',
        action: 'VALUE ACCUMULATE',
        reason: `${athDrop.toFixed(0)}% below ATH ($${ath.toLocaleString()}) — deep value with bullish momentum today`,
        risk: 'MEDIUM', potential: 'Multi-month recovery play',
        score: Math.abs(athDrop) * 0.5
      });
    }

    // ─── DUMP WARNING: Crashing hard ───
    if (change24h <= -12) {
      opps.push({
        type: 'WARNING', coin: symbol, price, emoji: '🚨',
        action: 'CAUTION / WAIT',
        reason: `Crashing ${change24h.toFixed(1)}% — wait for stabilization before entry`,
        risk: 'EXTREME', potential: 'Could go lower. Patience.',
        score: Math.abs(change24h) * 2
      });
    }
  }

  // Extreme Fear = contrarian buy signal
  if (fg && fg.value <= 20) {
    opps.push({
      type: 'SENTIMENT', coin: 'MARKET', price: 0, emoji: '😱',
      action: 'EXTREME FEAR — BUY ZONE',
      reason: `Fear & Greed at ${fg.value} (${fg.label}). Historically, extreme fear = best buying opportunities`,
      risk: 'MEDIUM', potential: 'Broad market mean reversion',
      score: (25 - fg.value) * 3
    });
  }

  opps.sort((a, b) => b.score - a.score);
  return opps;
}

// ─── Format Big Movers ────────────────────────────────────

function getBigMovers(markets) {
  return markets
    .filter(c => Math.abs(c.price_change_percentage_24h || 0) >= 5)
    .sort((a, b) => Math.abs(b.price_change_percentage_24h) - Math.abs(a.price_change_percentage_24h))
    .slice(0, 8)
    .map(c => {
      const symbol = Object.keys(COINGECKO_IDS).find(k => COINGECKO_IDS[k] === c.id) || c.symbol.toUpperCase();
      const change = c.price_change_percentage_24h;
      const emoji = change >= 0 ? '🟢' : '🔴';
      return { symbol, price: c.current_price, change: change.toFixed(2), volume: (c.total_volume / 1e6).toFixed(0), emoji };
    });
}

// ─── Main Scanner ──────────────────────────────────────────

async function runScan() {
  const args = process.argv.slice(2);
  const jsonOutput = args.includes('--json');

  // Fetch all data
  const [markets, fg, btcCoinbase] = await Promise.all([
    getMarketData(),
    getFearGreed(),
    getCoinbasePrice('BTC-USD')
  ]);

  if (!markets || markets.length === 0) {
    console.log('**⚠️ Crypto Scanner:** API unavailable. Will retry next scan.');
    return;
  }

  const btc = markets.find(m => m.id === 'bitcoin');
  const eth = markets.find(m => m.id === 'ethereum');
  const opportunities = analyzeOpportunities(markets, fg);
  const bigMovers = getBigMovers(markets);

  if (jsonOutput) {
    console.log(JSON.stringify({ timestamp: new Date().toISOString(), btc, eth, fg, opportunities, bigMovers }, null, 2));
    return;
  }

  // Format for Discord
  const lines = [];
  const now = new Date().toLocaleString('en-US', { timeZone: 'America/Los_Angeles', dateStyle: 'short', timeStyle: 'short' });

  lines.push(`**📊 Crypto Scanner** — ${now}`);
  lines.push('');

  // Market header
  if (btc) {
    const btcEmoji = btc.price_change_percentage_24h >= 0 ? '🟢' : '🔴';
    lines.push(`**BTC** ${btcEmoji} $${btc.current_price.toLocaleString()} (${btc.price_change_percentage_24h.toFixed(2)}%)`);
  }
  if (eth) {
    const ethEmoji = eth.price_change_percentage_24h >= 0 ? '🟢' : '🔴';
    lines.push(`**ETH** ${ethEmoji} $${eth.current_price.toLocaleString()} (${eth.price_change_percentage_24h.toFixed(2)}%)`);
  }
  if (fg) {
    lines.push(`**Fear & Greed:** ${fg.emoji} ${fg.value} — ${fg.label}`);
  }
  lines.push('');

  // Big movers
  if (bigMovers.length > 0) {
    lines.push('**⚡ Big Movers (24h):**');
    for (const m of bigMovers) {
      lines.push(`${m.emoji} **${m.symbol}** ${m.change}% | $${m.price.toLocaleString()} | Vol: $${m.volume}M`);
    }
    lines.push('');
  }

  // Opportunities
  if (opportunities.length > 0) {
    lines.push('**🎯 Opportunities:**');
    for (const o of opportunities.slice(0, 6)) {
      const riskTag = o.risk === 'EXTREME' ? '⛔' : o.risk === 'HIGH' ? '🔥' : o.risk === 'MEDIUM' ? '⚠️' : '✅';
      lines.push(`${o.emoji} **${o.coin}** — ${o.action}`);
      lines.push(`   ${o.reason}`);
      lines.push(`   ${riskTag} Risk: ${o.risk} | Target: ${o.potential}`);
    }
    lines.push('');
  }

  if (opportunities.length === 0 && bigMovers.length === 0) {
    lines.push('**⚪ Markets quiet.** No strong signals right now. Watching...');
    lines.push('');
  }

  lines.push('*Not financial advice. DYOR. Use stop-losses. 🐾*');

  console.log(lines.join('\n'));
}

runScan().catch(console.error);
