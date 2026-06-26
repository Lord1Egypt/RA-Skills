/**
 * Prompt 缓存管理器
 * 
 * 层级：Layer 10 - Efficiency Layer
 * 功能：Prompt 缓存管理、缓存策略、成本优化
 * 版本：V1.0.0
 * 状态：🟡 开发中
 */

// ============== 类型定义 ==============

/**
 * 缓存条目
 */
export interface CacheEntry {
  /** 缓存键 (prompt hash) */
  key: string;
  /** 原始 prompt */
  prompt: string;
  /** 缓存响应 */
  response: any;
  /** 创建时间 */
  createdAt: number;
  /** 过期时间 */
  expiresAt: number;
  /** 访问次数 */
  accessCount: number;
  /** 缓存命中次数 */
  hitCount: number;
  /** 模型 ID */
  modelId: string;
  /** Token 数 */
  tokenCount: number;
}

/**
 * 缓存配置
 */
export interface PromptCacheConfig {
  /** 启用缓存 */
  enabled: boolean;
  /** 缓存策略 */
  strategy: 'aggressive' | 'conservative' | 'adaptive';
  /** 缓存 TTL (秒) */
  ttlSeconds: number;
  /** 最大缓存条目 */
  maxEntries: number;
  /** 缓存读取成本 */
  cacheReadCost: number;
  /** 缓存写入成本 */
  cacheWriteCost: number;
  /** 最小缓存 prompt 长度 */
  minPromptLength: number;
  /** 缓存前缀 (用于分类) */
  cachePrefix?: string;
}

/**
 * 缓存统计
 */
export interface CacheStats {
  /** 总条目数 */
  totalEntries: number;
  /** 总请求数 */
  totalRequests: number;
  /** 命中次数 */
  hits: number;
  /** 未命中次数 */
  misses: number;
  /** 命中率 */
  hitRate: number;
  /** 节省 Token 数 */
  tokensSaved: number;
  /** 节省成本 */
  costSaved: number;
  /** 平均响应时间减少 (ms) */
  avgLatencyReductionMs: number;
}

/**
 * 缓存策略配置
 */
export interface CacheStrategyConfig {
  /** Aggressive: 缓存所有 prompt */
  aggressive: {
    minPromptLength: number;
    ttlSeconds: number;
  };
  /** Conservative: 只缓存长 prompt */
  conservative: {
    minPromptLength: number;
    ttlSeconds: number;
  };
  /** Adaptive: 根据命中率动态调整 */
  adaptive: {
    minPromptLength: number;
    ttlSeconds: number;
    targetHitRate: number;
    adjustmentIntervalMs: number;
  };
}

// ============== 默认配置 ==============

const DEFAULT_CACHE_CONFIG: PromptCacheConfig = {
  enabled: true,
  strategy: 'adaptive',
  ttlSeconds: 3600, // 1 小时
  maxEntries: 1000,
  cacheReadCost: 0.0001, // $0.0001 per read
  cacheWriteCost: 0.001, // $0.001 per write
  minPromptLength: 50, // 至少 50 字符才缓存
};

const DEFAULT_STRATEGY_CONFIG: CacheStrategyConfig = {
  aggressive: {
    minPromptLength: 20,
    ttlSeconds: 1800,
  },
  conservative: {
    minPromptLength: 200,
    ttlSeconds: 7200,
  },
  adaptive: {
    minPromptLength: 50,
    ttlSeconds: 3600,
    targetHitRate: 0.7,
    adjustmentIntervalMs: 300000, // 5 分钟
  },
};

// ============== 工具函数 ==============

/**
 * 生成 prompt hash
 */
function generatePromptHash(prompt: string, modelId: string): string {
  const data = `${modelId}:${prompt}`;
  let hash = 0;
  for (let i = 0; i < data.length; i++) {
    hash = ((hash << 5) - hash) + data.charCodeAt(i);
    hash = hash & hash;
  }
  return `cache_${Math.abs(hash).toString(36)}`;
}

// ============== 核心类 ==============

/**
 * Prompt 缓存管理器
 */
export class PromptCacheManager {
  private config: PromptCacheConfig;
  private cache: Map<string, CacheEntry>;
  private stats: {
    totalRequests: number;
    hits: number;
    misses: number;
    tokensSaved: number;
    costSaved: number;
    latencySavedMs: number;
  };
  private lastAdjustmentTime: number = Date.now();

  constructor(config: Partial<PromptCacheConfig> = {}) {
    this.config = { ...DEFAULT_CACHE_CONFIG, ...config };
    this.cache = new Map();
    this.stats = {
      totalRequests: 0,
      hits: 0,
      misses: 0,
      tokensSaved: 0,
      costSaved: 0,
      latencySavedMs: 0,
    };
  }

