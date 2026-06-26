/**
 * license-client.mjs
 * License validation client for Claude Anywhere.
 * Generates a machine_id from hostname+username (sha256, first 16 hex chars).
 */

import { createHash } from "crypto";
import { hostname, userInfo } from "os";

const CACHE_TTL_MS = 5 * 60 * 1000; // 5 minutes

let _cachedTier = null;
let _cacheTime = 0;

/**
 * Generate a stable machine ID from hostname + username (sha256 prefix).
 */
export function getMachineId() {
  const raw = `${hostname()}:${userInfo().username}`;
  return createHash("sha256").update(raw).digest("hex").slice(0, 16);
}

/**
 * Get current license tier ("free" | "pro").
 * If LICENSE_KEY is set, calls license server to validate.
 * Returns "free" when no key or server unreachable (with local fallback).
 * Results are cached for 5 minutes.
 *
 * Returns full info object:
 *   { tier, daily_count?, daily_limit?, trial_days_remaining? }
 */
export async function getLicenseTier() {
  const now = Date.now();
  if (_cachedTier && now - _cacheTime < CACHE_TTL_MS) {
    return _cachedTier;
  }

  const serverUrl = process.env.LICENSE_SERVER_URL?.trim() || "https://license.claudeanywhere.com";
  const machineId = getMachineId();
  const key = process.env.LICENSE_KEY?.trim();

  // 1) Key-based verification (existing users with LICENSE_KEY in .env)
  if (key) {
    try {
      const res = await fetch(`${serverUrl}/api/license/verify`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ license_key: key, machine_id: machineId }),
        signal: AbortSignal.timeout(5000),
      });
      if (res.ok) {
        const data = await res.json();
        const tier = data.valid ? (data.tier || "pro") : "free";
        _cachedTier = tier;
        _cacheTime = now;
        return tier;
      }
    } catch { /* fall through */ }
  }

  // 2) Machine-id-only verification (WeChat Pay / Gumroad auto-activated, no key needed)
  try {
    const res = await fetch(
      `${serverUrl}/api/license/verify_machine?mid=${encodeURIComponent(machineId)}`,
      { signal: AbortSignal.timeout(5000) }
    );
    if (res.ok) {
      const data = await res.json();
      if (data.valid) {
        _cachedTier = data.tier || "pro";
        _cacheTime = now;
        return _cachedTier;
      }
    }
  } catch { /* fall through */ }

  // Default to free
  if (_cachedTier) return _cachedTier;
  _cachedTier = "free";
  _cacheTime = now;
  return "free";
}

/**
 * Convenience method: returns true if current license is Pro.
 */
export async function isPro() {
  const tier = await getLicenseTier();
  return tier === "pro";
}

/**
 * Activate a license key against the server.
 * Returns { success: boolean, message: string }.
 */
export async function activateLicense(key) {
  const serverUrl = process.env.LICENSE_SERVER_URL?.trim() || "https://license.claudeanywhere.com";
  const machineId = getMachineId();

  try {
    const res = await fetch(`${serverUrl}/api/license/activate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ license_key: key, machine_id: machineId }),
      signal: AbortSignal.timeout(8000),
    });

    const data = await res.json();
    if (res.ok && data.success) {
      // Invalidate cache so next call re-validates
      _cachedTier = null;
      _cacheTime = 0;
      return { success: true, message: data.message || "License activated successfully." };
    }
    return { success: false, message: data.message || "Activation failed." };
  } catch (err) {
    return { success: false, message: `Cannot reach license server: ${err.message}` };
  }
}
