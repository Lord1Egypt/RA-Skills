"use strict";

const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { spawnSync } = require("node:child_process");

const DEFAULT_PACKAGE = "@bamdra/bamdra-openclaw-memory";
const PLUGIN_IDS = [
  "bamdra-openclaw-memory",
  "bamdra-user-bind",
  "bamdra-memory-vector",
];
const SKILL_IDS = [
  "bamdra-memory-operator",
  "bamdra-memory-upgrade-operator",
  "bamdra-user-bind-profile",
  "bamdra-user-bind-admin",
  "bamdra-memory-vector-operator",
];

function printHelp() {
  console.log("Usage: node ./scripts/upgrade-bamdra-memory.cjs <upgrade|install|uninstall> [options]");
  console.log("");
  console.log("Options:");
  console.log(`  --package <npm-spec>       Package to install (default: ${DEFAULT_PACKAGE})`);
  console.log("  --openclaw-home <path>     Override ~/.openclaw location");
  console.log("  --restart-gateway          Restart the gateway after successful install");
}

function parseArgs(argv) {
  const options = {
    mode: "upgrade",
    packageSpec: DEFAULT_PACKAGE,
    openclawHome: path.join(os.homedir(), ".openclaw"),
    restartGateway: false,
  };

  let modeSet = false;
  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === "--help" || arg === "-h") {
      printHelp();
      process.exit(0);
    }
    if (!arg.startsWith("--") && !modeSet) {
      if (!["upgrade", "install", "uninstall"].includes(arg)) {
        throw new Error(`Unknown mode: ${arg}`);
      }
      options.mode = arg;
      modeSet = true;
      continue;
    }
    if (arg === "--package") {
      options.packageSpec = argv[index + 1];
      index += 1;
      continue;
    }
    if (arg === "--openclaw-home") {
      options.openclawHome = path.resolve(argv[index + 1]);
      index += 1;
      continue;
    }
    if (arg === "--restart-gateway") {
      options.restartGateway = true;
      continue;
    }
    throw new Error(`Unknown argument: ${arg}`);
  }

  return options;
}

function log(message, details) {
  if (details) {
    console.log(`[bamdra-memory-upgrade] ${message}`, JSON.stringify(details));
    return;
  }
  console.log(`[bamdra-memory-upgrade] ${message}`);
}

function ensureDir(dirPath) {
  fs.mkdirSync(dirPath, { recursive: true });
}

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, "utf8"));
}

function writeJson(filePath, value) {
  fs.writeFileSync(filePath, `${JSON.stringify(value, null, 2)}\n`, "utf8");
}

function ensureObject(parent, key) {
  if (!parent[key] || typeof parent[key] !== "object" || Array.isArray(parent[key])) {
    parent[key] = {};
  }
  return parent[key];
}

function removeFromArray(value, targets) {
  if (!Array.isArray(value)) {
    return { changed: false, next: value };
  }
  const next = value.filter((item) => !targets.includes(item));
  return { changed: next.length !== value.length, next };
}

function sanitizeConfig(config) {
  let changed = false;
  const plugins = ensureObject(config, "plugins");
  const tools = ensureObject(config, "tools");
  const entries = ensureObject(plugins, "entries");
  const slots = ensureObject(plugins, "slots");

  for (const pluginId of PLUGIN_IDS) {
    if (pluginId in entries) {
      delete entries[pluginId];
      changed = true;
    }
  }

  const allowResult = removeFromArray(plugins.allow, PLUGIN_IDS);
  if (allowResult.changed) {
    plugins.allow = allowResult.next;
    changed = true;
  }

  const denyResult = removeFromArray(plugins.deny, PLUGIN_IDS);
  if (denyResult.changed) {
    plugins.deny = denyResult.next;
    changed = true;
  }

  if (slots.memory && PLUGIN_IDS.includes(slots.memory)) {
    delete slots.memory;
    changed = true;
  }
  if (slots.contextEngine && PLUGIN_IDS.includes(slots.contextEngine)) {
    delete slots.contextEngine;
    changed = true;
  }

  const toolTargets = [
    "bamdra_memory_list_topics",
    "bamdra_memory_switch_topic",
    "bamdra_memory_save_fact",
    "bamdra_memory_compact_topic",
    "bamdra_memory_search",
    "bamdra_user_bind_get_my_profile",
    "bamdra_user_bind_update_my_profile",
    "bamdra_user_bind_refresh_my_binding",
    "bamdra_user_bind_admin_query",
    "bamdra_user_bind_admin_edit",
    "bamdra_user_bind_admin_merge",
    "bamdra_user_bind_admin_list_issues",
    "bamdra_user_bind_admin_sync",
    "bamdra_memory_vector_search",
    "memory_list_topics",
    "memory_switch_topic",
    "memory_save_fact",
    "memory_compact_topic",
    "memory_search",
    "user_bind_get_my_profile",
    "user_bind_update_my_profile",
    "user_bind_refresh_my_binding",
    "user_bind_admin_query",
    "user_bind_admin_edit",
    "user_bind_admin_merge",
    "user_bind_admin_list_issues",
    "user_bind_admin_sync",
    "memory_vector_search",
  ];
  const toolAllowResult = removeFromArray(tools.allow, toolTargets);
  if (toolAllowResult.changed) {
    tools.allow = toolAllowResult.next;
    changed = true;
  }

  return changed;
}

