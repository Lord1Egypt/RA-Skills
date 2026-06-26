/**
 * 性能优化器
 * 
 * 层级：Layer 10 - Efficiency Layer
 * 功能：视频生成性能优化、缓存管理、批处理优化
 * 版本：V1.0.0
 * 状态：🟡 开发中
 */

import { VideoGenerationRequest, VideoGenerationResponse } from './comfyui-workflow-orchestrator';

// ============== 类型定义 ==============

/**
 * 性能指标
 */
export interface PerformanceMetrics {
  /** 平均响应时间 (ms) */
  avgResponseTimeMs: number;
  /** P95 响应时间 (ms) */
  p95ResponseTimeMs: number;
  /** P99 响应时间 (ms) */
  p99ResponseTimeMs: number;
  /** 成功率 */
  successRate: number;
  /** 每秒请求数 */
  requestsPerSecond: number;
  /** 缓存命中率 */
  cacheHitRate: number;
  /** 批处理效率提升 */
  batchEfficiencyGain: number;
}

/**
 * 缓存条目
 */
export interface CacheEntry<T> {
  /** 缓存键 */
  key: string;
  /** 缓存值 */
  value: T;
  /** 创建时间 */
  createdAt: number;
  /** 过期时间 */
  expiresAt: number;
  /** 访问次数 */
  accessCount: number;
}

/**
 * 优化配置
 */
export interface OptimizerConfig {
  /** 启用缓存 */
  enableCache: boolean;
  /** 缓存 TTL (秒) */
  cacheTTLSeconds: number;
  /** 最大缓存条目 */
  maxCacheEntries: number;
  /** 启用批处理 */
  enableBatching: boolean;
  /** 批处理窗口 (ms) */
  batchWindowMs: number;
  /** 最大批处理大小 */
  maxBatchSize: number;
  /** 启用预取 */
  enablePrefetch: boolean;
  /** 预取提前量 (秒) */
  prefetchAheadSeconds: number;
}

/**
 * 批处理请求
 */
export interface BatchRequest {
  /** 请求 ID 列表 */
  requestIds: string[];
  /** 请求列表 */
  requests: VideoGenerationRequest[];
  /** 批处理创建时间 */
  createdAt: number;
  /** 批处理状态 */
  status: 'pending' | 'processing' | 'completed';
}

// ============== 默认配置 ==============

const DEFAULT_OPTIMIZER_CONFIG: OptimizerConfig = {
  enableCache: true,
  cacheTTLSeconds: 3600, // 1 小时
  maxCacheEntries: 1000,
  enableBatching: true,
  batchWindowMs: 100, // 100ms 窗口
  maxBatchSize: 10,
  enablePrefetch: false,
  prefetchAheadSeconds: 30,
};

// ============== 工具函数 ==============

/**
 * 生成缓存键
 */
function generateCacheKey(request: VideoGenerationRequest): string {
  return `cache_${Buffer.from(
    JSON.stringify({
      prompt: request.prompt,
      duration: request.durationSeconds,
      resolution: request.resolution,
      aspectRatio: request.aspectRatio,
    })
  ).toString('base64')}`;
}

// ============== 核心类 ==============

/**
 * 性能优化器
 */
export class PerformanceOptimizer {
  private config: OptimizerConfig;
  private cache: Map<string, CacheEntry<VideoGenerationResponse>>;
  private batchQueue: BatchRequest | null = null;
  private metrics: {
    responseTimes: number[];
    totalRequests: number;
    cacheHits: number;
    batchRequests: number;
  };

  constructor(config: Partial<OptimizerConfig> = {}) {
    this.config = { ...DEFAULT_OPTIMIZER_CONFIG, ...config };
    this.cache = new Map();
    this.metrics = {
      responseTimes: [],
      totalRequests: 0,
      cacheHits: 0,
      batchRequests: 0,
    };
  }

  /**
   * 检查缓存
   */
  checkCache(request: VideoGenerationRequest): VideoGenerationResponse | null {
    if (!this.config.enableCache) {
      return null;
    }

    const key = generateCacheKey(request);
    const entry = this.cache.get(key);

    if (entry && Date.now() < entry.expiresAt) {
      entry.accessCount++;
      this.metrics.cacheHits++;
      console.log(`[Performance Optimizer] 📦 Cache hit: ${key}`);
      return entry.value;
    }

    // 清理过期条目
    if (entry && Date.now() >= entry.expiresAt) {
      this.cache.delete(key);
    }

    return null;
  }

