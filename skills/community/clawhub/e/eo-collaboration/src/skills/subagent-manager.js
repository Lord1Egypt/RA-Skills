/**
 * EO Subagent Manager - Practical Implementation
 * 
 * Features:
 * - Timeout per task
 * - Result tracking
 * - Error isolation
 * - Clean completion handling
 */

const DEFAULT_TIMEOUT_MS = 300000 // 5 min
const DEFAULT_MAX_CONCURRENT = 4

/**
 * @param {Array<{id: string, name: string, prompt: string, timeoutMs?: number}>} tasks
 * @returns {Promise<{results: Array, summary: Object, pending: Array>}}
 */
export async function runExpertTasks(tasks) {
  const results = new Map()
  const pending = new Set(tasks.map(t => t.id))
  
  tasks.forEach(t => {
    results.set(t.id, {
      id: t.id,
      name: t.name,
      success: false,
      output: null,
      error: null,
      timedOut: false,
    })
  })

  const startTime = Date.now()

  // Process in batches
  const batchSize = DEFAULT_MAX_CONCURRENT
  for (let i = 0; i < tasks.length; i += batchSize) {
    const batch = tasks.slice(i, i + batchSize)
    const batchPromises = batch.map(task => executeWithTimeout(task))
    await Promise.all(batchPromises)
  }

  function executeWithTimeout(task) {
    return new Promise(async (resolve) => {
      const timeoutMs = task.timeoutMs || DEFAULT_TIMEOUT_MS
      
      try {
        const handle = await sessions_spawn({
          task: task.prompt,
          mode: 'run',
          runTimeoutSeconds: Math.floor(timeoutMs / 1000),
        })

        // Wait with polling (simplified)
        const result = await waitForResult(handle, timeoutMs)
        
        results.set(task.id, {
          id: task.id,
          name: task.name,
          success: true,
          output: result,
        })
      } catch (error) {
        const errorMsg = error?.message || String(error)
        results.set(task.id, {
          id: task.id,
          name: task.name,
          success: false,
          error: errorMsg,
          timedOut: errorMsg.includes('timeout') || errorMsg.includes('timed out'),
        })
      } finally {
        pending.delete(task.id)
        resolve()
      }
    })
  }

  async function waitForResult(handle, timeoutMs) {
    const start = Date.now()
    while (Date.now() - start < timeoutMs) {
      // In actual use, would check handle status
      // This is a placeholder - actual implementation depends on OpenClaw API
      await new Promise(r => setTimeout(r, 1000))
      
      // Check if complete - depends on OpenClaw's actual API
      const status = handle.status?.()
      if (status === 'completed' || status === 'done') {
        return handle.output || 'completed'
      }
    }
    throw new Error('timeout')
  }

  // Wait for all pending
  while (pending.size > 0) {
    await new Promise(r => setTimeout(r, 500))
  }

  const resultsArray = Array.from(results.values())
  const summary = {
    total: resultsArray.length,
    succeeded: resultsArray.filter(r => r.success).length,
    failed: resultsArray.filter(r => !r.success && !r.timedOut).length,
    timedOut: resultsArray.filter(r => r.timedOut).length,
    totalDurationMs: Date.now() - startTime,
  }

  return { results: resultsArray, summary, pending: Array.from(pending) }
}

// ============================================================================
// Simpler Pattern - For Direct Use
// ============================================================================

/**
 * Spawn multiple tasks and wait for all with proper NO_REPLY handling
 * 
 * Usage:
 *   const { results, summary } = await spawnAndWaitAll([
 *     { id: 'task1', name: 'Design', prompt: 'Design a logo' },
 *     { id: 'task2', name: 'Copy', prompt: 'Write copy' },
 *   ])
 * 
 *   // Then send ONE reply to user
 */
export async function spawnAndWaitAll(tasks) {
  console.log(`[EO] Starting ${tasks.length} expert tasks...`)
  
  const handles = []
  
  // Spawn all
  for (const task of tasks) {
    console.log(`[EO] Spawning: ${task.name}`)
    const handle = await sessions_spawn({
      task: task.prompt,
      mode: 'run',
    })
    handles.push({ ...task, handle })
  }

  // Wait for all - actual implementation depends on OpenClaw's API
  console.log(`[EO] Waiting for ${handles.length} completions...`)
  
  // In practice, would use: await sessions_yield() after spawning
  // Then handle completion events with NO_REPLY
  
  return {
    handles,
    wait: async () => {
      // Placeholder - actual yield logic
      await sessions_yield(`Processing ${tasks.length} tasks...`)
    },
  }
}

/**
 * Format results for user display
 */
export function formatResultsSummary(results) {
  const summary = {
    total: results.length,
    succeeded: results.filter(r => r.success).length,
    failed: results.filter(r => !r.success).length,
  }
  
  let message = `✅ ${summary.succeeded}/${summary.total} tasks completed`
  if (summary.failed > 0) {
    message += `\n⚠️ ${summary.failed} failed:`
    results.filter(r => !r.success).forEach(r => {
      message += `\n  - ${r.name}: ${r.error || 'unknown error'}`
    })
  }
  
  return message
}
