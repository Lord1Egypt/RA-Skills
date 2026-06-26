/**
 * Disk Cache + Fetch Timeout Utilities
 *
 * Persistent JSON-file cache for CLI processes where in-memory caches are useless.
 * Uses Node built-ins only (fs/promises, path, AbortController).
 */

import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { join } from 'node:path';

// ─── Fetch with timeout ─────────────────────────────────────────────────

/**
 * Wrapper around native fetch with AbortController timeout.
 * Defaults to 5 000 ms. Throws on timeout (AbortError).
 */
export async function fetchWithTimeout(
  url: string,
  options: RequestInit & { timeoutMs?: number } = {},
): Promise<Response> {
  const { timeoutMs = 5_000, ...fetchOpts } = options;

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);

  try {
    return await fetch(url, { ...fetchOpts, signal: controller.signal });
  } finally {
    clearTimeout(timer);
  }
}

// ─── Disk cache ─────────────────────────────────────────────────────────

interface CacheEntry<T> {
  value: T;
  expiresAt: number; // epoch ms
}

type CacheFile<T> = Record<string, CacheEntry<T>>;

const MAX_ENTRIES = 500;

function getCacheDir(): string {
  return process.env.BLOOM_CACHE_DIR || join(process.cwd(), '.bloom-cache');
}

function namespacePath(namespace: string): string {
  return join(getCacheDir(), `${namespace}.json`);
}

async function ensureCacheDir(): Promise<void> {
  await mkdir(getCacheDir(), { recursive: true });
}

async function readNamespace<T>(namespace: string): Promise<CacheFile<T>> {
  try {
    const raw = await readFile(namespacePath(namespace), 'utf-8');
    return JSON.parse(raw) as CacheFile<T>;
  } catch {
    // File doesn't exist or is corrupt — start fresh
    return {};
  }
}

async function writeNamespace<T>(namespace: string, data: CacheFile<T>): Promise<void> {
  await ensureCacheDir();
  await writeFile(namespacePath(namespace), JSON.stringify(data), 'utf-8');
}

/**
 * Read a value from the disk cache. Returns undefined on miss or expiry.
 */
export async function diskCacheGet<T>(namespace: string, key: string): Promise<T | undefined> {
  const data = await readNamespace<T>(namespace);
  const entry = data[key];
  if (!entry) return undefined;
  if (Date.now() > entry.expiresAt) return undefined;
  return entry.value;
}

/**
 * Write a value to the disk cache with a TTL in milliseconds.
 * Prunes expired entries and caps total entries at 500.
 */
export async function diskCacheSet<T>(
  namespace: string,
  key: string,
  value: T,
  ttlMs: number,
): Promise<void> {
  const data = await readNamespace<T>(namespace);
  const now = Date.now();

  // Prune expired entries
  for (const k of Object.keys(data)) {
    if (data[k].expiresAt <= now) {
      delete data[k];
    }
  }

  // Set new entry
  data[key] = { value, expiresAt: now + ttlMs };

  // Cap at MAX_ENTRIES — evict oldest first
  const keys = Object.keys(data);
  if (keys.length > MAX_ENTRIES) {
    const sorted = keys.sort((a, b) => data[a].expiresAt - data[b].expiresAt);
    const toRemove = sorted.slice(0, keys.length - MAX_ENTRIES);
    for (const k of toRemove) {
      delete data[k];
    }
  }

  await writeNamespace(namespace, data);
}
