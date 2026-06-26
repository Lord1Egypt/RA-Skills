/**
 * 视频质量门禁单元测试
 */

import { VideoQualityGuard } from '../video-quality-guard';
import { VideoGenerationResponse } from '../comfyui-workflow-orchestrator';

describe('VideoQualityGuard', () => {
  let guard: VideoQualityGuard;

  beforeEach(() => {
    guard = new VideoQualityGuard();
  });

  const mockResponse: VideoGenerationResponse = {
    status: 'success',
    videoPath: '/videos/test-001.mp4',
    durationMs: 5000,
    qualityScore: 0.85,
    metadata: {
      model: 'wan2.6-t2v',
      resolution: '1080P',
      duration: 5,
      aspectRatio: '16:9',
    },
  };

  describe('checkQuality', () => {
    it('should pass high quality video', async () => {
      const report = await guard.checkQuality(mockResponse);

      expect(report.passed).toBe(true);
      expect(report.overallScore).toBeGreaterThanOrEqual(0.7);
      expect(report.recommendation).toBe('accept');
    });

    it('should include all enabled checks', async () => {
      const report = await guard.checkQuality(mockResponse);

      expect(report.items.length).toBeGreaterThan(0);
      expect(report.items.map(i => i.name)).toEqual(
        expect.arrayContaining(['resolution', 'duration', 'visualQuality'])
      );
    });

    it('should calculate weighted score correctly', async () => {
      const report = await guard.checkQuality(mockResponse);

      // All items should contribute to weighted score
      const totalWeight = report.items.reduce((sum, item) => sum + item.weight, 0);
      expect(totalWeight).toBeGreaterThan(0);
    });

    it('should recommend retry when quality is below threshold', async () => {
      // 使用自定义配置创建一个明确的边界场景
      const testGuard = new VideoQualityGuard({
        minPassScore: 0.85, // 高通过标准
        retryThreshold: 0.5,
        manualReviewThreshold: 0.75, // 75% 以上才建议人工审核
        // 只启用视觉质量检查，简化测试
        enabledChecks: ['visualQuality'],
        criticalChecks: [],
      });

      // 创建一个视觉质量分数在 retry 区间的响应
      const mediumQualityResponse: VideoGenerationResponse = {
        ...mockResponse,
        qualityScore: 0.80, // 视觉质量分数：0.75 <= 0.80 < 0.85，应该建议 retry
      };

      const report = await testGuard.checkQuality(mediumQualityResponse);

      // 由于只检查 visualQuality，整体分数就是 0.80
      // 低于 minPassScore (0.85) 但 >= manualReviewThreshold (0.75)
      // 应该建议 retry
      expect(report.passed).toBe(false);
      expect(report.overallScore).toBe(0.80);
      expect(report.recommendation).toBe('retry');
    });

    it('should recommend reject for very low quality', async () => {
      // 创建一个质量非常低的响应，分数低于 retryThreshold
      const veryLowQualityResponse: VideoGenerationResponse = {
        ...mockResponse,
        qualityScore: 0.3,
        metadata: {
          model: 'wan2.6-t2v',
          resolution: 'unknown', // 无效分辨率
          duration: 5,
          aspectRatio: '16:9',
        },
      };

      const report = await guard.checkQuality(veryLowQualityResponse);

      // 分数低于 retryThreshold (0.5)，应该建议 reject
      expect(report.recommendation).toBe('reject');
    });
  });

  describe('critical checks', () => {
    it('should fail when critical check fails', async () => {
      // 创建一个安全检查失败的响应
      const unsafeResponse: VideoGenerationResponse = {
        ...mockResponse,
        status: 'failed',
        error: 'Content safety violation',
      };

      const report = await guard.checkQuality(unsafeResponse);

      // 关键检查项失败应该导致总体失败，并建议 reject
      expect(report.passed).toBe(false);
      // 关键项失败会触发 reject
      expect(report.recommendation).toBe('reject');
      // 安全检查应该失败
      const safetyCheck = report.items.find(item => item.name === 'contentSafety');
      expect(safetyCheck?.passed).toBe(false);
    });
  });

  describe('getStatus', () => {
    it('should return guard status', () => {
      const status = guard.getStatus();

      expect(status).toHaveProperty('consecutiveFailures');
      expect(status).toHaveProperty('failureHistory');
      expect(status).toHaveProperty('config');
    });
  });

  describe('resetFailureCount', () => {
    it('should reset consecutive failures', () => {
      // Simulate some failures
      // @ts-ignore
      guard.consecutiveFailures = 5;

      guard.resetFailureCount();

      const status = guard.getStatus();
      expect(status.consecutiveFailures).toBe(0);
    });
  });

  describe('updateConfig', () => {
    it('should update configuration', () => {
      guard.updateConfig({ minPassScore: 0.8 });

      const status = guard.getStatus();
      expect(status.config.minPassScore).toBe(0.8);
    });
  });
});
