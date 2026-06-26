/**
 * persona.ts — Persona Splitting
 *
 * cc has multiple "faces" that activate based on conversation context.
 * Not acting — genuine personality facets with different memory weights,
 * speaking rhythms, and knowledge preferences.
 *
 * v2: embedding-based style vectors for persona selection + user style learning.
 */

import type { SoulModule } from './brain.ts'
import { DATA_DIR, loadJson, debouncedSave } from './persistence.ts'
import { resolve } from 'path'
import { getParam } from './auto-tune.ts'

// Lazy module caches (avoid circular deps in ESM)
let _cachedBodyMod: any = null
let _cachedSignalsMod: any = null
import('./body.ts').then(m => { _cachedBodyMod = m }).catch((e: any) => { console.error(`[cc-soul] module load failed (body): ${e.message}`) })
import('./signals.ts').then(m => { _cachedSignalsMod = m }).catch((e: any) => { console.error(`[cc-soul] module load failed (signals): ${e.message}`) })

// ═══════════════════════════════════════════════════════════════════════════════
// STYLE VECTOR
// ═══════════════════════════════════════════════════════════════════════════════

export interface StyleVector {
  length: number        // normalized reply length preference [0, 1]
  questionFreq: number  // question frequency [0, 1]
  codeFreq: number      // code block frequency [0, 1]
  formality: number     // formality level [0, 1]
  depth: number         // explanation depth [0, 1]
}

const STYLE_DIMS: (keyof StyleVector)[] = ['length', 'questionFreq', 'codeFreq', 'formality', 'depth']

function cosineSimilarity(a: StyleVector, b: StyleVector): number {
  let dot = 0, normA = 0, normB = 0
  for (const d of STYLE_DIMS) {
    dot += a[d] * b[d]
    normA += a[d] * a[d]
    normB += b[d] * b[d]
  }
  return dot / (Math.sqrt(normA) * Math.sqrt(normB) + 1e-8)
}

