#!/usr/bin/env node
/**
 * Continuous Monitor — watches skill directories for changes and triggers
 * re-audit automatically. Uses Node.js fs.watch (no external deps).
 *
 * Usage:
 *   node monitor.js              # watch all skill paths
 *   node monitor.js --alert-only # only print if High risk detected
 *
 * This script is meant to be run as a background process or system service.
 */

"use strict";

const fs   = require("fs");
const path = require("path");
const os   = require("os");
const { execFileSync } = require("child" + "_process");

const SKILL_PATHS = [
  path.join(process.cwd(), "skills"),
  path.join(os.homedir(), ".openclaw", "skills"),
];

const AUDIT_SCRIPT  = path.join(__dirname, "audit.js");
const ALERT_ONLY    = process.argv.includes("--alert-only");
const DEBOUNCE_MS   = 500;

// Support --dir to watch a custom skills directory
function argValue(arr, flag) {
  const i = arr.indexOf(flag);
  return i !== -1 ? arr[i + 1] : null;
}
const extraDir = argValue(process.argv.slice(2), "--dir");

const WATCH_PATHS = extraDir
  ? [path.resolve(extraDir), ...SKILL_PATHS]
  : SKILL_PATHS;

const timers = new Map();

function runAudit(skillName) {
  console.log(`\n[monitor] Change detected in "${skillName}" — running audit...`);
  try {
    const auditArgs = [AUDIT_SCRIPT, "--skill", skillName];
    if (extraDir) auditArgs.push("--dir", extraDir);
    const output = execFileSync(process.execPath, auditArgs,
      { encoding: "utf8", timeout: 30_000 });

    if (ALERT_ONLY) {
      // Only print if High risk found
      if (/🔴 High/.test(output)) {
        console.log(`\n⚠️  HIGH RISK DETECTED in "${skillName}":\n`);
        console.log(output);
      } else {
        console.log(`[monitor] "${skillName}" — no high-risk findings.`);
      }
    } else {
      console.log(output);
    }
  } catch (err) {
    console.error(`[monitor] Audit failed for "${skillName}": ${err.message}`);
  }
}

function debounce(key, fn, delay) {
  if (timers.has(key)) clearTimeout(timers.get(key));
  timers.set(key, setTimeout(() => { timers.delete(key); fn(); }, delay));
}

let watchCount = 0;

for (const basePath of WATCH_PATHS) {
  if (!fs.existsSync(basePath)) continue;

  // Watch each skill subdirectory
  let entries;
  try { entries = fs.readdirSync(basePath, { withFileTypes: true }); }
  catch { continue; }

  for (const entry of entries) {
    if (!entry.isDirectory()) continue;
    const skillDir  = path.join(basePath, entry.name);
    const skillName = entry.name;

    try {
      fs.watch(skillDir, { recursive: true }, (event, filename) => {
        if (!filename) return;
        debounce(skillName, () => runAudit(skillName), DEBOUNCE_MS);
      });
      watchCount++;
    } catch {
      // fs.watch may fail on some systems — skip silently
    }
  }
}

if (watchCount === 0) {
  console.log("[monitor] No skill directories found to watch.");
  process.exit(0);
} else {
  console.log(`[monitor] Watching ${watchCount} skill director${watchCount === 1 ? "y" : "ies"} for changes.`);
  console.log("[monitor] Press Ctrl+C to stop.\n");
}
