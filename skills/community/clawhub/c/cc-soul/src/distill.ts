/**
 * distill.ts — Three-layer memory distillation pipeline
 *
 * Layer 3: User mental model (~200 chars per user, always injected)
 * Layer 2: Topic graph nodes (~50 nodes, retrieved by topic)
 * Layer 1: Raw memories (thousands, rarely accessed directly)
 *
 * Triggered from heartbeat. Each layer has its own cadence:
 *   Layer 1 → 2: every 6 hours (cluster raw memories into topic nodes)
 *   Layer 2 → 3: every 12 hours (distill topics into user mental model)
 *   Layer 3 refresh: every 24 hours (full re-synthesis from all layers)
 */

import { resolve } from 'path'
import { DATA_DIR, loadJson, saveJson, debouncedSave, adaptiveCooldown } from './persistence.ts'
import { memoryState, addMemory, buildCoreMemoryContext } from './memory.ts'
import { spawnCLI } from './cli.ts'
import type { Memory } from './types.ts'
import { logDecision } from './decision-log.ts'
import { WORD_PATTERN } from './memory-utils.ts'
import { detectPolarityFlip } from './memory-utils.ts'

// ═══════════════════════════════════════════════════════════════════════════════
// PATHS & CONSTANTS
// ═══════════════════════════════════════════════════════════════════════════════

// Legacy JSON paths (kept for migration, not for primary storage)
const MENTAL_MODELS_PATH = resolve(DATA_DIR, 'mental_models.json')
const TOPIC_NODES_PATH = resolve(DATA_DIR, 'topic_nodes.json')
const DISTILL_STATE_PATH = resolve(DATA_DIR, 'distill_state.json')

const L1_TO_L2_BASE = 6 * 3600000    // 6 hours
const L2_TO_L3_BASE = 12 * 3600000   // 12 hours
const L3_REFRESH_BASE = 24 * 3600000 // 24 hours
// Adaptive cooldowns (scale by user activity when userId available)
const L1_TO_L2_COOLDOWN = L1_TO_L2_BASE   // used in global context (no userId)
const L2_TO_L3_COOLDOWN = L2_TO_L3_BASE
const L3_REFRESH_COOLDOWN = L3_REFRESH_BASE
const MIN_MEMORIES_FOR_DISTILL = 20       // don't distill if too few
const MAX_TOPIC_NODES = 80
const MAX_MODEL_LENGTH = 600              // chars per user mental model

// ═══════════════════════════════════════════════════════════════════════════════
// TYPES
// ═══════════════════════════════════════════════════════════════════════════════

interface TopicNode {
  topic: string            // e.g. "iOS逆向", "芒果偏好", "Python项目部署"
  summary: string          // distilled understanding
  sourceCount: number      // how many raw memories contributed
  lastUpdated: number
  userId?: string          // per-user or global
  // ── 蒸馏淘汰赛字段（P0b）──
  hitCount?: number        // 被 getRelevantTopics() 命中且注入 prompt 的次数
  missCount?: number       // 相关话题出现但该 node 未被命中的次数
  lastHitTs?: number       // 上次命中时间
  stale?: boolean          // 标记为需要重蒸馏
  confidence?: number      // 置信度 [0.1, 0.95]
}

interface MentalModel {
  userId: string
  model: string            // natural language: "这个人是..."（兼容旧数据）
  topics: string[]         // top topic references
  lastUpdated: number
  version: number
  // ── P1c: 分区增量更新 ──
  sections?: {
    identity: string       // 身份/职业/技术栈（cooldown 7天）
    style: string          // 沟通风格/偏好/雷区（cooldown 3天）
    facts: string          // 稳定偏好/习惯/家庭/关键事实（cooldown 1天）
    dynamics: string       // 近期状态：情绪基线、当前关注话题、行为变化（cooldown 3小时）
  }
  sectionUpdated?: {
    identity: number
    style: number
    facts: number
    dynamics: number
  }
}

interface DistillState {
  lastL1toL2: number
  lastL2toL3: number
  lastL3Refresh: number
  totalDistills: number
  // P2c: 溢出队列持久化
  pendingDecayDistill?: Array<{ contents: string[]; clusteredAt: number }>
  // PMI orphan tracking
  orphanMemoryContents?: string[]
  orphanAccumulatedAt?: number
}

// ═══════════════════════════════════════════════════════════════════════════════
// STATE
// ═══════════════════════════════════════════════════════════════════════════════

let topicNodes: TopicNode[] = []
let mentalModels = new Map<string, MentalModel>()
let distillState: DistillState = { lastL1toL2: 0, lastL2toL3: 0, lastL3Refresh: 0, totalDistills: 0 }

// ═══════════════════════════════════════════════════════════════════════════════
// LOAD / SAVE
// ═══════════════════════════════════════════════════════════════════════════════

