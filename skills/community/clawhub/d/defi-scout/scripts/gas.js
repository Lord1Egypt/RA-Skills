#!/usr/bin/env node
// gas.js — Current gas prices on Optimism and Base
// Usage: node gas.js

const https = require('https');

function rpc(host) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify({ jsonrpc: '2.0', id: 1, method: 'eth_gasPrice', params: [] });
    const req = https.request({ hostname: host, path: '/', method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Content-Length': body.length } },
      res => { let d = ''; res.on('data', c => d += c); res.on('end', () => resolve(JSON.parse(d))); });
    req.on('error', reject); req.write(body); req.end();
  });
}

function getEthPrice() {
  return new Promise((resolve, reject) => {
    https.get('https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd',
      res => { let d = ''; res.on('data', c => d += c);
        res.on('end', () => resolve(JSON.parse(d).ethereum?.usd || 2000)); })
      .on('error', () => resolve(2000));
  });
}

async function main() {
  const [opGas, baseGas, ethPrice] = await Promise.all([
    rpc('mainnet.optimism.io'),
    rpc('mainnet.base.org'),
    getEthPrice()
  ]);

  const toGwei = r => parseInt(r.result, 16) / 1e9;
  const txCostUsd = (gwei, gasUnits = 21000) => (gwei * gasUnits / 1e9) * ethPrice;
  const swapCostUsd = (gwei) => txCostUsd(gwei, 150000);

  const op = toGwei(opGas);
  const base = toGwei(baseGas);

  console.log(JSON.stringify({
    ethPriceUsd: ethPrice,
    optimism: {
      gasPriceGwei: parseFloat(op.toFixed(6)),
      simpleTransferUsd: parseFloat(txCostUsd(op).toFixed(6)),
      swapUsd: parseFloat(swapCostUsd(op).toFixed(6)),
      verdict: op < 0.01 ? 'very low — good time to transact' : op < 0.1 ? 'normal' : 'elevated'
    },
    base: {
      gasPriceGwei: parseFloat(base.toFixed(6)),
      simpleTransferUsd: parseFloat(txCostUsd(base).toFixed(6)),
      swapUsd: parseFloat(swapCostUsd(base).toFixed(6)),
      verdict: base < 0.01 ? 'very low — good time to transact' : base < 0.1 ? 'normal' : 'elevated'
    }
  }, null, 2));
}

main().catch(e => { console.error(e.message); process.exit(1); });
