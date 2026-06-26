/**
 * cc-soul — Data persistence layer
 *
 * Handles all file I/O: path constants, atomic save, debounced writes, config loading.
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync, renameSync, readdirSync } from 'fs'
import { resolve } from 'path'
import { homedir } from 'os'
import type { SoulConfig } from './types.ts'

// ═══════════════════════════════════════════════════════════════════════════════
// PATH CONSTANTS
// ═══════════════════════════════════════════════════════════════════════════════

// Data directory: auto-detect, no configuration needed
// OpenClaw users → existing path; everyone else → ~/.cc-soul/data (auto-created)
const _pluginsData = resolve(homedir(), '.openclaw/plugins/cc-soul/data')
const _hooksData = resolve(homedir(), '.openclaw/hooks/cc-soul/data')
const _standaloneData = resolve(homedir(), '.cc-soul/data')
export const DATA_DIR = existsSync(_pluginsData) ? _pluginsData
  : existsSync(_hooksData) ? _hooksData
  : _standaloneData

// ── Multi-agent isolation: each agent gets its own data subdirectory ──
let _activeAgentId = 'default'
export function setActiveAgent(agentId: string) {
  if (!agentId || agentId === _activeAgentId) return
  _activeAgentId = agentId
  const agentDir = resolve(DATA_DIR, 'agents', agentId)
  if (!existsSync(agentDir)) mkdirSync(agentDir, { recursive: true })
  console.log(`[cc-soul] active agent: ${agentId} → ${agentDir}`)
}
export function getActiveAgent(): string { return _activeAgentId }
export function getAgentDataDir(agentId?: string): string {
  const id = agentId || _activeAgentId
  if (id === 'default') return DATA_DIR  // backward compat: default agent uses root data dir
  const dir = resolve(DATA_DIR, 'agents', id)
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true })
  return dir
}
export const BRAIN_PATH = resolve(DATA_DIR, 'brain.json')
export const MEMORIES_PATH = resolve(DATA_DIR, 'memories.json')
export const RULES_PATH = resolve(DATA_DIR, 'rules.json')
export const STATS_PATH = resolve(DATA_DIR, 'stats.json')
export const CONFIG_PATH = resolve(DATA_DIR, 'config.json')
export const HISTORY_PATH = resolve(DATA_DIR, 'history.json')
export const GRAPH_PATH = resolve(DATA_DIR, 'graph.json')
export const HYPOTHESES_PATH = resolve(DATA_DIR, 'hypotheses.json')
export const EVAL_PATH = resolve(DATA_DIR, 'eval.json')
export const JOURNAL_PATH = resolve(DATA_DIR, 'journal.json')
export const USER_MODEL_PATH = resolve(DATA_DIR, 'user_model.json')
export const SOUL_EVOLVED_PATH = resolve(DATA_DIR, 'soul_evolved.json')
export const PATTERNS_PATH = resolve(DATA_DIR, 'patterns.json')
export const FOLLOW_UPS_PATH = resolve(DATA_DIR, 'followups.json')
export const PLANS_PATH = resolve(DATA_DIR, 'plans.json')
export const WORKFLOWS_PATH = resolve(DATA_DIR, 'workflows.json')
export const FEATURES_PATH = resolve(DATA_DIR, 'features.json')
export const SYNC_CONFIG_PATH = resolve(DATA_DIR, 'sync_config.json')
export const SYNC_EXPORT_PATH = resolve(DATA_DIR, 'sync-export.jsonl')
export const SYNC_IMPORT_PATH = resolve(DATA_DIR, 'sync-import.jsonl')
export const UPGRADE_META_PATH = resolve(DATA_DIR, 'upgrade_meta.json')
export const REMINDERS_PATH = resolve(DATA_DIR, 'reminders.json')
const _pluginsCode = resolve(homedir(), '.openclaw/plugins/cc-soul/cc-soul')
const _hooksCode = resolve(homedir(), '.openclaw/hooks/cc-soul/cc-soul')
const _moduleDir = existsSync(_pluginsCode) ? _pluginsCode : _hooksCode
/** @deprecated handler.ts is deprecated — use handler-state/handler-commands/handler-augments instead */
export const HANDLER_PATH = resolve(_moduleDir, 'handler.ts')
export const MODULE_DIR = _moduleDir
export const HANDLER_BACKUP_DIR = resolve(DATA_DIR, 'backups')

// ═══════════════════════════════════════════════════════════════════════════════
// ENSURE DATA DIR
// ═══════════════════════════════════════════════════════════════════════════════