export function loadDistillState() {
  // 优先从 SQLite 加载，fallback 到 JSON
  let sqlMod: any = null
  try { sqlMod = require('./sqlite-store.ts') } catch {}

  if (sqlMod?.dbLoadTopicNodes) {
    const dbNodes = sqlMod.dbLoadTopicNodes()
    if (dbNodes.length > 0) {
      topicNodes = dbNodes
    } else {
      // JSON fallback + 迁移
      topicNodes = loadJson<TopicNode[]>(TOPIC_NODES_PATH, [])
      for (const n of topicNodes) { try { sqlMod.dbSaveTopicNode(n) } catch {} }
    }
  } else {
    topicNodes = loadJson<TopicNode[]>(TOPIC_NODES_PATH, [])
  }

  if (sqlMod?.dbLoadDistillState) {
    distillState = sqlMod.dbLoadDistillState(distillState)
  } else {
    distillState = loadJson<DistillState>(DISTILL_STATE_PATH, distillState)
  }

  if (sqlMod?.dbLoadMentalModels) {
    const dbModels = sqlMod.dbLoadMentalModels()
    if (dbModels.size > 0) {
      mentalModels = dbModels
    } else {
      // JSON fallback + 迁移
      const raw = loadJson<Record<string, MentalModel>>(MENTAL_MODELS_PATH, {})
      mentalModels.clear()
      for (const [id, m] of Object.entries(raw)) {
        mentalModels.set(id, m)
        try { sqlMod.dbSaveMentalModel(m) } catch {}
      }
    }
  } else {
    const raw = loadJson<Record<string, MentalModel>>(MENTAL_MODELS_PATH, {})
    mentalModels.clear()
    for (const [id, m] of Object.entries(raw)) {
      mentalModels.set(id, m)
    }
  }

  console.log(`[cc-soul][distill] loaded: ${topicNodes.length} topics, ${mentalModels.size} mental models`)
}

function saveTopicNodes() {
  let sqlMod: any = null
  try { sqlMod = require('./sqlite-store.ts') } catch {}
  if (sqlMod?.dbSaveTopicNode) {
    for (const n of topicNodes) { try { sqlMod.dbSaveTopicNode(n) } catch {} }
  }
  // JSON 双写已移除——SQLite 是唯一数据源
}

function saveMentalModels() {
  let sqlMod: any = null
  try { sqlMod = require('./sqlite-store.ts') } catch {}
  if (sqlMod?.dbSaveMentalModel) {
    for (const [_, m] of mentalModels) { try { sqlMod.dbSaveMentalModel(m) } catch {} }
  }
  // JSON 双写已移除——SQLite 是唯一数据源
}

function saveDistillState_() {
  let sqlMod: any = null
  try { sqlMod = require('./sqlite-store.ts') } catch {}
  if (sqlMod?.dbSaveDistillState) {
    try { sqlMod.dbSaveDistillState(distillState) } catch {}
  }
  // JSON 双写已移除——SQLite 是唯一数据源
}

// ═══════════════════════════════════════════════════════════════════════════════
// LAYER 1 → LAYER 2: Raw memories → Topic nodes
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Cluster raw memories by topic similarity, then distill each cluster
 * into a topic node summary.
 */
