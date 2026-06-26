/**
 * Provider 路由管理器单元测试
 */

import { ProviderRouter } from '../provider-router';

describe('ProviderRouter', () => {
  let router: ProviderRouter;

  beforeEach(() => {
    router = new ProviderRouter();
  });

  describe('registerProvider', () => {
    it('should register a provider', () => {
      const provider = {
        id: 'test-provider',
        name: 'Test Provider',
        baseUrl: 'https://test.api.com',
        api: 'openai',
        priority: 1,
        weight: 10,
        timeoutMs: 30000,
        maxRetries: 3,
        enabled: true,
        healthCheck: {
          enabled: true,
          intervalMs: 60000,
          timeoutMs: 5000,
        },
      };

      router.registerProvider(provider);

      const stats = router.getStats();
      expect(stats.totalProviders).toBe(1);
    });
  });

  describe('selectProvider', () => {
    beforeEach(() => {
      router.registerProvider({
        id: 'provider-1',
        name: 'Provider 1',
        baseUrl: 'https://p1.api.com',
        api: 'openai',
        priority: 1,
        weight: 10,
        timeoutMs: 30000,
        maxRetries: 3,
        enabled: true,
        healthCheck: { enabled: true, intervalMs: 60000, timeoutMs: 5000 },
      });

      router.registerProvider({
        id: 'provider-2',
        name: 'Provider 2',
        baseUrl: 'https://p2.api.com',
        api: 'openai',
        priority: 2,
        weight: 10,
        timeoutMs: 30000,
        maxRetries: 3,
        enabled: true,
        healthCheck: { enabled: true, intervalMs: 60000, timeoutMs: 5000 },
      });
    });

    it('should select provider by priority', () => {
      const routerPriority = new ProviderRouter({ strategy: 'priority' });

      routerPriority.registerProvider({
        id: 'high-priority',
        name: 'High Priority',
        baseUrl: 'https://high.api.com',
        api: 'openai',
        priority: 1,
        weight: 10,
        timeoutMs: 30000,
        maxRetries: 3,
        enabled: true,
        healthCheck: { enabled: true, intervalMs: 60000, timeoutMs: 5000 },
      });

      routerPriority.registerProvider({
        id: 'low-priority',
        name: 'Low Priority',
        baseUrl: 'https://low.api.com',
        api: 'openai',
        priority: 5,
        weight: 10,
        timeoutMs: 30000,
        maxRetries: 3,
        enabled: true,
        healthCheck: { enabled: true, intervalMs: 60000, timeoutMs: 5000 },
      });

      const result = routerPriority.selectProvider();

      expect(result.selectedProvider).toBe('high-priority');
      expect(result.reason).toContain('Priority');
    });

    it('should return alternatives', () => {
      const result = router.selectProvider();

      expect(result.selectedProvider).toBeDefined();
      expect(result.alternatives.length).toBeGreaterThan(0);
    });

    it('should throw error when no providers available', () => {
      const emptyRouter = new ProviderRouter();

      expect(() => emptyRouter.selectProvider()).toThrow('No available providers');
    });
  });

  describe('recordResult', () => {
    it('should record successful request', () => {
      router.registerProvider({
        id: 'test-provider',
        name: 'Test',
        baseUrl: 'https://test.api.com',
        api: 'openai',
        priority: 1,
        weight: 10,
        timeoutMs: 30000,
        maxRetries: 3,
        enabled: true,
        healthCheck: { enabled: true, intervalMs: 60000, timeoutMs: 5000 },
      });

      router.recordResult('test-provider', true, 100);

      const status = router.getHealthStatus('test-provider');
      expect(status?.consecutiveFailures).toBe(0);
      expect(status?.successRate).toBeGreaterThan(0.9);
    });

    it('should record failed request', () => {
      router.registerProvider({
        id: 'test-provider',
        name: 'Test',
        baseUrl: 'https://test.api.com',
        api: 'openai',
        priority: 1,
        weight: 10,
        timeoutMs: 30000,
        maxRetries: 3,
        enabled: true,
        healthCheck: { enabled: true, intervalMs: 60000, timeoutMs: 5000 },
      });

      // Simulate 3 consecutive failures
      for (let i = 0; i < 3; i++) {
        router.recordResult('test-provider', false, 5000);
      }

      const status = router.getHealthStatus('test-provider');
      expect(status?.consecutiveFailures).toBe(3);
      expect(status?.healthy).toBe(false);
    });
  });

  describe('getStats', () => {
    it('should return router statistics', () => {
      router.registerProvider({
        id: 'provider-1',
        name: 'Provider 1',
        baseUrl: 'https://p1.api.com',
        api: 'openai',
        priority: 1,
        weight: 10,
        timeoutMs: 30000,
        maxRetries: 3,
        enabled: true,
        healthCheck: { enabled: true, intervalMs: 60000, timeoutMs: 5000 },
      });

      const stats = router.getStats();

      expect(stats).toHaveProperty('totalProviders');
      expect(stats).toHaveProperty('healthyProviders');
      expect(stats).toHaveProperty('avgSuccessRate');
    });
  });

  describe('recoverProvider', () => {
    it('should recover unhealthy provider', () => {
      router.registerProvider({
        id: 'test-provider',
        name: 'Test',
        baseUrl: 'https://test.api.com',
        api: 'openai',
        priority: 1,
        weight: 10,
        timeoutMs: 30000,
        maxRetries: 3,
        enabled: true,
        healthCheck: { enabled: true, intervalMs: 60000, timeoutMs: 5000 },
      });

      // Make provider unhealthy
      for (let i = 0; i < 3; i++) {
        router.recordResult('test-provider', false, 5000);
      }

      // Recover
      router.recoverProvider('test-provider');

      const status = router.getHealthStatus('test-provider');
      expect(status?.healthy).toBe(true);
      expect(status?.consecutiveFailures).toBe(0);
    });
  });
});
