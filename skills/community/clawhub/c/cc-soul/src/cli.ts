/**
 * cc-soul — AI Backend Abstraction Layer
 *
 * Supports multiple backends:
 * - "cli": Claude CLI (default, for Max subscription users)
 * - "openai-compatible": Any OpenAI-compatible API (OpenAI/Ollama/智谱/通义/OpenRouter/Groq/...)
 *
 * All 29 modules call spawnCLI() — they don't know or care which backend is active.
 * Switching backend = change config, zero code changes.
 */

import { spawn, execSync } from 'child_process'
import { homedir } from 'os'
import { existsSync, readFileSync } from 'fs'
import type { PostResponseResult } from './types.ts'
import { DATA_DIR, MODULE_DIR, loadJson } from './persistence.ts'
import { resolve } from 'path'
import { extractJSON } from './utils.ts'

// ═══════════════════════════════════════════════════════════════════════════════
// CIRCUIT BREAKER — consecutive failures → cooldown
// ═══════════════════════════════════════════════════════════════════════════════
let _consecutiveFailures = 0
let _circuitBreakerUntil = 0
const CIRCUIT_BREAKER_THRESHOLD = 3
const CIRCUIT_BREAKER_COOLDOWN_MS = 3600000 // 1 hour

// ═══════════════════════════════════════════════════════════════════════════════
// AI BACKEND CONFIG — user-configured via ai_config.json or soul.json
// ═══════════════════════════════════════════════════════════════════════════════

interface AIConfig {
  backend: 'cli' | 'openai-compatible'
  cli_command: string
  cli_args: string[]
  api_base: string
  api_key: string
  api_model: string
  max_concurrent: number
}

// ai_config.json 固定路径，不跟 DATA_DIR 走——所有用户统一一个位置
const CC_SOUL_HOME = resolve(homedir(), '.cc-soul/data')
const AI_CONFIG_PATH = resolve(CC_SOUL_HOME, 'ai_config.json')
export { AI_CONFIG_PATH }

/**
 * Auto-detect AI backend from OpenClaw's config.
 * Strategy: follow whatever model OpenClaw is using — read model.primary,
 * resolve provider from config.json + models.json, use the same backend.
 * Priority: ai_config.json (user override) > openclaw model.primary > defaults
 */
let _fallbackApiConfig: AIConfig | null = null

// OpenClaw provider resolution removed — cc-soul uses independent LLM config only

function detectAIConfig(): AIConfig {
  // 确保 ~/.cc-soul/data/ 目录和 ai_config.json 模板存在
  try {
    const { mkdirSync, existsSync, writeFileSync } = require('fs')
    mkdirSync(CC_SOUL_HOME, { recursive: true })
    if (!existsSync(AI_CONFIG_PATH)) {
      writeFileSync(AI_CONFIG_PATH, JSON.stringify({
        backend: 'openai-compatible', api_base: '', api_key: '', api_model: '',
        _guide: '填写 api_base、api_key、api_model 三个字段即可。',
        _examples: {
          DeepSeek: { api_base: 'https://api.deepseek.com/v1', api_model: 'deepseek-chat' },
          OpenAI: { api_base: 'https://api.openai.com/v1', api_model: 'gpt-4o-mini' },
          Ollama: { api_base: 'http://localhost:11434/v1', api_key: 'ollama', api_model: 'qwen2.5:7b' },
        },
      }, null, 2))
      console.log(`[cc-soul][ai] 已创建配置模板: ${AI_CONFIG_PATH}`)
    }
  } catch {}
  // 1. ~/.cc-soul/data/ai_config.json
  const userConfig = loadJson<Partial<AIConfig>>(AI_CONFIG_PATH, {})
  if (userConfig.backend && userConfig.api_base && userConfig.api_key) {
    console.log(`[cc-soul][ai] using ai_config.json: ${userConfig.api_model || 'unknown'} @ ${userConfig.api_base}`)
    return {
      backend: userConfig.backend,
      cli_command: userConfig.cli_command || '',
      cli_args: userConfig.cli_args || [],
      api_base: userConfig.api_base || '',
      api_key: userConfig.api_key || '',
      api_model: userConfig.api_model || '',
      max_concurrent: userConfig.max_concurrent || 5,
    }
  }

  // 2. 无配置 → 纯 NAM 模式（核心功能全部可用，后台 LLM 任务跳过）
  console.log(`[cc-soul][ai] 未配置 LLM，纯 NAM 模式。配置方法：编辑 ${AI_CONFIG_PATH} 填入 api_base、api_key、api_model`)
  return {
    backend: 'openai-compatible',
    cli_command: '',
    cli_args: [],
    api_base: '',
    api_key: '',
    api_model: '',
    max_concurrent: 5,
  }
}