export function distillL1toL2() {
  const now = Date.now()
  if (now - distillState.lastL1toL2 < L1_TO_L2_COOLDOWN) return

  // ── 会话门（学自 Claude Code Auto Dream）：至少 3 个有效会话后才允许蒸馏 ──
  // 防止用户不活跃时浪费 LLM 调用
  const MIN_SESSIONS_FOR_DISTILL = 3
  try {
    const { getSessionState, getLastActiveSessionKey } = require('./handler-state.ts')
    const sess = getSessionState(getLastActiveSessionKey())
    const sessionCount = sess?.sessionCount ?? sess?.turnCount ?? 0
    if (sessionCount < MIN_SESSIONS_FOR_DISTILL) return
  } catch {}

  distillState.lastL1toL2 = now

  // Get active, non-expired memories
  const active = memoryState.memories.filter(m =>
    m.scope !== 'expired' && m.scope !== 'archived' && m.scope !== 'decayed' &&
    m.content.length > 10
  )
  if (active.length < MIN_MEMORIES_FOR_DISTILL) return

  // Group by userId (or 'global' for no userId)
  const byUser = new Map<string, Memory[]>()
  for (const m of active) {
    const key = m.userId || '_global'
    if (!byUser.has(key)) byUser.set(key, [])
    byUser.get(key)!.push(m)
  }

  // For each user group, cluster by topic
  // Limit total CLI calls to avoid queue overflow (CLI queue max = 10)
  let cliCallsThisRound = 0
  const MAX_CLI_PER_DISTILL = 8
  // Track unclustered memories per user for PMI assignment pass
  const unclusteredByUser = new Map<string, Memory[]>()

  for (const [userId, memories] of byUser) {
    if (memories.length < 5) continue
    if (cliCallsThisRound >= MAX_CLI_PER_DISTILL) break

    // Simple topic clustering: group by scope + keyword overlap
    const clusters = clusterByKeywords(memories)

    // Collect unclustered memories for PMI pass
    const clusteredSet = new Set<string>()
    for (const cl of clusters) { if (cl.length >= 2) for (const m of cl) clusteredSet.add(m.content) }
    const unc = memories.filter(m => !clusteredSet.has(m.content))
    if (unc.length > 0) unclusteredByUser.set(userId, unc)

    // Emotion-weighted L2 promotion: sort clusters so emotionally significant ones get priority
    clusters.sort((a, b) => {
      const emotionScore = (cluster: Memory[]) => cluster.reduce((sum, m) => {
        const w = (m.emotion === 'important' || m.emotion === 'warm') ? 1.5
          : m.emotion === 'painful' ? 1.3 : 1.0
        return sum + w
      }, 0)
      return emotionScore(b) - emotionScore(a)
    })

    for (const cluster of clusters) {
      if (cluster.length < 2) continue
      if (cliCallsThisRound >= MAX_CLI_PER_DISTILL) break

      // Check if we already have a topic node for this cluster
      const clusterText = cluster.map(m => m.content.slice(0, 80)).join('\n')
      const existingNode = topicNodes.find(n =>
        n.userId === (userId === '_global' ? undefined : userId) &&
        keywordOverlap(n.topic, clusterText) > 0.3
      )

      if (existingNode && now - existingNode.lastUpdated < L1_TO_L2_COOLDOWN) continue

      // 优先用零 LLM 蒸馏（省 token）
      const zeroLLMResult = zeroLLMDistill(cluster.map(m => m.content))
      if (zeroLLMResult && zeroLLMResult.length > 10) {
        // 零 LLM 蒸馏成功，不调 LLM
        // 从第一条记忆提取主题名
        const topicName = cluster[0].content.slice(0, 10).replace(/[，。！？\s]+$/, '') || '未分类'
        const node: TopicNode = {
          topic: topicName.slice(0, 20),
          summary: zeroLLMResult.slice(0, 200),
          sourceCount: cluster.length,
          lastUpdated: Date.now(),
          userId: userId === '_global' ? undefined : userId,
        }
        if (existingNode) {
          existingNode.topic = node.topic
          existingNode.summary = node.summary
          existingNode.sourceCount += cluster.length
          existingNode.lastUpdated = node.lastUpdated
        } else {
          topicNodes.push(node)
          if (topicNodes.length > MAX_TOPIC_NODES) {
            topicNodes.sort((a, b) => b.lastUpdated - a.lastUpdated)
            topicNodes.length = MAX_TOPIC_NODES
          }
        }
        saveTopicNodes()
        console.log(`[cc-soul][distill] L1→L2 (zero-LLM): "${node.topic}" (${cluster.length} memories → 1 node)`)
        continue  // 跳过 LLM 蒸馏
      }

      // fallback: LLM 蒸馏（只在零 LLM 结果太短时）
      const prompt = [
        '将以下记忆片段蒸馏为一个主题节点。格式：',
        '主题: <2-6字的主题名>',
        '摘要: <1-2句话的核心理解，不超过100字>',
        '',
        '记忆片段:',
        ...cluster.slice(0, 15).map(m => `- ${m.content.slice(0, 120)}`),
      ].join('\n')

      cliCallsThisRound++
      spawnCLI(prompt, (output) => {
        if (!output || output.length < 10) return
        const topicMatch = output.match(/主题[:：]\s*(.+?)(?:\n|$)/)
        const summaryMatch = output.match(/摘要[:：]\s*(.+?)(?:\n|$)/)
        if (!topicMatch || !summaryMatch) return

        const node: TopicNode = {
          topic: topicMatch[1].trim().slice(0, 20),
          summary: summaryMatch[1].trim().slice(0, 200),
          sourceCount: cluster.length,
          lastUpdated: Date.now(),
          userId: userId === '_global' ? undefined : userId,
        }

        if (existingNode) {
          // Update existing
          existingNode.topic = node.topic
          existingNode.summary = node.summary
          existingNode.sourceCount += cluster.length
          existingNode.lastUpdated = node.lastUpdated
        } else {
          topicNodes.push(node)
          // Cap total nodes
          if (topicNodes.length > MAX_TOPIC_NODES) {
            topicNodes.sort((a, b) => b.lastUpdated - a.lastUpdated)
            topicNodes.length = MAX_TOPIC_NODES
          }
        }
        saveTopicNodes()
        console.log(`[cc-soul][distill] L1→L2: "${node.topic}" (${cluster.length} memories → 1 node)`)
      })
    }
  }

  // ── PMI-based incremental assignment for unclustered memories ──
  for (const [userId, unclustered] of unclusteredByUser) {
    const uid = userId === '_global' ? undefined : userId
    const orphans = distillState.orphanMemoryContents ??= []

    for (const m of unclustered) {
      const matched = assignMemoryToNode(m.content, topicNodes, uid)
      if (matched) {
        // Increment source count — memory is now represented by this node
        matched.sourceCount++
        matched.lastUpdated = now
      } else {
        // Orphan — no existing node matches
        if (!orphans.includes(m.content.slice(0, 200))) {
          orphans.push(m.content.slice(0, 200))
          distillState.orphanAccumulatedAt ??= now
        }
      }
    }

    // Orphan graduation: cluster orphans when enough accumulate
    if (orphans.length >= 5) {
      const PMI_THRESHOLD = 0.5
      const viable = clusterOrphansByPMI(orphans, PMI_THRESHOLD)

      for (const oc of viable) {
        const topicName = oc[0].slice(0, 10).replace(/[，。！？\s]+$/, '') || '未分类'
        const summary = zeroLLMDistill(oc) || oc.map(s => s.slice(0, 40)).join('；')
        topicNodes.push({
          topic: topicName.slice(0, 20),
          summary: summary.slice(0, 200),
          sourceCount: oc.length,
          lastUpdated: now,
          userId: uid,
        })
        // Remove graduated orphans
        for (const content of oc) {
          const idx = orphans.indexOf(content)
          if (idx >= 0) orphans.splice(idx, 1)
        }
      }

      // Force group by 24h time window if orphans pile up with no viable cluster
      if (orphans.length >= 20) {
        const topicName = '杂项话题'
        const summary = zeroLLMDistill(orphans.slice(0, 15)) || orphans.slice(0, 5).map(s => s.slice(0, 30)).join('；')
        topicNodes.push({
          topic: topicName,
          summary: summary.slice(0, 200),
          sourceCount: orphans.length,
          lastUpdated: now,
          userId: uid,
        })
        orphans.length = 0
        distillState.orphanAccumulatedAt = undefined
        console.log(`[cc-soul][distill] PMI orphans force-grouped into fallback node`)
      }

      // Cap total nodes
      if (topicNodes.length > MAX_TOPIC_NODES) {
        topicNodes.sort((a, b) => b.lastUpdated - a.lastUpdated)
        topicNodes.length = MAX_TOPIC_NODES
      }
      saveTopicNodes()
    }
  }

  distillState.totalDistills++
  saveDistillState_()
}

