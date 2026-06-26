/**
 * 状态监控模块
 * 
 * 监控模型供应商和适配器的健康状态，收集性能指标
 */

import { RouterLogger } from '../utils/logger.js';
import { calculateAverage, calculateStandardDeviation } from '../utils/index.js';
import type { IOpenClawInvoker, InvocationStats } from './types.js';
import type { OpenClawProvider } from './provider-discovery.js';

const logger = new RouterLogger({ module: 'status-monitor' });

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
  checkInterval: number; // 检查间隔（毫秒）
  healthCheckTimeout: number; // 健康检查超时（毫秒）
  failureThreshold: number; // 失败阈值（连续失败次数）
  recoveryThreshold: number; // 恢复阈值（连续成功次数）
  metricsWindow: number; // 指标时间窗口（毫秒）
  maxMetricsPerProvider: number; // 每个供应商保留的最大指标数
}

/**
 * 告警配置
 */
export interface AlertConfig {
  enabled: boolean;
  degradedThreshold: number; // 降级阈值（成功率）
  unhealthyThreshold: number; // 不健康阈值（成功率）
  consecutiveFailuresThreshold: number; // 连续失败阈值
  notificationChannels: string[]; // 通知渠道
}

/**
 * 状态监控器
 */
export class StatusMonitor {
  private adapters: Map<string, IOpenClawInvoker> = new Map();
  private providers: Map<string, OpenClawProvider> = new Map();
  private providerHealth: Map<string, ProviderHealth> = new Map();
  private config: MonitorConfig;
  private alertConfig: AlertConfig;
  private isMonitoring: boolean = false;
  private monitoringInterval?: NodeJS.Timeout;
  
  constructor(config?: Partial<MonitorConfig>, alertConfig?: Partial<AlertConfig>) {
    this.config = {
      checkInterval: 60000, // 1分钟
      healthCheckTimeout: 10000, // 10秒
      failureThreshold: 3,
      recoveryThreshold: 2,
      metricsWindow: 3600000, // 1小时
      maxMetricsPerProvider: 100,
      ...config,
    };
    
    this.alertConfig = {
      enabled: true,
      degradedThreshold: 0.9, // 90%成功率
      unhealthyThreshold: 0.7, // 70%成功率
      consecutiveFailuresThreshold: 5,
      notificationChannels: [],
      ...alertConfig,
    };
    
    logger.info('状态监控器初始化', {
      checkInterval: this.config.checkInterval,
      metricsWindow: this.config.metricsWindow,
    });
  }
  
  /**
   * 注册适配器进行监控
   */
  registerAdapter(adapter: IOpenClawInvoker, provider: OpenClawProvider): void {
    const providerId = provider.id;
    
    this.adapters.set(providerId, adapter);
    this.providers.set(providerId, provider);
    
    // 初始化健康状态
    if (!this.providerHealth.has(providerId)) {
      this.providerHealth.set(providerId, this.createInitialHealth(providerId));
    }
    
    logger.debug('注册适配器进行监控', {
      providerId,
      modelCount: provider.models.length,
      enabled: provider.enabled,
    });
  }
  
  /**
   * 创建初始健康状态
   */
  private createInitialHealth(providerId: string): ProviderHealth {
    return {
      providerId,
      status: HealthStatus.UNKNOWN,
      lastChecked: new Date(0),
      failureCount: 0,
      consecutiveFailures: 0,
      recoveryAttempts: 0,
      metrics: [],
      details: {
        connectionTest: false,
        apiAccessible: false,
      },
    };
  }
  
  /**
   * 开始监控
   */
  startMonitoring(): void {
    if (this.isMonitoring) {
      logger.warn('监控已经在运行中');
      return;
    }
    
    logger.info('开始状态监控', {
      checkInterval: this.config.checkInterval,
      providers: Array.from(this.adapters.keys()),
    });
    
    this.isMonitoring = true;
    
    // 立即执行一次检查
    this.performHealthCheck().catch(error => {
      logger.error('初始健康检查失败', error as Error);
    });
    
    // 设置定期检查
    this.monitoringInterval = setInterval(() => {
      this.performHealthCheck().catch(error => {
        logger.error('定期健康检查失败', error as Error);
      });
    }, this.config.checkInterval);
  }
  
  /**
   * 停止监控
   */
  stopMonitoring(): void {
    if (!this.isMonitoring) {
      return;
    }
    
    logger.info('停止状态监控');
    
    this.isMonitoring = false;
    
    if (this.monitoringInterval) {
      clearInterval(this.monitoringInterval);
      this.monitoringInterval = undefined;
    }
  }
  