// ── LLM 服务商预置表 ──
export const LLM_PROVIDERS: Record<string, { api_base: string; default_model: string; name: string }> = {
  deepseek:    { api_base: 'https://api.deepseek.com/v1',            default_model: 'deepseek-chat',                name: 'DeepSeek' },
  openai:      { api_base: 'https://api.openai.com/v1',              default_model: 'gpt-4o-mini',                  name: 'OpenAI' },
  siliconflow: { api_base: 'https://api.siliconflow.cn/v1',          default_model: 'Qwen/Qwen2.5-7B-Instruct',    name: '硅基流动' },
  volcengine:  { api_base: 'https://ark.cn-beijing.volces.com/api/v3', default_model: '',                           name: '火山引擎' },
  ollama:      { api_base: 'http://localhost:11434/v1',               default_model: 'qwen2.5:7b',                  name: 'Ollama（本地）' },
}

// ── LLM 连通性验证 ──
let _llmValidated: { ok: boolean; error?: string; ts: number } | null = null

export async function validateLLM(): Promise<{ ok: boolean; error?: string }> {
  if (!hasLLM()) return { ok: false, error: '未配置 LLM' }

  const cfg = _fallbackApiConfig || aiConfig
  if (!cfg.api_base || !cfg.api_key) return { ok: false, error: '未配置 api_base 或 api_key' }

  try {
    const resp = await fetch(cfg.api_base + '/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${cfg.api_key}`,
      },
      body: JSON.stringify({
        model: cfg.api_model,
        messages: [{ role: 'user', content: 'hi' }],
        max_tokens: 1,
      }),
      signal: AbortSignal.timeout(10000),
    })
    if (resp.ok) {
      _llmValidated = { ok: true, ts: Date.now() }
      return { ok: true }
    }
    const body = await resp.text().catch(() => '')
    let error = `HTTP ${resp.status}`
    if (resp.status === 401) error = 'API Key 无效'
    else if (resp.status === 404) error = 'API 地址错误或模型不存在'
    else if (body) error += `: ${body.slice(0, 100)}`
    _llmValidated = { ok: false, error, ts: Date.now() }
    return { ok: false, error }
  } catch (e: any) {
    const error = e.name === 'TimeoutError' ? 'API 连接超时（10s）' : `连接失败: ${e.message}`
    _llmValidated = { ok: false, error, ts: Date.now() }
    return { ok: false, error }
  }
}

export function getLLMStatus(): { configured: boolean; connected: boolean; model: string; error?: string } {
  const cfg = _fallbackApiConfig || aiConfig
  const configured = !!(cfg.api_base && cfg.api_key)
  return {
    configured,
    connected: _llmValidated?.ok ?? false,
    model: cfg.api_model || '',
    error: _llmValidated?.error,
  }
}

/** 保存 LLM 配置到 ai_config.json 并立即生效 */
export function saveLLMConfig(api_base: string, api_key: string, api_model: string) {
  const { writeFileSync } = require('fs')
  const config = {
    backend: 'openai-compatible',
    api_base,
    api_key,
    api_model,
    max_concurrent: 5,
  }
  writeFileSync(AI_CONFIG_PATH, JSON.stringify(config, null, 2))
  // 立即生效
  aiConfig.backend = 'openai-compatible'
  aiConfig.api_base = api_base
  aiConfig.api_key = api_key
  aiConfig.api_model = api_model
  // 同步 fallback
  _fallbackApiConfig = { ...aiConfig, cli_command: '', cli_args: [] }
  _llmValidated = null
  console.log(`[cc-soul][ai] config saved & activated: ${api_model} @ ${api_base}`)
}

// resolveProviderFallback removed — no longer needed

export function getFallbackApiConfig(): AIConfig | null { return _fallbackApiConfig }
export function setFallbackApiConfig(config: AIConfig) {
  _fallbackApiConfig = config
  // If setting from soul-api /config, also update main config so direct calls work
  if (config.api_base && config.api_key && config.api_model) {
    aiConfig.backend = 'openai-compatible'
    aiConfig.api_base = config.api_base
    aiConfig.api_key = config.api_key
    aiConfig.api_model = config.api_model
    console.log(`[cc-soul][ai] main config updated: ${config.api_model} @ ${config.api_base}`)
  }
}

