/**
 * values.ts — Behavioral value alignment
 *
 * Learns user preferences from interaction patterns, not hand-coded rules.
 * Each dimension is a spectrum; the system nudges scores based on signal words
 * found in user messages. Positive feedback amplifies the signal.
 */

import { resolve } from 'path'
import { DATA_DIR, loadJson, debouncedSave } from './persistence.ts'
import type { SoulModule } from './brain.ts'
import type { Augment } from './types.ts'

const VALUES_PATH = resolve(DATA_DIR, 'values.json')

// ── Types ──

interface ValueDimension {
  name: string              // e.g., "efficiency_vs_understanding"
  leftLabel: string         // e.g., "直接给方案"
  rightLabel: string        // e.g., "先解释原理"
  score: number             // -1 to 1, negative = prefers left, positive = prefers right
  evidence: number          // how many data points
  lastUpdated: number
}

interface ValueConflict {
  winner: string
  loser: string
  context: string
  ts: number
}

interface DimensionDef {
  name: string
  leftLabel: string
  rightLabel: string
  leftSignals: string[]
  rightSignals: string[]
}

// ── Dimension definitions ──

const VALUE_DIMENSIONS: DimensionDef[] = [
  {
    name: 'efficiency_vs_understanding',
    leftLabel: '直接给方案',
    rightLabel: '先解释原理',
    leftSignals: ['直接', '代码', '给我', '快', '别解释', '太长了', '简洁'],
    rightSignals: ['为什么', '原理', '解释', '怎么理解', '能说说', '详细'],
  },
  {
    name: 'formal_vs_casual',
    leftLabel: '正式严谨',
    rightLabel: '随意轻松',
    leftSignals: ['分析', '报告', '文档', '请', '总结'],
    rightSignals: ['哈哈', '牛', '靠', '啊', '呢', '嘿', '😂', '👍'],
  },
  {
    name: 'depth_vs_breadth',
    leftLabel: '深入钻研',
    rightLabel: '广泛涉猎',
    leftSignals: ['深入', '细节', '具体', '底层', '源码', '原理'],
    rightSignals: ['概览', '大概', '简单说', '总结', '对比', '哪些'],
  },
  {
    name: 'proactive_vs_reactive',
    leftLabel: '主动建议',
    rightLabel: '只回答问题',
    leftSignals: ['顺便', '还有', '建议', '你觉得'],
    rightSignals: ['别多说', '回答就行', '不用补充', '太长'],
  },
]

// ── State — per-user value maps ──

const userValues = new Map<string, ValueDimension[]>()
const userConflicts = new Map<string, ValueConflict[]>()

function createDefaultValues(): ValueDimension[] {
  return VALUE_DIMENSIONS.map(d => ({
    name: d.name,
    leftLabel: d.leftLabel,
    rightLabel: d.rightLabel,
    score: 0,
    evidence: 0,
    lastUpdated: 0,
  }))
}

function getUserValues(userId?: string): ValueDimension[] {
  if (!userId) return createDefaultValues()
  let values = userValues.get(userId)
  if (!values) {
    values = createDefaultValues()
    userValues.set(userId, values)
  }
  return values
}

// ── Public API ──

export function loadValues() {
  const loaded = loadJson<Record<string, any>>(VALUES_PATH, {})
  if (Array.isArray(loaded)) {
    // Migration: old format was a flat array (single-user). Store under '_default'.
    if (loaded.length > 0) {
      userValues.set('_default', loaded)
    }
  } else {
    const conflicts = loaded._conflicts as Record<string, ValueConflict[]> | undefined
    if (conflicts) {
      for (const [userId, arr] of Object.entries(conflicts)) userConflicts.set(userId, arr)
    }
    for (const [userId, vals] of Object.entries(loaded)) {
      if (userId === '_conflicts') continue
      userValues.set(userId, vals as ValueDimension[])
    }
  }
}

