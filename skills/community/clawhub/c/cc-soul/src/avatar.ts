/**
 * avatar.ts — AI Avatar (Digital Twin) Engine
 *
 * Not style mimicry — soul injection. The goal is not to imitate how the user
 * talks, but to BE the user: think with their values, decide with their patterns,
 * feel with their emotional state, relate with their social history.
 *
 * Three capabilities:
 *   1. Data Collection: auto-extract expression, decisions, social graph, emotions
 *   2. Soul Injection: generate replies AS the user (not imitating — being)
 *   3. Proxy Reply: act on behalf with boundary checks
 *
 * Data sources for soul injection (all already collected by other modules):
 *   - person-model: identity, values, beliefs, contradictions, communication decoder
 *   - avatar profile: expression style, catchphrases, decisions, social graph, emotions
 *   - memory.ts: full memory recall by sender name
 *   - body.ts: current mood, energy, emotional state
 *   - graph.ts: social context, entity relationships
 */

import { existsSync, readFileSync, mkdirSync } from 'fs'
import { resolve } from 'path'
import { DATA_DIR, debouncedSave, loadJson } from './persistence.ts'
import { spawnCLI } from './cli.ts'
import { body, emotionVector, getEmotionVector } from './body.ts'
import type { Memory } from './types.ts'

// Lazy-loaded modules (to avoid circular imports at module level)
// These are loaded once on first use and cached.
let _personModel: any = null
let _memory: any = null

async function getPersonModelModule() {
  if (!_personModel) _personModel = await import('./person-model.ts')
  return _personModel
}
async function getMemoryModule() {
  if (!_memory) _memory = await import('./memory.ts')
  return _memory
}

// ═══════════════════════════════════════════════════════════════════════════════
// TYPES
// ═══════════════════════════════════════════════════════════════════════════════

interface SocialContact {
  relation: string
  context: string
  samples: string[]   // messages mentioning this person (max 15) — LLM infers tone from these
}

/** Categorized samples — messages grouped by context */
interface CategorizedSamples {
  casual: string[]      // 闲聊
  technical: string[]   // 技术讨论
  emotional: string[]   // 情绪表达
  general: string[]     // 其他
}

interface LengthDistribution {
  short: number    // <10 字占比
  medium: number   // 10-30 字占比
  long: number     // >30 字占比
}

interface AvatarProfile {
  id: string
  name: string
  identity: { who: string; [key: string]: any }
  expression: {
    style: string
    口头禅: string[]
    习惯: string
    avg_msg_length: number
    samples: CategorizedSamples  // categorized user messages (max 15 per category)
    tone_variants: Record<string, string>  // deprecated, kept for compat
  }
  lengthDistribution: LengthDistribution
  decisions: {
    pattern: string
    traces: { scenario: string; chose: string; reason: string; rejected?: string }[]
  }
  social: Record<string, SocialContact>
  emotional_patterns: {
    baseline: string
    triggers: Record<string, string[]>
    reaction_style: Record<string, string>
  }
  preferences: Record<string, string>
  boundaries: {
    can_reply: string[]
    ask_first: string[]
    never: string[]
  }
  // Dynamic vocabulary — learned by LLM, not hardcoded.
  // Used as fast-path detection for subsequent messages.
  // Empty at start, populated after first LLM analysis cycle.
  vocabulary: {
    emotions: Record<string, string[]>   // e.g. {"frustrated": ["绷不住","烦死了"], "happy": ["牛","爽"]}
    decisions: string[]                  // e.g. ["我选","还是...吧","我决定"]
    relations: string[]                  // e.g. ["媳妇","哥们","领导","老大"]
    avoidance: string[]                  // topics this person avoids
    decoder: Record<string, string>      // short msg → real meaning
  }
  updated_at: number
}

// ═══════════════════════════════════════════════════════════════════════════════
// HELPERS
// ═══════════════════════════════════════════════════════════════════════════════

const TECH_KEYWORDS = /(?:code|bug|api|sdk|git|docker|npm|yarn|pip|import|class|func|def |return |async|await|http|sql|json|xml|debug|compile|deploy|linux|server|数据库|接口|编译|部署|框架|算法|内存|线程|进程|函数|变量|服务器)/i

/** Classify a message into one of four categories */
// classifyMessageCategory → 复用 signals.ts 的 classifyQuick（消除重复分类逻辑）
function classifyMessageCategory(msg: string): 'casual' | 'technical' | 'emotional' | 'general' {
  try {
    const { classifyQuick } = require('./signals.ts')
    return classifyQuick(msg)
  } catch {
    // fallback
    if (msg.length < 15) return 'casual'
    return 'general'
  }
}

/** Get all samples from categorized structure as flat array */
function getAllSamples(samples: CategorizedSamples): string[] {
  return [...samples.casual, ...samples.technical, ...samples.emotional, ...samples.general]
}

/** Total sample count across all categories */
function totalSampleCount(samples: CategorizedSamples): number {
  return samples.casual.length + samples.technical.length + samples.emotional.length + samples.general.length
}

/**
 * Rule-based expression style analysis — no LLM, runs every 10 samples.
 * Generates a concise style description like "简短、直接、偶尔反问".
 */
function updateExpressionStyle(profile: AvatarProfile): void {
  const all = getAllSamples(profile.expression.samples)
  if (all.length < 10) return

  const traits: string[] = []

  // Average sentence length
  const avgLen = all.reduce((sum, s) => sum + s.length, 0) / all.length
  if (avgLen < 10) traits.push('简短')
  else if (avgLen > 40) traits.push('话多')

  // Question mark frequency
  const questionCount = all.filter(s => /[?？]/.test(s)).length
  const questionRatio = questionCount / all.length
  if (questionRatio > 0.3) traits.push('爱反问')

  // Exclamation mark frequency
  const exclamCount = all.filter(s => /[!！]/.test(s)).length
  const exclamRatio = exclamCount / all.length
  if (exclamRatio > 0.3) traits.push('情绪化')

  // Comma usage (low comma = direct)
  const commaCount = all.filter(s => /[,，]/.test(s)).length
  const commaRatio = commaCount / all.length
  if (commaRatio < 0.2) traits.push('直接')

  // "其实" frequency (hedging)
  const qishiCount = all.filter(s => s.includes('其实')).length
  const qishiRatio = qishiCount / all.length
  if (qishiRatio > 0.15) traits.push('委婉')

  // Emoji usage
  const emojiCount = all.filter(s => /[\u{1F600}-\u{1F64F}\u{1F300}-\u{1F5FF}\u{1F680}-\u{1F6FF}\u{1F900}-\u{1F9FF}]/u.test(s)).length
  if (emojiCount / all.length > 0.3) traits.push('爱用表情')

  // Ellipsis usage
  const ellipsisCount = all.filter(s => /[…\.]{3,}|\.{3,}/.test(s)).length
  if (ellipsisCount / all.length > 0.2) traits.push('爱用省略号')

  if (traits.length > 0) {
    profile.expression.style = traits.join('、')
  }
}

