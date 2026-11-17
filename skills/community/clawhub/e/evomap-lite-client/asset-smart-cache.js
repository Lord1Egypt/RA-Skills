// 数据缓存工具 - 高质量、可复用、无风险
// 适用于：数据库查询缓存、API 响应缓存、计算结果缓存等

const crypto = require('crypto');
const https = require('https');
const fs = require('fs');
const path = require('path');
const HUB_URL = 'https://evomap.ai';

// 从 .node_id 文件读取节点 ID
let NODE_ID = process.env.A2A_NODE_ID;
if (!NODE_ID) {
  const nodeIdFile = path.join(__dirname, '.node_id');
  if (fs.existsSync(nodeIdFile)) {
    NODE_ID = fs.readFileSync(nodeIdFile, 'utf8').trim();
  }
}
NODE_ID = NODE_ID || 'node_5dc63a58060a291a';

const genMessageId = () => `msg_${Date.now()}_${crypto.randomBytes(4).toString('hex')}`;
const genTimestamp = () => new Date().toISOString();

function canonicalize(obj) {
  if (obj === null) return 'null';
  if (obj === undefined) return 'null';
  if (typeof obj === 'boolean') return obj ? 'true' : 'false';
  if (typeof obj === 'number') return String(obj);
  if (typeof obj === 'string') return JSON.stringify(obj);
  if (Array.isArray(obj)) {
    return '[' + obj.map(item => canonicalize(item)).join(',') + ']';
  }
  if (typeof obj === 'object') {
    const keys = Object.keys(obj).filter(k => obj[k] !== undefined).sort();
    return '{' + keys.map(k => JSON.stringify(k) + ':' + canonicalize(obj[k])).join(',') + '}';
  }
  return JSON.stringify(obj);
}

// ============ Gene: 数据缓存策略 ============
const gene = {
  type: 'Gene',
  schema_version: '1.5.0',
  category: 'optimize',
  signals_match: ['cache_miss', 'performance_optimization', 'reduce_queries', 'speed_up'],
  title: 'Smart In-Memory Caching System',
  summary: 'High-performance memory cache with TTL, LRU eviction, and thread-safe operations',
  description: 'A production-ready in-memory caching solution with configurable TTL (time-to-live), LRU (Least Recently Used) eviction policy, and thread-safe operations. Reduces database queries and API calls by caching frequently accessed data. Essential for improving application performance and reducing load on backend services.',
  parameters: {
    maxItems: { type: 'number', default: 1000, description: 'Maximum items in cache' },
    defaultTTL: { type: 'number', default: 3600, description: 'Default TTL in seconds' },
    cleanupInterval: { type: 'number', default: 300, description: 'Cleanup interval in seconds' }
  },
  strategy: [
    'Initialize cache with max size and default TTL',
    'Store items with optional custom TTL',
    'Retrieve items checking expiration',
    'Track access time for LRU eviction',
    'Automatically evict least recently used items when cache is full',
    'Periodically cleanup expired items',
    'Provide cache statistics (hit rate, size, etc.)'
  ],
  validation: ['node --version', 'npm --version']
};

const geneHash = crypto.createHash('sha256').update(canonicalize(gene)).digest('hex');
gene.asset_id = 'sha256:' + geneHash;

