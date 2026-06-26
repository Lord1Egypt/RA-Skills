/**
 * ╔═══════════════════════════════════════════════════════════════╗
 * ║  ⚠️  DEPRECATED — 请勿在新代码中引用此文件                     ║
 * ║  核心逻辑已拆分至:                                             ║
 * ║    handler-state.ts / handler-heartbeat.ts / handler-commands.ts ║
 * ║    handler-augments.ts / soul-process.ts / context-engine.ts    ║
 * ║  仅保留 initializeSoul() + handler() 供 soul-process.ts 调用    ║
 * ║  新功能一律加到对应子模块，不要改这个文件                        ║
 * ╚═══════════════════════════════════════════════════════════════╝
 *
 * cc-soul — OpenClaw HookHandler (Modular Orchestrator)
 *
 * Slim entry point that wires all modules together.
 * Split into:
 *   handler-state.ts     — global state, metrics, stats, session
 *   handler-heartbeat.ts — autonomous heartbeat loop
 *   handler-commands.ts  — command routing (40+ commands)
 *   handler-augments.ts  — augment building & selection
 *   handler.ts (this)    — init, bootstrap, preprocessed, sent, command, default export
 *
 * Events:
 * - agent:bootstrap      → inject full soul prompt
 * - message:preprocessed → cognition + memory recall + body tick
 * - message:sent         → record response + trigger async CLI ops
 * - command:new          → persist state, log stats
 */

import { existsSync, readFileSync, writeFileSync, readdirSync, mkdirSync } from 'fs'
import { execFile } from 'child_process'
import { platform, homedir } from 'os'
import { resolve } from 'path'

import type { Augment } from './types.ts'
import {
  metrics, stats, loadStats, saveStats,
  metricsRecordResponseTime,
  getSessionState, setLastActiveSessionKey, getLastActiveSessionKey,
  getPrivacyMode, setPrivacyMode,
  getReadAloudPending, setReadAloudPending,
  getHeartbeatInterval, setHeartbeatInterval,
  CJK_TOPIC_REGEX, CJK_WORD_REGEX,
  refreshNarrativeAsync,
  detectTopicShiftAndReset,
} from './handler-state.ts'
import { runHeartbeat } from './handler-heartbeat.ts'
import { routeCommand } from './handler-commands.ts'
import { buildAndSelectAugments, detectInjection, generatePrebuiltTips } from './handler-augments.ts'
import { brain } from './brain.ts'

import {
  ensureDataDir, loadJson, saveJson, debouncedSave, flushAll,
  MEMORIES_PATH, RULES_PATH, STATS_PATH, DATA_DIR, REMINDERS_PATH,
} from './persistence.ts'
import { spawnCLI, runPostResponseAnalysis, loadAIConfig, getActiveTaskStatus, getAgentBusy, setAgentBusy, setOnTaskDone, killGatewayClaude } from './cli.ts'
import { notifySoulActivity, notifyOwnerDM } from './notify.ts'
import { body, bodyTick, bodyOnMessage, bodyOnCorrection, bodyOnPositiveFeedback, bodyGetParams, processEmotionalContagion, getEmotionContext, loadBodyState, loadMoodHistory, getEmotionalArcContext, getEmotionSummary, emotionVector, generateMoodReport, trackEmotionAnchor } from './body.ts'
import {
  memoryState, loadMemories, addMemory, addMemoryWithEmotion,
  recall, getCachedFusedRecall, invalidateIDF, addToHistory, buildHistoryContext,
  batchTagUntaggedMemories, consolidateMemories,
  recallFeedbackLoop, triggerSessionSummary,
  triggerAssociativeRecall, getAssociativeRecall,
  parseMemoryCommands, executeMemoryCommands, getPendingSearchResults,
  scanForContradictions,
  predictiveRecall, generatePrediction,

  loadCoreMemories, buildCoreMemoryContext, autoPromoteToCoreMemory,
  loadEpisodes, buildEpisodeContext, recordEpisode,
  addWorkingMemory, buildWorkingMemoryContext, cleanupWorkingMemory,
  getMemoriesByScope, processMemoryDecay,
  sqliteMaintenance, getStorageStatus, saveMemories,
  auditMemoryHealth, trackRecallImpact,
} from './memory.ts'
import { ensureSQLiteReady } from './memory.ts'
import { graphState, loadGraph, addEntitiesFromAnalysis, queryEntityContext, generateEntitySummary, findMentionedEntities } from './graph.ts'
import { cogProcess, predictIntent, detectAtmosphere } from './cognition.ts'
import {
  rules, hypotheses, loadRules, loadHypotheses,
  getRelevantRules, onCorrectionAdvanced, verifyHypothesis,
  attributeCorrection,
  recordRuleQuality,
} from './evolution.ts'
import {
  evalMetrics, scoreResponse, selfCheckSync, selfCheckWithCLI,
  trackQuality, computeEval, getEvalSummary,
  loadQualityWeights, updateQualityWeights, resampleHardExamples,
} from './quality.ts'
import {
  innerState, loadInnerLife,
  writeJournalWithCLI, triggerDeepReflection,
  getRecentJournal,
  reflectOnLastResponse, extractFollowUp, peekPendingFollowUps,
  checkActivePlans, cleanupPlans,
} from './inner-life.ts'
// ── Optional modules: loaded dynamically, gracefully absent in public build ──
let trackPersonaStyle: (...args: any[]) => void = () => {}
let getPersonaDriftWarning: () => string | null = () => null
let checkPersonaDrift: (replyText: string, personaId: string, personaName: string, personaTone: string, idealVector?: any) => number = () => 0
let getPersonaDriftReinforcement: () => string | null = () => null
let getDriftCount: () => number = () => 0
let smartForgetSweep: (...args: any[]) => any = () => ({ toForget: [], toConsolidate: [] })
// cron-agent.ts removed — no users were using scheduled tasks
let compressAugments: (...args: any[]) => any[] = (a: any[]) => a
let buildDebateAugment: (...args: any[]) => any = () => null
let updateBeliefFromMessage: (...args: any[]) => void = () => {}
let getToMContext: () => string = () => ''
let detectMisconception: (...args: any[]) => string | null = () => null

