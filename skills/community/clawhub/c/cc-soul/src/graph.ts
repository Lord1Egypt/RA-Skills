import type { SoulModule } from './brain.ts'

/**
 * graph.ts — Entity Graph
 * Entity/relation storage and context query.
 * Storage: SQLite (official entities/relations tables), with in-memory cache for fast query.
 * Note: CLI-powered entity extraction is now handled by runPostResponseAnalysis in cli.ts.
 */

import type { Entity, Relation } from './types.ts'
import { getParam } from './auto-tune.ts'
import { onCacheEvent } from './memory-utils.ts'

// Event-Driven Cache Coherence：注册缓存失效
onCacheEvent('memory_deleted', () => invalidateEntityMemoryIndex())
onCacheEvent('consolidation', () => { invalidateEntityMemoryIndex(); _pageRankDirty = true })
onCacheEvent('identity_changed', () => { invalidateEntityMemoryIndex(); _pageRankDirty = true })
onCacheEvent('correction_received', () => { _pageRankDirty = true })
import { DATA_DIR, loadJson, debouncedSave } from './persistence.ts'
import { resolve } from 'path'
import {
  dbGetEntities, dbAddEntity, dbUpdateEntity,
  dbGetRelations, dbAddRelation,
  dbInvalidateEntity, dbTrimEntities, dbTrimRelations,
  dbInvalidateStaleRelations,
  isSQLiteReady,
} from './sqlite-store.ts'

// Stale threshold now tunable via auto-tune
function getStaleThresholdMs() { return getParam('graph.stale_days') * 24 * 60 * 60 * 1000 }

// ═══════════════════════════════════════════════════════════════════════════════
// Mutable state (in-memory cache, synced from DB)
// ═══════════════════════════════════════════════════════════════════════════════

export const graphState = {
  entities: [] as Entity[],
  relations: [] as Relation[],
  ranks: new Map<string, number>(),
}

// ── Inverted index: entity name → Set of memory indices that mention it ──
// Populated by graphWalkRecallScored on first call, then updated incrementally.
let _entityToMemIdx: Map<string, Set<number>> | null = null
let _indexedMemCount = 0

/** Build or incrementally update the inverted index for entity→memory mapping */
function ensureEntityMemoryIndex(memories: { content: string; scope?: string }[]): Map<string, Set<number>> {
  const entityNames = graphState.entities
    .filter(e => e.invalid_at === null && e.name.length >= 2)
    .map(e => e.name)

  if (!_entityToMemIdx) {
    // Full rebuild
    _entityToMemIdx = new Map()
    for (const name of entityNames) _entityToMemIdx.set(name, new Set())
    for (let i = 0; i < memories.length; i++) {
      const mem = memories[i]
      if (mem.scope === 'expired' || mem.scope === 'decayed') continue
      for (const name of entityNames) {
        if (mem.content.includes(name)) {
          _entityToMemIdx.get(name)!.add(i)
        }
      }
    }
    _indexedMemCount = memories.length
  } else if (memories.length > _indexedMemCount) {
    // Incremental: only scan new memories
    for (let i = _indexedMemCount; i < memories.length; i++) {
      const mem = memories[i]
      if (mem.scope === 'expired' || mem.scope === 'decayed') continue
      for (const name of entityNames) {
        if (mem.content.includes(name)) {
          if (!_entityToMemIdx.has(name)) _entityToMemIdx.set(name, new Set())
          _entityToMemIdx.get(name)!.add(i)
        }
      }
    }
    // Ensure new entities have entries
    for (const name of entityNames) {
      if (!_entityToMemIdx.has(name)) {
        const s = new Set<number>()
        for (let i = 0; i < memories.length; i++) {
          const mem = memories[i]
          if (mem.scope !== 'expired' && mem.scope !== 'decayed' && mem.content.includes(name)) s.add(i)
        }
        _entityToMemIdx.set(name, s)
      }
    }
    _indexedMemCount = memories.length
  }
  return _entityToMemIdx
}

/** Invalidate inverted index (call when entities change) */
export function invalidateEntityMemoryIndex() { _entityToMemIdx = null; _indexedMemCount = 0 }

// ── PageRank dirty flag ──
let _pageRankDirty = true

// ═══════════════════════════════════════════════════════════════════════════════
// Persistence — read/write via SQLite
// ═══════════════════════════════════════════════════════════════════════════════

export function loadGraph() {
  if (!isSQLiteReady()) return
  const entities = dbGetEntities()
  const relations = dbGetRelations()
  graphState.entities.length = 0
  graphState.entities.push(...entities)
  graphState.relations.length = 0
  graphState.relations.push(...relations)
}

