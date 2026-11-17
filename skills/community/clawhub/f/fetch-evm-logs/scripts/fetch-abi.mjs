#!/usr/bin/env node
/**
 * Fetch verified contract ABI from public sources (Sourcify, then Etherscan API).
 * Usage:
 *   node fetch-abi.mjs --chainId 1 --address 0x... [--out ./src/abi] [--etherscanKey KEY]
 */
import fs from 'fs';
import path from 'path';

function arg(name, fallback) {
  const i = process.argv.indexOf(`--${name}`);
  if (i >= 0 && process.argv[i + 1]) return process.argv[i + 1];
  return fallback;
}

const chainId = Number(arg('chainId'));
const address = String(arg('address', '')).toLowerCase();
const outDir = path.resolve(arg('out', path.join(process.cwd(), 'src/abi')));
const etherscanKey =
  arg('etherscanKey') || process.env.ETHERSCAN_API_KEY || '';

if (!chainId || !/^0x[a-f0-9]{40}$/.test(address)) {
  console.error('Usage: node fetch-abi.mjs --chainId <id> --address 0x... [--out dir]');
  process.exit(1);
}

const outPath = path.join(outDir, `abi_${address}_${chainId}.json`);

async function fromSourcify() {
  const urls = [
    `https://repo.sourcify.dev/contracts/full_match/${chainId}/${address}/metadata.json`,
    `https://repo.sourcify.dev/contracts/partial_match/${chainId}/${address}/metadata.json`,
    `https://sourcify.dev/server/v2/contract/${chainId}/${address}?fields=abi`,
  ];
  for (const url of urls) {
    try {
      const res = await fetch(url);
      if (!res.ok) continue;
      const data = await res.json();
      if (Array.isArray(data?.output?.abi)) return data.output.abi;
      if (Array.isArray(data?.abi)) return data.abi;
      if (Array.isArray(data?.compilation?.artifacts?.abi)) {
        return data.compilation.artifacts.abi;
      }
    } catch {
      // try next
    }
  }
  return null;
}

async function fromEtherscan() {
  if (!etherscanKey) return null;
  const url =
    `https://api.etherscan.io/v2/api?chainid=${chainId}` +
    `&module=contract&action=getabi&address=${address}&apikey=${etherscanKey}`;
  const res = await fetch(url);
  if (!res.ok) return null;
  const data = await res.json();
  if (data.status !== '1' || typeof data.result !== 'string') return null;
  try {
    const abi = JSON.parse(data.result);
    return Array.isArray(abi) ? abi : null;
  } catch {
    return null;
  }
}

const abi = (await fromSourcify()) || (await fromEtherscan());
if (!abi) {
  console.error(
    'ABI not found via Sourcify' +
      (etherscanKey ? ' or Etherscan' : ' (set ETHERSCAN_API_KEY for explorer fallback)') +
      '. Ask the user to provide the ABI JSON.',
  );
  process.exit(2);
}

fs.mkdirSync(outDir, { recursive: true });
fs.writeFileSync(outPath, JSON.stringify(abi, null, 2));
console.log(`Wrote ${outPath}`);
console.log(`Events: ${abi.filter((x) => x?.type === 'event').map((e) => e.name).join(', ') || '(none)'}`);
