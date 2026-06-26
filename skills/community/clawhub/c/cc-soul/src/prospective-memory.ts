/**
 * prospective-memory.ts — "Remember to do X when Y happens"
 *
 * Unlike retrospective memory (searching the past), prospective memory
 * is about FUTURE intentions. No competitor has this.
 *
 * Examples:
 *   User says "下周要面试" → trigger: "面试|紧张|准备" → remind: "上次面试你说薪资报低了"
 *   User says "明天要出差" → trigger: "出差|机场|酒店" → remind: "你上次出差忘带充电器"
 *   User says "提醒我下次..." → explicit prospective memory creation
 */

import type { Memory } from './types.ts'
import { DATA_DIR, loadJson, debouncedSave } from './persistence.ts'
import { resolve } from 'path'

const PM_PATH = resolve(DATA_DIR, 'prospective_memory.json')

export interface ProspectiveMemory {
  id: string
  trigger: string        // regex-friendly keywords to match against future messages
  remind: string         // what to surface when trigger matches
  createdAt: number
  expiresAt: number      // auto-expire (0 = never)
  firedAt?: number       // when it was triggered (null if not yet)
  source: 'auto' | 'user_explicit'  // auto-detected vs user said "提醒我..."
  userId?: string
}

let pmStore: ProspectiveMemory[] = loadJson<ProspectiveMemory[]>(PM_PATH, [])
function savePM() { debouncedSave(PM_PATH, pmStore) }

let _counter = 0
function makeId(): string { return `pm_${Date.now()}_${_counter++}` }

// ═══════════════════════════════════════════════════════════════════════════════
// AUTO-DETECTION — detect future intentions in user messages
// ═══════════════════════════════════════════════════════════════════════════════

interface FuturePattern {
  detect: RegExp                          // match user message
  triggerKeywords: string                 // what to listen for later
  remindTemplate: (match: RegExpMatchArray, msg: string) => string
  expiryDays: number                     // auto-expire after N days
}

const FUTURE_PATTERNS: FuturePattern[] = [
  {
    detect: /(?:下周|明天|后天|周[一二三四五六日天]).*(?:面试|interview)/,
    triggerKeywords: '面试|interview|紧张|准备|offer',
    remindTemplate: (_m, msg) => `用户之前提到有面试计划：${msg.slice(0, 60)}`,
    expiryDays: 14,
  },
  {
    detect: /(?:下周|明天|后天|周[一二三四五六日天]).*(?:出差|出行|旅行|飞)/,
    triggerKeywords: '出差|出行|机场|酒店|行李|航班',
    remindTemplate: (_m, msg) => `用户之前提到有出行计划：${msg.slice(0, 60)}`,
    expiryDays: 14,
  },
  {
    detect: /(?:准备|打算|计划|想).*(?:换工作|跳槽|离职|辞职)/,
    triggerKeywords: '简历|面试|offer|跳槽|离职|新工作',
    remindTemplate: (_m, msg) => `用户之前提到有跳槽意向：${msg.slice(0, 60)}`,
    expiryDays: 30,
  },
  {
    detect: /(?:准备|打算|计划|想).*(?:买房|买车|装修|搬家)/,
    triggerKeywords: '房|车|装修|搬家|贷款|首付|看房',
    remindTemplate: (_m, msg) => `用户之前提到有购买/搬迁计划：${msg.slice(0, 60)}`,
    expiryDays: 60,
  },
  {
    detect: /(?:下次|以后|记得).*(?:提醒|别忘|注意)/,
    triggerKeywords: '', // will be extracted from message
    remindTemplate: (_m, msg) => `用户要求记住：${msg.slice(0, 80)}`,
    expiryDays: 30,
  },
  {
    detect: /(?:deadline|ddl|截止|交付).*(?:下周|月底|号|日)/,
    triggerKeywords: 'deadline|ddl|截止|交付|来不及|进度',
    remindTemplate: (_m, msg) => `用户之前提到有截止日期：${msg.slice(0, 60)}`,
    expiryDays: 14,
  },
  {
    detect: /(?:下[周个]?月|下季度|明年).*(?:旅[行游]|出[国门]|度假)/,
    triggerKeywords: '旅行|出发|机票|签证|行李|酒店|攻略',
    remindTemplate: (_m, msg) => `用户之前提到有旅行计划：${msg.slice(0, 60)}`,
    expiryDays: 60,
  },
  {
    detect: /(?:下周|这周|明天|后天|周[一二三四五六日天]).*(?:开会|会议|review|评审|述职|分享|演讲|讲座|talk|汇报)/,
    triggerKeywords: '会议|review|评审|述职|汇报|PPT|材料|分享|演讲|讲座|slides',
    remindTemplate: (_m, msg) => `用户之前提到有会议/分享安排：${msg.slice(0, 60)}`,
    expiryDays: 7,
  },
  {
    detect: /(?:下周|这周|明天|后天|周[一二三四五六日天]).*(?:考试|测验|认证|答辩)/,
    triggerKeywords: '考试|测验|认证|答辩|复习|准备|通过',
    remindTemplate: (_m, msg) => `用户之前提到有考试计划：${msg.slice(0, 60)}`,
    expiryDays: 14,
  },
  {
    detect: /(?:准备|打算|计划|想).*(?:学|练|入门|转行|转型)/,
    triggerKeywords: '学习|入门|教程|课程|进度|坚持',
    remindTemplate: (_m, msg) => `用户之前提到有学习计划：${msg.slice(0, 60)}`,
    expiryDays: 30,
  },
]

