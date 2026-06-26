/**
 * sqlite-store.ts — SQLite storage layer
 *
 * Uses Node 22 built-in node:sqlite (zero dependencies).
 * Recall via tag/keyword search; semantic recall handled by activation-field.ts (NAM).
 */

import { resolve } from 'path'
import { existsSync, readFileSync } from 'fs'
import { homedir } from 'os'
import { createRequire } from 'module'
import { DATA_DIR, MEMORIES_PATH, REMINDERS_PATH, GRAPH_PATH } from './persistence.ts'
import type { Memory, Entity, Relation, StructuredFact } from './types.ts'
// embedder.ts removed — vector search retired, activation field handles all recall

// Database path: 始终使用 cc-soul 自己的独立数据库
// 学 Mem0/Zep/Letta：记忆系统有自己的数据库，不依赖宿主平台
const DB_PATH = resolve(DATA_DIR, 'soul.db')

// SQLite 工厂函数：测试时传 ':memory:' 隔离数据
let _overrideDbPath: string | null = null
export function setDbPath(path: string): void { _overrideDbPath = path }
export function getDbPath(): string { return _overrideDbPath ?? DB_PATH }

// Use globalThis to share db across multiple jiti module instances
const _g = globalThis as any
if (!_g.__ccSoulSqlite) _g.__ccSoulSqlite = { DatabaseSyncCtor: null, db: null, hasVec: false, sqliteReady: false }
const _s = _g.__ccSoulSqlite

// Aliases for convenient access
let DatabaseSyncCtor: any = _s.DatabaseSyncCtor
let db: any = _s.db
let hasVec: boolean = _s.hasVec
let sqliteReady: boolean = _s.sqliteReady

function _syncState() {
  _s.DatabaseSyncCtor = DatabaseSyncCtor; _s.db = db; _s.hasVec = hasVec; _s.sqliteReady = sqliteReady
}
function _loadState() {
  DatabaseSyncCtor = _s.DatabaseSyncCtor; db = _s.db; hasVec = _s.hasVec; sqliteReady = _s.sqliteReady
}

// ═══════════════════════════════════════════════════════════════════════════════
// INIT
// ═══════════════════════════════════════════════════════════════════════════════

