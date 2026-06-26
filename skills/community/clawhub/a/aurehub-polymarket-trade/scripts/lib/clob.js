import { readFileSync } from 'fs';
import { join } from 'path';
import { homedir } from 'os';

const DEFAULT_CLOB_URL = 'https://clob.polymarket.com';
const DEFAULT_CHAIN_ID = 137;
const DEFAULT_CREDS_PATH = join(homedir(), '.aurehub', '.polymarket_clob');

export function loadClobCreds(credsPath = DEFAULT_CREDS_PATH) {
  let raw;
  try {
    raw = readFileSync(credsPath, 'utf8');
  } catch {
    throw new Error(
      `CLOB credentials not found at "${credsPath}". Run: node scripts/setup.js`,
    );
  }
  try {
    return JSON.parse(raw);
  } catch (e) {
    throw new Error(
      `CLOB credentials corrupted at "${credsPath}": ${e.message}. Delete the file and re-run: node scripts/setup.js`,
    );
  }
}

export async function createL1Client(cfg, wallet) {
  const { ClobClient } = await import('@polymarket/clob-client');
  const host = cfg.yaml?.polymarket?.clob_url ?? DEFAULT_CLOB_URL;
  const chainId = cfg.yaml?.polymarket?.chain_id ?? DEFAULT_CHAIN_ID;
  return new ClobClient(host, chainId, wallet);
}

export async function createL2Client(cfg, wallet, credsPath = DEFAULT_CREDS_PATH) {
  const { ClobClient, SignatureType } = await import('@polymarket/clob-client');
  const host = cfg.yaml?.polymarket?.clob_url ?? DEFAULT_CLOB_URL;
  const chainId = cfg.yaml?.polymarket?.chain_id ?? DEFAULT_CHAIN_ID;
  const creds = loadClobCreds(credsPath);
  return new ClobClient(
    host, chainId, wallet,
    { key: creds.key, secret: creds.secret, passphrase: creds.passphrase },
    SignatureType.EOA,
    wallet.address,
  );
}
