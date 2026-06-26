/**
 * activation-field.ts — NAM: Neural Activation Memory（神经激活记忆）
 *
 * cc-soul 原创核心算法。记忆不是被"搜索"的，是自己"冒出来"的。
 * 将传统搜索（BM25/Trigram/向量）统一为单一激活场模型。
 * 无需外部模型，从用户交互中自主学习语义关联。
 *
 * 一个系统，4 种频率：
 *   每条消息（<30ms）：更新激活值 → 编码 + 召回
 *   每分钟：自然衰减 → 遗忘
 *   每小时：FSRS检查 + 巩固 + Anti-Hebbian清理
 *   每天：蒸馏 + 周期学习 + FSRS个性化
 *
 * 7 个激活信号（乘法组合）：
 *   ① 基础激活（ACT-R：频率 + 新近性）
 *   ② 上下文匹配（BM25F多字段加权 + AAM词扩展 + trigram融合）
 *   ③ 情绪共振（PADCN余弦 + 闪光灯 + 状态门控）
 *   ④ 扩散激活（邻居激活 × 连接权重 + 微连接涌现）
 *   ⑤ 干扰抑制（相似记忆竞争 + Anti-Hebbian + RIF持久衰减）
 *   ⑥ 时间语境（编码特异性 + recallContexts匹配 + 双振荡器 + 测试效应）
 *   ⑦ 时序共现（PAM有向链接：用户说A后常说B → 说A时含B的记忆boost）
 */

import type { Memory, CogHints } from './types.ts'
import { trigrams, trigramSimilarity, tokenize as _utilTokenize, WORD_PATTERN, TRIGRAM_THRESHOLD } from './memory-utils.ts'
import { expandQuery as _aamExpandQuery, learnAssociation as _aamLearn, isKnownWord as _aamIsKnownWord, getTemporalSuccessors as _aamGetTemporalSuccessors, getAAMNeighbors as _aamGetAAMNeighbors, isJunkToken as _aamIsJunkToken, learnTemporalLink as _aamLearnTemporalLink } from './aam.ts'
// 顶层 import 替代运行时 require（修复 benchmark ESM 环境下 require is not defined）
import { extractTimeRange as _extractTimeRange, _primingCache as _primingCacheRef, _predictivePrimingCache as _predictivePrimingRef } from './memory-recall.ts'
import { extractTagsLocal as _extractTagsLocal } from './memory.ts'

// ── 统一 import 所有模块（不用 require，ESM 兼容）──
// 核心模块直接 import，可选模块 lazy require（在 try/catch 里）
import { detectDomain as _detectDomain } from './epistemic.ts'
import * as _graphMod from './graph.ts'
import * as _factStoreMod from './fact-store.ts'
import { extractAnchors as _extractAnchors, inferTimeRange as _inferTemporalRange } from './temporal-anchor.ts'
import { getTopicRecallModifier as _getDriftModifier } from './semantic-drift.ts'
import { confidenceRecallModifier as _getConfModifier } from './confidence-cascade.ts'
import { getParam as _getAutoTuneParam } from './auto-tune.ts'

// ── Lightweight English Porter Stemmer (suffix-stripping, English only) ──
function porterStem(word: string): string {
  if (word.length < 4) return word
  let w = word.toLowerCase()
  // Step 1: plurals + past tense
  if (w.endsWith('ies') && w.length > 4) w = w.slice(0, -3) + 'i'
  else if (w.endsWith('sses')) w = w.slice(0, -2)
  else if (w.endsWith('s') && !w.endsWith('ss') && !w.endsWith('us')) w = w.slice(0, -1)
  // Step 2: past tense + gerund
  if (w.endsWith('eed')) { /* keep */ }
  else if (w.endsWith('ed') && w.length > 4) w = w.slice(0, -2)
  else if (w.endsWith('ing') && w.length > 5) w = w.slice(0, -3)
  // Step 3: common suffixes
  if (w.endsWith('tion')) w = w.slice(0, -4) + 't'
  else if (w.endsWith('ness') && w.length > 5) w = w.slice(0, -4)
  else if (w.endsWith('ment') && w.length > 5) w = w.slice(0, -4)
  else if (w.endsWith('ful') && w.length > 5) w = w.slice(0, -3)
  else if (w.endsWith('ous') && w.length > 5) w = w.slice(0, -3)
  else if (w.endsWith('ive') && w.length > 5) w = w.slice(0, -3)
  else if (w.endsWith('able') && w.length > 6) w = w.slice(0, -4)
  else if (w.endsWith('ible') && w.length > 6) w = w.slice(0, -4)
  else if (w.endsWith('ally') && w.length > 6) w = w.slice(0, -4) + 'al'
  else if (w.endsWith('ly') && w.length > 4) w = w.slice(0, -2)
  return w
}

// ═══════════════════════════════════════════════════════════════
// ActivationTrace — 召回路径溯源（服务于 AAM 正负反馈、decision-log、A/B 归因、MAGMA 验证）
// ═══════════════════════════════════════════════════════════════

export interface TraceStep {
  stage: 'candidate_selection' | 'signal_boost' | 'signal_suppress'
  via: string  // 'bm25' | 'aam_hop1' | 'aam_hop2' | 'graph' | 'cin' | 'system1_fact' | 'priming' | 'emotion' | 'recency' | 'interference' | 'mmr' | 'base_activation' | 'temporal' | 'confidence' | 'importance'
  word?: string
  rawScore: number
}

export interface ActivationTrace {
  memory: Memory
  score: number
  path: TraceStep[]
}

export interface RejectionRecord {
  content: string
  originalRank: number
  finalRank: number
  reason: 'interference' | 'mmr_dedup' | 'below_threshold' | 'budget_cut'
}

// 内存缓存：最近 3 轮的 trace，用 Date.now() 作 key
const _traceBuffer = new Map<number, { traces: ActivationTrace[]; rejections: RejectionRecord[] }>()

// ── BM25 标准分母：文档平均长度（在 computeActivationField 内预计算）──
let _currentAvgDocLen = 20
// SSH 模块级缓存
let _sshMemDims = new Map<string, Set<string>>()
let _sshDimFreqMap = new Map<string, number>()
let _sshQueryDims = new Set<string>()

// ── Recall Thermostat: learn which signals correlate with engaged memories ──
const _signalBuffer: { engaged: boolean; signals: { base: number; context: number; emotion: number; spread: number; interference: number; temporal: number; pam: number } }[] = []

export function recordRecallEngagement(engaged: boolean, signals: Record<string, number>): void {
  _signalBuffer.push({ engaged, signals: {
    base: signals.base || 0, context: signals.context || 0,
    emotion: signals.emotion || 0, spread: signals.spread || 0,
    interference: signals.interference || 0, temporal: signals.temporal || 0,
    pam: signals.pam || 0,
  }})
  if (_signalBuffer.length > 200) _signalBuffer.shift()

  if (_signalBuffer.length % 50 === 0 && _signalBuffer.length >= 50) {
    adjustSignalWeights()
  }
}

let _baseWeight = 0.3
let _contextWeight = 0.7

// 5 个可学习调制系数（初始值 = 当前硬编码值）
let _emotionCoeff = 0.5    // (0.5 + _emotionCoeff × s3)
let _spreadCoeff = 1.0     // (1 + _spreadCoeff × s4)
let _temporalCoeff = 0.2   // (0.8 + _temporalCoeff × s6)
let _pamCoeff = 1.0        // (1 + _pamCoeff × s7)
let _momentumCoeff = 1.0   // momentumScale 系数

export function getSignalWeights(): { base: number; context: number } {
  return { base: _baseWeight, context: _contextWeight }
}

function adjustSignalWeights(): void {
  const good = _signalBuffer.filter(s => s.engaged)
  const bad = _signalBuffer.filter(s => !s.engaged)
  if (good.length < 10 || bad.length < 5) return

  const avgGoodContext = good.reduce((s, g) => s + g.signals.context, 0) / good.length
  const avgBadContext = bad.reduce((s, b) => s + b.signals.context, 0) / bad.length
  const avgGoodBase = good.reduce((s, g) => s + g.signals.base, 0) / good.length
  const avgBadBase = bad.reduce((s, b) => s + b.signals.base, 0) / bad.length

  const contextDelta = avgGoodContext - avgBadContext
  const baseDelta = avgGoodBase - avgBadBase

  // Conservative adjustment: ±0.01 per cycle, clamped to [0.15, 0.45] for base
  _baseWeight = Math.max(0.15, Math.min(0.45, _baseWeight + baseDelta * 0.01))
  _contextWeight = 1 - _baseWeight

  // 5 信号自适应学习（学习率 0.003 = base/context 的 1/3，每 50 轮调一次）
  const signalNames = ['emotion', 'spread', 'temporal', 'pam'] as const  // interference 跳过（MMR 层面单独控制）
  const correlations: Record<string, number> = {}
  for (const name of signalNames) {
    const avgGood = good.reduce((s, g) => s + g.signals[name], 0) / good.length
    const avgBad = bad.reduce((s, b) => s + b.signals[name], 0) / bad.length
    correlations[name] = avgGood - avgBad
  }

  // 保守学习：步长 0.003，clamp 防极端
  _emotionCoeff = Math.max(0.1, Math.min(1.0, _emotionCoeff + (correlations.emotion || 0) * 0.003))
  _spreadCoeff = Math.max(0.2, Math.min(2.0, _spreadCoeff + (correlations.spread || 0) * 0.003))
  _temporalCoeff = Math.max(0.1, Math.min(0.5, _temporalCoeff + (correlations.temporal || 0) * 0.003))
  _pamCoeff = Math.max(0.3, Math.min(2.0, _pamCoeff + (correlations.pam || 0) * 0.003))
  _momentumCoeff = Math.max(0.3, Math.min(2.0, _momentumCoeff))  // momentum 暂不学习，后续接入

  try {
    const corrStr = signalNames.map(n => `${n}=${correlations[n].toFixed(3)}`).join(', ')
    const coeffStr = `emo=${_emotionCoeff.toFixed(3)},spr=${_spreadCoeff.toFixed(3)},tmp=${_temporalCoeff.toFixed(3)},pam=${_pamCoeff.toFixed(3)}`
    require('./decision-log.ts').logDecision('recall_thermostat', 'weight_adjust', `base=${_baseWeight.toFixed(3)}, ctx=${_contextWeight.toFixed(3)}, ${coeffStr}, samples=${_signalBuffer.length}, corr: ${corrStr}`)
  } catch {}
}

/** 获取最近 30 秒内的 trace（供 feedback 回溯用） */
export function getRecentTrace(): { traces: ActivationTrace[]; rejections: RejectionRecord[] } | null {
  const now = Date.now()
  const recent = [..._traceBuffer.entries()]
    .filter(([ts]) => now - ts < 30_000)
    .sort(([a], [b]) => b - a)
  return recent[0]?.[1] ?? null
}

/** 清理过期 trace（保留最近 3 轮） */
function pruneTraceBuffer() {
  if (_traceBuffer.size <= 3) return
  const sorted = [..._traceBuffer.keys()].sort((a, b) => a - b)
  while (sorted.length > 3) {
    _traceBuffer.delete(sorted.shift()!)
  }
}

// ═══════════════════════════════════════════════════════════════
// 对话惯性记忆（Conversational Momentum Memory）— cc-soul 原创
// EMA-based topic momentum: 持续讨论的话题维持高激活，即使偏题也不会骤降
// ═══════════════════════════════════════════════════════════════

const _topicMomentum = new Map<string, number>()  // topic → momentum score

// 按话题类型的衰减率（通过 detectDomain 判断）
const MOMENTUM_DECAY: Record<string, number> = {
  technical: 0.9,   // 工作项目：惯性持续 ~2 周
  emotional: 0.7,   // 生活琐事：~5 天
  default: 0.7,
}

/** 每条消息更新 momentum（在 activationRecall 中调用） */
function updateMomentum(query: string): void {
  // 检测 domain
  let domain = 'default'
  try {
    domain = _detectDomain(query) || 'default'
  } catch {}

  // 提取话题关键词
  const words = (query.match(WORD_PATTERN.CJK2_EN3) || []).map(w => w.toLowerCase())

  // ── 话题切换检测 ──
  // 短查询用绝对数量（零重叠才切换），长查询用比例（<15%）
  let overlapCount = 0
  for (const w of words) {
    if (_topicMomentum.has(w) && (_topicMomentum.get(w)! > 0.5)) overlapCount++
  }
  const overlapRatio = words.length > 0 ? overlapCount / words.length : 1
  const isSwitched = _topicMomentum.size > 3 && (
    (overlapRatio < 0.15 && words.length >= 5) ||
    (overlapCount === 0 && words.length >= 2)
  )

  // 衰减率：话题切换时急速衰减旧话题（×0.1），否则正常 EMA
  const decayRate = isSwitched ? 0.1 : (MOMENTUM_DECAY[domain] || MOMENTUM_DECAY.default)

  // 先衰减旧话题，再 +1 新词（顺序不能反）
  for (const [topic, score] of _topicMomentum) {
    const decayed = score * decayRate
    if (decayed < 0.1) _topicMomentum.delete(topic)
    else _topicMomentum.set(topic, decayed)
  }

  // 每个关键词 +1
  for (const w of words) {
    const current = _topicMomentum.get(w) || 0
    _topicMomentum.set(w, current + 1)
  }
}

/** 获取记忆的 momentum 加成（capped at +50%） */
export function getMomentumBoost(memContent: string): number {
  const words = (memContent.match(WORD_PATTERN.CJK2_EN3) || []).map(w => w.toLowerCase())
  let totalMomentum = 0
  for (const w of words) {
    totalMomentum += _topicMomentum.get(w) || 0
  }
  if (words.length === 0) return 0
  // 归一化：每词平均 momentum × 0.1，上限 +50%
  // 对话惯性是 NAM 独有能力，cap 提升到 80%（向量做不到连续对话加权）
  return Math.min(0.8, (totalMomentum / words.length) * 0.15)
}

// ═══════════════════════════════════════════════════════════════
// CATEGORY PRE-PRUNING — 按领域预筛，减少候选池，提升召回精度
// ═══════════════════════════════════════════════════════════════

