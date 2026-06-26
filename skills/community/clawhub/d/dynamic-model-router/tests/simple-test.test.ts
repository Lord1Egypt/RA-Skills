/**
 * 简单测试 - 验证DecisionEngine基础功能
 */

import { describe, test, expect } from '@jest/globals';
import { DecisionEngine } from '../src/routing/decision-engine.js';
import { RoutingStrategy } from '../src/routing/types.js';

describe('简单决策引擎测试', () => {
  test('应该创建DecisionEngine实例', () => {
    const engine = new DecisionEngine({
      learningEnabled: false,
      enableTaskSplitting: false,
      defaultStrategy: RoutingStrategy.BALANCED,
    });
    
    expect(engine).toBeDefined();
    expect(engine.getEngineStatus).toBeDefined();
    
    const status = engine.getEngineStatus();
    expect(status).toBeDefined();
    expect(typeof status.isInitialized).toBe('boolean');
  });
  
  test('应该处理简单路由请求', async () => {
    const engine = new DecisionEngine({
      learningEnabled: false,
      enableTaskSplitting: false,
    });
    
    // 等待初始化完成
    await new Promise(resolve => setTimeout(resolve, 100));
    
    const request = {
      task: {
        id: 'test_task_001',
        content: '简单的测试任务',
        language: 'zh' as const,
        complexity: 'simple' as const,
        category: ['test'],
        estimatedTokens: 100,
        createdAt: new Date(),
      },
      constraints: {},
    };
    
    const response = await engine.route(request);
    
    expect(response).toBeDefined();
    expect(response.decision).toBeDefined();
    expect(response.executionInstructions).toBeDefined();
    
    // 基本验证
    expect(response.decision.selectedModel).toBeDefined();
    expect(response.decision.decisionId).toBeDefined();
    expect(response.decision.timestamp).toBeDefined();
  });
});