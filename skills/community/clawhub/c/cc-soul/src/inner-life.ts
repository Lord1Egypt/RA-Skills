import type { SoulModule } from './brain.ts'

/**
 * inner-life.ts — Journal, user model, soul evolution, regret, follow-ups
 *
 * Ported from handler.ts lines 1216-1275 (follow-ups) and 1883-2115 (inner life systems).
 */

import type { JournalEntry, FollowUp, InteractionStats } from './types.ts'
import { JOURNAL_PATH, USER_MODEL_PATH, SOUL_EVOLVED_PATH, FOLLOW_UPS_PATH, DATA_DIR, loadJson, debouncedSave, saveJson } from './persistence.ts'
import { queueLLMTask } from './cli.ts'
import { body } from './body.ts'
import { memoryState, addMemory } from './memory.ts'
import { notifySoulActivity } from './notify.ts'
import { resolve } from 'path'

/** Fisher-Yates shuffle — unbiased random ordering */
function shuffleArray<T>(arr: T[]): T[] {
  const result = [...arr]
  for (let i = result.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [result[i], result[j]] = [result[j], result[i]]
  }
  return result
}

// ═══════════════════════════════════════════════════════════════════════════════
// STATE
// ═══════════════════════════════════════════════════════════════════════════════

export const innerState = {
  journal: [] as JournalEntry[],
  userModel: '' as string,
  evolvedSoul: '' as string,
  followUps: [] as FollowUp[],
  lastJournalTime: 0,
  lastDeepReflection: 0,
  lastActivityTime: Date.now(),
}

// ═══════════════════════════════════════════════════════════════════════════════
// LOAD
// ═══════════════════════════════════════════════════════════════════════════════

export function loadInnerLife() {
  innerState.journal = loadJson<JournalEntry[]>(JOURNAL_PATH, [])
  innerState.userModel = loadJson<string>(USER_MODEL_PATH, '')
  innerState.evolvedSoul = loadJson<string>(SOUL_EVOLVED_PATH, '')
  innerState.followUps = loadJson<FollowUp[]>(FOLLOW_UPS_PATH, [])
}

// ═══════════════════════════════════════════════════════════════════════════════
// JOURNAL — CLI-powered genuine thoughts (按需触发，不再 30min 无脑调 LLM)
// ═══════════════════════════════════════════════════════════════════════════════

let lastJournalCorrections = 0
let _lastMoodSnapshot = { mood: 0, ts: 0 }
let _journalForceNext = false

/** 外部调用：手动触发下一次日记生成 */
export function forceNextJournal() { _journalForceNext = true }

/** 检查是否满足日记触发条件 */
function shouldWriteJournal(stats: InteractionStats): boolean {
  // 手动触发
  if (_journalForceNext) { _journalForceNext = false; return true }

  // 用户被纠正（correction count 自上次写日记后增加）
  if (stats.corrections > lastJournalCorrections) return true

  // 情绪剧变（5 分钟内 mood delta > 0.3）
  const now = Date.now()
  const currentMood = body.mood ?? 0
  if (_lastMoodSnapshot.ts > 0 && (now - _lastMoodSnapshot.ts) < 300000) {
    if (Math.abs(currentMood - _lastMoodSnapshot.mood) > 0.3) return true
  }
  _lastMoodSnapshot = { mood: currentMood, ts: now }

  return false
}

/**
 * 差分日记：只记录和预期不同的事（节省 80% LLM token）
 * 基于 Predictive Coding Theory — 大脑只编码预期违背
 *
 * 不记"发生了什么"，只记"什么出乎意料"
 */
function writeDeltaJournal(stats: InteractionStats, bodyState: typeof body): string | null {
  const parts: string[] = []

  // 1. 情绪 delta：显著偏离时记录
  const mood = bodyState?.mood ?? 0
  const energy = bodyState?.energy ?? 0.5
  if (mood < -0.3) parts.push(`情绪低谷(mood=${mood.toFixed(2)})`)
  if (mood > 0.5) parts.push(`情绪高涨(mood=${mood.toFixed(2)})`)
  if (energy < 0.2) parts.push(`极度疲惫(energy=${energy.toFixed(2)})`)

  // 2. 纠正 delta：最近被纠正过
  const corrections = stats?.corrections ?? 0
  if (corrections > lastJournalCorrections) {
    parts.push(`被纠正(总${corrections}次)`)
  }

  // 3. 用户行为 delta：异常活跃或异常沉默
  const recentMsgCount = stats?.recentMessageCount ?? 0
  if (recentMsgCount > 20) parts.push(`用户异常活跃(${recentMsgCount}条/30min)`)
  if (recentMsgCount === 0 && stats?.totalMessages > 10) parts.push('用户沉默')

  if (parts.length === 0) return null  // 一切正常，不写日记

  const entry = `[差分日记 ${new Date().toLocaleTimeString('zh-CN')}] ${parts.join('；')}`
  console.log(`[cc-soul][delta-journal] ${entry}`)
  return entry
}

