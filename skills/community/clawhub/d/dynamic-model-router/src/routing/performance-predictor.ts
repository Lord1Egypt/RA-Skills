/**
 * 性能预测器 - 智能预测模型执行性能
 * 
 * 基于历史数据、模型能力、任务复杂度等多因素预测：
 * 1. 响应时间（延迟）预测
 * 2. 成本效率计算和预测
 * 3. 成功率预估和风险分析
 * 4. 输出质量评分预测
 */

import { RouterLogger } from '../utils/logger.js';
import { 
  type ModelInfo, 
  type TaskDescription,
  type ProviderInfo 
} from '../core/types.js';
import type { 
  TaskAnalysisResult,
  HistoricalPerformance,
  RoutingContext,
  PredictedPerformance
} from './types.js';
import { RouterError } from '../core/types.js';

const logger = new RouterLogger({ module: 'performance-predictor' });

/**
 * 性能预测器配置
 */
export interface PerformancePredictorConfig {
  // 预测方法
  predictionMethod: 'rule_based' | 'historical' | 'hybrid';
  
  // 历史数据配置
  historicalData: {
    minSamples: number; // 最小样本数
    decayFactor: number; // 衰减因子（0-1）
    maxAgeDays: number; // 最大数据年龄（天）
  };
  
  // 规则配置
  ruleBased: {
    baseLatencyByModel: Map<string, number>; // 基础延迟（毫秒）
    latencyPerToken: Map<string, number>; // 每token延迟
    baseSuccessRate: Map<string, number>; // 基础成功率
  };
  
  // 成本计算配置
  costCalculation: {
    costPerToken: Map<string, number>; // 每token成本
    overheadCost: Map<string, number>; // 固定开销
  };
  
  // 质量预测配置
  qualityPrediction: {
    capabilityWeights: Map<string, number>; // 能力权重
    complexityPenalty: number; // 复杂度惩罚系数
  };
}

/**
 * 性能预测器主类
 */
export class PerformancePredictor {
  private config: PerformancePredictorConfig;
  private historicalData: HistoricalPerformance[];
  private initialized = false;
  
  constructor(config?: Partial<PerformancePredictorConfig>) {
    logger.info('初始化性能预测器');
    
    // 默认配置
    this.config = {
      predictionMethod: 'hybrid',
      historicalData: {
        minSamples: 10,
        decayFactor: 0.9,
        maxAgeDays: 30
      },
      ruleBased: {
        baseLatencyByModel: new Map(),
        latencyPerToken: new Map(),
        baseSuccessRate: new Map()
      },
      costCalculation: {
        costPerToken: new Map(),
        overheadCost: new Map()
      },
      qualityPrediction: {
        capabilityWeights: new Map(),
        complexityPenalty: 0.1
      },
      ...config
    };
    
    this.historicalData = [];
    
    // 初始化默认规则
    this.initializeDefaultRules();
    
    logger.info('性能预测器实例创建完成');
  }
  
  /**
   * 初始化默认规则
   */
  private initializeDefaultRules(): void {
    logger.debug('初始化默认性能规则');
    
    // 默认模型性能规则（基于公开数据和经验）
    const defaultRules = {
      // DeepSeek模型
      'deepseek-chat': {
        baseLatency: 3000, // 3秒基础延迟
        latencyPerToken: 0.05, // 每token 0.05毫秒
        baseSuccessRate: 0.95, // 95%基础成功率
        costPerToken: 0.00028, // 成本（单位）
        overheadCost: 0.001, // 固定开销
        capabilityWeight: 0.85 // 能力权重
      },
      'deepseek-reasoner': {
        baseLatency: 5000, // 5秒基础延迟（推理模型更慢）
        latencyPerToken: 0.08,
        baseSuccessRate: 0.90,
        costPerToken: 0.00028,
        overheadCost: 0.002,
        capabilityWeight: 0.95
      },
      // 添加更多模型的默认规则...
    };
    
    // 加载到配置
    for (const [modelId, rules] of Object.entries(defaultRules)) {
      this.config.ruleBased.baseLatencyByModel.set(modelId, rules.baseLatency);
      this.config.ruleBased.latencyPerToken.set(modelId, rules.latencyPerToken);
      this.config.ruleBased.baseSuccessRate.set(modelId, rules.baseSuccessRate);
      this.config.costCalculation.costPerToken.set(modelId, rules.costPerToken);
      this.config.costCalculation.overheadCost.set(modelId, rules.overheadCost);
      this.config.qualityPrediction.capabilityWeights.set(modelId, rules.capabilityWeight);
    }
    
    logger.debug(`已加载${Object.keys(defaultRules).length}个模型的默认规则`);
  }
  
