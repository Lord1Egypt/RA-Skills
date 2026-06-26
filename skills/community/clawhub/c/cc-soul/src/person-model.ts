/**
 * person-model.ts — Person Model distillation
 *
 * Continuously distills conversation patterns into a holistic understanding
 * of who the user IS, not just what they said.
 */
import { resolve } from 'path'
import { DATA_DIR, loadJson, debouncedSave } from './persistence.ts'
import { memoryState, ensureMemoriesLoaded } from './memory.ts'
import { detectDomain } from './epistemic.ts'
import { buildMentalModelAugment, buildTopicAugment } from './distill.ts'

// ═══════════════════════════════════════════════════════════════════════════════
// LIVING PROFILE — 活画像：用户画像不是定期生成的文档，是随每条消息呼吸的有机体
// 每条重要消息 → 精准修改一个字段（不全量重写）
// 画像有版本号和时间线，能看到用户怎么变过来的
// ═══════════════════════════════════════════════════════════════════════════════

const LIVING_PROFILE_PATH = resolve(DATA_DIR, 'living_profile.json')

interface ProfileTrait {
  trait: string
  confidence: number
  evidence: number
  firstSeen: number
  lastSeen: number
  source?: 'regex' | 'crystallized'
  crystallizedAt?: number
}

interface ProfileChange {
  ts: number
  field: string
  oldValue: string
  newValue: string
  trigger: string  // 触发变化的消息
}

interface LivingProfile {
  identity: {
    name: string
    company: string
    role: string
    techStack: string[]
    location: string
    family: { name: string; relation: string; detail?: string }[]
    habits: string[]
  }
  traits: ProfileTrait[]
  timeline: ProfileChange[]
  predictions: { topic: string; basis: string; confidence: number }[]
  version: number
  lastUpdated: number
}

let livingProfile: LivingProfile = loadJson<LivingProfile>(LIVING_PROFILE_PATH, {
  identity: { name: '', company: '', role: '', techStack: [], location: '', family: [], habits: [] },
  traits: [],
  timeline: [],
  predictions: [],
  version: 0,
  lastUpdated: 0,
})

function saveLivingProfile() { debouncedSave(LIVING_PROFILE_PATH, livingProfile) }

/**
 * 每条消息后调用：检测是否有画像更新
 * 只在 importance >= 7（重要信息）时触发
 */
export function updateLivingProfile(content: string, scope: string, importance: number) {
  if (importance < 7) return  // 不够重要，不更新画像

  const p = livingProfile
  let changed = false

  // 名字检测
  const nameMatch = content.match(/(?:叫我|我叫|我是)\s*([^\s，。！？]{1,6})/)
  if (nameMatch && nameMatch[1] !== p.identity.name) {
    recordProfileChange('identity.name', p.identity.name, nameMatch[1], content)
    p.identity.name = nameMatch[1]
    changed = true
  }

  // 公司检测
  const companyMatch = content.match(/(?:在|去了?)\s*([^\s，。！？做]{2,8})(?:工作|上班|做|任职)/)
  if (companyMatch && companyMatch[1] !== p.identity.company) {
    recordProfileChange('identity.company', p.identity.company, companyMatch[1], content)
    p.identity.company = companyMatch[1]
    changed = true
  }

  // 职位检测
  const roleMatch = content.match(/做\s*(前端|后端|全栈|测试|设计|产品|运维|运营|开发|架构|数据|算法|管理)/)
  if (roleMatch && roleMatch[1] !== p.identity.role) {
    recordProfileChange('identity.role', p.identity.role, roleMatch[1], content)
    p.identity.role = roleMatch[1]
    changed = true
  }

  // 技术栈检测
  const techMatch = content.match(/(?:用|学|写|喜欢)\s*(Python|Go|Rust|Java|TypeScript|Vue|React|Docker|K8s|Swift|C\+\+)/gi)
  if (techMatch) {
    for (const t of techMatch) {
      const tech = t.replace(/^(?:用|学|写|喜欢)\s*/i, '').trim()
      if (tech && !p.identity.techStack.includes(tech)) {
        p.identity.techStack.push(tech)
        changed = true
      }
    }
  }

  // 家庭成员检测
  const familyMatch = content.match(/(?:我)?(女儿|儿子|孩子|老婆|老公|爸|妈|哥|姐|弟|妹)(?:叫\s*([^\s，。！？]{1,6}))?/)
  if (familyMatch) {
    const relation = familyMatch[1]
    const name = familyMatch[2] || ''
    const existing = p.identity.family.find(f => f.relation === relation)
    if (!existing) {
      p.identity.family.push({ relation, name, detail: content.slice(0, 40) })
      changed = true
    } else if (name && existing.name !== name) {
      existing.name = name
      changed = true
    }
  }

  // 居住地检测
  const locationMatch = content.match(/(?:住在?|在)\s*([^\s，。！？做工上]{2,6})(?:住|生活|定居)/)
  if (locationMatch && locationMatch[1] !== p.identity.location) {
    recordProfileChange('identity.location', p.identity.location, locationMatch[1], content)
    p.identity.location = locationMatch[1]
    changed = true
  }

  // 习惯检测
  const habitMatch = content.match(/(?:每天|习惯|经常|总是)\s*([^\s，。！？]{3,15})/)
  if (habitMatch) {
    const habit = habitMatch[1]
    if (!p.identity.habits.some(h => h.includes(habit.slice(0, 4)))) {
      p.identity.habits.push(habit)
      if (p.identity.habits.length > 10) p.identity.habits.shift()
      changed = true
    }
  }

  // 特征提取（从内容模式推断用户特征）
  const traitPatterns: [RegExp, string][] = [
    [/每天|坚持|一直/, '有规律性'],
    [/喜欢.*简洁|直接|不废话/, '效率导向'],
    [/学|研究|好奇|探索/, '学习型'],
    [/焦虑|压力|紧张|deadline/, '有压力'],
    [/开心|哈哈|太好了/, '乐观'],
    [/不喜欢|讨厌|受不了/, '有明确偏好'],
  ]
  for (const [pattern, trait] of traitPatterns) {
    if (pattern.test(content)) {
      const existing = p.traits.find(t => t.trait === trait)
      if (existing) {
        existing.evidence++
        existing.confidence = Math.min(0.95, existing.confidence + 0.05)
        existing.lastSeen = Date.now()
      } else {
        p.traits.push({ trait, confidence: 0.4, evidence: 1, firstSeen: Date.now(), lastSeen: Date.now() })
      }
      changed = true
    }
  }

  if (changed) {
    p.version++
    p.lastUpdated = Date.now()
    saveLivingProfile()
  }
}

