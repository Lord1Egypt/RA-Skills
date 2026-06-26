#!/usr/bin/env node
// Brave API shared utilities

/**
 * Parse CLI args from process.argv
 * Supports: --key value, --flag (true), --key=value
 */
function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i++) {
    if (argv[i].startsWith('--')) {
      const arg = argv[i].slice(2);
      if (arg.includes('=')) {
        const [key, val] = arg.split('=', 2);
        args[key] = val;
      } else {
        const val = argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[++i] : 'true';
        args[arg] = val;
      }
    }
  }
  return args;
}

/**
 * Fetch with retry logic.
 * Retries on 429 (Retry-After delay) and 5xx errors.
 * @param {string} url
 * @param {object} options
 * @param {number} [maxRetries=3]
 */
async function fetchWithRetry(url, options, maxRetries = 3) {
  let lastError;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      const res = await fetch(url, options);

      if (res.status === 429) {
        const retryAfter = parseInt(res.headers.get('Retry-After') || '5', 10);
        const delay = retryAfter * 1000;
        if (attempt < maxRetries) {
          await sleep(delay);
          continue;
        }
      }

      if (res.status >= 500 && attempt < maxRetries) {
        await sleep(500 * Math.pow(2, attempt));
        continue;
      }

      return res;
    } catch (err) {
      lastError = err;
      if (attempt < maxRetries) {
        await sleep(500 * Math.pow(2, attempt));
      }
    }
  }

  throw lastError;
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Simple in-memory cache with TTL.
 * Use as: cache.get(key) or cache.set(key, value, ttlMs)
 */
function createCache() {
  const store = new Map();
  return {
    get(key) {
      const entry = store.get(key);
      if (!entry) return null;
      if (Date.now() > entry.expires) {
        store.delete(key);
        return null;
      }
      return entry.value;
    },
    set(key, value, ttlMs = 60_000) {
      store.set(key, { value, expires: Date.now() + ttlMs });
    },
    clear() {
      store.clear();
    },
  };
}

module.exports = { parseArgs, fetchWithRetry, createCache, sleep };