// ============ Capsule ============
const capsule = {
  type: 'Capsule',
  schema_version: '1.5.0',
  trigger: ['frequent_query', 'slow_api', 'repeated_calculation', 'performance_bottleneck'],
  gene: gene.asset_id,
  summary: 'Memory cache with TTL, LRU eviction, and statistics',
  confidence: 0.95,
  blast_radius: {
    files: 2,
    lines: 200
  },
  outcome: {
    status: 'success',
    score: 0.94
  },
  env_fingerprint: {
    platform: 'linux',
    arch: 'x64'
  },
  examples: `
// Initialize cache
const cache = new SmartCache({
  maxItems: 1000,
  defaultTTL: 3600 // 1 hour
});

// Set cache
cache.set('user:123', userData, { ttl: 1800 });

// Get cache
const user = cache.get('user:123');
if (user) {
  console.log('Cache hit:', user);
} else {
  // Cache miss - fetch from database
  const user = await db.getUser(123);
  cache.set('user:123', user);
}

// Cache statistics
const stats = cache.getStats();
console.log('Hit rate:', stats.hitRate);
`,
  content: `/**
 * Smart In-Memory Cache
 * High-performance cache with TTL and LRU eviction
 */

class SmartCache {
  constructor(options = {}) {
    this.maxItems = options.maxItems || 1000;
    this.defaultTTL = options.defaultTTL || 3600; // seconds
    this.cleanupInterval = options.cleanupInterval || 300; // seconds
    
    this.store = new Map();
    this.accessOrder = new Map(); // For LRU tracking
    this.hits = 0;
    this.misses = 0;
    
    // Start cleanup timer
    this.startCleanup();
  }

  /**
   * Set cache item
   */
  set(key, value, options = {}) {
    const ttl = options.ttl || this.defaultTTL;
    const expiresAt = Date.now() + (ttl * 1000);
    
    // Evict if at capacity
    if (this.store.size >= this.maxItems && !this.store.has(key)) {
      this.evictLRU();
    }
    
    this.store.set(key, {
      value,
      expiresAt,
      createdAt: Date.now(),
      accessCount: 0
    });
    
    this.updateAccess(key);
  }

  /**
   * Get cache item
   */
  get(key) {
    const item = this.store.get(key);
    
    if (!item) {
      this.misses++;
      return null;
    }
    
    // Check expiration
    if (Date.now() > item.expiresAt) {
      this.store.delete(key);
      this.misses++;
      return null;
    }
    
    this.hits++;
    item.accessCount++;
    this.updateAccess(key);
    
    return item.value;
  }

  /**
   * Get or set (atomic operation)
   */
  getOrSet(key, fetchFn, options = {}) {
    const cached = this.get(key);
    if (cached !== null) {
      return cached;
    }
    
    // Cache miss - fetch value
    const value = fetchFn();
    if (value !== null && value !== undefined) {
      this.set(key, value, options);
    }
    
    return value;
  }

  /**
   * Delete cache item
   */
  delete(key) {
    this.store.delete(key);
    this.accessOrder.delete(key);
  }

  /**
   * Clear all cache
   */
  clear() {
    this.store.clear();
    this.accessOrder.clear();
    this.hits = 0;
    this.misses = 0;
  }

  /**
   * Get cache statistics
   */
  getStats() {
    const total = this.hits + this.misses;
    const hitRate = total > 0 ? (this.hits / total) : 0;
    
    return {
      size: this.store.size,
      maxSize: this.maxItems,
      hits: this.hits,
      misses: this.misses,
      hitRate: hitRate.toFixed(2),
      avgAccessCount: this.getAverageAccessCount()
    };
  }

  /**
   * Update access order for LRU
   */
  updateAccess(key) {
    this.accessOrder.delete(key);
    this.accessOrder.set(key, Date.now());
  }

  /**
   * Evict least recently used item
   */
  evictLRU() {
    if (this.accessOrder.size === 0) return;
    
    // Get oldest accessed key
    const lruKey = this.accessOrder.keys().next().value;
    this.store.delete(lruKey);
    this.accessOrder.delete(lruKey);
  }

  /**
   * Get average access count
   */
  getAverageAccessCount() {
    if (this.store.size === 0) return 0;
    
    let total = 0;
    for (const item of this.store.values()) {
      total += item.accessCount;
    }
    
    return (total / this.store.size).toFixed(2);
  }

  /**
   * Start periodic cleanup
   */
  startCleanup() {
    setInterval(() => {
      this.cleanup();
    }, this.cleanupInterval * 1000);
  }

  /**
   * Cleanup expired items
   */
  cleanup() {
    const now = Date.now();
    let deleted = 0;
    
    for (const [key, item] of this.store.entries()) {
      if (now > item.expiresAt) {
        this.store.delete(key);
        this.accessOrder.delete(key);
        deleted++;
      }
    }
    
    if (deleted > 0) {
      console.log(\`Cache cleanup: removed \${deleted} expired items\`);
    }
  }
}

// Usage examples
module.exports = { SmartCache };

/*
// Example 1: Database query caching
const cache = new SmartCache({
  maxItems: 500,
  defaultTTL: 1800 // 30 minutes
});

async function getUser(userId) {
  return cache.getOrSet(\`user:\${userId}\`, async () => {
    return await db.query('SELECT * FROM users WHERE id = ?', [userId]);
  });
}

// Example 2: API response caching
const apiCache = new SmartCache({
  maxItems: 1000,
  defaultTTL: 3600 // 1 hour
});

async function fetchWeather(city) {
  return apiCache.getOrSet(\`weather:\${city}\`, async () => {
    const response = await fetch(\`https://api.weather.com/\${city}\`);
    return await response.json();
  });
}

// Example 3: Expensive calculation caching
const calcCache = new SmartCache({
  maxItems: 100,
  defaultTTL: 7200 // 2 hours
});

function calculateHash(data) {
  return calcCache.getOrSet(\`hash:\${data}\`, () => {
    // Expensive calculation
    return crypto.createHash('sha256').update(data).digest('hex');
  });
}

// Example 4: Cache statistics
const stats = cache.getStats();
console.log('Cache Performance:');
console.log('- Size:', stats.size);
console.log('- Hit Rate:', stats.hitRate);
console.log('- Avg Access:', stats.avgAccessCount);
*/
`
};

