#!/usr/bin/env node

const fs = require("node:fs/promises");
const path = require("node:path");
const process = require("node:process");

const DEFAULT_BASE_URL = "https://ark.cn-beijing.volces.com";
const DEFAULT_DOWNLOAD_ROOT = "seedance-downloads";
const DEFAULT_POLL_INTERVAL_MS = 5000;
const DEFAULT_TIMEOUT_MS = 20 * 60 * 1000;
const TERMINAL_STATUSES = new Set(["succeeded", "failed", "expired"]);

const MIME_BY_EXTENSION = new Map([
  [".jpg", "image/jpeg"],
  [".jpeg", "image/jpeg"],
  [".png", "image/png"],
  [".webp", "image/webp"],
  [".bmp", "image/bmp"],
  [".tiff", "image/tiff"],
  [".tif", "image/tiff"],
  [".gif", "image/gif"],
  [".heic", "image/heic"],
  [".heif", "image/heif"],
  [".mp4", "video/mp4"],
  [".mov", "video/quicktime"],
  [".webm", "video/webm"],
  [".mp3", "audio/mpeg"],
  [".wav", "audio/wav"],
  [".m4a", "audio/mp4"],
  [".aac", "audio/aac"],
  [".flac", "audio/flac"],
  [".ogg", "audio/ogg"],
]);

async function main() {
  const parsed = parseArgv(process.argv.slice(2));
  const command = parsed.command || "run";
  const options = parsed.options;

  if (options.help || command === "help") {
    printHelp();
    return;
  }

  switch (command) {
    case "run":
      await handleRun(options);
      return;
    case "create":
      await handleCreate(options);
      return;
    case "get":
      await handleGet(options);
      return;
    case "list":
      await handleList(options);
      return;
    case "delete":
      await handleDelete(options);
      return;
    case "download":
      await handleDownload(options);
      return;
    default:
      throw new Error(`Unknown command: ${command}`);
  }
}

function printHelp() {
  console.log(`
Seedance video task helper for Volcengine Ark APIs.

Default command: run

Usage:
  node seedance-video.js [run] [options]
  node seedance-video.js create [options]
  node seedance-video.js get --task-id <id> [options]
  node seedance-video.js list [options]
  node seedance-video.js delete --task-id <id>
  node seedance-video.js download (--task-file <file> | --task-id <id>) [options]

Common options:
  --api-key <key>                Override ARK_API_KEY
  --base-url <url>               Override base URL (default: ${DEFAULT_BASE_URL})
  --model <id>                   Model ID (required unless payload JSON already contains model)
  --payload-file <file>          Load raw request JSON
  --prompt <text>                Add a text content item
  --image-url <url>              Add an image_url content item (repeatable)
  --image-file <path>            Add a local image as a base64 data URL (repeatable)
  --video-url <url>              Add a video_url content item (repeatable)
  --video-file <path>            Add a local video as a base64 data URL (repeatable)
  --audio-url <url>              Add an audio_url content item (repeatable)
  --audio-file <path>            Add a local audio as a base64 data URL (repeatable)
  --draft-task-id <id>           Add a draft_task content item (repeatable)
  --resolution <value>           e.g. 720p, 1080p
  --ratio <value>                e.g. 16:9, 9:16, 1:1
  --duration <seconds>           Video duration
  --frames <count>               Frame count
  --seed <number>                Sampling seed
  --camera-fixed <bool>          true / false
  --watermark <bool>             true / false
  --return-last-frame <bool>     true / false
  --callback-url <url>           Ark callback URL
  --draft <bool>                 Pass through draft mode if supported
  --download-dir <dir>           Where to save outputs
  --poll-interval <seconds>      Poll interval (default: 5)
  --timeout-sec <seconds>        Wait timeout (default: 1200)
  --wait                         Wait after create

List filters:
  --page-num <number>
  --page-size <number>
  --filter-status <status>
  --filter-model <model>
  --filter-task-id <id>          Repeatable

Download options:
  --task-file <path>             Load a saved task JSON and download outputs

Examples:
  node seedance-video.js --prompt "Rainy city at night, slow camera push" --download-dir "./out"
  node seedance-video.js --model "doubao-seedance-2-0-260128" --prompt "Rainy city at night, slow camera push" --download-dir "./out"
  node seedance-video.js create --model "doubao-seedance-1-0-pro-250528" --payload-file "./payload.json"
  node seedance-video.js get --task-id cgt-xxxx --download-dir "./out"
  `.trim());
}

