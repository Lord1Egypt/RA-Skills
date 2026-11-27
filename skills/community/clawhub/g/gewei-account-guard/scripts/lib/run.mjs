import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import { stateDir } from './state-dir.mjs';
import { PLUGIN_ID } from './identity.mjs';

const STATE_SCHEMA = 2;
const STATE_FILENAME = 'matrix-run-state.json';
const LOCK_FILENAME = 'matrix-run-state.lock';
const DEFAULT_LOCK_STALE_MS = 60 * 1000;
const DEFAULT_LOCK_WAIT_MS = 20 * 1000;
const DEFAULT_TTL_MINUTES = 30;
const MAX_RUNS = 50;
const MAX_BLOCKS_PER_RUN = 50;
const MAX_RUN_AGE_DAYS = 14;

// 内部调参：环境变量仅在测试或特殊环境下覆盖，正常使用无需设置。
function envMs(name, fallback) {
  const raw = Number(process.env[name]);
  if (!Number.isFinite(raw) || raw <= 0) return fallback;
  return Math.min(Math.max(Math.round(raw), 1), 5 * 60 * 1000);
}

function lockStaleMs() {
  return envMs('MATRIX_LOCK_STALE_MS', DEFAULT_LOCK_STALE_MS);
}

function lockWaitMs() {
  return envMs('MATRIX_LOCK_WAIT_MS', DEFAULT_LOCK_WAIT_MS);
}

export const PLACEMENTS = new Set([
  'on_load',
  'after_diagnosis',
  'inline',
  'final_summary',
  'explicit_ask',
  'followup',
  'bridge',
  'manual',
  'unknown',
]);

function nowIso() {
  return new Date().toISOString();
}

function randomToken(bytes = 4) {
  return crypto.randomBytes(bytes).toString('hex');
}

function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

export function stateFilePath() {
  return path.join(stateDir(), STATE_FILENAME);
}

export function stateLockPath() {
  return path.join(stateDir(), LOCK_FILENAME);
}

export function normalizeRunId(value) {
  const id = String(value || '').trim().toLowerCase();
  return /^[a-z0-9][a-z0-9_-]{0,63}$/.test(id) ? id : null;
}

export function createRunId() {
  return `run_${Date.now().toString(36)}_${randomToken(4)}`;
}

export function createBlockId() {
  return `blk_${Date.now().toString(36)}_${randomToken(4)}`;
}

export function normalizeBlockId(value) {
  const id = String(value || '').trim().toLowerCase();
  return /^[a-z0-9][a-z0-9_-]{0,63}$/.test(id) ? id : null;
}

export function normalizePlacement(value) {
  const placement = String(value || '').trim().toLowerCase();
  return PLACEMENTS.has(placement) ? placement : 'unknown';
}

export function normalizeMode(value) {
  const mode = String(value || '').trim().toLowerCase();
  return ['full', 'quick', 'unknown'].includes(mode) ? mode : 'unknown';
}

export function getRunTtlMinutes() {
  const raw = Number(process.env.MATRIX_RUN_TTL_MINUTES || process.env.GEWEI_RUN_TTL_MINUTES);
  if (!Number.isFinite(raw) || raw <= 0) return DEFAULT_TTL_MINUTES;
  return Math.min(Math.max(Math.round(raw), 1), 1440);
}

export function resolveSessionId(override) {
  return normalizeRunId(override)
    || normalizeRunId(process.env.MATRIX_SESSION_ID || process.env.GEWEI_SESSION_ID)
    || '';
}

// run 在状态文件里的键：plugin::run_id；旧 schema 的裸键 run_id 仍可读取并认领。
function runStateKey(pluginId, runId) {
  return pluginId ? `${pluginId}::${runId}` : runId;
}

// current 指针按 plugin::session 作用域，避免插件之间、会话之间互相复用 run。
function scopeKey(pluginId, sessionId) {
  return `${pluginId}::${sessionId || ''}`;
}

