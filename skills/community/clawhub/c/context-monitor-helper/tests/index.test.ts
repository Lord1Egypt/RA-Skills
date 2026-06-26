/**
 * context-monitor 单元测试
 */

import { estimateTokens, generateProgressBar, getModelContextLimit, generateStatusMessage, DEFAULT_CONFIG } from '../src/index';

describe('context-monitor', () => {
  describe('estimateTokens', () => {
    it('should estimate Chinese text tokens correctly', () => {
      const text = '你好世界';
      const tokens = estimateTokens(text);
      expect(tokens).toBeGreaterThan(0);
      expect(tokens).toBeLessThan(10);
    });

    it('should estimate English text tokens correctly', () => {
      const text = 'Hello World';
      const tokens = estimateTokens(text);
      expect(tokens).toBeGreaterThan(0);
      expect(tokens).toBeLessThan(10);
    });

    it('should handle mixed language text', () => {
      const text = '你好 Hello 世界 World';
      const tokens = estimateTokens(text);
      expect(tokens).toBeGreaterThan(0);
    });

    it('should handle empty text', () => {
      expect(estimateTokens('')).toBe(0);
      expect(estimateTokens(undefined as unknown as string)).toBe(0);
    });
  });

  describe('generateProgressBar', () => {
    it('should generate progress bar for 0%', () => {
      const bar = generateProgressBar(0, 10);
      expect(bar).toBe('░░░░░░░░░░');
    });

    it('should generate progress bar for 100%', () => {
      const bar = generateProgressBar(100, 10);
      expect(bar).toBe('▓▓▓▓▓▓▓▓▓▓');
    });

    it('should generate progress bar for 50%', () => {
      const bar = generateProgressBar(50, 10);
      expect(bar).toBe('▓▓▓▓▓░░░░░');
    });

    it('should use default length of 20', () => {
      const bar = generateProgressBar(50);
      expect(bar.length).toBe(20);
    });
  });

  describe('getModelContextLimit', () => {
    it('should return correct limit for qwen3.5-plus', () => {
      expect(getModelContextLimit('qwen3.5-plus')).toBe(256000);
    });

    it('should return correct limit for claude-3-5-sonnet', () => {
      expect(getModelContextLimit('claude-3-5-sonnet')).toBe(200000);
    });

    it('should return correct limit for gpt-4-turbo', () => {
      expect(getModelContextLimit('gpt-4-turbo')).toBe(128000);
    });

    it('should return default limit for unknown model', () => {
      expect(getModelContextLimit('unknown-model')).toBe(128000);
    });

    it('should handle empty model name', () => {
      expect(getModelContextLimit('')).toBe(128000);
    });
  });

  describe('generateStatusMessage', () => {
    it('should generate normal status message', () => {
      const stats = { used: 5000, limit: 10000, percentage: 50 };
      const message = generateStatusMessage(stats, DEFAULT_CONFIG);
      
      expect(message).toContain('📊');
      expect(message).toContain('50.0%');
      expect(message).toContain('5,000');
      expect(message).toContain('10,000');
    });

    it('should generate warning message when above 70%', () => {
      const stats = { used: 7500, limit: 10000, percentage: 75 };
      const message = generateStatusMessage(stats, DEFAULT_CONFIG);
      
      expect(message).toContain('⚠️');
      expect(message).toContain('75.0%');
      expect(message).toContain('/new');
      expect(message).toContain('/compact');
    });

    it('should generate critical message when above 90%', () => {
      const stats = { used: 9500, limit: 10000, percentage: 95 };
      const message = generateStatusMessage(stats, DEFAULT_CONFIG);
      
      expect(message).toContain('🚨');
      expect(message).toContain('95.0%');
      expect(message).toContain('立即');
    });

    it('should respect showProgressBar config', () => {
      const stats = { used: 5000, limit: 10000, percentage: 50 };
      const config = { ...DEFAULT_CONFIG, showProgressBar: false };
      const message = generateStatusMessage(stats, config);
      
      expect(message).not.toContain('▓');
      expect(message).not.toContain('░');
    });

    it('should respect showTokenCount config', () => {
      const stats = { used: 5000, limit: 10000, percentage: 50 };
      const config = { ...DEFAULT_CONFIG, showTokenCount: false };
      const message = generateStatusMessage(stats, config);
      
      expect(message).not.toContain('tokens');
    });
  });

  describe('DEFAULT_CONFIG', () => {
    it('should have correct default values', () => {
      expect(DEFAULT_CONFIG.warningThreshold).toBe(70);
      expect(DEFAULT_CONFIG.criticalThreshold).toBe(90);
      expect(DEFAULT_CONFIG.showProgressBar).toBe(true);
      expect(DEFAULT_CONFIG.showTokenCount).toBe(true);
      expect(DEFAULT_CONFIG.enabled).toBe(true);
    });
  });
});
