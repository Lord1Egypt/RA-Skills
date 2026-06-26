/**
 * SessionDebouncer
 * 
 * Automatically buffers and deduplicates user messages at the session level.
 * Batches related messages into fewer, higher-value model calls.
 * 
 * Zero config required — just wire it up. All tuning via options.
 */

class SessionDebouncer {
  constructor(sessionKey, flushCallback, options = {}) {
    this.sessionKey = sessionKey;
    this.flushCallback = flushCallback;

    // Tunable parameters
    this.debounceMs = options.debounceMs ?? 800;
    this.maxWaitMs = options.maxWaitMs ?? 3000;
    this.maxMessages = options.maxMessages ?? 5;
    this.maxTokens = options.maxTokens ?? 2048;

    // State
    this.buffer = [];
    this.timer = null;
    this.createdAt = null;
    this.metrics = {
      totalBatches: 0,
      totalMessages: 0,
      totalSavedCalls: 0,
      avgBatchSize: 0,
    };
  }

  /**
   * Enqueue a message. Automatically flushes when:
   * - maxMessages limit is hit
   * - maxWaitMs has elapsed since first message in buffer
   * - otherwise, waits for debounceMs of silence
   */
  enqueue(message) {
    const now = Date.now();

    // Start tracking time on first message in batch
    if (this.buffer.length === 0) {
      this.createdAt = now;
    }

    this.buffer.push({
      text: message.text || message,
      timestamp: now,
      id: message.id || `msg_${now}_${Math.random().toString(36).slice(2)}`,
    });

    // Flush immediately if we hit max messages
    if (this.buffer.length >= this.maxMessages) {
      this._logDebug(`Hit maxMessages limit (${this.maxMessages})`);
      this.flush();
      return;
    }

    // Flush if we've waited past absolute max
    const elapsedMs = now - this.createdAt;
    if (elapsedMs >= this.maxWaitMs) {
      this._logDebug(`Hit maxWaitMs limit (${this.maxWaitMs}ms, elapsed ${elapsedMs}ms)`);
      this.flush();
      return;
    }

    // Reset debounce timer
    clearTimeout(this.timer);
    this.timer = setTimeout(() => {
      this._logDebug(`Debounce timeout after ${this.debounceMs}ms`);
      this.flush();
    }, this.debounceMs);
  }

  /**
   * Manually trigger flush (e.g., user clicks "Send now")
   */
  forceFlush(reason = 'manual') {
    this._logDebug(`Force flush triggered: ${reason}`);
    this.flush();
  }

  /**
   * Flush the buffer and call the handler
   */
  flush() {
    if (this.buffer.length === 0) return;

    clearTimeout(this.timer);
    const messages = this.buffer;
    const batchSize = messages.length;
    const savedCalls = Math.max(0, batchSize - 1);

    this.buffer = [];
    this.timer = null;
    this.createdAt = null;

    // Update metrics
    this.metrics.totalBatches += 1;
    this.metrics.totalMessages += batchSize;
    this.metrics.totalSavedCalls += savedCalls;
    this.metrics.avgBatchSize = this.metrics.totalMessages / this.metrics.totalBatches;

    this._logDebug(
      `Flushing ${batchSize} message(s), saving ${savedCalls} model call(s)`
    );

    // Call the handler with all buffered messages
    Promise.resolve(this.flushCallback(messages, {
      batchSize,
      savedCalls,
      messageIds: messages.map(m => m.id),
    })).catch(err => {
      console.error(`[${this.sessionKey}] Flush failed:`, err);
    });
  }

  /**
   * Get current buffer state (for UI/logging)
   */
  getState() {
    const now = Date.now();
    const elapsedMs = this.createdAt ? now - this.createdAt : 0;

    return {
      buffered: this.buffer.length,
      waitingMs: elapsedMs,
      nextFlushMs: this.timer ? this.debounceMs - (elapsedMs % this.debounceMs) : null,
      isFull: this.buffer.length >= this.maxMessages,
      isExpired: elapsedMs >= this.maxWaitMs,
      metrics: this.metrics,
    };
  }

  /**
   * Get a human-readable status string (for logging/UI)
   */
  getStatusString() {
    const state = this.getState();
    if (state.buffered === 0) return 'ready';
    return `buffering ${state.buffered}/${this.maxMessages} (${state.waitingMs}ms)`;
  }

  /**
   * Reset metrics (e.g., for A/B testing)
   */
  resetMetrics() {
    this.metrics = {
      totalBatches: 0,
      totalMessages: 0,
      totalSavedCalls: 0,
      avgBatchSize: 0,
    };
  }

  _logDebug(message) {
    console.log(`[SessionDebouncer/${this.sessionKey}] ${message}`);
  }
}

export default SessionDebouncer;
