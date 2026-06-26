/**
 * 用户流程可视化器单元测试
 */

import { UserFlowVisualizer } from '../user-flow-visualizer';

describe('UserFlowVisualizer', () => {
  let visualizer: UserFlowVisualizer;
  let mockVideoSkill: any;
  let mockMcpBus: any;

  beforeEach(() => {
    mockVideoSkill = {
      submitTask: jest.fn().mockReturnValue({ success: true, taskId: 'test-task' }),
    };

    mockMcpBus = {
      createGenerateResponse: jest.fn().mockReturnValue({ headers: {}, body: {} }),
      send: jest.fn().mockResolvedValue({ status: 'success' }),
    };

    visualizer = new UserFlowVisualizer(mockVideoSkill, mockMcpBus);
  });

  describe('visualizeFlow', () => {
    it('should visualize user flow to video', async () => {
      const flow = {
        flowId: 'login-flow',
        flowName: '用户登录流程',
        description: '完整的用户登录流程',
        targetUser: '新用户',
        steps: [
          {
            sequence: 1,
            name: '打开登录页面',
            description: '用户访问登录页面',
            userAction: 'Navigate to login page',
            systemResponse: 'Display login form',
            durationSeconds: 3,
          },
          {
            sequence: 2,
            name: '输入凭据',
            description: '用户输入用户名和密码',
            userAction: 'Type username and password',
            systemResponse: 'Validate input',
            durationSeconds: 5,
          },
        ],
        expectedOutcome: '成功登录',
      };

      const result = await visualizer.visualizeFlow(flow);

      expect(result.flowId).toBe('login-flow');
      expect(result.status).toBe('success');
      expect(result.metadata.totalSteps).toBe(2);
    });

    it('should handle visualization failures', async () => {
      mockVideoSkill.submitTask.mockReturnValue({
        success: false,
        message: 'Visualization failed',
      });

      const flow = {
        flowId: 'test-flow',
        flowName: 'Test Flow',
        description: 'Test',
        targetUser: 'User',
        steps: [
          {
            sequence: 1,
            name: 'Step 1',
            description: 'Test',
            userAction: 'Click',
            systemResponse: 'OK',
            durationSeconds: 3,
          },
        ],
        expectedOutcome: 'Done',
      };

      const result = await visualizer.visualizeFlow(flow);

      expect(result.status).toBe('failed');
      expect(result.errors).toBeDefined();
    });
  });

  describe('generateFlowDiagram', () => {
    it('should generate Mermaid flowchart', () => {
      const flow = {
        flowId: 'test-flow',
        flowName: 'Test Flow',
        description: 'Test',
        targetUser: 'User',
        steps: [
          {
            sequence: 1,
            name: 'Step 1',
            description: 'First step',
            userAction: 'Click',
            systemResponse: 'OK',
            durationSeconds: 3,
          },
          {
            sequence: 2,
            name: 'Step 2',
            description: 'Second step',
            userAction: 'Submit',
            systemResponse: 'Complete',
            durationSeconds: 2,
          },
        ],
        expectedOutcome: 'Success',
      };

      const diagram = visualizer.generateFlowDiagram(flow);

      expect(diagram).toContain('flowchart TD');
      expect(diagram).toContain('Start([开始])');
      expect(diagram).toContain('Step1[1. Step 1]');
      expect(diagram).toContain('End([Success])');
    });
  });
});
