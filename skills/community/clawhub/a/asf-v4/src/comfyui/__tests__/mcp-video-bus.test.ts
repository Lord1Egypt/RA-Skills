/**
 * MCP 视频总线单元测试
 */

import { MCPVideoBus } from '../mcp-video-bus';

describe('MCPVideoBus', () => {
  let bus: MCPVideoBus;

  beforeEach(() => {
    bus = new MCPVideoBus();
  });

  describe('send', () => {
    it('should send message successfully', async () => {
      const message = bus.createGenerateRequest(
        { prompt: 'Test video' },
        'test-agent',
        'video-agent'
      );

      const result = await bus.send(message);

      expect(result.status).toBe('success');
      expect(result.messageId).toBeDefined();
      expect(result.durationMs).toBeLessThan(100);
    });

    it('should cache idempotent requests', async () => {
      const request = { prompt: 'Test video' };
      const message1 = bus.createGenerateRequest(request, 'test-agent', 'video-agent');
      const message2 = bus.createGenerateRequest(request, 'test-agent', 'video-agent');

      const result1 = await bus.send(message1);
      const result2 = await bus.send(message2);

      // 相同的幂等键应该返回缓存结果
      expect(result1.messageId).toBe(result2.messageId);
    });

    it('should reject expired messages', async () => {
      const message = bus.createGenerateRequest(
        { prompt: 'Test video' },
        'test-agent',
        'video-agent'
      );
      message.headers.expiresAt = Date.now() - 1000; // 已过期

      const result = await bus.send(message);

      expect(result.status).toBe('failed');
      expect(result.error).toContain('expired');
    });
  });

  describe('createGenerateRequest', () => {
    it('should create request with correct structure', () => {
      const message = bus.createGenerateRequest(
        { prompt: 'Test video', durationSeconds: 5 },
        'test-agent',
        'video-agent'
      );

      expect(message.headers.type).toBe('video.generate.request');
      expect(message.headers.from).toBe('test-agent');
      expect(message.headers.to).toBe('video-agent');
      expect(message.body.data.prompt).toBe('Test video');
      expect(message.body.metadata?.priority).toBe(5);
    });

    it('should generate unique traceId for each request', () => {
      const message1 = bus.createGenerateRequest({ prompt: 'Test' }, 'a', 'b');
      const message2 = bus.createGenerateRequest({ prompt: 'Test' }, 'a', 'b');

      expect(message1.headers.traceId).not.toBe(message2.headers.traceId);
    });
  });

  describe('createQualityCheckRequest', () => {
    it('should create quality check request', () => {
      const response = {
        status: 'success' as const,
        videoPath: '/video/test.mp4',
        qualityScore: 0.85,
      };

      const message = bus.createQualityCheckRequest(response, 'video-agent', 'quality-guard');

      expect(message.headers.type).toBe('video.quality.check.request');
      expect(message.body.metadata?.priority).toBe(8);
    });
  });

  describe('createDeployRequest', () => {
    it('should create deploy request', () => {
      const message = bus.createDeployRequest(
        '/video/test.mp4',
        0.9,
        'quality-guard',
        'deployment-controller'
      );

      expect(message.headers.type).toBe('video.deploy.request');
      expect(message.body.metadata?.priority).toBe(10);
    });
  });

  describe('getQueueStatus', () => {
    it('should return queue status', async () => {
      const message = bus.createGenerateRequest({ prompt: 'Test' }, 'a', 'b');
      await bus.send(message);

      const status = bus.getQueueStatus();

      expect(status.totalMessages).toBeGreaterThan(0);
      expect(status.tracesCount).toBeGreaterThan(0);
    });
  });

  describe('getTrace', () => {
    it('should retrieve trace by traceId', async () => {
      const message = bus.createGenerateRequest({ prompt: 'Test' }, 'a', 'b');
      await bus.send(message);

      const trace = bus.getTrace(message.headers.traceId);

      expect(trace).toBeDefined();
      expect(trace!.length).toBeGreaterThan(0);
    });
  });
});