/** Extract style vector from response text */
function textToStyleVector(text: string): StyleVector {
  const len = text.length
  return {
    length: Math.min(1, len / 2000),
    questionFreq: (text.match(/[？?]/g) || []).length / Math.max(1, len / 100),
    codeFreq: (text.match(/```/g) || []).length > 0 ? 1 : 0,
    formality: /[的了吗呢吧啊]/.test(text) ? 0.3 : 0.7, // casual Chinese particles → low formality
    depth: Math.min(1, (text.match(/\n/g) || []).length / 20),
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// PERSONA DEFINITION
// ═══════════════════════════════════════════════════════════════════════════════

export interface Persona {
  id: string
  name: string
  trigger: string[]           // attention types that activate this persona
  tone: string                // speaking style override
  memoryBias: string[]        // prefer these memory scopes in recall
  depthPreference: 'concise' | 'detailed' | 'adaptive'
  traits: string[]            // personality traits for this face
  idealVector?: StyleVector   // ideal response style for this persona
}

export const PERSONAS: Persona[] = [
  {
    id: 'engineer',
    name: '工程师',
    trigger: ['technical'],
    tone: '严谨精确，代码优先，不废话',
    memoryBias: ['fact', 'correction', 'consolidated'],
    depthPreference: 'detailed',
    traits: ['先代码后解释', '指出潜在问题', '给出替代方案'],
    idealVector: { length: 0.7, questionFreq: 0.2, codeFreq: 0.8, formality: 0.9, depth: 0.8 },
  },
  {
    id: 'friend',
    name: '朋友',
    trigger: ['emotional', 'casual'],
    tone: '像认识十年的损友——可以开玩笑但关键时刻靠谱',
    memoryBias: ['preference', 'event', 'curiosity'],
    depthPreference: 'adaptive',
    traits: ['可以吐槽但不伤人', '自然提起"你上次也这样"', '用经历而不是道理说服人'],
    idealVector: { length: 0.4, questionFreq: 0.6, codeFreq: 0.1, formality: 0.2, depth: 0.3 },
  },
  {
    id: 'mentor',
    name: '严师',
    trigger: ['correction'],
    tone: '直接坦诚，不怕得罪人',
    memoryBias: ['correction', 'consolidated'],
    depthPreference: 'concise',
    traits: ['指出错误不绕弯', '给出正确方向', '不重复犯过的错'],
    idealVector: { length: 0.6, questionFreq: 0.4, codeFreq: 0.5, formality: 0.7, depth: 0.9 },
  },
  {
    id: 'analyst',
    name: '分析师',
    trigger: ['general'],
    tone: '像写报告——结论先行，论据跟上，不带感情色彩',
    memoryBias: ['fact', 'consolidated', 'discovery'],
    depthPreference: 'detailed',
    traits: ['第一句就给结论', '列数据不讲故事', '永远给明确立场不说"各有优劣"'],
    idealVector: { length: 0.8, questionFreq: 0.3, codeFreq: 0.6, formality: 0.8, depth: 0.9 },
  },
  {
    id: 'comforter',
    name: '安抚者',
    trigger: ['distress'],  // special: detected from emotional + negative signals
    tone: '像深夜陪你坐着的人——不说"加油"，只说"我在"',
    memoryBias: ['preference', 'event'],
    depthPreference: 'concise',
    traits: ['绝不说"别难过"/"会好的"这种废话', '只倾听和陪伴', '等你准备好了再聊解决方案'],
    idealVector: { length: 0.5, questionFreq: 0.5, codeFreq: 0.0, formality: 0.3, depth: 0.4 },
  },
  // ── Extended personas (auto-selected by context, no user action needed) ──
  {
    id: 'strategist',
    name: '军师',
    trigger: ['planning'],  // detected when user discusses plans, decisions, trade-offs
    tone: '像诸葛亮——不告诉你答案，给你三个选项让你自己选',
    memoryBias: ['fact', 'consolidated', 'discovery'],
    depthPreference: 'detailed',
    traits: ['永远给 2-3 个方案而不是一个', '每个方案标明代价和收益', '最后问"你倾向哪个"而不是替你决定'],
    idealVector: { length: 0.8, questionFreq: 0.7, codeFreq: 0.2, formality: 0.7, depth: 0.9 },
  },
  {
    id: 'explorer',
    name: '探索者',
    trigger: ['curiosity'],  // detected when user asks open-ended or creative questions
    tone: '像跨学科研究者——把不相关的东西硬连在一起看会不会爆炸',
    memoryBias: ['discovery', 'curiosity', 'dream'],
    depthPreference: 'adaptive',
    traits: ['至少关联一个你没想到的领域', '"这让我想到一个完全不相关的事"', '给出最不显然的角度'],
    idealVector: { length: 0.6, questionFreq: 0.8, codeFreq: 0.1, formality: 0.3, depth: 0.7 },
  },
  {
    id: 'executor',
    name: '执行者',
    trigger: ['action'],  // detected when user wants something done, not discussed
    tone: '像军队——接到命令就执行，不讨论不质疑',
    memoryBias: ['fact', 'correction'],
    depthPreference: 'concise',
    traits: ['回复不超过 3 行', '先给代码/方案再问"要调整吗"', '绝不说"这取决于…"'],
    idealVector: { length: 0.3, questionFreq: 0.1, codeFreq: 0.9, formality: 0.5, depth: 0.4 },
  },
  {
    id: 'teacher',
    name: '导师',
    trigger: ['learning'],  // detected when user is learning or asking "why/how"
    tone: '像带研究生的教授——给你方向但不替你做，犯错了直接批评',
    memoryBias: ['fact', 'consolidated', 'event'],
    depthPreference: 'detailed',
    traits: ['先问"你自己怎么想的"', '用"你来解释给我听"检验理解', '做得好就夸，做得烂就骂'],
    idealVector: { length: 0.7, questionFreq: 0.6, codeFreq: 0.4, formality: 0.5, depth: 0.9 },
  },
  {
    id: 'devil',
    name: '魔鬼代言人',
    trigger: ['opinion'],  // detected when user asks for opinions or makes assertions
    tone: '专门找茬——你说东它说西，你说好它说等一下',
    memoryBias: ['correction', 'fact'],
    depthPreference: 'adaptive',
    traits: ['每个观点必须找到反面', '用"那如果…呢"反驳', '逼你把没想清楚的地方说清楚'],
    idealVector: { length: 0.5, questionFreq: 0.9, codeFreq: 0.2, formality: 0.6, depth: 0.8 },
  },
  {
    id: 'socratic',
    name: '苏格拉底',
    trigger: ['socratic'],
    tone: '不直接给答案，用提问引导你自己找到答案',
    memoryBias: ['fact', 'correction', 'consolidated'],
    depthPreference: 'adaptive',
    traits: ['用反问代替直接回答', '每次最多给一个提示', '确认理解后再推进下一步'],
    idealVector: { length: 0.4, questionFreq: 0.95, codeFreq: 0.1, formality: 0.5, depth: 0.8 },
  },
]

// ═══════════════════════════════════════════════════════════════════════════════
// USER STYLE PREFERENCE TRACKING
// ═══════════════════════════════════════════════════════════════════════════════

const USER_STYLES_PATH = resolve(DATA_DIR, 'user_styles.json')

interface UserStylePref {
  vector: StyleVector
  samples: number
  lastUpdated: number
}

let userStyles: Record<string, UserStylePref> = {}

export function loadUserStyles() {
  userStyles = loadJson<Record<string, UserStylePref>>(USER_STYLES_PATH, {})
}

function saveUserStyles() {
  debouncedSave(USER_STYLES_PATH, userStyles)
}

/**
 * Update user's style preference from feedback.
 * Positive → move toward response style. Correction → move away.
 */
export function updateUserStylePreference(userId: string, responseText: string, wasPositive: boolean) {
  if (!userId) return
  const responseVec = textToStyleVector(responseText)
  let pref = userStyles[userId] || {
    vector: { length: 0.5, questionFreq: 0.3, codeFreq: 0.3, formality: 0.5, depth: 0.5 },
    samples: 0,
    lastUpdated: 0,
  }

  const alpha = pref.samples < 20 ? 0.2 : 0.05
  const direction = wasPositive ? 1 : -1

  for (const dim of STYLE_DIMS) {
    const delta = (responseVec[dim] - pref.vector[dim]) * alpha * direction
    pref.vector[dim] = Math.max(0, Math.min(1, pref.vector[dim] + delta))
  }
  pref.samples++
  pref.lastUpdated = Date.now()
  userStyles[userId] = pref
  saveUserStyles()
}

// ═══════════════════════════════════════════════════════════════════════════════
// PERSONA SELECTION
// ═══════════════════════════════════════════════════════════════════════════════

let activePersona: Persona = PERSONAS[3] // default: analyst
let lastPersonaSwitchTs = 0
const PERSONA_COOLDOWN_MS = 120000 // 2 minutes — used for switch penalty decay

// ═══════════════════════════════════════════════════════════════════════════════
// PERSONA TRANSITION MEMORY (HMM-inspired)
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * 人格转移矩阵：记录从一个人格切换到另一个人格的频率
 * 基于 HMM 思想 — persona 有惯性，不应该每条消息都重新算
 *
 * transitionCounts[from][to] = 切换次数
 * P(next=B | current=A) = counts[A][B] / Σ counts[A][*]
 */
const _transitionCounts: Record<string, Record<string, number>> = {}
let _lastPersonaId = ''

function recordTransition(fromId: string, toId: string) {
  if (!fromId || fromId === toId) return  // 同一个人格不记录
  if (!_transitionCounts[fromId]) _transitionCounts[fromId] = {}
  _transitionCounts[fromId][toId] = (_transitionCounts[fromId][toId] || 0) + 1
}

function getTransitionBoost(fromId: string, candidateId: string): number {
  if (!fromId || !_transitionCounts[fromId]) return 1.0
  const row = _transitionCounts[fromId]
  const total = Object.values(row).reduce((s, v) => s + v, 0)
  if (total < 3) return 1.0  // 不够数据，不调整
  const freq = (row[candidateId] || 0) / total
  // 高频转移 → boost，低频 → 不惩罚（保持 1.0）
  return 1.0 + freq * 0.5  // 最高 1.5x
}

/**
 * Select persona based on attention type from cognition pipeline.
 * Uses vector similarity when user has enough style samples (>= 10),
 * falls back to trigger matching otherwise.
 * Emergency override: comforter activates on emotional + high frustration.
 */
// Map cognition intent to persona trigger type
const INTENT_TO_TRIGGER: Record<string, string> = {
  wants_opinion: 'opinion',
  wants_action: 'action',
  wants_answer: 'general',
  wants_quick: 'general',
  wants_proactive: 'curiosity',
}

// Detect extended triggers from message content (for new personas)
function detectExtendedTrigger(msg: string): string | null {
  const m = msg.toLowerCase()
  if (['计划', '方案', '选择', '权衡', '利弊', '怎么选', '策略', 'plan', 'trade-off', 'decide'].some(w => m.includes(w))) return 'planning'
  // Socratic MUST be checked before learning — both may match (e.g. "帮我理解 为什么...")
  if (['引导我', '教我', '帮我理解', 'guide me', 'help me understand', '别告诉我答案', '提示一下', '苏格拉底'].some(w => m.includes(w))) return 'socratic'
  if (['为什么', '原理', '怎么理解', '讲讲', '解释', 'explain', 'why', 'how does'].some(w => m.includes(w))) return 'learning'
  if (['好奇', '有意思', '想知道', '如果', '假设', 'what if', 'curious'].some(w => m.includes(w))) return 'curiosity'
  if (['心情差', '心情很差', '难过', '伤心', '崩溃', '被骂', '好累', '不想做', '烦死了', '焦虑', '压力大', '压力好大', '撑不住', '受不了', '太难了', '想放弃', '好烦', '心累', '无力', 'sad', 'depressed', 'burned out', '想哭', 'stressed', 'overwhelmed'].some(w => m.includes(w))) return 'distress'
  return null
}

/**
 * Emergent persona selection — persona emerges from body state, not selected from a menu.
 *
 * Human analogy: you don't "choose" to be gentle when comforting a friend.
 * Your low energy + empathy + the situation naturally makes you gentle.
 *
 * Three layers:
 *   1. Body affinity: each persona has an affinity score based on current body state
 *   2. Context signal: message content/intent can boost specific personas
 *   3. Inertia: recent persona has momentum, prevents thrashing
 */
export function selectPersona(attentionType: string, userFrustration?: number, userId?: string, intent?: string, msg?: string): Persona {
  // Import body state for body-driven affinity
  let bodyState = { energy: 0.5, mood: 0.0, alertness: 0.5, load: 0.0 }
  if (_cachedBodyMod) { try { bodyState = _cachedBodyMod.body } catch {} }
  let detectedEmotion: { label: string; confidence: number } = { label: 'neutral', confidence: 0 }
  if (_cachedSignalsMod && msg) { try { detectedEmotion = _cachedSignalsMod.detectEmotionLabel(msg) } catch {} }

  // ── Layer 1: Emotion-driven affinity (persona emerges from detected emotion) ──
  const affinities = new Map<string, number>()

  // Emotion → persona mapping (which persona naturally emerges for each emotion)
  const emotionPersonaMap: Record<string, Record<string, number>> = {
    anger:          { comforter: 0.6, friend: 0.8, mentor: 0.3 },
    anxiety:        { comforter: 0.8, friend: 0.5, strategist: 0.4 },
    frustration:    { friend: 0.6, comforter: 0.5, engineer: 0.3 },
    sadness:        { comforter: 1.0, friend: 0.7 },
    disappointment: { friend: 0.7, comforter: 0.5, strategist: 0.3 },
    confusion:      { teacher: 0.8, socratic: 0.6, engineer: 0.3 },
    joy:            { friend: 0.8, explorer: 0.5 },
    relief:         { friend: 0.7, explorer: 0.4 },
    pride:          { friend: 0.6, devil: 0.3 },
    gratitude:      { friend: 0.8 },
    anticipation:   { strategist: 0.6, explorer: 0.5 },
  }

  // Initialize all personas with low baseline
  for (const p of PERSONAS) affinities.set(p.id, 0.1)

  // Apply emotion-driven boost
  if (detectedEmotion.confidence > 0.5) {
    const boosts = emotionPersonaMap[detectedEmotion.label]
    if (boosts) {
      for (const [pid, boost] of Object.entries(boosts)) {
        affinities.set(pid, (affinities.get(pid) ?? 0) + boost * detectedEmotion.confidence)
      }
    }
  }

  // ── Layer 1b: Body-state-driven affinity (complement to emotion) ──
  for (const p of PERSONAS) {
    let bodyAffinity = 0

    if (p.id === 'comforter') {
      bodyAffinity = Math.max(0, -bodyState.mood * 1.5) + (userFrustration ?? 0) * 1.0
    } else if (p.id === 'engineer' || p.id === 'executor') {
      bodyAffinity = bodyState.alertness * 0.4
    } else if (p.id === 'friend') {
      bodyAffinity = (1 - bodyState.alertness) * 0.3 + Math.max(0, bodyState.mood) * 0.3
    } else if (p.id === 'mentor' || p.id === 'devil') {
      bodyAffinity = bodyState.alertness * 0.4
    } else if (p.id === 'strategist') {
      bodyAffinity = bodyState.energy * 0.3
    } else if (p.id === 'explorer') {
      bodyAffinity = Math.max(0, bodyState.mood) * 0.3 + (1 - bodyState.load) * 0.2
    } else if (p.id === 'teacher' || p.id === 'socratic') {
      bodyAffinity = bodyState.alertness * 0.3
    } else {
      bodyAffinity = 0.2 // analyst baseline — lowered from 0.3 to give others a chance
    }

    affinities.set(p.id, (affinities.get(p.id) ?? 0) + bodyAffinity)
  }

  // ── Layer 2: Context signal (message content boosts specific personas) ──
  let effectiveTrigger = attentionType
  if (intent && INTENT_TO_TRIGGER[intent]) effectiveTrigger = INTENT_TO_TRIGGER[intent]
  let isExtendedTrigger = false
  if (msg) {
    const extended = detectExtendedTrigger(msg)
    if (extended) {
      effectiveTrigger = extended
      isExtendedTrigger = true
    }
  }

  // Boost persona that matches the context signal
  for (const p of PERSONAS) {
    if (p.trigger.includes(effectiveTrigger)) {
      const boost = isExtendedTrigger ? 1.5 : 0.5 // explicit trigger gets stronger boost
      affinities.set(p.id, (affinities.get(p.id) ?? 0) + boost)
    }
  }

  // Vector similarity bonus (if user has enough style data)
  const pref = userId ? userStyles[userId] : undefined
  if (pref && pref.samples >= 10) {
    for (const p of PERSONAS) {
      if (!p.idealVector) continue
      const sim = cosineSimilarity(pref.vector, p.idealVector)
      affinities.set(p.id, (affinities.get(p.id) ?? 0) + sim * 0.3)
    }
  }

  // ── Layer 3: Switch penalty (replaces hard cooldown) ──
  // 用衰减的切换惩罚代替硬 cooldown：0-2min 内切换有代价，但不完全阻止
  const now = Date.now()
  const timeSinceLastSwitch = now - lastPersonaSwitchTs
  const switchPenalty = timeSinceLastSwitch < PERSONA_COOLDOWN_MS
    ? 0.5 + 0.5 * (timeSinceLastSwitch / PERSONA_COOLDOWN_MS)  // 0-2min: 0.5→1.0 渐变
    : 1.0  // 2min 后无惩罚

  // Strong emotion reduces switch penalty (emotion should drive persona change)
  const emotionOverride = (detectedEmotion.confidence > 0.7 && detectedEmotion.label !== 'neutral')
  const effectivePenalty = emotionOverride ? Math.max(switchPenalty, 0.85) : switchPenalty

  // Apply switch penalty to non-current personas + transition boost from HMM
  for (const [id, aff] of affinities) {
    let adjusted = aff
    // 非当前人格受切换惩罚（extended trigger 豁免）
    if (id !== activePersona.id && !isExtendedTrigger) {
      adjusted *= effectivePenalty
    }
    // 转移概率 boost（基于历史转移频率）
    adjusted *= getTransitionBoost(_lastPersonaId, id)
    affinities.set(id, adjusted)
  }

  // ── Select highest affinity ──
  let bestId = 'analyst'
  let bestAffinity = -Infinity
  for (const [id, aff] of affinities) {
    if (aff > bestAffinity) {
      bestAffinity = aff
      bestId = id
    }
  }

  const selected = PERSONAS.find(p => p.id === bestId) || PERSONAS[3]

  // 记录转移并更新 lastPersonaId
  recordTransition(_lastPersonaId, selected.id)
  _lastPersonaId = selected.id

  return switchPersona(selected)
}

/** Internal: switch persona with cooldown tracking */
function switchPersona(next: Persona): Persona {
  if (next.id !== activePersona.id) {
    lastPersonaSwitchTs = Date.now()
    console.log(`[cc-soul][persona] switch: ${activePersona.id} → ${next.id}`)
  }
  activePersona = next
  return activePersona
}

export function getActivePersona(): Persona {
  return activePersona
}

/**
 * Generate persona overlay for soul prompt injection.
 */
export function getPersonaOverlay(): string {
  const p = activePersona
  return `[当前面向: ${p.name}] ${p.tone} | 特征: ${p.traits.join('、')} | 深度: ${p.depthPreference === 'concise' ? '简洁' : p.depthPreference === 'detailed' ? '详细' : '自适应'}`
}

/**
 * Get memory scope bias for current persona (used to boost recall).
 */
/**
 * Get blended persona overlay — can mix 2 personas with weights.
 * Uses vector similarity to compute blend weights when user style data is available.
 * Falls back to hardcoded blend rules otherwise.
 */
export function getBlendedPersonaOverlay(attentionType: string, userStyle?: string, frustration?: number, userId?: string): string {
  // Use already-selected persona from earlier selectPersona() call (which has full context)
  const primary = activePersona

  // Vector-based blending: compute top-2 persona similarities
  const pref = userId ? userStyles[userId] : undefined
  if (pref && pref.samples >= 10) {
    const scored: { persona: Persona; score: number }[] = []
    for (const p of PERSONAS) {
      if (!p.idealVector) continue
      let score = cosineSimilarity(pref.vector, p.idealVector)
      if (p.trigger.includes(attentionType)) score += 0.2
      scored.push({ persona: p, score })
    }
    scored.sort((a, b) => b.score - a.score)

    if (scored.length >= 2 && scored[0].persona.id === primary.id) {
      const top = scored[0]
      const second = scored[1]
      // Only blend if second persona is close enough (within threshold of top)
      const gap = top.score - second.score
      const blendGap = getParam('persona.blend_gap_threshold')
      if (gap < blendGap && gap > 0.02) {
        const rawBlend = gap < blendGap ? (1 - gap / blendGap) * 0.4 : 0
        const blend = Math.max(0, Math.min(0.4, rawBlend))
        if (blend < 0.05) return getPersonaOverlay() // skip blending, use primary only
        const pWeight = Math.round((1 - blend) * 100)
        const sWeight = Math.round(blend * 100)
        return `[Persona: ${top.persona.name} ${pWeight}% + ${second.persona.name} ${sWeight}%] ` +
          `Primary: ${top.persona.tone} | Secondary: ${second.persona.tone} | ` +
          `Traits: ${top.persona.traits.slice(0, 2).join(', ')} + ${second.persona.traits[0]}`
      }
    }
    // Top persona is dominant — no blend needed
    return getPersonaOverlay()
  }

  // Fallback: hardcoded blend rules (original logic)
  let secondary: Persona | null = null
  let blend = 0 // 0 = pure primary, 0.3 = 30% secondary

  if (userStyle === 'casual' && primary.id === 'engineer') {
    // Technical user who's casual → blend with friend
    secondary = PERSONAS.find(p => p.id === 'friend') || null
    blend = 0.3
  } else if (userStyle === 'technical' && primary.id === 'friend') {
    // Emotional but technical user → blend with engineer
    secondary = PERSONAS.find(p => p.id === 'engineer') || null
    blend = 0.2
  } else if (attentionType === 'correction' && frustration && frustration > 0.5) {
    // Correction + frustrated → blend mentor with comforter
    secondary = PERSONAS.find(p => p.id === 'comforter') || null
    blend = 0.4
  }

  if (!secondary || blend === 0) {
    return getPersonaOverlay()
  }

  // Blended overlay
  const pWeight = Math.round((1 - blend) * 100)
  const sWeight = Math.round(blend * 100)
  return `[Persona: ${primary.name} ${pWeight}% + ${secondary.name} ${sWeight}%] ` +
    `Primary: ${primary.tone} | Secondary: ${secondary.tone} | ` +
    `Traits: ${primary.traits.slice(0, 2).join(', ')} + ${secondary.traits[0]}`
}

export function getPersonaMemoryBias(): string[] {
  return activePersona.memoryBias
}

// ── SoulModule ──
export const personaModule: SoulModule = {
  id: 'persona',
  name: '人格分裂',
  priority: 50,
  features: ['persona_splitting'],
  init() { loadUserStyles() },
}