/** Export all values as a plain object (for soul export) */
export function getAllValues(): Record<string, any> {
  const obj: Record<string, any> = {}
  for (const [userId, vals] of userValues) obj[userId] = vals
  if (userConflicts.size > 0) {
    const c: Record<string, ValueConflict[]> = {}
    for (const [userId, arr] of userConflicts) c[userId] = arr
    obj._conflicts = c
  }
  return obj
}

function saveValues() {
  const obj: Record<string, any> = {}
  for (const [userId, vals] of userValues) obj[userId] = vals
  if (userConflicts.size > 0) {
    const c: Record<string, ValueConflict[]> = {}
    for (const [userId, arr] of userConflicts) c[userId] = arr
    obj._conflicts = c
  }
  debouncedSave(VALUES_PATH, obj)
}

/** Call on each user message to detect preference signals */
export function detectValueSignals(userMsg: string, wasPositiveFeedback: boolean, userId?: string) {
  if (!userId) return
  const values = getUserValues(userId)
  const m = userMsg.toLowerCase()

  for (const dim of VALUE_DIMENSIONS) {
    const val = values.find(v => v.name === dim.name)
    if (!val) continue

    const leftHits = dim.leftSignals.filter(s => m.includes(s)).length
    const rightHits = dim.rightSignals.filter(s => m.includes(s)).length

    if (leftHits === 0 && rightHits === 0) continue

    // Positive feedback amplifies the signal (user liked what we did)
    const amplifier = wasPositiveFeedback ? 1.5 : 1.0

    const delta = ((rightHits - leftHits) / Math.max(1, leftHits + rightHits)) * 0.1 * amplifier
    val.score = Math.max(-1, Math.min(1, val.score + delta))
    val.evidence++
    val.lastUpdated = Date.now()
  }

  saveValues()
}

/** Generate prompt guidance based on learned values (for soul prompt) */
export function getValueGuidance(userId?: string): string {
  const values = getUserValues(userId)
  const meaningful = values.filter(v => v.evidence >= 3 && Math.abs(v.score) > 0.2)
  if (meaningful.length === 0) return ''

  const lines = meaningful.map(v => {
    const pref = v.score < 0 ? v.leftLabel : v.rightLabel
    const strength = Math.abs(v.score) > 0.6 ? '强烈' : '倾向'
    return `- ${strength}偏好: ${pref} (${v.evidence}次观察)`
  })

  return `## 从行为中学到的偏好\n${lines.join('\n')}`
}

/** Short context line for augment injection */
export function getValueContext(userId?: string): string {
  const values = getUserValues(userId)
  const meaningful = values.filter(v => v.evidence >= 5 && Math.abs(v.score) > 0.3)
  if (meaningful.length === 0) return ''

  const hints = meaningful.map(v => {
    const pref = v.score < 0 ? v.leftLabel : v.rightLabel
    return pref
  })

  return `[用户偏好] ${hints.join('、')}`
}

// ── Value conflict priority learning ──

export function recordConflict(winner: string, loser: string, context: string, userId?: string) {
  if (!userId) return
  let arr = userConflicts.get(userId)
  if (!arr) { arr = []; userConflicts.set(userId, arr) }
  arr.push({ winner, loser, context, ts: Date.now() })
  if (arr.length > 50) arr.splice(0, arr.length - 50) // cap at 50

  // 同步更新 Bradley-Terry 强度
  btUpdateStrength(winner, loser)

  saveValues()
}

export function getValuePriority(a: string, b: string, userId?: string): string | null {
  if (!userId) return null
  const arr = userConflicts.get(userId)
  if (!arr || arr.length === 0) return null

  // 优先使用 Bradley-Terry 概率模型（有足够数据时）
  const sA = btPreferenceScore(a)
  const sB = btPreferenceScore(b)
  if (sA !== 1.0 || sB !== 1.0) {
    // BT 模型有数据，用概率判断
    const result = btCompare(a, b)
    if (result.probability > 0.55) return result.winner  // 概率 > 55% 才算有倾向
  }

  // 回退到简单计数（兼容旧数据）
  let aWins = 0, bWins = 0
  for (const c of arr) {
    if (c.winner === a && c.loser === b) aWins++
    if (c.winner === b && c.loser === a) bWins++
  }
  if (aWins === 0 && bWins === 0) return null
  return aWins >= bWins ? a : b
}