// ═══════════════════════════════════════════════════════════════════════════════
// LAYER 2 → LAYER 3: Topic nodes → Mental model
// ═══════════════════════════════════════════════════════════════════════════════

// ── P1c: L3 分区 cooldown ──
const SECTION_COOLDOWNS: Record<string, number> = {
  identity: 7 * 86400000,     // 7 天
  style: 3 * 86400000,        // 3 天
  facts: 86400000,            // 1 天
  dynamics: 3 * 3600000,      // 3 小时
}

const SECTION_PROMPTS: Record<string, { name: string; desc: string }> = {
  identity: { name: '身份', desc: '身份、职业、技术栈、专业背景' },
  style: { name: '沟通风格', desc: '沟通偏好、说话风格、雷区、喜好' },
  facts: { name: '关键事实', desc: '稳定偏好、习惯、家庭情况、长期目标' },
  dynamics: { name: '近期状态', desc: '当前情绪基线、正在关注的话题/项目、近期行为变化' },
}

// dynamics 分区的衰减：14 天未更新的内容应被清除
const DYNAMICS_STALE_THRESHOLD = 14 * 86400000

/**
 * P1c: 分区增量更新 — 每个分区独立 cooldown + 变更检测
 * 只更新有变化的分区，其他分区保持不变
 */
export function distillL2toL3() {
  const now = Date.now()
  // 不再用全局 cooldown 挡住所有 section — 每个 section 有独立 cooldown
  // 只记录上次尝试时间用于 stats，不做 early return
  distillState.lastL2toL3 = now

  const userIds = new Set<string>()
  for (const n of topicNodes) {
    if (n.userId) userIds.add(n.userId)
  }
  for (const m of memoryState.memories) {
    if (m.userId && m.scope !== 'expired') userIds.add(m.userId)
  }
  userIds.add('_global')

  let cliCalls = 0
  const MAX_CLI_L3 = 4  // 每轮最多 4 个 section LLM 调用

  for (const userId of userIds) {
    if (cliCalls >= MAX_CLI_L3) break
    const isGlobal = userId === '_global'

    const userTopics = topicNodes.filter(n => isGlobal ? !n.userId : n.userId === userId)
    const userMems = memoryState.memories.filter(m =>
      (isGlobal ? !m.userId : m.userId === userId) &&
      m.scope !== 'expired' && m.scope !== 'archived' &&
      (m.scope === 'preference' || m.scope === 'correction' || m.scope === 'fact' || m.scope === 'consolidated')
    ).slice(-20)

    if (userTopics.length === 0 && userMems.length < 3) continue

    const existing = mentalModels.get(userId)

    // 如果旧模型没有 sections，先从 model 字段做一次性迁移
    if (existing && !existing.sections) {
      existing.sections = {
        identity: existing.model.slice(0, 150),
        style: '',
        facts: '',
        dynamics: '',
      }
      existing.sectionUpdated = {
        identity: 0, style: 0, facts: 0, dynamics: 0,
      }
    }

    const sections = existing?.sections ?? { identity: '', style: '', facts: '', dynamics: '' }
    const sectionUpdated = existing?.sectionUpdated ?? { identity: 0, style: 0, facts: 0, dynamics: 0 }

    // dynamics 衰减：14 天未更新则清空
    if (sections.dynamics && now - sectionUpdated.dynamics > DYNAMICS_STALE_THRESHOLD) {
      sections.dynamics = ''
    }

    // ── 紧急刷新触发器：检测重大变更信号，跳过 cooldown ──
    // 审核结论：identity 7天太慢，用户说"换工作了"应该立即刷新
    const URGENT_TRIGGERS: Record<string, RegExp> = {
      identity: /换工作|辞职|转行|改名|毕业|入职|退休|创业/,
      facts: /搬家|搬到|分手|结婚|生了|买了房|换了手机/,
      style: /以后.*别|不要再|换个方式|太啰嗦|说重点/,
    }
    const recentMsgs = memoryState.chatHistory.slice(-5).map(h => h.user).join(' ')
    const urgentSections = new Set<string>()
    for (const [sec, re] of Object.entries(URGENT_TRIGGERS)) {
      if (re.test(recentMsgs)) urgentSections.add(sec)
    }

    for (const sectionKey of ['identity', 'style', 'facts', 'dynamics'] as const) {
      if (cliCalls >= MAX_CLI_L3) break

      // cooldown 检查（紧急触发时跳过）
      const cooldown = SECTION_COOLDOWNS[sectionKey]
      const isUrgent = urgentSections.has(sectionKey)
      if (!isUrgent && now - sectionUpdated[sectionKey] < cooldown) continue
      if (isUrgent) {
        try { require('./decision-log.ts').logDecision('urgent_refresh', sectionKey, `trigger matched in recent msgs`) } catch {}
      }

      // 构建 section 专用 prompt
      const sectionInfo = SECTION_PROMPTS[sectionKey]
      const currentContent = sections[sectionKey] || '（空）'

      // 收集该 section 相关的证据
      const evidence: string[] = []
      for (const t of userTopics.slice(0, 10)) {
        evidence.push(`[${t.topic}] ${t.summary}`)
      }
      for (const m of userMems.slice(-10)) {
        evidence.push(`[${m.scope}] ${m.content.slice(0, 80)}`)
      }
      if (evidence.length === 0) continue

      const prompt = [
        `当前对用户「${sectionInfo.name}」的理解：`,
        '---',
        currentContent,
        '---',
        '',
        '新的证据：',
        ...evidence.map(e => `- ${e}`),
        '',
        '请基于新证据更新上面的理解。规则：',
        '1. 保留仍然成立的旧内容',
        '2. 用新证据修正或补充',
        '3. 如果证据与旧内容矛盾，以新证据为准并标注变化',
        `4. 范围限定：只写${sectionInfo.desc}相关的内容`,
        '5. 不超过 150 字',
        '6. 只输出更新后的内容，不要元说明',
      ].join('\n')

      cliCalls++
      spawnCLI(prompt, (output) => {
        if (!output || output.length < 10) return

        const newContent = output.slice(0, 150)

        // 变更检测：如果新旧内容几乎相同则跳过
        if (currentContent !== '（空）' && currentContent.length > 0) {
          const oldWords = new Set((currentContent.match(WORD_PATTERN.CJK2_EN3) || []).map(w => w.toLowerCase()))
          const newWords = new Set((newContent.match(WORD_PATTERN.CJK2_EN3) || []).map(w => w.toLowerCase()))
          let overlap = 0
          for (const w of oldWords) { if (newWords.has(w)) overlap++ }
          const sim = overlap / Math.max(1, Math.max(oldWords.size, newWords.size))
          if (sim > 0.92) {
            // LLM 照抄 → 跳过更新
            sectionUpdated[sectionKey] = now
            return
          }
        }

        // ── Retention Loss Guard（论文借鉴）：防止人设突变 ──
        // 按 section 独立检查。sim < 0.5 说明变化太大，保守融合而非直接替换
        if (currentContent !== '（空）' && currentContent.length > 10) {
          const { trigrams: _tri, trigramSimilarity: _triSim } = require('./memory-utils.ts')
          const retentionSim = _triSim(_tri(currentContent), _tri(newContent))
          if (retentionSim < 0.5) {
            sections[sectionKey] = `${currentContent}\n[近期补充] ${newContent}`.slice(0, 150)
            try { require('./decision-log.ts').logDecision('retention_guard', sectionKey, `sim=${retentionSim.toFixed(2)}<0.5, merged`) } catch {}
            sectionUpdated[sectionKey] = now
            return  // 不走正常替换路径
          }
        }

        // ── Entity Coverage Guard：防止实体丢失 ──
        {
          let _findEnts: ((msg: string) => string[]) | null = null
          try { _findEnts = require('./graph.ts').findMentionedEntities } catch {}
          if (_findEnts) {
            const oldEnts = new Set(_findEnts(currentContent))
            const newEnts = new Set(_findEnts(newContent))
            if (oldEnts.size > 2) {
              let lost = 0
              for (const e of oldEnts) { if (!newEnts.has(e)) lost++ }
              if (lost / oldEnts.size > 0.3) {
                try { require('./decision-log.ts').logDecision('distill_shield', sectionKey, `lost ${lost}/${oldEnts.size} entities, rejected`) } catch {}
                sectionUpdated[sectionKey] = now
                return  // Don't replace — too many entities lost
              }
            }
          }
        }

        sections[sectionKey] = newContent
        sectionUpdated[sectionKey] = now

        // 同步 model 字段（向后兼容）
        const model: MentalModel = {
          userId,
          model: [sections.identity, sections.style, sections.facts, sections.dynamics]
            .filter(Boolean).join('\n').slice(0, MAX_MODEL_LENGTH),
          sections,
          sectionUpdated,
          topics: userTopics.slice(0, 10).map(n => n.topic),
          lastUpdated: now,
          version: (existing?.version ?? 0) + 1,
        }
        mentalModels.set(userId, model)
        saveMentalModels()
        console.log(`[cc-soul][distill] L2→L3: ${isGlobal ? 'global' : userId.slice(0, 8)} section=${sectionKey} v${model.version}`)
      }, 60000)
    }
  }

  saveDistillState_()
}