let aiConfig: AIConfig = detectAIConfig()
let _configMtime = 0
try { _configMtime = require('fs').statSync(AI_CONFIG_PATH).mtimeMs } catch {}

export function loadAIConfig() {
  aiConfig = detectAIConfig()
  try { _configMtime = require('fs').statSync(AI_CONFIG_PATH).mtimeMs } catch {}
}

/** 检查 ai_config.json 是否被修改，是则热加载并自动验证连通性 */
export function hotReloadIfChanged() {
  try {
    const mtime = require('fs').statSync(AI_CONFIG_PATH).mtimeMs
    if (mtime > _configMtime) {
      _configMtime = mtime
      aiConfig = detectAIConfig()
      _llmValidated = null
      console.log(`[cc-soul][ai] ai_config.json changed, hot-reloaded: ${aiConfig.api_model || 'none'}`)
      // 自动验证连通性
      if (hasLLM()) {
        validateLLM().then(r => {
          if (r.ok) console.log(`[cc-soul][ai] ✅ 连接验证通过: ${aiConfig.api_model}`)
          else console.log(`[cc-soul][ai] ❌ 连接验证失败: ${r.error}`)
        }).catch(() => {})
      }
    }
  } catch {}
}

export function getAIConfig(): AIConfig {
  return aiConfig
}

// ═══════════════════════════════════════════════════════════════════════════════
// SPAWN CLI — unified AI invocation (routes to correct backend)
// ═══════════════════════════════════════════════════════════════════════════════

let activeCLICount = 0

// ── Agent 优先机制 ──
let agentBusy = false
export function getAgentBusy(): boolean { return agentBusy }
export function setAgentBusy(busy: boolean) {
  agentBusy = busy
  // Agent 释放后，自动处理排队任务
  if (!busy) drainQueue()
}

// ── CLI health monitoring ──
let consecutiveFailures = 0
const MAX_FAILURES_BEFORE_DEGRADE = 1
let degradedMode = false
let degradedAt = 0
const DEGRADE_RECOVERY_MS = 5 * 60 * 1000 // try recovery after 5 min

export function isCliDegraded(): boolean { return degradedMode }

/** Check if LLM is available (not degraded + valid config) */
export function hasLLM(): boolean {
  if (isCliDegraded()) return false
  const cfg = _fallbackApiConfig || aiConfig
  if (cfg?.backend === 'openai-compatible' && cfg.api_base && cfg.api_key) return true
  if (cfg?.backend === 'cli' && cfg.cli_command) return true
  return false
}

// ── 任务队列（agent busy 时排队，释放后自动执行）──
interface QueuedTask {
  prompt: string
  callback: (output: string) => void
  timeoutMs: number
  label: string
}
const taskQueue: QueuedTask[] = []
const MAX_QUEUE_SIZE = 10

function drainQueue() {
  while (taskQueue.length > 0 && !agentBusy && activeCLICount < aiConfig.max_concurrent) {
    const task = taskQueue.shift()!
    console.log(`[cc-soul][ai] 队列取出: ${task.label} (剩余 ${taskQueue.length})`)
    executeTask(task.prompt, task.callback, task.timeoutMs, task.label)
  }
}

// ── 任务完成通知 ──
type TaskDoneCallback = (label: string, elapsed: number, success: boolean) => void
let onTaskDone: TaskDoneCallback | null = null
export function setOnTaskDone(cb: TaskDoneCallback) { onTaskDone = cb }

// ── 任务状态追踪 ──
interface CLITask {
  label: string
  startedAt: number
  hasOutput: boolean
}
const activeTasks = new Map<number, CLITask>()
let taskIdCounter = 0

export function getActiveTaskStatus(): string {
  if (activeTasks.size === 0 && taskQueue.length === 0) return ''
  const now = Date.now()
  const running = [...activeTasks.values()]
    .map(t => {
      const elapsed = Math.round((now - t.startedAt) / 1000)
      const status = t.hasOutput ? '⚙️' : '⏳'
      return `${status} ${t.label} (${elapsed}s)`
    })
  const queued = taskQueue.length > 0 ? [`📋 排队 ${taskQueue.length} 个`] : []
  return [...running, ...queued].join(' | ')
}

const HARD_TIMEOUT_MS = 30000 // 30s hard ceiling — prevents infinite hangs when LLM stalls

