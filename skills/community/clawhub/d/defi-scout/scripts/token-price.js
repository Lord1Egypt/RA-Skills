#!/usr/bin/env node
// token-price.js — Token price via CoinGecko (no API key required)
// Usage: node token-price.js <coingecko-id> [<id2> ...]
// Example: node token-price.js ethereum optimism aerodrome-finance

const https = require('https');
const ids = process.argv.slice(2);
if (!ids.length) { console.error('Usage: token-price.js <coingecko-id> [...]'); process.exit(1); }

function cgFetch(path) {
  return new Promise((resolve, reject) => {
    https.get({ hostname: 'api.coingecko.com', path, headers: { 'Accept': 'application/json', 'User-Agent': 'Mozilla/5.0' } },
      res => { let d = ''; res.on('data', c => d += c); res.on('end', () => resolve(JSON.parse(d))); }
    ).on('error', reject);
  });
}

cgFetch(`/api/v3/simple/price?ids=${ids.join(',')}&vs_currencies=usd&include_24hr_change=true`)
  .then(raw => {
    const result = {};
    for (const [id, data] of Object.entries(raw)) {
      result[id] = { priceUsd: data.usd, change24h: data.usd_24h_change ? parseFloat(data.usd_24h_change.toFixed(2)) : null };
    }
    console.log(JSON.stringify(result, null, 2));
  }).catch(e => { console.error(e.message); process.exit(1); });