/**
 * Scan a user message for future intentions, auto-create prospective memories.
 */
export function detectProspectiveMemory(userMsg: string, userId?: string) {
  for (const pattern of FUTURE_PATTERNS) {
    const match = userMsg.match(pattern.detect)
    if (!match) continue

    // Check if we already have a similar PM
    const existing = pmStore.find(pm =>
      !pm.firedAt && pm.trigger === pattern.triggerKeywords && pm.userId === userId
    )
    if (existing) continue

    const pm: ProspectiveMemory = {
      id: makeId(),
      trigger: pattern.triggerKeywords || userMsg.slice(0, 30),
      remind: pattern.remindTemplate(match, userMsg),
      createdAt: Date.now(),
      expiresAt: pattern.expiryDays > 0 ? Date.now() + pattern.expiryDays * 86400000 : 0,
      source: /提醒|记得|别忘/.test(userMsg) ? 'user_explicit' : 'auto',
      userId,
    }
    pmStore.push(pm)
    savePM()
    console.log(`[cc-soul][prospective] created: "${pm.trigger}" → "${pm.remind.slice(0, 40)}"`)
  }
}

/**
 * Check if any prospective memory should fire for the current message.
 * Returns reminder text if triggered, null otherwise.
 */
export function checkProspectiveMemory(userMsg: string, userId?: string): string | null {
  const now = Date.now()
  const msgLower = userMsg.toLowerCase()
  const reminders: string[] = []

  for (const pm of pmStore) {
    if (pm.firedAt) continue  // already fired
    if (pm.expiresAt > 0 && now > pm.expiresAt) continue  // expired
    if (pm.userId && pm.userId !== userId) continue  // wrong user

    // Check trigger keywords
    const keywords = pm.trigger.split('|').filter(k => k.length >= 2)
    const matched = keywords.some(kw => msgLower.includes(kw.toLowerCase()))
    if (!matched) continue

    // Fire!
    pm.firedAt = now
    reminders.push(pm.remind)
    console.log(`[cc-soul][prospective] FIRED: "${pm.trigger}" → "${pm.remind.slice(0, 40)}"`)
  }

  if (reminders.length > 0) {
    savePM()
    return `[前瞻记忆] ${reminders.join('；')}`
  }
  return null
}

