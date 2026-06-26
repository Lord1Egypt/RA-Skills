/**
 * context-budget.ts — 自适应 Context Budget Manager
 *
 * 根据后端 AI 的 context window 动态分配 augments/history 预算。
 * 4K 小模型自动极限压缩，200K 大模型放开注入。
 *
 * 支持所有后端：Claude / GPT / Ollama / 通义 / 智谱 / 本地模型
 *
 * cc-soul 原创核心模块
 */

// ═══════════════════════════════════════════════════════════════════════════════
// TYPES
// ═══════════════════════════════════════════════════════════════════════════════

export interface ContextBudget {
  totalWindow: number
  systemPrompt: number
  outputReserve: number
  available: number          // total - system - output
  augmentBudget: number      // token 数
  historyBudget: number      // token 数
  historyTurns: number       // 可注入轮数
  compressionTier: 'none' | 'light' | 'aggressive' | 'extreme'
}

export interface AugmentCompressionConfig {
  maxAugments: number
  forceCompression: 'summary' | 'compressed_fact' | null
  skipTypes: string[]         // 跳过的低优先级 augment 类型
  maxAugmentTokens: number    // 单条 augment 最大 token
}

// ═══════════════════════════════════════════════════════════════════════════════
// KNOWN MODEL CONTEXT WINDOWS
// ═══════════════════════════════════════════════════════════════════════════════

const MODEL_WINDOWS: Record<string, number> = {
  // Claude
  'claude-opus-4-6': 200000,
  'claude-sonnet-4-6': 200000,
  'claude-haiku-4-5': 200000,
  'claude-3-5-sonnet': 200000,
  'claude-3-haiku': 200000,
  // OpenAI
  'gpt-4o': 128000,
  'gpt-4o-mini': 128000,
  'gpt-4-turbo': 128000,
  'gpt-4': 8192,
  'gpt-3.5-turbo': 16384,
  'o1': 200000,
  'o1-mini': 128000,
  'o3': 200000,
  'o3-mini': 200000,
  'o4-mini': 200000,
  // Ollama / 本地模型（保守估计）
  'llama3': 8192,
  'llama3.1': 131072,
  'llama3.2': 131072,
  'mistral': 32768,
  'mixtral': 32768,
  'qwen2': 32768,
  'qwen2.5': 131072,
  'deepseek-v2': 128000,
  'deepseek-v3': 128000,
  'deepseek-r1': 128000,
  'gemma2': 8192,
  'phi3': 4096,
  'phi4': 16384,
  // 国产
  'glm-4': 128000,
  'glm-4-flash': 128000,
  'qwen-turbo': 131072,
  'qwen-plus': 131072,
  'qwen-max': 32768,
  'doubao-seed': 32768,
  'moonshot-v1-128k': 128000,
  'moonshot-v1-32k': 32768,
  'moonshot-v1-8k': 8192,
  'yi-large': 32768,
  'ernie-4.0': 8192,
}

// ═══════════════════════════════════════════════════════════════════════════════
// CONTEXT WINDOW DETECTION
// ═══════════════════════════════════════════════════════════════════════════════

let _cachedWindow: number | null = null

/**
 * 检测当前后端的 context window 大小。
 * 优先级：ai_config.json 手动指定 > 模型名匹配 > 默认 32K
 */
export function getContextWindow(): number {
  if (_cachedWindow !== null) return _cachedWindow

  // 1. 检查 ai_config.json 手动指定
  try {
    const { DATA_DIR, loadJson } = require('./persistence.ts')
    const { resolve } = require('path')
    const config = loadJson(resolve(DATA_DIR, 'ai_config.json'), {})
    if (config.context_window && config.context_window > 0) {
      _cachedWindow = config.context_window
      return _cachedWindow
    }

    // 2. 从模型名推断
    const modelName = config.api_model || ''
    if (modelName) {
      // 精确匹配
      if (MODEL_WINDOWS[modelName]) {
        _cachedWindow = MODEL_WINDOWS[modelName]
        return _cachedWindow
      }
      // 前缀匹配
      for (const [key, window] of Object.entries(MODEL_WINDOWS)) {
        if (modelName.includes(key) || key.includes(modelName.split('/').pop() || '')) {
          _cachedWindow = window
          return _cachedWindow
        }
      }
    }
  } catch {}

  // 3. 从 OpenClaw 配置推断
  try {
    const { existsSync, readFileSync } = require('fs')
    const { homedir } = require('os')
    const { resolve } = require('path')
    const configPath = resolve(homedir(), '.openclaw/openclaw.json')
    if (existsSync(configPath)) {
      const raw = JSON.parse(readFileSync(configPath, 'utf-8'))
      const modelRef = raw?.agents?.defaults?.model?.primary || ''
      if (modelRef) {
        const modelId = modelRef.split('/').pop() || ''
        for (const [key, window] of Object.entries(MODEL_WINDOWS)) {
          if (modelId.includes(key) || key.includes(modelId)) {
            _cachedWindow = window
            return _cachedWindow
          }
        }
      }
    }
  } catch {}

  // 4. 默认 32K（安全保守）
  _cachedWindow = 32768
  return _cachedWindow
}

