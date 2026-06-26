/**
 * Provider 路由管理器
 * 
 * 层级：Layer 8.5 - Governance Control Plane
 * 功能：多 Provider 路由、故障切换、负载均衡
 * 版本：V1.0.0
 * 状态：🟡 开发中
 */

// ============== 类型定义 ==============

/**
 * Provider 配置
 */
export interface ProviderConfig {
  /** Provider ID */
  id: string;
  /** Provider 名称 */
  name: string;
  /** Base URL */
  baseUrl: string;
  /** API 类型 */
  api: string;
  /** 优先级 (1-10, 1 最高) */
  priority: number;
  /** 权重 (用于负载均衡) */
  weight: number;
  /** 超时时间 (ms) */
  timeoutMs: number;
  /** 最大重试次数 */
  maxRetries: number;
  /** 是否启用 */
  enabled: boolean;
  /** 健康检查配置 */
  healthCheck: {
    enabled: boolean;
    intervalMs: number;
    timeoutMs: number;
  };
}

/**
 * Provider 健康状态
 */
export interface ProviderHealthStatus {
  /** Provider ID */
  providerId: string;
  /** 是否健康 */
  healthy: boolean;
  /** 最后检查时间 */
  lastCheckAt: number;
  /** 连续失败次数 */
  consecutiveFailures: number;
  /** 平均响应时间 (ms) */
  avgResponseTimeMs: number;
  /** 成功率 */
  successRate: number;
}

/**
 * 路由策略
 */
export type RoutingStrategy =
  | 'priority' // 优先级优先
  | 'round_robin' // 轮询
  | 'weighted' // 加权轮询
  | 'latency' // 延迟最低
  | 'cost_optimized'; // 成本优化

/**
 * 路由配置
 */
export interface RouterConfig {
  /** 路由策略 */
  strategy: RoutingStrategy;
  /** Fallback 链 */
  fallbackChain: string[];
  /** 最大重试次数 */
  maxRetries: number;
  /** 超时时间 (ms) */
  timeoutMs: number;
  /** 启用健康检查 */
  enableHealthCheck: boolean;
  /** 健康检查间隔 (ms) */
  healthCheckIntervalMs: number;
  /** 自动剔除不健康 Provider */
  autoExcludeUnhealthy: boolean;
  /** 剔除时长 (ms) */
  excludeDurationMs: number;
}

/**
 * 路由结果
 */
export interface RoutingResult {
  /** 选中的 Provider */
  selectedProvider: string;
  /** 选择原因 */
  reason: string;
  /** 备选 Provider */
  alternatives: string[];
  /** 路由耗时 (ms) */
  routingTimeMs: number;
}

// ============== 默认配置 ==============

const DEFAULT_ROUTER_CONFIG: RouterConfig = {
  strategy: 'priority',
  fallbackChain: ['modelstudio', 'bailian', 'anthropic', 'openai'],
  maxRetries: 3,
  timeoutMs: 30000,
  enableHealthCheck: true,
  healthCheckIntervalMs: 60000, // 1 分钟
  autoExcludeUnhealthy: true,
  excludeDurationMs: 300000, // 5 分钟
};

// ============== 核心类 ==============

/**
 * Provider 路由管理器
 */
export class ProviderRouter {
  private config: RouterConfig;
  private providers: Map<string, ProviderConfig>;
  private healthStatus: Map<string, ProviderHealthStatus>;
  private roundRobinIndex: number = 0;
  private lastHealthCheckTime: number = 0;

  constructor(config: Partial<RouterConfig> = {}) {
    this.config = { ...DEFAULT_ROUTER_CONFIG, ...config };
    this.providers = new Map();
    this.healthStatus = new Map();
  }

  /**
   * 注册 Provider
   */
  registerProvider(provider: ProviderConfig): void {
    this.providers.set(provider.id, provider);
    this.healthStatus.set(provider.id, {
      providerId: provider.id,
      healthy: true,
      lastCheckAt: Date.now(),
      consecutiveFailures: 0,
      avgResponseTimeMs: 0,
      successRate: 1.0,
    });
    console.log(`[Provider Router] 📝 Registered: ${provider.id} (priority: ${provider.priority})`);
  }

  /**
   * 选择 Provider
   */
  selectProvider(modelPreference?: string): RoutingResult {
    const startTime = Date.now();
    const alternatives: string[] = [];

    // 获取可用的 Provider 列表
    const availableProviders = this.getAvailableProviders();

    if (availableProviders.length === 0) {
      throw new Error('No available providers');
    }

    let selected: ProviderConfig | null = null;
    let reason = '';

    // 根据策略选择
    switch (this.config.strategy) {
      case 'priority':
        selected = this.selectByPriority(availableProviders);
        reason = 'Priority-based selection';
        break;
      case 'round_robin':
        selected = this.selectRoundRobin(availableProviders);
        reason = 'Round-robin selection';
        break;
      case 'weighted':
        selected = this.selectWeighted(availableProviders);
        reason = 'Weighted selection';
        break;
      case 'latency':
        selected = this.selectByLatency(availableProviders);
        reason = 'Lowest latency selection';
        break;
      case 'cost_optimized':
        selected = this.selectByCost(availableProviders, modelPreference);
        reason = 'Cost-optimized selection';
        break;
    }

    if (!selected) {
      throw new Error('Failed to select provider');
    }

    // 构建备选列表
    availableProviders
      .filter(p => p.id !== selected!.id)
      .forEach(p => alternatives.push(p.id));

    return {
      selectedProvider: selected.id,
      reason,
      alternatives,
      routingTimeMs: Date.now() - startTime,
    };
  }

