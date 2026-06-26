/**
 * OpenClaw集成层 - 共享类型定义
 */

import type { OpenClawProvider } from './provider-discovery.js';

/**
 * 调用统计
 */
export interface InvocationStats {
  providerId: string;
  modelId: string;
  success: boolean;
  responseTime: number;
  tokensUsed: number;
  error?: string;
  timestamp: Date;
}

/**
 * 调用器接口
 * 统一各种调用实现（CLI、API、适配器等）的接口
 */
export interface IOpenClawInvoker {
  // 调用历史
  getInvocationHistory(limit?: number): InvocationStats[];
  
  // 统计信息
  getSuccessRate(): number;
  getAverageResponseTime(): number;
  getProviderSuccessRate(providerId: string): number;
  
  // 调用方法
  invokeModel(request: ModelRequest, provider: OpenClawProvider): Promise<InvocationResult>;
}

/**
 * 模型请求
 */
export interface ModelRequest {
  model: string;
  messages: Array<{
    role: 'user' | 'assistant' | 'system';
    content: string;
  }>;
  maxTokens?: number;
  temperature?: number;
  stream?: boolean;
}

/**
 * 模型响应
 */
export interface ModelResponse {
  id: string;
  content: string;
  model: string;
  usage?: {
    promptTokens: number;
    completionTokens: number;
    totalTokens: number;
  };
  finishReason?: string;
}

/**
 * 调用结果
 */
export interface InvocationResult {
  response: ModelResponse;
  stats: InvocationStats;
}

/**
 * 调用器配置
 */
export interface InvokerConfig {
  openclawPath: string;
  timeoutMs: number;
  maxRetries: number;
  workspaceDir: string;
  tempDir: string;
}

/**
 * 健康状态
 */
export enum HealthStatus {
  HEALTHY = 'healthy',
  DEGRADED = 'degraded',
  UNHEALTHY = 'unhealthy',
  UNKNOWN = 'unknown',
}

/**
 * 性能指标
 */
export interface PerformanceMetrics {
  providerId: string;
  modelId: string;
  
  // 成功率
  successRate: number;
  totalCalls: number;
  successfulCalls: number;
  failedCalls: number;
  
  // 响应时间（毫秒）
  avgResponseTime: number;
  minResponseTime: number;
  maxResponseTime: number;
  responseTimeStdDev: number;
  
  // Token使用
  avgInputTokens: number;
  avgOutputTokens: number;
  avgTotalTokens: number;
  
  // 错误分布
  errorDistribution: Record<string, number>;
  
  // 时间窗口
  windowStart: Date;
  windowEnd: Date;
  sampleCount: number;
}

/**
 * 供应商健康状态
 */
export interface ProviderHealth {
  providerId: string;
  status: HealthStatus;
  lastChecked: Date;
  lastSuccessfulCall?: Date;
  failureCount: number;
  consecutiveFailures: number;
  recoveryAttempts: number;
  
  // 指标
  metrics: PerformanceMetrics[];
  
  // 详情
  details: {
    connectionTest: boolean;
    apiAccessible: boolean;
    rateLimitRemaining?: number;
    rateLimitReset?: Date;
    errorMessage?: string;
  };
}

/**
 * 监控配置
 */
export interface MonitorConfig {
  checkInterval: number;
  healthCheckTimeout: number;
  failureThreshold: number;
  recoveryThreshold: number;
  metricsWindow: number;
  maxMetricsPerProvider: number;
}