/** Reload in-memory cache from DB */
function syncFromDb() {
  if (!isSQLiteReady()) return
  graphState.entities.length = 0
  graphState.entities.push(...dbGetEntities())
  graphState.relations.length = 0
  graphState.relations.push(...dbGetRelations())
}

// ═══════════════════════════════════════════════════════════════════════════════
// CRUD
// ═══════════════════════════════════════════════════════════════════════════════

export function addEntity(name: string, type: string, attrs: string[] = []) {
  if (!name || name.length < 2) return
  dbAddEntity(name, type, attrs)
  // Trim if needed
  dbTrimEntities(800)
  // Sync cache
  syncFromDb()
  _pageRankDirty = true
  invalidateEntityMemoryIndex()
}

export function addRelation(source: string, target: string, type: string) {
  if (!source || !target) return
  dbAddRelation(source, target, type)
  dbTrimRelations(800)
  syncFromDb()
  _pageRankDirty = true
}

// ── Batch add from merged post-response analysis ──
export function addEntitiesFromAnalysis(entities: { name: string; type: string; relation?: string }[]) {
  for (const e of entities) {
    if (e.name && e.name.length >= 2) {
      dbAddEntity(e.name, e.type)
      if (e.relation) dbAddRelation(e.name, '用户', e.relation.slice(0, 30))
    }
  }
  dbTrimEntities(800)
  dbTrimRelations(800)
  syncFromDb()
  _pageRankDirty = true
  invalidateEntityMemoryIndex()
}

// ═══════════════════════════════════════════════════════════════════════════════
// Invalidation
// ═══════════════════════════════════════════════════════════════════════════════

/** Mark a specific entity (and its relations) as invalid */
export function invalidateEntity(name: string) {
  dbInvalidateEntity(name)
  syncFromDb()
  _pageRankDirty = true
  invalidateEntityMemoryIndex()
}

/** Mark entities not mentioned in the last 90 days as stale (set invalid_at) */
export function invalidateStaleEntities(): number {
  const now = Date.now()
  let count = 0
  for (const entity of graphState.entities) {
    if (entity.invalid_at !== null) continue
    const lastActivity = Math.max(entity.valid_at || 0, entity.firstSeen || 0)
    if (now - lastActivity > getStaleThresholdMs() && entity.mentions <= 1) {
      dbUpdateEntity(entity.name, { invalid_at: now })
      count++
    }
  }
  if (count > 0) syncFromDb()
  return count
}

/** Mark relations not activated in the last 90 days as stale (set invalid_at) */
export function invalidateStaleRelations(): number {
  const now = Date.now()
  const thresholdMs = getStaleThresholdMs()
  let count = 0
  for (const r of graphState.relations) {
    if (r.invalid_at !== null) continue
    const lastActivity = Math.max(r.valid_at || 0, r.ts || 0)
    if (now - lastActivity > thresholdMs) {
      r.invalid_at = now
      count++
    }
  }
  if (count > 0) {
    // Persist via bulk DB update
    if (isSQLiteReady()) {
      dbInvalidateStaleRelations(thresholdMs)
    }
    _pageRankDirty = true
  }
  return count
}

// ═══════════════════════════════════════════════════════════════════════════════
// Query
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Find entities mentioned in message text (exact name match).
 */
export function findMentionedEntities(msg: string): string[] {
  const mentioned = graphState.entities
    .filter(e => e.invalid_at === null && e.name.length >= 3 &&
      new RegExp('(?:^|[^a-zA-Z\\u4e00-\\u9fff])' + e.name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '(?:[^a-zA-Z\\u4e00-\\u9fff]|$)', 'i').test(msg))
    .sort((a, b) => b.mentions - a.mentions)
    .slice(0, 5)

  // ── G4: 英文专有名词检测（图谱为空时也能发现新实体）──
  const _COMMON_CAPS = new Set(['The','This','That','What','When','Where','How','Who','Which','Why','Yes','No','And','But','For','Not','Are','Was','Were','Has','Have','Had','Does','Did','Will','Can','May','She','Her','His','They','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday','January','February','March','April','May','June','July','August','September','October','November','December'])
  const enNames = msg.match(/\b([A-Z][a-z]{2,})\b/g) || []
  const mentionedNames = new Set(mentioned.map(e => e.name.toLowerCase()))
  for (const name of enNames) {
    if (!_COMMON_CAPS.has(name) && !mentionedNames.has(name.toLowerCase())) {
      const existing = graphState.entities.find(e => e.name.toLowerCase() === name.toLowerCase())
      if (existing) {
        existing.mentions++
        mentioned.push(existing)
      } else {
        const newEntity = { name, type: 'person' as const, mentions: 1, activation: 0.3, created_at: Date.now(), lastMentionedAt: Date.now(), lastActivatedAt: Date.now(), invalid_at: null as number | null, attrs: {} as Record<string, string> }
        graphState.entities.push(newEntity as any)
        mentioned.push(newEntity as any)
      }
      mentionedNames.add(name.toLowerCase())
    }
  }

  // ── Spreading activation: boost mentioned entities + propagate to neighbors ──
  for (const e of mentioned) {
    e.activation = Math.min(1.0, (e.activation ?? 0) + 0.3)
    e.lastActivatedAt = Date.now()
    // Propagate to 1-hop neighbors with decay
    for (const r of graphState.relations) {
      if (r.invalid_at !== null) continue
      const neighbor = r.source === e.name ? r.target : r.target === e.name ? r.source : null
      if (!neighbor) continue
      const ne = graphState.entities.find(n => n.name === neighbor && n.invalid_at === null)
      if (ne) {
        ne.activation = Math.min(1.0, (ne.activation ?? 0) + 0.1)
        ne.lastActivatedAt = Date.now()
      }
    }
  }

  return mentioned.map(e => e.name)
}