// ── Workload 成本追踪（学自 Claude Code billing headers）──
const _workloadCosts = new Map<string, { calls: number; tokens: number }>()
export function getWorkloadCosts(): Record<string, { calls: number; tokens: number }> {
  return Object.fromEntries(_workloadCosts)
}
function trackWorkload(label: string, estimatedTokens: number): void {
  const workload = label.split(':')[0] || 'unknown'  // "distill:L1" → "distill"
  const entry = _workloadCosts.get(workload) ?? { calls: 0, tokens: 0 }
  entry.calls++
  entry.tokens += estimatedTokens
  _workloadCosts.set(workload, entry)
}

export function spawnCLI(prompt: string, callback: (output: string) => void, timeoutMs = 120000, label = 'ai-task') {
  // Circuit breaker: skip if in cooldown
  if (Date.now() < _circuitBreakerUntil) {
    console.log(`[cc-soul][ai] circuit breaker OPEN: ${_consecutiveFailures} consecutive failures, cooldown until ${new Date(_circuitBreakerUntil).toISOString()}`)
    callback('')
    return
  }
  // 成本追踪：按 workload 分类记录调用次数和估算 token
  trackWorkload(label, Math.ceil(prompt.length * 0.8))
  // Hard timeout: independent 30s safety net — if backend never calls back, force-resolve
  // Does NOT override caller's timeoutMs (that's passed to the backend as-is)
  let callbackSettled = false
  const hardTimer = setTimeout(() => {
    if (!callbackSettled) {
      callbackSettled = true
      console.log(`[cc-soul][ai] HARD TIMEOUT (${HARD_TIMEOUT_MS}ms) for ${label} — forcing callback('')`)
      callback('')
    }
  }, HARD_TIMEOUT_MS)

  const safeCallback = (result: string) => {
    if (callbackSettled) return // already timed out, discard late result
    callbackSettled = true
    clearTimeout(hardTimer)
    // Circuit breaker tracking
    if (result === '') {
      _consecutiveFailures++
      if (_consecutiveFailures >= CIRCUIT_BREAKER_THRESHOLD) {
        _circuitBreakerUntil = Date.now() + CIRCUIT_BREAKER_COOLDOWN_MS
        console.log(`[cc-soul][ai] circuit breaker OPEN: ${_consecutiveFailures} consecutive failures, cooldown until ${new Date(_circuitBreakerUntil).toISOString()}`)
      }
    } else {
      _consecutiveFailures = 0
    }
    callback(result)
  }

  // If fallback API is configured (from openclaw providers), prefer it for background tasks
  console.log(`[cc-soul][ai] spawnCLI: backend=${aiConfig.backend} fallback=${!!_fallbackApiConfig} label=${label}`)
  if (aiConfig.backend === 'cli' && _fallbackApiConfig) {
    callOpenAICompatibleDirect(_fallbackApiConfig, prompt, (result) => {
      if (onTaskDone) onTaskDone(label, 0, result.length > 0)
      safeCallback(result)
    }, timeoutMs)
    return
  }

  // One-shot CLI with strict serial queue (max 1 concurrent)
  // No persistent daemon — each task spawns claude -p, gets result, process exits cleanly
  if (activeCLICount >= 1) {
    // Already one task running — queue it
    if (taskQueue.length >= MAX_QUEUE_SIZE) {
      console.log(`[cc-soul][ai] queue full (${MAX_QUEUE_SIZE}), dropping: ${label}`)
      safeCallback('')
      return
    }
    taskQueue.push({ prompt, callback: safeCallback, timeoutMs, label })
    return
  }
  // No task running — execute immediately
  executeTask(prompt, safeCallback, timeoutMs, label)
}

