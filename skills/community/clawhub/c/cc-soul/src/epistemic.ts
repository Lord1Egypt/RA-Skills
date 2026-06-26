/**
 * epistemic.ts — Knowledge boundary self-awareness
 *
 * Tracks quality and correction rates per domain, auto-detects weak areas.
 * Provides confidence hints for augment injection and soul prompt.
 */

import { resolve } from 'path'
import type { SoulModule } from './brain.ts'
import type { InteractionStats } from './types.ts'
import { DATA_DIR, loadJson, debouncedSave } from './persistence.ts'

const EPISTEMIC_PATH = resolve(DATA_DIR, 'epistemic.json')

// ═══════════════════════════════════════════════════════════════════════════════
// TYPES
// ═══════════════════════════════════════════════════════════════════════════════

export interface DomainConfidence {
  domain: string           // "python" | "ios-reverse" | "图片识别" | "闲聊" etc
  totalResponses: number
  qualitySum: number
  corrections: number
  avgQuality: number       // computed
  correctionRate: number   // computed
}

// ═══════════════════════════════════════════════════════════════════════════════
// STATE
// ═══════════════════════════════════════════════════════════════════════════════

const domains = new Map<string, DomainConfidence>()

// ═══════════════════════════════════════════════════════════════════════════════
// DOMAIN DETECTION
// ═══════════════════════════════════════════════════════════════════════════════

// 缓存：同一条消息不重复检测
let _domainCache: { msg: string; result: string } | null = null

// 领域关键词表（种子，按特异性排序——越具体的越前面）
const DOMAIN_KEYWORDS: Array<{ domain: string; words: string[]; specificity: number }> = [
  { domain: 'ios-reverse', words: ['frida', 'hook', 'ida', 'mach-o', 'dyld', 'arm64', 'objc', '逆向', '砸壳', 'tweak', 'substrate', 'theos', 'cycript', 'reverse engineering', 'binary analysis'], specificity: 0.95 },
  { domain: 'rust', words: ['rust', 'cargo', '.rs', 'lifetime', 'borrow checker'], specificity: 0.9 },
  { domain: 'swift', words: ['swift', 'xcode', 'swiftui', 'uikit', 'cocoa', 'appkit'], specificity: 0.85 },
  { domain: 'golang', words: ['go ', 'golang', 'goroutine', '.go', 'func '], specificity: 0.85 },
  { domain: 'python', words: ['python', 'pip', 'flask', 'django', 'def ', 'import ', '.py', 'asyncio', 'pandas'], specificity: 0.7 },
  { domain: 'javascript', words: ['typescript', 'javascript', 'node', 'react', 'vue', '.ts', '.js', 'npm', 'pnpm', 'bun'], specificity: 0.7 },
  { domain: 'devops', words: ['docker', 'k8s', 'kubernetes', 'nginx', 'linux', 'bash', 'shell', 'systemd', 'ssh'], specificity: 0.75 },
  { domain: 'database', words: ['sql', 'mysql', 'postgres', 'mongodb', '数据库', 'redis', 'sqlite', 'database', 'query', 'index', 'schema'], specificity: 0.8 },
  { domain: '图片识别', words: ['图片', 'ocr', '识别', '照片', '截图', '看看这个', '这张图', 'image recognition', 'computer vision'], specificity: 0.85 },
  { domain: 'git', words: ['git', 'github', 'pr', 'merge', 'branch', 'commit', 'rebase'], specificity: 0.8 },
]

