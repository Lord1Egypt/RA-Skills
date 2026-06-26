/**
 * 决策引擎测试专用版本
 * 使用Mock存储和其他简化实现
 */
export declare class TestDecisionEngine {
    private config;
    private performancePredictor;
    private learningEngine;
    private storage;
    private statistics;
    private isInitialized;
    constructor(config?: any);
    initialize(): Promise<void>;
    getEngineStatus(): {
        isInitialized: boolean;
        config: any;
        statistics: any;
        modules: {
            performancePredictor: boolean;
            learningEngine: boolean;
            storage: boolean;
        };
    };
    route(request: any): Promise<{
        decision: {
            decisionId: string;
            timestamp: Date;
            task: any;
            selectedModel: {
                id: string;
                modelId: string;
                name: string;
            };
            selectedProvider: {
                id: string;
                name: string;
            };
            reasoning: {
                primaryReason: string;
                confidence: number;
                alternatives: never[];
            };
            predictedPerformance: {
                expectedLatency: number;
                expectedCost: number;
                expectedQuality: number;
            };
        };
        metrics: {
            decisionTime: number;
            predictionTime: number;
            storageTime: number;
        };
        executionInstructions: {
            modelId: string;
            providerId: string;
            requestConfig: {
                timeout: number;
                maxTokens: number;
                temperature: number;
            };
            monitoring: {
                trackLatency: boolean;
                trackSuccess: boolean;
                trackQuality: boolean;
            };
        };
        learningData: {
            features: {};
            predictedOutcome: {
                expectedLatency: number;
                expectedCost: number;
                expectedQuality: number;
                successProbability: number;
                confidence: number;
            };
        } | undefined;
    }>;
    resetStatistics(): void;
    getStatistics(): any;
}
export declare function createTestDecisionEngine(config?: any): TestDecisionEngine;
export default createTestDecisionEngine;
//# sourceMappingURL=decision-engine-mock.d.ts.map