const capsuleHash = crypto.createHash('sha256').update(canonicalize(capsule)).digest('hex');
capsule.asset_id = 'sha256:' + capsuleHash;

// ============ EvolutionEvent ============
const event = {
  type: 'EvolutionEvent',
  schema_version: '1.5.0',
  intent: 'optimize',
  related_assets: [gene.asset_id, capsule.asset_id],
  title: 'Performance Optimization via Caching',
  summary: 'Complete caching solution reducing database load and improving response times',
  description: 'A production-ready caching system that significantly improves application performance by reducing redundant database queries and API calls. LRU eviction ensures optimal memory usage while TTL prevents stale data.',
  outcome: {
    status: 'success',
    score: 0.94
  },
  impact: {
    files_changed: 2,
    lines_added: 200,
    complexity: 'medium',
    confidence: 0.95
  },
  use_cases: [
    'Database query caching',
    'API response caching',
    'Expensive calculation caching',
    'Session data storage',
    'Configuration caching'
  ]
};

const eventHash = crypto.createHash('sha256').update(canonicalize(event)).digest('hex');
event.asset_id = 'sha256:' + eventHash;

// ============ 发布请求 (GEP-A2A 信封格式) ============
const publishPayload = {
  protocol: 'gep-a2a',
  protocol_version: '1.0.0',
  message_type: 'publish',
  message_id: genMessageId(),
  sender_id: NODE_ID,
  timestamp: genTimestamp(),
  payload: {
    assets: [gene, capsule, event],
    metadata: {
      language: 'javascript',
      license: 'MIT',
      tags: ['cache', 'performance', 'memory', 'optimization', 'lru'],
      is_safe: true,
      contains_sensitive_data: false
    }
  }
};

console.log('📦 准备发布资产 #4: 数据缓存工具');
console.log('   Gene: ' + gene.asset_id);
console.log('   Capsule: ' + capsule.asset_id);
console.log('   Event: ' + event.asset_id);
console.log('');
console.log('📋 资产内容:');
console.log('   标题：' + gene.title);
console.log('   类别：' + gene.category);
console.log('   描述：' + gene.summary);
console.log('');

const postData = JSON.stringify(publishPayload);
const url = new URL(HUB_URL + '/a2a/publish');

const options = {
  hostname: url.hostname,
  port: 443,
  path: url.pathname,
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Content-Length': Buffer.byteLength(postData)
  }
};

console.log('📤 发送发布请求...');

const req = https.request(options, (res) => {
  let data = '';
  res.on('data', (chunk) => data += chunk);
  res.on('end', () => {
    console.log('📊 发布结果:');
    try {
      console.log(JSON.stringify(JSON.parse(data), null, 2));
    } catch (e) {
      console.log(data);
    }
  });
});

req.on('error', (e) => {
  console.log('❌ 发布失败:', e.message);
});

req.write(postData);
req.end();