/** 手动设置 context window（用于 API 模式传入） */
export function setContextWindow(tokens: number): void {
  _cachedWindow = tokens
}

/** 重置缓存（模型切换时） */
export function resetContextWindowCache(): void {
  _cachedWindow = null
}

// ═══════════════════════════════════════════════════════════════════════════════
// BUDGET COMPUTATION
// ═══════════════════════════════════════════════════════════════════════════════

interface Strategy {
  maxWindow: number
  augmentRatio: number
  historyRatio: number
  outputReserve: number
  tokensPerTurn: number      // 每轮对话估算 token 数
}

const STRATEGIES: Record<string, Strategy> = {
  extreme:    { maxWindow: 4096,    augmentRatio: 0.15, historyRatio: 0.30, outputReserve: 512,  tokensPerTurn: 150 },
  aggressive: { maxWindow: 8192,    augmentRatio: 0.20, historyRatio: 0.40, outputReserve: 800,  tokensPerTurn: 200 },
  light:      { maxWindow: 32768,   augmentRatio: 0.25, historyRatio: 0.40, outputReserve: 1500, tokensPerTurn: 250 },
  none:       { maxWindow: Infinity, augmentRatio: 0.30, historyRatio: 0.40, outputReserve: 2000, tokensPerTurn: 300 },
}

