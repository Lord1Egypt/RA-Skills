import { fileURLToPath } from 'url';
import { existsSync, readFileSync, realpathSync } from 'fs';
import { join } from 'path';
import { homedir } from 'os';
import { ethers } from 'ethers';
import { loadConfig, resolveRpcUrl } from './lib/config.js';
import { createSigner } from './lib/signer.js';
import { polyGasOverrides } from './lib/gas.js';
import {
  checkEnvFile, checkVaultFile, checkPasswordFile,
  checkConfigFile, checkNodeModules,
} from './setup.js';
import { confirm } from './lib/prompt.js';

const AUREHUB_DIR = join(homedir(), '.aurehub');
const DEFAULT_DATA_URL = 'https://data-api.polymarket.com';

const CTF_ABI = [
  'function redeemPositions(address collateralToken, bytes32 parentCollectionId, bytes32 conditionId, uint256[] indexSets)',
];

const ERC20_ABI = ['function balanceOf(address) view returns (uint256)'];

// ── Exported pure helpers (tested) ───────────────────────────────────────────

/**
 * Split positions into redeemable standard vs negRisk buckets.
 * Non-redeemable positions are discarded.
 */
export function filterRedeemable(positions) {
  const redeemable = positions.filter(p => p.redeemable);
  return {
    standard: redeemable.filter(p => !p.negativeRisk),
    negRisk:  redeemable.filter(p => p.negativeRisk),
  };
}

/**
 * Derive CTF indexSets from outcomeIndex.
 * Gnosis CTF binary market: indexSet is a bitmask — bit N set means outcome N is included.
 * outcomeIndex=0 → [1] (bit 0), outcomeIndex=1 → [2] (bit 1).
 */
export function buildIndexSets(outcomeIndex) {
  if (outcomeIndex < 0 || outcomeIndex > 30) {
    throw new Error(`outcomeIndex ${outcomeIndex} out of supported range (0–30)`);
  }
  return [1 << outcomeIndex];
}

/**
 * Format a preview table for the given standard redeemable positions.
 * Uses position.outcome (string from API) for display — NOT derived from outcomeIndex.
 */
export function formatRedeemPreview(positions) {
  const lines = ['Redeemable positions:\n'];
  lines.push(`  ${'Market'.padEnd(40)}  ${'Outcome'.padEnd(7)}  ${'Shares'.padStart(7)}  Receive`);
  lines.push(`  ${'─'.repeat(40)}  ${'─'.repeat(7)}  ${'─'.repeat(7)}  ${'─'.repeat(7)}`);

  let totalCents = 0;
  for (const p of positions) {
    const shares  = parseFloat(p.size).toFixed(2);
    const receive = (parseFloat(p.size) * 1).toFixed(2); // 1 share = $1 at resolution
    totalCents += Math.round(parseFloat(p.size) * 100);
    lines.push(
      `  ${p.slug.padEnd(40)}  ${p.outcome.padEnd(7)}  ${shares.padStart(7)}  ~$${receive}`
    );
  }
  const total = (totalCents / 100).toFixed(2);
  lines.push('');
  lines.push(`  Total: ~$${total} USDC.e`);
  return lines.join('\n');
}

// ── Redeem execution ──────────────────────────────────────────────────────────

async function fetchRedeemablePositions(address, cfg) {
  const { default: axios } = await import('axios');
  const dataUrl = cfg.yaml?.polymarket?.data_url ?? DEFAULT_DATA_URL;
  // sizeThreshold=.01 (lower than balance.js .1) to catch small winning positions
  const res = await axios.get(
    `${dataUrl}/positions?user=${address}&sizeThreshold=.01`,
    { timeout: 10_000 },
  );
  if (!Array.isArray(res.data)) {
    throw new Error('Positions API returned unexpected response — cannot determine redeemable positions');
  }
  return res.data;
}

