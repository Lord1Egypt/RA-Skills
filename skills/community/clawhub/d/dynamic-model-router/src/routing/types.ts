/**
 * 智能路由引擎类型定义
 */

import type { ProviderInfo, ModelInfo, TaskDescription, ModelResponse } from '../core/types.js';

/**
 * 路由决策结果
 */
export interface RoutingDecision {
  decisionId: string;
  timestamp: Date;
  
  // 输入
  task: TaskDescription;
  availableModels: ModelInfo[];
  availableProviders: ProviderInfo[];
  
  // 决策
  selectedModel: ModelInfo;
  selectedProvider: ProviderInfo;
  
  // 决策理由
  reasoning: RoutingReasoning;
  
  // 性能预测
  predictedPerformance: {
    expectedLatency: number; // 毫秒
    expectedCost: number; // 成本单位
    expectedQuality: number; // 0-1质量评分
    successProbability: number; // 0-1成功率
  };
  
  // 替代选项（按优先级排序）
  alternatives: Array<{
    model: ModelInfo;
    provider: ProviderInfo;
    score: number;
    reason: string;
  }>;
  
  // 任务拆分建议（如果需要）
  splitRecommendation?: TaskSplitRecommendation;
}

/**
 * 路由决策理由
 */
export interface RoutingReasoning {
  primaryFactors: Array<{
    factor: string;
    weight: number;
    explanation: string;
  }>;
  
  modelCapabilities: Array<{
    capability: string;
    matchScore: number;
    required: boolean;
  }>;
  
  costConsiderations: {
    costScore: number;
    budgetConstraint: boolean;
    costEfficiency: number;
  };
  
  performanceHistory: {
    successRate: number;
    avgLatency: number;
    reliabilityScore: number;
  };
  
  complexityAnalysis: {
    taskComplexity: number; // 0-10
    modelAdequacy: number; // 0-10
    complexityMatch: number; // 0-1
  };
}

/**
 * 任务拆分建议
 */
export interface TaskSplitRecommendation {
  shouldSplit: boolean;
  reason?: string;
  
  // 拆分方案
  splitPlan?: {
    subTasks: Array<{
      id: string;
      description: string;
      complexity: number;
      requiredCapabilities: string[];
      recommendedModel: ModelInfo;
    }>;
    
    // 执行策略
    executionStrategy: 'sequential' | 'parallel' | 'pipeline';
    estimatedTotalTime: number; // 毫秒
    estimatedTotalCost: number;
    
    // 协调要求
    coordinationRequirements: {
      needsContextSharing: boolean;
      needsResultAggregation: boolean;
      needsConsistencyCheck: boolean;
    };
  };
}

/**
 * 路由策略类型
 */
export enum RoutingStrategy {
  COST_OPTIMIZED = 'cost_optimized',      // 成本优先
  PERFORMANCE_OPTIMIZED = 'performance_optimized', // 性能优先
  BALANCED = 'balanced',                  // 平衡模式
  RELIABILITY_FIRST = 'reliability_first', // 可靠性优先
  QUALITY_FIRST = 'quality_first',        // 质量优先
  SPEED_FIRST = 'speed_first',            // 速度优先
}

/**
 * 路由约束
 */
export interface RoutingConstraints {
  maxCost?: number;
  maxLatency?: number;
  minQuality?: number;
  requiredCapabilities?: string[];
  preferredProviders?: string[];
  excludedModels?: string[];
  
  // 时间约束
  deadline?: Date;
  
  // 资源约束
  maxTokenUsage?: number;
  maxConcurrentRequests?: number;
}

/**
 * 路由配置
 */
export interface RoutingConfig {
  defaultStrategy: RoutingStrategy;
  constraints: RoutingConstraints;
  
  // 权重配置
  weights: {
    cost: number;
    latency: number;
    reliability: number;
    quality: number;
    capabilityMatch: number;
  };
  
  // 阈值配置
  thresholds: {
    minSuccessRate: number;
    maxAcceptableLatency: number;
    maxAcceptableCost: number;
    minCapabilityMatch: number;
  };
  
  // 高级配置
  enableTaskSplitting: boolean;
  enableParallelExecution: boolean;
  enableFallbackRouting: boolean;
  learningEnabled: boolean;
  
  // 回退策略
  fallbackStrategy: {
    maxRetries: number;
    fallbackModels: string[];
    escalationPath: Array<{
      condition: string;
      action: string;
    }>;
  };
}

/**
 * 路由上下文
 */
export interface RoutingContext {
  // 当前状态
  currentLoad: {
    providerLoad: Map<string, number>; // 0-1负载率
    modelLoad: Map<string, number>;
    recentErrors: Map<string, number>; // 近期错误数
  };
  
  // 历史性能
  historicalPerformance: {
    successRates: Map<string, number>;
    averageLatencies: Map<string, number>;
    costEfficiency: Map<string, number>;
  };
  
  // 环境因素
  environment: {
    timeOfDay: string;
    networkQuality: number; // 0-1
    systemLoad: number; // 0-1
  };
  