export function getConflictContext(userId?: string): string {
  if (!userId) return ''
  const arr = userConflicts.get(userId)
  if (!arr || arr.length < 2) return ''
  // Aggregate win counts per pair
  const pairMap = new Map<string, number>()
  for (const c of arr) {
    const key = `${c.winner}>${c.loser}`
    pairMap.set(key, (pairMap.get(key) || 0) + 1)
  }
  const hints: string[] = []
  for (const [key, count] of pairMap) {
    if (count < 2) continue
    const [w, l] = key.split('>')
    hints.push(`${w} > ${l}(${count}次)`)
  }
  if (hints.length === 0) return ''
  return `[价值观] 用户在取舍时: ${hints.join('、')}`
}

// ── Bradley-Terry 偏好概率模型 ──

/**
 * Bradley-Terry 偏好概率模型：
 * P(A > B) = strength(A) / (strength(A) + strength(B))
 * 比简单计数更好：能处理间接对比（A>B, B>C → A>C 的传递性）
 */
const _preferenceStrengths = new Map<string, number>()

function btUpdateStrength(winner: string, loser: string, learningRate: number = 0.1) {
  const sW = _preferenceStrengths.get(winner) || 1.0
  const sL = _preferenceStrengths.get(loser) || 1.0

  // Bradley-Terry 更新
  const pWin = sW / (sW + sL)
  const surprise = 1 - pWin  // 越意外的结果更新越大

  _preferenceStrengths.set(winner, sW * (1 + learningRate * surprise))
  _preferenceStrengths.set(loser, sL * (1 - learningRate * (1 - surprise)))

  // 归一化防止数值爆炸
  const total = [..._preferenceStrengths.values()].reduce((s, v) => s + v, 0)
  if (total > 100) {
    for (const [k, v] of _preferenceStrengths) {
      _preferenceStrengths.set(k, v / total * _preferenceStrengths.size)
    }
  }
}

function btPreferenceScore(item: string): number {
  return _preferenceStrengths.get(item) || 1.0
}

function btCompare(a: string, b: string): { winner: string; probability: number } {
  const sA = _preferenceStrengths.get(a) || 1.0
  const sB = _preferenceStrengths.get(b) || 1.0
  const pA = sA / (sA + sB)
  return pA >= 0.5 ? { winner: a, probability: pA } : { winner: b, probability: 1 - pA }
}

// ═══════════════════════════════════════════════════════════════════════════════
// SOUL MODULE — brain-managed lifecycle
// ═══════════════════════════════════════════════════════════════════════════════

export const valuesModule: SoulModule = {
  id: 'values',
  name: '价值观追踪',
  priority: 30,

  init() {
    loadValues()
  },

  onPreprocessed(event: any): Augment[] | void {
    const senderId = event?.context?.senderId
    if (!senderId) return
    const userMsg = event?.context?.userMessage || event?.message?.text || ''
    if (userMsg) detectValueSignals(userMsg, false, senderId)
    const ctx = getValueContext(senderId)
    if (ctx) return [{ content: ctx, priority: 3, tokens: Math.ceil(ctx.length / 3) }]
  },

  onSent(event: any) {
    const senderId = event?.context?.senderId
    const satisfaction = event?.context?.satisfaction
    if (senderId && satisfaction === 'POSITIVE') {
      const userMsg = event?.context?.userMessage || ''
      if (userMsg) detectValueSignals(userMsg, true, senderId)
    }
  },
}
