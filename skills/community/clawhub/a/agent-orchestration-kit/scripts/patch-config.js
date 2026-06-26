#!/usr/bin/env node
/**
 * patch-config.js — Merge Agent Orchestration Kit configuration into openclaw.json
 *
 * Usage:
 *   node patch-config.js --config ~/.openclaw/openclaw.json
 *   node patch-config.js --config ~/.openclaw/openclaw.json --agents leader,executor,reviewer
 *   node patch-config.js --config ~/.openclaw/openclaw.json --leader-workspace workspace-bae
 *   node patch-config.js --dry-run --config ~/.openclaw/openclaw.json
 *
 * Options:
 *   --config PATH              Path to openclaw.json (required)
 *   --agents LIST              Comma-separated agent list (default: auto-detect)
 *   --base-dir DIR             OpenClaw root directory (default: ~/.openclaw)
 *   --leader-workspace NAME    Leader workspace dir name (default: workspace)
 *   --dry-run                  Print changes without writing
 *   --help                     Show help
 */

const fs = require("fs");
const path = require("path");
const child_process = require("child_process");

// ── Tool Deny Lists ───────────────────────────────────────────────────
// Leader keeps exec; only apply_patch and browser are denied.

const AGENT_TOOL_DENY = {
  leader:   ["apply_patch", "browser"],
  executor: ["apply_patch", "browser"],
  reviewer: ["exec", "edit", "apply_patch", "write", "browser"],
};

const DEFAULT_TOOL_DENY = ["apply_patch", "browser"];

// ── Heartbeat Defaults ─────────────────────────────────────────────────
const HEARTBEAT_CONFIG = { every: "3m", target: "last" };

// ── Version Check ─────────────────────────────────────────────────────
// Uses a hardcoded command string — no user input, safe to use execSync.

function checkVersion() {
  const OPENCLAW_VERSION_CMD = "openclaw --version";
  try {
    const output = child_process
      .execSync(OPENCLAW_VERSION_CMD, { stdio: ["ignore", "pipe", "ignore"] })
      .toString()
      .trim();
    // e.g. "OpenClaw v2026.3.10" or "2026.3.10"
    const match = output.match(/(\d{4})\.(\d{1,2})\.(\d{1,2})/);
    if (!match) {
      console.log("[WARN] Could not parse openclaw version from: " + output);
      return;
    }
    const [, year, month, day] = match.map(Number);
    const ver = year * 10000 + month * 100 + day;
    const min = 2026 * 10000 + 2 * 100 + 26; // v2026.2.26
    if (ver < min) {
      console.log(
        `[WARN] openclaw v${year}.${month}.${day} is below the recommended minimum v2026.2.26.`
      );
      console.log("[WARN] Some features may not work correctly. Please upgrade openclaw.");
    } else {
      console.log(`[OK]   openclaw version: ${year}.${month}.${day}`);
    }
  } catch {
    console.log("[WARN] Could not run 'openclaw --version' — is openclaw installed?");
  }
}

// ── Agent Auto-Detection ──────────────────────────────────────────────

function detectAgents(baseDir, leaderWorkspace) {
  const detected = [];
  const leaderWsName = leaderWorkspace || "workspace";

  // Leader lives in the leader workspace dir (default: "workspace", custom: e.g. "workspace-bae")
  const leaderWs = path.join(baseDir, leaderWsName);
  if (fs.existsSync(path.join(leaderWs, "AGENTS.md"))) {
    detected.push("leader");
  }

  // Other agents live in workspace-<id>/
  let entries;
  try {
    entries = fs.readdirSync(baseDir, { withFileTypes: true });
  } catch {
    entries = [];
  }

  for (const entry of entries) {
    if (!entry.isDirectory()) continue;
    // Skip the leader workspace directory (whether default or custom)
    if (entry.name === leaderWsName) continue;
    const match = entry.name.match(/^workspace-(.+)$/);
    if (!match) continue;
    const agentId = match[1];
    const agentsmd = path.join(baseDir, entry.name, "AGENTS.md");
    if (fs.existsSync(agentsmd)) {
      detected.push(agentId);
    }
  }

  return detected;
}

// ── Argument Parsing ──────────────────────────────────────────────────

