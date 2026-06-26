#!/usr/bin/env node
/**
 * Channel 修复脚本
 * 
 * 问题：hook 在记录 channel 时可能存为 unknown
 * 解决：根据 message_id 格式自动推断 channel
 * 
 * 使用：node scripts/core/fix_channels.cjs
 */

const pg = require('pg');
const { Pool } = pg;

const pool = new Pool({
  host: process.env.PG_HOST || 'localhost',
  port: process.env.PG_PORT || 5432,
  database: process.env.PG_DB || 'cognitive_brain',
  user: process.env.PG_USER || 'postgres',
  password: process.env.PG_PASSWORD || ''
});

async function fixChannels() {
  console.log('🔧 开始修复 channel...\n');
  
  // 1. 修复 Feishu: message_id 以 om_ 开头
  const feishu = await pool.query(`
    UPDATE episodes 
    SET source_channel = 'feishu' 
    WHERE source_channel = 'unknown' 
    AND content LIKE '%message_id: om_%'
    RETURNING id
  `);
  console.log(`✅ Feishu: 修复 ${feishu.rowCount} 条`);
  
  // 2. 修复 QQ: [QQBot] 标记
  const qq = await pool.query(`
    UPDATE episodes 
    SET source_channel = 'qqbot' 
    WHERE source_channel = 'unknown' 
    AND content LIKE '%[QQBot]%'
    RETURNING id
  `);
  console.log(`✅ QQ: 修复 ${qq.rowCount} 条`);
  
  // 3. 修复 WebChat: 包含 webchat 标记
  const webchat = await pool.query(`
    UPDATE episodes 
    SET source_channel = 'webchat' 
    WHERE source_channel = 'unknown' 
    AND content LIKE '%webchat%'
    RETURNING id
  `);
  console.log(`✅ WebChat: 修复 ${webchat.rowCount} 条`);
  
  // 4. 查看最终分布
  const result = await pool.query(`
    SELECT source_channel, COUNT(*) as cnt 
    FROM episodes 
    GROUP BY source_channel 
    ORDER BY cnt DESC
  `);
  
  console.log('\n📊 Channel 分布:');
  result.rows.forEach(r => {
    const label = r.source_channel || '(null)';
    console.log(`   ${label.padEnd(10)}: ${r.cnt}`);
  });
  
  await pool.end();
  console.log('\n✨ 完成!');
}

fixChannels().catch(err => {
  console.error('❌ 错误:', err.message);
  process.exit(1);
});

