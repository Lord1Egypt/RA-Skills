#!/usr/bin/env node

import { readFile } from "node:fs/promises";
import { homedir } from "node:os";
import { isAbsolute, join } from "node:path";

const baseUrl = process.env.EASY_WEBBRIDGE_URL || "http://127.0.0.1:17777";
const runtimeRepository = "https://github.com/xxjrq/easy-webbridge";

function print(value) {
  console.log(JSON.stringify(value, null, 2));
}

function setupSteps() {
  return [
    `Install Easy WebBridge once: ${runtimeRepository}`,
    "Start the local bridge, then load its extension in the Chromium profile that is already logged in.",
    "Run this preflight command again.",
  ];
}

function fail(code, message, extra = {}) {
  print({ ok: false, code, message, ...extra });
  process.exit(1);
}

async function readToken() {
  if (process.env.EASY_WEBBRIDGE_TOKEN) return process.env.EASY_WEBBRIDGE_TOKEN;
  try {
    return (await readFile(join(homedir(), ".easy-webbridge", "bridge-token"), "utf8")).trim();
  } catch {
    fail("token-not-found", "Easy WebBridge token was not found.", { next: setupSteps() });
  }
}

async function health() {
  try {
    const response = await fetch(`${baseUrl}/health`);
    return response.ok ? await response.json() : null;
  } catch {
    return null;
  }
}

async function request(path, init = {}) {
  const response = await fetch(`${baseUrl}${path}`, {
    ...init,
    headers: {
      Authorization: `Bearer ${await readToken()}`,
      "Content-Type": "application/json",
      ...(init.headers || {}),
    },
  });
  const body = await response.json().catch(() => ({}));
  if (!response.ok) fail("bridge-request-failed", body.error || `HTTP ${response.status}`);
  return body;
}

async function command(browserId, action, args = {}) {
  return request(`/v1/browsers/${encodeURIComponent(browserId)}/commands`, {
    method: "POST",
    body: JSON.stringify({ action, args }),
  });
}

function valueAfter(flags, name) {
  const index = flags.indexOf(name);
  if (index < 0) return null;
  const value = flags[index + 1];
  if (!value || value.startsWith("--")) fail("invalid-arguments", `${name} requires a value.`);
  return value;
}

function parseTabId(value) {
  if (value == null) return undefined;
  if (!/^\d+$/.test(value) || Number(value) <= 0 || !Number.isSafeInteger(Number(value))) {
    fail("invalid-arguments", `tabId must be a positive safe integer; received ${value}.`);
  }
  return Number(value);
}

function parseCommandArgs(value) {
  let parsed;
  try {
    parsed = JSON.parse(value);
  } catch {
    fail("invalid-arguments", "args-json must contain valid JSON.");
  }
  if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) {
    fail("invalid-arguments", "args-json must be a JSON object.");
  }
  return parsed;
}

function usage() {
  console.error(`Usage:
  node scripts/easy-webbridge-client.mjs preflight
  node scripts/easy-webbridge-client.mjs list
  node scripts/easy-webbridge-client.mjs navigate <browserId> <url> [--new-tab] [--session <name>] [--group-title <title>]
  node scripts/easy-webbridge-client.mjs snapshot <browserId> [tabId]
  node scripts/easy-webbridge-client.mjs click <browserId> <selector> [tabId]
  node scripts/easy-webbridge-client.mjs fill <browserId> <selector> <value> [tabId]
  node scripts/easy-webbridge-client.mjs upload <browserId> <selector> <absolute-file> [absolute-file...]
  node scripts/easy-webbridge-client.mjs screenshot <browserId> [tabId]
  node scripts/easy-webbridge-client.mjs close-session <browserId> <session>
  node scripts/easy-webbridge-client.mjs command <browserId> <action> [args-json]`);
}

async function preflight() {
  const major = Number(process.versions.node.split(".")[0]);
  if (major < 20) fail("node-version", `Node.js 20+ is required; found ${process.version}.`);
  const status = await health();
  if (!status?.ok || status.service !== "easy-webbridge") {
    fail("runtime-unavailable", `Easy WebBridge is not running at ${baseUrl}.`, { next: setupSteps() });
  }
  const result = await request("/v1/browsers");
  const browsers = (result.browsers || []).filter((browser) => browser.online).map((browser) => ({
    browserId: browser.browserId,
    name: browser.displayName || browser.name || browser.browserId,
    platform: browser.platform || null,
    version: browser.version || null,
  }));
  if (browsers.length === 0) {
    fail("browser-offline", "Easy WebBridge is running, but no browser extension is online.", { next: setupSteps() });
  }
  return { ok: true, runtime: { url: baseUrl, service: status.service }, browsers };
}

async function main() {
  const [verb, ...args] = process.argv.slice(2);
  let result;
  if (verb === "preflight") {
    result = await preflight();
  } else if (verb === "list") {
    result = await request("/v1/browsers");
  } else if (verb === "navigate") {
    const [browserId, url, ...flags] = args;
    if (!browserId || !url) fail("invalid-arguments", "browserId and url are required.");
    const session = valueAfter(flags, "--session");
    const groupTitle = valueAfter(flags, "--group-title");
    result = await command(browserId, "navigate", {
      url,
      newTab: flags.includes("--new-tab"),
      ...(session ? { session } : {}),
      ...(groupTitle ? { groupTitle } : {}),
    });
  } else if (["snapshot", "screenshot"].includes(verb)) {
    const [browserId, tabId] = args;
    if (!browserId) fail("invalid-arguments", "browserId is required.");
    const parsedTabId = parseTabId(tabId);
    result = await command(browserId, verb, parsedTabId ? { tabId: parsedTabId } : {});
  } else if (verb === "click") {
    const [browserId, selector, tabId] = args;
    if (!browserId || !selector) fail("invalid-arguments", "browserId and selector are required.");
    const parsedTabId = parseTabId(tabId);
    result = await command(browserId, "click", { selector, ...(parsedTabId ? { tabId: parsedTabId } : {}) });
  } else if (verb === "fill") {
    const [browserId, selector, value, tabId] = args;
    if (!browserId || !selector || value == null) fail("invalid-arguments", "browserId, selector and value are required.");
    const parsedTabId = parseTabId(tabId);
    result = await command(browserId, "fill", { selector, value, ...(parsedTabId ? { tabId: parsedTabId } : {}) });
  } else if (verb === "upload") {
    const [browserId, selector, ...files] = args;
    if (!browserId || !selector || files.length === 0) fail("invalid-arguments", "browserId, selector and at least one file are required.");
    const relativeFiles = files.filter((file) => !isAbsolute(file));
    if (relativeFiles.length > 0) fail("invalid-arguments", "upload requires absolute file paths.", { relativeFiles });
    result = await command(browserId, "upload", { selector, files });
  } else if (verb === "close-session") {
    const [browserId, session] = args;
    if (!browserId || !session) fail("invalid-arguments", "browserId and session are required.");
    result = await command(browserId, "close_session", { session });
  } else if (verb === "command") {
    const [browserId, action, argsJson = "{}"] = args;
    if (!browserId || !action) fail("invalid-arguments", "browserId and action are required.");
    result = await command(browserId, action, parseCommandArgs(argsJson));
  } else {
    usage();
    process.exit(2);
  }
  print(result);
}

main().catch((error) => fail("client-error", error.message));
