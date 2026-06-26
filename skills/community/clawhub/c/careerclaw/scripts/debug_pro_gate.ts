/**
 * scripts/debug_pro_gate.ts — Traces every condition that controls isProActive.
 * Run: npx tsx --env-file=.env scripts/debug_pro_gate.ts
 */

import { existsSync, readFileSync } from "node:fs";
import { PRO_KEY, GUMROAD_PRODUCT_ID, RESUME_TXT_PATH, PROFILE_PATH } from "../src/config.js";
import { buildResumeIntelligence } from "../src/resume-intel.js";
import { checkLicense } from "../src/license.js";

console.log("\n=== Pro Gate Debug Trace ===\n");

// 1. PRO_KEY
console.log("1. PRO_KEY");
console.log(`   value   = ${JSON.stringify(PRO_KEY)}`);
console.log(`   truthy  = ${!!(PRO_KEY && PRO_KEY.trim().length > 0)}`);

// 2. GUMROAD_PRODUCT_ID
console.log("\n2. GUMROAD_PRODUCT_ID");
console.log(`   value   = ${JSON.stringify(GUMROAD_PRODUCT_ID)}`);
console.log(`   truthy  = ${!!GUMROAD_PRODUCT_ID}`);

// 3. Resume file
console.log("\n3. Resume file");
console.log(`   default path = ${RESUME_TXT_PATH}`);
console.log(`   exists       = ${existsSync(RESUME_TXT_PATH)}`);

const resumeText = existsSync(RESUME_TXT_PATH)
  ? readFileSync(RESUME_TXT_PATH, "utf8")
  : null;
console.log(`   text length  = ${resumeText?.length ?? 0} chars`);

// 4. Profile
console.log("\n4. Profile");
console.log(`   path   = ${PROFILE_PATH}`);
console.log(`   exists = ${existsSync(PROFILE_PATH)}`);

const profile = existsSync(PROFILE_PATH)
  ? JSON.parse(readFileSync(PROFILE_PATH, "utf8"))
  : null;
console.log(`   skills         = ${JSON.stringify(profile?.skills?.slice(0, 5))}`);
console.log(`   resume_summary = ${JSON.stringify(profile?.resume_summary?.slice(0, 60))}`);

// 5. resumeIntel
console.log("\n5. buildResumeIntelligence");
let resumeIntel = null;
try {
  resumeIntel = buildResumeIntelligence({
    resume_summary: profile?.resume_summary ?? "",
    skills: profile?.skills ?? [],
    target_roles: profile?.target_roles ?? [],
    ...(resumeText ? { resume_text: resumeText } : {}),
  });
  console.log(`   impact_signals count = ${resumeIntel.impact_signals.length}`);
  console.log(`   impact_signals (top5) = ${JSON.stringify(resumeIntel.impact_signals.slice(0, 5))}`);
  console.log(`   resumeIntel truthy    = true`);
} catch (err) {
  console.log(`   ❌ threw: ${String(err)}`);
}

// 6. Gate pre-check
console.log("\n6. Gate pre-check (proKey && resumeIntel)");
const gateOpen = !!(PRO_KEY && PRO_KEY.trim().length > 0 && resumeIntel);
console.log(`   gateOpen = ${gateOpen}`);

if (!gateOpen) {
  console.log("\n❌ STOP: gate is closed — isProActive will be false without calling checkLicense.");
  process.exit(1);
}

// 7. Live checkLicense
console.log("\n7. checkLicense (live Gumroad call)");
try {
  const result = await checkLicense(PRO_KEY!);
  console.log(`   valid  = ${result.valid}`);
  console.log(`   source = ${result.source}`);
  if (result.valid) {
    console.log("\n✅ isProActive = true — LLM enhancement should activate.");
  } else {
    console.log("\n❌ License invalid — isProActive = false.");
  }
} catch (err) {
  console.log(`   ❌ threw unexpectedly: ${String(err)}`);
}
