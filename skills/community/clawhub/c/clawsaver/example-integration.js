/**
 * Example: ClawSaver Integration
 * 
 * Shows how to wire SessionDebouncer into your session handler.
 * Modify as needed for your specific setup.
 */

import SessionDebouncer from './SessionDebouncer.js';

// ============================================================================
// SETUP: Create one debouncer per session
// ============================================================================

const debouncers = new Map(); // sessionKey -> SessionDebouncer

function getOrCreateDebouncer(sessionKey, options = {}) {
  if (!debouncers.has(sessionKey)) {
    // Use custom options or fall back to defaults
    const debouncer = new SessionDebouncer(
      sessionKey,
      (messages, meta) => processModelCall(sessionKey, messages, meta),
      {
        debounceMs: options.debounceMs ?? 800,
        maxWaitMs: options.maxWaitMs ?? 3000,
        maxMessages: options.maxMessages ?? 5,
      }
    );
    debouncers.set(sessionKey, debouncer);
  }
  return debouncers.get(sessionKey);
}

// ============================================================================
// MESSAGE INGESTION: Enqueue messages
// ============================================================================

async function handleUserMessage(sessionKey, message) {
  const debouncer = getOrCreateDebouncer(sessionKey);
  debouncer.enqueue(message);
  
  // Optional: Log current state
  logBufferStatus(sessionKey);
}

// ============================================================================
// MODEL CALL: Process batched messages
// ============================================================================

async function processModelCall(sessionKey, messages, meta) {
  const merged = mergeMessages(messages);
  
  console.log(
    `\n[${sessionKey}] Processing batched input:\n` +
    `  Messages: ${meta.batchSize}\n` +
    `  Saved calls: ${meta.savedCalls}\n` +
    `  Message IDs: ${meta.messageIds.join(', ')}\n`
  );

  try {
    // Call your model here
    // const result = await yourModel.complete(merged);
    
    // Placeholder for demo
    console.log(`[${sessionKey}] Model would receive:\n${merged}\n`);
    const result = `[Mock response to batch of ${meta.batchSize} messages]`;

    // Send response back to session
    await sendToSession(sessionKey, result);
  } catch (err) {
    console.error(`[${sessionKey}] Model call failed:`, err);
    // Add retry logic here if needed
  }
}

// ============================================================================
// UTILITIES
// ============================================================================

function mergeMessages(messages) {
  return messages
    .map((m, i) => `**Message ${i + 1}:**\n${m.text}`)
    .join('\n\n')
    + '\n\n_Please treat the above as a single combined user input._';
}

async function sendToSession(sessionKey, response) {
  // Placeholder — replace with your actual send logic
  console.log(`[${sessionKey}] Sending response:\n${response}\n`);
}

function logBufferStatus(sessionKey) {
  const debouncer = debouncers.get(sessionKey);
  if (!debouncer) return;
  
  const status = debouncer.getStatusString();
  if (status !== 'ready') {
    console.log(`[${sessionKey}] ${status}`);
  }
}

// ============================================================================
// MONITORING: Optional periodic logging
// ============================================================================

function startMetricsReporter(intervalMs = 60000) {
  setInterval(() => {
    if (debouncers.size === 0) return;

    console.log('\n--- ClawSaver Metrics ---');
    let totalSaved = 0;
    let totalBatches = 0;
    
    debouncers.forEach((debouncer, sessionKey) => {
      const state = debouncer.getState();
      const { totalBatches: b, totalSavedCalls: s, avgBatchSize: avg } = state.metrics;
      
      if (b > 0) {
        console.log(`${sessionKey}: ${b} batches, ${s} calls saved, avg batch ${avg.toFixed(1)}`);
        totalSaved += s;
        totalBatches += b;
      }
    });
    
    if (totalBatches > 0) {
      const savings = (totalSaved / (totalBatches + totalSaved)) * 100;
      console.log(`\nTotal: ${totalBatches} batches, ${totalSaved} calls saved (${savings.toFixed(1)}% reduction)`);
    }
    console.log('------------------------\n');
  }, intervalMs);
}

// ============================================================================
// OPTIONAL: Force flush for specific sessions
// ============================================================================

function flushSession(sessionKey, reason = 'manual') {
  const debouncer = debouncers.get(sessionKey);
  if (debouncer) {
    console.log(`[${sessionKey}] Force flushing: ${reason}`);
    debouncer.forceFlush(reason);
  }
}

function flushAllSessions(reason = 'shutdown') {
  debouncers.forEach((debouncer, sessionKey) => {
    console.log(`[${sessionKey}] Force flushing: ${reason}`);
    debouncer.forceFlush(reason);
  });
}

// ============================================================================
// OPTIONAL: Cleanup
// ============================================================================

function removeSession(sessionKey) {
  const debouncer = debouncers.get(sessionKey);
  if (debouncer) {
    debouncer.forceFlush('session-cleanup');
    debouncers.delete(sessionKey);
    console.log(`[${sessionKey}] Removed debouncer`);
  }
}

// ============================================================================
// EXPORTS
// ============================================================================

export {
  getOrCreateDebouncer,
  handleUserMessage,
  flushSession,
  flushAllSessions,
  removeSession,
  startMetricsReporter,
  getDebouncers,
};

function getDebouncers() {
  return debouncers;
}