  /**
   * 检查缓存
   */
  check(prompt: string, modelId: string): CacheEntry | null {
    if (!this.config.enabled) {
      return null;
    }

    // 检查 prompt 长度
    if (prompt.length < this.config.minPromptLength) {
      return null;
    }

    const key = generatePromptHash(prompt, modelId);
    const entry = this.cache.get(key);

    this.stats.totalRequests++;

    if (entry && Date.now() < entry.expiresAt) {
      entry.accessCount++;
      entry.hitCount++;
      this.stats.hits++;
      
      // 计算节省
      this.stats.tokensSaved += entry.tokenCount;
      this.stats.costSaved += entry.tokenCount * (this.config.cacheReadCost - this.config.cacheWriteCost);
      this.stats.latencySavedMs += 1500; // 假设缓存节省 1.5s

      console.log(`[Prompt Cache] 📦 Hit: ${key} (prompt: ${prompt.substring(0, 30)}...)`);
      return entry;
    }

    // 清理过期条目
    if (entry && Date.now() >= entry.expiresAt) {
      this.cache.delete(key);
    }

    this.stats.misses++;
    return null;
  }

  /**
   * 写入缓存
   */
  set(prompt: string, modelId: string, response: any, tokenCount: number): void {
    if (!this.config.enabled) {
      return;
    }

    // 检查 prompt 长度
    if (prompt.length < this.config.minPromptLength) {
      return;
    }

    // 检查缓存大小
    if (this.cache.size >= this.config.maxEntries) {
      this.evictCache();
    }

    const key = generatePromptHash(prompt, modelId);
    const now = Date.now();

    this.cache.set(key, {
      key,
      prompt,
      response,
      createdAt: now,
      expiresAt: now + this.config.ttlSeconds * 1000,
      accessCount: 1,
      hitCount: 0,
      modelId,
      tokenCount,
    });

    console.log(`[Prompt Cache] 💾 Write: ${key} (tokens: ${tokenCount})`);
  }

  /**
   * 获取缓存统计
   */
  getStats(): CacheStats {
    const hitRate = this.stats.totalRequests > 0
      ? this.stats.hits / this.stats.totalRequests
      : 0;

    return {
      totalEntries: this.cache.size,
      totalRequests: this.stats.totalRequests,
      hits: this.stats.hits,
      misses: this.stats.misses,
      hitRate: Math.round(hitRate * 100) / 100,
      tokensSaved: this.stats.tokensSaved,
      costSaved: Math.round(this.stats.costSaved * 100) / 100,
      avgLatencyReductionMs: this.stats.totalRequests > 0
        ? Math.round(this.stats.latencySavedMs / this.stats.totalRequests)
        : 0,
    };
  }

  /**
   * 清除缓存
   */
  clear(): void {
    this.cache.clear();
    console.log('[Prompt Cache] 🗑️ Cache cleared');
  }

  /**
   * 清除过期条目
   */
  cleanupExpired(): number {
    const now = Date.now();
    let cleaned = 0;

    this.cache.forEach((entry, key) => {
      if (now >= entry.expiresAt) {
        this.cache.delete(key);
        cleaned++;
      }
    });

    if (cleaned > 0) {
      console.log(`[Prompt Cache] 🧹 Cleaned ${cleaned} expired entries`);
    }

    return cleaned;
  }

  /**
   * 自适应调整策略
   */
  adjustStrategy(): void {
    if (this.config.strategy !== 'adaptive') {
      return;
    }

    const now = Date.now();
    if (now - this.lastAdjustmentTime < DEFAULT_STRATEGY_CONFIG.adaptive.adjustmentIntervalMs) {
      return;
    }

    const stats = this.getStats();
    const targetHitRate = DEFAULT_STRATEGY_CONFIG.adaptive.targetHitRate;

    // 如果命中率低于目标，降低 minPromptLength
    if (stats.hitRate < targetHitRate * 0.8) {
      this.config.minPromptLength = Math.max(20, this.config.minPromptLength - 10);
      console.log(`[Prompt Cache] 📉 Lowering minPromptLength to ${this.config.minPromptLength} (hit rate: ${stats.hitRate})`);
    }
    // 如果命中率高于目标，提高 minPromptLength 以节省内存
    else if (stats.hitRate > targetHitRate * 1.2) {
      this.config.minPromptLength = Math.min(200, this.config.minPromptLength + 10);
      console.log(`[Prompt Cache] 📈 Raising minPromptLength to ${this.config.minPromptLength} (hit rate: ${stats.hitRate})`);
    }

    this.lastAdjustmentTime = now;
  }

  /**
   * 导出缓存
   */
  exportCache(): CacheEntry[] {
    return Array.from(this.cache.values());
  }

  /**
   * 导入缓存
   */
  importCache(entries: CacheEntry[]): void {
    entries.forEach(entry => {
      if (Date.now() < entry.expiresAt) {
        this.cache.set(entry.key, entry);
      }
    });
    console.log(`[Prompt Cache] 📥 Imported ${entries.length} entries`);
  }

  // ============== 私有方法 ==============

  /**
   * 淘汰缓存 (LRU 策略)
   */
  private evictCache(): void {
    // 找到访问次数最少的条目
    let minAccess = Infinity;
    let minKey: string | null = null;

    this.cache.forEach((entry, key) => {
      if (entry.accessCount < minAccess) {
        minAccess = entry.accessCount;
        minKey = key;
      }
    });

    if (minKey) {
      this.cache.delete(minKey);
      console.log(`[Prompt Cache] 🗑️ Evicted: ${minKey}`);
    }
  }
}

// ============== 导出 ==============

export default PromptCacheManager;
