/**
 * 测试框架 Setup
 */
const path = require('path');

// 设置测试环境
process.env.NODE_ENV = 'test';
process.env.COGNITIVE_BRAIN_DIR = path.join(__dirname, '..');

// 简单的测试工具
const tests = [];
let beforeAllFn = null;
let afterAllFn = null;

function describe(name, fn) {
  console.log(`\n📦 ${name}`);
  fn();
}

function test(name, fn) {
  tests.push({ name, fn });
}

function beforeAll(fn) {
  beforeAllFn = fn;
}

function afterAll(fn) {
  afterAllFn = fn;
}

function expect(actual) {
  return {
    toBe(expected) {
      if (actual !== expected) {
        throw new Error(`Expected ${expected}, got ${actual}`);
      }
    },
    toEqual(expected) {
      if (JSON.stringify(actual) !== JSON.stringify(expected)) {
        throw new Error(`Expected ${JSON.stringify(expected)}, got ${JSON.stringify(actual)}`);
      }
    },
    toBeDefined() {
      if (actual === undefined) {
        throw new Error(`Expected value to be defined`);
      }
    },
    toBeGreaterThan(expected) {
      if (!(actual > expected)) {
        throw new Error(`Expected ${actual} to be greater than ${expected}`);
      }
    },
    toHaveProperty(key) {
      if (!(key in actual)) {
        throw new Error(`Expected object to have property ${key}`);
      }
    },
    toBeNull() {
      if (actual !== null) {
        throw new Error(`Expected null, got ${actual}`);
      }
    }
  };
}

async function runTests() {
  console.log('\n🧪 Running Cognitive Brain Tests\n');
  console.log('='.repeat(60));
  
  let passed = 0;
  let failed = 0;
  
  if (beforeAllFn) {
    try {
      await beforeAllFn();
    } catch (e) {
      console.error('❌ beforeAll failed:', e.message);
      return;
    }
  }
  
  for (const { name, fn } of tests) {
    try {
      await fn();
      console.log(`  ✅ ${name}`);
      passed++;
    } catch (e) {
      console.log(`  ❌ ${name}`);
      console.log(`     ${e.message}`);
      failed++;
    }
  }
  
  if (afterAllFn) {
    try {
      await afterAllFn();
    } catch (e) {
      console.error('❌ afterAll failed:', e.message);
    }
  }
  
  console.log('\n' + '='.repeat(60));
  console.log(`\nResults: ${passed} passed, ${failed} failed`);
  
  process.exit(failed > 0 ? 1 : 0);
}

module.exports = { describe, test, beforeAll, afterAll, expect, runTests };

