#!/usr/bin/env node
/**
 * Cognitive Brain - Session Start Loader
 * 在会话开始时加载共享记忆
 */

const { createLogger } = require('../../src/utils/logger.cjs');
const logger = createLogger('session_start_loader');
const { getSharedMemory } = require('./shared_memory.cjs');

async function loadSessionContext() {
  console.log('🧠 Loading shared memory context...\n');
  
  try {
    const sm = await getSharedMemory();
    const context = [];
    
    // 1. 加载用户档案
    const profile = await sm.getUserProfile();
    if (profile && profile.length > 0) {
      const p = JSON.parse(profile[0].content);
      context.push(`[👤 User Profile] Name: ${p.name}, Contact: ${p.contact || 'unknown'}`);
    }
    
    // 2. 加载教训
    const lessons = await sm.getLessons();
    if (lessons.length > 0) {
      context.push(`[⚠️ Key Lessons] ${lessons.length} lessons learned:`);
      lessons.slice(0, 3).forEach((l, i) => {
        context.push(`  ${i + 1}. ${l.content.substring(0, 60)}...`);
      });
    }
    
    // 3. 加载最近的系统记忆
    const recent = await sm.pool.query(`
      SELECT key, content, category 
      FROM system_memory 
      WHERE category IN ('chat', 'conversation', 'milestone')
      ORDER BY created_at DESC 
      LIMIT 5
    `);
    
    if (recent.rows.length > 0) {
      context.push(`[💬 Recent Context] ${recent.rows.length} recent memories:`);
      recent.rows.forEach((r, i) => {
        context.push(`  ${i + 1}. [${r.category}] ${r.key}: ${r.content.substring(0, 40)}...`);
      });
    }
    
    await sm.close();
    
    if (context.length > 0) {
      console.log('=== Shared Memory Context ===');
      console.log(context.join('\n'));
      console.log('\n============================\n');
    } else {
      console.log('No shared memory found.\n');
    }
    
  } catch (err) {
    console.error('❌ Error loading shared memory:', err.message);
  }
}

if (require.main === module) {
  loadSessionContext();
}

module.exports = { loadSessionContext };