/**
 * Cleanup: remove expired and long-fired prospective memories.
 */
export function cleanupProspectiveMemories() {
  const now = Date.now()
  const FIRED_RETENTION = 7 * 86400000  // keep fired PMs for 7 days
  const before = pmStore.length
  pmStore = pmStore.filter(pm => {
    if (pm.expiresAt > 0 && now > pm.expiresAt && !pm.firedAt) return false  // expired, never fired
    if (pm.firedAt && now - pm.firedAt > FIRED_RETENTION) return false  // fired long ago
    return true
  })
  if (pmStore.length < before) {
    savePM()
    console.log(`[cc-soul][prospective] cleanup: removed ${before - pmStore.length} expired PMs`)
  }
}

export function getProspectiveMemoryCount(): number {
  return pmStore.filter(pm => !pm.firedAt && (!pm.expiresAt || pm.expiresAt > Date.now())).length
}

/** Get all active (unfired, unexpired) PM trigger keywords for dedup with follow-ups */
export function getActivePMTriggers(): string[] {
  const now = Date.now()
  return pmStore
    .filter(pm => !pm.firedAt && (!pm.expiresAt || pm.expiresAt > now))
    .flatMap(pm => pm.trigger.split('|').filter(k => k.length >= 2))
    .map(k => k.toLowerCase())
}

/**
 * Auto-detect recurring themes from recent memories and create prospective memories.
 * If the same keyword appears 3+ times in the last 20 memories, it's likely an
 * ongoing concern — create a prospective memory so we can proactively bring it up.
 */
// ═══════════════════════════════════════════════════════════════════════════════
// FFT 周期学习：分析关键词在历史记忆中的时间周期性
// 原创算法——从"用户每周一问部署"这样的规律中学习
//
// 不用真正的 FFT（太重），用简化版：统计每个关键词在一周中各天的出现频率
// 如果某天的频率显著高于其他天 → 检测到周期
// ═══════════════════════════════════════════════════════════════════════════════

interface KeywordCycle {
  keyword: string
  peakDay: number        // 0=周日 1=周一 ... 6=周六
  peakHour: number       // 0-23
  frequency: number      // 在 peak 时段出现的频率
  confidence: number     // 0-1
  lastSeen: number
}

const CYCLES_PATH = resolve(DATA_DIR, 'keyword_cycles.json')
let keywordCycles: KeywordCycle[] = loadJson<KeywordCycle[]>(CYCLES_PATH, [])
function saveCycles() { debouncedSave(CYCLES_PATH, keywordCycles) }

/**
 * 从记忆历史中学习关键词周期
 * 每次 heartbeat 调用（不是每条消息）
 */