// ═══════════════════════════════════════════════════════════════════════════════
// PUBLIC API — for prompt injection and augments
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Get the mental model for a user. Falls back to global model.
 * This is what gets injected into SOUL.md / bootstrap.
 */
export function getMentalModel(userId?: string): string {
  if (userId) {
    const m = mentalModels.get(userId)
    if (m) return m.model
  }
  const g = mentalModels.get('_global')
  return g?.model ?? ''
}

/**
 * Get topic nodes relevant to a message (for Layer 2 augment).
 * 同时记录 hitCount/missCount 用于蒸馏淘汰赛。
 */
export function getRelevantTopics(msg: string, userId?: string, maxNodes = 5): TopicNode[] {
  if (topicNodes.length === 0) return []

  const RELEVANCE_THRESHOLD = 0.2
  const scored: { node: TopicNode; score: number }[] = []

  for (const node of topicNodes) {
    // Filter by user if specified
    if (userId && node.userId && node.userId !== userId) continue

    const overlap = keywordOverlap(msg, `${node.topic} ${node.summary}`)
    if (overlap > 0.1) {
      scored.push({ node, score: overlap })
    }
  }

  scored.sort((a, b) => b.score - a.score)

  // ── 淘汰赛：记录命中/未命中 ──
  const hits = scored.filter(s => s.score >= RELEVANCE_THRESHOLD)
  for (const h of hits) {
    h.node.hitCount = (h.node.hitCount ?? 0) + 1
    h.node.lastHitTs = Date.now()
  }

  // 未命中但话题相关（有实体重叠）的 → missCount++
  // P5 fix: 确保 miss 正确记录。scored 里 0.1 < score < 0.2 的是"话题相关但不够精确"
  const misses = scored.filter(s =>
    s.score > 0.1 && s.score < RELEVANCE_THRESHOLD && !hits.includes(s)
  )
  for (const m of misses) {
    m.node.missCount = (m.node.missCount ?? 0) + 1
  }
  // 诊断：如果 topicNodes 不为空但 scored 为空，说明查询跟所有话题都无关——这不算 miss
  if (topicNodes.length > 0 && scored.length === 0) {
    // 但如果消息有明确话题词（>4字非问句），所有节点都该计一次 miss
    if (msg.length > 4 && !/^[？?]/.test(msg)) {
      // 对最近活跃的 top-3 节点计 miss（它们应该但没有被覆盖到）
      const recentNodes = [...topicNodes]
        .sort((a, b) => (b.lastUpdated || 0) - (a.lastUpdated || 0))
        .slice(0, 3)
      for (const node of recentNodes) {
        node.missCount = (node.missCount ?? 0) + 1
      }
      if (recentNodes.length > 0) saveTopicNodes()
    }
  }

  if (hits.length > 0 || misses.length > 0) {
    saveTopicNodes()
  }

  return hits.slice(0, maxNodes).map(s => s.node)
}