export function detectDomain(msg: string): string {
  // 缓存命中
  if (_domainCache?.msg === msg) return _domainCache.result

  const m = msg.toLowerCase()

  // IDF 特异性优先：多个领域都匹配时，取特异性最高的
  let bestDomain = '通用'
  let bestScore = 0

  for (const { domain, words, specificity } of DOMAIN_KEYWORDS) {
    const hits = words.filter(w => m.includes(w)).length
    if (hits > 0) {
      const score = hits * specificity  // 命中数 × 特异性
      if (score > bestScore) {
        bestScore = score
        bestDomain = domain
      }
    }
  }

  // AAM 动态补充：查共现网络里跟已知领域词高频共现的新词
  if (bestDomain === '通用') {
    try {
      const { getCooccurrence } = require('./aam.ts')
      // 提取消息中的关键词
      const msgWords = (m.match(/[\u4e00-\u9fff]{2,}|[a-zA-Z]{3,}/gi) || []).map(w => w.toLowerCase())
      for (const mw of msgWords) {
        for (const { domain, words } of DOMAIN_KEYWORDS) {
          for (const dw of words.slice(0, 3)) {  // 只查前 3 个种子词
            if (getCooccurrence(mw, dw) >= 5) {  // 高共现
              bestDomain = domain
              break
            }
          }
          if (bestDomain !== '通用') break
        }
        if (bestDomain !== '通用') break
      }
    } catch {}
  }

  if (bestDomain === '通用') {
    if (msg.length < 20) bestDomain = '闲聊'
    else if (['怎么看', '你觉得', '建议', '应该', '推荐', 'what do you think', 'advice', 'suggest', 'recommend', 'should i', 'consultation'].some(w => m.includes(w))) bestDomain = '咨询'
    else if (['chat', 'casual', 'hey', 'hi ', 'hello', 'sup', "what's up"].some(w => m.includes(w)) && msg.length < 30) bestDomain = '闲聊'
  }

  _domainCache = { msg, result: bestDomain }
  return bestDomain
}

// ═══════════════════════════════════════════════════════════════════════════════
// PERSISTENCE
// ═══════════════════════════════════════════════════════════════════════════════

export function loadEpistemic() {
  const raw = loadJson<Record<string, DomainConfidence>>(EPISTEMIC_PATH, {})
  domains.clear()
  for (const [k, v] of Object.entries(raw)) {
    domains.set(k, v)
  }
  console.log(`[cc-soul][epistemic] loaded ${domains.size} domains`)
}

function saveEpistemic() {
  const obj: Record<string, DomainConfidence> = {}
  for (const [k, v] of domains) {
    obj[k] = v
  }
  debouncedSave(EPISTEMIC_PATH, obj)
}

// ═══════════════════════════════════════════════════════════════════════════════
// TRACKING
// ═══════════════════════════════════════════════════════════════════════════════

function ensureDomain(domain: string): DomainConfidence {
  let d = domains.get(domain)
  if (!d) {
    d = { domain, totalResponses: 0, qualitySum: 0, corrections: 0, avgQuality: 5, correctionRate: 0 }
    domains.set(domain, d)
  }
  return d
}

function recompute(d: DomainConfidence) {
  d.avgQuality = d.totalResponses > 0
    ? Math.round(d.qualitySum / d.totalResponses * 10) / 10
    : 5
  d.correctionRate = d.totalResponses > 0
    ? Math.round((d.corrections + 1) / (d.totalResponses + 2) * 1000) / 10
    : 0
}

export function trackDomainQuality(msg: string, score: number) {
  const domain = detectDomain(msg)
  const d = ensureDomain(domain)
  d.totalResponses++
  d.qualitySum += score
  recompute(d)
  saveEpistemic()
}

export function trackDomainCorrection(msg: string) {
  const domain = detectDomain(msg)
  const d = ensureDomain(domain)
  d.corrections++
  recompute(d)
  saveEpistemic()
}

// ═══════════════════════════════════════════════════════════════════════════════
// KNOWLEDGE DECAY MODEL — 知识衰减曲线
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * 知识衰减曲线：每个领域有独立的"知识半衰期"
 * 刚被纠正 → 置信度快速衰减
 * 一直答对 → 置信度缓慢巩固
 *
 * 公式：confidence(t) = base × (1 - decay × e^(-t/τ))
 * τ = 半衰期，由纠正率决定
 * base = 基础置信度，由回答质量决定
 */
export interface KnowledgeDecay {
  domain: string
  confidence: number      // [0, 1] 连续置信度
  trend: 'improving' | 'stable' | 'degrading'
  halfLife: number        // 天数：知识保持的半衰期
  lastCorrection: number  // 距上次纠正的天数
}

