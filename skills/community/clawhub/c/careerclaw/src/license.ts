/**
 * license.ts — Gumroad Pro license validation with offline cache.
 *
 * `checkLicense(key, options?)` validates a CareerClaw Pro license key
 * against the Gumroad API and caches the result for 7 days so the tool
 * works normally during short network outages.
 *
 * Design principles:
 *   - Raw key NEVER written to disk — only sha256(key) is cached.
 *   - Graceful degradation: if Gumroad is unreachable and the cache is
 *     fresh (< LICENSE_CACHE_TTL_MS), the cached result is trusted.
 *   - Free tier safe: if GUMROAD_PRODUCT_ID is not configured, returns
 *     { valid: false, source: "none" } immediately without erroring.
 *   - Testable: fetchFn and cachePath are injectable for offline tests.
 */

import { createHash } from "node:crypto";
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { dirname } from "node:path";
import {
  GUMROAD_API_BASE,
  GUMROAD_PRODUCT_ID,
  LICENSE_CACHE_PATH,
  LICENSE_CACHE_TTL_MS,
  HTTP_TIMEOUT_MS,
} from "./config.js";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export interface LicenseResult {
  valid: boolean;
  /** Where the result came from. */
  source: "api" | "cache" | "none";
}

export interface CheckLicenseOptions {
  /** Injectable fetch — defaults to global fetch. */
  fetchFn?: typeof fetch;
  /** Override cache file path — for tests using a tmpdir. */
  cachePath?: string;
}

interface LicenseCache {
  /** SHA-256 hex digest of the license key. */
  key_hash: string;
  /** ISO-8601 UTC timestamp when the API last confirmed validity. */
  validated_at: string;
}

// ---------------------------------------------------------------------------
// Public API
// ---------------------------------------------------------------------------

/**
 * Validate a CareerClaw Pro license key.
 *
 * Resolution order:
 *   1. If GUMROAD_PRODUCT_ID is unset → { valid: false, source: "none" }
 *   2. POST to Gumroad API (increment_uses_count=false)
 *      - success + not refunded + not chargebacked → cache hash, return api
 *      - refunded / chargebacked / not found → { valid: false, source: "api" }
 *   3. On network failure → read cache
 *      - hash matches + age < TTL → { valid: true, source: "cache" }
 *      - stale, missing, or hash mismatch → { valid: false, source: "none" }
 */
export async function checkLicense(
  key: string,
  options: CheckLicenseOptions = {}
): Promise<LicenseResult> {
  const fetchFn = options.fetchFn ?? fetch;
  const cachePath = options.cachePath ?? LICENSE_CACHE_PATH;

  // Guard: product ID must be configured
  if (!GUMROAD_PRODUCT_ID) {
    return { valid: false, source: "none" };
  }

  // Attempt live API validation
  try {
    const result = await verifyWithApi(key, GUMROAD_PRODUCT_ID, fetchFn);
    if (result.valid) {
      writeCache(key, cachePath);
    }
    return result;
  } catch {
    // Network failure — fall back to cache
    return readCache(key, cachePath);
  }
}

// ---------------------------------------------------------------------------
// Gumroad API call
// ---------------------------------------------------------------------------

interface GumroadResponse {
  success: boolean;
  message?: string;
  purchase?: {
    refunded: boolean;
    chargebacked: boolean;
  };
}

async function verifyWithApi(
  key: string,
  productId: string,
  fetchFn: typeof fetch
): Promise<LicenseResult> {
  const body = new URLSearchParams({
    product_id: productId,
    license_key: key,
    increment_uses_count: "false",
  });

  const res = await fetchFn(`${GUMROAD_API_BASE}/v2/licenses/verify`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: body.toString(),
    signal: AbortSignal.timeout(HTTP_TIMEOUT_MS),
  });

  // Gumroad returns 404 for invalid/unknown keys
  if (res.status === 404) {
    return { valid: false, source: "api" };
  }

  if (!res.ok) {
    // Non-404 HTTP errors (5xx, etc.) are treated as network failures
    throw new Error(`Gumroad HTTP ${res.status}`);
  }

  const data = (await res.json()) as GumroadResponse;

  if (!data.success) {
    return { valid: false, source: "api" };
  }

  if (data.purchase?.refunded || data.purchase?.chargebacked) {
    return { valid: false, source: "api" };
  }

  return { valid: true, source: "api" };
}

// ---------------------------------------------------------------------------
// Cache helpers
// ---------------------------------------------------------------------------

function hashKey(key: string): string {
  return createHash("sha256").update(key).digest("hex");
}

function writeCache(key: string, cachePath: string): void {
  try {
    mkdirSync(dirname(cachePath), { recursive: true });
    const cache: LicenseCache = {
      key_hash: hashKey(key),
      validated_at: new Date().toISOString(),
    };
    writeFileSync(cachePath, JSON.stringify(cache, null, 2), "utf8");
  } catch {
    // Cache write failure is non-fatal — validation already succeeded
  }
}

function readCache(key: string, cachePath: string): LicenseResult {
  try {
    const raw = readFileSync(cachePath, "utf8");
    const cache = JSON.parse(raw) as LicenseCache;

    // Hash must match the key being checked
    if (cache.key_hash !== hashKey(key)) {
      return { valid: false, source: "none" };
    }

    // Cache must be within the TTL window
    const age = Date.now() - new Date(cache.validated_at).getTime();
    if (age > LICENSE_CACHE_TTL_MS) {
      return { valid: false, source: "none" };
    }

    return { valid: true, source: "cache" };
  } catch {
    return { valid: false, source: "none" };
  }
}