/**
 * 蒸馏淘汰赛审计：标记 stale nodes，触发重蒸馏，晋升优秀节点
 * 从 heartbeat 的 runDistillPipeline() 调用
 */
export function auditTopicNodes(): { staleCount: number; promoted: number; orphanMemories: number } {
  const now = Date.now()
  let staleCount = 0
  let promoted = 0

  for (const node of topicNodes) {
    const total = (node.hitCount ?? 0) + (node.missCount ?? 0)
    const ratio = total > 0 ? (node.hitCount ?? 0) / total : 0
    const ageDays = (now - node.lastUpdated) / 86400000

    // stale 判定：ratio < 0.2 且 age > 7天 且 total >= 3
    if (ratio < 0.2 && ageDays > 7 && total >= 3) {
      node.stale = true
      staleCount++
      logDecision('stale_topic', node.topic,
        `ratio=${ratio.toFixed(2)}, age=${ageDays.toFixed(0)}d, hits=${node.hitCount ?? 0}/${total}`)
    }

    // 晋升判定：hitCount > 10 且 ratio > 0.6 → 提升为 core memory
    if ((node.hitCount ?? 0) > 10 && ratio > 0.6) {
      try {
        addMemory(
          `[蒸馏晋升] ${node.topic}: ${node.summary}`,
          'consolidated',
          node.userId,
          'global'
        )
        promoted++
        logDecision('promote_topic', node.topic,
          `ratio=${ratio.toFixed(2)}, hits=${node.hitCount}`)
      } catch {}
    }
  }

  // orphan memories：找不到匹配 topic node 的新记忆
  const recentMemories = memoryState.memories.filter(m =>
    m.scope !== 'expired' && m.scope !== 'archived' &&
    Date.now() - m.ts < 7 * 86400000 &&  // 最近 7 天
    m.content.length > 10
  )
  let orphanMemories = 0
  for (const m of recentMemories) {
    const hasMatch = topicNodes.some(n => {
      if (m.userId && n.userId && n.userId !== m.userId) return false
      return keywordOverlap(m.content, `${n.topic} ${n.summary}`) > 0.2
    })
    if (!hasMatch) orphanMemories++
  }

  // 触发重蒸馏条件
  const staleRatio = topicNodes.length > 0 ? staleCount / topicNodes.length : 0
  if (staleRatio > 0.3 || orphanMemories >= 5) {
    // 重置 stale nodes 的 lastUpdated 使其在下次 L1→L2 时被重新处理
    for (const node of topicNodes) {
      if (node.stale) {
        node.lastUpdated = 0
        node.stale = false  // 清除标记，等待重蒸馏
      }
    }
    saveTopicNodes()
    console.log(`[cc-soul][distill] audit triggered re-distill: staleRatio=${staleRatio.toFixed(2)}, orphans=${orphanMemories}`)
  }

  return { staleCount, promoted, orphanMemories }
}

/**
 * Build Layer 2 augment: topic context relevant to current message.
 */
export function buildTopicAugment(msg: string, userId?: string): string {
  const relevant = getRelevantTopics(msg, userId)
  if (relevant.length === 0) return ''
  const lines = relevant.map(n => `- [${n.topic}] ${n.summary}`)
  return `[主题记忆] 相关主题理解:\n${lines.join('\n')}`
}

/**
 * Build Layer 3 augment: user mental model for bootstrap/SOUL.md.
 */
export function buildMentalModelAugment(userId?: string): string {
  const model = getMentalModel(userId)
  if (!model) return ''
  return `[用户心智模型]\n${model}`
}

/**
 * Run the full distillation pipeline (called from heartbeat).
 */
export function runDistillPipeline() {
  // ── P6f: 消费 pending_distill 队列（遗忘即蒸馏的溢出）──
  try {
    const sqlMod = require('./sqlite-store.ts')
    if (sqlMod?.dbPopPendingDistill) {
      const pending = sqlMod.dbPopPendingDistill(3)
      for (const p of pending) {
        if (p.contents.length >= 2) {
          const result = zeroLLMDistill(p.contents)
          if (result && result.length > 10) {
            const node: TopicNode = {
              topic: result.slice(0, 20),
              summary: result.slice(0, 200),
              sourceCount: p.contents.length,
              lastUpdated: Date.now(),
              hitCount: 0, missCount: 0,
            }
            topicNodes.push(node)
            saveTopicNodes()
            console.log(`[cc-soul][distill] pending decay distill: "${node.topic}"`)
          }
        }
      }
    }
  } catch {}

  // ── 蒸馏淘汰赛审计（先审计再蒸馏，确保 stale nodes 被重置）──
  auditTopicNodes()

  distillL1toL2()
  // L2→L3：每个 section 有独立 cooldown，不需要全局频率限制
  distillL2toL3()
}

/**
 * Get distill stats for diagnostics.
 */
