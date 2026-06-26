import type { SoulModule } from './brain.ts'

/**
 * persona-drift.ts — Persona Drift Detection via Shannon Entropy
 *
 * Maintains a sliding window of style-feature vectors for each persona's
 * recent responses. Computes Shannon entropy over discretised feature
 * distributions; a sudden entropy spike signals stylistic instability.
 *
 * Exported API:
 *   trackPersonaStyle(responseText, personaId) — call after every reply
 *   getPersonaDriftWarning()                   — returns warning or null
 *   personaDriftModule                         — SoulModule for brain.ts
 */

import { resolve } from 'path'
import { DATA_DIR, loadJson, debouncedSave } from './persistence.ts'

// ═══════════════════════════════════════════════════════════════════════════════
// TYPES
// ═══════════════════════════════════════════════════════════════════════════════

/** Five-dimensional style feature vector */
interface StyleVector {
  /** Average response length (chars) */
  length: number
  /** Fraction of sentences that are questions (0-1) */
  questionFreq: number
  /** Fraction of text inside code fences (0-1) */
  codeFreq: number
  /** Formality score (0-1): ratio of formal markers to total markers */
  formality: number
  /** Depth score (0-1): ratio of complex/compound sentences */
  depth: number
}

interface DriftEntry {
  ts: number
  personaId: string
  vector: StyleVector
}

interface DriftState {
  /** Sliding window per persona: personaId -> recent entries */
  windows: Record<string, DriftEntry[]>
  /** Last computed entropy per persona */
  lastEntropy: Record<string, number>
  /** Last warning issued (to avoid spamming) */
  lastWarningTs: number
}

// ═══════════════════════════════════════════════════════════════════════════════
// CONSTANTS
// ═══════════════════════════════════════════════════════════════════════════════

const DRIFT_PATH = resolve(DATA_DIR, 'persona_drift.json')
const WINDOW_SIZE = 20          // keep last N replies per persona
const BUCKET_COUNT = 5          // discretisation bins per dimension
const ENTROPY_THRESHOLD = 1.5   // above this → drift warning
const WARNING_COOLDOWN = 600000 // 10 min between warnings

const DIMENSION_KEYS: (keyof StyleVector)[] = [
  'length', 'questionFreq', 'codeFreq', 'formality', 'depth',
]

// ═══════════════════════════════════════════════════════════════════════════════
// STATE
// ═══════════════════════════════════════════════════════════════════════════════

let state: DriftState = {
  windows: {},
  lastEntropy: {},
  lastWarningTs: 0,
}

function load(): void {
  state = loadJson<DriftState>(DRIFT_PATH, {
    windows: {},
    lastEntropy: {},
    lastWarningTs: 0,
  })
}

function save(): void {
  debouncedSave(DRIFT_PATH, state)
}

// ═══════════════════════════════════════════════════════════════════════════════
// FEATURE EXTRACTION
// ═══════════════════════════════════════════════════════════════════════════════

/** Split text into sentences (rough heuristic) */
function sentences(text: string): string[] {
  return text.split(/[.!?。！？]+/).filter(s => s.trim().length > 0)
}