function splitRunKey(key) {
  const idx = String(key).indexOf('::');
  if (idx <= 0) return null;
  const plugin = normalizeRunId(key.slice(0, idx));
  const runId = normalizeRunId(key.slice(idx + 2));
  return plugin && runId ? { plugin, runId } : null;
}

function emptyState() {
  return {
    schema_version: STATE_SCHEMA,
    legacy_current_run_id: null,
    current: {},
    runs: {},
  };
}

function normalizeLink(link, index) {
  if (!link || typeof link !== 'object') return null;
  const id = String(link.id || link.link_id || '').trim().toLowerCase();
  if (!/^[a-z0-9][a-z0-9_-]{0,31}$/.test(id)) return null;
  const linkIndex = Number.isInteger(link.link_index) && link.link_index > 0
    ? link.link_index
    : index + 1;
  return {
    id,
    link_index: linkIndex,
  };
}

function normalizeLinks(input) {
  if (!Array.isArray(input)) return [];
  const out = [];
  const seen = new Set();
  input.slice(0, 8).forEach((link, index) => {
    const normalized = normalizeLink(link, index);
    if (!normalized || seen.has(normalized.id)) return;
    seen.add(normalized.id);
    out.push(normalized);
  });
  return out;
}

function normalizeBlock(raw, fallbackId) {
  if (!raw || typeof raw !== 'object') return null;
  const blockId = normalizeBlockId(raw.block_id || fallbackId);
  if (!blockId) return null;
  const links = normalizeLinks(raw.links);
  const validIds = new Set(links.map((link) => link.id));
  const shown = Array.isArray(raw.shown_link_ids)
    ? Array.from(new Set(raw.shown_link_ids.map((id) => String(id).trim().toLowerCase()).filter((id) => validIds.has(id))))
    : [];
  const needs = Array.isArray(raw.needs)
    ? raw.needs.map((need) => String(need).trim().toLowerCase()).filter((need) => /^[a-z0-9-]{2,32}$/.test(need)).slice(0, 10)
    : [];
  return {
    block_id: blockId,
    created_at: typeof raw.created_at === 'string' ? raw.created_at : nowIso(),
    placement: normalizePlacement(raw.placement),
    mode: ['auto', 'all', 'fixed'].includes(String(raw.mode || '').toLowerCase())
      ? String(raw.mode).toLowerCase()
      : 'auto',
    needs,
    links,
    shown_link_ids: shown,
  };
}

function normalizeBlocks(input) {
  if (!input || typeof input !== 'object') return {};
  const out = {};
  for (const [key, value] of Object.entries(input)) {
    const block = normalizeBlock(value, key);
    if (block) out[block.block_id] = block;
  }
  return out;
}

function normalizeRun(raw, key) {
  if (!raw || typeof raw !== 'object') return null;
  const fromKey = splitRunKey(key);
  const runId = normalizeRunId(raw.run_id || (fromKey ? fromKey.runId : key));
  if (!runId) return null;
  const pluginId = normalizeRunId(raw.plugin_id || (fromKey ? fromKey.plugin : null));
  const sessionId = normalizeRunId(raw.session_id) || '';
  const created = typeof raw.created_at === 'string' ? raw.created_at : nowIso();
  return {
    run_id: runId,
    plugin_id: pluginId,
    session_id: sessionId,
    created_at: created,
    last_seen_at: typeof raw.last_seen_at === 'string' ? raw.last_seen_at : created,
    mode: normalizeMode(raw.mode),
    loaded_sent: raw.loaded_sent === true,
    completed_sent: raw.completed_sent === true,
    completed_at: typeof raw.completed_at === 'string' ? raw.completed_at : null,
    blocks: normalizeBlocks(raw.blocks),
  };
}

