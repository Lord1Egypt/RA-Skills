#!/usr/bin/env node
/**
 * recall.cjs - 召回记忆（优先应用层，fallback 数据库）
 * 用法: node recall.cjs "查询内容" [limit]
 */

const path = require('path');

const HOME = process.env.HOME || '/root';
const SKILL_DIR = path.join(HOME, '.openclaw/workspace/skills/cognitive-brain');

async function recallWithBrain(query, limit) {
  try {
    const { CognitiveBrain } = require(path.join(SKILL_DIR, 'src/index.js'));
    const brain = new CognitiveBrain();
    const memories = await brain.recall(query, { limit });
    if (brain.close) await brain.close();
    return memories || [];
  } catch (e) {
    console.error('[recall] Brain error:', e.message);
    return null;
  }
}

async function recallWithDB(query, limit) {
  try {
    const pg = require(path.join(SKILL_DIR, 'node_modules', 'pg'));
    const client = new pg.Client({
      host: process.env.PGHOST || 'localhost',
      port: process.env.PGPORT || 5432,
      database: process.env.PGDATABASE || 'cognitive_brain',
      user: process.env.PGUSER || 'postgres',
      password: process.env.PGPASSWORD || ''
    });
    
    await client.connect();
    
    const result = await client.query(`
      SELECT id, summary, role, type, created_at
      FROM episodes
      WHERE summary ILIKE $1 OR content ILIKE $1
      ORDER BY created_at DESC
      LIMIT $2
    `, [`%${query}%`, limit]);
    
    await client.end();
    
    return result.rows.map(r => ({
      summary: r.summary,
      role: r.role,
      createdAt: r.created_at
    }));
  } catch (e) {
    console.error('[recall] DB error:', e.message);
    return [];
  }
}

async function main() {
  const query = process.argv[2];
  const limit = parseInt(process.argv[3]) || 5;
  
  if (!query) {
    console.log('Usage: node recall.cjs "query" [limit]');
    process.exit(1);
  }
  
  // 优先尝试应用层（带 embedding）
  let memories = await recallWithBrain(query, limit);
  
  // 如果应用层失败，fallback 到数据库
  if (!memories) {
    console.error('[recall] Falling back to database...');
    memories = await recallWithDB(query, limit);
  }
  
  if (memories.length === 0) {
    console.log('[]');
    return;
  }
  
  const result = memories.map(m => ({
    summary: m.summary,
    role: m.role || 'unknown',
    time: m.createdAt ? new Date(m.createdAt).toISOString().replace('T', ' ').substring(0, 16) : 'unknown'
  }));
  
  console.log(JSON.stringify(result, null, 2));
}

main();
