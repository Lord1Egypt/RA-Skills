/**
 * dynamic-extractor.ts — 动态提取引擎（cc-soul 原创）
 *
 * 替代所有硬编码列表。核心模式：
 *   结构词（种子+可学习）× 内容词（纯学习）× 结构强度（per-user 自适应）
 *
 * 三档分类：
 *   永久保留：语言规则（停用词、标点）— 不在本模块管
 *   种子+学习：文化常见但有个人差异（宠物词、结束信号、情绪词）
 *   纯学习：完全因人而异（用户专有术语、昵称、表达习惯）
 */

import type { StructuredFact } from './types.ts'

// ═══════════════════════════════════════════════════════════════════════════════
// TYPES
// ═══════════════════════════════════════════════════════════════════════════════

export interface StructureWord {
  words?: string[]                                    // 简单匹配
  gapPatterns?: Array<{ prefix: string; suffix: string }>  // 间隔匹配（"在X工作"）
  slot: string                                        // 语义槽类型
  predicate: string                                   // 映射到 fact-store predicate
  seedStrength: 'strong' | 'medium' | 'weak'          // 冷启动强度
  learned?: boolean                                   // 是否从对话中学到的
}

// ═══════════════════════════════════════════════════════════════════════════════
// SEED STRUCTURE WORDS（冷启动种子，后续 per-user 动态调整）
// ═══════════════════════════════════════════════════════════════════════════════

const SEED_STRUCTURES: StructureWord[] = [
  // 所有权/宠物
  { words: ['养了', '喂', '遛', '家有', '有一只', '有一条', '有一个', 'have a', 'own a', 'my pet', 'feed', 'walk'], slot: 'ownership', predicate: 'has_pet', seedStrength: 'strong' },
  // 居住
  { words: ['住在', '搬到', '搬去', '搬家到', 'live in', 'moved to', 'located in', 'based in'], slot: 'location', predicate: 'lives_in', seedStrength: 'strong' },
  { gapPatterns: [{ prefix: '住在', suffix: '' }, { prefix: 'live in', suffix: '' }, { prefix: 'moved to', suffix: '' }, { prefix: 'based in', suffix: '' }], slot: 'location', predicate: 'lives_in', seedStrength: 'strong' },
  // 偏好
  { words: ['喜欢', '爱', '偏好', '迷上', '着迷', '特别喜欢', '超喜欢', 'like', 'love', 'prefer', 'enjoy', 'into', 'fan of'], slot: 'preference', predicate: 'likes', seedStrength: 'strong' },
  // 反感
  { words: ['讨厌', '不喜欢', '受不了', '不想用', '烦死', 'hate', 'dislike', "can't stand", "don't like"], slot: 'dislike', predicate: 'dislikes', seedStrength: 'strong' },
  // 工作
  { gapPatterns: [{ prefix: '在', suffix: '工作' }, { prefix: '在', suffix: '上班' }, { prefix: '入职', suffix: '' }, { prefix: '加入了', suffix: '' }, { prefix: 'work at', suffix: '' }, { prefix: 'work for', suffix: '' }, { prefix: 'employed at', suffix: '' }, { prefix: 'joined', suffix: '' }], slot: 'workplace', predicate: 'works_at', seedStrength: 'strong' },
  // 关系
  { words: ['女朋友', '男朋友', '老婆', '老公', '对象', '媳妇', '另一半', '爱人', 'girlfriend', 'boyfriend', 'wife', 'husband', 'partner', 'spouse'], slot: 'relationship', predicate: 'relationship', seedStrength: 'strong' },
  // 家庭
  { words: ['女儿', '儿子', '孩子', '爸', '妈', '哥', '姐', '弟', '妹', 'daughter', 'son', 'child', 'dad', 'mom', 'brother', 'sister', 'father', 'mother'], slot: 'family', predicate: 'has_family', seedStrength: 'strong' },
  // 职业
  { gapPatterns: [{ prefix: '我是', suffix: '工程师' }, { prefix: '我是', suffix: '开发' }, { prefix: '我是做', suffix: '的' }, { prefix: 'i am a', suffix: '' }, { prefix: 'i work as', suffix: '' }, { prefix: 'my job is', suffix: '' }], slot: 'occupation', predicate: 'occupation', seedStrength: 'strong' },
  // 习惯
  { words: ['每天', '习惯', '经常', '总是', '一般都', 'every day', 'usually', 'always', 'habit', 'routine'], slot: 'habit', predicate: 'habit', seedStrength: 'medium' },
  // 学习
  { words: ['在学', '在研究', '开始学', '入门', '最近在看', '想学', '准备学', '打算学', 'learning', 'studying', 'started learning', 'getting into', 'picked up'], slot: 'learning', predicate: 'learning', seedStrength: 'medium' },
  // 引用（弱信号）
  { words: ['提到', '说过', '聊到', '听说', 'mentioned', 'said', 'talked about', 'heard'], slot: 'mention', predicate: 'mentioned', seedStrength: 'weak' },
  // 比较偏好
  { gapPatterns: [{ prefix: '', suffix: '比' }], slot: 'comparison', predicate: 'prefers', seedStrength: 'medium' },

  // ── S2: 英文扩展模式（补充覆盖面）──
  // 教育
  { words: ['graduated from', 'studied at', 'majored in', 'degree in', 'enrolled in', 'attended'], slot: 'education', predicate: 'education', seedStrength: 'strong' },
  // 健康
  { words: ['allergic to', "can't eat", 'diagnosed with', 'suffer from', 'taking medication', 'prescribed'], slot: 'health', predicate: 'health_condition', seedStrength: 'strong' },
  // 年龄/身份
  { gapPatterns: [{ prefix: "i'm", suffix: 'years old' }, { prefix: 'i am', suffix: 'years old' }, { prefix: 'my name is', suffix: '' }, { prefix: 'call me', suffix: '' }], slot: 'identity', predicate: 'identity', seedStrength: 'strong' },
  // 乐器/运动
  { words: ['play the', 'play guitar', 'play piano', 'play violin', 'practice', 'train for'], slot: 'activity', predicate: 'plays', seedStrength: 'medium' },
  // 语言
  { words: ['speak', 'fluent in', 'native speaker', 'bilingual', 'learning to speak'], slot: 'language', predicate: 'speaks', seedStrength: 'medium' },
  // 旅行
  { words: ['traveled to', 'visited', 'went to', 'been to', 'trip to', 'vacation in'], slot: 'travel', predicate: 'traveled_to', seedStrength: 'medium' },
  // 购买/拥有
  { words: ['bought', 'purchased', 'got a new', 'recently got', 'just bought'], slot: 'purchase', predicate: 'bought', seedStrength: 'medium' },
  // 创作
  { words: ['painted', 'wrote', 'built', 'created', 'made', 'designed', 'composed'], slot: 'creation', predicate: 'created', seedStrength: 'medium' },
  // 婚姻
  { words: ['married to', 'engaged to', 'dating', 'in a relationship', 'my fiancé', 'my fiancée'], slot: 'relationship', predicate: 'married_to', seedStrength: 'strong' },
  // 恐惧
  { words: ['afraid of', 'scared of', 'phobia', 'terrified of', "can't stand"], slot: 'fear', predicate: 'fears', seedStrength: 'medium' },
  // 目标
  { words: ['want to', 'planning to', 'hope to', 'dream of', 'goal is', 'aiming for'], slot: 'goal', predicate: 'wants_to', seedStrength: 'weak' },
]

