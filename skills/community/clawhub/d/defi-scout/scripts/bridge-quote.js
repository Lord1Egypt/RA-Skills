#!/usr/bin/env node
// bridge-quote.js — Bridge fee quote via Across Protocol (no external deps)
// Usage: node bridge-quote.js <amount_eth> [from_chain=10] [to_chain=8453]
// Example: node bridge-quote.js 0.01 10 8453   (OP -> Base)
// Chains: 1=Ethereum, 10=Optimism, 8453=Base, 42161=Arbitrum

const https = require('https');

const amountEth = process.argv[2];
const fromChain = process.argv[3] || '10';
const toChain   = process.argv[4] || '8453';

if (!amountEth) {
  console.error('Usage: bridge-quote.js <amount_eth> [from_chain=10] [to_chain=8453]');
  process.exit(1);
}

// Parse ETH string to wei as BigInt (no ethers dependency)
function parseEther(ethStr) {
  const str = ethStr.trim();
  const [whole = '0', frac = ''] = str.split('.');
  const fracPadded = frac.padEnd(18, '0').slice(0, 18);
  if (!/^\d+$/.test(whole) || !/^\d+$/.test(fracPadded)) {
    throw new Error(`Invalid ETH amount: ${ethStr}`);
  }
  return BigInt(whole) * 1000000000000000000n + BigInt(fracPadded);
}

// Format wei BigInt to ETH string (6 decimal places)
function formatEther(wei) {
  if (wei < 0n) return '-' + formatEther(-wei);
  const weiStr = wei.toString().padStart(19, '0');
  const whole = weiStr.slice(0, -18) || '0';
  const frac = weiStr.slice(-18).slice(0, 6).replace(/0+$/, '') || '0';
  return `${whole}.${frac}`;
}

// Fetch with 10-second timeout
function fetchJSON(url) {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error('Request timed out after 10s')), 10000);
    https.get(url, res => {
      // Follow redirects
      if (res.statusCode === 301 || res.statusCode === 302) {
        clearTimeout(timer);
        return fetchJSON(res.headers.location).then(resolve).catch(reject);
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
  let amountWei;
  try {
    amountWei = parseEther(amountEth);
  } catch (e) {
    console.error(`Error: ${e.message}`);
    process.exit(1);
  }

  // WETH addresses (same on all OP Stack chains)
  const WETH = '0x4200000000000000000000000000000000000006';
  const url = `https://app.across.to/api/suggested-fees?inputToken=${WETH}&outputToken=${WETH}&originChainId=${fromChain}&destinationChainId=${toChain}&amount=${amountWei.toString()}`;

  let q;
  try {
    q = await fetchJSON(url);
  } catch (e) {
    console.error(`Bridge API error: ${e.message}`);
    process.exit(1);
  }

  if (q.isAmountTooLow) {
    console.log(JSON.stringify({ error: 'Amount too low for bridge' }));
    return;
  }

  const fee = BigInt(q.totalRelayFee?.total || q.relayFeeTotal || 0);
  const outputWei = amountWei - fee;
  const feePct = amountWei > 0n
    ? ((Number(fee) / Number(amountWei)) * 100).toFixed(4) + '%'
    : '0%';

  console.log(JSON.stringify({
    fromChain,
    toChain,
    inputEth: amountEth,
    outputEth: formatEther(outputWei),
    feeEth: formatEther(fee),
    feePct,
    estimatedFillSec: q.estimatedFillTimeSec,
    spokePool: q.spokePoolAddress,
    fillDeadline: q.fillDeadline
  }, null, 2));
}

main().catch(e => { console.error(e.message); process.exit(1); });
