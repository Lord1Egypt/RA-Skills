/**
 * 测试专用配置
 * 在测试环境中使用简化配置，避免外部依赖和长时间初始化
 */

export const TEST_CONFIG = {
  // 核心配置
  learningEnabled: false,
  enableTaskSplitting: false,
  enableFallbackRouting: false,
  enableParallelExecution: false,
  defaultStrategy: 'balanced' as const,
  
  // 简化存储配置
  storage: {
    useMemoryStorage: true, // 使用内存存储而非文件系统
    maxMemorySize: 10 * 1024 * 1024, // 10MB
  },
  
  // 禁用可能引起问题的模块
  disablePerformancePrediction: false, // 性能预测相对简单，可以保留
  disableLearningEngine: true, // 学习引擎可能复杂，先禁用
  disableExternalAPICalls: true, // 禁止外部API调用
  
  // 测试标志
  __TEST_MODE__: true,
  
  // 快速初始化模式
  fastInitialization: true,
  
  // 日志配置
  logLevel: 'error' as const, // 测试中只显示错误日志
};

/**
 * 检查是否在测试环境中
 */
export function isTestEnvironment(): boolean {
  return process.env.NODE_ENV === 'test' || 
         typeof jest !== 'undefined' ||
         process.env.JEST_WORKER_ID !== undefined;
}

/**
 * 获取测试专用的决策引擎配置
 */
export function getTestDecisionEngineConfig() {
  return {
    learningEnabled: TEST_CONFIG.learningEnabled,
    enableTaskSplitting: TEST_CONFIG.enableTaskSplitting,
    enableFallbackRouting: TEST_CONFIG.enableFallbackRouting,
    enableParallelExecution: TEST_CONFIG.enableParallelExecution,
    defaultStrategy: TEST_CONFIG.defaultStrategy,
  };
}

/**
 * 测试专用的存储配置
 */
export function getTestStorageConfig() {
  if (TEST_CONFIG.storage.useMemoryStorage) {
    return {
      storagePath: ':memory:', // 内存存储标记
      maxFileSize: TEST_CONFIG.storage.maxMemorySize,
      maxTotalSize: TEST_CONFIG.storage.maxMemorySize,
      compression: false,
      backupCount: 0,
    };
  }
  
  // 使用临时目录
  return {
    storagePath: '/tmp/test-dynamic-router-' + Date.now(),
    maxFileSize: 10 * 1024 * 1024,
    maxTotalSize: 50 * 1024 * 1024,
    compression: false,
    backupCount: 1,
  };
}