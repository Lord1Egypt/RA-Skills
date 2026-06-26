import { readFileSync, writeFileSync, existsSync, mkdirSync, renameSync, readdirSync } from "fs";
import { resolve } from "path";
import { homedir } from "os";
const _pluginsData = resolve(homedir(), ".openclaw/plugins/cc-soul/data");
const _hooksData = resolve(homedir(), ".openclaw/hooks/cc-soul/data");
const _standaloneData = resolve(homedir(), ".cc-soul/data");
const DATA_DIR = existsSync(_pluginsData) ? _pluginsData : existsSync(_hooksData) ? _hooksData : _standaloneData;
let _activeAgentId = "default";
function setActiveAgent(agentId) {
  if (!agentId || agentId === _activeAgentId) return;
  _activeAgentId = agentId;
  const agentDir = resolve(DATA_DIR, "agents", agentId);
  if (!existsSync(agentDir)) mkdirSync(agentDir, { recursive: true });
  console.log(`[cc-soul] active agent: ${agentId} \u2192 ${agentDir}`);
}
function getActiveAgent() {
  return _activeAgentId;
}
function getAgentDataDir(agentId) {
  const id = agentId || _activeAgentId;
  if (id === "default") return DATA_DIR;
  const dir = resolve(DATA_DIR, "agents", id);
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
  return dir;
}
const BRAIN_PATH = resolve(DATA_DIR, "brain.json");
const MEMORIES_PATH = resolve(DATA_DIR, "memories.json");
const RULES_PATH = resolve(DATA_DIR, "rules.json");
const STATS_PATH = resolve(DATA_DIR, "stats.json");
const CONFIG_PATH = resolve(DATA_DIR, "config.json");
const HISTORY_PATH = resolve(DATA_DIR, "history.json");
const GRAPH_PATH = resolve(DATA_DIR, "graph.json");
const HYPOTHESES_PATH = resolve(DATA_DIR, "hypotheses.json");
const EVAL_PATH = resolve(DATA_DIR, "eval.json");
const JOURNAL_PATH = resolve(DATA_DIR, "journal.json");
const USER_MODEL_PATH = resolve(DATA_DIR, "user_model.json");
const SOUL_EVOLVED_PATH = resolve(DATA_DIR, "soul_evolved.json");
const PATTERNS_PATH = resolve(DATA_DIR, "patterns.json");
const FOLLOW_UPS_PATH = resolve(DATA_DIR, "followups.json");
const PLANS_PATH = resolve(DATA_DIR, "plans.json");
const WORKFLOWS_PATH = resolve(DATA_DIR, "workflows.json");
const FEATURES_PATH = resolve(DATA_DIR, "features.json");
const SYNC_CONFIG_PATH = resolve(DATA_DIR, "sync_config.json");
const SYNC_EXPORT_PATH = resolve(DATA_DIR, "sync-export.jsonl");
const SYNC_IMPORT_PATH = resolve(DATA_DIR, "sync-import.jsonl");
const UPGRADE_META_PATH = resolve(DATA_DIR, "upgrade_meta.json");
const REMINDERS_PATH = resolve(DATA_DIR, "reminders.json");
const _pluginsCode = resolve(homedir(), ".openclaw/plugins/cc-soul/cc-soul");
const _hooksCode = resolve(homedir(), ".openclaw/hooks/cc-soul/cc-soul");
const _moduleDir = existsSync(_pluginsCode) ? _pluginsCode : _hooksCode;
const HANDLER_PATH = resolve(_moduleDir, "handler.ts");
const MODULE_DIR = _moduleDir;
const HANDLER_BACKUP_DIR = resolve(DATA_DIR, "backups");
function ensureDataDir() {
  if (!existsSync(DATA_DIR)) {
    mkdirSync(DATA_DIR, { recursive: true });
  }
}
let _kvDb = null;
let _kvDbFailed = false;
function getKVDb() {
  if (_kvDb || _kvDbFailed) return _kvDb;
  try {
    const dbPath = resolve(DATA_DIR, "soul_kv.db");
    const { DatabaseSync } = require("node:sqlite");
    _kvDb = new DatabaseSync(dbPath);
    _kvDb.exec("CREATE TABLE IF NOT EXISTS kv (key TEXT PRIMARY KEY, value TEXT, updated_at INTEGER)");
    _migrateJsonToSqlite();
    console.log(`[cc-soul][kv] SQLite KV store ready (${dbPath})`);
  } catch (e) {
    console.error(`[cc-soul][kv] SQLite init failed, falling back to JSON: ${e.message}`);
    _kvDbFailed = true;
  }
  return _kvDb;
}
function _kvKey(path) {
  return path.split("/").pop() || path;
}
function _migrateJsonToSqlite() {
  if (!_kvDb) return;
  try {
    const files = readdirSync(DATA_DIR).filter((f) => f.endsWith(".json"));
    let migrated = 0;
    const stmt = _kvDb.prepare("INSERT OR IGNORE INTO kv (key, value, updated_at) VALUES (?, ?, ?)");
    for (const f of files) {
      try {
        const raw = readFileSync(resolve(DATA_DIR, f), "utf-8").trim();
        if (raw) {
          stmt.run(f, raw, Date.now());
          migrated++;
        }
      } catch {
      }
    }
    if (migrated > 0) console.log(`[cc-soul][kv] migrated ${migrated} JSON files to SQLite`);
  } catch {
  }
}
function loadJson(path, fallback) {
  const db = getKVDb();
  const key = _kvKey(path);
  if (db) {
    try {
      const row = db.prepare("SELECT value FROM kv WHERE key = ?").get(key);
      if (row?.value) return JSON.parse(row.value);
    } catch {
    }
    return fallback;
  }
  try {
    const raw = readFileSync(path, "utf-8").trim();
    if (!raw) return fallback;
    return JSON.parse(raw);
  } catch {
    return fallback;
  }
}
const pendingSaves = /* @__PURE__ */ new Map();
function saveJson(path, data) {
  const pending = pendingSaves.get(path);
  if (pending?.timer) clearTimeout(pending.timer);
  pendingSaves.delete(path);
  const db = getKVDb();
  const key = _kvKey(path);
  const json = JSON.stringify(data, null, 2);
  if (db) {
    try {
      db.prepare("INSERT OR REPLACE INTO kv (key, value, updated_at) VALUES (?, ?, ?)").run(key, json, Date.now());
      return;
    } catch (e) {
      console.error(`[cc-soul][kv] SQLite write failed: ${e.message}`);
    }
  }
  ensureDataDir();
  const tmp = path + ".tmp";
  try {
    writeFileSync(tmp, json, "utf-8");
    renameSync(tmp, path);
  } catch (e) {
    console.error(`[cc-soul] failed to save ${path}: ${e.message}`);
  }
}
function debouncedSave(path, data, delayMs = 3e3) {
  const existing = pendingSaves.get(path);
  if (existing?.timer) clearTimeout(existing.timer);
  const snapshot = JSON.parse(JSON.stringify(data));
  const timer = setTimeout(() => {
    saveJson(path, snapshot);
    pendingSaves.delete(path);
  }, delayMs);
  pendingSaves.set(path, { data: snapshot, timer });
}
function flushAll() {
  for (const [path, entry] of pendingSaves) {
    if (entry.timer) clearTimeout(entry.timer);
    saveJson(path, entry.data);
  }
  pendingSaves.clear();
  syncMemoriesToWorkspace();
}
let _lastSyncHash = "";
let _cachedMemoryMod = null;
import("./memory.ts").then((m) => {
  _cachedMemoryMod = m;
}).catch((e) => {
  console.error(`[cc-soul] module load failed (memory): ${e.message}`);
});
function syncMemoriesToWorkspace() {
  try {
    let memoryState;
    try {
      memoryState = _cachedMemoryMod?.memoryState;
    } catch {
      return;
    }
    if (!memoryState?.memories?.length) return;
    const SYNC_SCOPES = /* @__PURE__ */ new Set(["long_term", "preference", "fact", "correction", "consolidated", "pinned"]);
    const important = memoryState.memories.filter(
      (m) => SYNC_SCOPES.has(m.scope) || SYNC_SCOPES.has(m.tier) || m.confidence && m.confidence >= 0.9 || m.recallCount && m.recallCount >= 3
    ).filter((m) => m.scope !== "expired" && m.scope !== "decayed");
    if (important.length === 0) return;
    const hash = `${important.length}_${important[0]?.ts}_${important[important.length - 1]?.ts}`;
    if (hash === _lastSyncHash) return;
    _lastSyncHash = hash;
    const lines = ["# cc-soul Memories\n", `> Auto-synced: ${(/* @__PURE__ */ new Date()).toISOString()} | ${important.length} entries
`];
    const grouped = /* @__PURE__ */ new Map();
    for (const m of important) {
      const key = m.scope || "other";
      if (!grouped.has(key)) grouped.set(key, []);
      grouped.get(key).push(m);
    }
    for (const [scope, mems] of grouped) {
      lines.push(`
## ${scope}
`);
      for (const m of mems.slice(0, 100)) {
        const emotionTag = m.emotion && m.emotion !== "neutral" ? ` [${m.emotion}]` : "";
        lines.push(`- ${m.content}${emotionTag}`);
      }
    }
    const workspaceMemDir = resolve(homedir(), ".openclaw/workspace/memory");
    mkdirSync(workspaceMemDir, { recursive: true });
    const outPath = resolve(workspaceMemDir, "cc-soul-memories.md");
    writeFileSync(outPath, lines.join("\n"), "utf-8");
    console.log(`[cc-soul][sync-workspace] synced ${important.length} memories to ${outPath}`);
  } catch (e) {
    console.error(`[cc-soul][sync-workspace] ${e.message}`);
  }
}
function adaptiveCooldown(baseMs, userId) {
  if (!userId) return baseMs;
  try {
    let getProfile;
    try {
      getProfile = require("./user-profiles.ts").getProfile;
    } catch {
      return baseMs;
    }
    const profile = getProfile(userId);
    if (!profile || !profile.firstSeen || !profile.messageCount) return baseMs;
    const daysSince = Math.max(1, (Date.now() - profile.firstSeen) / 864e5);
    const msgsPerDay = profile.messageCount / daysSince;
    const factor = Math.max(0.33, Math.min(3, 15 / Math.max(1, msgsPerDay)));
    return Math.round(baseMs * factor);
  } catch {
    return baseMs;
  }
}
function loadConfig() {
  const config = {};
  try {
    if (existsSync(CONFIG_PATH)) {
      const file = JSON.parse(readFileSync(CONFIG_PATH, "utf-8"));
      if (file.notify_webhook) config.notify_webhook = file.notify_webhook;
      if (file.sync) config.sync = file.sync;
    }
  } catch {
  }
  if (process.env.CC_SOUL_NOTIFY_WEBHOOK) config.notify_webhook = process.env.CC_SOUL_NOTIFY_WEBHOOK;
  return config;
}
const soulConfig = loadConfig();
let _shutdownRegistered = false;
function registerShutdownHooks() {
  if (_shutdownRegistered) return;
  _shutdownRegistered = true;
  const onExit = (signal) => {
    console.log(`[cc-soul][persistence] ${signal} received, flushing ${pendingSaves.size} pending saves\u2026`);
    flushAll();
  };
  process.on("SIGINT", () => {
    onExit("SIGINT");
    process.exit(0);
  });
  process.on("SIGTERM", () => {
    onExit("SIGTERM");
    process.exit(0);
  });
  process.on("beforeExit", () => {
    onExit("beforeExit");
  });
}
registerShutdownHooks();
export {
  BRAIN_PATH,
  CONFIG_PATH,
  DATA_DIR,
  EVAL_PATH,
  FEATURES_PATH,
  FOLLOW_UPS_PATH,
  GRAPH_PATH,
  HANDLER_BACKUP_DIR,
  HANDLER_PATH,
  HISTORY_PATH,
  HYPOTHESES_PATH,
  JOURNAL_PATH,
  MEMORIES_PATH,
  MODULE_DIR,
  PATTERNS_PATH,
  PLANS_PATH,
  REMINDERS_PATH,
  RULES_PATH,
  SOUL_EVOLVED_PATH,
  STATS_PATH,
  SYNC_CONFIG_PATH,
  SYNC_EXPORT_PATH,
  SYNC_IMPORT_PATH,
  UPGRADE_META_PATH,
  USER_MODEL_PATH,
  WORKFLOWS_PATH,
  adaptiveCooldown,
  debouncedSave,
  ensureDataDir,
  flushAll,
  getActiveAgent,
  getAgentDataDir,
  loadConfig,
  loadJson,
  registerShutdownHooks,
  saveJson,
  setActiveAgent,
  soulConfig
};
