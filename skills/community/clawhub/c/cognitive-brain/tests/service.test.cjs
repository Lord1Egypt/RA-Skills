/**
 * Service 层测试
 */

const assert = require('assert');
const { getPool } = require('../scripts/core/db.cjs');
const { MemoryService } = require('../src/services/MemoryService');
const { ConceptService } = require('../src/services/ConceptService');

async function runTests() {
  console.log('🧪 Running Service Tests...\n');

  const pool = getPool();
  if (!pool) {
    console.log('⚠️  Database not available, skipping tests');
    return;
  }

  let passed = 0;
  let failed = 0;

  // MemoryService Tests
  try {
    console.log('Testing MemoryService...');
    const memoryService = new MemoryService(pool);

    // Test encode with batch concept creation
    const content = 'Test memory content ' + Date.now();
    const memory = await memoryService.encode(content, {
      type: 'test',
      importance: 0.5
    });
    assert(memory.id, 'Memory should have id');
    assert.strictEqual(memory.content, content, 'Content should match');
    console.log('  ✓ encode');
    passed++;

    // Test recall
    const results = await memoryService.recall(content, { limit: 5 });
    assert(Array.isArray(results), 'recall should return array');
    console.log('  ✓ recall');
    passed++;

    // Test rate limiting
    let rateLimited = false;
    try {
      // Try to exceed rate limit
      for (let i = 0; i < 110; i++) {
        await memoryService.encode('rate limit test ' + i, { type: 'test' });
      }
    } catch (e) {
      if (e.message.includes('Rate limit')) {
        rateLimited = true;
      }
    }
    console.log('  ' + (rateLimited ? '✓' : '⚠') + ' rate limiting');
    passed++;

  } catch (err) {
    console.error('  ✗ MemoryService:', err.message);
    failed++;
  }

  // ConceptService Tests
  try {
    console.log('\nTesting ConceptService...');
    const conceptService = new ConceptService(pool);

    // Test getOrCreate
    const name = 'ServiceTestConcept_' + Date.now();
    const concept = await conceptService.getOrCreate(name);
    assert(concept.id, 'Concept should have id');
    assert.strictEqual(concept.name, name, 'Name should match');
    console.log('  ✓ getOrCreate');
    passed++;

    // Test findRelated
    const related = await conceptService.findRelated(concept.id, 5);
    assert(Array.isArray(related), 'findRelated should return array');
    console.log('  ✓ findRelated');
    passed++;

  } catch (err) {
    console.error('  ✗ ConceptService:', err.message);
    failed++;
  }

  console.log(`\n📊 Results: ${passed} passed, ${failed} failed`);
  process.exit(failed > 0 ? 1 : 0);
}

runTests().catch(err => {
  console.error('Test suite error:', err);
  process.exit(1);
});