// ═══════════════════════════════════════════════════════════════════════════════
// PER-USER STRENGTH LEARNING
// ═══════════════════════════════════════════════════════════════════════════════

// 运行时 per-user 强度缓存：userId → structureWord → { hits, total }
const _userStrength = new Map<string, Map<string, { hits: number; total: number }>>()

/**
 * 获取结构词对特定用户的有效强度
 * 优先用该用户的学习数据，没数据退化到 seed
 */
export function getEffectiveStrength(structureWord: string, userId?: string): number {
  if (userId) {
    const userMap = _userStrength.get(userId)
    if (userMap) {
      const data = userMap.get(structureWord)
      if (data && data.total >= 2) {
        return data.hits / data.total
      }
    }
  }
  // 退化到 seed
  for (const s of SEED_STRUCTURES) {
    if (s.words?.includes(structureWord)) {
      return s.seedStrength === 'strong' ? 1.0 : s.seedStrength === 'medium' ? 0.5 : 0.3
    }
  }
  return 0.3
}

/**
 * 更新结构词强度（每次成功提取事实后调用）
 */
export function updateStructureStrength(structureWord: string, userId: string, wasCorrectSlot: boolean): void {
  if (!_userStrength.has(userId)) _userStrength.set(userId, new Map())
  const userMap = _userStrength.get(userId)!
  const data = userMap.get(structureWord) ?? { hits: 0, total: 0 }
  data.total++
  if (wasCorrectSlot) data.hits++
  userMap.set(structureWord, data)
}