function recordProfileChange(field: string, oldValue: string, newValue: string, trigger: string) {
  livingProfile.timeline.push({
    ts: Date.now(),
    field,
    oldValue: oldValue || '(空)',
    newValue,
    trigger: trigger.slice(0, 60),
  })
  // 保留最近 50 条变更
  if (livingProfile.timeline.length > 50) livingProfile.timeline = livingProfile.timeline.slice(-50)
}

/** 获取活画像的文本摘要（注入 prompt） */
export function getLivingProfileSummary(): string {
  const p = livingProfile
  if (p.version === 0) return ''

  const parts: string[] = []
  const id = p.identity
  if (id.name) parts.push(`名字: ${id.name}`)
  if (id.company && id.role) parts.push(`工作: ${id.company} ${id.role}`)
  else if (id.company) parts.push(`公司: ${id.company}`)
  if (id.techStack.length > 0) parts.push(`技术: ${id.techStack.join(', ')}`)
  if (id.family.length > 0) parts.push(`家庭: ${id.family.map(f => `${f.relation}${f.name ? '(' + f.name + ')' : ''}`).join(', ')}`)
  if (id.location) parts.push(`住: ${id.location}`)
  if (id.habits.length > 0) parts.push(`习惯: ${id.habits.slice(-3).join('; ')}`)

  // 高置信度特征（区分结晶特征和正则特征）
  const crystallizedTraits = p.traits.filter(t => t.source === 'crystallized' && t.confidence > 0.5).map(t => t.trait)
  const regexTraits = p.traits.filter(t => t.source !== 'crystallized' && t.confidence > 0.5).map(t => t.trait)
  if (crystallizedTraits.length > 0) parts.push(`性格结晶: ${crystallizedTraits.join(', ')}`)
  if (regexTraits.length > 0) parts.push(`特征: ${regexTraits.join(', ')}`)

  // 最近变化
  const recentChanges = p.timeline.slice(-2)
  if (recentChanges.length > 0) {
    parts.push(`近期变化: ${recentChanges.map(c => `${c.field}: ${c.oldValue}→${c.newValue}`).join('; ')}`)
  }

  return parts.join(' | ')
}

export function getLivingProfile(): LivingProfile { return livingProfile }
export function getLivingProfileVersion(): number { return livingProfile.version }

// ═══════════════════════════════════════════════════════════════════════════════
// 记忆结晶（cc-soul 原创）
// 从 behavior patterns + evolution rules 中提炼抽象性格特征
// 不同于蒸馏（信息压缩），结晶是模式抽象
//
// 触发条件（三重门控）：
//   behavior pattern hits ≥ 10 AND confidence > 0.6 AND 距上次结晶 > 7 天
// ═══════════════════════════════════════════════════════════════════════════════

let _lastCrystallizationTs = 0
const CRYSTALLIZATION_COOLDOWN = 7 * 86400000  // 7 days

export function crystallizeTraits(): number {
  const now = Date.now()
  if (now - _lastCrystallizationTs < CRYSTALLIZATION_COOLDOWN) return 0

  const profile = livingProfile
  let crystallized = 0

  // Source 1: behavior patterns with high confidence (hits ≥ 10, confidence > 0.6)
  try {
    const bps = require('./behavioral-phase-space.ts')
    const patterns: Array<{ condition: string; action: string; hits: number; misses: number; confidence: number }> = bps.getLearnedPatterns?.() || []

    for (const p of patterns) {
      if (p.hits < 10 || p.confidence <= 0.6) continue

      // Check if already crystallized
      const existing = profile.traits.find(t =>
        t.source === 'crystallized' && (t.trait === p.action || t.trait.includes(p.condition?.slice(0, 10) || ''))
      )
      if (existing) continue

      // Crystallize: pattern → trait
      const trait: ProfileTrait = {
        trait: p.action.slice(0, 60),
        confidence: p.confidence,
        evidence: p.hits,
        firstSeen: now,
        lastSeen: now,
        source: 'crystallized',
        crystallizedAt: now,
      }

      // Upgrade existing regex-sourced trait if similar
      const regexIdx = profile.traits.findIndex(t =>
        t.source === 'regex' && t.trait.includes(p.action?.slice(0, 10) || '')
      )
      if (regexIdx >= 0) {
        profile.traits[regexIdx] = trait  // crystallized overrides regex
      } else {
        profile.traits.push(trait)
      }

      crystallized++
      try { require('./decision-log.ts').logDecision('crystallize', trait.trait.slice(0, 30), `hits=${p.hits}, conf=${p.confidence.toFixed(2)}`) } catch {}
    }
  } catch {}

  // Source 2: evolution rules — high-verification rules are stable enough to crystallize
  try {
    const { getRules } = require('./evolution.ts')
    const rules = getRules?.() ?? []
    for (const r of rules) {
      const ruleText = typeof r === 'string' ? r : r.rule || ''
      if (!ruleText || ruleText.length < 5) continue

      // Rules with hits ≥ 10 and good hit ratio are stable enough
      const hitRatio = r.hits / Math.max(1, r.hits + (r.misses ?? 0))
      if (r.hits < 10 || hitRatio < 0.6) continue

      const existing = profile.traits.find(t => t.trait === ruleText.slice(0, 60))
      if (existing) continue

      profile.traits.push({
        trait: ruleText.slice(0, 60),
        confidence: hitRatio,
        evidence: r.hits,
        firstSeen: now,
        lastSeen: now,
        source: 'crystallized',
        crystallizedAt: now,
      })
      crystallized++
    }
  } catch {}

  // Cap traits at 20 — crystallized prioritized over regex
  if (profile.traits.length > 20) {
    profile.traits.sort((a, b) => {
      if (a.source === 'crystallized' && b.source !== 'crystallized') return -1
      if (b.source === 'crystallized' && a.source !== 'crystallized') return 1
      return (b.confidence || 0) - (a.confidence || 0)
    })
    profile.traits = profile.traits.slice(0, 20)
  }

  if (crystallized > 0) {
    _lastCrystallizationTs = now
    profile.version++
    profile.lastUpdated = now
    saveLivingProfile()
    console.log(`[cc-soul][person-model] crystallized ${crystallized} traits`)
  }

  return crystallized
}