let recordTurnUsage: (inputText: string, outputText: string, augmentTokenCount: number) => void = () => {}
import('./cost-tracker.ts').then(m => { recordTurnUsage = m.recordTurnUsage }).catch((e: any) => { console.error(`[cc-soul] module load failed (cost-tracker): ${e.message}`) })
import('./persona-drift.ts').then(m => { trackPersonaStyle = m.trackPersonaStyle; getPersonaDriftWarning = m.getPersonaDriftWarning; checkPersonaDrift = m.checkPersonaDrift; getPersonaDriftReinforcement = m.getPersonaDriftReinforcement; getDriftCount = m.getDriftCount }).catch((e: any) => { console.error(`[cc-soul] module load failed (persona-drift): ${e.message}`) })
import('./smart-forget.ts').then(m => { smartForgetSweep = m.smartForgetSweep }).catch((e: any) => { console.error(`[cc-soul] module load failed (smart-forget): ${e.message}`) })
// cron-agent import removed
import('./context-compress.ts').then(m => { compressAugments = m.compressAugments }).catch((e: any) => { console.error(`[cc-soul] module load failed (context-compress): ${e.message}`) })
// debate.ts removed — multi-persona debate was too expensive (5x token per question)
import('./person-model.ts').then(m => { updateBeliefFromMessage = m.updateBeliefFromMessage; getToMContext = m.getToMContext; detectMisconception = m.detectMisconception }).catch((e: any) => { console.error(`[cc-soul] module load failed (person-model/tom): ${e.message}`) })
// ── End optional modules ──

// audit.ts removed — hash-chain audit log retired
import { buildSoulPrompt, selectAugments, estimateTokens, setNarrativeCache, narrativeCache, checkNarrativeCacheTTL } from './prompt-builder.ts'
import {
  taskState, initTasks, detectAndDelegateTask, checkTaskConfirmation,
  trackRequestPattern, detectSkillOpportunity, autoCreateSkill, getActivePlanHint,
  detectWorkflowTrigger, executeWorkflow, detectWorkflowOpportunity,
  findSkills, autoExtractSkill,
  startAutonomousGoal, getActiveGoalHint, detectGoalIntent,
} from './tasks.ts'
import { loadProfiles, updateProfileOnMessage, updateProfileOnCorrection, getProfileContext, getRhythmContext, getProfile, getProfileTier, updateRelationship, getRelationshipContext, trackGratitude, trackPersonaUsage } from './user-profiles.ts'
import { loadEpistemic, trackDomainQuality, trackDomainCorrection, getDomainConfidence, getCapabilityScore } from './epistemic.ts'
import { updateFlow, getFlowHints, getFlowContext, checkAllSessionEnds, generateSessionSummary, setOnSessionResolved } from './flow.ts'
import { loadValues, detectValueSignals, getValueContext, getAllValues } from './values.ts'
import { loadLorebook, queryLorebook, autoPopulateFromMemories } from './lorebook.ts'
import { prepareContext } from './context-prep.ts'
// patterns.ts removed — success pattern tracking retired
import { selectPersona, getActivePersona, getPersonaOverlay, getBlendedPersonaOverlay, getPersonaMemoryBias, loadUserStyles, updateUserStylePreference, PERSONAS } from './persona.ts'
import { checkAugmentConsistency, snapshotAugments, loadMetacognition, learnConflict, recordInteraction } from './metacognition.ts'
// meta-feedback.ts removed — augment outcome tracking retired
// fingerprint.ts removed — style fingerprint retired
import { loadFeatures, isEnabled, handleFeatureCommand } from './features.ts'
import { processIngestion, ingestFile } from './rag.ts'
// user-dashboard.ts 已删除
const handleDashboardCommand = () => '该功能已停用'
const generateMemoryMapHTML = () => ''
const generateDashboardHTML = () => ''
import { autoImportHistory } from './history-import.ts'
import { collectAvatarData } from './avatar.ts'
import { loadDistillState } from './distill.ts'
import { loadAbsenceState } from './absence-detection.ts'
import { healthCheck, recordModuleError, recordModuleActivity, postReplyCleanup } from './health.ts'
import { checkAutoTune, handleTuneCommand, getParam, updateBanditReward } from './auto-tune.ts'
import { loadEvolutions, checkEvolutionProgress, getEvolutionSummary } from './evolution.ts'
import { isContextEngineActive, isContextEngineRegistered, setLastAugments } from './context-engine.ts'

let agentBusyTimer: ReturnType<typeof setTimeout> | null = null


// ═══════════════════════════════════════════════════════════════════════════════
// INITIALIZATION
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Initialize all cc-soul subsystems. Safe to call multiple times (idempotent).
 */
// initializeSoul 已迁移到 init.ts — 这里做 re-export 保持向后兼容
export { initializeSoul, getInitialized, setInitialized } from './init.ts'

// ═══════════════════════════════════════════════════════════════════════════════
// EXPORTED EVENT HANDLERS
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * agent:bootstrap — inject full soul prompt into bootstrap files.
 */
export function handleBootstrap(event: any): void {
  if (!getInitialized()) initializeSoul()

  const ctx = event.context || {}
  const files = ctx.bootstrapFiles as any[]
  if (files) {
    const soulPrompt = buildSoulPrompt(
      stats.totalMessages, stats.corrections, stats.firstSeen,
      taskState.workflows,
    )
    files.push({ path: 'CC_SOUL.md', content: soulPrompt })
    console.log(`[cc-soul] bootstrap: injected soul (e=${body.energy.toFixed(2)}, m=${body.mood.toFixed(2)}, prompt=${soulPrompt.length} chars, ~${Math.round(soulPrompt.length * 0.4)} tokens)`)
  }
}

/**
 * message:preprocessed — cognition + memory recall + augment building + body tick.
 */
// ── Dedup guard: prevent duplicate processing when hook is registered multiple times ──
let _lastPreprocessedId = ''
let _lastPreprocessedTs = 0

// ── 近期回复去重：如果用户发了和之前一样的消息，提示 LLM 不要重复回答 ──
// 使用文件持久化（插件进程可能重启，内存Map会丢失）
const _RECENT_REPLIES_PATH = resolve(DATA_DIR, 'recent_replies.json')
let _recentRepliesObj: Record<string, { reply: string; ts: number }> = loadJson(_RECENT_REPLIES_PATH, {})
// 启动时清理过期条目
for (const [k, v] of Object.entries(_recentRepliesObj)) {
  if (Date.now() - v.ts > 3600000) delete _recentRepliesObj[k]
}
const _recentReplies = {
  get(key: string) { return _recentRepliesObj[key] },
  set(key: string, val: { reply: string; ts: number }) { _recentRepliesObj[key] = val; debouncedSave(_RECENT_REPLIES_PATH, _recentRepliesObj) },
  delete(key: string) { delete _recentRepliesObj[key] },
  [Symbol.iterator]: function* () { for (const [k, v] of Object.entries(_recentRepliesObj)) yield [k, v] as [string, { reply: string; ts: number }] },
}

