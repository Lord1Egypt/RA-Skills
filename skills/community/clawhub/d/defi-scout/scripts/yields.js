#!/usr/bin/env node
// yields.js — Top yield pools on Optimism and Base from DeFiLlama
// Usage: node yields.js [--chain optimism|base|all] [--min-tvl 1000000] [--top 20]

const https = require('https');
const args = process.argv.slice(2);
const chainFilter = args.includes('--chain') ? args[args.indexOf('--chain') + 1] : 'all';
const minTvl = args.includes('--min-tvl') ? parseInt(args[args.indexOf('--min-tvl') + 1]) : 1_000_000;
const top = args.includes('--top') ? parseInt(args[args.indexOf('--top') + 1]) : 20;

function fetch(url) {
  return new Promise((resolve, reject) => {
    https.get(url, res => {
      let d = ''; res.on('data', c => d += c);
      res.on('end', () => resolve(JSON.parse(d)));
    }).on('error', reject);
  });
}

async function main() {
  const data = await fetch('https://yields.llama.fi/pools');
  const CHAINS = { optimism: 'Optimism', base: 'Base' };
  const targetChains = chainFilter === 'all'
    ? Object.values(CHAINS)
    : [CHAINS[chainFilter] || chainFilter];

  const pools = data.data
    .filter(p => targetChains.includes(p.chain))
    .filter(p => p.tvlUsd >= minTvl)
    .filter(p => p.apy > 0)
    .sort((a, b) => b.apy - a.apy)
    .slice(0, top)
    .map(p => ({
      chain: p.chain,
      protocol: p.project,
      pool: p.symbol,
      apy: parseFloat(p.apy.toFixed(2)),
      tvlUsd: Math.round(p.tvlUsd),
      stablePair: p.stablecoin || false,
      ilRisk: !p.stablecoin,
      apyReward: p.apyReward ? parseFloat(p.apyReward.toFixed(2)) : 0,
      apyBase: p.apyBase ? parseFloat(p.apyBase.toFixed(2)) : 0,
      rewardTokens: p.rewardTokens && p.rewardTokens.length ? p.rewardTokens.map(addr => {
        const known = {
          '0x940181a94a35a4569e4529a3cdfb74e38fd98631': 'AERO',
          '0x9560e827af36c94d2ac33a39bce1fe78631088db': 'VELO',
          '0x4200000000000000000000000000000000000042': 'OP',
          '0x4200000000000000000000000000000000000006': 'WETH',
          '0x833589fcd6edb6e08f4c7c32d4f71b54bda02913': 'USDC',
        };
        return known[addr?.toLowerCase()] || addr?.slice(0,8) + '...';
      }).join(', ') : null,
    }));

  const result = {
    fetchedAt: new Date().toISOString(),
    filters: { chains: targetChains, minTvlUsd: minTvl, topN: top },
    stablePools: pools.filter(p => p.stablePair),
    volatilePools: pools.filter(p => !p.stablePair),
    all: pools
  };

  console.log(JSON.stringify(result, null, 2));
}

main().catch(e => { console.error(e.message); process.exit(1); });
