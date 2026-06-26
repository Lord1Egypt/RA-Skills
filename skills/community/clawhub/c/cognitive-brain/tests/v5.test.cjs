/**
 * v5.0 架构测试
 */
const { describe, test, expect, runTests } = require('../tests/setup.cjs');
const { CognitiveBrain } = require('../src/index.js');
const { getPool, closeAll } = require('../scripts/core/db.cjs');

describe('CognitiveBrain v5.0', () => {
  test('should create instance', async () => {
    const brain = new CognitiveBrain();
    expect(brain).toBeDefined();
    expect(brain.memory).toBeDefined();
    expect(brain.concept).toBeDefined();
    expect(brain.association).toBeDefined();
  });

  test('should encode memory', async () => {
    const brain = new CognitiveBrain();
    const memory = await brain.encode('Test content for v5', {
      type: 'test',
      sourceChannel: 'test'
    });
    
    expect(memory).toHaveProperty('id');
    expect(memory.content).toBe('Test content for v5');
    expect(memory.type).toBe('test');
  });

  test('should recall memory', async () => {
    const brain = new CognitiveBrain();
    const memories = await brain.recall('Test content for v5');
    expect(Array.isArray(memories)).toBe(true);
  });

  test('should get stats', async () => {
    const brain = new CognitiveBrain();
    const stats = await brain.stats();
    expect(stats).toHaveProperty('memory');
    expect(stats).toHaveProperty('concept');
  });
});

// Cleanup after all tests
setTimeout(async () => {
  const pool = getPool();
  await pool.query("DELETE FROM episodes WHERE type = 'test' OR source_channel = 'test'");
  await pool.query("DELETE FROM concepts WHERE name LIKE 'test-concept%'");
  await closeAll();
}, 100);

runTests();