/** Decay all entity activations. Called from heartbeat. */
export function decayActivations(factor = 0.92) {
  for (const e of graphState.entities) {
    if (e.activation && e.activation > 0.01) {
      e.activation *= factor
      if (e.activation < 0.01) e.activation = 0
    }
  }
}

// ── Relation type weights for BFS traversal ──
const RELATION_WEIGHTS: Record<string, number> = {
  caused_by: 1.5, depends_on: 1.3, contradicts: 0.5,
  uses: 1.0, works_at: 1.0, knows: 0.8, part_of: 0.9,
  related_to: 0.7, follows: 0.6,
  prefers_over: 1.1, triggers: 1.2, learned_from: 1.3,
}

/** Temporal gravity: recent relations weigh more, 90-day half-life, min 0.3 */
function temporalGravity(relation: any, now: number): number {
  const age = now - (relation.valid_at || relation.ts || 0)
  const ageDays = age / 86400000
  return Math.max(0.3, Math.exp(-ageDays / 90))
}

/**
 * From mentioned entities, traverse relations 1-2 hops to find related entity names.
 * Weighted by relation type — higher-weight relations are explored first.
 */
export function getRelatedEntities(mentionedEntities: string[], maxHops = 2, maxResults = 10): string[] {
  const now = Date.now()
  const visited = new Set<string>(mentionedEntities)
  let frontier = [...mentionedEntities]

  for (let hop = 0; hop < maxHops; hop++) {
    const candidates: { name: string; weight: number }[] = []
    for (const entity of frontier) {
      for (const r of graphState.relations) {
        if (r.invalid_at !== null) continue
        const neighbor = r.source === entity ? r.target : r.target === entity ? r.source : null
        if (!neighbor || visited.has(neighbor)) continue
        const relWeight = (r.weight ?? 1.0) * (RELATION_WEIGHTS[r.type] ?? 0.8) * temporalGravity(r, now)
        candidates.push({ name: neighbor, weight: relWeight })
      }
    }
    // Sort by weight descending — explore high-value relations first
    candidates.sort((a, b) => b.weight - a.weight)
    const nextFrontier: string[] = []
    for (const c of candidates) {
      if (visited.has(c.name)) continue
      visited.add(c.name)
      nextFrontier.push(c.name)
      if (visited.size >= maxResults + mentionedEntities.length) break
    }
    frontier = nextFrontier
    if (visited.size >= maxResults + mentionedEntities.length) break
  }

  for (const m of mentionedEntities) visited.delete(m)
  return [...visited].slice(0, maxResults)
}

/**
 * Graph Walk Recall — BFS from startEntity, collect related entities up to maxDepth,
 * then return memory contents that mention any of the walked entities.
 * Accepts memories externally to avoid circular dependency with memory.ts.
 */
export function graphWalkRecall(
  startEntity: string,
  memories: { content: string; scope?: string }[],
  maxDepth = 2,
  maxNodes = 10,
): string[] {
  // BFS to collect entity names
  const visited = new Set<string>([startEntity])
  let frontier = [startEntity]
  for (let depth = 0; depth < maxDepth && frontier.length > 0; depth++) {
    const next: string[] = []
    for (const entity of frontier) {
      for (const r of graphState.relations) {
        if (r.invalid_at !== null) continue
        const neighbor = r.source === entity ? r.target : r.target === entity ? r.source : null
        if (neighbor && !visited.has(neighbor)) {
          visited.add(neighbor)
          next.push(neighbor)
          if (visited.size >= maxNodes + 1) break
        }
      }
      if (visited.size >= maxNodes + 1) break
    }
    frontier = next
  }
  visited.delete(startEntity) // exclude the start entity itself
  if (visited.size === 0) return []

  // Find memories mentioning walked entities
  const results: string[] = []
  const walkedNames = [...visited]
  for (const mem of memories) {
    if (mem.scope === 'expired' || mem.scope === 'decayed') continue
    for (const name of walkedNames) {
      if (mem.content.includes(name)) {
        results.push(mem.content)
        break
      }
    }
    if (results.length >= maxNodes) break
  }
  return results
}

