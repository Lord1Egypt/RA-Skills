#!/usr/bin/env node
import { readFile } from "node:fs/promises";
import { homedir } from "node:os";
import { join, resolve } from "node:path";
import { pathToFileURL } from "node:url";

export function parseBridgeUrl(raw = process.env.EASY_WEBBRIDGE_URL || "http://127.0.0.1:17777") {
  let parsed;
  try {
    parsed = new URL(raw);
  } catch {
    throw new Error("EASY_WEBBRIDGE_URL must be an HTTP loopback URL");
  }
  const loopbackHosts = new Set(["127.0.0.1", "[::1]"]);
  if (parsed.protocol !== "http:" || !loopbackHosts.has(parsed.hostname)
    || parsed.username || parsed.password || parsed.pathname !== "/" || parsed.search || parsed.hash) {
    throw new Error("EASY_WEBBRIDGE_URL must use HTTP loopback 127.0.0.1 or [::1], without credentials, path, query, or fragment");
  }
  return parsed.origin;
}

// Validate the target before any token file or environment credential is read.
const baseUrl = parseBridgeUrl();

async function token() {
  if (process.env.EASY_WEBBRIDGE_TOKEN) return process.env.EASY_WEBBRIDGE_TOKEN;
  try {
    const value = (await readFile(join(homedir(), ".easy-webbridge", "bridge-token"), "utf8")).trim();
    if (value) return value;
  } catch {}
  throw new Error("Bridge token is unavailable; connect the local Bridge before using authenticated commands");
}

async function request(path, init = {}, authenticated = true) {
  const url = new URL(path, baseUrl);
  if (url.origin !== baseUrl) throw new Error("Refusing a request outside the local Bridge origin");
  const headers = { "Content-Type": "application/json", ...(init.headers || {}) };
  if (authenticated) headers.Authorization = `Bearer ${await token()}`;
  const response = await fetch(url, { ...init, headers, redirect: "error" });
  if (!response.ok) throw new Error(`Bridge request failed (HTTP ${response.status})`);
  try {
    return await response.json();
  } catch {
    throw new Error("Bridge returned an invalid JSON response");
  }
}

async function health() {
  try {
    return await request("/health", {}, false);
  } catch {
    return null;
  }
}

function usage() {
  console.error(`Usage:
  easy-webbridge list
  easy-webbridge status
  easy-webbridge command <browserId> <action> [args-json]
  easy-webbridge navigate <browserId> <url> [--new-tab] [--session <name>] [--group-title <title>] [--ungrouped]
  easy-webbridge snapshot <browserId> [tabId] [--frame-id <id>] [--compact] [--visibility visible|hidden|all] [--scope <css>] [--region viewport|x,y,width,height] [--max-elements <n>] [--offset <n>] [--text <query>] [--role <role>] [--text-mode page|matched|none] [--max-text-length <n>] [--max-bytes <n>]
  easy-webbridge click <browserId> <selector> [tabId] [--frame-id <id>] [--mode dom|native]
  easy-webbridge fill <browserId> <selector> <value> [tabId] [--frame-id <id>]
  easy-webbridge wait <browserId> [tabId] (--selector <css>|--text <text>|--url <part>) [--state attached|detached|visible|hidden] [--timeout-ms <n>] [--frame-id <id>]
  easy-webbridge batch <browserId> <actions-json> [tabId]
  easy-webbridge press-key <browserId> <key> [tabId]
  easy-webbridge key-combo <browserId> <keys-json> [tabId]
  easy-webbridge environment-info <browserId> [tabId]
  easy-webbridge capabilities <browserId>
  easy-webbridge screenshot <browserId> [tabId]`);
}

