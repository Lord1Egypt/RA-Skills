/**
 * scripts/debug_license.ts — Step-by-step license check trace.
 * Run: npx tsx --env-file=.env scripts/debug_license.ts
 */

import { GUMROAD_PRODUCT_ID, GUMROAD_API_BASE, PRO_KEY } from "../src/config.js";

console.log("\n=== License Debug Trace ===\n");

// Step 1 — env vars as seen by Node
console.log("1. Env vars (raw):");
console.log(`   PRO_KEY             = ${JSON.stringify(process.env["CAREERCLAW_PRO_KEY"])}`);

// Step 2 — config constants after parsing
console.log("\n2. Config constants:");
console.log(`   PRO_KEY            = ${JSON.stringify(PRO_KEY)}`);
console.log(`   GUMROAD_PRODUCT_ID = ${JSON.stringify(GUMROAD_PRODUCT_ID)}`);
console.log(`   GUMROAD_API_BASE   = ${GUMROAD_API_BASE}`);

// Step 3 — gate conditions
console.log("\n3. Gate conditions:");
console.log(`   PRO_KEY truthy              = ${!!(PRO_KEY && PRO_KEY.trim().length > 0)}`);
console.log(`   GUMROAD_PRODUCT_ID truthy   = ${!!GUMROAD_PRODUCT_ID}`);

if (!PRO_KEY || PRO_KEY.trim().length === 0) {
  console.log("\n❌ STOP: PRO_KEY is empty or unset — gate will not open.");
  process.exit(1);
}

if (!GUMROAD_PRODUCT_ID) {
  console.log("\n❌ STOP: GUMROAD_PRODUCT_ID is empty or unset — checkLicense() returns {valid:false, source:'none'} immediately.");
  process.exit(1);
}

// Step 4 — raw Gumroad API call (bypasses checkLicense() wrapper)
console.log("\n4. Raw Gumroad API call:");
const body = new URLSearchParams({
  product_id: GUMROAD_PRODUCT_ID,
  license_key: PRO_KEY,
  increment_uses_count: "false",
});

console.log(`   POST ${GUMROAD_API_BASE}/v2/licenses/verify`);
console.log(`   product_id  = ${GUMROAD_PRODUCT_ID}`);
console.log(`   license_key = ${PRO_KEY.slice(0, 8)}...`);

try {
  const res = await fetch(`${GUMROAD_API_BASE}/v2/licenses/verify`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: body.toString(),
    signal: AbortSignal.timeout(15_000),
  });

  const raw = await res.text();
  console.log(`\n   HTTP status: ${res.status}`);
  console.log(`   Response body:\n${raw}`);

  if (res.ok) {
    const data = JSON.parse(raw) as {
      success: boolean;
      message?: string;
      purchase?: { refunded: boolean; chargebacked: boolean };
    };
    console.log("\n5. Parsed result:");
    console.log(`   success      = ${data.success}`);
    console.log(`   message      = ${data.message ?? "(none)"}`);
    console.log(`   refunded     = ${data.purchase?.refunded}`);
    console.log(`   chargebacked = ${data.purchase?.chargebacked}`);

    const valid =
      data.success &&
      !data.purchase?.refunded &&
      !data.purchase?.chargebacked;
    console.log(`\n   → checkLicense would return: { valid: ${valid}, source: "api" }`);
  }
} catch (err) {
  console.log(`\n   ❌ Fetch threw: ${String(err)}`);
  console.log("   → checkLicense will fall back to cache.");
}
