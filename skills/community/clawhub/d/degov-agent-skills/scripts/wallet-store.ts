import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import crypto from 'node:crypto';
import { createInterface } from 'node:readline/promises';
import { createPublicClient, formatUnits, http, parseAbi } from 'viem';
import { privateKeyToAccount, generatePrivateKey } from 'viem/accounts';
import { base } from 'viem/chains';

const WALLET_FILE_MODE = 0o600;
const DEFAULT_STATE_DIR = path.join(os.homedir(), '.agents', 'state', 'dao-governance');
export const DEFAULT_WALLET_PATH = path.join(DEFAULT_STATE_DIR, 'wallet.json');
export const DEFAULT_PASSPHRASE_PATH = path.join(DEFAULT_STATE_DIR, 'wallet-passphrase');
const LEGACY_WALLET_PATHS = [
  path.join(os.homedir(), '.codex', 'memories', 'degov-agent-skills', 'dao-governance-wallet.json'),
];

export const USDC_ADDRESS = '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913';
const USDC_ABI = parseAbi(['function balanceOf(address) view returns (uint256)']);

interface EncryptedWalletPayload {
  algorithm: string;
  kdf: string;
  salt: string;
  iv: string;
  authTag: string;
  ciphertext: string;
}

interface WalletFile {
  createdAt: string;
  migratedAt?: string;
  address: `0x${string}`;
  privateKey?: `0x${string}`;
  crypto?: EncryptedWalletPayload;
}

export interface WalletAccount {
  walletPath: string;
  wallet: WalletFile;
  account: ReturnType<typeof privateKeyToAccount>;
}

export interface WalletBalance {
  raw: bigint;
  formatted: string;
}

function uniquePaths(paths: string[]): string[] {
  return Array.from(new Set(paths));
}

export function getDefaultWalletPath(): string {
  return process.env.DEGOV_AGENT_WALLET_PATH || DEFAULT_WALLET_PATH;
}

function getWalletSearchPaths(): string[] {
  const override = process.env.DEGOV_AGENT_WALLET_PATH;
  if (override) {
    return [override];
  }

  return uniquePaths([DEFAULT_WALLET_PATH, ...LEGACY_WALLET_PATHS]);
}

function findExistingWalletPath(): string | null {
  for (const candidate of getWalletSearchPaths()) {
    if (fs.existsSync(candidate)) {
      return candidate;
    }
  }
  return null;
}

function ensureWalletDir(walletPath: string): void {
  fs.mkdirSync(path.dirname(walletPath), { recursive: true });
}

function writeSecretFile(secretPath: string, secret: string): void {
  fs.mkdirSync(path.dirname(secretPath), { recursive: true });
  fs.writeFileSync(secretPath, `${secret}\n`, {
    mode: WALLET_FILE_MODE,
  });
  normalizeWalletPermissions(secretPath);
}

function normalizeWalletPermissions(walletPath: string): void {
  if (!fs.existsSync(walletPath)) {
    return;
  }

  try {
    const stat = fs.statSync(walletPath);
    if ((stat.mode & 0o777) !== WALLET_FILE_MODE) {
      fs.chmodSync(walletPath, WALLET_FILE_MODE);
    }
  } catch {
    // Best effort only.
  }
}

async function promptPassphrase(promptLabel: string): Promise<string> {
  if (!process.stdin.isTTY || !process.stdout.isTTY) {
    throw new Error(
      'Wallet passphrase required. Initialize the wallet first, or set DEGOV_AGENT_WALLET_PASSPHRASE or DEGOV_AGENT_WALLET_PASSPHRASE_PATH for non-interactive use.'
    );
  }

  const rl = createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  try {
    const value = await rl.question(promptLabel);
    if (!value) {
      throw new Error('Wallet passphrase cannot be empty.');
    }
    return value;
  } finally {
    rl.close();
  }
}

function getPassphrasePath(): string {
  return process.env.DEGOV_AGENT_WALLET_PASSPHRASE_PATH || DEFAULT_PASSPHRASE_PATH;
}