function parseArgs(argv) {
  const args = {
    config: null,
    agents: null, // null = auto-detect
    baseDir: path.join(process.env.HOME || require("os").homedir(), ".openclaw"),
    leaderWorkspace: null, // null = default "workspace"
    dryRun: false,
  };

  for (let i = 2; i < argv.length; i++) {
    switch (argv[i]) {
      case "--config":
        args.config = argv[++i];
        break;
      case "--agents":
        args.agents = argv[++i].split(",").map((s) => s.trim());
        break;
      case "--base-dir":
        args.baseDir = argv[++i];
        break;
      case "--leader-workspace":
        args.leaderWorkspace = argv[++i];
        break;
      case "--dry-run":
        args.dryRun = true;
        break;
      case "--help":
      case "-h":
        console.log(
          "Usage: node patch-config.js --config <path> [--agents <list>] [--base-dir <dir>] [--dry-run]"
        );
        console.log("");
        console.log("Options:");
        console.log("  --config PATH       Path to openclaw.json (required)");
        console.log("  --agents LIST       Comma-separated agent IDs (default: auto-detect)");
        console.log("  --base-dir DIR      OpenClaw root directory (default: ~/.openclaw)");
        console.log("  --leader-workspace NAME  Leader workspace dir name (default: workspace)");
        console.log("  --dry-run           Preview changes without writing");
        console.log("  --help              Show this help");
        process.exit(0);
        break;
      default:
        console.error(`[ERROR] Unknown option: ${argv[i]}`);
        process.exit(1);
    }
  }

  if (!args.config) {
    console.error("[ERROR] --config is required");
    process.exit(1);
  }

  return args;
}

// ── Deep Merge ────────────────────────────────────────────────────────
// Arrays are replaced, not merged.

function deepMerge(target, source) {
  const result = { ...target };
  for (const key of Object.keys(source)) {
    if (
      source[key] &&
      typeof source[key] === "object" &&
      !Array.isArray(source[key]) &&
      target[key] &&
      typeof target[key] === "object" &&
      !Array.isArray(target[key])
    ) {
      result[key] = deepMerge(target[key], source[key]);
    } else {
      result[key] = source[key];
    }
  }
  return result;
}

// ── Display Name from Agent ID ────────────────────────────────────────

function displayName(agentId) {
  return agentId
    .split("-")
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
    .join(" ");
}

// ── Build Agent Entry ─────────────────────────────────────────────────

function buildAgentEntry(agentId, args) {
  const wsDir = agentId === "leader" ? (args.leaderWorkspace || "workspace") : `workspace-${agentId}`;
  const toolDeny =
    agentId in AGENT_TOOL_DENY ? AGENT_TOOL_DENY[agentId] : DEFAULT_TOOL_DENY;

  const entry = {
    id: agentId,
    name: displayName(agentId),
    workspace: path.join(args.baseDir, wsDir),
    // No model key — inherits from agents.defaults.model
    tools: {
      deny: toolDeny,
    },
  };

  if (agentId === "leader") {
    entry.default = true;
    entry.identity = { name: "Assistant", emoji: "🎛️" };
    entry.heartbeat = HEARTBEAT_CONFIG;
  }

  if (agentId === "reviewer") {
    entry.sandbox = { mode: "non-main", scope: "session" };
  }

  return entry;
}

// ── Patch Config ──────────────────────────────────────────────────────

