#!/usr/bin/env node
// swap-quote.js — Price-based swap estimate using CoinGecko prices
// Usage: node swap-quote.js <token_in> <token_out> <amount_in> [--chain optimism|base]
// Example: node swap-quote.js ETH USDC 1.5 --chain base
// Note: Price estimate only — use protocol UI (Aerodrome/Velodrome) for execution

const https = require('https');

const args = process.argv.slice(2);
const chainFlagIdx = args.indexOf('--chain');
const chain = chainFlagIdx !== -1 ? args[chainFlagIdx + 1] : 'optimism';
const positional = args.filter((a, i) => a !== '--chain' && i !== chainFlagIdx + 1);

const [tokenInSymbol, tokenOutSymbol, amountInStr] = positional;

if (!tokenInSymbol || !tokenOutSymbol || !amountInStr) {
  console.error('Usage: node swap-quote.js <token_in> <token_out> <amount_in> [--chain optimism|base]');
  console.error('Example: node swap-quote.js ETH USDC 1.5 --chain base');
  process.exit(1);
}

if (!['optimism', 'base'].includes(chain)) {
  console.error('Chain must be "optimism" or "base"');
  process.exit(1);
}

const amountIn = parseFloat(amountInStr);
if (isNaN(amountIn) || amountIn <= 0) {
  console.error('amount_in must be a positive number');
  process.exit(1);
}

// CoinGecko IDs for supported symbols
const COINGECKO_IDS = {
  ETH:   'ethereum',
  WETH:  'ethereum',
  USDC:  'usd-coin',
  USDT:  'tether',
  OP:    'optimism',
  VELO:  'velodrome-finance',
  AERO:  'aerodrome-finance',
  CBETH: 'coinbase-wrapped-staked-eth',
};

const symIn  = tokenInSymbol.toUpperCase();
const symOut = tokenOutSymbol.toUpperCase();

const idIn  = COINGECKO_IDS[symIn];
const idOut = COINGECKO_IDS[symOut];

if (!idIn) {
  console.error(`Unsupported token: ${symIn}. Supported: ${Object.keys(COINGECKO_IDS).join(', ')}`);
  process.exit(1);
}
if (!idOut) {
  console.error(`Unsupported token: ${symOut}. Supported: ${Object.keys(COINGECKO_IDS).join(', ')}`);
  process.exit(1);
}

const DEX_FEE_PCT = 0.3;
const TIMEOUT_MS = 8000;

function fetchJSON(url) {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error(`Request timed out after ${TIMEOUT_MS}ms`)), TIMEOUT_MS);
    https.get(url, { headers: { 'User-Agent': 'defi-scout/1.0' } }, res => {
      if (res.statusCode === 301 || res.statusCode === 302) {
        clearTimeout(timer);
        return fetchJSON(res.headers.location).then(resolve).catch(reject);
      }
      if (res.statusCode === 429) {
        clearTimeout(timer);
        return reject(new Error('CoinGecko rate limit hit — wait 60s and retry'));
      }
      let d = '';
      res.on('data', c => d += c);
      res.on('end', () => {
        clearTimeout(timer);
        try { resolve(JSON.parse(d)); }
        catch (e) { reject(new Error(`Invalid JSON: ${d.slice(0, 200)}`)); }
      });
    }).on('error', e => { clearTimeout(timer); reject(e); });
  });
}

async function main() {
  // Deduplicate IDs for single API call
  const uniqueIds = [...new Set([idIn, idOut])].join(',');
  const url = `https://api.coingecko.com/api/v3/simple/price?ids=${uniqueIds}&vs_currencies=usd`;

  let prices;
  try {
    prices = await fetchJSON(url);
  } catch (e) {
    console.error(`CoinGecko error: ${e.message}`);
    process.exit(1);
  }

  const priceIn  = prices[idIn]?.usd;
  const priceOut = prices[idOut]?.usd;

  if (priceIn == null) {
    console.error(`Could not fetch price for ${symIn} (id: ${idIn})`);
    process.exit(1);
  }
  if (priceOut == null) {
    console.error(`Could not fetch price for ${symOut} (id: ${idOut})`);
    process.exit(1);
  }

  // estimatedAmountOut = (priceIn / priceOut) * amountIn * (1 - fee)
  const rawOut = (priceIn / priceOut) * amountIn;
  const estimatedAmountOut = rawOut * (1 - DEX_FEE_PCT / 100);

  console.log(JSON.stringify({
    tokenIn:              symIn,
    tokenOut:             symOut,
    amountIn,
    estimatedAmountOut:   parseFloat(estimatedAmountOut.toFixed(8)),
    priceIn,
    priceOut,
    feePct:               DEX_FEE_PCT,
    chain,
    disclaimer: 'Price estimate only — use protocol UI for exact quotes and execution',
  }, null, 2));
}

main().catch(e => { console.error(e.message); process.exit(1); });
