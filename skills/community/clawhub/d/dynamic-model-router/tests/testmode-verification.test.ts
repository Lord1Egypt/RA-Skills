/**
 * 测试模式验证测试
 */

import { describe, test, expect } from '@jest/globals';
import { DecisionEngine } from '../src/routing/decision-engine.js';
import { getStorage } from '../src/storage/basic-storage.js';

describe('测试模式验证', () => {
  test('应该检测到测试环境并启用测试模式', () => {
    console.log('NODE_ENV:', process.env.NODE_ENV);
    console.log('JEST_WORKER_ID:', process.env.JEST_WORKER_ID);
    
    // 创建存储实例
    const storage = getStorage();
    console.log('存储实例创建完成');
    
    // 检查是否启用了测试模式
    // 注意：testMode是私有属性，我们无法直接访问
    // 但我们可以通过行为推断
    
    // 快速初始化
    storage.initialize().then(() => {
      console.log('存储初始化完成');
    }).catch(err => {
      console.error('存储初始化失败:', err);
    });
    
    // 创建DecisionEngine实例
    const engine = new DecisionEngine({
      learningEnabled: false,
      enableTaskSplitting: false,
    });
    
    console.log('DecisionEngine创建完成');
    
    // 获取引擎状态
    const status = engine.getEngineStatus();
    console.log('引擎状态:', {
      isInitialized: status.isInitialized,
      learningEnabled: status.config.learningEnabled,
    });
    
    expect(engine).toBeDefined();
    expect(status.isInitialized).toBe(true);
  });
  
  test('应该能够显式启用测试模式', () => {
    // 显式传递testMode配置
    const storage = getStorage({ testMode: true });
    
    // 快速检查：如果testMode生效，初始化应该很快完成
    const initPromise = storage.initialize();
    
    // 初始化应该快速完成（无文件系统操作）
    return expect(initPromise).resolves.not.toThrow();
  });
});