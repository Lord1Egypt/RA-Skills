#!/usr/bin/env node
/**
 * 分布式缓存后端 v1.0
 * 
 * 核心职责：提供 Redis 和本地文件两种缓存后端
 * 
 * 第一性原理：
 * - 单机缓存有上限 → 分布式缓存可扩展
 * - Redis 不可用时有备选方案 → 本地文件缓存
 * - 统一接口 → 后端可插拔
 * 
 * 架构：
 * ┌─────────────────────────────────────────┐
 * │           CacheBackend (抽象层)          │
 * ├─────────────────────────────────────────┤
 * │  RedisBackend    │    FileBackend        │
 * │  (分布式)        │    (本地备选)         │
 * └─────────────────────────────────────────┘
 */

const fs = require('fs');
const path = require('path');

// ============ 抽象缓存后端 ============

class CacheBackend {
  constructor(options = {}) {
    this.options = options;
  }
  
  async get(key) { throw new Error('Not implemented'); }
  async set(key, value, ttl) { throw new Error('Not implemented'); }
  async delete(key) { throw new Error('Not implemented'); }
  async exists(key) { throw new Error('Not implemented'); }
  async cleanup() { throw new Error('Not implemented'); }
  async getStats() { throw new Error('Not implemented'); }
}

// ============ Redis 后端 ============

class RedisBackend extends CacheBackend {
  constructor(options = {}) {
    super(options);
    
    this.host = options.host || 'localhost';
    this.port = options.port || 6379;
    this.password = options.password || null;
    this.db = options.db || 0;
    this.keyPrefix = options.keyPrefix || 'openclaw:cache:';
    
    this.client = null;
    this.connected = false;
    this.stats = { hits: 0, misses: 0, writes: 0, errors: 0 };
    
    // 尝试连接
    this.connect();
  }
  
  /**
   * 连接 Redis
   */
  async connect() {
    try {
      // 动态加载 Redis 客户端
      const Redis = require('ioredis');
      
      this.client = new Redis({
        host: this.host,
        port: this.port,
        password: this.password,
        db: this.db,
        retryStrategy: (times) => {
          if (times > 3) {
            console.warn('[RedisBackend] 连接失败，使用本地缓存');
            return null; // 停止重试
          }
          return Math.min(times * 100, 3000);
        }
      });
      
      this.client.on('connect', () => {
        this.connected = true;
        console.log(`[RedisBackend] 已连接: ${this.host}:${this.port}`);
      });
      
      this.client.on('error', (err) => {
        console.error('[RedisBackend] 错误:', err.message);
        this.connected = false;
        this.stats.errors++;
      });
      
      this.client.on('close', () => {
        this.connected = false;
        console.log('[RedisBackend] 连接关闭');
      });
      
    } catch (e) {
      console.warn('[RedisBackend] ioredis 未安装，使用本地缓存');
      this.connected = false;
    }
  }
  
  /**
   * 获取缓存
   */
  async get(key) {
    if (!this.connected || !this.client) {
      this.stats.misses++;
      return null;
    }
    
    try {
      const fullKey = this.keyPrefix + key;
      const data = await this.client.get(fullKey);
      
      if (data) {
        this.stats.hits++;
        return JSON.parse(data);
      }
      
      this.stats.misses++;
      return null;
    } catch (e) {
      console.error('[RedisBackend] 获取失败:', e.message);
      this.stats.errors++;
      return null;
    }
  }
  
  /**
   * 设置缓存
   */
  async set(key, value, ttl = 3600) {
    if (!this.connected || !this.client) {
      return false;
    }
    
    try {
      const fullKey = this.keyPrefix + key;
      const data = JSON.stringify(value);
      
      if (ttl > 0) {
        await this.client.setex(fullKey, ttl, data);
      } else {
        await this.client.set(fullKey, data);
      }
      
      this.stats.writes++;
      return true;
    } catch (e) {
      console.error('[RedisBackend] 设置失败:', e.message);
      this.stats.errors++;
      return false;
    }
  }
  