  /**
   * 初始化预测器
   */
  async initialize(): Promise<void> {
    if (this.initialized) {
      logger.warn('预测器已经初始化');
      return;
    }
    
    try {
      logger.info('开始初始化性能预测器');
      
      // TODO: 从存储加载历史数据
      // await this.loadHistoricalData();
      
      // TODO: 训练预测模型（如果有足够数据）
      // if (this.historicalData.length >= this.config.historicalData.minSamples) {
      //   await this.trainPredictionModel();
      // }
      
      logger.info('性能预测器初始化完成');
      this.initialized = true;
      
    } catch (error) {
      logger.error('性能预测器初始化失败', error as Error);
      throw error;
    }
  }
  
  /**
   * 预测模型性能
   */
  async predictPerformance(
    task: TaskDescription,
    analysis: TaskAnalysisResult,
    model: ModelInfo,
    provider: ProviderInfo,
    context: RoutingContext
  ): Promise<PredictedPerformance> {
    if (!this.initialized) {
      await this.initialize();
    }
    
    const predictionId = `pred_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    const predictionLogger = new RouterLogger({ predictionId });
    
    try {
      predictionLogger.info('开始性能预测', {
        modelId: model.modelId,
        providerId: provider.id,
        taskId: task.id,
        taskComplexity: task.complexity,
        estimatedTokens: task.estimatedTokens
      });
      
      // 根据配置选择预测方法
      let prediction: PredictedPerformance;
      
      switch (this.config.predictionMethod) {
        case 'rule_based':
          prediction = this.predictByRules(task, analysis, model, provider, context);
          break;
          
        case 'historical':
          prediction = this.predictByHistory(task, analysis, model, provider, context);
          break;
          
        case 'hybrid':
        default:
          prediction = this.predictHybrid(task, analysis, model, provider, context);
          break;
      }
      
      // 添加元数据
      prediction.predictionId = predictionId;
      prediction.predictionMethod = this.config.predictionMethod;
      prediction.confidence = this.calculateConfidence(prediction, context);
      
      predictionLogger.info('性能预测完成', {
        expectedLatency: prediction.expectedLatency,
        expectedCost: prediction.expectedCost,
        expectedQuality: prediction.expectedQuality,
        successProbability: prediction.successProbability,
        confidence: prediction.confidence
      });
      
      return prediction;
      
    } catch (error) {
      predictionLogger.error('性能预测失败', error as Error);
      throw new RouterError(
        `性能预测失败: ${(error as Error).message}`,
        'PERFORMANCE_PREDICTION_FAILED',
        { taskId: task.id, modelId: model.modelId, error }
      );
    }
  }
  
  /**
   * 基于规则预测（默认方法）
   */
  private predictByRules(
    task: TaskDescription,
    analysis: TaskAnalysisResult,
    model: ModelInfo,
    _provider: ProviderInfo,
    context: RoutingContext
  ): PredictedPerformance {
    const modelId = model.modelId;
    
    // 获取模型规则
    const baseLatency = this.config.ruleBased.baseLatencyByModel.get(modelId) || 5000;
    const latencyPerToken = this.config.ruleBased.latencyPerToken.get(modelId) || 0.1;
    const baseSuccessRate = this.config.ruleBased.baseSuccessRate.get(modelId) || 0.85;
    const costPerToken = this.config.costCalculation.costPerToken.get(modelId) || 0.001;
    const overheadCost = this.config.costCalculation.overheadCost.get(modelId) || 0.005;
    const capabilityWeight = this.config.qualityPrediction.capabilityWeights.get(modelId) || 0.8;
    
    // 1. 延迟预测
    const tokenBasedLatency = task.estimatedTokens * latencyPerToken;
    const complexityFactor = 1 + (task.complexity === 'complex' ? 0.5 : 
                                 task.complexity === 'medium' ? 0.2 : 0);
    const loadFactor = 1 + (context.currentLoad.modelLoad.get(modelId) || 0);
    const networkFactor = 1 + (1 - (context.environment.networkQuality || 0.8));
    
    const expectedLatency = Math.round(
      (baseLatency + tokenBasedLatency) * 
      complexityFactor * 
      loadFactor * 
      networkFactor
    );
    
    // 2. 成本预测
    const tokenCost = task.estimatedTokens * costPerToken;
    const expectedCost = Math.round((tokenCost + overheadCost) * 1000) / 1000; // 保留3位小数
    
    // 3. 质量预测
    const capabilityScore = this.calculateCapabilityScore(model, analysis);
    const complexityPenalty = task.complexity === 'complex' ? this.config.qualityPrediction.complexityPenalty : 0;
    const expectedQuality = Math.max(0, Math.min(1, 
      capabilityWeight * capabilityScore - complexityPenalty
    ));
    
    // 4. 成功率预测
    const historicalSuccessRate = context.historicalPerformance.successRates.get(modelId) || baseSuccessRate;
    const recentErrors = context.currentLoad.recentErrors.get(modelId) || 0;
    const errorPenalty = recentErrors > 0 ? 0.1 * Math.min(recentErrors, 5) : 0; // 最多降低50%
    const successProbability = Math.max(0.1, Math.min(0.99, 
      historicalSuccessRate * (1 - errorPenalty)
    ));
    
    return {
      expectedLatency,
      expectedCost,
      expectedQuality,
      successProbability,
      predictionMethod: 'rule_based',
      confidence: 0.7, // 规则基础预测的置信度
      assumptions: [
        `基础延迟: ${baseLatency}ms`,
        `每token延迟: ${latencyPerToken}ms`,
        `复杂度因子: ${complexityFactor}`,
        `负载因子: ${loadFactor}`,
        `网络因子: ${networkFactor}`
      ]
    } as PredictedPerformance;
  }
  
  /**
   * 基于历史数据预测
   */
  private predictByHistory(
    task: TaskDescription,
    analysis: TaskAnalysisResult,
    model: ModelInfo,
    provider: ProviderInfo,
    context: RoutingContext
  ): PredictedPerformance {
    // TODO: 实现基于历史数据的预测
    // 需要从historicalData中查找相似任务的历史表现
    
    // 临时实现：回退到规则预测
    logger.warn('历史数据预测尚未实现，回退到规则预测');
    return this.predictByRules(task, analysis, model, provider, context);
  }
  
  /**
   * 混合预测（规则+历史）
   */
  private predictHybrid(
    task: TaskDescription,
    analysis: TaskAnalysisResult,
    model: ModelInfo,
    provider: ProviderInfo,
    context: RoutingContext
  ): PredictedPerformance {
    // 获取规则预测
    const rulePrediction = this.predictByRules(task, analysis, model, provider, context);
    
    // 如果有足够历史数据，进行历史预测并加权平均
    const hasHistoricalData = this.historicalData.length >= this.config.historicalData.minSamples;
    
    if (hasHistoricalData) {
      try {
        const historicalPrediction = this.predictByHistory(task, analysis, model, provider, context);
        
        // 加权平均（规则:历史 = 6:4）
        return {
          expectedLatency: Math.round(rulePrediction.expectedLatency * 0.6 + historicalPrediction.expectedLatency * 0.4),
          expectedCost: rulePrediction.expectedCost * 0.6 + historicalPrediction.expectedCost * 0.4,
          expectedQuality: rulePrediction.expectedQuality * 0.6 + historicalPrediction.expectedQuality * 0.4,
          successProbability: rulePrediction.successProbability * 0.6 + historicalPrediction.successProbability * 0.4,
          predictionMethod: 'hybrid',
          confidence: Math.max(rulePrediction.confidence || 0.7, historicalPrediction.confidence || 0.7),
          assumptions: [
            ...(rulePrediction.assumptions || []),
            ...(historicalPrediction.assumptions || []),
            '混合预测：规则(60%) + 历史(40%)'
          ]
        } as PredictedPerformance;
      } catch (error) {
        logger.warn('历史预测失败，使用规则预测', { error });
        return rulePrediction;
      }
    }
    
    // 没有足够历史数据，返回规则预测
    return rulePrediction;
  }
  
  /**
   * 计算能力匹配分数
   */
  private calculateCapabilityScore(model: ModelInfo, _analysis: TaskAnalysisResult): number {
    // TODO: 基于任务需求和模型能力计算匹配度
    
    // 简化实现：根据模型能力权重计算
    const modelCapabilities = model.capabilities || {};
    let totalCapability = 0;
    let count = 0;
    
    // 明确处理能力分数
    const capabilities = [
      modelCapabilities.coding,
      modelCapabilities.writing,
      modelCapabilities.analysis,
      modelCapabilities.translation,
      modelCapabilities.reasoning,
    ];
    
    for (const score of capabilities) {
      if (typeof score === 'number') {
        totalCapability += score;
        count++;
      }
    }
    
    return count > 0 ? totalCapability / count / 100 : 0.5; // 归一化到0-1
  }
  
  /**
   * 计算预测置信度
   */
  private calculateConfidence(prediction: PredictedPerformance, context: RoutingContext): number {
    let confidence = prediction.confidence || 0.7;
    
    // 基于历史数据量调整置信度
    const historicalSamples = this.historicalData.length;
    if (historicalSamples > 0) {
      const dataFactor = Math.min(1, historicalSamples / 100); // 最多100个样本
      confidence = confidence * 0.3 + dataFactor * 0.7;
    }
    
    // 基于网络质量调整
    const networkQuality = context.environment.networkQuality || 0.8;
    confidence = confidence * 0.8 + networkQuality * 0.2;
    
    return Math.max(0.1, Math.min(0.99, confidence));
  }
  
  /**
   * 记录实际性能（用于学习）
   */
  async recordActualPerformance(
    predictionId: string,
    actualPerformance: {
      actualLatency: number;
      actualCost: number;
      actualSuccess: boolean;
      actualQuality?: number;
      tokensUsed?: number;
      error?: string;
    },
    metadata: {
      taskId: string;
      modelId: string;
      providerId: string;
      timestamp: Date;
    }
  ): Promise<void> {
    try {
      logger.info('记录实际性能数据', {
        predictionId,
        taskId: metadata.taskId,
        modelId: metadata.modelId,
        actualLatency: actualPerformance.actualLatency,
        actualSuccess: actualPerformance.actualSuccess
      });
      
      // 创建历史记录
      // @ts-ignore - 变量声明但未使用
      const _historicalRecord: HistoricalPerformance = {
        id: `hist_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
        predictionId,
        taskId: metadata.taskId,
        modelId: metadata.modelId,
        providerId: metadata.providerId,
        
        // 预测值
        predicted: {
          latency: 0, // 需要从预测缓存中获取
          cost: 0,
          successProbability: 0,
          quality: 0
        },
        
        // 实际值
        actual: {
          latency: actualPerformance.actualLatency,
          cost: actualPerformance.actualCost,
          success: actualPerformance.actualSuccess,
          quality: actualPerformance.actualQuality,
          tokensUsed: actualPerformance.tokensUsed,
          error: actualPerformance.error
        },
        
        metadata: {
          ...metadata,
          recordedAt: new Date(),
          predictionMethod: 'unknown' // 需要从预测缓存中获取
        }
      };
      