export function ensureDataDir() {
  if (!existsSync(DATA_DIR)) {
    mkdirSync(DATA_DIR, { recursive: true })
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// LOAD JSON
// ═══════════════════════════════════════════════════════════════════════════════

// ── SQLite KV Store (primary) — JSON files as fallback ──
let _kvDb: any = null
let _kvDbFailed = false

function getKVDb() {
  if (_kvDb || _kvDbFailed) return _kvDb
  try {
    const dbPath = resolve(DATA_DIR, 'soul_kv.db')
    const { DatabaseSync } = require('node:sqlite')
    _kvDb = new DatabaseSync(dbPath)
    _kvDb.exec('CREATE TABLE IF NOT EXISTS kv (key TEXT PRIMARY KEY, value TEXT, updated_at INTEGER)')
    _migrateJsonToSqlite()
    console.log(`[cc-soul][kv] SQLite KV store ready (${dbPath})`)
  } catch (e: any) {
    console.error(`[cc-soul][kv] SQLite init failed, falling back to JSON: ${e.message}`)
    _kvDbFailed = true
  }
  return _kvDb
}

function _kvKey(path: string): string {
  // Extract filename from path: /Users/.../data/features.json → features.json
  return path.split('/').pop() || path
}

function _migrateJsonToSqlite() {
  if (!_kvDb) return
  try {
    const files = readdirSync(DATA_DIR).filter(f => f.endsWith('.json'))
    let migrated = 0
    const stmt = _kvDb.prepare('INSERT OR IGNORE INTO kv (key, value, updated_at) VALUES (?, ?, ?)')
    for (const f of files) {
      try {
        const raw = readFileSync(resolve(DATA_DIR, f), 'utf-8').trim()
        if (raw) { stmt.run(f, raw, Date.now()); migrated++ }
      } catch {}
    }
    if (migrated > 0) console.log(`[cc-soul][kv] migrated ${migrated} JSON files to SQLite`)
  } catch {}
}

export function loadJson<T>(path: string, fallback: T): T {
  const db = getKVDb()
  const key = _kvKey(path)

  // SQLite KV 是唯一数据源，不再 fallback 到 JSON 文件
  if (db) {
    try {
      const row = db.prepare('SELECT value FROM kv WHERE key = ?').get(key) as { value: string } | undefined
      if (row?.value) return JSON.parse(row.value)
    } catch {}
    return fallback  // SQLite 里没有 → 用默认值
  }

  // SQLite 不可用（init 失败）→ 只在这种极端情况下读 JSON
  try {
    const raw = readFileSync(path, 'utf-8').trim()
    if (!raw) return fallback
    return JSON.parse(raw)
  } catch {
    return fallback
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// SAVE JSON + DEBOUNCED SAVE — atomic write (tmp + rename), debounce layer
// ═══════════════════════════════════════════════════════════════════════════════

const pendingSaves = new Map<string, { data: any; timer: ReturnType<typeof setTimeout> | null }>()

export function saveJson(path: string, data: any) {
  const pending = pendingSaves.get(path)
  if (pending?.timer) clearTimeout(pending.timer)
  pendingSaves.delete(path)

  const db = getKVDb()
  const key = _kvKey(path)
  const json = JSON.stringify(data, null, 2)

  // SQLite KV 是唯一写入目标，不再写 JSON 文件
  if (db) {
    try {
      db.prepare('INSERT OR REPLACE INTO kv (key, value, updated_at) VALUES (?, ?, ?)').run(key, json, Date.now())
      return
    } catch (e: any) {
      console.error(`[cc-soul][kv] SQLite write failed: ${e.message}`)
    }
  }

  // SQLite 不可用（极端情况）→ 写 JSON
  ensureDataDir()
  const tmp = path + '.tmp'
  try {
    writeFileSync(tmp, json, 'utf-8')
    renameSync(tmp, path)
  } catch (e: any) {
    console.error(`[cc-soul] failed to save ${path}: ${e.message}`)
  }
}

export function debouncedSave(path: string, data: any, delayMs = 3000) {
  const existing = pendingSaves.get(path)
  if (existing?.timer) clearTimeout(existing.timer)
  const snapshot = JSON.parse(JSON.stringify(data))
  const timer = setTimeout(() => {
    saveJson(path, snapshot)
    pendingSaves.delete(path)
  }, delayMs)
  pendingSaves.set(path, { data: snapshot, timer })
}

export function flushAll() {
  for (const [path, entry] of pendingSaves) {
    if (entry.timer) clearTimeout(entry.timer)
    saveJson(path, entry.data)
  }
  pendingSaves.clear()

  // Sync essential memories to OpenClaw workspace for native memory_search compatibility
  // This ensures memories survive cc-soul uninstall
  syncMemoriesToWorkspace()
}

// ── Sync cc-soul memories to OpenClaw workspace ──
// Writes a markdown snapshot of important memories to ~/.openclaw/workspace/memory/
// OpenClaw's native memory_search indexes this directory

let _lastSyncHash = ''
let _cachedMemoryMod: any = null
import('./memory.ts').then(m => { _cachedMemoryMod = m }).catch((e: any) => { console.error(`[cc-soul] module load failed (memory): ${e.message}`) })

function syncMemoriesToWorkspace() {
  try {
    // Dynamic import to avoid circular dependency (persistence ← memory ← persistence)
    let memoryState: any
    try { memoryState = _cachedMemoryMod?.memoryState } catch { return }
    if (!memoryState?.memories?.length) return

    // Filter: only long-term, preference, fact, correction, consolidated
    const SYNC_SCOPES = new Set(['long_term', 'preference', 'fact', 'correction', 'consolidated', 'pinned'])
    const important = memoryState.memories.filter((m: any) =>
      SYNC_SCOPES.has(m.scope) ||
      SYNC_SCOPES.has(m.tier) ||
      (m.confidence && m.confidence >= 0.9) ||
      (m.recallCount && m.recallCount >= 3)
    ).filter((m: any) => m.scope !== 'expired' && m.scope !== 'decayed')

    if (important.length === 0) return

    // Quick hash check to avoid unnecessary writes
    const hash = `${important.length}_${important[0]?.ts}_${important[important.length - 1]?.ts}`
    if (hash === _lastSyncHash) return
    _lastSyncHash = hash

    // Build markdown
    const lines = ['# cc-soul Memories\n', `> Auto-synced: ${new Date().toISOString()} | ${important.length} entries\n`]

    // Group by scope
    const grouped = new Map<string, any[]>()
    for (const m of important) {
      const key = m.scope || 'other'
      if (!grouped.has(key)) grouped.set(key, [])
      grouped.get(key)!.push(m)
    }

    for (const [scope, mems] of grouped) {
      lines.push(`\n## ${scope}\n`)
      for (const m of mems.slice(0, 100)) { // cap per scope
        const emotionTag = m.emotion && m.emotion !== 'neutral' ? ` [${m.emotion}]` : ''
        lines.push(`- ${m.content}${emotionTag}`)
      }
    }

    // Write to workspace
    const workspaceMemDir = resolve(homedir(), '.openclaw/workspace/memory')
    mkdirSync(workspaceMemDir, { recursive: true })
    const outPath = resolve(workspaceMemDir, 'cc-soul-memories.md')
    writeFileSync(outPath, lines.join('\n'), 'utf-8')
    console.log(`[cc-soul][sync-workspace] synced ${important.length} memories to ${outPath}`)
  } catch (e: any) {
    // Silent fail — workspace sync is best-effort
    console.error(`[cc-soul][sync-workspace] ${e.message}`)
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// ADAPTIVE COOLDOWN — activity-based cooldown scaling (Strategy C)
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Scale a cooldown based on user activity level.
 * High activity (>50 msgs/day) → 0.33x cooldown (more frequent processing)
 * Low activity (<5 msgs/day) → 3x cooldown (save resources)
 * Returns scaled cooldown in ms.
 */
export function adaptiveCooldown(baseMs: number, userId?: string): number {
  if (!userId) return baseMs
  try {
    // Lazy import to avoid circular dependency with user-profiles.ts
    let getProfile: any
    try { getProfile = require('./user-profiles.ts').getProfile } catch {
      return baseMs
    }
    const profile = getProfile(userId)
    if (!profile || !profile.firstSeen || !profile.messageCount) return baseMs
    const daysSince = Math.max(1, (Date.now() - profile.firstSeen) / 86400000)
    const msgsPerDay = profile.messageCount / daysSince
    // High active(>50/day) → 0.33x, low freq(<5/day) → 3x
    const factor = Math.max(0.33, Math.min(3.0, 15 / Math.max(1, msgsPerDay)))
    return Math.round(baseMs * factor)
  } catch { return baseMs }
}

// ═══════════════════════════════════════════════════════════════════════════════
// CONFIG — env vars first, fall back to config.json
// ═══════════════════════════════════════════════════════════════════════════════

export function loadConfig(): SoulConfig {
  const config: SoulConfig = {}
  // Load from config.json if exists
  try {
    if (existsSync(CONFIG_PATH)) {
      const file = JSON.parse(readFileSync(CONFIG_PATH, 'utf-8'))
      if (file.notify_webhook) config.notify_webhook = file.notify_webhook
      if (file.sync) config.sync = file.sync
    }
  } catch {
    // config.json missing or malformed — proceed with defaults
  }
  // Env var override
  if (process.env.CC_SOUL_NOTIFY_WEBHOOK) config.notify_webhook = process.env.CC_SOUL_NOTIFY_WEBHOOK
  return config
}

// Loaded once at module init
export const soulConfig = loadConfig()

// ═══════════════════════════════════════════════════════════════════════════════
// GRACEFUL SHUTDOWN — flush pending saves on process exit (#12)
// ═══════════════════════════════════════════════════════════════════════════════

let _shutdownRegistered = false

export function registerShutdownHooks() {
  if (_shutdownRegistered) return
  _shutdownRegistered = true

  const onExit = (signal: string) => {
    console.log(`[cc-soul][persistence] ${signal} received, flushing ${pendingSaves.size} pending saves…`)
    flushAll()
  }

  process.on('SIGINT', () => { onExit('SIGINT'); process.exit(0) })
  process.on('SIGTERM', () => { onExit('SIGTERM'); process.exit(0) })
  process.on('beforeExit', () => { onExit('beforeExit') })
}

// Auto-register on module load
registerShutdownHooks()