const CATEGORY_KEYWORDS: Record<string, string[]> = {
  work: ['工作', '上班', '公司', '同事', '加班', '薪资', '面试', '简历', '老板', '晋升', 'work', 'job', 'company', 'boss', 'salary', 'career', 'office', 'colleague'],
  tech: ['代码', '编程', '服务器', '数据库', 'bug', 'Python', 'code', 'deploy', '开发', '接口', 'API', '框架', 'debug', 'programming', 'software'],
  health: ['血压', '睡眠', '运动', '减肥', '过敏', '体检', '医院', '吃药', '感冒', '头疼', 'health', 'doctor', 'exercise', 'running', 'fitness', 'gym', 'marathon', 'yoga', 'workout'],
  family: ['老婆', '女朋友', '孩子', '父母', '家人', '宝宝', '老公', '男朋友', '爸', '妈', 'wife', 'family', 'husband', 'kid', 'children', 'mother', 'father', 'daughter', 'son', 'sibling', 'grandma', 'grandmother'],
  finance: ['房贷', '工资', '股票', '理财', '存款', '基金', '投资', '账单', 'mortgage', 'salary', 'stock', 'invest', 'budget', 'savings'],
  food: ['吃', '做饭', '火锅', '外卖', '餐厅', '菜', '烧烤', '奶茶', 'food', 'restaurant', 'cook', 'recipe', 'bake', 'dinner', 'lunch'],
  travel: ['旅游', '出差', '机票', '酒店', '签证', '景点', 'travel', 'trip', 'flight', 'hotel', 'vacation', 'road trip', 'camping', 'hiking', 'beach'],
  emotion: ['开心', '难过', '焦虑', '压力', '心情', '烦', '崩溃', '郁闷', 'happy', 'sad', 'anxious', 'stress', 'excited', 'worried', 'proud', 'grateful', 'scared'],
  housing: ['房子', '租房', '装修', '搬家', '物业', '小区', 'house', 'rent', 'apartment', 'move', 'home', 'neighborhood'],
  social: ['朋友', '聚会', '约会', '社交', '饭局', 'friend', 'party', 'date', 'hangout', 'reunion', 'catch up', 'meeting'],
  education: ['学习', '大学', '考试', '课程', '论文', '毕业', 'study', 'university', 'exam', 'course', 'school', 'teacher', 'graduate', 'degree'],
  entertainment: ['电影', '游戏', '音乐', '看书', '追剧', '综艺', 'movie', 'game', 'music', 'book', 'read', 'concert', 'painting', 'art', 'pottery', 'piano', 'guitar', 'ukulele'],
  pet: ['猫', '狗', '宠物', '铲屎', '猫粮', '狗粮', 'cat', 'dog', 'pet', 'kitten', 'puppy', 'animal', 'foster', 'shelter'],
  identity: ['adoption', 'adopted', 'religion', 'religious', 'church', 'faith', 'LGBTQ', 'transgender', 'pride', 'community', 'volunteer', 'charity', 'mentorship', 'counseling', 'advocacy'],
  outdoor: ['hike', 'bike', 'camp', 'trail', 'park', 'garden', 'nature', 'sunrise', 'photography', 'landscape', 'mountain', 'lake'],
}

// 预编译：为每个 category 建一个 Set（加速查找）
const _categoryWordSets = new Map<string, Set<string>>()
for (const [cat, words] of Object.entries(CATEGORY_KEYWORDS)) {
  _categoryWordSets.set(cat, new Set(words.map(w => w.toLowerCase())))
}

/** 检测文本的领域分类，返回命中的 category 列表（按命中数降序）
 *  使用 stemming 扩大匹配覆盖（"ran"→"run" 匹配 "running"）*/
function detectCategories(text: string): string[] {
  const lower = text.toLowerCase()
  // 提取文本中的所有词（含 stemmed 形式）
  const textWords = new Set<string>()
  for (const w of (lower.match(/[a-z]{3,}/g) || [])) {
    textWords.add(w)
    textWords.add(porterStem(w))  // stemmed 形式
  }
  // CJK 保留
  for (const w of (lower.match(/[\u4e00-\u9fff]{2,4}/g) || [])) textWords.add(w)

  const scores: [string, number][] = []
  for (const [cat, wordSet] of _categoryWordSets) {
    let hits = 0
    for (const kw of wordSet) {
      // 直接包含 or stemmed 匹配
      if (lower.includes(kw)) { hits++; continue }
      const kwStem = kw.length >= 3 && /^[a-z]+$/.test(kw) ? porterStem(kw) : kw
      if (textWords.has(kwStem)) hits++
    }
    if (hits > 0) scores.push([cat, hits])
  }
  scores.sort((a, b) => b[1] - a[1])
  return scores.map(s => s[0])
}

/** 内容级 category 缓存（避免对同一条记忆重复检测） */
const _memCategoryCache = new Map<string, string[]>()
const MEM_CATEGORY_CACHE_MAX = 5000

function getMemCategories(mem: Memory): string[] {
  const key = (mem.content || '').slice(0, 80)
  let cats = _memCategoryCache.get(key)
  if (cats !== undefined) return cats
  cats = detectCategories(mem.content || '')
  if (_memCategoryCache.size >= MEM_CATEGORY_CACHE_MAX) {
    const keys = [..._memCategoryCache.keys()]
    for (let i = 0; i < keys.length / 2; i++) _memCategoryCache.delete(keys[i])
  }
  _memCategoryCache.set(key, cats)
  return cats
}

const CATEGORY_PRUNE_THRESHOLD = 100  // 只在候选池 > 100 时才启用剪枝
const CATEGORY_PRUNE_MIN_POOL = 20    // 剪枝后最少保留的记忆数
const CATEGORY_HIGH_IMPORTANCE = 8    // 高重要性记忆无条件保留

/**
 * 按领域预筛记忆：只保留与查询同 category 的 + 高重要性的
 * 返回剪枝后的 memories 子集（如果不值得剪枝，返回原数组）
 */
// Category soft-weighting: 不再硬删记忆，改为类别不匹配时降权 0.5
// 存储在 _categoryPenalty Map 中，供 computeActivationField 读取
const _categoryPenalty = new Map<string, number>()

/**
 * Topic-Partitioned Recall v3（hard-partition + stemming 增强 + 安全 fallback）
 * v1: soft-weighting → 效果弱
 * v2: hard-partition + 关键词匹配 → 英文覆盖不足 -6.4%
 * v3: hard-partition + stemming + 40% 安全阈值 + 无分类记忆保留
 */
function categoryPrePrune(memories: Memory[], query: string): Memory[] {
  _categoryPenalty.clear()

  if (memories.length <= CATEGORY_PRUNE_THRESHOLD) return memories

  // temporal 查询不做 hard-partition（时间答案可能在任何话题里）
  if (_currentQueryType === 'temporal') return memories

  const queryCats = detectCategories(query)
  if (queryCats.length === 0) return memories

  const queryCatSet = new Set(queryCats.slice(0, 3))
  const partitioned: Memory[] = []
  const seen = new Set<Memory>()

  for (const mem of memories) {
    // 无条件保留：高重要性 / summary / 蒸馏 / insight
    if ((mem.importance || 0) >= CATEGORY_HIGH_IMPORTANCE ||
        mem.tags?.includes('summary') || mem.scope === 'consolidated' ||
        mem.scope === 'fact' || mem.scope === 'insight') {
      if (!seen.has(mem)) { partitioned.push(mem); seen.add(mem) }
      continue
    }
    // 话题匹配（stemming 增强后覆盖率更高）
    const memCats = getMemCategories(mem)
    if (memCats.length === 0) {
      // 无法分类的记忆也保留（不冤枉）
      if (!seen.has(mem)) { partitioned.push(mem); seen.add(mem) }
      continue
    }
    for (const mc of memCats) {
      if (queryCatSet.has(mc)) {
        if (!seen.has(mem)) { partitioned.push(mem); seen.add(mem) }
        break
      }
    }
  }

  // 安全阈值：partition 后至少保留 50% 或 MIN_POOL
  if (partitioned.length < Math.max(CATEGORY_PRUNE_MIN_POOL, memories.length * 0.5)) {
    // fallback: soft-weighting
    for (const mem of memories) {
      if ((mem.importance || 0) >= CATEGORY_HIGH_IMPORTANCE) continue
      const memCats = getMemCategories(mem)
      if (memCats.length === 0) continue
      let matched = false
      for (const mc of memCats) { if (queryCatSet.has(mc)) { matched = true; break } }
      if (!matched) _categoryPenalty.set(memKey(mem), 0.5)
    }
    console.log(`[activation-field] topic-partition fallback: pool ${partitioned.length}/${memories.length} too small, soft-weight`)
    return memories
  }

  console.log(`[activation-field] topic-partition: ${partitioned.length}/${memories.length} (topics: ${[...queryCatSet].join(',')})`)
  return partitioned
}

function getCategoryWeight(mem: Memory): number {
  return _categoryPenalty.get(memKey(mem)) ?? 1.0
}

// ═══════════════════════════════════════════════════════════════
// ACTIVATION STATE — 每条记忆的实时激活值
// ═══════════════════════════════════════════════════════════════

const _activations = new Map<string, number>()  // memory content hash → activation value [0, 1]

// fact-store 已在顶层 import 为 _factStoreMod（行 35）

function memKey(mem: Memory): string {
  return `${(mem.content || '').slice(0, 50)}\0${mem.ts || 0}`
}

function getActivation(mem: Memory): number {
  return _activations.get(memKey(mem)) || 0
}

function setActivation(mem: Memory, value: number) {
  _activations.set(memKey(mem), Math.max(0, Math.min(1, value)))
}

// ═══════════════════════════════════════════════════════════════
// SIGNAL 1: 基础激活（ACT-R）
// ═══════════════════════════════════════════════════════════════

function baseActivation(mem: Memory, now: number): number {
  const n = Math.max(mem.recallCount || 1, 1)
  const createdAgo = Math.max((now - (mem.ts || now)) / 1000, 1)
  const lastAgo = Math.max((now - (mem.lastAccessed || mem.ts || now)) / 1000, 1)

  // ACT-R: B = ln(Σ t_i^(-d)), d=0.5
  let sum = 0
  const cap = Math.min(n, 20)  // 限制 recallCount 对 base activation 的贡献（从 50 降到 20）
  if (cap === 1) {
    sum = Math.pow(lastAgo, -0.5)
  } else {
    for (let i = 0; i < cap; i++) {
      const fraction = i / (cap - 1)
      const accessAgo = createdAgo - fraction * (createdAgo - lastAgo)
      sum += Math.pow(Math.max(accessAgo, 1), -0.5)
    }
  }
  const rawB = sum > 0 ? Math.log(sum) : -5

  // 归一化到 [0, 1]，sigmoid 映射
  return 1 / (1 + Math.exp(-rawB - 1))
}

// ═══════════════════════════════════════════════════════════════
// SIGNAL 2: 上下文匹配（AAM 词扩展 + 关键词重叠 + trigram）
// ═══════════════════════════════════════════════════════════════

// ── 动态 IDF + AWDF 缓存（版本化：只在 memory 增删改时重建，O(1) 命中）──
let _idfCache: Map<string, number> | null = null
let _idfVersion = 0
let _currentIdfVersion = -1
// AWDF: 每个词在所有包含它的记忆中的 baseActivation 总和
// 供 contextMatch 计算 awdf(w, mem) = ba(mem) / _wordActivationSum(w)
let _wordActivationSum: Map<string, number> | null = null

/** 通知 IDF 缓存失效（memory 增/删/改时调用） */
export function invalidateFieldIDF(): void { _idfVersion++ }

/** 从 memory pool 计算动态 IDF + AWDF 激活度加权表 */
function buildIdfCache(memories: Memory[]): Map<string, number> {
  const docFreq = new Map<string, number>()
  const activationSum = new Map<string, number>()
  const N = memories.length
  const now = Date.now()
  for (const mem of memories) {
    const content = mem.content || ''
    const seen = new Set<string>()
    // English 2+ letter words + numbers
    const enWords = content.match(/[a-zA-Z]{2,}|\d+/gi) || []
    for (const w of enWords) seen.add(w.toLowerCase())
    // CJK 2-char
    const cjk = content.match(/[\u4e00-\u9fff]+/g) || []
    for (const seg of cjk) {
      if (seg.length >= 2 && seg.length <= 4) seen.add(seg)
      for (let i = 0; i <= seg.length - 2; i++) seen.add(seg.slice(i, i + 2))
    }
    // AWDF: 累加每个词所在记忆的 baseActivation
    const ba = baseActivation(mem, now)
    for (const w of seen) {
      docFreq.set(w, (docFreq.get(w) || 0) + 1)
      activationSum.set(w, (activationSum.get(w) || 0) + ba)
    }
  }
  _wordActivationSum = activationSum

  const idf = new Map<string, number>()
  for (const [word, df] of docFreq) {
    // IDF = log(N / df)，归一化到 [floor, 1.0]
    // 小池守卫：N<20 时保持 0.1（词太少，IDF 区分度本身已足够）
    const floor = N < 20 ? 0.1 : 0.02
    const raw = Math.log(N / Math.max(1, df))
    const maxIdf = Math.log(N)  // 只出现 1 次的词
    idf.set(word, maxIdf > 0 ? Math.max(floor, raw / maxIdf) : 1.0)
  }
  return idf
}

// ═══════════════════════════════════════════════════════════════
// Query-Type Adaptive Parameters（查询类型自适应 k1/b）
// ═══════════════════════════════════════════════════════════════

type QueryType = 'precise' | 'temporal' | 'broad' | 'multi_entity'

interface QueryTypeParams { k1: number; b: number; temporalBoost: number }

// Query-type multipliers applied on top of auto-tune base k1/b
const QUERY_TYPE_MULTIPLIERS: Record<QueryType, { k1Mult: number; bMult: number; temporalBoost: number }> = {
  precise:      { k1Mult: 1.5,  bMult: 1.0,  temporalBoost: 1.0 },
  temporal:     { k1Mult: 1.0,  bMult: 0.67, temporalBoost: 2.0 },
  broad:        { k1Mult: 0.67, bMult: 0.4,  temporalBoost: 1.0 },
  multi_entity: { k1Mult: 0.8,  bMult: 0.5,  temporalBoost: 1.0 },  // 宽松匹配，让多实体都能命中
}

const PRECISE_RE = /什么|哪个|哪里|几[个岁号]|多少|谁是|who|what|where|how\s*many/i
const TEMPORAL_RE = /上次|之前|以前|上周|昨天|前天|上个月|最近|那时|那年|当时|when|last|before|after|ago|first\s+time|how\s+long|since\s+when|back\s+when|at\s+what\s+point|which\s+session|what\s+time/i

let _currentQueryType: QueryType = 'broad'
let _twoPassInProgress = false

/**
 * 查询类型分治检测（原创升级）
 * 不只是 BM25 参数调整，而是后续策略分派的依据：
 * - temporal → 时间信号优先 + date-entity boost
 * - multi_entity → iterative recall + coverage rerank
 * - precise → 精准匹配，topic partition 更激进
 * - broad → 宽泛召回，全量扫描
 */
function detectQueryType(query: string): QueryType {
  if (TEMPORAL_RE.test(query)) return 'temporal'
  // 多实体检测：2+ 大写人名 → multi_entity（multi_hop 特征）
  const names = (query.match(/\b[A-Z][a-z]{2,}\b/g) || [])
    .filter(n => !/^(What|When|Where|How|Who|Which|Why|The|This|That|Does|Did|Has|Have|Was|Were|Can|Could|Would|Should|Not|And|But|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|January|February|March|April|May|June|July|August|September|October|November|December)$/.test(n))
  if (names.length >= 2) return 'multi_entity'
  if (PRECISE_RE.test(query)) return 'precise'
  return 'broad'
}

