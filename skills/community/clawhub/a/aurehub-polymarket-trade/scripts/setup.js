import { existsSync, readFileSync, writeFileSync, chmodSync, realpathSync } from 'fs';
import { join } from 'path';
import { homedir } from 'os';
import { fileURLToPath } from 'url';
import { loadConfig, resolveRpcUrl } from './lib/config.js';
import { createSigner } from './lib/signer.js';
import { createL1Client } from './lib/clob.js';

const AUREHUB_DIR = join(homedir(), '.aurehub');
const SETUP_PATH_FILE = join(AUREHUB_DIR, '.polymarket_setup_path');
// SCRIPTS_DIR = absolute path to this scripts/ directory (written to .polymarket_setup_path at setup time)
const SCRIPTS_DIR = fileURLToPath(new URL('.', import.meta.url));

// ── Exported check functions (used by all scripts) ────────────────────────────

export function checkEnvFile(aurehubDir = AUREHUB_DIR) {
  const path = join(aurehubDir, '.env');
  if (!existsSync(path)) {
    throw new Error(
      `Missing ~/.aurehub/.env. Copy the example file from the skill directory:\n` +
      `  cp <skill-dir>/.env.example ~/.aurehub/.env\n` +
      `Then set POLYGON_RPC_URL to a Polygon JSON-RPC endpoint (e.g. https://polygon-rpc.com).`,
    );
  }
}

export function checkVaultFile(aurehubDir = AUREHUB_DIR) {
  const path = join(aurehubDir, '.wdk_vault');
  if (!existsSync(path)) {
    throw new Error(
      `Missing ~/.aurehub/.wdk_vault. This file is created by the xaut-trade skill setup.\n` +
      `Install xaut-trade first (npx skills add aurehub/skills → select xaut-trade) and complete its wallet setup, then return here.`,
    );
  }
}

export function checkPasswordFile(aurehubDir = AUREHUB_DIR) {
  const path = join(aurehubDir, '.wdk_password');
  if (!existsSync(path)) {
    throw new Error(
      `Missing ~/.aurehub/.wdk_password. This file is created by the xaut-trade skill setup.\n` +
      `Complete the xaut-trade wallet setup first, then return here.`,
    );
  }
}

export function checkConfigFile(aurehubDir = AUREHUB_DIR) {
  const path = join(aurehubDir, 'polymarket.yaml');
  if (!existsSync(path)) {
    throw new Error(
      `Missing ~/.aurehub/polymarket.yaml. Copy config.example.yaml:\n` +
      `  cp <skill-dir>/config.example.yaml ~/.aurehub/polymarket.yaml`,
    );
  }
}

/** Returns true/false (not throws) — caller decides whether to derive. */
export function checkClobCreds(aurehubDir = AUREHUB_DIR) {
  return existsSync(join(aurehubDir, '.polymarket_clob'));
}

export function checkNodeModules(scriptsDir) {
  const nm = join(scriptsDir, 'node_modules');
  if (!existsSync(nm)) {
    throw new Error(
      `node_modules not found at "${nm}".\nRun: cd ${scriptsDir} && npm install`,
    );
  }
}

/** Run all checks for trade flows (steps 1-8). Throws on first failure. */
export function runTradeEnvCheck(aurehubDir = AUREHUB_DIR) {
  checkVaultFile(aurehubDir);
  checkPasswordFile(aurehubDir);
  checkEnvFile(aurehubDir);
  checkConfigFile(aurehubDir);
  // step 5 (RPC URL resolvable) and step 6 (POL balance) are checked in trade.js
  // after provider is created
  if (!checkClobCreds(aurehubDir)) {
    throw new Error(
      `Missing ~/.aurehub/.polymarket_clob. Run: node scripts/setup.js`,
    );
  }
  // step 8: node_modules must exist
  const setupPathFile = join(aurehubDir, '.polymarket_setup_path');
  const scriptsDir = existsSync(setupPathFile)
    ? readFileSync(setupPathFile, 'utf8').trim()
    : SCRIPTS_DIR;
  checkNodeModules(scriptsDir);
}

/** Run env checks for setup flow (steps 1-5 — needs wallet but no CLOB creds yet). */
export function runSetupEnvCheck(aurehubDir = AUREHUB_DIR) {
  checkVaultFile(aurehubDir);
  checkPasswordFile(aurehubDir);
  checkEnvFile(aurehubDir);
  checkConfigFile(aurehubDir);
  // step 5: verify RPC URL env var is configured
  const cfg = loadConfig(aurehubDir);
  resolveRpcUrl(cfg);
}

/** Run env checks for browse flows (step 4 only — no wallet, no RPC, no CLOB needed).
 *  Browse uses only public HTTP APIs (Gamma + CLOB); no env file or RPC URL required. */
export function runBrowseEnvCheck(aurehubDir = AUREHUB_DIR) {
  checkConfigFile(aurehubDir);
}

// ── CLOB credential derivation ────────────────────────────────────────────────

export async function deriveClobCreds(aurehubDir = AUREHUB_DIR, opts = {}) {
  const cfg = loadConfig(aurehubDir);
  const wallet = await createSigner(cfg, { accountIndex: opts.accountIndex });
  const client = await createL1Client(cfg, wallet);
  const creds = await client.createApiKey(0);
  if (!creds.key || !creds.secret || !creds.passphrase) {
    throw new Error(
      `CLOB key derivation failed — Polymarket API returned incomplete credentials.\n` +
      `Wait a moment and re-run: node scripts/setup.js\n` +
      `If the problem persists, check that your wallet address is not geo-blocked (403 error = VPN required).`,
    );
  }
  const credsPath = join(aurehubDir, '.polymarket_clob');
  const data = {
    key: creds.key,
    secret: creds.secret,
    passphrase: creds.passphrase,
    nonce: creds.nonce ?? 0,
    derivedAt: new Date().toISOString(),
    walletAddress: wallet.address,
  };
  writeFileSync(credsPath, JSON.stringify(data, null, 2));
  try { chmodSync(credsPath, 0o600); } catch { console.warn(`⚠️  Could not restrict permissions on ${credsPath} — file may be readable by other users`); }
  // Write SCRIPTS_DIR for runtime resolution by other scripts
  writeFileSync(SETUP_PATH_FILE, SCRIPTS_DIR);
  const clobUrl = cfg.yaml?.polymarket?.clob_url ?? 'https://clob.polymarket.com';
  console.log(`✅ CLOB credentials saved to ${credsPath}`);
  console.log(`   Endpoint: ${clobUrl}`);
  console.log(`   Key: ${creds.key.slice(0, 12)}...`);
  console.log(`   Wallet: ${wallet.address}`);
  return data;
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
      runSetupEnvCheck();  // steps 1-5 including vault + password (needed for L1 signing)
      if (checkClobCreds()) {
        console.log('✅ Already configured. Delete ~/.aurehub/.polymarket_clob to re-derive.');
        process.exit(0);
      }
      await deriveClobCreds(undefined, { accountIndex: accountIdx });
    } catch (e) {
      console.error('❌', e.message);
      process.exit(1);
    }
  })();
}
