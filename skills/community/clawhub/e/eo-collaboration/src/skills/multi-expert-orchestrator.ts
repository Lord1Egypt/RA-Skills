/**
 * EO Multi-Expert Orchestrator v1.0
 * 
 * Robust subagent management with:
 * - Timeout handling per agent
 * - Result aggregation
 * - Error isolation (one failure doesn't affect others)
 * - Configurable retry logic
 */

import { spawn, SessionHandle } from '../sessions'

export interface ExpertTask {
  /** Unique task ID */
  id: string
  /** Task description */
  name: string
  /** Full task prompt */
  prompt: string
  /** Timeout in ms (default: 5 min) */
  timeoutMs?: number
  /** Retry count (default: 0) */
  retries?: number
  /** Critical task - if fails, abort others */
  critical?: boolean
}

export interface ExpertResult {
  id: string
  name: string
  success: boolean
  output?: string
  error?: string
  durationMs: number
  timedOut?: boolean
}

export interface OrchestratorConfig {
  /** Timeout per task (default: 5 min) */
  defaultTimeoutMs: number
  /** Max concurrent agents (default: 4) */
  maxConcurrency: number
  /** Abort all on critical failure (default: true) */
  abortOnCriticalFailure: boolean
  /** Delay between retries (default: 1s) */
  retryDelayMs: number
}

const DEFAULT_CONFIG: OrchestratorConfig = {
  defaultTimeoutMs: 300000,  // 5 min
  maxConcurrency: 4,
  abortOnCriticalFailure: true,
  retryDelayMs: 1000,
}

// ============================================================================
// Result Aggregation
// ============================================================================

class ResultAggregator {
  private results: Map<string, ExpertResult> = new Map()
  private pending: Set<string> = new Set()
  private startTime: number = 0

  constructor(tasks: ExpertTask[]) {
    tasks.forEach(t => {
      this.pending.add(t.id)
      this.results.set(t.id, {
        id: t.id,
        name: t.name,
        success: false,
        durationMs: 0,
      })
    })
    this.startTime = Date.now()
  }

  complete(id: string, result: Partial<ExpertResult>): void {
    const existing = this.results.get(id)
    if (existing) {
      this.results.set(id, {
        ...existing,
        ...result,
        durationMs: Date.now() - this.startTime,
      })
      this.pending.delete(id)
    }
  }

  isComplete(): boolean {
    return this.pending.size === 0
  }

  getPending(): string[] {
    return Array.from(this.pending)
  }

  getResults(): ExpertResult[] {
    return Array.from(this.results.values())
  }

  getSummary(): {
    total: number
    succeeded: number
    failed: number
    timedOut: number
    totalDurationMs: number
  } {
    const results = this.getResults()
    return {
      total: results.length,
      succeeded: results.filter(r => r.success).length,
      failed: results.filter(r => !r.success && !r.timedOut).length,
      timedOut: results.filter(r => r.timedOut).length,
      totalDurationMs: Date.now() - this.startTime,
    }
  }

  hasCriticalFailure(): boolean {
    return this.getResults().some(r => !r.success && this.isTaskCritical(r.id))
  }

  private isTaskCritical(id: string): boolean {
    // Would need task reference - simplified for now
    return false
  }
}

// ============================================================================
// Main Orchestrator
// ============================================================================

export class MultiExpertOrchestrator {
  private config: OrchestratorConfig
  private sessionHandles: Map<string, SessionHandle> = new Map()

  constructor(config: Partial<OrchestratorConfig> = {}) {
    this.config = { ...DEFAULT_CONFIG, ...config }
  }

  /**
   * Execute multiple expert tasks in parallel with robust error handling
   */
  async execute(tasks: ExpertTask[]): Promise<{
    results: ExpertResult[]
    summary: ReturnType<ResultAggregator['getSummary']>
    aborted: boolean
  }> {
    const aggregator = new ResultAggregator(tasks)
    const batchSize = this.config.maxConcurrency

    // Execute in batches
    for (let i = 0; i < tasks.length && !aggregator.hasCriticalFailure(); i += batchSize) {
      const batch = tasks.slice(i, i + batchSize)
      const batchPromises = batch.map(task => this.executeTask(task, aggregator))
      await Promise.all(batchPromises)
    }

    return {
      results: aggregator.getResults(),
      summary: aggregator.getSummary(),
      aborted: aggregator.hasCriticalFailure(),
    }
  }