// Lazy modules (avoid circular deps + ESM require)
let _bodyMod: any = null
let _memMod: any = null
let _cliMod: any = null
function lazyBody() { if (!_bodyMod) { import('./body.ts').then(m => { _bodyMod = m }).catch((e: any) => { console.error(`[cc-soul] module load failed (body): ${e.message}`) }) }; return _bodyMod }
function lazyMem() { if (!_memMod) { import('./memory.ts').then(m => { _memMod = m }).catch((e: any) => { console.error(`[cc-soul] module load failed (memory): ${e.message}`) }) }; return _memMod }
function lazyCli() { if (!_cliMod) { import('./cli.ts').then(m => { _cliMod = m }).catch((e: any) => { console.error(`[cc-soul] module load failed (cli): ${e.message}`) }) }; return _cliMod }
setTimeout(() => {
  import('./body.ts').then(m => { _bodyMod = m }).catch((e: any) => { console.error(`[cc-soul] module load failed (body): ${e.message}`) })
  import('./memory.ts').then(m => { _memMod = m }).catch((e: any) => { console.error(`[cc-soul] module load failed (memory): ${e.message}`) })
  import('./cli.ts').then(m => { _cliMod = m }).catch((e: any) => { console.error(`[cc-soul] module load failed (cli): ${e.message}`) })
}, 500)

const PERSON_MODEL_PATH = resolve(DATA_DIR, 'person_model.json')

export interface ReasoningProfile {
  style: 'conclusion_first' | 'buildup' | 'unknown'
  evidence: 'data' | 'analogy' | 'mixed' | 'unknown'
  certainty: 'assertive' | 'hedging' | 'mixed' | 'unknown'
  disagreement: 'dig_in' | 'compromise' | 'question' | 'unknown'
  _counts: { style: Record<string, number>; evidence: Record<string, number>; certainty: Record<string, number>; disagreement: Record<string, number>; total: number }
  // ── 推理风格演化追踪（按领域分别追踪）── 原创算法
  byDomain?: Record<string, {
    current: string       // 当前推理风格
    confidence: number    // [0, 1]
    trend: 'stabilizing' | 'shifting' | 'oscillating'
    history: Array<{ style: string; ts: number }>  // cap 20/domain
  }>
}

export interface PersonModel {
  identity: string           // who they are
  thinkingStyle: string      // how they think
  values: string[]           // what they care about (max 10)
  beliefs: string[]          // deep worldview beliefs (max 10)
  contradictions: string[]   // things they're contradictory about (max 5)
  communicationDecoder: Record<string, string>  // "算了" → "换个角度", "随便" → "你来决定"
  domainExpertise: Record<string, 'beginner' | 'intermediate' | 'expert'>
  reasoningProfile: ReasoningProfile
  updatedAt: number
  distillCount: number       // how many times distilled
}

const DEFAULT_PERSON_MODEL: PersonModel = {
  identity: '',
  thinkingStyle: '',
  values: [],
  beliefs: [],
  contradictions: [],
  communicationDecoder: {},
  domainExpertise: {},
  reasoningProfile: { style: 'unknown', evidence: 'unknown', certainty: 'unknown', disagreement: 'unknown', _counts: { style: {}, evidence: {}, certainty: {}, disagreement: {}, total: 0 } },
  updatedAt: 0,
  distillCount: 0,
}
// 字段兜底：JSON 可能是 {} 或缺少部分字段，确保每个字段都有默认值
const _rawPm = loadJson<Partial<PersonModel>>(PERSON_MODEL_PATH, DEFAULT_PERSON_MODEL)
let personModel: PersonModel = { ...DEFAULT_PERSON_MODEL, ..._rawPm }

export function getPersonModel(): PersonModel { return personModel }

/**
 * 分阶段人格蒸馏：
 * 5 条消息 → 粗粒度（基本偏好）
 * 15 条消息 → 中粒度（价值观 + 思维风格）
 * 30 条消息 → 细粒度（矛盾面 + 沟通密码 + 推理风格）
 *
 * 不再等 20 条才开始，5 条就给用户一个初步画像
 */
function getDistillPhase(messageCount: number): 'none' | 'coarse' | 'medium' | 'fine' {
  if (messageCount < 5) return 'none'
  if (messageCount < 15) return 'coarse'
  if (messageCount < 30) return 'medium'
  return 'fine'
}

/**
 * Distill person model from accumulated data.
 * Called from heartbeat (not every message — expensive).
 * Uses rule-based extraction, no LLM calls.
 */
