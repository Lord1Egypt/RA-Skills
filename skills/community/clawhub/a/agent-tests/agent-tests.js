#!/usr/bin/env node
/**
 * Agent Testing Framework — Define, run, and track tests for agent behavior
 * 
 * Modes:
 *   --test <name> <prompt> <expected> [assertions...]  → Run a single test
 *   --test --list                                       → List all tests
 *   --test --run [name]                                 → Run test(s)
 *   --test --add <name> <prompt> <expected> [assertions...]  → Add test case
 *   --test --remove <name>                              → Remove test case
 *   --regression                                        → Show regression report
 *   --benchmark <test> [iterations]                     → Run performance benchmark
 *   --status                                            → Test suite status
 */

const fs = require('fs');
const path = require('path');

const WORKSPACE = (() => {
  if (process.env.TEST_DIR) return process.env.TEST_DIR;
  let dir = __dirname;
  for (let i = 0; i < 10; i++) {
    if (fs.existsSync(path.join(dir, 'MEMORY.md'))) return dir;
    dir = path.resolve(dir, '..');
  }
  return path.resolve(__dirname, '..', '..');
})();

const DATA_DIR = path.join(WORKSPACE, 'memory', 'agent-tests');
const TESTS_FILE = path.join(DATA_DIR, 'tests.json');
const RESULTS_FILE = path.join(DATA_DIR, 'results.json');
const BENCHMARKS_FILE = path.join(DATA_DIR, 'benchmarks.json');

