'use strict';

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const {
  PRIVATE_FILE_MODE,
  bestEffortChmod,
  ensurePrivateDir,
  writePrivateFile,
  readMailboxStateFile,
  writeMergedMailboxStateFile,
} = require('./state');

const DEFAULT_CHANNEL = 'evomap-hub';
const SCHEMA_VERSION = 1;
const PROXY_PROTOCOL_VERSION = '0.1.0';
const DEFAULT_MAX_JSONL_LINE_BYTES = 16 * 1024 * 1024;
const JSONL_READ_CHUNK_BYTES = 64 * 1024;

// Merge `fields` into `target` while stripping keys that can mutate the
// prototype chain. Mailbox rows are persisted as JSONL and rebuilt on
// startup; without this filter a crafted messages.jsonl line containing
// __proto__/constructor/prototype could pollute Object.prototype during
// _rebuildIndex (see GHSA-2cjr-5v3h-v2w4).
function safeAssign(target, fields) {
  if (!fields || typeof fields !== 'object') return target;
  const keys = Object.keys(fields);
  for (let i = 0; i < keys.length; i++) {
    const k = keys[i];
    if (k === '__proto__' || k === 'constructor' || k === 'prototype') continue;
    target[k] = fields[k];
  }
  return target;
}

function sanitizeRow(row) {
  if (!row || typeof row !== 'object') return row;
  const out = {};
  safeAssign(out, row);
  if (out.fields && typeof out.fields === 'object') {
    const cleanFields = {};
    safeAssign(cleanFields, out.fields);
    out.fields = cleanFields;
  }
  return out;
}

// --- UUID v7 (RFC 9562) ---
// Bits 0-47: unix_ts_ms, Bits 48-51: ver=0b0111, Bits 52-63: rand_a,
// Bits 64-65: var=0b10, Bits 66-127: rand_b

function generateUUIDv7() {
  const now = Date.now();
  const msHex = now.toString(16).padStart(12, '0');

  const bytes = crypto.randomBytes(10);
  bytes[0] = (bytes[0] & 0x0f) | 0x70; // version 7
  bytes[2] = (bytes[2] & 0x3f) | 0x80; // variant 10

  const randHex = bytes.toString('hex');

  // Standard UUID format: 8-4-4-4-12 (32 hex total)
  return [
    msHex.slice(0, 8),
    msHex.slice(8, 12),
    randHex.slice(0, 4),
    randHex.slice(4, 8),
    randHex.slice(8, 20),
  ].join('-');
}

// --- JSONL file helpers ---

function safeParse(payload) {
  if (payload == null) return null;
  if (typeof payload !== 'string') return payload;
  try { return JSON.parse(payload); } catch { return payload; }
}

// Round-9: the round-8 cross-process append lock (§21.7) was REMOVED.
// Its premise -- that fs.appendFileSync to a regular file can interleave
// bytes mid-line unless each write stays under PIPE_BUF (512 B darwin,
// 4096 B linux) -- conflated two different POSIX guarantees. PIPE_BUF
// atomicity is defined for PIPES/FIFOs, not regular files. A single
// O_APPEND write() to a regular file is positioned atomically at EOF and
// is not interleaved with other appenders on the local filesystems evolver
// uses (~/.evomap); this was verified empirically on darwin/APFS --
// concurrent 4 KB..1 MB appends from 6 writers produced zero torn lines.
// So the lock guarded a non-problem. Worse, its 5 s deadline with a
// busy-wait (Atomics.wait, then a spin-loop fallback) ran on the single
// JS thread, so under any real contention it BLOCKED the event loop --
// starving the very heartbeat/SSE/HTTP it shared the process with, i.e.
// it could itself produce the "process alive but inert" symptom it claimed
// to prevent. fs.appendFileSync writes the whole buffer with O_APPEND, so
// a single record lands as one atomic append.
//
// Windows note: PIPE_BUF is a POSIX concept; it does not exist on Windows.
// Windows NTFS provides the same atomicity guarantee for O_APPEND writes to
// regular files that POSIX local filesystems do, so the removal above is
// equally valid on Windows. No platform-specific code is needed here.
function jsonlLineForWrite(obj, opts = {}) {
  const line = JSON.stringify(obj) + '\n';
  const maxLineBytes = Math.max(1, Math.floor(Number(opts.maxLineBytes) || resolveMaxJsonlLineBytes()));
  const lineBytes = Buffer.byteLength(line, 'utf8');
  if (lineBytes > maxLineBytes) {
    const err = new Error(`mailbox JSONL line is ${lineBytes} bytes; maximum is ${maxLineBytes} bytes`);
    err.code = 'MAILBOX_JSONL_LINE_TOO_LARGE';
    err.lineBytes = lineBytes;
    err.maxLineBytes = maxLineBytes;
    throw err;
  }
  return line;
}

