/**
 * features.ts — Feature toggle system
 *
 * Users can enable/disable individual cc-soul features via data/features.json.
 * All modules check isEnabled() before running.
 */

import { existsSync } from 'fs'
import { FEATURES_PATH, loadJson, saveJson } from './persistence.ts'

// ── Always-on features: zero-cost or essential, no toggle needed ──
const ALWAYS_ON = new Set([
  'memory_active', 'memory_consolidation', 'memory_contradiction_scan',
  'memory_tags', 'memory_core', 'memory_working',
  'auto_topic_save', 'auto_memory_reference', 'auto_memory_chain',
  'auto_repeat_detect', 'attention_decay', 'rhythm_adaptation',
  'trust_annotation', 'cost_tracker', 'wal_protocol', 'dag_archive',
  'auto_natural_citation', 'auto_contradiction_hint',
  // v2.3: promoted from DEFAULTS — zero-cost local computation
  'memory_associative_recall', 'memory_predictive', 'episodic_memory',
  'relationship_dynamics', 'intent_anticipation', 'plan_tracking',
  'smart_forget', 'context_compress', 'persona_drift', 'persona_drift_detection',
  'a2a', 'theory_of_mind', 'predictive_memory', 'scenario_shortcut',
  'context_reminder', 'auto_time_travel',
  'persona_splitting', 'emotional_contagion',
  'lorebook', 'skill_library',
  'emotional_arc', 'metacognition', 'autonomous_goals', 'cron_agent',
])

// ── Default features (all ON) ──

const DEFAULTS: Record<string, boolean> = {
  // Always-on core features are in ALWAYS_ON set above (no toggle needed)
  // Only features that users might genuinely want to disable remain here

  auto_daily_review: false,     // 关：每晚自动日报，有人觉得骚扰
  self_correction: true,        // 回复后自检，消耗 token
  memory_session_summary: true, // 会话摘要，消耗 token
  absence_detection: true,      // "你好久没提X"，有人觉得被监视
  behavior_prediction: true,    // 行为预测，有人觉得 creepy
  auto_mood_care: true,         // 情绪低落主动关心，有人觉得多余
}

// ── State ──

let features: Record<string, boolean> = { ...DEFAULTS }

// ── Public API ──

export function loadFeatures() {
  if (!existsSync(FEATURES_PATH)) {
    features = { ...DEFAULTS }
    saveJson(FEATURES_PATH, features)
    const on = Object.values(features).filter(v => v).length
    console.log(`[cc-soul][features] ${on}/${Object.keys(features).length} features enabled (fresh)`)
    return
  }

  const loaded = loadJson<Record<string, boolean>>(FEATURES_PATH, {})
  // Only add missing keys from DEFAULTS, never overwrite existing values
  let needsSave = false
  for (const [k, v] of Object.entries(DEFAULTS)) {
    if (!(k in loaded)) {
      loaded[k] = v
      needsSave = true
    }
  }
  // Remove always-on features from persisted file (they're hardcoded now)
  for (const k of ALWAYS_ON) {
    if (k in loaded) {
      delete loaded[k]
      needsSave = true
    }
  }
  features = loaded
  if (needsSave) saveJson(FEATURES_PATH, features)

  const on = Object.values(features).filter(v => v).length
  console.log(`[cc-soul][features] ${on}/${Object.keys(features).length} features enabled`)
}

/**
 * Check if a feature is enabled.
 * Usage: if (isEnabled('auto_daily_review')) { ... }
 */
export function isEnabled(feature: string): boolean {
  if (ALWAYS_ON.has(feature)) return true
  if (!(feature in features)) {
    console.warn(`[cc-soul][features] unknown feature "${feature}" — defaulting to OFF`)
    return false
  }
  return features[feature] !== false
}

/**
 * Toggle a feature at runtime (also saves to disk).
 */
export function setFeature(feature: string, enabled: boolean) {
  if (ALWAYS_ON.has(feature)) {
    console.log(`[cc-soul][features] ${feature} is always-on, cannot toggle`)
    return
  }
  if (!(feature in features)) return
  features[feature] = enabled
  saveJson(FEATURES_PATH, features)
  console.log(`[cc-soul][features] ${feature} → ${enabled ? 'ON' : 'OFF'}`)
}

/**
 * Get all feature states (for status display / dashboard).
 */
export function getAllFeatures(): Record<string, boolean> {
  const result: Record<string, boolean> = {}
  for (const k of ALWAYS_ON) result[k] = true
  Object.assign(result, features)
  return result
}

/**
 * Handle feature toggle commands from user messages.
 * "开启 auto_daily_review" / "关闭 xxx" / "功能状态"
 */
export function handleFeatureCommand(msg: string): string | boolean {
  const m = msg.trim()

  // Owner-only features: hidden from status display and cannot be toggled
  const HIDDEN_FEATURES = new Set(['self_upgrade', '_comment'])

  // Status check
  if (m === '功能状态' || m === 'features' || m === 'feature status') {
    const alwaysOnLines = [...ALWAYS_ON].map(k => `  🔒 ${k} (always-on)`)
    const toggleLines = Object.entries(features)
      .filter(([k]) => !HIDDEN_FEATURES.has(k))
      .map(([k, v]) => `  ${v ? '✅' : '❌'} ${k}`)
    const enabled = Object.entries(features).filter(([k, v]) => !HIDDEN_FEATURES.has(k) && v).length + ALWAYS_ON.size
    const total = Object.entries(features).filter(([k]) => !HIDDEN_FEATURES.has(k)).length + ALWAYS_ON.size
    const lines = [...alwaysOnLines, ...toggleLines].join('\n')
    console.log(`[cc-soul][features] status:\n${lines}`)
    return `功能开关 (${enabled}/${total} 已启用)\n${lines}`
  }

  // Owner-only features: cannot be toggled by regular users via chat
  const OWNER_ONLY = new Set(['self_upgrade'])

  // Toggle: "开启 xxx" / "关闭 xxx"
  const onMatch = m.match(/^(?:开启|启用|enable)\s+(\S+)$/)
  if (onMatch && ALWAYS_ON.has(onMatch[1])) {
    return `🔒 ${onMatch[1]} 是核心功能，始终开启，无法切换`
  }
  if (onMatch && onMatch[1] in features) {
    if (OWNER_ONLY.has(onMatch[1])) {
      console.log(`[cc-soul][features] ${onMatch[1]} is owner-only, cannot enable via chat`)
      return true
    }
    setFeature(onMatch[1], true)
    return `✅ 已开启: ${onMatch[1]}`
  }

  const offMatch = m.match(/^(?:关闭|禁用|disable)\s+(\S+)$/)
  if (offMatch && ALWAYS_ON.has(offMatch[1])) {
    return `🔒 ${offMatch[1]} 是核心功能，始终开启，无法切换`
  }
  if (offMatch && offMatch[1] in features) {
    if (OWNER_ONLY.has(offMatch[1])) {
      console.log(`[cc-soul][features] ${offMatch[1]} is owner-only, cannot disable via chat`)
      return `⚠️ ${offMatch[1]} 是 Owner 专属功能，无法通过聊天切换`
    }
    setFeature(offMatch[1], false)
    return `❌ 已关闭: ${offMatch[1]}`
  }

  return false
}
