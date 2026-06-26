/**
 * ComfyUI 工作流编排器单元测试
 */

import { ComfyUIWorkflowOrchestrator } from '../comfyui-workflow-orchestrator';

describe('ComfyUIWorkflowOrchestrator', () => {
  let orchestrator: ComfyUIWorkflowOrchestrator;

  beforeEach(() => {
    orchestrator = new ComfyUIWorkflowOrchestrator();
  });

  describe('validateRequest', () => {
    it('should pass valid request', () => {
      const request = {
        prompt: 'A beautiful sunset over the ocean',
        durationSeconds: 5,
        resolution: '1080P' as const,
      };

      // @ts-ignore - accessing private method for testing
      const result = orchestrator.validateRequest(request);

      expect(result.valid).toBe(true);
      expect(result.errors).toHaveLength(0);
    });

    it('should fail when prompt is missing', () => {
      const request = {
        durationSeconds: 5,
      };

      // @ts-ignore
      const result = orchestrator.validateRequest(request);

      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Prompt is required');
    });

    it('should fail when duration exceeds maximum', () => {
      const request = {
        prompt: 'Test video',
        durationSeconds: 15, // Exceeds 10s limit
      };

      // @ts-ignore
      const result = orchestrator.validateRequest(request);

      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Duration exceeds maximum (10s)');
    });

    it('should fail when images exceed limit', () => {
      const request = {
        prompt: 'Test video',
        images: ['img1.jpg', 'img2.jpg', 'img3.jpg', 'img4.jpg', 'img5.jpg', 'img6.jpg'],
      };

      // @ts-ignore
      const result = orchestrator.validateRequest(request);

      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Maximum 5 images allowed');
    });
  });

  describe('checkRateLimit', () => {
    it('should allow requests within limit', () => {
      const result = orchestrator.checkRateLimit('test-client');
      expect(result.allowed).toBe(true);
    });

    it('should block requests exceeding daily quota', () => {
      // @ts-ignore
      orchestrator.dailyQuotaUsed = 100; // Set to max

      const result = orchestrator.checkRateLimit('test-client');

      expect(result.allowed).toBe(false);
      expect(result.reason).toBe('Daily quota exceeded');
    });
  });

  describe('estimateCost', () => {
    it('should calculate base cost', () => {
      const request = {
        prompt: 'Test video',
      };

      // @ts-ignore
      const cost = orchestrator.estimateCost(request);

      expect(cost).toBeGreaterThan(0);
      expect(cost).toBeLessThanOrEqual(0.1); // Within budget
    });

    it('should increase cost for higher resolution', () => {
      const lowResRequest = { prompt: 'Test', resolution: '480P' as const };
      const highResRequest = { prompt: 'Test', resolution: '1080P' as const };

      // @ts-ignore
      const lowCost = orchestrator.estimateCost(lowResRequest);
      // @ts-ignore
      const highCost = orchestrator.estimateCost(highResRequest);

      expect(highCost).toBeGreaterThan(lowCost);
    });
  });

  describe('getUsageStats', () => {
    it('should return usage statistics', () => {
      const stats = orchestrator.getUsageStats();

      expect(stats).toHaveProperty('dailyQuotaUsed');
      expect(stats).toHaveProperty('dailyQuotaRemaining');
      expect(stats).toHaveProperty('requestCount');
    });
  });
});
