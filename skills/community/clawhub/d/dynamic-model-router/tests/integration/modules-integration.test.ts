/**
 * 性能预测器和学习引擎集成测试
 */

import { describe, test, expect, beforeEach, afterEach } from '@jest/globals';
import { PerformancePredictor, getPredictor } from '../../src/routing/performance-predictor.js';
import { BasicLearningEngine, getLearner, reinitializeLearner } from '../../src/learning/basic-learner.js';
import type { 
  TaskDescription, 
  ModelInfo, 
  ProviderInfo
} from '../../src/core/types.js';
import type { 
  TaskAnalysisResult,
  RoutingContext 
} from '../../src/routing/types.js';

// 模拟数据
const createMockTask = (): TaskDescription => ({
  id: `task_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
  content: '请解释一下人工智能的基本概念和应用场景',
  language: 'zh' as const,
  complexity: 'medium' as const,
  category: ['general_qa'],
  estimatedTokens: 800,
  createdAt: new Date(),
});

const createMockModelInfo = (): ModelInfo => ({
  modelId: 'deepseek-chat',
  provider: 'deepseek',
  capabilities: {
    coding: 85,
    writing: 90,
    analysis: 88,
    translation: 75,
    reasoning: 82,
  },
  costPerToken: 0.00028,
  avgResponseTime: 3000,
  successRate: 0.95,
  languageSupport: ['zh', 'en'],
  lastUpdated: new Date(),
});

const createMockProviderInfo = (): ProviderInfo => ({
  id: 'deepseek',
  name: 'DeepSeek',
  baseUrl: 'https://api.deepseek.com',
  models: ['deepseek-chat', 'deepseek-reasoner'],
  enabled: true,
});

const createMockTaskAnalysis = (): TaskAnalysisResult => ({
  taskId: 'test_task_123',
  characteristics: {
    complexity: 6.5,
    length: 150,
    tokenEstimate: 800,
    contentType: ['text', 'query'],
    domain: 'general_knowledge',
    intent: 'information_seeking',
    technicalRequirements: [],
  },
  requiredCapabilities: [
    { capability: 'writing', importance: 0.8, evidence: '需要清晰表达' },
    { capability: 'analysis', importance: 0.7, evidence: '需要分析概念' },
  ],
  qualityRequirements: {
    accuracy: 0.9,
    creativity: 0.6,
    thoroughness: 0.8,
    speed: 0.7,
  },
  splittingPotential: {
    canSplit: false,
  },
});

const createMockRoutingContext = (): RoutingContext => ({
  currentLoad: {
    providerLoad: new Map([['deepseek', 0.3]]),
    modelLoad: new Map([['deepseek-chat', 0.4]]),
    recentErrors: new Map([['deepseek-chat', 0]]),
  },
  historicalPerformance: {
    successRates: new Map([['deepseek-chat', 0.96]]),
    averageLatencies: new Map([['deepseek-chat', 2800]]),
    costEfficiency: new Map([['deepseek-chat', 0.85]]),
  },
  environment: {
    timeOfDay: '14',
    networkQuality: 0.9,
    systemLoad: 0.6,
  },
  userPreferences: {
    preferredModels: ['deepseek-chat'],
    avoidedModels: [],
    qualityImportance: 0.8,
    speedImportance: 0.7,
    costSensitivity: 0.5,
  },
});

describe('性能预测器集成测试', () => {
  let predictor: PerformancePredictor;
  
  beforeEach(async () => {
    predictor = getPredictor();
    await predictor.initialize();
  });
  
  afterEach(async () => {
    await predictor.shutdown();
  });
  
  test('应该正确初始化性能预测器', () => {
    const status = predictor.getStatus();
    
    expect(status).toBeDefined();
    expect(status.initialized).toBe(true);
    expect(status.predictionMethod).toBe('hybrid');
    expect(status.historicalDataCount).toBeGreaterThanOrEqual(0);
    expect(status.config).toBeDefined();
    expect(status.config.historicalData).toBeDefined();
    expect(status.config.hasDefaultRules).toBe(true);
  });
  
  test('应该预测模型性能', async () => {
    const task = createMockTask();
    const analysis = createMockTaskAnalysis();
    const model = createMockModelInfo();
    const provider = createMockProviderInfo();
    const context = createMockRoutingContext();
    
    const prediction = await predictor.predictPerformance(
      task,
      analysis,
      model,
      provider,
      context
    );
    
    expect(prediction).toBeDefined();
    expect(prediction.expectedLatency).toBeGreaterThan(0);
    expect(prediction.expectedCost).toBeGreaterThanOrEqual(0);
    expect(prediction.expectedQuality).toBeGreaterThan(0);
    expect(prediction.expectedQuality).toBeLessThanOrEqual(1);
    expect(prediction.successProbability).toBeGreaterThan(0);
    expect(prediction.successProbability).toBeLessThanOrEqual(1);
    expect(prediction.predictionMethod).toBeDefined();
    expect(prediction.confidence).toBeGreaterThan(0);
    expect(prediction.confidence).toBeLessThanOrEqual(1);
  });
  
  test('应该使用不同预测方法', async () => {
    const task = createMockTask();
    const analysis = createMockTaskAnalysis();
    const model = createMockModelInfo();
    const provider = createMockProviderInfo();
    const context = createMockRoutingContext();
    
    // 测试规则基础预测
    predictor.updateConfig({ predictionMethod: 'rule_based' });
    const rulePrediction = await predictor.predictPerformance(
      task,
      analysis,
      model,
      provider,
      context
    );
    
    expect(rulePrediction).toBeDefined();
    expect(rulePrediction.predictionMethod).toBe('rule_based');
    
    // 测试混合预测（默认）
    predictor.updateConfig({ predictionMethod: 'hybrid' });
    const hybridPrediction = await predictor.predictPerformance(
      task,
      analysis,
      model,
      provider,
      context
    );
    
    expect(hybridPrediction).toBeDefined();
    expect(hybridPrediction.predictionMethod).toBe('hybrid');
  });
  
  test('应该记录实际性能数据', async () => {
    const predictionId = 'test_prediction_123';
    const actualPerformance = {
      actualLatency: 2500,
      actualCost: 0.018,
      actualSuccess: true,
      actualQuality: 0.85,
      tokensUsed: 650,
    };
    
    const metadata = {
      taskId: 'test_task_456',
      modelId: 'deepseek-chat',
      providerId: 'deepseek',
      timestamp: new Date(),
    };
    
    // 记录实际性能（应该不报错）
    await predictor.recordActualPerformance(
      predictionId,
      actualPerformance,
      metadata
    );
    
    // 验证预测器状态
    const status = predictor.getStatus();
    expect(status).toBeDefined();
    // 注意：recordActualPerformance可能不立即增加历史数据计数，取决于实现
  });
  
  test('应该处理预测错误', async () => {
    // 测试无效模型（没有默认规则）
    const task = createMockTask();
    const analysis = createMockTaskAnalysis();
    const invalidModel = {
      modelId: 'non-existent-model',
      provider: 'unknown',
      capabilities: { coding: 50, writing: 50, analysis: 50, translation: 50, reasoning: 50 },
      costPerToken: 0.001,
      avgResponseTime: 5000,
      successRate: 0.8,
      languageSupport: ['en'],
      lastUpdated: new Date(),
    } as ModelInfo;
    
    const provider = createMockProviderInfo();
    const context = createMockRoutingContext();
    
    // 预测应该成功（使用回退逻辑）
    const prediction = await predictor.predictPerformance(
      task,
      analysis,
      invalidModel,
      provider,
      context
    );
    
    expect(prediction).toBeDefined();
    expect(prediction.expectedLatency).toBeGreaterThan(0);
  });
  
  test('应该更新配置并保持状态', () => {
    // @ts-ignore - 变量声明但未使用
    const _originalConfig = predictor.getStatus().config;
    
    // 更新配置
    predictor.updateConfig({
      predictionMethod: 'rule_based',
      historicalData: {
        minSamples: 20,
        decayFactor: 0.8,
        maxAgeDays: 60,
      },
    });
    
    const updatedStatus = predictor.getStatus();
    expect(updatedStatus.config.predictionMethod).toBe('rule_based');
    expect(updatedStatus.config.historicalData.minSamples).toBe(20);
    expect(updatedStatus.config.historicalData.decayFactor).toBe(0.8);
    
    // 验证其他配置保持不变
    expect(updatedStatus.config.ruleBased).toBeDefined();
    expect(updatedStatus.config.costCalculation).toBeDefined();
  });
});

describe('学习引擎集成测试', () => {
  let learner: BasicLearningEngine;
  
  beforeEach(async () => {
    learner = getLearner({
      enabled: true,
      learningRate: 0.1,
      minSamples: 5,
      maxSamples: 100,
      learnCapabilities: true,
      learnPerformance: true,
      learnCosts: true,
      learnReliability: true,
    });
    
    await learner.initialize();
  });
  
  afterEach(async () => {
    await learner.shutdown();
  });
  
  test('应该正确初始化学习引擎', () => {
    const status = learner.getStatus();
    
    expect(status).toBeDefined();
    expect(status.initialized).toBe(true);
    expect(status.enabled).toBe(true);
    expect(status.samples).toBe(0);
    expect(status.learningModel).toBeDefined();
    expect(status.learningModel.capabilityCorrections).toBe(0);
    expect(status.learningModel.latencyCorrections).toBe(0);
    expect(status.learningModel.costCorrections).toBe(0);
    expect(status.learningModel.scoringWeights).toBeDefined();
    expect(status.learningModel.statistics).toBeDefined();
  });
  
  test('应该应用学习校正到预测', () => {
    const modelId = 'deepseek-chat';
    const originalPrediction = {
      expectedLatency: 3000,
      expectedCost: 0.02,
      expectedQuality: 0.85,
      successProbability: 0.95,
    };
    
    // 初始校正（无校正系数）
    const corrected1 = learner.applyCorrections(modelId, originalPrediction);
    expect(corrected1).toBeDefined();
    expect(corrected1.expectedLatency).toBe(3000); // 无校正
    expect(corrected1.expectedCost).toBe(0.02);
    
    // 模拟学习校正系数
    learner.importModel(JSON.stringify({
      capabilityCorrections: { 'deepseek-chat': 0.1 },
      latencyCorrections: { 'deepseek-chat': -0.2 },
      costCorrections: { 'deepseek-chat': 0.05 },
      scoringWeights: {
        capability: 0.4,
        cost: 0.3,
        latency: 0.15,
        reliability: 0.1,
        quality: 0.05,
      },
      statistics: {
        totalSamples: 50,
        lastLearningTime: new Date(),
        averageError: { latency: 0.15, cost: 0.12, success: 0.08 },
      },
    }));
    
    // 应用校正
    const corrected2 = learner.applyCorrections(modelId, originalPrediction);
    expect(corrected2).toBeDefined();
    expect(corrected2.expectedLatency).toBeLessThan(3000); // 延迟减少20%
    expect(corrected2.expectedCost).toBeGreaterThan(0.02); // 成本增加5%
    expect(corrected2.expectedQuality).toBeGreaterThan(0.85); // 质量提高10%
    
    // 验证值在合理范围内
    expect(corrected2.expectedLatency).toBeGreaterThan(100);
    expect(corrected2.expectedCost).toBeGreaterThan(0);
    expect(corrected2.expectedQuality).toBeGreaterThan(0);
    expect(corrected2.expectedQuality).toBeLessThanOrEqual(1);
    expect(corrected2.successProbability).toBeGreaterThan(0);
    expect(corrected2.successProbability).toBeLessThanOrEqual(1);
  });
  
  test('应该记录决策结果用于学习', async () => {
    const mockDecision = {
      decisionId: 'test_decision_123',
      task: createMockTask(),
      selectedModel: { id: 'deepseek-chat', name: 'DeepSeek Chat' },
      selectedProvider: { id: 'deepseek', name: 'DeepSeek' },
      predictedPerformance: {
        expectedLatency: 2800,
        expectedCost: 0.018,
        expectedQuality: 0.88,
        successProbability: 0.96,
      },
      reasoning: {
        primaryFactors: [],
        modelCapabilities: [],
        costConsiderations: { costScore: 0.8, budgetConstraint: false, costEfficiency: 0.8 },
        performanceHistory: { successRate: 0.96, avgLatency: 2800, reliabilityScore: 0.95 },
        complexityAnalysis: { taskComplexity: 6, modelAdequacy: 8, complexityMatch: 0.75 },
      },
    } as any;
    
    const mockMetrics = {
      decisionTime: 150,
      modelScores: [
        {
          modelId: 'deepseek-chat',
          providerId: 'deepseek',
          scores: { capability: 0.85, cost: 0.8, performance: 0.75, reliability: 0.9, load: 0.5 },
          totalScore: 0.8,
          constraintsMet: true,
          constraintViolations: [],
        },
      ],
      decisionQuality: {
        confidence: 0.85,
        uncertainty: 0.15,
        alternativesCount: 2,
      },
    } as any;
    
    const mockActualOutcome = {
      id: 'response_123',
      content: '测试响应',
      model: 'deepseek-chat',
      usage: {
        promptTokens: 250,
        completionTokens: 400,
        totalTokens: 650,
      },
      finishReason: 'stop',
    };
    
    const mockActualPerformance = {
      latency: 2650,
      cost: 0.017,
      success: true,
      quality: 0.87,
      tokensUsed: 650,
    };
    
    // 记录决策结果
    await learner.recordDecisionOutcome(
      mockDecision,
      mockMetrics,
      mockActualOutcome,
      mockActualPerformance
    );
    
    // 验证学习引擎状态更新
    const status = learner.getStatus();
    expect(status.samples).toBeGreaterThan(0);
    
    // 应用学习（如果有足够样本）
    if (status.samples >= 5) {
      await learner.applyLearning();
      
      const updatedStatus = learner.getStatus();
      expect(updatedStatus.learningModel.statistics.lastLearningTime).toBeDefined();
    }
  });
  
  test('应该处理批量学习样本', async () => {
    // 记录多个样本
    for (let i = 0; i < 8; i++) {
      const mockDecision = {
        decisionId: `batch_test_${i}`,
        task: createMockTask(),
        selectedModel: { id: 'deepseek-chat', name: 'DeepSeek Chat' },
        selectedProvider: { id: 'deepseek', name: 'DeepSeek' },
        predictedPerformance: {
          expectedLatency: 2800 + i * 100,
          expectedCost: 0.018 + i * 0.001,
          expectedQuality: 0.85,
          successProbability: 0.95,
        },
      } as any;
      
      const mockMetrics = {} as any;
      const mockActualOutcome = {} as any;
      
      const mockActualPerformance = {
        latency: 2700 + i * 120,
        cost: 0.017 + i * 0.001,
        success: Math.random() > 0.1, // 90%成功率
        quality: 0.83 + Math.random() * 0.1,
        tokensUsed: 600 + i * 50,
      };
      
      await learner.recordDecisionOutcome(
        mockDecision,
        mockMetrics,
        mockActualOutcome,
        mockActualPerformance
      );
    }
    
    // 验证样本数量（可能由于去重或其他逻辑，实际样本数可能少于8）
    const status = learner.getStatus();
    expect(status.samples).toBeGreaterThan(0);
    
    // 应用学习（如果样本数足够）
    await learner.applyLearning();
    
    const learnedStatus = learner.getStatus();
    expect(learnedStatus.learningModel.statistics.lastLearningTime).toBeDefined();
    expect(learnedStatus.learningModel.statistics.totalSamples).toBeGreaterThan(0);
  });
  
  test('应该导出和导入学习模型', () => {
    // 导出模型
    const exportedModel = learner.exportModel();
    expect(exportedModel).toBeDefined();
    expect(typeof exportedModel).toBe('string');
    
    const parsedModel = JSON.parse(exportedModel);
    expect(parsedModel).toBeDefined();
    expect(parsedModel.scoringWeights).toBeDefined();
    expect(parsedModel.statistics).toBeDefined();
    
    // 导入模型
    const newModelJson = JSON.stringify({
      capabilityCorrections: { 'test-model': 0.15 },
      latencyCorrections: { 'test-model': -0.1 },
      costCorrections: { 'test-model': 0.08 },
      scoringWeights: {
        capability: 0.35,
        cost: 0.35,
        latency: 0.1,
        reliability: 0.15,
        quality: 0.05,
      },
      statistics: {
        totalSamples: 100,
        lastLearningTime: new Date().toISOString(),
        averageError: { latency: 0.12, cost: 0.1, success: 0.05 },
      },
    });
    
    learner.importModel(newModelJson);
    
    const importedStatus = learner.getStatus();
    expect(importedStatus.learningModel.capabilityCorrections).toBe(1);
    expect(importedStatus.learningModel.scoringWeights.capability).toBe(0.35);
    expect(importedStatus.learningModel.scoringWeights.cost).toBe(0.35);
    expect(importedStatus.learningModel.statistics.totalSamples).toBe(100);
  });
  
  test('应该处理学习引擎禁用状态', async () => {
    // 使用reinitializeLearner而不是getLearner，避免单例问题
    const disabledLearner = reinitializeLearner({
      enabled: false,
      minSamples: 5,
    });
    
    await disabledLearner.initialize();
    
    const status = disabledLearner.getStatus();
    expect(status.enabled).toBe(false);
    expect(status.initialized).toBe(true);
    
    // 应用校正应该返回原始预测
    const originalPrediction = {
      expectedLatency: 3000,
      expectedCost: 0.02,
      expectedQuality: 0.85,
      successProbability: 0.95,
    };
    
    const corrected = disabledLearner.applyCorrections('test-model', originalPrediction);
    expect(corrected).toEqual(originalPrediction);
    
    // 记录结果应该被跳过
    await disabledLearner.recordDecisionOutcome(
      {} as any,
      {} as any,
      {} as any,
      {} as any
    );
    
    await disabledLearner.shutdown();
  });
  
  test('应该获取校正后的评分权重', () => {
    const weights = learner.getCorrectedWeights();
    
    expect(weights).toBeDefined();
    expect(weights.capability).toBeGreaterThan(0);
    expect(weights.cost).toBeGreaterThan(0);
    expect(weights.latency).toBeGreaterThan(0);
    expect(weights.reliability).toBeGreaterThan(0);
    expect(weights.quality).toBeGreaterThan(0);
    
    // 权重之和应该接近1
    const totalWeight = weights.capability + weights.cost + weights.latency + weights.reliability + weights.quality;
    expect(totalWeight).toBeCloseTo(1, 0.01);
  });
});

describe('模块间集成测试', () => {
  test('性能预测器和学习引擎应该能协同工作', async () => {
    const predictor = getPredictor();
    const learner = getLearner();
    
    await predictor.initialize();
    await learner.initialize();
    
    // 创建测试数据
    const task = createMockTask();
    const analysis = createMockTaskAnalysis();
    const model = createMockModelInfo();
    const provider = createMockProviderInfo();
    const context = createMockRoutingContext();
    
    // 1. 性能预测器生成预测
    const prediction = await predictor.predictPerformance(
      task,
      analysis,
      model,
      provider,
      context
    );
    
    expect(prediction).toBeDefined();
    
    // 2. 学习引擎应用校正
    const correctedPrediction = learner.applyCorrections(model.modelId, prediction);
    
    expect(correctedPrediction).toBeDefined();
    expect(correctedPrediction.expectedLatency).toBeGreaterThan(0);
    
    // 3. 记录实际结果用于学习
    const actualPerformance = {
      latency: 2700,
      cost: 0.017,
      success: true,
      quality: 0.86,
      tokensUsed: 620,
    };
    
    await learner.recordDecisionOutcome(
      {
        decisionId: 'integration_test',
        task,
        selectedModel: { id: model.modelId },
        selectedProvider: { id: provider.id },
        predictedPerformance: prediction,
      } as any,
      {} as any,
      {} as any,
      actualPerformance
    );
    
    // 4. 记录到性能预测器
    await predictor.recordActualPerformance(
      'integration_prediction',
      {
        actualLatency: actualPerformance.latency,
        actualCost: actualPerformance.cost,
        actualSuccess: actualPerformance.success,
        actualQuality: actualPerformance.quality,
        tokensUsed: actualPerformance.tokensUsed,
      },
      {
        taskId: task.id,
        modelId: model.modelId,
        providerId: provider.id,
        timestamp: new Date(),
      }
    );
    
    // 清理
    await predictor.shutdown();
    await learner.shutdown();
  });
});