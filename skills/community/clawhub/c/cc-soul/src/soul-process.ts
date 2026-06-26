/**
 * soul-process.ts — Core message processing pipeline
 *
 * Handles POST /process and POST /feedback.
 * Runs the full cc-soul pipeline: cognition → emotion → memory → augments → return.
 * Does NOT call LLM — returns enriched context for customer's AI.
 */

import './persistence.ts' // ensure data dir init
import { handleError } from './errors.ts'

// 去重：防止同一条记忆在飞书群聊拆消息场景下被多次 penalize
const _lastPenalizeTs = new Map<string, number>()

// ── In-memory dedup cache (replaces file-based recent_replies.json) ──
const _dedupCache = new Map<string, { reply: string; ts: number }>()
let _crossTurnLastMsg: Record<string, string> = {}  // T3: 跨轮配对学习（按 userId 隔离）
const DEDUP_TTL = 3600000 // 1 hour (matches original expiry)
function cleanDedup() {
  const now = Date.now()
  for (const [k, v] of _dedupCache) {
    if (now - v.ts > DEDUP_TTL) _dedupCache.delete(k)
  }
}


/** Isolate independent pipeline steps — on throw, log degradation and return fallback */
async function safeCompute<T>(fn: () => Promise<T> | T, fallback: T, context: string): Promise<T> {
  try { return await fn() }
  catch (e: any) {
    try { const { logDecision } = require('./decision-log.ts'); logDecision('degraded', context, e.message) } catch {}
    console.warn(`[cc-soul][${context}] degraded: ${e.message}`)
    return fallback
  }
}