async function handleRun(options) {
  const client = createClient(options);
  const payload = await buildPayload(options);
  const createResponse = await client.createTask(payload);
  const taskId = assertTaskId(createResponse);
  const downloadDir = resolveDownloadDir(options.downloadDir, taskId);

  await ensureDir(downloadDir);
  await writeJson(path.join(downloadDir, "request.json"), sanitizePayloadForStorage(payload));

  console.log(`Created task: ${taskId}`);
  const task = await waitForTask(client, taskId, options);
  await writeJson(path.join(downloadDir, "task.json"), task);
  await maybeDownloadTaskOutputs(task, downloadDir);
  printSummary(task, downloadDir);
}

async function handleCreate(options) {
  const client = createClient(options);
  const payload = await buildPayload(options);
  const response = await client.createTask(payload);
  console.log(JSON.stringify(response, null, 2));

  const shouldWait = parseBoolean(options.wait, false);
  if (!shouldWait) {
    return;
  }

  const taskId = assertTaskId(response);
  const downloadDir = resolveDownloadDir(options.downloadDir, taskId);
  await ensureDir(downloadDir);
  await writeJson(path.join(downloadDir, "request.json"), sanitizePayloadForStorage(payload));

  const task = await waitForTask(client, taskId, options);
  await writeJson(path.join(downloadDir, "task.json"), task);
  await maybeDownloadTaskOutputs(task, downloadDir);
  printSummary(task, downloadDir);
}

async function handleGet(options) {
  const client = createClient(options);
  const taskId = requireOption(options.taskId, "--task-id is required for get");
  const task = await client.getTask(taskId);
  console.log(JSON.stringify(task, null, 2));

  if (options.downloadDir) {
    const downloadDir = resolveDownloadDir(options.downloadDir, task.id || taskId);
    await ensureDir(downloadDir);
    await writeJson(path.join(downloadDir, "task.json"), task);
    await maybeDownloadTaskOutputs(task, downloadDir);
  }
}

async function handleList(options) {
  const client = createClient(options);
  const response = await client.listTasks({
    pageNum: options.pageNum,
    pageSize: options.pageSize,
    status: options.filterStatus,
    model: options.filterModel,
    taskIds: toArray(options.filterTaskId),
  });
  console.log(JSON.stringify(response, null, 2));
}

async function handleDelete(options) {
  const client = createClient(options);
  const taskId = requireOption(options.taskId, "--task-id is required for delete");
  const response = await client.deleteTask(taskId);
  console.log(JSON.stringify(response, null, 2));
}

async function handleDownload(options) {
  const task = options.taskFile
    ? await readJson(path.resolve(options.taskFile))
    : await createClient(options).getTask(requireOption(options.taskId, "--task-id or --task-file is required for download"));

  const taskId = task.id || options.taskId || "unknown-task";
  const downloadDir = resolveDownloadDir(options.downloadDir, taskId);
  await ensureDir(downloadDir);
  await writeJson(path.join(downloadDir, "task.json"), task);
  await maybeDownloadTaskOutputs(task, downloadDir);
  printSummary(task, downloadDir);
}

function createClient(options) {
  const apiKey = options.apiKey || process.env.ARK_API_KEY;
  if (!apiKey) {
    throw new Error("Missing ARK_API_KEY. Set the environment variable or pass --api-key.");
  }

  const baseUrl = stripTrailingSlash(options.baseUrl || process.env.ARK_BASE_URL || DEFAULT_BASE_URL);
  const headers = {
    Authorization: `Bearer ${apiKey}`,
    "Content-Type": "application/json",
  };

  return {
    async createTask(payload) {
      return requestJson(`${baseUrl}/api/v3/contents/generations/tasks`, {
        method: "POST",
        headers,
        body: JSON.stringify(payload),
      });
    },
    async getTask(taskId) {
      return requestJson(`${baseUrl}/api/v3/contents/generations/tasks/${encodeURIComponent(taskId)}`, {
        method: "GET",
        headers,
      });
    },
    async listTasks(filters) {
      const url = new URL(`${baseUrl}/api/v3/contents/generations/tasks`);
      if (filters.pageNum) {
        url.searchParams.set("page_num", String(filters.pageNum));
      }
      if (filters.pageSize) {
        url.searchParams.set("page_size", String(filters.pageSize));
      }
      if (filters.status) {
        url.searchParams.set("filter.status", String(filters.status));
      }
      if (filters.model) {
        url.searchParams.set("filter.model", String(filters.model));
      }
      const taskIds = toArray(filters.taskIds).filter(Boolean);
      if (taskIds.length > 0) {
        url.searchParams.set("filter.task_ids", taskIds.join(","));
      }
      return requestJson(url.toString(), {
        method: "GET",
        headers,
      });
    },
    async deleteTask(taskId) {
      return requestJson(`${baseUrl}/api/v3/contents/generations/tasks/${encodeURIComponent(taskId)}`, {
        method: "DELETE",
        headers,
      });
    },
  };
}