export function distillPersonModel() {
  ensureMemoriesLoaded()
  const memories = memoryState.memories
  const phase = getDistillPhase(memories.length)
  if (phase === 'none') return // not enough data (< 5)

  // ── Values extraction: from preference + correction patterns ──
  const prefs = memories.filter(m => m.scope === 'preference' && m.scope !== 'expired')
  const corrections = memories.filter(m => m.scope === 'correction' && m.scope !== 'expired')

  // Extract values from preferences
  const newValues: string[] = []
  for (const p of prefs.slice(-20)) {
    if (p.content.length > 10 && p.content.length < 100) {
      newValues.push(p.content.slice(0, 60))
    }
  }
  if (newValues.length > 0) {
    personModel.values = [...new Set([...personModel.values, ...newValues])].slice(-10)
  }

  // ── Belief extraction: from repeated patterns in corrections ──
  // If user corrects the same type of thing 3+ times, it's a belief
  // (medium + fine phase)
  const correctionDomains = new Map<string, number>()
  if (phase === 'medium' || phase === 'fine') {
    for (const c of corrections) {
      const d = detectDomain(c.content)
      correctionDomains.set(d, (correctionDomains.get(d) || 0) + 1)
    }
    for (const [domain, count] of correctionDomains) {
      if (count >= 3 && !personModel.beliefs.some(b => b.includes(domain))) {
        personModel.beliefs.push(`在${domain}领域有强烈的观点（被纠正${count}次仍坚持）`)
        if (personModel.beliefs.length > 10) personModel.beliefs.shift()
      }
    }
  }

  // ── Contradiction archive: find conflicting preferences ──
  // (fine phase only — needs enough data to detect real contradictions)
  if (phase === 'fine') {
    const prefContents = prefs.map(p => p.content.toLowerCase())
    const negators = ['不', '没', '别', '反对', '讨厌', '不喜欢']
    for (let i = 0; i < prefContents.length; i++) {
      for (let j = i + 1; j < prefContents.length; j++) {
        // Check if two preferences contradict (one has negator of the other's keyword)
        const words1 = prefContents[i].match(/[\u4e00-\u9fff]{2,4}/g) || []
        const words2 = prefContents[j].match(/[\u4e00-\u9fff]{2,4}/g) || []
        for (const w of words1) {
          if (words2.some(w2 => negators.some(n => w2 === n + w || w2 === w + n))) {
            const contradiction = `说过"${prefs[i].content.slice(0, 30)}"但也说过"${prefs[j].content.slice(0, 30)}"`
            if (!personModel.contradictions.includes(contradiction)) {
              personModel.contradictions.push(contradiction)
              if (personModel.contradictions.length > 5) personModel.contradictions.shift()
            }
          }
        }
      }
    }
  }

  // ── Domain expertise: from chatHistory topic frequency + correction rate ──
  // (medium + fine phase)
  const history = memoryState.chatHistory
  if (phase === 'medium' || phase === 'fine') {
    const domainCounts = new Map<string, number>()
    for (const h of history.slice(-100)) {
      const d = detectDomain(h.user)
      if (d !== '闲聊' && d !== '通用') domainCounts.set(d, (domainCounts.get(d) || 0) + 1)
    }
    for (const [domain, count] of domainCounts) {
      const corrCount = correctionDomains.get(domain) || 0
      const corrRate = count > 0 ? corrCount / count : 0
      personModel.domainExpertise[domain] =
        count >= 10 && corrRate < 0.1 ? 'expert' :
        count >= 5 ? 'intermediate' : 'beginner'
    }
  }

  // ── Communication decoder: from short messages that got follow-ups ──
  // (fine phase only — needs enough conversational context)
  if (phase === 'fine') {
    for (let i = 0; i < history.length - 1; i++) {
      const msg = history[i].user
      if (msg.length <= 4 && msg.length >= 1) {
        // Short message patterns
        if (msg === '算了' || msg === '好吧') {
          personModel.communicationDecoder[msg] = personModel.communicationDecoder[msg] || '可能需要换个角度'
        }
        if (msg === '随便' || msg === '都行') {
          personModel.communicationDecoder[msg] = personModel.communicationDecoder[msg] || '希望你来做决定'
        }
      }
    }
  }

  // ── Emotional pattern extraction: via unified getMoodState() ──
  // (medium + fine phase)
  if (phase === 'medium' || phase === 'fine') {
    {
      const bm = lazyBody(); const getMoodState = bm?.getMoodState
      const moodState = getMoodState()
      if (moodState.moodRatio) {
        if (moodState.moodRatio.positive > moodState.moodRatio.negative * 2) {
          if (!personModel.values.includes('整体情绪积极')) personModel.values.push('整体情绪积极')
        } else if (moodState.moodRatio.negative > moodState.moodRatio.positive * 2) {
          if (!personModel.values.includes('近期情绪压力大')) personModel.values.push('近期情绪压力大')
        }
      }
    }

    // ── Emotion pattern tracking: which emotions does user experience most ──
    try {
      const memories = memoryState.memories.filter(m => (m as any).emotionLabel && m.scope !== 'expired')
      const emotionCounts = new Map<string, number>()
      for (const m of memories) {
        const label = (m as any).emotionLabel
        if (label && label !== 'neutral') {
          emotionCounts.set(label, (emotionCounts.get(label) || 0) + 1)
        }
      }
      if (emotionCounts.size >= 2) {
        const sorted = [...emotionCounts.entries()].sort((a, b) => b[1] - a[1])
        const topEmotions = sorted.slice(0, 3).map(([label, count]) => `${label}(${count}次)`)
        const pattern = `常见情绪: ${topEmotions.join('、')}`
        if (!personModel.values.includes(pattern) && !personModel.values.some(v => v.startsWith('常见情绪'))) {
          // Replace existing emotion pattern or add new
          const existingIdx = personModel.values.findIndex(v => v.startsWith('常见情绪'))
          if (existingIdx >= 0) personModel.values[existingIdx] = pattern
          else personModel.values.push(pattern)
        }
      }
    } catch {}
  }

  // ── Reasoning profile: evidence, certainty, disagreement (正则提取)
  //    style 维度通过正则推理（evidence/certainty/disagreement）
  // (fine phase only — needs substantial conversation data)
  if (phase === 'fine') {
    if (!personModel.reasoningProfile?._counts) {
      personModel.reasoningProfile = { style: 'unknown', evidence: 'unknown', certainty: 'unknown', disagreement: 'unknown', _counts: { style: {}, evidence: {}, certainty: {}, disagreement: {}, total: 0 } }
    }
    const rp = personModel.reasoningProfile
    const rc = rp._counts
    const msgs = history.slice(-50).map(h => h.user).filter(m => m.length > 15)

    // 检测当前领域（用于按域追踪推理风格演化）
    let currentDomain = 'general'
    try { currentDomain = require('./epistemic.ts').detectDomain(msgs[msgs.length - 1] || '') || 'general' } catch {}

    for (const m of msgs) {
      // Evidence preference
      if (/\d+%|\d+\.\d|数据|指标|metrics|stat/i.test(m)) rc.evidence.data = (rc.evidence.data || 0) + 1
      if (/就像|好比|类似|like\s|similar\sto|好像.*一样|打个比方/i.test(m)) rc.evidence.analogy = (rc.evidence.analogy || 0) + 1
      // Certainty（保留）
      if (/可能|也许|不确定|maybe|perhaps|might|大概|应该是/i.test(m)) rc.certainty.hedging = (rc.certainty.hedging || 0) + 1
      if (/肯定|一定|绝对|必须|definitely|must|always|毫无疑问|确定/i.test(m)) rc.certainty.assertive = (rc.certainty.assertive || 0) + 1
      // Disagreement（保留）
      if (/不对|你错了|我不同意|我坚持|no way|disagree|wrong/i.test(m)) rc.disagreement.dig_in = (rc.disagreement.dig_in || 0) + 1
      if (/也有道理|你说的对|折中|那就|行吧|fair point|compromise/i.test(m)) rc.disagreement.compromise = (rc.disagreement.compromise || 0) + 1
      if (/为什么|怎么说|你觉得呢|why|how come|what makes you/i.test(m)) rc.disagreement.question = (rc.disagreement.question || 0) + 1
      rc.total++
    }
    const pick = (counts: Record<string, number>) => { const e = Object.entries(counts); if (e.length === 0) return 'unknown'; e.sort((a, b) => b[1] - a[1]); return e[0][1] >= 10 ? (e.length > 1 && e[1][1] > e[0][1] * 0.6 ? 'mixed' : e[0][0]) : 'unknown' }
    if (rc.total >= 10) {
      rp.evidence = pick(rc.evidence) as any
      rp.certainty = pick(rc.certainty) as any
      rp.disagreement = pick(rc.disagreement) as any
    }

    // ── 推理风格演化追踪（按领域分别，cap 20/domain）──
    if (!rp.byDomain) rp.byDomain = {}
    if (rp.style !== 'unknown') {
      if (!rp.byDomain[currentDomain]) {
        rp.byDomain[currentDomain] = { current: rp.style, confidence: 0.5, trend: 'stabilizing', history: [] }
      }
      const domainTrack = rp.byDomain[currentDomain]
      domainTrack.history.push({ style: rp.style, ts: Date.now() })
      if (domainTrack.history.length > 20) domainTrack.history = domainTrack.history.slice(-20)
      domainTrack.current = rp.style
      domainTrack.confidence = Math.min(0.95, 0.3 + domainTrack.history.length * 0.03)

      // Trend 检测
      const lastFew = domainTrack.history.slice(-5)
      const styles = lastFew.map(h => h.style)
      const allSame = styles.every(s => s === styles[0])
      const uniqueCount = new Set(styles).size
      domainTrack.trend = allSame ? 'stabilizing' : uniqueCount >= 3 ? 'oscillating' : 'shifting'
    }
  }

  personModel.updatedAt = Date.now()
  personModel.distillCount++
  debouncedSave(PERSON_MODEL_PATH, personModel)
  console.log(`[cc-soul][person-model] distilled #${personModel.distillCount} (phase=${phase}): ${personModel.values.length} values, ${personModel.beliefs.length} beliefs, ${personModel.contradictions.length} contradictions`)

  // ── LLM deep synthesis (every 5th distill, fine phase only — expensive) ──
  // This is the REAL understanding layer: WHY, not just WHAT.
  // The regex above catches surface patterns; the LLM below synthesizes meaning.
  if (phase === 'fine' && personModel.distillCount % 5 === 0 && history.length >= 20) {
    const cm = lazyCli(); const spawnCLI = cm?.spawnCLI

    // Gather all available data for synthesis
    const dataPoints: string[] = []
    if (personModel.values.length > 0) dataPoints.push(`已知价值观：${personModel.values.join('、')}`)
    if (personModel.beliefs.length > 0) dataPoints.push(`已知信念：${personModel.beliefs.join('、')}`)
    if (personModel.contradictions.length > 0) dataPoints.push(`已知矛盾：${personModel.contradictions.join('、')}`)
    const expertDomains = Object.entries(personModel.domainExpertise)
    if (expertDomains.length > 0) dataPoints.push(`领域专长：${expertDomains.map(([d, l]) => `${d}(${l})`).join('、')}`)

    // Recent messages for behavioral context
    const recentMsgs = history.slice(-20).map(h => h.user).filter(m => m.length > 5)
    if (recentMsgs.length > 0) dataPoints.push(`最近的消息：\n${recentMsgs.slice(-10).map(m => `  "${m.slice(0, 60)}"`).join('\n')}`)

    // Deep memories
    try {
      const mm = lazyMem(); const getMemoriesByScope = mm?.getMemoriesByScope
      for (const scope of ['wisdom', 'deep_feeling', 'preference']) {
        const mems = getMemoriesByScope(scope)
        if (mems && mems.length > 0) {
          dataPoints.push(`${scope}记忆：${mems.slice(-3).map((m: any) => m.content.slice(0, 50)).join('；')}`)
        }
      }
    } catch {}

    spawnCLI(
      `你是一个人格心理学家。根据以下数据，用第一人称写一段深度自我认知（200字以内）。
不要列举数据，要做推理——分析 WHY：
- 我的核心驱动力是什么？
- 我的恐惧和不安全感是什么？
- 我的矛盾面背后的心理逻辑是什么？
- 用一段话描述"我的灵魂"

${dataPoints.join('\n')}`,
      (output: string) => {
        if (!output || output.length < 30) return
        personModel.identity = output.slice(0, 500)
        personModel.thinkingStyle = '' // will be filled by next analysis
        debouncedSave(PERSON_MODEL_PATH, personModel)
        console.log(`[cc-soul][person-model] LLM deep synthesis: ${output.slice(0, 60)}...`)
      }, 25000
    )

    // Separately analyze thinking style
    spawnCLI(
      `根据这些消息，用一句话概括这个人的思维方式（直觉型/分析型/情感驱动/结果导向等，不要列举，一句话）：
${recentMsgs.slice(-8).map(m => `"${m.slice(0, 60)}"`).join('\n')}`,
      (output: string) => {
        if (!output || output.length < 5) return
        personModel.thinkingStyle = output.slice(0, 100)
        debouncedSave(PERSON_MODEL_PATH, personModel)
        console.log(`[cc-soul][person-model] thinking style: ${output.slice(0, 60)}`)
      }, 15000
    )
  }
}

