#!/usr/bin/env node
/**
 * nssm-manager.js - Diagnose/refresh nssm service paths after choco upgrade
 *
 * Modes:
 *   diagnose              - Check all nssm services, detect shims
 *   update-path <service> - Output commands to refresh a specific service's path to the actual binary
 *   post-upgrade          - Full check after choco upgrade + output all refresh commands at once
 */

const { execFileSync } = require("child_process");
const fs = require("fs");
const path = require("path");

const CHOCO_BIN = "C:\\ProgramData\\chocolatey\\bin";
const CHOCO_LIB = "C:\\ProgramData\\chocolatey\\lib";

// ── helpers ──────────────────────────────────────────────

function getNssmServices() {
  try {
    const output = execFileSync(
      "powershell",
      [
        "-NoProfile",
        "-Command",
        "Get-CimInstance Win32_Service | Where-Object { $_.PathName -like '*nssm*' } | Select-Object -ExpandProperty Name",
      ],
      { encoding: "utf-8", timeout: 15000 },
    );
    return output
      .trim()
      .split(/\r?\n/)
      .map((s) => s.trim())
      .filter(Boolean);
  } catch {
    return [];
  }
}

function getServiceStatus(svc) {
  try {
    return execFileSync("nssm", ["status", svc], {
      encoding: "utf-8",
      stdio: ["pipe", "pipe", "pipe"],
    })
      .trim()
      .split(/\r?\n/)[0]
      .trim();
  } catch {
    return "UNKNOWN";
  }
}

function getNssmApp(svc) {
  try {
    const out = execFileSync("nssm", ["get", svc, "Application"], {
      encoding: "utf-8",
      stdio: ["pipe", "pipe", "pipe"],
    });
    // nssm sometimes appends LsaOpenPolicy warning – take first line only
    return out.trim().split(/\r?\n/)[0].trim();
  } catch {
    return null;
  }
}

function isChocoShim(appPath) {
  if (!appPath) return false;
  return appPath.toLowerCase().startsWith(CHOCO_BIN.toLowerCase());
}

/**
 * Recursively search for exeName inside choco lib/<pkg>/tools
 */
function findActualBinary(pkgName, exeName) {
  const toolsDir = path.join(CHOCO_LIB, pkgName, "tools");
  if (!fs.existsSync(toolsDir)) return null;

  function walk(dir) {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const full = path.join(dir, entry.name);
      if (entry.isFile() && entry.name.toLowerCase() === exeName.toLowerCase()) {
        return full;
      }
      if (entry.isDirectory()) {
        const found = walk(full);
        if (found) return found;
      }
    }
    return null;
  }

  return walk(toolsDir);
}

function isStaleChocoPath(appPath) {
  if (!appPath) return false;
  const lower = appPath.toLowerCase();
  return lower.includes("chocolatey\\lib\\") && !fs.existsSync(appPath);
}

function guessPkgFromLibPath(appPath) {
  const match = appPath.match(/chocolatey\\lib\\([^\\]+)\\/i);
  return match ? match[1] : null;
}

function analyzeService(svc) {
  const appPath = getNssmApp(svc);
  const status = getServiceStatus(svc);
  const isShim = isChocoShim(appPath);
  const isStale = isStaleChocoPath(appPath);

  const result = { service: svc, status, appPath, isShim, isStale, actual: null, commands: [] };

  if ((isShim || isStale) && appPath) {
    const exeName = path.basename(appPath);
    const pkgName = isShim
      ? exeName.replace(/\.exe$/i, "")
      : guessPkgFromLibPath(appPath) || exeName.replace(/\.exe$/i, "");
    result.actual = findActualBinary(pkgName, exeName);

    if (result.actual && result.actual.toLowerCase() !== appPath.toLowerCase()) {
      result.commands = [
        `nssm stop "${svc}"`,
        `nssm set "${svc}" Application "${result.actual}"`,
        `nssm start "${svc}"`,
      ];
    }
  }

  return result;
}

// ── commands ─────────────────────────────────────────────

function diagnose() {
  const services = getNssmServices();
  if (services.length === 0) {
    console.log("No services managed by nssm were found.");
    return;
  }

  console.log(`=== nssm service diagnosis (${services.length} services) ===\n`);

  const issues = [];

  for (const svc of services) {
    const info = analyzeService(svc);
    console.log(`[${svc}]`);
    console.log(`  Status: ${info.status}`);
    console.log(`  Path: ${info.appPath}`);
    console.log(`  Shim: ${info.isShim ? "YES (possible issue)" : "NO"}`);
    if (info.isStale) console.log(`  Stale: YES (binary path does not exist)`);
    if (info.actual) {
      console.log(`  Actual binary: ${info.actual}`);
    }
    if (info.commands.length > 0) issues.push(info);
    console.log("");
  }

  if (issues.length > 0) {
    console.log("=== Fixes required ===\n");
    for (const i of issues) {
      i.commands.forEach((c) => console.log(c));
      console.log("");
    }
    console.log("(Administrator privileges required)");
  } else {
    console.log("All nssm services are healthy.");
  }
}

function updatePath(serviceName) {
  if (!serviceName) {
    console.error("Usage: node nssm-manager.js update-path <service-name>");
    process.exit(1);
  }

  const info = analyzeService(serviceName);

  if (!info.appPath) {
    console.error(`Unable to retrieve the path for service "${serviceName}".`);
    process.exit(1);
  }

  if (info.commands.length === 0) {
    if (info.actual) {
      console.log(`"${serviceName}" path is already up to date: ${info.appPath}`);
    } else if (info.isShim) {
      console.error(`"${serviceName}" is a shim but the actual binary cannot be found.`);
      process.exit(1);
    } else {
      console.log(`"${serviceName}" is using a direct path (not a shim): ${info.appPath}`);
    }
    return;
  }

  // Output JSON for the AI to consume and execute
  console.log(JSON.stringify(info, null, 2));
}

function postUpgrade() {
  console.log("=== choco upgrade post-processing ===\n");

  const services = getNssmServices();
  if (services.length === 0) {
    console.log("No nssm services found.");
    return;
  }

  const allIssues = [];

  for (const svc of services) {
    const info = analyzeService(svc);
    console.log(`[${svc}] ${info.status} | shim=${info.isShim} | ${info.appPath}`);
    if (info.commands.length > 0) {
      allIssues.push(info);
    }
  }

  console.log("");

  if (allIssues.length === 0) {
    console.log("All service paths are healthy. No refresh needed.");
    return;
  }

  console.log(`=== ${allIssues.length} service path(s) need refresh ===\n`);

  // Generate a single PowerShell block for admin execution
  const cmds = allIssues.flatMap((i) => i.commands);
  console.log("--- Administrator PowerShell commands ---");
  console.log(cmds.join("; "));
  console.log("");
  console.log("--- Or run individually ---");
  for (const i of allIssues) {
    console.log(`\n# ${i.service}: ${i.appPath} -> ${i.actual}`);
    i.commands.forEach((c) => console.log(c));
  }
}

// ── main ─────────────────────────────────────────────────

const mode = process.argv[2] || "diagnose";
const arg = process.argv[3];

switch (mode) {
  case "diagnose":
    diagnose();
    break;
  case "update-path":
    updatePath(arg);
    break;
  case "post-upgrade":
    postUpgrade();
    break;
  default:
    console.error(`Unknown mode: ${mode}`);
    console.error("Modes: diagnose, update-path <service>, post-upgrade");
    process.exit(1);
}