async function buildPayload(options) {
  const payload = options.payloadFile ? await readJson(path.resolve(options.payloadFile)) : {};
  const content = Array.isArray(payload.content) ? [...payload.content] : [];

  if (options.prompt) {
    content.push({ type: "text", text: String(options.prompt) });
  }

  for (const item of toArray(options.imageUrl)) {
    content.push({ type: "image_url", image_url: { url: item } });
  }
  for (const item of toArray(options.videoUrl)) {
    content.push({ type: "video_url", video_url: { url: item } });
  }
  for (const item of toArray(options.audioUrl)) {
    content.push({ type: "audio_url", audio_url: { url: item } });
  }
  for (const item of toArray(options.draftTaskId)) {
    content.push({ type: "draft_task", draft_task: { id: item } });
  }

  for (const file of toArray(options.imageFile)) {
    content.push({ type: "image_url", image_url: { url: await fileToDataUrl(file) } });
  }
  for (const file of toArray(options.videoFile)) {
    content.push({ type: "video_url", video_url: { url: await fileToDataUrl(file) } });
  }
  for (const file of toArray(options.audioFile)) {
    content.push({ type: "audio_url", audio_url: { url: await fileToDataUrl(file) } });
  }

  if (content.length === 0) {
    throw new Error("No content specified. Use --prompt, media inputs, or --payload-file with a content array.");
  }

  payload.model = await resolveSelectedModel(options, payload.model);
  payload.content = content;

  applyIfDefined(payload, "resolution", options.resolution);
  applyIfDefined(payload, "ratio", options.ratio);
  applyNumberIfDefined(payload, "duration", options.duration);
  applyNumberIfDefined(payload, "frames", options.frames);
  applyNumberIfDefined(payload, "seed", options.seed);
  applyBooleanIfDefined(payload, "camera_fixed", options.cameraFixed);
  applyBooleanIfDefined(payload, "watermark", options.watermark);
  applyBooleanIfDefined(payload, "return_last_frame", options.returnLastFrame);
  applyBooleanIfDefined(payload, "draft", options.draft);
  applyIfDefined(payload, "callback_url", options.callbackUrl);

  return payload;
}

async function resolveSelectedModel(options, payloadModel) {
  const requested = options.model || payloadModel;
  if (!requested) {
    throw new Error("Missing model selection. Pass --model <MODEL_ID> or include model in --payload-file.");
  }
  return requested;
}

async function waitForTask(client, taskId, options) {
  const intervalMs = Math.max(1000, Number(options.pollInterval || DEFAULT_POLL_INTERVAL_MS / 1000) * 1000);
  const timeoutMs = Math.max(intervalMs, Number(options.timeoutSec || DEFAULT_TIMEOUT_MS / 1000) * 1000);
  const startedAt = Date.now();

  while (true) {
    const task = await client.getTask(taskId);
    const status = String(task.status || "").toLowerCase();
    console.log(`Task ${taskId} status: ${status || "unknown"}`);

    if (TERMINAL_STATUSES.has(status)) {
      if (status !== "succeeded") {
        const message = task.error ? `${task.error.code || "task_error"}: ${task.error.message || "task failed"}` : `Task ended with status ${status}`;
        throw new Error(message);
      }
      return task;
    }

    if (Date.now() - startedAt > timeoutMs) {
      throw new Error(`Timed out waiting for task ${taskId} after ${Math.round(timeoutMs / 1000)} seconds.`);
    }

    await sleep(intervalMs);
  }
}

async function maybeDownloadTaskOutputs(task, downloadDir) {
  const urls = collectOutputUrls(task.content || {});
  if (urls.length === 0) {
    console.log("No downloadable output URLs found in task content.");
    return;
  }

  console.log(`Downloading ${urls.length} output file(s) to ${downloadDir}`);
  for (let index = 0; index < urls.length; index += 1) {
    const item = urls[index];
    const filename = await buildDownloadFilename(item, index);
    const targetPath = path.join(downloadDir, filename);
    await downloadToFile(item.url, targetPath);
    console.log(`Saved ${item.key} -> ${targetPath}`);
  }
}