/**
 * Enhanced Graph Walk — BFS with weighted scoring.
 * Returns memory contents ranked by: hop distance (closer=better),
 * relation freshness (newer=better), entity mentions (more=better).
 */
// ═══════════════════════════════════════════════════════════════════════════════
// Personalized PageRank — query-biased ranking instead of global PageRank
// Seeds teleport back to query-relevant entities, so nearby nodes get higher rank.
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Personalized PageRank with seed entities as teleport targets.
 * α = teleport probability (back to seeds), 1-α = walk along edges.
 */
export function personalizedPageRank(seeds: string[], alpha = 0.15, maxIter = 20): Map<string, number> {
  if (seeds.length === 0) return new Map()

  const activeEntities = new Set(
    graphState.entities.filter(e => e.invalid_at === null).map(e => e.name)
  )
  // Only use seeds that exist in the graph
  const validSeeds = seeds.filter(s => activeEntities.has(s))
  if (validSeeds.length === 0) return new Map()

  const ranks = new Map<string, number>()
  // Initialize: seeds get equal rank, others get 0
  for (const s of validSeeds) ranks.set(s, 1 / validSeeds.length)

  // Build adjacency: outDegree per node
  const outEdges = new Map<string, { target: string; weight: number }[]>()
  const now = Date.now()
  for (const name of activeEntities) outEdges.set(name, [])
  for (const r of graphState.relations) {
    if (r.invalid_at !== null) continue
    if (!activeEntities.has(r.source) || !activeEntities.has(r.target)) continue
    const relTypeWeight = RELATION_WEIGHTS[r.type] ?? 0.8
    const w = (r.weight ?? 1.0) * (r.confidence ?? 0.7) * relTypeWeight * temporalGravity(r, now)
    outEdges.get(r.source)!.push({ target: r.target, weight: w })
  }

  for (let iter = 0; iter < maxIter; iter++) {
    const newRanks = new Map<string, number>()
    // Teleport component: α probability → return to seed nodes
    for (const s of validSeeds) newRanks.set(s, alpha / validSeeds.length)

    // Walk component: (1-α) probability → propagate along edges
    for (const [node, rank] of ranks) {
      const edges = outEdges.get(node)
      if (!edges || edges.length === 0) continue
      const totalWeight = edges.reduce((s, e) => s + e.weight, 0)
      if (totalWeight <= 0) continue
      for (const e of edges) {
        const share = (1 - alpha) * rank * (e.weight / totalWeight)
        newRanks.set(e.target, (newRanks.get(e.target) || 0) + share)
      }
    }

    // Copy new ranks
    ranks.clear()
    for (const [k, v] of newRanks) ranks.set(k, v)
  }

  return ranks
}

// ═══════════════════════════════════════════════════════════════════════════════
// Spreading Activation — replaces PPR as default graph scoring in graphWalkRecallScored
// Iteratively propagates activation from seed entities along weighted edges.
// ═══════════════════════════════════════════════════════════════════════════════

export function spreadingActivation(
  seeds: string[],
  graphStateRef: { relations: Relation[] },
  maxIter = 3,
  decayFactor = 0.5
): Map<string, number> {
  const activation = new Map<string, number>()
  // 初始激活
  for (const s of seeds) activation.set(s, 1.0)

  for (let iter = 0; iter < maxIter; iter++) {
    const newActivation = new Map<string, number>()
    for (const [node, act] of activation) {
      if (act < 0.01) continue  // prune negligible activations
      // 沿出边传播
      const edges = graphStateRef.relations.filter(r =>
        (r.source === node || r.target === node) && !r.invalid_at
      )
      for (const e of edges) {
        const neighbor = e.source === node ? e.target : e.source
        const edgeWeight = (e.weight || 1) * (RELATION_WEIGHTS[e.type] || 0.7)
        const spread = act * decayFactor * edgeWeight
        newActivation.set(neighbor, (newActivation.get(neighbor) || 0) + spread)
      }
    }
    // 合并到主激活图
    for (const [k, v] of newActivation) {
      activation.set(k, (activation.get(k) || 0) + v)
    }
  }
  return activation
}

