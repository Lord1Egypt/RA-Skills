// Append-only asset call log for tracking Hub asset interactions per evolution run.
// Log file: {evolution_dir}/asset_call_log.jsonl

const fs = require('fs');
const path = require('path');
const { getEvolutionDir } = require('./paths');

function getLogPath() {
  return path.join(getEvolutionDir(), 'asset_call_log.jsonl');
}

function ensureDir(filePath) {
  const dir = path.dirname(filePath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

/**
 * Append a single asset call record to the log.
 *
 * @param {object} entry
 * @param {string} entry.run_id
 * @param {string} entry.action - hub_search_hit | hub_search_miss | asset_reuse | asset_reference | asset_publish | asset_publish_skip | asset_inject | asset_inject_shadow
 * @param {string} [entry.asset_id]
 * @param {string} [entry.asset_type]
 * @param {string} [entry.source_node_id]
 * @param {string} [entry.chain_id]
 * @param {number} [entry.score]
 * @param {string} [entry.mode] - direct | reference
 * @param {string[]} [entry.signals]
 * @param {string} [entry.reason]
 * @param {number} [entry.tokens_saved] - tokens a reuse avoided (asset_reuse/asset_reference)
 * @param {string} [entry.tokens_saved_basis] - 'measured' | 'estimated_blast_radius' | 'estimated_default'
 * @param {number} [entry.tokens_spent] - real measured tokens spent deriving the asset (asset_publish)
 * @param {object} [entry.extra]
 */
function logAssetCall(entry) {
  if (!entry || typeof entry !== 'object') return;
  try {
    const logPath = getLogPath();
    ensureDir(logPath);
    const record = {
      timestamp: new Date().toISOString(),
      ...entry,
    };
    fs.appendFileSync(logPath, JSON.stringify(record) + '\n', 'utf8');
  } catch (e) {
    // Non-fatal: never block evolution for logging failure
  }
}

/**
 * Read asset call log entries with optional filters.
 *
 * @param {object} [opts]
 * @param {string} [opts.run_id] - filter by run_id
 * @param {string} [opts.action] - filter by action type
 * @param {number} [opts.last] - only return last N entries
 * @param {string} [opts.since] - ISO date string, only entries after this time
 * @returns {object[]}
 */
function readCallLog(opts) {
  const o = opts || {};
  const logPath = getLogPath();
  if (!fs.existsSync(logPath)) return [];

  const raw = fs.readFileSync(logPath, 'utf8');
  const lines = raw.split('\n').filter(Boolean);

  let entries = [];
  for (const line of lines) {
    try {
      entries.push(JSON.parse(line));
    } catch (e) { /* skip corrupt lines */ }
  }

  if (o.since) {
    const sinceTs = new Date(o.since).getTime();
    if (Number.isFinite(sinceTs)) {
      entries = entries.filter(e => new Date(e.timestamp).getTime() >= sinceTs);
    }
  }

  if (o.run_id) {
    entries = entries.filter(e => e.run_id === o.run_id);
  }

  if (o.action) {
    entries = entries.filter(e => e.action === o.action);
  }

  if (o.last && Number.isFinite(o.last) && o.last > 0) {
    entries = entries.slice(-o.last);
  }

  return entries;
}

/**
 * Summarize asset call log (for CLI display).
 *
 * @param {object} [opts] - same filters as readCallLog
 * @returns {object} summary with totals and per-action counts
 */
function summarizeCallLog(opts) {
  const entries = readCallLog(opts);
  const actionCounts = {};
  const assetsSeen = new Set();
  const runsSeen = new Set();

  for (const e of entries) {
    const a = e.action || 'unknown';
    actionCounts[a] = (actionCounts[a] || 0) + 1;
    if (e.asset_id) assetsSeen.add(e.asset_id);
    if (e.run_id) runsSeen.add(e.run_id);
  }

  return {
    total_entries: entries.length,
    unique_assets: assetsSeen.size,
    unique_runs: runsSeen.size,
    by_action: actionCounts,
    entries,
  };
}

/**
 * P4-a Slice A: local-only reuse-attribution rollup. Aggregates this node's
 * asset_reuse / asset_reference log entries per reused asset, giving the team a
 * LOCAL view of which Hub assets this node reused — without depending on the
 * lossy best-effort Hub sync, and without any network call or money movement.
 * Pure read over the local jsonl; safe to call anytime.
 *
 * @param {object} [opts] - readCallLog filters (e.g. {since})
 * @returns {{ total_reuse:number, total_reference:number, total_tokens_saved:number, by_asset:object[] }}
 */
function reuseAttributionSummary(opts) {
  const o = opts || {};
  const entries = readCallLog(o).filter(
    e => e.action === 'asset_reuse' || e.action === 'asset_reference'
  );
  const byAsset = new Map();
  let totalTokensSaved = 0;
  for (const e of entries) {
    const id = e.asset_id || '(unknown)';
    let agg = byAsset.get(id);
    if (!agg) {
      agg = { asset_id: id, source_node_id: e.source_node_id || null, chain_id: e.chain_id || null, reuse: 0, reference: 0, tokens_saved: 0 };
      byAsset.set(id, agg);
    }
    if (e.action === 'asset_reuse') agg.reuse += 1;
    else agg.reference += 1;
    const ts = Number(e.tokens_saved);
    if (Number.isFinite(ts) && ts > 0) { agg.tokens_saved += ts; totalTokensSaved += ts; }
    // keep first-seen source/chain; do not trust later rows to overwrite
    if (!agg.source_node_id && e.source_node_id) agg.source_node_id = e.source_node_id;
    if (!agg.chain_id && e.chain_id) agg.chain_id = e.chain_id;
  }
  const byAssetArr = Array.from(byAsset.values())
    .sort((a, b) => (b.reuse + b.reference) - (a.reuse + a.reference));
  return {
    total_reuse: entries.filter(e => e.action === 'asset_reuse').length,
    total_reference: entries.filter(e => e.action === 'asset_reference').length,
    total_tokens_saved: totalTokensSaved,
    by_asset: byAssetArr,
  };
}

/**
 * Local asset-cost index: maps asset_id -> real tokens spent deriving it,
 * rebuilt from this node's own asset_publish rows (which carry tokens_spent
 * measured from the proxy trace meter). Lets dispatch attribute a REAL
 * tokens_saved to a reuse of an asset this node derived, even when the
 * measured cost is not carried on the wire. Later publish rows win.
 *
 * @param {object} [opts] - readCallLog filters (e.g. {since})
 * @returns {Object<string, number>}
 */
function assetCostIndex(opts) {
  const entries = readCallLog(opts || {}).filter(e => e.action === 'asset_publish' && e.asset_id);
  const map = {};
  for (const e of entries) {
    const spent = Number(e.tokens_spent);
    if (Number.isFinite(spent) && spent > 0) map[e.asset_id] = spent;
  }
  return map;
}

module.exports = {
  logAssetCall,
  readCallLog,
  summarizeCallLog,
  reuseAttributionSummary,
  assetCostIndex,
  getLogPath,
};