/**
 * Get person model context for augment injection.
 */
export function getPersonModelContext(): string | null {
  if (personModel.distillCount === 0) return null

  const parts: string[] = ['[人格模型]']
  if (personModel.values.length > 0) {
    parts.push(`价值观: ${personModel.values.slice(-3).join('、')}`)
  }
  if (personModel.beliefs.length > 0) {
    parts.push(`信念: ${personModel.beliefs.slice(-2).join('、')}`)
  }
  if (personModel.contradictions.length > 0) {
    parts.push(`矛盾面: ${personModel.contradictions[0]}`)
  }
  const decoderEntries = Object.entries(personModel.communicationDecoder).slice(0, 3)
  if (decoderEntries.length > 0) {
    parts.push(`沟通密码: ${decoderEntries.map(([k, v]) => `"${k}"=${v}`).join('、')}`)
  }

  // Reasoning profile
  const rp = personModel.reasoningProfile
  if (rp && rp._counts?.total >= 10) {
    const labels: string[] = []
    if (rp.style !== 'unknown') labels.push(rp.style === 'conclusion_first' ? '结论先行' : '递进推理')
    if (rp.evidence !== 'unknown') labels.push(rp.evidence === 'data' ? '偏好数据论证' : rp.evidence === 'analogy' ? '偏好类比' : '数据+类比混合')
    if (rp.certainty !== 'unknown') labels.push(rp.certainty === 'assertive' ? '表达确定' : rp.certainty === 'hedging' ? '表达谨慎' : '确定/谨慎混合')
    if (rp.disagreement !== 'unknown') labels.push(rp.disagreement === 'dig_in' ? '分歧时坚持己见' : rp.disagreement === 'compromise' ? '分歧时倾向妥协' : '分歧时追问原因')
    if (labels.length > 0) parts.push(`推理风格: ${labels.join('、')}`)
  }

  if (parts.length <= 1) return null
  return parts.join(' | ') + ' — 用这些理解来调整回复方式'
}