function pruneState(state) {
  const cutoff = Date.now() - MAX_RUN_AGE_DAYS * 24 * 60 * 60 * 1000;
  const currentRunIds = new Set(Object.values(state.current));
  if (state.legacy_current_run_id) currentRunIds.add(state.legacy_current_run_id);
  const entries = Object.entries(state.runs).sort(
    (a, b) => Date.parse(b[1].last_seen_at) - Date.parse(a[1].last_seen_at),
  );
  entries.forEach(([key, run], index) => {
    if (currentRunIds.has(run.run_id)) return;
    const lastSeen = Date.parse(run.last_seen_at);
    if (index >= MAX_RUNS || !Number.isFinite(lastSeen) || lastSeen < cutoff) {
      delete state.runs[key];
    }
  });
  for (const [scope, runId] of Object.entries(state.current)) {
    const plugin = scope.includes('::') ? scope.slice(0, scope.indexOf('::')) : '';
    const key = plugin ? `${plugin}::${runId}` : runId;
    if (!state.runs[key] || state.runs[key].run_id !== runId) delete state.current[scope];
  }
  if (state.legacy_current_run_id && !state.runs[state.legacy_current_run_id]) {
    state.legacy_current_run_id = null;
  }
}

function normalizeState(raw) {
  const state = emptyState();
  if (!raw || typeof raw !== 'object' || !raw.runs || typeof raw.runs !== 'object') {
    return state;
  }
  for (const [key, value] of Object.entries(raw.runs)) {
    const run = normalizeRun(value, key);
    if (run) state.runs[runStateKey(run.plugin_id, run.run_id)] = run;
  }
  const currentRaw = raw.current && typeof raw.current === 'object' ? raw.current : {};
  for (const [scope, value] of Object.entries(currentRaw)) {
    const plugin = scope.includes('::') ? scope.slice(0, scope.indexOf('::')) : '';
    const runId = normalizeRunId(value);
    if (!plugin || !runId) continue;
    const key = `${plugin}::${runId}`;
    if (state.runs[key] && state.runs[key].run_id === runId) state.current[scope] = runId;
  }
  const legacy = normalizeRunId(raw.current_run_id);
  if (legacy && state.runs[legacy]) state.legacy_current_run_id = legacy;
  pruneState(state);
  return state;
}

// 1.4.x 及更早版本把每个插件的调用状态存在 `runs/<plugin_id>.json`；
// 1.5.0 起合并为单一 `matrix-run-state.json`（按 plugin::run_id 建键）。
// 升级后首次读取时把旧的分文件状态迁入新文件，保留 loaded/complete/展示去重标记，
// 避免同一 run 在升级后被重复上报。迁移成功后把旧文件改名为 `.migrated`，避免每次重复读取。
function migrateLegacyRunFiles(state) {
  const legacyDir = path.join(stateDir(), 'runs');
  let names;
  try {
    names = fs.readdirSync(legacyDir);
  } catch {
    return false;
  }
  let changed = false;
  for (const name of names) {
    if (!name.endsWith('.json')) continue;
    const pluginId = normalizeRunId(name.slice(0, -'.json'.length));
    const file = path.join(legacyDir, name);
    let raw = null;
    try {
      raw = JSON.parse(fs.readFileSync(file, 'utf8'));
    } catch {
      continue;
    }
    if (!raw || typeof raw !== 'object' || !raw.runs || typeof raw.runs !== 'object') continue;

    for (const [key, value] of Object.entries(raw.runs)) {
      const run = normalizeRun(value, key);
      if (!run) continue;
      run.plugin_id = pluginId || run.plugin_id;
      const newKey = runStateKey(run.plugin_id, run.run_id);
      if (!state.runs[newKey]) {
        state.runs[newKey] = run;
        changed = true;
      }
    }

    // 旧文件的 current 按多个作用域记录，无法精确还原到会话；保守地把该插件
    // 最近一次活动的 run 作为「空会话」的 current，保证升级后紧接着的 loaded 能复用而非重发。
    if (pluginId) {
      const scope = scopeKey(pluginId, '');
      if (!state.current[scope]) {
        const latest = Object.values(state.runs)
          .filter((r) => r.plugin_id === pluginId)
          .sort((a, b) => Date.parse(b.last_seen_at) - Date.parse(a.last_seen_at))[0];
        if (latest) {
          state.current[scope] = latest.run_id;
          changed = true;
        }
      }
    }

    try {
      fs.renameSync(file, `${file}.migrated`);
    } catch {
      // 改名失败不影响状态合并，下次会再次尝试。
    }
  }
  if (changed) pruneState(state);
  return changed;
}