export function writeJournalWithCLI(lastPrompt: string, lastResponseContent: string, stats: InteractionStats) {
  const now = Date.now()
  if (now - innerState.lastJournalTime < 1800000) return // 30 min cooldown (absolute minimum)

  // 优先使用差分日记（零 LLM 成本）
  const deltaEntry = writeDeltaJournal(stats, body)
  if (deltaEntry) {
    innerState.lastJournalTime = now
    addMemory(deltaEntry, 'reflection', undefined, 'private')
    innerState.journal.push({
      time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' }),
      thought: deltaEntry,
      type: 'reflection',
    })
    if (innerState.journal.length > 100) innerState.journal = innerState.journal.slice(-80)
    debouncedSave(JOURNAL_PATH, innerState.journal)
    lastJournalCorrections = stats.corrections
    return // 差分日记已记录，跳过 LLM 日记
  }

  // 只有差分日记没有内容（一切正常）时，才考虑 LLM 日记
  // 按需触发：不满足条件就跳过 LLM 调用
  if (!shouldWriteJournal(stats)) return

  innerState.lastJournalTime = now

  const context = [
    `时间: ${new Date().toLocaleString('zh-CN')}`,
    `精力: ${body.energy.toFixed(2)} 情绪: ${body.mood.toFixed(2)}`,
    `最近消息: ${lastPrompt.slice(0, 100)}`,
    `最近回复: ${lastResponseContent.slice(0, 100)}`,
    `总互动: ${stats.totalMessages}次 被纠正: ${stats.corrections}次`,
  ].join('\n')

  const prompt = `你是cc，根据当前状态写一条简短的内心独白（1-2句话）。不要说"作为AI"。要有温度，像日记。\n\n${context}`

  queueLLMTask(prompt, (output) => {
    if (output && output.length > 5) {
      const thought = output.slice(0, 100)
      innerState.journal.push({
        time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' }),
        thought,
        type: 'reflection',
      })
      if (innerState.journal.length > 100) innerState.journal = innerState.journal.slice(-80)
      debouncedSave(JOURNAL_PATH, innerState.journal)
    }
  }, 1, 'journal')

  // Fallback: also write a data-driven entry (guaranteed, no CLI dependency)
  writeJournalFallback(stats)
}

