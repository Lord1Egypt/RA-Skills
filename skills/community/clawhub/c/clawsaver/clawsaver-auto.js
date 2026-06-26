/**
 * ClawSaver Middleware Helper
 * 
 * Drop-in wrapper for OpenClaw skills. Handles batching automatically.
 * 
 * Usage:
 *   import { withBatching } from './clawsaver-auto.js';
 *   
 *   async function handleMessage(sessionKey, userMessage, modelFn) {
 *     return withBatching(sessionKey, userMessage, modelFn);
 *   }
 */

import SessionDebouncer from 'clawsaver';

const debouncers = new Map();
const handlers = new Map();

/**
 * Wrap a model function with automatic message batching.
 * 
 * @param {string} sessionKey - User/session ID
 * @param {string} userMessage - Incoming message text
 * @param {Function} modelFn - Your model call handler: async (text, meta) => response
 * @param {Object} options - Optional: { debounceMs, maxWaitMs, maxMessages }
 * @returns {Promise} Model response
 */
export async function withBatching(sessionKey, userMessage, modelFn, options = {}) {
  // Get or create debouncer for this session
  if (!debouncers.has(sessionKey)) {
    const debouncer = new SessionDebouncer(
      sessionKey,
      (messages, meta) => flushBatch(sessionKey, messages, meta),
      {
        debounceMs: options.debounceMs ?? 800,
        maxWaitMs: options.maxWaitMs ?? 3000,
        maxMessages: options.maxMessages ?? 5,
      }
    );
    debouncers.set(sessionKey, debouncer);
    handlers.set(sessionKey, modelFn);
  }

  // Update handler if a new one was passed (e.g., different model)
  if (modelFn && handlers.get(sessionKey) !== modelFn) {
    handlers.set(sessionKey, modelFn);
  }

  // Enqueue the message
  const debouncer = debouncers.get(sessionKey);
  debouncer.enqueue({ text: userMessage });

  // Return immediately — actual processing happens on batch flush
  // (For sync responses, use forceFlush below)
  return null;
}

/**
 * Synchronous wrapper: wait for batch to flush.
 * Use when you need immediate response (e.g., CLI, webhook).
 * 
 * @param {string} sessionKey 
 * @param {string} userMessage 
 * @param {Function} modelFn 
 * @param {Object} options 
 * @returns {Promise} Model response
 */
export async function withBatchingSync(sessionKey, userMessage, modelFn, options = {}) {
  // Enqueue message
  await withBatching(sessionKey, userMessage, modelFn, options);
  
  // Wait for it to flush (or timeout)
  return new Promise((resolve, reject) => {
    const debouncer = debouncers.get(sessionKey);
    const maxWait = options.maxWaitMs ?? 3000;
    
    const startTime = Date.now();
    const poll = setInterval(() => {
      const state = debouncer.getState();
      
      if (state.buffer.length === 0) {
        clearInterval(poll);
        const response = debouncer.lastResponse || null;
        resolve(response);
      } else if (Date.now() - startTime > maxWait) {
        clearInterval(poll);
        debouncer.forceFlush('sync-timeout');
        resolve(debouncer.lastResponse || null);
      }
    }, 50);
  });
}

/**
 * Internal: Process batched messages
 */
async function flushBatch(sessionKey, messages, meta) {
  const modelFn = handlers.get(sessionKey);
  if (!modelFn) return;

  // Merge messages into one prompt
  const merged = messages
    .map((m, i) => `**Message ${i + 1}:**\n${m.text}`)
    .join('\n\n')
    + '\n\n_Please treat the above as a single combined input._';

  try {
    // Call the model
    const response = await modelFn(merged, {
      batchSize: meta.batchSize,
      savedCalls: meta.savedCalls,
      sessionKey,
    });

    // Store response for potential sync retrieval
    debouncers.get(sessionKey).lastResponse = response;

    return response;
  } catch (err) {
    console.error(`[${sessionKey}] Batch processing failed:`, err);
    throw err;
  }
}

/**
 * Get debouncer for a session (for manual control)
 */
export function getDebouncer(sessionKey) {
  return debouncers.get(sessionKey);
}

/**
 * Force flush pending messages (e.g., session timeout, explicit user action)
 */
export function flush(sessionKey, reason = 'manual') {
  const debouncer = debouncers.get(sessionKey);
  if (debouncer) {
    debouncer.forceFlush(reason);
  }
}

/**
 * Get current metrics for a session
 */
export function getMetrics(sessionKey) {
  const debouncer = debouncers.get(sessionKey);
  if (!debouncer) return null;
  
  const state = debouncer.getState();
  const { totalBatches, totalSavedCalls, avgBatchSize } = state.metrics;
  
  return {
    batches: totalBatches,
    savedCalls: totalSavedCalls,
    avgBatchSize: avgBatchSize.toFixed(1),
    costReduction: totalSavedCalls > 0 
      ? ((totalSavedCalls / (totalBatches + totalSavedCalls)) * 100).toFixed(1) + '%'
      : '0%',
  };
}

/**
 * Clean up session (e.g., on logout, session end)
 */
export function cleanup(sessionKey) {
  const debouncer = debouncers.get(sessionKey);
  if (debouncer) {
    debouncer.forceFlush('cleanup');
    debouncers.delete(sessionKey);
    handlers.delete(sessionKey);
  }
}

/**
 * Clean up all sessions (e.g., on shutdown)
 */
export function cleanupAll(reason = 'shutdown') {
  for (const [sessionKey, debouncer] of debouncers.entries()) {
    debouncer.forceFlush(reason);
  }
  debouncers.clear();
  handlers.clear();
}

/**
 * Log metrics for all active sessions
 */
export function logMetrics() {
  if (debouncers.size === 0) {
    console.log('No active sessions');
    return;
  }

  console.log('\n=== ClawSaver Metrics ===');
  let totalBatches = 0;
  let totalSaved = 0;

  for (const [sessionKey, debouncer] of debouncers.entries()) {
    const metrics = getMetrics(sessionKey);
    if (metrics && metrics.batches > 0) {
      console.log(
        `${sessionKey}: ${metrics.batches} batches, ${metrics.savedCalls} calls saved, ` +
        `avg batch size ${metrics.avgBatchSize}`
      );
      totalBatches += metrics.batches;
      totalSaved += metrics.savedCalls;
    }
  }

  if (totalBatches > 0) {
    const reduction = ((totalSaved / (totalBatches + totalSaved)) * 100).toFixed(1);
    console.log(`\nTotal: ${totalBatches} batches, ${totalSaved} calls saved (${reduction}% reduction)`);
  }
  console.log('========================\n');
}

// Export default
export default { withBatching, withBatchingSync, getDebouncer, flush, getMetrics, cleanup, cleanupAll, logMetrics };
