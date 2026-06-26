/**
 * 基础学习引擎 - 从历史数据中学习优化路由决策
 * 
 * 核心功能：
 * 1. 记录决策结果和实际性能
 * 2. 分析预测误差，优化预测模型
 * 3. 调整模型评分权重
 * 4. 识别模型能力模式
 */

import { RouterLogger } from '../utils/logger.js';
import type { 
  RoutingDecision, 
  RoutingMetrics,
  PredictedPerformance
} from '../routing/types.js';
import type { ModelResponse } from '../core/types.js';

const logger = new RouterLogger({ module: 'basic-learner' });

/**
 * 学习引擎配置
 */
export interface LearningEngineConfig {
  enabled: boolean;
  
  // 学习参数
  learningRate: number; // 学习率 0-1
  minSamples: number; // 开始学习的最小样本数
  maxSamples: number; // 最大样本数（内存限制）
  
  // 学习领域
  learnCapabilities: boolean; // 学习模型能力
  learnPerformance: boolean; // 学习性能预测
  learnCosts: boolean; // 学习成本预测
  learnReliability: boolean; // 学习可靠性
  
  // 数据保留
  dataRetentionDays: number; // 数据保留天数
  autoCleanup: boolean; // 自动清理旧数据
}

/**
 * 学习样本
 */
export interface LearningSample {
  id: string;
  decisionId: string;
  taskId: string;
  modelId: string;
  providerId: string;
  
  // 输入特征
  features: {
    taskComplexity: number;
    taskLength: number;
    estimatedTokens: number;
    requiredCapabilities: string[];
    modelScores: Record<string, number>;
  };
  
  // 预测值
  predictions: {
    latency: number;
    cost: number;
    quality: number;
    successProbability: number;
  };
  
  // 实际值
  actuals: {
    latency: number;
    cost: number;
    success: boolean;
    quality?: number;
    tokensUsed?: number;
  };
  
  // 误差分析
  errors: {
    latencyError: number;
    costError: number;
    qualityError?: number;
    successError: number; // 1-successProbability (如果失败)
  };
  
  // 元数据
  metadata: {
    recordedAt: Date;
    predictionMethod: string;
    learningApplied: boolean;
  };
}

/**
 * 学习模型（简化）
 */
export interface LearningModel {
  // 模型能力校正
  capabilityCorrections: Map<string, number>; // modelId -> 校正系数
  
  // 性能预测校正
  latencyCorrections: Map<string, number>; // modelId -> 延迟校正系数
  costCorrections: Map<string, number>; // modelId -> 成本校正系数
  
  // 权重调整
  scoringWeights: {
    capability: number;
    cost: number;
    latency: number;
    reliability: number;
    quality: number;
  };
  
  // 统计信息
  statistics: {
    totalSamples: number;
    lastLearningTime: Date;
    averageError: {
      latency: number;
      cost: number;
      success: number;
    };
  };
}

/**
 * 基础学习引擎
 */
export class BasicLearningEngine {
  private config: LearningEngineConfig;
  private learningModel: LearningModel;
  private samples: LearningSample[];
  private initialized = false;
  
  constructor(config?: Partial<LearningEngineConfig>) {
    logger.info('初始化基础学习引擎');
    
    // 默认配置
    this.config = {
      enabled: true,
      learningRate: 0.1,
      minSamples: 10,
      maxSamples: 1000,
      learnCapabilities: true,
      learnPerformance: true,
      learnCosts: true,
      learnReliability: true,
      dataRetentionDays: 30,
      autoCleanup: true,
      ...config
    };
    
    // 初始化学习模型
    this.learningModel = {
      capabilityCorrections: new Map(),
      latencyCorrections: new Map(),
      costCorrections: new Map(),
      scoringWeights: {
        capability: 0.4,
        cost: 0.3,
        latency: 0.15,
        reliability: 0.1,
        quality: 0.05,
      },
      statistics: {
        totalSamples: 0,
        lastLearningTime: new Date(),
        averageError: {
          latency: 0,
          cost: 0,
          success: 0,
        },
      },
    };
    
    this.samples = [];
    
    logger.info('基础学习引擎实例创建完成');
  }
  