export function initSQLite(): boolean {
  // Check if another call path already initialized (jiti creates separate module instances)
  if (_s.sqliteReady && _s.db) {
    db = _s.db; DatabaseSyncCtor = _s.DatabaseSyncCtor; hasVec = _s.hasVec; sqliteReady = true
    return true
  }
  if (sqliteReady) return true

  // Load DatabaseSync — try multiple approaches (jiti/hook loader / ESM can lack require)
  if (!DatabaseSyncCtor) {
    // Helper: safe require that handles ESM contexts where require is undefined
    const _require = typeof require !== 'undefined' ? require : null

    // Approach 1: direct require (CJS context)
    if (_require) {
      try { DatabaseSyncCtor = _require('node:sqlite').DatabaseSync } catch {}
    }
    // Approach 2: createRequire with various anchor points (works in ESM where require is undefined)
    if (!DatabaseSyncCtor) {
      let metaUrl: string | undefined
      try { metaUrl = new Function('return import.meta.url')() } catch {}
      const anchors = [
        typeof __filename !== 'undefined' ? __filename : undefined,
        metaUrl,
        process.argv[1],
        process.execPath,
      ].filter(Boolean)
      for (const anchor of anchors) {
        try {
          const req = createRequire(anchor as string)
          DatabaseSyncCtor = req('node:sqlite').DatabaseSync
          if (DatabaseSyncCtor) break
        } catch {}
      }
    }
    // Approach 3: use Node's internal module loader
    if (!DatabaseSyncCtor) {
      try { DatabaseSyncCtor = (globalThis as any).process?.mainModule?.require?.('node:sqlite')?.DatabaseSync } catch {}
    }
    if (!DatabaseSyncCtor) {
      console.log(`[cc-soul][sqlite] node:sqlite unavailable (need Node 22+) — using JSON fallback`)
      return false
    }
  }

  try {
    db = new DatabaseSyncCtor(getDbPath(), { allowExtension: true })
  } catch (e: any) {
    console.error(`[cc-soul][sqlite] failed to open ${DB_PATH}: ${e.message}`)
    return false
  }

  // sqlite-vec removed — activation field (NAM) handles all semantic recall

  // Schema — 独立数据库：先建 memories 表，再加扩展列
  db.exec(`
    CREATE TABLE IF NOT EXISTS memories (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      scope TEXT DEFAULT 'fact',
      content TEXT NOT NULL,
      created_at TEXT,
      raw_line TEXT,
      access_count INTEGER DEFAULT 0,
      last_accessed TEXT
    )
  `)
  // 实体和关系表（graph.ts 用）
  db.exec(`CREATE TABLE IF NOT EXISTS entities (name TEXT PRIMARY KEY, type TEXT DEFAULT 'entity')`)
  db.exec(`CREATE TABLE IF NOT EXISTS relations (source TEXT, target TEXT, type TEXT, PRIMARY KEY(source, target, type))`)

  // cc-soul 扩展列（ALTER TABLE ADD COLUMN 安全——已存在则忽略）
  const ccSoulColumns: [string, string][] = [
    ['ts', 'INTEGER'],
    ['emotion', "TEXT DEFAULT 'neutral'"],
    ['userId', 'TEXT'],
    ['visibility', "TEXT DEFAULT 'global'"],
    ['channelId', 'TEXT'],
    ['tags', "TEXT DEFAULT '[]'"],
    ['confidence', 'REAL DEFAULT 0.7'],
    ['lastAccessed', 'INTEGER'],
    ['tier', "TEXT DEFAULT 'short_term'"],
    ['recallCount', 'INTEGER DEFAULT 0'],
    ['lastRecalled', 'INTEGER'],
    ['validFrom', 'INTEGER'],
    ['validUntil', 'INTEGER'],
    ['prospectiveTags', "TEXT DEFAULT '[]'"],
    ['_entityIds', "TEXT DEFAULT '[]'"],
  ]
  for (const [col, def] of ccSoulColumns) {
    try { db.exec(`ALTER TABLE memories ADD COLUMN ${col} ${def}`) } catch { /* already exists */ }
  }
  try { db.exec('CREATE INDEX IF NOT EXISTS idx_mem_scope ON memories(scope)') } catch { /* ok */ }
  try { db.exec('CREATE INDEX IF NOT EXISTS idx_mem_ts ON memories(ts)') } catch { /* ok */ }
  try { db.exec('CREATE INDEX IF NOT EXISTS idx_mem_vis ON memories(visibility)') } catch { /* ok */ }
  try { db.exec('CREATE INDEX IF NOT EXISTS idx_mem_user ON memories(userId)') } catch { /* ok */ }
  // Composite indexes for 100K+ memory performance
  try { db.exec('CREATE INDEX IF NOT EXISTS idx_mem_scope_ts ON memories(scope, ts)') } catch { /* ok */ }
  try { db.exec('CREATE INDEX IF NOT EXISTS idx_mem_user_scope ON memories(userId, scope)') } catch { /* ok */ }
  try { db.exec('CREATE INDEX IF NOT EXISTS idx_mem_user_ts ON memories(userId, ts)') } catch { /* ok */ }
  try { db.exec('CREATE INDEX IF NOT EXISTS idx_mem_tier ON memories(tier)') } catch { /* ok */ }

  // Structured facts table (Mem0-style triples, replaces structured_facts.json)
  db.exec(`
    CREATE TABLE IF NOT EXISTS structured_facts (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      subject TEXT NOT NULL,
      predicate TEXT NOT NULL,
      object TEXT NOT NULL,
      confidence REAL DEFAULT 0.7,
      source TEXT DEFAULT 'ai_observed',
      ts INTEGER NOT NULL,
      validUntil INTEGER DEFAULT 0,
      memoryRef TEXT
    );
    CREATE INDEX IF NOT EXISTS idx_fact_subj ON structured_facts(subject);
    CREATE INDEX IF NOT EXISTS idx_fact_subj_pred ON structured_facts(subject, predicate);
    CREATE INDEX IF NOT EXISTS idx_fact_valid ON structured_facts(validUntil);
  `)

  // Chat history table
  db.exec(`
    CREATE TABLE IF NOT EXISTS chat_history (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_msg TEXT NOT NULL,
      assistant_msg TEXT NOT NULL,
      ts INTEGER NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_chat_ts ON chat_history(ts);
  `)

  sqliteReady = true
  _syncState() // Share db connection across jiti module instances

  // ── Entity graph: ALTER TABLE to add cc-soul columns ──
  const entityColumns: [string, string][] = [
    ['mentions', 'INTEGER DEFAULT 0'],
    ['firstSeen', 'INTEGER'],
    ['attrs', "TEXT DEFAULT '[]'"],
    ['valid_at', 'INTEGER DEFAULT 0'],
    ['invalid_at', 'INTEGER'],
  ]
  for (const [col, def] of entityColumns) {
    try { db.exec(`ALTER TABLE entities ADD COLUMN ${col} ${def}`) } catch { /* already exists */ }
  }
  const relationColumns: [string, string][] = [
    ['ts', 'INTEGER'],
    ['valid_at', 'INTEGER DEFAULT 0'],
    ['invalid_at', 'INTEGER'],
    ['weight', 'REAL DEFAULT 1.0'],
    ['confidence', 'REAL DEFAULT 0.7'],
  ]
  for (const [col, def] of relationColumns) {
    try { db.exec(`ALTER TABLE relations ADD COLUMN ${col} ${def}`) } catch { /* already exists */ }
  }

  // ── P0-P3: 新增列和表 ──

  // P1a: Memory 表加 injection engagement 列
  const p1aColumns: [string, string][] = [
    ['injectionEngagement', 'INTEGER DEFAULT 0'],
    ['injectionMiss', 'INTEGER DEFAULT 0'],
  ]
  for (const [col, def] of p1aColumns) {
    try { db.exec(`ALTER TABLE memories ADD COLUMN ${col} ${def}`) } catch {}
  }

  // MemRL: utility score column
  try { db.exec(`ALTER TABLE memories ADD COLUMN utility REAL DEFAULT 0`) } catch {}

  // P0a: Graveyard 元数据列
  const p0aColumns: [string, string][] = [
    ['_graveyardOriginalScope', 'TEXT'],
    ['_graveyardTs', 'INTEGER'],
    ['_needsVerification', 'INTEGER DEFAULT 0'],
    ['bayesAlpha', 'REAL DEFAULT 2'],
    ['bayesBeta', 'REAL DEFAULT 1'],
  ]
  for (const [col, def] of p0aColumns) {
    try { db.exec(`ALTER TABLE memories ADD COLUMN ${col} ${def}`) } catch {}
  }

  // P0c: 决策日志表
  db.exec(`
    CREATE TABLE IF NOT EXISTS decision_log (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      action TEXT NOT NULL,
      key TEXT NOT NULL,
      reason TEXT NOT NULL,
      ts INTEGER NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_decision_ts ON decision_log(ts);
    CREATE INDEX IF NOT EXISTS idx_decision_action ON decision_log(action);
  `)

  // P0b: Topic nodes 表（替代 topic_nodes.json）
  db.exec(`
    CREATE TABLE IF NOT EXISTS topic_nodes (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      topic TEXT NOT NULL,
      summary TEXT NOT NULL,
      sourceCount INTEGER DEFAULT 0,
      lastUpdated INTEGER NOT NULL,
      userId TEXT,
      hitCount INTEGER DEFAULT 0,
      missCount INTEGER DEFAULT 0,
      lastHitTs INTEGER DEFAULT 0,
      stale INTEGER DEFAULT 0,
      confidence REAL DEFAULT 0.5
    );
    CREATE INDEX IF NOT EXISTS idx_topic_user ON topic_nodes(userId);
  `)

  // P1c: Mental models 表（替代 mental_models.json）
  db.exec(`
    CREATE TABLE IF NOT EXISTS mental_models (
      userId TEXT PRIMARY KEY,
      model TEXT NOT NULL,
      topics TEXT DEFAULT '[]',
      lastUpdated INTEGER NOT NULL,
      version INTEGER DEFAULT 1,
      section_identity TEXT DEFAULT '',
      section_style TEXT DEFAULT '',
      section_facts TEXT DEFAULT '',
      section_dynamics TEXT DEFAULT '',
      sectionUpdated_identity INTEGER DEFAULT 0,
      sectionUpdated_style INTEGER DEFAULT 0,
      sectionUpdated_facts INTEGER DEFAULT 0,
      sectionUpdated_dynamics INTEGER DEFAULT 0
    );
  `)

  // P2c: 蒸馏溢出队列表
  db.exec(`
    CREATE TABLE IF NOT EXISTS pending_distill (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      contents TEXT NOT NULL,
      clusteredAt INTEGER NOT NULL
    );
  `)

  // 蒸馏状态表（替代 distill_state.json）
  db.exec(`
    CREATE TABLE IF NOT EXISTS distill_state (
      key TEXT PRIMARY KEY,
      value TEXT NOT NULL
    );
  `)

  // FSRS 训练数据表（替代 fsrs_training.json）
  db.exec(`
    CREATE TABLE IF NOT EXISTS fsrs_training (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      elapsedDays REAL NOT NULL,
      stability REAL NOT NULL,
      recalled INTEGER NOT NULL,
      ts INTEGER NOT NULL
    );
  `)

  // 衰减参数表（替代 decay_params.json）
  db.exec(`
    CREATE TABLE IF NOT EXISTS decay_params (
      key TEXT PRIMARY KEY,
      value TEXT NOT NULL
    );
  `)

  // Augment 反馈表（替代 augment_feedback.json）
  db.exec(`
    CREATE TABLE IF NOT EXISTS augment_feedback (
      augmentType TEXT PRIMARY KEY,
      useful INTEGER DEFAULT 0,
      ignored INTEGER DEFAULT 0,
      totalScore REAL DEFAULT 0,
      count INTEGER DEFAULT 0,
      recentScores TEXT DEFAULT '[]'
    );
  `)

  // Auto-migrate cc-soul data from JSON to official DB on first connect
  migrateFromJSON()
  // habits/goals/reminders migration removed — life features deleted

  const count = (db.prepare('SELECT COUNT(*) as c FROM memories').get() as any)?.c || 0
  console.log(`[cc-soul][sqlite] database ready: ${count} memories, vec: ${hasVec}, db: ${DB_PATH}`)
  return true
}

