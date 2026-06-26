import {
  ClawVault,
  findVault
} from "../chunk-MXNXWOPL.js";
import {
  scanVaultLinks
} from "../chunk-4VQTUVH7.js";
import "../chunk-J7ZWCI2C.js";
import {
  formatAge
} from "../chunk-7ZRP733D.js";
import {
  hasQmd
} from "../chunk-VJIFT5T5.js";

// src/commands/doctor.ts
import * as fs from "fs";
import * as os from "os";
import * as path from "path";
var CLAWVAULT_DIR = ".clawvault";
var CHECKPOINT_FILE = "last-checkpoint.json";
var DAY_MS = 24 * 60 * 60 * 1e3;
var ACTIVE_USE_DAYS = 7;
function daysSince(date, now = Date.now()) {
  return Math.max(0, Math.floor((now - date.getTime()) / DAY_MS));
}
function describeAge(date, now = Date.now()) {
  return formatAge(now - date.getTime());
}
function loadCheckpointTimestamp(vaultPath) {
  const checkpointPath = path.join(vaultPath, CLAWVAULT_DIR, CHECKPOINT_FILE);
  if (!fs.existsSync(checkpointPath)) {
    return {};
  }
  try {
    const data = JSON.parse(fs.readFileSync(checkpointPath, "utf-8"));
    return { timestamp: data.timestamp };
  } catch (err) {
    return { error: err?.message || "Failed to parse checkpoint" };
  }
}
function getShellConfigPaths(shellPath) {
  const home = os.homedir();
  const shellName = shellPath ? path.basename(shellPath) : "bash";
  if (shellName === "zsh") {
    return [path.join(home, ".zshrc"), path.join(home, ".zprofile")];
  }
  if (shellName === "fish") {
    return [path.join(home, ".config", "fish", "config.fish")];
  }
  return [path.join(home, ".bashrc"), path.join(home, ".bash_profile"), path.join(home, ".profile")];
}
function hasClawvaultPathConfig(paths) {
  for (const filePath of paths) {
    if (!fs.existsSync(filePath)) continue;
    try {
      const content = fs.readFileSync(filePath, "utf-8");
      if (/CLAWVAULT_PATH\s*=/.test(content)) {
        return true;
      }
    } catch {
    }
  }
  return false;
}
async function resolveVault(vaultPath) {
  if (vaultPath) {
    const vault = new ClawVault(path.resolve(vaultPath));
    await vault.load();
    return vault;
  }
  const envPath = process.env.CLAWVAULT_PATH;
  if (envPath) {
    const vault = new ClawVault(path.resolve(envPath));
    await vault.load();
    return vault;
  }
  const found = await findVault();
  if (!found) {
    throw new Error("No ClawVault found. Run `clawvault init` first.");
  }
  return found;
}
async function doctor(vaultPath) {
  const checks = [];
  let warnings = 0;
  let errors = 0;
  if (hasQmd()) {
    checks.push({ label: "qmd installed", status: "ok" });
  } else {
    checks.push({
      label: "qmd installed",
      status: "error",
      hint: "Install qmd to enable ClawVault commands."
    });
    errors++;
  }
  const shellConfigs = getShellConfigPaths(process.env.SHELL).filter(fs.existsSync);
  if (hasClawvaultPathConfig(shellConfigs)) {
    checks.push({
      label: "CLAWVAULT_PATH in shell config",
      status: "ok",
      detail: shellConfigs.map((p) => path.basename(p)).join(", ")
    });
  } else {
    checks.push({
      label: "CLAWVAULT_PATH in shell config",
      status: "warn",
      hint: "Run `clawvault shell-init` and add it to your shell rc."
    });
    warnings++;
  }
  if (!hasQmd()) {
    return { vaultPath, checks, warnings, errors };
  }
  let vault;
  try {
    vault = await resolveVault(vaultPath);
    checks.push({ label: "vault found", status: "ok", detail: vault.getPath() });
  } catch (err) {
    checks.push({
      label: "vault found",
      status: "error",
      detail: err?.message || "Unable to locate vault"
    });
    errors++;
    return { vaultPath, checks, warnings, errors };
  }
  const stats = await vault.stats();
  const documents = await vault.list();
  const handoffs = await vault.list("handoffs");
  const inbox = await vault.list("inbox");
  const qmdCollection = vault.getQmdCollection();
  if (qmdCollection) {
    checks.push({ label: "qmd collection configured", status: "ok", detail: qmdCollection });
  } else {
    checks.push({
      label: "qmd collection configured",
      status: "warn",
      hint: "Set qmd collection in .clawvault.json"
    });
    warnings++;
  }
  const latestDoc = documents.slice().sort((a, b) => b.modified.getTime() - a.modified.getTime())[0];
  const latestDocAge = latestDoc ? daysSince(latestDoc.modified) : null;
  let lastHandoffAge = null;
  if (handoffs.length === 0) {
    checks.push({
      label: "recent handoff",
      status: "warn",
      hint: "Run `clawvault sleep` at the end of sessions."
    });
    warnings++;
  } else {
    const latestHandoff = handoffs.slice().sort((a, b) => b.modified.getTime() - a.modified.getTime())[0];
    lastHandoffAge = daysSince(latestHandoff.modified);
    const ageLabel = describeAge(latestHandoff.modified);
    if (lastHandoffAge > 1) {
      checks.push({
        label: "recent handoff",
        status: "warn",
        detail: `Last handoff ${ageLabel} ago`,
        hint: "Run `clawvault sleep` before long pauses."
      });
      warnings++;
    } else {
      checks.push({
        label: "recent handoff",
        status: "ok",
        detail: `Last handoff ${ageLabel} ago`
      });
    }
  }
  const checkpointInfo = loadCheckpointTimestamp(vault.getPath());
  const activeUse = latestDocAge !== null && latestDocAge <= ACTIVE_USE_DAYS || lastHandoffAge !== null && lastHandoffAge <= ACTIVE_USE_DAYS;
  if (checkpointInfo.error) {
    checks.push({
      label: "checkpoint freshness",
      status: "warn",
      detail: checkpointInfo.error
    });
    warnings++;
  } else if (!checkpointInfo.timestamp) {
    const status = activeUse ? "warn" : "ok";
    if (status === "warn") warnings++;
    checks.push({
      label: "checkpoint freshness",
      status,
      detail: activeUse ? "No checkpoint found" : "No checkpoint found (vault appears inactive)",
      hint: activeUse ? "Run `clawvault checkpoint` during heavy work." : void 0
    });
  } else {
    const checkpointDate = new Date(checkpointInfo.timestamp);
    const checkpointAge = daysSince(checkpointDate);
    const ageLabel = describeAge(checkpointDate);
    if (activeUse && checkpointAge > 1) {
      checks.push({
        label: "checkpoint freshness",
        status: "warn",
        detail: `Last checkpoint ${ageLabel} ago`,
        hint: "Checkpoint at least once per active day."
      });
      warnings++;
    } else {
      checks.push({
        label: "checkpoint freshness",
        status: "ok",
        detail: `Last checkpoint ${ageLabel} ago`
      });
    }
  }
  const linkScan = scanVaultLinks(vault.getPath());
  if (linkScan.orphans.length > 20) {
    checks.push({
      label: "orphan links",
      status: "warn",
      detail: `${linkScan.orphans.length} orphan link(s)`,
      hint: "Run `clawvault link --orphans` to review."
    });
    warnings++;
  } else {
    checks.push({
      label: "orphan links",
      status: "ok",
      detail: `${linkScan.orphans.length} orphan link(s)`
    });
  }
  if (inbox.length > 5) {
    checks.push({
      label: "inbox backlog",
      status: "warn",
      detail: `${inbox.length} inbox item(s) pending`,
      hint: "Process inbox items to keep memory tidy."
    });
    warnings++;
  } else {
    checks.push({
      label: "inbox backlog",
      status: "ok",
      detail: `${inbox.length} inbox item(s) pending`
    });
  }
  if (stats.documents < 5) {
    checks.push({
      label: "vault activity",
      status: "warn",
      detail: `${stats.documents} total documents`,
      hint: "Start capturing decisions, lessons, and projects."
    });
    warnings++;
  }
  return { vaultPath: vault.getPath(), checks, warnings, errors };
}
export {
  doctor
};