export function computeBudget(contextWindow?: number): ContextBudget {
  const totalWindow = contextWindow ?? getContextWindow()
  const systemPromptTokens = 500  // SOUL.md + 身份 + 系统指令

  let strategy: Strategy
  let tier: ContextBudget['compressionTier']

  if (totalWindow <= 4096) {
    strategy = STRATEGIES.extreme; tier = 'extreme'
  } else if (totalWindow <= 8192) {
    strategy = STRATEGIES.aggressive; tier = 'aggressive'
  } else if (totalWindow <= 32768) {
    strategy = STRATEGIES.light; tier = 'light'
  } else {
    strategy = STRATEGIES.none; tier = 'none'
  }

  const available = Math.max(0, totalWindow - systemPromptTokens - strategy.outputReserve)
  const augmentBudget = Math.floor(available * strategy.augmentRatio * _budgetFactor)
  const historyBudget = Math.floor(available * strategy.historyRatio)
  const historyTurns = Math.max(1, Math.floor(historyBudget / strategy.tokensPerTurn))

  return {
    totalWindow,
    systemPrompt: systemPromptTokens,
    outputReserve: strategy.outputReserve,
    available,
    augmentBudget,
    historyBudget,
    historyTurns,
    compressionTier: tier,
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// AUGMENT COMPRESSION CONFIG
// ═══════════════════════════════════════════════════════════════════════════════

export function getAugmentCompressionConfig(budget: ContextBudget): AugmentCompressionConfig {
  switch (budget.compressionTier) {
    case 'extreme':
      return {
        maxAugments: 3,
        forceCompression: 'compressed_fact',
        skipTypes: ['举一反三', '预测', '情绪外显', '思维盲点', '成长感知', '知识衰减'],
        maxAugmentTokens: 100,
      }
    case 'aggressive':
      return {
        maxAugments: 5,
        forceCompression: 'summary',
        skipTypes: ['思维盲点', '成长感知'],
        maxAugmentTokens: 200,
      }
    case 'light':
      return {
        maxAugments: 12,
        forceCompression: null,
        skipTypes: [],
        maxAugmentTokens: 500,
      }
    case 'none':
      return {
        maxAugments: 25,
        forceCompression: null,
        skipTypes: [],
        maxAugmentTokens: 1000,
      }
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// HISTORY TRIMMING
// ═══════════════════════════════════════════════════════════════════════════════

interface ChatTurn {
  user: string
  assistant: string
  ts: number
}

/**
 * 自适应历史裁剪：根据 budget 动态决定保留多少轮、每轮截断多少
 */
export function trimHistory(history: ChatTurn[], budget: ContextBudget): ChatTurn[] {
  if (history.length === 0) return history
  if (history.length <= budget.historyTurns) {
    // 轮数不超标，但单轮可能太长
    return applyPerTurnLimits(history, budget)
  }

  const maxTurns = budget.historyTurns

  switch (budget.compressionTier) {
    case 'extreme': {
      // 极限：首轮（任务上下文）+ 最近 N-1 轮，全部截断
      const first = history[0]
      const recent = history.slice(-(maxTurns - 1))
      return applyPerTurnLimits([
        { ...first, user: first.user.slice(0, 200), assistant: first.assistant.slice(0, 200) },
        ...recent,
      ], budget)
    }
    case 'aggressive': {
      // 积极：最近 N 轮，截断
      return applyPerTurnLimits(history.slice(-maxTurns), budget)
    }
    default: {
      // light / none：最近 N 轮
      return history.slice(-maxTurns)
    }
  }
}

function applyPerTurnLimits(turns: ChatTurn[], budget: ContextBudget): ChatTurn[] {
  // 每轮的 user/assistant 最大字符数
  const limits: Record<string, { user: number; assistant: number }> = {
    extreme:    { user: 200, assistant: 300 },
    aggressive: { user: 400, assistant: 600 },
    light:      { user: 800, assistant: 1200 },
    none:       { user: 2000, assistant: 4000 },
  }
  const limit = limits[budget.compressionTier]
  return turns.map(t => ({
    user: t.user.slice(0, limit.user),
    assistant: t.assistant.slice(0, limit.assistant),
    ts: t.ts,
  }))
}

// ═══════════════════════════════════════════════════════════════════════════════
// BUDGET FEEDBACK LOOP — 双向自适应
// 超预算 → 收紧；收紧后质量下降 → 放松。防止单向调节走极端
// ═══════════════════════════════════════════════════════════════════════════════

let _budgetFactor = 1.0
let _overBudgetCount = 0
let _qualityDropCount = 0

/** 记录实际 token 使用 vs 预算（由 prompt-builder 调用） */
export function recordBudgetUsage(actualTokens: number, budgetTokens: number): void {
  const ratio = budgetTokens > 0 ? actualTokens / budgetTokens : 0
  if (ratio > 0.9) {
    _overBudgetCount++
    if (_overBudgetCount >= 3) {
      _budgetFactor = Math.max(0.5, _budgetFactor * 0.85)
      _overBudgetCount = 0
      console.log(`[cc-soul][budget] tightened: factor=${_budgetFactor.toFixed(2)} (3× over 90%)`)
    }
  } else {
    _overBudgetCount = Math.max(0, _overBudgetCount - 1)  // 没超就缓慢恢复计数
  }
}

/** 记录质量反馈（由 quality.ts 调用）：收紧后质量下降 → 放松 */
export function recordBudgetQuality(qualityScore: number): void {
  if (qualityScore < 4 && _budgetFactor < 1.0) {
    _qualityDropCount++
    if (_qualityDropCount >= 3) {
      _budgetFactor = Math.min(1.0, _budgetFactor * 1.1)
      _qualityDropCount = 0
      console.log(`[cc-soul][budget] relaxed: factor=${_budgetFactor.toFixed(2)} (3× quality < 4)`)
    }
  } else {
    _qualityDropCount = Math.max(0, _qualityDropCount - 1)
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// DIAGNOSTIC
// ═══════════════════════════════════════════════════════════════════════════════

export function getBudgetDiagnostic(): string {
  const b = computeBudget()
  return [
    `[context-budget] window=${b.totalWindow}, tier=${b.compressionTier}`,
    `  available=${b.available} (augment=${b.augmentBudget}, history=${b.historyBudget})`,
    `  historyTurns=${b.historyTurns}, reserve=${b.outputReserve}`,
  ].join('\n')
}
