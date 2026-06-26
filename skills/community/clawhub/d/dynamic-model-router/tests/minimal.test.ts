/**
 * 最小化测试 - 验证基础功能
 */

import { describe, test, expect } from '@jest/globals';
import { DecisionEngine } from '../src/routing/decision-engine.js';

describe('最小化决策引擎测试', () => {
  test('应该创建DecisionEngine实例而不崩溃', () => {
    console.log('开始创建DecisionEngine实例...');
    const engine = new DecisionEngine({
      learningEnabled: false,
      enableTaskSplitting: false,
    });
    
    console.log('DecisionEngine实例创建成功');
    expect(engine).toBeDefined();
    
    const status = engine.getEngineStatus();
    console.log('引擎状态:', status);
    expect(status).toBeDefined();
    expect(status.isInitialized).toBe(true);
    
    console.log('测试通过');
  });
  
  test('应该获取引擎状态', () => {
    const engine = new DecisionEngine({});
    
    const status = engine.getEngineStatus();
    expect(status).toHaveProperty('isInitialized');
    expect(status).toHaveProperty('config');
    expect(status).toHaveProperty('statistics');
  });
});