function getStoredPassphrase(): string | null {
  const passphrasePath = getPassphrasePath();
  if (!fs.existsSync(passphrasePath)) {
    return null;
  }

  normalizeWalletPermissions(passphrasePath);
  const passphrase = fs.readFileSync(passphrasePath, 'utf8').trim();
  if (!passphrase) {
    throw new Error(`Wallet passphrase file is empty: ${passphrasePath}`);
  }

  return passphrase;
}

function generatePassphrase(): string {
  return crypto.randomBytes(32).toString('base64url');
}

function getOrCreateStoredPassphrase(): string {
  const existing = getStoredPassphrase();
  if (existing) {
    return existing;
  }

  const passphrase = generatePassphrase();
  writeSecretFile(getPassphrasePath(), passphrase);
  return passphrase;
}

async function resolvePassphrase(options: { confirm?: boolean } = {}): Promise<string> {
  const fromEnv = process.env.DEGOV_AGENT_WALLET_PASSPHRASE;
  if (fromEnv) {
    return fromEnv;
  }

  if (!options.confirm) {
    const stored = getStoredPassphrase();
    if (stored) {
      return stored;
    }
  }

  if (options.confirm) {
    return getOrCreateStoredPassphrase();
  }

  const passphrase = await promptPassphrase('Wallet passphrase: ');
  if (!options.confirm) {
    return passphrase;
  }

  const confirmation = await promptPassphrase('Confirm wallet passphrase: ');
  if (passphrase !== confirmation) {
    throw new Error('Wallet passphrase confirmation does not match.');
  }

  return passphrase;
}

function encryptPrivateKey(privateKey: `0x${string}`, passphrase: string): EncryptedWalletPayload {
  const salt = crypto.randomBytes(16);
  const iv = crypto.randomBytes(12);
  const key = crypto.scryptSync(passphrase, salt, 32);
  const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);
  const ciphertext = Buffer.concat([cipher.update(privateKey, 'utf8'), cipher.final()]);
  const authTag = cipher.getAuthTag();

  return {
    algorithm: 'aes-256-gcm',
    kdf: 'scrypt',
    salt: salt.toString('base64'),
    iv: iv.toString('base64'),
    authTag: authTag.toString('base64'),
    ciphertext: ciphertext.toString('base64'),
  };
}

function decryptPrivateKey(cryptoPayload: EncryptedWalletPayload, passphrase: string): `0x${string}` {
  const key = crypto.scryptSync(passphrase, Buffer.from(cryptoPayload.salt, 'base64'), 32);
  const decipher = crypto.createDecipheriv(
    cryptoPayload.algorithm,
    key,
    Buffer.from(cryptoPayload.iv, 'base64')
  ) as crypto.DecipherGCM;
  decipher.setAuthTag(Buffer.from(cryptoPayload.authTag, 'base64'));
  const plaintext = Buffer.concat([
    decipher.update(Buffer.from(cryptoPayload.ciphertext, 'base64')),
    decipher.final(),
  ]).toString('utf8');

  return plaintext as `0x${string}`;
}

function writeWalletFile(walletPath: string, payload: WalletFile): void {
  ensureWalletDir(walletPath);
  fs.writeFileSync(walletPath, `${JSON.stringify(payload, null, 2)}\n`, {
    mode: WALLET_FILE_MODE,
  });
  normalizeWalletPermissions(walletPath);
}

function readWalletFile(walletPath: string): WalletFile | null {
  if (!fs.existsSync(walletPath)) {
    return null;
  }

  normalizeWalletPermissions(walletPath);
  return JSON.parse(fs.readFileSync(walletPath, 'utf8')) as WalletFile;
}

export function getResolvedWalletPath(): string {
  return findExistingWalletPath() ?? getDefaultWalletPath();
}

