// ATP Task Pickup (merchant-side)
//
// When a buyer places an ATP order, the Hub creates a Task row in status
// "claimed" already bound to a target merchant node (see orderRouterService).
// That Task never appears in /a2a/fetch (which only returns status="open"
// tasks), so without this module the merchant's Evolver runtime never knows
// it has work to do, no resultAssetId is ever written, autoDeliver never
// runs, and the DeliveryProof expires after 7 days.
//
// This module bridges the gap by:
//   1. Polling /a2a/task/my for tasks with atp_order_id set and no
//      result_asset_id yet (the "merchant owes work" shape).
//   2. Producing a renderable sessions_spawn(...) prompt that the main loop
//      can emit to stdout. The Evolver wrapper (Cursor/Claude Code hook)
//      picks that up and launches a sub-session that answers the question
//      and runs `node index.js atp-complete` to settle the order.
//   3. Deduping via a local ledger so the same task is never spawned twice,
//      even across restarts.
//
// The module never *itself* prints sessions_spawn. It only PROVIDES the
// spawn string to whoever orchestrates stdout (evolve.js main loop), so the
// existing "one sessions_spawn per cycle" contract with the wrapper is
// preserved and evolve's normal bridge is not interfered with.

const fs = require('fs');
const path = require('path');

const { getMemoryDir } = require('../gep/paths');
const { renderSessionsSpawnCall } = require('../gep/bridge');
const hubClient = require('./hubClient');

const LEDGER_FILENAME = 'atp-pickup-ledger.json';
const LEDGER_MAX_ENTRIES = 500;
const SPAWN_COOLDOWN_MS = 5 * 60 * 1000; // do not respawn the same task within 5 min
const MAX_ANSWER_PROMPT_CHARS = 12000;

function _isEnabled() {
  const raw = (process.env.EVOLVER_ATP_PICKUP || 'on').toLowerCase().trim();
  return raw !== 'off' && raw !== '0' && raw !== 'false';
}

function _ledgerPath() {
  return path.join(getMemoryDir(), LEDGER_FILENAME);
}

function _emptyLedger() {
  return { version: 1, spawned: {} };
}

function _readLedger() {
  try {
    const p = _ledgerPath();
    if (!fs.existsSync(p)) return _emptyLedger();
    const raw = fs.readFileSync(p, 'utf8');
    const parsed = JSON.parse(raw);
    if (!parsed || typeof parsed !== 'object' || !parsed.spawned) return _emptyLedger();
    return parsed;
  } catch (_) {
    return _emptyLedger();
  }
}

function _writeLedger(ledger) {
  try {
    const dir = getMemoryDir();
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    const entries = Object.entries(ledger.spawned || {});
    if (entries.length > LEDGER_MAX_ENTRIES) {
      ledger.spawned = Object.fromEntries(entries.slice(-LEDGER_MAX_ENTRIES));
    }
    const tmp = _ledgerPath() + '.tmp';
    fs.writeFileSync(tmp, JSON.stringify(ledger, null, 2));
    fs.renameSync(tmp, _ledgerPath());
  } catch (_) {
    // Non-fatal: next tick will re-read Hub state. Stale ledger at worst
    // causes a duplicate spawn, which the Hub will 409 on already-completed
    // tasks without side effects.
  }
}

function _isEligible(task) {
  if (!task || typeof task !== 'object') return false;
  if (!task.atp_order_id) return false;
  if (task.result_asset_id) return false;
  if (task.status && task.status !== 'claimed' && task.status !== 'open') return false;
  if (!task.id) return false;
  return true;
}

function _recentlySpawned(ledger, taskId) {
  const entry = ledger.spawned && ledger.spawned[taskId];
  if (!entry || typeof entry !== 'object') return false;
  const ts = Number(entry.at) || 0;
  return Date.now() - ts < SPAWN_COOLDOWN_MS;
}

function _clipQuestion(q) {
  const s = String(q || '').trim();
  if (!s) return '(buyer did not provide a question body)';
  if (s.length <= MAX_ANSWER_PROMPT_CHARS) return s;
  return s.slice(0, MAX_ANSWER_PROMPT_CHARS - 40) + '\n...[TRUNCATED]...';
}

function _answerFilePath(taskId) {
  const safe = String(taskId || 'task').replace(/[^a-zA-Z0-9_\-]/g, '_').slice(0, 64);
  return path.join(getMemoryDir(), 'atp_answer_' + safe + '.md');
}

