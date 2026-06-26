#!/usr/bin/env node
const { getPool } = require('../core/db.cjs');

async function checkSchema() {
  const pool = getPool();
  console.log('=== 当前表结构 ===\n');
  
  // 查看 episodes 表结构
  const columns = await pool.query(`
    SELECT column_name, data_type, is_nullable
    FROM information_schema.columns
    WHERE table_name = 'episodes'
    ORDER BY ordinal_position
  `);
  
  console.log('episodes 表结构:');
  columns.rows.forEach(col => {
    const nullable = col.is_nullable === 'YES' ? 'NULL' : 'NOT NULL';
    console.log(`  ${col.column_name.padEnd(20)} ${col.data_type.padEnd(15)} ${nullable}`);
  });
  
  // 查看索引
  const indexes = await pool.query(`
    SELECT indexname, indexdef 
    FROM pg_indexes 
    WHERE tablename = 'episodes'
  `);
  
  console.log('\n索引:');
  indexes.rows.forEach(idx => console.log(`  - ${idx.indexname}`));
  
  await pool.end();
}

checkSchema().catch(console.error);