export function getDistillStats() {
  return {
    topicNodes: topicNodes.length,
    mentalModels: mentalModels.size,
    ...distillState,
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// ZERO-LLM DISTILL — 零 LLM 蒸馏：用规则提取特征替代 LLM 摘要
// 省 100% 的蒸馏 token，速度快 10x
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * 结构蒸馏 v2（零 LLM）— 利用 graph + fact-store + AAM 做结构化蒸馏
 * 不再输出 "关键词: X | 特征: Y" 格式，而是输出实体关系 + 行为模式 + 变化轨迹
 *
 * cc-soul 原创核心算法 — P1b
 */
export function zeroLLMDistill(memories: string[]): string {
  const parts: string[] = []

  // ── 第一层：fact-store 结构化三元组提取 ──
  let extractFacts: ((c: string) => any[]) | null = null
  try { extractFacts = require('./fact-store.ts').extractFacts } catch {}

  const allFacts: Array<{ subject: string; predicate: string; object: string }> = []
  if (extractFacts) {
    for (const content of memories) {
      const facts = extractFacts(content)
      for (const f of facts) {
        allFacts.push({ subject: f.subject, predicate: f.predicate, object: f.object })
      }
    }
  }

  // 去重三元组
  const uniqueFacts = allFacts.filter((f, i) =>
    allFacts.findIndex(x => x.subject === f.subject && x.predicate === f.predicate && x.object === f.object) === i
  ).slice(0, 3)

  if (uniqueFacts.length > 0) {
    parts.push(uniqueFacts.map(f => `${f.subject}${f.predicate}${f.object}`).join('，'))
  }

  // ── 第二层：entity graph 共现实体 ──
  let findMentionedEntities: ((msg: string) => string[]) | null = null
  try { findMentionedEntities = require('./graph.ts').findMentionedEntities } catch {}

  if (findMentionedEntities) {
    const entityCounts = new Map<string, number>()
    for (const content of memories) {
      const entities = findMentionedEntities(content)
      for (const e of entities) entityCounts.set(e, (entityCounts.get(e) ?? 0) + 1)
    }
    // 在 2+ 条记忆中出现的实体
    const coreEntities = [...entityCounts.entries()]
      .filter(([_, count]) => count >= 2)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 3)
      .map(([name]) => name)
    if (coreEntities.length > 0 && parts.length === 0) {
      parts.push(`涉及：${coreEntities.join('、')}`)
    }
  }

  // ── 第三层：行为模式提取（改进版规则，输出自然语言而非标签）──
  const behaviors: string[] = []
  const allText = memories.join(' ')

  // 偏好提取（带具体对象）
  const likeMatch = allText.match(/(?:喜欢|爱|偏好)(.{2,15}?)(?=[，。！？\s]|$)/g)
  if (likeMatch) {
    for (const m of likeMatch.slice(0, 2)) {
      behaviors.push(m.replace(/[，。！？\s]+$/, ''))
    }
  }
  const dislikeMatch = allText.match(/(?:讨厌|不喜欢|受不了)(.{2,15}?)(?=[，。！？\s]|$)/g)
  if (dislikeMatch) {
    for (const m of dislikeMatch.slice(0, 2)) {
      behaviors.push(m.replace(/[，。！？\s]+$/, ''))
    }
  }

  // 习惯提取
  const habitMatch = allText.match(/(?:每天|经常|习惯|总是)(.{2,20}?)(?=[，。！？\s]|$)/g)
  if (habitMatch) {
    behaviors.push(habitMatch[0].replace(/[，。！？\s]+$/, ''))
  }

  if (behaviors.length > 0) {
    parts.push(behaviors.join('；'))
  }

  // ── 第四层：时序矛盾检测（使用共享 detectPolarityFlip）──
  for (let i = 0; i < memories.length; i++) {
    for (let j = i + 1; j < memories.length; j++) {
      const a = memories[i], b = memories[j]
      if (detectPolarityFlip(a, b)) {
        // 检查是否关于同一实体（共享词）
        const wordsA = new Set((a.match(/[\u4e00-\u9fff]{2,4}/g) || []))
        const wordsB = new Set((b.match(/[\u4e00-\u9fff]{2,4}/g) || []))
        let shared = 0
        for (const w of wordsA) { if (wordsB.has(w)) shared++ }
        if (shared >= 1) {
          parts.push(`观点变化：从正面转负面`)
          // P6c: 矛盾检测 → 降低较早记忆的 Bayes 可信度
          try {
            const { penalizeTruthfulness } = require('./smart-forget.ts')
            const olderContent = a
            const matchedMem = memoryState.memories.find((m: any) => m && m.content === olderContent)
            if (matchedMem) {
              penalizeTruthfulness(matchedMem, `矛盾检测：与"${b.slice(0, 20)}"冲突`)
            }
          } catch {}
          break
        }
      }
    }
    if (parts.length >= 4) break
  }

  // ── Fallback：如果以上都没提取到，用改进版词频（过滤停用词）──
  if (parts.length === 0) {
    const STOP_WORDS = new Set('的了是在我你他她它不有这那就也和但都要会可以如果因为所以然后已经还没到被把从用于关于对于提到'.match(/[\u4e00-\u9fff]/g) || [])
    const allWords = new Map<string, number>()
    for (const content of memories) {
      const words = (content.match(WORD_PATTERN.CJK24_EN3) || []).map(w => w.toLowerCase())
      for (const w of words) {
        // 过滤：纯停用字组成的词（如"的了"、"是在"）
        const chars = w.match(/[\u4e00-\u9fff]/g) || []
        if (chars.length > 0 && chars.every(c => STOP_WORDS.has(c))) continue
        allWords.set(w, (allWords.get(w) || 0) + 1)
      }
    }
    const topWords = [...allWords.entries()]
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5)
      .map(([w]) => w)
    if (topWords.length > 0) parts.push(`关于${topWords.slice(0, 3).join('、')}的讨论`)
  }

  return parts.join('；').slice(0, 200) || memories[0]?.slice(0, 60) || ''
}