export function learnKeywordCycles(memories: { content: string; ts: number }[]) {
  if (memories.length < 50) return  // 需要足够数据

  // 提取关键词 → 按星期几/小时统计
  const weekdayFreq = new Map<string, number[]>()  // keyword → [周日, 周一, ..., 周六]
  const hourFreq = new Map<string, number[]>()     // keyword → [0时, 1时, ..., 23时]

  for (const mem of memories) {
    const words = (mem.content.match(/[\u4e00-\u9fff]{2,4}|[a-zA-Z]{3,}/gi) || [])
      .map(w => w.toLowerCase())
    const d = new Date(mem.ts)
    const day = d.getDay()
    const hour = d.getHours()

    for (const w of new Set(words)) {
      if (!weekdayFreq.has(w)) weekdayFreq.set(w, new Array(7).fill(0))
      if (!hourFreq.has(w)) hourFreq.set(w, new Array(24).fill(0))
      weekdayFreq.get(w)![day]++
      hourFreq.get(w)![hour]++
    }
  }

  // 检测周期：某天频率 > 平均值 × 2 且 ≥ 3 次 → 有周期
  const newCycles: KeywordCycle[] = []
  for (const [keyword, days] of weekdayFreq) {
    const total = days.reduce((s, v) => s + v, 0)
    if (total < 5) continue  // 总出现次数太少
    const avg = total / 7

    let peakDay = 0, peakCount = 0
    for (let i = 0; i < 7; i++) {
      if (days[i] > peakCount) { peakCount = days[i]; peakDay = i }
    }

    if (peakCount >= 3 && peakCount > avg * 2) {
      // 检测到周期！找峰值小时
      const hours = hourFreq.get(keyword) || new Array(24).fill(0)
      let peakHour = 0, peakHourCount = 0
      for (let i = 0; i < 24; i++) {
        if (hours[i] > peakHourCount) { peakHourCount = hours[i]; peakHour = i }
      }

      const confidence = Math.min(0.9, (peakCount / total - 1 / 7) * 3)

      newCycles.push({
        keyword,
        peakDay,
        peakHour,
        frequency: peakCount / total,
        confidence,
        lastSeen: Date.now(),
      })
    }
  }

  // 更新（保留 top 20 最高置信度的周期）
  if (newCycles.length > 0) {
    keywordCycles = newCycles.sort((a, b) => b.confidence - a.confidence).slice(0, 20)
    saveCycles()
    console.log(`[cc-soul][fft-cycles] learned ${keywordCycles.length} keyword cycles`)
  }
}

/**
 * 检查今天是否有周期性话题即将出现
 * 返回该主动提起的关键词
 */
export function getCyclicReminders(): string[] {
  const now = new Date()
  const today = now.getDay()
  const hour = now.getHours()

  const reminders: string[] = []
  for (const cycle of keywordCycles) {
    if (cycle.peakDay === today && Math.abs(cycle.peakHour - hour) <= 2 && cycle.confidence > 0.3) {
      reminders.push(cycle.keyword)
    }
  }
  return reminders
}

export function getKeywordCycleCount(): number { return keywordCycles.length }

// ═══════════════════════════════════════════════════════════════════════════════
// Auto-detect recurring themes
// ═══════════════════════════════════════════════════════════════════════════════

export function autoDetectFromMemories(memories: Memory[]) {
  // Take last 20 non-expired memories
  const recent = memories
    .filter(m => m.scope !== 'expired' && m.scope !== 'decayed')
    .slice(-20)
  if (recent.length < 5) return

  // Extract keywords (Chinese 2+ char, English 3+ char)
  const keywordCounts = new Map<string, number>()
  for (const m of recent) {
    const words = (m.content.match(/[\u4e00-\u9fff]{2,4}|[a-zA-Z]{4,}/g) || []).map(w => w.toLowerCase())
    const unique = new Set(words)
    for (const w of unique) {
      // Skip common stop words
      if (/^(什么|这个|那个|可以|不是|没有|就是|但是|然后|因为|所以|如果|the|and|for|this|that|with)$/.test(w)) continue
      keywordCounts.set(w, (keywordCounts.get(w) || 0) + 1)
    }
  }

  // Find keywords appearing 3+ times
  for (const [keyword, count] of keywordCounts) {
    if (count < 3) continue

    // Skip if we already have a PM with this trigger
    const exists = pmStore.some(pm =>
      !pm.firedAt && pm.trigger.includes(keyword) && pm.source === 'auto'
    )
    if (exists) continue

    const pm: ProspectiveMemory = {
      id: makeId(),
      trigger: keyword,
      remind: `用户近期多次提到"${keyword}"（${count}次），可能是持续关注的话题`,
      createdAt: Date.now(),
      expiresAt: Date.now() + 14 * 86400000, // 14 days
      source: 'auto',
    }
    pmStore.push(pm)
    savePM()
    console.log(`[cc-soul][prospective] auto-created from recurring theme: "${keyword}" (${count}x in last 20)`)
  }
}
