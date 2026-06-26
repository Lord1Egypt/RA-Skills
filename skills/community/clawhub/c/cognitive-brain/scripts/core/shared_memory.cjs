#!/usr/bin/env node
/**
 * Cognitive Brain - 共享工作区记忆模块 v5.0.0
 * 提供跨会话共享的记忆存储和实时同步
 * 
 * v5.0.0 更新:
 * - 兼容 v5.0 分层架构
 * - 优化错误处理
 * - 支持事务操作
 */

const fs = require('fs');
const path = require('path');
const { resolveModule } = require('../module_resolver.cjs');
const { createLogger } = require('../../src/utils/logger.cjs');
const logger = createLogger('shared_memory');

const HOME = process.env.HOME || '/root';
const SKILL_DIR = path.join(HOME, '.openclaw/workspace/skills/cognitive-brain');
const CONFIG_PATH = path.join(SKILL_DIR, 'config.json');

let config;
try {
  config = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
} catch (e) {
  console.error("[shared_memory] 无法加载配置:", e.message);
  config = { storage: { primary: {} } }; // 使用默认空配置，不退出进程
}

/**
 * 共享记忆客户端
 */
class SharedMemory {
  constructor() {
    this.pool = null;
    this.redis = null;
    this.listeners = new Map();
    this.isListening = false;
  }

  /**
   * 初始化数据库连接
   */
  async init() {
    const pg = resolveModule('pg');
    const { Pool } = pg;
    this.pool = new Pool(config.storage.primary);
    
    // 初始化 Redis（使用绝对路径）
    try {
      const redisPath = path.join(SKILL_DIR, 'node_modules', 'redis');
      const { createClient } = require(redisPath);
      this.redis = createClient({
        socket: {
          host: config.storage.cache?.host || 'localhost',
          port: config.storage.cache?.port || 6379
        }
      });
      await this.redis.connect();
      
      // 订阅变更通知
      this.subscriber = this.redis.duplicate();
      await this.subscriber.connect();
      
    } catch (e) { console.error("[shared_memory] 错误:", e.message);
      console.log('[SharedMemory] Redis 不可用，跳过实时同步');
    }
    
    return this;
  }

  /**
   * 获取系统记忆（替代读取 MEMORY.md）
   */
  async getSystemMemory(key, category = 'general') {
    const result = await this.pool.query(
      'SELECT * FROM system_memory WHERE key = $1 OR category = $2 ORDER BY updated_at DESC',
      [key, category]
    );
    return result.rows;
  }

  /**
   * 设置系统记忆（替代写入 MEMORY.md）
   */
  async setSystemMemory(key, content, category = 'general', importance = 0.5) {
    const result = await this.pool.query(
      `INSERT INTO system_memory (key, category, content, importance, version)
       VALUES ($1, $2, $3, $4, 1)
       ON CONFLICT (key) DO UPDATE SET
         content = EXCLUDED.content,
         importance = EXCLUDED.importance,
         version = system_memory.version + 1,
         updated_at = NOW()
       RETURNING *`,
      [key, category, content, importance]
    );
    
    // 广播变更
    await this.broadcastChange('system_memory', key, content);
    
    return result.rows[0];
  }

  /**
   * 获取所有用户相关记忆
   */
  async getUserProfile() {
    return await this.getSystemMemory('user', 'profile');
  }

  /**
   * 更新用户档案
   */
  async updateUserProfile(content) {
    return await this.setSystemMemory('user_profile', content, 'profile', 0.9);
  }

  /**
   * 获取所有教训
   */
  async getLessons() {
    return await this.getSystemMemory(null, 'lesson');
  }

  /**
   * 添加教训
   */
  async addLesson(key, content, importance = 0.8) {
    return await this.setSystemMemory(`lesson_${key}`, content, 'lesson', importance);
  }

  /**
   * 设置共享上下文（会话间共享）
   */
  async setSharedContext(sessionId, contextType, content, ttl = 3600) {
    const expiresAt = new Date(Date.now() + ttl * 1000);
    
    const result = await this.pool.query(
      `INSERT INTO shared_context (session_id, context_type, content, ttl, expires_at)
       VALUES ($1, $2, $3, $4, $5)
       ON CONFLICT (session_id, context_type) DO UPDATE SET
         content = EXCLUDED.content,
         ttl = EXCLUDED.ttl,
         expires_at = EXCLUDED.expires_at
       RETURNING *`,
      [sessionId, contextType, JSON.stringify(content), ttl, expiresAt]
    );
    
    // 也存入 Redis 加速读取
    if (this.redis) {
      const cacheKey = `shared:${sessionId}:${contextType}`;
      await this.redis.setEx(cacheKey, ttl, JSON.stringify(content));
    }
    
    return result.rows[0];
  }