function snapshotArgs(args) {
  const [browserId, ...tokens] = args;
  if (!browserId) throw new Error("browserId is required");
  const options = {};
  if (tokens[0] && !tokens[0].startsWith("--")) {
    const tabId = Number(tokens.shift());
    if (!Number.isSafeInteger(tabId)) throw new Error("tabId must be an integer");
    options.tabId = tabId;
  }
  const repeated = { "--text": "text", "--role": "roles" };
  const scalar = {
    "--visibility": "visibility",
    "--scope": "scopeSelector",
    "--max-elements": "maxElements",
    "--offset": "offset",
    "--text-mode": "textMode",
    "--max-text-length": "maxTextLength",
    "--max-bytes": "maxBytes",
    "--frame-id": "frameId",
  };
  while (tokens.length) {
    const flag = tokens.shift();
    if (flag === "--compact") {
      options.compact = true;
      continue;
    }
    if (flag === "--include-hidden") {
      options.visibility = "all";
      continue;
    }
    const value = tokens.shift();
    if (value === undefined || value.startsWith("--")) throw new Error(`${flag} requires a value`);
    if (flag === "--region") {
      if (value === "viewport") options.region = "viewport";
      else {
        const values = value.split(",").map(Number);
        if (values.length !== 4 || !values.every(Number.isFinite)) throw new Error("--region requires viewport or x,y,width,height");
        options.region = { x: values[0], y: values[1], width: values[2], height: values[3] };
      }
    } else if (repeated[flag]) {
      (options[repeated[flag]] ||= []).push(value);
    } else if (scalar[flag]) {
      options[scalar[flag]] = ["maxElements", "offset", "maxTextLength", "maxBytes", "frameId"].includes(scalar[flag]) ? Number(value) : value;
    } else {
      throw new Error(`Unknown snapshot option: ${flag}`);
    }
  }
  return { browserId, options };
}

function actionArgs(tokens, positionalCount, flags = {}) {
  const result = {};
  let index = 0;
  if (positionalCount && tokens[0] && !tokens[0].startsWith("--")) {
    const tabId = Number(tokens[0]);
    if (!Number.isSafeInteger(tabId)) throw new Error("tabId must be an integer");
    result.tabId = tabId;
    index = 1;
  }
  for (; index < tokens.length; index += 1) {
    const flag = tokens[index];
    const key = flags[flag];
    if (!key) throw new Error(`Unknown option: ${flag}`);
    const value = tokens[++index];
    if (value == null || value.startsWith("--")) throw new Error(`${flag} requires a value`);
    result[key] = key === "frameId" || key === "timeoutMs" ? Number(value) : value;
  }
  return result;
}

function navigateArgs(url, flags) {
  validateWebUrl(url);
  const options = { url, newTab: flags.includes("--new-tab") };
  const valueAfter = (name) => {
    const index = flags.indexOf(name);
    if (index < 0) return null;
    const value = flags[index + 1];
    if (!value || value.startsWith("--")) throw new Error(`${name} requires a value`);
    return value;
  };
  const requestedSession = valueAfter("--session");
  const requestedTitle = valueAfter("--group-title");
  if (options.newTab && !flags.includes("--ungrouped")) {
    const hostname = new URL(url).hostname;
    options.session = (requestedSession || `easy-webbridge:${hostname}`).slice(0, 120);
    options.groupTitle = (requestedTitle || hostname).slice(0, 80);
  } else if (requestedSession) {
    options.session = requestedSession;
    if (requestedTitle) options.groupTitle = requestedTitle;
  }
  return options;
}

const SAFE_ACTIONS = new Set([
  "list_tabs", "find_tab", "activate_tab", "close_tab", "close_session", "navigate",
  "snapshot", "list_frames", "wait_for", "capabilities", "click", "fill", "scroll",
  "screenshot", "upload", "save_as_pdf", "batch", "press_key", "key_combo",
  "environment_info", "browser_profile",
]);

function validateWebUrl(value) {
  let url;
  try { url = new URL(value); } catch { throw new Error("Target URL must be a valid HTTP(S) URL"); }
  if (!["http:", "https:"].includes(url.protocol) || !url.hostname || url.username || url.password) {
    throw new Error("Target URL must use HTTP(S) and must not include credentials");
  }
}

export function isAbsoluteUploadPath(value) {
  return typeof value === "string" && (value.startsWith("/") || /^[A-Za-z]:[\\/]/.test(value) || /^\\\\[^\\]+\\[^\\]+/.test(value));
}

function validateAction(action, args) {
  if (!SAFE_ACTIONS.has(action)) throw new Error(`Action is not available in this Skill CLI: ${action}`);
  if (action === "navigate") validateWebUrl(args.url);
  if (action === "batch") {
    if (!Array.isArray(args.actions) || args.actions.length < 1 || args.actions.length > 20) {
      throw new Error("batch requires 1 to 20 actions");
    }
    const batchActions = new Set(["click", "fill", "scroll", "wait_for", "press_key", "key_combo"]);
    for (const step of args.actions) {
      if (!step || typeof step !== "object" || Array.isArray(step) || !batchActions.has(step.action)) {
        throw new Error("batch contains an unsupported action");
      }
    }
  }
  if (action === "upload") {
    if (!args.selector || !Array.isArray(args.files) || !args.files.length || args.files.some((file) => !isAbsoluteUploadPath(file))) {
      throw new Error("upload requires a selector and absolute file paths");
    }
  }
}

