/**
 * 真实DecisionEngine简化测试
 * 使用最小化配置避免初始化问题
 */

import { describe, test, expect } from '@jest/globals';
import { DecisionEngine } from '../src/routing/decision-engine.js';

describe('真实DecisionEngine简化测试', () => {
  test('应该使用最小配置创建DecisionEngine', () => {
    console.log('测试1: 创建DecisionEngine...');
    const engine = new DecisionEngine({
      learningEnabled: false,
      enableTaskSplitting: false,
      enableFallbackRouting: false,
    });
    
    expect(engine).toBeDefined();
    
    // 快速检查状态
    const status = engine.getEngineStatus();
    console.log('引擎状态:', { isInitialized: status.isInitialized });
    
    expect(status.isInitialized).toBe(true);
    expect(status.config.learningEnabled).toBe(false);
    
    console.log('✅ 测试1通过');
  });
  
  test('应该获取引擎统计信息', () => {
    const engine = new DecisionEngine({ learningEnabled: false });
    
    const status = engine.getEngineStatus();
    expect(status.statistics).toBeDefined();
    expect(typeof status.statistics.totalDecisions).toBe('number');
    expect(status.statistics.totalDecisions).toBe(0);
  });
  
  test('应该处理简单路由请求', async () => {
    const engine = new DecisionEngine({ learningEnabled: false });
    
    // 等待初始化完成
    await new Promise(resolve => setTimeout(resolve, 200));
    
    const request = {
      task: {
        id: 'test_real_001',
        content: '真实引擎测试任务',
        language: 'zh' as const,
        complexity: 'simple' as const,
        category: ['test'],
        estimatedTokens: 50,
        createdAt: new Date(),
      },
      constraints: {},
    };
    
    console.log('开始路由请求...');
    const response = await engine.route(request);
    console.log('路由请求完成');
    
    expect(response).toBeDefined();
    expect(response.decision).toBeDefined();
    expect(response.executionInstructions).toBeDefined();
    
    // 基本验证
    expect(response.decision.selectedModel).toBeDefined();
    expect(response.executionInstructions.modelId).toBeDefined();
  }, 10000); // 10秒超时
});