export function graphWalkRecallScored(
  startEntities: string[],
  memories: { content: string; scope?: string }[],
  maxDepth = 2,
  maxResults = 8,
): { content: string; graphScore: number }[] {
  // ── Personalized PageRank 替代 BFS 平权遍历 ──
  // PPR 以 startEntities 为种子做有偏随机游走，天然偏向查询相关实体
  const pprRanks = personalizedPageRank(startEntities, 0.15, Math.min(maxDepth * 5, 20))

  // 融合 PPR 排名 + 2-hop 缓存中的引力
  const entityScores = new Map<string, number>()
  for (const start of startEntities) entityScores.set(start, 1.0)

  for (const [entity, pprScore] of pprRanks) {
    if (entityScores.has(entity)) continue
    // PPR 得分 + 引力加成（来自 contextualEntityRank 的 2-hop 缓存）
    const gravityBoost = _neighborCache.has(startEntities[0])
      && _neighborCache.get(startEntities[0])!.has(entity) ? 0.3 : 0
    entityScores.set(entity, pprScore + gravityBoost)
    if (entityScores.size >= maxResults * 3) break
  }

  // Remove start entities from results
  for (const s of startEntities) entityScores.delete(s)
  if (entityScores.size === 0) return []

  // Score memories using inverted index (O(walked_entities × avg_matches) instead of O(memories × entities))
  const idx = ensureEntityMemoryIndex(memories)
  const memScoreMap = new Map<number, number>()
  for (const [entityName, entityScore] of entityScores) {
    const memIndices = idx.get(entityName)
    if (!memIndices) continue
    for (const i of memIndices) {
      memScoreMap.set(i, (memScoreMap.get(i) || 0) + entityScore)
    }
  }

  const results: { content: string; graphScore: number }[] = []
  for (const [i, score] of memScoreMap) {
    if (i < memories.length) {
      results.push({ content: memories[i].content, graphScore: score })
    }
  }

  results.sort((a, b) => b.graphScore - a.graphScore)
  return results.slice(0, maxResults)
}

// ═══════════════════════════════════════════════════════════════════════════════
// #1 Knowledge Graph Enhancement
// ═══════════════════════════════════════════════════════════════════════════════

/** Summarize all relations and attributes for a given entity */
export function generateEntitySummary(entityName: string): string | null {
  const entity = graphState.entities.find(e => e.name === entityName && e.invalid_at === null)
  if (!entity) return null
  const rels = graphState.relations
    .filter(r => r.invalid_at === null && (r.source === entityName || r.target === entityName))
    .map(r => r.source === entityName ? `${r.type} → ${r.target}` : `${r.source} ${r.type} →`)
  const parts = [`[${entity.type}] ${entityName} (提及${entity.mentions}次)`]
  if (entity.attrs.length > 0) parts.push(`属性: ${entity.attrs.join(', ')}`)
  if (rels.length > 0) parts.push(`关系: ${rels.slice(0, 8).join('; ')}`)
  return parts.join(' | ')
}

export function queryEntityContext(msg: string): string[] {
  // Find mentioned entities for personalized PageRank seeding
  const mentionedNames: string[] = []
  const results: { text: string; rank: number }[] = []
  for (const entity of graphState.entities) {
    if (entity.invalid_at !== null) continue
    if (msg.includes(entity.name)) mentionedNames.push(entity.name)
  }

  // Use Spreading Activation with mentioned entities as seeds (query-biased)
  const pprRanks = mentionedNames.length > 0
    ? spreadingActivation(mentionedNames, graphState, 3, 0.5)
    : graphState.ranks  // fallback to global PageRank if no entities mentioned

  for (const entity of graphState.entities) {
    if (entity.invalid_at !== null) continue
    if (!msg.includes(entity.name)) continue
    const rels = graphState.relations.filter(r =>
      r.invalid_at === null && (r.source === entity.name || r.target === entity.name),
    )
    const rank = pprRanks.get(entity.name) || 0
    if (rels.length > 0) {
      const relStr = rels.map(r => `${r.source} ${r.type} ${r.target}`).join(', ')
      results.push({ text: `[${entity.type}] ${entity.name}: ${relStr}`, rank })
    } else if (entity.attrs.length > 0) {
      results.push({ text: `[${entity.type}] ${entity.name}: ${entity.attrs.join(', ')}`, rank })
    }
  }
  // Sort by personalized PageRank descending
  results.sort((a, b) => b.rank - a.rank)
  return results.slice(0, 3).map(r => r.text)
}