/**
 * Update length distribution statistics.
 */
function updateLengthDistribution(profile: AvatarProfile): void {
  const all = getAllSamples(profile.expression.samples)
  if (all.length === 0) return

  let short = 0, medium = 0, long = 0
  for (const s of all) {
    if (s.length < 10) short++
    else if (s.length <= 30) medium++
    else long++
  }
  const total = all.length
  profile.lengthDistribution = {
    short: Math.round(short / total * 100) / 100,
    medium: Math.round(medium / total * 100) / 100,
    long: Math.round(long / total * 100) / 100,
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// STATE
// ═══════════════════════════════════════════════════════════════════════════════

const PROFILES_DIR = resolve(DATA_DIR, 'avatar_profiles')
const profiles = new Map<string, AvatarProfile>()

function ensureDir() {
  if (!existsSync(PROFILES_DIR)) mkdirSync(PROFILES_DIR, { recursive: true })
}

// ═══════════════════════════════════════════════════════════════════════════════
// LOAD / SAVE
// ═══════════════════════════════════════════════════════════════════════════════

/** Migrate legacy string[] samples to CategorizedSamples */
function migrateSamples(profile: any): void {
  if (Array.isArray(profile.expression?.samples)) {
    const old: string[] = profile.expression.samples
    const categorized: CategorizedSamples = { casual: [], technical: [], emotional: [], general: [] }
    for (const s of old) {
      const cat = classifyMessageCategory(s)
      categorized[cat].push(s)
      if (categorized[cat].length > 15) categorized[cat].shift()
    }
    profile.expression.samples = categorized
  }
  // Ensure lengthDistribution exists
  if (!profile.lengthDistribution) {
    profile.lengthDistribution = { short: 0, medium: 0, long: 0 }
  }
}

export function loadAvatarProfile(userId: string): AvatarProfile {
  if (profiles.has(userId)) return profiles.get(userId)!

  ensureDir()
  const filePath = resolve(PROFILES_DIR, `${userId.replace(/[^a-zA-Z0-9_-]/g, '_')}.json`)

  if (existsSync(filePath)) {
    try {
      const data = JSON.parse(readFileSync(filePath, 'utf-8'))
      migrateSamples(data)
      profiles.set(userId, data)
      return data
    } catch {}
  }

  // Create empty profile
  const empty: AvatarProfile = {
    id: userId,
    name: '',
    identity: { who: '' },
    expression: {
      style: '',
      口头禅: [],
      习惯: '',
      avg_msg_length: 0,
      samples: { casual: [], technical: [], emotional: [], general: [] },
      tone_variants: {},
    },
    lengthDistribution: { short: 0, medium: 0, long: 0 },
    decisions: { pattern: '', traces: [] },
    social: {} as Record<string, SocialContact>,
    emotional_patterns: {
      baseline: '',
      triggers: {},
      reaction_style: {},
    },
    preferences: {},
    boundaries: {
      can_reply: [],
      ask_first: [],
      never: [],
    },
    vocabulary: {
      emotions: {},
      decisions: [],
      relations: [],
      avoidance: [],
      decoder: {},
    },
    updated_at: Date.now(),
  }
  profiles.set(userId, empty)
  return empty
}

function saveProfile(userId: string) {
  ensureDir()
  const profile = profiles.get(userId)
  if (!profile) return
  profile.updated_at = Date.now()
  const filePath = resolve(PROFILES_DIR, `${userId.replace(/[^a-zA-Z0-9_-]/g, '_')}.json`)
  debouncedSave(filePath, profile, 5000)
}

// ═══════════════════════════════════════════════════════════════════════════════
// DATA COLLECTION — called after every message (async, non-blocking)
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Auto-extract avatar data from user message. Called from handleSent.
 * Runs silently in background — user never notices.
 */
// Dedup: track last collected message per user to prevent double-collection
const _lastCollected = new Map<string, { msg: string; ts: number }>()

export function collectAvatarData(userMsg: string, botReply: string, userId: string) {
  if (!userMsg || userMsg.length < 3 || !userId) return
  if (userMsg.startsWith('/')) return // skip commands

  // Strip platform envelopes that may leak through
  let cleanMsg = userMsg
    .replace(/^\[Feishu[^\]]*\]\s*/i, '')
    .replace(/^\[message_id:\s*\S+\]\s*/i, '')
    .replace(/^[a-zA-Z0-9_\u4e00-\u9fff]{1,20}:\s*/, '')
    .replace(/^\n+/, '').trim()
  if (!cleanMsg || cleanMsg.length < 3) return

  // Dedup: skip if same message collected within 30s
  const last = _lastCollected.get(userId)
  if (last && last.msg === cleanMsg && Date.now() - last.ts < 30000) return
  _lastCollected.set(userId, { msg: cleanMsg, ts: Date.now() })

  const profile = loadAvatarProfile(userId)

  // ── 1. Expression samples (categorized, max 15 per category) ──
  if (cleanMsg.length >= 5 && cleanMsg.length <= 200) {
    const category = classifyMessageCategory(cleanMsg)
    const bucket = profile.expression.samples[category]
    // Dedup within bucket
    if (!bucket.includes(cleanMsg)) bucket.push(cleanMsg)
    if (bucket.length > 15) bucket.shift()

    // Update avg message length from all samples
    const all = getAllSamples(profile.expression.samples)
    const lens = all.map(s => s.length)
    profile.expression.avg_msg_length = Math.round(lens.reduce((a, b) => a + b, 0) / lens.length)

    // Update length distribution (#6)
    updateLengthDistribution(profile)

    // Every 10 total samples, update expression style by rules (#4)
    const total = totalSampleCount(profile.expression.samples)
    if (total > 0 && total % 10 === 0) {
      updateExpressionStyle(profile)
    }
  }

  // ── 2. 口头禅 detection (complete phrase extraction, sentence-boundary aware) ──
  // Strategy: split message into clauses by punctuation, extract 4-8 char phrases
  // from sentence HEAD and TAIL positions. Only ≥3 occurrences = catchphrase.
  // 2-3 char fragments are too short to be meaningful catchphrases — ignored.
  const knownNames = new Set(Object.keys(profile.social))

  // Split into clauses by common Chinese/English punctuation
  const clauses = cleanMsg.split(/[，。！？；、,\.!\?;\n]+/).filter(c => c.trim().length >= 4)

  const candidatePhrases = new Set<string>()
  for (const clause of clauses) {
    const trimmed = clause.trim()
    // Extract phrases of length 4-8 from HEAD and TAIL of each clause
    for (let len = 4; len <= 8; len++) {
      if (trimmed.length >= len) {
        candidatePhrases.add(trimmed.slice(0, len))           // head phrase
        candidatePhrases.add(trimmed.slice(trimmed.length - len))  // tail phrase
      }
    }
  }

  // Count frequency across ALL stored samples (same head/tail extraction)
  const allSamplesFlat = getAllSamples(profile.expression.samples)
  const allSamplesCount = allSamplesFlat.length
  for (const phrase of candidatePhrases) {
    if (phrase.length < 4 || phrase.length > 8) continue
    if (profile.expression.口头禅.includes(phrase)) continue
    if (knownNames.has(phrase)) continue

    // Count: how many samples have this phrase at sentence head or tail?
    let count = 0
    for (const sample of allSamplesFlat) {
      const sampleClauses = sample.split(/[，。！？；、,\.!\?;\n]+/).filter(c => c.trim().length >= 4)
      for (const sc of sampleClauses) {
        const st = sc.trim()
        if (st.startsWith(phrase) || st.endsWith(phrase)) { count++; break }
      }
    }

    if (count >= 3) {
      // Skip if it's a substring of an existing longer catchphrase
      const isSubOfExisting = profile.expression.口头禅.some(existing => existing.length > phrase.length && existing.includes(phrase))
      if (isSubOfExisting) continue
      // Skip if too universal (>60% of samples)
      const ratio = count / Math.max(allSamplesCount, 1)
      if (ratio > 0.6 && allSamplesCount >= 10) continue
      // Remove existing shorter substrings that this phrase supersedes
      profile.expression.口头禅 = profile.expression.口头禅.filter(existing => !(existing.length < phrase.length && phrase.includes(existing)))
      profile.expression.口头禅.push(phrase)
      if (profile.expression.口头禅.length > 10) profile.expression.口头禅.shift()
      console.log(`[cc-soul][avatar] new 口头禅 detected: "${phrase}"`)
    }
  }

  // ── 3. Decision trace extraction (fully dynamic) ──
  // Fast path: use learned vocabulary (if available)
  // Cold start: every message >15 chars goes to LLM for decision detection (expensive but necessary)
  // After vocabulary is learned: only matched messages go to LLM
  const decisionWords = profile.vocabulary?.decisions || []
  const hasDecisionFast = decisionWords.length > 0 && decisionWords.some(w => cleanMsg.includes(w))
  const inColdStart = decisionWords.length === 0 && cleanMsg.length > 15
  if ((hasDecisionFast || inColdStart) && profile.decisions.traces.length < 20) {
    spawnCLI(
      `从这句话中提取决策信息。如果有决策，输出 JSON: {"scenario":"场景","chose":"选了什么","reason":"为什么","rejected":"排除了什么"}。没有决策就回答 "null"。\n\n"${cleanMsg.slice(0, 200)}"`,
      (output) => {
        if (!output || output.includes('null')) return
        try {
          const trace = JSON.parse(output.match(/\{[\s\S]*\}/)?.[0] || 'null')
          if (trace && trace.scenario) {
            profile.decisions.traces.push(trace)
            if (profile.decisions.traces.length > 20) profile.decisions.traces.shift()
            saveProfile(userId)
            console.log(`[cc-soul][avatar] decision traced: ${trace.scenario} → ${trace.chose}`)
          }
        } catch {}
      }, 15000
    )
  }

  // ── 4. Social relation extraction (fully LLM-driven) ──
  // No hardcoded relation words. LLM decides what's a person mention and what the relation is.
  // Uses learned vocabulary.relations as a hint, but doesn't require it.
  {
    // Check if message mentions a known contact → add to their samples
    let mentionedKnown = false
    for (const [name, contact] of Object.entries(profile.social)) {
      const sc = contact as SocialContact
      if (cleanMsg.includes(name)) {
        mentionedKnown = true
        if (!sc.samples) sc.samples = []
        const sample = cleanMsg.slice(0, 100)
        if (!sc.samples.includes(sample)) {
          sc.samples.push(sample)
          if (sc.samples.length > 15) sc.samples.shift()
        }
      }
    }

    // If message seems to mention a person (CJK name-like pattern) and it's not a known contact
    // → ask LLM to extract the relationship
    const nameCandidate = cleanMsg.match(/[\u4e00-\u9fff]{2,4}(?:说|问|回|发|给|叫|让|找|约|跟|和|对|是我)/)
      || cleanMsg.match(/我[\u4e00-\u9fff]{2,6}[\u4e00-\u9fff]{2,3}/)  // "我同事阿昊" pattern
    if (nameCandidate && !mentionedKnown && Object.keys(profile.social).length < 30) {
      spawnCLI(
        `从这句话中提取人物关系。要求：
1. name 必须是具体的人名（如"阿昊""沈婉宁""老孟"），不能是称呼词（如"老公""爸爸""老板""VP"）
2. 如果只有称呼没有人名，回答 "null"
3. 输出 JSON: {"name":"具体人名","relation":"关系","context":"简要背景"}

"${cleanMsg.slice(0, 200)}"`,
        (output) => {
          if (!output || output.includes('null')) return
          try {
            const parsed = JSON.parse(output.match(/\{[\s\S]*\}/)?.[0] || 'null')
            if (parsed && parsed.name && parsed.relation && !profile.social[parsed.name]) {
              profile.social[parsed.name] = {
                relation: parsed.relation,
                context: (parsed.context || cleanMsg.slice(0, 60)).slice(0, 60),
                samples: [cleanMsg.slice(0, 100)],
              }
              saveProfile(userId)
              console.log(`[cc-soul][avatar] social relation (LLM): ${parsed.name} (${parsed.relation})`)
            }
          } catch {}
        }, 15000
      )
    }
  }

  // (Per-relationship sample collection is now inside section 4 above)

  // ── 5. Emotional pattern tracking (dynamic vocabulary) ──
  // Use learned vocabulary if available, otherwise skip (LLM will catch it in periodic analysis)
  const learnedEmotions = profile.vocabulary?.emotions || {}
  for (const [emotion, words] of Object.entries(learnedEmotions)) {
    if ((words as string[]).some(w => cleanMsg.includes(w))) {
      if (!profile.emotional_patterns.triggers[emotion]) {
        profile.emotional_patterns.triggers[emotion] = []
      }
      const trigger = cleanMsg.slice(0, 40)
      if (!profile.emotional_patterns.triggers[emotion].includes(trigger)) {
        profile.emotional_patterns.triggers[emotion].push(trigger)
        if (profile.emotional_patterns.triggers[emotion].length > 5) {
          profile.emotional_patterns.triggers[emotion].shift()
        }
      }
    }
  }

  // ── 6. Periodic LLM-driven expression deep analysis (every 10 samples) ──
  // Note: style is now updated by rule-based updateExpressionStyle() in section 1.
  // LLM analysis here focuses on deeper personality insights → stored in 习惯.
  {
    const allForLLM = getAllSamples(profile.expression.samples)
    if (allForLLM.length > 0 && allForLLM.length % 10 === 0) {
      const sampleList = allForLLM.slice(-15).map((s, i) => `${i + 1}. ${s}`).join('\n')
      spawnCLI(
        `深入分析这个用户的说话风格和性格特征。从以下消息中提取：
1. 说话风格（语气、用词习惯、标点特征、消息长度偏好）
2. 性格线索（内向/外向、直接/婉转、乐观/悲观、理性/感性）
3. 情绪表达方式（高兴/愤怒/低落时分别怎么表达）

用2-3句话综合概括，不要列清单：
${sampleList}`,
        (output) => {
          if (output && output.length > 10) {
            profile.expression.习惯 = output.slice(0, 300)
            saveProfile(userId)
            console.log(`[cc-soul][avatar] expression 习惯 updated: ${output.slice(0, 60)}`)
          }
        }, 15000
      )
    }
  }

  // ── 7. Dynamic vocabulary learning ──
  // LLM analyzes messages and builds a custom vocabulary for THIS person.
  // Trigger: every 10 samples (offset by 3), OR on first 10 samples if vocab is empty (cold start).
  const vocabEmpty = !profile.vocabulary?.emotions || Object.keys(profile.vocabulary.emotions).length === 0
  const allForVocab = getAllSamples(profile.expression.samples)
  const shouldLearnVocab = allForVocab.length > 0 && (
    allForVocab.length % 10 === 3 ||
    (vocabEmpty && allForVocab.length >= 8)  // cold start: learn after 8 samples
  )
  if (shouldLearnVocab) {
    const vocabBatch = allForVocab.slice(-10).map((s, i) => `${i + 1}. ${s}`).join('\n')
    spawnCLI(
      `分析这个用户的语言习惯，提取他/她个人的词汇表。输出 JSON：
{
  "emotions": {"开心":["这人用哪些词表达开心"],"烦躁":["..."],"低落":["..."],"愤怒":["..."]},
  "decisions": ["这人做决策时用的词/句式，如'我选''还是...吧'"],
  "relations": ["这人称呼别人用的词，如'媳妇''哥们''老大'"],
  "decoder": {"这人常用的短消息":"真实含义"},
  "avoidance": ["这人似乎回避的话题"]
}

只提取在消息中有证据的，没有就留空数组/对象。

消息：
${vocabBatch}`,
      (output) => {
        if (!output) return
        try {
          const vocab = JSON.parse(output.match(/\{[\s\S]*\}/)?.[0] || 'null')
          if (!vocab) return
          if (!profile.vocabulary) profile.vocabulary = { emotions: {}, decisions: [], relations: [], avoidance: [], decoder: {} }
          // Merge (don't replace — accumulate)
          if (vocab.emotions) {
            for (const [e, words] of Object.entries(vocab.emotions)) {
              if (!profile.vocabulary.emotions[e]) profile.vocabulary.emotions[e] = []
              for (const w of (words as string[])) {
                if (!profile.vocabulary.emotions[e].includes(w)) profile.vocabulary.emotions[e].push(w)
              }
              if (profile.vocabulary.emotions[e].length > 10) profile.vocabulary.emotions[e] = profile.vocabulary.emotions[e].slice(-10)
            }
          }
          if (vocab.decisions) {
            for (const d of vocab.decisions) {
              if (!profile.vocabulary.decisions.includes(d)) profile.vocabulary.decisions.push(d)
            }
            if (profile.vocabulary.decisions.length > 15) profile.vocabulary.decisions = profile.vocabulary.decisions.slice(-15)
          }
          if (vocab.relations) {
            for (const r of vocab.relations) {
              if (!profile.vocabulary.relations.includes(r)) profile.vocabulary.relations.push(r)
            }
          }
          if (vocab.decoder) {
            Object.assign(profile.vocabulary.decoder, vocab.decoder)
          }
          if (vocab.avoidance) {
            for (const a of vocab.avoidance) {
              if (!profile.vocabulary.avoidance.includes(a)) profile.vocabulary.avoidance.push(a)
            }
          }
          saveProfile(userId)
          console.log(`[cc-soul][avatar] vocabulary learned: ${JSON.stringify(vocab).slice(0, 100)}`)
        } catch {}
      }, 20000
    )
  }

  // ── 8. Deep soul extraction — LLM-driven, no hardcoded patterns ──
  // Every 10 messages, let LLM analyze the batch for deep patterns.
  // The LLM decides what's important — wisdom, regret, love, fear, anything.
  // No predefined categories. Every person is different.
  const allForDeep = getAllSamples(profile.expression.samples)
  if (allForDeep.length > 0 && allForDeep.length % 10 === 5) {
    // Offset by 5 from style analysis (which runs at %10===0) to spread load
    const recentBatch = allForDeep.slice(-10).map((s, i) => `${i + 1}. ${s}`).join('\n')
    spawnCLI(
      `你是一个人格分析师。分析以下消息，提取这个人内心深处的东西——不是表面的聊天内容，而是能反映他灵魂的东西。

可能包括但不限于：
- 人生信条或价值观（他反复强调的道理）
- 后悔或遗憾（他希望重来的事）
- 没说出口的话（对某人的隐藏情感）
- 对某人的深层感受（爱、愧疚、骄傲、担心）
- 他传递给别人的教诲
- 他的恐惧或焦虑
- 他的矛盾面（说一套做一套）
- 他的幽默方式（冷笑话、自嘲、损人、讽刺、谐音梗、比喻梗）
- 他回避的话题（一提到就转移话题或沉默的事）
- 他的情绪表达习惯（生气时安静还是爆发、伤心时自嘲还是沉默）

如果这批消息中有任何深层内容，输出 JSON 数组：
[{"type":"自定义类型","content":"提取的内容","about":"涉及的人(没有就空)"}]

如果这批消息只是日常闲聊没有深层内容，回答 "null"。

消息：
${recentBatch}`,
      async (output) => {
        if (!output || output.includes('null')) return
        try {
          const items = JSON.parse(output.match(/\[[\s\S]*\]/)?.[0] || 'null')
          if (!Array.isArray(items)) return
          const { addMemory } = await getMemoryModule()
          for (const item of items.slice(0, 3)) {
            if (!item.content) continue
            const scope = item.about ? 'deep_feeling' : 'wisdom'
            const tag = item.type || '深层'
            addMemory(`[${tag}] ${item.content.slice(0, 120)}${item.about ? ` (关于${item.about})` : ''}`, scope, userId, 'private')
            console.log(`[cc-soul][avatar] deep-soul LLM: [${tag}] ${item.content.slice(0, 40)}`)
          }
          saveProfile(userId)
        } catch {}
      }, 20000
    )
  }

  // ── 9. Reaction learning — learn how this user reacts to different situations ──
  // When the user sends a message, check if the PREVIOUS message (botReply/incoming)
  // was a trigger situation. If so, the user's current message IS their reaction.
  if (userMsg.length >= 2 && userMsg.length <= 20) {
    // Short messages are often reactions (e.g. "烦死了" "好的" "666")
    // Check if botReply contained a trigger-like pattern
    const triggerType = detectTriggerType(botReply)
    if (triggerType) {
      learnReaction(triggerType, userMsg.slice(0, 15))
    }
  }

  saveProfile(userId)
}

// ═══════════════════════════════════════════════════════════════════════════════
// SOUL INJECTION — generate reply AS the user (not imitating — being)
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Gather all cognitive data about the user from every module.
 * This is the "soul" that gets injected into the LLM.
 */
async function gatherSoulContext(userId: string, sender: string, message: string): Promise<string> {
  const profile = loadAvatarProfile(userId)
  const sections: string[] = []

  // ── 1. WHO I AM (person-model: identity + values + beliefs) ──
  try {
    const { getPersonModel } = await getPersonModelModule()
    const pm = getPersonModel()
    if (pm.distillCount > 0) {
      const parts: string[] = []
      if (pm.identity) parts.push(`我是：${pm.identity}`)
      if (pm.thinkingStyle) parts.push(`思维方式：${pm.thinkingStyle}`)
      if (pm.values.length > 0) parts.push(`价值观：${pm.values.join('、')}`)
      if (pm.beliefs.length > 0) parts.push(`信念：${pm.beliefs.join('、')}`)
      const rp = pm.reasoningProfile
      if (rp && rp._counts?.total >= 10) {
        const t: string[] = []
        if (rp.style !== 'unknown') t.push(rp.style === 'conclusion_first' ? '我习惯先说结论再解释' : '我习惯层层递进地论证')
        if (rp.evidence !== 'unknown') t.push(rp.evidence === 'data' ? '我喜欢用数据说话' : rp.evidence === 'analogy' ? '我喜欢打比方' : '我数据和类比都用')
        if (rp.certainty !== 'unknown') t.push(rp.certainty === 'assertive' ? '我说话很笃定' : rp.certainty === 'hedging' ? '我表达偏保守谨慎' : '我有时笃定有时谨慎')
        if (rp.disagreement !== 'unknown') t.push(rp.disagreement === 'dig_in' ? '不同意时我会坚持' : rp.disagreement === 'compromise' ? '不同意时我倾向妥协' : '不同意时我会追问为什么')
        if (t.length > 0) parts.push(`论证风格：${t.join('；')}`)
      }
      if (parts.length > 0) sections.push(`[我是谁]\n${parts.join('\n')}`)
    }
  } catch {}

  // ── 2. MY CONTRADICTIONS (真人都有矛盾) ──
  try {
    const { getPersonModel } = await getPersonModelModule()
    const pm = getPersonModel()
    if (pm.contradictions.length > 0) {
      sections.push(`[我的矛盾面]\n${pm.contradictions.map((c: string) => `- ${c}`).join('\n')}`)
    }
  } catch {}

  // ── 3. MY HISTORY WITH THIS PERSON (memories recall by sender name) ──
  try {
    const { recall } = await getMemoryModule()
    const memories: Memory[] = recall(sender + ' ' + message, 8, userId)
    const relevant = memories.filter(m =>
      m.content.includes(sender) || m.scope === 'episode' || m.scope === 'preference'
    ).slice(0, 6)
    if (relevant.length > 0) {
      sections.push(`[我和${sender}的记忆]\n${relevant.map(m => `- ${m.content.slice(0, 80)}`).join('\n')}`)
    }
  } catch {}

  // ── 4. MY DECISION PATTERNS (how I decide in similar scenarios) ──
  if (profile.decisions.traces.length > 0) {
    const traces = profile.decisions.traces.slice(-5)
      .map(t => `场景"${t.scenario}"→选了"${t.chose}"${t.reason ? '因为' + t.reason : ''}${t.rejected ? '，排除了' + t.rejected : ''}`)
    sections.push(`[我的决策模式]\n${traces.join('\n')}`)
  }

  // ── 5. MY EMOTIONAL STATE — real-time, not historical ──
  const emotionParts: string[] = []

  // Historical triggers (what kind of things make me react)
  for (const [emotion, triggers] of Object.entries(profile.emotional_patterns.triggers)) {
    if ((triggers as string[]).length > 0) {
      emotionParts.push(`${emotion}时我会说：${(triggers as string[]).slice(-2).join('、')}`)
    }
  }

  // CURRENT emotional state (already altered by the "nerve" above)
  try {
    // Mood — the core emotional axis
    const m = body.mood
    const moodLabel = m > 0.5 ? '很开心' : m > 0.2 ? '心情不错' : m > -0.2 ? '平静'
      : m > -0.5 ? '有点低落' : '很难受'

    // Energy — affects patience and verbosity
    const e = body.energy
    const energyLabel = e > 0.7 ? '精力充沛，愿意多聊' : e > 0.4 ? '状态还行'
      : e > 0.2 ? '有点累，不想说太多' : '极度疲惫，只想简短回复'

    // 5-dimensional emotion vector (per-user)
    const ev2 = getEmotionVector(userId)
    const dimensions: string[] = []
    if (ev2) {
      if (ev2.pleasure < -0.3) dimensions.push('不愉快')
      if (ev2.arousal > 0.5) dimensions.push('情绪激动')
      if (ev2.dominance < -0.3) dimensions.push('感到无力')
      if (ev2.certainty < -0.3) dimensions.push('不确定/焦虑')
      if (ev2.novelty > 0.3) dimensions.push('觉得新鲜/意外')
    }

    emotionParts.push(`此刻的我：${moodLabel}，${energyLabel}${dimensions.length > 0 ? '，' + dimensions.join('、') : ''}`)
    emotionParts.push(`（这会影响我回复的语气——低落时话少、疲惫时不耐烦、开心时话多）`)
  } catch {}

  if (emotionParts.length > 0) {
    sections.push(`[我此刻的情绪状态]\n${emotionParts.join('\n')}`)
  }

  // ── 6. MY COMMUNICATION DECODER (from learned vocabulary + person-model) ──
  {
    const allDecoder: Record<string, string> = {}
    // From learned vocabulary (dynamic)
    if (profile.vocabulary?.decoder) Object.assign(allDecoder, profile.vocabulary.decoder)
    // From person-model (rule-based fallback)
    try {
      const { getPersonModel } = await getPersonModelModule()
      const pm = getPersonModel()
      if (pm.communicationDecoder) Object.assign(allDecoder, pm.communicationDecoder)
    } catch {}
    const entries = Object.entries(allDecoder).slice(0, 8)
    if (entries.length > 0) {
      sections.push(`[我的沟通密码]\n${entries.map(([k, v]) => `我说"${k}"其实意思是"${v}"`).join('\n')}`)
    }
  }

  // ── 7. MY CURRENT SITUATION (recent events, unresolved things) ──
  try {
    const { recall } = await getMemoryModule()
    const recentMems: Memory[] = recall(message, 5, userId)
    const recent = recentMems
      .filter(m => Date.now() - (m.createdAt || 0) < 7 * 24 * 3600_000)
      .slice(0, 3)
    if (recent.length > 0) {
      sections.push(`[最近发生的事]\n${recent.map(m => `- ${m.content.slice(0, 60)}`).join('\n')}`)
    }
  } catch {}
  // Time awareness
  const now = new Date()
  const hour = now.getHours()
  const timeLabel = hour < 6 ? '凌晨' : hour < 9 ? '早上' : hour < 12 ? '上午' : hour < 14 ? '中午' : hour < 18 ? '下午' : hour < 22 ? '晚上' : '深夜'
  sections.push(`[当前时间] ${timeLabel}${hour}点`)

  // ── 8. MY KNOWLEDGE BOUNDARIES (what I know and don't know) ──
  try {
    const { getPersonModel } = await getPersonModelModule()
    const pm = getPersonModel()
    if (pm.domainExpertise && Object.keys(pm.domainExpertise).length > 0) {
      const expertAreas = Object.entries(pm.domainExpertise)
        .map(([d, level]) => `${d}: ${level}`)
      sections.push(`[我懂什么不懂什么]\n${expertAreas.join('、')}\n不懂的领域就说不懂，不要装专家`)
    }
  } catch {}

  // ── 9. MY BEHAVIORAL BOUNDARIES ──
  // Note: boundaries are defaults and should eventually be learned from data.
  if (profile.boundaries.never.length > 0) {
    sections.push(`[绝对不做]\n${profile.boundaries.never.map(b => `- ${b}`).join('\n')}`)
  }

  // ── 9. MY DEEPEST SELF (wisdom, regrets, unsaid words, deep feelings) ──
  // These are the memories that make a person irreplaceable.
  try {
    const { getMemoriesByScope } = await getMemoryModule()
    const deepScopes = ['wisdom', 'regret', 'unsaid', 'deep_feeling', 'value_transmit']
    const deepMemories: string[] = []
    for (const scope of deepScopes) {
      const mems = getMemoriesByScope(scope)
      if (mems && mems.length > 0) {
        for (const m of mems.slice(-3)) {
          deepMemories.push(m.content.slice(0, 80))
        }
      }
    }
    if (deepMemories.length > 0) {
      sections.push(`[我内心最深处的东西]\n${deepMemories.map(m => `- ${m}`).join('\n')}`)
    }
  } catch {}

  // ── 10. DEEP FEELINGS ABOUT THIS SPECIFIC PERSON ──
  try {
    const { recall } = await getMemoryModule()
    const feelingMems: Memory[] = recall(sender, 5, userId)
    const deepAboutSender = feelingMems.filter(m =>
      (m.scope === 'deep_feeling' || m.scope === 'unsaid' || m.scope === 'value_transmit')
      && m.content.includes(sender)
    ).slice(0, 3)
    if (deepAboutSender.length > 0) {
      sections.push(`[我对${sender}的深层感受]\n${deepAboutSender.map(m => `- ${m.content.slice(0, 80)}`).join('\n')}`)
    }
  } catch {}

  return sections.join('\n\n')
}

/**
 * Generate a reply AS the user — soul injection, not style mimicry.
 * Returns async via callback.
 */
export function generateAvatarReply(
  userId: string,
  sender: string,
  message: string,
  callback: (reply: string, refused?: boolean) => void,
) {
  // Wrap in async IIFE since getAvatarPrompt is async
  ;(async () => {
  const profile = loadAvatarProfile(userId)

  // ── Boundary check (dynamic — learned from data, no hardcoded patterns) ──
  if (profile.boundaries.never.length > 0) {
    const isNever = profile.boundaries.never.some(b => message.includes(b))
    if (isNever) {
      callback('', true) // refused
      return
    }
  }
  if (profile.boundaries.ask_first.length > 0) {
    const isAskFirst = profile.boundaries.ask_first.some(b => message.includes(b))
    if (isAskFirst) {
      callback(`[需要本人确认] ${sender}说: "${message}"`, true)
      return
    }
  }

  // ── Emotional "nerve" — amplify based on relationship depth ──
  // NOTE: processEmotionalContagion is already called by handlePreprocessed for normal messages.
  // We do NOT call it again here to avoid double-processing.
  // Instead, we only amplify the EXISTING emotional state based on relationship depth.
  try {
    const contactForEmotion = profile.social[sender] as SocialContact | undefined
    if (contactForEmotion && contactForEmotion.samples && contactForEmotion.samples.length >= 3) {
      const depth = Math.min(contactForEmotion.samples.length / 15, 1) // 0-1
      if (body.mood < 0) body.mood *= (1 + 0.3 * depth)
      if (body.mood > 0) body.mood *= (1 + 0.2 * depth)
      body.mood = Math.max(-1, Math.min(1, body.mood))
    }
  } catch {}

  // ── Instant reaction (rule-based, zero LLM cost) ──
  const contact = profile.social[sender] as SocialContact | undefined
  const relationshipDepth = contact?.samples ? Math.min(contact.samples.length / 15, 1) : 0
  const reaction = getInstantReaction(message, body.mood, relationshipDepth)

  // ── Build soul prompt (reuses getAvatarPrompt) then append the actual message ──
  const basePrompt = await getAvatarPrompt(userId, sender, message)
  const reactionLine = reaction ? `\n我的即时反应：${reaction}——这决定了我这条回复的语气和态度。\n` : ''
  const prompt = basePrompt + `\n\n${reactionLine}${sender}发来: "${message}"\n\n以我本人的身份回复。`

  spawnCLI(prompt, (output) => {
    if (!output) { callback('生成失败'); return }
    const reply = output.trim().replace(/^["']|["']$/g, '') // strip quotes
    console.log(`[cc-soul][avatar] soul-reply: ${sender}: "${message}" → "${reply.slice(0, 80)}"`)
    callback(reply)
  }, 25000)
  })().catch((e) => {
    console.error(`[cc-soul][avatar] generateAvatarReply error: ${e.message}`)
    callback('生成失败')
  })
}

// ═══════════════════════════════════════════════════════════════════════════════
// INSTANT REACTION — rule-based, zero LLM cost
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Generate a one-liner instant reaction based on message content, mood, and relationship depth.
 * This gives the LLM an emotional anchor BEFORE it starts generating the reply.
 * No LLM call — pure pattern matching.
 */
// ── Learned reaction patterns: stored per-user, updated from actual behavior ──
interface ReactionPattern {
  trigger: string       // regex source
  reactions: { text: string; count: number }[]  // observed reactions, sorted by frequency
}

const REACTION_PATTERNS_PATH = resolve(DATA_DIR, 'reaction_patterns.json')
let _reactionPatterns: ReactionPattern[] = loadJson<ReactionPattern[]>(REACTION_PATTERNS_PATH, [])

// Default triggers — only used as detection, reactions are learned
const DEFAULT_TRIGGERS: { name: string; regex: RegExp }[] = [
  { name: 'urged', regex: /催|怎么还没|快点|赶紧|来不及|deadline/ },
  { name: 'praised', regex: /厉害|牛|不错|好棒|666|太强|辛苦了/ },
  { name: 'criticized', regex: /笨|蠢|废物|垃圾|不行|太慢|太差/ },
  { name: 'help_needed', regex: /帮我|救|怎么办|搞不定|不会/ },
  { name: 'good_news', regex: /升职|加薪|过了|成功|拿到|offer|上线/ },
  { name: 'venting', regex: /压力|累|烦|难受|失眠|焦虑|崩溃|受不了/ },
  { name: 'joking', regex: /哈哈|lol|hhh|笑死|绝了|离谱/ },
  { name: 'apologizing', regex: /对不起|抱歉|不好意思|sorry/i },
  { name: 'questioning', regex: /你确定|真的假的|别骗|不信|靠谱吗/ },
  { name: 'greeting', regex: /早|晚安|你好|在吗|hey|hi/i },
]

// Fallback reactions when no learned data exists (cold start only)
const COLD_START_REACTIONS: Record<string, string> = {
  urged: '收到，抓紧',
  praised: '谢谢',
  criticized: '...',
  help_needed: '来看看',
  good_news: '恭喜！',
  venting: '怎么了',
  joking: '哈哈',
  apologizing: '没事',
  questioning: '确定的',
  greeting: '在',
}

function getInstantReaction(msg: string, mood: number, relationship: number): string {
  // Detect which trigger matches
  for (const trigger of DEFAULT_TRIGGERS) {
    if (!trigger.regex.test(msg)) continue

    // Look for learned reaction for this trigger
    const learned = _reactionPatterns.find(p => p.trigger === trigger.name)
    if (learned && learned.reactions.length > 0) {
      // Pick most frequent reaction, with mood/relationship variation
      const sorted = [...learned.reactions].sort((a, b) => b.count - a.count)
      // Mood affects which reaction to pick: positive mood → first, negative → second (if exists)
      const idx = mood < -0.3 && sorted.length > 1 ? 1 : 0
      return sorted[idx].text
    }

    // Cold start fallback
    return COLD_START_REACTIONS[trigger.name] || ''
  }
  return ''
}

/**
 * Learn user's actual reaction to a situation.
 * Called after observing how the user responded to a message of type X.
 * Over time, replaces cold-start defaults with real personality.
 */
export function learnReaction(triggerName: string, userReaction: string) {
  if (!userReaction || userReaction.length < 1 || userReaction.length > 20) return

  let pattern = _reactionPatterns.find(p => p.trigger === triggerName)
  if (!pattern) {
    pattern = { trigger: triggerName, reactions: [] }
    _reactionPatterns.push(pattern)
  }

  // Find or add this reaction
  const existing = pattern.reactions.find(r => r.text === userReaction)
  if (existing) {
    existing.count++
  } else {
    pattern.reactions.push({ text: userReaction, count: 1 })
  }

  // Keep top 5 reactions per trigger
  pattern.reactions.sort((a, b) => b.count - a.count)
  if (pattern.reactions.length > 5) pattern.reactions = pattern.reactions.slice(0, 5)

  debouncedSave(REACTION_PATTERNS_PATH, _reactionPatterns)
}

/**
 * Auto-detect trigger type from a message (for learning from user's past messages).
 */
export function detectTriggerType(msg: string): string | null {
  for (const trigger of DEFAULT_TRIGGERS) {
    if (trigger.regex.test(msg)) return trigger.name
  }
  return null
}

// Note: Active probing (Step 1) uses inner-life.ts follow-up system — no duplication.
// Note: Deep synthesis (Step 2) now lives in person-model.ts distillPersonModel() — no duplication.

/**
 * Build the soul injection prompt WITHOUT calling LLM.
 * Returns the system prompt that tells any LLM "respond as this user would".
 *
 * Use cases:
 *   - API caller feeds this to their own LLM
 *   - MCP / A2A integration where the host controls the LLM
 *   - Debugging / inspecting what the avatar "knows"
 *
 * @param userId  - owner of the avatar profile
 * @param sender  - who is sending the message (optional, defaults to "对方")
 * @param message - the incoming message to respond to (optional, defaults to generic)
 */
export async function getAvatarPrompt(
  userId: string,
  sender?: string,
  message?: string,
): Promise<string> {
  const effectiveSender = sender || '对方'
  const effectiveMessage = message || ''
  const profile = loadAvatarProfile(userId)

  // Gather soul context from all modules
  const soulContext = await gatherSoulContext(userId, effectiveSender, effectiveMessage)

  // Relationship context + strategy (#7)
  const contact = profile.social[effectiveSender] as SocialContact | undefined
  let relationshipStrategy = ''
  if (contact) {
    const sampleCount = contact.samples?.length || 0
    if (sampleCount < 3) relationshipStrategy = '和这个人不熟，保持礼貌客气，用全称'
    else if (sampleCount <= 15) relationshipStrategy = '和这个人比较熟，自然随意'
    else relationshipStrategy = '和这个人很亲密，可以开玩笑、用昵称、说话随意'
  }
  const relationshipBlock = contact
    ? [
      `${effectiveSender}是我的${contact.relation}（${contact.context}）`,
      relationshipStrategy ? `回复策略：${relationshipStrategy}` : '',
      contact.samples && contact.samples.length > 0
        ? `我提到${effectiveSender}时的原话（注意语气差异）：\n${contact.samples.slice(-5).map(s => `  "${s}"`).join('\n')}`
        : '',
    ].filter(Boolean).join('\n')
    : effectiveSender !== '对方' ? `${effectiveSender}是我认识的人` : ''

  // Expression DNA — inject samples matching current message category (#5)
  const msgCategory = effectiveMessage ? classifyMessageCategory(effectiveMessage) : 'general'
  const categorySamples = profile.expression.samples[msgCategory] || []
  // Also include a few general samples for diversity
  const generalSamples = msgCategory !== 'general' ? (profile.expression.samples.general || []).slice(-3) : []
  const samplesForPrompt = [...categorySamples.slice(-8), ...generalSamples]

  // Length distribution string (#6)
  const ld = profile.lengthDistribution
  const ldStr = (ld && (ld.short + ld.medium + ld.long) > 0)
    ? `消息长度分布：短(${Math.round(ld.short * 100)}%) 中(${Math.round(ld.medium * 100)}%) 长(${Math.round(ld.long * 100)}%)`
    : ''

  const expressionBlock = [
    profile.expression.style ? `说话风格：${profile.expression.style}` : '',
    profile.expression.习惯 ? `性格特征：${profile.expression.习惯}` : '',
    profile.expression.口头禅.length > 0 ? `口头禅：${profile.expression.口头禅.join('、')}` : '',
    `平均消息长度：${profile.expression.avg_msg_length || 15}字`,
    ldStr,
    samplesForPrompt.length > 0
      ? `最近的${msgCategory === 'general' ? '' : `${msgCategory}类`}消息示例：\n${samplesForPrompt.map(s => `  "${s}"`).join('\n')}`
      : '',
  ].filter(Boolean).join('\n')

  // Build the soul injection system prompt
  const parts = [
    `# 你现在就是「${profile.name || '我'}」`,
    `不是模仿，不是扮演，是成为。用我的大脑思考，用我的价值观判断，用我的方式回应。`,
    '',
    soulContext,
  ]

  if (relationshipBlock) {
    parts.push('', `[我和${effectiveSender}的关系]`, relationshipBlock)
  }

  parts.push(
    '',
    `[我的表达方式]`,
    expressionBlock,
    '',
    `---`,
    `核心原则：`,
    `1. 用我的口头禅、我的语气、我的思维方式`,
    `2. 回复长度控制在${profile.expression.avg_msg_length || 15}字左右（像真人发消息一样短）`,
    `3. 如果涉及决策，参考我的决策模式`,
    `4. 如果对方有情绪，用我对这个人的方式回应（不是通用安慰）`,
    `5. 如果话题我不懂，就说不懂，真人不会什么都知道`,
    `6. 如果我当前情绪低落/疲惫，回复可以更短、更敷衍、甚至只回"嗯"——真人在状态差的时候就是这样`,
    `7. 如果有幽默的空间，用我的幽默方式——不要用通用的幽默`,
    `8. 如果这个话题我不想聊，可以转移话题或者简短带过`,
    `9. 只输出回复内容，不要任何解释、前缀或引号`,
    `10. 偶尔可以说"我好像记得..."或"有点印象但想不起来了"——真人不是什么都记得清清楚楚的`,
  )

  return parts.filter(Boolean).join('\n')
}

// ═══════════════════════════════════════════════════════════════════════════════
// PUBLIC API
// ═══════════════════════════════════════════════════════════════════════════════

export function getAvatarStats(userId: string): {
  samples: number
  catchphrases: number
  decisions: number
  contacts: number
  emotions: number
  style: string
} {
  const profile = loadAvatarProfile(userId)
  return {
    samples: totalSampleCount(profile.expression.samples),
    catchphrases: profile.expression.口头禅.length,
    decisions: profile.decisions.traces.length,
    contacts: Object.keys(profile.social).length,
    emotions: Object.keys(profile.emotional_patterns.triggers).length,
    style: profile.expression.style || '(数据不足)',
  }
}
