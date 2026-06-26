/**
 * memory-lifecycle.ts — Periodic maintenance, consolidation, decay, and lifecycle operations
 * Extracted from memory.ts to reduce file size.
 */

import { resolve } from 'path'
import type { Memory } from './types.ts'
import { DATA_DIR, loadJson, debouncedSave, adaptiveCooldown } from './persistence.ts'
import { getParam } from './auto-tune.ts'
import { spawnCLI } from './cli.ts'
import {
  sqliteCleanupExpired,
  sqliteFindByContent, sqliteUpdateMemory, sqliteUpdateRawLine, getDb, sqliteCount,
} from './sqlite-store.ts'
import { findMentionedEntities, getRelatedEntities } from './graph.ts'
import {
  memoryState, scopeIndex, useSQLite,
  addMemory, addMemoryWithEmotion, saveMemories, syncToSQLite,
  rebuildScopeIndex, getLazyModule, compressMemory,
} from './memory.ts'
import { trigrams, trigramSimilarity, shuffleArray } from './memory-utils.ts'
import { recall, recallWithScores, invalidateIDF, rebuildRecallIndex, _memLookup } from './memory-recall.ts'
import { invalidateFieldIDF } from './activation-field.ts'

// ═══════════════════════════════════════════════════════════════════════════════
// Memory Consolidation (压缩合并)
// ═══════════════════════════════════════════════════════════════════════════════

let lastConsolidationTs = 0
const CONSOLIDATION_COOLDOWN_MS = (userId?: string) => adaptiveCooldown(getParam('lifecycle.consolidation_cooldown_hours') * 3600 * 1000, userId)
let consolidating = false

/**
 * Cluster memories by topic similarity using keyword overlap.
 * Only returns clusters of 3+ memories (worth consolidating).
 */
/**
 * TF-IDF vectorize a document and return term→weight map.
 * IDF is computed from the provided corpus.
 */
