/**
 * 数据库连接测试
 */
const { describe, test, beforeAll, afterAll, expect, runTests } = require('./setup.cjs');
const { getPool, closeAll } = require('../scripts/core/db.cjs');

describe('Database Connection', () => {
  test('should get pool instance', () => {
    const pool = getPool();
    expect(pool).toBeDefined();
  });
  
  test('should return same pool (singleton)', () => {
    const pool1 = getPool();
    const pool2 = getPool();
    expect(pool1).toEqual(pool2);
  });
  
  test('should query database', async () => {
    const pool = getPool();
    const result = await pool.query('SELECT 1 as test');
    expect(result.rows[0].test).toBe(1);
  });
});

describe('Core Tables', () => {
  test('should have episodes table', async () => {
    const pool = getPool();
    const result = await pool.query(`
      SELECT EXISTS (
        SELECT FROM information_schema.tables 
        WHERE table_name = 'episodes'
      ) as exists
    `);
    expect(result.rows[0].exists).toBe(true);
  });
  
  test('should have concepts table', async () => {
    const pool = getPool();
    const result = await pool.query(`
      SELECT EXISTS (
        SELECT FROM information_schema.tables 
        WHERE table_name = 'concepts'
      ) as exists
    `);
    expect(result.rows[0].exists).toBe(true);
  });
  
  test('should have associations table', async () => {
    const pool = getPool();
    const result = await pool.query(`
      SELECT EXISTS (
        SELECT FROM information_schema.tables 
        WHERE table_name = 'associations'
      ) as exists
    `);
    expect(result.rows[0].exists).toBe(true);
  });
});

afterAll(async () => {
  await closeAll();
});

runTests();

