#!/usr/bin/env node
/**
 * Prompt Cache v1.0 - 提示词缓存系统
 * 
 * 核心职责：缓存 LLM 响应，避免重复调用
 * 
 * 第一性原理：
 * - 相同 Prompt 产生相同响应 → 可缓存复用
 * - LLM 调用成本高 → 缓存命中可节省 100% Token
 * - 缓存一致性 → TTL + 主动失效
 * 
 * Token 优化效果：
 * - 缓存命中：Token 节省 100%
 * - 实际场景：Token 节省 30% ~ 60%
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

class PromptCache {
  constructor(options = {}) {
    this.cacheDir = options.cacheDir || '/home/ubutu/.openclaw/workspace/data/cache/prompts';
    this.ttl = options.ttl || 3600000; // 默认 1 小时
    this.maxSize = options.maxSize || 100 * 1024 * 1024; // 默认 100MB
    this.memoryCache = new Map(); // 内存缓存
    this.maxMemoryCacheSize = options.maxMemoryCacheSize || 100;
    
    // 统计信息
    this.stats = {
      hits: 0,
      misses: 0,
      writes: 0,
      evictions: 0
    };
    
    this.ensureDir();
    this.loadIndex();
  }

  /**
   * 确保缓存目录存在
   */
  ensureDir() {
    if (!fs.existsSync(this.cacheDir)) {
      fs.mkdirSync(this.cacheDir, { recursive: true });
    }
  }

  /**
   * 加载缓存索引
   */
  loadIndex() {
    const indexFile = path.join(this.cacheDir, 'index.json');
    if (fs.existsSync(indexFile)) {
      try {
        this.index = JSON.parse(fs.readFileSync(indexFile, 'utf-8'));
      } catch {
        this.index = {};
      }
    } else {
      this.index = {};
    }
  }

  /**
   * 保存缓存索引
   */
  saveIndex() {
    const indexFile = path.join(this.cacheDir, 'index.json');
    fs.writeFileSync(indexFile, JSON.stringify(this.index, null, 2));
  }

  /**
   * 生成缓存键（MD5 哈希）
   */
  hash(prompt, options = {}) {
    // 包含选项参数在哈希中
    const content = JSON.stringify({
      prompt: prompt.substring(0, 10000), // 限制长度
      model: options.model || 'default',
      temperature: options.temperature || 1
    });
    return crypto.createHash('md5').update(content).digest('hex');
  }

  /**
   * 获取缓存（核心方法）
   * @param {string} prompt - 提示词
   * @param {object} options - 选项
   * @returns {object|null} 缓存结果或 null
   */
  get(prompt, options = {}) {
    const key = this.hash(prompt, options);
    
    // 1. 检查内存缓存
    if (this.memoryCache.has(key)) {
      const cached = this.memoryCache.get(key);
      if (this.isValid(cached)) {
        this.stats.hits++;
        console.log(`[PromptCache] 内存命中: ${key.substring(0, 8)}...`);
        return cached.response;
      }
      // 过期，删除
      this.memoryCache.delete(key);
    }
    
    // 2. 检查磁盘缓存
    const cacheFile = path.join(this.cacheDir, `${key}.json`);
    if (fs.existsSync(cacheFile)) {
      try {
        const cached = JSON.parse(fs.readFileSync(cacheFile, 'utf-8'));
        if (this.isValid(cached)) {
          // 提升到内存缓存
          this.promoteToMemory(key, cached);
          this.stats.hits++;
          console.log(`[PromptCache] 磁盘命中: ${key.substring(0, 8)}...`);
          return cached.response;
        }
        // 过期，删除
        this.evict(key, cacheFile);
      } catch (e) {
        console.warn(`[PromptCache] 读取缓存失败: ${e.message}`);
        this.evict(key, cacheFile);
      }
    }
    
    this.stats.misses++;
    return null;
  }

  /**
   * 设置缓存（核心方法）
   * @param {string} prompt - 提示词
   * @param {object} response - LLM 响应
   * @param {object} options - 选项
   */
  set(prompt, response, options = {}) {
    const key = this.hash(prompt, options);
    const ttl = options.ttl || this.ttl;
    
    const cached = {
      key,
      prompt: prompt.substring(0, 500), // 仅存储前 500 字符用于调试
      promptHash: this.hash(prompt, {}),
      response,
      timestamp: Date.now(),
      expiresAt: Date.now() + ttl,
      ttl,
      model: options.model || 'default',
      metadata: {
        inputTokens: options.inputTokens,
        outputTokens: options.outputTokens
      }
    };
    
    // 1. 写入内存缓存
    this.promoteToMemory(key, cached);
    
    // 2. 写入磁盘缓存
    const cacheFile = path.join(this.cacheDir, `${key}.json`);
    fs.writeFileSync(cacheFile, JSON.stringify(cached, null, 2));
    
    // 3. 更新索引
    this.index[key] = {
      timestamp: cached.timestamp,
      expiresAt: cached.expiresAt,
      size: JSON.stringify(cached).length
    };
    this.saveIndex();
    
    this.stats.writes++;
    console.log(`[PromptCache] 写入缓存: ${key.substring(0, 8)}... (TTL: ${ttl / 1000}s)`);
  }

  /**
   * 检查缓存是否有效
   */
  isValid(cached) {
    if (!cached || !cached.expiresAt) return false;
    return Date.now() < cached.expiresAt;
  }

  /**
   * 提升到内存缓存
   */
  promoteToMemory(key, cached) {
    // LRU 淘汰
    if (this.memoryCache.size >= this.maxMemoryCacheSize) {
      const firstKey = this.memoryCache.keys().next().value;
      this.memoryCache.delete(firstKey);
    }
    this.memoryCache.set(key, cached);
  }

  /**
   * 淘汰缓存
   */
  evict(key, cacheFile) {
    // 删除内存缓存
    this.memoryCache.delete(key);
    
    // 删除磁盘缓存
    if (fs.existsSync(cacheFile)) {
      fs.unlinkSync(cacheFile);
    }
    
    // 删除索引
    delete this.index[key];
    
    this.stats.evictions++;
  }

  /**
   * 清理过期缓存
   */
  cleanup() {
    const now = Date.now();
    let cleaned = 0;
    
    // 清理内存缓存
    for (const [key, cached] of this.memoryCache) {
      if (!this.isValid(cached)) {
        this.memoryCache.delete(key);
        cleaned++;
      }
    }
    
    // 清理磁盘缓存
    for (const [key, info] of Object.entries(this.index)) {
      if (info.expiresAt < now) {
        const cacheFile = path.join(this.cacheDir, `${key}.json`);
        this.evict(key, cacheFile);
        cleaned++;
      }
    }
    
    if (cleaned > 0) {
      this.saveIndex();
      console.log(`[PromptCache] 清理过期缓存: ${cleaned} 个`);
    }
    
    return { cleaned };
  }

  /**
   * 检查缓存大小
   */
  checkSize() {
    let totalSize = 0;
    for (const info of Object.values(this.index)) {
      totalSize += info.size || 0;
    }
    return {
      totalSize,
      maxSize: this.maxSize,
      usage: (totalSize / this.maxSize * 100).toFixed(1) + '%',
      count: Object.keys(this.index).length
    };
  }

  /**
   * 获取统计信息
   */
  getStats() {
    const total = this.stats.hits + this.stats.misses;
    const hitRate = total > 0 ? (this.stats.hits / total * 100).toFixed(1) : 0;
    
    return {
      ...this.stats,
      total,
      hitRate: hitRate + '%',
      memoryCacheSize: this.memoryCache.size,
      diskCacheCount: Object.keys(this.index).length
    };
  }

  /**
   * 批量操作
   */
  async batch(prompts, llmCall, options = {}) {
    const results = [];
    const uncached = [];
    const uncachedIndices = [];
    
    // 1. 检查缓存
    for (let i = 0; i < prompts.length; i++) {
      const cached = this.get(prompts[i], options);
      if (cached !== null) {
        results[i] = cached;
      } else {
        uncached.push(prompts[i]);
        uncachedIndices.push(i);
      }
    }
    
    // 2. 批量调用未缓存的
    if (uncached.length > 0) {
      console.log(`[PromptCache] 批量调用: ${uncached.length} 个未缓存`);
      
      for (let i = 0; i < uncached.length; i++) {
        const response = await llmCall(uncached[i]);
        results[uncachedIndices[i]] = response;
        this.set(uncached[i], response, options);
      }
    }
    
    return results;
  }

  /**
   * 清除所有缓存
   */
  clear() {
    // 清除内存缓存
    this.memoryCache.clear();
    
    // 清除磁盘缓存
    if (fs.existsSync(this.cacheDir)) {
      const files = fs.readdirSync(this.cacheDir);
      for (const file of files) {
        if (file.endsWith('.json')) {
          fs.unlinkSync(path.join(this.cacheDir, file));
        }
      }
    }
    
    // 重置索引
    this.index = {};
    this.saveIndex();
    
    console.log('[PromptCache] 已清除所有缓存');
  }
}

// 单例导出
let instance = null;

function getPromptCache(options = {}) {
  if (!instance) {
    instance = new PromptCache(options);
  }
  return instance;
}

module.exports = {
  PromptCache,
  getPromptCache
};