function collectOutputUrls(value, prefix = "content") {
  const results = [];

  if (typeof value === "string") {
    if (isHttpUrl(value)) {
      results.push({ key: prefix, url: value });
    }
    return results;
  }

  if (Array.isArray(value)) {
    value.forEach((item, index) => {
      results.push(...collectOutputUrls(item, `${prefix}-${index}`));
    });
    return results;
  }

  if (!value || typeof value !== "object") {
    return results;
  }

  for (const [key, child] of Object.entries(value)) {
    const nextPrefix = `${prefix}.${key}`;
    if ((key === "url" || key.endsWith("_url")) && typeof child === "string" && isHttpUrl(child)) {
      results.push({ key: nextPrefix, url: child });
      continue;
    }
    results.push(...collectOutputUrls(child, nextPrefix));
  }

  return dedupeBy(results, (item) => `${item.key}|${item.url}`);
}

async function buildDownloadFilename(item, index) {
  const url = new URL(item.url);
  const pathname = url.pathname || "";
  let extension = path.extname(pathname);
  if (!extension) {
    extension = await inferExtensionFromUrl(item.url);
  }

  if (!extension) {
    extension = item.key.includes("video") ? ".mp4" : ".bin";
  }

  const safeKey = item.key.replace(/[^a-zA-Z0-9._-]+/g, "_").replace(/^_+|_+$/g, "");
  return `${String(index + 1).padStart(2, "0")}-${safeKey}${extension}`;
}

async function inferExtensionFromUrl(url) {
  const response = await fetch(url, { method: "HEAD" }).catch(() => null);
  if (!response || !response.ok) {
    return "";
  }
  return extensionFromContentType(response.headers.get("content-type"));
}