// ═══════════════════════════════════════════════════════════════════════════════
// TOPIC CONFIDENCE — 蒸馏反馈闭环：根据回复质量调整 topic node 置信度
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * 调整 topic node 的置信度。quality 高 → confidence 上升，quality 低 → 下降并标记重新蒸馏。
 */
export function adjustTopicConfidence(topicName: string, delta: number) {
  const node = topicNodes.find(n => n.topic === topicName)
  if (!node) return
  const confidence = (node.confidence ?? 0.5) + delta
  node.confidence = Math.max(0.1, Math.min(0.95, confidence))
  // confidence 过低 → 标记需要重新蒸馏
  if (node.confidence < 0.3) {
    node.lastUpdated = 0
    node.stale = true
    logDecision('stale_topic', topicName,
      `confidence=${node.confidence.toFixed(2)}<0.3, delta=${delta}`)
  }
  saveTopicNodes()
}

// ═══════════════════════════════════════════════════════════════════════════════
// INTERNAL UTILITIES
// ═══════════════════════════════════════════════════════════════════════════════

// ── PMI-based incremental assignment (enhancement over keyword overlap) ──

const CJK_WORD_RE = /[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi

function extractWords(text: string): string[] {
  return (text.match(CJK_WORD_RE) || []).map(w => w.toLowerCase())
}

/** Average positive PMI between keyword sets from two texts */
function memoryPMISimilarity(memContent: string, nodeText: string): number {
  let aamPmi: ((w1: string, w2: string) => number) | null = null
  try { aamPmi = require('./aam.ts').pmi } catch { return 0 }
  if (!aamPmi) return 0

  const mWords = [...new Set(extractWords(memContent))]
  const nWords = [...new Set(extractWords(nodeText))]
  if (mWords.length === 0 || nWords.length === 0) return 0

  let sum = 0, count = 0
  for (const mw of mWords) {
    for (const nw of nWords) {
      if (mw === nw) { sum += 3; count++; continue } // exact match → high synthetic PMI
      const p = aamPmi(mw, nw)
      if (p > 0) { sum += p; count++ }
    }
  }
  return count > 0 ? sum / count : 0
}

/** Find best matching TopicNode for a memory using PMI similarity. Returns null if orphan. */
function assignMemoryToNode(memContent: string, nodes: TopicNode[], userId?: string): TopicNode | null {
  let best: TopicNode | null = null, bestScore = 0
  for (const n of nodes) {
    if (userId && n.userId && n.userId !== userId) continue
    const score = memoryPMISimilarity(memContent, `${n.topic} ${n.summary}`)
    if (score > bestScore) { bestScore = score; best = n }
  }
  return bestScore > 0.3 ? best : null
}

/** Cluster orphan memory contents using PMI. Returns clusters with avg intra-PMI > threshold. */
function clusterOrphansByPMI(orphans: string[], threshold: number): string[][] {
  const clusters: string[][] = []
  const assigned = new Set<number>()

  for (let i = 0; i < orphans.length; i++) {
    if (assigned.has(i)) continue
    const cluster = [orphans[i]]
    assigned.add(i)
    for (let j = i + 1; j < orphans.length; j++) {
      if (assigned.has(j)) continue
      if (memoryPMISimilarity(orphans[i], orphans[j]) > threshold) {
        cluster.push(orphans[j])
        assigned.add(j)
      }
    }
    if (cluster.length >= 2) clusters.push(cluster)
  }
  return clusters
}

/**
 * Simple keyword-based clustering. Groups memories that share >40% keywords.
 */
function clusterByKeywords(memories: Memory[]): Memory[][] {
  const CJK_WORD = /[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi
  const clusters: Memory[][] = []
  const assigned = new Set<number>()

  for (let i = 0; i < memories.length; i++) {
    if (assigned.has(i)) continue
    const cluster = [memories[i]]
    assigned.add(i)

    const wordsI = new Set((memories[i].content.match(CJK_WORD) || []).map(w => w.toLowerCase()))
    if (wordsI.size === 0) continue

    for (let j = i + 1; j < memories.length; j++) {
      if (assigned.has(j)) continue
      const wordsJ = new Set((memories[j].content.match(CJK_WORD) || []).map(w => w.toLowerCase()))
      if (wordsJ.size === 0) continue

      let hits = 0
      for (const w of wordsI) { if (wordsJ.has(w)) hits++ }
      const overlap = hits / Math.max(1, Math.min(wordsI.size, wordsJ.size))

      if (overlap >= 0.4) {
        cluster.push(memories[j])
        assigned.add(j)
      }
    }

    if (cluster.length >= 2) {
      clusters.push(cluster)
    }
  }

  return clusters
}

/**
 * Calculate keyword overlap ratio between two text strings.
 */
function keywordOverlap(a: string, b: string): number {
  const CJK_WORD = /[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi
  const wordsA = new Set((a.match(CJK_WORD) || []).map(w => w.toLowerCase()))
  const wordsB = new Set((b.match(CJK_WORD) || []).map(w => w.toLowerCase()))
  if (wordsA.size === 0 || wordsB.size === 0) return 0

  let hits = 0
  for (const w of wordsA) { if (wordsB.has(w)) hits++ }
  return hits / Math.max(1, Math.min(wordsA.size, wordsB.size))
}
