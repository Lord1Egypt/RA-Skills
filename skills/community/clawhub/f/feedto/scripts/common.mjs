import fs from "node:fs/promises";
import { constants as fsConstants } from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export const scriptDir = __dirname;
export const stateDir = process.env.FEEDTO_STATE_DIR || path.join(os.homedir(), ".openclaw", "state", "feedto");

export const paths = {
  stateDir,
  queue: path.join(stateDir, "queue.json"),
  status: path.join(stateDir, "status.json"),
  pid: path.join(stateDir, "daemon.pid.json"),
  daemonLog: path.join(stateDir, "daemon.log"),
};

const DEFAULT_FETCH_TIMEOUT_MS = Number.parseInt(process.env.FEEDTO_HTTP_TIMEOUT_MS || "15000", 10);
const DEFAULT_MAX_LOG_BYTES = Number.parseInt(process.env.FEEDTO_MAX_LOG_BYTES || `${1024 * 1024}`, 10);

export function getApiUrl() {
  return (process.env.FEEDTO_API_URL || "https://feedto.ai").replace(/\/+$/, "");
}

export function getApiKey() {
  return (process.env.FEEDTO_API_KEY || "").trim();
}

export function requireApiKey() {
  const apiKey = getApiKey();
  if (!apiKey) {
    throw new Error("FEEDTO_API_KEY not set");
  }
  return apiKey;
}

export async function ensureStateDir() {
  await fs.mkdir(stateDir, { recursive: true });
}

export async function readJson(filePath, fallback) {
  try {
    const content = await fs.readFile(filePath, "utf8");
    return JSON.parse(content);
  } catch (error) {
    if (error && typeof error === "object" && "code" in error && error.code === "ENOENT") {
      return fallback;
    }
    throw error;
  }
}

export async function writeJsonAtomic(filePath, data) {
  await ensureStateDir();
  const tempPath = `${filePath}.${process.pid}.${Date.now()}.tmp`;
  await fs.writeFile(tempPath, `${JSON.stringify(data, null, 2)}\n`, "utf8");
  await fs.rename(tempPath, filePath);
}

async function acquireLock(lockPath, timeoutMs = 5_000) {
  const startedAt = Date.now();
  while (true) {
    try {
      await fs.mkdir(lockPath);
      return;
    } catch (error) {
      if (!(error && typeof error === "object" && "code" in error && error.code === "EEXIST")) {
        throw error;
      }
      if (Date.now() - startedAt >= timeoutMs) {
        throw new Error(`Timed out waiting for lock ${lockPath}`);
      }
      await sleep(50);
    }
  }
}

async function releaseLock(lockPath) {
  await fs.rm(lockPath, { recursive: true, force: true });
}

export async function withLock(name, fn) {
  const lockPath = path.join(stateDir, `${name}.lock`);
  await ensureStateDir();
  await acquireLock(lockPath);
  try {
    return await fn();
  } finally {
    await releaseLock(lockPath);
  }
}

export function normalizeFeed(raw) {
  if (!raw || typeof raw !== "object") return null;
  const feed = raw;
  if (typeof feed.id !== "string" || typeof feed.content !== "string" || typeof feed.created_at !== "string") {
    return null;
  }

  return {
    id: feed.id,
    type: typeof feed.type === "string" ? feed.type : "text",
    title: typeof feed.title === "string" ? feed.title : null,
    url: typeof feed.url === "string" ? feed.url : null,
    content: feed.content,
    metadata: feed.metadata && typeof feed.metadata === "object" ? feed.metadata : {},
    created_at: feed.created_at,
  };
}

export async function getQueuedFeeds() {
  const queue = await readJson(paths.queue, []);
  if (!Array.isArray(queue)) return [];
  return queue.map(normalizeFeed).filter(Boolean);
}

export async function enqueueFeeds(feeds) {
  return withLock("queue", async () => {
    const existing = await getQueuedFeeds();
    const byId = new Map(existing.map((feed) => [feed.id, feed]));

    for (const rawFeed of feeds) {
      const feed = normalizeFeed(rawFeed);
      if (!feed) continue;
      if (!byId.has(feed.id)) {
        byId.set(feed.id, feed);
      }
    }

    const updated = Array.from(byId.values()).sort((a, b) => a.created_at.localeCompare(b.created_at));
    await writeJsonAtomic(paths.queue, updated);
    return updated;
  });
}

export async function removeQueuedFeedIds(ids) {
  const wanted = new Set(ids.filter((id) => typeof id === "string"));
  return withLock("queue", async () => {
    const queue = await getQueuedFeeds();
    const remaining = queue.filter((feed) => !wanted.has(feed.id));
    await writeJsonAtomic(paths.queue, remaining);
    return remaining;
  });
}

