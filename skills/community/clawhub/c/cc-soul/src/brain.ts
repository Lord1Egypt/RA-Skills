/**
 * brain.ts — Module Registry + Fault Isolation Layer
 *
 * Central nervous system for cc-soul. All feature modules register here.
 * Each module runs in a try/catch sandbox — one module crashing never
 * takes down other modules. Circuit breaker auto-disables flaky modules
 * and retries them after a cooldown.
 *
 * Usage:
 *   brain.register(myModule)
 *   brain.initAll()
 *   brain.fire('onSent', event)
 */

import type { Augment } from './types.ts'
import { isEnabled } from './features.ts'

// ═══════════════════════════════════════════════════════════════════════════════
// MODULE INTERFACE — every feature module implements this
// ═══════════════════════════════════════════════════════════════════════════════

export interface SoulModule {
  /** Unique identifier (e.g. 'values', 'evolution', 'inner-life') */
  id: string
  /** Human-readable name (e.g. '价值观追踪') */
  name: string
  /** Module IDs this depends on (for init ordering) */
  dependencies?: string[]
  /** Priority for hook execution order (higher = first, default 50) */
  priority?: number
  /** Feature toggle keys — ALL must be enabled for module to run (from features.json) */
  features?: string[]
  /** Default enabled state — set to false to disable module by default (requires manual enable) */
  enabled?: boolean

  /** Called once on startup — load persisted data, start timers */
  init?(): void | Promise<void>
  /** Called on shutdown — clear timers, flush data */
  dispose?(): void

  // ── Event hooks (all optional) ──

  /** agent:bootstrap — return prompt snippet to inject */
  onBootstrap?(event: any): string | void
  /** message:preprocessed — return augments to inject */
  onPreprocessed?(event: any): Augment[] | void
  /** message:sent — async post-processing */
  onSent?(event: any): void
  /** command:new — handle user commands */
  onCommand?(event: any): void
  /** heartbeat — periodic autonomous work (every 30 min) */
  onHeartbeat?(): void
}

// ═══════════════════════════════════════════════════════════════════════════════
// CIRCUIT BREAKER — per-module fault isolation
// ═══════════════════════════════════════════════════════════════════════════════

interface CircuitBreaker {
  failures: number
  lastFailure: number
  state: 'closed' | 'open' | 'half-open'
}

const TRIP_THRESHOLD = 5        // consecutive failures to trip
const RESET_TIMEOUT = 5 * 60000 // 5 min cooldown before retry

// ═══════════════════════════════════════════════════════════════════════════════
// BRAIN — the registry
// ═══════════════════════════════════════════════════════════════════════════════

type HookName = 'onBootstrap' | 'onPreprocessed' | 'onSent' | 'onCommand' | 'onHeartbeat'

class Brain {
  private modules = new Map<string, SoulModule>()
  private breakers = new Map<string, CircuitBreaker>()
  private manualEnabled = new Set<string>()  // override enabled:false at runtime
  private manualDisabled = new Set<string>() // override enabled:true at runtime
  private initDone = false

  // ── Registration ──

  register(mod: SoulModule): void {
    if (this.modules.has(mod.id)) {
      console.log(`[brain] replacing module: ${mod.id}`)
    }
    this.modules.set(mod.id, mod)
    this.breakers.set(mod.id, { failures: 0, lastFailure: 0, state: 'closed' })
    console.log(`[brain] registered: ${mod.id} (${mod.name})`)
  }

  // ── Lifecycle ──

  async initAll(): Promise<void> {
    if (this.initDone) return
    this.initDone = true

    const sorted = this.topoSort()
    for (const id of sorted) {
      const mod = this.modules.get(id)!
      if (!mod.init) continue
      try {
        await mod.init()
        console.log(`[brain] init ok: ${id}`)
      } catch (e: any) {
        console.error(`[brain] init FAILED: ${id} — ${e.message}`)
        this.trip(id, e)
      }
    }
    console.log(`[brain] ${this.modules.size} modules initialized`)
  }

  disposeAll(): void {
    for (const [id, mod] of this.modules) {
      try { mod.dispose?.() } catch (e: any) {
        console.error(`[brain] dispose error: ${id} — ${e.message}`)
      }
    }
    this.initDone = false
  }

  // ── Event dispatch (fault-isolated) ──

  /** Fire a hook on all modules, collect Augment[] results (for onPreprocessed) */
  firePreprocessed(event: any): Augment[] {
    const allAugments: Augment[] = []
    for (const mod of this.sorted()) {
      if (!mod.onPreprocessed || !this.isAvailable(mod.id)) continue
      try {
        const result = mod.onPreprocessed(event)
        if (result && result.length > 0) allAugments.push(...result)
        this.success(mod.id)
      } catch (e: any) {
        this.fail(mod.id, 'onPreprocessed', e)
      }
    }
    return allAugments
  }

