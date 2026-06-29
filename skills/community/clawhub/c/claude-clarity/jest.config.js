/**
 * Clarity（心虫/草履虫）Jest 配置
 *
 * 使用 node 环境（无需 jsdom），匹配 tests/ 目录下所有 .test.js 文件。
 */
module.exports = {
  testEnvironment: 'node',
  testMatch: [
    '**/tests/**/*.test.js',
  ],
  testPathIgnorePatterns: [
    '/node_modules/',
    '/tests/self-benchmark/',
  ],
  // 测试超时 30 秒（部分模块加载较慢）
  testTimeout: 30000,
  // 收集覆盖率
  collectCoverageFrom: [
    'src/**/*.js',
  ],
  coveragePathIgnorePatterns: [
    '/node_modules/',
    '/tests/',
  ],
  // 不收集覆盖率信息时的安静模式
  verbose: false,
};
