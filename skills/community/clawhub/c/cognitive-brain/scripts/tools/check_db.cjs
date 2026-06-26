#!/usr/bin/env node
const { getPool } = require('../core/db.cjs');

async function checkDB() {
  const pool = getPool();
  console.log('=== 数据库全面检查 ===\n');
  
  // 1. episodes 表统计
  console.log('1. episodes 表统计:');
  const episodes = await pool.query(`
    SELECT 
      COUNT(*) as total,
      COUNT(DISTINCT source_channel) as channels,
      COUNT(DISTINCT type) as types,
      MIN(created_at) as earliest,
      MAX(created_at) as latest
    FROM episodes
  `);
  console.log('  总记录:', episodes.rows[0].total);
  console.log('  渠道数:', episodes.rows[0].channels);
  console.log('  类型数:', episodes.rows[0].types);
  console.log('  时间范围:', episodes.rows[0].earliest?.toISOString()?.split('T')[0], '→', episodes.rows[0].latest?.toISOString()?.split('T')[0]);
  
  // 2. 按渠道统计
  console.log('\n2. 按渠道统计:');
  const byChannel = await pool.query(`
    SELECT source_channel, COUNT(*) as count 
    FROM episodes 
    GROUP BY source_channel
    ORDER BY count DESC
  `);
  byChannel.rows.forEach(row => {
    const name = row.source_channel || 'null';
    console.log(`  - ${name}: ${row.count}`);
  });
  
  // 3. 按类型统计
  console.log('\n3. 按类型统计:');
  const byType = await pool.query(`
    SELECT type, COUNT(*) as count 
    FROM episodes 
    GROUP BY type
    ORDER BY count DESC
  `);
  byType.rows.forEach(row => console.log(`  - ${row.type}: ${row.count}`));
  
  // 4. 内容完整性检查
  console.log('\n4. 内容完整性:');
  const emptyContent = await pool.query(`
    SELECT COUNT(*) as count FROM episodes 
    WHERE content IS NULL OR content = ''
  `);
  console.log('  空内容记录:', emptyContent.rows[0].count);
  
  // 5. 检查最近24小时
  console.log('\n5. 最近24小时:');
  const recent = await pool.query(`
    SELECT COUNT(*) as count FROM episodes 
    WHERE created_at > NOW() - INTERVAL '24 hours'
  `);
  console.log('  新增:', recent.rows[0].count);
  
  // 6. 概念统计
  console.log('\n6. 概念统计:');
  const concepts = await pool.query(`
    SELECT COUNT(*) as total FROM concepts
  `);
  console.log('  总概念:', concepts.rows[0].total);
  
  // 7. 关联统计
  const assoc = await pool.query(`
    SELECT COUNT(*) as total FROM associations
  `);
  console.log('  关联数:', assoc.rows[0].total);
  
  await pool.end();
  console.log('\n✅ 检查完成');
}

checkDB().catch(err => {
  console.error('❌ 检查失败:', err.message);
  process.exit(1);
});