  /**
   * 获取共享上下文
   */
  async getSharedContext(sessionId, contextType) {
    // 先尝试 Redis
    if (this.redis) {
      const cacheKey = `shared:${sessionId}:${contextType}`;
      const cached = await this.redis.get(cacheKey);
      if (cached) {
        try {
          return JSON.parse(cached);
        } catch (e) {
          logger.warn('Redis 缓存解析失败', { error: e.message, cacheKey });
          // 删除损坏的缓存
          await this.redis.del(cacheKey);
        }
      }
    }
    
    // 从数据库读取
    const result = await this.pool.query(
      'SELECT * FROM shared_context WHERE session_id = $1 AND context_type = $2 AND expires_at > NOW()',
      [sessionId, contextType]
    );
    
    if (result.rows.length > 0) {
      return result.rows[0].content;
    }
    
    return null;
  }

  /**
   * 广播变更到所有会话
   */
  async broadcastChange(table, key, data) {
    if (this.redis) {
      await this.redis.publish('memory:change', JSON.stringify({
        table,
        key,
        data,
        timestamp: Date.now()
      }));
    }
  }

  /**
   * 监听变更
   */
  onChange(callback) {
    if (!this.subscriber) {
      console.log('[SharedMemory] Redis 不可用，无法监听变更');
      return;
    }
    
    this.subscriber.subscribe('memory:change', (message) => {
      try {
        const data = JSON.parse(message);
        callback(data);
      } catch (e) { console.error("[shared_memory] 错误:", e.message);
        console.error('[SharedMemory] 解析变更消息失败:', e);
      }
    });
  }

  /**
   * 获取所有活跃会话
   */
  async getActiveSessions() {
    const result = await this.pool.query(
      'SELECT DISTINCT session_id FROM shared_context WHERE expires_at > NOW()'
    );
    return result.rows.map(r => r.session_id);
  }

  /**
   * 清理过期数据
   */
  async cleanup() {
    await this.pool.query('DELETE FROM shared_context WHERE expires_at < NOW()');
    await this.pool.query('DELETE FROM memory_changes WHERE changed_at < NOW() - INTERVAL \'7 days\'');
  }

  /**
   * 关闭连接
   */
  async close() {
    if (this.pool) {
      await this.pool.end();
    }
    if (this.redis) {
      await this.redis.quit();
    }
    if (this.subscriber) {
      await this.subscriber.quit();
    }
  }
}

// 单例模式
let sharedMemoryInstance = null;

async function getSharedMemory() {
  if (!sharedMemoryInstance) {
    sharedMemoryInstance = new SharedMemory();
    await sharedMemoryInstance.init();
  }
  return sharedMemoryInstance;
}

// CLI 接口
async function main() {
  const args = process.argv.slice(2);
  const action = args[0];
  
  const sm = await getSharedMemory();
  
  switch (action) {
    case 'get':
      const key = args[1];
      const data = await sm.getSystemMemory(key);
      console.log(JSON.stringify(data, null, 2));
      break;
      
    case 'set':
      const setKey = args[1];
      const content = args[2];
      const category = args[3] || 'general';
      const result = await sm.setSystemMemory(setKey, content, category);
      console.log('✅ 已设置:', result.key);
      break;
      
    case 'user':
      const user = await sm.getUserProfile();
      console.log(JSON.stringify(user, null, 2));
      break;
      
    case 'lessons':
      const lessons = await sm.getLessons();
      console.log(JSON.stringify(lessons, null, 2));
      break;
      
    case 'cleanup':
      await sm.cleanup();
      console.log('✅ 清理完成');
      break;
      
    default:
      console.log(`
共享工作区记忆模块 v5.0.0

用法:
  node shared_memory.cjs get <key>           # 获取系统记忆
  node shared_memory.cjs set <key> <content> [category]  # 设置系统记忆
  node shared_memory.cjs user                # 获取用户档案
  node shared_memory.cjs lessons             # 获取所有教训
  node shared_memory.cjs cleanup             # 清理过期数据
      `);
  }
  
  await sm.close();
}

if (require.main === module) {
  main();
}

module.exports = { SharedMemory, getSharedMemory };

