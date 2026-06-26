/**
 * 导入测试 - 验证模块导入是否正常
 */

import { describe, test, expect } from '@jest/globals';

describe('模块导入测试', () => {
  test('应该能够导入DecisionEngine', async () => {
    console.log('开始导入DecisionEngine...');
    const module = await import('../src/routing/decision-engine.js');
    console.log('导入完成');
    expect(module.DecisionEngine).toBeDefined();
    expect(typeof module.DecisionEngine).toBe('function');
  });
  
  test('应该能够导入其他核心模块', async () => {
    const modules = [
      '../src/routing/performance-predictor.js',
      '../src/learning/basic-learner.js',
      '../src/storage/basic-storage.js',
    ];
    
    for (const modulePath of modules) {
      console.log(`导入 ${modulePath}...`);
      const module = await import(modulePath);
      expect(module).toBeDefined();
      console.log(`✅ ${modulePath} 导入成功`);
    }
  });
});