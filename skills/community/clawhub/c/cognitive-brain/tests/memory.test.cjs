/**
 * 记忆编码测试
 */
const { describe, test, afterAll, expect, runTests } = require('./setup.cjs');
const { getPool, closeAll } = require('../scripts/core/db.cjs');

describe('Memory Encoding', () => {
  const pool = getPool();
  let testMemoryId = null;
  
  test('should insert a memory', async () => {
    const result = await pool.query(`
      INSERT INTO episodes (content, summary, type, importance, source_channel, role)
      VALUES ($1, $2, $3, $4, $5, $6)
      RETURNING id
    `, ['Test content for encoding', 'Test summary', 'test', 0.5, 'test', 'user']);
    
    expect(result.rows[0]).toHaveProperty('id');
    testMemoryId = result.rows[0].id;
  });
  
  test('should retrieve the memory', async () => {
    const result = await pool.query(`
      SELECT * FROM episodes WHERE content = $1
    `, ['Test content for encoding']);
    
    expect(result.rows.length).toBeGreaterThan(0);
    expect(result.rows[0].type).toBe('test');
  });
  
  test('should update importance', async () => {
    await pool.query(`
      UPDATE episodes SET importance = $1 WHERE id = $2
    `, [0.9, testMemoryId]);
    
    const result = await pool.query(`
      SELECT importance FROM episodes WHERE id = $1
    `, [testMemoryId]);
    
    expect(result.rows[0].importance).toBe(0.9);
  });
  
  test('should delete test memory', async () => {
    await pool.query(`
      DELETE FROM episodes WHERE id = $1
    `, [testMemoryId]);
    
    const result = await pool.query(`
      SELECT * FROM episodes WHERE id = $1
    `, [testMemoryId]);
    
    expect(result.rows.length).toBe(0);
  });
});

describe('Concept Management', () => {
  const pool = getPool();
  
  test('should insert a concept', async () => {
    await pool.query(`
      INSERT INTO concepts (name, access_count)
      VALUES ($1, $2)
      ON CONFLICT (name) DO NOTHING
    `, ['test_concept', 1]);
    
    const result = await pool.query(`
      SELECT * FROM concepts WHERE name = $1
    `, ['test_concept']);
    
    expect(result.rows.length).toBeGreaterThan(0);
  });
  
  test('should update access count', async () => {
    await pool.query(`
      UPDATE concepts SET access_count = access_count + 1 WHERE name = $1
    `, ['test_concept']);
    
    const result = await pool.query(`
      SELECT access_count FROM concepts WHERE name = $1
    `, ['test_concept']);
    
    expect(result.rows[0].access_count).toBeGreaterThan(1);
  });
  
  test('should delete test concept', async () => {
    await pool.query(`
      DELETE FROM concepts WHERE name = $1
    `, ['test_concept']);
    
    const result = await pool.query(`
      SELECT * FROM concepts WHERE name = $1
    `, ['test_concept']);
    
    expect(result.rows.length).toBe(0);
  });
});

afterAll(async () => {
  const pool = getPool();
  // Cleanup test data
  await pool.query("DELETE FROM episodes WHERE type = 'test' OR source_channel = 'test'");
  await pool.query("DELETE FROM concepts WHERE name = 'test_concept'");
  await closeAll();
});

runTests();

