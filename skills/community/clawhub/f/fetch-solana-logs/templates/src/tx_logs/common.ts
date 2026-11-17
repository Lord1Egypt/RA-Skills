import fs from 'fs';
import path from 'path';
import { Connection, PublicKey } from '@solana/web3.js';
import { BorshCoder, Idl, Program } from '@coral-xyz/anchor';
import { isSolanaAddress } from '../utils/utils';

export const outputBaseDir = './output';
/** Project-root list of Solana addresses to pull, e.g. `["Addr1", "Addr2"]` */
export const targetsConfigPath = './target_solana_addr.json';

export type AccountType = 'program' | 'account' | 'auto';

export interface TargetAccount {
  address: string;
  /** program = decode ix with IDL; account = wallet/PDA history only; auto = detect on-chain */
  type?: AccountType;
}

export function getHeliusApiKey(): string {
  const key = process.env.HELIUS_API_KEY;
  if (!key) {
    throw new Error('Missing HELIUS_API_KEY in env (.env)');
  }
  return key;
}

export function getHeliusRpcUrl(): string {
  if (process.env.SOLANA_RPC_URL) {
    return process.env.SOLANA_RPC_URL;
  }
  const key = process.env.HELIUS_API_KEY;
  if (key) {
    return `https://mainnet.helius-rpc.com/?api-key=${key}`;
  }
  return 'https://api.mainnet-beta.solana.com';
}

export function getConnection(): Connection {
  return new Connection(getHeliusRpcUrl(), 'confirmed');
}

/** Per-address output folder: `output/<addr>/` */
export function outputDirFor(address: string): string {
  return path.join(outputBaseDir, address);
}

/** IDL file: `output/<addr>/idl_<addr>.json` */
export function idlOutputPath(address: string): string {
  return path.join(outputDirFor(address), `idl_${address}.json`);
}

export function txLogsPath(address: string): string {
  return path.join(outputDirFor(address), `tx_logs_${address}.txt`);
}

export function txParsedPath(address: string): string {
  return path.join(outputDirFor(address), `tx_logs_parsed_${address}.json`);
}

export function ensureOutputDir(address: string): string {
  const dir = outputDirFor(address);
  fs.mkdirSync(dir, { recursive: true });
  return dir;
}

export interface CliOptions {
  /** Explicit addresses from CLI / env; empty → fall back to target_solana_addr.json */
  addresses: string[];
  limit: number | null;
  recent: boolean;
}

/**
 * Parse shared CLI flags.
 *
 * Examples:
 *   pnpm s1 -- --addr <ADDR> --limit 50 --recent
 *   pnpm s1 -- <ADDR> --limit 50
 *   pnpm s2 -- -a <ADDR1> -a <ADDR2>
 *   ADDR=<ADDR> pnpm s1 -- --limit 50
 */
export function parseCliArgs(argv: string[] = process.argv.slice(2)): CliOptions {
  const addresses: string[] = [];
  let limit: number | null = null;
  let recent = false;

  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];

    if (a === '--') {
      continue;
    }

    if (a === '--addr' || a === '-a') {
      const v = argv[++i];
      if (!v || v.startsWith('-')) {
        throw new Error(`${a} requires a Solana address`);
      }
      addresses.push(v);
      continue;
    }
    if (a.startsWith('--addr=')) {
      addresses.push(a.slice('--addr='.length));
      continue;
    }

    if (a === '--limit') {
      const v = argv[++i];
      const n = Number(v);
      if (!Number.isFinite(n) || n <= 0) {
        throw new Error(`invalid --limit ${v}`);
      }
      limit = n;
      continue;
    }
    if (a.startsWith('--limit=')) {
      const n = Number(a.slice('--limit='.length));
      if (!Number.isFinite(n) || n <= 0) {
        throw new Error(`invalid ${a}`);
      }
      limit = n;
      continue;
    }

    if (a === '--recent') {
      recent = true;
      continue;
    }

    if (a.startsWith('-')) {
      throw new Error(`Unknown flag: ${a}`);
    }

    // positional address
    addresses.push(a);
  }

  if (!addresses.length && process.env.ADDR) {
    for (const part of process.env.ADDR.split(/[,\s]+/)) {
      if (part) addresses.push(part);
    }
  }

  // --limit alone implies a recent window pull
  if (limit != null) {
    recent = true;
  }

  return { addresses, limit, recent };
}

/** Resolve targets: CLI/env addresses win; otherwise read target_solana_addr.json. */
export function resolveTargets(cliArgs?: string[]): TargetAccount[] {
  const opts = cliArgs ? parseCliArgs(cliArgs) : parseCliArgs();
  return resolveTargetsFromOptions(opts);
}