/** Get adaptive k1/b — reads base from auto-tune, applies query-type + language multipliers */
function getAdaptiveParams(queryType: QueryType, query?: string): QueryTypeParams {
  const baseK1 = _getAutoTuneParam('memory.bm25_k1')
  const baseB = _getAutoTuneParam('memory.bm25_b')
  const mult = QUERY_TYPE_MULTIPLIERS[queryType]

  // 语言自适应：英文记忆天然更长，降低长度惩罚（b↓），提高词频饱和度（k1↑）
  const isChinese = query ? /[\u4e00-\u9fff]/.test(query) : true
  const langK1 = isChinese ? 1.0 : 1.25   // 英文 k1 +25%
  const langB = isChinese ? 1.0 : 0.67    // 英文 b -33%（降低长度惩罚）

  return {
    k1: baseK1 * mult.k1Mult * langK1,
    b: baseB * mult.bMult * langB,
    temporalBoost: mult.temporalBoost,
  }
}

function contextMatch(query: string, mem: Memory, expandedWords: Map<string, number>, memBaseActivation?: number): number {
  const content = mem.content || ''
  const contentLower = content.toLowerCase()

  // ── 方式 A：扩展词加权匹配（IDF 加权版）──
  const memWords = new Set<string>()
  const cjkSegs = content.match(/[\u4e00-\u9fff]+/g) || []
  for (const seg of cjkSegs) {
    if (seg.length >= 2 && seg.length <= 4) memWords.add(seg)
    if (seg.length > 4) {
      for (let i = 0; i <= seg.length - 2; i++) {
        const frag = seg.slice(i, i + 2)
        if (expandedWords.has(frag)) memWords.add(frag)
      }
      for (let len = 3; len <= Math.min(4, seg.length); len++) {
        for (let i = 0; i <= seg.length - len; i++) memWords.add(seg.slice(i, i + len))
      }
    }
    if (seg.length > 2 && seg.length <= 4) {
      for (let i = 0; i <= seg.length - 2; i++) memWords.add(seg.slice(i, i + 2))
    }
  }
  const enWords = content.match(/[a-zA-Z]{2,}|\d+/gi) || []
  for (const w of enWords) {
    const wl = w.toLowerCase()
    memWords.add(wl)
    if (/^[a-zA-Z]{2,}$/.test(w)) memWords.add(porterStem(wl))
  }
  // _mergedKeywords：update 时被覆盖的旧内容关键词（信息保留）
  const _mk = (mem as any)._mergedKeywords as string[] | undefined
  if (_mk) for (const w of _mk) { memWords.add(w); memWords.add(porterStem(w)) }

  // IDF 加权匹配 + BM25+ delta：高频词权重降低，长文档不被过度惩罚
  // k1 controls term saturation: higher = exact match matters more (precise queries)
  // b controls length normalization: higher = penalize long docs more
  const adaptiveParams = getAdaptiveParams(_currentQueryType, query)
  const BM25_DELTA = adaptiveParams.k1  // BM25+ lower-bound: precise→2.0, broad→0.8
  // BM25 长度归一化：avgDocLen 作分母（标准 BM25），但中文短记忆池 avgDocLen 可能过小
  // 兜底：avgDocLen < 10 时用 expandedWords.size（原始行为）
  const _bm25Denom = _currentAvgDocLen >= 10 ? _currentAvgDocLen : Math.max(expandedWords.size, 10)
  const lengthNorm = 1 - adaptiveParams.b + adaptiveParams.b * (memWords.size / _bm25Denom)
  // ── Rocchio-style 双层计分：expansion hits 是 BONUS，不稀释分母 ──
  // Original words (weight >= 0.9): 构成分母，命中计入分子
  // Expansion words (weight < 0.9): 命中只加 bonus，不进分母
  let originalHits = 0, originalDenom = 0
  let expansionHits = 0, expansionTotal = 0
  let tier2Hits = 0, tier2Total = 0
  for (const [word, weight] of expandedWords) {
    const idfWeight = _idfCache?.get(word) ?? 1.0
    // AWDF: 激活场感知 IDF — 当前记忆的激活度占该词所有记忆激活度总和的比例
    // 高激活记忆中的词权重更高（NAM 独有信号，传统 IR 无此维度）
    const AWDF_ALPHA = 0.5
    const totalAct = _wordActivationSum?.get(word) ?? 0
    const awdf = (memBaseActivation !== undefined && totalAct > 0)
      ? memBaseActivation / totalAct : 0
    const effectiveWeight = weight * idfWeight * (1 + AWDF_ALPHA * awdf)
    const saturation = (adaptiveParams.k1 + 1) / (lengthNorm + adaptiveParams.k1)
    const hitValue = effectiveWeight * saturation + BM25_DELTA
    const maxValue = effectiveWeight * ((adaptiveParams.k1 + 1) / (1 + adaptiveParams.k1)) + BM25_DELTA
    const isOriginal = weight >= 0.9
    // Stem English words for matching
    const stemmed = /^[a-zA-Z]{2,}$/.test(word) ? porterStem(word) : null
    const matched = memWords.has(word) || (stemmed !== null && memWords.has(stemmed))
    if (isOriginal) {
      originalDenom += maxValue
      if (matched) originalHits += hitValue
    } else {
      expansionTotal += maxValue
      if (matched) expansionHits += hitValue
    }
    // Tier 2 fallback (全部词，含碎片)
    tier2Total += maxValue
    if (matched) tier2Hits += hitValue
  }
  // Rocchio: base = originalHits / denom, bonus = expansionHits * 0.3 / expansionDenom
  const safeDenom = Math.max(originalDenom, 0.01)
  const safeExpDenom = Math.max(expansionTotal, 0.01)
  const baseScore = originalHits / safeDenom
  const expansionBonus = expansionHits * 0.5 / safeExpDenom  // 0.3→0.5: 概念扩展词应得更多信任（CONCEPT_HIERARCHY 权重 0.85）
  const tier1Score = baseScore + expansionBonus
  const tier2Score = tier2Total > 0 ? tier2Hits / tier2Total : 0
  // Tier 1 命中直接用，Tier 2 打 7 折（碎片词匹配不应得高分）
  const rawWordScore = Math.max(tier1Score, tier2Score * 0.7)
  // 最低门槛：中文用固定低阈值（CJK 滑动窗口产生大量扩展词，动态阈值会过严）
  // 英文用动态阈值（扩展词更有意义，不存在滑动窗口碎片）
  const _hasCJK = /[\u4e00-\u9fff]/.test(query)
  const _expandedCount = Math.max(1, expandedWords.size)
  const minCoverage = _hasCJK
    ? (_currentQueryType === 'broad' ? 0.01 : 0.03)  // 中文：保持原始阈值
    : Math.max(0.005, 1.0 / _expandedCount)           // 英文：动态阈值
  const wordScore = rawWordScore < minCoverage ? 0 : rawWordScore

  // ── 方式 B：n-gram 短语匹配（连续词序列比独立词匹配更强）──
  // 从 query 提取 2-gram 和 3-gram，如果在记忆中完整出现则大幅加分
  const queryLower = query.toLowerCase()
  const queryTokens = (queryLower.match(WORD_PATTERN.CJK24_EN2_NUM) || []).map(w => w.toLowerCase())
  let phraseScore = 0
  if (queryTokens.length >= 2) {
    let phraseHits = 0, phrasePossible = 0
    // 2-gram
    for (let i = 0; i < queryTokens.length - 1; i++) {
      const bigram = queryTokens[i] + ' ' + queryTokens[i + 1]
      // 也检查无空格连续（中文）
      const bigramNoSpace = queryTokens[i] + queryTokens[i + 1]
      phrasePossible++
      if (contentLower.includes(bigram) || contentLower.includes(bigramNoSpace)) phraseHits++
    }
    // 3-gram
    for (let i = 0; i < queryTokens.length - 2; i++) {
      const trigram = queryTokens[i] + ' ' + queryTokens[i + 1] + ' ' + queryTokens[i + 2]
      phrasePossible++
      if (contentLower.includes(trigram)) phraseHits += 2  // 3-gram 命中权重更高
    }
    phraseScore = phrasePossible > 0 ? phraseHits / phrasePossible : 0
  }

  // ── 方式 C：trigram 模糊匹配 ──
  const triScore = trigramSimilarity(trigrams(query), trigrams(content))

  // BM25F 字段加权移到 rerank 阶段（只对 top-50），此处只算内容基础分
  // 英文 trigram 权重提升：拼写变体/缩写/词形变化更依赖 trigram
  const _enRatio = ((query.match(/[a-zA-Z]+/g) || []).join('').length) / Math.max(query.length, 1)
  const _triWeight = _enRatio > 0.5 ? 1.0 : 0.8
  let sshScore = 0
  if (_sshQueryDims.size > 0) {
    const memDims = _sshMemDims.get(contentLower)
    if (memDims && memDims.size > 0) {
      let wo = 0, tw = 0
      for (const d of _sshQueryDims) {
        const df = _sshDimFreqMap.get(d) || 1
        const idf = 1 / Math.max(1, df)
        tw += idf
        if (memDims.has(d)) wo += idf
      }
      sshScore = tw > 0 ? wo / tw : 0
    }
  }
  // ── CER: Contextual Entity Relevance（原创子算法——嵌套在 contextMatch 内）──
  // BM25 的弱点：词覆盖率低时整条记忆被截断（wordScore=0）
  // CER 补偿：只要实体名+动作词同时命中，就给分——绕过 BM25 的分母膨胀问题
  let cerScore = 0
  // 提取 query 中的实体名（大写开头，排除疑问词）
  const _cerEntities = (query.match(/\b[A-Z][a-z]{2,}\b/g) || [])
    .filter(n => !/^(What|When|Where|How|Who|Which|Why|The|This|That|Does|Did|Has|Have|Was|Were|Can|Could|Would|Should|Not|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)$/.test(n))
  if (_cerEntities.length > 0) {
    const entityHit = _cerEntities.some(n => contentLower.includes(n.toLowerCase()))
    if (entityHit) {
      // 实体命中后检查内容词重叠（至少 1 个非实体非停用词命中）
      const _cerContentWords = (query.match(/[a-zA-Z]{4,}/gi) || [])
        .map(w => w.toLowerCase())
        .filter(w => !EN_STOP_WORDS.has(w) && !_cerEntities.map(e => e.toLowerCase()).includes(w))
      const contentHits = _cerContentWords.filter(w => {
        if (contentLower.includes(w)) return true
        // Porter stem fallback
        const stem = porterStem(w)
        return stem !== w && contentLower.includes(stem)
      }).length
      if (contentHits > 0) {
        cerScore = Math.min(0.8, contentHits / Math.max(_cerContentWords.length, 1))
      }
    }
  }

  // 多通道融合：max + 次高 × 0.15（多通道同时支持时给额外奖励，原创）
  const _cmScores = [wordScore, phraseScore * 1.2, triScore * _triWeight, sshScore * 0.8, cerScore * 0.9].sort((a, b) => b - a)
  return _cmScores[0] + (_cmScores.length >= 2 && _cmScores[1] > 0.05 ? _cmScores[1] * 0.15 : 0)
}

// ═══════════════════════════════════════════════════════════════
// SIGNAL 3: 情绪共振（PADCN 余弦 + 闪光灯 + 状态门控）
// ═══════════════════════════════════════════════════════════════

function emotionResonance(mem: Memory, currentMood: number, currentAlertness: number): number {
  let score = 0.5  // 中性基线

  // 状态门控（Godden & Baddeley）：编码时和当前的情绪差距越大，越难召回
  if (mem.situationCtx?.mood !== undefined) {
    const moodDist = Math.abs(currentMood - mem.situationCtx.mood)
    const alertDist = Math.abs(currentAlertness - (mem.situationCtx.energy || 0.5))
    const stateDist = Math.sqrt(moodDist * moodDist + alertDist * alertDist)
    const gate = 1 / (1 + Math.exp(stateDist * 3 - 1.5))
    score *= Math.max(0.2, gate)
  }

  // 情绪一致性（Bower 1981）：心情好时更容易想起好事
  if (currentMood > 0.3 && mem.emotion === 'warm') score *= 1.4
  if (currentMood < -0.3 && mem.emotion === 'painful') score *= 1.4

  // 闪光灯效应（Cahill & McGaugh）：平滑曲线替代 3 档跳跃
  const ei = mem.emotionIntensity || 0
  score *= (1 + ei * 0.5)  // ei=0 → ×1.0, ei=0.5 �� ×1.25, ei=1.0 → ×1.5

  return Math.min(1, score)
}

// ═══════════════════════════════════════════════════════════════
// SIGNAL 4: 扩散激活（邻居激活值传播）
// ═══════════════════════════════════════════════════════════════

// ── AAM neighbor cache (lazy-loaded, avoids import side effects) ──
let _aamGetNeighbors: ((word: string, topK?: number) => { word: string; pmiScore: number; fanOut: number }[]) | null | false = null
function getAAMNeighborsFn(): typeof _aamGetNeighbors {
  if (_aamGetNeighbors === false) return null  // import failed before
  if (_aamGetNeighbors) return _aamGetNeighbors
  try {
    _aamGetNeighbors = _aamGetAAMNeighbors || false
    return _aamGetNeighbors || null
  } catch { _aamGetNeighbors = false; return null }
}

// ═══════════════════════════════════════════════════════════════
// ERF: Entity Resonance Field（实体共振场）— cc-soul 原创
//
// 在记忆激活场之外维护一个实体级别的激活场。
// 查询进来时：实体被激活 → 通过图谱边扩散 → 反向 boost 含相关实体的记忆
// 解决多跳推理：query→实体A→(图谱边)→实体B→含B的记忆自动浮现
//
// 与传统 graph retrieval 的区别：
//   graph BFS: 离散的"找到/没找到"
//   ERF: 连续的激活值 0-1，远的实体弱激活、近的强激活
// ═══════════════════════════════════════════════════════════════

// 实体激活值缓存（每次查询重建）
let _erfCache: Map<string, number> | null = null
let _aamNeighborCache: Map<string, number> | null = null  // 查询级 AAM 邻居缓存

/**
 * 构建实体共振场：从查询中提取实体，通过图谱边扩散
 * @returns entity → activation value [0, 1]
 */
function buildEntityResonanceField(query: string, memories: Memory[]): Map<string, number> {
  const erf = new Map<string, number>()

  try {
    const graph = _graphMod
    if (!graph.findMentionedEntities || !graph.getRelatedEntities) return erf

    // Step 1: 从查询中找实体 → 激活值 1.0
    const queryEntities = graph.findMentionedEntities(query) as string[]
    for (const e of queryEntities) erf.set(e, 1.0)

    // 也从查询关键词里找（防止实体提取遗漏）
    const queryWords = (query.match(WORD_PATTERN.CJK24_EN3) || [])
    for (const w of queryWords) {
      if (!erf.has(w) && graph.findMentionedEntities(w).length > 0) {
        erf.set(w, 0.8)
      }
    }

    if (erf.size === 0) return erf

    // Step 2: 通过图谱边扩散（2 跳，衰减 0.5/0.25）
    const hop1 = graph.getRelatedEntities([...erf.keys()], 1, 20) as string[]
    for (const e of hop1) {
      if (!erf.has(e)) erf.set(e, 0.5)  // 1-hop: 50% 激活
    }

    const hop2 = graph.getRelatedEntities(hop1, 1, 15) as string[]
    for (const e of hop2) {
      if (!erf.has(e)) erf.set(e, 0.25)  // 2-hop: 25% 激活
    }
  } catch {}

  return erf
}