  /**
   * 执行健康检查
   */
  private async performHealthCheck(): Promise<void> {
    const startTime = Date.now();
    
    logger.debug('开始健康检查周期');
    
    const checkPromises = Array.from(this.adapters.entries()).map(
      async ([providerId, adapter]) => {
        try {
          await this.checkProviderHealth(providerId, adapter);
        } catch (error) {
          logger.error('供应商健康检查失败', error as Error, { providerId });
        }
      }
    );
    
    await Promise.allSettled(checkPromises);
    
    // 收集和计算指标
    this.collectMetrics();
    
    // 发送告警（如果需要）
    if (this.alertConfig.enabled) {
      this.checkAndSendAlerts();
    }
    
    const duration = Date.now() - startTime;
    logger.debug('健康检查周期完成', { durationMs: duration });
  }
  
  /**
   * 检查供应商健康状态
   */
  private async checkProviderHealth(providerId: string, _adapter: IOpenClawInvoker): Promise<void> {
    const health = this.providerHealth.get(providerId)!;
    const provider = this.providers.get(providerId);
    
    if (!provider) {
      logger.error('找不到供应商信息', undefined, { providerId });
      return;
    }
    
    health.lastChecked = new Date();
    
    // 跳过禁用的供应商
    if (!provider.enabled) {
      health.status = HealthStatus.UNHEALTHY;
      health.details.errorMessage = '供应商被禁用';
      return;
    }
    
    try {
      // 执行连接测试
      const isAccessible = await this.testConnection(provider);
      
      if (isAccessible) {
        // 连接成功
        health.details.connectionTest = true;
        health.details.apiAccessible = true;
        health.consecutiveFailures = 0;
        health.recoveryAttempts++;
        
        // 更新状态
        if (health.status === HealthStatus.UNHEALTHY && health.recoveryAttempts >= this.config.recoveryThreshold) {
          health.status = HealthStatus.HEALTHY;
          health.recoveryAttempts = 0;
          logger.info('供应商恢复健康', { providerId });
        } else if (health.status === HealthStatus.UNKNOWN || health.status === HealthStatus.DEGRADED) {
          health.status = HealthStatus.HEALTHY;
        }
        
        // 记录最后成功时间
        health.lastSuccessfulCall = new Date();
        
        logger.debug('供应商健康检查通过', { providerId });
        
      } else {
        // 连接失败
        this.handleProviderFailure(health, '连接测试失败');
      }
      
    } catch (error) {
      // 检查过程中出错
      this.handleProviderFailure(health, (error as Error).message);
    }
  }
  
  /**
   * 测试连接
   */
  private async testConnection(provider: OpenClawProvider): Promise<boolean> {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.config.healthCheckTimeout);
    