function appendLine(filePath, obj) {
  const line = jsonlLineForWrite(obj);
  fs.appendFileSync(filePath, line, { encoding: 'utf8', mode: PRIVATE_FILE_MODE });
  bestEffortChmod(filePath, PRIVATE_FILE_MODE);
}

function resolveMaxJsonlLineBytes(env = process.env) {
  const raw = Number(env.EVOMAP_MAILBOX_MAX_LINE_BYTES);
  if (Number.isFinite(raw) && raw > 0) return Math.floor(raw);
  return DEFAULT_MAX_JSONL_LINE_BYTES;
}

function forEachJsonLine(filePath, onRow, opts = {}) {
  const stats = { parsed: 0, corrupt: 0, overlong: 0 };
  if (!fs.existsSync(filePath)) return stats;

  const maxLineBytes = Math.max(1, Math.floor(Number(opts.maxLineBytes) || resolveMaxJsonlLineBytes()));
  const chunk = Buffer.allocUnsafe(JSONL_READ_CHUNK_BYTES);
  let fd = null;
  let parts = [];
  let lineBytes = 0;
  let dropping = false;

  const resetLine = () => {
    parts = [];
    lineBytes = 0;
    dropping = false;
  };

  const appendSegment = (segment) => {
    if (!segment || segment.length === 0 || dropping) return;
    if (lineBytes + segment.length > maxLineBytes) {
      parts = [];
      lineBytes = 0;
      dropping = true;
      return;
    }
    parts.push(Buffer.from(segment));
    lineBytes += segment.length;
  };

  const finishLine = (hasNewline = false) => {
    const totalLineBytes = lineBytes + (hasNewline ? 1 : 0);
    if (dropping) {
      stats.overlong += 1;
      resetLine();
      return;
    }
    if (totalLineBytes > maxLineBytes) {
      stats.overlong += 1;
      resetLine();
      return;
    }
    if (lineBytes === 0) {
      resetLine();
      return;
    }
    const trimmed = Buffer.concat(parts, lineBytes).toString('utf8').trim();
    resetLine();
    if (!trimmed) return;
    try {
      onRow(JSON.parse(trimmed));
      stats.parsed += 1;
    } catch {
      stats.corrupt += 1;
    }
  };

  try {
    fd = fs.openSync(filePath, 'r');
    while (true) {
      const bytesRead = fs.readSync(fd, chunk, 0, chunk.length, null);
      if (bytesRead <= 0) break;
      let start = 0;
      for (let i = 0; i < bytesRead; i++) {
        if (chunk[i] !== 0x0a) continue;
        appendSegment(chunk.subarray(start, i));
        finishLine(true);
        start = i + 1;
      }
      if (start < bytesRead) appendSegment(chunk.subarray(start, bytesRead));
    }
    finishLine();
  } catch (err) {
    stats.read_failed = 1;
    const detail = err && err.message ? err.message : String(err);
    const wrapped = new Error(`failed to read mailbox JSONL ${filePath}: ${detail}`);
    wrapped.code = 'MAILBOX_JSONL_READ_FAILED';
    wrapped.stats = stats;
    wrapped.cause = err;
    throw wrapped;
  } finally {
    if (fd !== null) {
      try { fs.closeSync(fd); } catch { /* ignore close errors */ }
    }
  }
  return stats;
}

// --- In-memory index that backs JSONL persistence ---