/**
 * 从 ERF 获取记忆的实体共振分数
 * 记忆中包含的实体在 ERF 中越活跃，分数越高
 */
function getEntityResonance(mem: Memory, erf: Map<string, number>): number {
  if (erf.size === 0) return 0
  const content = mem.content || ''
  let totalResonance = 0
  let entityCount = 0

  for (const [entity, activation] of erf) {
    if (content.includes(entity)) {
      totalResonance += activation
      entityCount++
    }
  }

  // G2: 分层 cap——精确命中越多越可信
  if (entityCount === 0) return 0
  const capBase = entityCount >= 2 ? 0.65 : entityCount === 1 ? 0.5 : 0.4
  return Math.min(capBase, totalResonance * 0.15 * Math.sqrt(entityCount))
}

function spreadingActivation(mem: Memory, allMemories: Memory[], query?: string): number {
  const hasTags = mem.tags && mem.tags.length > 0
  const myTags = hasTags ? new Set(mem.tags!.map(t => t.toLowerCase())) : new Set<string>()
  let totalSpread = 0
  let count = 0

  // ── Path A: tag-based spreading (original) ──
  if (hasTags) {
    for (const other of allMemories) {
      if (other === mem || !other.tags || other.tags.length === 0) continue
      const otherActivation = getActivation(other)
      if (otherActivation < 0.2) continue

      const shared = other.tags.filter(t => myTags.has(t.toLowerCase())).length
      if (shared > 0) {
        totalSpread += otherActivation * (shared / Math.max(myTags.size, 1)) * 0.3
        count++
      }
      if (count >= 10) break
    }
  }

  // ── Path B: AAM co-occurrence（查询级缓存版，不再对每条记忆重复计算 PMI）──
  // 旧版对每条记忆做 5×5×3=75 次 PMI 查询，438 条 = 32K 次 → 20 秒
  // 新版用 _aamNeighborCache（在 computeActivationField 中预建），O(1) 查表
  if (count < 3 && query && _aamNeighborCache && _aamNeighborCache.size > 0) {
    const memKeywords = (mem.content || '').match(WORD_PATTERN.CJK24_EN3) || []
    let aamBoost = 0
    for (const kw of memKeywords.slice(0, 8)) {
      const score = _aamNeighborCache.get(kw.toLowerCase())
      if (score) aamBoost += score
    }
    totalSpread += Math.min(0.3, aamBoost)
  }

  // ── Path C: Entity Resonance Field（实体共振场）──
  // ERF 在 computeActivationField 中预建，通过 _erfCache 传递
  if (_erfCache && _erfCache.size > 0) {
    const erfBoost = getEntityResonance(mem, _erfCache)
    if (erfBoost > 0) totalSpread += erfBoost
  }

  return Math.min(0.6, totalSpread)
}

// ═══════════════════════════════════════════════════════════════
// SIGNAL 5: 干扰抑制（相似记忆竞争）
// ═══════════════════════════════════════════════════════════════

/** Compute MMR-based interference factor for a candidate against already-selected memories.
 *  Uses max similarity to ANY selected memory (maximal marginal relevance style).
 *  A3 SIMPLE extension: temporal proximity amplifies interference (Brown, Neath & Chater 2007).
 *  Log-scale invariant: 5s vs 25s ago has same discriminability as 5min vs 25min ago.
 *  Returns suppression factor in [0.3, 1.0]. */
function interferenceMMR(memTri: Set<string>, selectedTris: Set<string>[], isSummary: boolean, memAge?: number, selectedAges?: number[]): number {
  if (selectedTris.length === 0) return 1.0

  // MMR core: max similarity to ANY already-selected memory
  let maxSim = 0
  let maxSimIdx = 0
  for (let i = 0; i < selectedTris.length; i++) {
    const sim = trigramSimilarity(memTri, selectedTris[i])
    if (sim > maxSim) { maxSim = sim; maxSimIdx = i }
  }

  // A3 SIMPLE: temporal proximity amplifies interference
  // Two memories from same time period are more likely redundant
  let temporalFactor = 1.0
  if (memAge !== undefined && selectedAges && selectedAges.length > maxSimIdx) {
    const selAge = selectedAges[maxSimIdx]
    if (selAge > 0 && memAge > 0) {
      const logDist = Math.abs(Math.log(memAge + 1) - Math.log(selAge + 1))
      // logDist ≈ 0 → same time period → amplify interference
      // logDist > 3 → very different times → no extra interference
      temporalFactor = 1.0 + 0.3 * Math.exp(-2 * logDist)  // [1.0, 1.3]
    }
  }

  // Apply temporal amplification to similarity
  const effectiveSim = Math.min(1.0, maxSim * temporalFactor)

  if (isSummary) {
    if (effectiveSim > TRIGRAM_THRESHOLD.DEDUP_MERGE) return 0.5
    if (effectiveSim > TRIGRAM_THRESHOLD.INTERFERENCE_STRONG) return 0.8
  } else {
    if (effectiveSim > TRIGRAM_THRESHOLD.INTERFERENCE_STRONG) return 0.3
    if (effectiveSim > TRIGRAM_THRESHOLD.INTERFERENCE_LIGHT) return 0.7
  }
  return 1.0
}

// ═══════════════════════════════════════════════════════════════
// SIGNAL 6: 时间语境（编码特异性 + 节律 + recallContexts 匹配）
// ═══════════════════════════════════════════════════════════════

interface TimeRange { fromMs: number; toMs: number }

function temporalContext(mem: Memory, timeRange?: TimeRange | null, queryWords?: Set<string>): number {
  // Triple Query Decomposition: 如果有明确时间范围，用范围过滤代替新近性衰减
  if (timeRange) {
    const ts = mem.ts || 0
    // 范围内 = 1.0，范围外 = 按距离软衰减（不是 0，给邻近记忆机会）
    if (ts >= timeRange.fromMs && ts <= timeRange.toMs) return 1.0
    const span = timeRange.toMs - timeRange.fromMs || 86400000
    const dist = Math.min(Math.abs(ts - timeRange.fromMs), Math.abs(ts - timeRange.toMs))
    return Math.max(0, 1.0 - dist / span)  // 距范围 1 个 span 宽度内线性衰减
  }

  const now = new Date()
  const memDate = new Date(mem.ts || Date.now())

  // 编码特异性（时间维度）：同一时段的记忆更容易被想起
  const hourDiff = Math.abs(now.getHours() - memDate.getHours())
  const timeMatch = 1 - Math.min(hourDiff, 24 - hourDiff) / 12  // [0, 1]

  // 同一天类型（工作日 vs 周末）
  const sameType = (now.getDay() === 0 || now.getDay() === 6) ===
                   (memDate.getDay() === 0 || memDate.getDay() === 6) ? 1 : 0.8

  // 编码特异性（语境维度，Tulving 1983）：
  // 如果记忆曾在类似查询语境下被召回过，此次更容易再次浮现
  let encodingSpecificity = 0
  if (queryWords && queryWords.size > 0 && mem.recallContexts && mem.recallContexts.length > 0) {
    for (const ctx of mem.recallContexts) {
      const ctxWords = (ctx.match(WORD_PATTERN.CJK2_EN3) || []).map(w => w.toLowerCase())
      const overlap = ctxWords.filter(w => queryWords.has(w)).length
      if (overlap >= 2) {
        encodingSpecificity = Math.min(0.3, overlap * 0.08)  // 2词+0.16, 3词+0.24, cap 0.3
        break
      }
    }
  }

  const base = timeMatch * 0.5 + sameType * 0.5 + encodingSpecificity
  // Temporal query type → boost temporal signal (capped at 1.0)
  const tBoost = QUERY_TYPE_MULTIPLIERS[_currentQueryType]?.temporalBoost ?? 1.0
  return Math.min(1, base * tBoost)
}

// ═══════════════════════════════════════════════════════════════
// 核心：统一激活值计算
// ═══════════════════════════════════════════════════════════════

export interface ActivationResult {
  memory: Memory
  activation: number
  signals: {
    base: number
    context: number
    emotion: number
    spread: number
    interference: number
    temporal: number
  }
  path?: TraceStep[]
}

/**
 * 统一激活场：对所有记忆计算激活值，返回 top-N
 *
 * activation = (0.3×① + 0.7×②) × (0.5 + 0.5×③) × (1 + ④) × ⑤ × (0.8 + 0.2×⑥)
 *              ╰── 加法融合 ──╯   ╰──────── 乘法调制 ────────╯
 *
 * 加法融合（base + context）：
 * - 解决 ACT-R 衰减碾压 context 的问题：base 365x 动态范围 vs context 20x
 * - 0.3/0.7 权重：长期陪伴场景，相关性比新近性重要
 * - 旧但相关的记忆 (base=0.002, ctx=0.9) → 0.3×0.002 + 0.7×0.9 = 0.63
 * - 新但无关的记忆 (base=0.73, ctx=0.05) → 0.3×0.73 + 0.7×0.05 = 0.25
 *
 * 乘法调制（emotion × spread × interference × temporal）：
 * - 情绪为 0 → 0.5×（降半，但不封锁）
 * - 扩散为 0 → 1.0（没有邻居不影响）
 * - 干扰为 0.3 → 被强竞争者压制到 30%
 * - 时间为 0 → 0.8（时间不匹配轻微降低）
 */
