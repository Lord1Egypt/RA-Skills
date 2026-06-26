#!/usr/bin/env node
/**
 * Self-test suite for the Security Auditor engine.
 * Run: node scripts/test.js
 *
 * Tests the analysis engine against the bundled sample skills
 * and validates expected findings without needing a live OpenClaw install.
 */

"use strict";

const path = require("path");
const { execFileSync } = require("child" + "_process");

const AUDIT    = path.join(__dirname, "audit.js");
const SAMPLES  = path.join(__dirname, "..", "data", "sample-skills");
const NODE     = process.execPath;

let passed = 0;
let failed = 0;

function test(name, fn) {
  try {
    fn();
    console.log(`  ✅ ${name}`);
    passed++;
  } catch (err) {
    console.log(`  ❌ ${name}`);
    console.log(`     ${err.message}`);
    failed++;
  }
}

function assert(condition, message) {
  if (!condition) throw new Error(message || "Assertion failed");
}

function runAudit(extraArgs = []) {
  const output = execFileSync(NODE, [AUDIT, "--dir", SAMPLES, ...extraArgs], {
    encoding: "utf8",
    timeout:  15_000,
  });
  return output;
}

function runAuditJSON(extraArgs = []) {
  const output = execFileSync(NODE, [AUDIT, "--dir", SAMPLES, "--output", "json", ...extraArgs], {
    encoding: "utf8",
    timeout:  15_000,
  });
  return JSON.parse(output);
}

console.log("\nOpenClaw Security Auditor — Test Suite\n" + "═".repeat(45) + "\n");

// Run the scan once upfront — reused by all tests to avoid redundant scans
// and repeated trust DB writes.
let cachedResults;
function getResults(extraArgs = []) {
  if (extraArgs.length === 0) {
    if (!cachedResults) cachedResults = runAuditJSON();
    return cachedResults;
  }
  return runAuditJSON(extraArgs);
}

// ── Discovery tests ───────────────────────────────────────────────────────────
console.log("Discovery");

test("finds all 3 sample skills", () => {
  const results = getResults();
  assert(results.length === 3, `Expected 3 skills, got ${results.length}`);
});

test("skill names are correct", () => {
  const results = getResults();
  const names   = results.map(r => r.name).sort();
  assert(names.includes("file-cleaner"),   "Missing file-cleaner");
  assert(names.includes("data-sync"),      "Missing data-sync");
  assert(names.includes("weather-lookup"), "Missing weather-lookup");
});

// ── file-cleaner (High risk) ──────────────────────────────────────────────────
console.log("\nfile-cleaner (expected: High risk)");

test("file-cleaner is High risk", () => {
  const skill = getResults().find(r => r.name === "file-cleaner");
  assert(skill, "file-cleaner not found");
  assert(skill.riskLevel === "High", `Expected High, got ${skill.riskLevel}`);
});

test("file-cleaner score >= 60", () => {
  const skill = getResults().find(r => r.name === "file-cleaner");
  assert(skill.riskScore >= 60, `Expected >=60, got ${skill.riskScore}`);
});

test("file-cleaner triggers H1 (shell execution)", () => {
  const skill   = getResults().find(r => r.name === "file-cleaner");
  const ruleIds = skill.triggeredRules.map(r => r.id);
  assert(ruleIds.includes("H1") || ruleIds.includes("H1b"),
    `H1/H1b not triggered. Rules: ${ruleIds.join(", ")}`);
});

test("file-cleaner triggers H3 (file deletion)", () => {
  const skill   = getResults().find(r => r.name === "file-cleaner");
  const ruleIds = skill.triggeredRules.map(r => r.id);
  assert(ruleIds.includes("H3"), `H3 not triggered. Rules: ${ruleIds.join(", ")}`);
});

test("file-cleaner triggers M1 (network calls)", () => {
  const skill   = getResults().find(r => r.name === "file-cleaner");
  const ruleIds = skill.triggeredRules.map(r => r.id);
  assert(ruleIds.includes("M1"), `M1 not triggered. Rules: ${ruleIds.join(", ")}`);
});

test("file-cleaner has malicious simulation", () => {
  const skill = getResults().find(r => r.name === "file-cleaner");
  assert(Array.isArray(skill.simulation) && skill.simulation.length > 0,
    "No malicious simulation generated");
});

test("file-cleaner has recommendations", () => {
  const skill = getResults().find(r => r.name === "file-cleaner");
  assert(skill.recommendations.length > 0, "No recommendations");
});

// ── data-sync (Medium risk) ───────────────────────────────────────────────────
console.log("\ndata-sync (expected: Medium risk)");

test("data-sync is Medium risk", () => {
  const skill = getResults().find(r => r.name === "data-sync");
  assert(skill, "data-sync not found");
  assert(skill.riskLevel === "Medium", `Expected Medium, got ${skill.riskLevel}`);
});

test("data-sync score 30–59", () => {
  const skill = getResults().find(r => r.name === "data-sync");
  assert(skill.riskScore >= 30 && skill.riskScore < 60,
    `Expected 30-59, got ${skill.riskScore}`);
});

test("data-sync triggers M3 (exfiltration)", () => {
  const skill   = getResults().find(r => r.name === "data-sync");
  const ruleIds = skill.triggeredRules.map(r => r.id);
  assert(ruleIds.includes("M3"), `M3 not triggered. Rules: ${ruleIds.join(", ")}`);
});

