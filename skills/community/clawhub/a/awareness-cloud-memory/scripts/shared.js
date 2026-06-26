#!/usr/bin/env node
// ---------------------------------------------------------------------------
// Shared config + HTTP helpers for all Awareness skill scripts
// ---------------------------------------------------------------------------

const fs = require("fs");
const path = require("path");

// ---------------------------------------------------------------------------
// Config
// ---------------------------------------------------------------------------

function loadConfig() {
  const defaults = {
    apiKey: process.env.AWARENESS_API_KEY || "",
    baseUrl: process.env.AWARENESS_BASE_URL || "https://awareness.market/api/v1",
    memoryId: process.env.AWARENESS_MEMORY_ID || "",
    agentRole: process.env.AWARENESS_AGENT_ROLE || "builder_agent",
    recallLimit: 8,
    localUrl: process.env.AWARENESS_LOCAL_URL || "http://localhost:37800",
  };

  const home = process.env.HOME || process.env.USERPROFILE || "";
  const configPaths = [
    path.join(home, ".openclaw", "openclaw.json"),
    path.join(process.env.cwd || process.cwd(), "openclaw.json"),
  ];

  for (const p of configPaths) {
    try {
      if (fs.existsSync(p)) {
        const raw = JSON.parse(fs.readFileSync(p, "utf-8"));
        const sc = raw?.skills?.["awareness-cloud-memory"]?.config || {};
        if (sc.apiKey) defaults.apiKey = sc.apiKey;
        if (sc.baseUrl) defaults.baseUrl = sc.baseUrl;
        if (sc.memoryId) defaults.memoryId = sc.memoryId;
        if (sc.agentRole) defaults.agentRole = sc.agentRole;
        if (sc.recallLimit) defaults.recallLimit = sc.recallLimit;
        if (sc.localUrl) defaults.localUrl = sc.localUrl;
        break;
      }
    } catch { /* skip */ }
  }
  return defaults;
}

// ---------------------------------------------------------------------------
// Resolve API endpoint (local daemon or cloud)
// ---------------------------------------------------------------------------

async function resolveEndpoint(config) {
  let baseUrl = config.baseUrl;
  let apiKey = config.apiKey;
  let memoryId = config.memoryId || "local";

  try {
    const h = await fetch(`${config.localUrl}/healthz`, {
      method: "GET", signal: AbortSignal.timeout(1500),
    });
    if (h.ok) {
      baseUrl = `${config.localUrl}/api/v1`;
      apiKey = "";
    }
  } catch {
    if (!apiKey || !config.memoryId) return null;
  }

  return { baseUrl, apiKey, memoryId };
}

// ---------------------------------------------------------------------------
// Session ID persistence
// ---------------------------------------------------------------------------

function getSessionId() {
  const tmpDir = process.env.TMPDIR || process.env.TMP || "/tmp";
  const pidFile = path.join(tmpDir, "awareness-session-id");
  try {
    const data = fs.readFileSync(pidFile, "utf-8").trim();
    const [id, ts] = data.split("|");
    if (id && ts && Date.now() - Number(ts) < 4 * 60 * 60 * 1000) return id;
  } catch { /* expired or missing */ }
  const id = `openclaw-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
  try { fs.writeFileSync(pidFile, `${id}|${Date.now()}`); } catch { /* ignore */ }
  return id;
}

// ---------------------------------------------------------------------------
// HTTP helpers
// ---------------------------------------------------------------------------

function headers(apiKey) {
  const h = { "Content-Type": "application/json", Accept: "application/json" };
  if (apiKey) h.Authorization = `Bearer ${apiKey}`;
  return h;
}

async function apiGet(baseUrl, apiKey, path, params) {
  const qs = params && params.toString() ? `?${params}` : "";
  const res = await fetch(`${baseUrl}${path}${qs}`, {
    headers: headers(apiKey), signal: AbortSignal.timeout(10000),
  });
  if (!res.ok) throw new Error(`GET ${path} → ${res.status}`);
  return res.json();
}

async function apiPost(baseUrl, apiKey, path, body) {
  const res = await fetch(`${baseUrl}${path}`, {
    method: "POST", headers: headers(apiKey),
    body: JSON.stringify(body), signal: AbortSignal.timeout(10000),
  });
  if (!res.ok) throw new Error(`POST ${path} → ${res.status}`);
  return res.json();
}

async function apiPatch(baseUrl, apiKey, path, body) {
  const res = await fetch(`${baseUrl}${path}`, {
    method: "PATCH", headers: headers(apiKey),
    body: JSON.stringify(body), signal: AbortSignal.timeout(10000),
  });
  if (!res.ok) throw new Error(`PATCH ${path} → ${res.status}`);
  return res.json();
}

// ---------------------------------------------------------------------------
// Read stdin as JSON
// ---------------------------------------------------------------------------

async function readStdin() {
  const chunks = [];
  for await (const chunk of process.stdin) chunks.push(chunk);
  const raw = Buffer.concat(chunks).toString("utf-8").trim();
  return raw ? JSON.parse(raw) : {};
}

// ---------------------------------------------------------------------------
// Parse CLI args as JSON
// ---------------------------------------------------------------------------

function parseArgs() {
  const args = process.argv.slice(2);
  if (args.length === 0) return {};
  // Single JSON argument
  if (args[0].startsWith("{")) return JSON.parse(args.join(" "));
  // Key=value pairs
  const result = {};
  for (const arg of args) {
    const eq = arg.indexOf("=");
    if (eq > 0) {
      const key = arg.slice(0, eq);
      let val = arg.slice(eq + 1);
      if (val === "true") val = true;
      else if (val === "false") val = false;
      else if (/^\d+$/.test(val)) val = Number(val);
      result[key] = val;
    } else {
      // Positional: first is query
      if (!result.query) result.query = arg;
      else result.query += " " + arg;
    }
  }
  return result;
}

module.exports = {
  loadConfig, resolveEndpoint, getSessionId,
  apiGet, apiPost, apiPatch, readStdin, parseArgs,
};