export function computeKnowledgeDecay(domain: string, domainData: any): KnowledgeDecay {
  const total = domainData?.totalResponses || 0
  const corrections = domainData?.corrections || 0
  const avgQuality = total > 0 ? (domainData?.qualitySum || 5 * total) / total : 5
  const lastCorrectionTs = domainData?.lastCorrectionTs || 0
  const daysSinceCorrection = lastCorrectionTs > 0 ? (Date.now() - lastCorrectionTs) / 86400000 : 999

  // 基础置信度：由平均质量决定 (sigmoid 映射)
  const base = 1 / (1 + Math.exp(-(avgQuality - 5) * 0.8))

  // 半衰期：纠正率越高，半衰期越短（知识越不稳定）
  // Beta(1,1) prior smoothing: avoids high variance with small samples
  const correctionRate = total > 0 ? (corrections + 1) / (total + 2) : 0
  const halfLife = Math.max(3, 30 * (1 - correctionRate))  // 3-30 天

  // 衰减：距上次纠正越久，恢复越多
  const decay = correctionRate > 0 ? 0.3 * Math.exp(-daysSinceCorrection / halfLife) : 0

  // 最终置信度
  const confidence = Math.max(0.1, Math.min(0.95, base * (1 - decay)))

  // 趋势：最近 5 次回答的质量趋势
  let trend: 'improving' | 'stable' | 'degrading' = 'stable'
  if (total >= 5) {
    if (daysSinceCorrection < 3) trend = 'degrading'
    else if (daysSinceCorrection > 14 && correctionRate < 0.1) trend = 'improving'
  }

  return { domain, confidence, trend, halfLife, lastCorrection: daysSinceCorrection }
}

// ═══════════════════════════════════════════════════════════════════════════════
// CONFIDENCE QUERY
// ═══════════════════════════════════════════════════════════════════════════════

export function getDomainConfidence(msg: string): { domain: string; confidence: 'high' | 'medium' | 'low'; hint: string; decay?: KnowledgeDecay } {
  const domain = detectDomain(msg)
  const d = domains.get(domain)

  // New domain — not enough data
  if (!d || d.totalResponses < 3) {
    return { domain, confidence: 'medium', hint: '' }
  }

  // 使用知识衰减曲线计算连续置信度
  const kd = computeKnowledgeDecay(domain, d)
  const confLabel: 'high' | 'medium' | 'low' = kd.confidence > 0.7 ? 'high' : kd.confidence > 0.4 ? 'medium' : 'low'
  const hint = confLabel === 'low'
    ? `[知识边界] "${domain}" 置信度${(kd.confidence*100).toFixed(0)}%，${kd.trend === 'degrading' ? '最近被纠正过' : '历史准确率低'}，请仔细核实`
    : ''
  return { domain, confidence: confLabel, hint, decay: kd }
}

// ═══════════════════════════════════════════════════════════════════════════════
// WEAK DOMAINS — domains with high correction rate or low quality
// ═══════════════════════════════════════════════════════════════════════════════

/** Returns domain names with high correction rate or low quality, sorted by worst first */
export function getWeakDomains(): string[] {
  return [...domains.values()]
    .filter(d => d.totalResponses >= 5 && (d.correctionRate > 10 || d.avgQuality < 5))
    .sort((a, b) => b.correctionRate - a.correctionRate)
    .map(d => d.domain)
}

// ═══════════════════════════════════════════════════════════════════════════════
// SOUL PROMPT SUMMARY
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * P1-#12: getCapabilityScore — 对话能力评分公示
 * 格式化输出每个域的质量分和纠正率
 */