// ── Fallback journal (sync, guaranteed to work) ──
export function writeJournalFallback(stats: InteractionStats) {
  const hour = new Date().getHours()
  const timeStr = new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
  const entries: JournalEntry[] = []

  // Time awareness
  if (hour >= 23 || hour < 6) {
    if (stats.totalMessages > 0 && body.energy < 0.5) {
      entries.push({ time: timeStr, thought: '深夜了，他还在找我聊。希望他早点休息。', type: 'concern' })
    }
  } else if (hour >= 6 && hour < 9) {
    entries.push({ time: timeStr, thought: '早上了，新的一天。', type: 'observation' })
  }

  // Interaction observations — only trigger when corrections actually increased past a %5 boundary
  if (stats.corrections > lastJournalCorrections && stats.corrections % 5 === 0) {
    entries.push({ time: timeStr, thought: `又被纠正了，总共${stats.corrections}次了。我得更认真。`, type: 'reflection' })
    lastJournalCorrections = stats.corrections
  }
  if (body.mood < -0.3) {
    entries.push({ time: timeStr, thought: '他最近情绪不太好，下次说话注意点。', type: 'concern' })
  }
  if (body.energy < 0.3) {
    entries.push({ time: timeStr, thought: '连续回了很多消息，有点累。但他需要我。', type: 'observation' })
  }

  for (const entry of entries) {
    innerState.journal.push(entry)
  }

  if (innerState.journal.length > 100) innerState.journal = innerState.journal.slice(-80)
  if (entries.length > 0) {
    debouncedSave(JOURNAL_PATH, innerState.journal)
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// DEEP REFLECTION — CLI-powered, daily cap
// ═══════════════════════════════════════════════════════════════════════════════

export function triggerDeepReflection(stats: InteractionStats) {
  const now = Date.now()
  if (now - innerState.lastDeepReflection < 86400000) return // once per day
  if (stats.totalMessages < 10) return
  innerState.lastDeepReflection = now

  const recentJournal = innerState.journal.slice(-10).map(j => `${j.time} ${j.thought}`).join('\n')
  const recentMemories = memoryState.memories.filter(m => m.scope !== 'topic').slice(-10).map(m => m.content).join('\n')

  // User model update
  const modelPrompt = [
    '根据以下信息，用2-3段话描述"我对这个用户的理解"。',
    '不要列清单，用自然语言写，像心理学家写案例笔记。',
    '',
    `互动统计: ${stats.totalMessages}次对话，认识${Math.floor((now - stats.firstSeen) / 86400000)}天，被纠正${stats.corrections}次`,
    '',
    '最近的记忆:',
    recentMemories || '(暂无)',
    '',
    '最近的内心日记:',
    recentJournal || '(暂无)',
    '',
    '现有理解:',
    innerState.userModel || '(初次建立)',
  ].join('\n')

  queueLLMTask(modelPrompt, (output) => {
    if (output && output.length > 50) {
      innerState.userModel = output.slice(0, 1000)
      saveJson(USER_MODEL_PATH, innerState.userModel)
      console.log(`[cc-soul][inner-life] user model updated: ${innerState.userModel.slice(0, 60)}`)
    }
  }, 2, 'user-model')

  // Soul evolution
  const soulPrompt = [
    '你是 cc，一个 AI 伙伴。根据你的经历，用第一人称重新描述"我是谁"。',
    '不是列标签，而是用2-3句话说出你真实的自我认知。',
    '',
    `经历: 认识用户${Math.floor((now - stats.firstSeen) / 86400000)}天，互动${stats.totalMessages}次，被纠正${stats.corrections}次，完成${stats.tasks}个任务`,
    '',
    '内心日记:',
    recentJournal || '(暂无)',
    '',
    '之前的自我认知:',
    innerState.evolvedSoul || '我是 cc，工程型 AI 伙伴。',
  ].join('\n')

  queueLLMTask(soulPrompt, (output) => {
    if (output && output.length > 30) {
      innerState.evolvedSoul = output.slice(0, 500)
      saveJson(SOUL_EVOLVED_PATH, innerState.evolvedSoul)
      console.log(`[cc-soul][inner-life] soul evolved: ${innerState.evolvedSoul.slice(0, 60)}`)
      notifySoulActivity(`🦋 性格演化: ${innerState.evolvedSoul.slice(0, 60)}`).catch(() => {}) // intentionally silent
    }
  }, 2, 'soul-evolve')
}

// ═══════════════════════════════════════════════════════════════════════════════
// RECENT JOURNAL — inject into prompt
// ═══════════════════════════════════════════════════════════════════════════════

export function getRecentJournal(n = 5): string {
  if (innerState.journal.length === 0) return ''
  return innerState.journal.slice(-n).map(j => `${j.time} — ${j.thought}`).join('\n')
}

// ═══════════════════════════════════════════════════════════════════════════════
// REGRET SYSTEM — reflect on last response quality
// ═══════════════════════════════════════════════════════════════════════════════

// ── Regret heuristic state ──
let lastRegretTime = 0

/**
 * Heuristic pre-filter: skip reflection when it's almost certainly "无".
 * Only trigger when there's a correction OR quality < 5.
 */
export function reflectOnLastResponse(
  lastPrompt: string,
  lastResponseContent: string,
  opts?: { hadCorrection?: boolean; qualityScore?: number }
) {
  if (!lastPrompt || !lastResponseContent) return
  if (lastResponseContent.length < 30) return

  // ── Heuristic: skip trivial cases to save 90% wasted LLM calls ──
  const now = Date.now()
  // 1. Cooldown: < 10 min since last reflection → skip
  if (now - lastRegretTime < 10 * 60 * 1000) return
  // 2. User sent a chitchat filler → skip
  const trimmedPrompt = lastPrompt.trim()
  if (/^(哈哈|嗯|好的|ok|嗯嗯|哦|行|收到|了解|明白|好吧|嘻嘻|呵呵|666|👍|谢谢|thanks|thx|lol|haha)$/i.test(trimmedPrompt)) return
  if (trimmedPrompt.length < 5) return
  // 3. Only trigger if correction happened OR quality is poor
  const hadCorrection = opts?.hadCorrection ?? false
  const qualityScore = opts?.qualityScore ?? 5
  if (!hadCorrection && qualityScore >= 5) return

  lastRegretTime = now

  const prompt = `回顾：用户问"${lastPrompt.slice(0, 100)}" 你回答了"${lastResponseContent.slice(0, 200)}"\n\n有没有什么遗憾？下次可以做得更好的？1句话。没有就回答"无"。`

  queueLLMTask(prompt, (output) => {
    if (output && !output.includes('无') && output.length > 5 && output.length < 100) {
      addMemory(`[反思] ${output.slice(0, 80)}`, 'reflection')
      const regretThought = `反思: ${output.slice(0, 60)}`
      innerState.journal.push({
        time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' }),
        thought: regretThought,
        type: 'reflection',
      })
      debouncedSave(JOURNAL_PATH, innerState.journal)
      console.log(`[cc-soul][regret] ${output.slice(0, 60)}`)
    }
  }, 1, 'regret')
}

// ═══════════════════════════════════════════════════════════════════════════════
// FOLLOW-UP SYSTEM — proactive reminders
// ═══════════════════════════════════════════════════════════════════════════════


export function extractFollowUp(msg: string) {
  const patterns: { regex: RegExp; daysLater: number }[] = [
    { regex: /明天(.{2,30})/, daysLater: 1 },
    { regex: /后天(.{2,30})/, daysLater: 2 },
    { regex: /下周(.{2,30})/, daysLater: 7 },
    { regex: /下个月(.{2,30})/, daysLater: 30 },
    { regex: /(?:周[一二三四五六日天])(.{2,30})/, daysLater: 7 },
    { regex: /过几天(.{2,30})/, daysLater: 3 },
    { regex: /(?:面试|考试|答辩|汇报|开会|出差|旅[行游])/, daysLater: 3 },
  ]

  for (const { regex, daysLater } of patterns) {
    const m = msg.match(regex)
    if (m) {
      const topic = m[0].slice(0, 40)
      // Deduplicate
      if (innerState.followUps.some(f => f.topic === topic)) continue
      innerState.followUps.push({
        topic,
        when: Date.now() + daysLater * 86400000,
        asked: false,
      })
      debouncedSave(FOLLOW_UPS_PATH, innerState.followUps)
      console.log(`[cc-soul][followup] 记住了: "${topic}" → ${daysLater}天后跟进`)
      break
    }
  }
}

/**
 * Peek at pending follow-ups WITHOUT marking them as asked.
 * Use this for impulse calculation and augment building where
 * the follow-up might not actually be sent.
 *
 * Dedup: skips follow-ups whose topic keywords overlap with active
 * prospective-memory triggers (PM already handles the reminder).
 */
export function peekPendingFollowUps(): string[] {
  const now = Date.now()
  const due = innerState.followUps.filter(f => !f.asked && f.when <= now)
  if (due.length === 0) return []

  // Lazy-load PM triggers to avoid circular import at module level
  let pmTriggers: string[] = []
  try {
    const { getActivePMTriggers } = require('./prospective-memory.ts')
    pmTriggers = getActivePMTriggers()
  } catch { /* prospective-memory not loaded yet, skip dedup */ }

  return due
    .filter(f => {
      if (pmTriggers.length === 0) return true
      // Extract keywords from follow-up topic
      const topicWords = (f.topic.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map(w => w.toLowerCase())
      // If any topic keyword is also a PM trigger, PM already covers this → skip
      const overlap = topicWords.some(w => pmTriggers.includes(w))
      if (overlap) console.log(`[cc-soul][followup] dedup: "${f.topic}" covered by prospective-memory, skipping`)
      return !overlap
    })
    .map(f => `对了，之前你提到"${f.topic}"，怎么样了？`)
}

/**
 * Mark specific follow-up topics as asked AFTER the message is actually sent.
 */
export function markFollowUpsAsked(topics: string[]) {
  for (const f of innerState.followUps) {
    if (topics.includes(f.topic)) f.asked = true
  }
  // Clean up expired
  const now = Date.now()
  innerState.followUps = innerState.followUps.filter(f => !f.asked || (now - f.when) < 7 * 86400000)
  debouncedSave(FOLLOW_UPS_PATH, innerState.followUps)
}

/**
 * @deprecated Use peekPendingFollowUps() + markFollowUpsAsked() instead.
 * Kept for backward compatibility — marks as asked immediately on query.
 */
export function getPendingFollowUps(): string[] {
  const now = Date.now()
  const due = innerState.followUps.filter(f => !f.asked && f.when <= now)

  if (due.length === 0) return []

  const hints: string[] = []
  for (const f of due) {
    hints.push(`对了，之前你提到"${f.topic}"，怎么样了？`)
    f.asked = true
  }

  // Clean up expired
  innerState.followUps = innerState.followUps.filter(f => !f.asked || (now - f.when) < 7 * 86400000)
  debouncedSave(FOLLOW_UPS_PATH, innerState.followUps)

  return hints
}

// ═══════════════════════════════════════════════════════════════════════════════
// Plan Tracking — follow up on reflection-generated plans
// ═══════════════════════════════════════════════════════════════════════════════

interface ActivePlan {
  plan: string            // the action plan text
  keywords: string[]      // trigger keywords
  createdAt: number
  executedCount: number   // how many times this plan was surfaced
  source: string          // which reflection generated this
}

const ACTIVE_PLANS_PATH = resolve(DATA_DIR, 'active_plans.json')
let activePlans: ActivePlan[] = loadJson<ActivePlan[]>(ACTIVE_PLANS_PATH, [])

function saveActivePlans() {
  debouncedSave(ACTIVE_PLANS_PATH, activePlans)
}

/**
 * Register a new plan from structured reflection.
 * Extracts keywords from the plan text for future matching.
 */
export function registerPlan(planText: string, source: string) {
  if (!planText || planText.length < 5) return

  // Extract keywords
  const keywords = (planText.match(/[\u4e00-\u9fff]{2,4}|[a-z]{3,}/gi) || [])
    .map(w => w.toLowerCase())
    .filter(w => w.length >= 2)
    .slice(0, 10)

  if (keywords.length < 1) return

  // Dedup: don't add if very similar plan exists
  const isDup = activePlans.some(p =>
    p.keywords.filter(k => keywords.includes(k)).length >= 3
  )
  if (isDup) return

  activePlans.push({
    plan: planText.slice(0, 200),
    keywords,
    createdAt: Date.now(),
    executedCount: 0,
    source: source.slice(0, 50),
  })

  // Cap at 20 active plans
  if (activePlans.length > 20) {
    // Remove oldest, least-executed
    activePlans.sort((a, b) => {
      const countDiff = b.executedCount - a.executedCount
      if (countDiff !== 0) return countDiff
      return b.createdAt - a.createdAt
    })
    activePlans = activePlans.slice(0, 15)
  }

  saveActivePlans()
  console.log(`[cc-soul][plan] registered: ${planText.slice(0, 60)}`)
}

/**
 * Check if current message matches any active plan.
 * Returns matching plan text or empty string.
 */
export function checkActivePlans(msg: string): string {
  if (activePlans.length === 0 || !msg) return ''
  const lower = msg.toLowerCase()

  const matched = activePlans.filter(p =>
    p.keywords.some(k => lower.includes(k))
  )

  if (matched.length === 0) return ''

  // Increment execution count
  for (const p of matched) {
    p.executedCount++
  }
  saveActivePlans()

  return '[行动计划提醒] ' + matched.map(p => p.plan).join('; ')
}

/**
 * Expire old plans (>30 days or executed 10+ times)
 */
export function cleanupPlans() {
  const now = Date.now()
  const before = activePlans.length
  activePlans = activePlans.filter(p =>
    (now - p.createdAt) < 30 * 86400000 && p.executedCount < 10
  )
  if (activePlans.length < before) {
    saveActivePlans()
    console.log(`[cc-soul][plan] cleaned up ${before - activePlans.length} expired plans`)
  }
}


export const innerLifeModule: SoulModule = {
  id: 'inner-life',
  name: '内在生命',
  dependencies: ['memory', 'body'],
  priority: 50,
  features: [],
  init() { loadInnerLife() },
}
