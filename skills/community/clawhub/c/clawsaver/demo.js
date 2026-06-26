#!/usr/bin/env node

/**
 * ClawSaver Demo
 * 
 * Simulates realistic user message patterns and shows batching in action.
 * Run with: node demo.js
 */

import SessionDebouncer from './SessionDebouncer.js';

function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Simulate a user sending multiple related messages quickly
 */
async function runScenario(name, sessionKey, messages, debounceMs, expectBatches) {
  console.log(`\n${'='.repeat(70)}`);
  console.log(`Scenario: ${name}`);
  console.log(`${'='.repeat(70)}`);
  console.log(`Config: debounceMs=${debounceMs}ms`);
  console.log(`Expected batches: ${expectBatches}\n`);

  const batches = [];
  
  const debouncer = new SessionDebouncer(
    sessionKey,
    (msgs, meta) => {
      batches.push({ messages: msgs, meta });
      console.log(`  ✓ Batch ${batches.length}: ${meta.batchSize} message(s), ` +
                  `saved ${meta.savedCalls} call(s)`);
    },
    { debounceMs, maxWaitMs: 5000 }
  );

  // Simulate messages arriving at different times
  for (const [delayBefore, text] of messages) {
    await delay(delayBefore);
    console.log(`  → User sends: "${text}"`);
    debouncer.enqueue({ text, id: `msg_${Date.now()}` });
  }

  // Wait for final batch to flush
  await delay(debounceMs + 100);

  // Results
  const state = debouncer.getState();
  console.log(`\nResults:`);
  console.log(`  Batches created: ${batches.length}`);
  console.log(`  Total messages: ${state.metrics.totalMessages}`);
  console.log(`  Total saved calls: ${state.metrics.totalSavedCalls}`);
  console.log(`  Avg batch size: ${state.metrics.avgBatchSize.toFixed(1)}`);
  
  if (batches.length === expectBatches) {
    console.log(`  ✅ PASS: Got expected ${expectBatches} batch(es)`);
  } else {
    console.log(`  ❌ FAIL: Expected ${expectBatches} batches, got ${batches.length}`);
  }

  return batches;
}

/**
 * Main demo
 */
async function main() {
  console.log('ClawSaver Demo\n');
  console.log('Showing how message batching reduces model calls...\n');

  // Scenario 1: User hits send, then realizes they forgot something
  // (Should batch because they send both within the debounce window)
  await runScenario(
    'Accidental early send (user sends 2x quickly)',
    'session-1',
    [
      [0, 'What is machine learning?'],
      [300, 'And can you give an example?'],
      // (debounce 800ms, so they batch at ~1100ms total)
    ],
    800,
    1 // Expect 1 batch
  );

  // Scenario 2: User carefully types multi-part prompt over 2s
  // (Should batch — all arrive within debounce windows)
  await runScenario(
    'Multi-part prompt sent carefully',
    'session-2',
    [
      [0, 'I need help with a project.'],
      [400, 'The user wants to batch API calls.'],
      [800, 'Should I use a queue or debounce?'],
      // (debounce 500ms, so batch waits ~1300ms to collect all)
    ],
    500,
    1 // Expect 1 batch
  );

  // Scenario 3: User sends one message, then waits, then sends another
  // (Should create 2 separate batches)
  await runScenario(
    'Long pause between messages (separate batches)',
    'session-3',
    [
      [0, 'First question about performance.'],
      // (long pause)
      [1500, 'Okay, second unrelated question about caching.'],
      // (debounce 800ms, so flush at 800ms, then again at 2300ms)
    ],
    800,
    2 // Expect 2 batches
  );

  // Scenario 4: Very aggressive batching (short debounce)
  await runScenario(
    'Aggressive batching (200ms debounce)',
    'session-4',
    [
      [0, 'Fast question 1'],
      [50, 'Fast question 2'],
      [100, 'Fast question 3'],
      // (debounce 200ms, so batch waits ~300ms to collect all)
    ],
    200,
    1 // Expect 1 batch
  );

  // Scenario 5: Very conservative batching (long debounce)
  await runScenario(
    'Conservative batching (2000ms debounce)',
    'session-5',
    [
      [0, 'Slow message 1'],
      [600, 'Slow message 2'],
      [1200, 'Slow message 3'],
      // (debounce 2000ms, so batch doesn\'t flush until 3200ms)
    ],
    2000,
    1 // Expect 1 batch
  );

  // Summary
  console.log(`\n${'='.repeat(70)}`);
  console.log('Demo complete!\n');
  console.log('Key insights:');
  console.log('  • Short debounce (200ms) → fewer batches but less latency');
  console.log('  • Long debounce (2000ms) → more batching but more latency');
  console.log('  • Sweet spot depends on your users\' message patterns');
  console.log(`${'='.repeat(70)}\n`);
}

main().catch(err => {
  console.error('Demo failed:', err);
  process.exit(1);
});
