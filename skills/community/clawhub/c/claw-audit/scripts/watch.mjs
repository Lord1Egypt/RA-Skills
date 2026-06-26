#!/usr/bin/env node

/**
 * ClawAudit Watch Mode
 * Monitors skill directories for new installations and alerts on suspicious skills.
 *
 * Usage:
 *   node watch.mjs              # Start watching
 *   node watch.mjs --interval 5 # Check every 5 seconds (default: 10)
 */

import { watch, existsSync, readdirSync, readFileSync } from "fs";
import { join } from "path";
import { homedir } from "os";
import { spawnSync } from "child_process";
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";
import { COLORS } from "./lib/utils.mjs";

const __dirname = dirname(fileURLToPath(import.meta.url));
const HOME = homedir();

// Parse interval arg
let interval = 10;
const intervalIdx = process.argv.indexOf("--interval");
if (intervalIdx !== -1 && process.argv[intervalIdx + 1]) {
  interval = parseInt(process.argv[intervalIdx + 1], 10) || 10;
}

const { BOLD, GREEN, RED, YELLOW, GRAY, RESET } = COLORS;

// Skill directories to watch
const WATCH_DIRS = [
  join(HOME, ".openclaw", "skills"),
  join(HOME, "openclaw", "skills"),
  join(HOME, ".clawdbot", "skills"),
];

if (process.env.OPENCLAW_WORKSPACE) {
  WATCH_DIRS.unshift(join(process.env.OPENCLAW_WORKSPACE, "skills"));
}

// Cron jobs.json path
const CRON_JOBS_PATH = join(HOME, ".openclaw", "cron", "jobs.json");

// Track cron job state
let lastCronHash = null;

function getCronHash() {
  try {
    return readFileSync(CRON_JOBS_PATH, "utf-8");
  } catch {
    return null;
  }
}

function runConfigAudit() {
  console.log(`\n${YELLOW}🔍 Cron jobs changed — running config audit...${RESET}`);
  const auditScript = resolve(__dirname, "audit-config.mjs");
  const proc = spawnSync("node", [auditScript, "--json"], { encoding: "utf-8", timeout: 15000 });
  try {
    const data = JSON.parse(proc.stdout);
    const { critical = 0, warnings = 0 } = data;
    const findings = data.findings || [];

    if (critical > 0 || warnings > 0) {
      const cronFindings = findings.filter((f) => ["WARN-021", "WARN-022"].includes(f.code));
      if (cronFindings.length > 0) {
        console.log(`${RED}🚨 Cron config issues detected:${RESET}`);
        for (const f of cronFindings) {
          const icon = f.severity === "critical" ? RED + "🔴" : YELLOW + "🟡";
          console.log(`${icon} ${f.code}: ${f.title}${RESET}`);
          console.log(`${GRAY}   ${f.detail}${RESET}`);
          if (f.fix) console.log(`${GRAY}   💡 ${f.fix}${RESET}`);
        }
      } else {
        console.log(`${YELLOW}⚠️  ${warnings} warning(s), ${critical} critical — no cron-specific issues.${RESET}`);
      }
    } else {
      console.log(`${GREEN}✅ Cron config looks good — no issues detected.${RESET}`);
    }
  } catch {
    console.log(`${GRAY}   Audit parse error: ${proc.stderr || "unknown"}${RESET}`);
  }
}

// Track known skills
let knownSkills = new Set();

function getInstalledSkills(dir) {
  if (!existsSync(dir)) return [];
  try {
    return readdirSync(dir, { withFileTypes: true })
      .filter((d) => d.isDirectory())
      .map((d) => d.name);
  } catch {
    return [];
  }
}

function scanNewSkill(skillName, skillDir) {
  console.log(`\n${YELLOW}🔍 Scanning new skill: ${BOLD}${skillName}${RESET}`);
  try {
    // Use spawnSync with argument array to prevent shell injection via skillName
    const proc = spawnSync(
      "bash",
      [resolve(__dirname, "scan-skills.sh"), "--skill", skillName, "--json"],
      { encoding: "utf-8", timeout: 15000 }
    );
    if (proc.status !== 0 && !proc.stdout) throw new Error(proc.stderr || "scan failed");
    const data = JSON.parse(proc.stdout);

    if (data.critical > 0) {
      console.log(`${RED}🚨 ALERT: ${data.critical} critical finding(s) in "${skillName}"!${RESET}`);
      console.log(`${RED}   This skill may be malicious. Review immediately.${RESET}`);
      for (const f of data.findings) {
        const parsed = typeof f === "string" ? JSON.parse(f) : f;
        if (parsed.severity === "critical") {
          console.log(`${RED}   • ${parsed.code}: ${parsed.label}${RESET}`);
        }
      }
    } else if (data.warnings > 0) {
      console.log(`${YELLOW}⚠️  ${data.warnings} warning(s) in "${skillName}". Review recommended.${RESET}`);
    } else {
      console.log(`${GREEN}✅ "${skillName}" looks clean.${RESET}`);
    }
  } catch (err) {
    console.log(`${GRAY}   Could not scan (skill may have no scannable files)${RESET}`);
  }
}

function checkForChanges() {
  // Check skills
  for (const dir of WATCH_DIRS) {
    const skills = getInstalledSkills(dir);
    for (const skill of skills) {
      const key = `${dir}:${skill}`;
      if (!knownSkills.has(key)) {
        knownSkills.add(key);
        if (initialized) {
          scanNewSkill(skill, join(dir, skill));
        }
      }
    }
  }

  // Check cron jobs.json
  const currentHash = getCronHash();
  if (currentHash !== null && currentHash !== lastCronHash) {
    if (initialized && lastCronHash !== null) {
      runConfigAudit();
    }
    lastCronHash = currentHash;
  }
}

// --- Main ---
let initialized = false;

console.log(`${BOLD}🛡️  ClawAudit Watch Mode${RESET}`);
console.log(`${GRAY}Monitoring skills + cron job config...${RESET}`);
console.log(`${GRAY}Check interval: ${interval}s${RESET}`);
console.log(`${GRAY}Skill dirs:${RESET}`);
for (const dir of WATCH_DIRS) {
  const exists = existsSync(dir);
  console.log(`   ${exists ? GREEN + "●" : GRAY + "○"} ${dir}${RESET}`);
}
const cronExists = existsSync(CRON_JOBS_PATH);
console.log(`${GRAY}Cron jobs:${RESET}`);
console.log(`   ${cronExists ? GREEN + "●" : GRAY + "○"} ${CRON_JOBS_PATH}${RESET}`);
console.log(`\n${GRAY}Press Ctrl+C to stop.${RESET}\n`);

// Initial population
checkForChanges();
initialized = true;

// Also try native fs.watch where available
for (const dir of WATCH_DIRS) {
  if (existsSync(dir)) {
    try {
      watch(dir, { recursive: false }, (eventType, filename) => {
        if (eventType === "rename" && filename) {
          setTimeout(() => checkForChanges(), 500);
        }
      });
    } catch {
      // fs.watch not supported on all platforms for all dir types
    }
  }
}

// Watch cron jobs.json for changes
if (existsSync(CRON_JOBS_PATH)) {
  try {
    watch(CRON_JOBS_PATH, () => {
      setTimeout(() => checkForChanges(), 500);
    });
  } catch {
    // Fallback to polling
  }
}

// Polling fallback
setInterval(checkForChanges, interval * 1000);

// Keep alive
process.on("SIGINT", () => {
  console.log(`\n${GRAY}Watch mode stopped.${RESET}\n`);
  process.exit(0);
});
