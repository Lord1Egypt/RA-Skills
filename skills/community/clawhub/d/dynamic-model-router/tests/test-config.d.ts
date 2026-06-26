/**
 * 测试专用配置
 * 在测试环境中使用简化配置，避免外部依赖和长时间初始化
 */
export declare const TEST_CONFIG: {
    learningEnabled: boolean;
    enableTaskSplitting: boolean;
    enableFallbackRouting: boolean;
    enableParallelExecution: boolean;
    defaultStrategy: "balanced";
    storage: {
        useMemoryStorage: boolean;
        maxMemorySize: number;
    };
    disablePerformancePrediction: boolean;
    disableLearningEngine: boolean;
    disableExternalAPICalls: boolean;
    __TEST_MODE__: boolean;
    fastInitialization: boolean;
    logLevel: "error";
};
/**
 * 检查是否在测试环境中
 */
export declare function isTestEnvironment(): boolean;
/**
 * 获取测试专用的决策引擎配置
 */
export declare function getTestDecisionEngineConfig(): {
    learningEnabled: boolean;
    enableTaskSplitting: boolean;
    enableFallbackRouting: boolean;
    enableParallelExecution: boolean;
    defaultStrategy: "balanced";
};
/**
 * 测试专用的存储配置
 */
export declare function getTestStorageConfig(): {
    storagePath: string;
    maxFileSize: number;
    maxTotalSize: number;
    compression: boolean;
    backupCount: number;
};
//# sourceMappingURL=test-config.d.ts.map