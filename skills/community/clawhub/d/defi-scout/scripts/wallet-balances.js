#!/usr/bin/env node
// wallet-balances.js — ETH + key ERC-20 balances on Optimism and Base
// Usage: node wallet-balances.js <address>

const https = require('https');
const addr = process.argv[2];
if (!addr) { console.error('Usage: wallet-balances.js <address>'); process.exit(1); }

const TOKENS = {
  optimism: [
    { symbol: 'USDC',  addr: '0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85', dec: 6 },
    { symbol: 'USDT',  addr: '0x94b008aA00579c1307B0EF2c499aD98a8ce58e58', dec: 6 },
    { symbol: 'WETH',  addr: '0x4200000000000000000000000000000000000006', dec: 18 },
    { symbol: 'OP',    addr: '0x4200000000000000000000000000000000000042', dec: 18 },
    { symbol: 'VELO',  addr: '0x9560e827aF36c94D2Ac33a39bCE1Fe78631088Db', dec: 18 },
  ],
  base: [
    { symbol: 'USDC',  addr: '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913', dec: 6 },
    { symbol: 'WETH',  addr: '0x4200000000000000000000000000000000000006', dec: 18 },
    { symbol: 'AERO',  addr: '0x940181a94A35A4569E4529A3CDfB74e38FD98631', dec: 18 },
    { symbol: 'cbETH', addr: '0x2Ae3F1Ec7F1F5012CFEab0185bfc7aa3cf0DEc22', dec: 18 },
  ]
};
const RPC = { optimism: 'mainnet.optimism.io', base: 'mainnet.base.org' };
const CG_IDS = 'ethereum,optimism,aerodrome-finance,coinbase-wrapped-staked-eth';
const balanceOf = a => '0x70a08231' + a.slice(2).padStart(64, '0');

function rpc(host, method, params) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify({ jsonrpc: '2.0', id: 1, method, params });
    const req = https.request({ hostname: host, path: '/', method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Content-Length': body.length } },
      res => { let d = ''; res.on('data', c => d += c); res.on('end', () => resolve(JSON.parse(d))); });
    req.on('error', reject); req.write(body); req.end();
  });
}

function cgFetch(path) {
  return new Promise((resolve, reject) => {
    https.get({ hostname: 'api.coingecko.com', path,
      headers: { 'Accept': 'application/json', 'User-Agent': 'Mozilla/5.0' } },
      res => { let d = ''; res.on('data', c => d += c); res.on('end', () => resolve(JSON.parse(d))); }
    ).on('error', reject);
  });
}

async function main() {
  const prices = await cgFetch(`/api/v3/simple/price?ids=${CG_IDS}&vs_currencies=usd`);
  const ETH_USD  = prices.ethereum?.usd || 0;
  const OP_USD   = prices.optimism?.usd || 0;
  const AERO_USD = prices['aerodrome-finance']?.usd || 0;
  const CBETH_USD= prices['coinbase-wrapped-staked-eth']?.usd || 0;

  const result = { address: addr, ethPriceUsd: ETH_USD, chains: {}, totalUsd: 0 };

  for (const [chain, tokens] of Object.entries(TOKENS)) {
    const host = RPC[chain];
    const ethBal = await rpc(host, 'eth_getBalance', [addr, 'latest']);
    const ethAmt = parseInt(ethBal.result, 16) / 1e18;
    const tokenBals = await Promise.all(tokens.map(t =>
      rpc(host, 'eth_call', [{ to: t.addr, data: balanceOf(addr) }, 'latest'])
    ));

    const priceMap = { ETH: ETH_USD, WETH: ETH_USD, OP: OP_USD, AERO: AERO_USD, cbETH: CBETH_USD, USDC: 1, USDT: 1 };
    const holdings = [{ symbol: 'ETH', amount: parseFloat(ethAmt.toFixed(8)), usd: parseFloat((ethAmt * ETH_USD).toFixed(4)) }];

    tokens.forEach((t, i) => {
      const amt = parseInt(tokenBals[i].result, 16) / Math.pow(10, t.dec);
      if (amt > 0.000001) {
        const usdPx = priceMap[t.symbol] || 0;
        holdings.push({ symbol: t.symbol, amount: parseFloat(amt.toFixed(t.dec === 6 ? 4 : 8)), usd: parseFloat((amt * usdPx).toFixed(4)) });
      }
    });

    const chainTotal = holdings.reduce((s, h) => s + h.usd, 0);
    result.chains[chain] = { holdings, totalUsd: parseFloat(chainTotal.toFixed(4)) };
    result.totalUsd += chainTotal;
  }

  result.totalUsd = parseFloat(result.totalUsd.toFixed(4));
  console.log(JSON.stringify(result, null, 2));
}

main().catch(e => { console.error(e.message); process.exit(1); });
