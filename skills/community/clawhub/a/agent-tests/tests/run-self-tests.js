#!/usr/bin/env node
/**
 * SAFETY: Test infrastructure only — calls `node agent-tests.js` with
 * hardcoded flags; no user input enters the shell. This is test
 * infrastructure, not production agent code.
 */
/**
 * Agent Tests — Self-Test Suite
 * 
 * Tests the framework's own assertion engine, report generation,
 * regression detection, and CLI integration.
 * 
 * Run: node tests/run-self-tests.js
 */

const path = require('path');

// Load the framework's assertion engine directly
const AT = require(path.resolve(__dirname, '..', 'agent-tests.js'));

// ─── Test Runner ──────────────────────────────────────────────────────────

let totalTests = 0;
let totalPassed = 0;
const results = [];

function assert(condition, description) {
  totalTests++;
  const passed = !!condition;
  if (passed) totalPassed++;
  results.push({ passed, description });
  console.log(`  ${passed ? '✅' : '❌'} ${description}`);
  return passed;
}

function group(name, fn) {
  console.log(`\n📋 ${name}`);
  fn();
}

// ─── 1. evaluateAssertion Tests ──────────────────────────────────────────

group('evaluateAssertion() — 9 cases', () => {
  assert(AT.evaluateAssertion('contains:Hello', 'Hello world', 'Hello'),
    'Default: "Hello" in "Hello world"');
  assert(!AT.evaluateAssertion('contains:xyz', 'Hello world', 'xyz'),
    'Default: "xyz" NOT in "Hello world"');
  assert(AT.evaluateAssertion('contains:test', 'this is a test', 'test'),
    'contains: — substring match');
  assert(!AT.evaluateAssertion('contains:missing', 'hello world', 'missing'),
    'contains: — substring not found');
  assert(AT.evaluateAssertion('not_contains:error', 'all good', 'error'),
    'not_contains: — value absent');
  assert(!AT.evaluateAssertion('not_contains:hello', 'hello world', 'hello'),
    'not_contains: — value present (should fail)');
  assert(AT.evaluateAssertion('regex:\\d{3}', 'abc123def', '123'),
    'regex: — pattern matches');
  assert(!AT.evaluateAssertion('regex:\\d{3}', 'abc12def', '123'),
    'regex: — pattern does not match');
  assert(AT.evaluateAssertion('length:5', 'hello', '5'),
    'length: — exact match');
  assert(!AT.evaluateAssertion('length:4', 'hello', '4'),
    'length: — wrong length');
});

// ─── 2. Report Generation Tests ──────────────────────────────────────────

group('Report generation — 4 cases', () => {
  const emptyReport = AT.generateRegressionReport([]);
  assert(emptyReport.includes('No test results'),
    'Empty results shows "no results" message');
  
  const singleResult = [{
    testName: 'test-a',
    timestamp: '2026-06-20T10:00:00Z',
    duration: 50,
    passed: true,
    assertions: [{ assertion: 'contains:ok', passed: true }]
  }];
  const singleReport = AT.generateRegressionReport(singleResult);
  assert(singleReport.includes('test-a'),
    'Single test appears in report');
  assert(singleReport.includes('100%'),
    '100% pass rate for single pass');
  
  const mixedResults = [
    { testName: 'test-b', timestamp: '2026-06-20T10:00:00Z', duration: 50, passed: true, assertions: [] },
    { testName: 'test-b', timestamp: '2026-06-20T10:01:00Z', duration: 60, passed: false, assertions: [{ assertion: 'contains:fail', passed: false }] },
    { testName: 'test-b', timestamp: '2026-06-20T10:02:00Z', duration: 55, passed: true, assertions: [] }
  ];
  const mixedReport = AT.generateRegressionReport(mixedResults);
  assert(mixedReport.includes('67%'),
    'Mixed results shows correct pass rate');
  assert(mixedReport.includes('test-b'),
    'Test name appears in report');
});

// ─── 3. Regression Detection Tests ───────────────────────────────────────

group('Regression detection — 3 cases', () => {
  const noRegression = AT.detectRegression(
    [{ passed: true }, { passed: true }],
    [{ passed: true }, { passed: true }]
  );
  assert(!noRegression, 'Identical results = no regression');
  
  const regression = AT.detectRegression(
    [{ passed: true }, { passed: true }],
    [{ passed: true }, { passed: false }]
  );
  assert(regression, 'Worse results = regression detected');
  
  const improvement = AT.detectRegression(
    [{ passed: false }, { passed: false }],
    [{ passed: true }, { passed: true }]
  );
  assert(!improvement, 'Better results = no regression');
});

// ─── 4. CLI Integration Tests ────────────────────────────────────────────

group('CLI integration — 5 cases', async () => {
  const testDir = path.join(__dirname, 'fixtures', 'cli-test-' + Date.now());
  process.env.TEST_DIR = testDir;
  
  const addResult = AT.addTest('self-test-example', 'Test prompt', 'test output');
  assert(addResult === true, 'addTest returns true');
  
  const tests = AT.loadTests(testDir);
  assert(tests['self-test-example'] !== undefined, 'addTest persists to file');
  assert(tests['self-test-example'].name === 'self-test-example', 'addTest sets correct name');
  assert(tests['self-test-example'].prompt === 'Test prompt', 'addTest sets correct prompt');
  assert(tests['self-test-example'].expected === 'test output', 'addTest sets correct expected');
  
  const listResult = AT.listTests(testDir);
  assert(listResult.includes('self-test-example'), 'listTests shows added test');
  
  AT.removeTest('self-test-example', testDir);
  const afterRemove = AT.loadTests(testDir);
  assert(afterRemove['self-test-example'] === undefined, 'removeTest removes from file');
  
  delete process.env.TEST_DIR;
});

// ─── 5. Error Handling Tests ─────────────────────────────────────────────

group('Error handling — 2 cases', async () => {
  const invalidDir = path.join(__dirname, 'fixtures', 'invalid-' + Date.now());
  process.env.TEST_DIR = invalidDir;
  
  const tests = AT.loadTests(invalidDir);
  assert(Array.isArray(tests) || typeof tests === 'object', 'loadTests handles missing file gracefully');
  
  const runResult = await AT.runTest('nonexistent-test', invalidDir);
  assert(runResult === null, 'runTest returns null for missing test');
  
  delete process.env.TEST_DIR;
});

// ─── Summary ──────────────────────────────────────────────────────────────

console.log('\n═══════════════════════════════════════');
console.log(`  Agent Tests Self-Test Results`);
console.log(`  ${totalPassed}/${totalTests} tests passing`);
console.log('═══════════════════════════════════════');

if (totalPassed < totalTests) {
  console.log('\n❌ Self-tests FAILED — do not publish until fixed');
  process.exit(1);
} else {
  console.log('\n✅ All self-tests passed');
  process.exit(0);
}
