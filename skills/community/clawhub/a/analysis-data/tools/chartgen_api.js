#!/usr/bin/env node
/**
 * ChartGen AI API helper — portable tool for OpenClaw skill.
 *
 * Zero external dependencies — uses only Node.js built-ins.
 * API key is read from environment / config — the skill never needs to know
 * or pass secrets. API requests are sent only to https://chartgen.ai.
 *
 * Usage (skill only passes business data):
 *   node tools/chartgen_api.js submit <request.json>
 *   node tools/chartgen_api.js poll   <task_id>
 *   node tools/chartgen_api.js wait   <task_id>
 *   node tools/chartgen_api.js run    <request.json>
 */

const https = require("https");
const fs = require("fs");
const os = require("os");
const path = require("path");
const { URL } = require("url");

const TOOL_VERSION = "1.0.6";

const BASE_URL = "https://chartgen.ai";
const API_HOST = "chartgen.ai";
const POLL_INTERVAL_MS = 20_000;
const MAX_POLLS = 75;

const ALLOWED_EXTENSIONS = new Set([".csv", ".xls", ".xlsx", ".tsv"]);

const HTML_CHANNELS = new Set([
  // Channels that support HTML inline rendering (case-insensitive match).
]);

function buildApiUrl(pathname) {
  const url = new URL(pathname, BASE_URL);
  if (url.protocol !== "https:" || url.hostname !== API_HOST) {
    throw new Error("Unsafe ChartGen API endpoint");
  }
  return url.toString();
}

function normalizeChannel(channel) {
  if (channel === undefined || channel === null || channel === "") {
    return undefined;
  }
  if (typeof channel !== "string") {
    throw new Error("channel must be a string");
  }
  const value = channel.trim();
  if (!/^[A-Za-z0-9][A-Za-z0-9 ._-]{0,63}$/.test(value)) {
    throw new Error(
      "channel must be 1-64 characters using letters, numbers, spaces, dots, underscores, or hyphens",
    );
  }
  return value;
}

function normalizeTaskId(taskId) {
  if (typeof taskId !== "string") {
    throw new Error("task_id must be a string");
  }
  const value = taskId.trim();
  if (!/^[A-Za-z0-9_.-]{1,128}$/.test(value)) {
    throw new Error(
      "task_id must be 1-128 characters using letters, numbers, dots, underscores, or hyphens",
    );
  }
  return value;
}

function normalizeFilePaths(files) {
  if (files === undefined || files === null) {
    return undefined;
  }
  if (!Array.isArray(files)) {
    throw new Error("files must be an array of file paths");
  }
  for (const file of files) {
    if (typeof file !== "string" || file.length === 0) {
      throw new Error("files must contain only non-empty string paths");
    }
    if (!path.isAbsolute(file)) {
      throw new Error("files must contain only absolute paths");
    }
  }
  return files.length > 0 ? files : undefined;
}

function loadSubmitRequest(requestFile) {
  if (!requestFile) {
    throw new Error("missing request JSON file");
  }

  let raw;
  try {
    raw = fs.readFileSync(path.resolve(requestFile), "utf-8");
  } catch (err) {
    throw new Error(`could not read request JSON file: ${err.message}`);
  }

  let data;
  try {
    data = JSON.parse(raw);
  } catch (err) {
    throw new Error(`request JSON is invalid: ${err.message}`);
  }

  if (!data || typeof data !== "object" || Array.isArray(data)) {
    throw new Error("request JSON must be an object");
  }
  if (typeof data.query !== "string" || data.query.trim().length === 0) {
    throw new Error("query must be a non-empty string");
  }

  return {
    query: data.query,
    channel: normalizeChannel(data.channel),
    filePaths: normalizeFilePaths(data.files),
  };
}

