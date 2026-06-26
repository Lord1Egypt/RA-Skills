/**
 * cost-tracker.ts — Token Usage & Cost Tracking
 *
 * Tracks estimated token usage per conversation and per day.
 * Provides cost visibility for cc-soul augment budget awareness.
 */

import type { SoulModule } from './brain.ts'
import { DATA_DIR, loadJson, debouncedSave } from './persistence.ts'
import { resolve } from 'path'

// ═══════════════════════════════════════════════════════════════════════════════
// State
// ═══════════════════════════════════════════════════════════════════════════════

const COST_PATH = resolve(DATA_DIR, 'cost_tracker.json')

interface DailyUsage {
  date: string            // YYYY-MM-DD
  inputTokens: number     // estimated input tokens
  outputTokens: number    // estimated output tokens
  augmentTokens: number   // tokens used by cc-soul augments
  turns: number           // number of conversation turns
}

interface CostState {
  daily: DailyUsage[]     // rolling 30-day history
  sessionTokens: number   // current session accumulated tokens
  sessionTurns: number    // current session turns
  totalTokens: number     // all-time total
  totalTurns: number      // all-time total turns
}

export const costState: CostState = {
  daily: [],
  sessionTokens: 0,
  sessionTurns: 0,
  totalTokens: 0,
  totalTurns: 0,
}

// ═══════════════════════════════════════════════════════════════════════════════
// Persistence
// ═══════════════════════════════════════════════════════════════════════════════

function loadCostState() {
  const data = loadJson<CostState>(COST_PATH, {
    daily: [], sessionTokens: 0, sessionTurns: 0, totalTokens: 0, totalTurns: 0,
  })
  costState.daily = data.daily || []
  costState.totalTokens = data.totalTokens || 0
  costState.totalTurns = data.totalTurns || 0
  // Session resets on load
  costState.sessionTokens = 0
  costState.sessionTurns = 0
  // Trim to 30 days
  const thirtyDaysAgo = new Date(Date.now() - 30 * 86400000).toISOString().slice(0, 10)
  costState.daily = costState.daily.filter(d => d.date >= thirtyDaysAgo)
}

function saveCostState() {
  debouncedSave(COST_PATH, costState)
}

// ═══════════════════════════════════════════════════════════════════════════════
// Token estimation
// ═══════════════════════════════════════════════════════════════════════════════

/** Rough token estimate: ~1.5 tokens per CJK char, ~0.75 per English word */
function estimateTokens(text: string): number {
  if (!text) return 0
  const cjk = (text.match(/[\u4e00-\u9fff\u3400-\u4dbf]/g) || []).length
  const nonCjk = text.length - cjk
  return Math.ceil(cjk * 1.5 + nonCjk * 0.25)
}

// ═══════════════════════════════════════════════════════════════════════════════
// Public API
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Record a conversation turn's token usage.
 * Called from handler after each turn.
 */
export function recordTurnUsage(inputText: string, outputText: string, augmentTokenCount: number) {
  const inputTokens = estimateTokens(inputText)
  const outputTokens = estimateTokens(outputText)
  const total = inputTokens + outputTokens + augmentTokenCount

  // Session tracking
  costState.sessionTokens += total
  costState.sessionTurns++
  costState.totalTokens += total
  costState.totalTurns++

  // Daily tracking
  const today = new Date().toISOString().slice(0, 10)
  let daily = costState.daily.find(d => d.date === today)
  if (!daily) {
    daily = { date: today, inputTokens: 0, outputTokens: 0, augmentTokens: 0, turns: 0 }
    costState.daily.push(daily)
  }
  daily.inputTokens += inputTokens
  daily.outputTokens += outputTokens
  daily.augmentTokens += augmentTokenCount
  daily.turns++

  saveCostState()
}

/**
 * Get formatted cost summary for dashboard display.
 */
export function getCostSummary(): string {
  const lines: string[] = [
    '💰 Token Usage',
    '═══════════════════════════════',
  ]

  // Session
  lines.push(`Session: ~${costState.sessionTokens.toLocaleString()} tokens (${costState.sessionTurns} turns)`)

  // Today
  const today = new Date().toISOString().slice(0, 10)
  const todayUsage = costState.daily.find(d => d.date === today)
  if (todayUsage) {
    const todayTotal = todayUsage.inputTokens + todayUsage.outputTokens + todayUsage.augmentTokens
    lines.push(`Today: ~${todayTotal.toLocaleString()} tokens (${todayUsage.turns} turns)`)
    lines.push(`  Input: ${todayUsage.inputTokens.toLocaleString()} | Output: ${todayUsage.outputTokens.toLocaleString()} | Augments: ${todayUsage.augmentTokens.toLocaleString()}`)
  }

  // 7-day average
  const sevenDaysAgo = new Date(Date.now() - 7 * 86400000).toISOString().slice(0, 10)
  const recentDays = costState.daily.filter(d => d.date >= sevenDaysAgo)
  if (recentDays.length > 0) {
    const avgTokens = recentDays.reduce((s, d) => s + d.inputTokens + d.outputTokens + d.augmentTokens, 0) / recentDays.length
    const avgTurns = recentDays.reduce((s, d) => s + d.turns, 0) / recentDays.length
    lines.push(`7d avg: ~${Math.round(avgTokens).toLocaleString()} tokens/day (${Math.round(avgTurns)} turns/day)`)
  }

  // All-time
  lines.push(`All-time: ~${costState.totalTokens.toLocaleString()} tokens (${costState.totalTurns} turns)`)

  // Augment overhead ratio (today)
  if (todayUsage && todayUsage.inputTokens > 0) {
    const overhead = todayUsage.augmentTokens / (todayUsage.inputTokens + todayUsage.augmentTokens) * 100
    lines.push(`Augment overhead: ${overhead.toFixed(1)}%`)
  }

  return lines.join('\n')
}

/**
 * Get daily usage data for dashboard HTML chart.
 */
export function getDailyUsageData(): { dates: string[]; tokens: number[]; turns: number[] } {
  const dates = costState.daily.map(d => d.date.slice(5)) // MM-DD
  const tokens = costState.daily.map(d => d.inputTokens + d.outputTokens + d.augmentTokens)
  const turns = costState.daily.map(d => d.turns)
  return { dates, tokens, turns }
}

// ═══════════════════════════════════════════════════════════════════════════════
// SoulModule
// ═══════════════════════════════════════════════════════════════════════════════

export const costTrackerModule: SoulModule = {
  id: 'cost-tracker',
  name: 'Token 成本追踪',
  features: ['cost_tracker'],
  priority: 10,
  init() { loadCostState() },
}