// ═══════════════════════════════════════════════════════════════════════════════
// CORE EXTRACTION — 替代 fact-store 的硬编码正则
// ═══════════════════════════════════════════════════════════════════════════════

interface ExtractionResult {
  subject: string
  predicate: string
  object: string
  confidence: number
  source: 'user_said' | 'ai_inferred'
  structureWord: string    // 匹配到的结构词（用于强度学习）
  slot: string
}

/**
 * 动态事实提取：结构词（种子+学习）× 内容词（纯学习）
 */
export function dynamicExtract(content: string, userId?: string): ExtractionResult[] {
  const results: ExtractionResult[] = []
  if (!content || content.length < 4) return results

  for (const structure of SEED_STRUCTURES) {
    // 间隔匹配
    if (structure.gapPatterns) {
      for (const gp of structure.gapPatterns) {
        const extracted = matchGapPattern(content, gp)
        if (extracted && extracted.length >= 1 && extracted.length <= 15) {
          const strength = getEffectiveStrength(gp.prefix || gp.suffix, userId)
          const threshold = structure.seedStrength === 'strong' ? 0.3 : structure.seedStrength === 'medium' ? 0.5 : 0.7
          if (strength >= threshold) {
            results.push({
              subject: 'user', predicate: structure.predicate, object: extracted.replace(/[，。！？\s]+$/, '').replace(/[了的呢吧啊嘛]+$/, ''),
              confidence: Math.min(0.95, strength), source: 'user_said',
              structureWord: gp.prefix || gp.suffix, slot: structure.slot,
            })
          }
        }
      }
    }

    // 简单词匹配
    if (structure.words) {
      for (const word of structure.words) {
        const idx = content.indexOf(word)
        if (idx < 0) continue

        // 主语检查：结构词前面如果是第三人称（老板/他/她/同事），subject 不是 user
        const beforeWord = content.slice(Math.max(0, idx - 6), idx)
        const thirdPerson = /老板|同事|他|她|朋友|对方|客户/.test(beforeWord)
        if (thirdPerson && structure.predicate !== 'relationship') continue  // 跳过非用户主语

        // 提取结构词后面的内容词（到标点/空格/句末截止）
        const afterWord = content.slice(idx + word.length).trim()
        const contentWord = afterWord.match(/^([^\s，。！？,;；\n]{1,15})/)?.[1]
        if (!contentWord || contentWord.length < 1) continue

        // 检查该用户对这个结构词的强度
        const strength = getEffectiveStrength(word, userId)
        const threshold = structure.seedStrength === 'strong' ? 0.3 : structure.seedStrength === 'medium' ? 0.5 : 0.7

        if (strength >= threshold) {
          let object = contentWord.replace(/[，。！？\s]+$/, '').replace(/[了的呢吧啊嘛]+$/, '')
          if (object.length < 1) continue
          // relationship 特殊处理：结构词（女朋友/老婆等）+ 名字
          if (structure.slot === 'relationship') {
            // "女朋友小雨" → "女朋友：小雨"；"女朋友叫小雨" → "女朋友：小雨"
            object = object.replace(/^叫/, '')
            object = `${word}：${object}`
          }
          results.push({
            subject: 'user', predicate: structure.predicate, object,
            confidence: Math.min(0.95, strength), source: 'user_said',
            structureWord: word, slot: structure.slot,
          })
        }
        break  // 每个 structure 只匹配一次
      }
    }
  }

  // AAM 动态补充：检查 learned structure words
  try {
    const learnedStructures = getLearnedStructureWords(userId)
    for (const ls of learnedStructures) {
      for (const word of ls.words ?? []) {
        const idx = content.indexOf(word)
        if (idx < 0) continue
        const afterWord = content.slice(idx + word.length).trim()
        const contentWord = afterWord.match(/^([^\s，。！？,;；\n]{1,15})/)?.[1]
        if (!contentWord) continue
        results.push({
          subject: 'user', predicate: ls.predicate, object: contentWord.replace(/[，。！？\s]+$/, ''),
          confidence: 0.6, source: 'ai_inferred',
          structureWord: word, slot: ls.slot,
        })
        break
      }
    }
  } catch {}

  // 去重：同 predicate+object 只保留第一条
  const seen = new Set<string>()
  const deduped = results.filter(r => {
    const key = `${r.predicate}:${r.object}`
    if (seen.has(key)) return false
    seen.add(key)
    return true
  })
  return deduped
}

/**
 * 间隔匹配：prefix + gap + suffix
 * "在 Google 工作" → prefix="在" + gap="Google" + suffix="工作"
 */