// ═══════════════════════════════════════════════════════════════════════════════
// #5 PageRank — importance ranking for knowledge graph nodes
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Simplified PageRank with mention-based boost.
 * Called from heartbeat to periodically recompute node importance.
 * Skips recomputation if graph hasn't changed since last run (dirty flag).
 */
/**
 * P5d: contextualEntityRank — 替换 PageRank
 *
 * 以当前查询实体为中心，计算 2-hop 邻居的引力。
 * 同一实体在不同对话中重要性不同（语境感知）。
 *
 * 同时兼容 heartbeat 调用（无查询时计算全局质量 M(e)）。
 */

// 2-hop 邻居缓存（heartbeat 时预计算）
const _neighborCache = new Map<string, Set<string>>()

/**
 * computeEntityRanks — 计算每个实体的质量 M(e) 和 2-hop 邻居缓存
 *
 * 不是标准 PageRank（不做幂迭代传播）。对几百实体的小图，
 * 直接用 M(e) = mentions × recencyFactor × emotionalCharge 比迭代更有效。
 *
 * 保留旧函数名 computePageRank 作为别名（handler-heartbeat.ts 在调用）。
 */
export function computeEntityRanks(): void {
  computePageRank()
}
export function computePageRank(iterations = 3, dampingFactor = 0.85): void {
  if (!_pageRankDirty && graphState.ranks.size > 0) return
  const activeEntities = graphState.entities.filter(e => e.invalid_at === null)
  const N = activeEntities.length
  if (N === 0) { graphState.ranks.clear(); return }

  const now = Date.now()
  const names = new Set(activeEntities.map(e => e.name))

  // ── Step 1: 计算每个实体的质量 M(e) = mentions × recencyFactor × emotionalCharge ──
  const ranks = new Map<string, number>()
  for (const entity of activeEntities) {
    const refTs = entity.lastActivatedAt || entity.firstSeen || entity.valid_at || now
    const ageDays = Math.max(0, (now - refTs) / 86400000)
    const recencyFactor = Math.exp(-ageDays / 30)  // 30天半衰期
    const emotionalCharge = 1 + (entity.activation ?? 0) * 0.5
    const M = Math.max(0.01, entity.mentions * recencyFactor * emotionalCharge)
    ranks.set(entity.name, M)
  }

  // ── Step 2: 预计算 2-hop 邻居表（缓存，供 rankEntitiesByContext 使用）──
  _neighborCache.clear()
  const adjacency = new Map<string, Set<string>>()
  for (const name of names) adjacency.set(name, new Set())

  for (const r of graphState.relations) {
    if (r.invalid_at !== null) continue
    if (!names.has(r.source) || !names.has(r.target)) continue
    adjacency.get(r.source)!.add(r.target)
    adjacency.get(r.target)!.add(r.source)  // 无向处理
  }

  for (const name of names) {
    const hop1 = adjacency.get(name) || new Set()
    const hop2 = new Set<string>(hop1)
    for (const n1 of hop1) {
      const n1Neighbors = adjacency.get(n1) || new Set()
      for (const n2 of n1Neighbors) {
        if (n2 !== name) hop2.add(n2)
      }
    }
    _neighborCache.set(name, hop2)
  }

  graphState.ranks = ranks
  _pageRankDirty = false
  console.log(`[cc-soul][graph] contextualEntityRank: ${N} entities, ${_neighborCache.size} neighbor caches`)
}

// ═══════════════════════════════════════════════════════════════════════════════
// Social Graph — 关系图谱：追踪用户提到的人物及情绪关联
// (merged from social-graph.ts)
// ═══════════════════════════════════════════════════════════════════════════════

// [DELETED] 独立的 socialGraph 数组 — 社交信息已融入知识图谱（Entity type='person'）

const ROLE_PATTERNS = /老板|领导|boss|同事|colleague|朋友|女朋友|男朋友|老婆|老公|爸|妈|哥|姐|弟|妹|老师|客户/g

export function detectMentionedPeople(msg: string): string[] {
  const roles = msg.match(ROLE_PATTERNS) || []
  // Also detect names like 小李, 小王, etc
  const names = msg.match(/[小大老][A-Z\u4e00-\u9fff]/g) || []
  return [...new Set([...roles, ...names])]
}

/**
 * 社交图谱融入知识图谱（原创改造）
 * 人物 = Entity(type='person')，社交关系 = Relation
 * 不再维护独立的 socialGraph 数组
 */