async function downloadToFile(url, targetPath) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Download failed for ${url}: ${response.status} ${response.statusText}`);
  }

  const buffer = Buffer.from(await response.arrayBuffer());
  await fs.writeFile(targetPath, buffer);
}

async function requestJson(url, init) {
  const response = await fetch(url, init);
  const text = await response.text();
  const data = text ? tryParseJson(text) : {};

  if (!response.ok) {
    const details = data && typeof data === "object"
      ? JSON.stringify(data)
      : text || `${response.status} ${response.statusText}`;
    throw new Error(`Ark API request failed: ${response.status} ${response.statusText} - ${details}`);
  }

  return data;
}

function parseArgv(argv) {
  let command = null;
  const options = {};

  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];

    if (!token.startsWith("-") && command === null) {
      command = token;
      continue;
    }

    if (token === "--help" || token === "-h") {
      options.help = true;
      continue;
    }

    if (!token.startsWith("--")) {
      throw new Error(`Unexpected argument: ${token}`);
    }

    const eqIndex = token.indexOf("=");
    const keyPart = eqIndex >= 0 ? token.slice(2, eqIndex) : token.slice(2);
    const rawValue = eqIndex >= 0 ? token.slice(eqIndex + 1) : null;
    const key = toCamelCase(keyPart);
    const expectsValue = rawValue !== null || (argv[index + 1] && !argv[index + 1].startsWith("--"));
    const value = rawValue !== null ? rawValue : expectsValue ? argv[++index] : true;
    assignOption(options, key, value);
  }

  return { command, options };
}

function assignOption(options, key, value) {
  const repeatable = new Set([
    "imageUrl",
    "imageFile",
    "videoUrl",
    "videoFile",
    "audioUrl",
    "audioFile",
    "draftTaskId",
    "filterTaskId",
  ]);

  if (repeatable.has(key)) {
    if (!Array.isArray(options[key])) {
      options[key] = [];
    }
    options[key].push(value);
    return;
  }

  options[key] = value;
}

function toCamelCase(value) {
  return value.replace(/-([a-z])/g, (_, letter) => letter.toUpperCase());
}

function toArray(value) {
  if (value === undefined || value === null) {
    return [];
  }
  return Array.isArray(value) ? value : [value];
}

function applyIfDefined(target, key, value) {
  if (value !== undefined && value !== null && value !== "") {
    target[key] = value;
  }
}

function applyNumberIfDefined(target, key, value) {
  if (value === undefined || value === null || value === "") {
    return;
  }

  const parsed = Number(value);
  if (!Number.isFinite(parsed)) {
    throw new Error(`Expected a number for ${key}, got: ${value}`);
  }
  target[key] = parsed;
}

function applyBooleanIfDefined(target, key, value) {
  if (value === undefined || value === null || value === "") {
    return;
  }
  target[key] = parseBoolean(value);
}

function parseBoolean(value, defaultValue) {
  if (value === undefined || value === null || value === "") {
    if (defaultValue !== undefined) {
      return defaultValue;
    }
    throw new Error("Expected a boolean value.");
  }

  if (typeof value === "boolean") {
    return value;
  }

  const normalized = String(value).trim().toLowerCase();
  if (["true", "1", "yes", "y", "on"].includes(normalized)) {
    return true;
  }
  if (["false", "0", "no", "n", "off"].includes(normalized)) {
    return false;
  }

  throw new Error(`Invalid boolean value: ${value}`);
}

function requireOption(value, message) {
  if (value === undefined || value === null || value === "") {
    throw new Error(message);
  }
  return value;
}

function assertTaskId(response) {
  const taskId = response.id || response.task_id || response.taskId;
  if (!taskId) {
    throw new Error(`Could not find task ID in create response: ${JSON.stringify(response)}`);
  }
  return taskId;
}

function resolveDownloadDir(downloadDir, taskId) {
  if (downloadDir) {
    return path.resolve(downloadDir);
  }
  return path.resolve(process.cwd(), DEFAULT_DOWNLOAD_ROOT, taskId);
}

async function ensureDir(dirPath) {
  await fs.mkdir(dirPath, { recursive: true });
}

async function writeJson(filePath, data) {
  await fs.writeFile(filePath, JSON.stringify(data, null, 2));
}

async function readJson(filePath) {
  const content = await fs.readFile(filePath, "utf8");
  return JSON.parse(content);
}

function sanitizePayloadForStorage(value) {
  if (Array.isArray(value)) {
    return value.map((item) => sanitizePayloadForStorage(item));
  }

  if (!value || typeof value !== "object") {
    if (typeof value === "string" && isDataUrl(value)) {
      return redactDataUrl(value);
    }
    return value;
  }

  const result = {};
  for (const [key, child] of Object.entries(value)) {
    if (typeof child === "string" && isDataUrl(child)) {
      result[key] = redactDataUrl(child);
      continue;
    }
    result[key] = sanitizePayloadForStorage(child);
  }
  return result;
}

function isDataUrl(value) {
  return /^data:[^;]+;base64,/i.test(String(value));
}

function redactDataUrl(value) {
  const text = String(value);
  const prefix = text.slice(0, text.indexOf(","));
  return `[REDACTED_DATA_URL ${prefix};bytes=${text.length}]`;
}

function tryParseJson(text) {
  try {
    return JSON.parse(text);
  } catch {
    return text;
  }
}

function stripTrailingSlash(url) {
  return String(url).replace(/\/+$/, "");
}

function extensionFromContentType(contentType) {
  if (!contentType) {
    return "";
  }

  const normalized = contentType.split(";")[0].trim().toLowerCase();
  for (const [extension, mime] of MIME_BY_EXTENSION.entries()) {
    if (mime === normalized) {
      return extension;
    }
  }
  return "";
}

function isHttpUrl(value) {
  return /^https?:\/\//i.test(String(value));
}

async function fileToDataUrl(filePath) {
  const absolutePath = path.resolve(filePath);
  const buffer = await fs.readFile(absolutePath);
  const extension = path.extname(absolutePath).toLowerCase();
  const mimeType = MIME_BY_EXTENSION.get(extension);

  if (!mimeType) {
    throw new Error(`Unsupported file extension for data URL conversion: ${extension || "<none>"} (${absolutePath})`);
  }

  return `data:${mimeType};base64,${buffer.toString("base64")}`;
}

function printSummary(task, downloadDir) {
  const lines = [
    `Task ID: ${task.id || "unknown"}`,
    `Model: ${task.model || "unknown"}`,
    `Status: ${task.status || "unknown"}`,
  ];

  if (task.content && task.content.video_url) {
    lines.push(`Video URL: ${task.content.video_url}`);
  }
  if (task.content && task.content.last_frame_url) {
    lines.push(`Last frame URL: ${task.content.last_frame_url}`);
  }
  if (downloadDir) {
    lines.push(`Download dir: ${downloadDir}`);
  }

  console.log(lines.join("\n"));
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function dedupeBy(items, keyFn) {
  const seen = new Set();
  const result = [];

  for (const item of items) {
    const key = keyFn(item);
    if (seen.has(key)) {
      continue;
    }
    seen.add(key);
    result.push(item);
  }

  return result;
}

main().catch((error) => {
  console.error(error.stack || error.message || String(error));
  process.exitCode = 1;
});