class MailboxStore {
  constructor(dataDir) {
    if (!dataDir) throw new Error('dataDir is required');
    ensurePrivateDir(dataDir);
    this.dataDir = dataDir;

    this._messagesFile = path.join(dataDir, 'messages.jsonl');
    this._stateFile = path.join(dataDir, 'state.json');
    bestEffortChmod(this._messagesFile, PRIVATE_FILE_MODE);
    bestEffortChmod(this._stateFile, PRIVATE_FILE_MODE);

    // in-memory indexes
    this._messages = new Map();          // id -> message object
    this._outbound = [];                 // ordered outbound refs (id)
    this._inbound = [];                  // ordered inbound refs (id)

    this._state = {};                    // key-value state (cursors, node_id, etc.)

    this._loadState();
    this._rebuildIndex();
  }

  _loadState() {
    this._state = readMailboxStateFile(this._stateFile) || {};
    const existingVersion = this._state._schema_version || 0;
    const beforeMigrationState = { ...this._state };
    if (existingVersion < SCHEMA_VERSION) {
      this._runMigrations(existingVersion, SCHEMA_VERSION);
    }
    this._state._schema_version = SCHEMA_VERSION;
    const updatedKeys = new Set(['_schema_version']);
    for (const key of Object.keys(this._state)) {
      if (this._state[key] !== beforeMigrationState[key]) updatedKeys.add(key);
    }
    for (const key of Object.keys(beforeMigrationState)) {
      if (!Object.prototype.hasOwnProperty.call(this._state, key)) updatedKeys.add(key);
    }
    this._persistState(updatedKeys);
  }

  _runMigrations(fromVersion, toVersion) {
    for (let v = fromVersion + 1; v <= toVersion; v++) {
      const migrator = MIGRATIONS[v];
      if (typeof migrator === 'function') {
        migrator(this);
      }
    }
  }

  _persistState(updatedKeys) {
    // Round-7 (§20.5): per-PID tmp path. Two evolver processes (daemon +
    // ad-hoc CLI / proxy + loop) writing to the same `${stateFile}.tmp`
    // would otherwise interleave: process B's writeFileSync truncates
    // A's tmp mid-write, then B's rename completes with B's truncated
    // payload as the final state.json. `state.json` holds the cached
    // node_secret after a hub rotation -- a torn write here is the
    // load-bearing trigger for the "401-loop -> reauth backoff -> dead
    // for 30 min..4 h" symptom this branch targets. Matches the
    // precedent set by _persistNodeSecret in src/gep/a2aProtocol.js.
    //
    // Use the shared merge helper so stale long-running stores cannot
    // resurrect an older node_secret tuple after another path rotates or clears
    // it directly on disk.
    this._state = writeMergedMailboxStateFile(this._stateFile, this._state, updatedKeys);
  }

  _rebuildIndex() {
    this._messages.clear();
    this._outbound = [];
    this._inbound = [];

    const TERMINAL = new Set(['synced', 'delivered', 'failed', 'rejected']);
    const stats = forEachJsonLine(this._messagesFile, (rawRow) => {
      const row = sanitizeRow(rawRow);
      if (!row || typeof row !== 'object') return;
      if (row._op === 'update') {
        const existing = this._messages.get(row.id);
        if (existing) safeAssign(existing, row.fields);
        return;
      }
      if (!row.id) return;
      this._messages.set(row.id, row);
    });
    this._lastRebuildStats = stats;
    for (const [id, msg] of this._messages) {
      if (!msg || typeof msg !== 'object') continue;
      if (TERMINAL.has(msg.status)) continue;
      if (msg.direction === 'outbound') this._outbound.push(id);
      else if (msg.direction === 'inbound') this._inbound.push(id);
    }
  }

  _appendMessage(msg) {
    appendLine(this._messagesFile, msg);
    this._messages.set(msg.id, msg);
    if (msg.direction === 'outbound') this._outbound.push(msg.id);
    else if (msg.direction === 'inbound') this._inbound.push(msg.id);
  }

  _appendUpdate(id, fields) {
    appendLine(this._messagesFile, { _op: 'update', id, fields });
    const existing = this._messages.get(id);
    if (existing) safeAssign(existing, fields);
  }

  _evictFromIndex(id) {
    const msg = this._messages.get(id);
    if (!msg) return;
    const arr = msg.direction === 'outbound' ? this._outbound : this._inbound;
    const idx = arr.indexOf(id);
    if (idx !== -1) arr.splice(idx, 1);
  }