  /**
   * 初始化学习引擎
   */
  async initialize(): Promise<void> {
    if (this.initialized) {
      logger.warn('学习引擎已经初始化');
      return;
    }
    
    if (!this.config.enabled) {
      logger.info('学习引擎被禁用');
      this.initialized = true;
      return;
    }
    
    try {
      logger.info('开始初始化基础学习引擎');
      
      // TODO: 从存储加载学习模型
      // await this.loadLearningModel();
      
      // TODO: 从存储加载历史样本
      // await this.loadSamples();
      
      // 如果有足够样本，应用学习
      if (this.samples.length >= this.config.minSamples) {
        await this.applyLearning();
      }
      
      // 确保lastLearningTime是Date对象
      const lastLearningTime = this.learningModel.statistics.lastLearningTime;
      const modelAge = lastLearningTime instanceof Date 
        ? lastLearningTime.toISOString() 
        : new Date(lastLearningTime || Date.now()).toISOString();
      
      logger.info('基础学习引擎初始化完成', {
        sampleCount: this.samples.length,
        modelAge,
      });
      
      this.initialized = true;
      
    } catch (error) {
      logger.error('学习引擎初始化失败', error as Error);
      throw error;
    }
  }
  
  /**
   * 记录决策结果用于学习
   */
  async recordDecisionOutcome(
    decision: RoutingDecision,
    metrics: RoutingMetrics,
    actualOutcome: ModelResponse,
    actualPerformance?: {
      latency: number;
      cost: number;
      success: boolean;
      quality?: number;
      tokensUsed?: number;
    }
  ): Promise<void> {
    if (!this.config.enabled) {
      return;
    }
    
    if (!this.initialized) {
      await this.initialize();
    }
    
    const sampleId = `sample_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    const sampleLogger = new RouterLogger({ sampleId });
    
    try {
      // 安全提取modelId，处理多种格式
      let modelId: string;
      if (typeof decision.selectedModel === 'string') {
        modelId = decision.selectedModel;
      } else if (decision.selectedModel?.modelId) {
        modelId = decision.selectedModel.modelId;
      } else {
        // 回退：尝试从对象中提取任何可能的标识符
        modelId = 'unknown-model';
        try {
          const modelObj = decision.selectedModel as any;
          if (modelObj?.id) modelId = modelObj.id;
          else if (modelObj?.name) modelId = modelObj.name;
          else if (modelObj?.model) modelId = modelObj.model;
        } catch {
          // 忽略错误，使用默认值
        }
      }
      
      sampleLogger.info('记录决策结果用于学习', {
        decisionId: decision.decisionId,
        modelId,
        success: actualOutcome !== undefined,
      });
      
      // 提取特征
      const features = this.extractFeatures(decision, metrics);
      
      // 提取预测值
      const predictions = {
        latency: decision.predictedPerformance.expectedLatency,
        cost: decision.predictedPerformance.expectedCost,
        quality: decision.predictedPerformance.expectedQuality,
        successProbability: decision.predictedPerformance.successProbability,
      };
      
      // 计算实际值
      const actuals = actualPerformance || {
        latency: 0, // 需要实际数据
        cost: 0,
        success: actualOutcome !== undefined,
        quality: 0.5,
        tokensUsed: actualOutcome?.usage?.totalTokens || 0,
      };
      
      // 计算误差
      const errors = this.calculateErrors(predictions, actuals);
      
      // 创建学习样本
      const sample: LearningSample = {
        id: sampleId,
        decisionId: decision.decisionId,
        taskId: decision.task.id,
        modelId: decision.selectedModel.modelId,
        providerId: decision.selectedProvider.id,
        features,
        predictions,
        actuals,
        errors,
        metadata: {
          recordedAt: new Date(),
          predictionMethod: 'unknown', // decision.predictedPerformance没有predictionMethod属性
          learningApplied: false,
        },
      };
      
      // 保存样本
      this.samples.push(sample);
      
      // 更新统计
      this.updateStatistics(sample);
      
      // 如果达到样本阈值，触发学习
      if (this.samples.length >= this.config.minSamples && 
          this.samples.length % 10 === 0) { // 每10个样本学习一次
        await this.applyLearning();
      }
      
      // 如果样本过多，清理旧数据
      if (this.samples.length > this.config.maxSamples) {
        this.cleanupOldSamples();
      }
      
      sampleLogger.debug('决策结果记录完成');
      
    } catch (error) {
      sampleLogger.error('记录决策结果失败', error as Error);
      // 不抛出错误，避免影响主流程
    }
  }
  
  /**
   * 应用学习（更新学习模型）
   */
  async applyLearning(): Promise<void> {
    if (!this.config.enabled || this.samples.length < this.config.minSamples) {
      return;
    }
    
    const learningId = `learning_${Date.now()}`;
    const learningLogger = new RouterLogger({ learningId });
    
    try {
      learningLogger.info('开始应用学习', {
        sampleCount: this.samples.length,
        minSamples: this.config.minSamples,
      });
      
      // 1. 分析误差模式
      const errorPatterns = this.analyzeErrorPatterns();
      
      // 2. 更新模型能力校正
      if (this.config.learnCapabilities) {
        this.updateCapabilityCorrections(errorPatterns);
      }
      
      // 3. 更新性能预测校正
      if (this.config.learnPerformance) {
        this.updatePerformanceCorrections(errorPatterns);
      }
      
      // 4. 更新成本预测校正
      if (this.config.learnCosts) {
        this.updateCostCorrections(errorPatterns);
      }
      
      // 5. 更新权重调整
      if (this.config.learnReliability) {
        this.updateScoringWeights(errorPatterns);
      }
      
      // 6. 更新统计信息
      this.learningModel.statistics.lastLearningTime = new Date();
      this.learningModel.statistics.totalSamples = this.samples.length;
      
      // 标记样本为已学习
      this.samples.forEach(sample => {
        sample.metadata.learningApplied = true;
      });
      
      // TODO: 保存学习模型
      // await this.saveLearningModel();
      
      learningLogger.info('学习应用完成', {
        modelUpdates: {
          capabilityCorrections: this.learningModel.capabilityCorrections.size,
          latencyCorrections: this.learningModel.latencyCorrections.size,
          costCorrections: this.learningModel.costCorrections.size,
        },
        averageErrors: this.learningModel.statistics.averageError,
      });
      
    } catch (error) {
      learningLogger.error('应用学习失败', error as Error);
      throw error;
    }
  }
  
  /**
   * 应用学习校正到预测
   */
  applyCorrections(
    modelId: string,
    predictions: PredictedPerformance
  ): PredictedPerformance {
    if (!this.config.enabled) {
      return predictions;
    }
    
    const corrected = { ...predictions };
    
    // 应用延迟校正
    const latencyCorrection = this.learningModel.latencyCorrections.get(modelId);
    if (latencyCorrection) {
      corrected.expectedLatency *= (1 + latencyCorrection);
    }
    
    // 应用成本校正
    const costCorrection = this.learningModel.costCorrections.get(modelId);
    if (costCorrection) {
      corrected.expectedCost *= (1 + costCorrection);
    }
    
    // 应用能力校正（影响质量预测）
    const capabilityCorrection = this.learningModel.capabilityCorrections.get(modelId);
    if (capabilityCorrection) {
      corrected.expectedQuality *= (1 + capabilityCorrection);
      // 能力校正也影响成功率
      corrected.successProbability *= (1 + capabilityCorrection * 0.5);
    }
    
    // 确保值在合理范围内
    corrected.expectedLatency = Math.max(100, corrected.expectedLatency);
    corrected.expectedCost = Math.max(0, corrected.expectedCost);
    corrected.expectedQuality = Math.max(0, Math.min(1, corrected.expectedQuality));
    corrected.successProbability = Math.max(0.1, Math.min(0.99, corrected.successProbability));
    
    return corrected;
  }
  
  /**
   * 获取校正后的评分权重
   */
  getCorrectedWeights(): LearningModel['scoringWeights'] {
    return { ...this.learningModel.scoringWeights };
  }
  
  /**
   * 提取特征
   */
  private extractFeatures(decision: RoutingDecision, metrics: RoutingMetrics): LearningSample['features'] {
    const selectedScore = metrics.modelScores.find(s => 
      s.modelId === decision.selectedModel.modelId && 
      s.providerId === decision.selectedProvider.id
    );
    
    return {
      taskComplexity: decision.task.complexity === 'complex' ? 0.8 : 
                     decision.task.complexity === 'medium' ? 0.5 : 0.2,
      taskLength: decision.task.content.length,
      estimatedTokens: decision.task.estimatedTokens || 1000,
      requiredCapabilities: decision.reasoning.modelCapabilities?.map(mc => mc.capability) || [],
      modelScores: selectedScore ? {
        capability: selectedScore.scores.capability,
        cost: selectedScore.scores.cost,
        latency: selectedScore.scores.performance,
        reliability: selectedScore.scores.reliability,
        quality: selectedScore.scores.capability, // 简化
      } : {},
    };
  }
  
  /**
   * 计算误差
   */
  private calculateErrors(
    predictions: LearningSample['predictions'],
    actuals: LearningSample['actuals']
  ): LearningSample['errors'] {
    return {
      latencyError: actuals.latency > 0 ? (actuals.latency - predictions.latency) / actuals.latency : 0,
      costError: actuals.cost > 0 ? (actuals.cost - predictions.cost) / actuals.cost : 0,
      qualityError: actuals.quality !== undefined ? (actuals.quality - predictions.quality) : undefined,
      successError: actuals.success ? 0 : 1 - predictions.successProbability,
    };
  }
  
  /**
   * 分析误差模式
   */
  private analyzeErrorPatterns(): any {
    const recentSamples = this.samples.slice(-100); // 最近100个样本
    
    const patterns = {
      byModel: new Map<string, {
        count: number;
        avgLatencyError: number;
        avgCostError: number;
        avgSuccessError: number;
      }>(),
      
      byComplexity: new Map<string, {
        count: number;
        avgLatencyError: number;
        avgCostError: number;
      }>(),
      
      overall: {
        totalSamples: recentSamples.length,
        avgLatencyError: 0,
        avgCostError: 0,
        avgSuccessError: 0,
      },
    };
    
    // 按模型分组
    for (const sample of recentSamples) {
      // 按模型
      if (!patterns.byModel.has(sample.modelId)) {
        patterns.byModel.set(sample.modelId, {
          count: 0,
          avgLatencyError: 0,
          avgCostError: 0,
          avgSuccessError: 0,
        });
      }
      const modelPattern = patterns.byModel.get(sample.modelId)!;
      modelPattern.count++;
      modelPattern.avgLatencyError += sample.errors.latencyError;
      modelPattern.avgCostError += sample.errors.costError;
      modelPattern.avgSuccessError += sample.errors.successError;
      
      // 按复杂度
      const complexity = sample.features.taskComplexity > 0.7 ? 'high' :
                        sample.features.taskComplexity > 0.4 ? 'medium' : 'low';
      
      if (!patterns.byComplexity.has(complexity)) {
        patterns.byComplexity.set(complexity, {
          count: 0,
          avgLatencyError: 0,
          avgCostError: 0,
        });
      }
      const complexityPattern = patterns.byComplexity.get(complexity)!;
      complexityPattern.count++;
      complexityPattern.avgLatencyError += sample.errors.latencyError;
      complexityPattern.avgCostError += sample.errors.costError;
      
      // 总体
      patterns.overall.avgLatencyError += sample.errors.latencyError;
      patterns.overall.avgCostError += sample.errors.costError;
      patterns.overall.avgSuccessError += sample.errors.successError;
    }
    
    // 计算平均值
    for (const [_modelId, pattern] of patterns.byModel) {
      pattern.avgLatencyError /= pattern.count;
      pattern.avgCostError /= pattern.count;
      pattern.avgSuccessError /= pattern.count;
    }
    
    for (const [_complexity, pattern] of patterns.byComplexity) {
      pattern.avgLatencyError /= pattern.count;
      pattern.avgCostError /= pattern.count;
    }
    
    if (patterns.overall.totalSamples > 0) {
      patterns.overall.avgLatencyError /= patterns.overall.totalSamples;
      patterns.overall.avgCostError /= patterns.overall.totalSamples;
      patterns.overall.avgSuccessError /= patterns.overall.totalSamples;
    }
    
    return patterns;
  }
  
  /**
   * 更新模型能力校正
   */
  private updateCapabilityCorrections(errorPatterns: any): void {
    for (const [modelId, pattern] of errorPatterns.byModel) {
      // 基于成功率误差调整能力校正
      const successError = pattern.avgSuccessError;
      if (Math.abs(successError) > 0.1) { // 误差超过10%
        const currentCorrection = this.learningModel.capabilityCorrections.get(modelId) || 0;
        const newCorrection = currentCorrection + (successError * this.config.learningRate * -1);
        this.learningModel.capabilityCorrections.set(modelId, newCorrection);
        
        logger.debug('更新模型能力校正', {
          modelId,
          successError,
          oldCorrection: currentCorrection,
          newCorrection,
        });
      }
    }
  }
  
  /**
   * 更新性能预测校正
   */
  private updatePerformanceCorrections(errorPatterns: any): void {
    for (const [modelId, pattern] of errorPatterns.byModel) {
      // 基于延迟误差调整性能校正
      const latencyError = pattern.avgLatencyError;
      if (Math.abs(latencyError) > 0.2) { // 误差超过20%
        const currentCorrection = this.learningModel.latencyCorrections.get(modelId) || 0;
        const newCorrection = currentCorrection + (latencyError * this.config.learningRate);
        this.learningModel.latencyCorrections.set(modelId, newCorrection);
        
        logger.debug('更新性能预测校正', {
          modelId,
          latencyError,
          oldCorrection: currentCorrection,
          newCorrection,
        });
      }
    }
  }
  
  /**
   * 更新成本预测校正
   */
  private updateCostCorrections(errorPatterns: any): void {
    for (const [modelId, pattern] of errorPatterns.byModel) {
      // 基于成本误差调整成本校正
      const costError = pattern.avgCostError;
      if (Math.abs(costError) > 0.2) { // 误差超过20%
        const currentCorrection = this.learningModel.costCorrections.get(modelId) || 0;
        const newCorrection = currentCorrection + (costError * this.config.learningRate);
        this.learningModel.costCorrections.set(modelId, newCorrection);
        
        logger.debug('更新成本预测校正', {
          modelId,
          costError,
          oldCorrection: currentCorrection,
          newCorrection,
        });
      }
    }
  }
  
  /**
   * 更新评分权重
   */
  private updateScoringWeights(errorPatterns: any): void {
    // 基于总体误差模式调整权重
    const weights = this.learningModel.scoringWeights;
    const totalError = Math.abs(errorPatterns.overall.avgLatencyError) +
                      Math.abs(errorPatterns.overall.avgCostError) +
                      Math.abs(errorPatterns.overall.avgSuccessError);
    
    if (totalError > 0.3) { // 总体误差较大时调整权重
      // 增加误差较小因素的权重，减少误差较大因素的权重
      const errorRatios = {
        latency: Math.abs(errorPatterns.overall.avgLatencyError) / totalError,
        cost: Math.abs(errorPatterns.overall.avgCostError) / totalError,
        success: Math.abs(errorPatterns.overall.avgSuccessError) / totalError,
      };
      
      // 调整（简化逻辑）
      weights.latency *= (1 - errorRatios.latency * 0.1);
      weights.cost *= (1 - errorRatios.cost * 0.1);
      weights.reliability *= (1 - errorRatios.success * 0.1);
      
      // 归一化
      const totalWeight = weights.capability + weights.cost + weights.latency + weights.reliability + weights.quality;
      weights.capability /= totalWeight;
      weights.cost /= totalWeight;
      weights.latency /= totalWeight;
      weights.reliability /= totalWeight;
      weights.quality /= totalWeight;
      
      logger.debug('更新评分权重', {
        oldWeights: { ...weights },
        errorRatios,
        totalError,
      });
    }
  }
  
  /**
   * 更新统计信息
   */
  private updateStatistics(sample: LearningSample): void {
    const stats = this.learningModel.statistics.averageError;
    const sampleCount = this.learningModel.statistics.totalSamples;
    
    // 指数移动平均
    const alpha = 0.1;
    stats.latency = stats.latency * (1 - alpha) + Math.abs(sample.errors.latencyError) * alpha;
    stats.cost = stats.cost * (1 - alpha) + Math.abs(sample.errors.costError) * alpha;
    stats.success = stats.success * (1 - alpha) + sample.errors.successError * alpha;
    
    this.learningModel.statistics.totalSamples = sampleCount + 1;
  }
  
  /**
   * 清理旧样本
   */
  private cleanupOldSamples(): void {
    if (!this.config.autoCleanup) {
      return;
    }
    
    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - this.config.dataRetentionDays);
    
    const initialCount = this.samples.length;
    this.samples = this.samples.filter(sample => 
      sample.metadata.recordedAt > cutoffDate
    );
    
    const removedCount = initialCount - this.samples.length;
    if (removedCount > 0) {
      logger.info('清理旧样本', {
        removedCount,
        remainingCount: this.samples.length,
        cutoffDate: cutoffDate.toISOString(),
      });
    }
  }
  
  /**
   * 获取学习引擎状态
   */
  getStatus(): any {
    return {
      initialized: this.initialized,
      enabled: this.config.enabled,
      samples: this.samples.length,
      learningModel: {
        capabilityCorrections: this.learningModel.capabilityCorrections.size,
        latencyCorrections: this.learningModel.latencyCorrections.size,
        costCorrections: this.learningModel.costCorrections.size,
        scoringWeights: this.learningModel.scoringWeights,
        statistics: this.learningModel.statistics,
      },
    };
  }
  
  /**
   * 导出学习模型
   */
  exportModel(): string {
    return JSON.stringify(this.learningModel, null, 2);
  }
  
  /**
   * 导入学习模型
   */
  importModel(modelJson: string): void {
    const model = JSON.parse(modelJson);
    this.learningModel = {
      capabilityCorrections: new Map(Object.entries(model.capabilityCorrections || {})),
      latencyCorrections: new Map(Object.entries(model.latencyCorrections || {})),
      costCorrections: new Map(Object.entries(model.costCorrections || {})),
      scoringWeights: model.scoringWeights || this.learningModel.scoringWeights,
      statistics: model.statistics || this.learningModel.statistics,
    };
    
    logger.info('学习模型导入完成', {
      capabilityCorrections: this.learningModel.capabilityCorrections.size,
      modelAge: this.learningModel.statistics.lastLearningTime,
    });
  }
  
  /**
   * 关闭学习引擎
   */
  async shutdown(): Promise<void> {
    logger.info('关闭基础学习引擎');
    
    try {
      // TODO: 保存学习模型和样本
      // await this.saveLearningModel();
      // await this.saveSamples();
      
      this.initialized = false;
      logger.info('基础学习引擎关闭完成');
      
    } catch (error) {
      logger.error('关闭学习引擎时发生错误', error as Error);
      throw error;
    }
  }
}

// 默认学习引擎实例
let defaultLearner: BasicLearningEngine | null = null;

/**
 * 获取默认学习引擎实例
 */
export function getLearner(config?: Partial<LearningEngineConfig>): BasicLearningEngine {
  if (!defaultLearner) {
    defaultLearner = new BasicLearningEngine(config);
  }
  return defaultLearner;
}

/**
 * 重新初始化学习引擎
 */
export function reinitializeLearner(config?: Partial<LearningEngineConfig>): BasicLearningEngine {
  defaultLearner = new BasicLearningEngine(config);
  return defaultLearner;
}

export default getLearner;