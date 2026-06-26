/**
 * 使用Mock的简化测试
 * 验证测试架构是否工作
 */

import { describe, test, expect, beforeEach } from '@jest/globals';
import { createTestDecisionEngine } from './mocks/decision-engine-mock.js';

describe('Mock决策引擎测试', () => {
  let engine: any;
  
  beforeEach(() => {
    engine = createTestDecisionEngine({
      learningEnabled: false,
      enableTaskSplitting: false,
    });
  });
  
  test('应该创建测试决策引擎实例', () => {
    expect(engine).toBeDefined();
    expect(typeof engine.route).toBe('function');
    expect(typeof engine.getEngineStatus).toBe('function');
  });
  
  test('应该获取引擎状态', () => {
    const status = engine.getEngineStatus();
    expect(status.isInitialized).toBe(true);
    expect(status.config.learningEnabled).toBe(false);
    expect(status.statistics.totalDecisions).toBe(0);
  });
  
  test('应该处理路由请求', async () => {
    const request = {
      task: {
        id: 'test_task_001',
        content: '测试任务内容',
        language: 'zh',
        complexity: 'simple',
        category: ['test'],
        estimatedTokens: 100,
        createdAt: new Date(),
      },
      constraints: {},
    };
    
    const response = await engine.route(request);
    
    expect(response).toBeDefined();
    expect(response.decision).toBeDefined();
    expect(response.decision.decisionId).toContain('test_decision_');
    expect(response.decision.selectedModel.id).toBe('deepseek-chat');
    expect(response.executionInstructions.modelId).toBe('deepseek-chat');
  });
  
  test('应该更新统计信息', async () => {
    const initialStats = engine.getStatistics();
    expect(initialStats.totalDecisions).toBe(0);
    
    const request = {
      task: {
        id: 'test_task_002',
        content: '另一个测试任务',
        language: 'zh',
        complexity: 'simple',
        category: ['test'],
        estimatedTokens: 50,
        createdAt: new Date(),
      },
      constraints: {},
    };
    
    await engine.route(request);
    
    const updatedStats = engine.getStatistics();
    expect(updatedStats.totalDecisions).toBe(1);
  });
});