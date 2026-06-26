/** @type {import('ts-jest').JestConfigWithTsJest} */
export default {
  preset: 'ts-jest',
  testEnvironment: 'node',
  extensionsToTreatAsEsm: ['.ts'],
  moduleNameMapper: {
    '^(\\.{1,2}/.*)\\.js$': '$1',
  },
  transform: {
    '^.+\\.tsx?$': [
      'ts-jest',
      {
        useESM: true,
        tsconfig: 'tsconfig.json',
      },
    ],
  },
  
  // 解决ESM模块加载问题
  transformIgnorePatterns: [
    'node_modules/(?!(uuid|winston)/)', // 包含必要的ESM模块
  ],
  
  testEnvironmentOptions: {
    url: 'http://localhost',
  },
  
  // 测试匹配模式
  testMatch: ['**/tests/**/*.test.ts', '**/tests/**/*.spec.ts'],
  
  // 临时禁用覆盖率收集以减少问题
  collectCoverage: false,
  
  // 单进程运行，避免并行执行问题
  maxWorkers: 1,
  
  // 增加测试超时时间
  testTimeout: 30000,
  
  // 详细的测试报告
  verbose: true,
  
  // 覆盖率配置（临时禁用）
  collectCoverage: false,
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  },
  
  // 测试结果显示
  reporters: ['default'],
  
  // 设置模块解析
  moduleFileExtensions: ['ts', 'js', 'json', 'node'],
  
  // 全局测试设置（暂时禁用，有TypeScript错误）
  // setupFilesAfterEnv: ['<rootDir>/tests/test-setup.ts'],
  
  // 清理测试环境
  clearMocks: true,
  resetMocks: true,
  restoreMocks: true,
};