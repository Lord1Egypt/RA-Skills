/**
 * 视频生成技能单元测试
 */

import { VideoGenerationSkill } from '../video-generation-skill';

describe('VideoGenerationSkill', () => {
  let skill: VideoGenerationSkill;

  beforeEach(() => {
    skill = new VideoGenerationSkill();
  });

  describe('submitTask', () => {
    it('should accept valid task', () => {
      const task = {
        id: 'task-001',
        description: 'Generate product demo video',
        priority: 5,
        request: {
          prompt: 'A sleek product showcase video',
          durationSeconds: 5,
        },
        clientId: 'test-client',
        createdAt: Date.now(),
        retryCount: 0,
        maxRetries: 3,
      };

      const result = skill.submitTask(task);

      expect(result.success).toBe(true);
      expect(result.taskId).toBe('task-001');
    });

    it('should reject task with missing fields', () => {
      const task = {
        id: 'task-002',
        description: '', // Missing description
        priority: 3,
        request: {} as any,
        clientId: 'test-client',
        createdAt: Date.now(),
        retryCount: 0,
        maxRetries: 3,
      };

      const result = skill.submitTask(task);

      expect(result.success).toBe(false);
    });

    it('should reject task with past deadline', () => {
      const task = {
        id: 'task-003',
        description: 'Expired task',
        priority: 3,
        request: { prompt: 'Test' },
        clientId: 'test-client',
        createdAt: Date.now(),
        deadline: Date.now() - 10000, // 10 seconds ago
        retryCount: 0,
        maxRetries: 3,
      };

      const result = skill.submitTask(task);

      expect(result.success).toBe(false);
      expect(result.message).toContain('deadline');
    });
  });

  describe('getQueueStatus', () => {
    it('should return queue status', () => {
      const status = skill.getQueueStatus();

      expect(status).toHaveProperty('pendingTasks');
      expect(status).toHaveProperty('runningTasks');
      expect(status).toHaveProperty('maxConcurrentTasks');
    });
  });

  describe('cancelTask', () => {
    it('should return false for non-existent task', () => {
      const result = skill.cancelTask('non-existent-task');

      expect(result.success).toBe(false);
      expect(result.message).toContain('not found');
    });
  });

  describe('getUsageStats', () => {
    it('should return usage statistics', () => {
      const stats = skill.getUsageStats();

      expect(stats).toHaveProperty('totalTasks');
      expect(stats).toHaveProperty('completedTasks');
      expect(stats).toHaveProperty('failedTasks');
      expect(stats).toHaveProperty('successRate');
    });
  });
});