  /**
   * 删除缓存
   */
  async delete(key) {
    if (!this.connected || !this.client) {
      return false;
    }
    
    try {
      const fullKey = this.keyPrefix + key;
      await this.client.del(fullKey);
      return true;
    } catch (e) {
      console.error('[RedisBackend] 删除失败:', e.message);
      return false;
    }
  }
  
  /**
   * 检查是否存在
   */
  async exists(key) {
    if (!this.connected || !this.client) {
      return false;
    }
    
    try {
      const fullKey = this.keyPrefix + key;
      const result = await this.client.exists(fullKey);
      return result === 1;
    } catch (e) {
      return false;
    }
  }
  
  /**
   * 清理过期缓存（Redis 自动处理）
   */
  async cleanup() {
    // Redis 自动过期，无需手动清理
    return { cleaned: 0 };
  }
  
  /**
   * 获取统计
   */
  async getStats() {
    const total = this.stats.hits + this.stats.misses;
    const hitRate = total > 0 ? (this.stats.hits / total * 100).toFixed(1) : 0;
    
    return {
      type: 'redis',
      connected: this.connected,
      host: this.host,
      port: this.port,
      ...this.stats,
      hitRate: hitRate + '%'
    };
  }
}

// ============ 本地文件后端 ============

class FileBackend extends CacheBackend {
  constructor(options = {}) {
    super(options);
    
    this.cacheDir = options.cacheDir || '/home/ubutu/.openclaw/workspace/data/cache/file-backend';
    this.maxSize = options.maxSize || 100 * 1024 * 1024; // 100MB
    this.memoryCache = new Map();
    this.maxMemorySize = options.maxMemorySize || 100;
    
    this.stats = { hits: 0, misses: 0, writes: 0, errors: 0 };
    
    this.ensureDir();
  }
  
  /**
   * 确保目录存在
   */
  ensureDir() {
    if (!fs.existsSync(this.cacheDir)) {
      fs.mkdirSync(this.cacheDir, { recursive: true });
    }
  }
  
  /**
   * 获取缓存
   */
  async get(key) {
    // 1. 检查内存缓存
    if (this.memoryCache.has(key)) {
      const cached = this.memoryCache.get(key);
      if (this.isValid(cached)) {
        this.stats.hits++;
        return cached.value;
      }
      this.memoryCache.delete(key);
    }
    
    // 2. 检查文件缓存
    const filePath = this.getFilePath(key);
    if (fs.existsSync(filePath)) {
      try {
        const data = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
        if (this.isValid(data)) {
          // 提升到内存
          this.promoteToMemory(key, data);
          this.stats.hits++;
          return data.value;
        }
        // 过期，删除
        fs.unlinkSync(filePath);
      } catch (e) {
        this.stats.errors++;
      }
    }
    
    this.stats.misses++;
    return null;
  }
  
  /**
   * 设置缓存
   */
  async set(key, value, ttl = 3600) {
    const data = {
      value,
      timestamp: Date.now(),
      expiresAt: Date.now() + (ttl * 1000),
      ttl
    };
    
    // 1. 写入内存
    this.promoteToMemory(key, data);
    
    // 2. 写入文件
    const filePath = this.getFilePath(key);
    try {
      fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
      this.stats.writes++;
      return true;
    } catch (e) {
      console.error('[FileBackend] 写入失败:', e.message);
      this.stats.errors++;
      return false;
    }
  }
  
  /**
   * 删除缓存
   */
  async delete(key) {
    // 删除内存
    this.memoryCache.delete(key);
    
    // 删除文件
    const filePath = this.getFilePath(key);
    if (fs.existsSync(filePath)) {
      try {
        fs.unlinkSync(filePath);
        return true;
      } catch {
        return false;
      }
    }
    return true;
  }
  
  /**
   * 检查是否存在
   */
  async exists(key) {
    const data = await this.get(key);
    return data !== null;
  }
  
