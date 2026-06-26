#!/usr/bin/env node
/**
 * 缓存管理器 v6.1
 * 
 * 核心功能:
 * 1. LRU 缓存 (最近最少使用淘汰)
 * 2. TTL 过期 (自动过期)
 * 3. 多级缓存 (内存 + 文件)
 * 4. 缓存统计 (命中率/大小)
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// ============ LRU 缓存类 ============

class LRUCache {
  constructor(options = {}) {
    this.maxSize = options.maxSize || 1000;
    this.ttl = options.ttl || 300000; // 5 分钟默认过期
    this.cache = new Map();
    this.stats = {
      hits: 0,
      misses: 0,
      sets: 0,
      deletes: 0,
      evictions: 0
    };
    
    // 定期清理过期项
    this.startCleanup();
  }

  /**
   * 获取缓存
   */
  get(key) {
    const item = this.cache.get(key);
    
    if (!item) {
      this.stats.misses++;
      return null;
    }
    
    // 检查是否过期
    if (this.ttl > 0 && Date.now() - item.timestamp > this.ttl) {
      this.cache.delete(key);
      this.stats.misses++;
      return null;
    }
    
    // 移到最近使用 (更新 timestamp)
    item.timestamp = Date.now();
    this.cache.delete(key);
    this.cache.set(key, item);
    
    this.stats.hits++;
    return item.value;
  }

  /**
   * 设置缓存
   */
  set(key, value, ttl = null) {
    // 如果缓存已满，删除最旧的
    if (this.cache.size >= this.maxSize) {
      const firstKey = this.cache.keys().next().value;
      this.cache.delete(firstKey);
      this.stats.evictions++;
    }
    
    this.cache.set(key, {
      value,
      timestamp: Date.now(),
      ttl: ttl || this.ttl
    });
    
    this.stats.sets++;
  }

  /**
   * 删除缓存
   */
  delete(key) {
    const deleted = this.cache.delete(key);
    if (deleted) {
      this.stats.deletes++;
    }
    return deleted;
  }

  /**
   * 清空缓存
   */
  clear() {
    this.cache.clear();
    this.stats = {
      hits: 0,
      misses: 0,
      sets: 0,
      deletes: 0,
      evictions: 0
    };
  }

  /**
   * 检查键是否存在
   */
  has(key) {
    const item = this.cache.get(key);
    if (!item) return false;
    
    if (this.ttl > 0 && Date.now() - item.timestamp > this.ttl) {
      this.cache.delete(key);
      return false;
    }
    
    return true;
  }

  /**
   * 获取缓存大小
   */
  size() {
    return this.cache.size;
  }

  /**
   * 获取统计信息
   */
  getStats() {
    const total = this.stats.hits + this.stats.misses;
    const hitRate = total > 0 ? (this.stats.hits / total * 100) : 0;
    
    return {
      ...this.stats,
      size: this.cache.size,
      maxSize: this.maxSize,
      hitRate: hitRate.toFixed(2) + '%'
    };
  }

  /**
   * 启动定期清理
   */
  startCleanup() {
    if (this.ttl > 0) {
      setInterval(() => {
        this.cleanup();
      }, Math.min(this.ttl / 2, 60000)); // 最多 1 分钟清理一次
    }
  }

  /**
   * 清理过期项
   */
  cleanup() {
    if (this.ttl <= 0) return;
    
    const now = Date.now();
    let cleaned = 0;
    
    for (const [key, item] of this.cache) {
      const ttl = item.ttl || this.ttl;
      if (now - item.timestamp > ttl) {
        this.cache.delete(key);
        cleaned++;
      }
    }
    
    if (cleaned > 0) {
      console.log(`🧹 清理了 ${cleaned} 个过期缓存项`);
    }
  }

  /**
   * 导出缓存
   */
  export() {
    const data = [];
    for (const [key, item] of this.cache) {
      data.push({ key, ...item });
    }
    return JSON.stringify(data, null, 2);
  }

  /**
   * 导入缓存
   */
  import(json) {
    const data = JSON.parse(json);
    for (const item of data) {
      this.cache.set(item.key, {
        value: item.value,
        timestamp: item.timestamp,
        ttl: item.ttl
      });
    }
  }
}

// ============ 多级缓存类 ============

