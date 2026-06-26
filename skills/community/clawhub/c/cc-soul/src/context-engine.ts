/**
 * context-engine.ts — cc-soul as OpenClaw Context Engine Plugin
 *
 * This module transforms cc-soul from a hook-only plugin into a full
 * Context Engine provider, solving:
 * - message:sent not always firing → afterTurn() always fires
 * - Soul prompt truncation → systemPromptAddition is first-class, never truncated
 * - Augments being budget-cut → systemPromptAddition is first-class
 *
 * Strategy: register as kind:"context-engine", implement the ContextEngine interface,
 * and also register hooks for message:preprocessed augment injection.
 * Compaction is delegated to OpenClaw's built-in runtime.
 */

import { buildSoulPrompt, selectAugments, estimateTokens } from './prompt-builder.ts'
import { memoryState, addMemory, addMemoryWithEmotion, parseMemoryCommands, executeMemoryCommands, recall, ensureMemoriesLoaded } from './memory.ts'
import { bodyOnPositiveFeedback } from './body.ts'
import { addEntitiesFromAnalysis } from './graph.ts'
import { runPostResponseAnalysis, setAgentBusy, killGatewayClaude, spawnCLI } from './cli.ts'
import { notifyOwnerDM } from './notify.ts'
import { taskState } from './tasks.ts'
import { trackQuality } from './quality.ts'
import { getSessionState, getLastActiveSessionKey } from './handler-state.ts'
// fingerprint.ts removed
// ── New module hooks (optional, loaded async) ──
let trackPersonaStyle: (text: string, personaId: string) => void = () => {}
let updateBeliefFromMessage: (user: string, bot: string) => void = () => {}
let trackRecallImpact: (contents: string[], score: number) => void = () => {}
let getActivePersona: () => { id: string } | null = () => null
import('./persona-drift.ts').then(m => { trackPersonaStyle = m.trackPersonaStyle }).catch((e: any) => { console.error(`[cc-soul] module load failed (persona-drift): ${e.message}`) })
import('./person-model.ts').then(m => { updateBeliefFromMessage = m.updateBeliefFromMessage }).catch((e: any) => { console.error(`[cc-soul] module load failed (person-model/tom): ${e.message}`) })
import('./memory.ts').then(m => { trackRecallImpact = m.trackRecallImpact }).catch((e: any) => { console.error(`[cc-soul] module load failed (memory): ${e.message}`) })
import('./persona.ts').then(m => { getActivePersona = m.getActivePersona }).catch((e: any) => { console.error(`[cc-soul] module load failed (persona): ${e.message}`) })

function syncResponseToSession(sessionKey: string | undefined, content: string) {
  try {
    const sk = sessionKey || getLastActiveSessionKey()
    const sess = getSessionState(sk)
    if (sess) sess.lastResponseContent = content
  } catch (_) {}
}

// ── State (module-level) ──

const _state = {
  lastUserMsg: '',
  lastBotResponse: '',
  lastSenderId: '',
  lastAugments: [] as string[],
  _sessionFile: '',
}

/** Called from hook handler to pass sender context */
export function setLastSenderId(id: string) { _state.lastSenderId = id }

/** Called from handler.ts to cache augments for assemble() */
export function setLastAugments(augments: string[]) { _state.lastAugments = augments }

// ── Stats accessor (avoids circular import from handler.ts) ──

let statsAccessor: () => { totalMessages: number; corrections: number; firstSeen: number } = () => ({
  totalMessages: 0, corrections: 0, firstSeen: Date.now(),
})

export function setStatsAccessor(fn: typeof statsAccessor) { statsAccessor = fn }

// ── The Context Engine implementation ──