function moveIfExists(sourcePath, backupRoot) {
  if (!fs.existsSync(sourcePath)) {
    return null;
  }
  ensureDir(backupRoot);
  const targetPath = path.join(backupRoot, path.basename(sourcePath));
  fs.renameSync(sourcePath, targetPath);
  return { sourcePath, targetPath };
}

function restoreMoves(moves) {
  for (const move of moves.slice().reverse()) {
    if (!move) continue;
    if (fs.existsSync(move.targetPath)) {
      fs.renameSync(move.targetPath, move.sourcePath);
    }
  }
}

function runCommand(command, args) {
  const result = spawnSync(command, args, {
    stdio: "inherit",
    env: process.env,
  });
  if (result.status !== 0) {
    throw new Error(`${command} ${args.join(" ")} failed with exit code ${result.status ?? "unknown"}`);
  }
}

function restartGatewayIfNeeded(enabled) {
  if (!enabled) {
    log("next-step", {
      message: "Restart OpenClaw or the gateway so the refreshed plugin set is loaded.",
    });
    return;
  }
  runCommand("openclaw", ["gateway", "restart"]);
  log("gateway-restarted");
}

function main() {
  const options = parseArgs(process.argv.slice(2));
  const openclawHome = options.openclawHome;
  const configPath = path.join(openclawHome, "openclaw.json");
  const extensionsDir = path.join(openclawHome, "extensions");
  const skillsDir = path.join(openclawHome, "skills");

  if (!fs.existsSync(configPath)) {
    throw new Error(`OpenClaw config not found: ${configPath}`);
  }

  ensureDir(extensionsDir);
  ensureDir(skillsDir);

  const timestamp = new Date().toISOString().replace(/[:.]/g, "-");
  const backupRoot = path.join(openclawHome, "backups", `bamdra-memory-upgrade-${timestamp}`);
  ensureDir(backupRoot);

  const backupConfigPath = path.join(backupRoot, "openclaw.json.before");
  fs.copyFileSync(configPath, backupConfigPath);
  log("backup-created", { backupRoot, mode: options.mode });

  const moves = [];
  try {
    if (options.mode === "upgrade" || options.mode === "uninstall") {
      const config = readJson(configPath);
      sanitizeConfig(config);
      writeJson(configPath, config);
      log("config-sanitized", { configPath });
    }

    if (options.mode === "upgrade" || options.mode === "uninstall") {
      for (const pluginId of PLUGIN_IDS) {
        moves.push(moveIfExists(path.join(extensionsDir, pluginId), path.join(backupRoot, "extensions")));
      }
      for (const skillId of SKILL_IDS) {
        moves.push(moveIfExists(path.join(skillsDir, skillId), path.join(backupRoot, "skills")));
      }
      log("old-artifacts-moved");
    }

    if (options.mode === "install" || options.mode === "upgrade") {
      runCommand("openclaw", ["plugins", "install", options.packageSpec]);
      log("install-finished", { packageSpec: options.packageSpec, mode: options.mode });
      restartGatewayIfNeeded(options.restartGateway);
    } else {
      log("uninstall-complete", { backupRoot });
    }

    log("done", { backupRoot, mode: options.mode });
  } catch (error) {
    log("operation-failed-restoring", {
      message: error instanceof Error ? error.message : String(error),
    });
    fs.copyFileSync(backupConfigPath, configPath);
    restoreMoves(moves);
    throw error;
  }
}

try {
  main();
} catch (error) {
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
}