class MultiLevelCache {
  constructor(options = {}) {
    this.l1 = new LRUCache({
      maxSize: options.l1MaxSize || 100,
      ttl: options.l1Ttl || 60000 // 1 分钟
    });
    
    this.l2 = new LRUCache({
      maxSize: options.l2MaxSize || 1000,
      ttl: options.l2Ttl || 300000 // 5 分钟
    });
    
    this.fileCache = options.fileCache || null;
    this.stats = {
      l1Hits: 0,
      l2Hits: 0,
      fileHits: 0,
      misses: 0
    };
  }

  /**
   * 获取缓存 (L1 → L2 → File)
   */
  get(key) {
    // L1 缓存
    const l1Value = this.l1.get(key);
    if (l1Value !== null) {
      this.stats.l1Hits++;
      return l1Value;
    }
    
    // L2 缓存
    const l2Value = this.l2.get(key);
    if (l2Value !== null) {
      this.stats.l2Hits++;
      // 提升到 L1
      this.l1.set(key, l2Value);
      return l2Value;
    }
    
    // 文件缓存
    if (this.fileCache) {
      const fileValue = this.getFromFile(key);
      if (fileValue !== null) {
        this.stats.fileHits++;
        // 提升到 L1 和 L2
        this.l1.set(key, fileValue);
        this.l2.set(key, fileValue);
        return fileValue;
      }
    }
    
    this.stats.misses++;
    return null;
  }

  /**
   * 设置缓存 (L1 + L2 + File)
   */
  set(key, value, options = {}) {
    const { persist = false } = options;
    
    // L1 和 L2 总是设置
    this.l1.set(key, value);
    this.l2.set(key, value);
    
    // 文件缓存可选
    if (persist && this.fileCache) {
      this.saveToFile(key, value);
    }
  }

  /**
   * 从文件获取
   */
  getFromFile(key) {
    if (!this.fileCache) return null;
    
    const file = path.join(this.fileCache, `${this.hash(key)}.json`);
    if (!fs.existsSync(file)) return null;
    
    try {
      const content = fs.readFileSync(file, 'utf-8');
      const data = JSON.parse(content);
      
      // 检查是否过期
      if (data.expires && Date.now() > data.expires) {
        fs.unlinkSync(file);
        return null;
      }
      
      return data.value;
    } catch (error) {
      return null;
    }
  }

  /**
   * 保存到文件
   */
  saveToFile(key, value, ttl = 3600000) { // 1 小时默认
    if (!this.fileCache) return;
    
    const file = path.join(this.fileCache, `${this.hash(key)}.json`);
    const data = {
      key,
      value,
      createdAt: Date.now(),
      expires: Date.now() + ttl
    };
    
    fs.writeFileSync(file, JSON.stringify(data, null, 2));
  }

  /**
   * 哈希函数
   */
  hash(key) {
    return crypto.createHash('md5').update(key).digest('hex');
  }

  /**
   * 获取统计信息
   */
  getStats() {
    const total = this.stats.l1Hits + this.stats.l2Hits + this.stats.fileHits + this.stats.misses;
    const hitRate = total > 0 ? ((this.stats.l1Hits + this.stats.l2Hits + this.stats.fileHits) / total * 100) : 0;
    
    return {
      ...this.stats,
      l1Size: this.l1.size(),
      l2Size: this.l2.size(),
      hitRate: hitRate.toFixed(2) + '%',
      l1Stats: this.l1.getStats(),
      l2Stats: this.l2.getStats()
    };
  }

  /**
   * 清空所有缓存
   */
  clear() {
    this.l1.clear();
    this.l2.clear();
    this.stats = {
      l1Hits: 0,
      l2Hits: 0,
      fileHits: 0,
      misses: 0
    };
  }
}

// ============ 缓存装饰器 ============

function cached(ttl = 300000, cacheKeyFn = null) {
  const cache = new LRUCache({ ttl });
  
  return function(target, name, descriptor) {
    const originalMethod = descriptor.value;
    
    descriptor.value = function(...args) {
      // 生成缓存键
      let key;
      if (cacheKeyFn) {
        key = cacheKeyFn.apply(this, args);
      } else {
        key = `${name}:${JSON.stringify(args)}`;
      }
      
      // 查缓存
      const cached = cache.get(key);
      if (cached !== null) {
        return cached;
      }
      
      // 执行原方法
      const result = originalMethod.apply(this, args);
      
      // 如果是 Promise，处理异步结果
      if (result instanceof Promise) {
        return result.then(value => {
          cache.set(key, value);
          return value;
        });
      }
      
      // 设置缓存
      cache.set(key, result);
      return result;
    };
    
    // 添加清除缓存的方法
    descriptor.value.clearCache = () => {
      cache.clear();
    };
    
    return descriptor;
  };
}

