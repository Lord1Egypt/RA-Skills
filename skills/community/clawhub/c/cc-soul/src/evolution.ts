import type { SoulModule } from './brain.ts'

/**
 * evolution.ts — Rules + Hypotheses + Advanced Evolution
 *
 * Ported from handler.ts lines 1023-1099 (rules) + 1384-1480 (hypotheses/advanced).
 */

import { createHash } from 'crypto'
import { existsSync, mkdirSync, writeFileSync, readFileSync, readdirSync } from 'fs'
import type { Rule, Hypothesis } from './types.ts'
import { resolve } from 'path'
import { RULES_PATH, HYPOTHESES_PATH, DATA_DIR, loadJson, debouncedSave } from './persistence.ts'
import { addMemory, trigrams, trigramSimilarity } from './memory.ts'
import { notifySoulActivity } from './notify.ts'
import { spawnCLI, queueLLMTask } from './cli.ts'
import { extractJSON } from './utils.ts'
import { getParam } from './auto-tune.ts'
// audit.ts removed
import { detectDomain } from './epistemic.ts'

// ── Bayesian utilities ──

/** Beta distribution posterior mean */
function betaMean(alpha: number, beta: number): number {
  return alpha / (alpha + beta)
}

/** Wilson score lower bound — 95% CI lower bound without scipy */
function betaLowerBound(alpha: number, beta: number, z = 1.96): number {
  const n = alpha + beta - 2
  if (n <= 0) return 0
  const p = (alpha - 1) / n
  return (p + z * z / (2 * n) - z * Math.sqrt((p * (1 - p) + z * z / (4 * n)) / n)) /
         (1 + z * z / n)
}

/** Enough data for statistical significance? */
function isSignificant(alpha: number, beta: number, minSamples = 8): boolean {
  return (alpha + beta - 2) >= minSamples
}

// ── State ──

const MAX_RULES = 50

export let rules: Rule[] = []
export let hypotheses: Hypothesis[] = []

/** Getter for cross-module access (avoids circular import issues) */
export function getRules(): Rule[] { return rules }

function md5(s: string): string {
  return createHash('md5').update(s).digest('hex').slice(0, 16)
}

// ── Rules ──

export function loadRules() {
  rules = loadJson<Rule[]>(RULES_PATH, [])
}

function saveRules() {
  debouncedSave(RULES_PATH, rules)
}

// Rule dedup threshold now tunable via auto-tune

/** Compress rules by merging similar pairs (trigram similarity > 0.6) */
function compressRules() {
  const MERGE_THRESHOLD = 0.6
  const merged = new Set<number>()

  for (let i = 0; i < rules.length; i++) {
    if (merged.has(i)) continue
    const triA = trigrams(rules[i].rule)
    for (let j = i + 1; j < rules.length; j++) {
      if (merged.has(j)) continue
      const triB = trigrams(rules[j].rule)
      if (trigramSimilarity(triA, triB) > MERGE_THRESHOLD) {
        // Keep the one with higher hitCount, absorb the other
        const [keep, drop] = rules[i].hits >= rules[j].hits ? [i, j] : [j, i]
        rules[keep].hits += rules[drop].hits
        rules[keep].rule = rules[keep].rule.length >= rules[drop].rule.length
          ? rules[keep].rule
          : rules[drop].rule  // keep the more detailed version
        merged.add(drop)
        console.log(`[cc-soul][evolve] rule compress: merged "${rules[drop].rule.slice(0, 30)}" into "${rules[keep].rule.slice(0, 30)}"`)
        if (drop === i) break
      }
    }
  }

  if (merged.size > 0) {
    const before = rules.length
    // Filter in-place
    const kept = rules.filter((_, idx) => !merged.has(idx))
    rules.length = 0
    rules.push(...kept)
    console.log(`[cc-soul][evolve] rule compress: ${before} → ${rules.length} (merged ${merged.size})`)
  }
}

const DOMAIN_GENERALIZATION: Record<string, string> = {
  python: '回答 Python 相关问题时要特别谨慎，先确认版本号和具体特性再回答',
  javascript: '回答 JS/TS 相关问题时注意区分运行时和框架版本差异',
  swift: '回答 Swift 相关问题时注意区分 Swift 版本和 API 变更',
  'ios-reverse': '回答 iOS 逆向问题时注意工具版本和系统兼容性',
  rust: '回答 Rust 问题时注意 edition 和 API 稳定性差异',
  golang: '回答 Go 问题时注意版本和模块系统差异',
  database: '回答数据库问题时注意引擎差异和版本兼容',
  devops: '回答运维问题时注意发行版和工具版本差异',
  git: '回答 Git 问题时注意不同平台和版本的行为差异',
}

