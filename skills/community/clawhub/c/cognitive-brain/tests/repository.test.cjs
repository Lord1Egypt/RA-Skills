/**
 * Repository 层测试
 */

const assert = require('assert');
const { getPool } = require('../scripts/core/db.cjs');
const { ConceptRepository } = require('../src/repositories/ConceptRepository');
const { AssociationRepository } = require('../src/repositories/AssociationRepository');
const { MemoryRepository } = require('../src/repositories/MemoryRepository');
const { Concept } = require('../src/domain/Concept');
const { Association } = require('../src/domain/Association');
const { Memory } = require('../src/domain/Memory');

async function runTests() {
  console.log('🧪 Running Repository Tests...\n');

  const pool = getPool();
  if (!pool) {
    console.log('⚠️  Database not available, skipping tests');
    return;
  }

  let passed = 0;
  let failed = 0;

  // ConceptRepository Tests
  try {
    console.log('Testing ConceptRepository...');
    const conceptRepo = new ConceptRepository(pool);

    // Test create
    const concept = new Concept({ name: 'TestConcept_' + Date.now() });
    const saved = await conceptRepo.create(concept);
    assert(saved.id, 'Concept should have id after save');
    assert.strictEqual(saved.name, concept.name, 'Name should match');
    console.log('  ✓ create');
    passed++;

    // Test findByName
    const found = await conceptRepo.findByName(concept.name);
    assert(found, 'Should find concept by name');
    assert.strictEqual(found.name, concept.name, 'Found name should match');
    console.log('  ✓ findByName');
    passed++;

    // Test createMany (batch)
    const names = ['Batch1', 'Batch2', 'Batch3'].map(n => n + '_' + Date.now());
    const batchSaved = await conceptRepo.createMany(names);
    assert.strictEqual(batchSaved.length, 3, 'Should create 3 concepts');
    console.log('  ✓ createMany (batch insert)');
    passed++;

    // Test findTop
    const top = await conceptRepo.findTop(5);
    assert(Array.isArray(top), 'findTop should return array');
    console.log('  ✓ findTop');
    passed++;

  } catch (err) {
    console.error('  ✗ ConceptRepository:', err.message);
    failed++;
  }

  // AssociationRepository Tests
  try {
    console.log('\nTesting AssociationRepository...');
    const conceptRepo = new ConceptRepository(pool);
    const assocRepo = new AssociationRepository(pool);

    // Create two concepts first
    const c1 = await conceptRepo.create(new Concept({ name: 'AssocTest1_' + Date.now() }));
    const c2 = await conceptRepo.create(new Concept({ name: 'AssocTest2_' + Date.now() }));

    // Test create
    const assoc = new Association({
      fromId: c1.id,
      toId: c2.id,
      type: 'related',
      weight: 0.5
    });
    const savedAssoc = await assocRepo.create(assoc);
    assert(savedAssoc.id, 'Association should have id');
    console.log('  ✓ create');
    passed++;

    // Test findByConcept
    const found = await assocRepo.findByConcept(c1.id);
    assert(Array.isArray(found), 'findByConcept should return array');
    assert(found.length > 0, 'Should find at least one association');
    console.log('  ✓ findByConcept');
    passed++;

    // Test createMany (batch)
    const c3 = await conceptRepo.create(new Concept({ name: 'BatchAssoc3_' + Date.now() }));
    const assocs = [
      new Association({ fromId: c1.id, toId: c3.id, type: 'related', weight: 0.3 }),
      new Association({ fromId: c2.id, toId: c3.id, type: 'related', weight: 0.4 })
    ];
    const batchAssocs = await assocRepo.createMany(assocs);
    assert.strictEqual(batchAssocs.length, 2, 'Should create 2 associations');
    console.log('  ✓ createMany (batch insert)');
    passed++;

  } catch (err) {
    console.error('  ✗ AssociationRepository:', err.message);
    failed++;
  }

  console.log(`\n📊 Results: ${passed} passed, ${failed} failed`);
  process.exit(failed > 0 ? 1 : 0);
}

runTests().catch(err => {
  console.error('Test suite error:', err);
  process.exit(1);
});