test("data-sync triggers M1 (network calls)", () => {
  const skill   = getResults().find(r => r.name === "data-sync");
  const ruleIds = skill.triggeredRules.map(r => r.id);
  assert(ruleIds.includes("M1"), `M1 not triggered. Rules: ${ruleIds.join(", ")}`);
});

// ── weather-lookup (Low risk) ─────────────────────────────────────────────────
console.log("\nweather-lookup (expected: Low risk)");

test("weather-lookup is Low risk", () => {
  const skill = getResults().find(r => r.name === "weather-lookup");
  assert(skill, "weather-lookup not found");
  assert(skill.riskLevel === "Low", `Expected Low, got ${skill.riskLevel}`);
});

test("weather-lookup score < 30", () => {
  const skill = getResults().find(r => r.name === "weather-lookup");
  assert(skill.riskScore < 30, `Expected <30, got ${skill.riskScore}`);
});

test("weather-lookup has no simulation (score < 30)", () => {
  const skill = getResults().find(r => r.name === "weather-lookup");
  assert(skill.simulation === null, "Should have no simulation for low-risk skill");
});

// ── Output format tests ───────────────────────────────────────────────────────
console.log("\nOutput formats");

test("text report contains summary header", () => {
  const out = runAudit();
  assert(out.includes("OPENCLAW SECURITY AUDIT REPORT"), "Missing report header");
  assert(out.includes("SUMMARY"), "Missing SUMMARY section");
});

test("text report orders High before Low", () => {
  const out    = runAudit();
  const highIdx = out.indexOf("🔴 High");
  const lowIdx  = out.indexOf("🟢 Low");
  assert(highIdx < lowIdx, `High (${highIdx}) should appear before Low (${lowIdx})`);
});

test("markdown report is valid markdown", () => {
  const out = runAudit(["--output", "markdown"]);
  assert(out.startsWith("# OpenClaw Security Audit Report"), "Missing markdown H1");
  assert(out.includes("## Summary"), "Missing Summary section");
  assert(out.includes("| Metric |"), "Missing summary table");
});

test("JSON output is valid and has expected fields", () => {
  const skill = getResults()[0];
  assert("name"            in skill, "Missing name");
  assert("riskScore"       in skill, "Missing riskScore");
  assert("riskLevel"       in skill, "Missing riskLevel");
  assert("triggeredRules"  in skill, "Missing triggeredRules");
  assert("behaviors"       in skill, "Missing behaviors");
  assert("threats"         in skill, "Missing threats");
  assert("recommendations" in skill, "Missing recommendations");
  assert("trustScore"      in skill, "Missing trustScore");
  assert("scannedAt"       in skill, "Missing scannedAt");
});

// ── Single skill scan ─────────────────────────────────────────────────────────
console.log("\nSingle skill scan");

test("--skill flag filters to one skill", () => {
  const results = getResults(["--skill", "file-cleaner"]);
  assert(results.length === 1, `Expected 1 result, got ${results.length}`);
  assert(results[0].name === "file-cleaner", "Wrong skill returned");
});

test("--skill with unknown name exits non-zero", () => {
  let threw = false;
  try {
    execFileSync(NODE, [AUDIT, "--dir", SAMPLES, "--skill", "nonexistent-skill-xyz"], {
      encoding: "utf8", timeout: 5_000,
    });
  } catch {
    threw = true;
  }
  assert(threw, "Should have exited non-zero for unknown skill");
});

// ── False positive checks ─────────────────────────────────────────────────────
console.log("\nFalse positive checks");

test("weather-lookup does not trigger H1 (no shell exec)", () => {
  const skill   = getResults().find(r => r.name === "weather-lookup");
  const ruleIds = skill.triggeredRules.map(r => r.id);
  assert(!ruleIds.includes("H1") && !ruleIds.includes("H1b"),
    `H1 falsely triggered on weather-lookup. Rules: ${ruleIds.join(", ")}`);
});

test("weather-lookup does not trigger H3 (no file deletion)", () => {
  const skill   = getResults().find(r => r.name === "weather-lookup");
  const ruleIds = skill.triggeredRules.map(r => r.id);
  assert(!ruleIds.includes("H3"),
    `H3 falsely triggered on weather-lookup. Rules: ${ruleIds.join(", ")}`);
});

test("weather-lookup does not trigger H4 (no obfuscation)", () => {
  const skill   = getResults().find(r => r.name === "weather-lookup");
  const ruleIds = skill.triggeredRules.map(r => r.id);
  assert(!ruleIds.includes("H4"),
    `H4 falsely triggered on weather-lookup. Rules: ${ruleIds.join(", ")}`);
});

// ── Trust score ───────────────────────────────────────────────────────────────
console.log("\nTrust score");

test("trust score is present and in range 0-100", () => {
  for (const r of getResults()) {
    assert(typeof r.trustScore.score === "number",
      `${r.name}: trustScore.score not a number`);
    assert(r.trustScore.score >= 0 && r.trustScore.score <= 100,
      `${r.name}: trustScore.score out of range: ${r.trustScore.score}`);
  }
});

// ── Summary ───────────────────────────────────────────────────────────────────
console.log("\n" + "═".repeat(45));
console.log(`Results: ${passed} passed, ${failed} failed`);
if (failed > 0) {
  console.log("\nSome tests failed. See details above.");
  process.exit(1);
} else {
  console.log("\nAll tests passed.");
}
