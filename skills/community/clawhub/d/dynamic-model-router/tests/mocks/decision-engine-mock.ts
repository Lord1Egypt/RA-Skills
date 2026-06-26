/**
 * 决策引擎测试专用版本
 * 使用Mock存储和其他简化实现
 */

import { getMockStorage } from './storage-mock.js';

// 模拟的性能预测器
class MockPerformancePredictor {
  async initialize() {
    return Promise.resolve();
  }
  
  async predictPerformance(_task: any, _model: any) {
    return {
      expectedLatency: 1000,
      expectedCost: 0.01,
      expectedQuality: 0.8,
      successProbability: 0.95,
      confidence: 0.7,
    };
  }
}

// 模拟的学习引擎
class MockLearningEngine {
  async initialize() {
    return Promise.resolve();
  }
  
  async recordDecision(_decision: any, _actualPerformance: any) {
    return Promise.resolve();
  }
  
  async getModelCorrections(_modelId: string) {
    return {
      latencyCorrection: 0,
      costCorrection: 0,
      qualityCorrection: 0,
    };
  }
}

export class TestDecisionEngine {
  private config: any;
  private performancePredictor: MockPerformancePredictor;
  private learningEngine: MockLearningEngine;
  private storage: any;
  private statistics: any;
  private isInitialized = false;
  
  constructor(config?: any) {
    this.config = {
      learningEnabled: false,
      enableTaskSplitting: false,
      enableFallbackRouting: true,
      defaultStrategy: 'balanced',
      ...config,
    };
    
    this.performancePredictor = new MockPerformancePredictor();
    this.learningEngine = new MockLearningEngine();
    this.storage = getMockStorage();
    
    this.statistics = {
      totalDecisions: 0,
      successfulDecisions: 0,
      averageDecisionTime: 0,
      learningSamples: 0,
    };
    
    // 立即标记为已初始化（测试中不需要真实初始化）
    this.isInitialized = true;
    
    console.log('[TestDecisionEngine] 创建测试版决策引擎');
  }
  
  async initialize(): Promise<void> {
    if (this.isInitialized) {
      return Promise.resolve();
    }
    
    await Promise.all([
      this.performancePredictor.initialize(),
      this.learningEngine.initialize(),
      this.storage.initialize(),
    ]);
    
    this.isInitialized = true;
    return Promise.resolve();
  }
  
  getEngineStatus() {
    return {
      isInitialized: this.isInitialized,
      config: this.config,
      statistics: this.statistics,
      modules: {
        performancePredictor: true,
        learningEngine: true,
        storage: true,
      },
    };
  }
  
  async route(request: any) {
    this.statistics.totalDecisions++;
    
    // 简化路由逻辑
    const decision = {
      decisionId: `test_decision_${Date.now()}`,
      timestamp: new Date(),
      task: request.task,
      selectedModel: {
        id: 'deepseek-chat',
        modelId: 'deepseek-chat',
        name: 'DeepSeek Chat',
      },
      selectedProvider: {
        id: 'deepseek',
        name: 'DeepSeek',
      },
      reasoning: {
        primaryReason: '测试模式：默认选择DeepSeek',
        confidence: 0.8,
        alternatives: [],
      },
      predictedPerformance: {
        expectedLatency: 1000,
        expectedCost: 0.01,
        expectedQuality: 0.8,
      },
    };
    
    const performance = await this.performancePredictor.predictPerformance(
      request.task,
      decision.selectedModel
    );
    
    return {
      decision,
      metrics: {
        decisionTime: 5,
        predictionTime: 2,
        storageTime: 1,
      },
      executionInstructions: {
        modelId: 'deepseek-chat',
        providerId: 'deepseek',
        requestConfig: {
          timeout: 30000,
          maxTokens: 2048,
          temperature: 0.7,
        },
        monitoring: {
          trackLatency: true,
          trackSuccess: true,
          trackQuality: false,
        },
      },
      learningData: this.config.learningEnabled ? {
        features: {},
        predictedOutcome: performance,
      } : undefined,
    };
  }
  
  // 测试辅助方法
  resetStatistics() {
    this.statistics = {
      totalDecisions: 0,
      successfulDecisions: 0,
      averageDecisionTime: 0,
      learningSamples: 0,
    };
  }
  
  getStatistics() {
    return { ...this.statistics };
  }
}

// 工厂函数
export function createTestDecisionEngine(config?: any) {
  return new TestDecisionEngine(config);
}

export default createTestDecisionEngine;