function executeTask(prompt: string, callback: (output: string) => void, timeoutMs: number, label: string) {
  activeCLICount++ // increment before async dispatch to prevent over-concurrency in drainQueue
  const taskId = taskIdCounter++
  const startedAt = Date.now()

  // 包装 callback：完成时通知 + 释放 + 处理队列
  const wrappedCallback = (result: string) => {
    const elapsed = Math.round((Date.now() - startedAt) / 1000)
    const success = result.length > 0
    // 通知完成
    if (onTaskDone) onTaskDone(label, elapsed, success)
    // 原始回调
    callback(result)
    // 处理排队任务
    setTimeout(() => drainQueue(), 100)
  }

  if (aiConfig.backend === 'openai-compatible') {
    activeTasks.set(taskId, { label, startedAt, hasOutput: false })
    callOpenAICompatible(prompt, (result) => {
      activeTasks.delete(taskId)
      wrappedCallback(result)
    }, timeoutMs)
  } else {
    callCLI(prompt, wrappedCallback, timeoutMs, label, taskId)
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// BACKEND 1: CLI — One-shot per task (openclaw manages session persistence)
// Each task spawns `claude -p`, gets result, process exits cleanly.
// Session continuity is handled by openclaw's sessionMode/--resume mechanism.
// ═══════════════════════════════════════════════════════════════════════════════

function callCLI(prompt: string, callback: (output: string) => void, timeoutMs: number, label: string, taskId: number) {
  activeTasks.set(taskId, { label, startedAt: Date.now(), hasOutput: false })
  let settled = false
  function release() {
    if (!settled) { settled = true; activeCLICount--; activeTasks.delete(taskId) }
  }
  try {
    const proc = spawn(aiConfig.cli_command, [...aiConfig.cli_args, prompt], {
      cwd: homedir(), timeout: timeoutMs, stdio: ['pipe', 'pipe', 'pipe'],
    })
    proc.stdin?.end()
    // Safety: force kill if process doesn't exit within timeout + 10s grace
    const killTimer = setTimeout(() => {
      if (proc.pid) {
        try { process.kill(proc.pid, 0); process.kill(proc.pid, 'SIGKILL'); console.log(`[cc-soul][ai] force-killed stuck PID ${proc.pid}`) } catch {}
      }
    }, timeoutMs + 10000)
    proc.on('close', () => clearTimeout(killTimer))
    const MAX_OUTPUT = 512 * 1024
    let output = ''

    proc.stdout?.on('data', (d: Buffer) => {
      const task = activeTasks.get(taskId)
      if (task) task.hasOutput = true
      if (output.length < MAX_OUTPUT) {
        output += d.toString()
        if (output.length > MAX_OUTPUT) output = output.slice(0, MAX_OUTPUT)
      }
    })
    proc.stderr?.on('data', () => {})

    const heartbeat = setInterval(() => {
      const task = activeTasks.get(taskId)
      const elapsed = task ? Math.round((Date.now() - task.startedAt) / 1000) : 0
      console.log(`[cc-soul][ai] ${label}: ${task?.hasOutput ? '工作中' : '等待中'} (${elapsed}s, ${Math.round(output.length / 1024)}kb)`)
    }, 30000)

    proc.on('close', (code: number | null, signal: string | null) => {
      clearInterval(heartbeat)
      const elapsed = Math.round((Date.now() - (activeTasks.get(taskId)?.startedAt || Date.now())) / 1000)
      release()
      if (signal === 'SIGTERM') {
        console.log(`[cc-soul][ai] ${label}: 超时 (${timeoutMs}ms)`)
        consecutiveFailures++
        if (consecutiveFailures >= MAX_FAILURES_BEFORE_DEGRADE && !degradedMode) {
          degradedMode = true; degradedAt = Date.now()
          console.error('[cc-soul][ai] CLI degraded mode: too many consecutive failures')
        }
        callback('')
        return
      }
      const trimmed = output.trim()
      // Detect known CLI error patterns in stdout (claude CLI may output errors to stdout)
      const isErrorOutput = /Invalid API key|API key expired|authentication failed|rate limit|overloaded/i.test(trimmed)
      if (isErrorOutput || code !== 0) {
        consecutiveFailures++
        if (consecutiveFailures >= MAX_FAILURES_BEFORE_DEGRADE && !degradedMode) {
          degradedMode = true; degradedAt = Date.now()
          console.error(`[cc-soul][ai] CLI degraded mode: too many failures (last: ${trimmed.slice(0, 80)})`)
        }
        console.log(`[cc-soul][ai] ${label}: CLI 错误 (code=${code}, ${trimmed.slice(0, 80)})`)
        callback('')
        return
      }
      consecutiveFailures = 0; degradedMode = false
      console.log(`[cc-soul][ai] ${label}: 完成 (${elapsed}s, ${output.length}bytes)`)
      callback(trimmed)
    })
    proc.on('error', (err: Error) => {
      clearInterval(heartbeat); release()
      consecutiveFailures++
      console.error(`[cc-soul][ai] ${label}: 错误 ${err.message}`)
      callback('')
    })
  } catch (err: any) {
    release()
    console.error(`[cc-soul][ai] CLI spawn failed: ${err.message}`)
    callback('')
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// POST-REPLY CLEANUP: kill gateway-spawned claude processes to free concurrency
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Kill claude CLI processes spawned by the gateway (CWD contains .openclaw/hooks).
 * Safe: never touches user terminal claude processes.
 * Called after message:sent to immediately free concurrency slots.
 */
export function killGatewayClaude() {
  // OpenClaw manages CLI lifecycle via ProcessSupervisor + sessionMode.
  // cc-soul should NOT kill any claude processes.
}

// ═══════════════════════════════════════════════════════════════════════════════
// BACKEND 2: OpenAI-compatible API (covers OpenAI/Ollama/智谱/通义/OpenRouter/Groq/...)
// ═══════════════════════════════════════════════════════════════════════════════

async function callOpenAICompatible(prompt: string, callback: (output: string) => void, timeoutMs: number) {
  const controller = new AbortController()
  const timer = setTimeout(() => controller.abort(), timeoutMs)

  try {
    const resp = await fetch(`${aiConfig.api_base}/chat/completions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${aiConfig.api_key}`,
      },
      body: JSON.stringify({
        model: aiConfig.api_model,
        messages: [{ role: 'user', content: prompt }],
        max_tokens: 2048,
      }),
      signal: controller.signal,
    })

    clearTimeout(timer)

    if (!resp.ok) {
      const errText = await resp.text().catch(() => '')
      console.error(`[cc-soul][ai] API error ${resp.status}: ${errText.slice(0, 200)}`)
      consecutiveFailures++
      if (consecutiveFailures >= MAX_FAILURES_BEFORE_DEGRADE && !degradedMode) {
        degradedMode = true
        degradedAt = Date.now()
        console.error('[cc-soul][ai] CLI degraded mode: too many consecutive failures')
      }
      callback('')
      return
    }

    const data = await resp.json() as any
    const content = data.choices?.[0]?.message?.content || ''
    consecutiveFailures = 0
    degradedMode = false
    callback(content.trim())
  } catch (e: any) {
    clearTimeout(timer)
    consecutiveFailures++
    if (consecutiveFailures >= MAX_FAILURES_BEFORE_DEGRADE && !degradedMode) {
      degradedMode = true
      degradedAt = Date.now()
      console.error('[cc-soul][ai] CLI degraded mode: too many consecutive failures')
    }
    if (e.name === 'AbortError') {
      console.log(`[cc-soul][ai] API timeout after ${timeoutMs}ms`)
    } else {
      console.error(`[cc-soul][ai] API error: ${e.message}`)
    }
    callback('')
  } finally {
    activeCLICount--
  }
}

/**
 * Direct API call with explicit config (no global aiConfig mutation).
 * Used for fallback API calls when main backend is CLI.
 */
async function callOpenAICompatibleDirect(cfg: AIConfig, prompt: string, callback: (output: string) => void, timeoutMs: number) {
  const controller = new AbortController()
  const timer = setTimeout(() => controller.abort(), timeoutMs)
  try {
    const resp = await fetch(`${cfg.api_base}/chat/completions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${cfg.api_key}`,
      },
      body: JSON.stringify({
        model: cfg.api_model,
        messages: [{ role: 'user', content: prompt }],
        max_tokens: 2048,
      }),
      signal: controller.signal,
    })
    clearTimeout(timer)
    if (!resp.ok) {
      const errText = await resp.text().catch(() => '')
      console.error(`[cc-soul][ai] fallback API error ${resp.status}: ${errText.slice(0, 200)}`)
      callback('')
      return
    }
    const data = await resp.json() as any
    const content = data.choices?.[0]?.message?.content || ''
    console.log(`[cc-soul][ai] fallback API ok: ${content.length} chars`)
    callback(content.trim())
  } catch (e: any) {
    clearTimeout(timer)
    console.error(`[cc-soul][ai] fallback API error: ${e.message}`)
    callback('')
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// BACKEND 3: Anthropic API (Haiku) — dedicated channel for background tasks
// ═══════════════════════════════════════════════════════════════════════════════

const HAIKU_MODEL = 'claude-haiku-4-5-20251001'
let anthropicApiKey = ''

function getAnthropicApiKey(): string {
  if (anthropicApiKey) return anthropicApiKey
  try {
    const raw = JSON.parse(readFileSync(OPENCLAW_CONFIG_PATH, 'utf-8'))
    anthropicApiKey = raw?.env?.ANTHROPIC_API_KEY || ''
  } catch { /* ignore */ }
  return anthropicApiKey
}

/**
 * Call Anthropic Messages API directly (Haiku model).
 * Independent of CLI — no concurrency conflict, no queue.
 */
async function callAnthropicHaiku(prompt: string, callback: (output: string) => void, timeoutMs: number) {
  const apiKey = getAnthropicApiKey()
  if (!apiKey) {
    console.log('[cc-soul][haiku] no ANTHROPIC_API_KEY, falling back to CLI')
    callback('')
    return
  }

  const controller = new AbortController()
  const timer = setTimeout(() => controller.abort(), timeoutMs)

  try {
    const resp = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': apiKey,
        'anthropic-version': '2023-06-01',
      },
      body: JSON.stringify({
        model: HAIKU_MODEL,
        max_tokens: 2048,
        messages: [{ role: 'user', content: prompt }],
      }),
      signal: controller.signal,
    })

    clearTimeout(timer)

    if (!resp.ok) {
      const errText = await resp.text().catch(() => '')
      console.error(`[cc-soul][haiku] API error ${resp.status}: ${errText.slice(0, 200)}`)
      callback('')
      return
    }

    const data = await resp.json() as any
    const content = data.content?.[0]?.text || ''
    console.log(`[cc-soul][haiku] ok: ${content.length} chars, ${data.usage?.input_tokens || 0}+${data.usage?.output_tokens || 0} tokens`)
    callback(content.trim())
  } catch (e: any) {
    clearTimeout(timer)
    if (e.name === 'AbortError') {
      console.log(`[cc-soul][haiku] timeout after ${timeoutMs}ms`)
    } else {
      console.error(`[cc-soul][haiku] error: ${e.message}`)
    }
    callback('')
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// LLM BATCH QUEUE — defer non-urgent tasks to low-activity hours (2-5 AM)
// ═══════════════════════════════════════════════════════════════════════════════

interface BatchTask {
  prompt: string
  callback: (result: string) => void
  priority: number
  label: string
  queuedAt: number
}

const batchQueue: BatchTask[] = []
const BATCH_MAX = 20
const BATCH_PER_TICK = 5

function isBatchWindow(): boolean {
  const h = new Date().getHours()
  return h >= 2 && h < 5
}

export function queueLLMTask(prompt: string, callback: (result: string) => void, priority = 0, label = 'batch') {
  batchQueue.push({ prompt, callback, priority, label, queuedAt: Date.now() })
  batchQueue.sort((a, b) => b.priority - a.priority)
  console.log(`[cc-soul][batch] queued: ${label} (pri=${priority}, total=${batchQueue.length})`)
  // Overflow: process highest-priority immediately regardless of time
  if (batchQueue.length > BATCH_MAX) {
    console.log(`[cc-soul][batch] overflow (>${BATCH_MAX}), draining top ${BATCH_PER_TICK}`)
    drainBatchQueue(BATCH_PER_TICK)
  }
}

export function drainBatchQueue(limit = BATCH_PER_TICK) {
  let processed = 0
  while (batchQueue.length > 0 && processed < limit) {
    const task = batchQueue.shift()!
    console.log(`[cc-soul][batch] processing: ${task.label} (remaining=${batchQueue.length})`)
    spawnCLI(task.prompt, task.callback, 120000, `batch:${task.label}`)
    processed++
  }
}

/** Called from heartbeat — processes batch queue during 2-5 AM */
export function tickBatchQueue() {
  if (batchQueue.length === 0) return
  if (!isBatchWindow()) {
    console.log(`[cc-soul][batch] ${batchQueue.length} tasks queued, waiting for 2-5 AM window`)
    return
  }
  console.log(`[cc-soul][batch] AM window active, draining up to ${BATCH_PER_TICK}`)
  drainBatchQueue()
}

export function getBatchQueueStatus(): { queued: number; labels: string[] } {
  return { queued: batchQueue.length, labels: batchQueue.slice(0, 5).map(t => t.label) }
}

// ═══════════════════════════════════════════════════════════════════════════════
// MERGED POST-RESPONSE ANALYSIS
// ═══════════════════════════════════════════════════════════════════════════════

const EMPTY_RESULT: PostResponseResult = {
  memories: [],
  entities: [],
  satisfaction: 'NEUTRAL',
  quality: { score: 5, issues: [] },
  emotion: 'neutral',
  reflection: null,
}

export function runPostResponseAnalysis(
  userMsg: string,
  botResponse: string,
  callback: (result: PostResponseResult) => void,
) {
  const prompt = `分析以下对话，严格按JSON输出（不要其他文字）：

用户: "${userMsg.slice(0, 500)}"
回复: "${botResponse.slice(0, 500)}"

请同时完成以下分析：
1. memories: 提取值得长期记住的信息。每条: {"content":"内容","scope":"类型","visibility":"可见性"}，scope只能是: preference/fact/event/opinion。visibility只能是: global(通用知识/技术事实，对所有人有用)/channel(频道相关，只在当前群有用)/private(个人相关，只对当前用户有用)。没有就空数组。
2. memory_ops: 基于对话内容判断是否需要修改已有记忆。每条: {"action":"update/delete","keyword":"匹配关键词","reason":"原因","new_content":"新内容(仅update需要)"}。例如用户说"我换工作了"→删除旧公司记忆+新增新公司。没有就空数组。
3. entities: 提取人名、项目名、公司名、技术名。每条: {"name":"名","type":"类型","relation":"关系"}，type只能是: person/project/company/tech/place。没有就空数组。
4. satisfaction: 判断用户对回复的满意度: POSITIVE/NEUTRAL/NEGATIVE/TOO_VERBOSE
5. quality: 回复质量评分1-10 + 问题列表。{"score":N,"issues":["问题"]}
6. emotion: 对话情感标签: neutral/warm/important/painful/funny
7. reflection: 回复有什么遗憾或可改进的？1句话，没有就null

JSON格式(严格):
{"memories":[],"memory_ops":[],"entities":[],"satisfaction":"NEUTRAL","quality":{"score":5,"issues":[]},"emotion":"neutral","reflection":null}`

  spawnCLI(
    prompt,
    (output) => {
      try {
        const result = extractJSON(output)
        if (result) {
          // ── Anti-hallucination: validate & clamp AI self-assessment ──
          const rawScore = result.quality?.score
          const clampedScore = typeof rawScore === 'number'
            ? Math.max(1, Math.min(10, Math.round(rawScore)))
            : 5
          // Heuristic cross-check: if AI says POSITIVE but user msg is very short
          // or contains negative signals, downgrade to NEUTRAL
          let satisfaction = result.satisfaction || 'NEUTRAL'
          const validSatisfactions = ['POSITIVE', 'NEUTRAL', 'NEGATIVE', 'TOO_VERBOSE']
          if (!validSatisfactions.includes(satisfaction)) satisfaction = 'NEUTRAL'
          const userLower = userMsg.toLowerCase()
          const hasNegativeSignal = /不行|不对|错了|有问题|别|不要|不好|差|垃圾|废话|no|wrong|bad|stop|don't/.test(userLower)
          const hasPositiveSignal = /谢|好的|棒|赞|感谢|不错|厉害|可以|thank|great|good|nice|perfect|awesome/.test(userLower)
          if (satisfaction === 'POSITIVE' && hasNegativeSignal && !hasPositiveSignal) {
            console.log(`[cc-soul][anti-hallucination] satisfaction POSITIVE→NEUTRAL: user msg has negative signals`)
            satisfaction = 'NEUTRAL'
          }
          if (satisfaction === 'NEGATIVE' && hasPositiveSignal && !hasNegativeSignal) {
            console.log(`[cc-soul][anti-hallucination] satisfaction NEGATIVE→NEUTRAL: user msg has positive signals`)
            satisfaction = 'NEUTRAL'
          }
          // Cap memories per turn to prevent hallucinated bulk extraction
          const MAX_MEMORIES_PER_TURN = 5
          const MAX_OPS_PER_TURN = 3
          const memories = (result.memories || []).slice(0, MAX_MEMORIES_PER_TURN).map((m: any) => ({
            content: m.content,
            scope: m.scope,
            visibility: m.visibility || undefined,
          })).filter((m: any) => m.content && m.content.length >= 3)
          const memoryOps = (result.memory_ops || []).slice(0, MAX_OPS_PER_TURN).map((op: any) => ({
            action: op.action as 'update' | 'delete',
            keyword: op.keyword || '',
            reason: op.reason || '',
            newContent: op.new_content || '',
          }))

          callback({
            memories,
            memoryOps,
            entities: (result.entities || []).slice(0, 10),
            satisfaction,
            quality: { score: clampedScore, issues: result.quality?.issues || [] },
            emotion: result.emotion || 'neutral',
            reflection: result.reflection || null,
          })
          return
        }
      } catch (e: any) {
        console.error(`[cc-soul][ai] analysis parse error: ${e.message}`)
      }
      callback({ ...EMPTY_RESULT })
    },
    45000,
  )
}

// ═══════════════════════════════════════════════════════════════════════════════
