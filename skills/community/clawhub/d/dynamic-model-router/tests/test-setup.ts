/**
 * Jest测试全局设置
 * 在所有测试运行前执行
 */

import { jest } from '@jest/globals';

// 设置全局测试超时
jest.setTimeout(30000);

// 设置测试环境变量
process.env.NODE_ENV = 'test';
process.env.TEST_MODE = 'true';

// 全局测试辅助函数
global.console = {
  ...console,
  // 在测试中简化日志输出
  log: (...args) => {
    if (process.env.VERBOSE_TEST === 'true') {
      console.log(...args);
    }
  },
  info: (...args) => {
    if (process.env.VERBOSE_TEST === 'true') {
      console.info(...args);
    }
  },
  debug: (...args) => {
    // 测试中默认不显示debug日志
  },
};

// 模拟可能会引起问题的模块
jest.mock('fs/promises', () => ({
  ...jest.requireActual('fs/promises'),
  // 可以在这里添加fs模块的模拟实现
}));

// 模拟path模块
jest.mock('path', () => ({
  ...jest.requireActual('path'),
  join: (...args: string[]) => args.join('/'), // 简化路径连接
}));

// 全局测试清理
afterAll(() => {
  // 清理测试产生的临时文件
  console.log('测试套件完成');
});

// 全局beforeEach钩子
beforeEach(() => {
  // 重置所有模拟
  jest.clearAllMocks();
  
  // 设置测试专用环境
  process.env.TEST_RUN_ID = Date.now().toString();
});

// 测试辅助类型声明
declare global {
  namespace NodeJS {
    interface Global {
      TEST_MODE: boolean;
    }
  }
  
  // 简化测试中的console使用
  const console: Console;
}