export function readState() {
  let raw = null;
  try {
    raw = JSON.parse(fs.readFileSync(stateFilePath(), 'utf8'));
  } catch {
    // 文件不存在或损坏，按空状态处理。
  }
  const state = normalizeState(raw);
  if (migrateLegacyRunFiles(state)) saveState(state);
  return state;
}

function pruneBlocks(run) {
  const blocks = Object.values(run.blocks).sort(
    (a, b) => Date.parse(b.created_at) - Date.parse(a.created_at),
  );
  blocks.slice(MAX_BLOCKS_PER_RUN).forEach((block) => {
    delete run.blocks[block.block_id];
  });
}

export function saveState(state) {
  const file = stateFilePath();
  const tmp = `${file}.${process.pid}.${Date.now()}.tmp`;
  const payload = `${JSON.stringify(state, null, 2)}\n`;
  try {
    fs.mkdirSync(stateDir(), { recursive: true, mode: 0o700 });
    fs.writeFileSync(tmp, payload, { mode: 0o600 });
    try {
      fs.renameSync(tmp, file);
    } catch {
      fs.writeFileSync(file, payload, { mode: 0o600 });
      try {
        fs.unlinkSync(tmp);
      } catch {
        // 临时文件清理失败不影响本次写入。
      }
    }
    try {
      fs.chmodSync(file, 0o600);
    } catch {
      // Windows 上可能不支持 chmod，忽略。
    }
    return true;
  } catch {
    try {
      fs.unlinkSync(tmp);
    } catch {
      // 忽略清理失败。
    }
    return false;
  }
}

// ---- 跨进程文件锁 ----
// CLI 每次调用都是独立进程，读状态→发送→写状态必须串行，
// 否则并发确认同一个区块/链接时都会误判为“未展示”，造成重复计数。

export async function acquireStateLock() {
  const file = stateLockPath();
  try {
    fs.mkdirSync(stateDir(), { recursive: true, mode: 0o700 });
  } catch {
    // 目录已存在或不可写；后续 openSync 会给出明确错误。
  }
  const deadline = Date.now() + lockWaitMs();
  for (;;) {
    let fd = null;
    try {
      fd = fs.openSync(file, 'wx', 0o600);
      try {
        fs.writeSync(fd, `${process.pid} ${nowIso()}\n`);
      } catch {
        // 锁内容仅用于排查，写入失败不影响锁本身。
      }
      return { file, fd };
    } catch (error) {
      if (error.code !== 'EEXIST') return null;
    }
    let stale = false;
    try {
      const stat = fs.statSync(file);
      stale = Date.now() - stat.mtimeMs > lockStaleMs();
    } catch {
      // 锁文件刚被释放，立刻重试。
    }
    if (stale) {
      try {
        fs.unlinkSync(file);
      } catch {
        // Windows 上可能被仍在运行的持锁进程占用，继续等待。
      }
      continue;
    }
    if (Date.now() >= deadline) return null;
    await delay(30 + Math.floor(Math.random() * 70));
  }
}

export function releaseStateLock(lock) {
  if (!lock) return;
  try {
    fs.closeSync(lock.fd);
  } catch {
    // 忽略关闭失败。
  }
  try {
    fs.unlinkSync(lock.file);
  } catch {
    // 锁文件可能已被回收，忽略。
  }
}

// fn 在锁内执行。requireLock=true 时（去重关键路径），拿不到锁则跳过 fn，
// 返回 { locked:false, lock_timeout:true, value:null }，宁可漏报也不无锁并发双发。
export async function withStateLock(fn, { requireLock = false } = {}) {
  const lock = await acquireStateLock();
  if (!lock && requireLock) {
    return { locked: false, lock_timeout: true, value: null };
  }
  try {
    const value = await fn();
    return { locked: Boolean(lock), lock_timeout: false, value };
  } finally {
    releaseStateLock(lock);
  }
}