async function command(browserId, action, args = {}, timeoutMs = 15_000) {
  if (!browserId || typeof browserId !== "string") throw new Error("browserId is required");
  if (!args || typeof args !== "object" || Array.isArray(args)) throw new Error("command args must be an object");
  validateAction(action, args);
  return request(`/v1/browsers/${encodeURIComponent(browserId)}/commands`, {
    method: "POST",
    body: JSON.stringify({ action, args, timeoutMs }),
  });
}

async function main() {
  const [verb, ...args] = process.argv.slice(2);
  let result;
  if (verb === "list") {
    result = await request("/v1/browsers");
  } else if (verb === "status") {
    result = await health() || { ok: false, service: "easy-webbridge", online: false, url: baseUrl };
  } else if (verb === "command") {
    const [browserId, action, argsJson = "{}"] = args;
    if (!browserId || !action) throw new Error("browserId and action are required");
    result = await command(browserId, action, JSON.parse(argsJson));
  } else if (verb === "navigate") {
    const [browserId, url, ...flags] = args;
    if (!browserId || !url) throw new Error("browserId and url are required");
    result = await command(browserId, "navigate", navigateArgs(url, flags));
  } else if (verb === "snapshot") {
    const parsed = snapshotArgs(args);
    result = await command(parsed.browserId, "snapshot", parsed.options);
  } else if (verb === "screenshot") {
    const [browserId, tabId] = args;
    if (!browserId) throw new Error("browserId is required");
    result = await command(browserId, verb, tabId ? { tabId: Number(tabId) } : {});
  } else if (verb === "click") {
    const [browserId, selector, ...tail] = args;
    if (!browserId || !selector) throw new Error("browserId and selector are required");
    result = await command(browserId, "click", { selector, ...actionArgs(tail, 1, { "--frame-id": "frameId", "--mode": "mode" }) });
  } else if (verb === "fill") {
    const [browserId, selector, value, ...tail] = args;
    if (!browserId || !selector || value == null) throw new Error("browserId, selector and value are required");
    result = await command(browserId, "fill", { selector, value, ...actionArgs(tail, 1, { "--frame-id": "frameId" }) });
  } else if (verb === "wait") {
    const [browserId, ...tail] = args;
    if (!browserId) throw new Error("browserId is required");
    const options = actionArgs(tail, 1, { "--frame-id": "frameId", "--selector": "selector", "--text": "text", "--url": "url", "--state": "state", "--timeout-ms": "timeoutMs" });
    result = await command(browserId, "wait_for", options, Math.min(120_000, (options.timeoutMs || 10_000) + 2_000));
  } else if (verb === "batch") {
    const [browserId, actionsJson, tabId] = args;
    if (!browserId || !actionsJson) throw new Error("browserId and actions-json are required");
    const options = JSON.parse(actionsJson);
    if (tabId != null) options.tabId = Number(tabId);
    result = await command(browserId, "batch", options, Math.min(120_000, Number(options.maxDurationMs || 30_000) + 2_000));
  } else if (verb === "press-key") {
    const [browserId, key, tabId] = args;
    if (!browserId || !key) throw new Error("browserId and key are required");
    result = await command(browserId, "press_key", { key, ...(tabId == null ? {} : { tabId: Number(tabId) }) });
  } else if (verb === "key-combo") {
    const [browserId, keysJson, tabId] = args;
    if (!browserId || !keysJson) throw new Error("browserId and keys-json are required");
    result = await command(browserId, "key_combo", { keys: JSON.parse(keysJson), ...(tabId == null ? {} : { tabId: Number(tabId) }) });
  } else if (verb === "environment-info") {
    const [browserId, tabId] = args;
    if (!browserId) throw new Error("browserId is required");
    result = await command(browserId, "environment_info", tabId == null ? {} : { tabId: Number(tabId) });
  } else if (verb === "capabilities") {
    const [browserId] = args;
    if (!browserId) throw new Error("browserId is required");
    result = await command(browserId, "capabilities", {});
  } else {
    usage();
    process.exitCode = 2;
    return;
  }
  const output = JSON.stringify(result, null, 2);
  if (Buffer.byteLength(output, "utf8") > 1_000_000) throw new Error("Bridge response is too large; request a narrower snapshot");
  console.log(output);
}

if (process.argv[1] && pathToFileURL(resolve(process.argv[1])).href === import.meta.url) {
  main().catch((error) => {
    console.error(JSON.stringify({ ok: false, error: error.message }, null, 2));
    process.exit(1);
  });
}