  // --- Public API: send / writeInbound ---

  send({ type, payload, channel, priority, refId, expiresAt }) {
    const id = generateUUIDv7();
    const now = Date.now();
    const msg = {
      id,
      channel: channel || DEFAULT_CHANNEL,
      direction: 'outbound',
      type,
      status: 'pending',
      payload: safeParse(payload),
      priority: priority || 'normal',
      ref_id: refId || null,
      created_at: now,
      synced_at: null,
      expires_at: expiresAt || null,
      retry_count: 0,
      error: null,
    };
    this._appendMessage(msg);
    return { message_id: id, status: 'pending' };
  }

  writeInbound({ id, type, payload, channel, priority, refId, expiresAt }) {
    const msgId = id || generateUUIDv7();
    // At-least-once delivery from the Hub / retry loops can send the same
    // message id twice. Without idempotency, poll() and countPending() would
    // double-count the retry. See community PR #515.
    if (this._messages.has(msgId)) return msgId;

    const now = Date.now();
    const msg = {
      id: msgId,
      channel: channel || DEFAULT_CHANNEL,
      direction: 'inbound',
      type,
      status: 'pending',
      payload: safeParse(payload),
      priority: priority || 'normal',
      ref_id: refId || null,
      created_at: now,
      synced_at: null,
      expires_at: expiresAt || null,
      retry_count: 0,
      error: null,
    };
    this._appendMessage(msg);
    return msgId;
  }

  writeInboundBatch(messages) {
    const ids = [];
    for (const m of messages) {
      ids.push(this.writeInbound(m));
    }
    return ids;
  }

  // --- Public API: query ---

  getById(id) {
    const msg = this._messages.get(id);
    return msg ? { ...msg } : null;
  }

  poll({ channel, type, limit } = {}) {
    const max = Math.max(1, Math.min(limit || 20, 100));
    const results = [];
    for (const id of this._inbound) {
      if (results.length >= max) break;
      const msg = this._messages.get(id);
      if (!msg || msg.status !== 'pending') continue;
      if (channel && msg.channel !== channel) continue;
      if (type && msg.type !== type) continue;
      results.push({ ...msg });
    }
    return results;
  }

  pollOutbound({ channel, limit } = {}) {
    const ch = channel || DEFAULT_CHANNEL;
    const max = Math.max(1, Math.min(limit || 50, 200));
    const results = [];

    const priorityOrder = { high: 0, normal: 1, low: 2 };
    const candidates = [];
    for (const id of this._outbound) {
      const msg = this._messages.get(id);
      if (!msg || msg.status !== 'pending') continue;
      if (msg.channel !== ch) continue;
      candidates.push(msg);
    }
    candidates.sort((a, b) => {
      const pa = priorityOrder[a.priority] ?? 1;
      const pb = priorityOrder[b.priority] ?? 1;
      if (pa !== pb) return pa - pb;
      return a.created_at - b.created_at;
    });
    for (let i = 0; i < Math.min(candidates.length, max); i++) {
      results.push({ ...candidates[i] });
    }
    return results;
  }

  // --- Public API: status updates ---

  ack(messageIds) {
    const ids = Array.isArray(messageIds) ? messageIds : [messageIds];
    let count = 0;
    for (const id of ids) {
      const msg = this._messages.get(id);
      if (msg && msg.direction === 'inbound') {
        this._appendUpdate(id, { status: 'delivered' });
        this._evictFromIndex(id);
        count++;
      }
    }
    return count;
  }

  updateStatus(id, status, { error, syncedAt } = {}) {
    const TERMINAL = new Set(['synced', 'delivered', 'failed', 'rejected']);
    const fields = { status };
    if (syncedAt) fields.synced_at = syncedAt;
    else if (status === 'synced') fields.synced_at = Date.now();
    if (error !== undefined) fields.error = error;
    else if (status !== 'failed' && status !== 'rejected') fields.error = null;
    this._appendUpdate(id, fields);
    if (TERMINAL.has(status)) {
      this._evictFromIndex(id);
    }
  }

  updateStatusBatch(updates) {
    for (const u of updates) {
      this.updateStatus(u.id, u.status, { error: u.error, syncedAt: u.syncedAt });
    }
  }