export function getCapabilityScore(): string {
  if (domains.size === 0) return '🎯 能力评分\n═══════════════════════════════\n暂无数据，需要更多对话来建立域置信度。'

  const entries = [...domains.values()]
    .filter(d => d.totalResponses >= 2)
    .sort((a, b) => b.totalResponses - a.totalResponses)

  if (entries.length === 0) return '🎯 能力评分\n═══════════════════════════════\n样本不足，至少每个领域 2 次对话。'

  const lines = [
    '🎯 能力评分',
    '═══════════════════════════════',
    `${'域'.padEnd(15)} ${'质量'.padStart(5)} ${'纠正率'.padStart(7)} ${'样本'.padStart(5)}`,
    '─'.repeat(35),
  ]
  for (const d of entries) {
    const bar = d.avgQuality >= 7 ? '✓' : d.avgQuality < 5 ? '✗' : '~'
    lines.push(`${bar} ${d.domain.padEnd(13)} ${d.avgQuality.toFixed(1).padStart(5)} ${(d.correctionRate + '%').padStart(7)} ${d.totalResponses.toString().padStart(5)}`)
  }

  const overall = entries.reduce((s, d) => s + d.qualitySum, 0) / Math.max(1, entries.reduce((s, d) => s + d.totalResponses, 0))
  lines.push('─'.repeat(35))
  lines.push(`综合质量: ${overall.toFixed(1)}/10`)

  return lines.join('\n')
}

export function getEpistemicSummary(): string {
  if (domains.size === 0) return ''

  const entries = [...domains.values()]
    .filter(d => d.totalResponses >= 3) // only show domains with enough data
    .sort((a, b) => b.totalResponses - a.totalResponses)

  if (entries.length === 0) return ''

  const lines: string[] = []

  // Weak domains (high correction rate or low quality)
  const weak = entries.filter(d =>
    (d.correctionRate > 10 && d.totalResponses >= 5) ||
    (d.avgQuality < 5 && d.totalResponses >= 5),
  )
  if (weak.length > 0) {
    lines.push('⚠ 薄弱领域（回答前要格外谨慎）：')
    for (const d of weak) {
      lines.push(`- ${d.domain}: 质量${d.avgQuality}/10, 纠正率${d.correctionRate}%, 样本${d.totalResponses}`)
    }
  }

  // Strong domains
  const strong = entries.filter(d => d.avgQuality > 7 && d.totalResponses >= 10)
  if (strong.length > 0) {
    lines.push('✓ 擅长领域：')
    for (const d of strong) {
      lines.push(`- ${d.domain}: 质量${d.avgQuality}/10, 样本${d.totalResponses}`)
    }
  }

  return lines.join('\n')
}

// ═══════════════════════════════════════════════════════════════════════════════
// #6 Growth Vectors — quantify agent growth trajectory
// ═══════════════════════════════════════════════════════════════════════════════

export interface GrowthVector {
  dimension: string
  current: number
  trend: 'up' | 'down' | 'stable'
  label: string
}

/**
 * Compute growth vectors from stats, rules, memories, epistemic domains.
 * No extra storage needed — all computed from existing data.
 */