async function handleProcess(body: any): Promise<any> {
  // 热加载 ai_config.json（用户改了文件不用重启）
  try { (await import('./cli.ts')).hotReloadIfChanged() } catch {}

  const message = body.message || ''
  const userId = body.user_id || body.userId || 'default'
  const agentId = body.agent_id || body.agentId || 'default'
  const customPrompt = body.system_prompt || ''

  // 自适应 context budget：如果调用方传了 context_window，设置到 budget manager
  if (body.context_window && typeof body.context_window === 'number') {
    try {
      const { setContextWindow } = await import('./context-budget.ts')
      setContextWindow(body.context_window)
    } catch {}
  }

  // ── 确保记忆已加载（lazy-load 模式必须在 recall 之前调用）──
  try { (await import('./memory.ts')).ensureMemoriesLoaded() } catch {}

  // ── 轮次快照：防止并发读-改-写冲突 ──
  let turnSnapshot: Map<string, number> | null = null
  try {
    const { memoryState } = await import('./memory.ts')
    turnSnapshot = new Map()
    for (const m of memoryState.memories) {
      if (m.memoryId) turnSnapshot.set(m.memoryId, m.lineage?.length ?? 0)
    }
  } catch {}

  // Multi-agent isolation: switch data directory if agent_id provided
  if (agentId !== 'default') {
    try { const { setActiveAgent } = await import('./persistence.ts'); setActiveAgent(agentId) } catch {}
  }

  // Privacy mode check: skip memory operations if privacy is ON
  let isPrivacy = false
  try {
    const { getPrivacyMode } = await import('./handler-state.ts')
    isPrivacy = getPrivacyMode()
  } catch {}

  // Bootstrap mode: empty message → return system_prompt only
  if (!message) {
    try {
      const { ensureDataDir } = await import('./persistence.ts')
      ensureDataDir()
      try { (await import('./memory.ts')).ensureSQLiteReady() } catch {}
    } catch {}
    try { (await import('./handler.ts')).initializeSoul() } catch {}
    let soulPrompt = ''
    try {
      const { buildSoulPrompt } = await import('./prompt-builder.ts')
      const { stats } = await import('./handler-state.ts')
      soulPrompt = buildSoulPrompt(stats.totalMessages, stats.corrections, stats.firstSeen, [])
    } catch {}
    return { system_prompt: customPrompt ? customPrompt + '\n\n' + soulPrompt : soulPrompt, augments: [] }
  }

  // ── Command detection: check before full pipeline ──
  try {
    const { routeCommand, routeCommandDirect } = await import('./handler-commands.ts')
    const { getSessionState } = await import('./handler-state.ts')
    const session = getSessionState(userId)
    let cmdReply = ''
    const replyFn = (t: string) => { cmdReply = t }
    const cmdCtx = { bodyForAgent: '', reply: replyFn }

    // Try routeCommand first (sync, handles write commands)
    const handled = routeCommand(message, cmdCtx, session, userId, '', { context: { senderId: userId } })
    if (handled && cmdReply) {
      return { command: true, command_reply: cmdReply }
    }

    // Try routeCommandDirect (async, handles read-only commands like 价值观/审计 etc.)
    if (!cmdReply) {
      const directHandled = await routeCommandDirect(message, { replyCallback: replyFn })
      if (directHandled && cmdReply) {
        return { command: true, command_reply: cmdReply }
      }
    }
  } catch (cmdErr: any) {
    console.error(`[cc-soul][api] command detection error: ${cmdErr.message}`)
  }

  // Initialize (lazy)
  try {
    (await import('./persistence.ts')).ensureDataDir()
    try { (await import('./memory.ts')).ensureSQLiteReady() } catch {}
  } catch {}
  try { (await import('./handler.ts')).initializeSoul() } catch {}

  // ── 交叉学习：每条用户消息喂 AAM（不只是查询时）──
  try { (await import('./aam.ts')).learnAssociation(message) } catch {}

  // ── T3: 跨轮配对学习——相邻消息建立语义桥梁（按 userId 隔离）──
  try {
    const _uid = senderId || 'default'
    if (!_crossTurnLastMsg) _crossTurnLastMsg = {}
    const lastMsg = _crossTurnLastMsg[_uid] || ''
    if (lastMsg.length > 10 && message.length > 10) {
      const prev = (lastMsg.match(/[\u4e00-\u9fff]{2,}|[a-zA-Z]{3,}/gi) || []).slice(0, 8)
      const curr = (message.match(/[\u4e00-\u9fff]{2,}|[a-zA-Z]{3,}/gi) || []).slice(0, 8)
      if (prev.length > 0 && curr.length > 0) {
        (await import('./aam.ts')).learnAssociation(prev.join(' ') + ' ' + curr.join(' '), 0.3)
      }
    }
    _crossTurnLastMsg[_uid] = message
  } catch {}

  // ── 语义漂移追踪：每条用户消息喂滑动窗口 ──
  try { (await import('./semantic-drift.ts')).trackMessage(message) } catch {}

  // ── 0.5 语言自适应种子翻译（首次启动 + 有 LLM → 翻译种子词；没 LLM → 跳过）──
  try { (await import('./aam.ts')).maybeTranslateSeedsForLanguage(message) } catch {}

  // ── 1. Body tick + emotional processing (isolated — failure won't block cognition) ──
  const bodyFallback = { mood: 0, energy: 0.5, alertness: 0.5 }
  const bodyResult = await safeCompute(async () => {
    const bodyMod = await import('./body.ts')
    try { bodyMod.loadBodyState() } catch {}
    let peakHour: number | undefined
    try { peakHour = (await import('./user-profiles.ts')).getUserPeakHour(userId); if (peakHour === -1) peakHour = undefined } catch {}
    bodyMod.bodyTick(peakHour)
    bodyMod.bodyOnMessage(message.length > 50 ? 0.6 : 0.3)
    return { mood: bodyMod.body.mood, energy: bodyMod.body.energy, alertness: bodyMod.body.alertness ?? 0.5 }
  }, bodyFallback, 'body-tick')

  let moodScore = bodyResult.mood, energyScore = bodyResult.energy, emotion = 'neutral'

  // ── 2. Cognition (isolated — failure won't block body/emotion) ──
  const cogFallback = { attention: 'general' as const, intent: 'wants_answer', strategy: 'balanced', complexity: 0.3, hints: [], spectrum: { information: 0.5, action: 0.2, emotional: 0.2, validation: 0.1, exploration: 0.2 } }
  let cogResult: any = await safeCompute(async () => {
    const { cogProcess } = await import('./cognition.ts')
    const { getSessionState: _getSess } = await import('./handler-state.ts')
    const _sess = _getSess(userId)
    const result = cogProcess(message, _sess.lastResponseContent || '', _sess.lastPrompt || '', userId)
    if (result.attention === 'correction') {
      try {
        (await import('./user-profiles.ts')).updateProfileOnCorrection(userId)
        ;(await import('./body.ts')).bodyOnCorrection()
        const { emitCacheEvent } = require('./memory-utils.ts')
        emitCacheEvent('correction_received')
      } catch {}
    }
    return result
  }, cogFallback, 'cognition')

  // ── 3. Flow（moved before emotional contagion so frustration is available）──
  let flow: any = null
  try { flow = (await import('./flow.ts')).updateFlow(message, '', userId) } catch {}

  // ── Topic River: 话题切换时递增 segment ID ──
  if (flow?.turnCount === 1) {
    try { (await import('./memory.ts')).incrementSegment() } catch {}
  }

  // ── 2b. Emotional contagion (with actual frustration from flow) ──
  try {
    const bodyMod = await import('./body.ts')
    const attention = cogResult?.attention || 'general'
    const frustration = flow?.frustrationTrajectory?.current ?? flow?.frustration ?? 0
    bodyMod.processEmotionalContagion(message, attention, frustration, userId)
    moodScore = bodyMod.body.mood; energyScore = bodyMod.body.energy
    emotion = moodScore > 0.3 ? 'positive' : moodScore < -0.3 ? 'negative' : 'neutral'
  } catch {}

  // ── 3.5 共享 extractFacts 结果（避免 3 个模块各自重新跑正则）──
  // 一次提取，带 source/userId，下游 addFacts + person-model/user-profiles/avatar 共用
  let _sharedFacts: any[] = []
  try {
    const { extractFacts } = await import('./fact-store.ts')
    _sharedFacts = extractFacts(message, 'user_said', userId)
    ;(globalThis as any).__ccSoulSharedFacts = _sharedFacts
    ;(globalThis as any).__ccSoulSharedFactsTs = Date.now()
  } catch {}

  // ── 4. User profile ──
  try { (await import('./user-profiles.ts')).updateProfileOnMessage(userId, message) } catch {}

  // ── 5. WAL protocol ──
  if (!isPrivacy) {
    try {
      const { addMemory } = await import('./memory.ts')
      const walEntries: string[] = []
      const prefMatch = message.match(/我(?:最|特别|超|很|比较)?(?:喜欢|不喜欢|讨厌|爱|偏好|住在?|是|养了?|有|擅长|从事|叫|在.{1,10}(?:工作|上班|做))(.{2,40})/g)
      if (prefMatch) for (const p of prefMatch.slice(0, 3)) {
        // 动态疑问句检测：用句法结构而非词表
        // 1. 消息级：整句以问号结尾 = 提问
        // 2. 结构级：中文疑问句的句法特征（动词重叠 AB不AB、句尾语气词）
        // 3. 信息量：提取出的 object 比消息短太多 = 可能是残片
        const trimmed = message.trim()
        const isQuestion = /[？?]$/.test(trimmed) ||          // 问号结尾
          /(.)\1不\1/.test(trimmed) ||                         // 动词重叠疑问（是不是/有没有）
          /[吗呢吧嘛]$/.test(trimmed) ||                       // 语气词结尾
          /[？?]/.test(p)                                       // 匹配片段含问号
        if (isQuestion) continue
        // 信息量检查：提取的内容占消息比例太低（<20%）= 可能是误提取
        if (p.length < message.length * 0.2 && p.length < 8) continue
        walEntries.push(p.slice(0, 60))
      }
      const rememberMatch = message.match(/(?:记住|帮我记|你要知道)[：:，,\s]*(.{4,60})/g)
      if (rememberMatch) for (const r of rememberMatch.slice(0, 3)) walEntries.push(r.slice(0, 60))
      for (const entry of walEntries) addMemory(`[WAL事实] ${entry}`, 'wal', userId, 'private')
      if (walEntries.length > 0) console.log(`[cc-soul][api] WAL: ${walEntries.length} entries`)
    } catch {}

    // ── 5b. 直接事实提取（复用 L205 的 _sharedFacts，不再重跑 60+ 条正则）──
    try {
      if (_sharedFacts.length > 0) {
        const { addFacts } = await import('./fact-store.ts')
        addFacts(_sharedFacts)
      }
    } catch {}

    // ── 6. Avatar collection ──
    try { (await import('./avatar.ts')).collectAvatarData(message, '', userId) } catch {}
  }

  // ── 7. Proactive hints ──
  try {
    const { generateProactiveItems } = await import('./soul-proactive.ts')
    const hints = await generateProactiveItems()
    if (hints.length > 0) {
      const { addWorkingMemory } = await import('./memory.ts')
      addWorkingMemory(`[自动洞察]\n${hints.map(h => h.message).join('\n')}`, userId)
    }
  } catch {}

  // ── 7b. Duplicate message detection (in-memory cache) ──
  let dupHint = ''
  try {
    cleanDedup()
    const dedupKey = message.slice(0, 100).toLowerCase().trim()
    const prev = _dedupCache.get(dedupKey)
    if (prev && Date.now() - prev.ts < DEDUP_TTL) {
      const replyHint = prev.reply ? `上次的回复摘要："${prev.reply.slice(0, 100)}"。` : ''
      dupHint = `[重要] 用户发了和之前一样的消息："${message.slice(0, 50)}"。${replyHint}不要重复上次的回答，换个角度或说"这个刚说过，还有什么不清楚的？"。`
    }
    // Only write if no existing entry (don't overwrite reply from feedback)
    if (!_dedupCache.has(dedupKey)) {
      _dedupCache.set(dedupKey, { reply: '', ts: Date.now() })
    } else {
      _dedupCache.get(dedupKey)!.ts = Date.now()  // update timestamp but preserve reply
    }
  } catch {}

  // ── 8. Build augments ──
  // 注：激活场召回已内置于 recall()，buildAndSelectAugments 会自动调用，无需在此单独调用
  let selected: string[] = []
  let augmentObjects: any[] = []
  let recalled: any[] = []
  try {
    const { buildAndSelectAugments } = await import('./handler-augments.ts')
    const { getSessionState } = await import('./handler-state.ts')
    const session = getSessionState(userId)
    session.lastPrompt = message
    session.lastSenderId = userId

    // CGAF: 生成 cogHints 供 recall 链路使用
    let _cogHints: any = null
    try { _cogHints = (await import('./cognition.ts')).toCogHints(message) } catch {}

    const result = await buildAndSelectAugments({
      userMsg: message, session, senderId: userId, channelId: '',
      cog: cogResult || { attention: 'general', intent: 'wants_answer', strategy: 'balanced', complexity: 0.3, hints: [] },
      cogHints: _cogHints,
      flow: flow || { turnCount: 0, frustration: 0 },
      flowKey: userId, followUpHints: [], workingMemKey: userId,
    })
    selected = result.selected || []
    // 注入重复消息检测提醒
    if (dupHint) selected.unshift(`[重复消息检测] ${dupHint}`)
    augmentObjects = (result.augments || []).map((a: any) => ({
      content: a.content || '', priority: a.priority || 0, tokens: a.tokens || 0,
    }))
    recalled = (result.augments || [])
      .filter((a: any) => a.content?.includes('记忆') || a.content?.includes('recall'))
      .map((a: any) => ({ content: a.content, scope: 'recalled' }))
  } catch (e: any) {
    console.log(`[cc-soul][api] augment build error: ${e.message}`)
  }

  // ── 9. Soul prompt ──
  let soulPrompt = ''
  try {
    const { buildSoulPrompt } = await import('./prompt-builder.ts')
    const { stats } = await import('./handler-state.ts')
    soulPrompt = buildSoulPrompt(stats.totalMessages, stats.corrections, stats.firstSeen, [])
  } catch {}

  // 重复消息提醒已由内存版 _dedupCache (L266-281) 处理，磁盘版 recent_replies.json 已移除

  // ── System prompt 分段缓存（学自 Claude Code static/dynamic split）──
  // static_prompt: 身份/价值观/规则（跨会话不变，API 可缓存）
  // dynamic_prompt: 记忆/情绪/augment/去重提醒（每次变化）
  // 支持 prompt caching 的 API 可以只对 static 部分计费 0.1×
  const staticPrompt = soulPrompt  // buildSoulPrompt 输出的核心身份
  const dynamicPrompt = selected.join('\n\n')  // augments 是动态的

  return {
    system_prompt: customPrompt ? customPrompt + '\n\n' + staticPrompt : staticPrompt,
    // 新增：分段输出，让调用方可以分别处理 static/dynamic
    static_prompt: staticPrompt,
    dynamic_prompt: dynamicPrompt,
    augments: dynamicPrompt,
    augments_array: augmentObjects,
    memories: recalled.map((m: any) => ({ content: m.content, scope: m.scope, emotion: m.emotion })),
    mood: moodScore,
    energy: energyScore,
    emotion,
    cognition: cogResult ? {
      attention: cogResult.attention, intent: cogResult.intent,
      strategy: cogResult.strategy, complexity: cogResult.complexity,
    } : null,
  }
}

