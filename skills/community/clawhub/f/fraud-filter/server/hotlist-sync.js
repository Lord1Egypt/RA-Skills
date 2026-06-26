/**
 * Hotlist sync.
 *
 * Fetches api.fraud-filter.com/hotlist.json hourly and caches it to
 * data/hotlist.json. The hotlist contains endpoint hashes that have received
 * a surge of failure reports in the last 24 hours — providing faster blocking
 * than waiting for the nightly trust.json rebuild.
 *
 * trust-db.js reads the cached file directly; no import needed here.
 */

import { writeFileSync, existsSync, mkdirSync } from "node:fs";
import { resolve, dirname } from "node:path";

const HOTLIST_URL =
  process.env.FRAUD_FILTER_HOTLIST_URL ||
  "https://api.fraud-filter.com/hotlist.json";

const HOTLIST_CACHE_PATH = resolve(
  process.env.FRAUD_FILTER_HOTLIST ||
    new URL("../data/hotlist.json", import.meta.url).pathname
);

/**
 * Fetch the hotlist from the remote API and save to cache.
 * Safe to call in the background — never throws.
 */
export async function syncHotlist() {
  try {
    const res = await fetch(HOTLIST_URL, {
      headers: { "User-Agent": "fraud-filter-skill/1.0" },
      signal: AbortSignal.timeout(5_000),
    });
    if (!res.ok) {
      console.error(`[hotlist-sync] HTTP ${res.status} from ${HOTLIST_URL}`);
      return;
    }
    const data = await res.json();
    const dir = dirname(HOTLIST_CACHE_PATH);
    if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
    writeFileSync(HOTLIST_CACHE_PATH, JSON.stringify(data), { mode: 0o600 });
    console.log(
      `[hotlist-sync] cached ${data.blocked?.length ?? "?"} hotlisted endpoints`
    );
  } catch (err) {
    console.error(`[hotlist-sync] fetch failed: ${err.message}`);
  }
}
