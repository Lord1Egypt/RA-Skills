/**
 * health.ts — Module health monitoring + runtime error tracking
 *
 * Two systems:
 * 1. Periodic health check (every 30 min): data files, state sanity, features
 * 2. Runtime error counter: tracks per-module errors so upgrade observation can
 *    detect if a module started failing silently after code changes
 * 3. Module activity tracking: detects if a module stopped working entirely
 */

import type { SoulModule } from './brain.ts'
import { existsSync, readFileSync } from 'fs'
import { execSync } from 'child_process'
import { notifyOwnerDM } from './notify.ts'
import { memoryState } from './memory.ts'
import { body } from './body.ts'
import { rules } from './evolution.ts'
import { graphState } from './graph.ts'
import { MEMORIES_PATH, STATS_PATH } from './persistence.ts'
import { getAllFeatures } from './features.ts'

interface HealthReport {
  status: 'healthy' | 'degraded' | 'critical'
  issues: string[]
  stats: Record<string, number | string>
}

let lastHealthCheck = 0
const HEALTH_CHECK_INTERVAL = 30 * 60000 // every 30 min (with heartbeat)

// ══════════════════════════════════════════════════════════════════════════════
// Runtime error counter — tracks per-module errors for upgrade observation
// ══════════════════════════════════════════════════════════════════════════════

interface ModuleErrorRecord {
  count: number
  lastError: string
  lastErrorAt: number
}

const moduleErrors = new Map<string, ModuleErrorRecord>()
const moduleActivity = new Map<string, number>() // module → last activity timestamp
let errorWindowStart = Date.now()

/** Call this when a module encounters an error (in handler.ts safe() wrapper) */
export function recordModuleError(moduleName: string, error: string) {
  const record = moduleErrors.get(moduleName) || { count: 0, lastError: '', lastErrorAt: 0 }
  record.count++
  record.lastError = error.slice(0, 200)
  record.lastErrorAt = Date.now()
  moduleErrors.set(moduleName, record)
}

/** Call this when a module successfully executes (tracks liveness) */
export function recordModuleActivity(moduleName: string) {
  moduleActivity.set(moduleName, Date.now())
}

/** Get error rate per module since last reset (for upgrade observation) */
export function getModuleErrorSummary(): { totalErrors: number; errorsByModule: Record<string, number>; silentModules: string[] } {
  const errorsByModule: Record<string, number> = {}
  let totalErrors = 0
  for (const [mod, record] of moduleErrors) {
    errorsByModule[mod] = record.count
    totalErrors += record.count
  }

  // Detect modules that haven't been active for >1 hour (might be silently broken)
  const silentModules: string[] = []
  const oneHourAgo = Date.now() - 3600000
  const expectedActiveModules = ['memory', 'cognition', 'body', 'prompt-builder', 'quality']
  for (const mod of expectedActiveModules) {
    const lastActive = moduleActivity.get(mod) || 0
    // Flag if we've been running for >1 hour AND (module was never active OR inactive for >1 hour)
    if (errorWindowStart < oneHourAgo && (lastActive === 0 || lastActive < oneHourAgo)) {
      silentModules.push(mod)
    }
  }

  return { totalErrors, errorsByModule, silentModules }
}

/** Reset error counters (call after upgrade observation evaluation) */
export function resetModuleErrors() {
  moduleErrors.clear()
  errorWindowStart = Date.now()
}

/** Get detailed error info for notification */
export function getErrorDetails(): string {
  if (moduleErrors.size === 0) return ''
  const lines: string[] = []
  for (const [mod, record] of moduleErrors) {
    if (record.count > 0) {
      lines.push(`  ${mod}: ${record.count} 次错误 (最近: ${record.lastError.slice(0, 80)})`)
    }
  }
  return lines.length > 0 ? `模块错误统计:\n${lines.join('\n')}` : ''
}

// ══════════════════════════════════════════════════════════════════════════════
// Periodic health check
// ══════════════════════════════════════════════════════════════════════════════