export async function redeem({ cfg, provider, wallet, marketFilter, dryRun }) {
  const contracts = cfg.yaml?.contracts ?? {};
  const usdceAddr = contracts.usdc_e   ?? '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174';
  const ctfAddr   = contracts.ctf_contract ?? '0x4D97DCd97eC945f40cF65F87097ACe5EA0476045';

  if (!ethers.utils.isAddress(usdceAddr)) throw new Error(`Invalid usdc_e address in config`);
  if (!ethers.utils.isAddress(ctfAddr))   throw new Error(`Invalid ctf_contract address in config`);

  // Gas check
  const polRaw = await provider.getBalance(wallet.address);
  const polBalance = parseFloat(ethers.utils.formatEther(polRaw));
  if (polBalance < 0.01) {
    throw new Error(`Insufficient POL gas: have ${polBalance.toFixed(4)} POL, need ≥ 0.01`);
  }

  // Fetch positions (throws on API error — no silent [] swallowing)
  const allPositions = await fetchRedeemablePositions(wallet.address, cfg);

  // Apply optional market filter
  const filtered = marketFilter
    ? allPositions.filter(p => p.slug === marketFilter || p.conditionId === marketFilter)
    : allPositions;

  const { standard, negRisk } = filterRedeemable(filtered);

  // Handle negRisk skip notice and empty standard bucket
  if (standard.length === 0) {
    if (negRisk.length > 0) {
      console.log(`\n⚠️  Skipped ${negRisk.length} negRisk position(s) (not supported in v1):`);
      for (const p of negRisk) console.log(`    ${p.slug} → redeem at polymarket.com`);
      return;
    }
    console.log('\nNo redeemable positions found.');
    return;
  }

  // Print negRisk notice when there are also standard positions to process
  if (negRisk.length > 0) {
    console.log(`\n⚠️  Skipped ${negRisk.length} negRisk position(s) (not supported in v1):`);
    for (const p of negRisk) console.log(`    ${p.slug} → redeem at polymarket.com`);
  }

  // Preview
  console.log('\n' + formatRedeemPreview(standard));

  if (dryRun) {
    console.log('\n[dry-run] No transactions submitted.');
    return;
  }

  // Single confirmation
  const confirmed = await confirm('\nRedeem all? (yes/no):');
  if (!confirmed) { console.log('Cancelled.'); return; }

  // Execute
  const ctf = new ethers.Contract(ctfAddr, CTF_ABI, wallet);
  const results = [];

  for (const p of standard) {
    try {
      console.log(`\nSubmitting redeem for ${p.slug}...`);
      const gasOverrides = await polyGasOverrides(provider);
      const tx = await ctf.redeemPositions(
        usdceAddr,
        ethers.constants.HashZero,
        ethers.utils.hexZeroPad(p.conditionId, 32),
        buildIndexSets(p.outcomeIndex),
        gasOverrides,
      );
      await tx.wait();
      console.log(`✅ Redeemed ${p.slug} — tx: ${tx.hash}`);
      results.push({ slug: p.slug, txHash: tx.hash, success: true });
    } catch (e) {
      console.error(`❌ Failed to redeem ${p.slug}: ${e.message}`);
      results.push({ slug: p.slug, success: false, error: e.message });
    }
  }

  // Post-redeem balance (only when at least one redemption succeeded)
  if (results.some(r => r.success)) {
    const usdce = new ethers.Contract(usdceAddr, ERC20_ABI, provider);
    const usdceBal = await usdce.balanceOf(wallet.address);
    const usdceFormatted = parseFloat(ethers.utils.formatUnits(usdceBal, 6)).toFixed(2);
    console.log(`\nUpdated balance: $${usdceFormatted} USDC.e`);
  }

  return results;
}

// ── CLI entry point ───────────────────────────────────────────────────────────
if (process.argv[1] && realpathSync(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const args = process.argv.slice(2);
  const getArg = f => { const i = args.indexOf(f); return i >= 0 ? args[i + 1] : null; };
  const dryRun      = args.includes('--dry-run');
  const marketFilter = getArg('--market') ?? null;
  const accountIdx = (() => { const v = getArg('--account'); if (v === null) return undefined; const n = parseInt(v, 10); if (Number.isNaN(n) || n < 0 || String(n) !== v) { console.error('--account must be a non-negative integer'); process.exit(1); } return n; })();

  (async () => {
    try {
      // Lighter env check — no CLOB credentials needed for on-chain redeem
      checkEnvFile(); checkVaultFile(); checkPasswordFile(); checkConfigFile();
      const setupPath = join(AUREHUB_DIR, '.polymarket_setup_path');
      const scriptsDir = existsSync(setupPath)
        ? readFileSync(setupPath, 'utf8').trim()
        : fileURLToPath(new URL('.', import.meta.url));
      checkNodeModules(scriptsDir);

      const cfg = loadConfig();
      const rpcUrl = resolveRpcUrl(cfg);
      const provider = new ethers.providers.JsonRpcProvider(rpcUrl);
      const wallet = (await createSigner(cfg, { accountIndex: accountIdx })).connect(provider);

      await redeem({ cfg, provider, wallet, marketFilter, dryRun });
    } catch (e) {
      if (e.response?.status === 403) {
        console.error('❌ 403 Forbidden — Polymarket API blocked in your region. Use a VPN.');
      } else {
        console.error('❌', e.message);
      }
      process.exit(1);
    }
  })();
}