export async function updateStatus(patch) {
  return withLock("status", async () => {
    const current = await readJson(paths.status, {});
    const next = {
      stateDir,
      apiUrl: getApiUrl(),
      ...(current && typeof current === "object" ? current : {}),
      ...(patch && typeof patch === "object" ? patch : {}),
      updatedAt: new Date().toISOString(),
    };
    await writeJsonAtomic(paths.status, next);
    return next;
  });
}

export async function fetchJson(url, init = {}) {
  const timeoutMs = Number.isFinite(init.timeoutMs) ? init.timeoutMs : DEFAULT_FETCH_TIMEOUT_MS;
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const response = await fetch(url, {
      ...init,
      signal: init.signal || controller.signal,
    });
    const text = await response.text();
    let data = null;

    try {
      data = text ? JSON.parse(text) : null;
    } catch {
      data = null;
    }

    return {
      ok: response.ok,
      status: response.status,
      text,
      data,
    };
  } finally {
    clearTimeout(timer);
  }
}

async function trimLogIfNeeded() {
  const maxBytes = DEFAULT_MAX_LOG_BYTES;
  if (!Number.isFinite(maxBytes) || maxBytes <= 0) return;

  try {
    const stat = await fs.stat(paths.daemonLog);
    if (stat.size <= maxBytes) return;

    const content = await fs.readFile(paths.daemonLog, "utf8");
    const keepBytes = Math.floor(maxBytes / 2);
    const tail = Buffer.from(content).subarray(Math.max(0, Buffer.byteLength(content) - keepBytes)).toString("utf8");
    await fs.writeFile(paths.daemonLog, `[truncated ${new Date().toISOString()}]\n${tail}`, "utf8");
  } catch (error) {
    if (error && typeof error === "object" && "code" in error && error.code === "ENOENT") {
      return;
    }
    throw error;
  }
}

export async function appendLog(message) {
  await ensureStateDir();
  await trimLogIfNeeded();
  await fs.appendFile(paths.daemonLog, `${new Date().toISOString()} ${message}\n`, "utf8");
}

export function isProcessAlive(pid) {
  if (!pid || !Number.isInteger(pid)) return false;
  try {
    process.kill(pid, 0);
    return true;
  } catch {
    return false;
  }
}

export async function canAccess(filePath) {
  try {
    await fs.access(filePath, fsConstants.F_OK);
    return true;
  } catch {
    return false;
  }
}

export function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

export function formatAgeMs(timestamp) {
  if (!timestamp) return null;
  const value = typeof timestamp === "string" ? Date.parse(timestamp) : Number(timestamp);
  if (!Number.isFinite(value) || value <= 0) return null;

  const deltaMs = Math.max(0, Date.now() - value);
  if (deltaMs < 1000) return "just now";
  if (deltaMs < 60_000) return `${Math.floor(deltaMs / 1000)}s ago`;
  if (deltaMs < 3_600_000) return `${Math.floor(deltaMs / 60_000)}m ago`;
  return `${Math.floor(deltaMs / 3_600_000)}h ago`;
}

export async function getRuntimeSnapshot() {
  const [queue, status, pidInfo] = await Promise.all([
    getQueuedFeeds(),
    readJson(paths.status, {}),
    readJson(paths.pid, {}),
  ]);

  const pid = typeof pidInfo.pid === "number" ? pidInfo.pid : null;
  const heartbeatAt = typeof status.heartbeatAt === "string" ? status.heartbeatAt : null;

  return {
    apiUrl: getApiUrl(),
    stateDir,
    queueLength: queue.length,
    oldestQueuedAt: queue[0]?.created_at || null,
    newestQueuedAt: queue[queue.length - 1]?.created_at || null,
    pid,
    processAlive: pid ? isProcessAlive(pid) : false,
    state: typeof status.state === "string" ? status.state : "unknown",
    mode: typeof status.mode === "string" ? status.mode : null,
    message: typeof status.message === "string" ? status.message : null,
    lastError: typeof status.lastError === "string" ? status.lastError : null,
    heartbeatAt,
    heartbeatAge: formatAgeMs(heartbeatAt),
    lastFeedAt: typeof status.lastFeedAt === "string" ? status.lastFeedAt : null,
    lastFeedAge: formatAgeMs(status.lastFeedAt),
    lastBackfillCount: Number.isFinite(status.lastBackfillCount) ? status.lastBackfillCount : null,
    updatedAt: typeof status.updatedAt === "string" ? status.updatedAt : null,
  };
}
