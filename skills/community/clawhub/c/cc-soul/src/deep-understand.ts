/**
 * deep-understand.ts — 7 维深层理解引擎
 * 周期性分析积累数据，产出影响回复策略的洞察。纯规则驱动，不调 LLM。
 */
import { resolve } from 'path'
import { DATA_DIR, loadJson, debouncedSave } from './persistence.ts'
import { memoryState, ensureMemoriesLoaded } from './memory.ts'
import { getPersonModel } from './person-model.ts'

const DU_PATH = resolve(DATA_DIR, 'deep_understand.json')

interface DeepUnderstandState {
  temporal: { peakHours: number[]; stressDay: string | null; lateNightFrequency: number }
  sayDo: { gaps: { stated: string; actual: string; frequency: number }[] }
  growth: { direction: 'growing' | 'plateauing' | 'struggling'; details: string }
  unspoken: { needs: { domain: string; confidence: number; evidence: string }[] }
  cognitive: { load: 'high' | 'normal' | 'low'; indicator: string }
  stress: { stressLevel: number; signals: string[] }
  dynamicProfile: string
  updatedAt: number
}

const DEFAULTS: DeepUnderstandState = {
  temporal: { peakHours: [], stressDay: null, lateNightFrequency: 0 },
  sayDo: { gaps: [] }, growth: { direction: 'plateauing', details: '' },
  unspoken: { needs: [] }, cognitive: { load: 'normal', indicator: '' },
  stress: { stressLevel: 0, signals: [] }, dynamicProfile: '', updatedAt: 0,
}

let state: DeepUnderstandState = loadJson<DeepUnderstandState>(DU_PATH, { ...DEFAULTS })

// ── 1. Temporal Patterns ──
function analyzeTemporalPatterns(): DeepUnderstandState['temporal'] {
  const history = memoryState.chatHistory
  if (history.length < 10) return state.temporal
  const hourCounts = new Array(24).fill(0)
  const dayMood = new Map<number, number[]>()
  let lateNight = 0
  for (const h of history) {
    const d = new Date(h.ts), hr = d.getHours()
    hourCounts[hr]++
    if (hr >= 23 || hr < 4) lateNight++
    const day = d.getDay()
    if (!dayMood.has(day)) dayMood.set(day, [])
    dayMood.get(day)!.push((h.user.length < 10 && (hr >= 22 || hr < 6)) ? -1 : 0)
  }
  const peakHours = hourCounts.map((c: number, i: number) => ({ h: i, c }))
    .sort((a: {h:number,c:number}, b: {h:number,c:number}) => b.c - a.c)
    .slice(0, 3).filter((x: {h:number,c:number}) => x.c > 0).map((x: {h:number,c:number}) => x.h)
  let stressDay: string | null = null, worstAvg = 0
  const dayNames = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
  for (const [day, moods] of dayMood) {
    if (moods.length < 3) continue
    const avg = moods.reduce((a, b) => a + b, 0) / moods.length
    if (avg < worstAvg) { worstAvg = avg; stressDay = dayNames[day] }
  }
  return { peakHours, stressDay, lateNightFrequency: lateNight / history.length }
}

