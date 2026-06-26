/**
 * 缓存管理模块
 * Redis 缓存封装
 */

const { createLogger } = require('../../src/utils/logger.cjs');
const logger = createLogger('cache');
const configPath = require('path').join(__dirname, '..', '..', 'config.json');
let config;
try {
  config = JSON.parse(require('fs').readFileSync(configPath, 'utf8'));
} catch (e) {
  config = { storage: { cache: { host: 'localhost', port: 6379, db: 0 } } };
}

let redisClient = null;

/**
 * 初始化 Redis 连接
 * @returns {Promise<boolean>}
 */
async function initRedis() {
  if (redisClient) return true;

  try {
    const redis = require('redis');
    const { createClient } = redis;

    redisClient = createClient({
      socket: {
        host: config.storage.cache?.host || 'localhost',
        port: config.storage.cache?.port || 6379
      },
      database: config.storage.cache?.db || 0
    });

    await redisClient.connect();
    return true;
  } catch (e) {
    console.log('[cache] Redis 不可用，跳过缓存');
    return false;
  }
}

/**
 * 获取缓存
 * @param {string} key - 缓存键
 * @returns {Promise<any>}
 */
async function getCache(key) {
  if (!redisClient) return null;

  try {
    const cached = await redisClient.get(`brain:${key}`);
    if (cached) {
      return JSON.parse(cached);
    }
  } catch (e) {
    // ignore
  }
  return null;
}

/**
 * 设置缓存
 * @param {string} key - 缓存键
 * @param {any} value - 缓存值
 * @param {number} ttlSeconds - 过期时间（秒）
 */
async function setCache(key, value, ttlSeconds = 60) {
  if (!redisClient) return;

  try {
    await redisClient.setEx(`brain:${key}`, ttlSeconds, JSON.stringify(value));
  } catch (e) {
    // ignore
  }
}

/**
 * 删除缓存
 * @param {string} key - 缓存键
 */
async function delCache(key) {
  if (!redisClient) return;

  try {
    await redisClient.del(`brain:${key}`);
  } catch (e) {
    // ignore
  }
}

/**
 * 清理所有缓存
 */
async function clearCache() {
  if (!redisClient) return;

  try {
    await redisClient.flushDb();
  } catch (e) {
    // ignore
  }
}

/**
 * 关闭 Redis 连接
 */
async function closeRedis() {
  if (redisClient) {
    await redisClient.quit();
    redisClient = null;
  }
}

module.exports = {
  initRedis,
  getCache,
  setCache,
  delCache,
  clearCache,
  closeRedis
};