export function createCcSoulContextEngine() {
  return {
    info: {
      id: 'cc-soul',
      name: 'cc-soul Context Engine',
      version: '1.3.0',
      ownsCompaction: false, // delegate compaction to OpenClaw runtime
    },

    async bootstrap(_params: {
      sessionId: string
      sessionKey?: string
      sessionFile: string
    }) {
      console.log(`[cc-soul][context-engine] bootstrap`)
      // Save session file path for dispose() to read bot response
      _state._sessionFile = _params.sessionFile
      return { bootstrapped: true }
    },

    async ingest(params: {
      sessionId: string
      sessionKey?: string
      message: { role: string; content: unknown; [key: string]: unknown }
      isHeartbeat?: boolean
    }) {
      // Track messages for afterTurn analysis
      if (params.message.role === 'user' && typeof params.message.content === 'string') {
        _state.lastUserMsg = params.message.content
      }
      if (params.message.role === 'assistant' && typeof params.message.content === 'string') {
        _state.lastBotResponse = params.message.content
        // Sync to session state so handlePreprocessed's "Previous turn analysis" has data
        syncResponseToSession(params.sessionKey, params.message.content)
      }
      return { ingested: true }
    },

    async ingestBatch(params: {
      sessionId: string
      sessionKey?: string
      messages: { role: string; content: unknown; [key: string]: unknown }[]
      isHeartbeat?: boolean
    }) {
      for (const msg of params.messages) {
        if (msg.role === 'user' && typeof msg.content === 'string') _state.lastUserMsg = msg.content
        if (msg.role === 'assistant' && typeof msg.content === 'string') _state.lastBotResponse = msg.content
      }
      return { ingestedCount: params.messages.length }
    },

    /**
     * afterTurn — always fires after a turn, solving message:sent unreliability.
     */
    async afterTurn(params: {
      sessionId: string
      sessionKey?: string
      sessionFile: string
      messages: { role: string; content: unknown; [key: string]: unknown }[]
      prePromptMessageCount: number
      autoCompactionSummary?: string
      isHeartbeat?: boolean
      tokenBudget?: number
    }) {
      // Release agent + cleanup
      setAgentBusy(false)
      killGatewayClaude()

      if (params.isHeartbeat) return

      // Extract user/assistant messages from params if ingest() wasn't called
      if (!_state.lastUserMsg || !_state.lastBotResponse) {
        if (params.messages?.length > 0) {
          for (let i = params.messages.length - 1; i >= 0; i--) {
            const m = params.messages[i]
            let text = ''
            if (typeof m.content === 'string') {
              text = m.content
            } else if (Array.isArray(m.content)) {
              text = (m.content as any[])
                .filter((p: any) => p?.type === 'text')
                .map((p: any) => p.text || '')
                .join(' ')
            }
            if (!text) continue
            if (m.role === 'assistant' && !_state.lastBotResponse) {
              _state.lastBotResponse = text
            }
            if (m.role === 'user' && !_state.lastUserMsg) {
              const cleaned = text.replace(/^Conversation info[\s\S]*?```\n*/m, '').replace(/^Sender[\s\S]*?```\n*/m, '').trim()
              if (cleaned) _state.lastUserMsg = cleaned
            }
            if (_state.lastUserMsg && _state.lastBotResponse) break
          }
        }
      }

      if (!_state.lastUserMsg || !_state.lastBotResponse) return

      const userMsg = _state.lastUserMsg
      const botResponse = _state.lastBotResponse

      _afterTurnCalled = true
      console.log(`[cc-soul][context-engine] afterTurn: post-response analysis (${userMsg.slice(0, 30)}...)`)

      // ── 泄漏检测：AI 回复中是否包含内部分析泄漏 ──
      const LEAK_PATTERNS = [
        /^.*?(?:用户说|用户在|用户想|用户需要|用户问).{2,30}(?:这是|说明|表明|意味)/m,
        /^.*?这是(?:一个|在).{2,20}(?:请求|时刻|场景|测试|信号)/m,
        /^.*?我应该(?:先|表示|给予|提供)/m,
      ]
      for (const pat of LEAK_PATTERNS) {
        if (pat.test(botResponse)) {
          console.error(`[cc-soul][LEAK] 检测到回复泄漏内部分析: "${botResponse.match(pat)?.[0]?.slice(0, 60)}"`)
          try { (await import('./decision-log.ts')).logDecision('response_leak', botResponse.match(pat)?.[0]?.slice(0, 40) || '?', `pattern=${pat.source.slice(0, 30)}`) } catch {}
          break
        }
      }

      // Sync session state so handleSent-dependent code works
      try {
        const { getSessionState, getLastActiveSessionKey } = await import('./handler-state.ts')
        const sk = getLastActiveSessionKey()
        const sess = getSessionState(sk)
        if (sess) {
          sess.lastResponseContent = botResponse
        }
      } catch {}

      // Self-correction: check if response has issues
      try {
        const { selfCheckSync } = await import('./quality.ts')
        const { scoreResponse } = await import('./quality.ts')
        if (userMsg.length > 5 && botResponse.length > 20) {
          const selfIssue = selfCheckSync(userMsg, botResponse)
          if (selfIssue) {
            const scScore = scoreResponse(userMsg, botResponse)
            if (scScore <= 3) {
              notifyOwnerDM(`⚠️ 刚才的回答可能有误：${selfIssue}。评分 ${scScore}/10`)
                .catch(() => {}) // intentionally silent — notification
              console.log(`[cc-soul][self-correction] issue: ${selfIssue} (score=${scScore})`)
            }
          }
        }
      } catch {}

      // Persona drift detection
      try {
        const { checkPersonaDrift } = await import('./persona-drift.ts')
        const { getActivePersona } = await import('./persona.ts')
        const persona = getActivePersona()
        if (persona) {
          checkPersonaDrift(botResponse, persona.id, persona.name, persona.tone, persona.idealVector)
        }
      } catch {}

      // Cost tracking
      try {
        const { recordTurnUsage } = await import('./cost-tracker.ts')
        recordTurnUsage(userMsg, botResponse, 0)
      } catch {}

      // Brain modules onSent (theory-of-mind, persona-drift, values)
      try {
        const { brain } = await import('./brain.ts')
        brain.fire('onSent', { userMessage: userMsg, botReply: botResponse, senderId: _state.lastSenderId })
      } catch {}

      // Active memory management from response text
      {
        const memCommands = parseMemoryCommands(botResponse)
        if (memCommands.length > 0) {
          executeMemoryCommands(memCommands, _state.lastSenderId)
        }
      }

      // Full post-response analysis
      runPostResponseAnalysis(userMsg, botResponse, (result) => {
        for (const m of result.memories) {
          addMemoryWithEmotion(m.content, m.scope, _state.lastSenderId, m.visibility, undefined, result.emotion, true)
        }
        addEntitiesFromAnalysis(result.entities)

        // LLM-driven memory operations
        if (result.memoryOps && result.memoryOps.length > 0) {
          for (const op of result.memoryOps) {
            if (!op.keyword || op.keyword.length < 4) continue
            if (!op.reason || op.reason.length < 3) continue
            const kw = op.keyword.toLowerCase()
            if (op.action === 'delete') {
              let deleted = 0
              for (const mem of memoryState.memories) {
                if (deleted >= 2) break
                if (mem.content.toLowerCase().includes(kw) && mem.scope !== 'expired') {
                  mem.scope = 'expired'
                  deleted++
                }
              }
              if (deleted > 0) console.log(`[cc-soul][memory-ops] DELETE ${deleted} (keyword: ${op.keyword}, reason: ${op.reason})`)
            } else if (op.action === 'update' && op.newContent) {
              for (const mem of memoryState.memories) {
                if (mem.content.toLowerCase().includes(kw) && mem.scope !== 'expired') {
                  console.log(`[cc-soul][memory-ops] UPDATE: "${mem.content.slice(0, 40)}" → "${op.newContent.slice(0, 40)}"`)
                  mem.content = op.newContent
                  mem.ts = Date.now()
                  mem.tags = undefined
                  break
                }
              }
            }
          }
        }

        if (result.satisfaction === 'POSITIVE') bodyOnPositiveFeedback()
        trackQuality(result.quality.score)
        if (result.reflection) addMemory(`[反思] ${result.reflection}`, 'reflection', _state.lastSenderId, 'private')

        console.log(`[cc-soul][context-engine] afterTurn complete: sat=${result.satisfaction} q=${result.quality.score}`)

        // ── New module hooks (run inside callback so we have quality score) ──
        try { trackPersonaStyle(botResponse, getActivePersona()?.id ?? 'default') } catch (_) {}
        try { updateBeliefFromMessage(userMsg, botResponse) } catch (_) {}
        try { trackRecallImpact([], result.quality.score) } catch (_) {}
      })

      // Reset
      _state.lastUserMsg = ''
      _state.lastBotResponse = ''
    },

    /**
     * assemble — inject soul prompt as systemPromptAddition (first-class, never truncated).
     */
    async assemble(params: {
      sessionId: string
      sessionKey?: string
      messages: { role: string; content: unknown; [key: string]: unknown }[]
      tokenBudget?: number
    }) {
      console.log('[cc-soul][context-engine] ★★★ assemble() CALLED ★★★')
      const s = statsAccessor()
      const soulPrompt = buildSoulPrompt(
        s.totalMessages, s.corrections, s.firstSeen,
        taskState.workflows,
      )

      // Extract lastUserMsg from params.messages if ingest() wasn't called
      // console.log(`[cc-soul][context-engine] assemble: _state.lastUserMsg="${(_state.lastUserMsg||'').slice(0,20)}", msgs=${params.messages?.length || 0}`)
      if (!_state.lastUserMsg && params.messages?.length > 0) {
        for (let i = params.messages.length - 1; i >= 0; i--) {
          const m = params.messages[i]
          if (m.role !== 'user') continue
          // Content can be string or array of {type: 'text', text: '...'}
          let text = ''
          if (typeof m.content === 'string') {
            text = m.content
          } else if (Array.isArray(m.content)) {
            text = (m.content as any[])
              .filter(p => p?.type === 'text')
              .map(p => p.text || '')
              .join(' ')
          }
          if (text.length > 0) {
            // Strip OpenClaw metadata envelope
            let cleaned = text
            // Remove OpenClaw metadata: find the last ``` and take everything after it
            const lastBacktick = text.lastIndexOf('```')
            if (lastBacktick !== -1) {
              cleaned = text.slice(lastBacktick + 3).trim()
            }
            // Remove [message_id: xxx] prefix
            cleaned = cleaned.replace(/^\[message_id:\s*\S+\]\s*/i, '')
            // Remove "name: " prefix (e.g. "wang: ")
            cleaned = cleaned.replace(/^[a-zA-Z0-9_\u4e00-\u9fff]{1,20}:\s/, '')
            cleaned = cleaned.trim()
            if (cleaned) {
              _state.lastUserMsg = cleaned
              break
            }
          }
        }
        if (_state.lastUserMsg) {
          console.log(`[cc-soul][context-engine] assemble: extracted lastUserMsg="${_state.lastUserMsg.slice(0, 40)}"`)
          // Command detection in assemble (reliable fallback when preprocessed hook doesn't fire)
          try {
            const { routeCommandDirect, wasHandledByDirect } = await import('./handler-commands.ts')
            if (typeof routeCommandDirect === 'function') {
              const rawMsg = _state.lastUserMsg
                .replace(/^\[message_id:\s*\S+\]\s*/i, '')
                .replace(/^[a-zA-Z0-9_\u4e00-\u9fff]{1,20}:\s/, '')
                .trim()
              // Skip if already handled by inbound_claim path
              if (!wasHandledByDirect(rawMsg)) {
                routeCommandDirect(rawMsg, params)
              }
            }
          } catch (_) {}
        }
      }

      // If preprocessed hook hasn't populated augments yet (async race),
      // do a synchronous memory recall directly in assemble() as fallback
      let augmentsToUse = _state.lastAugments
      // 每次 assemble 都同步 recall——不依赖缓存的 augments
      // 解决一轮延迟问题：确保当前消息的记忆实时注入，不管走什么 AI 后端
      if (_state.lastUserMsg) {
        try {
          // CGAF: 生�� cogHints 供 recall 使用（<1ms 纯正则，不阻塞）
          let _ceHints: any = null
          try { _ceHints = require('./cognition.ts').toCogHints(_state.lastUserMsg) } catch {}
          const recalled = recall(_state.lastUserMsg, 8, _state.lastSenderId || undefined, undefined, undefined, undefined, _ceHints)
          if (recalled.length > 0) {
            const memAugment = '[相关记忆] ' + recalled.map(m => {
              const emotionTag = m.emotion && m.emotion !== 'neutral' ? ` (${m.emotion})` : ''
              return m.content.slice(0, 80) + emotionTag
            }).join('；')
            // 替换缓存中旧的记忆 augment（如果有），确保用当前轮的
            augmentsToUse = augmentsToUse.filter(a => !/^\[记忆\]|\[相关记忆\]|\[相关事实\]/.test(a))
            augmentsToUse.push(memAugment)
            console.log(`[cc-soul][context-engine] assemble: sync recall injected ${recalled.length} memories for "${_state.lastUserMsg.slice(0, 30)}"`)
          }
        } catch {}
      }

      // Merge SOUL.md + augments — strip bracket tags + rewrite third-person analysis
      const cleanedAugments = augmentsToUse.map(a => {
        let c = a.replace(/^\[([^\]]+)\]\s*/, '')  // strip [tag] prefix
        // Rewrite third-person "用户..." to second-person "你..." to prevent LLM mimicry
        c = c.replace(/^用户(说了?|提到|指出|表示|认为|觉得|想要|需要|在|的|问)/g, '你$1')
        c = c.replace(/用户(情绪|心情|状态|风格|偏好)/g, '你的$1')
        c = c.replace(/该用户/g, '这个人')
        c = c.replace(/当前用户/g, '对方')
        // Strip analysis-style prefixes that LLMs tend to echo
        c = c.replace(/^(检测到|发现|分析|注意到|观察到|识别到)\s*/g, '')
        return c
      })
      const parts = [soulPrompt]
      if (cleanedAugments.length > 0) {
        parts.push(cleanedAugments.join('\n'))
      }
      const fullPrompt = parts.join('\n\n')

      console.log(`[cc-soul][context-engine] assemble: ${soulPrompt.length} chars soul + ${augmentsToUse.length} augments = ${fullPrompt.length} chars total`)
      if (augmentsToUse.length > 0) {
        console.log(`[cc-soul][context-engine] augment preview: ${augmentsToUse.map(a => a.slice(0, 60)).join(' | ')}`)
        const hasMemory = augmentsToUse.some(a => a.includes('[相关记忆]'))
        console.log(`[cc-soul][context-engine] assemble: has [相关记忆]=${hasMemory}`)
      }

      return {
        messages: params.messages,
        estimatedTokens: 0,
        systemPromptAddition: fullPrompt,
      }
    },

    /**
     * compact — delegate to runtime with soul-aware instructions.
     */
    async compact(params: {
      sessionId: string
      sessionKey?: string
      sessionFile: string
      tokenBudget?: number
      force?: boolean
      currentTokenCount?: number
      compactionTarget?: 'budget' | 'threshold'
      customInstructions?: string
    }) {
      // Add core memory hints to compaction instructions
      const coreHints = memoryState.memories
        .filter(m => m.scope === 'core' || m.scope === 'important')
        .slice(0, 10)
        .map(m => m.content.slice(0, 50))
        .join('; ')

      const soulInstructions = coreHints
        ? `IMPORTANT: Preserve these key user facts during compaction: ${coreHints}`
        : undefined

      const merged = [params.customInstructions, soulInstructions].filter(Boolean).join('\n\n')

      try {
        // Dynamic import — resolved at runtime through OpenClaw's module system
        const mod = await import('openclaw/plugin-sdk')
        return await mod.delegateCompactionToRuntime({
          ...params,
          customInstructions: merged || params.customInstructions,
        })
      } catch {
        console.log('[cc-soul][context-engine] delegateCompactionToRuntime unavailable')
        return { ok: true, compacted: false, reason: 'delegate unavailable' }
      }
    },

    async dispose() {
      console.log('[cc-soul][context-engine] dispose')

      // WORKAROUND: OpenClaw API mode doesn't call afterTurn() or message:sent hook.
      // Use dispose() as fallback trigger for post-response analysis.
      // Extract bot response from session JSONL if ingest() wasn't called
      if (!_state.lastBotResponse && _state._sessionFile) {
        try {
          const { readFileSync, existsSync } = await import('fs')
          if (existsSync(_state._sessionFile)) {
            const lines = readFileSync(_state._sessionFile, 'utf-8').split('\n').filter((l: string) => l.trim())
            for (let i = lines.length - 1; i >= 0; i--) {
              try {
                const entry = JSON.parse(lines[i])
                if (entry?.type === 'message' && entry?.message?.role === 'assistant') {
                  const content = entry.message.content
                  if (typeof content === 'string') {
                    _state.lastBotResponse = content
                  } else if (Array.isArray(content)) {
                    const texts = content.filter((p: any) => p?.type === 'text').map((p: any) => p.text || '')
                    _state.lastBotResponse = texts.join(' ')
                  }
                  if (_state.lastBotResponse) break
                }
              } catch (_) {}
            }
            if (_state.lastBotResponse) {
              console.log(`[cc-soul][context-engine] dispose: recovered bot response from session (${_state.lastBotResponse.length} chars)`)
            }
          }
        } catch (_) {}
      }

      if (_state.lastUserMsg && _state.lastBotResponse) {
        console.log(`[cc-soul][context-engine] dispose: triggering afterTurn fallback (user=${_state.lastUserMsg.slice(0, 30)}, bot=${_state.lastBotResponse.slice(0, 30)})`)
        const userMsg = _state.lastUserMsg
        const botResponse = _state.lastBotResponse

        // Active memory management from response text
        {
          const memCommands = parseMemoryCommands(botResponse)
          if (memCommands.length > 0) {
            executeMemoryCommands(memCommands, _state.lastSenderId)
          }
        }

        // Full post-response analysis (async, fire-and-forget)
        runPostResponseAnalysis(userMsg, botResponse, (result) => {
          for (const m of result.memories) {
            addMemoryWithEmotion(m.content, m.scope, _state.lastSenderId, m.visibility, undefined, result.emotion, true)
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
                  if (mem.content.toLowerCase().includes(kw) && mem.scope !== 'expired') {
                    mem.scope = 'expired'
                    deleted++
                  }
                }
                if (deleted > 0) console.log(`[cc-soul][memory-ops] DELETE ${deleted} (keyword: ${op.keyword})`)
              } else if (op.action === 'update' && op.newContent) {
                for (const mem of memoryState.memories) {
                  if (mem.content.toLowerCase().includes(kw) && mem.scope !== 'expired') {
                    mem.content = op.newContent
                    mem.ts = Date.now()
                    mem.tags = undefined
                    break
                  }
                }
              }
            }
          }

          if (result.satisfaction === 'POSITIVE') bodyOnPositiveFeedback()
          trackQuality(result.quality.score)
          if (result.reflection) addMemory(`[反思] ${result.reflection}`, 'reflection', _state.lastSenderId, 'private')
          console.log(`[cc-soul][context-engine] dispose-afterTurn complete: sat=${result.satisfaction} q=${result.quality.score}`)

          // New module hooks
          try { trackPersonaStyle(botResponse, getActivePersona()?.id ?? 'default') } catch (_) {}
          try { updateBeliefFromMessage(userMsg, botResponse) } catch (_) {}
          })

        // Reset
        _state.lastUserMsg = ''
        _state.lastBotResponse = ''
      }
    },
  }
}

// ── Plugin registration helper ──

let _registered = false
let _afterTurnCalled = false

/**
 * Try to register cc-soul as a Context Engine via plugin-sdk.
 * Returns true if registered, false if falling back to hook mode.
 */
export async function tryRegisterContextEngine(): Promise<boolean> {
  if (_registered) return true

  try {
    const { registerContextEngine } = await import('openclaw/plugin-sdk')
    const result = registerContextEngine('cc-soul', () => createCcSoulContextEngine())
    if (result.ok) {
      _registered = true
      console.log('[cc-soul][context-engine] ✅ registered as Context Engine')
      return true
    }
    console.log(`[cc-soul][context-engine] registration blocked: ${result.existingOwner}`)
    return false
  } catch (e: any) {
    console.log(`[cc-soul][context-engine] not available (${e.message?.slice(0, 60)}), hook mode`)
    return false
  }
}

export function isContextEngineActive(): boolean {
  return _registered && _afterTurnCalled
}

export function isContextEngineRegistered(): boolean {
  return _registered
}