// ═══════════════════════════════════════════════════════════════════════════════
// MIGRATE from JSON
// ═══════════════════════════════════════════════════════════════════════════════

export function migrateFromJSON() {
  if (!db) return

  // Check if cc-soul data already migrated (look for cc-soul specific scope values)
  const ccSoulCount = (db.prepare("SELECT COUNT(*) as c FROM memories WHERE scope IN ('fact','short_term','mid_term','long_term','pinned','correction','discovery','visual','preference','consolidated')").get() as any)?.c || 0
  if (ccSoulCount > 0) return // already migrated

  if (!existsSync(MEMORIES_PATH)) return

  try {
    const memories: Memory[] = JSON.parse(readFileSync(MEMORIES_PATH, 'utf-8'))
    if (!Array.isArray(memories) || memories.length === 0) return

    console.log(`[cc-soul][sqlite] migrating ${memories.length} memories from JSON...`)

    const insert = db.prepare(`
      INSERT OR IGNORE INTO memories (content, scope, ts, created_at, raw_line, emotion, userId, visibility, channelId, tags, confidence, lastAccessed, access_count, tier, recallCount, lastRecalled, validFrom, validUntil, prospectiveTags, _entityIds)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `)

    db.exec('BEGIN')
    try {
      for (const m of memories) {
        if (m.scope === 'expired') continue
        const tsVal = m.ts || Date.now()
        insert.run(
          m.content,
          m.scope,
          tsVal,
          new Date(tsVal).toISOString(),
          m.content.slice(0, 200),
          m.emotion || 'neutral',
          m.userId || null,
          m.visibility || 'global',
          m.channelId || null,
          JSON.stringify(m.tags || []),
          m.confidence ?? 0.7,
          m.lastAccessed || null,
          0,
          m.tier || 'short_term',
          m.recallCount || 0,
          m.lastRecalled || null,
          m.validFrom || null,
          m.validUntil || null,
          JSON.stringify(m.prospectiveTags || []),
          JSON.stringify(m._entityIds || []),
        )
      }
      db.exec('COMMIT')
    } catch (e) {
      db.exec('ROLLBACK')
      throw e
    }

    const migrated = (db.prepare('SELECT COUNT(*) as c FROM memories').get() as any)?.c || 0
    console.log(`[cc-soul][sqlite] migrated ${migrated} memories to SQLite`)
  } catch (e: any) {
    console.error(`[cc-soul][sqlite] migration failed: ${e.message}`)
  }
}

/**
 * Migrate chat history from JSON to SQLite.
 */