function matchGapPattern(text: string, pattern: { prefix: string; suffix: string }): string | null {
  if (!pattern.prefix && !pattern.suffix) return null
  if (pattern.prefix && !pattern.suffix) {
    // 只有前缀：提取前缀后的内容词
    const idx = text.indexOf(pattern.prefix)
    if (idx < 0) return null
    const after = text.slice(idx + pattern.prefix.length).trim()
    return after.match(/^([^\s，。！？,;；\n]{1,15})/)?.[1] ?? null
  }
  // prefix + suffix：提取间隔
  const re = new RegExp(`${escapeRegex(pattern.prefix)}([^，。！？,;；\\n]{1,15})${escapeRegex(pattern.suffix)}`)
  const match = text.match(re)
  return match ? match[1].trim() : null
}

function escapeRegex(s: string): string {
  return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
}

// ═══════════════════════════════════════════════════════════════════════════════
// STRUCTURE WORD DISCOVERY — 从对话中发现新结构词
// ═══════════════════════════════════════════════════════════════════════════════

// 用户学到的新结构词缓存
const _learnedStructures = new Map<string, StructureWord[]>()  // userId → structures

function getLearnedStructureWords(userId?: string): StructureWord[] {
  if (!userId) return []
  return _learnedStructures.get(userId) ?? []
}

/**
 * 发现新结构词（heartbeat 调用）
 * 条件：某个 2-3 字短语后面跟的内容词 a) 变化多样 b) 但互相共现（同一语义类别）
 */
export function discoverNewStructureWords(userId: string): void {
  try {
    const aamMod = require('./aam.ts')
    if (!aamMod.getCooccurrence) return

    // 从 AAM 找高频出现的 2-3 字短语
    // 简化版：从 memory 中统计
    const { memoryState } = require('./memory.ts')
    const userMems = memoryState.memories.filter((m: any) => m.userId === userId && m.source === 'user_said')
    if (userMems.length < 10) return  // 数据不够

    const phraseFollowers = new Map<string, string[]>()  // phrase → followers

    for (const m of userMems) {
      const content = m.content || ''
      // 提取 2-3 字短语 + 后面的内容词
      const matches = content.matchAll(/(\p{Script=Han}{2,3})\s*(\p{Script=Han}{2,4})/gu)
      for (const match of matches) {
        const phrase = match[1]
        const follower = match[2]
        if (!phraseFollowers.has(phrase)) phraseFollowers.set(phrase, [])
        phraseFollowers.get(phrase)!.push(follower)
      }
    }

    // 筛选：出现 3+ 次 + followers 有类别集中度
    for (const [phrase, followers] of phraseFollowers) {
      if (followers.length < 3) continue
      // 已经是种子？跳过
      if (SEED_STRUCTURES.some(s => s.words?.includes(phrase))) continue
      // 已经学过？跳过
      const existing = _learnedStructures.get(userId) ?? []
      if (existing.some(s => s.words?.includes(phrase))) continue

      // 类别集中度检查：follower 之间的互相共现
      const unique = [...new Set(followers)]
      if (unique.length < 2) continue

      let intraCooccurrence = 0
      const maxPairs = unique.length * (unique.length - 1) / 2
      for (let i = 0; i < unique.length && i < 10; i++) {
        for (let j = i + 1; j < unique.length && j < 10; j++) {
          if (aamMod.getCooccurrence(unique[i], unique[j]) >= 2) intraCooccurrence++
        }
      }
      const concentration = maxPairs > 0 ? intraCooccurrence / maxPairs : 0

      if (concentration > 0.3) {
        // 发现新结构词
        const newStructure: StructureWord = {
          words: [phrase],
          slot: `learned_${phrase}`,
          predicate: `related_to_${phrase}`,
          seedStrength: 'medium',
          learned: true,
        }
        if (!_learnedStructures.has(userId)) _learnedStructures.set(userId, [])
        _learnedStructures.get(userId)!.push(newStructure)
        // Cap
        const list = _learnedStructures.get(userId)!
        if (list.length > 20) list.splice(0, list.length - 20)

        console.log(`[cc-soul][dynamic-extractor] discovered structure word "${phrase}" for ${userId.slice(0, 8)} (concentration=${concentration.toFixed(2)})`)
      }
    }
  } catch {}
}

// ═══════════════════════════════════════════════════════════════════════════════
// END SIGNAL LEARNING — 结束信号从行为学习
// ═══════════════════════════════════════════════════════════════════════════════