/** A3: distill common patterns from multiple rules */
function distillRules(ruleList: any[]): string | null {
  if (ruleList.length < 2) return null

  // Path A: fact-store triple common factors
  try {
    const { extractFacts } = require('./fact-store.ts')
    const allFacts = ruleList.flatMap((r: any) => extractFacts(r.rule || r.text || ''))
    const predCounts = new Map<string, number>()
    for (const f of allFacts) {
      const key = `${f.subject}:${f.predicate}`
      predCounts.set(key, (predCounts.get(key) || 0) + 1)
    }
    const common = [...predCounts.entries()].filter(([, c]) => c >= 2).map(([k]) => k.replace(':', ' → '))
    if (common.length > 0) return `[规则共性] ${common.join('; ')}`
  } catch {}

  // Path B: keyword intersection fallback
  const wordSets = ruleList.map((r: any) => {
    const text = r.rule || r.text || ''
    return new Set((text.match(/[\u4e00-\u9fff]{2,}|[a-zA-Z]{3,}/gi) || []).map((w: string) => w.toLowerCase()))
  })
  let intersection = new Set(wordSets[0] || [])
  for (let i = 1; i < wordSets.length; i++) {
    intersection = new Set([...intersection].filter(w => wordSets[i].has(w)))
  }
  if (intersection.size >= 2) return `[${[...intersection].slice(0, 3).join('/')}] 注意相关问题`
  return null
}

/** After adding a rule, check if its domain has 2+ rules → create a generalized rule */
export function generalizeRules(newRuleText: string) {
  const domain = detectDomain(newRuleText)
  const template = DOMAIN_GENERALIZATION[domain]
  if (!template) return
  // Count rules in same domain (excluding generalized ones already present)
  const sameDomain = rules.filter(r => detectDomain(r.rule) === domain && r.source !== 'generalized')
  if (sameDomain.length < 2) return

  // A3: try distillRules first — use data-driven generalization if available
  const distilled = distillRules(sameDomain)
  const ruleText = distilled || template

  // Already have a generalized rule for this domain?
  const existing = rules.find(r => r.rule === ruleText)
  if (existing) {
    existing.hits = Math.max(existing.hits, ...sameDomain.map(r => r.hits)) + 1
    return
  }
  const maxHits = Math.max(...sameDomain.map(r => r.hits), 1)
  rules.push({ rule: ruleText, source: 'generalized', ts: Date.now(), hits: maxHits + 1 })
  console.log(`[cc-soul][evolve] generalized rule for domain=${domain}: "${ruleText.slice(0, 50)}"`)
}