    try {
      // 使用简单的HTTP HEAD请求测试连接
      const testUrl = this.getConnectionTestUrl(provider);
      
      const response = await fetch(testUrl, {
        method: 'HEAD',
        headers: {
          'User-Agent': 'OpenClaw-DynamicRouter-Monitor/0.1.0',
        },
        signal: controller.signal,
      });
      
      clearTimeout(timeoutId);
      
      // 检查响应状态
      const isOk = response.ok || response.status < 500;
      
      // 尝试提取速率限制信息
      if (response.headers) {
        const rateLimitRemaining = response.headers.get('x-ratelimit-remaining');
        // @ts-ignore - 变量声明但未使用
        const _rateLimitReset = response.headers.get('x-ratelimit-reset');
        
        if (rateLimitRemaining) {
          provider.models.forEach((_model: {
            id: string;
            name: string;
            reasoning: boolean;
            contextWindow: number;
            maxTokens: number;
            cost: {
              input: number;
              output: number;
              cacheRead?: number;
              cacheWrite?: number;
            };
          }) => {
            // 这里可以记录速率限制信息
          });
        }
      }
      
      return isOk;
      
    } catch (error) {
      clearTimeout(timeoutId);
      return false;
    }
  }
  
  /**
   * 获取连接测试URL
   */
  private getConnectionTestUrl(provider: OpenClawProvider): string {
    // 不同供应商的连接测试端点
    const testEndpoints: Record<string, string> = {
      'deepseek': '/health',
      'openai': '/models',
      'anthropic': '/v1/messages',
      'google': '/v1/models',
      'mistral': '/v1/models',
      'cohere': '/v1/generate',
      'minimax': '/v1/models',
      'qwen': '/v1/models',
      'baichuan': '/v1/models',
    };
    
    const endpoint = testEndpoints[provider.id] || '/';
    return `${provider.baseUrl}${endpoint}`;
  }
  
  /**
   * 处理供应商故障
   */
  private handleProviderFailure(health: ProviderHealth, errorMessage: string): void {
    health.failureCount++;
    health.consecutiveFailures++;
    health.details.connectionTest = false;
    health.details.apiAccessible = false;
    health.details.errorMessage = errorMessage;
    
    // 更新状态
    if (health.consecutiveFailures >= this.config.failureThreshold) {
      health.status = HealthStatus.UNHEALTHY;
      health.recoveryAttempts = 0;
      
      logger.warn('供应商标记为不健康', {
        providerId: health.providerId,
        consecutiveFailures: health.consecutiveFailures,
        errorMessage,
      });
    } else {
      health.status = HealthStatus.DEGRADED;
      
      logger.debug('供应商健康降级', {
        providerId: health.providerId,
        consecutiveFailures: health.consecutiveFailures,
        errorMessage,
      });
    }
  }
  
  /**
   * 收集指标
   */
  private collectMetrics(): void {
    const now = new Date();
    const windowStart = new Date(now.getTime() - this.config.metricsWindow);
    
    for (const [providerId, adapter] of this.adapters.entries()) {
      const health = this.providerHealth.get(providerId);
      if (!health) continue;
      
      // 获取调用历史
      const callHistory = adapter.getInvocationHistory();
      
      // 过滤时间窗口内的调用
      const windowCalls = callHistory.filter(call => 
        call.timestamp >= windowStart && call.timestamp <= now
      );
      
      if (windowCalls.length === 0) {
        continue;
      }
      
      // 计算指标
      const metrics = this.calculateMetrics(providerId, windowCalls, windowStart, now);
      
      // 添加到健康状态
      health.metrics.push(metrics);
      
      // 保持指标数量在限制内
      if (health.metrics.length > this.config.maxMetricsPerProvider) {
        health.metrics = health.metrics.slice(-this.config.maxMetricsPerProvider);
      }
    }
  }
  
  /**
   * 计算性能指标
   */
  private calculateMetrics(
    providerId: string,
    calls: InvocationStats[],
    windowStart: Date,
    windowEnd: Date
  ): PerformanceMetrics {
    // 按模型分组
    const callsByModel = new Map<string, InvocationStats[]>();
    
    for (const call of calls) {
      if (!callsByModel.has(call.modelId)) {
        callsByModel.set(call.modelId, []);
      }
      callsByModel.get(call.modelId)!.push(call);
    }
    
    // 计算每个模型的指标（这里简化：只计算第一个模型的指标）
    const firstModelId = callsByModel.keys().next().value || 'unknown';
    const modelCalls = callsByModel.get(firstModelId) || [];
    
    // 成功率
    const successfulCalls = modelCalls.filter(call => call.success).length;
    const failedCalls = modelCalls.filter(call => !call.success).length;
    const totalCalls = modelCalls.length;
    const successRate = totalCalls > 0 ? successfulCalls / totalCalls : 0;
    
    // 响应时间
    const responseTimes = modelCalls.map(call => call.responseTime);
    const avgResponseTime = calculateAverage(responseTimes);
    const minResponseTime = Math.min(...responseTimes);
    const maxResponseTime = Math.max(...responseTimes);
    const responseTimeStdDev = calculateStandardDeviation(responseTimes);
    
    // 错误分布
    const errorDistribution: Record<string, number> = {};
    modelCalls
      .filter(call => !call.success && call.error)
      .forEach(call => {
        const errorType = this.extractErrorType(call.error!);
        errorDistribution[errorType] = (errorDistribution[errorType] || 0) + 1;
      });
    
    return {
      providerId,
      modelId: firstModelId,
      successRate,
      totalCalls,
      successfulCalls,
      failedCalls,
      avgResponseTime,
      minResponseTime,
      maxResponseTime,
      responseTimeStdDev,
      avgInputTokens: 0, // 这些需要从实际的API响应中获取
      avgOutputTokens: 0,
      avgTotalTokens: calculateAverage(modelCalls.map(call => call.tokensUsed)),
      errorDistribution,
      windowStart,
      windowEnd,
      sampleCount: modelCalls.length,
    };
  }
  
  /**
   * 提取错误类型
   */
  private extractErrorType(errorMessage: string): string {
    const errorPatterns = [
      { pattern: /timeout/i, type: 'TIMEOUT' },
      { pattern: /rate.*limit/i, type: 'RATE_LIMIT' },
      { pattern: /auth/i, type: 'AUTHENTICATION' },
      { pattern: /network/i, type: 'NETWORK' },
      { pattern: /server.*error/i, type: 'SERVER_ERROR' },
      { pattern: /not.*found/i, type: 'NOT_FOUND' },
    ];
    
    for (const { pattern, type } of errorPatterns) {
      if (pattern.test(errorMessage)) {
        return type;
      }
    }
    
    return 'OTHER';
  }
  
  /**
   * 检查和发送告警
   */
  private checkAndSendAlerts(): void {
    for (const health of this.providerHealth.values()) {
      // 获取最新指标
      const latestMetrics = health.metrics[health.metrics.length - 1];
      
      if (!latestMetrics) {
        continue;
      }
      
      // 检查是否需要告警
      const needsAlert = this.shouldAlert(health, latestMetrics);
      
      if (needsAlert) {
        this.sendAlert(health, latestMetrics);
      }
    }
  }
  
  /**
   * 检查是否需要告警
   */
  private shouldAlert(health: ProviderHealth, metrics: PerformanceMetrics): boolean {
    // 不健康状态
    if (health.status === HealthStatus.UNHEALTHY) {
      return true;
    }
    
    // 降级状态且配置了告警
    if (health.status === HealthStatus.DEGRADED && 
        metrics.successRate < this.alertConfig.degradedThreshold) {
      return true;
    }
    
    // 连续失败
    if (health.consecutiveFailures >= this.alertConfig.consecutiveFailuresThreshold) {
      return true;
    }
    
    // 成功率低于不健康阈值
    if (metrics.successRate < this.alertConfig.unhealthyThreshold) {
      return true;
    }
    
    return false;
  }
  
  /**
   * 发送告警
   */
  private sendAlert(health: ProviderHealth, metrics: PerformanceMetrics): void {
    const alertMessage = this.formatAlertMessage(health, metrics);
    
    logger.warn('发送供应商健康告警', {
      providerId: health.providerId,
      status: health.status,
      successRate: metrics.successRate,
      consecutiveFailures: health.consecutiveFailures,
      alertMessage,
    });
    
    // TODO: 实现实际的通知发送
    // 例如：发送到Telegram、Slack、邮件等
  }
  
  /**
   * 格式化告警消息
   */
  private formatAlertMessage(health: ProviderHealth, metrics: PerformanceMetrics): string {
    const lines = [
      `🚨 供应商健康告警`,
      `供应商: ${health.providerId}`,
      `状态: ${health.status}`,
      `成功率: ${(metrics.successRate * 100).toFixed(1)}%`,
      `连续失败: ${health.consecutiveFailures}次`,
      `最后检查: ${health.lastChecked.toLocaleString('zh-CN')}`,
    ];
    
    if (health.details.errorMessage) {
      lines.push(`错误: ${health.details.errorMessage}`);
    }
    
    return lines.join('\n');
  }
  
  /**
   * 获取供应商健康状态
   */
  getProviderHealth(providerId: string): ProviderHealth | undefined {
    return this.providerHealth.get(providerId);
  }
  
  /**
   * 获取所有供应商健康状态
   */
  getAllProviderHealth(): ProviderHealth[] {
    return Array.from(this.providerHealth.values());
  }
  
  /**
   * 获取健康供应商列表
   */
  getHealthyProviders(): string[] {
    return Array.from(this.providerHealth.entries())
      .filter(([_, health]) => health.status === HealthStatus.HEALTHY)
      .map(([providerId]) => providerId);
  }
  
  /**
   * 获取不健康供应商列表
   */
  getUnhealthyProviders(): string[] {
    return Array.from(this.providerHealth.entries())
      .filter(([_, health]) => health.status === HealthStatus.UNHEALTHY)
      .map(([providerId]) => providerId);
  }
  
  /**
   * 获取监控状态
   */
  getMonitoringStatus(): any {
    return {
      isMonitoring: this.isMonitoring,
      totalProviders: this.adapters.size,
      healthyProviders: this.getHealthyProviders().length,
      unhealthyProviders: this.getUnhealthyProviders().length,
      checkInterval: this.config.checkInterval,
      lastCheckTime: Array.from(this.providerHealth.values())
        .map(h => h.lastChecked)
        .sort((a, b) => b.getTime() - a.getTime())[0] || null,
    };
  }
  
  /**
   * 获取配置
   */
  getConfig(): MonitorConfig {
    return { ...this.config };
  }
  
  /**
   * 更新配置
   */
  updateConfig(config: Partial<MonitorConfig>): void {
    this.config = { ...this.config, ...config };
    logger.info('监控配置更新', { updates: config });
  }
  
  /**
   * 重置供应商健康状态
   */
  resetProviderHealth(providerId: string): void {
    if (this.providerHealth.has(providerId)) {
      this.providerHealth.set(providerId, this.createInitialHealth(providerId));
      logger.info('重置供应商健康状态', { providerId });
    }
  }
  
  /**
   * 清理旧指标
   */
  cleanupOldMetrics(): void {
    const now = new Date();
    const cutoffTime = new Date(now.getTime() - this.config.metricsWindow * 2); // 两倍时间窗口
    
    for (const health of this.providerHealth.values()) {
      const originalCount = health.metrics.length;
      health.metrics = health.metrics.filter(metric => 
        metric.windowEnd >= cutoffTime
      );
      
      if (health.metrics.length < originalCount) {
        logger.debug('清理旧指标', {
          providerId: health.providerId,
          removed: originalCount - health.metrics.length,
          remaining: health.metrics.length,
        });
      }
    }
  }
}