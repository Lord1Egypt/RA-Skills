#!/usr/bin/env node
/**
 * encode_reply.cjs - 编码 AI 回复到 Cognitive Brain
 * 用法: node encode_reply.cjs "回复内容" [channel]
 */

const path = require('path');

// 加载 Cognitive Brain
const HOME = process.env.HOME || '/root';
const SKILL_DIR = path.join(HOME, '.openclaw/workspace/skills/cognitive-brain');

async function main() {
  const content = process.argv[2];
  const channel = process.argv[3] || 'lightclawbot';
  
  if (!content || content.length < 5) {
    console.log('Usage: node encode_reply.cjs "reply content" [channel]');
    process.exit(1);
  }
  
  try {
    // 直接使用 PostgreSQL 插入，跳过 embedding
    const pg = require(path.join(SKILL_DIR, 'node_modules', 'pg'));
    const client = new pg.Client({
      host: process.env.PGHOST || 'localhost',
      port: process.env.PGPORT || 5432,
      database: process.env.PGDATABASE || 'cognitive_brain',
      user: process.env.PGUSER || 'postgres',
      password: process.env.PGPASSWORD || ''
    });
    
    await client.connect();
    
    const id = require('crypto').randomUUID();
    const now = new Date();
    
    await client.query(`
      INSERT INTO episodes (id, content, summary, type, importance, role, source_channel, created_at, layers)
      VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
    `, [
      id,
      content,
      content.substring(0, 100),
      'episodic',
      0.7,
      'assistant',
      channel,
      now,
      JSON.stringify(['episodic'])
    ]);
    
    await client.end();
    console.log(`✅ AI reply saved: ${id}`);
  } catch (e) {
    console.error('❌ Error:', e.message);
    process.exit(1);
  }
}

main();
