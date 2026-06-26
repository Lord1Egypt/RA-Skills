/**
 * 统一数据库连接管理
 * 避免重复创建连接池
 */

const path = require('path');
const fs = require('fs');
const { createLogger } = require('../../src/utils/logger.cjs');

// 创建模块级 logger
const logger = createLogger('db');

// 确定技能目录
const SKILL_DIR = process.env.COGNITIVE_BRAIN_DIR || 
                  path.resolve(__dirname, '..', '..');
const CONFIG_PATH = path.join(SKILL_DIR, 'config.json');

// 缓存连接池
let pool = null;
let redisClient = null;

/**
 * 获取 PostgreSQL 连接池（单例）
 */
function getPool() {
  if (pool) return pool;
  
  try {
    // 使用绝对路径加载 pg（Hook 环境需要）
    const pg = require(path.join(SKILL_DIR, 'node_modules', 'pg'));
    const config = loadConfig();
    const dbConfig = config.storage?.primary || {
      host: 'localhost',
      port: 5432,
      database: 'cognitive_brain',
      user: 'postgres',
      password: process.env.PGPASSWORD || ''
    };
    
    pool = new pg.Pool({
      ...dbConfig,
      connectionTimeoutMillis: dbConfig.connectionTimeoutMillis || 5000,
      query_timeout: dbConfig.queryTimeout || 10000,
      max: dbConfig.poolSize || 10, // 最大连接数，可配置
      idleTimeoutMillis: dbConfig.idleTimeoutMillis || 30000,
      acquireTimeoutMillis: dbConfig.acquireTimeoutMillis || 5000
    });
    
    // 错误处理
    pool.on('error', (err) => {
      logger.error('连接池错误', { message: err.message });
    });
    
    return pool;
  } catch (err) {
    logger.error('初始化失败', { message: err.message });
    return null;
  }
}

/**
 * 获取 Redis 客户端（单例）
 */
async function getRedisClient() {
  if (redisClient) return redisClient;
  
  try {
    // 使用绝对路径加载 redis（Hook 环境需要）
    const redis = require(path.join(SKILL_DIR, 'node_modules', 'redis'));
    const config = loadConfig();
    const cacheConfig = config.storage?.cache || {
      host: 'localhost',
      port: 6379
    };
    
    const url = cacheConfig.url || `redis://${cacheConfig.host}:${cacheConfig.port}`;
    
    redisClient = redis.createClient({
      url,
      socket: {
        reconnectStrategy: (retries) => Math.min(retries * 100, 3000)
      }
    });
    
    redisClient.on('error', (err) => {
      logger.error('Redis错误', { message: err.message });
    });

    await redisClient.connect();
    return redisClient;
  } catch (err) {
    logger.error('Redis初始化失败', { message: err.message });
    return null;
  }
}

/**
 * 加载配置（带缓存）
 */
let configCache = null;
let configCacheTime = 0;
const CONFIG_CACHE_TTL = 5000; // 5秒缓存

function loadConfig() {
  const now = Date.now();
  if (configCache && (now - configCacheTime) < CONFIG_CACHE_TTL) {
    return configCache;
  }
  
  try {
    if (!fs.existsSync(CONFIG_PATH)) {
      return {};
    }
    configCache = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
    configCacheTime = now;
    return configCache;
  } catch (err) {
    console.error('[DB] 配置加载失败:', err.message);
    return {};
  }
}

/**
 * 关闭所有连接（清理资源）
 */
async function closeAll() {
  const promises = [];
  
  if (pool) {
    promises.push(pool.end().catch(() => {}));
    pool = null;
  }
  
  if (redisClient) {
    promises.push(redisClient.disconnect().catch(() => {}));
    redisClient = null;
  }
  
  await Promise.all(promises);
}

// 进程退出时清理
process.on('exit', closeAll);
process.on('SIGINT', () => {
  closeAll().then(() => process.exit(0)).catch(err => {
    console.error('[DB] 关闭连接失败:', err.message);
    process.exit(1);
  });
});

/**
 * 创建临时连接池（使用完需要手动关闭）
 * 适用于一次性操作，如批量导入
 */
function createTempPool() {
  try {
    const pg = require('pg');
    const config = loadConfig();
    const dbConfig = config.storage?.primary || {
      host: 'localhost',
      port: 5432,
      database: 'cognitive_brain',
      user: 'postgres',
      password: process.env.PGPASSWORD || ''
    };
    
    return new pg.Pool({
      ...dbConfig,
      connectionTimeoutMillis: 5000,
      query_timeout: 10000,
      max: 5 // 临时连接池较小
    });
  } catch (err) {
    console.error('[DB] 临时连接池创建失败:', err.message);
    return null;
  }
}

module.exports = {
  getPool,
  createTempPool,
  getRedisClient,
  loadConfig,
  closeAll,
  SKILL_DIR,
  CONFIG_PATH
};

