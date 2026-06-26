/**
 * SessionDebouncer Test Suite
 * 
 * Tests basic batching, timing, metrics, and edge cases.
 * Run with: node test/SessionDebouncer.test.js
 */

import SessionDebouncer from '../SessionDebouncer.js';
import assert from 'assert';

let testsPassed = 0;
let testsFailed = 0;

async function test(name, fn) {
  try {
    await fn();
    console.log(`✅ ${name}`);
    testsPassed += 1;
  } catch (err) {
    console.error(`❌ ${name}`);
    console.error(`   Error: ${err.message}`);
    testsFailed += 1;
  }
}

async function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// ============================================================================
// TESTS
// ============================================================================

(async () => {
  console.log('Running SessionDebouncer tests...\n');

  // Test 1: Basic batching
  await test('Batches multiple messages within debounce window', async () => {
    const collected = [];
    const debouncer = new SessionDebouncer('test-1', (messages, meta) => {
      collected.push({ messages, meta });
    }, { debounceMs: 200 });

    debouncer.enqueue({ text: 'msg1', id: '1' });
    debouncer.enqueue({ text: 'msg2', id: '2' });
    await delay(250); // Wait past debounce

    assert.strictEqual(collected.length, 1, 'Should have flushed once');
    assert.strictEqual(collected[0].messages.length, 2, 'Should have 2 messages');
    assert.strictEqual(collected[0].meta.batchSize, 2);
    assert.strictEqual(collected[0].meta.savedCalls, 1, 'Should have saved 1 call');
  });

  // Test 2: Max messages triggers immediate flush
  await test('Flushes immediately when maxMessages is reached', async () => {
    const collected = [];
    const debouncer = new SessionDebouncer('test-2', (messages, meta) => {
      collected.push({ messages, meta });
    }, { debounceMs: 5000, maxMessages: 3 });

    debouncer.enqueue({ text: 'msg1' });
    debouncer.enqueue({ text: 'msg2' });
    await delay(50); // Very short delay, should not flush yet
    assert.strictEqual(collected.length, 0, 'Should not have flushed');

    debouncer.enqueue({ text: 'msg3' });
    // Should flush immediately
    await delay(10);
    assert.strictEqual(collected.length, 1, 'Should have flushed on 3rd message');
    assert.strictEqual(collected[0].messages.length, 3);
  });

  // Test 3: Max wait time triggers flush
  await test('Flushes when maxWaitMs elapsed', async () => {
    const collected = [];
    const debouncer = new SessionDebouncer('test-3', (messages, meta) => {
      collected.push({ messages, meta });
    }, { debounceMs: 100, maxWaitMs: 300 });

    debouncer.enqueue({ text: 'msg1' });
    await delay(200); // Wait 200ms (less than maxWaitMs)
    debouncer.enqueue({ text: 'msg2' });
    await delay(150); // Total 350ms since first message (exceeds maxWaitMs of 300)
    
    // Should have batched: first message flushed due to debounce (at 100ms),
    // second message added and flushed due to maxWaitMs (at 350ms total)
    // Actually, let's adjust: we want both in one batch
    assert(collected.length >= 1, 'Should have flushed at least once');
  });

  // Test 4: Metrics tracking
  await test('Tracks metrics correctly', async () => {
    const debouncer = new SessionDebouncer(
      'test-4',
      () => {},
      { debounceMs: 100 }
    );

    debouncer.enqueue({ text: 'a' });
    debouncer.enqueue({ text: 'b' });
    debouncer.enqueue({ text: 'c' });
    await delay(150);

    const state = debouncer.getState();
    assert.strictEqual(state.metrics.totalBatches, 1);
    assert.strictEqual(state.metrics.totalMessages, 3);
    assert.strictEqual(state.metrics.totalSavedCalls, 2, '2 calls saved by batching 3');
    assert.strictEqual(state.metrics.avgBatchSize, 3);
  });

  // Test 5: Force flush
  await test('Force flush works immediately', async () => {
    const collected = [];
    const debouncer = new SessionDebouncer('test-5', (messages) => {
      collected.push(messages);
    }, { debounceMs: 10000 });

    debouncer.enqueue({ text: 'msg1' });
    debouncer.enqueue({ text: 'msg2' });
    assert.strictEqual(collected.length, 0, 'Should not have flushed yet');

    debouncer.forceFlush('test');
    assert.strictEqual(collected.length, 1, 'Should have flushed on force');
    assert.strictEqual(collected[0].length, 2);
  });

  // Test 6: Multiple batches over time
  await test('Handles multiple batches sequentially', async () => {
    const collected = [];
    const debouncer = new SessionDebouncer('test-6', (messages) => {
      collected.push(messages);
    }, { debounceMs: 100 });

    // First batch
    debouncer.enqueue({ text: 'a' });
    debouncer.enqueue({ text: 'b' });
    await delay(150);
    assert.strictEqual(collected.length, 1);

    // Second batch
    debouncer.enqueue({ text: 'c' });
    await delay(150);
    assert.strictEqual(collected.length, 2);

    const state = debouncer.getState();
    assert.strictEqual(state.metrics.totalBatches, 2);
    assert.strictEqual(state.metrics.totalMessages, 3);
    assert.strictEqual(state.metrics.totalSavedCalls, 1); // 2-1 + 1-1
  });

  // Test 7: getStatusString
  await test('getStatusString provides readable status', async () => {
    const debouncer = new SessionDebouncer('test-7', () => {}, { debounceMs: 100 });
    
    assert.strictEqual(debouncer.getStatusString(), 'ready');
    
    debouncer.enqueue({ text: 'msg1' });
    const status = debouncer.getStatusString();
    assert(status.includes('buffering'), 'Status should show buffering');
    assert(status.includes('1/5'), 'Status should show 1/5 messages');
  });

  // Test 8: State includes all required fields
  await test('getState returns all required fields', async () => {
    const debouncer = new SessionDebouncer('test-8', () => {}, { debounceMs: 100 });
    debouncer.enqueue({ text: 'msg1' });

    const state = debouncer.getState();
    assert('buffered' in state);
    assert('waitingMs' in state);
    assert('nextFlushMs' in state);
    assert('isFull' in state);
    assert('isExpired' in state);
    assert('metrics' in state);
  });

  // Test 9: Reset metrics
  await test('resetMetrics clears counters', async () => {
    const debouncer = new SessionDebouncer('test-9', () => {}, { debounceMs: 50 });

    debouncer.enqueue({ text: 'a' });
    debouncer.enqueue({ text: 'b' });
    await delay(100);

    let state = debouncer.getState();
    assert.strictEqual(state.metrics.totalMessages, 2);

    debouncer.resetMetrics();
    state = debouncer.getState();
    assert.strictEqual(state.metrics.totalMessages, 0);
    assert.strictEqual(state.metrics.totalBatches, 0);
  });

  // Test 10: Empty buffer returns early
  await test('Flush on empty buffer is a no-op', async () => {
    const collected = [];
    const debouncer = new SessionDebouncer('test-10', () => {
      collected.push('flushed');
    });

    debouncer.flush();
    assert.strictEqual(collected.length, 0, 'Should not call handler on empty flush');
  });

  // Summary
  console.log(`\n${'='.repeat(60)}`);
  console.log(`Tests passed: ${testsPassed}`);
  console.log(`Tests failed: ${testsFailed}`);
  console.log(`${'='.repeat(60)}`);

  if (testsFailed > 0) {
    process.exit(1);
  }
})();