/**
 * Unified user understanding context.
 * Merges: person model (rule-based) + distill mental model (LLM-synthesized) + topic context.
 * handler-augments.ts should call THIS instead of three separate functions.
 */
export function getUnifiedUserContext(msg: string, userId?: string): string | null {
  const sections: string[] = []

  // Layer 3: LLM-synthesized mental model (from distill.ts)
  const mentalModel = buildMentalModelAugment(userId)
  if (mentalModel) sections.push(mentalModel.slice(0, 200))

  // Person model: rule-based personality distillation
  const pmCtx = getPersonModelContext()
  if (pmCtx) sections.push(pmCtx)

  // Layer 2: topic-relevant context for current message
  const topicCtx = buildTopicAugment(msg, userId)
  if (topicCtx) sections.push(topicCtx)

  if (sections.length === 0) return null
  return '[用户理解]\n' + sections.join('\n')
}

// ═══════════════════════════════════════════════════════════════════════════════
// THEORY OF MIND — 用户认知模型（merged from theory-of-mind.ts）
// Tracks beliefs, misconceptions, frustrations, goals via rule-based detection.
// Persisted to data/theory_of_mind.json.
// ═══════════════════════════════════════════════════════════════════════════════

const TOM_PATH = resolve(DATA_DIR, 'theory_of_mind.json')
const MAX_BELIEFS = 100
const MAX_KNOWLEDGE = 200
const MAX_FRUSTRATIONS = 20
const MAX_GOALS = 20

interface Belief {
  value: string
  confidence: number
  source: string
  ts: number
}

type KnowledgeLevel = 'knows' | 'unsure' | 'misconception'

interface KnowledgeEntry {
  topic: string
  level: KnowledgeLevel
  detail?: string
  ts: number
}

interface ToMState {
  model: {
    beliefs: Record<string, Belief>
    knowledge: Record<string, KnowledgeEntry>
    goals: string[]
    frustrations: string[]
  }
  corrections: { topic: string; correctInfo: string; ts: number }[]
  recentTopics: { topic: string; ts: number }[]
}

let tomState: ToMState = {
  model: { beliefs: {}, knowledge: {}, goals: [], frustrations: [] },
  corrections: [],
  recentTopics: [],
}

let _tomLoaded = false
function ensureToMLoaded() {
  if (_tomLoaded) return
  _tomLoaded = true
  const loaded = loadJson<ToMState>(TOM_PATH, {
    model: { beliefs: {}, knowledge: {}, goals: [], frustrations: [] },
    corrections: [],
    recentTopics: [],
  })
  tomState = loaded
  if (!tomState.model) tomState.model = { beliefs: {}, knowledge: {}, goals: [], frustrations: [] }
  if (!tomState.model.beliefs) tomState.model.beliefs = {}
  if (!tomState.model.knowledge) tomState.model.knowledge = {}
  if (!tomState.model.goals) tomState.model.goals = []
  if (!tomState.model.frustrations) tomState.model.frustrations = []
  if (!tomState.corrections) tomState.corrections = []
  if (!tomState.recentTopics) tomState.recentTopics = []
}

function persistToM() { debouncedSave(TOM_PATH, tomState) }

// ── Pattern tables ──