  /**
   * 清理过期缓存
   */
  async cleanup() {
    let cleaned = 0;
    
    // 清理内存
    for (const [key, data] of this.memoryCache) {
      if (!this.isValid(data)) {
        this.memoryCache.delete(key);
        cleaned++;
      }
    }
    
    // 清理文件
    if (fs.existsSync(this.cacheDir)) {
      const files = fs.readdirSync(this.cacheDir).filter(f => f.endsWith('.json'));
      for (const file of files) {
        try {
          const filePath = path.join(this.cacheDir, file);
          const data = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
          if (!this.isValid(data)) {
            fs.unlinkSync(filePath);
            cleaned++;
          }
        } catch {
          // 损坏的文件，删除
          fs.unlinkSync(path.join(this.cacheDir, file));
          cleaned++;
        }
      }
    }
    
    if (cleaned > 0) {
      console.log(`[FileBackend] 清理过期缓存: ${cleaned} 个`);
    }
    
    return { cleaned };
  }
  
  /**
   * 获取统计
   */
  async getStats() {
    const total = this.stats.hits + this.stats.misses;
    const hitRate = total > 0 ? (this.stats.hits / total * 100).toFixed(1) : 0;
    
    // 计算磁盘使用
    let diskSize = 0;
    let fileCount = 0;
    if (fs.existsSync(this.cacheDir)) {
      const files = fs.readdirSync(this.cacheDir).filter(f => f.endsWith('.json'));
      fileCount = files.length;
      for (const file of files) {
        try {
          diskSize += fs.statSync(path.join(this.cacheDir, file)).size;
        } catch {}
      }
    }
    
    return {
      type: 'file',
      ...this.stats,
      hitRate: hitRate + '%',
      memoryCacheSize: this.memoryCache.size,
      diskCacheCount: fileCount,
      diskCacheSize: (diskSize / 1024 / 1024).toFixed(2) + ' MB'
    };
  }
  
  // ============ 私有方法 ============
  
  getFilePath(key) {
    return path.join(this.cacheDir, `${key}.json`);
  }
  
  isValid(data) {
    if (!data || !data.expiresAt) return false;
    return Date.now() < data.expiresAt;
  }
  
  promoteToMemory(key, data) {
    // LRU 淘汰
    if (this.memoryCache.size >= this.maxMemorySize) {
      const firstKey = this.memoryCache.keys().next().value;
      this.memoryCache.delete(firstKey);
    }
    this.memoryCache.set(key, data);
  }
}

// ============ 智能后端选择 ============

class SmartCacheBackend extends CacheBackend {
  constructor(options = {}) {
    super(options);
    
    // 尝试 Redis，失败则使用 File
    this.redisBackend = new RedisBackend(options.redis || {});
    this.fileBackend = new FileBackend(options.file || {});
    
    this.primary = null;
    this.fallback = null;
    
    // 等待 Redis 连接状态确定
    setTimeout(() => {
      if (this.redisBackend.connected) {
        this.primary = this.redisBackend;
        this.fallback = this.fileBackend;
        console.log('[SmartCacheBackend] 使用 Redis 后端');
      } else {
        this.primary = this.fileBackend;
        this.fallback = null;
        console.log('[SmartCacheBackend] 使用文件后端');
      }
    }, 1000);
    
    // 默认使用文件后端
    this.primary = this.fileBackend;
  }
  
  async get(key) {
    return this.primary.get(key);
  }
  
  async set(key, value, ttl) {
    return this.primary.set(key, value, ttl);
  }
  
  async delete(key) {
    return this.primary.delete(key);
  }
  
  async exists(key) {
    return this.primary.exists(key);
  }
  
  async cleanup() {
    return this.primary.cleanup();
  }
  
  async getStats() {
    const stats = await this.primary.getStats();
    return {
      ...stats,
      redisAvailable: this.redisBackend.connected
    };
  }
}

// 导出
module.exports = {
  CacheBackend,
  RedisBackend,
  FileBackend,
  SmartCacheBackend
};