export function computeActivationField(
  memories: Memory[],
  query: string,
  mood: number,
  alertness: number,
  expandedWords: Map<string, number>,
  topN: number = 10,
  timeRange?: TimeRange | null,
  cogHints?: CogHints | null,
): ActivationResult[] {
  const now = Date.now()

  // ── CGAF: Cognition-Gated Activation Field ──
  // 当有 cogHints 时，用 Bayesian 连续概率调制信号权重（替代硬编码正则）
  // 当无 cogHints 时，回退到旧的 IMAF 正则（兼容性）
  const _imaf = (() => {
    if (cogHints) {
      const h = cogHints
      // 连续插值：多假设概率叠加，不是 if/else 互斥
      // temporal query 检测（补充 cognition 不覆盖的维度）
      const isTemporalQ = /什么时候|上次|上周|when did|last time|recently|what happened|ago|how long/i.test(query)
      const hasEntityName = !!(query.match(/\b[A-Z][a-z]{2,}\b/g)?.filter(n => !/^(What|When|Where|How|Who|Which|Why|The|This|That|Does|Did|Has|Have|Was|Were|Can|Could|Would|Should|Not)$/.test(n)).length)
      const isCausalQ = /为什么|原因|导致|why|because|cause|reason|how come/i.test(query)

      let s1 = 1.0 - 0.3 * h.casualProb                          // 闲聊时 base 降权
      let s2 = 1.0 + 0.5 * h.technicalProb                       // 技术/精确查询 context 加权
      let s3 = 0.3 + 1.7 * h.emotionalProb                       // 情绪问题情绪共振拉满
      let s4 = 1.0 + 1.0 * h.complexity                          // 复杂问题扩散激活更多
      let s6 = 1.0 + 0.5 * h.correctionProb                      // 纠正时近期记忆更重要

      // temporal query 叠加调制（cognition 不区分 temporal）
      if (isTemporalQ) { s1 += 1.0; s6 += 2.0; s3 *= 0.3; s4 *= 0.5 }
      // entity query 叠加
      if (hasEntityName) { s2 += 0.5; s4 += 1.0 }
      // causal query 叠加
      if (isCausalQ) { s4 += 1.0; s6 += 0.5 }

      return { s1, s2, s3, s4, s6 }
    }
    // Fallback: 旧 IMAF 正则（无 cogHints 时）
    if (/为什么|原因|导致|why|because|cause|reason|how come/i.test(query))
      return { s1: 1.0, s2: 1.0, s3: 0.5, s4: 2.0, s6: 1.5 }
    if (/什么时候|上次|上周|when did|last time|recently|what happened|ago/i.test(query))
      return { s1: 2.0, s2: 0.8, s3: 0.3, s4: 0.5, s6: 3.0 }
    if (query.match(/\b[A-Z][a-z]{2,}\b/g)?.filter(n => !/^(What|When|Where|How|Who|Which|Why|The|This|That|Does|Did|Has|Have|Was|Were|Can|Could)$/.test(n)).length)
      return { s1: 0.8, s2: 1.5, s3: 0.5, s4: 2.0, s6: 0.8 }
    if (/感觉|心情|开心|难过|焦虑|feel|happy|sad|anxious|stressed|mood/i.test(query))
      return { s1: 0.8, s2: 1.0, s3: 2.0, s4: 0.5, s6: 0.5 }
    return { s1: 1.0, s2: 1.0, s3: 1.0, s4: 1.0, s6: 1.0 }
  })()

  // 预计算记忆平均文档长度（BM25 标准分母，替代 expandedWords.size）
  _currentAvgDocLen = memories.reduce((s, m) => s + ((m.content || '').match(/[\u4e00-\u9fff]|[a-zA-Z]+/g) || []).length, 0) / Math.max(memories.length, 1)

  // 构建动态 IDF 缓存（版本化：只在 invalidateFieldIDF 被调用后才重建）
  if (!_idfCache || _currentIdfVersion !== _idfVersion) {
    _idfCache = buildIdfCache(memories)
    _currentIdfVersion = _idfVersion
  }

  // 构建实体共振场（ERF）— 一次性，供 spreadingActivation Path C 使用
  _erfCache = buildEntityResonanceField(query, memories)



  // SSH: Seed-Based Semantic Hashing（英文 only，中文 seeds 维度太广会误匹配）
  _sshMemDims = new Map()
  _sshDimFreqMap = new Map()
  _sshQueryDims = new Set()
  if (!/[\u4e00-\u9fff]/.test(query)) {
    try {
      const { getSemanticDimensions: _getSSD } = require('./aam.ts')
      if (_getSSD) {
        for (const mem of memories) {
          const cl = (mem.content || '').toLowerCase()
          const ws = cl.match(/[a-zA-Z]{3,}/gi) || []
          const dims = new Set<string>()
          for (const w of ws.slice(0, 20)) {
            const wd = _getSSD(w.toLowerCase())
            for (const d of wd) dims.add(d)
          }
          if (dims.size > 0) {
            _sshMemDims.set(cl, dims)
            for (const d of dims) _sshDimFreqMap.set(d, (_sshDimFreqMap.get(d) || 0) + 1)
          }
        }
        for (const [w, wt] of expandedWords) {
          if ((wt as number) >= 0.5) {
            const wd = _getSSD(w)
            for (const d of wd) _sshQueryDims.add(d)
          }
        }
      }
    } catch {}
  }

  // 预建 AAM neighbor 缓存 — 把查询词的 1-hop AAM 邻居预计算好
  // 供 spreadingActivation Path B 用，避免每条记忆重复 PMI 计算（O(N²) → O(N)）
  _aamNeighborCache = new Map()
  try {
    const fn = getAAMNeighborsFn()
    if (fn) {
      const queryWords = new Set(
        (query.toLowerCase().match(WORD_PATTERN.CJK24_EN3) || []).map(w => w.toLowerCase())
      )
      // 对每个查询词，找其 AAM 邻居，记录 word → score
      for (const qw of queryWords) {
        const neighbors = fn(qw, 5)
        for (const n of neighbors) {
          const fanDamping = 1 / Math.sqrt(Math.max(1, n.fanOut))
          const score = n.pmiScore / 5 * fanDamping
          const existing = _aamNeighborCache.get(n.word) || 0
          if (score > existing) _aamNeighborCache.set(n.word, score)
        }
      }
    }
  } catch {}

  const results: ActivationResult[] = []
  const currentTop: Memory[] = []  // 用于干扰抑制

  // 构建查询词集合（供 encoding specificity + temporal co-occurrence 使用）
  const queryWordSet = new Set<string>()
  const queryLower = query.toLowerCase()
  const qCjk = queryLower.match(/[\u4e00-\u9fff]{2,4}/g) || []
  for (const s of qCjk) queryWordSet.add(s)
  const qEn = queryLower.match(/[a-zA-Z]{3,}/gi) || []
  for (const w of qEn) queryWordSet.add(w.toLowerCase())

  // Signal 7: 预计算 temporal co-occurrence successors（PAM directed）
  let temporalSuccessors: Set<string> | null = null
  try {
    if (_aamGetTemporalSuccessors) {
      temporalSuccessors = new Set<string>()
      for (const qw of queryWordSet) {
        const succs = _aamGetTemporalSuccessors(qw, 5)
        if (succs) for (const s of succs) temporalSuccessors.add(s.word)
      }
    }
  } catch {}

  // 冷启动检测：如果 _activations 几乎为空（< 10 条），说明没有历史交互
  // Signal 4 (spread) 和 Signal 7 (PAM) 不会贡献分数，context 应该主导
  const isColdStart = _activations.size < 10
  if (isColdStart) {
    _baseWeight = 0.15
    _contextWeight = 0.85
  }

  // 第一遍：计算原始激活值（不含干扰抑制）
  const rawResults: { mem: Memory; raw: number; signals: any; path: TraceStep[] }[] = []

  for (const mem of memories) {
    if (mem.scope === 'expired' || mem.scope === 'decayed') continue
    if (!mem.content || mem.content.length < 3) continue

    const s1 = baseActivation(mem, now)
    const s2 = contextMatch(query, mem, expandedWords, s1)
    // 下限保护：s2 极低的记忆跳过（恢复硬过滤，但阈值从 0.005 降到 0.002）
    // 原因：s2=0.0005 的底分 + 高 base activation 会挤掉真正相关的弱匹配记忆
    if (s2 < 0.002) continue
    const s3 = emotionResonance(mem, mood, alertness)
    const s4 = spreadingActivation(mem, memories, query)
    const s6 = temporalContext(mem, timeRange, queryWordSet)

    // ── 加法融合（base + context）× 乘法调制（emotion × spread × temporal）──
    // 核心改变：base 和 context 从乘法改为加法
    // 原因：乘法下 base 的 365x 动态范围碾压 context 的 20x，旧但相关的记忆永远输给新但无关的
    // 加法下：score = 0.3×base + 0.7×context，context 有独立贡献，不被 base 乘没
    // 权重由 Recall Thermostat 动态调节（默认 0.3/0.7）
    const { base: wBase, context: wCtx } = getSignalWeights()
    const baseContextScore = wBase * _imaf.s1 * s1 + wCtx * _imaf.s2 * s2

    // IMAF 意图调制 + Thermostat 自适应
    const raw = baseContextScore * (0.5 + _emotionCoeff * _imaf.s3 * s3) * (1 + _spreadCoeff * _imaf.s4 * s4) * (0.8 + _temporalCoeff * _imaf.s6 * s6)

    // confidence 软缩放（不是乘法杀死，是 0.6-1.0 区间）
    const conf = mem.confidence ?? 0.7
    const confScale = 0.6 + conf * 0.4

    // importance 加成（surprise 编码的结果）
    // importance 线性插值替代二值跳跃（imp=5→1.0, imp=8→1.15, imp=10→1.25）
    let impBoost = 1 + Math.max(0, ((mem.importance ?? 5) - 5)) * 0.05
    // 纠正免疫：correction scope 的记忆永久加权（向量做不到——语义距离无法区分纠正前后）
    if (mem.scope === 'correction') impBoost *= 1.5
    // 被纠正的记忆（有 supersededBy）永久降权
    if ((mem as any).supersededBy) impBoost *= 0.3

    // Signal 7: PAM Temporal Co-occurrence（有向共现加成）
    // 用户先说 A 再说 B → 下次说 A 时，含 B 的记忆获得 boost
    let s7 = 0
    if (temporalSuccessors && temporalSuccessors.size > 0) {
      const memContentLower = (mem.content || '').toLowerCase()
      const memW = (memContentLower.match(WORD_PATTERN.CJK24_EN3) || [])
      let hits = 0
      for (const w of memW) {
        if (temporalSuccessors.has(w.toLowerCase())) hits++
        if (hits >= 3) break  // cap contribution
      }
      s7 = Math.min(0.3, hits * 0.1)  // 提升：each hit +0.1, max +0.3（对话惯性是 NAM 独有优势）
    }

    // 对话惯性加成（momentum boost，由 _momentumCoeff 调制）
    const momentum = getMomentumBoost(mem.content || '')

    // Signal 8: Prospective Tag Match（前瞻性标签命中——零 LLM doc2query）
    let s8 = 0
    if ((mem as any).prospectiveTags?.length > 0) {
      let ptHits = 0
      for (const tag of (mem as any).prospectiveTags) {
        const tl = tag.toLowerCase()
        if (expandedWords.has(tl) || queryLower.includes(tl)) ptHits++
      }
      if (ptHits > 0) s8 = Math.min(1.0, ptHits / (mem as any).prospectiveTags.length * 2)
    }

    // MemRL utility modulation
    const utilityMod = 1 + ((mem as any).utility ?? 0) * 0.1

    // ── Signal 9: microLinks history boost（曾被成功召回的记忆更可信）──
    let microLinkBoost = 1.0
    if (mem.microLinks && mem.microLinks.length > 0) {
      // 检查 microLinks 中是否有跟当前查询相关的历史召回
      const qWords = new Set((queryLower.match(WORD_PATTERN.CJK2_EN3) || []).map((w: string) => w.toLowerCase()))
      let linkHits = 0
      for (const link of mem.microLinks) {
        if (link.sharedKeywords?.some((k: string) => qWords.has(k.toLowerCase()))) linkHits++
      }
      if (linkHits > 0) microLinkBoost = 1 + Math.min(0.2, linkHits * 0.05)  // max +20%
    }

    // ── Signal 10: insight/reflexion 记忆优先（蒸馏后的高质量信号）──
    const insightBoost = (mem.scope === 'insight' || mem.scope === 'reflexion') ? 1.15 : 1.0

    // ── Signal 11: person-model 上下文调制（用户画像驱动召回偏好）──
    // 技术型用户偏重 fact/tech 记忆，情感型用户偏重 event/emotion 记忆
    let personModelMod = 1.0
    try {
      const { getPersonModel } = require('./person-model.ts')
      const pm = getPersonModel()
      if (pm?.thinkingStyle) {
        const style = pm.thinkingStyle
        if (style === 'analytical' && (mem.scope === 'fact' || mem.tags?.some((t: string) => t.includes('tech')))) personModelMod = 1.1
        if (style === 'emotional' && (mem.scope === 'event' || mem.tags?.some((t: string) => t.includes('emotion')))) personModelMod = 1.1
      }
    } catch {}

    const catWeight = getCategoryWeight(mem)
    const finalRaw = raw * confScale * impBoost * (1 + _momentumCoeff * momentum) * (1 + _pamCoeff * s7) * (1 + s8 * 0.5) * utilityMod * catWeight * microLinkBoost * insightBoost * personModelMod

    // 构建 trace path
    const path: TraceStep[] = [
      { stage: 'candidate_selection', via: s2 > 0.3 ? 'aam_context' : 'bm25', rawScore: s2 },
      { stage: 'signal_boost', via: 'base_activation', rawScore: s1 },
    ]
    if (s3 > 0.6) path.push({ stage: 'signal_boost', via: 'emotion', rawScore: s3 })
    if (s4 > 0.05) path.push({ stage: 'signal_boost', via: 'spread', rawScore: s4 })
    if (s6 > 0.7) path.push({ stage: 'signal_boost', via: 'temporal', rawScore: s6 })
    if (confScale > 0.8) path.push({ stage: 'signal_boost', via: 'confidence', rawScore: confScale })
    if (impBoost > 1.0) path.push({ stage: 'signal_boost', via: 'importance', rawScore: impBoost })
    if (momentum > 0.05) path.push({ stage: 'signal_boost', via: 'momentum', rawScore: momentum })
    if (s7 > 0.01) path.push({ stage: 'signal_boost', via: 'temporal_cooccur', rawScore: s7 })

    if (finalRaw > 0.001) {  // 候选门槛极低，靠排序筛选而非硬阈值
      rawResults.push({
        mem, raw: finalRaw,
        signals: { base: s1, context: s2, emotion: s3, spread: s4, interference: 1.0, temporal: s6 },
        path,
      })
    }
  }

  // 排序
  rawResults.sort((a, b) => b.raw - a.raw)

  // ── 存入时序 PAM：同批存入的记忆互相 boost ──
  // 同一次 feedback 存入的记忆 ts 差距 < 5s，天然具有语义关联
  // top-3 候选的同批记忆获得 20% boost（零冷启动，不依赖学习数据）
  const PAM_TS_WINDOW = 5000  // 5 秒窗口
  const PAM_BATCH_BOOST = 1.2
  const topK = Math.min(3, rawResults.length)
  for (let i = topK; i < rawResults.length; i++) {
    const cTs = rawResults[i].mem.ts || 0
    for (let j = 0; j < topK; j++) {
      const tTs = rawResults[j].mem.ts || 0
      if (Math.abs(cTs - tTs) < PAM_TS_WINDOW && rawResults[i].mem.content !== rawResults[j].mem.content) {
        rawResults[i].raw *= PAM_BATCH_BOOST
        break  // 只 boost 一次
      }
    }
  }
  // boost 后重排
  rawResults.sort((a, b) => b.raw - a.raw)

  // 第二遍：MMR 干扰抑制（已选的会压制后续的相似记忆）
  // Pre-cache trigrams for all candidates to avoid O(N²) recomputation
  const _trigramCache = new Map<string, Set<string>>()
  const _getTriCached = (content: string): Set<string> => {
    let tri = _trigramCache.get(content)
    if (!tri) { tri = trigrams(content); _trigramCache.set(content, tri) }
    return tri
  }
  const selectedTris: Set<string>[] = []  // trigrams of selected memories (for MMR)
  const selectedAges: number[] = []      // ages of selected memories (for A3 SIMPLE)

  for (const r of rawResults) {
    const memContent = r.mem.content || ''
    const memTri = _getTriCached(memContent)
    const isSummary = r.mem.scope === 'fact' || r.mem.scope === 'consolidated'
      || memContent.startsWith('[summary]') || memContent.startsWith('[Session')
    const memAge = now - (r.mem.ts || now)
    const s5 = interferenceMMR(memTri, selectedTris, isSummary, memAge, selectedAges)
    let activation = r.raw * s5

    // ── Semantic drift modifier：上升话题 boost，下降话题 slight reduction ──
    try {
      const content = r.mem.content || ''
      const contentWords = (content.match(WORD_PATTERN.CJK2_EN3) || [])
      let driftMod = 1.0
      for (const w of contentWords.slice(0, 5)) {
        const m = _getDriftModifier(w.toLowerCase())
        if (m !== 1.0) { driftMod = m; break }  // 取第一个有信号的词
      }
      activation *= driftMod
    } catch {}

    // ── Confidence cascade modifier：高置信 boost，低置信 penalize ──
    try {
      activation *= _getConfModifier(r.mem)
    } catch {}

    r.signals.interference = s5

    // trace: 记录干扰抑制
    if (s5 < 1.0) r.path.push({ stage: 'signal_suppress', via: 'interference', rawScore: s5 })

    // 更新激活值缓存
    setActivation(r.mem, activation)

    // 阈值：只过滤绝对零分（排序已经保证质量，不需要严格阈值）
    if (activation > 0.001) {
      results.push({
        memory: r.mem,
        activation,
        signals: r.signals,
        path: r.path,
      })
      currentTop.push(r.mem)
      selectedTris.push(memTri)
      selectedAges.push(memAge)
    }

    if (results.length >= topN) break
  }

  // ── Retrieval-Induced Forgetting (Anderson et al. 1994) ──
  // 被选中的记忆强化激活，竞争失败但相似的 runner-up 降低激活值
  // 与 interferenceSuppress 不同：interference 是当轮排序压制，RIF 是跨轮持久衰减
  if (results.length > 0) {
    const selectedContents = new Set(results.map(r => (r.memory.content || '').slice(0, 50)))
    const selectedWords = new Set<string>()
    for (const r of results) {
      const ws = ((r.memory.content || '').match(WORD_PATTERN.CJK2_EN3) || [])
      for (const w of ws) selectedWords.add(w.toLowerCase())
    }
    // runner-ups: rawResults 中排名靠后、未入选、但与选中记忆词重叠高的
    const rifStart = Math.min(results.length, rawResults.length)
    const rifEnd = Math.min(rifStart + 30, rawResults.length)
    for (let i = rifStart; i < rifEnd; i++) {
      const r = rawResults[i]
      if (selectedContents.has((r.mem.content || '').slice(0, 50))) continue
      if (r.mem.scope === 'core_memory' || r.mem.scope === 'correction') continue
      const mw = ((r.mem.content || '').match(WORD_PATTERN.CJK2_EN3) || [])
      let overlap = 0
      for (const w of mw) { if (selectedWords.has(w.toLowerCase())) overlap++ }
      if (mw.length > 0 && overlap / mw.length > 0.4) {
        // 持久性轻微降低激活值（-5%）
        const curAct = getActivation(r.mem)
        if (curAct > 0.05) setActivation(r.mem, curAct * 0.95)
      }
    }
  }

  // 记录 trace + rejection log
  const turnTs = Date.now()
  const traces: ActivationTrace[] = results.map(r => ({
    memory: r.memory, score: r.activation, path: r.path || []
  }))

  // Rejection log：top-20 中没进 results 的
  const rejections: RejectionRecord[] = []
  const selectedSet = new Set(results.map(r => memKey(r.memory)))
  for (let i = 0; i < Math.min(20, rawResults.length); i++) {
    if (!selectedSet.has(memKey(rawResults[i].mem))) {
      rejections.push({
        content: (rawResults[i].mem.content || '').slice(0, 30),
        originalRank: i + 1,
        finalRank: -1,
        reason: rawResults[i].signals.interference < 1.0 ? 'interference' : 'below_threshold',
      })
    }
  }

  _traceBuffer.set(turnTs, { traces, rejections })
  pruneTraceBuffer()

  return results
}

// ═══════════════════════════════════════════════════════════════
// 每分钟 tick：自然衰减
// ═══════════════════════════════════════════════════════════════

export function decayAllActivations(factor: number = 0.995) {
  for (const [key, val] of _activations) {
    const newVal = val * factor
    if (newVal < 0.01) {
      _activations.delete(key)
    } else {
      _activations.set(key, newVal)
    }
  }
}

// ═══════════════════════════════════════════════════════════════
// 查询扩展（复用 AAM 的 PMI 网络）
// ═══════════════════════════════════════════════════════════════

