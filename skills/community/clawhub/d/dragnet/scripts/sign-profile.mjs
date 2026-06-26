#!/usr/bin/env node
/**
 * Dragnet Profile Signer
 *
 * Signs a dragnet-profile.json using HMAC-SHA-256.
 * The canonical form is JSON.stringify with sorted keys, excluding _sig.
 *
 * Usage:
 *   node sign-profile.mjs <input.json> [output.json]
 *
 * If output is omitted, writes to dragnet-profile.json in cwd.
 */

import { createHmac } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";

const KEY = "dn-validation-key-alpha-2025";

function canonical(obj) {
  const clone = { ...obj };
  delete clone._sig;
  return JSON.stringify(clone, Object.keys(clone).sort());
}

function sign(obj) {
  const data = canonical(obj);
  const sig = createHmac("sha256", KEY).update(data).digest("hex");
  return { ...obj, _sig: sig };
}

function verify(obj) {
  if (!obj._sig) return false;
  const data = canonical(obj);
  const expected = createHmac("sha256", KEY).update(data).digest("hex");
  return expected === obj._sig;
}

// --- CLI ---
const [, , inputPath, outputPath] = process.argv;

if (!inputPath) {
  console.error("Usage: node sign-profile.mjs <input.json> [output.json]");
  process.exit(1);
}

const raw = readFileSync(resolve(inputPath), "utf-8");
const profile = JSON.parse(raw);

// Strip any existing signature before re-signing
delete profile._sig;

const signed = sign(profile);

// Verify round-trip
if (!verify(signed)) {
  console.error("FATAL: round-trip verification failed");
  process.exit(2);
}

const out = outputPath
  ? resolve(outputPath)
  : resolve(process.cwd(), "dragnet-profile.json");

writeFileSync(out, JSON.stringify(signed, null, 2) + "\n");
console.log(`✓ Signed profile written to ${out}`);
console.log(`  Signature: ${signed._sig.slice(0, 16)}…`);