  // 用户偏好
  userPreferences: {
    preferredModels: string[];
    avoidedModels: string[];
    qualityImportance: number;
    speedImportance: number;
    costSensitivity: number;
  };
}

/**
 * 路由评估指标
 */
export interface RoutingMetrics {
  decisionTime: number; // 决策耗时（毫秒）
  
  modelScores: Array<{
    modelId: string;
    providerId: string;
    
    // 各项评分
    scores: {
      cost: number;
      capability: number;
      performance: number;
      reliability: number;
      load: number;
    };
    
    // 加权总分
    totalScore: number;
    
    // 是否符合约束
    constraintsMet: boolean;
    constraintViolations: string[];
  }>;
  
  // 决策质量指标
  decisionQuality: {
    confidence: number; // 决策置信度 0-1
    uncertainty: number; // 不确定性 0-1
    alternativesCount: number; // 可用替代方案数量
  };
}

/**
 * 路由请求
 */
export interface RoutingRequest {
  task: TaskDescription;
  context?: RoutingContext;
  constraints?: RoutingConstraints;
  strategy?: RoutingStrategy;
  
  // 高级选项
  enableLearning?: boolean;
  requireExplanation?: boolean;
  trackPerformance?: boolean;
}

/**
 * 路由响应
 */
export interface RoutingResponse {
  decision: RoutingDecision;
  metrics: RoutingMetrics;
  
  // 执行指令
  executionInstructions: {
    modelId: string;
    providerId: string;
    requestConfig: {
      timeout?: number;
      maxTokens?: number;
      temperature?: number;
    };
    
    // 监控指令
    monitoring: {
      trackLatency: boolean;
      trackSuccess: boolean;
      trackQuality: boolean;
    };
  };
  
  // 学习数据
  learningData?: {
    features: Record<string, any>;
    predictedOutcome: any;
    actualOutcome?: any;
  };
}

/**
 * 路由引擎接口
 */
export interface IRoutingEngine {
  // 配置管理
  getConfig(): RoutingConfig;
  updateConfig(config: Partial<RoutingConfig>): void;
  
  // 核心路由
  route(request: RoutingRequest): Promise<RoutingResponse>;
  
  // 批量路由
  batchRoute(requests: RoutingRequest[]): Promise<RoutingResponse[]>;
  
  // 任务分析
  analyzeTask(task: TaskDescription): Promise<TaskAnalysisResult>;
  
  // 性能学习
  learnFromOutcome(decisionId: string, actualOutcome: ModelResponse): Promise<void>;
  
  // 状态查询
  getEngineStatus(): EngineStatus;
}

/**
 * 任务分析结果
 */
export interface TaskAnalysisResult {
  taskId: string;
  
  // 任务特征
  characteristics: {
    complexity: number; // 0-10
    length: number; // 字符数
    tokenEstimate: number; // 预计token数
    
    // 内容类型
    contentType: Array<'text' | 'code' | 'data' | 'query' | 'instruction' | 'creative'>;
    
    // 领域
    domain?: string;
    
    // 意图
    intent?: string;
    
    // 技术要求
    technicalRequirements: string[];
  };
  
  // 能力要求
  requiredCapabilities: Array<{
    capability: string;
    importance: number; // 0-1
    evidence: string;
  }>;
  
  // 质量要求
  qualityRequirements: {
    accuracy: number;
    creativity: number;
    thoroughness: number;
    speed: number;
  };
  
  // 拆分建议
  splittingPotential: {
    canSplit: boolean;
    optimalSplits?: number;
    splitPoints?: string[];
  };
}

/**
 * 引擎状态
 */
export interface EngineStatus {
  isInitialized: boolean;
  config: RoutingConfig;
  statistics: {
    totalDecisions: number;
    successfulDecisions: number;
    averageDecisionTime: number;
    learningSamples: number;
  };
  health: {
    memoryUsage: number;
    lastDecisionTime: number;
    errorRate: number;
  };
}

/**
 * 预测性能指标
 */
export interface PredictedPerformance {
  expectedLatency: number; // 毫秒
  expectedCost: number; // 成本单位
  expectedQuality: number; // 0-1质量评分
  successProbability: number; // 0-1成功率
  
  // 元数据
  predictionId?: string;
  predictionMethod?: string;
  confidence?: number; // 0-1置信度
  assumptions?: string[]; // 预测假设
  timestamp?: Date;
}

/**
 * 历史性能记录
 */
export interface HistoricalPerformance {
  id: string;
  predictionId: string;
  taskId: string;
  modelId: string;
  providerId: string;
  
  // 预测值
  predicted: {
    latency: number;
    cost: number;
    successProbability: number;
    quality: number;
  };
  
  // 实际值
  actual: {
    latency: number;
    cost: number;
    success: boolean;
    quality?: number;
    tokensUsed?: number;
    error?: string;
  };
  
  metadata: {
    recordedAt: Date;
    predictionMethod: string;
    taskComplexity?: string;
    estimatedTokens?: number;
  };
}