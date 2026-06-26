/**
 * 性能优化器单元测试
 */

import { PerformanceOptimizer } from '../performance-optimizer';

describe('PerformanceOptimizer', () => {
  let optimizer: PerformanceOptimizer;

  beforeEach(() => {
    optimizer = new PerformanceOptimizer();
  });

  describe('checkCache', () => {
    it('should return null when cache is empty', () => {
      const request = { prompt: 'Test video' };
      const result = optimizer.checkCache(request);
      expect(result).toBeNull();
    });

    it('should return cached response when available', () => {
      const request = { prompt: 'Test video' };
      const mockResponse = { status: 'success' as const, videoPath: '/test.mp4' };

      optimizer.setCache(request, mockResponse);
      const result = optimizer.checkCache(request);

      expect(result).toEqual(mockResponse);
    });

    it('should return null for expired cache', () => {
      const request = { prompt: 'Test video' };
      const mockResponse = { status: 'success' as const, videoPath: '/test.mp4' };

      // 创建 TTL 为 1 秒的配置
      const shortTTL = new PerformanceOptimizer({ cacheTTLSeconds: 1 });
      shortTTL.setCache(request, mockResponse);

      // 等待过期（添加 .unref() 避免进程退出警告）
      const timer = setTimeout(() => {
        const result = shortTTL.checkCache(request);
        expect(result).toBeNull();
        timer.unref(); // 清理定时器
      }, 1100);
      timer.unref(); // 为父定时器也添加 .unref()
    });
  });

  describe('getMetrics', () => {
    it('should return performance metrics', () => {
      optimizer.recordResponseTime(100);
      optimizer.recordResponseTime(200);
      optimizer.recordResponseTime(150);

      const metrics = optimizer.getMetrics();

      expect(metrics.avgResponseTimeMs).toBeGreaterThan(0);
      expect(metrics.p95ResponseTimeMs).toBeGreaterThanOrEqual(metrics.avgResponseTimeMs);
      expect(metrics.p99ResponseTimeMs).toBeGreaterThanOrEqual(metrics.p95ResponseTimeMs);
    });

    it('should calculate cache hit rate', () => {
      const request = { prompt: 'Test' };
      const response = { status: 'success' as const, videoPath: '/test.mp4' };

      optimizer.setCache(request, response);
      optimizer.checkCache(request); // Hit
      optimizer.checkCache(request); // Hit
      optimizer.recordResponseTime(100);
      optimizer.recordResponseTime(100);
      optimizer.recordResponseTime(100);

      const metrics = optimizer.getMetrics();
      expect(metrics.cacheHitRate).toBeGreaterThan(0);
    });
  });

  describe('getCacheStats', () => {
    it('should return cache statistics', () => {
      const request1 = { prompt: 'Test 1' };
      const request2 = { prompt: 'Test 2' };
      const response = { status: 'success' as const, videoPath: '/test.mp4' };

      optimizer.setCache(request1, response);
      optimizer.setCache(request2, response);

      const stats = optimizer.getCacheStats();

      expect(stats.size).toBe(2);
      expect(stats.maxSize).toBe(1000);
    });
  });

  describe('clearCache', () => {
    it('should clear all cache entries', () => {
      const request = { prompt: 'Test' };
      const response = { status: 'success' as const, videoPath: '/test.mp4' };

      optimizer.setCache(request, response);
      optimizer.clearCache();

      const stats = optimizer.getCacheStats();
      expect(stats.size).toBe(0);
    });
  });
});
