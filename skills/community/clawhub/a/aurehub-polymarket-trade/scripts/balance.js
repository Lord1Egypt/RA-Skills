import { fileURLToPath } from 'url';
import { existsSync, realpathSync } from 'fs';
import { join } from 'path';
import { homedir } from 'os';
import { ethers } from 'ethers';
import { loadConfig, resolveRpcUrl } from './lib/config.js';
import { createSigner } from './lib/signer.js';
import { createL2Client } from './lib/clob.js';
import { runSetupEnvCheck } from './setup.js';

const ERC20_ABI = ['function balanceOf(address) view returns (uint256)'];
const AUREHUB_DIR = join(homedir(), '.aurehub');
const DEFAULT_DATA_URL = 'https://data-api.polymarket.com';

export async function fetchPositions(address, cfg) {
  try {
    const { default: axios } = await import('axios');
    const dataUrl = cfg.yaml?.polymarket?.data_url ?? DEFAULT_DATA_URL;
    const res = await axios.get(
      `${dataUrl}/positions?user=${address}&sizeThreshold=.1`,
      { timeout: 10_000 },
    );
    return Array.isArray(res.data) ? res.data : [];
  } catch {
    return [];
  }
}

export async function getBalances(cfg, opts = {}) {
  const rpcUrl = resolveRpcUrl(cfg);
  const provider = new ethers.providers.JsonRpcProvider(rpcUrl);
  const wallet = (await createSigner(cfg, { accountIndex: opts.accountIndex })).connect(provider);
  const address = wallet.address;

  const contracts = cfg.yaml?.contracts ?? {};
  const usdceAddr = contracts.usdc_e ?? '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174';
  if (!ethers.utils.isAddress(usdceAddr)) throw new Error(`Invalid contract address in config: usdc_e = "${usdceAddr}"`);

  const polBal   = await provider.getBalance(address);
  const usdce    = new ethers.Contract(usdceAddr, ERC20_ABI, provider);
  const usdceBal = await usdce.balanceOf(address);

  const result = {
    address,
    pol:       parseFloat(ethers.utils.formatEther(polBal)).toFixed(4),
    usdce:     ethers.utils.formatUnits(usdceBal, 6),
    clob:      null,
    positions: [],
  };

  const credsPath = join(AUREHUB_DIR, '.polymarket_clob');
  if (existsSync(credsPath)) {
    try {
      const client = await createL2Client(cfg, wallet, credsPath);
      await client.updateBalanceAllowance({ asset_type: 'COLLATERAL' });
      const bal = await client.getBalanceAllowance({ asset_type: 'COLLATERAL' });
      const raw = parseFloat(bal.balance);
      if (!isNaN(raw)) result.clob = (raw / 1e6).toFixed(2);
    } catch { /* CLOB balance optional */ }
  }

  result.positions = await fetchPositions(address, cfg);

  return result;
}

export function formatBalances(b) {
  const lines = [
    `💰 ${b.address}`,
    `   POL:    ${b.pol}`,
    `   USDC.e: $${parseFloat(b.usdce).toFixed(2)}  ← trading token`,
  ];
  if (b.clob !== null) lines.push(`   CLOB:   $${b.clob}  ← available for orders`);

  if (b.positions?.length > 0) {
    lines.push('');
    lines.push('   Positions:');
    for (const p of b.positions) {
      const size  = parseFloat(p.size).toFixed(2);
      const price = parseFloat(p.curPrice).toFixed(2);
      const value = parseFloat(p.currentValue).toFixed(2);
      lines.push(`     ${p.outcome.padEnd(4)} ${p.slug.padEnd(32)} ${size} shares  $${price}/share  ~$${value}`);
    }
  }

  lines.push('');
  return lines.join('\n');
}

// ── CLI entry point ───────────────────────────────────────────────────────────
if (process.argv[1] && realpathSync(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const accountIdx = (() => {
    const args = process.argv.slice(2);
    const i = args.indexOf('--account');
    if (i === -1) return undefined;
    const raw = args[i + 1];
    const v = parseInt(raw, 10);
    if (Number.isNaN(v) || v < 0 || String(v) !== raw) { console.error('--account must be a non-negative integer'); process.exit(1); }
    return v;
  })();

  (async () => {
    try {
      runSetupEnvCheck();
      const cfg = loadConfig();
      const b = await getBalances(cfg, { accountIndex: accountIdx });
      console.log(formatBalances(b));
    } catch (e) {
      console.error('❌', e.message);
      process.exit(1);
    }
  })();
}