export function updateSocialGraph(msg: string, mood: number) {
  const people = detectMentionedPeople(msg)
  for (const name of people) {
    // 人物作为 Entity 存入知识图谱
    let entity = graphState.entities.find(e => e.name === name && e.type === 'person')
    if (!entity) {
      entity = {
        name, type: 'person', attrs: [],
        firstSeen: Date.now(), mentions: 0,
        valid_at: Date.now(), invalid_at: null,
      }
      graphState.entities.push(entity)
      _pageRankDirty = true
    }
    entity.mentions++
    entity.lastActivatedAt = Date.now()
    entity.activation = Math.min(1, (entity.activation ?? 0) + 0.3)

    // 动态人物关系推断（不靠称呼列表，靠语境共现）
    try {
      const { inferRelationship } = require('./dynamic-extractor.ts')
      const rel = inferRelationship(name)
      if (rel !== 'unknown' && !entity.attrs.includes(`role:${rel}`)) {
        entity.attrs = entity.attrs.filter((a: string) => !a.startsWith('role:'))
        entity.attrs.push(`role:${rel}`)
      }
    } catch {}

    // 情绪归因到具体关系边，而非粗暴加到人物上
    // "老板夸我" → Relation { source: "老板", target: "用户", type: "praised", mood: 0.5 }
    const moodLabel = mood > 0.2 ? 'positive_interaction' : mood < -0.2 ? 'negative_interaction' : 'neutral_interaction'
    const topic = msg.replace(new RegExp(name, 'g'), '').match(/[\u4e00-\u9fff]{2,4}/)?.[0]

    // 存情绪关系到 attrs（每次都 push，不去重——getSocialContext 靠计数判断情绪倾向）
    entity.attrs.push(moodLabel)
    if (entity.attrs.length > 20) entity.attrs = entity.attrs.slice(-20)

    // 检测通讯风格
    const formalRe = /请问|您|汇报|报告|会议|安排|deadline|项目|审批|review|领导|老板|boss|客户/i
    const casualRe = /哈哈|lol|hhh|卧槽|牛逼|nb|6{2,}|yyds|绝了|离谱|兄弟|哥们|姐妹|朋友/i
    if (formalRe.test(msg) && !entity.attrs.includes('tone:formal')) entity.attrs.push('tone:formal')
    if (casualRe.test(msg) && !entity.attrs.includes('tone:casual')) entity.attrs.push('tone:casual')

    // 称呼合并：如果消息中同时出现两个人物名，可能是别名
    // "我女朋友小雨" → addRelation("女朋友", "小雨", "alias_of")
    if (people.length >= 2) {
      for (const other of people) {
        if (other === name) continue
        const hasAlias = graphState.relations.some(r =>
          r.type === 'alias_of' && ((r.source === name && r.target === other) || (r.source === other && r.target === name))
        )
        if (!hasAlias && msg.includes(name) && msg.includes(other) && Math.abs(msg.indexOf(name) - msg.indexOf(other)) < 10) {
          addRelation(name, other, 'alias_of')
        }
      }
    }

    // 话题关联
    if (topic) {
      const hasTopicRel = graphState.relations.some(r =>
        r.source === name && r.target === topic && r.type === 'mentioned_with'
      )
      if (!hasTopicRel) addRelation(name, topic, 'mentioned_with')
    }
  }
  // 持久化到 SQLite（实体已在内存 graphState 中更新）
  if (people.length > 0) {
    for (const name of people) {
      const entity = graphState.entities.find(e => e.name === name && e.type === 'person')
      if (entity) try { dbUpdateEntity(entity.name, { mentions: entity.mentions, attrs: entity.attrs }) } catch {}
    }
    _pageRankDirty = true
  }
}

export function getSocialContext(msg: string): string | null {
  const people = detectMentionedPeople(msg)
  if (people.length === 0) return null
  const hints: string[] = []

  for (const name of people) {
    // 从知识图谱查询人物实体
    const entity = graphState.entities.find(e => e.name === name && e.type === 'person')
    if (!entity || entity.mentions < 2) continue

    // 情绪统计从 attrs 中提取
    const posCount = entity.attrs.filter(a => a === 'positive_interaction').length
    const negCount = entity.attrs.filter(a => a === 'negative_interaction').length
    const emotionLabel = posCount + negCount < 2 ? '数据不足'
      : negCount > posCount * 2 ? '明显焦虑/压力'
      : posCount > negCount * 2 ? '积极/开心'
      : '混合情绪'

    const tone = entity.attrs.includes('tone:formal') ? '正式'
      : entity.attrs.includes('tone:casual') ? '轻松' : '混合'

    // 2-hop 关联：通过知识图谱发现关联实体
    const related = _neighborCache.get(name)
    const relatedHint = related && related.size > 0
      ? `，关联：${[...related].slice(0, 3).join('/')}`
      : ''

    hints.push(`${name}：提到${entity.mentions}次，情绪${emotionLabel}，语境${tone}${relatedHint}`)
  }

  if (hints.length === 0) return null
  return `[关系图谱] ${hints.join('；')}`
}

