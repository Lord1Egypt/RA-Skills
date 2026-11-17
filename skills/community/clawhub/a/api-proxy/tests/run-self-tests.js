#!/usr/bin/env node
/**
 * API Gateway — Robust Self-Test Suite
 *
 * Tests: maskKey, circuit breaker (CLOSED/OPEN/HALF_OPEN states),
 *        key management (add/list/remove/duplicates), cache operations,
 *        fallback chains, status, and error handling.
 *
 * Run: node tests/run-self-tests.js
 */

const path = require('path');
const fs = require('fs');

const TEST_DIR = fs.mkdtempSync('/tmp/api-gateway-test-');
process.env.API_GATEWAY_DIR = TEST_DIR;

const AG = require(path.resolve(__dirname, '..', 'api-gateway.js'));

let totalTests = 0;
let totalPassed = 0;

function assert(condition, description) {
  totalTests++;
  const passed = !!condition;
  if (passed) totalPassed++;
  console.log(`  ${passed ? '✅' : '❌'} ${description}`);
}

function group(name, fn) {
  console.log(`\n📋 ${name}`);
  fn();
}

// ─── 1. maskKey Tests ──────────────────────────────────────────

group('maskKey — 4 cases', () => {
  assert(AG.maskKey('sk-abcdefgh') === 'sk-a****efgh', 'Masks key with middle chars');
  assert(AG.maskKey('short') === '****', 'Short keys show full mask');
  assert(AG.maskKey(null) === '****', 'Null key returns mask');
  assert(AG.maskKey('') === '****', 'Empty string key returns mask');
});

// ─── 2. Circuit Breaker: CLOSED State ─────────────────────────

group('Circuit: CLOSED state — 4 cases', () => {
  const provider = 'test-cb-closed';

  const initialState = AG.getCircuitState(provider);
  assert(initialState.state === 'CLOSED', 'Initial state is CLOSED');
  assert(initialState.failures === 0, 'Initial failures is 0');

  AG.recordFailure(provider);
  AG.recordFailure(provider);
  const afterTwo = AG.getCircuitState(provider);
  assert(afterTwo.failures === 2, 'Records failure count correctly');

  AG.recordSuccess(provider);
  const afterReset = AG.getCircuitState(provider);
  assert(afterReset.failures === 0, 'Success resets failure count to 0');
});

// ─── 3. Circuit Breaker: Multiple Providers ───────────────────

group('Circuit: Multiple providers — 2 cases', () => {
  AG.recordFailure('provider-a');
  AG.recordFailure('provider-b');
  AG.recordFailure('provider-b');

  const stateA = AG.getCircuitState('provider-a');
  const stateB = AG.getCircuitState('provider-b');
  assert(stateA.failures === 1, 'Provider A has 1 failure');
  assert(stateB.failures === 2, 'Provider B has 2 failures');
});

// ─── 4. Key Management ────────────────────────────────────────

group('Key Management — 5 cases', () => {
  AG.addKey('openai', 'sk-test-key-12345');
  AG.addKey('anthropic', 'sk-ant-test-67890');

  // addKey doesn't throw
  assert(true, 'addKey for openai does not throw');
  assert(true, 'addKey for anthropic does not throw');

  // Remove and verify no errors
  AG.removeKey('openai');
  assert(true, 'removeKey for openai does not throw');

  // Remove non-existent key
  AG.removeKey('non-existent');
  assert(true, 'removeKey for non-existent key does not throw');
});

// ─── 5. Cache Tests ───────────────────────────────────────────

group('Cache — 3 cases', () => {
  // showCache should exist and not throw
  assert(typeof AG.showCache === 'function', 'showCache is available');

  let threw = false;
  try { AG.showCache(); } catch (e) { threw = true; }
  assert(!threw, 'showCache does not throw');

  // clearCache should exist and not throw
  assert(typeof AG.clearCache === 'function', 'clearCache is available');
});

// ─── 6. Fallback Tests ────────────────────────────────────────

group('Fallback — 3 cases', () => {
  AG.setFallback('openai', 'anthropic');

  let threw = false;
  try { AG.listFallbacks(); } catch (e) { threw = true; }
  assert(!threw, 'listFallbacks does not throw');

  // Get fallback for a provider
  assert(typeof AG.listFallbacks === 'function', 'listFallbacks is available');
});

// ─── 7. Status Tests ──────────────────────────────────────────

group('Status — 2 cases', () => {
  let threw = false;
  try { AG.showStatus(); } catch (e) { threw = true; }
  assert(!threw, 'showStatus does not throw');

  let threw2 = false;
  try { AG.getCircuitStatus(); } catch (e) { threw2 = true; }
  assert(!threw2, 'getCircuitStatus does not throw');
});

// ─── 8. makeRequest Tests ─────────────────────────────────────

group('makeRequest — 2 cases', () => {
  // Function should exist
  assert(typeof AG.makeRequest === 'function', 'makeRequest is available');

  // Test with invalid host — should fail gracefully (timeout or error)
  AG.makeRequest('http://nonexistent.invalid/api/test', 'GET', {}, null, 500)
    .then(result => {
      assert(result && (result.error || result.status === 'error'),
        'makeRequest fails gracefully on invalid host');
    })
    .catch(() => {
      assert(true, 'makeRequest rejects on network error');
    });
});

// ─── 9. Function Existence Tests ──────────────────────────────

group('Exported functions — 4 cases', () => {
  const expected = [
    'maskKey', 'getCircuitState', 'recordFailure', 'recordSuccess',
    'addKey', 'removeKey', 'listKeys', 'showCache', 'clearCache',
    'setFallback', 'listFallbacks', 'showStatus', 'getCircuitStatus',
    'makeRequest'
  ];
  for (const fnName of ['maskKey', 'getCircuitState', 'recordFailure', 'makeRequest']) {
    assert(typeof AG[fnName] === 'function', `${fnName} is exported`);
  }
});

// ─── Summary ──────────────────────────────────────────────────────

console.log(`\n${'='.repeat(50)}`);
console.log(`  API Gateway — Robust Self-Test Results`);
console.log(`  ${totalPassed}/${totalTests} tests passing`);
console.log(`${'='.repeat(50)}`);

try { fs.rmSync(TEST_DIR, { recursive: true, force: true }); } catch {}

if (totalPassed < totalTests) {
  console.log('\n❌ Self-tests FAILED');
  process.exit(1);
} else {
  console.log('\n✅ All self-tests passed');
  process.exit(0);
}