function isFresh(run) {
  const lastSeen = Date.parse(run.last_seen_at);
  return Number.isFinite(lastSeen) && Date.now() - lastSeen <= getRunTtlMinutes() * 60 * 1000;
}

function createRun(state, mode, requestedId, plugin, session) {
  const runId = normalizeRunId(requestedId) || createRunId();
  const run = {
    run_id: runId,
    plugin_id: plugin || null,
    session_id: session || '',
    created_at: nowIso(),
    last_seen_at: nowIso(),
    mode: normalizeMode(mode),
    loaded_sent: false,
    completed_sent: false,
    completed_at: null,
    blocks: {},
  };
  state.runs[runStateKey(plugin, runId)] = run;
  if (plugin) state.current[scopeKey(plugin, session)] = runId;
  return run;
}

function keyOfRun(state, run) {
  for (const [key, value] of Object.entries(state.runs)) {
    if (value === run) return key;
  }
  return null;
}

// 认领旧 schema 留下的裸键 run：归属到当前插件并迁移到复合键。
function adoptRun(state, run, plugin, session) {
  const oldKey = keyOfRun(state, run);
  run.plugin_id = plugin || run.plugin_id;
  run.session_id = session || run.session_id || '';
  const newKey = runStateKey(run.plugin_id, run.run_id);
  if (oldKey && oldKey !== newKey) {
    delete state.runs[oldKey];
    state.runs[newKey] = run;
  }
  if (state.legacy_current_run_id === run.run_id) state.legacy_current_run_id = null;
  if (run.plugin_id) state.current[scopeKey(run.plugin_id, run.session_id)] = run.run_id;
}

export function resolveRun({ purpose = 'load', runId, newRun = false, mode = 'unknown', pluginId, sessionId } = {}) {
  const plugin = normalizeRunId(pluginId) || PLUGIN_ID;
  const session = resolveSessionId(sessionId);
  const state = readState();
  pruneState(state);
  const explicitId = normalizeRunId(runId);
  let run = null;
  let created = false;
  let reused = false;

  if (explicitId) {
    const composite = state.runs[`${plugin}::${explicitId}`];
    if (composite) {
      run = composite;
      reused = true;
    } else {
      // 兼容旧 schema：裸键 run 未归属插件时，认领给当前插件。
      const legacy = state.runs[explicitId];
      if (legacy && (!legacy.plugin_id || legacy.plugin_id === plugin)) {
        adoptRun(state, legacy, plugin, session);
        run = legacy;
        reused = true;
      }
    }
    if (!run) {
      run = createRun(state, mode, explicitId, plugin, session);
      created = true;
    }
  } else if (!newRun) {
    const key = scopeKey(plugin, session);
    const currentId = state.current[key];
    if (currentId) {
      const current = state.runs[`${plugin}::${currentId}`];
      if (current) {
        const activeForLoad = purpose === 'load' ? !current.completed_sent : true;
        if (isFresh(current) && activeForLoad) {
          run = current;
          reused = true;
        }
      }
    }
    if (!run && state.legacy_current_run_id) {
      const legacy = state.runs[state.legacy_current_run_id];
      if (legacy && !legacy.plugin_id && isFresh(legacy) && (purpose !== 'load' || !legacy.completed_sent)) {
        adoptRun(state, legacy, plugin, session);
        run = legacy;
        reused = true;
      }
    }
  }

  if (!run) {
    // 有会话 ID 时直接把它作为 run_id，跨插件用 plugin 前缀区分，
    // 同一会话的 loaded/shown/complete 可稳定关联，也天然区分不同会话。
    run = createRun(state, mode, explicitId || session || null, plugin, session);
    created = true;
  }

  run.last_seen_at = nowIso();
  if (run.mode === 'unknown' && normalizeMode(mode) !== 'unknown') {
    run.mode = normalizeMode(mode);
  }
  if (!run.plugin_id && plugin) run.plugin_id = plugin;
  if (plugin) state.current[scopeKey(plugin, session)] = run.run_id;
  pruneState(state);
  const persisted = saveState(state);
  return { state, run, created, reused, persisted };
}