export async function handlePreprocessed(event: any): Promise<void> {
  if (!getInitialized()) initializeSoul()

  // Dedup: skip if this exact event was already processed (within 5s window)
  const eventId = event?.context?.messageId || event?.messageId || ''
  const now = Date.now()
  if (eventId && eventId === _lastPreprocessedId && now - _lastPreprocessedTs < 5000) {
    return // already processed this message
  }
  if (eventId) {
    _lastPreprocessedId = eventId
    _lastPreprocessedTs = now
  }

  // ── Early exit: skip augment/system content re-routed to preprocessed ──
  // Must happen BEFORE setAgentBusy to avoid blocking the agent pipeline
  {
    const ctx0 = event.context || {}
    const raw0 = (ctx0.body || '') as string  // 用原始 body，不用 bodyForAgent（可能包含上次注入的 augment）
    const msg0 = raw0.replace(/^\[message_id:\s*\S+\]\s*/i, '').replace(/^[a-zA-Z0-9_\u4e00-\u9fff]{1,20}:\s*/, '').trim()
    if (!msg0) return
    if (/^[\[(（]?(对话历史|当前面向|认知|相关记忆|Working Memory|内部矛盾|隐私模式|Goal|Intent|用户档案|情绪|举一反三|回答完主问题)/i.test(msg0)) {
      console.log(`[cc-soul][preprocessed] skipped system augment content: ${msg0.slice(0, 40)}...`)
      return // don't touch agentBusy, don't kill agent
    }
  }

  // Kill gateway Claude so cc-soul can inject augments into bodyForAgent
  // before OpenClaw restarts the agent with the modified message
  killGatewayClaude()
  setAgentBusy(true)
  if (agentBusyTimer) clearTimeout(agentBusyTimer)
  agentBusyTimer = setTimeout(() => {
    agentBusyTimer = null
    setAgentBusy(false)
    console.log('[cc-soul] agentBusy auto-released (60s safety timeout)')
  }, 60000)

  const ctx = event.context || {}
  const rawMsg = (ctx.bodyForAgent || ctx.body || '') as string
  const userMsg = rawMsg
    .replace(/^\[message_id:\s*\S+\]\s*/i, '')
    .replace(/^[a-zA-Z0-9_\u4e00-\u9fff]{1,20}:\s*/, '')
    .trim()
  if (!userMsg) { setAgentBusy(false); return }

  // Dedup fallback: if no messageId, dedup by content + timestamp (within 3s)
  if (!eventId) {
    const contentKey = userMsg.slice(0, 50)
    if (contentKey === _lastPreprocessedId && now - _lastPreprocessedTs < 3000) {
      return
    }
    _lastPreprocessedId = contentKey
    _lastPreprocessedTs = now
  }

  // #14 语音朗读检测
  setReadAloudPending(userMsg.startsWith('朗读') || userMsg.toLowerCase().startsWith('read aloud'))

  const _metricsStart = Date.now()

  bodyTick()
  recordModuleActivity('memory')
  recordModuleActivity('cognition')
  recordModuleActivity('prompt-builder')

  const senderId = (ctx.senderId || '') as string
  const channelId = (ctx.conversationId || event.sessionKey || '') as string
  updateProfileOnMessage(senderId, userMsg)

  const sessionKey = event.sessionKey || channelId || senderId || '_default'
  const session = getSessionState(sessionKey)
  setLastActiveSessionKey(sessionKey)

  // Extract last assistant response from event.messages (moved after session init)
  if (session.lastPrompt && !session.lastResponseContent && Array.isArray(event.messages)) {
    for (let i = event.messages.length - 1; i >= 0; i--) {
      const msg = event.messages[i]
      if (msg?.role === 'assistant' && typeof msg?.content === 'string' && msg.content.length > 5) {
        session.lastResponseContent = msg.content
        console.log(`[cc-soul][sync] recovered lastResponse (${msg.content.length} chars)`)
        break
      }
    }
  }

  // ── Topic-shift detection: reset CLI session when topic changes ──
  const topicShifted = detectTopicShiftAndReset(session, userMsg, sessionKey)
  if (topicShifted) {
    console.log(`[cc-soul][topic-shift] detected for ${sessionKey}, CLI session cleared`)

    // ── Feature 3: 话题自动保存 — topic shift 时自动保存上一个话题到 branches/ ──
    {
      try {
        const branchDir = resolve(DATA_DIR, 'branches')
        if (!existsSync(branchDir)) mkdirSync(branchDir, { recursive: true })
        const recentMsgs = memoryState.chatHistory.slice(-10)
        if (recentMsgs.length >= 2) {
          const topicWordList = recentMsgs.flatMap(h => (h.user || '').match(/[\u4e00-\u9fff]{2,4}|[A-Za-z]{3,}/g) || [])
          const freq = new Map<string, number>()
          for (const w of topicWordList) { const k = w.toLowerCase(); freq.set(k, (freq.get(k) || 0) + 1) }
          const topicLabel = [...freq.entries()].sort((a, b) => b[1] - a[1])[0]?.[0] || `topic_${Date.now()}`
          const branchData = {
            topic: topicLabel,
            savedAt: Date.now(),
            autoSaved: true,
            chatHistory: recentMsgs,
            persona: getActivePersona()?.id || 'default',
          }
          const branchPath = resolve(branchDir, `${topicLabel}.json`)
          saveJson(branchPath, branchData)
          console.log(`[cc-soul][auto-topic-save] saved topic「${topicLabel}」(${recentMsgs.length} turns) → ${branchPath}`)
        }
      } catch (e: any) {
        console.log(`[cc-soul][auto-topic-save] failed: ${e.message}`)
      }
    }

    // ── Episodic memory: record completed episode on topic shift ──
    {
      try {
        const recentHistory = memoryState.chatHistory.slice(-10)
        if (recentHistory.length >= 2) {
          const turns = recentHistory.map(h => [
            { role: 'user' as const, content: h.user },
            { role: 'assistant' as const, content: h.bot },
          ]).flat()
          // Extract topic label from recent messages
          const topicWords = recentHistory.flatMap(h => (h.user || '').match(/[\u4e00-\u9fff]{2,4}|[A-Za-z]{3,}/g) || [])
          const freq = new Map<string, number>()
          for (const w of topicWords) { const k = w.toLowerCase(); freq.set(k, (freq.get(k) || 0) + 1) }
          const topicLabel = [...freq.entries()].sort((a, b) => b[1] - a[1]).slice(0, 3).map(e => e[0]).join(' ') || 'general'
          // Check if there was a correction in this episode
          const hadCorrection = recentHistory.some(h => /不对|错了|不是这样|纠正|其实/.test(h.user))
          const correction = hadCorrection ? { what: '上一轮对话中被纠正', cause: '需要从 episode 中学习' } : undefined
          recordEpisode(topicLabel, turns, correction, 'resolved', 0)
        }
      } catch (e: any) {
        console.log(`[cc-soul][episodic] record failed: ${e.message}`)
      }
    }
  }

  // ── Previous turn analysis & learning loop ──
  let prevScore = -1
  if (session.lastPrompt && session.lastResponseContent && session.lastResponseContent.length > 5) {
    addToHistory(session.lastPrompt, session.lastResponseContent)
  }
  if (session.lastPrompt && session.lastResponseContent && session.lastResponseContent.length > 20) {
    prevScore = scoreResponse(session.lastPrompt, session.lastResponseContent)
    trackQuality(prevScore)
    trackDomainQuality(session.lastPrompt, prevScore)

    const prevIssue = selfCheckSync(session.lastPrompt, session.lastResponseContent)
    if (prevIssue) {
      console.log(`[cc-soul][quality] ${prevIssue} | ctx: ${session.lastPrompt.slice(0, 80)}`)
      body.anomaly = Math.min(1.0, body.anomaly + 0.1)
    }

    verifyHypothesis(session.lastPrompt, true)
    extractFollowUp(session.lastPrompt)
    trackRequestPattern(session.lastPrompt)
    detectAndDelegateTask(session.lastPrompt, session.lastResponseContent, event)

    // ── New module hooks: run on previous turn's data (since message:sent is unreliable) ──
    try { trackPersonaStyle(session.lastResponseContent, getActivePersona()?.id ?? 'default') } catch (_) {}
    try { updateBeliefFromMessage(session.lastPrompt, session.lastResponseContent) } catch (_) {}
    try { trackUserPattern(session.lastPrompt, prevScore >= 5) } catch (_) {}
    try { trackRecallImpact(session.lastRecalledContents, prevScore) } catch (_) {}

    if (!getPrivacyMode()) {
      const snapPrompt = session.lastPrompt
      const snapResponse = session.lastResponseContent
      const snapSenderId = session.lastSenderId
      const snapChannelId = session.lastChannelId
      session._lastAnalyzedPrompt = snapPrompt
      metrics.cliCalls++
      runPostResponseAnalysis(snapPrompt, snapResponse, (result) => {
        for (const m of result.memories) {
          addMemoryWithEmotion(m.content, m.scope, snapSenderId, m.visibility, snapChannelId, result.emotion, true)
        }
        addEntitiesFromAnalysis(result.entities)
        if (result.memoryOps && result.memoryOps.length > 0) {
          for (const op of result.memoryOps) {
            if (!op.keyword || op.keyword.length < 4) continue
            if (!op.reason || op.reason.length < 3) continue
            const kw = op.keyword.toLowerCase()
            if (op.action === 'delete') {
              let deleted = 0
              for (const mem of memoryState.memories) {
                if (deleted >= 2) break
                if (mem.content.toLowerCase().includes(kw) && mem.scope !== 'expired') { mem.scope = 'expired'; deleted++ }
              }
              if (deleted > 0) console.log(`[cc-soul][memory-ops] DELETE ${deleted} (keyword: ${op.keyword})`)
            } else if (op.action === 'update' && op.newContent) {
              for (const mem of memoryState.memories) {
                if (mem.content.toLowerCase().includes(kw) && mem.scope !== 'expired') {
                  console.log(`[cc-soul][memory-ops] UPDATE: "${mem.content.slice(0, 40)}" → "${op.newContent.slice(0, 40)}"`)
                  mem.content = op.newContent; mem.ts = Date.now(); mem.tags = undefined; break
                }
              }
            }
          }
        }
        if (result.satisfaction === 'POSITIVE') { bodyOnPositiveFeedback(); stats.positiveFeedback++ }
        // Heuristic: only persist reflection when quality is actually poor (score < 5)
        // — the merged analysis returns reflection for free, but 90% are trivial "无" equivalents
        if (result.reflection && result.quality.score < 5) addMemory(`[反思] ${result.reflection}`, 'reflection', snapSenderId, 'private', snapChannelId)
        const codeBlocks = snapResponse.match(/```(\w+)?\n([\s\S]*?)```/g)
        if (codeBlocks && codeBlocks.length > 0) {
          const lang = snapResponse.match(/```(\w+)/)?.[1] || 'unknown'
          addMemory(`[代码模式] 语言:${lang} | ${snapPrompt.slice(0, 50)}`, 'code_pattern', snapSenderId)
        }
        console.log(`[cc-soul][post-analysis] sat=${result.satisfaction} q=${result.quality.score} mem=${result.memories.length} ops=${result.memoryOps?.length || 0}`)
        // ── Brain modules onSent (persona-drift, theory-of-mind) ──
        brain.fire('onSent', { userMessage: snapPrompt, botReply: snapResponse, senderId: snapSenderId, channelId: snapChannelId, quality: result.quality })
      })
    }
  }

  // cron routing removed

  // ── Command routing ──
  if (routeCommand(userMsg, ctx, session, senderId, channelId, event)) {
    return
  }

  // Soul Mode removed from handler.ts — now handled via POST /soul API endpoint in soul-api.ts

  // ── WAL Protocol: persist key info from user message BEFORE AI reply ──
  if (!getPrivacyMode()) {
    try {
      const walEntries: { content: string; type: string }[] = []

      // Preference declarations: 我喜欢/我不喜欢/我是/我住在/我的...
      const prefPatterns = [
        /我(?:比较)?喜欢(.{2,30})/g,
        /我(?:不|讨厌|很少|从不)喜欢(.{2,30})/g,
        /我是(.{2,20})/g,
        /我住在(.{2,20})/g,
        /我的(.{2,20}?)(?:是|叫|在)(.{2,20})/g,
        /(?:my |i (?:like|prefer|love|hate|am|live in) )(.{2,40})/gi,
      ]
      for (const pat of prefPatterns) {
        pat.lastIndex = 0
        let m: RegExpExecArray | null
        while ((m = pat.exec(userMsg)) !== null) {
          const extracted = m[0].trim()
          if (extracted.length >= 4 && extracted.length <= 80) {
            walEntries.push({ content: `[WAL偏好] ${extracted}`, type: 'preference' })
          }
        }
      }

      // Date/time/event facts: 明天/下周/X月X日 + 事件
      const factPatterns = [
        /(?:明天|后天|下周|下个月|今天|今晚|周[一二三四五六日天]|(?:\d{1,2}月\d{1,2}[日号])|(?:\d{4}[-/]\d{1,2}[-/]\d{1,2}))(.{2,40})/g,
        /(?:deadline|due|meeting|会议|截止|到期|出发|航班|考试|面试|约了)(.{2,30})/gi,
      ]
      for (const pat of factPatterns) {
        pat.lastIndex = 0
        let m: RegExpExecArray | null
        while ((m = pat.exec(userMsg)) !== null) {
          const extracted = m[0].trim()
          if (extracted.length >= 4 && extracted.length <= 80) {
            walEntries.push({ content: `[WAL事实] ${extracted}`, type: 'fact' })
          }
        }
      }

      // Deduplicate and write (max 3 per message to avoid spam)
      const seen = new Set<string>()
      let written = 0
      for (const entry of walEntries) {
        if (written >= 3) break
        const key = entry.content.slice(0, 40)
        if (seen.has(key)) continue
        seen.add(key)
        addMemory(entry.content, 'wal', senderId, 'private', channelId)
        written++
      }
      console.log(`[cc-soul][wal] checked: ${walEntries.length} extracted, ${written} written from "${userMsg.slice(0, 30)}"`)
    } catch (e: any) {
      console.log(`[cc-soul][wal] error: ${e.message}`)
    }
  }

  // Pending follow-ups
  const followUpHints = peekPendingFollowUps()

  // Working memory
  const workingMemKey = channelId || senderId || '_default'
  addWorkingMemory(userMsg.slice(0, 100), workingMemKey)

  // ── Cognition pipeline ──
  const cog = cogProcess(userMsg, session.lastResponseContent, session.lastPrompt, senderId)
  bodyOnMessage(cog.complexity)

  // Metacognitive feedback
  if (session.lastAugmentsUsed.length > 0 && prevScore >= 0) {
    const wasCorrected = cog.attention === 'correction'
    learnConflict(session.lastAugmentsUsed, wasCorrected)
    recordInteraction(session.lastAugmentsUsed, prevScore, wasCorrected)
  }

  const recentUserMsgs = memoryState.chatHistory.slice(-3).map(h => h.user)
  const intentHints = predictIntent(userMsg, senderId, recentUserMsgs)
  if (intentHints.length > 0) cog.hints.push(...intentHints)

  const atmosphere = detectAtmosphere(userMsg, memoryState.chatHistory.slice(-5))
  if (atmosphere.length > 0) cog.hints.push(...atmosphere)

  const flowKey = senderId ? (channelId ? channelId + ':' + senderId : senderId) : (channelId || '_default')
  const flow = updateFlow(userMsg, session.lastResponseContent, flowKey)

  processEmotionalContagion(userMsg, cog.attention, flow.frustration, senderId)

  const persona = selectPersona(cog.attention, flow.frustration, senderId, cog.intent, userMsg)
  if (persona) {
    console.log(`[cc-soul][persona] selected: ${persona.id} (${persona.name}) | trigger: ${cog.attention}/${cog.intent}`)
    if (senderId) trackPersonaUsage(senderId, persona.id)
  }

  const endedSessions = checkAllSessionEnds()
  for (const s of endedSessions) {
    generateSessionSummary(s.topic, s.turnCount, s.flowKey)
  }

  // Track correction
  if (cog.attention === 'correction') {
    stats.corrections++
    updateProfileOnCorrection(senderId)
    updateRelationship(senderId, 'correction')
    onCorrectionAdvanced(userMsg, session.lastResponseContent)
    trackDomainCorrection(userMsg)
    attributeCorrection(userMsg, session.lastResponseContent, session.lastAugmentsUsed)
    // Record correction as episodic memory for future recall
    if (session.lastResponseContent) {
      try {
        recordEpisode(
          userMsg.slice(0, 80),
          [{ role: 'assistant', content: session.lastResponseContent.slice(0, 200) }, { role: 'user', content: userMsg.slice(0, 200) }],
          { what: userMsg.slice(0, 100), cause: '用户纠正了上一轮回复' },
          'resolved',
          0.4,
          `被纠正: ${userMsg.slice(0, 80)}`
        )
      } catch (_) {}
    }
    session._pendingCorrectionVerify = true
  }

  // Hypothesis verification — runs on every non-correction message
  // (session.lastPrompt is empty in per-message contexts, so we verify here instead)
  if (cog.attention !== 'correction') {
    verifyHypothesis(userMsg, true)
  } else {
    verifyHypothesis(userMsg, false)
  }

  // Track topics
  CJK_TOPIC_REGEX.lastIndex = 0
  const topicWords = userMsg.match(CJK_TOPIC_REGEX)
  if (topicWords) {
    topicWords.slice(0, 3).forEach(w => stats.topics.add(w))
  }

  // Track emotion anchors: correlate current topics with mood
  if (topicWords && topicWords.length > 0) {
    try { trackEmotionAnchor(topicWords.slice(0, 3)) } catch (_) {}
  }

  // Update stats
  stats.totalMessages++
  if (stats.firstSeen === 0) stats.firstSeen = Date.now()
  saveStats()

  detectValueSignals(userMsg, false, senderId)

  // ── New module augments (pre-build) ──
  let _extraAugments: string[] = []
  try {
    const tomCtx = getToMContext()
    if (tomCtx) _extraAugments.push(tomCtx)
  } catch (_) {}
  try {
    const driftWarn = getPersonaDriftWarning()
    if (driftWarn) _extraAugments.push(`[人格漂移警告] ${driftWarn}`)
  } catch (_) {}
  try {
    const debateAug = buildDebateAugment(userMsg)
    if (debateAug) _extraAugments.push(debateAug.content)
  } catch (_) {}
  try {
    const skillSug = getSkillSuggestion()
    if (skillSug) _extraAugments.push(skillSug)
  } catch (_) {}
  try {
    const misconception = detectMisconception(userMsg)
    if (misconception) _extraAugments.push(`[认知偏差] ${misconception}`)
  } catch (_) {}
  // Persona drift reinforcement (from previous turn's checkPersonaDrift)
  try {
    const reinforcement = getPersonaDriftReinforcement()
    if (reinforcement) _extraAugments.push(reinforcement)
  } catch (_) {}

  // ── 重复消息检测：1小时内发过一样的消息则注入提醒 ──
  const _userMsgKey = userMsg.slice(0, 100).toLowerCase().trim()
  const _prevReply = _recentReplies.get(_userMsgKey)
  let _dupHint: string | null = null
  if (_prevReply && Date.now() - _prevReply.ts < 3600000) {
    _dupHint = `[重要] 用户刚才发了和之前一样的消息。上次的回复摘要："${_prevReply.reply.slice(0, 100)}"。不要重复上次的回答，可以说"这个刚说过"或换个角度回答。`
  }

  // ── Augment building & selection ──
  const { selected, associated } = await buildAndSelectAugments({
    userMsg, session, senderId, channelId,
    cog, flow, flowKey,
    followUpHints, workingMemKey,
  })

  // 注入重复消息提醒（高优先级，放在最前面）
  if (_dupHint) selected.unshift(`[重复消息检测] ${_dupHint}`)

  // Merge extra augments from new modules & compress
  if (_extraAugments.length > 0) selected.push(..._extraAugments)
  // Note: compressAugments expects TimedAugment[], not string[]; skip compression for extra augments

  // ── Brain modules onPreprocessed (debate, context-compress, etc.) ──
  try {
    const brainAugments = brain.firePreprocessed({ userMessage: userMsg, senderId, channelId, cog, augments: selected })
    for (const aug of brainAugments) {
      if (aug.content) selected.push(aug.content)
    }
  } catch (_) {}

  session.lastAugmentsUsed = selected
  setLastAugments(selected)
  // Log augment names for debugging
  const augNames = selected.map(s => {
    const m = s.match(/^\[([^\]]+)\]/)
    return m ? m[1] : s.slice(0, 20)
  })
  console.log(`[cc-soul][augment-inject] ${selected.length} augments: ${augNames.join(', ')}`)

  // Inject history + selected augments
  const historyCtx = buildHistoryContext()
  // Inject augments as hidden system context — must be clearly separated from user message
  // to prevent LLM from "analyzing" augments and leaking thinking process
  const cleanedSelected = selected.map(s => s.replace(/^\[([^\]]+)\]\s*/, ''))
  // Move 举一反三 augment to the end (closest to user message) for better LLM attention
  const extraThinkIdx = cleanedSelected.findIndex(s => s.includes('顺便说一下') || s.includes('举一反三'))
  let extraThinkItem: string | null = null
  if (extraThinkIdx !== -1) {
    extraThinkItem = cleanedSelected.splice(extraThinkIdx, 1)[0]
  }
  const allContext = [historyCtx, ...cleanedSelected, extraThinkItem].filter(Boolean) as string[]
  if (allContext.length > 0) {
    const suffix = '\n\n---\n'
    const postfix = '' // bodyForAgent is NOT visible to LLM — postfix is useless
    const injected = allContext.join('\n\n') + suffix + userMsg + postfix
    ctx.bodyForAgent = injected
    // Also set on event.context in case OpenClaw reads from there
    if (event.context) event.context.bodyForAgent = injected
    console.log(`[cc-soul][bodyForAgent] set ${injected.length} chars on ctx + event.context`)
  } else {
    console.log(`[cc-soul][bodyForAgent] EMPTY — no augments to inject`)
  }

  // Dynamic SOUL.md rewrite: append augments + pre-built 举一反三
  // This is the ONLY reliable path to inject content into LLM
  try {
    const workspaceDir = resolve(homedir(), '.openclaw/workspace')
    const soulPath = resolve(workspaceDir, 'SOUL.md')
    const baseSoul = buildSoulPrompt(stats.totalMessages, stats.corrections, stats.firstSeen, taskState.workflows)
    const augmentSection = cleanedSelected.length > 0
      ? '\n\n## 内部指令（仅本轮有效）\n' + cleanedSelected.join('\n')
      : ''

    // 举一反三已移除 — 被 facts 驱动的参考信息替代（handler-augments.ts）
    let tipsSection = ''

    // SOUL.md disk write removed — Context Engine mode returns prompt via assemble()
    console.log(`[cc-soul] prompt built: ${cleanedSelected.length} augments${tipsSection ? ' + 举一反三' : ''}`)
  } catch (e: any) {
    console.log(`[cc-soul] SOUL.md dynamic update failed: ${e.message}`)
  }

  triggerDeepReflection(stats)

  // ── Metrics ──
  metrics.augmentsInjected += selected.length
  metrics.recallCalls++
  metricsRecordResponseTime(Date.now() - _metricsStart)

  session.lastPrompt = userMsg
  session.lastSenderId = senderId
  session.lastChannelId = channelId
  session.lastResponseContent = ''
  session._dedupKey = userMsg.slice(0, 100).toLowerCase().trim()  // for reply dedup in handleSent
  // Save the clean user message (before augment injection) for avatar data collection.
  {
    let raw = ((event.context || {}).body || userMsg) as string
    raw = raw.replace(/^\[message_id:\s*\S+\]\s*/i, '')
    // Strip nickname prefix: "wang: " or "用户名: "
    raw = raw.replace(/^[a-zA-Z0-9_\u4e00-\u9fff]{1,20}:\s*/, '')
    // Strip any remaining newline prefix
    raw = raw.replace(/^\n+/, '').trim()
    session._rawUserMsg = raw || userMsg
  }
  innerState.lastActivityTime = Date.now()

  // Delayed post-processing: afterTurn() doesn't fire reliably,
  // so we do it here with a setTimeout to wait for LLM response
  const _snapPrompt = userMsg
  const _snapRawMsg = session._rawUserMsg
  const _snapSenderId = senderId
  const _snapChannelId = channelId
  const _isCasual = /^(哈哈|嗯|好的?|ok|早|晚安|谢谢|收到|了解|明白|懂了)$/i.test(userMsg.trim())
  if (!_isCasual && userMsg.length >= 5) {
    setTimeout(async () => {
      try {
        // Check if session has been superseded by a newer message
        const currentSession = getSessionState(getLastActiveSessionKey())
        if (currentSession.lastPrompt && currentSession.lastPrompt !== _snapPrompt) return // session overridden by newer message

        // Read bot response from session JSONL
        const sessionDir = resolve(homedir(), '.openclaw/agents/cc/sessions')
        const files = readdirSync(sessionDir).filter((f: string) => f.endsWith('.jsonl')).sort()
        if (files.length === 0) return
        const lastFile = resolve(sessionDir, files[files.length - 1])
        const lines = readFileSync(lastFile, 'utf-8').trim().split('\n')
        let botResponse = ''
        for (let i = lines.length - 1; i >= 0; i--) {
          try {
            const obj = JSON.parse(lines[i])
            if (obj?.message?.role === 'assistant') {
              botResponse = Array.isArray(obj.message.content)
                ? obj.message.content.filter((c: any) => c?.type === 'text').map((c: any) => c.text || '').join('')
                : (obj.message.content || '')
              break
            }
          } catch {}
        }
        if (!botResponse || botResponse.length < 20) return

        session.lastResponseContent = botResponse
        console.log(`[cc-soul][delayed-post] processing response (${botResponse.length} chars) for "${_snapPrompt.slice(0, 30)}"`)

        // Self-correction
        if (isEnabled('self_correction')) {
          const selfIssue = selfCheckSync(_snapPrompt, botResponse)
          if (selfIssue) {
            const scScore = scoreResponse(_snapPrompt, botResponse)
            if (scScore <= 3) {
              notifyOwnerDM(`⚠️ 刚才的回答可能有误：${selfIssue}。评分 ${scScore}/10`).catch(() => {}) // intentionally silent
              console.log(`[cc-soul][delayed-post] self-correction: ${selfIssue} (score=${scScore})`)
            }
          }
        }

        // Persona drift
        try {
          const persona = getActivePersona()
          if (persona) {
            const driftScore = checkPersonaDrift(botResponse, persona.id, persona.name, persona.tone, persona.idealVector)
            if (driftScore > 0.5) { stats.driftCount++; saveStats() }
          }
        } catch {}

        // Cost tracking
        try { recordTurnUsage(_snapPrompt, botResponse, 0) } catch {}

        // Brain modules onSent
        try { brain.fire('onSent', { userMessage: _snapPrompt, botReply: botResponse, senderId: _snapSenderId, channelId: _snapChannelId }) } catch {}

        // Memory commands from response
        {
          const memCmds = parseMemoryCommands(botResponse)
          if (memCmds.length > 0) executeMemoryCommands(memCmds, _snapSenderId, _snapChannelId)
        }

        // History + post-response analysis
        addToHistory(_snapPrompt, botResponse)
        const prevScore = scoreResponse(_snapPrompt, botResponse)
        trackQuality(prevScore)

        if (!getPrivacyMode()) {
          runPostResponseAnalysis(_snapPrompt, botResponse, (result) => {
            for (const m of result.memories) {
              addMemoryWithEmotion(m.content, m.scope, _snapSenderId, m.visibility, _snapChannelId, result.emotion, true)
            }
            addEntitiesFromAnalysis(result.entities)
            if (result.satisfaction === 'POSITIVE') bodyOnPositiveFeedback()
            console.log(`[cc-soul][delayed-post] analysis done: sat=${result.satisfaction} q=${result.quality.score} mem=${result.memories.length}`)
          })
        }

        // Avatar data collection — use RAW user message (not augmented prompt)
        try { collectAvatarData(_snapRawMsg || _snapPrompt, botResponse, _snapSenderId) } catch (_) {}
      } catch (e: any) {
        console.log(`[cc-soul][delayed-post] error: ${e.message}`)
      }
    }, 45000)
  }
}

/**
 * message:sent -- record response + trigger async post-response analysis.
 */
export function handleSent(event: any): void {
  if (!getInitialized()) initializeSoul()
  setAgentBusy(false)
  killGatewayClaude()
  postReplyCleanup().catch(() => { /* cleanup failure is non-fatal */ })

  const sentSessionKey = event.sessionKey || getLastActiveSessionKey()
  const session = getSessionState(sentSessionKey)

  const content = (event.context?.content || event.content || event.text || '') as string
  console.log(`[cc-soul][handleSent] content=${content.length} chars, keys=${Object.keys(event).join(',')}`)
  if (content) {
    session.lastResponseContent = content

    // 记录回复到去重缓存
    {
      const _sentMsgKey = session._dedupKey || (session.lastPrompt || '').slice(0, 100).toLowerCase().trim()
      if (_sentMsgKey) {
        _recentReplies.set(_sentMsgKey, { reply: content.slice(0, 200), ts: Date.now() })
        // 清理超过1小时的记录
        for (const [k, v] of Object.entries(_recentRepliesObj)) {
          if (Date.now() - v.ts > 3600000) _recentReplies.delete(k)
        }
      }
    }

    // ── Answer Affinity：评估注入记忆对回答的贡献度 ──
    try {
      if (session.lastRecalledContents.length > 0 && content.length > 20) {
        const { scoreAffinity } = require('./answer-affinity.ts')
        const stubMemories = session.lastRecalledContents.map((c: string) => ({ content: c, ts: Date.now(), scope: 'recalled' as const }))
        const affinityResults = scoreAffinity(stubMemories, content, session.lastPrompt || '')
        const usedCount = affinityResults.filter((r: any) => r.signal === 'used').length
        if (usedCount > 0 || affinityResults.length > 0) {
          console.log(`[cc-soul][affinity] ${usedCount}/${affinityResults.length} memories contributed to response`)
        }
      }
    } catch {}

    // Cost tracking
    {
      const augTokens = session.lastAugmentsUsed.reduce((sum, a) => sum + estimateTokens(a), 0)
      try { recordTurnUsage(session.lastPrompt || '', content, augTokens) } catch (_) { /* cost-tracker not available */ }
    }

    // #14 语音朗读
    if (getReadAloudPending() && platform() === 'darwin') {
      setReadAloudPending(false)
      const safeText = content.replace(/["`$\\]/g, '').slice(0, 2000)
      execFile('say', [safeText], (err) => { if (err) console.log(`[cc-soul][tts] say failed: ${err.message}`) })
    }
    setReadAloudPending(false)

    // 举一反三 post-processing moved to context-engine.ts afterTurn()

    // Persona drift detection (rule-based)
    try {
      const persona = getActivePersona()
      if (persona) {
        const driftScore = checkPersonaDrift(content, persona.id, persona.name, persona.tone, persona.idealVector)
        if (driftScore > 0.5) {
          stats.driftCount++
          saveStats()
        }
      }
    } catch (_) {}

    // ── #8 自我纠错 ──
    if (isEnabled('self_correction') && session.lastPrompt && content.length > 20) {
      const selfIssue = selfCheckSync(session.lastPrompt, content)
      if (selfIssue) {
        const scScore = scoreResponse(session.lastPrompt, content)
        if (scScore <= 3) {
          notifyOwnerDM(`⚠️ 刚才的回答可能有误：${selfIssue}。补充：回复质量评分 ${scScore}/10，问题="${session.lastPrompt.slice(0, 60)}"`)
            .catch(() => {}) // intentionally silent
          console.log(`[cc-soul][self-correction] issue detected (score=${scScore}): ${selfIssue}`)
        }
      }
    }

    // Active memory management
    {
      const memCommands = parseMemoryCommands(content)
      if (memCommands.length > 0) {
        executeMemoryCommands(memCommands, session.lastSenderId, session.lastChannelId)
      }
    }

    // Record reasoning chain (recalled memories) to journal
    if (session.lastRecalledContents.length > 0) {
      const timeStr = new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
      innerState.journal.push({
        time: timeStr,
        thought: `[推理链] 回复「${session.lastPrompt.slice(0, 30)}」时召回 ${session.lastRecalledContents.length} 条记忆: ${session.lastRecalledContents.slice(0, 3).map(c => c.slice(0, 40)).join('; ')}`,
        type: 'observation',
      })
    }

    const snapPrompt = session.lastPrompt
    const snapResponse = session.lastResponseContent
    const snapSenderId = session.lastSenderId
    const snapChannelId = session.lastChannelId
    const snapRecalled = [...session.lastRecalledContents]
    const snapMatchedRules = [...session.lastMatchedRuleTexts]

    setTimeout(() => {
      if (session._lastAnalyzedPrompt === snapPrompt) return
      if (snapPrompt && snapResponse && !getPrivacyMode()) {
        session._lastAnalyzedPrompt = snapPrompt
        metrics.cliCalls++
        runPostResponseAnalysis(snapPrompt, snapResponse, (result) => {
          for (const m of result.memories) {
            addMemoryWithEmotion(m.content, m.scope, snapSenderId, m.visibility, snapChannelId, result.emotion, true)
          }
          addEntitiesFromAnalysis(result.entities)
          if (result.memoryOps && result.memoryOps.length > 0) {
            const MAX_OPS_PER_TURN = 3
            const MAX_DELETE_PER_OP = 2
            let opsExecuted = 0
            for (const op of result.memoryOps) {
              if (opsExecuted >= MAX_OPS_PER_TURN) {
                console.log(`[cc-soul][memory-ops] CAPPED at ${MAX_OPS_PER_TURN} ops (anti-hallucination)`)
                break
              }
              if (!op.keyword || op.keyword.length < 4) {
                console.log(`[cc-soul][memory-ops] SKIP: keyword too short "${op.keyword}" (anti-hallucination)`)
                continue
              }
              if (!op.reason || op.reason.length < 3) {
                console.log(`[cc-soul][memory-ops] SKIP: no valid reason for ${op.action} "${op.keyword}" (anti-hallucination)`)
                continue
              }
              const kw = op.keyword.toLowerCase()
              if (op.action === 'delete') {
                let deleted = 0
                // Re-snapshot memories array ref to avoid stale closure (async 2s delay)
                const mems = memoryState.memories
                for (let i = 0; i < mems.length && deleted < MAX_DELETE_PER_OP; i++) {
                  if (mems[i].content.toLowerCase().includes(kw) && mems[i].scope !== 'expired') {
                    mems[i].scope = 'expired'
                    deleted++
                  }
                }
                if (deleted > 0) console.log(`[cc-soul][memory-ops] DELETE ${deleted} memories (keyword: ${op.keyword}, reason: ${op.reason})`)
              } else if (op.action === 'update' && op.newContent) {
                // Use findIndex to locate target at call-time, not stale iterator
                const idx = memoryState.memories.findIndex(m => m.content.toLowerCase().includes(kw) && m.scope !== 'expired')
                if (idx >= 0) {
                  const mem = memoryState.memories[idx]
                  console.log(`[cc-soul][memory-ops] UPDATE: "${mem.content.slice(0, 40)}" → "${op.newContent.slice(0, 40)}" (reason: ${op.reason})`)
                  mem.content = op.newContent
                  mem.ts = Date.now()
                  mem.tags = undefined
                }
              }
              opsExecuted++
            }
          }
          if (result.satisfaction === 'POSITIVE') {
            bodyOnPositiveFeedback()
            detectValueSignals(snapPrompt, true, snapSenderId)
            updateRelationship(snapSenderId, 'positive')
            stats.positiveFeedback++
            trackGratitude(snapPrompt, snapResponse, snapSenderId)
            updateUserStylePreference(snapSenderId, snapResponse, true)
          } else if (result.satisfaction === 'NEGATIVE') {
            updateUserStylePreference(snapSenderId, snapResponse, false)
          }
          const qScore = Math.max(1, Math.min(10, result.quality.score))
          trackQuality(qScore)
          if (snapRecalled.length > 0) trackRecallImpact(snapRecalled, qScore)
          updateBanditReward(qScore, result.satisfaction === 'NEGATIVE')
          if (qScore <= 4) {
            body.alertness = Math.min(1.0, body.alertness + 0.08)
          }
          if (snapMatchedRules.length > 0) {
            const matchedRuleObjs = rules.filter(r => snapMatchedRules.includes(r.rule))
            if (matchedRuleObjs.length > 0) {
              recordRuleQuality(matchedRuleObjs, result.quality.score)
            }
          }
          // Heuristic: only persist reflection when quality < 5 (avoid storing trivial "无" reflections)
          if (result.reflection && result.quality.score < 5) {
            addMemory(`[反思] ${result.reflection}`, 'reflection', snapSenderId, 'private', snapChannelId)
          }
        })

        recallFeedbackLoop(snapPrompt, snapRecalled)
        triggerAssociativeRecall(snapPrompt, snapRecalled)

        writeJournalWithCLI(snapPrompt, snapResponse, stats)
        detectWorkflowOpportunity(snapPrompt, snapResponse)

        CJK_WORD_REGEX.lastIndex = 0
        const recentTopicWords = (snapPrompt.match(CJK_WORD_REGEX) || []).slice(0, 5)
        generatePrediction(recentTopicWords, snapSenderId)

        if (isEnabled('skill_library')) autoExtractSkill(snapPrompt, snapResponse)

        refreshNarrativeAsync()

        // ── New module post-response hooks ──
        try { const ap = getActivePersona(); trackPersonaStyle(snapResponse, ap?.id ?? 'default') } catch (_) {}
        try { updateBeliefFromMessage(snapPrompt, snapResponse) } catch (_) {}

        // Session summary — write conversation digest for cross-session continuity
        if (isEnabled('memory_session_summary') && (stats.totalMessages % 10 === 0 || memoryState.chatHistory.length >= 8)) {
          triggerSessionSummary()
        }

        // ── Avatar data collection: use RAW user message (not augmented prompt) ──
        try { collectAvatarData(session._rawUserMsg || snapPrompt, snapResponse, snapSenderId) } catch (_) {}

        innerState.lastActivityTime = Date.now()
      }
    }, 2000)
  }
}

/**
 * command:new -- persist everything, log stats.
 */
export function handleCommand(event: any): void {
  if (!getInitialized()) initializeSoul()
  flushAll()
  computeEval(stats.totalMessages, stats.corrections, true)
  console.log(
    `[cc-soul] session ${event.action} | ` +
    `mem:${memoryState.memories.length} rules:${rules.length} entities:${graphState.entities.length} | ` +
    `msgs:${stats.totalMessages} corrections:${stats.corrections} tasks:${stats.tasks} | ` +
    `eval: ${getEvalSummary(stats.totalMessages, stats.corrections)} | ` +
    `body: e=${body.energy.toFixed(2)} m=${body.mood.toFixed(2)} a=${body.alertness.toFixed(2)}`,
  )
}

// ═══════════════════════════════════════════════════════════════════════════════
// HOOK HANDLER (default export — backward compatibility for hook mode)
// ═══════════════════════════════════════════════════════════════════════════════

const handler = async (event: any): Promise<void> => {
  if (!getInitialized()) initializeSoul()

  try {
    if (event.type === 'agent' && event.action === 'bootstrap') {
      if (isContextEngineActive()) return
      handleBootstrap(event)
      return
    }

    if (event.type === 'message' && event.action === 'preprocessed') {
      handlePreprocessed(event)
      return
    }

    if (event.type === 'message' && event.action === 'sent') {
      // Always handle sent — CE afterTurn() may not fire
      handleSent(event)
      return
    }

    if (event.type === 'command') {
      handleCommand(event)
    }

  } catch (err: any) {
    recordModuleError('handler', err?.message || String(err))
    console.error('[cc-soul] error:', err?.message || err)
  }
}

export default handler

// ═══════════════════════════════════════════════════════════════════════════════
// RE-EXPORTS (backward compatibility — external modules may import from handler)
// ═══════════════════════════════════════════════════════════════════════════════

export { runHeartbeat } from './handler-heartbeat.ts'
export { getStats, metrics, formatMetrics } from './handler-state.ts'