async function handleFeedback(body: any): Promise<any> {
  const userMessage = body.user_message || ''
  const aiReply = body.ai_reply || ''
  const userId = body.user_id || body.userId || 'default'
  const agentId = body.agent_id || body.agentId || 'default'
  const satisfaction = body.satisfaction || ''

  // Multi-agent isolation
  if (agentId !== 'default') {
    try { const { setActiveAgent } = await import('./persistence.ts'); setActiveAgent(agentId) } catch {}
  }

  if (!userMessage || !aiReply) return { error: 'user_message and ai_reply required' }

  // Privacy mode: skip all learning/memory operations
  try {
    const { getPrivacyMode } = await import('./handler-state.ts')
    if (getPrivacyMode()) return { learned: false, reason: 'privacy_mode' }
  } catch {}

  // Update dedup cache with actual reply content (in-memory)
  try {
    const dedupKey = userMessage.slice(0, 100).toLowerCase().trim()
    _dedupCache.set(dedupKey, { reply: aiReply.slice(0, 200), ts: Date.now() })
    cleanDedup()
  } catch {}

  // History
  try { (await import('./memory.ts')).addToHistory(userMessage, aiReply) } catch {}

  // Avatar
  try { (await import('./avatar.ts')).collectAvatarData(userMessage, aiReply, userId) } catch {}

  // Quality
  let qualityScore = -1
  try {
    const { scoreResponse, trackQuality } = await import('./quality.ts')
    qualityScore = scoreResponse(userMessage, aiReply)
    trackQuality(qualityScore)
    const { getSessionState, getLastActiveSessionKey } = await import('./handler-state.ts')
    const sess = getSessionState(getLastActiveSessionKey())
    if (sess) sess.lastQualityScore = qualityScore
  } catch {}

  // Body feedback
  try {
    const { bodyOnPositiveFeedback, bodyOnCorrection } = await import('./body.ts')
    if (satisfaction === 'positive') {
      bodyOnPositiveFeedback()
      // P2b: 正面反馈 → 提升最近被注入记忆的 Bayes 可信度
      try {
        const { confirmTruthfulness } = await import('./smart-forget.ts')
        const { memoryState } = await import('./memory.ts')
        const recentInjected = memoryState.memories.filter((m: any) =>
          m && (m.injectionEngagement ?? 0) > 0 && Date.now() - (m.lastAccessed || 0) < 600000
        ).slice(0, 3)
        for (const m of recentInjected) {
          confirmTruthfulness(m, `用户正面反馈(satisfaction=positive)`)
        }
      } catch {}
    }
    if (satisfaction === 'negative') bodyOnCorrection()
  } catch {}

  // Gratitude
  try { (await import('./user-profiles.ts')).trackGratitude(userMessage, aiReply, userId) } catch {}

  // Raw persistence (sync, never lost)
  try {
    const { addMemory } = await import('./memory.ts')
    addMemory(`[对话] 用户: ${userMessage.slice(0, 60)} → AI: ${aiReply.slice(0, 60)}`, 'fact', userId, 'private')
    // 用原始用户消息单独做 fact 提取（对话对格式会污染正则匹配）
    const { autoExtractFromMemory } = await import('./fact-store.ts')
    autoExtractFromMemory(userMessage, 'fact', 'user_said')
  } catch {}

  // 活画像微更新
  try {
    const { updateLivingProfile } = await import('./person-model.ts')
    // importance 从消息内容关键词判断
    const importance = /名字|叫我|工作|公司|住|女儿|儿子|老婆|喜欢|讨厌|每天|习惯/.test(userMessage) ? 8 : 5
    updateLivingProfile(userMessage, 'fact', importance)
  } catch {}

  // LLM deep analysis (async, with timeout)
  try {
    const { runPostResponseAnalysis } = await import('./cli.ts')
    const { addMemoryWithEmotion } = await import('./memory.ts')
    const { addEntitiesFromAnalysis } = await import('./graph.ts')

    const analysisPromise = new Promise<void>((resolve) => {
      const timeout = setTimeout(() => { console.log(`[cc-soul][api] feedback analysis timed out`); resolve() }, 20000)
      runPostResponseAnalysis(userMessage, aiReply, (result: any) => {
        clearTimeout(timeout)
        try {
          for (const m of (result.memories || [])) {
            // 防 LLM 幻觉：检查 Tier 2 提取的记忆是否在用户实际消息中有依据
            // 如果记忆内容的关键词在用户消息中完全找不到 → 可能是幻觉
            const memKeywords = (m.content.match(/[\u4e00-\u9fff]{2,}|[a-zA-Z]{3,}/gi) || []).map((w: string) => w.toLowerCase())
            const msgKeywords = new Set((userMessage.match(/[\u4e00-\u9fff]{2,}|[a-zA-Z]{3,}/gi) || []).map((w: string) => w.toLowerCase()))
            const grounded = memKeywords.filter((w: string) => msgKeywords.has(w)).length
            if (memKeywords.length > 0 && grounded === 0 && m.scope === 'fact') {
              console.log(`[cc-soul][anti-hallucination] SKIP ungrounded fact: ${m.content.slice(0, 50)}`)
              continue  // 跳过无依据的 fact
            }
            addMemoryWithEmotion(m.content, m.scope, userId, m.visibility, '', result.emotion, true)
          }
          if (result.entities) addEntitiesFromAnalysis(result.entities)
          if (result.memoryOps?.length > 0) {
            import('./memory.ts').then(({ executeMemoryCommands }) => {
              executeMemoryCommands(result.memoryOps.slice(0, 3), userId, '')
            }).catch((e: any) => { console.error(`[cc-soul] module load failed (memory): ${e.message}`) })
          }

          // ── Tier 2 → Tier 1 反馈环：LLM 发现的结构喂给动态引擎学习 ──
          try {
            const { dynamicExtract, updateStructureStrength } = require('./dynamic-extractor.ts')
            for (const m of (result.memories || [])) {
              // LLM 提取的记忆内容 → 尝试用动态引擎也提取一遍
              const tier1Results = dynamicExtract(m.content, userId)
              if (tier1Results.length > 0) {
                // Tier 1 也能提取 → 强化该结构词（确认有效）
                for (const r of tier1Results) updateStructureStrength(r.structureWord, userId, true)
              } else {
                // Tier 1 提取不到但 Tier 2 提取到了 → 潜在的新结构词
                // 从 LLM 的记忆内容中提取 2-3 字短语，记录为候选结构词
                const cjkPhrases = m.content.match(/[\u4e00-\u9fff]{2,3}/g) || []
                for (const phrase of cjkPhrases.slice(0, 3)) {
                  // 记录到 AAM：这个短语出现在有效的事实提取语境中
                  try {
                    const aamMod = require('./aam.ts')
                    const bodyMod = require('./body.ts')
                    aamMod.learnAssociation?.(`${phrase} ${m.scope}`, Math.abs(bodyMod?.body?.mood ?? 0))
                  } catch {}
                }
              }
            }
          } catch {}

          console.log(`[cc-soul][api] feedback: ${(result.memories||[]).length} memories`)
        } catch {}
        resolve()
      })
    })
    analysisPromise.catch(() => {}) // intentionally silent — background analysis
  } catch (e: any) {
    console.log(`[cc-soul][api] feedback error: ${e.message}`)
  }

  // ── Activation field Hebbian feedback ──
  try {
    const { hebbianUpdate } = await import('./aam.ts')
    const { decayAllActivations } = await import('./activation-field.ts')
    // 每次 feedback 触发一次小衰减
    decayAllActivations(0.995)
    // quality 高 → 强化刚才用到的 key weights；quality 低 → 削弱
    if (qualityScore > 6) {
      hebbianUpdate({ lexical: 0.5, temporal: 0.3, emotional: 0.3, entity: 0.3, behavioral: 0.2, factual: 0.4, causal: 0.2, sequence: 0.2 }, true)
    } else if (qualityScore >= 0 && qualityScore < 4) {
      hebbianUpdate({ lexical: 0.5, temporal: 0.3, emotional: 0.3, entity: 0.3, behavioral: 0.2, factual: 0.4, causal: 0.2, sequence: 0.2 }, false)
    }
  } catch {}

  // ── 蒸馏反馈闭环：根据质量反馈 topic node 置信度 ──
  try {
    const { feedbackDistillQuality, feedbackMemoryEngagement } = await import('./handler-augments.ts')
    if (qualityScore >= 0) feedbackDistillQuality(qualityScore)
    // P1a: 记忆级 engagement 反馈
    feedbackMemoryEngagement(userMessage, userId)
    // PAM 时序共现：喂用户原话（双语），而不是 LLM 碎片
    try {
      const aamMod = await import('./aam.ts')
      aamMod.learnTemporalLink?.(userMessage)
    } catch {}
  } catch {}

  // ── 主动记忆重构（Letta 启发，零 LLM）：从 AI 回复中检测修正信号 ──
  try {
    // 使用轮次快照检测并发修改
    const isMemoryStale = (mem: any): boolean => {
      if (!turnSnapshot || !mem.memoryId) return false
      const snapLen = turnSnapshot.get(mem.memoryId)
      return snapLen !== undefined && (mem.lineage?.length ?? 0) !== snapLen
    }

    const UPDATE_SIGNALS = [
      /(?:之前|以前).*?(?:现在|目前|最近)/,     // "之前X现在Y" → 事实变化
      /(?:不过|但是).*?(?:看来|似乎|好像)/,      // "不过看来X" → 修正
      /(?:原来|其实).*?(?:是|应该是)/,            // "原来是X" → 纠正
    ]
    const { memoryState } = await import('./memory.ts')
    const { penalizeTruthfulness } = await import('./smart-forget.ts')
    const { findMentionedEntities } = await import('./graph.ts')

    // 获取本轮注入的记忆
    const { getLastAugmentSnapshot } = await import('./metacognition.ts')
    const injected = getLastAugmentSnapshot()

    for (const signal of UPDATE_SIGNALS) {
      if (!signal.test(aiReply)) continue
      // AI 回复中有修正信号 → 检查是否引用了某条注入记忆的实体
      for (const augContent of injected) {
        const memEntities = findMentionedEntities(augContent)
        const replyMentionsEntity = memEntities.some((e: string) => aiReply.includes(e))
        if (replyMentionsEntity) {
          // 找到对应的 Memory 对象
          const mem = memoryState.memories.find((m: any) =>
            m && m.content && augContent.includes(m.content.slice(0, 30))
          )
          if (mem) {
            if (isMemoryStale(mem)) continue
            const penalizeKey = mem.memoryId || (mem.content||'').slice(0, 30)
            const lastTs = _lastPenalizeTs.get(penalizeKey) ?? 0
            if (Date.now() - lastTs < 5000) continue  // 5秒内对同一记忆跳过
            _lastPenalizeTs.set(penalizeKey, Date.now())
            // 防内存泄漏：超过 100 条时清理最旧的
            if (_lastPenalizeTs.size > 100) {
              let oldest = Infinity, oldestKey = ''
              for (const [k, v] of _lastPenalizeTs) { if (v < oldest) { oldest = v; oldestKey = k } }
              if (oldestKey) _lastPenalizeTs.delete(oldestKey)
            }
            penalizeTruthfulness(mem, 'AI 回复暗示修正')
            try { const { logDecision } = require('./decision-log.ts'); logDecision('active_reconstruct', (mem.content||'').slice(0,30), `AI回复含修正信号`) } catch {}
          }
          break
        }
      }
      break  // 每轮最多检测一次
    }
  } catch {}

  // P5h: engagement 信号驱动质量权重学习
  try {
    const { updateQualityFromEngagement } = await import('./quality.ts')
    // 用 qualityScore 归一化到 0-1 作为 engagement 代理
    if (qualityScore >= 0) {
      updateQualityFromEngagement(userMessage, aiReply, qualityScore / 10)
    }
  } catch {}

  // Record observation for behavior engine learning
  try {
    const { recordObservation } = await import('./behavioral-phase-space.ts')
    const { getSessionState, getLastActiveSessionKey } = await import('./handler-state.ts')
    const { body: bodyState } = await import('./body.ts')
    const sess = getSessionState(getLastActiveSessionKey())
    const reaction = satisfaction === 'positive' ? 'satisfied' as const
      : satisfaction === 'negative' ? 'corrected' as const
      : 'neutral' as const
    recordObservation(userMessage, bodyState.mood, sess, reaction, 'balanced')
  } catch {}

  return { learned: true }
}
