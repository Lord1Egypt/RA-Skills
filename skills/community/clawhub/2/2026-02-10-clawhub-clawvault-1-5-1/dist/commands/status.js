import {
  ClawVault
} from "../chunk-MXNXWOPL.js";
import {
  scanVaultLinks
} from "../chunk-4VQTUVH7.js";
import "../chunk-J7ZWCI2C.js";
import {
  formatAge
} from "../chunk-7ZRP733D.js";
import {
  QmdUnavailableError,
  hasQmd
} from "../chunk-VJIFT5T5.js";

// src/commands/status.ts
import * as fs from "fs";
import * as path from "path";
import { execFileSync } from "child_process";
var CLAWVAULT_DIR = ".clawvault";
var CHECKPOINT_FILE = "last-checkpoint.json";
var DIRTY_DEATH_FLAG = "dirty-death.flag";
function findGitRoot(startPath) {
  let current = path.resolve(startPath);
  while (true) {
    if (fs.existsSync(path.join(current, ".git"))) {
      return current;
    }
    const parent = path.dirname(current);
    if (parent === current) return null;
    current = parent;
  }
}
function getGitStatus(repoRoot) {
  const output = execFileSync("git", ["-C", repoRoot, "status", "--porcelain"], {
    encoding: "utf-8"
  });
  const lines = output.split("\n").filter(Boolean);
  return { clean: lines.length === 0, dirtyCount: lines.length };
}
function parseQmdCollectionsText(raw) {
  const names = [];
  const regex = /^(\S+)\s+\(qmd:\/\/\1\/\)/gm;
  let match;
  while ((match = regex.exec(raw)) !== null) {
    names.push(match[1]);
  }
  return names;
}
function getQmdIndexStatus(collection, root) {
  const output = execFileSync("qmd", ["collection", "list"], { encoding: "utf-8" });
  const names = parseQmdCollectionsText(output);
  if (names.includes(collection)) {
    return "present";
  }
  return "missing";
}
function loadCheckpoint(vaultPath) {
  const checkpointPath = path.join(vaultPath, CLAWVAULT_DIR, CHECKPOINT_FILE);
  if (!fs.existsSync(checkpointPath)) {
    return { data: null };
  }
  try {
    const data = JSON.parse(fs.readFileSync(checkpointPath, "utf-8"));
    return { data };
  } catch (err) {
    return { data: null, error: err?.message || "Failed to parse checkpoint" };
  }
}
async function getStatus(vaultPath) {
  if (!hasQmd()) {
    throw new QmdUnavailableError();
  }
  const vault = new ClawVault(path.resolve(vaultPath));
  await vault.load();
  const stats = await vault.stats();
  const linkScan = scanVaultLinks(vault.getPath());
  const issues = [];
  const checkpointInfo = loadCheckpoint(vault.getPath());
  const checkpoint = checkpointInfo.data;
  if (checkpointInfo.error) {
    issues.push(`Checkpoint parse error: ${checkpointInfo.error}`);
  }
  const checkpointStatus = {
    exists: Boolean(checkpoint),
    timestamp: checkpoint?.timestamp,
    age: checkpoint?.timestamp ? formatAge(Date.now() - new Date(checkpoint.timestamp).getTime()) : void 0,
    sessionKey: checkpoint?.sessionKey,
    model: checkpoint?.model,
    tokenEstimate: checkpoint?.tokenEstimate
  };
  if (!checkpointStatus.exists) {
    issues.push("No checkpoint found");
  }
  const dirtyFlagPath = path.join(vault.getPath(), CLAWVAULT_DIR, DIRTY_DEATH_FLAG);
  if (fs.existsSync(dirtyFlagPath)) {
    issues.push("Dirty death flag is set");
  }
  const qmdCollection = vault.getQmdCollection();
  const qmdRoot = vault.getQmdRoot();
  let qmdIndexStatus = "missing";
  let qmdError;
  try {
    qmdIndexStatus = getQmdIndexStatus(qmdCollection, qmdRoot);
    if (qmdIndexStatus !== "present") {
      issues.push(`qmd collection ${qmdIndexStatus.replace("-", " ")}`);
    }
  } catch (err) {
    qmdError = err?.message || "Failed to check qmd index";
    issues.push(`qmd status error: ${qmdError}`);
  }
  let gitStatus;
  const gitRoot = findGitRoot(vault.getPath());
  if (gitRoot) {
    try {
      const gitInfo = getGitStatus(gitRoot);
      gitStatus = { repoRoot: gitRoot, ...gitInfo };
      if (!gitInfo.clean) {
        issues.push(`Uncommitted changes: ${gitInfo.dirtyCount}`);
      }
    } catch (err) {
      issues.push(`Git status error: ${err?.message || "unknown error"}`);
    }
  }
  return {
    vaultName: vault.getName(),
    vaultPath: vault.getPath(),
    health: issues.length === 0 ? "ok" : "warning",
    issues,
    checkpoint: checkpointStatus,
    qmd: {
      collection: qmdCollection,
      root: qmdRoot,
      indexStatus: qmdIndexStatus,
      error: qmdError
    },
    git: gitStatus,
    links: {
      total: linkScan.linkCount,
      orphans: linkScan.orphans.length
    },
    documents: stats.documents,
    categories: stats.categories
  };
}
function formatStatus(status) {
  let output = "ClawVault Status\n";
  output += "-".repeat(40) + "\n";
  output += `Vault: ${status.vaultName}
`;
  output += `Path: ${status.vaultPath}
`;
  output += `Health: ${status.health}
`;
  if (status.issues.length > 0) {
    output += `Issues: ${status.issues.join("; ")}
`;
  } else {
    output += "Issues: none\n";
  }
  output += "\nCheckpoint:\n";
  if (!status.checkpoint.exists) {
    output += "  - none\n";
  } else {
    output += `  - Timestamp: ${status.checkpoint.timestamp}
`;
    if (status.checkpoint.age) {
      output += `  - Age: ${status.checkpoint.age}
`;
    }
    if (status.checkpoint.sessionKey) {
      output += `  - Session key: ${status.checkpoint.sessionKey}
`;
    }
    if (status.checkpoint.model) {
      output += `  - Model: ${status.checkpoint.model}
`;
    }
    if (status.checkpoint.tokenEstimate !== void 0) {
      output += `  - Token estimate: ${status.checkpoint.tokenEstimate}
`;
    }
  }
  output += "\nqmd:\n";
  output += `  - Collection: ${status.qmd.collection}
`;
  output += `  - Root: ${status.qmd.root}
`;
  output += `  - Index: ${status.qmd.indexStatus}
`;
  if (status.qmd.error) {
    output += `  - Error: ${status.qmd.error}
`;
  }
  if (status.git) {
    output += "\nGit:\n";
    output += `  - Repo: ${status.git.repoRoot}
`;
    output += `  - Status: ${status.git.clean ? "clean" : "dirty"} (${status.git.dirtyCount} change(s))
`;
  }
  output += "\nLinks:\n";
  output += `  - Total: ${status.links.total}
`;
  if (status.links.orphans > 0) {
    output += `  - Orphans: ${status.links.orphans}
`;
  }
  output += "\nDocuments:\n";
  output += `  - Total: ${status.documents}
`;
  output += "  - By category:\n";
  for (const [category, count] of Object.entries(status.categories)) {
    output += `    * ${category}: ${count}
`;
  }
  output += "-".repeat(40) + "\n";
  return output;
}
async function statusCommand(vaultPath, options = {}) {
  const status = await getStatus(vaultPath);
  if (options.json) {
    console.log(JSON.stringify(status, null, 2));
    return;
  }
  console.log(formatStatus(status));
}
export {
  formatStatus,
  getStatus,
  statusCommand
};