export function addRule(rule: string, source: string) {
  if (!rule || rule.length < 5) return
  // Exact dedup
  if (rules.some(r => r.rule === rule)) return

  // Semantic dedup: trigram similarity check against existing rules
  const newTrigrams = trigrams(rule)
  const similar = rules.find(r => trigramSimilarity(trigrams(r.rule), newTrigrams) > getParam('evolution.rule_dedup_threshold'))
  if (similar) {
    // Merge: keep the existing rule but bump its hits and update source
    similar.hits++
    console.log(`[cc-soul][evolve] rule dedup: "${rule.slice(0, 40)}" merged into "${similar.rule.slice(0, 40)}"`)
    saveRules()
    return
  }

  // ── Causal context: extract conditions from rule content ──
  const CJK_RE = /[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi
  const conditions = (rule.match(CJK_RE) || []).map((w: string) => w.toLowerCase()).slice(0, 5)

  rules.push({
    rule, source: source.slice(0, 100), ts: Date.now(), hits: 0,
    cause: source.includes('纠正') || source.includes('correction') ? source.slice(0, 80) : undefined,
    conditions: conditions.length > 0 ? conditions : undefined,
  })

  // Correction generalization: if domain has 2+ rules, create a broader rule
  generalizeRules(rule)

  // Compress: when rules exceed 40, merge similar pairs via trigram similarity
  if (rules.length > 40) {
    compressRules()
  }

  if (rules.length > MAX_RULES) {
    // Remove least hit oldest rules (in-place to preserve export let reference)
    rules.sort((a, b) => (b.hits * 10 + b.ts / 1e10) - (a.hits * 10 + a.ts / 1e10) || b.ts - a.ts)
    rules.length = MAX_RULES
  }
  saveRules()
}

export function getRelevantRules(msg: string, topN = 3, trackHits = true): Rule[] {
  if (rules.length === 0) return []

  const msgWords = new Set((msg.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map(w => w.toLowerCase()))
  if (msgWords.size === 0) return rules.slice(0, topN) // return most recent if can't match

  const scored = rules.map(r => {
    const ruleWords = (r.rule.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).map(w => w.toLowerCase())
    const overlap = ruleWords.filter(w => msgWords.has(w)).length

    // ── Causal condition matching: rules with conditions get boosted when conditions match ──
    let conditionBoost = 0
    if (r.conditions && r.conditions.length > 0) {
      const condHits = r.conditions.filter(c => msgWords.has(c)).length
      conditionBoost = condHits / r.conditions.length // 0-1: how many conditions match
      // Rules with unmet conditions get penalized (wrong context)
      if (condHits === 0 && r.conditions.length >= 2) conditionBoost = -0.5
    }

    // Quality-aware scoring: rules that led to good responses get boosted
    let qualityBoost = 0
    if (r.matchedCount && r.matchedCount >= 3 && r.matchedQualitySum) {
      const avgQuality = r.matchedQualitySum / r.matchedCount
      qualityBoost = avgQuality >= 7 ? 0.5 : avgQuality <= 3 ? -0.5 : 0
    }

    return { ...r, score: overlap + r.hits * 0.1 + conditionBoost + qualityBoost }
  })

  scored.sort((a, b) => b.score - a.score)
  const relevant = scored.filter(r => r.score > 0).slice(0, topN)

  // Increment hits + matchedCount (skip when called from prompt-builder to avoid double counting)
  if (trackHits) {
    for (const r of relevant) {
      const orig = rules.find(o => o.rule === r.rule)
      if (orig) {
        orig.hits++
        orig.matchedCount = (orig.matchedCount || 0) + 1
      }
    }
  }

  return relevant
}

// ── Hypotheses ──

export function loadHypotheses() {
  hypotheses = loadJson<Hypothesis[]>(HYPOTHESES_PATH, [])
  // Migration: convert old counter format to Bayesian
  for (const h of hypotheses) {
    if (h.alpha === undefined || h.beta === undefined) {
      h.alpha = 1 + (h.evidence_for || 0)
      h.beta = 1 + (h.evidence_against || 0)
    }
  }
}

export function formHypothesis(pattern: string, observation: string) {
  const id = md5(pattern)
  if (hypotheses.some(h => h.id === id)) return

  hypotheses.push({
    id,
    description: `当遇到"${pattern.slice(0, 30)}"时: ${observation.slice(0, 60)}`,
    alpha: 2,   // prior Beta(1,1) + 1 initial success observation
    beta: 1,
    status: 'active',
    created: Date.now(),
    verifyCount: 0,
  })

  // 限制数量 (in-place to preserve export let reference)
  if (hypotheses.length > 30) {
    const kept = hypotheses
      .filter(h => h.status !== 'rejected')
      .sort((a, b) => betaMean(b.alpha, b.beta) - betaMean(a.alpha, a.beta) || b.created - a.created)
      .slice(0, 25)
    hypotheses.length = 0
    hypotheses.push(...kept)
  }

  saveHypothesesSafe()
  console.log(`[cc-soul][evolve] 新假设: ${pattern.slice(0, 30)} → ${observation.slice(0, 40)}`)
  notifySoulActivity(`🧬 新假设: ${pattern.slice(0, 30)} → ${observation.slice(0, 40)}`).catch(() => {}) // intentionally silent
}

function saveHypothesesSafe() {
  if (hypotheses === undefined || hypotheses === null) return
  debouncedSave(HYPOTHESES_PATH, hypotheses)
}

let _verifyingHypotheses = false
export function verifyHypothesis(situation: string, wasCorrect: boolean) {
  if (_verifyingHypotheses) return // prevent recursion
  _verifyingHypotheses = true
  try {
    if (hypotheses.length === 0) {
      try { loadHypotheses() } catch {}
    }
    if (hypotheses.length === 0) { _verifyingHypotheses = false; return }
    _verifyHypothesisInner(situation, wasCorrect)
  } finally { _verifyingHypotheses = false }
}

function _verifyHypothesisInner(situation: string, wasCorrect: boolean) {
  for (const h of hypotheses) {
    if (h.status === 'rejected' || h.status === 'verified') continue

    // Match hypothesis to current situation — tightened to 0.2 to reduce false-positive token waste
    const sim = trigramSimilarity(trigrams(h.description), trigrams(situation))
    if (sim < 0.2) continue

    if (!h.verifyCount) h.verifyCount = 0

    // Bayesian update
    if (wasCorrect) { h.alpha++ } else { h.beta++ }
    const mean = betaMean(h.alpha, h.beta)
    console.log(`[cc-soul][evolve] 假设验证: "${h.description.slice(0, 40)}" sim=${sim.toFixed(2)} correct=${wasCorrect} verify=${h.verifyCount} α=${h.alpha} β=${h.beta}`)

    if (wasCorrect) {
      h.verifyCount++
    } else {
      h.verifyCount = 0
    }

    if (wasCorrect && h.verifyCount >= 3 && h.status === 'active') {
      h.status = 'verified'
      addRule(h.description, 'hypothesis_solidified')
      console.log(`[cc-soul][evolve] 规则固化: ${h.description.slice(0, 40)} (验证${h.verifyCount}次)`)
      notifySoulActivity(`🔒 规则固化: ${h.description.slice(0, 40)}`).catch(() => {}) // intentionally silent
      continue
    }

    // Reject when statistically significant and upper bound of success rate < 0.4
    // Upper bound of success = 1 - lower bound of failure rate (swap α/β)
    if (h.status === 'active' && isSignificant(h.alpha, h.beta) && (1 - betaLowerBound(h.beta, h.alpha)) < getParam('evolution.hypothesis_reject_ci_ub')) {
      h.status = 'rejected'
      console.log(`[cc-soul][evolve] 假设被否定: ${h.description.slice(0, 40)} (mean=${mean.toFixed(3)})`)
      notifySoulActivity(`❌ 假设否定: ${h.description.slice(0, 40)}`).catch(() => {}) // intentionally silent
    }
  }
  saveHypothesesSafe()
}

// ── Correction Evolution (basic pattern extraction) ──

function onCorrectionEvolution(userMsg: string) {
  const patterns = [
    /不要(.{2,30})/,
    /别(.{2,20})/,
    /应该(.{2,30})/,
    /正确的是(.{2,30})/,
  ]
  for (const p of patterns) {
    const m = userMsg.match(p)
    if (m) {
      addRule(m[0], userMsg.slice(0, 80))
      break
    }
  }
  addMemory(`纠正: ${userMsg.slice(0, 60)}`, 'correction')
}

// ── Advanced Correction (causal attribution + hypothesis) ──

export function onCorrectionAdvanced(userMsg: string, lastResponse: string) {
  // 基础规则提取
  onCorrectionEvolution(userMsg)

  // 因果归因
  const causalPatterns: { pattern: RegExp; cause: string }[] = [
    { pattern: /太长|太啰嗦|简洁/, cause: '回答太冗长，用户要简洁' },
    { pattern: /跑偏|离题|不是问/, cause: '理解偏了，没回答到点上' },
    { pattern: /不准|不对|错误/, cause: '信息不准确' },
    { pattern: /口气|语气|态度/, cause: '语气不对' },
    { pattern: /太简单|没深度|浅/, cause: '回答太浅' },
  ]

  for (const { pattern, cause } of causalPatterns) {
    if (pattern.test(userMsg)) {
      formHypothesis(userMsg.slice(0, 50), cause)
      break
    }
  }

  // 验证之前的假设：这次被纠正了 = 假设对应的策略失败
  verifyHypothesis(lastResponse, false)
}

// ── Correction Attribution (纠正归因 — LLM 判断出错根因) ──

export function attributeCorrection(userMsg: string, lastResponse: string, augmentsUsed: string[]) {
  queueLLMTask(
    `上一次回复: "${lastResponse.slice(0, 300)}"\n` +
    `注入的上下文: ${augmentsUsed.slice(0, 3).join('; ').slice(0, 200)}\n` +
    `用户纠正: "${userMsg.slice(0, 200)}"\n\n` +
    `判断回复出错的原因（只选一个）:\n` +
    `1=模型幻觉 2=记忆误导 3=规则冲突 4=理解偏差 5=领域不足\n` +
    `格式: {"cause":N,"detail":"一句话"}`,
    (output) => {
      try {
        const result = extractJSON(output)
        if (result) {
          const causeNames = ['', '模型幻觉', '记忆误导', '规则冲突', '理解偏差', '领域不足']
          const causeName = causeNames[result.cause] || '未知'
          console.log(`[cc-soul][attribution] cause=${causeName}: ${result.detail}`)
          addMemory(`[纠正归因] ${causeName}: ${result.detail}`, 'correction')
        }
      } catch (e: any) { console.error(`[cc-soul][attribution] parse error: ${e.message}`) }
    }, 3, 'attribution'
  )
}


/**
 * Record quality score for rules that were matched in the current response.
 * Called from handler.ts after scoreResponse, with the rules that were injected.
 */
export function recordRuleQuality(matchedRules: Rule[], qualityScore: number) {
  for (const r of matchedRules) {
    const orig = rules.find(o => o.rule === r.rule)
    if (orig) {
      orig.matchedQualitySum = (orig.matchedQualitySum || 0) + qualityScore
    }
  }
  saveRules()
}

// ═══════════════════════════════════════════════════════════════════════════════
// GEP — Generalized Evolution Protocol (标准化演化资产导出/导入)
// ═══════════════════════════════════════════════════════════════════════════════

export interface GEPAssets {
  version: string
  format: string
  exportedAt: string
  agent: string
  assets: {
    rules: Rule[]
    hypotheses: Hypothesis[]
    skills: string[]
    stats: {
      totalMessages: number
      corrections: number
      rulesSolidified: number
    }
    // legacy fields (kept for backward compat)
    corrections?: number
    growthVectors?: string[]
    metadata?: {
      totalMessages: number
      firstSeen: number
      rulesSolidified: number
    }
  }
}

/**
 * Export evolution assets in GEP format.
 * Returns the JSON object and writes to DATA_DIR/export/evolution_assets_{date}.json.
 */
export function exportEvolutionAssets(stats: { totalMessages: number; firstSeen: number; corrections: number }): { data: GEPAssets; path: string } {
  const exportDir = resolve(DATA_DIR, 'export')
  if (!existsSync(exportDir)) mkdirSync(exportDir, { recursive: true })

  const solidifiedCount = hypotheses.filter(h => h.status === 'verified').length

  // Collect auto-generated skill filenames
  const skillsDir = resolve(DATA_DIR, 'skills/auto')
  let skillNames: string[] = []
  try {
    if (existsSync(skillsDir)) {
      skillNames = (readdirSync(skillsDir) as string[]).filter((f: string) => f.endsWith('.md'))
    }
  } catch { /* no skills dir */ }

  const growthVectors: string[] = []

  const data: GEPAssets = {
    version: '1.0',
    format: 'GEP',
    exportedAt: new Date().toISOString(),
    agent: 'cc-soul',
    assets: {
      rules: rules.map(r => ({ ...r })),
      hypotheses: hypotheses.map(h => ({ ...h })),
      skills: skillNames,
      stats: {
        totalMessages: stats.totalMessages,
        corrections: stats.corrections,
        rulesSolidified: solidifiedCount,
      },
      // legacy fields for backward compat
      corrections: stats.corrections,
      growthVectors,
      metadata: {
        totalMessages: stats.totalMessages,
        firstSeen: stats.firstSeen,
        rulesSolidified: solidifiedCount,
      },
    },
  }

  const today = new Date().toISOString().slice(0, 10)
  const exportPath = resolve(exportDir, `evolution_assets_${today}.json`)
  writeFileSync(exportPath, JSON.stringify(data, null, 2), 'utf-8')
  console.log(`[cc-soul][gep] exported ${rules.length} rules + ${hypotheses.length} hypotheses to ${exportPath}`)

  return { data, path: exportPath }
}

/**
 * Import evolution assets from GEP format file.
 * Merges rules and hypotheses (dedup by content/id).
 */
export function importEvolutionAssets(filePath: string): { rulesAdded: number; hypothesesAdded: number } {
  const raw = readFileSync(filePath, 'utf-8')
  const data = JSON.parse(raw) as GEPAssets

  if (!data.version || !data.assets) {
    throw new Error('Invalid GEP format: missing version or assets')
  }

  let rulesAdded = 0
  let hypothesesAdded = 0

  // Import rules (dedup by rule text)
  if (Array.isArray(data.assets.rules)) {
    for (const r of data.assets.rules) {
      if (!r.rule || r.rule.length < 5) continue
      if (rules.some(existing => existing.rule === r.rule)) continue
      rules.push({
        rule: r.rule,
        source: r.source || 'gep_import',
        ts: r.ts || Date.now(),
        hits: r.hits || 0,
        matchedCount: r.matchedCount,
        matchedQualitySum: r.matchedQualitySum,
      })
      rulesAdded++
    }
    if (rules.length > MAX_RULES) {
      rules.sort((a, b) => (b.hits * 10 + b.ts / 1e10) - (a.hits * 10 + a.ts / 1e10) || b.ts - a.ts)
      rules.length = MAX_RULES
    }
    saveRules()
  }

  // Import hypotheses (dedup by id)
  if (Array.isArray(data.assets.hypotheses)) {
    for (const h of data.assets.hypotheses) {
      if (!h.id || !h.description) continue
      if (hypotheses.some(existing => existing.id === h.id)) continue
      hypotheses.push({
        id: h.id,
        description: h.description,
        alpha: h.alpha ?? 2,
        beta: h.beta ?? 1,
        status: h.status || 'active',
        created: h.created || Date.now(),
        verifyCount: h.verifyCount || 0,
      })
      hypothesesAdded++
    }
    if (hypotheses.length > 30) {
      const kept = hypotheses
        .filter(h => h.status !== 'rejected')
        .sort((a, b) => (b.alpha / (b.alpha + b.beta)) - (a.alpha / (a.alpha + a.beta)) || b.created - a.created)
        .slice(0, 25)
      hypotheses.length = 0
      hypotheses.push(...kept)
    }
    saveHypothesesSafe()
  }

  console.log(`[cc-soul][gep] imported ${rulesAdded} rules + ${hypothesesAdded} hypotheses from ${filePath}`)

  return { rulesAdded, hypothesesAdded }
}

// ═══════════════════════════════════════════════════════════════════════════════
// GRADUAL EVOLUTION (Phased Upgrades) — migrated from experiment.ts
// ═══════════════════════════════════════════════════════════════════════════════

interface EvolutionPhase {
  phase: number
  description: string
  status: 'pending' | 'active' | 'completed' | 'failed'
  startedAt: number
  duration: number
  metrics: { quality: number; corrections: number } | null
}

interface GradualEvolution {
  id: string
  goal: string
  phases: EvolutionPhase[]
  currentPhase: number
  startedAt: number
  status: 'in_progress' | 'completed' | 'abandoned'
}

const EVOLUTIONS_PATH = resolve(DATA_DIR, 'evolutions.json')
let evolutions: GradualEvolution[] = loadJson(EVOLUTIONS_PATH, [])

export function loadEvolutions() {
  evolutions = loadJson(EVOLUTIONS_PATH, [])
}

export function startEvolution(goal: string, phaseDescriptions: string[], phaseDurationDays = 2): string {
  const id = `evo_${Date.now()}`
  const phases: EvolutionPhase[] = phaseDescriptions.map((desc, i) => ({
    phase: i + 1, description: desc,
    status: i === 0 ? 'active' as const : 'pending' as const,
    startedAt: i === 0 ? Date.now() : 0, duration: phaseDurationDays * 86400000, metrics: null,
  }))
  evolutions.push({ id, goal, phases, currentPhase: 0, startedAt: Date.now(), status: 'in_progress' })
  debouncedSave(EVOLUTIONS_PATH, evolutions)
  return id
}

export function checkEvolutionProgress() {
  const now = Date.now()
  for (const evo of evolutions) {
    if (evo.status !== 'in_progress') continue
    const current = evo.phases[evo.currentPhase]
    if (!current || current.status !== 'active') continue
    if (now - current.startedAt < current.duration) continue
    current.status = 'completed'
    const next = evo.phases[evo.currentPhase + 1]
    if (next) { next.status = 'active'; next.startedAt = now; evo.currentPhase++ }
    else { evo.status = 'completed' }
    debouncedSave(EVOLUTIONS_PATH, evolutions)
  }
}

export function getEvolutionSummary(): string {
  const active = evolutions.filter(e => e.status === 'in_progress')
  if (active.length === 0) return ''
  return active.map(e => {
    const p = e.phases[e.currentPhase]
    return `进化: ${e.goal} — 阶段 ${p?.phase ?? '?'}/${e.phases.length}: ${p?.description ?? '?'}`
  }).join('\n')
}

export const evolutionModule: SoulModule = {
  id: 'evolution',
  name: '进化引擎',
  dependencies: ['memory'],
  priority: 50,
  init() { loadRules(); loadHypotheses(); loadEvolutions() },
}