function safeMultipartFilename(name) {
  return String(name || "upload.dat")
    .replace(/["\\\r\n]/g, "_")
    .slice(0, 255) || "upload.dat";
}

// ---------------------------------------------------------------------------
// API key resolution — tool reads it, skill never touches it
// ---------------------------------------------------------------------------

function resolveApiKey() {
  if (process.env.CHARTGEN_API_KEY) return process.env.CHARTGEN_API_KEY;

  const home = os.homedir();
  const candidates = [
    process.env.OPENCLAW_STATE_DIR
      ? path.join(process.env.OPENCLAW_STATE_DIR, "skills", "chartgen", "config.json")
      : "",
    path.join(home, ".openclaw", "skills", "chartgen", "config.json"),
    path.join(home, ".config", "chartgen", "api_key"),
    path.join(home, ".chartgen", "api_key"),
  ].filter(Boolean);

  for (const file of candidates) {
    try {
      const raw = fs.readFileSync(file, "utf-8").trim();
      if (file.endsWith(".json")) {
        const obj = JSON.parse(raw);
        const key = obj.api_key || obj.apiKey || obj.token || obj.access_token;
        if (key) return String(key);
      } else {
        if (raw.length > 0) return raw;
      }
    } catch {
      // file not found or unreadable — try next
    }
  }
  return null;
}

// ---------------------------------------------------------------------------
// OpenClaw media directory resolution
// ---------------------------------------------------------------------------

function getMediaDir() {
  const stateDir = process.env.OPENCLAW_STATE_DIR;
  if (stateDir) {
    const media = path.join(stateDir, "media");
    if (ensureDir(media)) return media;
    const workspace = path.join(stateDir, "workspace");
    if (ensureDir(workspace)) return workspace;
  }

  const home = os.homedir();
  const candidates = [
    path.join(home, ".openclaw", "media"),
    path.join(home, ".openclaw", "workspace"),
  ];
  for (const dir of candidates) {
    if (ensureDir(dir)) return dir;
  }

  return os.tmpdir();
}

function ensureDir(dir) {
  try {
    fs.mkdirSync(dir, { recursive: true });
    return true;
  } catch {
    return false;
  }
}

// ---------------------------------------------------------------------------
// File validation
// ---------------------------------------------------------------------------

function validateFiles(filePaths) {
  const files = [];

  for (const fp of filePaths) {
    if (typeof fp !== "string" || fp.length === 0) {
      return { valid: false, error: "File paths must be non-empty strings" };
    }

    const resolved = path.resolve(fp);
    const ext = path.extname(resolved).toLowerCase();

    if (!ALLOWED_EXTENSIONS.has(ext)) {
      return {
        valid: false,
        error:
          `Unsupported file type "${ext}" for file "${path.basename(resolved)}". ` +
          `Supported types: ${[...ALLOWED_EXTENSIONS].join(", ")}`,
      };
    }

    try {
      fs.accessSync(resolved, fs.constants.R_OK);
    } catch {
      return { valid: false, error: `File not accessible: "${resolved}"` };
    }

    const stat = fs.statSync(resolved);
    if (!stat.isFile()) {
      return { valid: false, error: `Not a file: "${resolved}"` };
    }
    if (stat.size === 0) {
      return { valid: false, error: `File is empty: "${resolved}"` };
    }

    files.push({
      filePath: resolved,
      fileName: safeMultipartFilename(path.basename(resolved)),
      content: fs.readFileSync(resolved),
    });
  }

  return { valid: true, files };
}

// ---------------------------------------------------------------------------
// HTTP helpers
// ---------------------------------------------------------------------------

function request(opts) {
  return new Promise((resolve, reject) => {
    const parsed = new URL(opts.url);
    if (parsed.protocol !== "https:") {
      reject(new Error("Refusing non-HTTPS request"));
      return;
    }

    const reqOpts = {
      hostname: parsed.hostname,
      port: parsed.port || 443,
      path: parsed.pathname + parsed.search,
      method: opts.method || "GET",
      headers: opts.headers || {},
      timeout: opts.timeoutMs || 30_000,
    };

    const req = https.request(reqOpts, (res) => {
      const chunks = [];
      res.on("data", (chunk) => chunks.push(chunk));
      res.on("end", () => {
        resolve({
          status: res.statusCode || 0,
          body: Buffer.concat(chunks).toString("utf-8"),
        });
      });
    });

    req.on("error", (err) => reject(err));
    req.on("timeout", () => {
      req.destroy();
      reject(new Error("Request timed out"));
    });

    if (opts.body) req.write(opts.body);
    req.end();
  });
}

// ---------------------------------------------------------------------------
// Multipart upload
// ---------------------------------------------------------------------------

async function uploadFiles(apiKey, fileInfos) {
  const boundary =
    "----ChartGenBoundary" +
    Date.now().toString(36) +
    Math.random().toString(36).slice(2);

  const parts = [];
  for (const f of fileInfos) {
    const header =
      `--${boundary}\r\n` +
      `Content-Disposition: form-data; name="files"; filename="${f.fileName}"\r\n` +
      `Content-Type: application/octet-stream\r\n\r\n`;
    parts.push(Buffer.from(header, "utf-8"));
    parts.push(f.content);
    parts.push(Buffer.from("\r\n", "utf-8"));
  }
  parts.push(Buffer.from(`--${boundary}--\r\n`, "utf-8"));

  const body = Buffer.concat(parts);

  try {
    const res = await request({
      url: buildApiUrl("/api/usl-service/fileTable/upload"),
      method: "POST",
      headers: {
        "Content-Type": `multipart/form-data; boundary=${boundary}`,
        Authorization: apiKey,
        "Content-Length": String(body.length),
      },
      body,
      timeoutMs: 60_000,
    });

    if (res.status >= 400) {
      const detail =
        res.body.length > 0 && res.body.length < 500 ? ` — ${res.body}` : "";
      return { error: `Upload failed: HTTP ${res.status}${detail}` };
    }

    const json = JSON.parse(res.body);
    if (json.code === "00000" && Array.isArray(json.data)) {
      return { fileIds: json.data.map((f) => f.id) };
    }
    return {
      error: `Upload failed: ${json.desc || json.message || "unexpected response"}`,
    };
  } catch (err) {
    return { error: `Upload failed: ${err.message}` };
  }
}

// ---------------------------------------------------------------------------
// API methods
// ---------------------------------------------------------------------------

async function submit(apiKey, query, filePaths, channel) {
  let fileIds = [];

  if (filePaths && filePaths.length > 0) {
    const validation = validateFiles(filePaths);
    if (!validation.valid) {
      return { error: validation.error, status: "error" };
    }

    const uploadRes = await uploadFiles(apiKey, validation.files);
    if (uploadRes.error) {
      return { error: uploadRes.error, status: "error" };
    }
    fileIds = uploadRes.fileIds || [];
  }

  const payload = { query, tool_version: TOOL_VERSION };
  if (fileIds.length > 0) payload.file_ids = fileIds;
  if (channel) {
    payload.channel = channel;
    if (HTML_CHANNELS.has(channel.toLowerCase())) {
      payload.request_html = true;
    }
  }
  const body = JSON.stringify(payload);

  try {
    const res = await request({
      url: buildApiUrl("/api/agent/chat"),
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: apiKey,
      },
      body,
    });

    if (res.status === 426) {
      const info = JSON.parse(res.body);
      return {
        error: "upgrade_required",
        message: info.message || "Tool version is outdated.",
        min_version: info.min_version,
        current_version: TOOL_VERSION,
        status: "error",
      };
    }

    if (res.status >= 400) {
      return { error: `HTTP ${res.status}`, status: "error" };
    }
    const result = JSON.parse(res.body);
    if (result.task_id) {
      try {
        result.task_id = normalizeTaskId(result.task_id);
      } catch (err) {
        return {
          error: `invalid_task_id in ChartGen response: ${err.message}`,
          status: "error",
        };
      }
    }
    return result;
  } catch (err) {
    return { error: `Connection failed: ${err.message}`, status: "error" };
  }
}

async function poll(apiKey, taskId) {
  let safeTaskId;
  try {
    safeTaskId = normalizeTaskId(taskId);
  } catch (err) {
    return { error: `invalid_task_id: ${err.message}`, status: "error" };
  }

  try {
    const res = await request({
      url: buildApiUrl(`/api/agent/task/${encodeURIComponent(safeTaskId)}`),
      method: "GET",
      headers: { Authorization: apiKey },
      timeoutMs: 15_000,
    });

    if (res.status >= 400) {
      return { error: `HTTP ${res.status}`, status: "error" };
    }
    const result = JSON.parse(res.body);
    return await cleanResult(result);
  } catch (err) {
    return { error: `Poll failed: ${err.message}`, status: "error" };
  }
}

// ---------------------------------------------------------------------------
// Path-safe helpers — prevent path traversal from API-provided identifiers
// ---------------------------------------------------------------------------

function sanitizeTag(tag) {
  const s = String(tag || Date.now());
  return s.replace(/[^a-zA-Z0-9_\-]/g, "_").slice(0, 128) || String(Date.now());
}

function sanitizeExt(ext) {
  const s = String(ext || "png").replace(/^\./, "");
  return s.replace(/[^a-zA-Z0-9]/g, "").slice(0, 10) || "bin";
}

// ---------------------------------------------------------------------------
// Image saving
// ---------------------------------------------------------------------------

function saveBase64(dataUri, tag, ext) {
  ext = sanitizeExt(ext || "png");
  tag = sanitizeTag(tag);
  try {
    const marker = "base64,";
    const idx = dataUri.indexOf(marker);
    const raw = idx !== -1 ? dataUri.slice(idx + marker.length) : dataUri;
    const buf = Buffer.from(raw, "base64");
    const mediaDir = getMediaDir();
    const name = `chartgen_${tag}.${ext}`;
    const dest = path.join(mediaDir, name);
    fs.writeFileSync(dest, buf);
    return dest;
  } catch {
    return null;
  }
}

function downloadFile(url, tag, ext) {
  tag = sanitizeTag(tag);
  ext = sanitizeExt(ext);
  return new Promise((resolve) => {
    try {
      const parsed = new URL(url);
      if (parsed.protocol !== "https:") {
        resolve(null);
        return;
      }

      const mediaDir = getMediaDir();
      const dest = path.join(mediaDir, `chartgen_${tag}.${ext}`);
      https.get(parsed, (res) => {
        if (res.statusCode === 301 || res.statusCode === 302) {
          if (!res.headers.location) {
            resolve(null);
            return;
          }
          const nextUrl = new URL(res.headers.location, parsed).toString();
          downloadFile(nextUrl, tag, ext).then(resolve);
          return;
        }
        if (res.statusCode !== 200) {
          res.resume();
          resolve(null);
          return;
        }
        const file = fs.createWriteStream(dest);
        res.pipe(file);
        file.on("finish", () => { file.close(); resolve(dest); });
        file.on("error", () => resolve(null));
      }).on("error", () => resolve(null));
    } catch { resolve(null); }
  });
}

async function cleanResult(result) {
  if (result.status !== "finished" || !result.artifacts) return result;

  for (const art of result.artifacts) {
    if (art.image_base64) {
      const tag = art.artifact_id ? String(art.artifact_id) : String(Date.now());
      const saved = saveBase64(art.image_base64, tag);
      if (saved) art.image_path = saved;
    }
    delete art.image_base64;
    delete art.raw_data;

    if (art.type === "ppt") {
      if (art.preview_images && art.preview_images.length > 0) {
        const paths = [];
        for (let i = 0; i < art.preview_images.length; i++) {
          const ptag = `${art.artifact_id || Date.now()}_slide${i + 1}`;
          const p = saveBase64(art.preview_images[i], ptag);
          if (p) paths.push(p);
        }
        art.preview_paths = paths;
      }
      delete art.preview_images;

      if (art.pptx_base64) {
        const dtag = String(art.artifact_id || Date.now());
        const dp = saveBase64(art.pptx_base64, dtag, "pptx");
        if (dp) art.download_path = dp;
      } else if (art.download_url) {
        const dtag = String(art.artifact_id || Date.now());
        const dp = await downloadFile(art.download_url, dtag, "pptx");
        if (dp) art.download_path = dp;
      }
      delete art.pptx_base64;
      delete art.download_url;
    }

    // Excel / file artifacts
    if (art.file_base64) {
      const fname = art.file_name || `artifact_${art.artifact_id || Date.now()}`;
      const ext = path.extname(fname).replace(".", "") || "xlsx";
      const dtag = String(art.artifact_id || Date.now());
      const dp = saveBase64(art.file_base64, dtag, ext);
      if (dp) art.download_path = dp;
      delete art.file_base64;
    }
  }

  if (result.html_content) {
    let html = result.html_content;
    for (const art of result.artifacts) {
      if (art.artifact_id && art.image_path) {
        const normalizedPath = art.image_path.replace(/\\/g, "/");
        html = html.replace(
          `src="artifact:${art.artifact_id}"`,
          `src="file://${normalizedPath}"`,
        );
      }
    }
    result.html_content = html;
  }

  if (result.session_id) {
    const sid = encodeURIComponent(String(result.session_id));
    if (result.artifacts.length === 1 && result.artifacts[0].artifact_id) {
      const artifactId = encodeURIComponent(String(result.artifacts[0].artifact_id));
      result.edit_url =
        `${BASE_URL}/chat/${sid}?artifactId=${artifactId}`;
    } else {
      result.edit_url = `${BASE_URL}/chat/${sid}`;
    }
  }

  delete result.session_id;
  delete result.round_id;
  delete result.user_query;
  delete result.round_data_raw;

  return result;
}

// ---------------------------------------------------------------------------
// Polling helpers
// ---------------------------------------------------------------------------

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function waitForTask(apiKey, taskId, intervalMs, maxPolls) {
  try {
    taskId = normalizeTaskId(taskId);
  } catch (err) {
    return { error: `invalid_task_id: ${err.message}`, status: "error" };
  }

  intervalMs = intervalMs || POLL_INTERVAL_MS;
  maxPolls = maxPolls || MAX_POLLS;

  for (let attempt = 1; attempt <= maxPolls; attempt++) {
    await sleep(intervalMs);
    const result = await poll(apiKey, taskId);
    const st = result.status || "";

    if (st === "finished" || st === "error" || st === "not_found") {
      return result;
    }

    if (attempt % 3 === 0) {
      const progress = result.progress || "processing";
      process.stderr.write(
        JSON.stringify({ poll: attempt, status: st, progress }) + "\n",
      );
    }
  }

  return { error: "Polling timed out", task_id: taskId, status: "timeout" };
}

async function run(apiKey, query, filePaths, channel) {
  const submitRes = await submit(apiKey, query, filePaths, channel);
  if (submitRes.error) return { error: submitRes.error, status: "error" };

  const taskId = submitRes.task_id;
  if (!taskId)
    return { error: "No task_id in submit response", status: "error" };

  return waitForTask(apiKey, taskId);
}

// ---------------------------------------------------------------------------
// User-facing error messages — skill just relays `user_message` to the user.
// ---------------------------------------------------------------------------

function getUserMessage(error) {
  const lower = error.toLowerCase();

  if (lower.startsWith("api_key_not_configured"))
    return "";

  if (lower.includes("http 401") || lower.includes("http 403"))
    return (
      "⚠️ Your ChartGen API key is invalid or expired. " +
      "Please check or regenerate it at https://chartgen.ai/chat → Menu → API."
    );

  if (lower.includes("http 429"))
    return "⏳ Rate limit reached. Please wait a moment and try again.";

  if (lower.includes("http 5"))
    return "⚠️ ChartGen service is temporarily unavailable. Please try again in a few minutes.";

  if (lower.includes("connection failed") || lower.includes("request timed out"))
    return "⚠️ Could not connect to ChartGen. Please check your network and try again.";

  if (lower.includes("unsupported file type"))
    return "⚠️ " + error + "\nPlease re-send with supported file types: CSV, XLS, XLSX, TSV.";

  if (lower.includes("file not accessible") || lower.includes("not a file") || lower.includes("file is empty"))
    return "⚠️ " + error + "\nPlease verify the file path and try again.";

  if (lower.includes("upload failed"))
    return "⚠️ File upload failed. Please try again.";

  if (lower === "upgrade_required")
    return "";

  return "⚠️ " + error;
}

function enrichError(result) {
  if (result.error && typeof result.error === "string") {
    const lower = result.error.toLowerCase();
    if (lower === "upgrade_required" || lower.startsWith("api_key_not_configured")) {
      return result;
    }
    const msg = getUserMessage(result.error);
    if (msg) result.user_message = msg;
  }
  return result;
}

// ---------------------------------------------------------------------------
// CLI entry point
// ---------------------------------------------------------------------------

function fail(msg) {
  process.stdout.write(JSON.stringify(enrichError({ error: msg })) + "\n");
  process.exit(1);
}

function requireApiKey() {
  const apiKey = resolveApiKey();
  if (!apiKey) {
    fail(
      "api_key_not_configured. " +
      "Please set your ChartGen API key: " +
      'export CHARTGEN_API_KEY="your-key" ' +
      "or save it to ~/.chartgen/api_key . " +
      "Get a key at https://chartgen.ai/chat → Menu → API",
    );
  }
  return apiKey;
}

async function main() {
  const [, , cmd, ...args] = process.argv;

  let result;

  switch (cmd) {
    case "submit": {
      if (args.length !== 1) {
        process.stderr.write(
          "Usage: chartgen_api.js submit <request.json>\n",
        );
        process.exit(1);
      }
      let requestData;
      try {
        requestData = loadSubmitRequest(args[0]);
      } catch (err) {
        fail(`invalid_request_file: ${err.message}`);
      }
      const apiKey = requireApiKey();
      result = await submit(
        apiKey,
        requestData.query,
        requestData.filePaths,
        requestData.channel,
      );
      break;
    }
    case "poll": {
      if (args.length !== 1) {
        process.stderr.write("Usage: chartgen_api.js poll <task_id>\n");
        process.exit(1);
      }
      let taskId;
      try {
        taskId = normalizeTaskId(args[0]);
      } catch (err) {
        fail(`invalid_task_id: ${err.message}`);
      }
      const apiKey = requireApiKey();
      result = await poll(apiKey, taskId);
      break;
    }
    case "wait": {
      if (args.length !== 1) {
        process.stderr.write("Usage: chartgen_api.js wait <task_id>\n");
        process.exit(1);
      }
      let taskId;
      try {
        taskId = normalizeTaskId(args[0]);
      } catch (err) {
        fail(`invalid_task_id: ${err.message}`);
      }
      const apiKey = requireApiKey();
      result = await waitForTask(apiKey, taskId);
      break;
    }
    case "run": {
      if (args.length !== 1) {
        process.stderr.write(
          "Usage: chartgen_api.js run <request.json>\n",
        );
        process.exit(1);
      }
      let requestData;
      try {
        requestData = loadSubmitRequest(args[0]);
      } catch (err) {
        fail(`invalid_request_file: ${err.message}`);
      }
      const apiKey = requireApiKey();
      result = await run(
        apiKey,
        requestData.query,
        requestData.filePaths,
        requestData.channel,
      );
      break;
    }
    case "version": {
      process.stdout.write(TOOL_VERSION + "\n");
      process.exit(0);
    }
    default:
      process.stderr.write(
        `ChartGen AI API Tool v${TOOL_VERSION}  (${BASE_URL})\n\n` +
        "Commands:\n" +
        "  submit  <request.json>                           Submit task\n" +
        "  poll    <task_id>                                Single status check\n" +
        "  wait    <task_id>                                Poll until done (~25 min max)\n" +
        "  run     <request.json>                           submit + wait\n" +
        "  version                                          Print tool version\n\n" +
        "Request JSON shape:\n" +
        '  { "query": "...", "channel": "Web", "files": ["/path/data.xlsx"] }\n\n' +
        "Supported file types: " +
        [...ALLOWED_EXTENSIONS].join(", ") +
        "\n\n" +
        "API key is read automatically from:\n" +
        "  1. CHARTGEN_API_KEY environment variable\n" +
        "  2. ~/.openclaw/skills/chartgen/config.json\n" +
        "  3. ~/.chartgen/api_key\n\n" +
        "Get a key: https://chartgen.ai/chat → Menu → API\n",
      );
      process.exit(1);
  }

  if (result && typeof result === "object" && result.error) {
    enrichError(result);
  }
  process.stdout.write(JSON.stringify(result, null, 2) + "\n");
}

main().catch((err) => {
  process.stderr.write(JSON.stringify({ error: String(err) }) + "\n");
  process.exit(1);
});