      // TODO: 存储历史记录
      // this.historicalData.push(historicalRecord);
      
      // TODO: 如果数据太多，清理旧数据
      // this.cleanupOldData();
      
      // TODO: 触发学习更新（如果达到阈值）
      // if (this.historicalData.length % 10 === 0) {
      //   await this.updateLearningModel();
      // }
      
      logger.debug('实际性能数据记录完成');
      
    } catch (error) {
      logger.error('记录实际性能数据失败', error as Error);
      // 不抛出错误，避免影响主流程
    }
  }
  
  /**
   * 获取预测器状态
   */
  getStatus(): any {
    return {
      initialized: this.initialized,
      predictionMethod: this.config.predictionMethod,
      historicalDataCount: this.historicalData.length,
      config: {
        predictionMethod: this.config.predictionMethod,
        historicalData: this.config.historicalData,
        ruleBased: this.config.ruleBased,
        costCalculation: this.config.costCalculation,
        hasDefaultRules: this.config.ruleBased.baseLatencyByModel.size > 0
      }
    };
  }
  
  /**
   * 更新配置
   */
  updateConfig(updates: Partial<PerformancePredictorConfig>): PerformancePredictorConfig {
    logger.info('更新性能预测器配置', { updates });
    this.config = { ...this.config, ...updates };
    return this.config;
  }
  
  /**
   * 导出配置
   */
  exportConfig(): string {
    return JSON.stringify(this.config, null, 2);
  }
  
  /**
   * 关闭预测器
   */
  async shutdown(): Promise<void> {
    logger.info('关闭性能预测器');
    
    try {
      // TODO: 保存历史数据到存储
      // await this.saveHistoricalData();
      
      this.initialized = false;
      logger.info('性能预测器关闭完成');
      
    } catch (error) {
      logger.error('关闭性能预测器时发生错误', error as Error);
      throw error;
    }
  }
}

// 默认预测器实例
let defaultPredictor: PerformancePredictor | null = null;

/**
 * 获取默认预测器实例
 */
export function getPredictor(config?: Partial<PerformancePredictorConfig>): PerformancePredictor {
  if (!defaultPredictor) {
    defaultPredictor = new PerformancePredictor(config);
  }
  return defaultPredictor;
}

/**
 * 重新初始化预测器
 */
export function reinitializePredictor(config?: Partial<PerformancePredictorConfig>): PerformancePredictor {
  defaultPredictor = new PerformancePredictor(config);
  return defaultPredictor;
}

// 导出类型和接口
export type { PredictedPerformance, HistoricalPerformance } from './types.js';
export default getPredictor;