export function getGrowthVectors(): GrowthVector[] {
  // Lazy imports to avoid circular deps (evolution/person-model import from epistemic)
  let rules: any[] = []
  let stats: any = { totalMessages: 0, corrections: 0 }
  let getDbFn: any = () => null
  try { rules = require('./evolution.ts').getRules?.() || [] } catch {}
  try { stats = require('./handler-state.ts').stats || stats } catch {}
  try { const { getDb } = require('./sqlite-store.ts'); getDbFn = getDb } catch {}

  const vectors: GrowthVector[] = []
  const now = Date.now()
  const WEEK = 7 * 86400000

  // 1. correction_rate: 7-day window vs previous 7-day window
  try {
    const db = getDbFn()
    if (db) {
      const cur7d = (db.prepare("SELECT COUNT(*) as c FROM memories WHERE scope = 'correction' AND ts > ?").get(now - WEEK) as any)?.c || 0
      const prev7d = (db.prepare("SELECT COUNT(*) as c FROM memories WHERE scope = 'correction' AND ts > ? AND ts <= ?").get(now - 2 * WEEK, now - WEEK) as any)?.c || 0
      const curChats = (db.prepare("SELECT COUNT(*) as c FROM chat_history WHERE ts > ?").get(now - WEEK) as any)?.c || 1
      const prevChats = (db.prepare("SELECT COUNT(*) as c FROM chat_history WHERE ts > ? AND ts <= ?").get(now - 2 * WEEK, now - WEEK) as any)?.c || 1
      const curRate = cur7d / curChats
      const prevRate = prev7d / prevChats
      const trend = curRate < prevRate - 0.02 ? 'up' : curRate > prevRate + 0.02 ? 'down' : 'stable'
      vectors.push({
        dimension: 'correction_rate',
        current: Math.round(curRate * 1000) / 10,
        trend,
        label: `纠正率 ${(curRate * 100).toFixed(1)}%${trend === 'up' ? ' (改善中)' : trend === 'down' ? ' (需注意)' : ''}`,
      })
    }
  } catch {}

  // 2. rule_count: rules growth
  try {
    const ruleCount = (rules as any[]).length
    const recentRules = (rules as any[]).filter((r: any) => now - r.ts < WEEK).length
    const trend = recentRules >= 3 ? 'up' : recentRules === 0 ? 'stable' : 'stable'
    vectors.push({
      dimension: 'rule_count',
      current: ruleCount,
      trend,
      label: `规则 ${ruleCount} 条 (本周+${recentRules})`,
    })
  } catch {}

  // 3. memory_quality: average confidence of active memories
  try {
    const db = getDbFn()
    if (db) {
      const curAvg = (db.prepare("SELECT AVG(confidence) as avg FROM memories WHERE scope != 'expired' AND scope != 'decayed' AND ts > ?").get(now - WEEK) as any)?.avg
      const prevAvg = (db.prepare("SELECT AVG(confidence) as avg FROM memories WHERE scope != 'expired' AND scope != 'decayed' AND ts > ? AND ts <= ?").get(now - 2 * WEEK, now - WEEK) as any)?.avg
      if (curAvg != null) {
        const cur = Math.round(curAvg * 100) / 100
        const trend = prevAvg != null ? (curAvg > prevAvg + 0.03 ? 'up' : curAvg < prevAvg - 0.03 ? 'down' : 'stable') : 'stable'
        vectors.push({
          dimension: 'memory_quality',
          current: cur,
          trend,
          label: `记忆质量 ${cur.toFixed(2)}${trend === 'up' ? ' (提升)' : trend === 'down' ? ' (下降)' : ''}`,
        })
      }
    }
  } catch {}

  // 4. recall_accuracy: ratio of recalled memories that were subsequently accessed again (proxy for accuracy)
  try {
    const db = getDbFn()
    if (db) {
      const totalRecalled = (db.prepare("SELECT COUNT(*) as c FROM memories WHERE recallCount > 0 AND scope != 'expired'").get() as any)?.c || 0
      const highRecall = (db.prepare("SELECT COUNT(*) as c FROM memories WHERE recallCount >= 3 AND scope != 'expired'").get() as any)?.c || 0
      const accuracy = totalRecalled > 0 ? highRecall / totalRecalled : 0
      vectors.push({
        dimension: 'recall_accuracy',
        current: Math.round(accuracy * 100),
        trend: accuracy > 0.3 ? 'up' : accuracy < 0.1 ? 'down' : 'stable',
        label: `召回准确率 ${(accuracy * 100).toFixed(0)}% (高频命中 ${highRecall}/${totalRecalled})`,
      })
    }
  } catch {}

  // 5. domain_breadth: number of tracked domains
  try {
    const domainCount = domains.size
    const activeDomains = [...domains.values()].filter(d => d.totalResponses >= 3).length
    vectors.push({
      dimension: 'domain_breadth',
      current: activeDomains,
      trend: activeDomains > 5 ? 'up' : 'stable',
      label: `领域覆盖 ${activeDomains} 个活跃领域 (共 ${domainCount})`,
    })
  } catch {}

  return vectors
}

/**
 * Format growth vectors for display.
 */
