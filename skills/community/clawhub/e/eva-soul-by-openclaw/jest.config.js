/**
 * EVA Soul - Jest 测试配置
 */
module.exports = {
  testEnvironment: 'node',
  testMatch: ['**/__tests__/**/*.test.js', '**/*.test.js'],
  collectCoverageFrom: [
    'lib/**/*.js',
    'hooks/**/*.js',
    '!hooks/logger.js',
    '!hooks/performanceMonitor.js'
  ],
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'lcov'],
  verbose: true,
  testTimeout: 10000,
  // 不使用 ESM
  transform: {},
  // 清理 mock 状态
  clearMocks: true,
  restoreMocks: true
};
