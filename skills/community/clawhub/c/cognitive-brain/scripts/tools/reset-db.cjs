#!/usr/bin/env node
/**
 * Cognitive Brain - 数据库重置脚本
 * 清空所有数据但保留表结构
 */

const fs = require('fs');
const path = require('path');

const SKILL_DIR = path.join(__dirname, "..", "..");
const CONFIG_PATH = path.join(SKILL_DIR, 'config.json');

const args = process.argv.slice(2);
const force = args.includes('--force');

async function resetDatabase() {
  console.log('\n🔄 Cognitive Brain 数据库重置\n');
  console.log('='.repeat(50));
  
  // 加载配置
  if (!fs.existsSync(CONFIG_PATH)) {
    console.error('❌ 配置文件不存在，请先运行 npm run setup');
    process.exit(1);
  }
  
  const config = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
  
  // 确认
  if (!force && process.stdin.isTTY) {
    const rl = require('readline').createInterface({
      input: process.stdin,
      output: process.stdout
    });
    
    console.log('\n⚠️  这将清空所有记忆数据！\n');
    const answer = await new Promise(resolve => {
      rl.question('确认重置? [y/N]: ', resolve);
    });
    rl.close();
    
    if (answer.toLowerCase() !== 'y') {
      console.log('已取消');
      process.exit(0);
    }
  }
  
  try {
    const { Pool } = require('pg');
    const pool = new Pool(config.storage.primary);
    
    console.log('\n📦 连接数据库...');
    await pool.query('SELECT 1');
    console.log('✅ 连接成功\n');
    
    // 清空表数据
    const tables = ['episodes', 'associations', 'concepts', 'reflections',
                    'user_profiles', 'self_awareness', 'subagent_logs'];
    
    console.log('🗑️  清空数据表...');
    for (const table of tables) {
      try {
        await pool.query(`TRUNCATE TABLE ${table} CASCADE`);
        console.log(`  ✅ ${table}`);
      } catch (e) {
        console.log(`  ⚠️  ${table}: ${e.message}`);
      }
    }
    
    // 清空 Redis
    console.log('\n🗑️  清空 Redis 缓存...');
    try {
      const { createClient } = require('redis');
      const redis = createClient({
        socket: {
          host: config.storage.cache.host,
          port: config.storage.cache.port
        }
      });
      
      await redis.connect();
      const keys = await redis.keys('brain:*');
      if (keys.length > 0) {
        await redis.del(keys);
        console.log(`  ✅ 删除 ${keys.length} 个缓存键`);
      } else {
        console.log('  ✅ 缓存为空');
      }
      await redis.quit();
    } catch (e) {
      console.log(`  ⚠️  Redis 清理失败: ${e.message}`);
    }
    
    await pool.end();
    
    console.log('\n' + '='.repeat(50));
    console.log('\n✨ 数据库已重置!\n');
    
  } catch (e) {
    console.error('\n❌ 重置失败:', e.message);
    process.exit(1);
  }
}

resetDatabase();
