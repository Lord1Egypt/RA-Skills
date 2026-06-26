#!/usr/bin/env node
// aave-position.js — Check Aave V3 position health on Optimism and Base
// Usage: node aave-position.js <address>
// Output: JSON with collateral, debt, available borrows, health factor per chain
// No external dependencies — uses Node.js built-ins only

const https = require('https');

const address = process.argv[2];
if (!address || !/^0x[0-9a-fA-F]{40}$/.test(address)) {
  console.error('Usage: node aave-position.js <0x-address>');
  process.exit(1);
}

const CHAINS = {
  optimism: {
    rpc: 'https://mainnet.optimism.io',
    pool: '0x794a61358D6845594F94dc1DB02A252b5b4814aD',
  },
  base: {
    rpc: 'https://mainnet.base.org',
    pool: '0xA238Dd80C259a72e81d7e4664a9801593F98d1c5',
  },
};

// getUserAccountData(address) selector
const SELECTOR = '0xbf92857c';
const TIMEOUT_MS = 8000;

// Pad address to 32 bytes (ABI encoding)
function encodeAddress(addr) {
  return addr.replace('0x', '').toLowerCase().padStart(64, '0');
}

// Decode ABI-encoded uint256 from 32-byte hex chunk
function decodeUint256(hex) {
  return BigInt('0x' + hex);
}

// Divide BigInt by 1e18, return string with 4 decimal places
function fromWad(val) {
  const whole = val / BigInt(1e18);
  const frac = (val % BigInt(1e18)) * 10000n / BigInt(1e18);
  return `${whole}.${frac.toString().padStart(4, '0')}`;
}

// Divide BigInt by 1e8 (USD base units), return string with 2 decimal places
function fromUSD8(val) {
  const whole = val / 100000000n;
  const frac = val % 100000000n * 100n / 100000000n;
  return `${whole}.${frac.toString().padStart(2, '0')}`;
}

function rpcCall(rpcUrl, to, data) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify({
      jsonrpc: '2.0',
      id: 1,
      method: 'eth_call',
      params: [{ to, data }, 'latest'],
    });

    const url = new URL(rpcUrl);
    const options = {
      hostname: url.hostname,
      path: url.pathname + url.search,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(body),
      },
    };

    const timer = setTimeout(() => {
      req.destroy();
      reject(new Error(`RPC call to ${rpcUrl} timed out after ${TIMEOUT_MS}ms`));
    }, TIMEOUT_MS);

    const req = https.request(options, res => {
      let d = '';
      res.on('data', c => d += c);
      res.on('end', () => {
        clearTimeout(timer);
        try {
          const json = JSON.parse(d);
          if (json.error) return reject(new Error(json.error.message || JSON.stringify(json.error)));
          resolve(json.result);
        } catch (e) {
          reject(new Error(`Invalid JSON from RPC: ${d.slice(0, 200)}`));
        }
      });
    });

    req.on('error', e => { clearTimeout(timer); reject(e); });
    req.write(body);
    req.end();
  });
}

async function queryChain(chainName, chain, addr) {
  const calldata = SELECTOR + encodeAddress(addr);

  let result;
  try {
    result = await rpcCall(chain.rpc, chain.pool, calldata);
  } catch (e) {
    return { error: e.message };
  }

  if (!result || result === '0x') {
    return { error: 'No data returned (address may have no Aave position)' };
  }

  // Strip 0x prefix, split into 32-byte (64 hex char) chunks
  const hex = result.replace('0x', '');
  if (hex.length < 64 * 6) {
    return { error: `Unexpected response length: ${hex.length}` };
  }

  const totalCollateralBase     = decodeUint256(hex.slice(0,   64));
  const totalDebtBase           = decodeUint256(hex.slice(64,  128));
  const availableBorrowsBase    = decodeUint256(hex.slice(128, 192));
  const currentLiquidationThreshold = decodeUint256(hex.slice(192, 256));
  const ltv                     = decodeUint256(hex.slice(256, 320));
  const healthFactor            = decodeUint256(hex.slice(320, 384));

  const healthFactorNum = Number(healthFactor) / 1e18;
  const data = {
    totalCollateralUSD:  fromUSD8(totalCollateralBase),
    totalDebtUSD:        fromUSD8(totalDebtBase),
    availableBorrowsUSD: fromUSD8(availableBorrowsBase),
    liquidationThresholdBps: currentLiquidationThreshold.toString(),
    ltvBps:              ltv.toString(),
    healthFactor:        fromWad(healthFactor),
  };

  // Health factor of type(uint256).max means no debt (infinite)
  const MAX_UINT256 = 2n ** 256n - 1n;
  if (healthFactor === MAX_UINT256) {
    data.healthFactor = 'infinite (no debt)';
  } else if (healthFactorNum < 1.2) {
    data.warning = `⚠️  Health factor ${data.healthFactor} is critically low — liquidation risk!`;
  }

  return data;
}

async function main() {
  const [optimismData, baseData] = await Promise.all([
    queryChain('optimism', CHAINS.optimism, address),
    queryChain('base',     CHAINS.base,     address),
  ]);

  const output = {
    address,
    chains: {
      optimism: optimismData,
      base: baseData,
    },
  };

  console.log(JSON.stringify(output, null, 2));
}

main().catch(e => { console.error(e.message); process.exit(1); });