// ============ CLI 接口 ============

function printHelp() {
  console.log(`
缓存管理器 v6.1

用法：node cache-manager.js <命令> [选项]

命令:
  test                运行缓存测试
  stats               查看统计信息
  benchmark           性能基准测试

示例:
  node cache-manager.js test
  node cache-manager.js stats
  node cache-manager.js benchmark
`);
}

// ============ 主程序 ============

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  if (!command || command === '--help' || command === '-h') {
    printHelp();
    return;
  }

  switch (command) {
    case 'test':
      console.log('🧪 运行缓存测试...\n');
      
      const cache = new LRUCache({ maxSize: 100, ttl: 5000 });
      
      // 测试设置和获取
      cache.set('key1', 'value1');
      console.log(`✅ set/get: ${cache.get('key1') === 'value1' ? '通过' : '失败'}`);
      
      // 测试缓存命中
      cache.set('key2', 'value2');
      cache.get('key2');
      cache.get('key2');
      const stats = cache.getStats();
      console.log(`✅ 命中率：${stats.hitRate}`);
      
      // 测试过期
      const tempCache = new LRUCache({ ttl: 100 });
      tempCache.set('temp', 'value');
      await new Promise(r => setTimeout(r, 200));
      console.log(`✅ 过期：${tempCache.get('temp') === null ? '通过' : '失败'}`);
      
      console.log('\n📊 缓存统计:');
      console.log(JSON.stringify(cache.getStats(), null, 2));
      break;

    case 'stats':
      const statsCache = new LRUCache({ maxSize: 1000 });
      
      // 模拟一些操作
      for (let i = 0; i < 100; i++) {
        statsCache.set(`key${i}`, `value${i}`);
      }
      for (let i = 0; i < 50; i++) {
        statsCache.get(`key${i}`);
      }
      for (let i = 50; i < 100; i++) {
        statsCache.get(`key${i}`);
      }
      
      console.log('📊 缓存统计:');
      console.log(JSON.stringify(statsCache.getStats(), null, 2));
      break;

    case 'benchmark':
      console.log('⚡ 运行性能基准测试...\n');
      
      const benchCache = new LRUCache({ maxSize: 10000, ttl: 0 });
      
      // 写入性能
      const writeStart = Date.now();
      for (let i = 0; i < 10000; i++) {
        benchCache.set(`key${i}`, `value${i}`);
      }
      const writeTime = Date.now() - writeStart;
      console.log(`写入 10000 项：${writeTime}ms (${(10000/writeTime*1000).toFixed(0)} ops/s)`);
      
      // 读取性能
      const readStart = Date.now();
      for (let i = 0; i < 10000; i++) {
        benchCache.get(`key${i}`);
      }
      const readTime = Date.now() - readStart;
      console.log(`读取 10000 项：${readTime}ms (${(10000/readTime*1000).toFixed(0)} ops/s)`);
      
      // 命中率测试
      const hitCache = new LRUCache({ maxSize: 1000, ttl: 0 });
      for (let i = 0; i < 1000; i++) {
        hitCache.set(`key${i}`, `value${i}`);
      }
      
      let hits = 0;
      const hitStart = Date.now();
      for (let i = 0; i < 10000; i++) {
        const key = `key${Math.floor(Math.random() * 1000)}`;
        if (hitCache.get(key) !== null) hits++;
      }
      const hitTime = Date.now() - hitStart;
      console.log(`命中率测试：${(hits/10000*100).toFixed(2)}% (${hitTime}ms)`);
      
      console.log('\n📊 最终统计:');
      console.log(JSON.stringify(benchCache.getStats(), null, 2));
      break;

    default:
      console.log(`未知命令：${command}`);
      printHelp();
  }
}

// 导出 API
module.exports = { LRUCache, MultiLevelCache, cached };

// 运行 CLI
if (require.main === module) {
  main().catch(console.error);
}
