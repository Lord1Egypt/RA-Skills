// test/signalDetect.test.js
// Unit tests for evolver-signal-detect.js stratification logic

const test = require('node:test');
const assert = require('node:assert');

// Simulate the stratifyContent and detectSignals functions from evolver-signal-detect.js
const SIGNAL_KEYWORDS = {
  perf_bottleneck: ['timeout', 'slow', 'latency', 'bottleneck', 'oom', 'out of memory', 'performance'],
  capability_gap: ['not supported', 'unsupported', 'not implemented', 'missing feature', 'not available'],
  log_error: ['error:', 'exception:', 'typeerror', 'referenceerror', 'syntaxerror', 'failed'],
  user_feature_request: ['add feature', 'implement', 'new function', 'new module', 'please add'],
  recurring_error: ['same error', 'still failing', 'not fixed', 'keeps failing', 'repeatedly'],
  deployment_issue: ['deploy failed', 'build failed', 'ci failed', 'pipeline', 'rollback'],
  test_failure: ['test failed', 'test failure', 'assertion', 'expect(', 'assert.'],
};

function stratifyContent(text) {
  const lines = text.split('\n');
  const documentText = [];

  for (const line of lines) {
    const trimmed = line.trim();
    if (trimmed.startsWith('//') || trimmed.startsWith('#') || trimmed.startsWith('*') ||
        trimmed.startsWith('{') || trimmed.startsWith('[') || trimmed.startsWith('}') ||
        trimmed.startsWith(']') || trimmed.startsWith('/*')) {
      continue;
    }
    documentText.push(line);
  }

  return documentText.join('\n');
}

function detectSignals(text) {
  if (!text || typeof text !== 'string') return [];

  const stratified = stratifyContent(text);
  const lower = stratified.toLowerCase();

  const found = [];
  for (const [signal, keywords] of Object.entries(SIGNAL_KEYWORDS)) {
    for (const kw of keywords) {
      if (lower.includes(kw)) {
        found.push(signal);
        break;
      }
    }
  }
  return [...new Set(found)];
}

test('signalDetect: filters code lines', (t) => {
  const input = 'const x = {"error": "timeout"};  // error handling\nActual issue: timeout occurred';
  const signals = detectSignals(input);

  assert.strictEqual(signals.length, 1, 'Should detect only real error from document text');
  assert(signals.includes('perf_bottleneck'), 'Should detect timeout as bottleneck');
  assert(!signals.includes('log_error'), 'Should not detect error from JSON field');
});

test('signalDetect: filters comment lines', (t) => {
  const input = 'The system failed because:\n// TODO: Handle error cases\n// Need to catch exceptions\nActual error: connection refused';
  const signals = detectSignals(input);

  assert.strictEqual(signals.length, 1, 'Should not detect from comments');
  assert(signals.includes('log_error'), 'Should detect real error');
});

test('signalDetect: filters JSON structure', (t) => {
  const input = '{\n  "status": "error",\n  "message": "failed"\n}\nThe API returned an error response';
  const signals = detectSignals(input);

  assert.strictEqual(signals.length, 1, 'Should not double-count from JSON');
  assert(signals.includes('log_error'), 'Should detect real error message');
});

test('signalDetect: detects perf_bottleneck', (t) => {
  const input = 'The database query is slow and causes timeouts in production';
  const signals = detectSignals(input);

  assert(signals.includes('perf_bottleneck'), 'Should detect slow/timeout');
});

test('signalDetect: detects capability_gap', (t) => {
  const input = 'This feature is not supported in the current version';
  const signals = detectSignals(input);

  assert(signals.includes('capability_gap'), 'Should detect not supported');
});

test('signalDetect: detects user_feature_request', (t) => {
  const input = 'We need to implement a new module for data processing';
  const signals = detectSignals(input);

  assert(signals.includes('user_feature_request'), 'Should detect implement/new');
});

test('signalDetect: detects deployment_issue', (t) => {
  const input = 'The build failed during CI pipeline execution';
  const signals = detectSignals(input);

  assert(signals.includes('deployment_issue'), 'Should detect build/CI failed');
});

test('signalDetect: detects test_failure', (t) => {
  const input = 'Test failed: assertion error in payload validation';
  const signals = detectSignals(input);

  assert(signals.includes('test_failure'), 'Should detect test failure');
});

test('signalDetect: handles empty input', (t) => {
  const signals = detectSignals('');
  assert.strictEqual(signals.length, 0, 'Should handle empty string');
});

test('signalDetect: handles null/undefined', (t) => {
  assert.deepStrictEqual(detectSignals(null), [], 'Should handle null');
  assert.deepStrictEqual(detectSignals(undefined), [], 'Should handle undefined');
});

test('signalDetect: ignores code blocks', (t) => {
  const input = `
function handleError() {
  if (error) {
    throw new Error("Exception occurred");
  }
}

The actual production error was connection timeout
`;
  const signals = detectSignals(input);

  // Should only detect "timeout" from document, not from code
  assert(signals.includes('perf_bottleneck'), 'Should detect timeout');
  assert(!signals.includes('log_error'), 'Should filter error from code');
});

test('signalDetect: multi-signal detection', (t) => {
  const input = `
Error: timeout occurred
The API is slow and the feature is not supported
Test failed with assertion error
`;
  const signals = detectSignals(input);

  assert(signals.includes('log_error'), 'Should detect error');
  assert(signals.includes('perf_bottleneck'), 'Should detect slow');
  assert(signals.includes('capability_gap'), 'Should detect not supported');
  assert(signals.includes('test_failure'), 'Should detect test failure');
});

test('signalDetect: deduplication', (t) => {
  const input = 'Error: timeout. Another error: connection failed. Error: OOM.';
  const signals = detectSignals(input);

  assert.strictEqual(signals.length, 2, 'Should deduplicate signal types');
  assert(signals.includes('log_error'), 'Should have log_error');
  assert(signals.includes('perf_bottleneck'), 'Should have perf_bottleneck');
});