// 英文停用词（高频功能词，不应作为查询关键词）
const EN_STOP_WORDS = new Set([
  'the', 'and', 'for', 'that', 'this', 'with', 'from', 'are', 'was', 'were',
  'not', 'but', 'have', 'has', 'had', 'will', 'can', 'you', 'your', 'they',
  'them', 'their', 'what', 'when', 'where', 'which', 'who', 'whom', 'how',
  'did', 'does', 'would', 'could', 'should', 'been', 'being', 'its', 'she',
  'her', 'his', 'him', 'all', 'also', 'than', 'then', 'some', 'such',
  'about', 'after', 'before', 'between', 'into', 'through', 'during',
  'each', 'very', 'just', 'other', 'more', 'most', 'only', 'over',
])

export function expandQueryForField(query: string): Map<string, number> {
  const expanded = new Map<string, number>()

  // CJK: 2-char sliding window（跟 AAM tokenizer 一致）
  const cjkSegs = query.match(/[\u4e00-\u9fff]+/g) || []
  for (const seg of cjkSegs) {
    // 2-char sliding window
    for (let i = 0; i <= seg.length - 2; i++) expanded.set(seg.slice(i, i + 2), 1.0)
    // 完整 3-4 字词也加入（如 "减肥期"）
    if (seg.length >= 3 && seg.length <= 4) expanded.set(seg, 1.0)
  }
  // English: 2+ letter words + numbers, 停用词降权 + Porter stemming
  const _QUERY_SIGNAL_WORDS = new Set(['what','where','when','how','which','did','does','who','whom'])
  const enWords = query.match(/[a-zA-Z]{2,}|\d+/gi) || []
  for (const w of enWords) {
    const wl = w.toLowerCase()
    const weight = _QUERY_SIGNAL_WORDS.has(wl) ? 0.5 : EN_STOP_WORDS.has(wl) ? 0.1 : 1.0
    expanded.set(wl, weight)
    // Also add stemmed form for English words (e.g. "phobias" → "phobia")
    if (/^[a-zA-Z]{2,}$/.test(w)) {
      const stemmed = porterStem(wl)
      if (stemmed !== wl && !expanded.has(stemmed)) expanded.set(stemmed, weight)
    }
  }

  // 短查询：单字 CJK 也加入（在 AAM 扩展之前，确保"车"等单字能参与扩展）
  if (query.length < 15) {
    const singleChars = query.match(/[\u4e00-\u9fff]/g) || []
    for (const ch of singleChars) {
      if (!expanded.has(ch)) expanded.set(ch, 0.5)
    }
  }

  // AAM 查询扩展（同义词 + 概念层级 + 共字关联 + PMI）
  // 直接 import，不用 require（ESM 兼容）
  const KNOWN_SINGLE_CJK = new Set('吃喝睡走跑坐站看听说写读洗穿买卖车钱房书药酒茶怕蛇猫狗鱼学玩住飞骑游'.split(''))
  const queryWords: string[] = []
  for (const [w, wt] of expanded) {
    if ((wt as number) < 0.3) continue
    if (w.length === 1 && /[\u4e00-\u9fff]/.test(w)) {
      if (KNOWN_SINGLE_CJK.has(w)) queryWords.push(w)
    } else if (w.length < 2) {
      // skip
    } else if (/[a-zA-Z]/.test(w) || w.length >= 3) {
      queryWords.push(w)
    } else {
      if (_aamIsKnownWord(w)) queryWords.push(w)
    }
  }
  // ── 查询抽象度感知：抽象查询放宽 AAM 扩展参数 ──
  // Bower 认知网络模型：抽象概念激活范围比具体概念更广
  // 向量做不到：向量不知道 "通勤方式" 该搜宽、"血压" 该搜窄
  const _ABSTRACT_WORDS = new Set([
    '方式', '习惯', '品味', '爱好', '特点', '性格', '规划', '想法',
    '压力', '负担', '活动', '情况', '经历', '偏好', '风格', '水平',
    '能力', '状况', '态度', '目标', '计划', '条件', '背景', '圈子',
    'style', 'habit', 'taste', 'hobby', 'trait', 'plan', 'idea',
    'preference', 'routine', 'activity', 'experience', 'skill',
  ])
  const _contentWords = queryWords.filter(w => !EN_STOP_WORDS.has(w) && w.length >= 2)
  const _queryAbstract = _contentWords.length > 0 && _contentWords.some(w => _ABSTRACT_WORDS.has(w))

  try {
    const _aamMaxExp = _queryAbstract ? 30 : 20
    const _aamMinW = _queryAbstract ? 0.1 : 0.15
    const aamExpanded = _aamExpandQuery(queryWords, _aamMaxExp)
    for (const { word, weight } of aamExpanded) {
      if (weight >= _aamMinW && !expanded.has(word)) {
        // A7: Cue Overload penalty — words hitting too many memories are less diagnostic
        // IDF naturally captures this: low IDF = high df = many hits = less diagnostic
        const idf = _idfCache?.get(word) ?? 0.5
        const adjustedWeight = weight * Math.max(0.3, idf)  // floor at 30% to avoid killing useful expansions
        expanded.set(word, adjustedWeight)
      }
    }
    if (_queryAbstract) {
      console.log(`[activation-field] abstract query detected: maxExp=${_aamMaxExp}, minW=${_aamMinW}, expanded=${expanded.size}`)
    }
  } catch {}

  // 短查询降低门槛：单字 CJK 也加入
  if (query.length < 10) {
    const singleChars = query.match(/[\u4e00-\u9fff]/g) || []
    for (const ch of singleChars) {
      if (!expanded.has(ch)) expanded.set(ch, 0.3)
    }
  }

  // Single-char CJK that are synonym table keys → promote to expansion candidates
  try {
    for (const [w, wt] of [...expanded.entries()]) {
      if (w.length === 1 && /[\u4e00-\u9fff]/.test(w) && (wt as number) <= 0.3) {
        if (_aamIsKnownWord(w)) {
          expanded.set(w, 0.8)
        }
      }
    }
  } catch {}

  // ── 行为预测扩展：predictNextTopic 的预测词注入查询（产品模式）──
  if (!process.env.CC_SOUL_BENCHMARK) {
    try {
      const { getTopPredictions } = require('./behavioral-phase-space.ts')
      const predictions = getTopPredictions?.(3) || []
      for (const pred of predictions) {
        const word = (pred.topic || pred.word || '').toLowerCase()
        if (word.length >= 2 && !expanded.has(word)) {
          expanded.set(word, (pred.probability || 0.3) * 0.3)  // 预测词低权重，不干扰主查询
        }
      }
    } catch {}
  }

  return expanded
}

// ═══════════════════════════════════════════════════════════════
// 统一入口：替代 recall()
// ═══════════════════════════════════════════════════════════════