// ── 2. Say-Do Gap ──
function analyzeSayDoGap(): DeepUnderstandState['sayDo'] {
  ensureMemoriesLoaded()
  const history = memoryState.chatHistory
  const intents = memoryState.memories.filter(m => /我要|我打算|我会|我准备|I will|I'm going to/i.test(m.content) && m.scope !== 'expired')
  const gaps: DeepUnderstandState['sayDo']['gaps'] = []
  for (const intent of intents.slice(-10)) {
    const c = intent.content.toLowerCase()
    if (/早睡|早点睡|sleep early/.test(c)) {
      const after = history.filter(h => h.ts > intent.ts)
      const late = after.filter(h => { const hr = new Date(h.ts).getHours(); return hr >= 0 && hr < 5 }).length
      if (after.length > 5 && late / after.length > 0.3)
        gaps.push({ stated: '早睡', actual: `${Math.round(late / after.length * 100)}%消息在凌晨`, frequency: late })
    }
    if (/少加班|多休息|放松|rest more|take break/.test(c)) {
      const wknd = history.filter(h => { const d = new Date(h.ts); return h.ts > intent.ts && (d.getDay() === 0 || d.getDay() === 6) }).length
      if (wknd > 10) gaps.push({ stated: '多休息', actual: `周末仍有${wknd}条消息`, frequency: wknd })
    }
  }
  return { gaps: gaps.slice(0, 5) }
}

// ── 3. Growth Trajectory ──
function analyzeGrowth(): DeepUnderstandState['growth'] {
  const history = memoryState.chatHistory
  if (history.length < 20) return { direction: 'plateauing', details: '数据不足' }
  const half = Math.floor(history.length / 2)
  const first = history.slice(0, half), second = history.slice(half)
  const avgLen = (a: typeof history) => a.reduce((s, h) => s + h.user.length, 0) / a.length
  const l1 = avgLen(first), l2 = avgLen(second)
  const techRe = /async|await|deploy|refactor|pipeline|架构|重构|微服务|并发|索引|缓存/gi
  const techCount = (a: typeof history) => { const s = new Set<string>(); for (const h of a) { const m = h.user.match(techRe); if (m) m.forEach(w => s.add(w.toLowerCase())) } return s.size }
  const t1 = techCount(first), t2 = techCount(second)
  if (l2 > l1 * 1.3 && t2 > t1) return { direction: 'growing', details: `长度+${Math.round((l2/l1-1)*100)}%，词汇${t1}→${t2}` }
  if (l2 < l1 * 0.7 || t2 < t1 * 0.5) return { direction: 'struggling', details: '消息变短或词汇减少' }
  return { direction: 'plateauing', details: '模式稳定' }
}

// ── 3b. Learning Curve Fit (幂律学习曲线拟合) ──

/**
 * 学习曲线拟合：用幂律学习曲线 performance = a × t^b 拟合用户成长
 * 认知科学基础：Power Law of Learning (Newell & Rosenbloom 1981)
 *
 * b > 0 = 在成长
 * b ≈ 0 = 平台期
 * b < 0 = 退步
 */
export interface LearningCurve {
  growthRate: number      // b 值：正=成长，0=平台，负=退步
  currentLevel: number    // 当前水平估计 [0, 1]
  plateau: boolean        // 是否进入平台期
  prediction: string      // 自然语言描述
}

export function fitLearningCurve(history: { user: string; ts: number }[]): LearningCurve {
  if (history.length < 10) return { growthRate: 0, currentLevel: 0.5, plateau: false, prediction: '数据不足' }

  // 按时间排序，每 5 条消息一组计算"水平"指标
  const windowSize = 5
  const dataPoints: { t: number; level: number }[] = []

  for (let i = 0; i <= history.length - windowSize; i += windowSize) {
    const window = history.slice(i, i + windowSize)
    const avgLen = window.reduce((s, h) => s + h.user.length, 0) / windowSize
    // 词汇丰富度：唯一 2-gram 数 / 总 2-gram 数
    const allWords = window.map(h => h.user.match(/[\u4e00-\u9fff]{2,}|[a-z]{3,}/gi) || []).flat()
    const unique = new Set(allWords.map(w => w.toLowerCase()))
    const richness = allWords.length > 0 ? unique.size / allWords.length : 0
    // 综合水平 = 长度归一化 * 0.4 + 词汇丰富度 * 0.6
    const level = Math.min(1, (avgLen / 100) * 0.4 + richness * 0.6)
    dataPoints.push({ t: i / windowSize + 1, level })
  }

  if (dataPoints.length < 3) return { growthRate: 0, currentLevel: 0.5, plateau: false, prediction: '数据不足' }

  // 对数线性回归拟合 log(level) = log(a) + b * log(t)
  // 即 y = c + b * x，其中 y = log(level), x = log(t)
  const xs = dataPoints.map(d => Math.log(d.t + 1))
  const ys = dataPoints.map(d => Math.log(Math.max(0.01, d.level)))
  const n = xs.length
  const sumX = xs.reduce((s, x) => s + x, 0)
  const sumY = ys.reduce((s, y) => s + y, 0)
  const sumXY = xs.reduce((s, x, i) => s + x * ys[i], 0)
  const sumXX = xs.reduce((s, x) => s + x * x, 0)

  const b = (n * sumXY - sumX * sumY) / (n * sumXX - sumX * sumX + 1e-9)
  const currentLevel = dataPoints[dataPoints.length - 1].level
  const plateau = Math.abs(b) < 0.05 && dataPoints.length >= 5

  let prediction = ''
  if (b > 0.15) prediction = '快速成长期，保持节奏'
  else if (b > 0.05) prediction = '稳步提升中'
  else if (b > -0.05) prediction = '平台期，可能需要新挑战'
  else prediction = '有所下滑，建议调整方向'

  return { growthRate: b, currentLevel, plateau, prediction }
}

// ── 4. Unspoken Needs ──
function analyzeUnspokenNeeds(): DeepUnderstandState['unspoken'] {
  const recent = memoryState.chatHistory.filter(h => h.ts > Date.now() - 7 * 86400000)
  const domains: [string, RegExp][] = [
    ['编程/coding', /代码|bug|error|函数|class|api|编程|开发|调试|debug|code|programming|development|compile|runtime|stack/i],
    ['职场/career', /工作|老板|同事|面试|加班|薪|绩效|晋升|job|boss|colleague|interview|overtime|salary|promotion|workplace|career/i],
    ['健康/health', /睡眠|运动|头疼|累|健身|饮食|体检|sleep|exercise|headache|tired|fitness|diet|medical|workout/i],
    ['情感/emotion', /感觉|心情|焦虑|压力|开心|难过|孤独|feeling|mood|anxious|stress|happy|sad|lonely|depressed/i],
    ['学习/learning', /学习|考试|课程|教程|理解|掌握|study|exam|course|tutorial|understand|learn|education/i],
  ]
  const counts = new Map<string, number>()
  for (const h of recent) for (const [d, re] of domains) if (re.test(h.user)) counts.set(d, (counts.get(d) || 0) + 1)
  const needs = [...counts.entries()].filter(([, n]) => n >= 3)
    .map(([d, n]) => ({ domain: d, confidence: Math.min(1, n / 10), evidence: `本周${n}次` }))
    .sort((a, b) => b.confidence - a.confidence).slice(0, 5)
  return { needs }
}

// ── 5. Cognitive Load ──
function analyzeCognitiveLoad(): DeepUnderstandState['cognitive'] {
  const history = memoryState.chatHistory
  if (history.length < 5) return { load: 'normal', indicator: '' }
  const allAvg = history.reduce((s, h) => s + h.user.length, 0) / history.length
  const r5 = history.slice(-5)
  const rAvg = r5.reduce((s, h) => s + h.user.length, 0) / r5.length
  if (rAvg < allAvg * 0.4 && rAvg < 20) return { load: 'high', indicator: `均${Math.round(rAvg)}字(历史${Math.round(allAvg)})` }
  if (rAvg > allAvg * 1.5 && rAvg > 80) return { load: 'low', indicator: `详细模式${Math.round(rAvg)}字` }
  return { load: 'normal', indicator: '' }
}

// ── 6. Stress Fingerprint ──
function analyzeStress(): DeepUnderstandState['stress'] {
  const history = memoryState.chatHistory
  if (history.length < 5) return { stressLevel: 0, signals: [] }
  const recent = history.slice(-10), signals: string[] = []
  let score = 0
  const rAvg = recent.reduce((s, h) => s + h.user.length, 0) / recent.length
  const hAvg = history.reduce((s, h) => s + h.user.length, 0) / history.length
  if (rAvg < hAvg * 0.5 && rAvg < 15) { score += 0.3; signals.push('碎片化') }
  if (recent.reduce((s, h) => s + (h.user.match(/[?？!！.。…]{2,}/g) || []).length, 0) >= 3) { score += 0.2; signals.push('标点激增') }
  if (recent.filter(h => /算了|随便|fuck|shit|烦|累|不管了|懒得|无所谓|操|靠|妈的|whatever|tired|give up|don't care|screw it|damn|crap|ugh|fed up|sick of|over it/.test(h.user)).length >= 2) { score += 0.3; signals.push('压力词/stress words') }
  if (recent.filter(h => { const hr = new Date(h.ts).getHours(); return hr >= 1 && hr < 5 }).length >= 2) { score += 0.2; signals.push('深夜') }
  return { stressLevel: Math.min(1, score), signals }
}

// ── 6b. Cognitive Load Dynamics (弹簧-阻尼压力模型) ──

/**
 * 认知负荷波动模型：建模压力的积累-释放动力学
 * 不是检测"现在有没有压力"，而是建模压力的轨迹
 *
 * 积累期：连续短消息 + 负面词 → 压力上升
 * 释放期：长消息 + 正面反馈 → 压力释放
 * 爆发预测：压力超过阈值且加速 → 预测即将爆发
 *
 * 物理模型：弹簧-阻尼系统
 * dx/dt = -k*x + F(t) - γ*v
 * x = 压力水平, k = 恢复弹性, F(t) = 外部应激, γ = 阻尼（韧性）
 */
export interface StressDynamics {
  level: number           // 当前压力 [0, 1]
  velocity: number        // 变化速率（正=恶化）
  phase: 'accumulating' | 'peak' | 'releasing' | 'calm'
  turnsToBreakdown: number | null  // 预测几轮后可能爆发（null=不会）
  resilience: number      // 估计的恢复弹性 [0, 1]
}

export function analyzeStressDynamics(history: { user: string; ts: number }[]): StressDynamics {
  if (history.length < 5) return { level: 0, velocity: 0, phase: 'calm', turnsToBreakdown: null, resilience: 0.5 }

  const recent = history.slice(-15)
  const signals: number[] = []

  for (let i = 0; i < recent.length; i++) {
    const msg = recent[i].user
    let signal = 0

    // 消息长度信号：短消息 = 压力（失去耐心）
    if (msg.length < 10) signal += 0.15
    else if (msg.length > 80) signal -= 0.1  // 长消息 = 在思考/释放

    // 负面词信号
    if (/烦|累|崩|急|压力|焦虑|受不了|算了|不想|头疼|烦死|frustrated|stressed|overwhelmed|exhausted|annoyed|ugh|burnout/.test(msg)) signal += 0.25
    // 正面词信号
    if (/谢|好的|明白|解决|搞定|不错|太好|thanks|got it|solved|fixed|great|awesome|nice/.test(msg)) signal -= 0.15

    // 标点信号：多个感叹号/问号 = 激动
    if (/[！!]{2,}|[？?]{2,}/.test(msg)) signal += 0.1

    // 时间间隔信号：快速连发 = 急躁
    if (i > 0) {
      const gap = recent[i].ts - recent[i - 1].ts
      if (gap < 10000) signal += 0.1  // 10秒内连发
    }

    signals.push(Math.max(-0.3, Math.min(0.5, signal)))
  }

  // 弹簧-阻尼模型：模拟压力积累
  let x = 0       // 位置（压力水平）
  let v = 0       // 速度
  const k = 0.15  // 恢复弹性（越大恢复越快）
  const gamma = 0.3  // 阻尼系数
  const dt = 1

  for (const F of signals) {
    const a = -k * x + F - gamma * v  // 加速度
    v += a * dt
    x += v * dt
    x = Math.max(0, Math.min(1, x))
    v = Math.max(-0.5, Math.min(0.5, v))
  }

  // 判断阶段
  let phase: StressDynamics['phase'] = 'calm'
  if (x > 0.6 && v > 0) phase = 'peak'
  else if (x > 0.3 && v > 0.05) phase = 'accumulating'
  else if (x > 0.3 && v < -0.05) phase = 'releasing'

  // 爆发预测：如果压力在上升，线性外推几轮后到 0.8
  let turnsToBreakdown: number | null = null
  if (v > 0.03 && x > 0.3) {
    turnsToBreakdown = Math.ceil((0.8 - x) / v)
    if (turnsToBreakdown > 10 || turnsToBreakdown < 0) turnsToBreakdown = null
  }

  // 韧性估计：从历史中观察压力峰值后的恢复速度
  const resilience = Math.max(0.1, Math.min(0.9, k + (1 - x) * 0.3))

  return { level: x, velocity: v, phase, turnsToBreakdown, resilience }
}

// ── 7. Dynamic Profile ──
function synthesizeProfile(): string {
  const pm = getPersonModel(), parts: string[] = []
  const { temporal: t, growth: g, stress: s, cognitive: c, sayDo: sd, unspoken: u } = state
  if (t.peakHours.length > 0) parts.push(`活跃${t.peakHours.join('/')}时`)
  if (t.lateNightFrequency > 0.3) parts.push('夜猫子')
  if (g.direction === 'growing') parts.push('上升期')
  else if (g.direction === 'struggling') parts.push('瓶颈期')
  if (s.stressLevel > 0.5) parts.push(`压力高(${s.signals.join('+')})`)
  // 认知负荷波动模型（优先用耦合压力振荡器，fallback 到独立 stress dynamics）
  let pressureAdded = false
  try {
    const { getCoupledPressure } = require('./flow.ts')
    const cp = getCoupledPressure()
    if (cp && (cp.frustration > 0.3 || cp.stress > 0.3)) {
      if (cp.phase === 'building' || cp.phase === 'critical') parts.push(`压力${cp.phase === 'critical' ? '临界' : '积累中'}(挫败${(cp.frustration*100).toFixed(0)}%,压力${(cp.stress*100).toFixed(0)}%,耦合${(cp.couplingStrength*100).toFixed(0)}%)`)
      if (cp.turnsToBreakdown !== null) parts.push(`预计${cp.turnsToBreakdown}轮后可能爆发`)
      if (cp.phase === 'recovering') parts.push('压力释放中')
      pressureAdded = true
    }
  } catch {}
  if (!pressureAdded) {
    // Fallback: 独立 stress dynamics
    const stressDyn = analyzeStressDynamics(memoryState.chatHistory)
    if (stressDyn.phase === 'accumulating') parts.push(`压力积累中(${(stressDyn.level*100).toFixed(0)}%)`)
    if (stressDyn.turnsToBreakdown !== null) parts.push(`预计${stressDyn.turnsToBreakdown}轮后可能爆发`)
    if (stressDyn.phase === 'releasing') parts.push('压力释放中')
  }
  // 学习曲线拟合
  const lc = fitLearningCurve(memoryState.chatHistory)
  if (lc.prediction && lc.prediction !== '数据不足') parts.push(lc.prediction)
  if (c.load === 'high') parts.push('负荷高→简洁')
  else if (c.load === 'low') parts.push('专注→可深入')
  if (sd.gaps.length > 0) parts.push(`言行不一:${sd.gaps[0].stated}`)
  if (u.needs[0]?.confidence > 0.5) parts.push(`潜在需求:${u.needs[0].domain}`)
  if (pm.identity) parts.push(pm.identity.slice(0, 60))
  return parts.join('；')
}

// ── Public API ──
/** heartbeat 调用 — 刷新全部分析 */
export function updateDeepUnderstand(): void {
  ensureMemoriesLoaded()
  if (memoryState.chatHistory.length < 10) return
  state.temporal = analyzeTemporalPatterns()
  state.sayDo = analyzeSayDoGap()
  state.growth = analyzeGrowth()
  state.unspoken = analyzeUnspokenNeeds()
  state.cognitive = analyzeCognitiveLoad()
  state.stress = analyzeStress()
  state.dynamicProfile = synthesizeProfile()
  state.updatedAt = Date.now()
  debouncedSave(DU_PATH, state)
}

/** handler-augments 调用 — 返回紧凑洞察字符串 */
export function getDeepUnderstandContext(): string {
  if (!state.updatedAt) return ''
  const parts: string[] = []
  const { stress: s, cognitive: c, growth: g, unspoken: u, sayDo: sd, temporal: t } = state
  if (s.stressLevel > 0.4) parts.push(`压力${(s.stressLevel*10).toFixed(0)}/10(${s.signals.join(',')})`)
  if (c.load !== 'normal') parts.push(c.load === 'high' ? '认知负荷高→简洁回复' : '专注模式→可深入')
  if (g.direction !== 'plateauing') parts.push(g.direction === 'growing' ? '成长期→适当提高难度' : '瓶颈期→多鼓励')
  if (u.needs[0]?.confidence > 0.5) parts.push(`可能需要${u.needs[0].domain}方面的帮助`)
  if (sd.gaps[0]) parts.push(`说"${sd.gaps[0].stated}"但${sd.gaps[0].actual}→温和引导`)
  if (t.lateNightFrequency > 0.4) parts.push('经常深夜活跃')
  if (parts.length === 0) return ''
  return '[深层理解] ' + parts.join('；')
}