export function resolveTargetsFromOptions(opts: CliOptions): TargetAccount[] {
  if (opts.addresses.length) {
    return validateAddresses(opts.addresses);
  }

  if (!fs.existsSync(targetsConfigPath)) {
    throw new Error(
      `No targets. Pass --addr <ADDR> (or positional addr), set ADDR=, or create ${targetsConfigPath}`,
    );
  }

  const raw = JSON.parse(fs.readFileSync(targetsConfigPath, 'utf8'));
  const addresses: string[] = Array.isArray(raw)
    ? raw.map((item) =>
        typeof item === 'string' ? item : (item as TargetAccount)?.address,
      )
    : typeof raw === 'string'
      ? [raw]
      : raw?.address
        ? [raw.address]
        : [];

  if (!addresses.length) {
    throw new Error(
      `No addresses found in ${targetsConfigPath}. Expected e.g. ["Addr1", "Addr2"]`,
    );
  }

  return validateAddresses(addresses);
}

function validateAddresses(addresses: string[]): TargetAccount[] {
  const out: TargetAccount[] = [];
  for (const raw of addresses) {
    const address = (raw || '').trim();
    if (!address) {
      throw new Error(`Empty address in ${targetsConfigPath}`);
    }
    if (!isSolanaAddress(address)) {
      throw new Error(
        `Invalid Solana address (isSolanaAddress failed): ${address}`,
      );
    }
    out.push({ address, type: 'auto' });
  }
  return out;
}

/** Detect whether an address is an executable program on-chain. */
export async function resolveAccountType(
  target: TargetAccount,
  connection = getConnection(),
): Promise<'program' | 'account'> {
  if (target.type === 'program' || target.type === 'account') {
    return target.type;
  }

  const info = await connection.getAccountInfo(new PublicKey(target.address));
  if (info?.executable) {
    return 'program';
  }
  return 'account';
}

export function loadIdlFromOutput(programAddress: string): Idl | null {
  const fpath = idlOutputPath(programAddress);
  if (!fs.existsSync(fpath)) return null;
  return JSON.parse(fs.readFileSync(fpath, 'utf8')) as Idl;
}

export function saveIdlToOutput(programAddress: string, idl: Idl): string {
  ensureOutputDir(programAddress);
  const fpath = idlOutputPath(programAddress);
  fs.writeFileSync(fpath, JSON.stringify(idl, null, 2));
  return fpath;
}

/**
 * If the address has an on-chain (or already saved) Anchor IDL, ensure it is
 * written to `output/<addr>/idl_<addr>.json`. Returns the IDL or null.
 */
export async function ensureIdlSaved(
  programAddress: string,
  connection = getConnection(),
): Promise<Idl | null> {
  const existing = loadIdlFromOutput(programAddress);
  if (existing) {
    console.log(`[idl] already at ${idlOutputPath(programAddress)}`);
    return existing;
  }

  console.log(`[idl] fetching on-chain IDL for ${programAddress}…`);
  try {
    const idl = await Program.fetchIdl(programAddress, { connection });
    if (idl) {
      const fpath = saveIdlToOutput(programAddress, idl);
      console.log(`[idl] saved → ${fpath}`);
      return idl;
    }
    console.log(`[idl] no on-chain IDL for ${programAddress}`);
  } catch (err) {
    console.warn(`[idl] on-chain fetch failed:`, (err as Error).message);
  }

  return null;
}

/** Load IDL from output dir, or fetch + save if missing. */
export async function loadOrFetchIdl(
  programAddress: string,
  connection = getConnection(),
): Promise<Idl | null> {
  return ensureIdlSaved(programAddress, connection);
}

export function makeInstructionCoder(idl: Idl): BorshCoder {
  return new BorshCoder(idl);
}

/** JSON-safe serialization for Anchor decode results (BN, Buffer, nested). */
export function serializeDecoded(value: unknown): unknown {
  if (value == null) return value;
  if (typeof value === 'bigint') return value.toString();
  if (typeof value === 'number' || typeof value === 'boolean' || typeof value === 'string') {
    return value;
  }
  if (Buffer.isBuffer(value) || value instanceof Uint8Array) {
    return Buffer.from(value).toString('hex');
  }
  if (Array.isArray(value)) {
    return value.map(serializeDecoded);
  }
  if (typeof value === 'object') {
    const maybeBn = value as { toString?: (radix?: number) => string; _bn?: unknown };
    if (
      maybeBn._bn != null ||
      (typeof maybeBn.toString === 'function' &&
        (value as object).constructor?.name === 'BN')
    ) {
      return maybeBn.toString!(10);
    }
    if (typeof (value as { toBase58?: () => string }).toBase58 === 'function') {
      return (value as { toBase58: () => string }).toBase58();
    }
    const out: Record<string, unknown> = {};
    for (const [k, v] of Object.entries(value as Record<string, unknown>)) {
      out[k] = serializeDecoded(v);
    }
    return out;
  }
  return String(value);
}
