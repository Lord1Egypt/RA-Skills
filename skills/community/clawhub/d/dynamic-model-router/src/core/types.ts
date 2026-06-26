/**
 * 动态模型路由技能 - 核心类型定义
 */

// 任务描述接口
export interface TaskDescription {
  id: string;
  content: string;
  language: 'zh' | 'en' | 'mixed' | 'other';
  complexity: 'simple' | 'medium' | 'complex';
  category: string[];
  estimatedTokens: number;
  createdAt: Date;
}

// 模型能力画像
export interface ModelCapability {
  modelId: string;
  provider: string;
  capabilities: {
    coding: number; // 0-100
    writing: number;
    analysis: number;
    translation: number;
    reasoning: number;
  };
  costPerToken: number;
  avgResponseTime: number;
  successRate: number;
  languageSupport: string[];
  lastUpdated: Date;
}

// ModelInfo别名（向后兼容）
export type ModelInfo = ModelCapability;

// 路由决策
export interface RoutingDecision {
  taskId: string;
  selectedModel: string;
  selectedProvider: string;
  confidence: number;
  alternatives: Array<{
    model: string;
    provider: string;
    score: number;
  }>;
  reasoning: string;
  createdAt: Date;
}

// 执行结果
export interface ExecutionResult {
  decisionId: string;
  success: boolean;
  responseTime: number;
  tokensUsed: number;
  userFeedback?: number; // 1-5
  error?: string;
  completedAt: Date;
}

// 配置接口
export interface RouterConfig {
  enabled: boolean;
  learningEnabled: boolean;
  defaultStrategy: 'cost' | 'quality' | 'balanced';
  
  complexityThresholds: {
    simple: number; // 0-1
    medium: number; // 0-1
  };
  
  scoringWeights: {
    capabilityMatch: number;
    costEfficiency: number;
    performance: number;
    reliability: number;
  };
  
  providers: {
    autoDiscover: boolean;
    refreshInterval: number; // seconds
  };
  
  learning: {
    feedbackCollection: boolean;
    optimizationInterval: number; // seconds
    minSamplesForOptimization: number;
  };
}

// 错误类型
export class RouterError extends Error {
  constructor(
    message: string,
    public readonly code: string,
    public readonly details?: any
  ) {
    super(message);
    this.name = 'RouterError';
  }
}

// 供应商信息
export interface ProviderInfo {
  id: string;
  name: string;
  baseUrl: string;
  apiKey?: string;
  models: string[];
  enabled: boolean;
}

// 模型调用请求
export interface ModelRequest {
  model: string;
  messages: Array<{
    role: 'user' | 'assistant' | 'system';
    content: string;
  }>;
  maxTokens?: number;
  temperature?: number;
}

// 模型调用响应
export interface ModelResponse {
  id: string;
  content: string;
  model: string;
  usage: {
    promptTokens: number;
    completionTokens: number;
    totalTokens: number;
  };
  finishReason: string;
}

// 常量定义
export const CONSTANTS = {
  // 复杂度阈值默认值
  COMPLEXITY_THRESHOLDS: {
    SIMPLE: 0.3,
    MEDIUM: 0.7,
  },
  
  // 评分权重默认值
  SCORING_WEIGHTS: {
    CAPABILITY_MATCH: 0.4,
    COST_EFFICIENCY: 0.3,
    PERFORMANCE: 0.2,
    RELIABILITY: 0.1,
  },
  
  // 默认配置
  DEFAULT_CONFIG: {
    enabled: true,
    learningEnabled: true,
    defaultStrategy: 'balanced',
    complexityThresholds: {
      simple: 0.3,
      medium: 0.7,
    },
    scoringWeights: {
      capabilityMatch: 0.4,
      costEfficiency: 0.3,
      performance: 0.2,
      reliability: 0.1,
    },
    providers: {
      autoDiscover: true,
      refreshInterval: 3600,
    },
    learning: {
      feedbackCollection: true,
      optimizationInterval: 86400,
      minSamplesForOptimization: 100,
    },
  } as RouterConfig,
};