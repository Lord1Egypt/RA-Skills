#!/usr/bin/env node

import { execFileSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

const SKILL_KEY = "studio-agent";
const DEFAULT_CONFIG_PATH = "~/.openclaw/clawdbot.json";
const REQUIRED_ENV_KEYS = [
  "CZ_AGENT_WS_URL",
  "CZ_INSTANCE_ID",
  "CZ_INSTANCE_NAME",
  "CZ_PROJECT_ID",
  "CZ_WORKSPACE",
];
const BOOLEAN_ENV_KEYS = new Set(["CZ_AUTO_CREATE_CONVERSATION"]);
const URL_SCHEME_RE = /^[A-Za-z][A-Za-z0-9+.-]*:\/\//;
const LOCAL_WS_HOSTS = new Set(["localhost", "127.0.0.1", "::1", "0.0.0.0"]);

const TOP_LEVEL_ALIASES = {
  wsUrl: "CZ_AGENT_WS_URL",
  wsBaseUrl: "CZ_AGENT_WS_URL",
  baseUrl: "CZ_AGENT_WS_URL",
  url: "CZ_AGENT_WS_URL",
  token: "CZ_AGENT_TOKEN",
  userId: "CZ_USER_ID",
  tenantId: "CZ_TENANT_ID",
  instanceId: "CZ_INSTANCE_ID",
  instanceName: "CZ_INSTANCE_NAME",
  projectId: "CZ_PROJECT_ID",
  projectName: "CZ_PROJECT_NAME",
  workspace: "CZ_WORKSPACE",
  workspaceId: "CZ_WORKSPACE_ID",
  username: "CZ_USERNAME",
  sessionId: "CZ_SESSION_ID",
  conversationId: "CZ_CONVERSATION_ID",
  autoCreateConversation: "CZ_AUTO_CREATE_CONVERSATION",
  conversationTitle: "CZ_CONVERSATION_TITLE",
  requestTimeoutSeconds: "CZ_REQUEST_TIMEOUT_SECONDS",
  stopGraceSeconds: "CZ_STOP_GRACE_SECONDS",
  startupConnectTimeoutSeconds: "CZ_STARTUP_CONNECT_TIMEOUT_SECONDS",
  reconnectMaxAttempts: "CZ_RECONNECT_MAX_ATTEMPTS",
  alwaysAllowTools: "CZ_ALWAYS_ALLOW_TOOLS",
  interruptDecisionMode: "CZ_INTERRUPT_DECISION_MODE",
  emitAssistantDeltas: "CZ_EMIT_ASSISTANT_DELTAS",
};

const IDENTITY_ALIASES = {
  user_id: "CZ_USER_ID",
  tenant_id: "CZ_TENANT_ID",
  instance_id: "CZ_INSTANCE_ID",
  instance_name: "CZ_INSTANCE_NAME",
  project_id: "CZ_PROJECT_ID",
  project_name: "CZ_PROJECT_NAME",
  workspace: "CZ_WORKSPACE",
  workspace_id: "CZ_WORKSPACE_ID",
  username: "CZ_USERNAME",
  token: "CZ_AGENT_TOKEN",
  session_id: "CZ_SESSION_ID",
};

function usage() {
  return [
    "Studio Agent skill config manager",
    "",
    "Usage:",
    "  node skills/studio-agent/scripts/configure-skill.mjs template",
    "  node skills/studio-agent/scripts/configure-skill.mjs validate --input <file>",
    "  node skills/studio-agent/scripts/configure-skill.mjs apply --input <file> [--config <path>] [--restart] [--dry-run] [--replace]",
    "",
    "Options:",
    "  --input <file>            JSON input file",
    "  --json <json>             JSON input string",
    "  --config <path>           OpenClaw config file path (defaults to `openclaw config file` result)",
    "  --restart                 Run `openclaw gateway restart` after apply",
    "  --dry-run                 Preview changes without writing",
    "  --replace                 Replace skill env map instead of merge",
    "  --keep-cz-agent-token     Persist CZ_AGENT_TOKEN in env map (default: token stays in CZ_AGENT_WS_URL only)",
    "  -h, --help                Show help",
    "",
    "Input expectation (minimal):",
    "  wsUrl/baseUrl (host:port or ws URL), token, instanceId, instanceName, projectId, workspace",
    "  optional: alwaysAllowTools (comma-separated tool names)",
    "  optional: interruptDecisionMode (auto_approve|auto_reject|off), emitAssistantDeltas (true|false)",
    "  Script builds CZ_AGENT_WS_URL as: <base>/<path>?x-clickzetta-token=<token>&env=prod",
    "  default scheme policy when scheme missing: local -> ws://, remote -> wss://",
    "  default path policy when path missing: local -> /ws, remote -> /ai",
  ].join("\n");
}

function isRecord(value) {
  return Boolean(value) && typeof value === "object" && !Array.isArray(value);
}

function asString(value) {
  if (value === undefined || value === null) {
    return undefined;
  }
  if (typeof value === "boolean") {
    return value ? "true" : "false";
  }
  const text = String(value).trim();
  return text ? text : undefined;
}

function parseBooleanEnv(value) {
  const text = asString(value);
  if (!text) {
    return undefined;
  }
  const normalized = text.toLowerCase();
  if (["1", "true", "yes", "on"].includes(normalized)) {
    return "true";
  }
  if (["0", "false", "no", "off"].includes(normalized)) {
    return "false";
  }
  return undefined;
}

function setEnvValue(target, key, value) {
  if (!key) {
    return;
  }
  if (BOOLEAN_ENV_KEYS.has(key)) {
    const parsed = parseBooleanEnv(value);
    if (parsed !== undefined) {
      target[key] = parsed;
      return;
    }
  }
  const text = asString(value);
  if (text !== undefined) {
    target[key] = text;
  }
}

function parseArgs(argv) {
  const args = [...argv];
  let command = "apply";
  if (args[0] && !args[0].startsWith("-")) {
    command = args.shift();
  }
  const opts = {
    inputPath: undefined,
    jsonInput: undefined,
    configPath: undefined,
    restart: false,
    dryRun: false,
    replace: false,
    keepTokenEnv: false,
  };

  while (args.length > 0) {
    const arg = args.shift();
    if (!arg) {
      continue;
    }
    if (arg === "-h" || arg === "--help") {
      return { command, opts, help: true };
    }
    if (arg === "--restart") {
      opts.restart = true;
      continue;
    }
    if (arg === "--dry-run") {
      opts.dryRun = true;
      continue;
    }
    if (arg === "--replace") {
      opts.replace = true;
      continue;
    }
    if (arg === "--keep-cz-agent-token") {
      opts.keepTokenEnv = true;
      continue;
    }
    if (arg === "--input") {
      opts.inputPath = args.shift();
      if (!opts.inputPath) {
        throw new Error("--input requires a file path");
      }
      continue;
    }
    if (arg === "--json") {
      opts.jsonInput = args.shift();
      if (!opts.jsonInput) {
        throw new Error("--json requires a JSON string");
      }
      continue;
    }
    if (arg === "--config") {
      opts.configPath = args.shift();
      if (!opts.configPath) {
        throw new Error("--config requires a file path");
      }
      continue;
    }
    throw new Error(`Unknown argument: ${arg}`);
  }

  return { command, opts, help: false };
}

function readJsonFile(filePath) {
  const text = fs.readFileSync(filePath, "utf8");
  const parsed = JSON.parse(text);
  if (!isRecord(parsed)) {
    throw new Error(`JSON root must be an object: ${filePath}`);
  }
  return parsed;
}

function parseJsonInput(text) {
  const parsed = JSON.parse(text);
  if (!isRecord(parsed)) {
    throw new Error("JSON input root must be an object");
  }
  return parsed;
}

function extractTokenFromWsUrl(wsUrl) {
  const urlText = asString(wsUrl);
  if (!urlText) {
    return undefined;
  }
  try {
    const url = new URL(urlText);
    return asString(url.searchParams.get("x-clickzetta-token"));
  } catch {
    return undefined;
  }
}

function parseTokenClaims(rawToken) {
  const token = asString(rawToken);
  if (!token) {
    return undefined;
  }
  const parts = token.split(".");
  if (parts.length < 2) {
    return undefined;
  }
  try {
    const payload = Buffer.from(parts[1], "base64url").toString("utf8");
    const parsed = JSON.parse(payload);
    return isRecord(parsed) ? parsed : undefined;
  } catch {
    return undefined;
  }
}

function normalizeWsBaseUrl(rawUrl) {
  const text = asString(rawUrl);
  if (!text) {
    return undefined;
  }
  const hasExplicitScheme = URL_SCHEME_RE.test(text);
  const withScheme = hasExplicitScheme ? text : `ws://${text}`;
  try {
    const parsed = new URL(withScheme);
    if (!parsed.hostname) {
      return undefined;
    }
    if (hasExplicitScheme) {
      if (parsed.protocol === "https:") {
        parsed.protocol = "wss:";
      } else if (parsed.protocol === "http:") {
        parsed.protocol = "ws:";
      } else {
        parsed.protocol = parsed.protocol === "wss:" ? "wss:" : "ws:";
      }
    } else {
      parsed.protocol = isLocalWsHost(parsed.hostname) ? "ws:" : "wss:";
    }
    parsed.username = "";
    parsed.password = "";
    return parsed;
  } catch {
    return undefined;
  }
}

function isLocalWsHost(hostname) {
  const normalized = asString(hostname)?.toLowerCase();
  if (!normalized) {
    return false;
  }
  return LOCAL_WS_HOSTS.has(normalized);
}

function buildStudioWsUrl(baseUrl, token) {
  const parsed = normalizeWsBaseUrl(baseUrl);
  const tokenText = asString(token);
  if (!parsed || !tokenText) {
    return undefined;
  }

  // Keep explicit path from user input. Only auto-select when path is missing/root.
  if (!parsed.pathname || parsed.pathname === "/") {
    parsed.pathname = isLocalWsHost(parsed.hostname) ? "/ws" : "/ai";
  }

  if (!parsed.searchParams.has("env")) {
    parsed.searchParams.set("env", "prod");
  } else {
    // Skill convention: normalize env to prod.
    parsed.searchParams.set("env", "prod");
  }
  parsed.searchParams.set("x-clickzetta-token", tokenText);
  return parsed.toString();
}

function injectTokenIntoWsUrl(wsUrl, token) {
  const wsText = asString(wsUrl);
  const tokenText = asString(token);
  if (!wsText || !tokenText) {
    return wsText;
  }
  try {
    const parsed = new URL(wsText);
    parsed.searchParams.set("x-clickzetta-token", tokenText);
    return parsed.toString();
  } catch {
    return wsText;
  }
}

function normalizeInput(raw, opts) {
  const env = {};
  const notes = [];

  if (isRecord(raw.env)) {
    for (const [key, value] of Object.entries(raw.env)) {
      if (!key.startsWith("CZ_")) {
        continue;
      }
      setEnvValue(env, key, value);
    }
  }

  for (const [key, value] of Object.entries(raw)) {
    if (key === "env" || key === "identity") {
      continue;
    }
    if (key.startsWith("CZ_")) {
      setEnvValue(env, key, value);
      continue;
    }
    const mapped = TOP_LEVEL_ALIASES[key];
    if (mapped) {
      setEnvValue(env, mapped, value);
    }
  }

  if (isRecord(raw.identity)) {
    for (const [key, value] of Object.entries(raw.identity)) {
      const mapped = IDENTITY_ALIASES[key];
      if (mapped) {
        setEnvValue(env, mapped, value);
      }
    }
  }

  const rawBaseUrl =
    asString(raw.wsUrl) ??
    asString(raw.wsBaseUrl) ??
    asString(raw.baseUrl) ??
    asString(raw.url) ??
    asString(env.CZ_AGENT_WS_URL);
  const tokenFromInput =
    asString(raw.token) ??
    asString(raw.wsToken) ??
    asString(raw.cztToken) ??
    asString(env.CZ_AGENT_TOKEN) ??
    asString(raw?.identity?.token);
  const tokenFromWsUrl = extractTokenFromWsUrl(rawBaseUrl);
  const resolvedToken = tokenFromInput ?? tokenFromWsUrl;

  if (rawBaseUrl && resolvedToken) {
    const rebuilt = buildStudioWsUrl(rawBaseUrl, resolvedToken);
    if (rebuilt) {
      env.CZ_AGENT_WS_URL = rebuilt;
      notes.push(
        "Built CZ_AGENT_WS_URL from input URL + token with env=prod (path kept; default local /ws, remote /ai when missing).",
      );
    }
  } else if (env.CZ_AGENT_WS_URL && resolvedToken) {
    const merged = injectTokenIntoWsUrl(env.CZ_AGENT_WS_URL, resolvedToken);
    if (merged) {
      env.CZ_AGENT_WS_URL = merged;
      notes.push("Token merged into existing CZ_AGENT_WS_URL query param x-clickzetta-token.");
    }
  }

  if (resolvedToken) {
    env.CZ_AGENT_TOKEN = resolvedToken;
  }

  if (!opts.keepTokenEnv && env.CZ_AGENT_TOKEN) {
    delete env.CZ_AGENT_TOKEN;
    notes.push("Dropped CZ_AGENT_TOKEN (default behavior).");
  }

  return { env, notes };
}

function validateEnv(env) {
  const errors = [];
  const warnings = [];
  let tokenClaims;

  for (const key of REQUIRED_ENV_KEYS) {
    if (!asString(env[key])) {
      errors.push(`Missing required field: ${key}`);
    }
  }

  const wsUrl = asString(env.CZ_AGENT_WS_URL);
  if (wsUrl) {
    try {
      const parsed = new URL(wsUrl);
      if (parsed.protocol !== "ws:" && parsed.protocol !== "wss:") {
        errors.push("CZ_AGENT_WS_URL must start with ws:// or wss://");
      }
      const isLocal = isLocalWsHost(parsed.hostname);
      if (isLocal && parsed.pathname !== "/ws") {
        warnings.push("Local CZ_AGENT_WS_URL usually uses /ws.");
      }
      if (!isLocal && parsed.pathname !== "/ai") {
        warnings.push("Remote CZ_AGENT_WS_URL usually uses /ai.");
      }
      const envValue = asString(parsed.searchParams.get("env"));
      if (envValue !== "prod") {
        warnings.push("CZ_AGENT_WS_URL query param env is not prod; this skill expects env=prod.");
      }
      const token = asString(parsed.searchParams.get("x-clickzetta-token"));
      if (!token) {
        errors.push("CZ_AGENT_WS_URL missing x-clickzetta-token query param (token is required).");
      } else {
        tokenClaims = parseTokenClaims(token);
      }
    } catch {
      errors.push("CZ_AGENT_WS_URL is not a valid URL");
    }
  }

  const envUserId = asString(env.CZ_USER_ID);
  const envTenantId = asString(env.CZ_TENANT_ID);
  const claimUserId = asString(tokenClaims?.userId) ?? asString(tokenClaims?.user_id);
  const claimTenantId =
    asString(tokenClaims?.tenantId) ??
    asString(tokenClaims?.tenant_id) ??
    asString(tokenClaims?.accountId) ??
    asString(tokenClaims?.account_id);

  if (!envUserId && !claimUserId) {
    warnings.push(
      "Could not infer user identity from token. If runtime reports missing user_id, provide userId explicitly.",
    );
  }
  if (!envTenantId && !claimTenantId) {
    warnings.push(
      "Could not infer tenant identity from token. If runtime reports missing tenant_id, provide tenantId explicitly.",
    );
  }

  return { errors, warnings };
}

function expandHome(inputPath) {
  if (!inputPath) {
    return inputPath;
  }
  if (inputPath.startsWith("~/")) {
    return path.join(os.homedir(), inputPath.slice(2));
  }
  return inputPath;
}

function resolveConfigPath(configPathArg) {
  if (configPathArg) {
    return path.resolve(expandHome(configPathArg));
  }
  try {
    const output = execFileSync("openclaw", ["config", "file"], {
      encoding: "utf8",
      stdio: ["ignore", "pipe", "pipe"],
    });
    const lines = output
      .split(/\r?\n/)
      .map((line) => line.trim())
      .filter(Boolean);
    for (let i = lines.length - 1; i >= 0; i -= 1) {
      const line = lines[i];
      if (line.endsWith(".json")) {
        return path.resolve(expandHome(line));
      }
      const match = line.match(/(~?\/[^\s]+\.json)$/);
      if (match?.[1]) {
        return path.resolve(expandHome(match[1]));
      }
    }
  } catch {
    // ignore and use fallback
  }
  return path.resolve(expandHome(DEFAULT_CONFIG_PATH));
}

function ensureObject(parent, key) {
  const current = parent[key];
  if (isRecord(current)) {
    return current;
  }
  const next = {};
  parent[key] = next;
  return next;
}

function getSkillEnvRef(config) {
  const skills = ensureObject(config, "skills");
  const entries = ensureObject(skills, "entries");
  const skill = ensureObject(entries, SKILL_KEY);
  return ensureObject(skill, "env");
}

function diffKeys(before, after) {
  const added = [];
  const updated = [];
  const removed = [];
  const beforeKeys = new Set(Object.keys(before));
  const afterKeys = new Set(Object.keys(after));

  for (const key of afterKeys) {
    if (!beforeKeys.has(key)) {
      added.push(key);
      continue;
    }
    if (before[key] !== after[key]) {
      updated.push(key);
    }
  }
  for (const key of beforeKeys) {
    if (!afterKeys.has(key)) {
      removed.push(key);
    }
  }

  return { added, updated, removed };
}

function loadInputOrThrow(opts) {
  if (opts.jsonInput) {
    return parseJsonInput(opts.jsonInput);
  }
  if (opts.inputPath) {
    return readJsonFile(path.resolve(expandHome(opts.inputPath)));
  }
  throw new Error("Missing input. Pass --input <file> or --json <json>.");
}

function buildTemplate() {
  return {
    wsUrl: "localhost:8000",
    token: "<PASTE_TOKEN>",
    instanceId: "32",
    instanceName: "tmwmzxzs",
    projectId: "718955",
    workspace: "cxx_test_new_2",
  };
}

function printValidationResult(label, normalized, checks) {
  console.error(`\n[${label}]`);
  if (normalized.notes.length > 0) {
    for (const note of normalized.notes) {
      console.error(`- note: ${note}`);
    }
  }
  if (checks.warnings.length > 0) {
    for (const warning of checks.warnings) {
      console.error(`- warning: ${warning}`);
    }
  }
  if (checks.errors.length > 0) {
    for (const error of checks.errors) {
      console.error(`- error: ${error}`);
    }
  }
  console.error(`- env keys: ${Object.keys(normalized.env).sort().join(", ")}`);
}

function runRestart() {
  execFileSync("openclaw", ["gateway", "restart"], { stdio: "inherit" });
}

function main() {
  const { command, opts, help } = parseArgs(process.argv.slice(2));
  if (help) {
    console.log(usage());
    return;
  }

  if (command === "template") {
    console.log(`${JSON.stringify(buildTemplate(), null, 2)}\n`);
    return;
  }

  if (command !== "validate" && command !== "apply") {
    throw new Error(`Unknown command: ${command}`);
  }

  const input = loadInputOrThrow(opts);
  const normalized = normalizeInput(input, opts);
  const checks = validateEnv(normalized.env);
  printValidationResult(command, normalized, checks);
  if (checks.errors.length > 0) {
    process.exitCode = 1;
    return;
  }

  if (command === "validate") {
    console.log(`${JSON.stringify({ env: normalized.env }, null, 2)}\n`);
    return;
  }

  const configPath = resolveConfigPath(opts.configPath);
  let config = {};
  if (fs.existsSync(configPath)) {
    const parsed = JSON.parse(fs.readFileSync(configPath, "utf8"));
    if (!isRecord(parsed)) {
      throw new Error(`Config root must be an object: ${configPath}`);
    }
    config = parsed;
  }

  const envRef = getSkillEnvRef(config);
  const before = { ...envRef };
  const next = opts.replace ? { ...normalized.env } : { ...before, ...normalized.env };
  if (!opts.keepTokenEnv && next.CZ_AGENT_TOKEN) {
    delete next.CZ_AGENT_TOKEN;
  }

  const diff = diffKeys(before, next);
  config.skills.entries[SKILL_KEY].env = next;

  if (opts.dryRun) {
    console.error(`\n[dry-run] target config: ${configPath}`);
    console.error(`- added: ${diff.added.join(", ") || "(none)"}`);
    console.error(`- updated: ${diff.updated.join(", ") || "(none)"}`);
    console.error(`- removed: ${diff.removed.join(", ") || "(none)"}`);
    console.log(`${JSON.stringify({ env: next }, null, 2)}\n`);
    return;
  }

  fs.mkdirSync(path.dirname(configPath), { recursive: true });
  fs.writeFileSync(configPath, `${JSON.stringify(config, null, 2)}\n`, "utf8");

  console.error(`\nApplied ${SKILL_KEY} env config to: ${configPath}`);
  console.error(`- added: ${diff.added.join(", ") || "(none)"}`);
  console.error(`- updated: ${diff.updated.join(", ") || "(none)"}`);
  console.error(`- removed: ${diff.removed.join(", ") || "(none)"}`);
  console.log(`${JSON.stringify({ env: next }, null, 2)}\n`);

  if (opts.restart) {
    runRestart();
  } else {
    console.error("Tip: run `openclaw gateway restart` to apply immediately.");
  }
}

try {
  main();
} catch (error) {
  console.error(error instanceof Error ? error.message : String(error));
  console.error(`\n${usage()}`);
  process.exitCode = 1;
}
