#!/usr/bin/env node
/**
 * ChartGen AI API helper — portable tool for OpenClaw skill.
 *
 * Zero external dependencies — uses only Node.js built-ins.
 * API key and URL are read from environment / config — the skill never
 * needs to know or pass secrets.
 *
 * Usage (skill only passes business data):
 *   node tools/chartgen_api.js submit "<query>" <channel> [file1 file2 ...]
 *   node tools/chartgen_api.js poll   <task_id>
 *   node tools/chartgen_api.js wait   <task_id>
 *   node tools/chartgen_api.js run    "<query>" <channel> [file1 file2 ...]
 */

const https = require("https");
const http = require("http");
const fs = require("fs");
const os = require("os");
const path = require("path");
const { URL } = require("url");

const TOOL_VERSION = "1.0.2";

const BASE_URL = process.env.CHARTGEN_API_URL || "https://chartgen.ai";
const POLL_INTERVAL_MS = 20_000;
const MAX_POLLS = 75;

const ALLOWED_EXTENSIONS = new Set([".csv", ".xls", ".xlsx", ".tsv"]);

const HTML_CHANNELS = new Set([
  // Channels that support HTML inline rendering (case-insensitive match).
]);

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
      fileName: path.basename(resolved),
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
    const lib = parsed.protocol === "https:" ? https : http;

    const reqOpts = {
      hostname: parsed.hostname,
      port: parsed.port || (parsed.protocol === "https:" ? 443 : 80),
      path: parsed.pathname + parsed.search,
      method: opts.method || "GET",
      headers: opts.headers || {},
      timeout: opts.timeoutMs || 30_000,
    };

    const req = lib.request(reqOpts, (res) => {
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
      url: `${BASE_URL}/api/usl-service/fileTable/upload`,
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
      url: `${BASE_URL}/api/agent/chat`,
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
    return JSON.parse(res.body);
  } catch (err) {
    return { error: `Connection failed: ${err.message}`, status: "error" };
  }
}

async function poll(apiKey, taskId) {
  try {
    const res = await request({
      url: `${BASE_URL}/api/agent/task/${taskId}`,
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
      const mediaDir = getMediaDir();
      const dest = path.join(mediaDir, `chartgen_${tag}.${ext}`);
      const mod = url.startsWith("https") ? https : http;
      const file = fs.createWriteStream(dest);
      mod.get(url, (res) => {
        if (res.statusCode === 301 || res.statusCode === 302) {
          downloadFile(res.headers.location, tag, ext).then(resolve);
          return;
        }
        if (res.statusCode !== 200) { resolve(null); return; }
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
    const sid = result.session_id;
    if (result.artifacts.length === 1 && result.artifacts[0].artifact_id) {
      result.edit_url =
        `${BASE_URL}/chat/${sid}?artifactId=${result.artifacts[0].artifact_id}`;
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

async function main() {
  const [, , cmd, ...args] = process.argv;

  const apiKey = resolveApiKey();
  if (!apiKey && cmd && cmd !== "help" && cmd !== "version") {
    fail(
      "api_key_not_configured. " +
      "Please set your ChartGen API key: " +
      'export CHARTGEN_API_KEY="your-key" ' +
      "or save it to ~/.chartgen/api_key . " +
      "Get a key at https://chartgen.ai/chat → Menu → API",
    );
  }

  let result;

  switch (cmd) {
    case "submit": {
      const [query, channel, ...filePaths] = args;
      if (!query) {
        process.stderr.write(
          'Usage: chartgen_api.js submit "<query>" <channel> [file1 file2 ...]\n',
        );
        process.exit(1);
      }
      result = await submit(
        apiKey,
        query,
        filePaths.length > 0 ? filePaths : undefined,
        channel,
      );
      break;
    }
    case "poll": {
      const taskId = args[0];
      if (!taskId) {
        process.stderr.write("Usage: chartgen_api.js poll <task_id>\n");
        process.exit(1);
      }
      result = await poll(apiKey, taskId);
      break;
    }
    case "wait": {
      const taskId = args[0];
      if (!taskId) {
        process.stderr.write("Usage: chartgen_api.js wait <task_id>\n");
        process.exit(1);
      }
      result = await waitForTask(apiKey, taskId);
      break;
    }
    case "run": {
      const [query, channel, ...filePaths] = args;
      if (!query) {
        process.stderr.write(
          'Usage: chartgen_api.js run "<query>" <channel> [file1 file2 ...]\n',
        );
        process.exit(1);
      }
      result = await run(
        apiKey,
        query,
        filePaths.length > 0 ? filePaths : undefined,
        channel,
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
        '  submit  "<query>" <channel> [file1 file2 ...]   Submit task\n' +
        "  poll    <task_id>                                Single status check\n" +
        "  wait    <task_id>                                Poll until done (~25 min max)\n" +
        '  run     "<query>" <channel> [file1 file2 ...]   submit + wait\n' +
        "  version                                          Print tool version\n\n" +
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