  incrementRetry(id, error) {
    const msg = this._messages.get(id);
    const newCount = msg ? (msg.retry_count || 0) + 1 : 1;
    this._appendUpdate(id, { retry_count: newCount, error: error || null });
  }

  list({ type, direction, status, limit, offset } = {}) {
    if (!type) throw new Error('type is required for list()');
    const max = Math.max(1, Math.min(limit || 20, 100));
    const skip = Math.max(0, offset || 0);

    const all = [];
    for (const [, msg] of this._messages) {
      if (type !== '%' && msg.type !== type) continue;
      if (direction && msg.direction !== direction) continue;
      if (status && msg.status !== status) continue;
      all.push(msg);
    }
    all.sort((a, b) => b.created_at - a.created_at);
    return all.slice(skip, skip + max).map(m => ({ ...m }));
  }

  countPending({ direction, channel, type } = {}) {
    const dir = direction || 'outbound';
    let count = 0;
    const idList = dir === 'outbound' ? this._outbound : this._inbound;
    for (const id of idList) {
      const msg = this._messages.get(id);
      if (!msg || msg.status !== 'pending') continue;
      if (channel && msg.channel !== channel) continue;
      if (type && msg.type !== type) continue;
      count++;
    }
    return count;
  }

  // --- Public API: state / cursors ---

  getCursor(key) {
    const val = this._state[`cursor:${key}`];
    return val !== undefined ? val : null;
  }

  setCursor(key, value) {
    const stateKey = `cursor:${key}`;
    this._state[stateKey] = value;
    this._persistState([stateKey]);
  }

  getState(key) {
    const val = this._state[key];
    return val !== undefined ? val : null;
  }

  setState(key, value) {
    this._state[key] = typeof value === 'string' ? value : JSON.stringify(value);
    this._persistState([key]);
  }

  setNodeSecretState({ secret = '', version = '', source = '', envSuppressed = '' } = {}) {
    this._state.node_secret = secret;
    this._state.node_secret_version = version ? String(version) : '';
    this._state.node_secret_source = source;
    this._state.node_secret_env_suppressed = envSuppressed;
    this._persistState([
      'node_secret',
      'node_secret_version',
      'node_secret_source',
      'node_secret_env_suppressed',
    ]);
  }

  // --- Compaction (reduces JSONL file size by rewriting only current state) ---

  compact() {
    // Round-7 (§20.5): same per-PID tmp rationale as _persistState.
    // Two concurrent compact() calls (daemon + ad-hoc CLI) racing on
    // the same `${messagesFile}.tmp` lose the loser's compacted log.
    const tmpFile = `${this._messagesFile}.${process.pid}.tmp`;
    const entries = [];
    for (const [, msg] of this._messages) {
      entries.push(msg);
    }
    entries.sort((a, b) => a.created_at - b.created_at);

    const lines = entries.map((msg) => jsonlLineForWrite(msg));

    const fd = fs.openSync(tmpFile, 'w', PRIVATE_FILE_MODE);
    try {
      for (const line of lines) {
        fs.writeSync(fd, line);
      }
    } finally {
      fs.closeSync(fd);
    }
    bestEffortChmod(tmpFile, PRIVATE_FILE_MODE);
    // Windows: renameSync throws EPERM when the destination already exists.
    // Remove it first so the swap succeeds on all platforms.
    if (process.platform === 'win32') {
      try { fs.unlinkSync(this._messagesFile); } catch (e) {
        if (e.code !== 'ENOENT') throw e;
      }
    }
    fs.renameSync(tmpFile, this._messagesFile);
    bestEffortChmod(this._messagesFile, PRIVATE_FILE_MODE);
    this._rebuildIndex();
  }

  close() {
    // no-op for JSONL (no file handles to close), but kept for API compatibility
  }
}

// Migration registry: key = target schema version, value = function(store)
// Each migration mutates in-memory state or rewrites JSONL as needed.
// Add new entries when SCHEMA_VERSION is bumped.
const MIGRATIONS = {
  // version 1 is the initial schema -- no migration needed from 0 (fresh install)
};

module.exports = { MailboxStore, generateUUIDv7, DEFAULT_CHANNEL, SCHEMA_VERSION, PROXY_PROTOCOL_VERSION };