export async function getAccount(): Promise<WalletAccount> {
  const walletPath = getResolvedWalletPath();
  const wallet = readWalletFile(walletPath);
  if (!wallet) {
    throw new Error('Wallet not initialized. Run: pnpm exec tsx degov-client.ts wallet init');
  }

  let privateKey: `0x${string}`;
  if (wallet.crypto) {
    const passphrase = await resolvePassphrase();
    privateKey = decryptPrivateKey(wallet.crypto, passphrase);
  } else if (wallet.privateKey) {
    privateKey = wallet.privateKey;
  } else {
    throw new Error('Wallet file is missing secret material.');
  }

  return {
    walletPath,
    wallet,
    account: privateKeyToAccount(privateKey),
  };
}

export async function initWallet(): Promise<{
  walletPath: string;
  created: boolean;
  address: `0x${string}`;
  encrypted: boolean;
}> {
  const existingPath = findExistingWalletPath();
  if (existingPath) {
    const existing = readWalletFile(existingPath);
    if (existing?.address && (existing.privateKey || existing.crypto)) {
      return {
        walletPath: existingPath,
        created: false,
        address: existing.address,
        encrypted: Boolean(existing.crypto),
      };
    }
  }

  const passphrase = await resolvePassphrase({ confirm: true });
  const privateKey = generatePrivateKey();
  const account = privateKeyToAccount(privateKey);
  const walletPath = getDefaultWalletPath();
  writeWalletFile(walletPath, {
    createdAt: new Date().toISOString(),
    address: account.address,
    crypto: encryptPrivateKey(privateKey, passphrase),
  });

  return {
    walletPath,
    created: true,
    address: account.address,
    encrypted: true,
  };
}

export async function migrateWallet(): Promise<{
  sourceWalletPath: string;
  walletPath: string;
  migrated: boolean;
  moved: boolean;
  address: `0x${string}`;
  encrypted: boolean;
}> {
  const sourceWalletPath = findExistingWalletPath();
  if (!sourceWalletPath) {
    throw new Error('Wallet not initialized. Run: pnpm exec tsx degov-client.ts wallet init');
  }

  const sourceWallet = readWalletFile(sourceWalletPath);
  if (!sourceWallet?.address) {
    throw new Error('Wallet file is incomplete.');
  }

  const targetWalletPath = getDefaultWalletPath();
  const moved = sourceWalletPath !== targetWalletPath;

  if (sourceWallet.crypto && sourceWalletPath === targetWalletPath) {
    return {
      sourceWalletPath,
      walletPath: targetWalletPath,
      migrated: false,
      moved: false,
      address: sourceWallet.address,
      encrypted: true,
    };
  }

  let cryptoPayload = sourceWallet.crypto;
  if (!cryptoPayload) {
    if (!sourceWallet.privateKey) {
      throw new Error('Wallet file is missing secret material.');
    }
    const passphrase = await resolvePassphrase({ confirm: true });
    cryptoPayload = encryptPrivateKey(sourceWallet.privateKey, passphrase);
  }

  writeWalletFile(targetWalletPath, {
    createdAt: sourceWallet.createdAt || new Date().toISOString(),
    migratedAt: new Date().toISOString(),
    address: sourceWallet.address,
    crypto: cryptoPayload,
  });

  if (moved && fs.existsSync(sourceWalletPath)) {
    fs.rmSync(sourceWalletPath, { force: true });
  }

  return {
    sourceWalletPath,
    walletPath: targetWalletPath,
    migrated: true,
    moved,
    address: sourceWallet.address,
    encrypted: true,
  };
}

export async function getUsdcBalance(address: `0x${string}`): Promise<WalletBalance> {
  const publicClient = createPublicClient({
    chain: base,
    transport: http('https://mainnet.base.org'),
  });

  const balance = await publicClient.readContract({
    address: USDC_ADDRESS,
    abi: USDC_ABI,
    functionName: 'balanceOf',
    args: [address],
  });

  return {
    raw: balance,
    formatted: formatUnits(balance, 6),
  };
}