function _buildSpawnTask(task, opts) {
  const capabilities = Array.isArray(task.capabilities) ? task.capabilities.slice(0, 8) : [];
  const signalsCsv = task.signals ? String(task.signals) : '';
  const answerPath = _answerFilePath(task.id);
  const question = _clipQuestion(task.user_question_body || task.description || task.title);

  const evolverExec = opts && opts.evolverExec ? opts.evolverExec : 'node index.js';

  const lines = [
    'You are an ATP merchant sub-agent. A buyer has paid credits for your node to answer their request.',
    '',
    '# Task',
    '- Task ID: ' + task.id,
    '- ATP Order ID: ' + task.atp_order_id,
    '- Title: ' + String(task.title || '(no title)').slice(0, 200),
    '- Capabilities requested: ' + (capabilities.length ? capabilities.join(', ') : '(none)'),
    '- Signals: ' + (signalsCsv || '(none)'),
    '',
    '# Buyer question',
    question,
    '',
    '# Your job',
    '1. Produce a concrete, useful answer to the buyer question above.',
    '   - Use your existing tools (web search, code read, reasoning) as appropriate.',
    '   - Keep the answer focused and actionable; do not invent facts.',
    '   - If the question is ambiguous, answer the most reasonable interpretation and state your assumption.',
    '2. Write the full answer to this file (plain text or markdown):',
    '     ' + answerPath,
    '3. Settle the order by running EXACTLY this command from the Evolver install dir:',
    '     ' + evolverExec + ' atp-complete \\',
    '       --task-id=' + task.id + ' \\',
    '       --order-id=' + task.atp_order_id + ' \\',
    '       --answer-file=' + answerPath +
      (capabilities.length ? ' \\\n       --capabilities=' + capabilities.join(',') : '') +
      (signalsCsv ? ' \\\n       --signals=' + signalsCsv : ''),
    '4. If atp-complete prints "[ATP-Complete] OK asset_id=...", you are done.',
    '   If it prints "FAILED", read the stage= field. Safe to retry the same command.',
    '',
    '# Hard rules',
    '- Do NOT commit or push any repo changes -- this is a per-order side task, not a code evolution.',
    '- Do NOT run `node index.js solidify` or `node index.js run`.',
    '- Do NOT fabricate the answer; if you cannot answer, still run atp-complete with a short',
    '  honest explanation so the buyer is not left waiting for 7 days.',
    '- Keep the answer under 12k characters.',
  ];
  return lines.join('\n');
}

/**
 * Fetch a pickup action if one is due. Idempotent -- safe to call from the
 * main loop every cycle.
 *
 * @param {object} [opts]
 * @param {number} [opts.limit=5] -- how many Hub tasks to consider per call
 * @param {string} [opts.evolverExec] -- how the wrapper should invoke Evolver
 * @returns {Promise<null | { spawnCall: string, task: object }>}
 *   null when there is nothing to do; otherwise a sessions_spawn() string
 *   the caller SHOULD print to stdout on its next cycle output and the task
 *   we picked so the caller can log it.
 */
async function pickOne(opts) {
  if (!_isEnabled()) return null;
  const limit = Math.max(1, Math.min(20, Number(opts && opts.limit) || 5));

  let listResult;
  try {
    listResult = await hubClient.listMyTasks(limit);
  } catch (_) {
    return null;
  }
  if (!listResult || !listResult.ok) return null;

  const tasks = (listResult.data && Array.isArray(listResult.data.tasks))
    ? listResult.data.tasks
    : (Array.isArray(listResult.data) ? listResult.data : []);
  if (!tasks.length) return null;

  const ledger = _readLedger();
  let picked = null;
  for (const t of tasks) {
    if (!_isEligible(t)) continue;
    if (_recentlySpawned(ledger, t.id)) continue;
    picked = t;
    break;
  }
  if (!picked) return null;

  const spawnTask = _buildSpawnTask(picked, opts);
  const spawnCall = renderSessionsSpawnCall({
    task: spawnTask,
    agentId: 'atp_pickup',
    cleanup: 'delete',
    label: 'atp_pickup_' + String(picked.id).slice(0, 32),
  });

  ledger.spawned = ledger.spawned || {};
  ledger.spawned[picked.id] = { at: Date.now(), order_id: picked.atp_order_id };
  _writeLedger(ledger);

  return { spawnCall, task: picked };
}

/**
 * Forget a previously-spawned task so the main loop will retry it next cycle.
 * Called by callers that detected the spawn channel was unavailable (e.g.
 * wrapper not attached) so we do not burn the cooldown on a no-op spawn.
 */
function forget(taskId) {
  if (!taskId) return;
  const ledger = _readLedger();
  if (ledger.spawned && ledger.spawned[taskId]) {
    delete ledger.spawned[taskId];
    _writeLedger(ledger);
  }
}

module.exports = {
  pickOne,
  forget,
  _isEnabled,
  _isEligible,
  _buildSpawnTask,
  _recentlySpawned,
  _answerFilePath,
};
