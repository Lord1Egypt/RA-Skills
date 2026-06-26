/**
 * user-profiles.ts — Per-user profile tracking
 *
 * Tracks stats, tier, and preferences per sender.
 * Owner detection via message count threshold.
 * Style detection via simple keyword heuristic.
 */

import type { SoulModule } from './brain.ts'
import { loadJson, debouncedSave, DATA_DIR } from './persistence.ts'
import { resolve } from 'path'
import type { UserProfile, UserRhythm } from './types.ts'

const PROFILES_PATH = resolve(DATA_DIR, 'user_profiles.json')
const profiles = new Map<string, UserProfile>()

// ── Bio extraction patterns ──
const BIO_PATTERNS = [
  /我是(?:一[名个位])?(.{2,20}(?:工程师|开发者|设计师|产品经理|架构师|分析师|研究员|学生|老师|教授|运维|测试|前端|后端|全栈|数据[^，。\s]{0,6}|科学家))/,
  /我(?:做|搞|干|从事|负责)(.{2,30}?)(?:的|工作|方面|领域|行业)/,
  /我的(?:职业|工作|专业|方向)是(.{2,30})/,
  /(?:我|本人)(?:擅长|精通|熟悉|会)(.{2,40})/,
  /i(?:'m| am) (?:a |an )?(.{2,40}(?:engineer|developer|designer|manager|analyst|student|researcher))/i,
  /my (?:job|role|profession|expertise) is (.{2,40})/i,
]

// ── Explicit "remember me" patterns ──
const REMEMBER_ME_PATTERNS = [
  /(?:记住|记下|帮我记|你要知道)[：:，,\s]*(.{4,80})/,
  /(?:remember|note)[：:，,\s]*(.{4,80})/i,
]

// ── Technical keyword set for style detection ──
const TECH_KEYWORDS = [
  'code', 'bug', 'error', 'crash', 'debug', 'hook', 'frida', 'ida',
  'api', 'sdk', 'json', 'http', 'git', 'deploy', 'docker', 'nginx',
  'python', 'typescript', 'swift', 'rust', 'sql', 'redis',
  '代码', '函数', '报错', '编译', '调试', '部署', '接口', '数据库',
  '重构', '线程', '进程', '内存', '指针', '反编译', '汇编', '逆向',
]

// ═══════════════════════════════════════════════════════════════════════════════
// LOAD / SAVE
// ═══════════════════════════════════════════════════════════════════════════════

export function loadProfiles() {
  const raw = loadJson<Record<string, any>>(PROFILES_PATH, {})
  profiles.clear()
  for (const [id, p] of Object.entries(raw)) {
    profiles.set(id, p as UserProfile)
  }
  console.log(`[cc-soul][profiles] loaded ${profiles.size} user profiles`)
}

function saveProfiles() {
  const obj: Record<string, UserProfile> = {}
  for (const [id, p] of profiles) {
    obj[id] = p
  }
  debouncedSave(PROFILES_PATH, obj)
}

// ═══════════════════════════════════════════════════════════════════════════════
// GET / CREATE
// ═══════════════════════════════════════════════════════════════════════════════

export function getProfile(userId: string): UserProfile {
  if (!userId) {
    // fallback for missing sender — return a transient 'new' profile
    return {
      userId: 'unknown',
      displayName: '',
      tier: 'new',
      messageCount: 0,
      corrections: 0,
      lastSeen: Date.now(),
      firstSeen: Date.now(),
      topics: [],
      style: 'mixed',
      trust: 0.5,
      familiarity: 0,
      relationshipTrend: 'stable',
      lastConflict: 0,
      sharedEpisodes: 0,
    }
  }
  let p = profiles.get(userId)
  if (!p) {
    p = {
      userId,
      displayName: '',
      tier: detectTier(userId, 0),
      messageCount: 0,
      corrections: 0,
      lastSeen: Date.now(),
      firstSeen: Date.now(),
      topics: [],
      style: 'mixed',
      trust: 0.5,
      familiarity: 0,
      relationshipTrend: 'stable',
      lastConflict: 0,
      sharedEpisodes: 0,
    }
    profiles.set(userId, p)
    saveProfiles()
  }
  return p
}

// ═══════════════════════════════════════════════════════════════════════════════
// UPDATE ON MESSAGE
// ═══════════════════════════════════════════════════════════════════════════════

export function updateProfileOnMessage(userId: string, msg: string) {
  if (!userId) return
  const p = getProfile(userId)
  p.messageCount++
  p.lastSeen = Date.now()

  // Language DNA: track word patterns
  if (!p.languageDna) p.languageDna = { topWords: {}, avgLength: 0, samples: 0 }
  const words = msg.match(/[\u4e00-\u9fff]{2,4}|[a-zA-Z]{3,}/gi) || []
  for (const w of words.slice(0, 10)) {
    const k = w.toLowerCase()
    p.languageDna.topWords[k] = (p.languageDna.topWords[k] || 0) + 1
  }
  p.languageDna.avgLength = (p.languageDna.avgLength * p.languageDna.samples + msg.length) / (p.languageDna.samples + 1)
  p.languageDna.samples++
  // Keep only top 50 words
  if (Object.keys(p.languageDna.topWords).length > 80) {
    const sorted = Object.entries(p.languageDna.topWords).sort((a: any, b: any) => b[1] - a[1])
    p.languageDna.topWords = Object.fromEntries(sorted.slice(0, 50))
  }

  // Update familiarity: grows with interaction count, caps at 1.0
  p.familiarity = Math.min(1.0, p.messageCount / 50) // 50 messages → fully familiar

  // Tier re-eval
  p.tier = detectTier(userId, p.messageCount)

  // Topic extraction (Chinese 3+ char words)
  const topicWords = msg.match(/[\u4e00-\u9fff]{3,}/g)
  if (topicWords) {
    for (const w of topicWords.slice(0, 3)) {
      if (!p.topics.includes(w)) {
        p.topics.push(w)
        if (p.topics.length > 50) p.topics.shift()
      }
    }
  }

  // Style detection (rolling heuristic)
  p.style = detectStyle(msg, p)

  // Language detection (first 10 messages, then stable)
  if (!p.language || p.messageCount <= 10) {
    p.language = detectLanguage(msg)
  }

  // Bio extraction: capture user self-description
  extractBio(p, msg)

  // Rhythm tracking
  updateRhythm(p, msg)

  saveProfiles()
}

// ═══════════════════════════════════════════════════════════════════════════════
// LANGUAGE DETECTION
// ═══════════════════════════════════════════════════════════════════════════════

function detectLanguage(msg: string): string {
  const cjk = (msg.match(/[\u4e00-\u9fff]/g) || []).length
  const hiragana = (msg.match(/[\u3040-\u309f]/g) || []).length
  const katakana = (msg.match(/[\u30a0-\u30ff]/g) || []).length
  const hangul = (msg.match(/[\uac00-\ud7af]/g) || []).length
  const cyrillic = (msg.match(/[\u0400-\u04ff]/g) || []).length
  const arabic = (msg.match(/[\u0600-\u06ff]/g) || []).length
  const total = msg.length || 1

  if ((hiragana + katakana) / total > 0.15) return 'ja'
  if (hangul / total > 0.15) return 'ko'
  if (cjk / total > 0.15) return 'zh'
  if (cyrillic / total > 0.15) return 'ru'
  if (arabic / total > 0.15) return 'ar'
  // Latin-based: detect by common words
  const lower = msg.toLowerCase()
  if (/\b(el|la|los|las|es|está|como|pero|por|que)\b/.test(lower)) return 'es'
  if (/\b(le|la|les|est|dans|pour|avec|mais|des)\b/.test(lower)) return 'fr'
  if (/\b(der|die|das|ist|und|ein|auf|mit|nicht)\b/.test(lower)) return 'de'
  return 'en'
}

// ═══════════════════════════════════════════════════════════════════════════════
// UPDATE ON CORRECTION
// ═══════════════════════════════════════════════════════════════════════════════

export function updateProfileOnCorrection(userId: string) {
  if (!userId) return
  const p = getProfile(userId)
  p.corrections++
  saveProfiles()
}

// ═══════════════════════════════════════════════════════════════════════════════
// TIER DETECTION
// ═══════════════════════════════════════════════════════════════════════════════

function detectTier(userId: string, messageCount: number): 'owner' | 'known' | 'new' {
  if (messageCount >= 50) return 'owner'
  if (messageCount >= 10) return 'known'
  return 'new'
}

export function getProfileTier(userId: string): 'owner' | 'known' | 'new' {
  return getProfile(userId).tier
}

// ═══════════════════════════════════════════════════════════════════════════════
// STYLE DETECTION
// ═══════════════════════════════════════════════════════════════════════════════

function detectStyle(msg: string, profile: UserProfile): 'technical' | 'casual' | 'mixed' {
  const lower = msg.toLowerCase()
  const techHits = TECH_KEYWORDS.filter(kw => lower.includes(kw)).length

  // If this message is clearly technical
  if (techHits >= 2) {
    // If was casual before, transition to mixed
    if (profile.style === 'casual') return 'mixed'
    return 'technical'
  }

  // Short messages + emoji/informal = casual
  const hasEmoji = /[\u{1F300}-\u{1FAFF}]|[😀-🙏]|[🤣🥹🫡🤔🤷💀🔥👀❤️]/u.test(msg)
  if (msg.length < 20 || hasEmoji) {
    if (profile.style === 'technical') return 'mixed'
    return 'casual'
  }

  return profile.style // keep current
}

// ═══════════════════════════════════════════════════════════════════════════════
// BIO EXTRACTION
// ═══════════════════════════════════════════════════════════════════════════════

function extractBio(profile: UserProfile, msg: string) {
  // Try explicit "remember me" patterns first
  for (const re of REMEMBER_ME_PATTERNS) {
    const m = msg.match(re)
    if (m && m[1]) {
      const newBio = m[1].trim()
      if (newBio.length >= 4 && (!profile.bio || !profile.bio.includes(newBio))) {
        profile.bio = profile.bio ? `${profile.bio}; ${newBio}` : newBio
        if (profile.bio.length > 300) profile.bio = profile.bio.slice(-300)
        console.log(`[cc-soul][profiles] bio updated (explicit): ${newBio.slice(0, 40)}`)
        return
      }
    }
  }

  // Try auto-detection patterns (only if no bio yet or bio is short)
  if (profile.bio && profile.bio.length > 50) return // already have enough
  for (const re of BIO_PATTERNS) {
    const m = msg.match(re)
    if (m && m[1]) {
      const extracted = m[1].trim()
      if (extracted.length >= 4 && (!profile.bio || !profile.bio.includes(extracted))) {
        profile.bio = profile.bio ? `${profile.bio}; ${extracted}` : extracted
        if (profile.bio.length > 300) profile.bio = profile.bio.slice(-300)
        console.log(`[cc-soul][profiles] bio updated (auto): ${extracted.slice(0, 40)}`)
        return
      }
    }
  }
}

/**
 * Manually set user bio (called from handler-commands for /remember-me style commands)
 */
export function setBio(userId: string, bio: string) {
  if (!userId || !bio) return
  const p = getProfile(userId)
  p.bio = bio.slice(0, 300)
  saveProfiles()
  console.log(`[cc-soul][profiles] bio set for ${userId}: ${bio.slice(0, 40)}`)
}

// ═══════════════════════════════════════════════════════════════════════════════
// RHYTHM TRACKING
// ═══════════════════════════════════════════════════════════════════════════════

function updateRhythm(profile: UserProfile, msg: string) {
  if (!profile.rhythm) {
    profile.rhythm = {
      activeHours: new Array(24).fill(0),
      weekdayTopics: [],
      weekendTopics: [],
      avgResponseDelay: 0,
      lastMessageTs: 0,
    }
  }

  const now = new Date()
  const hour = now.getHours()
  const isWeekend = now.getDay() === 0 || now.getDay() === 6

  // Track active hours
  profile.rhythm.activeHours[hour]++

  // Track response delay (EMA)
  if (profile.rhythm.lastMessageTs > 0) {
    const delay = (Date.now() - profile.rhythm.lastMessageTs) / 1000
    if (delay < 3600) { // only count if within an hour (not a new session)
      profile.rhythm.avgResponseDelay = profile.rhythm.avgResponseDelay * 0.9 + delay * 0.1
    }
  }
  profile.rhythm.lastMessageTs = Date.now()

  // Track topic by day type
  const topicWords = (msg.match(/[\u4e00-\u9fff]{3,}/g) || []).slice(0, 2)
  const targetTopics = isWeekend ? profile.rhythm.weekendTopics : profile.rhythm.weekdayTopics
  for (const w of topicWords) {
    if (!targetTopics.includes(w)) targetTopics.push(w)
  }
  if (targetTopics.length > 20) targetTopics.splice(0, targetTopics.length - 15)
}

// ═══════════════════════════════════════════════════════════════════════════════
// RHYTHM CONTEXT — time-aware hints for prompt augmentation
// ═══════════════════════════════════════════════════════════════════════════════

export function getRhythmContext(userId: string): string {
  const profile = getProfile(userId)
  if (!profile.rhythm || profile.messageCount < 20) return '' // not enough data

  const now = new Date()
  const hour = now.getHours()
  const isWeekend = now.getDay() === 0 || now.getDay() === 6

  const hints: string[] = []

  // Late night detection
  if (hour >= 23 || hour < 6) {
    hints.push('深夜了，简短回复，不用深入展开')
  }

  // Off-peak detection (user rarely active at this hour)
  const maxActivity = Math.max(...profile.rhythm.activeHours)
  const currentHourActivity = profile.rhythm.activeHours[hour]
  if (maxActivity > 0 && currentHourActivity < maxActivity * 0.1) {
    hints.push('用户不常在这个时段活跃，可能在忙')
  }

  // Weekend/weekday topic mode
  if (isWeekend && profile.rhythm.weekendTopics.length > 0) {
    hints.push(`周末模式: 用户常聊 ${profile.rhythm.weekendTopics.slice(-3).join('、')}`)
  } else if (!isWeekend && profile.rhythm.weekdayTopics.length > 0) {
    hints.push(`工作日模式: 用户常聊 ${profile.rhythm.weekdayTopics.slice(-3).join('、')}`)
  }

  if (hints.length === 0) return ''
  return `[节律感知] ${hints.join('; ')}`
}

// ═══════════════════════════════════════════════════════════════════════════════
// RHYTHM QUERY — for voice module peak-hour detection
// ═══════════════════════════════════════════════════════════════════════════════

export function getUserPeakHour(userId: string): number {
  const profile = getProfile(userId)
  if (!profile.rhythm) return -1
  const max = Math.max(...profile.rhythm.activeHours)
  if (max === 0) return -1  // no data yet
  return profile.rhythm.activeHours.indexOf(max)
}

// ═══════════════════════════════════════════════════════════════════════════════
// PROFILE CONTEXT — for prompt injection
// ═══════════════════════════════════════════════════════════════════════════════

export function getProfileContext(userId: string): string {
  const p = getProfile(userId)
  const parts: string[] = []

  const tierLabel = p.tier === 'owner' ? '主人' : p.tier === 'known' ? '老朋友' : '新朋友'
  parts.push(`[当前对话者] ${tierLabel}`)

  if (p.bio) {
    parts.push(`身份: ${p.bio}`)
  }

  if (p.messageCount > 0) {
    parts.push(`互动${p.messageCount}次`)
  }

  if (p.corrections > 0 && p.messageCount > 0) {
    const rate = ((p.corrections / p.messageCount) * 100).toFixed(1)
    parts.push(`纠正率${rate}%`)
  }

  parts.push(`风格偏好: ${p.style === 'technical' ? '技术型' : p.style === 'casual' ? '闲聊型' : '混合型'}`)

  if (p.topics.length > 0) {
    parts.push(`常聊: ${p.topics.slice(-5).join('、')}`)
  }

  // Tier-specific hints
  if (p.tier === 'owner') {
    parts.push('提示: 主人，技术深度优先，不需要过多解释')
  } else if (p.tier === 'new') {
    parts.push('提示: 新用户，先观察再适配，耐心一些')
  }

  return parts.join(' | ')
}

// ═══════════════════════════════════════════════════════════════════════════════
// RELATIONSHIP DYNAMICS
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Update relationship metrics based on interaction outcomes.
 */
export function updateRelationship(userId: string, event: 'correction' | 'positive' | 'session_end') {
  if (!userId) return
  const p = getProfile(userId)

  switch (event) {
    case 'correction':
      p.trust = Math.max(0, p.trust - 0.03)  // small trust hit
      p.lastConflict = Date.now()
      break
    case 'positive':
      p.trust = Math.min(1, p.trust + 0.02)
      p.familiarity = Math.min(1, p.familiarity + 0.01)
      break
    case 'session_end':
      p.sharedEpisodes++
      p.familiarity = Math.min(1, p.familiarity + 0.005)
      break
  }

  // Trend detection: simple threshold-based
  if (p.trust > 0.7) p.relationshipTrend = 'improving'
  else if (p.trust < 0.3) p.relationshipTrend = 'declining'
  else p.relationshipTrend = 'stable'

  saveProfiles()
}

/**
 * Get relationship context for augment injection.
 */
export function getRelationshipContext(userId: string): string {
  if (!userId) return ''
  const p = getProfile(userId)
  if (p.messageCount < 10) return '' // not enough data

  const hints: string[] = []

  if (p.trust < 0.3) {
    hints.push('trust is low — be cautious, hedge uncertainty, avoid bold claims')
  } else if (p.trust > 0.8) {
    hints.push('high trust — can be more direct, give bold opinions')
  }

  if (p.familiarity > 0.7) {
    hints.push('well-known user — skip background explanations')
  } else if (p.familiarity < 0.2) {
    hints.push('relatively new — provide more context')
  }

  if (p.relationshipTrend === 'declining') {
    hints.push('relationship declining — be extra careful and supportive')
  }

  if (hints.length === 0) return ''
  return `[Relationship] ${hints.join('; ')}`
}

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORTS for other modules
// ═══════════════════════════════════════════════════════════════════════════════

// ═══════════════════════════════════════════════════════════════════════════════
// GRATITUDE TRACKING — build a "strengths" profile from user thanks/praise
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * When user says thanks/praise, record WHAT they were thankful for.
 * Builds a strengths profile over time: what cc does well, per-user.
 */
export function trackGratitude(userMsg: string, lastResponse: string, senderId: string) {
  const gratitudeWords = ['谢谢', '感谢', '太好了', '牛', '厉害', '完美', 'thanks', 'perfect', '棒', '赞']
  if (!gratitudeWords.some(w => userMsg.toLowerCase().includes(w))) return

  const topic = lastResponse.split('\n')[0]?.slice(0, 60) || '(未知)'

  import('./memory.ts').then(({ addMemory }) => {
    addMemory(`[用户感谢] ${topic}`, 'gratitude', senderId, 'private')
    console.log(`[cc-soul][gratitude] tracked: ${topic.slice(0, 40)} from ${senderId || 'unknown'}`)
  }).catch((e: any) => { console.error(`[cc-soul] module load failed (memory): ${e.message}`) })
}

// ═══════════════════════════════════════════════════════════════════════════════
// PERSONA USAGE TRACKING
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Track which persona was used for a user interaction.
 * Builds a usage histogram over time for personality growth visualization.
 */
export function trackPersonaUsage(userId: string, personaId: string) {
  if (!userId || !personaId) return
  const p = getProfile(userId)
  if (!p.personaHistory) p.personaHistory = []

  const existing = p.personaHistory.find(h => h.persona === personaId)
  if (existing) {
    existing.count++
  } else {
    p.personaHistory.push({ persona: personaId, count: 1 })
  }
  saveProfiles()
}

/**
 * Get persona usage summary for dashboard display.
 * Returns top 3 personas + recent trend.
 */
export function getPersonaUsageSummary(userId: string): string {
  const p = getProfile(userId)
  if (!p.personaHistory || p.personaHistory.length === 0) return ''

  const sorted = [...p.personaHistory].sort((a, b) => b.count - a.count)
  const total = sorted.reduce((sum, h) => sum + h.count, 0)
  const top3 = sorted.slice(0, 3)

  const lines: string[] = ['🎭 人格变化轨迹']
  for (const h of top3) {
    const pct = (h.count / total * 100).toFixed(0)
    const bar = '█'.repeat(Math.ceil(h.count / total * 15))
    lines.push(`  ${h.persona.padEnd(10)} ${bar} ${pct}% (${h.count}次)`)
  }

  // Trend: compare top persona dominance
  if (sorted.length >= 2) {
    const dominance = sorted[0].count / total
    if (dominance > 0.6) {
      lines.push(`  趋势: 主要以「${sorted[0].persona}」模式互动`)
    } else {
      lines.push(`  趋势: 多面互动，风格均衡`)
    }
  }

  return lines.join('\n')
}

export { profiles }

// ── SoulModule ──
export const userProfilesModule: SoulModule = {
  id: 'user-profiles',
  name: '用户画像',
  priority: 50,
  init() { loadProfiles() },
}
