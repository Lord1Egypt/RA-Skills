#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');
// Note: child_process is not used directly; task delivery uses HTTP POST to localhost plugin endpoint
const { randomUUID } = require('crypto');

const QUEUE_PATH = path.join(__dirname, 'queue.json');
const HISTORY_PATH = path.join(__dirname, 'history.json');
const LOCK_PATH = path.join(__dirname, 'daemon.lock');
const LOG_PATH = path.join(__dirname, 'daemon.log');
const INTERVAL_MS = 30 * 1000;
const HISTORY_LIMIT = 100;

// Load TARGETS from user config: ~/.openclaw/queue/targets.json
// Format: { "myagent": "agent:myagent:main", "other": "agent:other:main" }
// If not found, daemon accepts full session keys (e.g. "agent:main:main") as-is.
const TARGETS_PATH = path.join(path.dirname(QUEUE_PATH), 'targets.json');
function loadTargets() {
  try {
    const raw = fs.readFileSync(TARGETS_PATH, 'utf8');
    return JSON.parse(raw);
  } catch (_) {
    return {};
  }
}

function log(line) {
  const ts = new Date().toISOString();
  fs.appendFileSync(LOG_PATH, `[${ts}] ${line}\n`);
}

function withLock(fn) {
  let fd;
  try {
    fd = fs.openSync(LOCK_PATH, 'wx');
  } catch (err) {
    log('Lock exists, skipping tick.');
    return;
  }
  try {
    fn();
  } finally {
    try { fs.closeSync(fd); } catch (_) {}
    try { fs.unlinkSync(LOCK_PATH); } catch (_) {}
  }
}

function loadQueue() {
  try {
    const raw = fs.readFileSync(QUEUE_PATH, 'utf8');
    const q = JSON.parse(raw);
    return Array.isArray(q) ? q : [];
  } catch (_) {
    return [];
  }
}

function saveQueue(queue) {
  fs.writeFileSync(QUEUE_PATH, JSON.stringify(queue, null, 2));
}

function loadHistory() {
  try {
    const raw = fs.readFileSync(HISTORY_PATH, 'utf8');
    const h = JSON.parse(raw);
    return Array.isArray(h) ? h : [];
  } catch (_) {
    return [];
  }
}

function appendHistory(entry) {
  const history = loadHistory();
  history.push(entry);
  const trimmed = history.length > HISTORY_LIMIT ? history.slice(-HISTORY_LIMIT) : history;
  fs.writeFileSync(HISTORY_PATH, JSON.stringify(trimmed, null, 2));
}

function recordHistory(item, status, errorMessage) {
  const entry = {
    id: item.id,
    to: item.to,
    task: item.task,
    runAt: item.runAt,
    firedAt: new Date().toISOString(),
    status,
  };
  if (status === 'failed' && errorMessage) entry.error = errorMessage;
  appendHistory(entry);
}

function sendMessage(to, task) {
  const TARGETS = loadTargets();
  // Resolve: check targets.json aliases first, then accept full session key directly
  if (!TARGETS[to] && !to.startsWith('agent:')) {
    log(`Unknown target: ${to} — not in targets.json and not a full session key. Task skipped.`);
    return;
  }
  const resolvedTo = TARGETS[to] || to; // use mapped alias or raw session key
  // POST to queue-wake plugin — enqueues system event + calls requestHeartbeatNow for exact-time delivery
  const http = require('http');
  const body = JSON.stringify({ to: resolvedTo, task });
  return new Promise((resolve, reject) => {
    const req = http.request({
      hostname: '127.0.0.1',
      port: 18789,
      path: '/api/queue-wake',
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(body) }
    }, (res) => {
      let data = '';
      res.on('data', d => data += d);
      res.on('end', () => {
        if (res.statusCode === 200) resolve(data);
        else reject(new Error(`queue-wake returned ${res.statusCode}: ${data}`));
      });
    });
    req.on('error', reject);
    req.setTimeout(5000, () => { req.destroy(new Error('timeout')); });
    req.write(body);
    req.end();
  });
}

async function tick() {
  withLock(async () => {
    const now = Date.now();
    const queue = loadQueue();
    const remaining = [];
    for (const item of queue) {
      const runAt = Date.parse(item.runAt || '');
      if (!runAt || runAt > now) {
        remaining.push(item);
        continue;
      }
      // Drop TTL-expired items (delivery window passed)
      const ttlMs = (item.ttl || 300) * 1000;
      if (now > runAt + ttlMs) {
        log(`Dropped ${item.id} (TTL expired ${Math.round((now - runAt - ttlMs) / 1000)}s ago)`);
        recordHistory(item, 'expired');
        continue;
      }
      try {
        await sendMessage(item.to, item.task);
        log(`Sent ${item.id} to ${item.to}`);
        recordHistory(item, 'fired');
        if (item.then) {
          const chainedAt = new Date().toISOString();
          remaining.push({
            id: randomUUID(),
            to: item.to,
            task: item.then,
            runAt: chainedAt,
            createdAt: chainedAt,
            ttl: item.ttl || 300,
          });
        }
      } catch (err) {
        const msg = err && err.message ? err.message : String(err);
        log(`Error sending ${item.id}: ${msg}`);
        recordHistory(item, 'failed', msg);
        remaining.push(item);
      }
    }
    saveQueue(remaining);
  });
}

log('Daemon started.');
setInterval(tick, INTERVAL_MS);
setTimeout(tick, 1000);
