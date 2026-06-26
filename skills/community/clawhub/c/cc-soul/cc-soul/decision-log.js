let _cache = [];
let _cacheLoaded = false;
function getDb() {
  try {
    const mod = require("./sqlite-store.ts");
    return mod;
  } catch {
    return null;
  }
}
function ensureCache() {
  if (_cacheLoaded) return;
  _cacheLoaded = true;
  const mod = getDb();
  if (mod?.dbGetDecisions) {
    _cache = mod.dbGetDecisions(void 0, 200);
  }
}
function logDecision(action, key, reason, trace) {
  const decision = { action, key, reason, ts: Date.now() };
  if (trace) decision.trace = trace;
  ensureCache();
  _cache.push(decision);
  if (_cache.length > 200) _cache = _cache.slice(-200);
  const reasonWithTrace = trace ? `${reason} [trace: via=${trace.via || "unknown"}, score=${trace.score?.toFixed(3) ?? "N/A"}]` : reason;
  const mod = getDb();
  if (mod?.dbLogDecision) {
    mod.dbLogDecision(action, key, reasonWithTrace);
  }
}
function getDecisions(filter) {
  ensureCache();
  if (!filter) return _cache;
  return _cache.filter(
    (d) => d.action.includes(filter) || d.key.includes(filter) || d.reason.includes(filter)
  );
}
function dumpDecisions() {
  ensureCache();
  return _cache.map(
    (d) => `[${new Date(d.ts).toISOString().slice(5, 16)}] ${d.action}: ${d.key} | ${d.reason}`
  ).join("\n");
}
function getDecisionStats() {
  ensureCache();
  const byAction = {};
  for (const d of _cache) {
    byAction[d.action] = (byAction[d.action] || 0) + 1;
  }
  return { total: _cache.length, byAction };
}
export {
  dumpDecisions,
  getDecisionStats,
  getDecisions,
  logDecision
};