export function formatGrowthVectors(): string {
  const vectors = getGrowthVectors()
  if (vectors.length === 0) return '成长轨迹: 数据不足，需要更多对话积累。'
  const trendIcon = (t: string) => t === 'up' ? '📈' : t === 'down' ? '📉' : '➡️'
  const lines = [
    '🌱 成长轨迹',
    '═══════════════════════════════',
    ...vectors.map(v => `  ${trendIcon(v.trend)} ${v.label}`),
  ]
  return lines.join('\n')
}

// ═══════════════════════════════════════════════════════════════════════════════
// BLIND SPOT QUESTIONS — proactively ask about gaps in user knowledge
// ═══════════════════════════════════════════════════════════════════════════════

const PENDING_Q_PATH = resolve(DATA_DIR, 'pending_questions.json')

interface PendingQuestion {
  domain: string
  question: string
  createdAt: number
  askedAt?: number
}

const DOMAIN_QUESTIONS: Record<string, string[]> = {
  python: ['Python 版本用 3.x 哪个？', '写测试用 pytest 还是 unittest？', '包管理用 pip/poetry/uv？', 'IDE 用什么？PyCharm/VS Code？'],
  devops: ['CI/CD 用什么？GitHub Actions/Jenkins？', '容器化了吗？Docker/Podman？', '云服务商用哪家？'],
  database: ['主力数据库用什么？', '用 ORM 还是裸 SQL？', '备份策略是什么样的？'],
  javascript: ['前端框架用 React/Vue/其他？', '构建工具用 Vite/Webpack？', '状态管理用什么方案？'],
  swift: ['SwiftUI 还是 UIKit 为主？', 'Xcode 版本？', '包管理用 SPM 还是 CocoaPods？'],
  git: ['Git 工作流用什么？GitFlow/Trunk-based？', 'Code review 流程是怎样的？'],
}

let pendingQuestions: PendingQuestion[] = loadJson<PendingQuestion[]>(PENDING_Q_PATH, [])

/** Heartbeat: scan domains for blind spots, generate up to 3 pending questions */
export function scanBlindSpotQuestions() {
  // Lazy require to avoid circular deps (person-model imports from epistemic)
  let pm: any = null
  try { pm = require('./person-model.ts').getPersonModel?.() } catch {}
  const knownText = pm ? JSON.stringify(pm).toLowerCase() : ''

  const active = [...domains.values()]
    .filter(d => d.totalResponses >= 5)
    .sort((a, b) => b.totalResponses - a.totalResponses)

  // Prune asked questions older than 7 days
  const SEVEN_DAYS = 7 * 86400000
  pendingQuestions = pendingQuestions.filter(q => !q.askedAt || Date.now() - q.askedAt < SEVEN_DAYS)

  for (const d of active) {
    if (pendingQuestions.filter(q => !q.askedAt).length >= 3) break
    const templates = DOMAIN_QUESTIONS[d.domain]
    if (!templates) continue
    for (const tpl of templates) {
      // Skip if already pending or recently asked
      if (pendingQuestions.some(q => q.question === tpl)) continue
      // Skip if person-model already contains relevant keywords
      const keywords = tpl.match(/[\u4e00-\u9fa5a-zA-Z]{2,}/g) || []
      if (keywords.some(k => knownText.includes(k.toLowerCase()))) continue
      pendingQuestions.push({ domain: d.domain, question: tpl, createdAt: Date.now() })
      break // one question per domain per scan
    }
  }
  debouncedSave(PENDING_Q_PATH, pendingQuestions)
}

/** Augment injection: pop one unasked question, mark as asked */
export function popBlindSpotQuestion(): string | null {
  const q = pendingQuestions.find(q => !q.askedAt)
  if (!q) return null
  q.askedAt = Date.now()
  debouncedSave(PENDING_Q_PATH, pendingQuestions)
  return `[主动提问] 用户经常聊 ${q.domain} 但从没提过相关偏好，可以自然地问一下：${q.question}`
}

// ── SoulModule ──
export const epistemicModule: SoulModule = {
  id: 'epistemic',
  name: '知识边界自觉',
  priority: 50,
  init() { loadEpistemic() },
}
