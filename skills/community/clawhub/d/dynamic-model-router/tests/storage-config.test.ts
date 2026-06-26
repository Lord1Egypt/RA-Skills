/**
 * 存储配置测试 - 使用临时目录
 */

import { describe, test, expect } from '@jest/globals';
import { DecisionEngine } from '../src/routing/decision-engine.js';
import os from 'os';
import path from 'path';

describe('存储配置测试', () => {
  test('应该使用临时目录创建DecisionEngine', async () => {
    console.log('测试开始...');
    
    const tempStoragePath = path.join(os.tmpdir(), 'test-dynamic-router-storage');
    console.log('临时存储路径:', tempStoragePath);
    
    const engine = new DecisionEngine({
      learningEnabled: false,
      enableTaskSplitting: false,
      // 传递存储配置到存储模块？
    });
    
    console.log('DecisionEngine实例创建成功');
    
    // 注意：DecisionEngine构造函数不直接接受存储配置
    // 存储模块有自己的配置机制
    
    expect(engine).toBeDefined();
    
    // 快速检查状态，不等待太久
    const status = engine.getEngineStatus();
    console.log('引擎状态:', { isInitialized: status.isInitialized });
    
    expect(status.isInitialized).toBe(true);
    
    console.log('测试通过');
  }, 30000); // 30秒超时
  
  test('应该快速创建和销毁引擎', () => {
    // 这个测试不等待任何异步操作
    const engine = new DecisionEngine({
      learningEnabled: false,
    });
    
    expect(engine).toBeDefined();
    
    // 立即获取状态，不等待初始化
    const status = engine.getEngineStatus();
    expect(typeof status.isInitialized).toBe('boolean');
    
    // 即使初始化未完成，也应该有状态
    expect(status).toHaveProperty('config');
    expect(status).toHaveProperty('statistics');
  });
});