function patchConfig(config, agents, args) {
  const patched = { ...config };

  // ── Ensure agents section exists ──
  if (!patched.agents) patched.agents = {};

  // ── Agent defaults ──
  patched.agents.defaults = deepMerge(patched.agents.defaults || {}, {
    compaction: { mode: "safeguard" },
    timeoutSeconds: 1800,
    maxConcurrent: 4,
    subagents: { maxConcurrent: 8 },
    heartbeat: HEARTBEAT_CONFIG,
  });
  console.log("[SET]  agents.defaults.heartbeat: every 3m");

  // Remove stale fields that cause an implicit "Main" agent
  delete patched.agents.defaults.workspace;
  delete patched.agents.defaults.models;

  // ── Build agent list ──
  const existingList = patched.agents.list || [];
  const existingIds = new Set(existingList.map((a) => a.id));
  const newEntries = [];

  for (const agentId of agents) {
    if (!existingIds.has(agentId)) {
      newEntries.push(buildAgentEntry(agentId, args));
      console.log(`[ADD]  Agent: ${agentId}`);
    } else {
      console.log(`[SKIP] Agent: ${agentId} (already exists)`);
    }
  }

  patched.agents.list = [...existingList, ...newEntries];

  // ── A2A configuration ──
  if (!patched.tools) patched.tools = {};
  patched.tools.agentToAgent = {
    enabled: true,
    allow: [...agents],
  };
  patched.tools.sessions = { visibility: "all" };
  console.log("[SET]  tools.agentToAgent");

  // Exec safe-bin trusted dirs (Homebrew paths for exec-capable agents)
  if (!patched.tools.exec) patched.tools.exec = {};
  if (!patched.tools.exec.safeBinTrustedDirs) {
    patched.tools.exec.safeBinTrustedDirs = [
      "/bin",
      "/usr/bin",
      "/opt/homebrew/bin",
      "/usr/local/bin",
    ];
    console.log("[SET]  tools.exec.safeBinTrustedDirs");
  } else {
    console.log("[SKIP] tools.exec.safeBinTrustedDirs (already configured)");
  }

  // ── Session configuration ──
  if (!patched.session) patched.session = {};
  patched.session.agentToAgent = { maxPingPongTurns: 3 };
  if (!patched.session.parentForkMaxTokens) {
    patched.session.parentForkMaxTokens = 100000;
  }
  console.log("[SET]  session.agentToAgent.maxPingPongTurns: 3");
  console.log("[SET]  session.parentForkMaxTokens: 100000");

  // ── Hooks ──
  patched.hooks = deepMerge(patched.hooks || {}, {
    internal: {
      enabled: true,
      entries: {
        "boot-md":               { enabled: true },
        "bootstrap-extra-files": { enabled: true },
        "command-logger":        { enabled: true },
        "session-memory":        { enabled: true },
      },
    },
  });
  console.log("[SET]  hooks.internal entries");

  // ── Messages ──
  if (!patched.messages) patched.messages = {};
  if (!patched.messages.ackReactionScope) {
    patched.messages.ackReactionScope = "all";
    console.log("[SET]  messages.ackReactionScope: all");
  }

  // ── Commands ──
  patched.commands = deepMerge(patched.commands || {}, {
    native: "auto",
    nativeSkills: "auto",
    restart: true,
  });

  // NOTE: No memory/QMD section in this kit.

  return patched;
}

// ── Main ──────────────────────────────────────────────────────────────

function main() {
  const args = parseArgs(process.argv);

  // Check openclaw version
  checkVersion();
  console.log("");

  // Resolve agent list (auto-detect or explicit)
  let agents = args.agents;
  if (!agents) {
    agents = detectAgents(args.baseDir, args.leaderWorkspace);
    if (agents.length === 0) {
      console.log(
        "[WARN] No agents detected in " + args.baseDir +
        " (looking for workspace/ and workspace-<id>/ dirs with AGENTS.md)"
      );
      console.log("[WARN] Defaulting to: leader, executor, reviewer");
      agents = ["leader", "executor", "reviewer"];
    } else {
      console.log(`[AUTO] Detected agents: ${agents.join(", ")}`);
    }
  }

  if (!agents.includes("leader")) {
    console.error("[ERROR] Leader agent is required (no workspace/AGENTS.md found)");
    process.exit(1);
  }

  console.log(`[INFO] Config:   ${args.config}`);
  console.log(`[INFO] Agents:   ${agents.join(", ")}`);
  console.log(`[INFO] Base dir: ${args.baseDir}`);
  if (args.dryRun) console.log("[INFO] DRY RUN — no changes will be written");
  console.log("");

  // Read existing config
  let config = {};
  if (fs.existsSync(args.config)) {
    const raw = fs.readFileSync(args.config, "utf8");
    config = JSON.parse(raw);
    console.log("[OK]   Read existing openclaw.json");
  } else {
    console.log("[INFO] No existing openclaw.json — creating new");
  }

  // Apply patches
  const patched = patchConfig(config, agents, args);

  // Write result
  if (args.dryRun) {
    console.log("\n[DRY RUN] Would write:");
    console.log(JSON.stringify(patched, null, 2));
  } else {
    // Backup original
    if (fs.existsSync(args.config)) {
      const backupPath = args.config + ".backup-" + Date.now();
      fs.copyFileSync(args.config, backupPath);
      console.log(`\n[OK]   Backup: ${backupPath}`);
    }

    // Ensure parent directory exists
    const configDir = path.dirname(args.config);
    if (!fs.existsSync(configDir)) {
      fs.mkdirSync(configDir, { recursive: true });
    }

    fs.writeFileSync(args.config, JSON.stringify(patched, null, 2) + "\n");
    console.log(`[OK]   Written: ${args.config}`);
  }

  console.log("\n[OK]   Config patching complete");
  console.log("\nNext steps:");
  console.log("  1. openclaw gateway restart");
  console.log("  2. openclaw doctor           (validate config + DM allowlist inheritance)");
  console.log("  3. openclaw secrets audit    (optional: check for plaintext secrets)");
}

main();
