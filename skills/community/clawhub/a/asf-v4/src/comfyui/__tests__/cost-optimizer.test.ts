/**
 * 成本优化器单元测试
 */

import { CostOptimizer } from '../cost-optimizer';

describe('CostOptimizer', () => {
  let optimizer: CostOptimizer;

  beforeEach(() => {
    optimizer = new CostOptimizer();
  });

  describe('calculateCost', () => {
    it('should calculate base cost for default settings', () => {
      const cost = optimizer.calculateCost();

      expect(cost.baseCost).toBe(0.02);
      expect(cost.resolutionMultiplier).toBe(2.0); // 1080P
      expect(cost.durationMultiplier).toBe(1.0); // 5 seconds
      expect(cost.totalCost).toBe(0.04);
    });

    it('should calculate cost for different resolutions', () => {
      const cost480 = optimizer.calculateCost(5, '480P');
      const cost720 = optimizer.calculateCost(5, '720P');
      const cost1080 = optimizer.calculateCost(5, '1080P');

      expect(cost480.totalCost).toBeLessThan(cost720.totalCost);
      expect(cost720.totalCost).toBeLessThan(cost1080.totalCost);
    });

    it('should calculate cost with audio', () => {
      const costWithoutAudio = optimizer.calculateCost(5, '1080P', false);
      const costWithAudio = optimizer.calculateCost(5, '1080P', true);

      expect(costWithAudio.totalCost).toBeGreaterThan(costWithoutAudio.totalCost);
    });

    it('should scale cost with duration', () => {
      const cost5s = optimizer.calculateCost(5, '1080P');
      const cost10s = optimizer.calculateCost(10, '1080P');

      expect(cost10s.totalCost).toBeGreaterThan(cost5s.totalCost);
    });
  });

  describe('checkBudget', () => {
    it('should allow requests within budget', () => {
      const result = optimizer.checkBudget(0.05);

      expect(result.allowed).toBe(true);
      expect(result.remainingBudget).toBeDefined();
    });

    it('should block requests exceeding max cost', () => {
      const result = optimizer.checkBudget(0.15); // Exceeds $0.1 max

      expect(result.allowed).toBe(false);
      expect(result.reason).toContain('exceeds max');
    });

    it('should block when daily budget exhausted', () => {
      const limitedOptimizer = new CostOptimizer({ dailyBudget: 1 });
      
      // 模拟已用预算
      (limitedOptimizer as any).spentToday = 1.0;

      const result = limitedOptimizer.checkBudget(0.05);

      expect(result.allowed).toBe(false);
      expect(result.reason).toContain('budget exhausted');
    });
  });

  describe('getUsageStats', () => {
    it('should return usage statistics', () => {
      optimizer.recordExpense(0.05);
      optimizer.recordExpense(0.03);

      const stats = optimizer.getUsageStats();

      expect(stats.spentToday).toBe(0.08);
      expect(stats.requestsToday).toBe(2);
      expect(stats.avgCostPerRequest).toBe(0.04);
    });

    it('should calculate budget utilization', () => {
      const limitedOptimizer = new CostOptimizer({ dailyBudget: 10 });
      limitedOptimizer.recordExpense(5);

      const stats = limitedOptimizer.getUsageStats();

      expect(stats.budgetUtilization).toBe(0.5); // 50%
    });
  });

  describe('getSuggestions', () => {
    it('should suggest resolution downgrade for 1080P', () => {
      const suggestions = optimizer.getSuggestions('1080P', 5);

      const resolutionSuggestion = suggestions.find(s => s.type === 'resolution_downgrade');
      expect(resolutionSuggestion).toBeDefined();
      expect(resolutionSuggestion?.estimatedSavings).toBeGreaterThan(0);
    });

    it('should suggest duration reduction for long videos', () => {
      const suggestions = optimizer.getSuggestions('1080P', 15);

      const durationSuggestion = suggestions.find(s => s.type === 'duration_reduction');
      expect(durationSuggestion).toBeDefined();
      expect(durationSuggestion?.impact).toBe('high');
    });

    it('should return suggestions sorted by savings', () => {
      const suggestions = optimizer.getSuggestions('1080P', 20);

      for (let i = 1; i < suggestions.length; i++) {
        expect(suggestions[i - 1].estimatedSavings).toBeGreaterThanOrEqual(
          suggestions[i].estimatedSavings
        );
      }
    });
  });

  describe('optimizeRequest', () => {
    it('should optimize for cost priority', () => {
      const request = {
        resolution: '1080P',
        durationSeconds: 15,
      };

      const { optimized, savings } = optimizer.optimizeRequest(request, 'cost_priority');

      expect(optimized.resolution).toBe('720P');
      expect(optimized.durationSeconds).toBeLessThanOrEqual(10);
      expect(savings).toBeGreaterThan(0);
    });

    it('should not optimize for quality priority', () => {
      const request = {
        resolution: '1080P',
        durationSeconds: 15,
      };

      const { optimized, savings } = optimizer.optimizeRequest(request, 'quality_priority');

      expect(optimized.resolution).toBe('1080P');
      expect(savings).toBe(0);
    });

    it('should apply balanced optimization', () => {
      const request = {
        resolution: '1080P',
        durationSeconds: 20,
      };

      const { optimized } = optimizer.optimizeRequest(request, 'balanced');

      expect(optimized.durationSeconds).toBe(15);
    });
  });

  describe('resetBudget', () => {
    it('should reset budget manually', () => {
      optimizer.recordExpense(0.05);
      optimizer.resetBudget();

      const stats = optimizer.getUsageStats();
      expect(stats.spentToday).toBe(0);
      expect(stats.requestsToday).toBe(0);
    });
  });
});
