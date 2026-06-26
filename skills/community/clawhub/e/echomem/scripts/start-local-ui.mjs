#!/usr/bin/env node
import { constants } from "node:fs";
import { access, readdir, readFile } from "node:fs/promises";
import { homedir } from "node:os";
import path from "node:path";
import { pathToFileURL } from "node:url";

function parseArgs(argv) {
  const args = {
    local: false,
    cloud: false,
    apiKey: "",
    memoryDir: "",
    openclawHome: "",
    pluginRoot: "",
    workspaceDir: "",
  };

  for (let index = 0; index < argv.length; index += 1) {
    const value = argv[index];
    if (value === "--local") {
      args.local = true;
      continue;
    }
    if (value === "--cloud") {
      args.cloud = true;
      continue;
    }
    if (value === "--api-key") {
      args.apiKey = argv[index + 1] || "";
      index += 1;
      continue;
    }
    if (value === "--memory-dir") {
      args.memoryDir = argv[index + 1] || "";
      index += 1;
      continue;
    }
    if (value === "--openclaw-home") {
      args.openclawHome = argv[index + 1] || "";
      index += 1;
      continue;
    }
    if (value === "--plugin-root") {
      args.pluginRoot = argv[index + 1] || "";
      index += 1;
      continue;
    }
    if (value === "--workspace-dir") {
      args.workspaceDir = argv[index + 1] || "";
      index += 1;
    }
  }

  return args;
}

async function ensureReadable(filePath) {
  await access(filePath, constants.R_OK);
}

async function importFromPlugin(pluginRoot, relativePath) {
  const absolutePath = path.join(pluginRoot, relativePath);
  await ensureReadable(absolutePath);
  return import(pathToFileURL(absolutePath).href);
}

function resolveOpenClawHome(args) {
  if (args.openclawHome) {
    return path.resolve(args.openclawHome);
  }
  const configPath = process.env.OPENCLAW_CONFIG_PATH?.trim();
  if (configPath) {
    return path.dirname(path.resolve(configPath));
  }
  return path.join(homedir(), ".openclaw");
}

async function manifestHasPluginId(candidateRoot, pluginId) {
  try {
    const raw = await readFile(path.join(candidateRoot, "openclaw.plugin.json"), "utf8");
    const manifest = JSON.parse(raw);
    return manifest?.id === pluginId;
  } catch {
    return false;
  }
}

async function resolvePluginRoot({ openclawHome, pluginRootArg }) {
  const pluginId = "echo-memory-cloud-openclaw-plugin";
  const packageNames = ["openclaw-memory", "echo-memory-cloud-openclaw-plugin"];
  const candidates = [];

  function pushCandidate(candidatePath) {
    if (!candidatePath) return;
    const resolved = path.resolve(candidatePath);
    if (!candidates.includes(resolved)) {
      candidates.push(resolved);
    }
  }

  pushCandidate(pluginRootArg);
  pushCandidate(process.env.ECHOMEM_PLUGIN_ROOT?.trim());
  pushCandidate(path.join(openclawHome, "extensions", pluginId));
  for (const packageName of packageNames) {
    pushCandidate(path.join(openclawHome, "node_modules", "@echomem", packageName));
  }

  try {
    const entries = await readdir(path.join(openclawHome, "extensions"), { withFileTypes: true });
    for (const entry of entries) {
      if (!entry.isDirectory()) continue;
      const candidateRoot = path.join(openclawHome, "extensions", entry.name);
      if (await manifestHasPluginId(candidateRoot, pluginId)) {
        pushCandidate(candidateRoot);
      }
    }
  } catch {
    // Ignore missing extensions directory.
  }

  for (const candidateRoot of candidates) {
    try {
      await ensureReadable(path.join(candidateRoot, "package.json"));
      return candidateRoot;
    } catch {
      // Try the next candidate.
    }
  }

  throw new Error(
    [
      "EchoMemory plugin was not found in the active OpenClaw install paths.",
      `Searched: ${candidates.join(", ")}`,
      "Install or link the plugin into OpenClaw first, or pass --plugin-root explicitly.",
    ].join("\n"),
  );
}

const args = parseArgs(process.argv.slice(2));
const openclawHome = resolveOpenClawHome(args);
let pluginRoot;
try {
  pluginRoot = await resolvePluginRoot({
    openclawHome,
    pluginRootArg: args.pluginRoot,
  });
} catch (error) {
  console.error(String(error?.message ?? error));
  process.exit(1);
}

const [{ buildConfig }, { createApiClient }, { startLocalServer }] = await Promise.all([
  importFromPlugin(pluginRoot, "lib/config.js"),
  importFromPlugin(pluginRoot, "lib/api-client.js"),
  importFromPlugin(pluginRoot, "lib/local-server.js"),
]);

const overrideConfig = {};
if (args.local) {
  overrideConfig.localOnlyMode = true;
}
if (args.cloud) {
  overrideConfig.localOnlyMode = false;
}
if (args.apiKey) {
  overrideConfig.apiKey = args.apiKey;
}
if (args.memoryDir) {
  overrideConfig.memoryDir = args.memoryDir;
}

const cfg = buildConfig(overrideConfig);
const client = !cfg.localOnlyMode && cfg.apiKey ? createApiClient(cfg) : null;
const workspaceDir = args.workspaceDir
  ? path.resolve(args.workspaceDir)
  : path.resolve(path.dirname(cfg.memoryDir), "..");

console.log("EchoMemory manual local UI startup");
console.log(`Mode: ${cfg.localOnlyMode ? "local" : "cloud"}`);
console.log(`OpenClaw home: ${openclawHome}`);
console.log(`Plugin root: ${pluginRoot}`);
console.log(`Memory dir: ${cfg.memoryDir}`);
console.log(`API key: ${cfg.apiKey ? `${cfg.apiKey.slice(0, 3)}...${cfg.apiKey.slice(-3)}` : "not set"}`);

const url = await startLocalServer(workspaceDir, {
  apiClient: client,
  cfg,
  syncRunner: null,
});

console.log(`Local workspace viewer: ${url}`);