/** Extract a StyleVector from raw response text */
function extractStyle(text: string): StyleVector {
  const len = text.length
  const sents = sentences(text)
  const sentCount = Math.max(sents.length, 1)

  // Question frequency
  const questionMarks = (text.match(/[?？]/g) || []).length
  const questionFreq = Math.min(questionMarks / sentCount, 1)

  // Code frequency: chars inside ``` fences / total chars
  let codeChars = 0
  const codeBlocks = text.match(/```[\s\S]*?```/g) || []
  for (const block of codeBlocks) codeChars += block.length
  const codeFreq = len > 0 ? Math.min(codeChars / len, 1) : 0

  // Formality: presence of formal markers vs casual markers
  const formalMarkers = (text.match(/\b(therefore|furthermore|consequently|however|nevertheless|regarding|accordingly|hence|thus|moreover)\b/gi) || []).length
  const casualMarkers = (text.match(/\b(yeah|ok|cool|lol|haha|gonna|wanna|kinda|btw|nah)\b/gi) || []).length
  const totalMarkers = formalMarkers + casualMarkers
  const formality = totalMarkers > 0 ? formalMarkers / totalMarkers : 0.5

  // Depth: ratio of long sentences (>80 chars) — proxy for complexity
  const longSents = sents.filter(s => s.trim().length > 80).length
  const depth = longSents / sentCount

  return {
    length: len,
    questionFreq,
    codeFreq,
    formality,
    depth,
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// SHANNON ENTROPY
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Discretise a single dimension's values into `BUCKET_COUNT` equal-width bins
 * and return the Shannon entropy of the resulting distribution.
 */
function dimensionEntropy(values: number[]): number {
  if (values.length < 2) return 0

  const min = Math.min(...values)
  const max = Math.max(...values)
  const range = max - min

  // All identical → zero entropy
  if (range === 0) return 0

  const counts = new Array(BUCKET_COUNT).fill(0)
  for (const v of values) {
    let bucket = Math.floor(((v - min) / range) * BUCKET_COUNT)
    if (bucket >= BUCKET_COUNT) bucket = BUCKET_COUNT - 1
    counts[bucket]++
  }

  const n = values.length
  let entropy = 0
  for (const c of counts) {
    if (c === 0) continue
    const p = c / n
    entropy -= p * Math.log2(p)
  }
  return entropy
}

/**
 * Compute the average Shannon entropy across all style dimensions
 * for a persona's recent window.
 */
function computeEntropy(entries: DriftEntry[]): number {
  if (entries.length < 3) return 0

  let totalEntropy = 0
  for (const dim of DIMENSION_KEYS) {
    const values = entries.map(e => e.vector[dim])
    // Normalise length dimension to 0-1 range (divide by max)
    const normValues = dim === 'length'
      ? (() => {
          const mx = Math.max(...values, 1)
          return values.map(v => v / mx)
        })()
      : values
    totalEntropy += dimensionEntropy(normValues)
  }

  return totalEntropy / DIMENSION_KEYS.length
}

// ═══════════════════════════════════════════════════════════════════════════════
// PUBLIC API
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Record a response's style features for drift tracking.
 * Call this after every AI reply.
 */
export function trackPersonaStyle(responseText: string, personaId: string): void {
  if (!responseText || responseText.length < 10) return

  const vector = extractStyle(responseText)
  const entry: DriftEntry = { ts: Date.now(), personaId, vector }

  if (!state.windows[personaId]) state.windows[personaId] = []
  const win = state.windows[personaId]
  win.push(entry)

  // Trim to window size
  if (win.length > WINDOW_SIZE) {
    state.windows[personaId] = win.slice(-WINDOW_SIZE)
  }

  // Recompute entropy
  state.lastEntropy[personaId] = computeEntropy(state.windows[personaId])
  save()
}

/**
 * Check if the active persona is drifting.
 * Returns a human-readable warning string, or null if everything is stable.
 */
export function getPersonaDriftWarning(): string | null {
  const now = Date.now()
  if (now - state.lastWarningTs < WARNING_COOLDOWN) return null

  for (const [pid, entropy] of Object.entries(state.lastEntropy)) {
    if (entropy > ENTROPY_THRESHOLD) {
      const win = state.windows[pid]
      const sampleSize = win?.length ?? 0
      state.lastWarningTs = now
      save()
      return `[persona-drift] ⚠ persona "${pid}" entropy=${entropy.toFixed(3)} (threshold ${ENTROPY_THRESHOLD}, window=${sampleSize}) — style is unstable, consider anchoring persona traits`
    }
  }
  return null
}

// ═══════════════════════════════════════════════════════════════════════════════
// RULE-BASED DRIFT DETECTION (per-reply, no LLM)
// ═══════════════════════════════════════════════════════════════════════════════

/** Persona-specific drift rules — returns drift score 0-1 */
interface PersonaRules {
  id: string
  check: (text: string, vector: StyleVector) => number
}

const COMFORTER_EMPATHY = /(?:理解|明白|辛苦|不容易|没关系|别担心|慢慢来|陪你|心疼|加油|抱抱|放心|支持你|感同身受|understand|sorry|hear you|it's ok|hang in there)/i
const SOCRATIC_QUESTION = /[?？]/g
const MENTOR_MIN_LENGTH = 50

const PERSONA_RULES: PersonaRules[] = [
  {
    id: 'comforter',
    check: (text) => COMFORTER_EMPATHY.test(text) ? 0 : 0.7,
  },
  {
    id: 'socratic',
    check: (text) => {
      const qCount = (text.match(SOCRATIC_QUESTION) || []).length
      return qCount > 0 ? 0 : 0.8
    },
  },
  {
    id: 'mentor',
    check: (text) => text.length < MENTOR_MIN_LENGTH ? 0.6 : 0,
  },
]

/** Generic vector-based drift: compare reply vector to persona idealVector */
function vectorDriftScore(replyVector: StyleVector, idealVector: StyleVector): number {
  // Euclidean distance in 5D, normalized to [0,1]
  let sumSq = 0
  const dims: (keyof StyleVector)[] = ['length', 'questionFreq', 'codeFreq', 'formality', 'depth']
  for (const d of dims) {
    const diff = (replyVector[d] || 0) - (idealVector[d] || 0)
    sumSq += diff * diff
  }
  // max possible distance = sqrt(5) ≈ 2.236
  return Math.sqrt(sumSq) / 2.236
}

/** Track cumulative drift count */
let driftCount = 0
export function getDriftCount(): number { return driftCount }

/** Last drift reinforcement message (consumed once by augment builder) */
let _pendingReinforcement: string | null = null

/**
 * Check if a reply drifts from the current persona's expected style.
 * Returns drift score (0-1). Score > 0.5 triggers a reinforcement augment.
 * Call this in handleSent after getting the reply text.
 */
export function checkPersonaDrift(replyText: string, personaId: string, personaName: string, personaTone: string, idealVector?: StyleVector): number {
  if (!replyText || replyText.length < 10) return 0

  const replyVector = extractStyle(replyText)
  let score = 0

  // 1. Persona-specific rule check
  const rule = PERSONA_RULES.find(r => r.id === personaId)
  if (rule) {
    score = Math.max(score, rule.check(replyText, replyVector))
  }

  // 2. Generic vector distance (if idealVector provided)
  if (idealVector) {
    const vScore = vectorDriftScore(replyVector, idealVector)
    score = Math.max(score, vScore)
  }

  // 3. If drift detected, prepare reinforcement for next augment injection
  if (score > 0.5) {
    driftCount++
    _pendingReinforcement = `[人格增强] 你当前角色是「${personaName}」，请保持「${personaTone}」风格。drift_score=${score.toFixed(2)}`
    console.log(`[persona-drift] rule-based drift detected: persona=${personaId} score=${score.toFixed(2)} driftCount=${driftCount}`)
  }

  return score
}

/**
 * Get and consume pending reinforcement message.
 * Returns the message once, then clears it.
 */
export function getPersonaDriftReinforcement(): string | null {
  const msg = _pendingReinforcement
  _pendingReinforcement = null
  return msg
}

// ═══════════════════════════════════════════════════════════════════════════════
// SOUL MODULE
// ═══════════════════════════════════════════════════════════════════════════════

export const personaDriftModule: SoulModule = {
  id: 'persona-drift',
  name: '人格漂移检测',
  priority: 30,

  init(): void {
    load()
    console.log(`[persona-drift] loaded — tracking ${Object.keys(state.windows).length} persona(s)`)
  },

  dispose(): void {
    // Flush pending saves
    debouncedSave(DRIFT_PATH, state, 0)
  },

  /** Inject drift warning into bootstrap if detected */
  onBootstrap(): string | void {
    const warning = getPersonaDriftWarning()
    if (warning) return warning
  },

  /** After each reply, track style (if personaId available in event) */
  onSent(event: any): void {
    const text = event?.response ?? event?.assistantMessage ?? ''
    const pid = event?.personaId ?? event?.persona ?? 'default'
    if (text) trackPersonaStyle(text, pid)
  },
}
