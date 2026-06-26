#!/usr/bin/env node

import fs from 'fs';
import os from 'os';
import path from 'path';
import crypto from 'crypto';

const CACHE_DIR = path.join(os.tmpdir(), 'baidu-yijian-vision-cache');

/**
 * Read a JSON cache file. Returns null if missing, expired, or invalid.
 * Deletes the file if TTL has expired (prevents disk leak).
 */
export function readCache(filePath, ttl) {
  if (!fs.existsSync(filePath)) return null;
  try {
    const data = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
    if (ttl && Date.now() - data.timestamp > ttl) {
      try { fs.unlinkSync(filePath); } catch {}
      return null;
    }
    return data;
  } catch {
    return null;
  }
}

/**
 * Write a JSON cache file. Ensures parent directory exists.
 */
export function writeCache(filePath, data) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf-8');
}

/**
 * Get the cache directory path.
 */
export function getCacheDir() {
  return CACHE_DIR;
}

/**
 * Generate a cache file path that includes a hash of the API key,
 * so different users/keys get isolated cache files.
 *
 * @param {string} basePath - Original cache file path (e.g. ".../workspace-cache.json")
 * @param {string} apiKey - API key to hash into the filename
 * @returns {string} Path with key hash suffix (e.g. ".../workspace-cache-a1b2c3.json")
 */
export function keyHashedPath(basePath, apiKey) {
  const hash = crypto.createHash('sha256').update(apiKey).digest('hex').slice(0, 8);
  const ext = path.extname(basePath);
  const base = path.basename(basePath, ext);
  const dir = path.dirname(basePath);
  return path.join(dir, `${base}-${hash}${ext}`);
}

/**
 * Delete a cache file if it exists. Silently ignores missing files.
 */
export function clearCache(filePath) {
  try {
    if (fs.existsSync(filePath)) fs.unlinkSync(filePath);
  } catch {
    // ignore
  }
}