export function migrateHistoryFromJSON(historyPath: string) {
  if (!db) return
  const count = (db.prepare('SELECT COUNT(*) as c FROM chat_history').get() as any)?.c || 0
  if (count > 0) return

  if (!existsSync(historyPath)) return

  try {
    const history = JSON.parse(readFileSync(historyPath, 'utf-8'))
    if (!Array.isArray(history) || history.length === 0) return

    console.log(`[cc-soul][sqlite] migrating ${history.length} chat turns from JSON...`)

    const insert = db.prepare('INSERT INTO chat_history (user_msg, assistant_msg, ts) VALUES (?, ?, ?)')
    db.exec('BEGIN')
    try {
      for (const turn of history) {
        insert.run(turn.user || '', turn.assistant || '', turn.ts || Date.now())
      }
      db.exec('COMMIT')
    } catch (e) {
      db.exec('ROLLBACK')
      throw e
    }

    console.log(`[cc-soul][sqlite] migrated ${history.length} chat turns to SQLite`)
  } catch (e: any) {
    console.error(`[cc-soul][sqlite] chat history migration failed: ${e.message}`)
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// MEMORY CRUD
// ═══════════════════════════════════════════════════════════════════════════════

export function sqliteAddMemory(mem: Omit<Memory, 'relevance'>): number {
  if (!db) return -1
  const now = Date.now()
  const tsVal = mem.ts || now
  const result = db.prepare(`
    INSERT OR IGNORE INTO memories (content, scope, ts, created_at, raw_line, emotion, userId, visibility, channelId, tags, confidence, lastAccessed, access_count, tier, recallCount, validFrom, validUntil, prospectiveTags, _entityIds)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
  `).run(
    mem.content,
    mem.scope,
    tsVal,
    new Date(tsVal).toISOString(),  // official field
    mem.content.slice(0, 200),       // official field
    mem.emotion || 'neutral',
    mem.userId || null,
    mem.visibility || 'global',
    mem.channelId || null,
    JSON.stringify(mem.tags || []),
    mem.confidence ?? 0.7,
    mem.lastAccessed || now,
    0,                                // official access_count
    mem.tier || 'short_term',
    mem.recallCount || 0,
    mem.validFrom || null,
    mem.validUntil || null,
    JSON.stringify(mem.prospectiveTags || []),
    JSON.stringify(mem._entityIds || []),
  )
  const id = Number(result.lastInsertRowid)

  return id
}

export function sqliteUpdateMemory(id: number, updates: Partial<Memory>) {
  if (!db) return
  const sets: string[] = []
  const values: any[] = []
  if (updates.scope !== undefined) { sets.push('scope = ?'); values.push(updates.scope) }
  if (updates.content !== undefined) { sets.push('content = ?'); values.push(updates.content) }
  if (updates.emotion !== undefined) { sets.push('emotion = ?'); values.push(updates.emotion) }
  if (updates.tags !== undefined) { sets.push('tags = ?'); values.push(JSON.stringify(updates.tags)) }
  if (updates.confidence !== undefined) { sets.push('confidence = ?'); values.push(updates.confidence) }
  if (updates.lastAccessed !== undefined) { sets.push('lastAccessed = ?'); values.push(updates.lastAccessed) }
  if (updates.tier !== undefined) { sets.push('tier = ?'); values.push(updates.tier) }
  if (updates.recallCount !== undefined) { sets.push('recallCount = ?'); values.push(updates.recallCount) }
  if (updates.lastRecalled !== undefined) { sets.push('lastRecalled = ?'); values.push(updates.lastRecalled) }
  if (updates.validUntil !== undefined) { sets.push('validUntil = ?'); values.push(updates.validUntil) }
  if (updates.utility !== undefined) { sets.push('utility = ?'); values.push(updates.utility) }
  if (sets.length === 0) return
  values.push(id)
  db.prepare(`UPDATE memories SET ${sets.join(', ')} WHERE id = ?`).run(...values)

}

/**
 * Update the raw_line column for DAG archiving (preserves original content).
 */
export function sqliteUpdateRawLine(id: number, rawLine: string): void {
  if (!db) return
  db.prepare('UPDATE memories SET raw_line = ? WHERE id = ?').run(rawLine, id)
}

export function sqliteGetAll(excludeExpired = true): Memory[] {
  if (!db) return []
  const where = excludeExpired ? "WHERE scope != 'expired'" : ''
  return (db.prepare(`SELECT * FROM memories ${where} ORDER BY ts DESC`).all() as any[]).map(rowToMemory)
}

export function sqliteCount(): number {
  if (!db) return 0
  return (db.prepare("SELECT COUNT(*) as c FROM memories WHERE scope != 'expired'").get() as any)?.c || 0
}

/**
 * Find memory by content (for dedup/update). Returns {id, memory} or null.
 */
export function sqliteFindByContent(content: string): { id: number; memory: Memory } | null {
  if (!db) return null
  const row = db.prepare('SELECT * FROM memories WHERE content = ? AND scope != ? LIMIT 1').get(content, 'expired') as any
  if (!row) return null
  return { id: row.id, memory: rowToMemory(row) }
}

// ═══════════════════════════════════════════════════════════════════════════════
// RECALL — vector search (primary when available) + tag/keyword fallback
// ── Weibull recency (unified with smart-forget.ts model, inlined to avoid circular import) ──
const WEIBULL_K = 1.5
const WEIBULL_LAMBDA: Record<string, number> = { fact: 30, preference: 90, correction: Infinity, episode: 14, emotion: 7 }
function weibullRecency(ageDays: number, scope?: string): number {
  const lambda = WEIBULL_LAMBDA[scope || 'fact'] ?? 30
  if (!isFinite(lambda)) return 1.0
  if (ageDays <= 0) return 1.0
  return Math.exp(-Math.pow(ageDays / lambda, WEIBULL_K))
}

// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Recall memories relevant to msg. Tag/keyword search (activation field handles semantic recall).
 */
export async function sqliteRecall(msg: string, topN = 3, userId?: string, channelId?: string): Promise<Memory[]> {
  if (!db) return []
  return tagRecall(msg, topN, userId, channelId)
}

/**
 * Synchronous tag/keyword recall — used as fallback when vectors unavailable.
 */
export function tagRecall(msg: string, topN = 3, userId?: string, channelId?: string): Memory[] {
  if (!db) return []

  const queryWords = (msg.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map(w => w.toLowerCase())
  if (queryWords.length === 0) return []

  let visWhere = "AND scope NOT IN ('expired','archived')"
  const params: any[] = []
  if (channelId) {
    visWhere += ` AND (visibility = 'global' OR (visibility = 'channel' AND channelId = ?))`
    params.push(channelId)
  }
  if (userId) {
    visWhere += ` AND (visibility != 'private' OR userId = ?)`
    params.push(userId)
  }

  // Search both recent memories AND preference/wal/fact memories (which are often older but important)
  const all = db.prepare(`SELECT * FROM memories WHERE 1=1 ${visWhere} ORDER BY ts DESC LIMIT 500`).all(...params) as any[]
  // Also include important scopes that might be older
  const important = db.prepare(`SELECT * FROM memories WHERE scope IN ('preference','wal','fact','consolidated','pinned') ${visWhere} ORDER BY ts DESC LIMIT 100`).all(...params) as any[]
  const seenIds = new Set(all.map((r: any) => r.id))
  for (const r of important) { if (!seenIds.has(r.id)) { all.push(r); seenIds.add(r.id) } }

  const scored: (Memory & { score: number })[] = []
  for (const row of all) {
    const mem = rowToMemory(row)
    let sim = 0

    const tags: string[] = mem.tags || []
    if (tags.length > 0) {
      let hits = 0
      for (const qw of queryWords) {
        for (const tag of tags) {
          if (tag.includes(qw) || qw.includes(tag)) { hits++; break }
        }
      }
      sim = hits / Math.max(1, queryWords.length)
    } else {
      const content = mem.content.toLowerCase()
      const hits = queryWords.filter(w => content.includes(w)).length
      sim = hits / Math.max(1, queryWords.length) * 0.7
    }

    if (sim < 0.05) continue

    const ageDays = (Date.now() - mem.ts) / 86400000
    const recency = weibullRecency(ageDays, mem.scope)
    const scopeBoost = (mem.scope === 'preference' || mem.scope === 'fact') ? 1.3
      : (mem.scope === 'correction') ? 1.5
      : (mem.scope === 'consolidated') ? 1.5
      : 1.0
    const emotionBoost = mem.emotion === 'important' ? 1.4
      : mem.emotion === 'painful' ? 1.3
      : mem.emotion === 'warm' ? 1.2
      : 1.0
    const userBoost = (userId && mem.userId === userId) ? 1.3 : 1.0
    const confidenceWeight = mem.confidence ?? 0.7
    // DAG archive: archived memories participate with reduced weight
    const archiveWeight = mem.scope === 'archived' ? 0.3 : 1.0
    // ── Parity with recallWithScores: add missing 5 dimensions ──
    const usageBoost = (mem.tags && mem.tags.length > 5) ? 1.2 : 1.0
    const consolidatedBoost = mem.scope === 'consolidated' ? 1.5 : mem.scope === 'pinned' ? 2.0 : 1.0
    const lastAcc = mem.lastAccessed || mem.ts || 0
    const accAgeDays = (Date.now() - lastAcc) / 86400000
    const tierWeight = ((accAgeDays <= 1 || (mem.recallCount ?? 0) >= 5) ? 1.5
                      : (accAgeDays <= 7) ? 1.0
                      : (accAgeDays <= 30) ? 0.8 : 0.5)
    const temporalWeight = (mem.validUntil && mem.validUntil > 0 && mem.validUntil < Date.now()) ? 0.3 : 1.0

    scored.push({ ...mem, score: sim * recency * scopeBoost * emotionBoost * userBoost * confidenceWeight * archiveWeight * usageBoost * consolidatedBoost * tierWeight * temporalWeight })
  }

  scored.sort((a, b) => b.score - a.score)
  return scored.slice(0, topN)
}

// vectorRecall, storeEmbeddingAsync, backfillEmbeddings removed — vector search retired

// ═══════════════════════════════════════════════════════════════════════════════
// TIME-BASED RECALL — uses (scope, ts) composite index for O(log n) queries
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Time-range recall via SQLite. Uses idx_mem_scope_ts composite index.
 * Returns memories between `from` and `to` (ms timestamps), excluding expired/decayed.
 */
export function sqliteRecallByTime(opts: {
  from: number; to: number; scope?: string; userId?: string; topN?: number
}): Memory[] {
  const _db = ensureDb()
  if (!_db) return []
  const topN = opts.topN ?? 20
  const conditions: string[] = ["scope NOT IN ('expired','decayed')", 'ts >= ?', 'ts <= ?']
  const params: any[] = [opts.from, opts.to]
  if (opts.scope) { conditions.push('scope = ?'); params.push(opts.scope) }
  if (opts.userId) { conditions.push('userId = ?'); params.push(opts.userId) }
  params.push(topN)
  const rows = _db.prepare(
    `SELECT * FROM memories WHERE ${conditions.join(' AND ')} ORDER BY ts DESC LIMIT ?`
  ).all(...params) as any[]
  return rows.map(rowToMemory)
}

// ═══════════════════════════════════════════════════════════════════════════════
// STRUCTURED FACTS CRUD — replaces JSON filter with indexed SQL queries
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Add a structured fact to SQLite. Returns the row id.
 */
export function sqliteAddFact(fact: StructuredFact): number {
  const _db = ensureDb()
  if (!_db) return -1
  const result = _db.prepare(`
    INSERT INTO structured_facts (subject, predicate, object, confidence, source, ts, validUntil, memoryRef)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
  `).run(
    fact.subject, fact.predicate, fact.object,
    fact.confidence, fact.source, fact.ts,
    fact.validUntil ?? 0, fact.memoryRef || null,
  )
  return Number(result.lastInsertRowid)
}

/**
 * Query facts by subject/predicate/object. Uses idx_fact_subj_pred index.
 * Only returns valid (non-expired) facts.
 */
export function sqliteQueryFacts(opts: { subject?: string; predicate?: string; object?: string }): StructuredFact[] {
  const _db = ensureDb()
  if (!_db) return []
  const conditions: string[] = ['validUntil = 0']
  const params: any[] = []
  if (opts.subject) { conditions.push('subject = ?'); params.push(opts.subject) }
  if (opts.predicate) { conditions.push('predicate = ?'); params.push(opts.predicate) }
  if (opts.object) { conditions.push('object LIKE ?'); params.push(`%${opts.object}%`) }
  const rows = _db.prepare(
    `SELECT * FROM structured_facts WHERE ${conditions.join(' AND ')} ORDER BY ts DESC`
  ).all(...params) as any[]
  return rows.map(r => ({
    subject: r.subject, predicate: r.predicate, object: r.object,
    confidence: r.confidence, source: r.source, ts: r.ts,
    validUntil: r.validUntil, memoryRef: r.memoryRef || undefined,
  }))
}

/**
 * Invalidate conflicting facts (same subject+predicate, different object).
 */
export function sqliteInvalidateFacts(subject: string, predicate: string, exceptObject: string): number {
  const _db = ensureDb()
  if (!_db) return 0
  const result = _db.prepare(
    `UPDATE structured_facts SET validUntil = ? WHERE subject = ? AND predicate = ? AND object != ? AND validUntil = 0`
  ).run(Date.now(), subject, predicate, exceptObject)
  return result.changes
}

/**
 * Get all valid facts count.
 */
export function sqliteFactCount(): number {
  const _db = ensureDb()
  if (!_db) return 0
  return (_db.prepare('SELECT COUNT(*) as c FROM structured_facts WHERE validUntil = 0').get() as any)?.c || 0
}

/**
 * Get all valid facts for a subject (for summary generation).
 */
export function sqliteGetFactsBySubject(subject: string): StructuredFact[] {
  const _db = ensureDb()
  if (!_db) return []
  const rows = _db.prepare(
    'SELECT * FROM structured_facts WHERE subject = ? AND validUntil = 0 ORDER BY ts DESC'
  ).all(subject) as any[]
  return rows.map(r => ({
    subject: r.subject, predicate: r.predicate, object: r.object,
    confidence: r.confidence, source: r.source, ts: r.ts,
    validUntil: r.validUntil, memoryRef: r.memoryRef || undefined,
  }))
}

/**
 * Load ALL facts from SQLite (including expired ones with validUntil > 0).
 * Used by fact-store.ts initialization to replace JSON loading.
 */
export function sqliteLoadAllFacts(): StructuredFact[] {
  const _db = ensureDb()
  if (!_db) return []
  const rows = _db.prepare(
    'SELECT * FROM structured_facts ORDER BY ts DESC'
  ).all() as any[]
  return rows.map(r => ({
    subject: r.subject, predicate: r.predicate, object: r.object,
    confidence: r.confidence, source: r.source, ts: r.ts,
    validUntil: r.validUntil, memoryRef: r.memoryRef || undefined,
  }))
}

// ═══════════════════════════════════════════════════════════════════════════════
// CHAT HISTORY CRUD
// ═══════════════════════════════════════════════════════════════════════════════

export function sqliteAddChatTurn(user: string, assistant: string) {
  if (!db) return
  db.prepare('INSERT INTO chat_history (user_msg, assistant_msg, ts) VALUES (?, ?, ?)').run(
    user.slice(0, 1000),
    assistant.slice(0, 2000),
    Date.now(),
  )
}

export function sqliteGetRecentHistory(limit = 30): { user: string; assistant: string; ts: number }[] {
  if (!db) return []
  const rows = db.prepare('SELECT * FROM chat_history ORDER BY ts DESC LIMIT ?').all(limit) as any[]
  return rows.reverse().map(row => ({
    user: row.user_msg,
    assistant: row.assistant_msg,
    ts: row.ts,
  }))
}

export function sqliteTrimHistory(maxKeep = 100) {
  if (!db) return
  const count = (db.prepare('SELECT COUNT(*) as c FROM chat_history').get() as any)?.c || 0
  if (count <= maxKeep) return
  const cutoff = db.prepare('SELECT ts FROM chat_history ORDER BY ts DESC LIMIT 1 OFFSET ?').get(maxKeep) as any
  if (cutoff) {
    db.prepare('DELETE FROM chat_history WHERE ts < ?').run(cutoff.ts)
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// MAINTENANCE
// ═══════════════════════════════════════════════════════════════════════════════

export function sqliteCleanupExpired() {
  if (!db) return
  const cutoff = Date.now() - 30 * 86400000
  // Clean up expired memories and their vectors
  const expiredIds = db.prepare("SELECT id FROM memories WHERE scope = 'expired' AND ts < ?").all(cutoff) as any[]
  if (expiredIds.length > 0) {
    const ids = expiredIds.map((r: any) => r.id)
    const placeholders = ids.map(() => '?').join(',')
    if (hasVec) {
      try { db.prepare(`DELETE FROM mem_vec WHERE memory_id IN (${placeholders})`).run(...ids) } catch { /* ok */ }
    }
    db.prepare(`DELETE FROM memories WHERE id IN (${placeholders})`).run(...ids)
    console.log(`[cc-soul][sqlite] cleaned up ${ids.length} expired memories`)
  }
}

export function isSQLiteReady(): boolean {
  return sqliteReady
}

// ═══════════════════════════════════════════════════════════════════════════════
// HELPERS
// ═══════════════════════════════════════════════════════════════════════════════

function rowToMemory(row: any): Memory {
  // ts: cc-soul uses INTEGER ms; official uses created_at TEXT — handle both
  let ts = row.ts
  if (!ts && row.created_at) {
    try { ts = new Date(row.created_at).getTime() } catch { ts = Date.now() }
  }
  return {
    content: row.content,
    scope: row.scope,
    ts: ts || Date.now(),
    emotion: row.emotion || 'neutral',
    userId: row.userId || undefined,
    visibility: row.visibility || 'global',
    channelId: row.channelId || undefined,
    tags: row.tags ? (() => { try { return JSON.parse(row.tags) } catch { return [] } })() : [],
    confidence: row.confidence ?? 0.7,
    lastAccessed: row.lastAccessed || row.last_accessed ? new Date(row.last_accessed).getTime() : undefined,
    tier: row.tier || 'short_term',
    recallCount: row.recallCount ?? row.access_count ?? 0,
    lastRecalled: row.lastRecalled || undefined,
    validFrom: row.validFrom || undefined,
    validUntil: row.validUntil || undefined,
    prospectiveTags: row.prospectiveTags ? (() => { try { const p = JSON.parse(row.prospectiveTags); return p.length > 0 ? p : undefined } catch { return undefined } })() : undefined,
    _entityIds: row._entityIds ? (() => { try { const e = JSON.parse(row._entityIds); return e.length > 0 ? e : undefined } catch { return undefined } })() : undefined,
  }
}

/** Ensure db is initialized, return the connection. Retries once if previous attempt failed. */
let _dbFailed = false
function ensureDb(): any {
  _loadState()
  if (db) return db
  if (_dbFailed) return null
  if (!sqliteReady) {
    try { initSQLite() } catch { _dbFailed = true; /* init failed, db stays null */ }
    _loadState() // check if another context succeeded
    if (!db) _dbFailed = true
  }
  return db
}

export function getDb() { return ensureDb() }

// habits/goals/reminders CRUD removed — life features deleted

// ═══════════════════════════════════════════════════════════════════════════════
// DUE REMINDERS — time-based reminders queried by heartbeat
// ═══════════════════════════════════════════════════════════════════════════════

export function dbGetDueReminders(): { id: number; msg: string }[] {
  const _db = ensureDb(); if (!_db) return []
  const now = new Date().toISOString()
  const rows = _db.prepare(
    "SELECT id, content FROM reminders WHERE status = 'pending' AND repeat_type != 'context' AND remind_at <= ?"
  ).all(now) as any[]
  return rows.map(r => ({ id: r.id, msg: r.content || '' }))
}

export function dbMarkReminderFired(id: number): void {
  const _db = ensureDb(); if (!_db) return
  _db.prepare("UPDATE reminders SET status = 'fired' WHERE id = ?").run(id)
}

// ═══════════════════════════════════════════════════════════════════════════════
// CONTEXT REMINDERS — keyword-triggered reminders (repeat_type = 'context')
// ═══════════════════════════════════════════════════════════════════════════════

export function dbAddContextReminder(keyword: string, content: string, userId?: string): number {
  const _db = ensureDb(); if (!_db) return -1
  const now = new Date().toISOString()
  // remind_at stores the keyword, repeat_type = 'context'
  const result = _db.prepare(
    "INSERT INTO reminders (chat_id, content, remind_at, repeat_type, status, created_at) VALUES (?, ?, ?, 'context', 'pending', ?)"
  ).run(userId || '', content, keyword, now)
  return Number(result.lastInsertRowid)
}

export function dbGetContextReminders(userId?: string): { id: number; keyword: string; content: string; userId: string }[] {
  const _db = ensureDb(); if (!_db) return []
  const rows = _db.prepare("SELECT * FROM reminders WHERE status = 'pending' AND repeat_type = 'context'").all() as any[]
  return rows
    .filter(r => !userId || !r.chat_id || r.chat_id === userId)
    .map(r => ({
      id: r.id,
      keyword: r.remind_at || '',
      content: r.content || '',
      userId: r.chat_id || '',
    }))
}

// habits/goals/reminders JSON migration removed — life features deleted

// ═══════════════════════════════════════════════════════════════════════════════
// ENTITY GRAPH CRUD — uses official entities + relations tables
// ═══════════════════════════════════════════════════════════════════════════════

export function dbGetEntities(): Entity[] {
  if (!ensureDb()) return []
  const rows = db.prepare('SELECT * FROM entities ORDER BY mentions DESC').all() as any[]
  return rows.map(rowToEntity)
}

export function dbAddEntity(name: string, type: string, attrs: string[] = []): void {
  if (!ensureDb() || !name || name.length < 2) return
  const now = Date.now()
  const nowIso = new Date(now).toISOString()
  // Upsert: try INSERT first, on conflict update mentions
  const existing = db.prepare('SELECT name, mentions, attrs FROM entities WHERE name = ?').get(name) as any
  if (existing) {
    const oldAttrs: string[] = (() => { try { return JSON.parse(existing.attrs || '[]') } catch { return [] } })()
    for (const a of attrs) { if (!oldAttrs.includes(a)) oldAttrs.push(a) }
    db.prepare('UPDATE entities SET mentions = ?, attrs = ?, invalid_at = NULL WHERE name = ?')
      .run((existing.mentions || 0) + 1, JSON.stringify(oldAttrs), name)
  } else {
    db.prepare(`INSERT INTO entities (name, type, mentions, firstSeen, attrs, valid_at, invalid_at)
      VALUES (?, ?, 1, ?, ?, ?, NULL)`)
      .run(name, type, now, JSON.stringify(attrs), now)
  }
}

export function dbUpdateEntity(name: string, updates: Partial<Entity>): void {
  if (!ensureDb()) return
  const sets: string[] = []
  const values: any[] = []
  if (updates.type !== undefined) { sets.push('type = ?'); values.push(updates.type) }
  if (updates.mentions !== undefined) { sets.push('mentions = ?'); values.push(updates.mentions) }
  if (updates.attrs !== undefined) { sets.push('attrs = ?'); values.push(JSON.stringify(updates.attrs)) }
  if (updates.valid_at !== undefined) { sets.push('valid_at = ?'); values.push(updates.valid_at) }
  if (updates.invalid_at !== undefined) { sets.push('invalid_at = ?'); values.push(updates.invalid_at) }
  if (updates.firstSeen !== undefined) { sets.push('firstSeen = ?'); values.push(updates.firstSeen) }
  if (sets.length === 0) return
  values.push(name)
  db.prepare(`UPDATE entities SET ${sets.join(', ')} WHERE name = ?`).run(...values)
}

export function dbGetRelations(): Relation[] {
  if (!ensureDb()) return []
  const rows = db.prepare('SELECT * FROM relations ORDER BY ts DESC').all() as any[]
  return rows.map(rowToRelation)
}

export function dbAddRelation(source: string, target: string, type: string, weight = 1.0, confidence = 0.7): void {
  if (!ensureDb() || !source || !target) return
  const now = Date.now()
  const nowIso = new Date(now).toISOString()
  // Check for existing active relation
  const existing = db.prepare(
    'SELECT source FROM relations WHERE source = ? AND target = ? AND type = ? AND invalid_at IS NULL'
  ).get(source, target, type) as any
  if (existing) return
  db.prepare(`INSERT INTO relations (source, target, type, ts, valid_at, invalid_at, weight, confidence)
    VALUES (?, ?, ?, ?, ?, NULL, ?, ?)`)
    .run(source, target, type, now, now, weight, confidence)
}

export function dbInvalidateEntity(name: string): void {
  if (!ensureDb()) return
  const now = Date.now()
  db.prepare('UPDATE entities SET invalid_at = ? WHERE name = ? AND invalid_at IS NULL').run(now, name)
  db.prepare('UPDATE relations SET invalid_at = ? WHERE (source = ? OR target = ?) AND invalid_at IS NULL').run(now, name, name)
}

export function dbInvalidateStaleRelations(thresholdMs: number): number {
  if (!ensureDb()) return 0
  const now = Date.now()
  const cutoff = now - thresholdMs
  const result = db.prepare(
    'UPDATE relations SET invalid_at = ? WHERE invalid_at IS NULL AND COALESCE(valid_at, ts, 0) < ?'
  ).run(now, cutoff)
  return (result as any).changes || 0
}

export function dbTrimEntities(maxKeep = 800): void {
  if (!ensureDb()) return
  const count = (db.prepare('SELECT COUNT(*) as c FROM entities').get() as any)?.c || 0
  if (count <= maxKeep + 100) return
  // Smart eviction: score = mentions * recency * validity
  // Invalid entities evicted first, then lowest composite score
  db.prepare(`DELETE FROM entities WHERE name IN (
    SELECT name FROM entities ORDER BY
      CASE WHEN invalid_at IS NOT NULL THEN 0 ELSE 1 END ASC,
      (COALESCE(mentions, 0) + 1) * (1.0 / (1.0 + (? - COALESCE(valid_at, firstSeen, 0)) / 86400000.0 / 30.0)) ASC
    LIMIT ?
  )`).run(Date.now(), count - maxKeep)
}

export function dbTrimRelations(maxKeep = 800): void {
  if (!ensureDb()) return
  const count = (db.prepare('SELECT COUNT(*) as c FROM relations').get() as any)?.c || 0
  if (count <= 1000) return
  db.prepare(`DELETE FROM relations WHERE rowid IN (
    SELECT rowid FROM relations ORDER BY
      CASE WHEN invalid_at IS NOT NULL THEN 0 ELSE 1 END ASC,
      ts ASC
    LIMIT ?
  )`).run(count - maxKeep)
}

function rowToEntity(row: any): Entity {
  return {
    name: row.name,
    type: row.type || 'unknown',
    attrs: (() => { try { return JSON.parse(row.attrs || '[]') } catch { return [] } })(),
    firstSeen: row.firstSeen || (row.created_at ? new Date(row.created_at).getTime() : 0),
    mentions: row.mentions || 0,
    valid_at: row.valid_at || 0,
    invalid_at: row.invalid_at ?? null,
  }
}

function rowToRelation(row: any): Relation {
  return {
    source: row.source || row.src,
    target: row.target || row.dst,
    type: row.type || row.relation,
    ts: row.ts || (row.created_at ? new Date(row.created_at).getTime() : 0),
    valid_at: row.valid_at || 0,
    invalid_at: row.invalid_at ?? null,
    weight: row.weight ?? 1.0,
    confidence: row.confidence ?? 0.7,
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// P0-P3: NEW TABLE CRUD
// ═══════════════════════════════════════════════════════════════════════════════

// ── Decision Log (P0c) ──

export function dbLogDecision(action: string, key: string, reason: string): void {
  if (!db) return
  db.prepare('INSERT INTO decision_log (action, key, reason, ts) VALUES (?, ?, ?, ?)').run(action, key, reason, Date.now())
  // Ringbuffer: keep last 200
  try { db.exec('DELETE FROM decision_log WHERE id NOT IN (SELECT id FROM decision_log ORDER BY id DESC LIMIT 200)') } catch {}
}

export function dbGetDecisions(filter?: string, limit = 200): Array<{ action: string; key: string; reason: string; ts: number }> {
  if (!db) return []
  if (filter) {
    return db.prepare('SELECT action, key, reason, ts FROM decision_log WHERE action LIKE ? OR key LIKE ? OR reason LIKE ? ORDER BY ts DESC LIMIT ?')
      .all(`%${filter}%`, `%${filter}%`, `%${filter}%`, limit) as any[]
  }
  return db.prepare('SELECT action, key, reason, ts FROM decision_log ORDER BY ts DESC LIMIT ?').all(limit) as any[]
}

// ── Topic Nodes (P0b) ──

export function dbSaveTopicNode(node: any): void {
  if (!db) return
  const existing = db.prepare('SELECT id FROM topic_nodes WHERE topic = ? AND (userId = ? OR (userId IS NULL AND ? IS NULL))').get(node.topic, node.userId ?? null, node.userId ?? null)
  if (existing) {
    db.prepare(`UPDATE topic_nodes SET summary=?, sourceCount=?, lastUpdated=?, hitCount=?, missCount=?, lastHitTs=?, stale=?, confidence=? WHERE id=?`)
      .run(node.summary, node.sourceCount, node.lastUpdated, node.hitCount ?? 0, node.missCount ?? 0, node.lastHitTs ?? 0, node.stale ? 1 : 0, node.confidence ?? 0.5, (existing as any).id)
  } else {
    db.prepare(`INSERT INTO topic_nodes (topic, summary, sourceCount, lastUpdated, userId, hitCount, missCount, lastHitTs, stale, confidence) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`)
      .run(node.topic, node.summary, node.sourceCount, node.lastUpdated, node.userId ?? null, node.hitCount ?? 0, node.missCount ?? 0, node.lastHitTs ?? 0, node.stale ? 1 : 0, node.confidence ?? 0.5)
  }
}

export function dbLoadTopicNodes(): any[] {
  if (!db) return []
  return (db.prepare('SELECT * FROM topic_nodes ORDER BY lastUpdated DESC').all() as any[]).map(row => ({
    ...row, stale: !!row.stale, userId: row.userId ?? undefined,
  }))
}

// dbDeleteTopicNode removed — unused

// ── Mental Models (P1c) ──

export function dbSaveMentalModel(model: any): void {
  if (!db) return
  db.prepare(`INSERT OR REPLACE INTO mental_models (userId, model, topics, lastUpdated, version, section_identity, section_style, section_facts, section_dynamics, sectionUpdated_identity, sectionUpdated_style, sectionUpdated_facts, sectionUpdated_dynamics) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`)
    .run(
      model.userId,
      model.model,
      JSON.stringify(model.topics ?? []),
      model.lastUpdated,
      model.version ?? 1,
      model.sections?.identity ?? '',
      model.sections?.style ?? '',
      model.sections?.facts ?? '',
      model.sections?.dynamics ?? '',
      model.sectionUpdated?.identity ?? 0,
      model.sectionUpdated?.style ?? 0,
      model.sectionUpdated?.facts ?? 0,
      model.sectionUpdated?.dynamics ?? 0,
    )
}

export function dbLoadMentalModels(): Map<string, any> {
  if (!db) return new Map()
  const rows = db.prepare('SELECT * FROM mental_models').all() as any[]
  const map = new Map<string, any>()
  for (const row of rows) {
    map.set(row.userId, {
      userId: row.userId,
      model: row.model,
      topics: JSON.parse(row.topics || '[]'),
      lastUpdated: row.lastUpdated,
      version: row.version,
      sections: {
        identity: row.section_identity || '',
        style: row.section_style || '',
        facts: row.section_facts || '',
        dynamics: row.section_dynamics || '',
      },
      sectionUpdated: {
        identity: row.sectionUpdated_identity || 0,
        style: row.sectionUpdated_style || 0,
        facts: row.sectionUpdated_facts || 0,
        dynamics: row.sectionUpdated_dynamics || 0,
      },
    })
  }
  return map
}

// ── Distill State (replaces distill_state.json) ──

export function dbSaveDistillState(state: any): void {
  if (!db) return
  db.prepare('INSERT OR REPLACE INTO distill_state (key, value) VALUES (?, ?)').run('state', JSON.stringify(state))
}

export function dbLoadDistillState(fallback: any): any {
  if (!db) return fallback
  const row = db.prepare('SELECT value FROM distill_state WHERE key = ?').get('state') as any
  if (!row) return fallback
  try { return JSON.parse(row.value) } catch { return fallback }
}

// pending_distill queue removed — sync path used instead

// ── FSRS Training (replaces fsrs_training.json) ──

export function dbAddFSRSTraining(elapsedDays: number, stability: number, recalled: boolean): void {
  if (!db) return
  db.prepare('INSERT INTO fsrs_training (elapsedDays, stability, recalled, ts) VALUES (?, ?, ?, ?)').run(elapsedDays, stability, recalled ? 1 : 0, Date.now())
  // Keep last 500
  try { db.exec('DELETE FROM fsrs_training WHERE id NOT IN (SELECT id FROM fsrs_training ORDER BY id DESC LIMIT 500)') } catch {}
}

export function dbLoadFSRSTraining(): Array<{ elapsedDays: number; stability: number; recalled: boolean }> {
  if (!db) return []
  return (db.prepare('SELECT elapsedDays, stability, recalled FROM fsrs_training ORDER BY ts DESC LIMIT 500').all() as any[])
    .map(r => ({ ...r, recalled: !!r.recalled }))
}

// ── Decay Params (replaces decay_params.json) ──

export function dbSaveDecayParams(params: any): void {
  if (!db) return
  db.prepare('INSERT OR REPLACE INTO decay_params (key, value) VALUES (?, ?)').run('params', JSON.stringify(params))
}

export function dbLoadDecayParams(fallback: any): any {
  if (!db) return fallback
  const row = db.prepare('SELECT value FROM decay_params WHERE key = ?').get('params') as any
  if (!row) return fallback
  try { return JSON.parse(row.value) } catch { return fallback }
}

// ── Augment Feedback (replaces augment_feedback.json) ──

export function dbSaveAugmentFeedback(type: string, data: { useful: number; ignored: number; totalScore: number; count: number; recentScores: number[] }): void {
  if (!db) return
  db.prepare('INSERT OR REPLACE INTO augment_feedback (augmentType, useful, ignored, totalScore, count, recentScores) VALUES (?, ?, ?, ?, ?, ?)')
    .run(type, data.useful, data.ignored, data.totalScore, data.count, JSON.stringify(data.recentScores))
}

export function dbLoadAugmentFeedback(): Record<string, { useful: number; ignored: number; totalScore: number; count: number; recentScores: number[] }> {
  if (!db) return {}
  const rows = db.prepare('SELECT * FROM augment_feedback').all() as any[]
  const result: any = {}
  for (const r of rows) {
    result[r.augmentType] = {
      useful: r.useful, ignored: r.ignored,
      totalScore: r.totalScore, count: r.count,
      recentScores: JSON.parse(r.recentScores || '[]'),
    }
  }
  return result
}