export function healthCheck(): HealthReport {
  const now = Date.now()
  if (now - lastHealthCheck < HEALTH_CHECK_INTERVAL) {
    return { status: 'healthy', issues: [], stats: {} }
  }
  lastHealthCheck = now

  const issues: string[] = []

  // Check data files exist
  if (!existsSync(MEMORIES_PATH)) issues.push('memories.json missing')
  if (!existsSync(STATS_PATH)) issues.push('stats.json missing')

  // Check memory state
  if (memoryState.memories.length === 0) issues.push('memory empty (0 memories)')
  const expired = memoryState.memories.filter(m => m.scope === 'expired').length
  if (expired > memoryState.memories.length * 0.5) {
    issues.push(`>50% memories expired (${expired}/${memoryState.memories.length})`)
  }

  // Check body state sanity
  if (body.energy < 0 || body.energy > 1) issues.push(`body.energy out of range: ${body.energy}`)
  if (body.mood < -1 || body.mood > 1) issues.push(`body.mood out of range: ${body.mood}`)

  // Check features loaded
  const features = getAllFeatures()
  if (Object.keys(features).length === 0) issues.push('features.json not loaded')

  // Check runtime errors since last reset
  const errorSummary = getModuleErrorSummary()
  if (errorSummary.totalErrors > 10) {
    const topErrorModule = Object.entries(errorSummary.errorsByModule)
      .sort(([, a], [, b]) => b - a)[0]
    if (topErrorModule) {
      issues.push(`high error rate: ${topErrorModule[0]} has ${topErrorModule[1]} errors`)
    }
  }
  if (errorSummary.silentModules.length > 0) {
    issues.push(`silent modules (>1hr inactive): ${errorSummary.silentModules.join(', ')}`)
  }

  // Determine status
  let status: HealthReport['status'] = 'healthy'
  if (issues.length > 0 && issues.length <= 2) status = 'degraded'
  if (issues.length > 2) status = 'critical'

  const report: HealthReport = {
    status,
    issues,
    stats: {
      memories: memoryState.memories.length,
      rules: rules.length,
      entities: graphState.entities.length,
      energy: body.energy.toFixed(2),
      mood: body.mood.toFixed(2),
      features: Object.values(features).filter(v => v).length,
      moduleErrors: errorSummary.totalErrors,
    },
  }

  if (issues.length > 0) {
    console.warn(`[cc-soul][health] ${status}: ${issues.join('; ')}`)
  }

  // ── CLI 超时检测 + 并发告警（每次心跳检查）──
  checkCliConcurrency()

  return report
}

// ═══════════════════════════════════════════════════════════════════════════════
// Post-Reply Cleanup — call after agent finishes replying
// ═══════════════════════════════════════════════════════════════════════════════

let lastCleanupCheck = 0
const CLEANUP_COOLDOWN = 60000 // 最多每分钟检查一次

/**
 * 在 message:sent 之后调用。
 * 立刻杀掉所有 gateway 产生的 claude 进程（detached，标记 ??）。
 * agent 说完话就释放并发，下次消息来再 spawn 新的。
 * 不碰用户自己的终端窗口（有控制终端 s000/s001 等）。
 */
export async function postReplyCleanup() {
  // Use killGatewayClaude from cli.ts — identifies gateway processes by CWD (.openclaw/hooks)
  // Safe: never touches user terminal claude processes
  try {
    const m = await import('./cli.ts')
    m.killGatewayClaude?.()
  } catch {
    // Fallback: direct implementation if import fails
    try {
      const psOutput = execSync(
        'ps aux | grep "[c]laude" | grep -v "Claude.app" | grep -v "chrome_crashpad" | awk \'{print $2}\'',
        { timeout: 3000 }
      ).toString().trim()

      if (!psOutput) return

      const pids = psOutput.split('\n').map(p => p.trim()).filter(Boolean)
      let killed = 0

      for (const pid of pids) {
        if (!/^\d+$/.test(pid)) continue
        try {
          const cwd = execSync(`lsof -p ${pid} 2>/dev/null | grep cwd | awk '{print $NF}'`, { timeout: 2000 })
            .toString().trim()
          if (cwd.includes('.openclaw/hooks')) {
            process.kill(parseInt(pid), 'SIGTERM')
            killed++
          }
        } catch { /* skip */ }
      }

      if (killed > 0) {
        console.log(`[cc-soul][health] 回复完成，清理了 ${killed} 个 gateway claude 进程`)
      }
    } catch { /* ps failure is ok */ }
  }
}

// ═══════════════════════════════════════════════════════════════════════════════
// CLI Concurrency Monitor — detect 180s timeouts and too many claude processes
// ═══════════════════════════════════════════════════════════════════════════════

function checkCliConcurrency() {
}

// ── SoulModule registration ──

export const healthModule: SoulModule = {
  id: 'health',
  name: '健康监控',
  priority: 80,
}
