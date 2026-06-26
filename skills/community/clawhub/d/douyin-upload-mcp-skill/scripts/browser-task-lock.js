import { mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { homedir } from 'node:os';

const STATE_DIR = process.env.DOUYIN_MONITOR_STATE_DIR || join(homedir(), '.openclaw', 'workspace', 'douyin-ops');
const LOCK_DIR = process.env.DOUYIN_BROWSER_TASK_LOCK || join(STATE_DIR, 'browser-task.lock');
const LOCK_META = join(LOCK_DIR, 'meta.json');
const PUBLISH_PRIORITY_PATH = process.env.DOUYIN_BROWSER_PUBLISH_PRIORITY || join(STATE_DIR, 'browser-publish-priority.json');
const DEFAULT_TIMEOUT_MS = 180_000;
const STALE_MS = Number(process.env.DOUYIN_BROWSER_TASK_LOCK_STALE_MS || 6 * 60 * 60_000);
const PUBLISH_PRIORITY_STALE_MS = Number(process.env.DOUYIN_BROWSER_PUBLISH_PRIORITY_STALE_MS || 2 * 60 * 60_000);

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function readJson(path) {
  try {
    return JSON.parse(readFileSync(path, 'utf8'));
  } catch {
    return null;
  }
}

function readLockMeta() {
  return readJson(LOCK_META);
}

export function readBrowserTaskLockMeta() {
  return readLockMeta();
}

export function readPublishPriorityMeta() {
  return readJson(PUBLISH_PRIORITY_PATH);
}

function processAlive(pid) {
  const value = Number(pid);
  if (!Number.isInteger(value) || value <= 0) return false;
  try {
    process.kill(value, 0);
    return true;
  } catch (err) {
    return err?.code === 'EPERM';
  }
}

function isPublishOwner(owner) {
  return String(owner || '').startsWith('publish:');
}

function isStale(meta, staleMs = STALE_MS) {
  const createdAt = Date.parse(meta?.createdAt || '');
  if (!createdAt) return true;
  if (processAlive(meta?.pid)) return false;
  return Date.now() - createdAt > staleMs;
}

export function publishPriorityActive() {
  const meta = readPublishPriorityMeta();
  if (!meta) return false;
  if (isStale(meta, PUBLISH_PRIORITY_STALE_MS)) {
    rmSync(PUBLISH_PRIORITY_PATH, { force: true });
    return false;
  }
  return isPublishOwner(meta.owner);
}

function writePublishPriority(owner) {
  mkdirSync(dirname(PUBLISH_PRIORITY_PATH), { recursive: true });
  const meta = {
    owner,
    pid: process.pid,
    createdAt: new Date().toISOString(),
  };
  writeFileSync(PUBLISH_PRIORITY_PATH, JSON.stringify(meta, null, 2));
  return () => {
    const current = readPublishPriorityMeta();
    if (current?.pid === process.pid && current?.owner === owner) {
      rmSync(PUBLISH_PRIORITY_PATH, { force: true });
    }
  };
}

export function shouldDeferToPublish(owner = '') {
  if (isPublishOwner(owner)) return false;
  const lock = readLockMeta();
  return isPublishOwner(lock?.owner) || publishPriorityActive();
}

export async function acquireBrowserTaskLock(owner, timeoutMs = DEFAULT_TIMEOUT_MS, options = {}) {
  mkdirSync(dirname(LOCK_DIR), { recursive: true });
  const isPublish = isPublishOwner(owner) || options.priority === 'publish';
  const clearPublishPriority = isPublish ? writePublishPriority(owner) : null;
  const deferToPublish = options.deferToPublish !== false && !isPublish;
  const pollMs = Number(options.pollMs || 500);
  const deadline = Date.now() + timeoutMs;
  try {
    while (Date.now() < deadline) {
      if (deferToPublish && shouldDeferToPublish(owner)) {
        if (options.skipIfPublishActive) {
          if (clearPublishPriority) clearPublishPriority();
          return null;
        }
        await sleep(pollMs);
        continue;
      }
      try {
        mkdirSync(LOCK_DIR);
        writeFileSync(LOCK_META, JSON.stringify({
          owner,
          pid: process.pid,
          priority: isPublish ? 'publish' : 'normal',
          createdAt: new Date().toISOString(),
        }, null, 2));
        let released = false;
        return () => {
          if (released) return;
          released = true;
          const current = readLockMeta();
          if (current?.pid === process.pid && current?.owner === owner) {
            rmSync(LOCK_DIR, { recursive: true, force: true });
          }
          if (clearPublishPriority) clearPublishPriority();
        };
      } catch (err) {
        if (err?.code !== 'EEXIST') throw err;
        const meta = readLockMeta();
        if (isStale(meta)) {
          rmSync(LOCK_DIR, { recursive: true, force: true });
          continue;
        }
        await sleep(pollMs);
      }
    }
  } catch (err) {
    if (clearPublishPriority) clearPublishPriority();
    throw err;
  }
  const meta = readLockMeta();
  const publishPriority = readPublishPriorityMeta();
  if (clearPublishPriority) clearPublishPriority();
  throw new Error(`browser_task_lock_timeout: ${JSON.stringify({ lock: meta || {}, publishPriority: publishPriority || {} })}`);
}