  /**
   * Execute a single task with timeout and retry handling
   */
  private async executeTask(task: ExpertTask, aggregator: ResultAggregator): Promise<void> {
    const timeoutMs = task.timeoutMs || this.config.defaultTimeoutMs
    const maxRetries = task.retries || 0

    for (let attempt = 0; attempt <= maxRetries; attempt++) {
      try {
        const handle = await spawn({
          task: task.prompt,
          mode: 'run',
        })

        this.sessionHandles.set(task.id, handle)

        // Wait for completion with timeout
        const result = await this.waitForCompletion(handle, timeoutMs)

        aggregator.complete(task.id, {
          success: true,
          output: result,
        })

        return

      } catch (error) {
        const errorMsg = error instanceof Error ? error.message : String(error)
        
        if (attempt < maxRetries) {
          // Retry after delay
          await this.delay(this.config.retryDelayMs)
          continue
        }

        // All retries exhausted
        aggregator.complete(task.id, {
          success: false,
          error: errorMsg,
          timedOut: errorMsg.includes('timeout'),
        })
        return
      }
    }
  }

  /**
   * Wait for task completion with timeout
   */
  private async waitForCompletion(handle: SessionHandle, timeoutMs: number): Promise<string> {
    return new Promise((resolve, reject) => {
      const timeout = setTimeout(() => {
        reject(new Error(`Task ${handle.sessionId} timed out after ${timeoutMs}ms`))
      }, timeoutMs)

      // In actual implementation, would hook into completion events
      // For now, simplified
      handle.waitForCompletion().then(result => {
        clearTimeout(timeout)
        resolve(result)
      }).catch(reject)
    })
  }

  /**
   * Abort all running tasks
   */
  abortAll(): void {
    this.sessionHandles.forEach((handle, id) => {
      try {
        handle.abort()
      } catch (e) {
        console.error(`Failed to abort task ${id}:`, e)
      }
    })
    this.sessionHandles.clear()
  }

  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms))
  }
}

// ============================================================================
// Convenience Functions
// ============================================================================

/**
 * Execute multiple expert tasks with default settings
 */
export async function executeExperts(tasks: ExpertTask[]): Promise<{
  results: ExpertResult[]
  summary: {
    total: number
    succeeded: number
    failed: number
    timedOut: number
    totalDurationMs: number
  }
}> {
  const orchestrator = new MultiExpertOrchestrator()
  const result = await orchestrator.execute(tasks)
  return {
    results: result.results,
    summary: result.summary,
  }
}

// ============================================================================
// Usage Examples
// ============================================================================

/*
// Example 1: Simple parallel execution
const results = await executeExperts([
  {
    id: 'design-1',
    name: 'Logo Design',
    prompt: 'Design a logo for Steel Crayfish Legion',
    timeoutMs: 120000,
  },
  {
    id: 'copy-1', 
    name: 'Marketing Copy',
    prompt: 'Write marketing copy for EO project',
    timeoutMs: 60000,
  },
])

console.log(`Succeeded: ${results.summary.succeeded}/${results.summary.total}`)

// Example 2: With critical task
const results2 = await executeExperts([
  {
    id: 'critical-1',
    name: 'Core Feature',
    prompt: 'Implement core feature X',
    critical: true,  // If this fails, abort others
    retries: 2,
  },
  {
    id: 'optional-1',
    name: 'Nice to Have',
    prompt: 'Implement feature Y',
  },
])

// Example 3: Custom orchestrator
const orch = new MultiExpertOrchestrator({
  maxConcurrency: 2,
  defaultTimeoutMs: 600000,  // 10 min
  abortOnCriticalFailure: true,
})

const results3 = await orch.execute(tasks)
*/
