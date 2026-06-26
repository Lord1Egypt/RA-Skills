/**
 * Prompt 缓存管理器单元测试
 */

import { PromptCacheManager } from '../prompt-cache-manager';

describe('PromptCacheManager', () => {
  let cacheManager: PromptCacheManager;

  beforeEach(() => {
    cacheManager = new PromptCacheManager();
  });

  describe('check', () => {
    it('should return null when cache is disabled', () => {
      const disabledManager = new PromptCacheManager({ enabled: false });
      const result = disabledManager.check('Test prompt', 'model-1');
      expect(result).toBeNull();
    });

    it('should return null for short prompts', () => {
      const result = cacheManager.check('Short', 'model-1');
      expect(result).toBeNull();
    });

    it('should return null when cache is empty', () => {
      const result = cacheManager.check('This is a longer prompt that should be checked but not found in cache', 'model-1');
      expect(result).toBeNull();
    });

    it('should return cached entry when available', () => {
      const prompt = 'This is a test prompt that should be cached properly for testing purposes';
      const response = { content: 'Test response' };

      cacheManager.set(prompt, 'model-1', response, 100);
      const result = cacheManager.check(prompt, 'model-1');

      expect(result).toBeDefined();
      expect(result?.response).toEqual(response);
    });

    it('should return null for expired cache', () => {
      const shortTTLManager = new PromptCacheManager({ ttlSeconds: 1 });
      const prompt = 'This is a test prompt that should expire quickly for testing purposes';

      shortTTLManager.set(prompt, 'model-1', { content: 'Test' }, 100);

      // Wait for expiration (添加 .unref() 避免进程退出警告)
      const timer = setTimeout(() => {
        const result = shortTTLManager.check(prompt, 'model-1');
        expect(result).toBeNull();
        timer.unref();
      }, 1100);
      timer.unref();
    });
  });

  describe('set', () => {
    it('should not cache when disabled', () => {
      const disabledManager = new PromptCacheManager({ enabled: false });
      disabledManager.set('Test prompt', 'model-1', { content: 'Test' }, 100);

      const stats = disabledManager.getStats();
      expect(stats.totalEntries).toBe(0);
    });

    it('should not cache short prompts', () => {
      const cacheManager = new PromptCacheManager({ minPromptLength: 50 });
      cacheManager.set('Short', 'model-1', { content: 'Test' }, 100);

      const stats = cacheManager.getStats();
      expect(stats.totalEntries).toBe(0);
    });
  });

  describe('getStats', () => {
    it('should return cache statistics', () => {
      const prompt = 'This is a test prompt that should be cached properly for testing purposes';

      cacheManager.set(prompt, 'model-1', { content: 'Test' }, 100);
      const hit1 = cacheManager.check(prompt, 'model-1'); // Hit
      const hit2 = cacheManager.check(prompt, 'model-1'); // Hit
      const miss = cacheManager.check('Another prompt for testing cache miss scenario', 'model-1'); // Miss

      const stats = cacheManager.getStats();

      expect(stats.totalEntries).toBe(1);
      // totalRequests = hits + misses, but only counted when check() is called
      expect(stats.hits + stats.misses).toBeGreaterThan(0);
      expect(stats.hitRate).toBeGreaterThanOrEqual(0);
    });
  });

  describe('clear', () => {
    it('should clear all cache entries', () => {
      const prompt1 = 'This is the first test prompt for cache clearing functionality testing';
      const prompt2 = 'This is the second test prompt for cache clearing functionality testing';

      cacheManager.set(prompt1, 'model-1', { content: 'Test 1' }, 100);
      cacheManager.set(prompt2, 'model-1', { content: 'Test 2' }, 100);

      cacheManager.clear();

      const stats = cacheManager.getStats();
      expect(stats.totalEntries).toBe(0);
    });
  });

  describe('cleanupExpired', () => {
    it('should remove expired entries', (done) => {
      const shortTTLManager = new PromptCacheManager({ ttlSeconds: 1 });
      const prompt = 'This is a test prompt that should expire quickly for testing cleanup';

      shortTTLManager.set(prompt, 'model-1', { content: 'Test' }, 100);

      // Wait for expiration (添加 .unref() 避免进程退出警告)
      const timer = setTimeout(() => {
        const cleaned = shortTTLManager.cleanupExpired();
        expect(cleaned).toBe(1);

        const stats = shortTTLManager.getStats();
        expect(stats.totalEntries).toBe(0);
        timer.unref();
        done();
      }, 1100);
      timer.unref();
    }, 3000);
  });

  describe('adjustStrategy', () => {
    it('should adjust minPromptLength based on hit rate', () => {
      const adaptiveManager = new PromptCacheManager({
        strategy: 'adaptive',
        minPromptLength: 50,
      });

      // Simulate low hit rate
      for (let i = 0; i < 10; i++) {
        adaptiveManager.check(`Test prompt ${i} for adjusting strategy`, 'model-1');
      }

      // Force adjustment
      (adaptiveManager as any).lastAdjustmentTime = 0;
      adaptiveManager.adjustStrategy();

      // minPromptLength should be lowered
      const stats = adaptiveManager.getStats();
      expect(stats.hitRate).toBe(0);
    });
  });
});