// per-user 结束信号学习：phrase → { endCount, continueCount }
const _endSignalData = new Map<string, Map<string, { endCount: number; continueCount: number }>>()

/**
 * 记录结束信号学习数据
 * 在 flow.ts 的 updateFlow 中调用
 */
export function learnEndSignal(lastUserMsg: string, followUpBehavior: 'silence' | 'topic_switch' | 'continue', userId?: string): void {
  const key = userId ?? '_global'
  if (!_endSignalData.has(key)) _endSignalData.set(key, new Map())
  const userMap = _endSignalData.get(key)!

  // 提取末尾短语（用分词而非截断）
  const tails = extractTailPhrases(lastUserMsg)
  for (const tail of tails) {
    const data = userMap.get(tail) ?? { endCount: 0, continueCount: 0 }
    if (followUpBehavior === 'continue') {
      data.continueCount++
    } else {
      data.endCount++
    }
    userMap.set(tail, data)
  }
}

/**
 * 判断是否是结束信号
 */
export function isEndSignal(msg: string, userId?: string): boolean {
  const tails = extractTailPhrases(msg)
  const key = userId ?? '_global'
  const userMap = _endSignalData.get(key)

  // 1. 学到的信号（优先）
  if (userMap) {
    for (const tail of tails) {
      const data = userMap.get(tail)
      if (data && data.endCount + data.continueCount >= 3) {
        const rate = data.endCount / (data.endCount + data.continueCount)
        if (rate > 0.7) return true
        if (rate < 0.3) return false
      }
    }
  }

  // 2. 种子列表（兜底）
  return /搞定|可以了|好了|解决了|明白了|OK|行吧|没问题|谢谢|thanks/i.test(msg)
}

/** 提取末尾语义短语（倒序分词，不是截断） */
function extractTailPhrases(msg: string): string[] {
  const phrases: string[] = []
  // 从末尾提取 2-6 字的中文短语
  const cjkMatches = msg.match(/[\u4e00-\u9fff]{2,6}/g) || []
  if (cjkMatches.length > 0) {
    phrases.push(cjkMatches[cjkMatches.length - 1])  // 最后一个中文短语
    if (cjkMatches.length > 1) phrases.push(cjkMatches[cjkMatches.length - 2])  // 倒数第二个
  }
  // 英文短词
  const enMatches = msg.match(/[a-zA-Z]{2,10}/gi) || []
  if (enMatches.length > 0) phrases.push(enMatches[enMatches.length - 1].toLowerCase())
  return phrases
}

// ═══════════════════════════════════════════════════════════════════════════════
// PERSON RELATIONSHIP INFERENCE — 人物关系从语境推断
// ═══════════════════════════════════════════════════════════════════════════════

// 语境种子（冷启动，后续从 AAM 补充）
const WORK_CONTEXT_SEEDS = new Set(['代码', '项目', '会议', 'review', '上线', '部署', '需求', '排期', '加班', '进度', '文档', 'bug', '测试'])
const LIFE_CONTEXT_SEEDS = new Set(['吃饭', '看电影', '逛街', '回家', '周末', '旅游', '做饭', '散步', '约会', '生日'])
const COMMAND_SEEDS = new Set(['让我', '要求', '安排', '批准', '审批', '交给', '催', '指示', '叫我'])

/**
 * 从语境推断人物关系（不靠称呼列表）
 */
export function inferRelationship(personName: string, userId?: string): 'superior' | 'colleague' | 'close_relation' | 'family' | 'acquaintance' | 'unknown' {
  try {
    const aamMod = require('./aam.ts')
    if (!aamMod.getCooccurrence) return 'unknown'

    let workScore = 0, lifeScore = 0, commandScore = 0

    // 检查人名跟各语境种子的共现
    for (const w of WORK_CONTEXT_SEEDS) {
      workScore += aamMod.getCooccurrence(personName, w) ?? 0
    }
    for (const w of LIFE_CONTEXT_SEEDS) {
      lifeScore += aamMod.getCooccurrence(personName, w) ?? 0
    }
    for (const w of COMMAND_SEEDS) {
      commandScore += aamMod.getCooccurrence(personName, w) ?? 0
    }

    const total = workScore + lifeScore + commandScore
    if (total < 3) return 'unknown'

    if (commandScore > workScore * 0.5) return 'superior'
    if (workScore > lifeScore * 2) return 'colleague'
    if (lifeScore > workScore * 2) return 'close_relation'
    return 'acquaintance'
  } catch {
    return 'unknown'
  }
}