  /** Fire a hook on all modules, collect string results (for onBootstrap) */
  fireBootstrap(event: any): string[] {
    const snippets: string[] = []
    for (const mod of this.sorted()) {
      if (!mod.onBootstrap || !this.isAvailable(mod.id)) continue
      try {
        const result = mod.onBootstrap(event)
        if (result) snippets.push(result)
        this.success(mod.id)
      } catch (e: any) {
        this.fail(mod.id, 'onBootstrap', e)
      }
    }
    return snippets
  }

  /** Fire a void hook on all modules (for onSent, onCommand, onHeartbeat) */
  fire(hook: 'onSent' | 'onCommand' | 'onHeartbeat', event?: any): void {
    for (const mod of this.sorted()) {
      const fn = mod[hook]
      if (!fn || !this.isAvailable(mod.id)) continue
      try {
        fn.call(mod, event)
        this.success(mod.id)
      } catch (e: any) {
        this.fail(mod.id, hook, e)
      }
    }
  }

  // ── Query ──

  getModule<T extends SoulModule>(id: string): T | undefined {
    return this.modules.get(id) as T | undefined
  }

  /** Enable a module at runtime (overrides enabled:false) */
  enableModule(id: string): boolean {
    if (!this.modules.has(id)) return false
    this.manualDisabled.delete(id)
    this.manualEnabled.add(id)
    console.log(`[brain] ${id}: enabled`)
    return true
  }

  /** Disable a module at runtime */
  disableModule(id: string): boolean {
    if (!this.modules.has(id)) return false
    this.manualEnabled.delete(id)
    this.manualDisabled.add(id)
    console.log(`[brain] ${id}: disabled`)
    return true
  }

  listModules(): { id: string; name: string; status: 'ok' | 'tripped' | 'recovering' | 'disabled' }[] {
    return [...this.modules.values()].map(mod => {
      const b = this.breakers.get(mod.id)!
      const featureOff = mod.features?.length && mod.features.some(f => !isEnabled(f))
      return {
        id: mod.id,
        name: mod.name,
        status: featureOff ? 'disabled' : b.state === 'closed' ? 'ok' : b.state === 'open' ? 'tripped' : 'recovering',
      }
    })
  }

  getHealth(): string {
    const mods = this.listModules()
    const ok = mods.filter(m => m.status === 'ok').length
    const tripped = mods.filter(m => m.status === 'tripped')
    if (tripped.length === 0) return `${ok}/${mods.length} modules ok`
    return `${ok}/${mods.length} ok, tripped: ${tripped.map(m => m.id).join(', ')}`
  }

  // ── Circuit breaker internals ──

  private isAvailable(id: string): boolean {
    const mod = this.modules.get(id)
    // Manual runtime override
    if (this.manualDisabled.has(id)) return false
    // Module-level kill switch — enabled defaults to true
    if (mod?.enabled === false && !this.manualEnabled.has(id)) return false
    // Feature toggle check — if module declares features, ALL must be enabled
    if (mod?.features && mod.features.length > 0) {
      if (mod.features.some(f => !isEnabled(f))) return false
    }

    const b = this.breakers.get(id)
    if (!b) return false
    if (b.state === 'closed') return true
    if (b.state === 'open') {
      // Check if cooldown elapsed → move to half-open
      if (Date.now() - b.lastFailure > RESET_TIMEOUT) {
        b.state = 'half-open'
        console.log(`[brain] ${id}: half-open (retrying)`)
        return true
      }
      return false
    }
    // half-open: allow one attempt
    return true
  }

  private success(id: string): void {
    const b = this.breakers.get(id)
    if (!b) return
    if (b.state !== 'closed') {
      console.log(`[brain] ${id}: recovered ✓`)
    }
    b.failures = 0
    b.state = 'closed'
  }

  private fail(id: string, hook: string, e: Error): void {
    console.error(`[brain] ${id}.${hook} error: ${e.message}`)
    this.trip(id, e)
  }

  private trip(id: string, e: Error): void {
    const b = this.breakers.get(id)
    if (!b) return
    b.failures++
    b.lastFailure = Date.now()
    if (b.failures >= TRIP_THRESHOLD && b.state === 'closed') {
      b.state = 'open'
      console.error(`[brain] ⚡ ${id}: TRIPPED after ${b.failures} failures — disabled for ${RESET_TIMEOUT / 1000}s`)
    }
  }

  // ── Topological sort by dependencies ──

  private topoSort(): string[] {
    const visited = new Set<string>()
    const result: string[] = []

    const visit = (id: string) => {
      if (visited.has(id)) return
      visited.add(id)
      const mod = this.modules.get(id)
      if (mod?.dependencies) {
        for (const dep of mod.dependencies) {
          if (this.modules.has(dep)) visit(dep)
        }
      }
      result.push(id)
    }

    for (const id of this.modules.keys()) visit(id)
    return result
  }

  /** Get modules sorted by priority (descending) */
  private sorted(): SoulModule[] {
    return [...this.modules.values()]
      .filter(m => this.isAvailable(m.id))
      .sort((a, b) => (b.priority ?? 50) - (a.priority ?? 50))
  }
}

// ── Singleton ──
export const brain = new Brain()