/** Reset graph state (for testing) */
export function _resetSocialGraph() {
  graphState.entities = graphState.entities.filter(e => e.type !== 'person')
}

// ═══════════════════════════════════════════════════════════════════════════════
// Causal Chain — 沿 caused_by 方向做有向 BFS，返回因果链上的实体
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Trace causal chain from given entities along caused_by/triggers/depends_on edges.
 * Returns chain of entity names with direction arrows for augment display.
 */
/**
 * 双向因果图追踪（原创改造）
 *
 * 向上追因：为什么发生？(caused_by, depends_on)  → target→source 方向
 * 向下追果：导致了什么？(triggers, leads_to)      → source→target 方向
 *
 * 每条因果边有隐式强度（关系 confidence × weight）
 */
const CAUSE_TYPES = new Set(['caused_by', 'depends_on', 'learned_from'])
const EFFECT_TYPES = new Set(['triggers', 'leads_to'])

function traceDirection(
  start: string,
  relTypes: Set<string>,
  direction: 'up' | 'down',
  maxHops: number,
): Array<{ entity: string; type: string; strength: number }> {
  const visited = new Set<string>([start])
  const results: Array<{ entity: string; type: string; strength: number }> = []
  let frontier = [start]

  for (let hop = 0; hop < maxHops && frontier.length > 0; hop++) {
    const next: string[] = []
    for (const current of frontier) {
      for (const r of graphState.relations) {
        if (r.invalid_at !== null) continue
        if (!relTypes.has(r.type)) continue

        // 方向：向上追因 → 从 target 找 source；向下追果 → 从 source 找 target
        let neighbor: string | null = null
        if (direction === 'up' && r.target === current && !visited.has(r.source)) {
          neighbor = r.source
        } else if (direction === 'down' && r.source === current && !visited.has(r.target)) {
          neighbor = r.target
        }
        if (!neighbor) continue

        const strength = (r.confidence ?? 0.7) * (r.weight ?? 1.0) / (hop + 1)  // hop 衰减
        visited.add(neighbor)
        results.push({ entity: neighbor, type: r.type, strength })
        next.push(neighbor)
      }
    }
    frontier = next
  }

  return results.sort((a, b) => b.strength - a.strength)
}

export function traceCausalChain(startEntities: string[], maxHops = 3): string[] {
  const chains: string[] = []

  for (const start of startEntities.slice(0, 3)) {
    // 向上追因
    const causes = traceDirection(start, CAUSE_TYPES, 'up', maxHops)
    if (causes.length > 0) {
      const causeStr = causes.slice(0, 3).map(c => `${c.entity}(${c.type},s=${c.strength.toFixed(2)})`).join(' ← ')
      chains.push(`${start} 的原因：${causeStr}`)
    }

    // 向下追果
    const effects = traceDirection(start, EFFECT_TYPES, 'down', maxHops)
    if (effects.length > 0) {
      const effectStr = effects.slice(0, 3).map(e => `${e.entity}(${e.type},s=${e.strength.toFixed(2)})`).join(' → ')
      chains.push(`${start} 的影响：${effectStr}`)
    }
  }

  return chains
}

/**
 * 从记忆的 because 字段补充图谱中缺失的因果边
 * heartbeat 时调用
 */
export function enrichCausalFromMemories(): void {
  try {
    const { memoryState } = require('./memory.ts')
    const memories = memoryState?.memories
    if (!memories) return

    let added = 0
    for (const m of memories) {
      if (!m.because || m.scope === 'expired') continue
      const effectEntities = findMentionedEntities(m.content)
      const causeEntities = findMentionedEntities(m.because)
      if (effectEntities.length === 0 || causeEntities.length === 0) continue

      for (const cause of causeEntities) {
        for (const effect of effectEntities) {
          if (cause === effect) continue
          // 检查是否已有这条因果边
          const exists = graphState.relations.some(r =>
            r.source === effect && r.target === cause && r.type === 'caused_by' && r.invalid_at === null
          )
          if (!exists) {
            addRelation(effect, cause, 'caused_by')
            added++
          }
        }
      }
      if (added >= 10) break  // 每轮最多补充 10 条，防止一次性太多
    }
    if (added > 0) console.log(`[cc-soul][graph] enriched ${added} causal edges from memory.because`)
  } catch {}
}

export const graphModule: SoulModule = {
  id: 'graph',
  name: '知识图谱',
  priority: 50,
  init() { loadGraph() },
}