function tfidfVector(doc: string, idfMap: Map<string, number>): Map<string, number> {
  const words = (doc.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map(w => w.toLowerCase())
  const tf = new Map<string, number>()
  for (const w of words) tf.set(w, (tf.get(w) || 0) + 1)
  const vec = new Map<string, number>()
  for (const [term, count] of tf) {
    vec.set(term, count * (idfMap.get(term) ?? 1.0))
  }
  return vec
}

/** Cosine similarity between two TF-IDF vectors. */
function cosineSim(a: Map<string, number>, b: Map<string, number>): number {
  let dot = 0, normA = 0, normB = 0
  for (const [k, v] of a) { normA += v * v; if (b.has(k)) dot += v * b.get(k)! }
  for (const [, v] of b) normB += v * v
  if (normA === 0 || normB === 0) return 0
  return dot / (Math.sqrt(normA) * Math.sqrt(normB))
}

// ═══════════════════════════════════════════════════════════════════════════════
// SimHash — IDF-weighted locality-sensitive hashing (replaces MinHash)
// Estimates cosine distance instead of Jaccard; better for weighted TF-IDF vectors.
// ═══════════════════════════════════════════════════════════════════════════════

const SIMHASH_BITS = 64

/** FNV-1a 64-bit hash (BigInt) */
function fnv1a64(token: string): bigint {
  let h = 14695981039346656037n  // FNV offset basis
  for (let i = 0; i < token.length; i++) {
    h ^= BigInt(token.charCodeAt(i))
    h = (h * 1099511628211n) & 0xFFFFFFFFFFFFFFFFn  // FNV prime, mask to 64 bits
  }
  return h
}

/** SimHash: IDF-weighted fingerprint producing a 64-bit signature */
function simHash(tokens: string[], idf: Map<string, number>, bits = SIMHASH_BITS): bigint {
  const v = new Float64Array(bits)
  for (const token of tokens) {
    const weight = idf.get(token) ?? 0.01  // 未知词给最小权重（停用词 IDF≈0，不能 fallback 给 1.0）
    const hash = fnv1a64(token)
    for (let i = 0; i < bits; i++) {
      if ((hash >> BigInt(i)) & 1n) v[i] += weight
      else v[i] -= weight
    }
  }
  let sig = 0n
  // 用中位数而非 0 作为阈值——IDF 权重分布偏斜时，0 阈值导致高位全偏正
  const sorted = [...v].sort((a, b) => a - b)
  const median = sorted[Math.floor(sorted.length / 2)]
  for (let i = 0; i < bits; i++) {
    if (v[i] > median) sig |= (1n << BigInt(i))
  }
  return sig
}

/** Hamming distance between two SimHash signatures, normalized to [0, 1] */
function simHashDistance(a: bigint, b: bigint, bits = SIMHASH_BITS): number {
  let xor = a ^ b
  let count = 0
  while (xor > 0n) { count += Number(xor & 1n); xor >>= 1n }
  if (bits === 0) return 0
  return count / bits  // 0=identical, 1=completely different
}

/** Tokenize text into word-level shingles for SimHash */
// tokenize → 使用统一的 tokenize('bigram') from memory-utils.ts
import { tokenize as _tokenize } from './memory-utils.ts'
function tokenize(text: string): string[] { return _tokenize(text, 'bigram') }

function clusterByTopic(mems: Memory[]): Memory[][] {
  // Cap input to most recent 200
  const capped = mems.length > 200 ? mems.slice(-200) : mems
  if (capped.length < 3) return []

  // Step 1: Build IDF from corpus
  const df = new Map<string, number>()
  const N = capped.length
  for (const m of capped) {
    const words = new Set((m.content.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map(w => w.toLowerCase()))
    for (const w of words) df.set(w, (df.get(w) || 0) + 1)
  }
  const idfMap = new Map<string, number>()
  for (const [word, count] of df) idfMap.set(word, Math.log(N / (1 + count)))

  // Step 2: Tokenize and generate SimHash signatures (IDF-weighted)
  const tokenLists = capped.map(m => tokenize(m.content))
  const sigs = tokenLists.map(ts => ts.length > 0 ? simHash(ts, idfMap) : 0n)

  // Step 3: Find candidate pairs — SimHash distance < 0.35 (≈ cosine similarity > 0.3)
  // Use bucket-based grouping on upper 8 bits for O(n) amortized candidate generation
  const BUCKET_BITS = 8
  const buckets = new Map<number, number[]>()
  for (let i = 0; i < sigs.length; i++) {
    const bucketKey = Number((sigs[i] >> BigInt(SIMHASH_BITS - BUCKET_BITS)) & BigInt((1 << BUCKET_BITS) - 1))
    if (!buckets.has(bucketKey)) buckets.set(bucketKey, [])
    buckets.get(bucketKey)!.push(i)
  }

  const candidatePairs = new Set<string>()
  for (const [, indices] of buckets) {
    if (indices.length < 2 || indices.length > 50) continue
    for (let a = 0; a < indices.length; a++) {
      for (let b = a + 1; b < indices.length; b++) {
        const key = indices[a] < indices[b] ? `${indices[a]}:${indices[b]}` : `${indices[b]}:${indices[a]}`
        candidatePairs.add(key)
      }
    }
  }
  // Also check neighboring buckets (1-bit hamming distance on bucket key)
  for (const [bk, indices] of buckets) {
    for (let bit = 0; bit < BUCKET_BITS; bit++) {
      const neighbor = bk ^ (1 << bit)
      const nIndices = buckets.get(neighbor)
      if (!nIndices) continue
      for (const a of indices) {
        for (const b of nIndices) {
          if (a === b) continue
          const key = a < b ? `${a}:${b}` : `${b}:${a}`
          candidatePairs.add(key)
        }
      }
    }
  }

  // Step 4: Verify candidates with SimHash distance, then precise TF-IDF cosine
  const vecs = capped.map(m => tfidfVector(m.content, idfMap))

  // Union-Find for merging verified pairs
  const parent = Array.from({ length: capped.length }, (_, i) => i)
  function find(x: number): number { return parent[x] === x ? x : (parent[x] = find(parent[x])) }
  function unite(a: number, b: number) { parent[find(a)] = find(b) }

  for (const pair of candidatePairs) {
    const [ai, bi] = pair.split(':').map(Number)
    if (find(ai) === find(bi)) continue
    // Fast check: SimHash distance (cosine proxy)
    const dist = simHashDistance(sigs[ai], sigs[bi])
    if (dist > 0.4) continue  // too dissimilar
    // Precise verification: TF-IDF cosine
    if (cosineSim(vecs[ai], vecs[bi]) >= 0.25) unite(ai, bi)
  }

  // Collect clusters
  const clusterMap = new Map<number, Memory[]>()
  for (let i = 0; i < capped.length; i++) {
    const root = find(i)
    if (!clusterMap.has(root)) clusterMap.set(root, [])
    clusterMap.get(root)!.push(capped[i])
  }

  return [...clusterMap.values()].filter(c => c.length >= 3) // only consolidate clusters of 3+
}

export function consolidateMemories() {
  // Safety: force-release consolidating lock if stuck for >5 minutes
  if (consolidating && Date.now() - lastConsolidationTs > 5 * 60 * 1000) {
    console.error('[cc-soul][consolidation] force-releasing stuck lock (>5min)')
    consolidating = false
  }
  if (consolidating) return
  // Use SQLite count if available (memoryState.memories may be empty in lazy-load mode)
  const totalCount = useSQLite ? sqliteCount() : memoryState.memories.length
  if (totalCount < 500) return
  if (Date.now() - lastConsolidationTs < CONSOLIDATION_COOLDOWN_MS()) return
  consolidating = true
  lastConsolidationTs = Date.now()

  // Group memories by scope
  const groups = new Map<string, Memory[]>()
  for (const mem of memoryState.memories) {
    const key = mem.scope || 'unknown'
    if (!groups.has(key)) groups.set(key, [])
    groups.get(key)!.push(mem)
  }

  let pendingCLICalls = 0
  // Collect all removals and additions across callbacks, apply once when all complete
  const allContentToRemove = new Set<string>()
  const allSummariesToAdd: { content: string; visibility: Memory['visibility'] }[] = []

  // For scopes with >50 entries, consolidate oldest batch by topic clusters
  for (const [scope, mems] of groups) {
    if (mems.length < 50) continue
    if (scope === 'consolidated') continue // don't re-consolidate

    // Take oldest 20, cluster by topic, consolidate each cluster separately
    const oldest = mems.sort((a, b) => a.ts - b.ts).slice(0, 20)

    // ── Topic River: segment-based pre-clustering（同 segment 优先合并）──
    const segmentGroups = new Map<number, Memory[]>()
    const noSegment: Memory[] = []
    for (const m of oldest) {
      if (m._segmentId != null) {
        const g = segmentGroups.get(m._segmentId) || []
        g.push(m)
        segmentGroups.set(m._segmentId, g)
      } else {
        noSegment.push(m)
      }
    }
    const segmentClusters = [...segmentGroups.values()].filter(g => g.length >= 3)
    // Remaining memories (no segment or small segment groups) go through SimHash clustering
    const remaining = noSegment.concat([...segmentGroups.values()].filter(g => g.length < 3).flat())
    const simhashClusters = remaining.length >= 3 ? clusterByTopic(remaining) : []
    const clusters = [...segmentClusters, ...simhashClusters]

    if (clusters.length === 0) continue

    for (const cluster of clusters) {
      const contents = cluster.map(m => compressMemory(m)).join('\n')
      pendingCLICalls++

      // B1: try zeroLLMDistill first to avoid LLM call
      try {
        const { zeroLLMDistill } = require('./distill.ts')
        const zeroResult = zeroLLMDistill(cluster.map((m: any) => m.content))
        if (zeroResult && zeroResult.length > 10) {
          pendingCLICalls--
          const summaries = [zeroResult.slice(0, 200)]
          for (const o of cluster) allContentToRemove.add(`${o.content}\0${o.ts}`)
          for (const summary of summaries) {
            allSummariesToAdd.push({ content: compressMemory({ content: summary } as Memory), visibility: cluster[0]?.visibility || 'global' })
          }
          console.log(`[cc-soul][memory] consolidated ${cluster.length} ${scope} memories (zero-LLM)`)
          if (pendingCLICalls <= 0) {
            let maxEngagement = 0, maxRecallCount = 0
            for (const mem of memoryState.memories) {
              if (allContentToRemove.has(`${mem.content}\0${mem.ts}`)) {
                maxEngagement = Math.max(maxEngagement, mem.injectionEngagement ?? 0)
                maxRecallCount = Math.max(maxRecallCount, mem.recallCount ?? 0)
              }
            }
            memoryState.memories = memoryState.memories.filter(m => !allContentToRemove.has(`${m.content}\0${m.ts}`))
            for (const s of allSummariesToAdd) {
              addMemory(s.content, 'consolidated', undefined, s.visibility)
            }
            consolidating = false
          }
          continue
        }
      } catch {}

      spawnCLI(
        `以下是${scope}类型的${cluster.length}条同主题记忆，请合并为1-2条摘要（保留关键信息）：\n\n${contents.slice(0, 1500)}\n\n格式：每条摘要一行`,
        (output) => {
          try {
            pendingCLICalls--
            // #7: Verify memories haven't been modified during async wait
            if (memoryState.memories.length === 0) {
              if (pendingCLICalls <= 0) consolidating = false
              return
            }
            if (!output || output.length < 10) {
              if (pendingCLICalls <= 0) consolidating = false
              return
            }
            const summaries = output.split('\n').filter(l => l.trim().length > 5).slice(0, 3)

            // Collect removals and additions — don't splice yet
            for (const o of cluster) allContentToRemove.add(`${o.content}\0${o.ts}`)
            for (const summary of summaries) {
              allSummariesToAdd.push({
                content: compressMemory({ content: summary.trim() } as Memory),
                visibility: cluster[0]?.visibility || 'global',
              })
            }
            console.log(`[cc-soul][memory] consolidated ${cluster.length} ${scope} memories -> ${summaries.length} summaries`)

            // When ALL callbacks complete, apply removals and additions in one batch
            if (pendingCLICalls <= 0) {
              // 稳定性继承：在删除前计算源记忆中最大的 engagement/recallCount
              let maxEngagement = 0, maxRecallCount = 0
              for (const mem of memoryState.memories) {
                if (allContentToRemove.has(`${mem.content}\0${mem.ts}`)) {
                  maxEngagement = Math.max(maxEngagement, mem.injectionEngagement ?? 0)
                  maxRecallCount = Math.max(maxRecallCount, mem.recallCount ?? 0)
                }
              }
              // Reverse-splice all collected removals at once (keyed by content+ts to avoid same-content collisions)
              for (let i = memoryState.memories.length - 1; i >= 0; i--) {
                if (allContentToRemove.has(`${memoryState.memories[i].content}\0${memoryState.memories[i].ts}`)) {
                  memoryState.memories.splice(i, 1)
                }
              }
              // Add all consolidated summaries
              for (const entry of allSummariesToAdd) {
                memoryState.memories.push({
                  content: entry.content,
                  scope: 'consolidated',
                  ts: Date.now(),
                  visibility: entry.visibility,
                  confidence: 0.8,
                  recallCount: maxRecallCount,
                  injectionEngagement: maxEngagement,
                  lastAccessed: Date.now(),
                  tier: 'long_term',
                })
              }
              rebuildScopeIndex()
              rebuildRecallIndex(memoryState.memories)
              saveMemories()
              invalidateIDF()
              invalidateFieldIDF()
              // 巩固后缓存失效：通过事件总线通知所有缓存
              try { const { emitCacheEvent } = require('./memory-utils.ts'); emitCacheEvent('consolidation') } catch {}
              consolidating = false
            }
          } catch (e: any) {
            console.error(`[cc-soul][consolidation] callback error: ${e.message}`)
            pendingCLICalls = Math.max(0, pendingCLICalls)
            if (pendingCLICalls <= 0) consolidating = false
          }
        }
      )
    }
  }

  // If no CLI calls were made, release the lock immediately
  if (pendingCLICalls === 0) consolidating = false

  // Generate insights after consolidation (reuses 24h cooldown, no extra timer)
  generateInsights()
}

// ═══════════════════════════════════════════════════════════════════════════════
// Insight Generation — extract behavioral patterns from recent memories
// ═══════════════════════════════════════════════════════════════════════════════

const MAX_INSIGHTS = 20

/**
 * Scan memories from the last 7 days, ask AI to extract 1-3 behavioral
 * patterns / preference insights, and store them as scope='insight' memories.
 * Called automatically at the end of consolidateMemories (shares its 24h cooldown),
 * or manually via generateInsights().
 */
export function generateInsights() {
  const sevenDaysAgo = Date.now() - 7 * 86400000
  const recentMemories = memoryState.memories.filter(
    m => m.ts >= sevenDaysAgo && m.scope !== 'expired' && m.scope !== 'insight'
  )
  if (recentMemories.length < 5) return // not enough data

  // B3: rule-based insights first — skip LLM if we find patterns
  const ruleInsights: string[] = []
  // Scope distribution insight
  const scopeCounts = new Map<string, number>()
  for (const m of recentMemories) scopeCounts.set(m.scope, (scopeCounts.get(m.scope) || 0) + 1)
  const topScope = [...scopeCounts.entries()].sort((a, b) => b[1] - a[1])[0]
  if (topScope && topScope[1] >= 5) ruleInsights.push(`最近${topScope[1]}条记忆都是${topScope[0]}类型`)
  // Emotion trend
  const negCount = recentMemories.filter(m => (m as any).emotion === 'painful' || ((m as any).situationCtx?.mood ?? 0) < -0.3).length
  if (negCount >= 3) ruleInsights.push('最近情绪偏低的记忆增多')
  // Correction trend
  const corrCount = recentMemories.filter(m => m.scope === 'correction').length
  if (corrCount >= 3) ruleInsights.push(`某领域被纠正${corrCount}次，需要加强`)
  if (ruleInsights.length > 0) {
    for (const insight of ruleInsights) addMemory(insight, 'insight', undefined, 'private')
    console.log(`[cc-soul][insights] rule-based: ${ruleInsights.length} insights generated (zero-LLM)`)
    return
  }

  // Build a digest of recent memories (cap to avoid token explosion)
  const digest = recentMemories
    .sort((a, b) => b.ts - a.ts)
    .slice(0, 60)
    .map(m => `[${m.scope}] ${m.content.slice(0, 120)}`)
    .join('\n')

  spawnCLI(
    `分析以下用户近期记忆，总结1-3条行为模式或偏好洞察。每条一行，格式：[洞察] 内容\n\n${digest.slice(0, 2000)}`,
    (output) => {
      if (!output || output.length < 10) return

      const insights = output
        .split('\n')
        .map(l => l.trim())
        .filter(l => l.startsWith('[洞察]'))
        .map(l => l.replace(/^\[洞察\]\s*/, '').trim())
        .filter(l => l.length >= 5)
        .slice(0, 3)

      if (insights.length === 0) return

      // Store each insight as scope='insight'
      for (const insight of insights) {
        addMemory(insight, 'insight', undefined, 'private')
      }

      // Enforce MAX_INSIGHTS cap — remove oldest insights beyond limit
      // Use content+ts keys (not array indices) to avoid stale-index bugs after addMemory eviction
      const allInsights = memoryState.memories
        .filter(m => m.scope === 'insight')
        .sort((a, b) => a.ts - b.ts)
      if (allInsights.length > MAX_INSIGHTS) {
        const toRemoveKeys = new Set(
          allInsights.slice(0, allInsights.length - MAX_INSIGHTS).map(m => `${m.content}\0${m.ts}`)
        )
        for (let i = memoryState.memories.length - 1; i >= 0; i--) {
          const m = memoryState.memories[i]
          if (toRemoveKeys.has(`${m.content}\0${m.ts}`)) {
            memoryState.memories.splice(i, 1)
          }
        }
        rebuildScopeIndex()
        rebuildRecallIndex(memoryState.memories)
        saveMemories()
      }

      console.log(`[cc-soul][insight] generated ${insights.length} insights from ${recentMemories.length} recent memories`)
    }
  )
}

// ═══════════════════════════════════════════════════════════════════════════════
// Recall Feedback Loop — background improvement of missed recalls
// ═══════════════════════════════════════════════════════════════════════════════

let lastRecallFeedbackTs = 0
const RECALL_FEEDBACK_COOLDOWN = 60000 // 1 min cooldown

/**
 * After a response is sent, check if recall missed relevant memories.
 * If so, add cross-tags to missed memories so they'll be found next time.
 * Called async from handler.ts message:sent.
 *
 * v2.3: Uses local trigram similarity instead of LLM — zero cost, instant.
 */
export function recallFeedbackLoop(userMsg: string, recalledContents: string[]) {
  const now = Date.now()
  if (now - lastRecallFeedbackTs < RECALL_FEEDBACK_COOLDOWN) return
  if (memoryState.memories.length < 20) return
  if (userMsg.length < 10) return
  lastRecallFeedbackTs = now

  // Sample some un-recalled memories (random 30, excluding what was already recalled)
  const recalledSet = new Set(recalledContents)
  const candidates = shuffleArray(memoryState.memories
    .filter(m => !recalledSet.has(m.content) && m.content.length > 15))
    .slice(0, 30)

  if (candidates.length === 0) return

  // Local relevance scoring via trigram similarity
  const queryTri = trigrams(userMsg)
  const RELEVANCE_THRESHOLD = 0.08 // low bar — cross-tagging is cheap, false positives are OK

  const queryWords = (userMsg.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || [])
    .map(w => w.toLowerCase())
    .slice(0, 8)

  if (queryWords.length === 0) return

  let patched = 0
  for (const mem of candidates) {
    const memTri = trigrams(mem.content)
    const sim = trigramSimilarity(queryTri, memTri)
    if (sim < RELEVANCE_THRESHOLD) continue

    // Also check keyword overlap for higher confidence
    const memLower = mem.content.toLowerCase()
    const keywordHits = queryWords.filter(w => memLower.includes(w)).length
    if (sim < 0.12 && keywordHits === 0) continue // need either decent trigram or keyword hit

    // O(1) lookup via _memLookup instead of O(n) findIndex
    const real = _memLookup.get(`${mem.content}\0${mem.ts}`)
    if (!real) continue
    if (!real.tags) real.tags = []
    for (const w of queryWords) {
      if (!real.tags.includes(w)) {
        real.tags.push(w)
      }
    }
    // Cap tags at 25
    if (real.tags.length > 25) real.tags = real.tags.slice(-25)
    patched++
  }

  if (patched > 0) {
    saveMemories()
    console.log(`[cc-soul][recall-feedback] patched ${patched} memories with cross-tags (local trigram)`)
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// Multi-Signal Behavior Fusion (多信号行为融合)
// ═══════════════════════════════════════════════════════════════════════════════
//
// Replaces naive "reply length" heuristic with a 4-signal weighted assessment.
// Empirically ~3x more accurate than length-only judgment because:
//   - A short "ok" after a greeting is fine (not negative)
//   - A follow-up question is positive, not negative (even if short)
//   - Topic switch signals disinterest regardless of reply length
//   - Reply delay encodes engagement (fast=interested, timeout=abandoned)

/**
 * Multi-signal behavior fusion: combines 4 signals to assess last-turn reply quality.
 * More accurate than single "reply length" heuristic by ~3x.
 *
 * Signal 1: Reply length (short = possible dissatisfaction)
 * Signal 2: Reply delay (fast = engaged or follow-up; long silence = abandoned)
 * Signal 3: Follow-up detection (question = wants more info, not unhappy)
 * Signal 4: Topic switch (switch = previous topic ended / unwanted)
 */
export function assessResponseQuality(
  userReply: string,
  replyDelayMs: number,
  prevTopic: string,
  currentTopic: string,
): { quality: number; signal: 'positive' | 'neutral' | 'negative'; reason: string } {
  let score = 0.5  // default neutral
  const reasons: string[] = []

  // Signal 1: Length (weight 0.25)
  const len = userReply.length
  if (len > 50) { score += 0.12; reasons.push('长回复') }
  else if (len > 15) { score += 0.05 }
  else if (len < 5) { score -= 0.1; reasons.push('极短回复') }

  // Signal 2: Delay (weight 0.25)
  const delaySec = replyDelayMs / 1000
  if (delaySec < 5) { score += 0.1; reasons.push('快速回复') }       // fast = interested
  else if (delaySec > 120) { score -= 0.15; reasons.push('长时间沉默') }  // too long = possibly abandoned
  // 30-60s is normal thinking time, no adjustment

  // Signal 3: Follow-up detection (weight 0.25)
  if (/[？?]/.test(userReply) || /怎么|为什么|能不能|具体|详细/.test(userReply)) {
    score += 0.12
    reasons.push('追问')
  }
  // Closing phrases = end signal
  if (/^(嗯|好的?|ok|谢谢|收到|明白|了解)\s*[。.!！]?\s*$/i.test(userReply.trim())) {
    score -= 0.05  // mildly negative: satisfied but topic is done
    reasons.push('结束语')
  }

  // Signal 4: Topic switch (weight 0.25)
  if (prevTopic && currentTopic && prevTopic !== currentTopic) {
    score -= 0.08  // topic switch = previous topic may have been unsatisfying
    reasons.push('话题切换')
  }

  score = Math.max(0, Math.min(1, score))
  const signal = score > 0.6 ? 'positive' : score < 0.35 ? 'negative' : 'neutral'

  return { quality: score, signal, reason: reasons.join('+') || '正常' }
}

// ═══════════════════════════════════════════════════════════════════════════════
// Unified Association Engine — three-layer associative recall
// ═══════════════════════════════════════════════════════════════════════════════
//
// Layer A (sync, instant):  Graph entities + Topic nodes → association keywords → 2nd-hop recall
// Layer B (async, cached):  LLM deep association → "reminds me of..." connections
//
// Layer A runs pre-response (available this turn).
// Layer B runs post-response (cached for next turn).
// Together they replace the old keyword-only + LLM-only split.

let cachedAssociation: { query: string; result: string; memories: string[]; ts: number } | null = null
const ASSOCIATION_COOLDOWN = 30000 // 30s cooldown

/**
 * Layer A: Synchronous graph+topic association.
 * Returns additional memories found through entity graph traversal and topic node matching.
 * Called from handler-augments.ts during augment building.
 */
export function associateSync(userMsg: string, recalled: Memory[], userId?: string, channelId?: string): Memory[] {
  if (userMsg.length < 5 || recalled.length < 2) return []

  const CJK_RE = /[\u4e00-\u9fff]{2,}|[a-z]{4,}/gi
  const seenContents = new Set(recalled.map(m => m.content.slice(0, 60)))
  const associationKeywords = new Set<string>()

  // Source 1: Graph entity activation — walk from mentioned entities to neighbors
  const mentioned = findMentionedEntities(userMsg)
  if (mentioned.length > 0) {
    const related = getRelatedEntities(mentioned, 2, 6)
    for (const entity of related) {
      const words = (entity.match(CJK_RE) || []).map((w: string) => w.toLowerCase())
      for (const w of words) associationKeywords.add(w)
    }
  }

  // Source 2: Topic nodes — find matching topics from distilled knowledge
  try {
    const distMod = getLazyModule('distill'); const getRelevantTopics = distMod?.getRelevantTopics
    const topics = getRelevantTopics(userMsg, userId, 3) as { topic: string; summary: string }[]
    for (const t of topics) {
      const words = ((t.topic + ' ' + t.summary).match(CJK_RE) || []).map((w: string) => w.toLowerCase())
      for (const w of words.slice(0, 3)) associationKeywords.add(w)
    }
  } catch { /* distill module not loaded yet */ }

  // Source 3: Keywords from top recalled memories (chain association)
  for (const m of recalled.slice(0, 3)) {
    const words = (m.content.match(CJK_RE) || []).map((w: string) => w.toLowerCase())
    for (const w of words.slice(0, 2)) associationKeywords.add(w)
  }

  // Remove words already in user message
  const userWords = new Set((userMsg.match(CJK_RE) || []).map((w: string) => w.toLowerCase()))
  for (const w of userWords) associationKeywords.delete(w)

  if (associationKeywords.size < 2) return []

  // 2nd-hop recall using combined association keywords
  const query = [...associationKeywords].slice(0, 8).join(' ')
  const associated = recall(query, 6, userId, channelId)

  // Dedup against first round
  const novel = associated.filter(m => !seenContents.has(m.content.slice(0, 60)))
  if (novel.length > 0) {
    console.log(`[cc-soul][association] sync: "${query.slice(0, 30)}" → ${novel.length} associated memories`)
  }
  return novel.slice(0, 4)
}

/**
 * Layer B: Async LLM deep association (post-response).
 * Uses top recalled + Layer A results to ask LLM for hidden connections.
 * Result cached for next turn.
 */
export function triggerAssociativeRecall(userMsg: string, topRecalled: string[]) {
  if (userMsg.length < 10) return
  if (cachedAssociation && Date.now() - cachedAssociation.ts < ASSOCIATION_COOLDOWN) return

  // Use Layer A results + random sample for LLM to analyze
  const recalledSet = new Set(topRecalled)
  const pool = shuffleArray(memoryState.memories
    .filter(m => !recalledSet.has(m.content) && m.content.length > 15 && m.scope !== 'proactive' && m.scope !== 'expired' && m.scope !== 'decayed'))
    .slice(0, 20)

  if (pool.length < 3) return

  const memList = pool.map((m, i) => `${i + 1}. ${m.content.slice(0, 80)}`).join('\n')

  spawnCLI(
    `用户说: "${userMsg.slice(0, 200)}"\n\n` +
    `已直接召回: ${topRecalled.slice(0, 3).map(r => r.slice(0, 40)).join('; ')}\n\n` +
    `以下记忆中，哪些和用户话题有隐含关联？（不是字面匹配，是深层联想——比如话题相关、因果链、同一时期的事）\n` +
    `${memList}\n\n` +
    `选1-3条最相关的，格式: "序号. 内容摘要 — 关联原因"。都不相关回答"无"`,
    (output) => {
      if (!output || output.includes('无') || output.length < 5) {
        cachedAssociation = null
        return
      }
      // Extract referenced memory contents for augment
      const nums = output.match(/(\d+)\./g)?.map(n => parseInt(n)) || []
      const referencedMems = nums.filter(n => n >= 1 && n <= pool.length).map(n => pool[n - 1].content.slice(0, 80))

      cachedAssociation = {
        query: userMsg.slice(0, 50),
        result: output.slice(0, 300),
        memories: referencedMems,
        ts: Date.now(),
      }
      console.log(`[cc-soul][association] deep: ${referencedMems.length} hidden connections found`)
    }
  )
}

/**
 * Get cached deep association result (from Layer B, previous turn).
 */
export function getAssociativeRecall(): string {
  if (!cachedAssociation) return ''
  if (Date.now() - cachedAssociation.ts > 300000) {
    cachedAssociation = null
    return ''
  }
  return `[深层联想] ${cachedAssociation.result}`
}

// ═══════════════════════════════════════════════════════════════════════════════
// Session Summary — triggered when conversation flow resolves or goes idle
// ═══════════════════════════════════════════════════════════════════════════════

let lastSessionSummaryTs = 0
const SESSION_SUMMARY_COOLDOWN = 1800000 // 30 min cooldown

// ═══════════════════════════════════════════════════════════════════════════════
// Active Memory Management — model can explicitly manage memories via markers
// ═══════════════════════════════════════════════════════════════════════════════

interface MemoryCommand {
  action: 'remember' | 'forget' | 'update' | 'search'
  content: string
  oldContent?: string  // for update
}

/**
 * Parse memory commands from model's response text.
 * Markers: （记下了：...）（忘掉：...）（更正记忆：旧→新）（想查：...）
 */
export function parseMemoryCommands(responseText: string): MemoryCommand[] {
  const commands: MemoryCommand[] = []

  // （记下了：...） or （记住：...）
  const rememberPattern = /[（(](?:记下了|记住|记下|save)[：:]\s*(.+?)[）)]/g
  let match
  while ((match = rememberPattern.exec(responseText)) !== null) {
    commands.push({ action: 'remember', content: match[1].trim() })
  }

  // （忘掉：...） or （忘记：...）
  const forgetPattern = /[（(](?:忘掉|忘记|forget|过时了)[：:]\s*(.+?)[）)]/g
  while ((match = forgetPattern.exec(responseText)) !== null) {
    commands.push({ action: 'forget', content: match[1].trim() })
  }

  // （更正记忆：旧内容→新内容）
  const updatePattern = /[（(](?:更正记忆|更新记忆|update)[：:]\s*(.+?)\s*(?:→|->)+\s*(.+?)[）)]/g
  while ((match = updatePattern.exec(responseText)) !== null) {
    commands.push({ action: 'update', content: match[2].trim(), oldContent: match[1].trim() })
  }

  // （想查：...）
  const searchPattern = /[（(](?:想查|查一下|search|回忆一下)[：:]\s*(.+?)[）)]/g
  while ((match = searchPattern.exec(responseText)) !== null) {
    commands.push({ action: 'search', content: match[1].trim() })
  }

  return commands
}

/** Cached search results from model's search requests, injected next turn */
let pendingSearchResults: string[] = []

export function getPendingSearchResults(): string[] {
  const results = [...pendingSearchResults]
  pendingSearchResults = []
  return results
}

/**
 * Execute memory commands parsed from model response.
 * Called from handler.ts message:sent.
 */
export function executeMemoryCommands(commands: MemoryCommand[], userId?: string, channelId?: string) {
  for (const cmd of commands) {
    switch (cmd.action) {
      case 'remember':
        addMemory(cmd.content, 'fact', userId, 'global', channelId)
        console.log(`[cc-soul][active-memory] REMEMBER: ${cmd.content.slice(0, 60)}`)
        break

      case 'forget': {
        // Anti-hallucination: require keyword >= 4 chars to prevent overly broad matches
        const keyword = cmd.content.toLowerCase().trim()
        if (keyword.length < 4) {
          console.log(`[cc-soul][active-memory] FORGET blocked: keyword too short "${keyword}" (min 4 chars, anti-hallucination)`)
          break
        }
        // Find and mark matching memories as expired (don't delete, just tag)
        const MAX_FORGET_PER_CMD = 3 // anti-hallucination: cap bulk deletions
        let forgotten = 0
        for (const mem of memoryState.memories) {
          if (forgotten >= MAX_FORGET_PER_CMD) {
            console.log(`[cc-soul][active-memory] FORGET capped at ${MAX_FORGET_PER_CMD} (keyword: ${keyword.slice(0, 30)}), remaining untouched`)
            break
          }
          if (mem.content.toLowerCase().includes(keyword) && mem.scope !== 'consolidated' && mem.scope !== 'expired') {
            mem.scope = 'expired'
            forgotten++
          }
        }
        if (forgotten > 0) {
          saveMemories()
          rebuildScopeIndex() // scope changed, index stale
          console.log(`[cc-soul][active-memory] FORGET: marked ${forgotten} memories as expired (keyword: ${cmd.content.slice(0, 30)})`)
        }
        break
      }

      case 'update': {
        // Find old memory, replace content
        if (!cmd.oldContent) break
        const oldKw = cmd.oldContent.toLowerCase()
        for (const mem of memoryState.memories) {
          if (mem.content.toLowerCase().includes(oldKw) && mem.scope !== 'expired') {
            console.log(`[cc-soul][active-memory] UPDATE: "${mem.content.slice(0, 40)}" → "${cmd.content.slice(0, 40)}"`)
            mem.content = cmd.content
            mem.ts = Date.now()
            mem.tags = undefined // re-tag on next cycle
            break // only update first match
          }
        }
        saveMemories()
        rebuildScopeIndex() // content changed, index may need update
        break
      }

      case 'search': {
        // Search and cache results for next turn injection
        const results = recall(cmd.content, 5, userId, channelId)
        if (results.length > 0) {
          pendingSearchResults = results.map(m => `- ${m.content}${m.emotion && m.emotion !== 'neutral' ? ` (${m.emotion})` : ''}`)
          console.log(`[cc-soul][active-memory] SEARCH "${cmd.content.slice(0, 30)}": found ${results.length} results (cached for next turn)`)
        }
        break
      }
    }
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// Memory Contradiction Detection — periodic scan for conflicting memories
// ═══════════════════════════════════════════════════════════════════════════════

let lastContradictionScan = 0
const CONTRADICTION_SCAN_COOLDOWN = 24 * 3600000 // once per day

/**
 * Scan memories for contradictions within the same scope.
 * Group by scope, sample pairs, ask CLI to detect conflicts.
 * Conflicting older memories get marked as expired.
 */
export function scanForContradictions() {
  const now = Date.now()
  if (now - lastContradictionScan < CONTRADICTION_SCAN_COOLDOWN) return
  if (memoryState.memories.length < 20) return
  lastContradictionScan = now

  // Group by scope, only check fact/preference/correction (most likely to conflict)
  const conflictScopes = ['fact', 'preference', 'correction']
  const groups = new Map<string, Memory[]>()
  for (const mem of memoryState.memories) {
    if (!conflictScopes.includes(mem.scope)) continue
    if (mem.scope === 'expired') continue
    if (!groups.has(mem.scope)) groups.set(mem.scope, [])
    groups.get(mem.scope)!.push(mem)
  }

  for (const [scope, mems] of groups) {
    if (mems.length < 5) continue

    // Sample recent 10 vs older 10 (most likely conflict pairs)
    const sorted = [...mems].sort((a, b) => b.ts - a.ts)
    const recent = sorted.slice(0, 10)
    const older = sorted.slice(10, 20)
    if (older.length < 3) continue

    // B2: try fact-store contradiction detection first to skip LLM
    let foundContradiction = false
    try {
      const { extractFacts } = require('./fact-store.ts')
      const { classifyConflict } = require('./memory-utils.ts')
      for (const r of recent) {
        for (const o of older) {
          const rFacts = extractFacts(r.content)
          const oFacts = extractFacts(o.content)
          const conflict = classifyConflict(oFacts, rFacts)
          if (conflict === 'supersede') {
            o.validUntil = o.validUntil || Date.now()
            foundContradiction = true
            try { require('./decision-log.ts').logDecision('contradiction_zerollm', o.content.slice(0, 30), `superseded by ${r.content.slice(0, 30)}`) } catch {}
          }
        }
      }
    } catch {}
    if (foundContradiction) continue  // Skip LLM for this scope

    const recentList = recent.map((m, i) => `新${i + 1}. ${m.content.slice(0, 80)}`).join('\n')
    const olderList = older.map((m, i) => `旧${i + 1}. ${m.content.slice(0, 80)}`).join('\n')

    spawnCLI(
      `以下是同类型(${scope})的新旧记忆，检查是否有矛盾（同一件事说法不同、前后不一致）。\n\n` +
      `最近的记忆:\n${recentList}\n\n` +
      `较早的记忆:\n${olderList}\n\n` +
      `如果有矛盾，输出格式: "旧N 与 新M 矛盾: 原因"（可多条）\n` +
      `如果没有矛盾，回答"无"`,
      (output) => {
        if (!output || output.includes('无')) return

        // Parse contradiction pairs
        const lines = output.split('\n').filter(l => l.includes('矛盾'))
        let timeBounded = 0
        for (const line of lines) {
          const oldMatch = line.match(/旧(\d+)/)
          if (oldMatch) {
            const idx = parseInt(oldMatch[1]) - 1
            if (idx >= 0 && idx < older.length) {
              const memIdx = memoryState.memories.findIndex(m => m.content === older[idx].content && m.ts === older[idx].ts)
              if (memIdx >= 0) {
                // Temporal knowledge: mark as time-bounded rather than deleting
                // Keep scope intact — the fact was true in the past, just not anymore
                const mem = memoryState.memories[memIdx]
                mem.validUntil = Date.now()
                if (!mem.validFrom) mem.validFrom = mem.ts
                timeBounded++
              }
            }
          }
        }

        if (timeBounded > 0) {
          saveMemories()
          console.log(`[cc-soul][contradiction] time-bounded ${timeBounded} contradicted memories in scope "${scope}" (kept as historical)`)
        }
      }
    )
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// Predictive Memory — pre-load context before user speaks
// ═══════════════════════════════════════════════════════════════════════════════

let lastPredictionTs = 0
let cachedPrediction: string[] = []

/**
 * Based on user's rhythm (time patterns) + recent conversation topics,
 * predict what they might ask about and pre-load relevant memories.
 * Called at the START of preprocessed, before the user's actual message is processed.
 */
export function predictiveRecall(userId?: string, channelId?: string): string[] {
  const now = Date.now()
  // Only predict if we have cached results (generated async after last message)
  const results = [...cachedPrediction]
  cachedPrediction = [] // consume
  return results
}

/**
 * Async: after a message is processed, predict what comes next.
 * Uses recent topics + time of day + conversation pattern.
 * Called from handler.ts message:sent.
 */
export function generatePrediction(recentTopics: string[], userId?: string) {
  if (recentTopics.length === 0) return
  if (Date.now() - lastPredictionTs < 60000) return // 1 min cooldown
  lastPredictionTs = Date.now()

  // Find memories related to recent topics (pre-warm for next message)
  const topicStr = recentTopics.slice(-3).join('、')
  const candidates = memoryState.memories
    .filter(m => {
      if (m.scope === 'expired' || m.scope === 'proactive') return false
      const content = m.content.toLowerCase()
      return recentTopics.some(t => content.includes(t.toLowerCase()))
    })
    .sort((a, b) => b.ts - a.ts)
    .slice(0, 5)

  if (candidates.length > 0) {
    cachedPrediction = candidates.map(m => m.content)
    console.log(`[cc-soul][predictive] pre-loaded ${candidates.length} memories for topics: ${topicStr}`)
  }
}

export function triggerSessionSummary(recentTurns?: number) {
  const now = Date.now()
  if (now - lastSessionSummaryTs < SESSION_SUMMARY_COOLDOWN) return
  if (memoryState.chatHistory.length < 3) return
  lastSessionSummaryTs = now

  const turns = memoryState.chatHistory.slice(-(recentTurns || 10))

  // B4: extractive session summary first — skip LLM if we can build a decent summary
  if (turns.length >= 2) {
    const firstTopic = turns[0].user.slice(0, 50)
    const lastPoint = turns[turns.length - 1].assistant.slice(0, 80)
    let entities: string[] = []
    try { entities = require('./graph.ts').findMentionedEntities(turns.map((t: any) => t.user).join(' ')).slice(0, 3) } catch {}
    const extractive = `讨论了${firstTopic}${entities.length > 0 ? '，涉及' + entities.join('/') : ''}。${lastPoint}`
    if (extractive.length > 30) {
      addMemory(`[会话摘要] ${extractive.slice(0, 300)}`, 'consolidated', undefined, 'global')
      console.log(`[cc-soul][session-summary] extractive: ${extractive.slice(0, 80)}`)
      return
    }
  }

  const conversation = turns.map(t => `用户: ${t.user.slice(0, 200)}\n助手: ${t.assistant.slice(0, 200)}`).join('\n\n')

  spawnCLI(
    `以下是一段完整对话，请写一条高质量的会话摘要（2-3句话），包含：\n` +
    `1. 讨论了什么主题\n` +
    `2. 关键结论或决定\n` +
    `3. 是否有遗留问题\n` +
    `不要说"用户和助手讨论了..."，直接写内容。\n\n${conversation}`,
    (output) => {
      if (output && output.length > 20) {
        addMemory(`[会话摘要] ${output.slice(0, 300)}`, 'consolidated', undefined, 'global')
        console.log(`[cc-soul][session-summary] ${output.slice(0, 80)}`)
      }
    }
  )
}

// ═══════════════════════════════════════════════════════════════════════════════
// Network Knowledge Maintenance — expiry + trust decay
// ═══════════════════════════════════════════════════════════════════════════════

let lastNetworkCleanup = 0
const NETWORK_CLEANUP_COOLDOWN = 24 * 3600000 // daily

/**
 * Clean up network knowledge:
 * 1. Expire knowledge older than 90 days that hasn't been "confirmed" by local usage
 * 2. Downgrade low-trust knowledge that was never recalled
 * 3. Remove contradictions between network and local knowledge (local wins)
 */
export function cleanupNetworkKnowledge() {
  const now = Date.now()
  if (now - lastNetworkCleanup < NETWORK_CLEANUP_COOLDOWN) return
  lastNetworkCleanup = now

  let expired = 0
  let downgraded = 0

  for (const mem of memoryState.memories) {
    if (!mem.content.startsWith('[网络知识')) continue
    if (mem.scope === 'expired') continue

    const ageDays = (now - mem.ts) / 86400000

    // Rule 1: Network knowledge older than 90 days with no tags (never recalled/used) → expire
    if (ageDays > 90 && (!mem.tags || mem.tags.length === 0)) {
      mem.scope = 'expired'
      expired++
      continue
    }

    // Rule 2: Low-trust knowledge older than 30 days → expire
    if (mem.content.includes('低可信') && ageDays > 30) {
      mem.scope = 'expired'
      expired++
      continue
    }

    // Rule 3: "待验证" knowledge older than 60 days → downgrade to expired
    if (mem.content.includes('待验证') && ageDays > 60) {
      mem.scope = 'expired'
      downgraded++
      continue
    }
  }

  if (expired > 0 || downgraded > 0) {
    saveMemories()
    console.log(`[cc-soul][network-cleanup] expired ${expired}, downgraded ${downgraded} network memories`)
  }
}

/**
 * When local knowledge contradicts network knowledge, local wins.
 * Called during scanForContradictions — enhanced to handle network vs local.
 */
// ═══════════════════════════════════════════════════════════════════════════════
// EPISODIC MEMORY — complete event chains, not just facts
// ═══════════════════════════════════════════════════════════════════════════════

const EPISODES_PATH = resolve(DATA_DIR, 'episodes.json')
const MAX_EPISODES = 200

interface Episode {
  id: string
  timestamp: number
  topic: string
  turns: { role: 'user' | 'assistant'; content: string; emotion?: string }[]
  correction?: { what: string; cause: string }
  resolution: 'resolved' | 'abandoned' | 'ongoing'
  lesson?: string          // what was learned from this episode
  frustrationPeak: number  // max frustration during episode
}

let episodes: Episode[] = []

export function loadEpisodes() {
  episodes = loadJson<Episode[]>(EPISODES_PATH, [])
  console.log(`[cc-soul][episodes] loaded ${episodes.length} episodes`)
}

function saveEpisodes() {
  debouncedSave(EPISODES_PATH, episodes)
}

/**
 * Record a complete episode from conversation flow data.
 * Called when a conversation topic resolves or is abandoned.
 */
export function recordEpisode(
  topic: string,
  turns: { role: 'user' | 'assistant'; content: string }[],
  correction?: { what: string; cause: string },
  resolution: 'resolved' | 'abandoned' = 'resolved',
  frustrationPeak = 0,
  lesson?: string,
) {
  const episode: Episode = {
    id: Date.now().toString(36) + Math.random().toString(36).slice(2, 4),
    timestamp: Date.now(),
    topic: topic.slice(0, 100),
    turns: turns.slice(-10).map(t => ({ ...t, content: t.content.slice(0, 200) })),
    correction,
    resolution,
    lesson,
    frustrationPeak,
  }

  episodes.push(episode)
  if (episodes.length > MAX_EPISODES) episodes = episodes.slice(-Math.floor(MAX_EPISODES * 0.8))
  saveEpisodes()
  console.log(`[cc-soul][episodes] recorded: ${topic.slice(0, 40)} [${resolution}]`)
}

/**
 * Recall relevant episodes for current context.
 * Matches by topic keywords.
 */
export function recallEpisodes(msg: string, topN = 2): Episode[] {
  if (episodes.length === 0) return []
  const words = new Set((msg.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map(w => w.toLowerCase()))
  if (words.size === 0) return []

  const scored = episodes.map(ep => {
    const topicWords = (ep.topic.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map(w => w.toLowerCase())
    const overlap = topicWords.filter(w => words.has(w)).length
    // Boost episodes with corrections (more educational)
    const correctionBoost = ep.correction ? 1.5 : 1.0
    return { ep, score: overlap * correctionBoost }
  }).filter(s => s.score > 0).sort((a, b) => b.score - a.score)

  return scored.slice(0, topN).map(s => s.ep)
}

/**
 * Build episode context for augment injection.
 */
export function buildEpisodeContext(msg: string): string {
  const relevant = recallEpisodes(msg)
  if (relevant.length === 0) return ''

  const lines = relevant.map(ep => {
    let desc = `[Episode] ${ep.topic}`
    if (ep.correction) desc += ` — you made a mistake: ${ep.correction.what} (cause: ${ep.correction.cause})`
    if (ep.lesson) desc += ` — lesson: ${ep.lesson}`
    if (ep.frustrationPeak > 0.5) desc += ` — user was frustrated`
    return desc
  })
  return lines.join('\n')
}

export { episodes }

// ═══════════════════════════════════════════════════════════════════════════════
// TIME-DECAY TIERED MEMORY — short_term → mid_term → long_term lifecycle
// ═══════════════════════════════════════════════════════════════════════════════

const HOUR_MS = 3600000
const DAY_MS = 86400000
const SHORT_TERM_THRESHOLD = 24 * HOUR_MS       // 24 hours
const MID_TERM_THRESHOLD = 30 * DAY_MS           // 30 days
const RECALL_UPGRADE_COUNT = 1                    // recalls needed to upgrade short→mid

let lastDecayTs = 0
const DECAY_COOLDOWN = 6 * HOUR_MS               // run at most every 6 hours

// ═══════════════════════════════════════════════════════════════════════════════
// Creative Forgetting — 渐进模糊化而非二元存亡
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * 遗忘创造力：记忆不是"活/死"二元状态，而是渐进模糊化
 * 基于 Fuzzy-trace Theory (Reyna & Brainerd 1995)
 *
 * Stage 1 (Verbatim): 完整原文，<30天
 * Stage 2 (Detail-fading): 移除具体日期/数字，30-90天
 * Stage 3 (Gist-only): 只保留核心要旨，90-180天
 * Stage 4 (Schema-absorbed): 被吸收进 person-model，记忆消亡
 */
function creativeForget(mem: Memory, ageDays: number): { action: 'keep' | 'fade' | 'gist' | 'absorb'; content?: string } {
  // 核心记忆/纠正/高importance 不做模糊化
  if (mem.scope === 'correction' || mem.scope === 'pinned' || mem.scope === 'consolidated') return { action: 'keep' }
  if ((mem.importance ?? 5) >= 8) return { action: 'keep' }
  if ((mem.recallCount ?? 0) >= 5) return { action: 'keep' } // 频繁被用的不模糊

  if (ageDays < 30) return { action: 'keep' }

  if (ageDays < 90) {
    // Stage 2: 细节模糊化（纯规则，不用 LLM）
    let content = mem.content
    // 移除具体日期
    content = content.replace(/\d{4}[年\-\/]\d{1,2}[月\-\/]\d{1,2}[日号]?/g, '')
    // 移除具体时间
    content = content.replace(/[上下]午\d{1,2}[点时:：]\d{0,2}分?/g, '')
    content = content.replace(/凌晨|早上|中午|傍晚|晚上\d{1,2}点/g, '')
    // 数字模糊化：大数字变量级
    content = content.replace(/(\d{4,})(\s*元|块|万|千)/g, (_, n, unit) => {
      const num = parseInt(n)
      if (num >= 10000) return `几${unit === '万' ? '万' : '万' + unit}`
      if (num >= 1000) return `几千${unit}`
      return `${n}${unit}`
    })
    // 移除"今天""昨天""刚才"等时效词
    content = content.replace(/今天|昨天|前天|刚才|刚刚|方才/g, '之前')
    content = content.trim().replace(/\s{2,}/g, ' ')
    if (content.length < 5) return { action: 'keep' } // 模糊后太短，保留原文
    return { action: 'fade', content }
  }

  if (ageDays < 180) {
    // Stage 3: 抽象升维压缩 — 从事实升维到特征理解
    // "用户每天跑步5公里但膝盖疼还坚持" → "运动型+意志力强+有损伤风险"
    const content = mem.content
    const traits: string[] = []

    // 行为特征提取规则（不是正则匹配具体内容，而是提取模式）
    if (/每天|经常|总是|习惯|一直/.test(content)) traits.push('有规律性')
    if (/坚持|还是|虽然.*但|即使.*也/.test(content)) traits.push('意志力强')
    if (/喜欢|最爱|偏好|热爱/.test(content)) {
      const obj = content.match(/喜欢(.{2,8})/)?.[1] || ''
      if (obj) traits.push(`偏好:${obj.replace(/[，。！？\s]+$/, '')}`)
    }
    if (/讨厌|不喜欢|受不了|反感/.test(content)) {
      const obj = content.match(/(?:讨厌|不喜欢)(.{2,8})/)?.[1] || ''
      if (obj) traits.push(`反感:${obj.replace(/[，。！？\s]+$/, '')}`)
    }
    if (/焦虑|压力|紧张|担心/.test(content)) traits.push('有压力')
    if (/学|研究|探索|尝试/.test(content)) traits.push('学习型')
    if (/帮|支持|关心|照顾/.test(content)) traits.push('关怀型')
    if (/快|效率|优化|性能/.test(content)) traits.push('效率导向')
    if (/疼|不舒服|生病|失眠/.test(content)) traits.push('健康问题')
    if (/开心|高兴|兴奋|满足/.test(content)) traits.push('正面体验')
    if (/难过|伤心|失望|沮丧/.test(content)) traits.push('负面体验')

    if (traits.length === 0) {
      // 无法升维，降级为关键词提取（原逻辑）
      const keywords = (content.match(/[\u4e00-\u9fff]{2,4}|[a-zA-Z]{3,}/g) || []).slice(0, 5)
      if (keywords.length === 0) return { action: 'keep' }
      return { action: 'gist', content: `[模糊记忆] ${keywords.join('、')}` }
    }

    return { action: 'gist', content: `[特征理解] ${traits.join('、')}` }
  }

  // Stage 4: 超过180天，应该被吸收进 person-model
  return { action: 'absorb' }
}

/**
 * Process time-based memory decay and tier transitions.
 * Called from heartbeat. Scans all memories and applies tier lifecycle:
 *
 * - short_term > 24h + recallCount >= 2 → upgrade to mid_term
 * - short_term > 24h + recallCount < 2  → mark decayed (scope = 'decayed', keep content)
 * - mid_term > 30 days + no recall in last 30 days → downgrade to long_term, compress content
 *
 * Compatible with old data: missing tier defaults to 'short_term', missing recallCount defaults to 0.
 */
export function processMemoryDecay() {
  const now = Date.now()
  if (now - lastDecayTs < DECAY_COOLDOWN) return
  lastDecayTs = now

  // Fix ts=0 memories: use lastAccessed if available, otherwise distribute over last 30 days
  let tsRepaired = 0
  for (const mem of memoryState.memories) {
    if (!mem.ts || mem.ts === 0) {
      mem.ts = mem.lastAccessed || (now - Math.random() * 30 * DAY_MS)
      tsRepaired++
    }
  }
  if (tsRepaired > 0) {
    console.log(`[cc-soul][memory-decay] repaired ${tsRepaired} memories with ts=0`)
  }

  let upgraded = 0
  let decayed = 0
  let compressed = 0
  let faded = 0
  let gisted = 0
  let absorbed = 0

  const useArchive = true // dag_archive is always-on
  let archived = 0

  // High-value scopes: skip decay entirely (never expire, always recallable)
  const PROTECTED_SCOPES = new Set([
    'fact', 'wal', 'preference', 'event',
    'correction', 'deep_feeling', 'wisdom', 'pinned',
  ])

  for (const mem of memoryState.memories) {
    // Skip already expired/consolidated/decayed/pinned/archived
    if (mem.scope === 'expired' || mem.scope === 'decayed' || mem.scope === 'pinned' || mem.scope === 'archived') continue

    // High-value memories: never decay, always available for recall
    if (PROTECTED_SCOPES.has(mem.scope)) continue

    // MemRL utility 软调制：高 utility 记忆降低衰减概率（不硬免疫）
    // utility=3 → 70% 概率跳过本轮衰减；utility=1 → 30% 跳过
    if ((mem.utility ?? 0) > 0 && Math.random() < Math.min(0.7, (mem.utility ?? 0) * 0.15)) continue

    // 72h 巩固免疫：刚合并产出的记忆需要时间被用户验证，避免立刻衰减
    if (mem.scope === 'consolidated' && (now - (mem.ts || 0)) < 72 * 60 * 60 * 1000) continue

    const tier = mem.tier || 'short_term'
    const age = now - (mem.ts || mem.lastAccessed || now)
    const recallCount = mem.recallCount ?? 0
    const lastRecalled = mem.lastRecalled ?? 0

    // ── Creative Forgetting: 渐进模糊化而非二元删除 ──
    const ageDays = age / DAY_MS
    const cf = creativeForget(mem, ageDays)
    if (cf.action === 'fade' && cf.content && cf.content !== mem.content) {
      // 保存原文到 history
      if (!mem.history) mem.history = []
      if (mem.history.length < 5) mem.history.push({ content: mem.content, ts: now })
      mem.content = cf.content
      mem.tier = 'fading'
      faded++
      continue
    }
    if (cf.action === 'gist' && cf.content) {
      if (!mem.history) mem.history = []
      if (mem.history.length < 5) mem.history.push({ content: mem.content, ts: now })
      mem.content = cf.content
      mem.tier = 'gist'
      gisted++
      continue
    }
    if (cf.action === 'absorb') {
      mem.scope = 'expired'
      mem.tier = 'absorbed'
      absorbed++
      // TODO: 吸收进 person-model（异步）
      continue
    }

    if (tier === 'short_term' && age > SHORT_TERM_THRESHOLD) {
      // 升级条件：有效召回（用户 engaged）比次数更重要
      // 审核结论：recallCount ≥ 1 太低，偶然的 spreading activation 会误升级
      const effectiveRecall = (mem.injectionEngagement ?? 0) >= 1 || recallCount >= RECALL_UPGRADE_COUNT
      if (effectiveRecall) {
        // Promoted: actively used memory → mid_term
        mem.tier = 'mid_term'
        upgraded++
      } else if (useArchive) {
        // DAG Archive: compress but preserve original in raw_line
        archiveMemory(mem)
        archived++
      } else {
        // Legacy: hard decay
        mem.scope = 'decayed'
        mem.tier = 'short_term'
        decayed++
      }
    } else if (tier === 'mid_term' && age > MID_TERM_THRESHOLD) {
      // Check if recalled in the last 30 days
      const recentlyRecalled = lastRecalled > 0 && (now - lastRecalled) < MID_TERM_THRESHOLD
      if (!recentlyRecalled) {
        // Downgrade to long_term with content compression
        mem.tier = 'long_term'
        // Compress: keep first 100 chars as core fact summary
        if (mem.content.length > 120) {
          mem.content = mem.content.slice(0, 100).trimEnd() + '…'
        }
        compressed++
      }
    }
    // MemRL utility decay: 0.99/cycle, half-life ~3 days
    if (mem.utility && Math.abs(mem.utility) > 0.01) {
      mem.utility *= 0.99
      if (Math.abs(mem.utility) < 0.01) mem.utility = 0
    }

    // long_term memories stay as-is (already compressed, permanent storage)
  }

  if (upgraded > 0 || decayed > 0 || compressed > 0 || archived > 0 || faded > 0 || gisted > 0 || absorbed > 0) {
    rebuildScopeIndex()
    rebuildRecallIndex(memoryState.memories)
    saveMemories()
    console.log(`[cc-soul][memory-decay] upgraded=${upgraded} decayed=${decayed} compressed=${compressed} archived=${archived} faded=${faded} gisted=${gisted} absorbed=${absorbed}`)
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// Expired Memory Physical Cleanup — remove truly dead memories from storage
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Physically delete expired memories older than 30 days.
 * Also cleans up decayed memories older than 90 days that were never recalled.
 * Called from heartbeat (daily cadence).
 */
let lastPhysicalCleanup = 0
const PHYSICAL_CLEANUP_COOLDOWN = 24 * 3600000 // once per day

export function pruneExpiredMemories() {
  const now = Date.now()
  if (now - lastPhysicalCleanup < PHYSICAL_CLEANUP_COOLDOWN) return
  lastPhysicalCleanup = now

  // SQLite cleanup (handles both expired deletion + vector cleanup)
  if (useSQLite) {
    sqliteCleanupExpired()
  }

  // In-memory array cleanup
  const before = memoryState.memories.length
  const EXPIRED_CUTOFF = 30 * 86400000   // 30 days
  const DECAYED_CUTOFF = 90 * 86400000   // 90 days

  // High-value scopes: never physically delete
  const PROTECTED_SCOPES_DEL = new Set([
    'fact', 'wal', 'preference', 'event',
    'correction', 'deep_feeling', 'wisdom', 'pinned',
  ])

  memoryState.memories = memoryState.memories.filter(m => {
    if (PROTECTED_SCOPES_DEL.has(m.scope)) return true  // never delete high-value
    if (m.scope === 'expired' && now - m.ts > EXPIRED_CUTOFF) return false
    if (m.scope === 'decayed' && now - m.ts > DECAYED_CUTOFF && (m.recallCount ?? 0) === 0) return false
    return true
  })

  const removed = before - memoryState.memories.length
  if (removed > 0) {
    rebuildScopeIndex()
    rebuildRecallIndex(memoryState.memories)
    saveMemories()
    console.log(`[cc-soul][prune] physically removed ${removed} dead memories (${before} → ${memoryState.memories.length})`)
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// Old Memory Compression — compress verbose old memories to save storage + tokens
// ═══════════════════════════════════════════════════════════════════════════════

let lastCompression = 0
const COMPRESSION_COOLDOWN = 24 * 3600000 // once per day

/**
 * Compress old memories in-place:
 * - Memories > 7 days old with content > 100 chars → summarize to ~50%
 * - Memories > 30 days old with content > 60 chars → compress to key facts
 * - Preserves history[] for audit trail
 * - Skips: correction, core, consolidated (already condensed)
 */
export function compressOldMemories() {
  const now = Date.now()
  if (now - lastCompression < COMPRESSION_COOLDOWN) return
  lastCompression = now

  const SKIP_SCOPES = new Set(['correction', 'consolidated', 'expired', 'decayed', 'dream', 'curiosity'])
  const SEVEN_DAYS = 7 * 86400000
  const THIRTY_DAYS = 30 * 86400000
  let compressed = 0

  for (const mem of memoryState.memories) {
    if (SKIP_SCOPES.has(mem.scope)) continue
    // 闪光灯记忆永不压缩（detailLevel: 'full'）
    if (mem.flashbulb?.detailLevel === 'full') continue
    const age = now - mem.ts

    // Level 1: >7 days, >100 chars → summarize
    if (age > SEVEN_DAYS && mem.content.length > 100 && mem.tier !== 'long_term') {
      const original = mem.content
      // Simple summarization: keep first sentence + key nouns
      const firstSentence = mem.content.split(/[。！？\n]/)[0]
      if (firstSentence && firstSentence.length < mem.content.length * 0.6) {
        if (!mem.history) mem.history = []
        mem.history.push({ content: original, ts: now })
        mem.content = firstSentence.slice(0, 80)
        mem.tier = 'mid_term'
        compressed++
      }
    }

    // Level 2: >30 days, still >60 chars → 用 fact-store 三元组替代粗暴截断
    // 审核结论：正则提取语义不靠谱，SPO 三元组更精确
    if (age > THIRTY_DAYS && mem.content.length > 60 && mem.tier !== 'long_term') {
      const original = mem.content
      if (!mem.history) mem.history = []
      if (!mem.history.some(h => h.content === original)) {
        mem.history.push({ content: original, ts: now })
      }

      // 优先用 fact-store 三元组作为 gist（零 LLM，语义准确）
      let gist = ''
      try {
        const { extractFacts } = require('./fact-store.ts')
        const facts = extractFacts(original)
        if (facts.length > 0) {
          gist = facts.slice(0, 3).map((f: any) => `${f.subject}${f.predicate}${f.object}`).join('，')
        }
      } catch {}

      // 没有三元组 → 退化为关键词标签（承认有损，不叫"特征理解"）
      if (!gist) {
        gist = original.slice(0, 40) + '…'
      }

      mem.content = gist
      mem.tier = 'long_term'
      compressed++
    }
  }

  if (compressed > 0) {
    saveMemories()
    console.log(`[cc-soul][compress] compressed ${compressed} old memories`)
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// Decayed Memory Revival — rescue valuable memories from the graveyard
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Scan decayed memories for those still worth keeping:
 * - Has tags (was processed by CLI)
 * - confidence > 0.5
 * - scope was fact/preference/correction before decay
 * - Was recalled at least once
 * Revive up to 20 per cycle.
 */
let lastRevival = 0
const REVIVAL_COOLDOWN = 12 * 3600000 // twice per day

export function reviveDecayedMemories() {
  const now = Date.now()
  if (now - lastRevival < REVIVAL_COOLDOWN) return
  lastRevival = now

  const candidates = memoryState.memories.filter(m =>
    m.scope === 'decayed' &&
    m.tags && m.tags.length > 0 &&
    (m.confidence ?? 0) > 0.5 &&
    ((m.recallCount ?? 0) > 0 || m.emotion === 'important' || m.emotion === 'warm')
  )

  if (candidates.length === 0) return

  // Sort by value: recallCount + confidence + emotion importance
  candidates.sort((a, b) => {
    const scoreA = (a.recallCount ?? 0) * 2 + (a.confidence ?? 0) + (a.emotion === 'important' ? 1 : 0)
    const scoreB = (b.recallCount ?? 0) * 2 + (b.confidence ?? 0) + (b.emotion === 'important' ? 1 : 0)
    return scoreB - scoreA
  })

  let revived = 0
  for (const mem of candidates.slice(0, 20)) {
    mem.scope = 'fact' // restore to active scope
    mem.tier = 'mid_term' // put in mid-term (not short, to avoid immediate re-decay)
    mem.lastAccessed = now
    revived++
  }

  if (revived > 0) {
    rebuildScopeIndex()
    saveMemories()
    console.log(`[cc-soul][revival] revived ${revived} valuable decayed memories (from ${candidates.length} candidates)`)
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// DAG Archive — lossless memory compression (raw_line preserves original)
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Archive a memory: generate summary, store original in raw_line, set scope='archived'.
 * Preserves ts, tags, emotion and all metadata.
 */
function archiveMemory(mem: any) {
  // Store original full content in raw_line (used by official DB column)
  mem.raw_line = mem.content
  // Generate summary: first 50 chars + ellipsis
  const summary = mem.content.length > 50
    ? mem.content.slice(0, 50).trimEnd() + '...'
    : mem.content
  mem.content = summary
  mem.scope = 'archived'
  // Keep original tier for potential restoration
  if (!mem._originalTier) mem._originalTier = mem.tier || 'short_term'

  // Sync to SQLite if available
  if (useSQLite) {
    const row = sqliteFindByContent(mem.raw_line)
    if (row) {
      sqliteUpdateMemory(row.id, { scope: 'archived', content: summary })
      // Update raw_line directly via prepared statement
      sqliteUpdateRawLine(row.id, mem.raw_line)
    }
  }
}

/**
 * Restore archived memories matching a keyword.
 * Moves raw_line back to content, sets scope to 'mid_term'.
 * Returns count of restored memories.
 */
export function restoreArchivedMemories(keyword: string): number {
  // Use DB directly — memoryState may not have archived memories
  const _db = getDb()
  if (!_db) return 0
  const kw = `%${keyword}%`
  const rows = _db.prepare("SELECT id, content, raw_line FROM memories WHERE scope = 'archived' AND (raw_line LIKE ? OR content LIKE ?) LIMIT 10").all(kw, kw) as any[]
  let restored = 0
  for (const row of rows) {
    const newContent = row.raw_line || row.content
    _db.prepare("UPDATE memories SET content = ?, scope = 'mid_term', tier = 'mid_term', lastAccessed = ?, raw_line = '' WHERE id = ?").run(newContent, Date.now(), row.id)
    restored++
  }
  if (restored > 0) console.log(`[cc-soul][dag-archive] restored ${restored} memories matching "${keyword}"`)
  return restored
}

export function resolveNetworkConflicts() {
  const now = Date.now()
  const localFacts = memoryState.memories.filter(m =>
    !m.content.startsWith('[网络知识') &&
    (m.scope === 'fact' || m.scope === 'consolidated') &&
    m.scope !== 'expired'
  )
  const networkFacts = memoryState.memories.filter(m =>
    m.content.startsWith('[网络知识') && m.scope !== 'expired'
  )

  if (localFacts.length === 0 || networkFacts.length === 0) return

  let resolved = 0
  for (const net of networkFacts) {
    // Check if any local fact covers the same topic with different content
    const netWords = new Set(
      (net.content.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map(w => w.toLowerCase())
    )

    for (const local of localFacts) {
      const localWords = (local.content.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || [])
        .map(w => w.toLowerCase())
      const overlap = localWords.filter(w => netWords.has(w)).length

      // High topic overlap but different content → potential conflict
      // Local knowledge is more trusted (user verified), expire network version
      if (overlap >= 3 && local.content !== net.content.replace(/^\[网络知识[|｜][^\]]*\]\s*/, '')) {
        // Only expire if local is newer
        if (local.ts > net.ts) {
          net.scope = 'expired'
          resolved++
          break
        }
      }
    }
  }

  if (resolved > 0) {
    saveMemories()
    console.log(`[cc-soul][network-conflicts] resolved ${resolved} network vs local conflicts (local wins)`)
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// SQLite Maintenance — called from heartbeat
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Periodic SQLite maintenance: cleanup expired, backfill embeddings.
 * Safe to call frequently — internally rate-limited.
 */
export async function sqliteMaintenance() {
  if (!useSQLite) return
  sqliteCleanupExpired()
  // VACUUM：每天最多执行一次，防止 DB 文件膨胀
  try {
    const now = Date.now()
    if (now - _lastVacuumTs > 86400000) {  // 24 小时间隔
      const sqlMod = require('./sqlite-store.ts')
      if (sqlMod?.isSQLiteReady?.()) {
        // VACUUM 会重建数据库文件，回收被删除数据占用的空间
        let db: any = null
        try { db = require('./sqlite-store.ts').getDb?.() } catch {}
        if (db) {
          db.exec('VACUUM')
          _lastVacuumTs = now
          console.log('[cc-soul][sqlite] VACUUM completed')
        }
      }
    }
  } catch {}
}
let _lastVacuumTs = 0

/** Expose storage backend status for diagnostics */
export function getStorageStatus(): { backend: 'sqlite' | 'json'; vectorSearch: boolean } {
  return {
    backend: useSQLite ? 'sqlite' : 'json',
    vectorSearch: false,  // retired — activation field handles recall
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// #10 记忆卫生审计 — heartbeat 每天运行一次
// ═══════════════════════════════════════════════════════════════════════════════

const AUDIT_PATH = resolve(DATA_DIR, 'memory_audit.json')
let lastAuditTs = 0

export function auditMemoryHealth() {
  const now = Date.now()
  if (now - lastAuditTs < 86400000) return // 每天最多一次
  lastAuditTs = now

  const active = memoryState.memories.filter(m => m.scope !== 'expired' && m.scope !== 'decayed')

  // 1. 重复记忆（trigram similarity > 0.9）— 采样前 500 条避免 O(n^2) 爆炸
  const sample = active.slice(0, 500)
  const duplicates: { a: string; b: string; sim: number }[] = []
  for (let i = 0; i < sample.length && duplicates.length < 20; i++) {
    const tA = trigrams(sample[i].content)
    for (let j = i + 1; j < sample.length && duplicates.length < 20; j++) {
      const sim = trigramSimilarity(tA, trigrams(sample[j].content))
      if (sim > 0.9) duplicates.push({ a: sample[i].content.slice(0, 60), b: sample[j].content.slice(0, 60), sim: +sim.toFixed(2) })
    }
  }

  // 2. 极短记忆
  const tooShort = active.filter(m => m.content.length < 10).map(m => m.content)

  // 3. 无标签的活跃记忆
  const untagged = active.filter(m => !m.tags || m.tags.length === 0).length

  // 4. 低置信度记忆
  const lowConfidence = active.filter(m => (m.confidence ?? 0.7) < 0.3).length

  // 5. 僵尸记忆（从未被命中且存活超过30天）
  const thirtyDaysAgo = now - 30 * 86400000
  const zombie = active.filter(m => (m.recallCount ?? 0) === 0 && m.ts < thirtyDaysAgo).length

  // 6. 过期未清理（validUntil 已过但 scope 未标记 expired）
  const staleExpiry = active.filter(m => m.validUntil && m.validUntil < now).length

  // 7. 生成建议
  const parts: string[] = []
  if (duplicates.length > 0) parts.push(`建议合并 ${duplicates.length} 组重复记忆`)
  if (tooShort.length > 0) parts.push(`建议清理 ${tooShort.length} 条过短记忆`)
  if (untagged > active.length * 0.3) parts.push(`${untagged} 条记忆缺少标签，建议批量打标`)
  if (lowConfidence > 0) parts.push(`${lowConfidence} 条低置信度记忆（<0.3），建议清理`)
  if (zombie > 0) parts.push(`${zombie} 条僵尸记忆（30天零命中），建议淘汰`)
  if (staleExpiry > 0) parts.push(`${staleExpiry} 条记忆已过 validUntil 但未过期，建议清理`)

  const audit = { ts: now, duplicates, tooShort: tooShort.slice(0, 20), untagged, lowConfidence, zombie, staleExpiry, suggestions: parts.join('；') || '记忆状态良好' }
  debouncedSave(AUDIT_PATH, audit)
  console.log(`[cc-soul][memory-audit] duplicates=${duplicates.length} short=${tooShort.length} untagged=${untagged} lowConf=${lowConfidence} zombie=${zombie} staleExpiry=${staleExpiry}`)
}

// ═══════════════════════════════════════════════════════════════════════════════
// 因果推论框架：从"用户说X → AI回Y → 用户反应Z"推导因果链
// 原创算法——不只记录事件，还推导事件之间的因果关系
//
// 例：
// 用户说"部署出问题了" → AI说"检查日志" → 用户说"找到了，是配置错了"
// → 因果链：部署问题 → 检查日志 → 发现配置错误
//
// 记录这些链，下次类似问题直接推荐完整解决路径
// ═══════════════════════════════════════════════════════════════════════════════

interface CausalChain {
  trigger: string       // 触发事件（用户的问题）
  steps: string[]       // 解决步骤
  outcome: 'resolved' | 'unresolved' | 'unknown'
  confidence: number    // 0-1
  ts: number
  hitCount: number      // 被使用次数
}

const CAUSAL_PATH = resolve(DATA_DIR, 'causal_chains.json')
let causalChains: CausalChain[] = loadJson<CausalChain[]>(CAUSAL_PATH, [])
function saveCausalChains() { debouncedSave(CAUSAL_PATH, causalChains) }

/**
 * 从对话历史中提取因果链
 * 输入：最近 N 轮对话 [{user, ai, ts}]
 */
export function extractCausalChain(
  history: { user: string; ai: string; ts: number }[]
): CausalChain | null {
  if (history.length < 3) return null

  // 检测"问题→尝试→解决"模式
  const first = history[0]
  const last = history[history.length - 1]

  // 触发：第一条消息含问题信号
  const isProblem = /问题|报错|出错|不行|怎么办|bug|error|crash|失败|异常/.test(first.user)
  if (!isProblem) return null

  // 结果：最后一条消息含解决信号
  const isResolved = /解决|搞定|好了|找到|原来|明白了|谢谢|可以了/.test(last.user)
  const isUnresolved = /还是不行|放弃|算了|不管了/.test(last.user)

  if (!isResolved && !isUnresolved) return null

  // 提取步骤：中间的 AI 回复作为步骤
  const steps = history.slice(0, -1).map(h => {
    // 提取 AI 回复中的关键动作
    const actions = h.ai.match(/(?:检查|试试|确认|查看|运行|执行|修改|更新|重启|清除|添加|删除).{2,20}/g)
    return actions ? actions[0] : h.ai.slice(0, 30)
  }).filter(Boolean)

  if (steps.length === 0) return null

  const chain: CausalChain = {
    trigger: first.user.slice(0, 60),
    steps,
    outcome: isResolved ? 'resolved' : 'unresolved',
    confidence: isResolved ? 0.7 : 0.3,
    ts: Date.now(),
    hitCount: 0,
  }

  // 去重：如果已有类似 trigger 的链，更新而非新增
  const existing = causalChains.find(c => {
    const cWords = new Set((c.trigger.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map(w => w.toLowerCase()))
    const newWords = (chain.trigger.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map(w => w.toLowerCase())
    const overlap = newWords.filter(w => cWords.has(w)).length
    return overlap >= 2
  })

  if (existing) {
    // 更新已有链
    if (chain.outcome === 'resolved') {
      existing.steps = chain.steps  // 用最新的解决步骤
      existing.outcome = 'resolved'
      existing.confidence = Math.min(0.95, existing.confidence + 0.1)
      existing.ts = Date.now()
    }
    saveCausalChains()
    return null  // 已更新，不返回新链
  }

  // 新增
  causalChains.push(chain)
  if (causalChains.length > 50) {
    // 淘汰最旧的未使用链
    causalChains.sort((a, b) => (b.hitCount * 10 + b.ts / 1e10) - (a.hitCount * 10 + a.ts / 1e10))
    causalChains = causalChains.slice(0, 50)
  }
  saveCausalChains()
  console.log(`[cc-soul][causal] new chain: "${chain.trigger.slice(0, 30)}" → ${chain.steps.length} steps → ${chain.outcome}`)
  return chain
}

/**
 * 查询因果链：给定一个问题，找到之前解决过的类似问题的步骤
 */
export function queryCausalChain(problem: string): CausalChain | null {
  const problemWords = new Set((problem.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map(w => w.toLowerCase()))
  if (problemWords.size === 0) return null

  let bestChain: CausalChain | null = null
  let bestScore = 0

  for (const chain of causalChains) {
    if (chain.outcome !== 'resolved') continue
    const chainWords = (chain.trigger.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map(w => w.toLowerCase())
    const overlap = chainWords.filter(w => problemWords.has(w)).length
    const score = overlap / Math.max(1, problemWords.size) * chain.confidence
    if (score > bestScore && score > 0.3) {
      bestScore = score
      bestChain = chain
    }
  }

  if (bestChain) {
    bestChain.hitCount++
    saveCausalChains()
  }
  return bestChain
}

export function getCausalChainCount(): number { return causalChains.filter(c => c.outcome === 'resolved').length }