const BELIEF_PATTERNS: { regex: RegExp; extractor: (m: RegExpMatchArray) => { key: string; value: string } }[] = [
  { regex: /我以为(.+?)(?:[，。！？]|$)/, extractor: (m) => ({ key: m[1].trim().slice(0, 30), value: `用户以为：${m[1].trim()}` }) },
  { regex: /我觉得(.+?)(?:[，。！？]|$)/, extractor: (m) => ({ key: m[1].trim().slice(0, 30), value: `用户认为：${m[1].trim()}` }) },
  { regex: /难道不是(.+?)(?:[？?]|$)/, extractor: (m) => ({ key: m[1].trim().slice(0, 30), value: `用户质疑：难道不是${m[1].trim()}` }) },
  { regex: /I (?:thought|think|believe|assumed)\s+(.+?)(?:[.,!?]|$)/i, extractor: (m) => ({ key: m[1].trim().slice(0, 30), value: `User believes: ${m[1].trim()}` }) },
  { regex: /isn't it\s+(.+?)(?:[?]|$)/i, extractor: (m) => ({ key: m[1].trim().slice(0, 30), value: `User questions: isn't it ${m[1].trim()}` }) },
]

const FRUSTRATION_PATTERNS = [
  /为什么(总是|又|还是|一直)/, /太(慢|烦|复杂|难用)了/, /搞不(懂|定|明白)/, /受不了/,
  /why (does it|is it) (always|still|again)/i, /so (frustrat|annoy|confus)/i, /doesn't (work|make sense)/i,
]

const GOAL_PATTERNS: { regex: RegExp; extractor: (m: RegExpMatchArray) => string }[] = [
  { regex: /我想(要)?(.+?)(?:[，。！？]|$)/, extractor: (m) => m[2].trim() },
  { regex: /我需要(.+?)(?:[，。！？]|$)/, extractor: (m) => m[1].trim() },
  { regex: /帮我(.+?)(?:[，。！？]|$)/, extractor: (m) => m[1].trim() },
  { regex: /I want to\s+(.+?)(?:[.,!?]|$)/i, extractor: (m) => m[1].trim() },
  { regex: /I need\s+(.+?)(?:[.,!?]|$)/i, extractor: (m) => m[1].trim() },
]

function bayesianBeliefConfidence(existing: number | undefined, isReinforced: boolean): number {
  const prior = existing ?? 0.5
  return isReinforced ? prior + (1 - prior) * 0.2 : prior * 0.6
}

// ── Core API ──

export function updateBeliefFromMessage(msg: string, botReply: string): void {
  if (!msg) return
  ensureToMLoaded()

  // 1. Beliefs
  for (const pat of BELIEF_PATTERNS) {
    const match = msg.match(pat.regex)
    if (match) {
      const { key, value } = pat.extractor(match)
      const existing = tomState.model.beliefs[key]
      tomState.model.beliefs[key] = {
        value,
        confidence: existing ? bayesianBeliefConfidence(existing.confidence, true) : 0.5,
        source: 'user_stated',
        ts: Date.now(),
      }
    }
  }

  // 2. Frustrations
  for (const pat of FRUSTRATION_PATTERNS) {
    if (pat.test(msg)) {
      const snippet = msg.slice(0, 60)
      if (!tomState.model.frustrations.includes(snippet)) {
        tomState.model.frustrations.push(snippet)
        if (tomState.model.frustrations.length > MAX_FRUSTRATIONS) tomState.model.frustrations.shift()
      }
      break
    }
  }

  // 3. Goals
  for (const pat of GOAL_PATTERNS) {
    const match = msg.match(pat.regex)
    if (match) {
      const goal = pat.extractor(match)
      if (goal.length > 2 && !tomState.model.goals.includes(goal)) {
        tomState.model.goals.push(goal)
        if (tomState.model.goals.length > MAX_GOALS) tomState.model.goals.shift()
      }
    }
  }

  // 4. Correction detection → misconception
  const correctionPatterns = [/实际上/, /其实/, /不是.*而是/, /纠正/, /actually/i, /correction/i, /that's not quite right/i]
  for (const pat of correctionPatterns) {
    if (pat.test(botReply)) {
      const topic = msg.slice(0, 30).trim()
      tomState.corrections.push({ topic, correctInfo: botReply.slice(0, 100), ts: Date.now() })
      if (tomState.corrections.length > 50) tomState.corrections.shift()

      for (const beliefKey of Object.keys(tomState.model.beliefs)) {
        if (topic.includes(beliefKey) || beliefKey.includes(topic.slice(0, 10))) {
          tomState.model.beliefs[beliefKey].confidence =
            bayesianBeliefConfidence(tomState.model.beliefs[beliefKey].confidence, false)
        }
      }

      tomState.model.knowledge[topic] = { topic, level: 'misconception', detail: botReply.slice(0, 100), ts: Date.now() }
      break
    }
  }

  // 5. Topic tracking for knowledge gap detection
  const topicKey = msg.replace(/^(请问|你好|hey|hi|hello|帮我|我想|能不能)\s*/i, '').replace(/[？?！!。.，,]+$/, '').trim().slice(0, 20)
  if (topicKey) {
    tomState.recentTopics.push({ topic: topicKey, ts: Date.now() })
    if (tomState.recentTopics.length > 30) tomState.recentTopics.shift()
    const recent10 = tomState.recentTopics.slice(-10)
    const count = recent10.filter((t) => t.topic === topicKey).length
    if (count >= 3 && tomState.model.knowledge[topicKey]?.level !== 'misconception') {
      tomState.model.knowledge[topicKey] = { topic: topicKey, level: 'unsure', detail: `User asked about "${topicKey}" ${count} times recently`, ts: Date.now() }
    }
  }

  // Cap sizes
  const beliefKeys = Object.keys(tomState.model.beliefs)
  if (beliefKeys.length > MAX_BELIEFS) {
    const now = Date.now()
    const sorted = beliefKeys.sort((a, b) => {
      const ba = tomState.model.beliefs[a], bb = tomState.model.beliefs[b]
      return ((bb?.confidence ?? 0.5) * Math.exp(-(now - (bb?.ts || 0)) / (30 * 86400000))) -
             ((ba?.confidence ?? 0.5) * Math.exp(-(now - (ba?.ts || 0)) / (30 * 86400000)))
    })
    for (let i = MAX_BELIEFS; i < sorted.length; i++) delete tomState.model.beliefs[sorted[i]]
  }
  const knowledgeKeys = Object.keys(tomState.model.knowledge)
  if (knowledgeKeys.length > MAX_KNOWLEDGE) {
    const sorted = knowledgeKeys.sort((a, b) => (tomState.model.knowledge[a]?.ts || 0) - (tomState.model.knowledge[b]?.ts || 0))
    for (let i = 0; i < sorted.length - MAX_KNOWLEDGE; i++) delete tomState.model.knowledge[sorted[i]]
  }

  persistToM()
}

export function detectMisconception(msg: string): string | null {
  if (!msg) return null
  ensureToMLoaded()
  if (tomState.corrections.length === 0) return null
  const lower = msg.toLowerCase()
  for (const c of tomState.corrections) {
    const topicLower = c.topic.toLowerCase()
    if (topicLower.length > 3 && lower.includes(topicLower)) {
      if (/我以为|我觉得|难道不是|i think|i thought|isn't it/i.test(msg)) {
        return `用户可能仍然认为关于"${c.topic}"的错误信息。上次纠正：${c.correctInfo}`
      }
    }
  }
  return null
}

export function getToMContext(): string {
  ensureToMLoaded()
  const parts: string[] = []
  const misconceptions = Object.values(tomState.model.knowledge).filter((k) => k.level === 'misconception')
  if (misconceptions.length > 0) {
    parts.push(`[用户曾有的错误认知]\n${misconceptions.slice(-3).map((k) => `- ${k.topic}: ${k.detail || ''}`).join('\n')}`)
  }
  const gaps = Object.values(tomState.model.knowledge).filter((k) => k.level === 'unsure')
  if (gaps.length > 0) {
    parts.push(`[用户不太确定的领域]\n${gaps.slice(-3).map((k) => `- ${k.topic}`).join('\n')}`)
  }
  const beliefs = Object.values(tomState.model.beliefs).sort((a, b) => b.ts - a.ts).slice(0, 3)
  if (beliefs.length > 0) {
    parts.push(`[用户当前信念]\n${beliefs.map((b) => `- ${b.value}`).join('\n')}`)
  }
  if (tomState.model.frustrations.length > 0) {
    parts.push(`[用户感到沮丧的事]\n${tomState.model.frustrations.slice(-3).map((f) => `- ${f}`).join('\n')}`)
  }
  if (tomState.model.goals.length > 0) {
    parts.push(`[用户目标]\n${tomState.model.goals.slice(-3).map((g) => `- ${g}`).join('\n')}`)
  }
  return parts.join('\n')
}

// ═══════════════════════════════════════════════════════════════════════════════
// PAVE: Personality Attribute Variance-based Extraction
// cc-soul 原创算法 — 从系统学到的参数反推用户性格
//
// 5 数据源：CIN认知场 + mood历史方差 + correction频率 + 消息长度 + auto-tune参数
// ═══════════════════════════════════════════════════════════════════════════════

export interface PersonalityProfile {
  emotionalSensitivity: number   // 0-1
  complexityPreference: number   // 0-1
  patienceLevel: number          // 0-1
  consistencyNeed: number        // 0-1
  socialOrientation: number      // 0-1
  dataReady: boolean
}

export function inferPersonality(): PersonalityProfile | null {
  // Data threshold: at least 50 interactions
  let totalMessages = 0
  try {
    const { stats } = require('./handler-state.ts')
    totalMessages = stats.totalMessages || 0
  } catch {}
  if (totalMessages < 50) return null

  let emotionalSensitivity = 0.5
  let complexityPreference = 0.5
  let patienceLevel = 0.5
  let consistencyNeed = 0.5
  let socialOrientation = 0.5
  let dataReady = false

  // Source 1: CIN cognitive field (most direct personality signal)
  try {
    const cin = require('./cin.ts')
    const field = cin.getCurrentField?.()
    if (field && field.sampleCount >= 20) {
      dataReady = true
      complexityPreference = 0.5 + (field.strength[0] || 0) * 0.3
      socialOrientation = 0.5 + (field.strength[1] || 0) * 0.3
      patienceLevel = 0.5 - (field.strength[3] || 0) * 0.3
      emotionalSensitivity = 0.5 + (field.strength[4] || 0) * 0.3
    }
  } catch {}

  // Source 2: mood history variance → consistencyNeed
  try {
    const { getMoodHistory } = require('./body.ts')
    const history = getMoodHistory?.() || []
    if (history.length >= 20) {
      const moods = history.slice(-50).map((h: any) => h.mood || 0)
      const avg = moods.reduce((s: number, m: number) => s + m, 0) / moods.length
      const stddev = Math.sqrt(moods.reduce((s: number, m: number) => s + (m - avg) ** 2, 0) / moods.length)
      consistencyNeed = Math.max(0, Math.min(1, 1 - stddev * 3))
      dataReady = true
    }
  } catch {}

  // Source 3: correction frequency → perfectionism/tolerance
  try {
    const { stats } = require('./handler-state.ts')
    if (stats.totalMessages > 0) {
      const correctionRate = (stats.corrections || 0) / stats.totalMessages
      if (correctionRate > 0.1) complexityPreference = Math.min(1, complexityPreference + 0.2)
      if (correctionRate > 0.15) patienceLevel = Math.max(0, patienceLevel - 0.2)
    }
  } catch {}

  // Source 4: average message length → expression style
  try {
    const { getProfile } = require('./user-profiles.ts')
    const profile = getProfile?.('_default')
    if (profile?.languageDna?.avgLength) {
      const avgLen = profile.languageDna.avgLength
      if (avgLen > 80) complexityPreference = Math.min(1, complexityPreference + 0.15)
      if (avgLen < 20) patienceLevel = Math.max(0, patienceLevel - 0.15)
    }
  } catch {}

  // Source 5: auto-tune bandit parameters
  try {
    const { getParam } = require('./auto-tune.ts')
    const frustrationDecay = getParam('flow.frustration_shortening_rate')
    if (frustrationDecay && frustrationDecay !== 0.2) {
      patienceLevel = Math.max(0, Math.min(1, 1 - frustrationDecay / 0.3))
      dataReady = true
    }
  } catch {}

  const clamp = (v: number) => Math.max(0, Math.min(1, v))

  return {
    emotionalSensitivity: clamp(emotionalSensitivity),
    complexityPreference: clamp(complexityPreference),
    patienceLevel: clamp(patienceLevel),
    consistencyNeed: clamp(consistencyNeed),
    socialOrientation: clamp(socialOrientation),
    dataReady,
  }
}
