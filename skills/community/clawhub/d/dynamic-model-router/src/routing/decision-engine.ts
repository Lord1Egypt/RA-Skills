/**
 * 路由决策引擎 - 核心算法实现
 * 
 * 负责智能选择最优AI模型，考虑因素包括：
 * 1. 任务复杂度和需求
 * 2. 模型能力和特性
 * 3. 成本效率和性能
 * 4. 历史表现和可靠性
 * 5. 用户偏好和约束
 */

import { RouterLogger } from '../utils/logger.js';
import path from 'path';
import { 
  type RoutingRequest, 
  type RoutingResponse, 
  type RoutingDecision,
  type RoutingMetrics,
  type RoutingContext,
  type RoutingConstraints,
  type RoutingConfig,
  type TaskAnalysisResult,
  type IRoutingEngine,
  type EngineStatus,
  RoutingStrategy
} from './types.js';
import { PerformancePredictor, getPredictor } from './performance-predictor.js';
import { BasicLearningEngine, getLearner } from '../learning/basic-learner.js';
import { BasicStorage, getStorage } from '../storage/basic-storage.js';

import type { TaskDescription } from '../core/types.js';
import { RouterError } from '../core/types.js';

const logger = new RouterLogger({ module: 'decision-engine' });

/**
 * 路由决策引擎实现
 */
export class DecisionEngine implements IRoutingEngine {
  private config: RoutingConfig;
  private statistics: EngineStatus['statistics'];
  private performancePredictor: PerformancePredictor;
  private learningEngine: BasicLearningEngine;
  private storage: BasicStorage;
  private learningSamples: Array<{
    decisionId: string;
    features: Record<string, any>;
    predictedOutcome: any;
    actualOutcome?: any;
    timestamp: Date;
  }> = [];
  private maxLearningSamples: number = 1000;
  
  constructor(config?: Partial<RoutingConfig>) {
    this.config = {
      defaultStrategy: RoutingStrategy.BALANCED,
      constraints: {},
      weights: {
        cost: 0.3,
        latency: 0.2,
        reliability: 0.25,
        quality: 0.15,
        capabilityMatch: 0.1,
      },
      thresholds: {
        minSuccessRate: 0.8,
        maxAcceptableLatency: 30000, // 30秒
        maxAcceptableCost: 100,
        minCapabilityMatch: 0.6,
      },
      enableTaskSplitting: true,
      enableParallelExecution: false,
      enableFallbackRouting: true,
      learningEnabled: true,
      fallbackStrategy: {
        maxRetries: 3,
        fallbackModels: [],
        escalationPath: [],
      },
      ...config,
    };
    
    this.statistics = {
      totalDecisions: 0,
      successfulDecisions: 0,
      averageDecisionTime: 0,
      learningSamples: 0,
    };
    
    // 初始化性能预测器
    this.performancePredictor = getPredictor();
    this.performancePredictor.initialize().catch(error => {
      logger.warn('性能预测器初始化失败，将使用简化预测', { error: error.message });
    });
    
    // 初始化学习引擎
    this.learningEngine = getLearner({
      enabled: this.config.learningEnabled,
      minSamples: 10,
      maxSamples: 1000,
    });
    this.learningEngine.initialize().catch(error => {
      logger.warn('学习引擎初始化失败，学习功能将不可用', { error: error.message });
    });
    
    // 初始化存储模块
    this.storage = getStorage({
      storagePath: path.join(process.cwd(), '.dynamic-router-storage'),
      maxTotalSize: 100 * 1024 * 1024, // 100MB
    });
    this.storage.initialize().catch(error => {
      logger.warn('存储模块初始化失败，持久化功能将不可用', { error: error.message });
    });
    
    logger.info('路由决策引擎初始化完成', {
      defaultStrategy: this.config.defaultStrategy,
      learningEnabled: this.config.learningEnabled,
      modules: ['performance-predictor', 'learning-engine', 'storage'],
    });
  }
  