export function activationRecall(
  memories: Memory[],
  query: string,
  topN: number = 5,
  mood: number = 0,
  alertness: number = 0.5,
  cogHints?: CogHints | null,
): Memory[] {
  if (!query || memories.length === 0) return []

  // 提取查询中的人名（英文大写开头 + 中文姓氏）
  const _queryNames: string[] = []
  const _enNameCandidates = query.match(/\b([A-Z][a-z]{2,})\b/g) || []
  const _NON_NAMES = new Set(['What','When','Where','Which','Who','How','Why','The','This','That','Does','Did','Has','Have','Was','Were','Can','Could','Would','Should','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'])
  for (const n of _enNameCandidates) {
    if (!_NON_NAMES.has(n)) _queryNames.push(n.toLowerCase())
  }

  // ── 聚合查询自适应：分数平坦度判定（完全动态，零硬编码正则）──
  let _isAggregation = false
  const _originalTopN = topN

  // 查询类型检测（adaptive k1/b）
  _currentQueryType = detectQueryType(query)

  // temporal 查询需要更多候选做时间排序比较
  if (_currentQueryType === 'temporal') {
    topN = Math.max(topN, 10)
  }

  // 查询扩展
  const expanded = expandQueryForField(query)

  // 更新对话惯性 momentum
  updateMomentum(query)

  // ── Triple Query Decomposition（三层查询分解）──
  // 1. 时间通道：提取时间范围（精确时间过滤，替代新近性衰减）
  let timeRange: TimeRange | null = null
  try {
    timeRange = _extractTimeRange(query)  // 顶层 import，ESM 安全
  } catch {}

  // 1.2 时间锚推理：当正则提取失败时，从高情绪记忆推断时间范围
  if (!timeRange) {
    try {
      const anchors = _extractAnchors(memories)
      if (anchors.length > 0) {
        const inferred = _inferTemporalRange(query, anchors)
        if (inferred) {
          timeRange = { fromMs: inferred.from, toMs: inferred.to }
          console.log(`[activation-field] temporal-anchor: inferred range [${new Date(inferred.from).toLocaleDateString()} ~ ${new Date(inferred.to).toLocaleDateString()}] from ${anchors.length} anchors`)
        }
      }
    } catch {}
  }

  // 1.5 隐含时间感知（向量做不到——向量不知道"最近"意味着什么）
  let recencyBias = 0  // 0=no bias, >0=天数(偏好近N天), -1=偏好旧记忆
  if (!timeRange) {
    if (/最近|目前|现在|these days|lately|recently/i.test(query)) recencyBias = 7
    if (/以前|之前|曾经|过去|当年|before|used to/i.test(query)) recencyBias = -1
  }

  // 2. 关键词通道：去停用词后的 BM25 关键词（更精准的词法匹配）
  let lexicalQuery = query
  try {
    const keywords: string[] = _extractTagsLocal(query)  // 顶层 import，ESM 安全
    if (keywords.length > 0) lexicalQuery = keywords.join(' ')
  } catch {}

  // 3. 实体通道：图谱实体（已在下方 graph expansion 中处理）
  // 4. AAM 通道：保持使用完整原始 query（联想需要完整语境）

  // ── 否定查询识别：搜索负面经历而非正面事实 ──
  // "不擅长什么" → 搜 correction scope + painful emotion 的记忆
  // 否定检测是语法特征（硬编码），扩展走 AAM + scope/emotion 标签（动态）
  const _NEG_PATTERNS = /不擅长|不喜欢|不爱|不想|不敢|不吃|不看|不会|害怕|讨厌|恐惧|反感|忌口|don't like|afraid of|hate|bad at|can't stand/i
  const _NEG_QUESTION = /什么|吗|呢|哪|几|\?|？/
  const _isNegationQuery = _NEG_PATTERNS.test(query) && _NEG_QUESTION.test(query)

  if (_isNegationQuery) {
    const _negSeedWords = ['放弃', '失败', '不会', '怕', '讨厌', '难', '差', '糟', '亏',
      'quit', 'failed', 'afraid', 'hate', 'bad', 'lost']
    for (const nw of _negSeedWords) {
      if (!expanded.has(nw)) expanded.set(nw, 0.5)
    }
    try {
      const negExpanded = _aamExpandQuery(_negSeedWords.filter(w => w.length >= 2), 10)
      for (const { word, weight } of negExpanded) {
        if (!expanded.has(word)) expanded.set(word, weight * 0.6)
      }
    } catch {}
    console.log(`[activation-field] negation query detected, expanded +${_negSeedWords.length} neg seeds`)
  }

  // ── Category Pre-Pruning：按领域预筛，减少候选池 ──
  // 在 computeActivationField 之前执行，同时加速 IDF 缓存构建
  memories = categoryPrePrune(memories, query)

  // ── Parallel Channel: fact-store 关键词召回（与 NAM 并行，最终融合）──
  // 遍历所有已存三元组，用查询词+AAM扩展词评分，不短路，结果在 NAM 之后融合
  let _parallelFactMems: Memory[] = []
  try {
    const factStore = _factStoreMod
    const allFacts = factStore.getAllFacts() as { subject: string; predicate: string; object: string; ts?: number; confidence?: number; validUntil?: number }[]
    const queryLowerS1 = query.toLowerCase()
    // 提取查询关键词（CJK 2-gram + 英文 2+ 字母 + 数字）
    const queryTokensS1 = new Set((queryLowerS1.match(WORD_PATTERN.CJK24_EN2_NUM) || []).map(w => w.toLowerCase()))
    // AAM 扩展词也参与匹配（扩展语义覆盖面）
    for (const [w] of expanded) queryTokensS1.add(w.toLowerCase())

    const scoredFacts: { mem: Memory; matchScore: number }[] = []
    for (const fact of allFacts) {
      if (fact.validUntil && fact.validUntil > 0 && fact.validUntil < Date.now()) continue  // 已失效
      const objLower = (fact.object || '').toLowerCase()
      const predLower = (fact.predicate || '').toLowerCase()
      const subjLower = (fact.subject || '').toLowerCase()
      const factText = `${subjLower} ${predLower} ${objLower}`
      const factTokens = (factText.match(WORD_PATTERN.CJK24_EN2_NUM) || []).map(w => w.toLowerCase())

      // 双向匹配评分（不只 boolean，而是 overlap 程度）
      let matchScore = 0
      // 1. 查询词 → fact 字段（"猫" in "一只叫豆豆的猫"）
      for (const token of queryTokensS1) {
        if (objLower.includes(token) || token.includes(objLower)) matchScore += 2  // object 命中权重高
        if (predLower.includes(token)) matchScore += 1.5  // predicate 命中
        if (subjLower.includes(token)) matchScore += 0.5  // subject 命中（通常是 "user"，低权重）
      }
      // 2. fact 的词 → 查询词集合（"PostgreSQL" in queryTokens）
      for (const ft of factTokens) {
        if (queryTokensS1.has(ft)) matchScore += 1
      }
      // 3. confidence 加权
      matchScore *= (fact.confidence || 0.7)

      if (matchScore > 0) {
        scoredFacts.push({
          mem: {
            content: `[事实] ${fact.predicate}: ${fact.object}`,
            scope: 'fact', ts: fact.ts || Date.now(), confidence: fact.confidence || 0.9,
            source: 'fact_store_parallel',
            recallCount: 10, lastAccessed: Date.now(), importance: 9,
          } as Memory,
          matchScore,
        })
      }
    }
    // 按评分排序 + 去重（同一 predicate 只取 top 2）
    scoredFacts.sort((a, b) => b.matchScore - a.matchScore)
    const predCount = new Map<string, number>()
    for (const sf of scoredFacts) {
      const pred = sf.mem.content.match(/\[事实\]\s*([^:]+)/)?.[1] || ''
      const count = predCount.get(pred) || 0
      if (count < 2) { (sf.mem as any)._matchScore = sf.matchScore; _parallelFactMems.push(sf.mem); predCount.set(pred, count + 1) }
    }
    if (_parallelFactMems.length > 0) {
      console.log(`[activation-field] fact-store parallel: ${_parallelFactMems.length} facts scored from ${allFacts.length} total`)
    }
  } catch {}

  // ── P5c: cascadeRecall 管线式集成 ──
  // Step 1: AAM 扩展查询词（增强召回率）
  // expanded 已经是 Map<string, number>，直接合并 AAM 扩展词
  try {
    const aamExpansion = _aamExpandQuery(
      (query.match(WORD_PATTERN.CJK2_EN3) || []).map((w: string) => w.toLowerCase()),
      5
    )
    if (aamExpansion.length > 0) {
      for (const exp of aamExpansion) {
        if (!expanded.has(exp.word)) {
          expanded.set(exp.word, exp.weight)
        }
      }
    }
  } catch {}

  // Step 2: 激活场计算（用扩展后的查询，候选集更完整）
  // 过采样倍数：cogHints.complexity 可用时按复杂度调整，否则按池大小
  const _baseOversample = memories.length <= 100 ? 2 : memories.length <= 300 ? 3 : 4
  const _oversample = cogHints ? Math.min(4, Math.max(2, Math.round(_baseOversample * (0.7 + 0.6 * cogHints.complexity)))) : _baseOversample
  let results = computeActivationField(memories, lexicalQuery, mood, alertness, expanded, topN * _oversample, timeRange, cogHints)

  // ── DQR: Dual-Query Recall（双查询召回）——用扩展词重组第二个查询再搜一次 ──
  // 原创：论文证明 dual-query 能提升 6.7%，我们用 AAM 扩展词自动生成第二查询（零 LLM）
  if (results.length > 0 && results[0].activation < 0.5 && expanded.size > 5) {
    // 只在首轮结果不够好时触发（top-1 分数 < 0.3 = 不太确定）
    try {
      // 取 expanded 里权重最高的 5 个非原始词作为第二查询
      const altWords = [...expanded.entries()]
        .filter(([w, wt]) => (wt as number) < 0.95 && (wt as number) >= 0.5 && w.length >= 3)  // 排除原始词
        .sort((a, b) => (b[1] as number) - (a[1] as number))
        .slice(0, 5)
        .map(([w]) => w)
      if (altWords.length >= 2) {
        const altQuery = altWords.join(' ')
        const altExpanded = new Map(expanded)  // 复用已有扩展
        const altResults = computeActivationField(memories, altQuery, mood, alertness, altExpanded, topN * 2, timeRange, cogHints)
        // 合并去重
        const seenContent = new Set(results.map(r => r.memory.content))
        for (const r of altResults) {
          if (!seenContent.has(r.memory.content)) {
            results.push(r)
            seenContent.add(r.memory.content)
          }
        }
        results.sort((a, b) => b.activation - a.activation)
      }
    } catch {}
  }

  // ── Entity-Focused Reformulation（原创：实体焦点查询改写）──
  // "What instruments does Melanie play?" → 额外搜 "Melanie play"（只保留实体+动词）
  // 原理：长查询的 BM25 被疑问词（what/does）和概念词（instruments）分散了
  // 短查询只含实体+动词，BM25 更聚焦到包含该人实际行为的记忆
  if (_queryNames && _queryNames.length >= 1 && results.length > 0 && results[0].activation < 0.8) {
    try {
      const verbs = (lexicalQuery.match(/\b[a-z]{3,}(?:ed|ing|s|es)?\b/gi) || [])
        .filter(w => !EN_STOP_WORDS.has(w.toLowerCase()) && !_queryNames.includes(w.toLowerCase()))
        .slice(0, 3)
      if (verbs.length >= 1) {
        const focusedQuery = _queryNames.join(' ') + ' ' + verbs.join(' ')
        const focusedResults = computeActivationField(memories, focusedQuery, mood, alertness, expanded, topN * 2, timeRange, cogHints)
        const seenContent = new Set(results.map(r => r.memory.content))
        for (const r of focusedResults) {
          if (!seenContent.has(r.memory.content)) {
            results.push(r)
            seenContent.add(r.memory.content)
          }
        }
        results.sort((a, b) => b.activation - a.activation)
      }
    } catch {}
  }

  // ── Temporal Entity Expansion：推理型查询用纯实体名做第二轮 recall ──
  // "Would Caroline be religious?" → 第二轮用 "Caroline" 搜索，补充该人的全面信息
  // 只对 temporal 查询且有实体名时触发
  if (_currentQueryType === 'temporal' && _queryNames && _queryNames.length >= 1 && results.length > 0) {
    try {
      const entityQuery = _queryNames.join(' ')
      const entityResults = computeActivationField(memories, entityQuery, mood, alertness, expanded, topN, timeRange, cogHints)
      const seenContent = new Set(results.map(r => r.memory.content))
      let added = 0
      for (const r of entityResults) {
        if (!seenContent.has(r.memory.content)) {
          results.push(r)
          seenContent.add(r.memory.content)
          added++
          if (added >= 5) break  // 最多补 5 条实体记忆
        }
      }
      if (added > 0) results.sort((a, b) => b.activation - a.activation)
    } catch {}
  }

  // ── 分数平坦度检测 → 聚合查询自适应 topN ──
  // 无明显赢家 = 查询需要综合多条记忆（"我是怎样的人"/"描述我的一天"）
  if (results.length >= 5) {
    const _scores = results.slice(0, Math.min(10, results.length)).map(r => r.activation)
    const _topScore = _scores[0]
    const _tailScore = _scores[_scores.length - 1]
    const _dropoff = _topScore > 0 ? (_topScore - _tailScore) / _topScore : 1
    let _dropoffThreshold = 0.3
    try { _dropoffThreshold = require('./auto-tune.ts').getParam('recall.aggregation_dropoff') || 0.3 } catch {}

    if (_dropoff < _dropoffThreshold) {
      _isAggregation = true
      topN = Math.max(topN, 8)
      console.log(`[activation-field] aggregation detected: dropoff=${_dropoff.toFixed(3)} < ${_dropoffThreshold}, topN ${_originalTopN}→${topN}`)
    }
  }

  // ── 隐含时间 re-scoring（向量做不到的时间感知）──
  if (recencyBias !== 0 && results.length > 0) {
    // 不修改原始 activation（后续 PRF/fusion 还需要原始值），用 _recencyScore 排序
    const now = Date.now()
    const scored = results.map(r => {
      const ageDays = (now - (r.memory.ts || now)) / 86400000
      let boost = 1.0
      if (recencyBias > 0 && ageDays <= recencyBias) boost = 1.5
      if (recencyBias < 0 && ageDays > 30) boost = 1.3
      return { ...r, _recencyScore: r.activation * boost }
    })
    scored.sort((a, b) => b._recencyScore - a._recencyScore)
    results = scored.map(({ _recencyScore, ...r }) => r) as typeof results
    // 注：不改 r.activation，只改排序
  }

  // ── Temporal Tie-Break（原创）：temporal 查询时，含日期的记忆 tie-break 优先 ──
  if (_currentQueryType === 'temporal' && results.length > 1) {
    const DATE_PATTERN = /\b(?:january|february|march|april|may|june|july|august|september|october|november|december)\b|\b\d{4}\b|\b\d{1,2}\s+\w+\s+\d{4}\b/i
    for (const r of results) {
      if (DATE_PATTERN.test(r.memory.content || '')) {
        r.activation *= 1.15  // 15% boost for date-containing memories in temporal queries
      }
    }
    results.sort((a, b) => b.activation - a.activation)
  }

  // ── PRF: Pseudo-Relevance Feedback（伪相关反馈二次召回）──
  // 首轮结果质量不足时触发：top-1 activation < 0.15 或 top-10 覆盖率低
  // PRF：首轮结果质量不足时触发
  const _prfThreshold = results.length >= topN ? 0.15 : 0.03
  if (results.length > 0 && results[0].activation < _prfThreshold) {
    const prfTopN = Math.min(3, results.length)
    const prfKeywords = new Map<string, number>()  // word → IDF weight

    // 从 top-3 结果提取词并用 IDF 加权
    for (let i = 0; i < prfTopN; i++) {
      const content = results[i].memory.content || ''
      const words = (content.match(WORD_PATTERN.CJK24_EN3) || [])
      for (const w of words) {
        const wl = w.toLowerCase()
        if (EN_STOP_WORDS.has(wl)) continue
        const idf = _idfCache?.get(wl) ?? 0.5
        prfKeywords.set(wl, Math.max(prfKeywords.get(wl) || 0, idf))
      }
    }

    // 取 top-5 IDF 最高的词
    const sortedPrfWords = [...prfKeywords.entries()]
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5)

    // 合并到查询扩展词（不覆盖已有的）
    let prfAdded = 0
    for (const [word, idf] of sortedPrfWords) {
      if (!expanded.has(word)) {
        expanded.set(word, idf * 0.5)  // PRF 扩展词降权 50%
        prfAdded++
      }
    }

    if (prfAdded > 0) {
      // 二次召回（PRF flag 内置：只跑 1 轮，不递归）
      const prfResults = computeActivationField(memories, lexicalQuery, mood, alertness, expanded, topN * 2, timeRange, cogHints)

      // 合并 + 去重（by content）
      const seen = new Set(results.map(r => r.memory.content))
      for (const r of prfResults) {
        if (!seen.has(r.memory.content)) {
          results.push(r)
          seen.add(r.memory.content)
        }
      }
      // 重新排序
      results.sort((a, b) => b.activation - a.activation)
      console.log(`[activation-field] PRF: +${prfAdded} keywords, ${prfResults.length} second-pass → ${results.length} merged`)
    }
  }

  // Step 3: CIN 已内置于 computeActivationField 的 6 信号中（contextMatch + interferenceSuppress）
  // 不需要额外 rerank，激活场本身就是多信号融合

  // Step 4: CWRF — 如果有多个独立通道结果，用置信度加权融合
  // （activation field 是统一路径，CWRF 应用于 recallWithScores 的 5 通道融合中）

  // ── 启动效应（Priming Effect）：最近提到的词降低识别阈值 ──
  try {
    if (_primingCacheRef && _primingCacheRef.size > 0) {
      const now = Date.now()
      const PRIMING_WINDOW = 5 * 60 * 1000
      for (const r of results) {
        const words = (r.memory.content.match(WORD_PATTERN.CJK2_EN3) || [])
        let hits = 0
        for (const w of words) {
          const ts = _primingCacheRef.get(w.toLowerCase())
          if (ts && now - ts < PRIMING_WINDOW) hits++
        }
        if (hits > 0 && words.length > 0) {
          const boost = Math.min(0.3, hits / words.length)
          r.activation *= (1 + boost)
          try { require('./decision-log.ts').logDecision('priming', (r.memory.content || '').slice(0, 30), `hits=${hits}/${words.length}, boost=${boost.toFixed(2)}`) } catch {}
        }
      }
      results.sort((a, b) => b.activation - a.activation)
    }
  } catch {}

  // ── 预测性启动（Predictive Priming）：上一轮 AAM 时序后继预热的记忆获得 boost ──
  try {
    if (_predictivePrimingRef && _predictivePrimingRef.size > 0) {
      const now = Date.now()
      const PP_WINDOW = 5 * 60 * 1000
      let ppHits = 0
      for (const r of results) {
        const cached = _predictivePrimingRef.get(r.memory.content)
        if (cached && now - cached.primedAt < PP_WINDOW) {
          // boost 与预测相关度成正比，最多 +25%
          const boost = Math.min(0.25, cached.predictedRelevance * 0.5)
          r.activation *= (1 + boost)
          ppHits++
          try { require('./decision-log.ts').logDecision('predictive_priming_hit', (r.memory.content || '').slice(0, 30), `relevance=${cached.predictedRelevance.toFixed(2)}, boost=${boost.toFixed(2)}, age=${((now - cached.primedAt) / 1000).toFixed(0)}s`) } catch {}
        }
      }
      if (ppHits > 0) results.sort((a, b) => b.activation - a.activation)
    }
  } catch {}

  // ── BM25F 字段加权 rerank（仅 top-50，避免全量计算）──
  const queryLower = lexicalQuery.toLowerCase()
  const SCOPE_KW: Record<string, string[]> = {
    correction: ['纠正','错了','不对','correct','fix'], preference: ['喜欢','偏好','prefer','like'],
    fact: ['事实','知道','记住','fact','know'], event: ['发生','经历','event','happen'],
  }
  const EMO_KW: Record<string, string[]> = {
    warm: ['开心','高兴','快乐','happy'], painful: ['难过','伤心','痛苦','sad'],
    important: ['重要','关键','important'], funny: ['搞笑','好笑','哈哈','funny'],
  }
  for (let i = 0; i < Math.min(50, results.length); i++) {
    const m = results[i].memory
    let bonus = 0
    if (m.tags?.length) { bonus += (m.tags.filter((t: string) => queryLower.includes(t.toLowerCase())).length / m.tags.length) * 3.0 }
    const sk = SCOPE_KW[m.scope || '']; if (sk?.some((k: string) => queryLower.includes(k))) bonus += 1.5
    const ek = EMO_KW[m.emotion || '']; if (ek?.some((k: string) => queryLower.includes(k))) bonus += 2.0
    // 否定查询：correction/painful 记忆加权（冷启动 fallback，不依赖 AAM）
    if (_isNegationQuery) {
      if (m.scope === 'correction') bonus += 2.0
      if (m.emotion === 'painful') bonus += 2.0
    }
    // Summary/蒸馏记忆优先（浓缩了关键事实，天然高质量）
    if (m.tags?.includes('summary') || m.scope === 'fact') bonus += 2.5
    // Speaker 标签匹配：查询指定了 speaker 时优先匹配
    if (m.tags?.length) {
      const speakerMatch = /speaker\s*1|speaker\s*2|user|assistant/i.exec(queryLower)
      if (speakerMatch) {
        const targetRole = /speaker\s*1|user/i.test(speakerMatch[0]) ? 'user' : 'assistant'
        if (m.tags.some((t: string) => t === `speaker:${targetRole}`)) bonus += 2.0
      }
    }
    // Entity name boost：查询含人名时，包含该名字的记忆加权
    if (_queryNames && _queryNames.length > 0) {
      const ml = (m.content || '').toLowerCase()
      for (const name of _queryNames) {
        if (ml.includes(name)) { bonus += 2.5; break }
      }
    }
    results[i].activation *= (1 + Math.min(0.3, bonus / 6.5))
  }
  results.sort((a, b) => b.activation - a.activation)


  // ── Fact-Store Parallel Fusion：facts 按 matchScore 混入 NAM 结果排序 ──
  // 不再强制置顶（activation=1.0 在大候选池里会把低相关 facts 推到 top，污染结果）
  // 改为：facts 的 activation = NAM top-1 的 activation × matchScore 归一化比例
  if (_parallelFactMems.length > 0) {
    const seenContent = new Set(results.map(r => r.memory.content))
    const factResults: ActivationResult[] = []
    const namTopActivation = results.length > 0 ? results[0].activation : 0.5
    for (const fm of _parallelFactMems) {
      if (seenContent.has(fm.content)) continue
      const factObj = fm.content.replace(/^\[事实\]\s*\S+:\s*/, '')
      const hasSimilar = results.some(r => r.memory.content.includes(factObj) && factObj.length >= 2)
      if (hasSimilar) continue
      // matchScore 存在 fm 的临时字段（在上面 fact-store 评分时存入）
      const ms = (fm as any)._matchScore || 3
      // facts activation = NAM top × matchScore 归一化（matchScore 通常 2-10）
      const factActivation = namTopActivation * Math.min(1.0, ms / 6)
      factResults.push({
        memory: fm,
        activation: factActivation,
        signals: { base: 0, context: 1, emotion: 0, spread: 0, interference: 1, temporal: 0 },
      })
      seenContent.add(fm.content)
    }
    if (factResults.length > 0) {
      // 混入排序（不置顶），让高 matchScore 的 facts 自然竞争
      results = [...results, ...factResults]
      results.sort((a, b) => b.activation - a.activation)
      console.log(`[activation-field] fusion: ${factResults.length} facts merged into ${results.length} total results`)
    }
  }

  // ── Graph Walk Fusion：PPR 实体扩散结果混入 NAM 排序 ──
  // graphWalkRecallScored 返回 { content, graphScore }，用分数归一化混入
  try {
    const entities = _graphMod.findMentionedEntities(lexicalQuery)
    if (entities.length > 0) {
      const graphResults = _graphMod.graphWalkRecallScored(entities, memories, 2, topN)
      if (graphResults.length > 0) {
        const seenContent = new Set(results.map(r => r.memory.content))
        const namTopActivation = results.length > 0 ? results[0].activation : 0.5
        const maxGraphScore = graphResults[0].graphScore || 1
        let graphAdded = 0
        for (const gr of graphResults) {
          if (seenContent.has(gr.content)) continue
          const mem = memories.find(m => m.content === gr.content)
          if (!mem) continue
          const graphActivation = namTopActivation * Math.min(1.0, gr.graphScore / maxGraphScore) * 0.8
          results.push({ memory: mem, activation: graphActivation, signals: { base: 0, context: 0, emotion: 0, spread: 1, interference: 1, temporal: 0 } })
          seenContent.add(gr.content)
          graphAdded++
        }
        if (graphAdded > 0) {
          results.sort((a, b) => b.activation - a.activation)
          console.log(`[activation-field] graph-fusion: ${graphAdded} graph memories merged (entities: ${entities.slice(0, 3).join(',')})`)
        }
      }
    }
  } catch {}

  // ── MMR Diversification：最大边际相关性，避免返回过于相似的记忆 ──
  // 聚合查询跳过 MMR：需要同主题多条记忆，MMR 会踢掉它们
  if (results.length > topN && !_isAggregation) {
    const mmrResults: typeof results = []
    const remaining = [...results]
    const LAMBDA = 0.7  // 0.7 relevance, 0.3 diversity

    // Greedily select MMR-optimal memories
    while (mmrResults.length < topN && remaining.length > 0) {
      let bestIdx = 0
      let bestScore = -Infinity

      for (let i = 0; i < remaining.length; i++) {
        const relevance = remaining[i].activation

        // Max similarity to already selected (trigrams() has built-in LRU cache)
        let maxSim = 0
        for (const selected of mmrResults) {
          const sim = trigramSimilarity(
            trigrams(remaining[i].memory.content || ''),
            trigrams(selected.memory.content || '')
          )
          if (sim > maxSim) maxSim = sim
        }

        const mmrScore = LAMBDA * relevance - (1 - LAMBDA) * maxSim
        if (mmrScore > bestScore) {
          bestScore = mmrScore
          bestIdx = i
        }
      }

      mmrResults.push(remaining[bestIdx])
      remaining.splice(bestIdx, 1)
    }

    results = mmrResults
  }

  // ── Segment Cohesion Boost（第二遍）：同 segment/session 的记忆互相印证时加分 ──
  // 人脑原理：回忆一个场景时，整个场景的上下文记忆一起被激活
  // 实现：对当前 top 结果统计各 segment 出现次数，出现 2+ 次的 segment 内记忆获得 boost
  // segment 来源：优先 segmentId 字段，fallback 读 tags 里的 session:N（benchmark 兼容）
  if (results.length >= 4) {
    const getSegment = (mem: any): string | null => {
      if (mem.segmentId !== undefined && mem.segmentId > 0) return `seg:${mem.segmentId}`
      if (mem.tags?.length) {
        const st = mem.tags.find((t: string) => /^session:/.test(t))
        if (st) return st
      }
      return null
    }
    const topSlice = results.slice(0, Math.min(topN * 2, results.length))
    const segCounts = new Map<string, number>()
    for (const r of topSlice) {
      const seg = getSegment(r.memory)
      if (seg) segCounts.set(seg, (segCounts.get(seg) || 0) + 1)
    }
    // 只对出现 2+ 次的 segment 做 boost（单条不算印证）
    let boosted = 0
    for (const r of results) {
      const seg = getSegment(r.memory)
      if (seg) {
        const count = segCounts.get(seg) || 0
        if (count >= 2) {
          r.activation *= 1 + Math.min(0.15, (count - 1) * 0.05)  // 2条+5%, 3条+10%, 上限+15%
          boosted++
        }
      }
    }
    if (boosted > 0) {
      results.sort((a, b) => b.activation - a.activation)
      console.log(`[activation-field] segment-cohesion: boosted ${boosted} memories across ${[...segCounts.values()].filter(v => v >= 2).length} segments`)
    }
  }

  // ── Coverage Rerank：多约束覆盖最大化（multi-hop / 跨实体查询）──
  // 原创算法：从"单条最相关"变成"组合覆盖最多约束"
  // 只在多实体查询时触发，避免对单约束查询引入噪声
  if (_queryNames && _queryNames.length >= 2 && results.length > topN) {
    const constraints = new Set<string>()
    for (const n of _queryNames) constraints.add('entity:' + n)
    const contentWords = (lexicalQuery.match(/[a-z]{4,}/gi) || [])
      .filter(w => !EN_STOP_WORDS.has(w.toLowerCase()))
      .slice(0, 6)
    for (const w of contentWords) constraints.add('kw:' + w.toLowerCase())

    const pool = results.slice(0, topN * 2)
    const selected: typeof results = []
    const uncovered = new Set(constraints)

    while (selected.length < topN && pool.length > 0) {
      let bestIdx = 0, bestScore = -1
      for (let i = 0; i < pool.length; i++) {
        const ml = pool[i].memory.content.toLowerCase()
        let gain = 0
        for (const c of uncovered) {
          if (ml.includes(c.split(':')[1])) gain++
        }
        const rankScore = 1 / (1 + i)
        const combined = 0.6 * rankScore + 0.4 * (gain / Math.max(constraints.size, 1))
        if (combined > bestScore) { bestScore = combined; bestIdx = i }
      }
      const picked = pool.splice(bestIdx, 1)[0]
      selected.push(picked)
      const ml = picked.memory.content.toLowerCase()
      for (const c of [...uncovered]) {
        if (ml.includes(c.split(':')[1])) uncovered.delete(c)
      }
    }
    results = selected
  }

  // ── NAM Coordinator Pattern（原创：协调器式多维度保证召回）──
  if (results.length > topN && topN >= 6) {
    const seen = new Set<string>()
    const coordinated: typeof results = []
    for (const r of results) {
      if (coordinated.length >= Math.ceil(topN * 0.5)) break
      if (!seen.has(r.memory.content)) { coordinated.push(r); seen.add(r.memory.content) }
    }
    const byContext = [...results].sort((a, b) => b.signals.context - a.signals.context)
    for (const r of byContext) {
      if (coordinated.length >= Math.ceil(topN * 0.7)) break
      if (!seen.has(r.memory.content)) { coordinated.push(r); seen.add(r.memory.content) }
    }
    const byBase = [...results].sort((a, b) => b.signals.base - a.signals.base)
    for (const r of byBase) {
      if (coordinated.length >= Math.ceil(topN * 0.9)) break
      if (!seen.has(r.memory.content)) { coordinated.push(r); seen.add(r.memory.content) }
    }
    if (_currentQueryType === 'temporal') {
      const byTemporal = [...results].sort((a, b) => b.signals.temporal - a.signals.temporal)
      for (const r of byTemporal) {
        if (coordinated.length >= topN - 1) break
        if (!seen.has(r.memory.content) && r.signals.temporal > 0) { coordinated.push(r); seen.add(r.memory.content) }
      }
    }
    const bySpread = [...results].sort((a, b) => b.signals.spread - a.signals.spread)
    for (const r of bySpread) {
      if (coordinated.length >= topN - 1) break
      if (!seen.has(r.memory.content) && r.signals.spread > 0) { coordinated.push(r); seen.add(r.memory.content) }
    }
    const episodeOnly = results.filter(r => r.memory.scope === 'episode' && !r.memory.tags?.includes('summary'))
      .sort((a, b) => b.activation - a.activation)
    for (const r of episodeOnly) {
      if (coordinated.length >= topN) break
      if (!seen.has(r.memory.content)) { coordinated.push(r); seen.add(r.memory.content) }
    }
    for (const r of results) {
      if (coordinated.length >= topN) break
      if (!seen.has(r.memory.content)) { coordinated.push(r); seen.add(r.memory.content) }
    }
    coordinated.sort((a, b) => b.activation - a.activation)
    results = coordinated
  }

  // ── 分治策略后处理（原创：Query-Type Dispatch）──
  // 不同查询类型用不同的后处理策略，而非统一参数
  if (_currentQueryType === 'multi_entity' && !_twoPassInProgress && _queryNames && _queryNames.length >= 2) {
    // 策略 B：multi_entity → iterative recall（从 top-5 提取桥梁词做二轮召回）
    try {
      const top5 = results.slice(0, 5)
      const topTokens = new Map<string, number>()
      for (const r of top5) {
        for (const t of ((r.memory.content || '').toLowerCase().match(WORD_PATTERN.CJK2_EN3) || [])) {
          if (!EN_STOP_WORDS.has(t)) topTokens.set(t, (topTokens.get(t) || 0) + 1)
        }
      }
      const bridgeTokens = [...topTokens.entries()]
        .filter(([t, freq]) => freq >= 2 && !expanded.has(t) && (_idfCache?.get(t) ?? 0.5) > 0.3)
        .sort((a, b) => b[1] - a[1]).slice(0, 3).map(([t]) => t)

      if (bridgeTokens.length >= 1) {
        _twoPassInProgress = true
        const seen = new Set(results.map(r => r.memory.content))
        let p2Added = 0
        for (const entity of _queryNames.slice(0, 2)) {
          const p2Query = entity + ' ' + bridgeTokens.join(' ')
          const p2Res = computeActivationField(memories, p2Query, mood, alertness, expanded, topN, timeRange, cogHints)
          for (const r of p2Res.slice(0, 3)) {
            if (!seen.has(r.memory.content)) {
              r.activation *= 0.6
              results.push(r); seen.add(r.memory.content); p2Added++
            }
          }
        }
        if (p2Added > 0) {
          results.sort((a, b) => b.activation - a.activation)
          console.log(`[activation-field] dispatch:multi_entity iterative recall +${p2Added} results`)
        }
        _twoPassInProgress = false
      }
    } catch { _twoPassInProgress = false }
  }

  if (_currentQueryType === 'temporal') {
    // 策略 D：temporal → 含日期的记忆优先 tie-break
    const DATE_PATTERN = /\b(?:january|february|march|april|may|june|july|august|september|october|november|december)\b|\b\d{4}\b|\b\d{1,2}\s+\w+\s+\d{4}\b/i
    for (const r of results) {
      if (DATE_PATTERN.test(r.memory.content || '')) r.activation *= 1.05
    }
    results.sort((a, b) => b.activation - a.activation)
  }

  // 截断到 topN
  const topResults = results.slice(0, topN)

  if (topResults.length > 0) {
    console.log(`[activation-field] cascade: ${expanded.size} expanded words → ${results.length} candidates → ${topResults.length} selected`)
  }

  // 学习：每条消息都喂入 AAM 关联网络 + 时序共现
  try {
    _aamLearn(query, Math.abs(mood))
    // PAM 有向时序共现：用户说 A 后说 B → A→B 链接
    _aamLearnTemporalLink(query)
  } catch {}

  // ── System 1→2：零 LLM 召回质量低时，LLM 兜底 ──
  // 异步模式 B：不阻塞当前返回，LLM 结果异步写入，下一轮受益
  // benchmark 环境跳过（避免 spawnCLI 超时阻塞）
  if (!process.env.CC_SOUL_BENCHMARK && (topResults.length === 0 || (topResults.length > 0 && topResults[0].activation < 0.1))) {
    try {
      const { hasLLM } = require('./cli.ts')
      if (hasLLM()) {
        const { spawnCLI } = require('./cli.ts')
        // LLM query rewriting: 让 LLM 扩展查询词，结果存入 AAM 供下次使用
        spawnCLI(
          `用户问了"${query.slice(0, 100)}"，请列出3-5个相关的关键词或同义词，每行一个，只输出关键词不要解释`,
          (output: string) => {
            if (!output) return
            const keywords = output.split('\n').map(l => l.trim()).filter(l => l.length >= 2 && l.length <= 20)
            // 存入 AAM 共现网络，让下次召回能用这些扩展词
            try {
              const aam = require('./aam.ts')
              const queryWords = (query.match(WORD_PATTERN.CJK2_EN3) || [])
              for (const kw of keywords) {
                for (const qw of queryWords) {
                  aam.learnAssociation?.(qw + ' ' + kw)
                }
              }
            } catch {}
            try { require('./decision-log.ts').logDecision('system2_escalation', query.slice(0, 30), `expanded: ${keywords.join(',')}`) } catch {}
          },
          10000  // 10s timeout, low priority
        )
      }
    } catch {}
  }

  return topResults.map(r => r.memory)
}