function ensureDir(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

function loadJSON(file, fallback) {
  try {
    const data = fs.readFileSync(file, 'utf8');
    return JSON.parse(data);
  } catch { return fallback || {}; }
}

// ─── EXPORTS (for self-tests) ──────────────────────────────────────────────
function getTestDir() {
  return process.env.TEST_DIR || DATA_DIR;
}
function getTestsFile() {
  return path.join(getTestDir(), 'tests.json');
}
function getResultsFile() {
  return path.join(getTestDir(), 'results.json');
}

module.exports = {
  evaluateAssertion,
  loadTests: (dir) => loadJSON(path.join(dir || getTestDir(), 'tests.json'), {}),
  addTest: (name, prompt, expected, assertions) => {
    const tf = getTestsFile();
    const tests = loadJSON(tf, {});
    tests[name] = { name, prompt, expected, assertions, created: getToday(), updated: getToday(), runCount: 0, passRate: 0 };
    saveJSON(tf, tests);
    return true;
  },
  removeTest: (name, dir) => {
    const tf = path.join(dir || getTestDir(), 'tests.json');
    const tests = loadJSON(tf, {});
    if (tests[name]) { delete tests[name]; saveJSON(tf, tests); }
  },
  listTests: (dir) => {
    const tests = loadJSON(path.join(dir || getTestDir(), 'tests.json'), {});
    const entries = Object.entries(tests);
    if (entries.length === 0) return '[agent-tests] No tests defined.';
    let output = `[agent-tests] Defined tests (${entries.length}):\n\n${'Name'.padEnd(25)} ${'Runs'.padEnd(8)} ${'Pass Rate'.padEnd(12)} ${'Updated'.padEnd(12)}\n${'-'.repeat(60)}\n`;
    for (const [name, test] of entries) {
      const rate = test.passRate > 0 ? `${test.passRate}%` : 'N/A';
      output += `${name.padEnd(25)} ${String(test.runCount || 0).padEnd(8)} ${rate.padEnd(12)} ${test.updated.padEnd(12)}\n`;
    }
    return output;
  },
  runTest: async (name, dir) => {
    const tf = path.join(dir || getTestDir(), 'tests.json');
    const tests = loadJSON(tf, {});
    if (!tests[name]) return null;
    const test = tests[name];
    const actualOutput = '[agent would produce output here]';
    const assertions = test.assertions.map(a => ({ assertion: a, passed: evaluateAssertion(a, actualOutput, test.expected) }));
    const allPassed = assertions.every(a => a.passed);
    return { name, passed: allPassed, duration: 0, assertions };
  },
  generateRegressionReport: (results) => {
    if (results.length === 0) return '[agent-tests] No test results yet.';
    const byTest = {};
    for (const r of results) { if (!byTest[r.testName]) byTest[r.testName] = []; byTest[r.testName].push(r); }
    let report = '';
    for (const [name, testResults] of Object.entries(byTest)) {
      const total = testResults.length;
      const passed = testResults.filter(r => r.passed).length;
      const rate = Math.round((passed / total) * 100);
      report += `  ${name}: ${rate}% (${passed}/${total})\n`;
    }
    return report;
  },
  detectRegression: (oldResults, newResults) => {
    if (oldResults.length !== newResults.length) return true;
    for (let i = 0; i < oldResults.length; i++) {
      if (oldResults[i].passed && !newResults[i].passed) return true;
    }
    return false;
  }
};

function saveJSON(file, data) {
  ensureDir(path.dirname(file));
  fs.writeFileSync(file, JSON.stringify(data, null, 2), 'utf8');
}

function getToday() {
  return new Date().toISOString().split('T')[0];
}

// ─── TEST MANAGEMENT ──────────────────────────────────────────────────────

function addTest(name, prompt, expected, assertions = []) {
  const tests = loadJSON(TESTS_FILE, {});
  tests[name] = {
    name,
    prompt,
    expected,
    assertions,
    created: getToday(),
    updated: getToday(),
    runCount: 0,
    passRate: 0
  };
  saveJSON(TESTS_FILE, tests);
  console.log(`[agent-tests] Added test: ${name}`);
}

function removeTest(name) {
  const tests = loadJSON(TESTS_FILE, {});
  if (tests[name]) {
    delete tests[name];
    saveJSON(TESTS_FILE, tests);
    console.log(`[agent-tests] Removed test: ${name}`);
  } else {
    console.log(`[agent-tests] Not found: ${name}`);
  }
}

function listTests() {
  const tests = loadJSON(TESTS_FILE, {});
  const entries = Object.entries(tests);
  
  if (entries.length === 0) {
    console.log('[agent-tests] No tests defined.');
    return;
  }
  
  console.log(`[agent-tests] Defined tests (${entries.length}):\n`);
  console.log(`${'Name'.padEnd(25)} ${'Runs'.padEnd(8)} ${'Pass Rate'.padEnd(12)} ${'Updated'.padEnd(12)}`);
  console.log('-'.repeat(60));
  
  for (const [name, test] of entries) {
    const rate = test.passRate > 0 ? `${test.passRate}%` : 'N/A';
    console.log(`${name.padEnd(25)} ${String(test.runCount || 0).padEnd(8)} ${rate.padEnd(12)} ${test.updated.padEnd(12)}`);
  }
}

// ─── RUN TEST ──────────────────────────────────────────────────────────────

async function runTest(name) {
  const tests = loadJSON(TESTS_FILE, {});
  const results = loadJSON(RESULTS_FILE, []);
  
  if (!tests[name]) {
    console.log(`[agent-tests] Test not found: ${name}`);
    return null;
  }
  
  const test = tests[name];
  const startTime = Date.now();
  
  console.log(`[agent-tests] Running: ${name}`);
  console.log(`  Prompt: ${test.prompt.substring(0, 100)}...`);
  console.log(`  Expected: ${test.expected.substring(0, 100)}...`);
  
  // In production, this would call the agent/model to get the actual output
  // For now, we simulate the test framework structure
  const actualOutput = '[agent would produce output here]';
  const endTime = Date.now();
  const duration = endTime - startTime;
  
  // Run assertions
  const assertions = [];
  let allPassed = true;
  
  for (const assertion of test.assertions) {
    const passed = evaluateAssertion(assertion, actualOutput, test.expected);
    assertions.push({ assertion, passed });
    if (!passed) allPassed = false;
  }
  
  // Update test stats
  test.runCount = (test.runCount || 0) + 1;
  const total = test.runCount;
  const prevPasses = (test.passRate / 100) * (total - 1) || 0;
  test.passRate = Math.round(((prevPasses + (allPassed ? 1 : 0)) / total) * 100);
  test.updated = getToday();
  saveJSON(TESTS_FILE, tests);
  
  // Record result
  results.push({
    testName: name,
    timestamp: new Date().toISOString(),
    duration,
    passed: allPassed,
    assertions,
    actualOutput: actualOutput.substring(0, 500),
    expectedOutput: test.expected.substring(0, 500)
  });
  if (results.length > 1000) results.splice(0, results.length - 1000);
  saveJSON(RESULTS_FILE, results);
  
  const icon = allPassed ? '✅' : '❌';
  console.log(`  Result: ${icon} ${allPassed ? 'PASS' : 'FAIL'} (${duration}ms)`);
  
  return { name, passed: allPassed, duration, assertions };
}

function evaluateAssertion(assertion, actual, expected) {
  // Simple assertion evaluator
  if (assertion.startsWith('contains:')) {
    return actual.includes(assertion.replace('contains:', ''));
  }
  if (assertion.startsWith('not_contains:')) {
    return !actual.includes(assertion.replace('not_contains:', ''));
  }
  if (assertion.startsWith('regex:')) {
    const regex = new RegExp(assertion.replace('regex:', ''));
    return regex.test(actual);
  }
  if (assertion.startsWith('length:')) {
    const len = parseInt(assertion.replace('length:', ''));
    return actual.length === len;
  }
  // Default: check if expected is in actual
  return actual.includes(expected);
}

// ─── REGRESSION ────────────────────────────────────────────────────────────

function showRegression() {
  const results = loadJSON(RESULTS_FILE, []);
  
  if (results.length === 0) {
    console.log('[agent-tests] No test results yet.');
    return;
  }
  
  console.log(`[agent-tests] Regression report (${results.length} tests run):\n`);
  
  // Group by test name
  const byTest = {};
  for (const r of results) {
    if (!byTest[r.testName]) byTest[r.testName] = [];
    byTest[r.testName].push(r);
  }
  
  for (const [name, testResults] of Object.entries(byTest)) {
    const total = testResults.length;
    const passed = testResults.filter(r => r.passed).length;
    const rate = Math.round((passed / total) * 100);
    const avgDuration = Math.round(testResults.reduce((s, r) => s + r.duration, 0) / total);
    
    const icon = rate === 100 ? '✅' : rate >= 80 ? '⚠️' : '❌';
    console.log(`  ${icon} ${name}: ${rate}% (${passed}/${total}) — avg ${avgDuration}ms`);
    
    // Show recent failures
    const failures = testResults.filter(r => !r.passed);
    if (failures.length > 0) {
      console.log(`    Recent failures:`);
      for (const f of failures.slice(-3)) {
        console.log(`      ${f.timestamp}: ${f.assertions.filter(a => !a.passed).map(a => a.assertion).join(', ')}`);
      }
    }
  }
}

// ─── BENCHMARK ─────────────────────────────────────────────────────────────

async function benchmark(testName, iterations = 5) {
  const tests = loadJSON(TESTS_FILE, {});
  const results = loadJSON(RESULTS_FILE, []);
  
  if (!tests[testName]) {
    console.log(`[agent-tests] Test not found: ${testName}`);
    return;
  }
  
  console.log(`[agent-tests] Benchmarking: ${testName} (${iterations} iterations)\n`);
  
  const durations = [];
  let totalPassed = 0;
  
  for (let i = 0; i < iterations; i++) {
    const start = Date.now();
    const result = await runTest(testName);
    const duration = Date.now() - start;
    durations.push(duration);
    if (result && result.passed) totalPassed++;
  }
  
  const avgDuration = Math.round(durations.reduce((a, b) => a + b, 0) / durations.length);
  const minDuration = Math.min(...durations);
  const maxDuration = Math.max(...durations);
  const passRate = Math.round((totalPassed / iterations) * 100);
  
  console.log(`\n[Benchmark] ${testName}:`);
  console.log(`  Average: ${avgDuration}ms`);
  console.log(`  Min: ${minDuration}ms`);
  console.log(`  Max: ${maxDuration}ms`);
  console.log(`  Pass rate: ${passRate}%`);
  
  // Save benchmark
  const benchmarks = loadJSON(BENCHMARKS_FILE, {});
  if (!benchmarks[testName]) benchmarks[testName] = [];
  benchmarks[testName].push({
    timestamp: new Date().toISOString(),
    iterations,
    avgDuration,
    minDuration,
    maxDuration,
    passRate
  });
  if (benchmarks[testName].length > 50) benchmarks[testName].splice(0, benchmarks[testName].length - 50);
  saveJSON(BENCHMARKS_FILE, benchmarks);
}

// ─── STATUS ────────────────────────────────────────────────────────────────

function showStatus() {
  const tests = loadJSON(TESTS_FILE, {});
  const results = loadJSON(RESULTS_FILE, []);
  const benchmarks = loadJSON(BENCHMARKS_FILE, {});
  
  const entries = Object.entries(tests);
  const totalRuns = entries.reduce((s, [, t]) => s + (t.runCount || 0), 0);
  
  console.log('[agent-tests] Status:\n');
  console.log(`  Tests defined: ${entries.length}`);
  console.log(`  Total runs: ${totalRuns}`);
  console.log(`  Results recorded: ${results.length}`);
  console.log(`  Benchmarks: ${Object.keys(benchmarks).length} tests`);
  
  if (entries.length > 0) {
    const passed = entries.filter(([, t]) => t.passRate === 100).length;
    console.log(`  100% pass rate: ${passed}/${entries.length}`);
  }
}

// ─── CLI ───────────────────────────────────────────────────────────────────

const args = process.argv.slice(2);
let mode = 'status';
let searchQuery = null;

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--test') mode = 'test';
  if (args[i] === '--regression') mode = 'regression';
  if (args[i] === '--benchmark') mode = 'benchmark';
  if (args[i] === '--status') mode = 'status';
  if (args[i] === '--list') searchQuery = 'list';
  if (args[i] === '--run') searchQuery = 'run';
  if (args[i] === '--add') searchQuery = 'add';
  if (args[i] === '--remove') searchQuery = 'remove';
  if (args[i] === '--dir' && i + 1 < args.length) process.env.TEST_DIR = args[i + 1];
}

(async () => {
  switch (mode) {
    case 'test': {
      if (searchQuery === 'list') listTests();
      else if (searchQuery === 'run') {
        const testName = args[2];
        if (testName) await runTest(testName);
        else {
          const tests = loadJSON(TESTS_FILE, {});
          for (const name of Object.keys(tests)) await runTest(name);
        }
      } else if (searchQuery === 'add') {
        const name = args[2];
        const prompt = args[3];
        const expected = args[4];
        const assertions = args.slice(5);
        if (!name || !prompt || !expected) {
          console.log('Usage: agent-tests.js --test --add <name> <prompt> <expected> [assertions...]');
        } else {
          addTest(name, prompt, expected, assertions);
        }
      } else if (searchQuery === 'remove') {
        removeTest(args[2]);
      } else {
        console.log('Usage: agent-tests.js --test --list|--run|--add|--remove');
      }
      break;
    }
    case 'regression':
      showRegression();
      break;
    case 'benchmark': {
      const testName = args[2];
      const iterations = parseInt(args[3]) || 5;
      if (!testName) {
        console.log('Usage: agent-tests.js --benchmark <test> [iterations]');
      } else {
        await benchmark(testName, iterations);
      }
      break;
    }
    default:
      showStatus();
      break;
  }
})();