  /**
   * 核心路由方法
   */
  async route(request: RoutingRequest): Promise<RoutingResponse> {
    const startTime = Date.now();
    const decisionId = `decision_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    
    logger.debug('开始路由决策', {
      decisionId,
      taskId: request.task.id,
      strategy: request.strategy || this.config.defaultStrategy,
    });
    
    try {
      // 1. 验证输入
      this.validateRoutingRequest(request);
      
      // 2. 分析任务
      const taskAnalysis = await this.analyzeTask(request.task);
      
      // 3. 获取可用模型信息（从上下文或外部传入）
      // 注意：这里假设availableModels和availableProviders已提供
      // 实际实现中需要从外部获取
      
      // 4. 计算模型评分
      const modelScores = await this.calculateModelScores(
        request.task,
        taskAnalysis,
        request.context,
        request.constraints
      );
      
      // 5. 应用路由策略
      const selectedModel = this.applyRoutingStrategy(
        modelScores,
        request.strategy || this.config.defaultStrategy,
        request.constraints
      );
      
      // 6. 构建决策结果
      const decision = await this.buildRoutingDecision(
        decisionId,
        request,
        taskAnalysis,
        modelScores,
        selectedModel
      );
      
      // 7. 构建执行指令
      const executionInstructions = this.buildExecutionInstructions(
        selectedModel,
        request,
        decision
      );
      
      // 8. 计算指标
      const metrics = this.calculateRoutingMetrics(
        startTime,
        modelScores,
        decision
      );
      
      // 9. 构建响应
      const response: RoutingResponse = {
        decision,
        metrics,
        executionInstructions,
        learningData: {
          features: this.extractLearningFeatures(request, taskAnalysis, modelScores),
          predictedOutcome: {
            expectedLatency: decision.predictedPerformance.expectedLatency,
            expectedCost: decision.predictedPerformance.expectedCost,
            expectedQuality: decision.predictedPerformance.expectedQuality,
          },
        },
      };
      
      // 10. 更新统计
      this.updateStatistics(true, Date.now() - startTime);
      
      logger.info('路由决策完成', {
        decisionId,
        selectedModel: `${selectedModel.providerId}/${selectedModel.modelId}`,
        decisionTime: metrics.decisionTime,
        confidence: metrics.decisionQuality.confidence,
      });
      
      return response;
      
    } catch (error) {
      const decisionTime = Date.now() - startTime;
      this.updateStatistics(false, decisionTime);
      
      logger.error('路由决策失败', error as Error, { decisionId });
      
      // 尝试回退策略
      if (this.config.enableFallbackRouting) {
        return await this.applyFallbackStrategy(request, error as Error, decisionId);
      }
      
      throw new RouterError(
        `路由决策失败: ${(error as Error).message}`,
        'ROUTING_DECISION_FAILED',
        { decisionId }
      );
    }
  }
  
  /**
   * 记录实际执行结果用于学习
   */
  async recordActualOutcome(
    decisionId: string,
    actualOutcome: any, // ModelResponse简化
    actualPerformance?: {
      latency: number;
      cost: number;
      success: boolean;
      quality?: number;
      tokensUsed?: number;
    }
  ): Promise<void> {
    if (!this.config.learningEnabled || !this.learningEngine) {
      logger.debug('学习功能被禁用或未初始化，跳过记录实际结果');
      return;
    }
    
    try {
      logger.debug('记录实际执行结果用于学习', { decisionId });
      
      // 需要从存储中加载决策记录（这里简化）
      // 实际实现中应该从存储或缓存中获取决策上下文
      
      // 调用学习引擎记录结果
      await this.learningEngine.recordDecisionOutcome(
        {} as any, // 决策对象（需要从存储加载）
        {} as any, // 指标对象
        actualOutcome,
        actualPerformance
      );
      
      // 保存历史性能记录到存储
      if (this.storage && actualPerformance) {
        await this.storage.saveHistoricalPerformance(
          {
            decisionId,
            actualPerformance,
            actualOutcome,
          },
          {
            timestamp: new Date(),
          }
        );
      }
      
      logger.debug('实际执行结果记录完成', { decisionId });
      
    } catch (error) {
      logger.error('记录实际执行结果失败', error as Error, { decisionId });
      // 不抛出错误，避免影响主流程
    }
  }
  
  /**
   * 批量路由
   */
  async batchRoute(requests: RoutingRequest[]): Promise<RoutingResponse[]> {
    logger.debug('开始批量路由', { requestCount: requests.length });
    
    const startTime = Date.now();
    const results: RoutingResponse[] = [];
    
    // 简单实现：顺序处理每个请求
    // 未来可以优化为并行处理
    for (const request of requests) {
      try {
        const result = await this.route(request);
        results.push(result);
      } catch (error) {
        logger.error('批量路由中单个请求失败', error as Error);
        
        // 创建失败响应
        const errorResponse = this.createErrorResponse(request, error as Error);
        results.push(errorResponse);
      }
    }
    
    const totalTime = Date.now() - startTime;
    logger.info('批量路由完成', {
      requestCount: requests.length,
      successCount: results.filter(r => r.decision.selectedModel !== undefined).length,
      totalTime,
    });
    
    return results;
  }
  
  /**
   * 分析任务
   */
  async analyzeTask(task: TaskDescription): Promise<TaskAnalysisResult> {
    const startTime = Date.now();
    
    logger.debug('开始任务分析', { taskId: task.id });
    
    try {
      // 1. 基础特征提取
      const characteristics = await this.extractTaskCharacteristics(task);
      
      // 2. 能力需求分析
      const requiredCapabilities = await this.analyzeRequiredCapabilities(task, characteristics);
      
      // 3. 质量要求分析
      const qualityRequirements = await this.analyzeQualityRequirements(task, characteristics);
      
      // 4. 拆分潜力分析
      const splittingPotential = await this.analyzeSplittingPotential(task, characteristics);
      
      const analysisResult: TaskAnalysisResult = {
        taskId: task.id,
        characteristics,
        requiredCapabilities,
        qualityRequirements,
        splittingPotential,
      };
      
      const analysisTime = Date.now() - startTime;
      logger.debug('任务分析完成', {
        taskId: task.id,
        complexity: characteristics.complexity,
        analysisTime,
      });
      
      return analysisResult;
      
    } catch (error) {
      logger.error('任务分析失败', error as Error, { taskId: task.id });
      
      // 返回默认分析结果
      return this.createDefaultTaskAnalysis(task);
    }
  }
  
  /**
   * 从结果中学习
   */
  async learnFromOutcome(decisionId: string, actualOutcome: any): Promise<void> {
    if (!this.config.learningEnabled) {
      return;
    }
    
    logger.debug('从决策结果中学习', { decisionId });
    
    try {
      // 查找对应的学习样本
      const sampleIndex = this.learningSamples.findIndex(s => s.decisionId === decisionId);
      
      if (sampleIndex === -1) {
        logger.warn('找不到对应的学习样本', { decisionId });
        return;
      }
      
      // 更新样本的实际结果
      this.learningSamples[sampleIndex].actualOutcome = actualOutcome;
      
      // 这里可以添加实际的学习逻辑，例如：
      // 1. 比较预测结果和实际结果
      // 2. 调整权重和阈值
      // 3. 更新模型性能认知
      
      this.statistics.learningSamples++;
      
      logger.debug('学习完成', { 
        decisionId,
        learningSamples: this.statistics.learningSamples,
      });
      
      // 如果学习样本过多，清理旧样本
      if (this.learningSamples.length > this.maxLearningSamples) {
        this.learningSamples = this.learningSamples.slice(-this.maxLearningSamples);
        logger.debug('清理旧学习样本', { remaining: this.learningSamples.length });
      }
      
    } catch (error) {
      logger.error('学习过程失败', error as Error, { decisionId });
    }
  }
  
  /**
   * 获取引擎状态
   */
  getEngineStatus(): EngineStatus {
    return {
      isInitialized: true,
      config: this.config,
      statistics: this.statistics,
      health: {
        memoryUsage: this.calculateMemoryUsage(),
        lastDecisionTime: this.statistics.averageDecisionTime,
        errorRate: this.calculateErrorRate(),
      },
    };
  }
  
  /**
   * 获取配置
   */
  getConfig(): RoutingConfig {
    return { ...this.config };
  }
  
  /**
   * 更新配置
   */
  updateConfig(config: Partial<RoutingConfig>): void {
    this.config = { ...this.config, ...config };
    logger.info('路由配置更新', { updates: config });
  }
  
  // ============== 私有方法 ==============
  
  /**
   * 验证路由请求
   */
  private validateRoutingRequest(request: RoutingRequest): void {
    if (!request.task) {
      throw new RouterError('任务描述不能为空', 'INVALID_REQUEST');
    }
    
    if (!request.task.id || !request.task.content) {
      throw new RouterError('任务ID和内容不能为空', 'INVALID_REQUEST');
    }
    
    logger.debug('路由请求验证通过', { taskId: request.task.id });
  }
  
  /**
   * 计算模型评分
   */
  private async calculateModelScores(
    task: TaskDescription,
    analysis: TaskAnalysisResult,
    context?: RoutingContext,
    constraints?: RoutingConstraints
  ): Promise<RoutingMetrics['modelScores']> {
    // 这里简化实现，返回模拟评分
    // 实际实现中需要：
    // 1. 获取可用模型列表
    // 2. 计算每个模型的各项评分
    // 3. 应用约束过滤
    // 4. 计算加权总分
    
    logger.debug('开始计算模型评分', { taskId: task.id });
    
    // 模拟数据 - 实际应从外部获取
    const mockModels: Array<{
      modelId: string;
      providerId: string;
      capabilities: string[];
      costPerToken: number;
      avgLatency: number;
      successRate: number;
      contextWindow: number;
    }> = [
      {
        modelId: 'deepseek-chat',
        providerId: 'deepseek',
        capabilities: ['chat', 'general', 'analysis'],
        costPerToken: 0.00028,
        avgLatency: 1500,
        successRate: 0.95,
        contextWindow: 128000,
      },
      {
        modelId: 'deepseek-reasoner',
        providerId: 'deepseek',
        capabilities: ['chat', 'reasoning', 'analysis', 'coding'],
        costPerToken: 0.00042,
        avgLatency: 3000,
        successRate: 0.92,
        contextWindow: 128000,
      },
      {
        modelId: 'gpt-4o',
        providerId: 'openai',
        capabilities: ['chat', 'analysis', 'coding', 'creative'],
        costPerToken: 0.005,
        avgLatency: 2500,
        successRate: 0.98,
        contextWindow: 128000,
      },
    ];
    
    const scores: RoutingMetrics['modelScores'] = [];
    
    for (const model of mockModels) {
      // 计算各项评分
      const capabilityScore = this.calculateCapabilityScore(model, analysis);
      const costScore = this.calculateCostScore(model, task);
      const performanceScore = this.calculatePerformanceScore(model, context);
      const reliabilityScore = model.successRate;
      const loadScore = context?.currentLoad?.modelLoad?.get(model.modelId) || 0.5;
      
      // 计算加权总分
      const totalScore = (
        capabilityScore * this.config.weights.capabilityMatch +
        costScore * this.config.weights.cost +
        performanceScore * this.config.weights.latency +
        reliabilityScore * this.config.weights.reliability +
        (1 - loadScore) * 0.1 // 负载越低越好
      );
      
      // 检查约束
      const constraintsMet = this.checkConstraints(model, constraints);
      const constraintViolations = constraintsMet ? [] : ['未通过约束检查'];
      
      scores.push({
        modelId: model.modelId,
        providerId: model.providerId,
        scores: {
          cost: costScore,
          capability: capabilityScore,
          performance: performanceScore,
          reliability: reliabilityScore,
          load: loadScore,
        },
        totalScore,
        constraintsMet,
        constraintViolations,
      });
    }
    
    // 按总分排序
    scores.sort((a, b) => b.totalScore - a.totalScore);
    
    logger.debug('模型评分计算完成', {
      taskId: task.id,
      modelCount: scores.length,
      topScore: scores[0]?.totalScore,
    });
    
    return scores;
  }
  
  /**
   * 计算能力匹配度
   */
  private calculateCapabilityScore(
    model: any,
    analysis: TaskAnalysisResult
  ): number {
    if (!analysis.requiredCapabilities || analysis.requiredCapabilities.length === 0) {
      return 0.8; // 默认分数
    }
    
    let totalImportance = 0;
    let matchedImportance = 0;
    
    for (const requirement of analysis.requiredCapabilities) {
      totalImportance += requirement.importance;
      
      if (model.capabilities.includes(requirement.capability)) {
        matchedImportance += requirement.importance;
      }
    }
    
    return totalImportance > 0 ? matchedImportance / totalImportance : 0.8;
  }
  
  /**
   * 计算成本评分（成本越低分数越高）
   */
  private calculateCostScore(model: any, task: TaskDescription): number {
    // 简化计算：基于token成本
    const estimatedTokens = task.estimatedTokens || 1000;
    const estimatedCost = estimatedTokens * model.costPerToken;
    
    // 成本越低分数越高，使用指数衰减
    const baseScore = Math.exp(-estimatedCost * 10);
    return Math.max(0.1, Math.min(1.0, baseScore));
  }
  
  /**
   * 计算性能评分
   */
  private calculatePerformanceScore(model: any, context?: RoutingContext): number {
    // 基于延迟的评分（延迟越低分数越高）
    const baseLatency = model.avgLatency;
    const networkFactor = context?.environment?.networkQuality || 0.8;
    
    // 归一化延迟评分
    const maxAcceptableLatency = this.config.thresholds.maxAcceptableLatency;
    const latencyScore = 1 - Math.min(baseLatency / maxAcceptableLatency, 1);
    
    return latencyScore * networkFactor;
  }
  
  /**
   * 检查约束
   */
  private checkConstraints(model: any, constraints?: RoutingConstraints): boolean {
    if (!constraints) {
      return true;
    }
    
    // 检查排除的模型
    if (constraints.excludedModels?.includes(model.modelId)) {
      return false;
    }
    
    // 检查偏好的供应商
    if (constraints.preferredProviders && constraints.preferredProviders.length > 0) {
      if (!constraints.preferredProviders.includes(model.providerId)) {
        return false;
      }
    }
    
    // 检查所需能力
    if (constraints.requiredCapabilities && constraints.requiredCapabilities.length > 0) {
      for (const capability of constraints.requiredCapabilities) {
        if (!model.capabilities.includes(capability)) {
          return false;
        }
      }
    }
    
    return true;
  }
  
  /**
   * 应用路由策略
   */
  private applyRoutingStrategy(
    scores: RoutingMetrics['modelScores'],
    strategy: RoutingStrategy,
    _constraints?: RoutingConstraints
  ): { modelId: string; providerId: string } {
    // 过滤通过约束的模型
    const eligibleScores = scores.filter(score => score.constraintsMet);
    
    if (eligibleScores.length === 0) {
      throw new RouterError('没有符合约束的可用模型', 'NO_ELIGIBLE_MODELS');
    }
    
    let selectedIndex = 0;
    
    switch (strategy) {
      case RoutingStrategy.COST_OPTIMIZED:
        // 成本优化：选择成本评分最高的
        selectedIndex = eligibleScores.reduce(
          (best, current, index) => 
            current.scores.cost > eligibleScores[best].scores.cost ? index : best,
          0
        );
        break;
        
      case RoutingStrategy.PERFORMANCE_OPTIMIZED:
        // 性能优化：选择性能评分最高的
        selectedIndex = eligibleScores.reduce(
          (best, current, index) => 
            current.scores.performance > eligibleScores[best].scores.performance ? index : best,
          0
        );
        break;
        
      case RoutingStrategy.RELIABILITY_FIRST:
        // 可靠性优先：选择可靠性评分最高的
        selectedIndex = eligibleScores.reduce(
          (best, current, index) => 
            current.scores.reliability > eligibleScores[best].scores.reliability ? index : best,
          0
        );
        break;
        
      case RoutingStrategy.QUALITY_FIRST:
        // 质量优先：选择能力匹配度最高的
        selectedIndex = eligibleScores.reduce(
          (best, current, index) => 
            current.scores.capability > eligibleScores[best].scores.capability ? index : best,
          0
        );
        break;
        
      case RoutingStrategy.SPEED_FIRST:
        // 速度优先：综合考虑性能和负载
        selectedIndex = eligibleScores.reduce(
          (best, current, index) => {
            const currentSpeedScore = current.scores.performance * (1 - current.scores.load);
            const bestSpeedScore = eligibleScores[best].scores.performance * (1 - eligibleScores[best].scores.load);
            return currentSpeedScore > bestSpeedScore ? index : best;
          },
          0
        );
        break;
        
      case RoutingStrategy.BALANCED:
      default:
        // 平衡策略：选择总分最高的（默认）
        selectedIndex = 0; // 已经按总分排序
        break;
    }
    
    const selected = eligibleScores[selectedIndex];
    
    logger.debug('应用路由策略', {
      strategy,
      selectedModel: `${selected.providerId}/${selected.modelId}`,
      totalScore: selected.totalScore,
      eligibleCount: eligibleScores.length,
    });
    
    return {
      modelId: selected.modelId,
      providerId: selected.providerId,
    };
  }
  
  /**
   * 构建路由决策
   */
  private async buildRoutingDecision(
    decisionId: string,
    request: RoutingRequest,
    analysis: TaskAnalysisResult,
    scores: RoutingMetrics['modelScores'],
    selectedModel: { modelId: string; providerId: string }
  ): Promise<RoutingDecision> {
    const selectedScore = scores.find(s => 
      s.modelId === selectedModel.modelId && s.providerId === selectedModel.providerId
    );
    
    if (!selectedScore) {
      throw new RouterError('找不到选中的模型评分', 'INTERNAL_ERROR');
    }
    
    // 构建决策理由
    const reasoning = this.buildRoutingReasoning(selectedScore, analysis);
    
    // 构建性能预测
    const predictedPerformance = await this.predictPerformance(
      selectedScore, 
      request.task,
      analysis,
      request.context
    );
    
    // 构建替代选项（排除已选模型）
    const alternatives = scores
      .filter(s => !(s.modelId === selectedModel.modelId && s.providerId === selectedModel.providerId))
      .slice(0, 3) // 最多3个替代选项
      .map(score => ({
        model: { id: score.modelId, name: score.modelId } as any, // 简化
        provider: { id: score.providerId, name: score.providerId } as any, // 简化
        score: score.totalScore,
        reason: this.getAlternativeReason(score),
      }));
    
    // 检查是否需要任务拆分
    const splitRecommendation = this.checkTaskSplitting(analysis, selectedScore);
    
    return {
      decisionId,
      timestamp: new Date(),
      task: request.task,
      availableModels: [], // 简化
      availableProviders: [], // 简化
      selectedModel: { 
        modelId: selectedModel.modelId, 
        provider: selectedModel.providerId,
        capabilities: { coding: 0, writing: 0, analysis: 0, translation: 0, reasoning: 0 },
        costPerToken: 0.001,
        avgResponseTime: 1000,
        successRate: 0.95,
        languageSupport: ['en', 'zh'],
        lastUpdated: new Date()
      } as any,
      selectedProvider: { 
        id: selectedModel.providerId, 
        name: selectedModel.providerId,
        baseUrl: '',
        models: [selectedModel.modelId],
        enabled: true
      } as any,
      reasoning,
      predictedPerformance,
      alternatives,
      splitRecommendation,
    };
  }
  
  /**
   * 构建路由理由
   */
  private buildRoutingReasoning(
    selectedScore: RoutingMetrics['modelScores'][0],
    analysis: TaskAnalysisResult
  ): any {
    const primaryFactors: Array<{ factor: string; weight: number; explanation: string }> = [];
    
    // 添加主要因素
    if (selectedScore.scores.capability > 0.8) {
      primaryFactors.push({
        factor: '能力匹配',
        weight: this.config.weights.capabilityMatch,
        explanation: `模型能力与任务需求高度匹配 (${(selectedScore.scores.capability * 100).toFixed(1)}%)`,
      });
    }
    
    if (selectedScore.scores.cost > 0.7) {
      primaryFactors.push({
        factor: '成本效率',
        weight: this.config.weights.cost,
        explanation: `成本效率较高 (${(selectedScore.scores.cost * 100).toFixed(1)}%)`,
      });
    }
    
    if (selectedScore.scores.reliability > 0.9) {
      primaryFactors.push({
        factor: '可靠性',
        weight: this.config.weights.reliability,
        explanation: `历史可靠性良好 (${(selectedScore.scores.reliability * 100).toFixed(1)}%)`,
      });
    }
    
    // 能力匹配分析
    const modelCapabilities = analysis.requiredCapabilities.map(req => ({
      capability: req.capability,
      matchScore: selectedScore.scores.capability,
      required: req.importance > 0.7,
    }));
    
    return {
      primaryFactors,
      modelCapabilities,
      costConsiderations: {
        costScore: selectedScore.scores.cost,
        budgetConstraint: true,
        costEfficiency: selectedScore.scores.cost,
      },
      performanceHistory: {
        successRate: selectedScore.scores.reliability,
        avgLatency: 0, // 需要实际数据
        reliabilityScore: selectedScore.scores.reliability,
      },
      complexityAnalysis: {
        taskComplexity: analysis.characteristics.complexity,
        modelAdequacy: selectedScore.scores.capability * 10,
        complexityMatch: selectedScore.scores.capability,
      },
    };
  }
  
  /**
   * 预测性能
   */
  private async predictPerformance(
    selectedScore: RoutingMetrics['modelScores'][0],
    task: TaskDescription,
    analysis?: TaskAnalysisResult,
    context?: RoutingContext
  ): Promise<RoutingDecision['predictedPerformance']> {
    try {
      // 尝试使用性能预测器
      if (this.performancePredictor) {
        // 构建简化的模型和提供者信息对象
        const modelInfo: any = {
          modelId: selectedScore.modelId,
          capabilities: {
            coding: selectedScore.scores.capability * 100,
            writing: selectedScore.scores.capability * 100,
            analysis: selectedScore.scores.capability * 100,
            translation: 70, // 默认值
            reasoning: selectedScore.scores.capability * 100,
          },
          costPerToken: 0.00028, // 默认成本
          avgResponseTime: 3000, // 默认响应时间
          successRate: selectedScore.scores.reliability,
          languageSupport: ['zh', 'en'],
          lastUpdated: new Date(),
        };
        
        const providerInfo: any = {
          id: selectedScore.providerId,
          name: selectedScore.providerId,
          baseUrl: '', // 占位符
          models: [selectedScore.modelId],
          enabled: true,
        };
        
        // 使用性能预测器进行预测
        const prediction = await this.performancePredictor.predictPerformance(
          task,
          analysis || {
            taskId: task.id,
            characteristics: {
              complexity: 5,
              length: task.content.length,
              tokenEstimate: task.estimatedTokens || 1000,
              contentType: ['text'],
              technicalRequirements: [],
            },
            requiredCapabilities: [],
            qualityRequirements: {
              accuracy: 0.8,
              creativity: 0.5,
              thoroughness: 0.7,
              speed: 0.6,
            },
            splittingPotential: {
              canSplit: false,
            },
          },
          modelInfo,
          providerInfo,
          context || {
            currentLoad: {
              providerLoad: new Map(),
              modelLoad: new Map(),
              recentErrors: new Map(),
            },
            historicalPerformance: {
              successRates: new Map([[selectedScore.modelId, selectedScore.scores.reliability]]),
              averageLatencies: new Map(),
              costEfficiency: new Map(),
            },
            environment: {
              timeOfDay: new Date().getHours().toString(),
              networkQuality: 0.9,
              systemLoad: 0.5,
            },
            userPreferences: {
              preferredModels: [],
              avoidedModels: [],
              qualityImportance: 0.7,
              speedImportance: 0.6,
              costSensitivity: 0.5,
            },
          }
        );
        
        // 应用学习校正
        let correctedPrediction = prediction;
        if (this.learningEngine) {
          try {
            correctedPrediction = this.learningEngine.applyCorrections(
              selectedScore.modelId,
              prediction
            );
          } catch (error) {
            logger.warn('应用学习校正失败，使用原始预测', {
              modelId: selectedScore.modelId,
              error: (error as Error).message,
            });
          }
        }
        
        return {
          expectedLatency: correctedPrediction.expectedLatency,
          expectedCost: correctedPrediction.expectedCost,
          expectedQuality: correctedPrediction.expectedQuality,
          successProbability: correctedPrediction.successProbability,
        };
      }
    } catch (error) {
      logger.warn('性能预测器失败，使用简化预测逻辑', { 
        error: (error as Error).message,
        modelId: selectedScore.modelId,
      });
    }
    
    // 回退到简化预测逻辑
    const estimatedTokens = task.estimatedTokens || 1000;
    
    const fallbackPrediction = {
      expectedLatency: 2000 + estimatedTokens * 0.1, // 基础延迟 + token相关延迟
      expectedCost: estimatedTokens * 0.0003, // 估算成本
      expectedQuality: selectedScore.scores.capability * 0.9 + selectedScore.scores.reliability * 0.1,
      successProbability: selectedScore.scores.reliability * 0.95,
    };
    
    // 应用学习校正
    let correctedPrediction = fallbackPrediction;
    if (this.learningEngine) {
      try {
        correctedPrediction = this.learningEngine.applyCorrections(
          selectedScore.modelId,
          fallbackPrediction
        );
      } catch (error) {
        logger.warn('应用学习校正失败，使用原始预测', {
          modelId: selectedScore.modelId,
          error: (error as Error).message,
        });
      }
    }
    
    return correctedPrediction;
  }
  
  /**
   * 获取替代选项理由
   */
  private getAlternativeReason(score: RoutingMetrics['modelScores'][0]): string {
    const strengths: string[] = [];
    
    if (score.scores.capability > 0.8) strengths.push('能力匹配度高');
    if (score.scores.cost > 0.8) strengths.push('成本效率高');
    if (score.scores.reliability > 0.9) strengths.push('可靠性好');
    if (score.scores.performance > 0.8) strengths.push('性能优秀');
    
    return strengths.length > 0 
      ? `优势: ${strengths.join(', ')}`
      : `综合评分: ${(score.totalScore * 100).toFixed(1)}%`;
  }
  
  /**
   * 检查任务拆分
   */
  private checkTaskSplitting(
    analysis: TaskAnalysisResult,
    selectedScore: RoutingMetrics['modelScores'][0]
  ): RoutingDecision['splitRecommendation'] {
    if (!this.config.enableTaskSplitting) {
      return { shouldSplit: false };
    }
    
    // 简化逻辑：复杂任务且能力匹配度不足时建议拆分
    const shouldSplit = analysis.characteristics.complexity > 7 && selectedScore.scores.capability < 0.7;
    
    if (!shouldSplit) {
      return { shouldSplit: false };
    }
    
    return {
      shouldSplit: true,
      reason: `任务复杂度较高(${analysis.characteristics.complexity}/10)且当前模型能力匹配度不足(${(selectedScore.scores.capability * 100).toFixed(1)}%)`,
      splitPlan: {
        subTasks: [
          {
            id: 'subtask_1',
            description: '分析任务核心需求',
            complexity: 5,
            requiredCapabilities: ['analysis'],
            recommendedModel: { id: 'deepseek-reasoner', name: 'DeepSeek Reasoner' } as any,
          },
          {
            id: 'subtask_2',
            description: '生成详细解决方案',
            complexity: 7,
            requiredCapabilities: ['generation', 'creative'],
            recommendedModel: { id: 'gpt-4o', name: 'GPT-4o' } as any,
          },
        ],
        executionStrategy: 'sequential',
        estimatedTotalTime: 10000,
        estimatedTotalCost: 0.05,
        coordinationRequirements: {
          needsContextSharing: true,
          needsResultAggregation: true,
          needsConsistencyCheck: true,
        },
      },
    };
  }
  
  /**
   * 构建执行指令
   */
  private buildExecutionInstructions(
    selectedModel: { modelId: string; providerId: string },
    request: RoutingRequest,
    decision: RoutingDecision
  ): RoutingResponse['executionInstructions'] {
    return {
      modelId: selectedModel.modelId,
      providerId: selectedModel.providerId,
      requestConfig: {
        timeout: 60000, // 60秒超时
        maxTokens: request.task.estimatedTokens ? Math.min(request.task.estimatedTokens * 2, 8192) : 4096,
        temperature: 0.7,
      },
      monitoring: {
        trackLatency: true,
        trackSuccess: true,
        trackQuality: decision.predictedPerformance.expectedQuality > 0.8,
      },
    };
  }
  
  /**
   * 计算路由指标
   */
  private calculateRoutingMetrics(
    startTime: number,
    scores: RoutingMetrics['modelScores'],
    decision: RoutingDecision
  ): RoutingMetrics {
    const decisionTime = Date.now() - startTime;
    
    // 计算决策质量
    const topScores = scores.slice(0, 3).map(s => s.totalScore);
    const scoreSpread = topScores.length > 1 
      ? (topScores[0] - topScores[1]) / topScores[0]
      : 1.0;
    
    const confidence = Math.min(0.95, 0.7 + scoreSpread * 0.3);
    const uncertainty = 1 - confidence;
    
    return {
      decisionTime,
      modelScores: scores,
      decisionQuality: {
        confidence,
        uncertainty,
        alternativesCount: decision.alternatives.length,
      },
    };
  }
  
  /**
   * 提取学习特征
   */
  private extractLearningFeatures(
    request: RoutingRequest,
    analysis: TaskAnalysisResult,
    scores: RoutingMetrics['modelScores']
  ): Record<string, any> {
    return {
      taskComplexity: analysis.characteristics.complexity,
      taskLength: request.task.content.length,
      requiredCapabilitiesCount: analysis.requiredCapabilities.length,
      modelCount: scores.length,
      topScore: scores[0]?.totalScore || 0,
      scoreSpread: scores.length > 1 ? scores[0].totalScore - scores[1].totalScore : 0,
      strategy: request.strategy || this.config.defaultStrategy,
      timestamp: new Date().toISOString(),
    };
  }
  
  /**
   * 更新统计信息
   */
  private updateStatistics(success: boolean, decisionTime: number): void {
    this.statistics.totalDecisions++;
    
    if (success) {
      this.statistics.successfulDecisions++;
    }
    
    // 更新平均决策时间（移动平均）
    const alpha = 0.1; // 平滑系数
    this.statistics.averageDecisionTime = 
      this.statistics.averageDecisionTime * (1 - alpha) + decisionTime * alpha;
  }
  
  /**
   * 应用回退策略
   */
  private async applyFallbackStrategy(
    request: RoutingRequest,
    error: Error,
    decisionId: string
  ): Promise<RoutingResponse> {
    logger.warn('应用回退策略', { decisionId, error: error.message });
    
    // 简化回退策略：选择默认模型
    const fallbackModel = {
      modelId: 'deepseek-chat',
      providerId: 'deepseek',
    };
    
    // 构建简化的决策
    const decision: RoutingDecision = {
      decisionId: `${decisionId}_fallback`,
      timestamp: new Date(),
      task: request.task,
      availableModels: [],
      availableProviders: [],
      selectedModel: { id: fallbackModel.modelId, name: fallbackModel.modelId } as any,
      selectedProvider: { id: fallbackModel.providerId, name: fallbackModel.providerId } as any,
      reasoning: {
        primaryFactors: [{ factor: '回退策略', weight: 1, explanation: '主路由失败，使用回退模型' }],
        modelCapabilities: [],
        costConsiderations: { costScore: 0.5, budgetConstraint: false, costEfficiency: 0.5 },
        performanceHistory: { successRate: 0.8, avgLatency: 2000, reliabilityScore: 0.8 },
        complexityAnalysis: { taskComplexity: 5, modelAdequacy: 5, complexityMatch: 0.5 },
      },
      predictedPerformance: {
        expectedLatency: 3000,
        expectedCost: 0.01,
        expectedQuality: 0.7,
        successProbability: 0.8,
      },
      alternatives: [],
    };
    
    return {
      decision,
      metrics: {
        decisionTime: 100,
        modelScores: [],
        decisionQuality: {
          confidence: 0.5,
          uncertainty: 0.5,
          alternativesCount: 0,
        },
      },
      executionInstructions: {
        modelId: fallbackModel.modelId,
        providerId: fallbackModel.providerId,
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
    };
  }
  
  /**
   * 创建错误响应
   */
  private createErrorResponse(request: RoutingRequest, error: Error): RoutingResponse {
    const decisionId = `error_${Date.now()}`;
    
    return {
      decision: {
        decisionId,
        timestamp: new Date(),
        task: request.task,
        availableModels: [],
        availableProviders: [],
        selectedModel: undefined as any,
        selectedProvider: undefined as any,
        reasoning: {
          primaryFactors: [{ factor: '错误', weight: 1, explanation: error.message }],
          modelCapabilities: [],
          costConsiderations: { costScore: 0, budgetConstraint: false, costEfficiency: 0 },
          performanceHistory: { successRate: 0, avgLatency: 0, reliabilityScore: 0 },
          complexityAnalysis: { taskComplexity: 0, modelAdequacy: 0, complexityMatch: 0 },
        },
        predictedPerformance: {
          expectedLatency: 0,
          expectedCost: 0,
          expectedQuality: 0,
          successProbability: 0,
        },
        alternatives: [],
      },
      metrics: {
        decisionTime: 0,
        modelScores: [],
        decisionQuality: {
          confidence: 0,
          uncertainty: 1,
          alternativesCount: 0,
        },
      },
      executionInstructions: {
        modelId: '',
        providerId: '',
        requestConfig: {},
        monitoring: {
          trackLatency: false,
          trackSuccess: false,
          trackQuality: false,
        },
      },
    };
  }
  
  /**
   * 提取任务特征
   */
  private async extractTaskCharacteristics(task: TaskDescription): Promise<TaskAnalysisResult['characteristics']> {
    // 简化实现
    const content = task.content;
    const length = content.length;
    
    // 估算复杂度（简化）
    let complexity = 3; // 基础复杂度
    
    if (length > 500) complexity += 2;
    if (length > 1000) complexity += 2;
    
    // 关键词检测
    const complexKeywords = ['分析', '设计', '实现', '优化', '评估', '比较', '解释'];
    const codeKeywords = ['代码', '编程', '函数', '算法', 'bug', '错误'];
    const creativeKeywords = ['创意', '故事', '诗歌', '想象', '创新'];
    
    let keywordCount = 0;
    for (const keyword of [...complexKeywords, ...codeKeywords, ...creativeKeywords]) {
      if (content.includes(keyword)) {
        keywordCount++;
      }
    }
    
    complexity += Math.min(keywordCount, 3);
    
    // 限制在1-10之间
    complexity = Math.max(1, Math.min(10, complexity));
    
    // 估算token数
    const tokenEstimate = Math.ceil(length / 3);
    
    // 内容类型检测
    const contentType: Array<'text' | 'code' | 'data' | 'query' | 'instruction' | 'creative'> = ['text'];
    if (codeKeywords.some(kw => content.includes(kw))) contentType.push('code');
    if (creativeKeywords.some(kw => content.includes(kw))) contentType.push('creative');
    
    return {
      complexity,
      length,
      tokenEstimate,
      contentType,
      technicalRequirements: [],
    };
  }
  
  /**
   * 分析所需能力
   */
  private async analyzeRequiredCapabilities(
    task: TaskDescription,
    characteristics: TaskAnalysisResult['characteristics']
  ): Promise<TaskAnalysisResult['requiredCapabilities']> {
    const capabilities: TaskAnalysisResult['requiredCapabilities'] = [];
    const content = task.content.toLowerCase();
    
    // 基于内容检测能力需求
    if (characteristics.contentType.includes('code')) {
      capabilities.push({
        capability: 'coding',
        importance: 0.9,
        evidence: '任务包含代码相关术语',
      });
    }
    
    if (content.includes('分析') || content.includes('analyze')) {
      capabilities.push({
        capability: 'analysis',
        importance: 0.8,
        evidence: '任务要求分析能力',
      });
    }
    
    if (content.includes('翻译') || content.includes('translate')) {
      capabilities.push({
        capability: 'translation',
        importance: 0.7,
        evidence: '任务涉及翻译',
      });
    }
    
    if (content.includes('推理') || content.includes('reason')) {
      capabilities.push({
        capability: 'reasoning',
        importance: 0.85,
        evidence: '任务需要推理能力',
      });
    }
    
    // 确保至少有一个基本能力
    if (capabilities.length === 0) {
      capabilities.push({
        capability: 'general',
        importance: 0.5,
        evidence: '通用任务需求',
      });
    }
    
    return capabilities;
  }
  
  /**
   * 分析质量要求
   */
  private async analyzeQualityRequirements(
    _task: TaskDescription,
    characteristics: TaskAnalysisResult['characteristics']
  ): Promise<TaskAnalysisResult['qualityRequirements']> {
    // 基于复杂度和内容类型估算质量要求
    const complexityFactor = characteristics.complexity / 10;
    
    return {
      accuracy: 0.5 + complexityFactor * 0.3,
      creativity: characteristics.contentType.includes('creative') ? 0.8 : 0.3,
      thoroughness: 0.6 + complexityFactor * 0.2,
      speed: 1 - complexityFactor * 0.4, // 复杂度越高，速度要求越低
    };
  }
  
  /**
   * 分析拆分潜力
   */
  private async analyzeSplittingPotential(
    _task: TaskDescription,
    characteristics: TaskAnalysisResult['characteristics']
  ): Promise<TaskAnalysisResult['splittingPotential']> {
    // 简化逻辑：长文本和复杂任务有拆分潜力
    const canSplit = characteristics.length > 300 && characteristics.complexity > 5;
    
    if (!canSplit) {
      return { canSplit: false };
    }
    
    // 估算最优拆分数量
    const optimalSplits = Math.min(3, Math.ceil(characteristics.length / 500));
    
    return {
      canSplit: true,
      optimalSplits,
      splitPoints: ['主要需求分析', '详细方案设计', '实施步骤规划'].slice(0, optimalSplits),
    };
  }
  
  /**
   * 创建默认任务分析
   */
  private createDefaultTaskAnalysis(task: TaskDescription): TaskAnalysisResult {
    return {
      taskId: task.id,
      characteristics: {
        complexity: 5,
        length: task.content.length,
        tokenEstimate: Math.ceil(task.content.length / 3),
        contentType: ['text'],
        technicalRequirements: [],
      },
      requiredCapabilities: [
        {
          capability: 'general',
          importance: 0.5,
          evidence: '通用任务需求',
        },
      ],
      qualityRequirements: {
        accuracy: 0.7,
        creativity: 0.3,
        thoroughness: 0.6,
        speed: 0.8,
      },
      splittingPotential: {
        canSplit: false,
      },
    };
  }
  
  /**
   * 计算内存使用率
   */
  private calculateMemoryUsage(): number {
    // 简化实现：返回固定值
    // 实际实现可以使用process.memoryUsage()
    return 0.3; // 30%
  }
  
  /**
   * 计算错误率
   */
  private calculateErrorRate(): number {
    if (this.statistics.totalDecisions === 0) {
      return 0;
    }
    
    const errorCount = this.statistics.totalDecisions - this.statistics.successfulDecisions;
    return errorCount / this.statistics.totalDecisions;
  }
}

/**
 * 决策引擎工厂
 */
export class DecisionEngineFactory {
  private static instance: DecisionEngine;
  
  static getInstance(config?: Partial<RoutingConfig>): DecisionEngine {
    if (!DecisionEngineFactory.instance) {
      DecisionEngineFactory.instance = new DecisionEngine(config);
      logger.info('创建路由决策引擎单例');
    }
    
    return DecisionEngineFactory.instance;
  }
  
  static destroyInstance(): void {
    if (DecisionEngineFactory.instance) {
      DecisionEngineFactory.instance = null as any;
      logger.info('销毁路由决策引擎单例');
    }
  }
}