/** 带 activation 分数的召回（benchmark 投票制用） */
export function activationRecallWithScores(
  memories: Memory[], query: string, topK: number,
  mood: number, alertness: number, cogHints?: any
): { memory: Memory; activation: number }[] {
  // 复用 activationRecall 的内部逻辑，但保留分数
  // 先调用 computeActivationField 获取带分数的结果
  const expandedWords = (() => {
    try {
      const aam = require('./aam.ts')
      const words = query.toLowerCase().match(/[a-z]{2,}/gi) || []
      return aam.expandQuery?.(words.slice(0, 5).map((w: string) => w.toLowerCase()), 10) || new Map()
    } catch { return new Map<string, number>() }
  })()
  const results = computeActivationField(memories, query, mood, alertness, expandedWords, topK * 3, null, cogHints)
  return results.slice(0, topK).map(r => ({ memory: r.memory, activation: r.activation }))
}

/** 获取当前 IDF 缓存（selectAnswer 用） */
export function getIdfCache(): Map<string, number> | null { return _idfCache }

// ═══════════════════════════════════════════════════════════════
// 调试/透明度
// ═══════════════════════════════════════════════════════════════

export function explainActivation(result: ActivationResult): string {
  const s = result.signals
  const parts = [
    `base=${s.base.toFixed(2)}`,
    `ctx=${s.context.toFixed(2)}`,
    `emo=${s.emotion.toFixed(2)}`,
    `spread=${s.spread.toFixed(2)}`,
    `inhib=${s.interference.toFixed(2)}`,
    `time=${s.temporal.toFixed(2)}`,
  ]
  return `activation=${result.activation.toFixed(3)} [${parts.join(' ')}]`
}

export function getFieldStats(): { totalActivated: number; avgActivation: number } {
  const values = [..._activations.values()]
  return {
    totalActivated: values.filter(v => v > 0.05).length,
    avgActivation: values.length > 0 ? values.reduce((s, v) => s + v, 0) / values.length : 0,
  }
}
