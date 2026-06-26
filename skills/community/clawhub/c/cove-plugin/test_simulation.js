#!/usr/bin/env node
/**
 * CoVe Plugin — Test Suite
 *
 * Tests the plugin components without requiring a live LLM.
 * For live integration tests, set COVE_LIVE_TEST=1.
 *
 * Usage:
 *   npm test              # Unit tests (no LLM needed)
 *   COVE_LIVE_TEST=1 npm test  # Full integration test (needs running sidecar)
 */

const { loadConfig, parseSimpleYaml } = require('./src/config');
const { loadKnowledge, readDir } = require('./src/knowledge');
const { braveSearch } = require('./src/web_search');
const { logResult } = require('./src/csm-logger');

let passed = 0;
let failed = 0;

function assert(condition, name) {
  if (condition) {
    console.log(`  ✅ ${name}`);
    passed++;
  } else {
    console.log(`  ❌ ${name}`);
    failed++;
  }
}

// ── Config tests ────────────────────────────────────────────────────────────

console.log('\n📋 Config tests');

const yaml = `
policy: "standard"
max_correction_attempts: 2
auto_correct: false
log_results_to_dashboard: true

knowledge_sources:
  use_system_memory: true
  document_paths: ["/tmp/docs"]
  enable_web_search: true
`;

const parsed = parseSimpleYaml(yaml);
assert(parsed.policy === 'standard', 'Parses string values');
assert(parsed.max_correction_attempts === 2, 'Parses integer values');
assert(parsed.auto_correct === false, 'Parses boolean false');
assert(parsed.log_results_to_dashboard === true, 'Parses boolean true');
assert(parsed.knowledge_sources?.use_system_memory === true, 'Parses nested boolean');
assert(parsed.knowledge_sources?.enable_web_search === true, 'Parses nested web_search');
assert(Array.isArray(parsed.knowledge_sources?.document_paths), 'Parses inline array');

const config = loadConfig();
assert(typeof config.policy === 'string', 'loadConfig returns policy');
assert(typeof config.auto_correct === 'boolean', 'loadConfig returns auto_correct');
assert(typeof config.knowledge_sources === 'object', 'loadConfig returns knowledge_sources');

// ── Knowledge tests ─────────────────────────────────────────────────────────

console.log('\n📚 Knowledge tests');

const knowledge = loadKnowledge(config);
assert(typeof knowledge === 'string', 'loadKnowledge returns string');
console.log(`    Knowledge context length: ${knowledge.length} chars`);

// ── Logger tests ────────────────────────────────────────────────────────────

console.log('\n📝 Logger tests');

const mockReport = {
  verified: false,
  claims: [
    { claim: 'test claim', status: 'verified', source: 'test.md', correction: null },
    { claim: 'wrong claim', status: 'inaccurate', source: 'data.csv', correction: 'correct info' },
  ],
  summary: { total: 2, verified: 1, inaccurate: 1, unverifiable: 0 },
  durationMs: 1234,
};

// Capture console output
const origLog = console.log;
let logOutput = '';
console.log = (msg) => { logOutput += msg + '\n'; };
logResult(mockReport, { log_results_to_dashboard: true });
console.log = origLog;

assert(logOutput.includes('[cove]'), 'Logger outputs with [cove] prefix');
assert(logOutput.includes('2 claims'), 'Logger reports claim count');
assert(logOutput.includes('wrong claim'), 'Logger reports inaccuracies');

// ── Web search tests ────────────────────────────────────────────────────────

console.log('\n🌐 Web search tests');

assert(typeof braveSearch === 'function', 'braveSearch is a function');
assert(config.brave_api_key === null || typeof config.brave_api_key === 'string', 'brave_api_key resolved in config');
console.log(`    Brave API key: ${config.brave_api_key ? 'found' : 'not configured'}`);

// Direct LLM provider tests
console.log('\n🤖 LLM provider tests');

assert(config.llm_provider === null || typeof config.llm_provider === 'string', 'llm_provider resolved in config');
assert(config.llm_api_key === null || typeof config.llm_api_key === 'string', 'llm_api_key resolved in config');
console.log(`    LLM provider: ${config.llm_provider || 'sidecar (default)'}`);
console.log(`    LLM API key: ${config.llm_api_key ? 'found' : 'not set (will use sidecar)'}`);

// ── Vector store tests ──────────────────────────────────────────────────────

console.log('\n🗄️  Vector store tests');

const { queryVectorStore, listProviders } = require('./src/vector_store');
assert(typeof queryVectorStore === 'function', 'queryVectorStore is a function');
assert(typeof listProviders === 'function', 'listProviders is a function');

const providers = listProviders();
assert(providers.includes('qdrant'), 'Supports Qdrant');
assert(providers.includes('chroma'), 'Supports Chroma');
assert(providers.includes('weaviate'), 'Supports Weaviate');
assert(providers.includes('milvus'), 'Supports Milvus');
assert(providers.includes('redis'), 'Supports Redis');
assert(providers.includes('openviking'), 'Supports OpenViking');
console.log(`    Providers: ${providers.join(', ')}`);

// ── Live integration test ───────────────────────────────────────────────────

if (process.env.COVE_LIVE_TEST === '1') {
  console.log('\n🔴 Live integration test (requires running OpenClaw sidecar)');

  const { verifyResponse } = require('./src/verify_claims');

  (async () => {
    try {
      const report = await verifyResponse(
        'The Earth orbits the Sun at approximately 150 million kilometers.',
        { policy: 'basic', auto_correct: true }
      );

      assert(report.claims.length > 0, 'Live test: extracted claims');
      assert(typeof report.verified === 'boolean', 'Live test: returned verified flag');
      assert(typeof report.summary === 'object', 'Live test: returned summary');
      console.log(`    Claims found: ${report.summary.total}`);
      console.log(`    Verified: ${report.summary.verified}, Inaccurate: ${report.summary.inaccurate}`);
      console.log(`    Duration: ${report.durationMs}ms`);

      printSummary();
    } catch (err) {
      console.log(`  ❌ Live test failed: ${err.message}`);
      failed++;
      printSummary();
    }
  })();
} else {
  console.log('\n💡 Set COVE_LIVE_TEST=1 to run live integration tests.');
  printSummary();
}

function printSummary() {
  console.log('\n═══════════════════════════════');
  console.log(`  ${passed} passed, ${failed} failed`);
  console.log('═══════════════════════════════\n');
  process.exit(failed > 0 ? 1 : 0);
}