  /**
   * 记录 Provider 请求结果
   */
  recordResult(providerId: string, success: boolean, responseTimeMs: number): void {
    const status = this.healthStatus.get(providerId);
    if (!status) {
      return;
    }

    status.lastCheckAt = Date.now();

    if (success) {
      status.consecutiveFailures = 0;
      status.successRate = Math.min(1.0, status.successRate + 0.1);
    } else {
      status.consecutiveFailures++;
      status.successRate = Math.max(0.0, status.successRate - 0.2);

      // 自动剔除不健康的 Provider
      if (
        this.config.autoExcludeUnhealthy &&
        status.consecutiveFailures >= 3
      ) {
        status.healthy = false;
        console.warn(
          `[Provider Router] ⚠️ Provider ${providerId} marked unhealthy (${status.consecutiveFailures} failures)`
        );
      }
    }

    // 更新平均响应时间
    status.avgResponseTimeMs =
      (status.avgResponseTimeMs * 0.8) + (responseTimeMs * 0.2);
  }

  /**
   * 获取 Provider 健康状态
   */
  getHealthStatus(providerId: string): ProviderHealthStatus | undefined {
    return this.healthStatus.get(providerId);
  }

  /**
   * 获取所有 Provider 状态
   */
  getAllHealthStatus(): ProviderHealthStatus[] {
    return Array.from(this.healthStatus.values());
  }

  /**
   * 手动恢复 Provider
   */
  recoverProvider(providerId: string): void {
    const status = this.healthStatus.get(providerId);
    if (status) {
      status.healthy = true;
      status.consecutiveFailures = 0;
      console.log(`[Provider Router] ✅ Provider ${providerId} recovered`);
    }
  }

  /**
   * 获取路由统计
   */
  getStats(): {
    totalProviders: number;
    healthyProviders: number;
    unhealthyProviders: number;
    avgSuccessRate: number;
    avgResponseTimeMs: number;
  } {
    const statuses = Array.from(this.healthStatus.values());
    const healthy = statuses.filter(s => s.healthy);
    const unhealthy = statuses.filter(s => !s.healthy);

    return {
      totalProviders: statuses.length,
      healthyProviders: healthy.length,
      unhealthyProviders: unhealthy.length,
      avgSuccessRate:
        statuses.length > 0
          ? statuses.reduce((sum, s) => sum + s.successRate, 0) / statuses.length
          : 0,
      avgResponseTimeMs:
        statuses.length > 0
          ? statuses.reduce((sum, s) => sum + s.avgResponseTimeMs, 0) / statuses.length
          : 0,
    };
  }

  // ============== 私有方法 ==============

  /**
   * 获取可用的 Provider 列表
   */
  private getAvailableProviders(): ProviderConfig[] {
    return Array.from(this.providers.values())
      .filter(p => p.enabled)
      .filter(p => {
        const status = this.healthStatus.get(p.id);
        return !status || status.healthy;
      })
      .sort((a, b) => a.priority - b.priority);
  }

  /**
   * 按优先级选择
   */
  private selectByPriority(providers: ProviderConfig[]): ProviderConfig {
    return providers[0];
  }

  /**
   * 轮询选择
   */
  private selectRoundRobin(providers: ProviderConfig[]): ProviderConfig {
    this.roundRobinIndex = (this.roundRobinIndex + 1) % providers.length;
    return providers[this.roundRobinIndex];
  }

  /**
   * 加权选择
   */
  private selectWeighted(providers: ProviderConfig[]): ProviderConfig {
    const totalWeight = providers.reduce((sum, p) => sum + p.weight, 0);
    let random = Math.random() * totalWeight;

    for (const provider of providers) {
      random -= provider.weight;
      if (random <= 0) {
        return provider;
      }
    }

    return providers[providers.length - 1];
  }

  /**
   * 按延迟选择
   */
  private selectByLatency(providers: ProviderConfig[]): ProviderConfig {
    return providers.reduce((best, current) => {
      const bestStatus = this.healthStatus.get(best.id);
      const currentStatus = this.healthStatus.get(current.id);

      const bestLatency = bestStatus?.avgResponseTimeMs || Infinity;
      const currentLatency = currentStatus?.avgResponseTimeMs || Infinity;

      return currentLatency < bestLatency ? current : best;
    });
  }

  /**
   * 按成本选择 (模拟)
   */
  private selectByCost(
    providers: ProviderConfig[],
    modelPreference?: string
  ): ProviderConfig {
    // 简化实现：优先选择免费/低成本 Provider
    const costOrder = ['modelstudio', 'bailian', 'anthropic', 'openai'];

    for (const providerId of costOrder) {
      const provider = providers.find(p => p.id === providerId);
      if (provider) {
        return provider;
      }
    }

    return providers[0];
  }
}

// ============== 导出 ==============

export default ProviderRouter;