  /**
   * 写入缓存
   */
  setCache(request: VideoGenerationRequest, response: VideoGenerationResponse): void {
    if (!this.config.enableCache) {
      return;
    }

    const key = generateCacheKey(request);
    const now = Date.now();

    // 检查缓存大小
    if (this.cache.size >= this.config.maxCacheEntries) {
      this.evictCache();
    }

    this.cache.set(key, {
      key,
      value: response,
      createdAt: now,
      expiresAt: now + this.config.cacheTTLSeconds * 1000,
      accessCount: 1,
    });
  }

  /**
   * 添加到批处理队列
   */
  addToBatch(request: VideoGenerationRequest, requestId: string): void {
    if (!this.config.enableBatching) {
      return;
    }

    if (!this.batchQueue) {
      this.batchQueue = {
        requestIds: [],
        requests: [],
        createdAt: Date.now(),
        status: 'pending',
      };

      // 设置批处理定时器
      setTimeout(() => this.flushBatch(), this.config.batchWindowMs);
    }

    this.batchQueue.requestIds.push(requestId);
    this.batchQueue.requests.push(request);

    // 检查是否达到最大批处理大小
    if (this.batchQueue.requests.length >= this.config.maxBatchSize) {
      this.flushBatch();
    }
  }

  /**
   * 刷新批处理队列
   */
  private flushBatch(): void {
    if (!this.batchQueue || this.batchQueue.requests.length === 0) {
      return;
    }

    this.batchQueue.status = 'processing';
    this.metrics.batchRequests++;

    console.log(
      `[Performance Optimizer] 📦 Flushing batch: ${this.batchQueue.requests.length} requests`
    );

    // 实际应调用批处理 API
    // 这里仅做模拟

    this.batchQueue = null;
  }

  /**
   * 记录响应时间
   */
  recordResponseTime(responseTimeMs: number): void {
    this.metrics.responseTimes.push(responseTimeMs);
    this.metrics.totalRequests++;

    // 保持最近 1000 个样本
    if (this.metrics.responseTimes.length > 1000) {
      this.metrics.responseTimes.shift();
    }
  }

  /**
   * 获取性能指标
   */
  getMetrics(): PerformanceMetrics {
    const times = this.metrics.responseTimes.sort((a, b) => a - b);
    const total = times.length;

    const avg = total > 0 ? times.reduce((a, b) => a + b, 0) / total : 0;
    const p95 = total > 0 ? times[Math.floor(total * 0.95)] || 0 : 0;
    const p99 = total > 0 ? times[Math.floor(total * 0.99)] || 0 : 0;

    const successRate =
      this.metrics.totalRequests > 0
        ? (this.metrics.totalRequests - this.metrics.batchRequests) /
          this.metrics.totalRequests
        : 0;

    const cacheHitRate =
      this.metrics.totalRequests > 0
        ? this.metrics.cacheHits / this.metrics.totalRequests
        : 0;

    const batchEfficiencyGain =
      this.metrics.batchRequests > 0
        ? (this.metrics.batchRequests * 0.3) / this.metrics.totalRequests // 假设批处理节省 30%
        : 0;

    return {
      avgResponseTimeMs: Math.round(avg),
      p95ResponseTimeMs: Math.round(p95),
      p99ResponseTimeMs: Math.round(p99),
      successRate: Math.round(successRate * 100) / 100,
      requestsPerSecond: this.metrics.totalRequests / (total > 0 ? total / 1000 : 1),
      cacheHitRate: Math.round(cacheHitRate * 100) / 100,
      batchEfficiencyGain: Math.round(batchEfficiencyGain * 100) / 100,
    };
  }

  /**
   * 清理缓存
   */
  clearCache(): void {
    this.cache.clear();
    console.log('[Performance Optimizer] 🗑️ Cache cleared');
  }

  /**
   * 获取缓存统计
   */
  getCacheStats(): {
    size: number;
    maxSize: number;
    hitRate: number;
  } {
    return {
      size: this.cache.size,
      maxSize: this.config.maxCacheEntries,
      hitRate:
        this.metrics.totalRequests > 0
          ? this.metrics.cacheHits / this.metrics.totalRequests
          : 0,
    };
  }

  /**
   * 预取数据
   */
  prefetch(requests: VideoGenerationRequest[]): void {
    if (!this.config.enablePrefetch) {
      return;
    }

    console.log(`[Performance Optimizer] 🔮 Prefetching ${requests.length} requests`);

    // 实际应调用预取 API
    // 这里仅做模拟
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
      console.log(`[Performance Optimizer] 🗑️ Evicted cache entry: ${minKey}`);
    }
  }
}

// ============== 导出 ==============

export default PerformanceOptimizer;
