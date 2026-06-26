#!/usr/bin/env node
// ⚠️ DO NOT EDIT — auto-generated from sdks/_shared/scripts/shared.js
// Edit the source in sdks/_shared/scripts/ then run:
//   bash scripts/sync-shared-scripts.sh
// See docs/features/f-036/shared-scripts-consolidation.md

// ---------------------------------------------------------------------------
// Shared config + HTTP helpers for all Awareness skill scripts
// ---------------------------------------------------------------------------

const fs = require("fs");
const path = require("path");

// ---------------------------------------------------------------------------
// Config
// ---------------------------------------------------------------------------

function loadConfig() {
  // Environment variables (read once; applied as highest-priority override at the end)
  const envApiKey = process.env.AWARENESS_API_KEY || "";
  const envMemoryId = process.env.AWARENESS_MEMORY_ID || "";
  const envBaseUrl = process.env.AWARENESS_BASE_URL || "";
  const envAgentRole = process.env.AWARENESS_AGENT_ROLE || "";
  const envLocalUrl = process.env.AWARENESS_LOCAL_URL || "";

  const defaults = {
    apiKey: "",
    baseUrl: "https://awareness.market/api/v1",
    memoryId: "",
    agentRole: "builder_agent",
    recallLimit: 8,
    localUrl: "http://localhost:37800",
  };

  // --- Priority 3: ~/.openclaw/openclaw.json or ./openclaw.json (skill config) ---
  const home = process.env.HOME || process.env.USERPROFILE || "";
  const configPaths = [
    path.join(home, ".openclaw", "openclaw.json"),
    path.join(process.env.PWD || process.cwd(), "openclaw.json"),
  ];

  for (const p of configPaths) {
    try {
      if (fs.existsSync(p)) {
        const raw = JSON.parse(fs.readFileSync(p, "utf-8"));
        // Try skill config first, then plugin config
        const sc =
          raw?.skills?.["awareness-memory"]?.config ||
          raw?.plugins?.entries?.["openclaw-memory"]?.config ||
          {};
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

  // --- Priority 2: ~/.awareness/credentials.json (written by setup.js) ---
  try {
    const credsFile = path.join(home, ".awareness", "credentials.json");
    if (fs.existsSync(credsFile)) {
      const creds = JSON.parse(fs.readFileSync(credsFile, "utf-8"));
      if (creds.apiKey) defaults.apiKey = creds.apiKey;
      if (creds.baseUrl) defaults.baseUrl = creds.baseUrl;
      if (creds.memoryId) defaults.memoryId = creds.memoryId;
    }
  } catch { /* skip */ }

  // --- Priority 1.5: Workspace registry (per-project port) + project config ---
  const projectDir = path.resolve(process.env.PWD || process.cwd());
  let wsPortOverride = false;
  try {
    const wsFile = path.join(home, ".awareness", "workspaces.json");
    if (fs.existsSync(wsFile)) {
      const workspaces = JSON.parse(fs.readFileSync(wsFile, "utf-8"));
      const ws = workspaces[projectDir];
      // Only read port from registry — memoryId comes from project config.json
      if (ws && ws.port) {
        defaults.localUrl = `http://localhost:${ws.port}`;
        wsPortOverride = true;
      }
    }
  } catch { /* skip */ }
  // Project-level .awareness/config.json is the single source for cloud config
  try {
    const projConfig = path.join(projectDir, ".awareness", "config.json");
    if (fs.existsSync(projConfig)) {
      const pc = JSON.parse(fs.readFileSync(projConfig, "utf-8"));
      if (pc.cloud?.api_key) defaults.apiKey = pc.cloud.api_key;
      if (pc.cloud?.memory_id) defaults.memoryId = pc.cloud.memory_id;
      if (pc.cloud?.api_base) defaults.baseUrl = pc.cloud.api_base;
    }
  } catch { /* skip */ }

  // --- Priority 1 (highest): Environment variables override everything ---
  // Exception: AWARENESS_LOCAL_URL does NOT override workspace registry port,
  // because the env var is global (written to .zshrc) while the registry is per-project.
  if (envApiKey) defaults.apiKey = envApiKey;
  if (envBaseUrl) defaults.baseUrl = envBaseUrl;
  if (envMemoryId) defaults.memoryId = envMemoryId;
  if (envAgentRole) defaults.agentRole = envAgentRole;
  if (envLocalUrl && !wsPortOverride) defaults.localUrl = envLocalUrl;

  return defaults;
}

// ---------------------------------------------------------------------------
// Resolve API endpoint (local daemon or cloud)
// ---------------------------------------------------------------------------

async function resolveEndpoint(config) {
  // Try local daemon first
  try {
    const h = await fetch(`${config.localUrl}/healthz`, {
      method: "GET", signal: AbortSignal.timeout(1500),
    });
    if (h.ok) {
      return {
        mode: "local",
        localUrl: config.localUrl,
        baseUrl: config.baseUrl,
        apiKey: config.apiKey || "",     // pass cloud key for hybrid recall
        memoryId: config.memoryId || "local",
      };
    }
  } catch { /* local daemon not available — try to auto-start */ }

  // Skip daemon auto-start if env vars provide cloud credentials directly
  const hasEnvCloudCreds = Boolean(process.env.AWARENESS_API_KEY && process.env.AWARENESS_MEMORY_ID);
  if (hasEnvCloudCreds) {
    return {
      mode: "cloud",
      localUrl: null,
      baseUrl: config.baseUrl || "https://awareness.market/api/v1",
      apiKey: config.apiKey,
      memoryId: config.memoryId,
    };
  }

  // Auto-start local daemon if not running (skip on Termux/Android — not supported)
  const isTermux = Boolean(process.env.TERMUX_VERSION) ||
    (typeof process.env.PREFIX === "string" && process.env.PREFIX.includes("com.termux"));
  if (isTermux) return null;  // fast-fail on Android — caller handles device auth

  try {
    const { spawn } = require("child_process");
    const child = spawn("npx", ["-y", "@awareness-sdk/local", "start"], {
      cwd: process.cwd(),
      detached: true,
      stdio: "ignore",
    });
    child.unref();
    // Poll healthz for up to 6 seconds (hook timeout is 15s)
    for (let i = 0; i < 12; i++) {
      await new Promise((r) => setTimeout(r, 500));
      try {
        const retry = await fetch(`${config.localUrl}/healthz`, {
          method: "GET", signal: AbortSignal.timeout(1000),
        });
        if (retry.ok) {
          return {
            mode: "local",
            localUrl: config.localUrl,
            baseUrl: config.baseUrl,
            apiKey: config.apiKey || "",
            memoryId: config.memoryId || "local",
          };
        }
      } catch { /* keep polling */ }
    }
    // Daemon failed to start within 6 seconds
    process.stderr.write(
      "[awareness] Local daemon failed to start. Possible causes:\n" +
      "  - missing 'better-sqlite3' native dependency (run: npm install -g @awareness-sdk/local)\n" +
      "  - port 37800 already in use\n" +
      "  Falling back to cloud mode...\n"
    );
  } catch { /* npx/spawn not available */ }

  // Fall back to cloud
  if (!config.apiKey || !config.memoryId) return null;
  return {
    mode: "cloud",
    localUrl: null,
    baseUrl: config.baseUrl,
    apiKey: config.apiKey,
    memoryId: config.memoryId,
  };
}

// ---------------------------------------------------------------------------
// Session ID persistence
// ---------------------------------------------------------------------------

function getSessionId() {
  // Use project-local session file to isolate sessions across projects
  const projectDir = path.resolve(process.env.PWD || process.cwd());
  const awarenessDir = path.join(projectDir, ".awareness");
  let sessionFile;
  try {
    if (fs.existsSync(awarenessDir)) {
      sessionFile = path.join(awarenessDir, "session-id");
    }
  } catch { /* ignore */ }
  // Fallback to global tmp if no .awareness dir
  if (!sessionFile) {
    const tmpDir = process.env.TMPDIR || process.env.TMP || "/tmp";
    sessionFile = path.join(tmpDir, "awareness-session-id");
  }
  try {
    const data = fs.readFileSync(sessionFile, "utf-8").trim();
    const [id, ts] = data.split("|");
    if (id && ts && Date.now() - Number(ts) < 4 * 60 * 60 * 1000) return id;
  } catch { /* expired or missing */ }
  const id = `openclaw-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
  try { fs.writeFileSync(sessionFile, `${id}|${Date.now()}`); } catch { /* ignore */ }
  return id;
}

// ---------------------------------------------------------------------------
// MCP JSON-RPC call (for local daemon)
// ---------------------------------------------------------------------------

let _mcpIdCounter = 1;

function parseRecallSummaryText(text, ids = []) {
  const cleaned = String(text || "").replace(/^Found \d+ memories:\n\n/, "").trim();
  if (!cleaned) return [];

  const chunks = cleaned
    .split(/\n\n(?=\d+\.\s+\[[^\]]*\]\s+)/)
    .map((chunk) => chunk.trim())
    .filter(Boolean);

  return chunks.map((chunk, index) => {
    const match = chunk.match(/^\d+\.\s+\[([^\]]*)\]\s+([^\n]+?)(?:\s+\([^)]*\))?(?:\n\s+([\s\S]*))?$/);
    if (!match) {
      return {
        id: ids[index],
        content: chunk,
      };
    }

    const [, type, rawTitle, rawSummary = ""] = match;
    // Strip trailing metadata like (85%, 3d ago, ~120tok) from title
    const title = rawTitle.replace(/\s*\([^)]*%[^)]*\)\s*$/, "").trim();
    const summary = rawSummary.trim();
    const prefix = type ? `[${type}] ` : "";
    const content = summary ? `${prefix}${title}\n${summary}` : `${prefix}${title}`;
    return {
      id: ids[index],
      type: type || undefined,
      title: title.trim(),
      summary: summary || undefined,
      content,
    };
  });
}

async function mcpCall(localUrl, toolName, args, timeoutMs = 10000) {
  const res = await fetch(`${localUrl}/mcp`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      jsonrpc: "2.0",
      id: _mcpIdCounter++,
      method: "tools/call",
      params: { name: toolName, arguments: args },
    }),
    signal: AbortSignal.timeout(timeoutMs),
  });
  if (!res.ok) throw new Error(`MCP ${toolName} → ${res.status}`);
  const json = await res.json();
  if (json.error) throw new Error(json.error.message || JSON.stringify(json.error));
  const content = json.result?.content || [];
  if (content.length > 1) {
    const text = content[0]?.text || "";
    try {
      const extra = JSON.parse(content[1]?.text || "{}");
      if (Array.isArray(extra._ids) || extra._meta) {
        const ids = Array.isArray(extra._ids) ? extra._ids.map((id) => String(id)) : [];
        return {
          results: parseRecallSummaryText(text, ids),
          _ids: ids,
          _meta: extra._meta || {},
          readable_text: text,
        };
      }
    } catch {
      // Fall through to first-block parsing
    }
  }
  const text = content[0]?.text;
  if (!text) return json.result;
  try { return JSON.parse(text); } catch { return text; }
}

// ---------------------------------------------------------------------------
// HTTP helpers (for cloud API)
// ---------------------------------------------------------------------------

function headers(apiKey) {
  const h = { "Content-Type": "application/json", Accept: "application/json" };
  if (apiKey) h.Authorization = `Bearer ${apiKey}`;
  return h;
}

async function apiGet(baseUrl, apiKey, urlPath, params) {
  const qs = params && params.toString() ? `?${params}` : "";
  const res = await fetch(`${baseUrl}${urlPath}${qs}`, {
    headers: headers(apiKey), signal: AbortSignal.timeout(10000),
  });
  if (!res.ok) throw new Error(`GET ${urlPath} → ${res.status}`);
  return res.json();
}

async function apiPost(baseUrl, apiKey, urlPath, body) {
  const res = await fetch(`${baseUrl}${urlPath}`, {
    method: "POST", headers: headers(apiKey),
    body: JSON.stringify(body), signal: AbortSignal.timeout(10000),
  });
  if (!res.ok) throw new Error(`POST ${urlPath} → ${res.status}`);
  return res.json();
}

async function apiPatch(baseUrl, apiKey, urlPath, body) {
  const res = await fetch(`${baseUrl}${urlPath}`, {
    method: "PATCH", headers: headers(apiKey),
    body: JSON.stringify(body), signal: AbortSignal.timeout(10000),
  });
  if (!res.ok) throw new Error(`PATCH ${urlPath} → ${res.status}`);
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
    } else if (!arg.startsWith("--")) {
      // Positional: first is query
      if (!result.query) result.query = arg;
      else result.query += " " + arg;
    }
  }
  return result;
}

module.exports = {
  loadConfig, resolveEndpoint, getSessionId,
  mcpCall, apiGet, apiPost, apiPatch, readStdin, parseArgs,
};