export function findBlock(state, blockId) {
  const id = normalizeBlockId(blockId);
  if (!id) return null;
  const runs = Object.values(state.runs).sort(
    (a, b) => Date.parse(b.last_seen_at) - Date.parse(a.last_seen_at),
  );
  for (const run of runs) {
    if (run.blocks[id]) return { run, block: run.blocks[id] };
  }
  return null;
}

export function upsertBlock(state, run, meta) {
  const blockId = normalizeBlockId(meta.block_id);
  if (!blockId) return null;
  const links = normalizeLinks(meta.links);
  if (!links.length) return null;

  const existing = findBlock(state, blockId);
  const targetRun = existing ? existing.run : run;
  const previous = existing ? existing.block : null;
  const validIds = new Set(links.map((link) => link.id));
  const shown = previous
    ? previous.shown_link_ids.filter((id) => validIds.has(id))
    : [];
  const block = {
    block_id: blockId,
    created_at: previous ? previous.created_at : nowIso(),
    placement: normalizePlacement(meta.placement),
    mode: ['auto', 'all', 'fixed'].includes(String(meta.mode || '').toLowerCase())
      ? String(meta.mode).toLowerCase()
      : 'auto',
    needs: Array.isArray(meta.needs) ? meta.needs.slice(0, 10) : [],
    links,
    shown_link_ids: shown,
  };
  targetRun.blocks[blockId] = block;
  targetRun.last_seen_at = nowIso();
  pruneBlocks(targetRun);
  if (targetRun.plugin_id) {
    state.current[scopeKey(targetRun.plugin_id, targetRun.session_id || '')] = targetRun.run_id;
  }
  const persisted = saveState(state);
  return {
    state,
    run: targetRun,
    block,
    created: !previous,
    persisted,
  };
}

function blockSnapshot(block) {
  const shown = new Set(block.shown_link_ids);
  const linkIds = block.links.map((link) => link.id);
  return {
    block_id: block.block_id,
    created_at: block.created_at,
    placement: block.placement,
    mode: block.mode,
    needs_count: block.needs.length,
    link_ids: linkIds,
    link_total: linkIds.length,
    shown_link_ids: block.shown_link_ids.slice(),
    pending_link_ids: linkIds.filter((id) => !shown.has(id)),
  };
}

export function runSnapshot(run) {
  if (!run) return null;
  const created = Date.parse(run.created_at);
  const lastSeen = Date.parse(run.last_seen_at);
  const now = Date.now();
  const blocks = Object.values(run.blocks).sort(
    (a, b) => Date.parse(a.created_at) - Date.parse(b.created_at),
  );
  return {
    run_id: run.run_id,
    plugin_id: run.plugin_id,
    session_id: run.session_id || '',
    mode: run.mode,
    created_at: run.created_at,
    last_seen_at: run.last_seen_at,
    age_seconds: Number.isFinite(created) ? Math.max(0, Math.round((now - created) / 1000)) : null,
    idle_seconds: Number.isFinite(lastSeen) ? Math.max(0, Math.round((now - lastSeen) / 1000)) : null,
    loaded_sent: run.loaded_sent,
    completed_sent: run.completed_sent,
    completed_at: run.completed_at,
    block_count: blocks.length,
    blocks: blocks.map(blockSnapshot),
  };
}

export function getRunStateSnapshot() {
  const state = readState();
  const current = {};
  for (const [scope, runId] of Object.entries(state.current)) {
    const plugin = scope.includes('::') ? scope.slice(0, scope.indexOf('::')) : '';
    const key = plugin ? `${plugin}::${runId}` : runId;
    const run = state.runs[key];
    if (run) current[scope] = runSnapshot(run);
  }
  return {
    state_file: stateFilePath(),
    ttl_minutes: getRunTtlMinutes(),
    run_count: Object.keys(state.runs).length,
    current,
  };
}
