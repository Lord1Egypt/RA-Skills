/**
 * 金丝雀部署器
 * 
 * 层级：Layer 8.5 - Governance Control Plane
 * 功能：视频生成技能的渐进式部署、流量切换、自动回滚
 * 版本：V1.0.0
 * 状态：🟡 开发中
 */

import { VideoGenerationRequest, VideoGenerationResponse } from './comfyui-workflow-orchestrator';
import { MCPVideoBus } from './mcp-video-bus';
import { ConfigManager } from './governance-config-store';

// ============== 类型定义 ==============

/**
 * 部署阶段
 */
export type CanaryStage = 0.01 | 0.05 | 0.2 | 0.5 | 1.0;

/**
 * 部署状态
 */
export type DeployStatus = 'pending' | 'deploying' | 'monitoring' | 'completed' | 'rolled_back' | 'failed';

/**
 * 部署配置
 */
export interface CanaryDeployConfig {
  /** 部署阶段流量比例 */
  stages: CanaryStage[];
  /** 每阶段观察时间 (分钟) */
  stageDurationMinutes: number;
  /** 成功率阈值 */
  successRateThreshold: number;
  /** 平均延迟阈值 (ms) */
  avgLatencyThresholdMs: number;
  /** 错误率阈值 */
  errorRateThreshold: number;
  /** 自动回滚启用 */
  autoRollbackEnabled: boolean;
}

/**
 * 部署指标
 */
export interface DeployMetrics {
  /** 总请求数 */
  totalRequests: number;
  /** 成功请求数 */
  successfulRequests: number;
  /** 失败请求数 */
  failedRequests: number;
  /** 平均延迟 (ms) */
  avgLatencyMs: number;
  /** P95 延迟 (ms) */
  p95LatencyMs: number;
  /** P99 延迟 (ms) */
  p99LatencyMs: number;
  /** 成功率 */
  successRate: number;
  /** 错误率 */
  errorRate: number;
}

/**
 * 部署会话
 */
export interface DeploySession {
  /** 会话 ID */
  id: string;
  /** 技能版本 */
  version: string;
  /** 当前阶段 */
  currentStage: CanaryStage;
  /** 部署状态 */
  status: DeployStatus;
  /** 开始时间 */
  startedAt: number;
  /** 阶段开始时间 */
  stageStartedAt: number;
  /** 阶段指标 */
  stageMetrics: DeployMetrics;
  /** 累计指标 */
  cumulativeMetrics: DeployMetrics;
  /** 回滚原因 */
  rollbackReason?: string;
}

/**
 * 部署结果
 */
export interface DeployResult {
  /** 部署状态 */
  status: DeployStatus;
  /** 最终阶段 */
  finalStage: CanaryStage;
  /** 部署耗时 (分钟) */
  durationMinutes: number;
  /** 最终指标 */
  finalMetrics: DeployMetrics;
  /** 回滚原因 (如果有) */
  rollbackReason?: string;
}

// ============== 默认配置 ==============

const DEFAULT_CANARY_CONFIG: CanaryDeployConfig = {
  stages: [0.01, 0.05, 0.2, 0.5, 1.0],
  stageDurationMinutes: 10,
  successRateThreshold: 0.95,
  avgLatencyThresholdMs: 5000,
  errorRateThreshold: 0.05,
  autoRollbackEnabled: true,
};

// ============== 核心类 ==============

/**
 * 金丝雀部署器
 */
export class CanaryDeployer {
  private config: CanaryDeployConfig;
  private mcpBus: MCPVideoBus;
  private configManager: ConfigManager;
  private activeSession: DeploySession | null = null;
  private trafficRouter: Map<string, number> = new Map(); // clientId -> canary percentage

  constructor(
    config: Partial<CanaryDeployConfig> = {},
    mcpBus: MCPVideoBus,
    configManager: ConfigManager
  ) {
    this.config = { ...DEFAULT_CANARY_CONFIG, ...config };
    this.mcpBus = mcpBus;
    this.configManager = configManager;
  }

  /**
   * 开始部署
   */
  async startDeploy(version: string): Promise<DeploySession> {
    if (this.activeSession) {
      throw new Error(`Deploy already in progress: ${this.activeSession.id}`);
    }

    const now = Date.now();
    const sessionId = `deploy_${version}_${now}`;

    const session: DeploySession = {
      id: sessionId,
      version,
      currentStage: 0.01,
      status: 'deploying',
      startedAt: now,
      stageStartedAt: now,
      stageMetrics: this.createEmptyMetrics(),
      cumulativeMetrics: this.createEmptyMetrics(),
    };

    this.activeSession = session;

    // 发送部署开始通知
    await this.notifyDeployStart(session);

    console.log(`[Canary Deployer] 🚀 Deploy started: ${sessionId} (v${version})`);
    return session;
  }

  /**
   * 记录请求指标
   */
  recordRequest(isSuccess: boolean, latencyMs: number): void {
    if (!this.activeSession) {
      return;
    }

    const metrics = this.activeSession.stageMetrics;
    metrics.totalRequests++;

    if (isSuccess) {
      metrics.successfulRequests++;
    } else {
      metrics.failedRequests++;
    }

    // 更新延迟统计
    this.updateLatencyMetrics(metrics, latencyMs);

    // 检查是否需要阶段升级或回滚
    this.checkStageProgress();
  }

  /**
   * 获取当前流量分配
   */
  getTrafficAllocation(clientId: string): number {
    if (!this.activeSession) {
      return 0;
    }
    return this.activeSession.currentStage * 100;
  }

  /**
   * 应该使用金丝雀版本吗
   */
  shouldUseCanary(clientId: string): boolean {
    if (!this.activeSession) {
      return false;
    }

    const canaryPercentage = this.activeSession.currentStage * 100;
    const clientHash = this.hashClientId(clientId) % 100;

    return clientHash < canaryPercentage;
  }

  /**
   * 获取部署状态
   */
  getDeployStatus(): DeploySession | null {
    return this.activeSession;
  }

  /**
   * 手动推进到下一阶段
   */
  async advanceStage(): Promise<void> {
    if (!this.activeSession) {
      throw new Error('No active deployment');
    }

    const currentIndex = this.config.stages.indexOf(this.activeSession.currentStage);
    if (currentIndex === -1 || currentIndex >= this.config.stages.length - 1) {
      throw new Error('Already at final stage');
    }

    const nextStage = this.config.stages[currentIndex + 1];
    this.activeSession.currentStage = nextStage;
    this.activeSession.stageStartedAt = Date.now();
    this.activeSession.stageMetrics = this.createEmptyMetrics();
    this.activeSession.status = 'monitoring';

    console.log(`[Canary Deployer] ➡️ Stage advanced to ${nextStage * 100}%`);

    // 发送阶段推进通知
    await this.notifyStageAdvance(this.activeSession);
  }

  /**
   * 执行回滚
   */
  async rollback(reason: string): Promise<void> {
    if (!this.activeSession) {
      throw new Error('No active deployment to rollback');
    }

    this.activeSession.status = 'rolled_back';
    this.activeSession.rollbackReason = reason;

    console.log(`[Canary Deployer] ⚠️ Rollback executed: ${reason}`);

    // 发送回滚通知
    await this.notifyRollback(this.activeSession, reason);

    // 清理会话
    this.activeSession = null;
  }

  /**
   * 完成部署
   */
  async completeDeploy(): Promise<DeployResult> {
    if (!this.activeSession) {
      throw new Error('No active deployment');
    }

    this.activeSession.status = 'completed';
    const result: DeployResult = {
      status: 'completed',
      finalStage: this.activeSession.currentStage,
      durationMinutes: (Date.now() - this.activeSession.startedAt) / 60000,
      finalMetrics: this.activeSession.cumulativeMetrics,
    };

    console.log(`[Canary Deployer] ✅ Deploy completed: ${this.activeSession.id}`);

    // 发送完成通知
    await this.notifyDeployComplete(this.activeSession);

    this.activeSession = null;
    return result;
  }

  // ============== 私有方法 ==============

  private createEmptyMetrics(): DeployMetrics {
    return {
      totalRequests: 0,
      successfulRequests: 0,
      failedRequests: 0,
      avgLatencyMs: 0,
      p95LatencyMs: 0,
      p99LatencyMs: 0,
      successRate: 0,
      errorRate: 0,
    };
  }

  private updateLatencyMetrics(metrics: DeployMetrics, latencyMs: number): void {
    // 简单移动平均
    const count = metrics.totalRequests;
    metrics.avgLatencyMs =
      (metrics.avgLatencyMs * (count - 1) + latencyMs) / count;

    // 简化版 P95/P99 (实际应使用直方图)
    metrics.p95LatencyMs = Math.max(metrics.p95LatencyMs, latencyMs * 0.95);
    metrics.p99LatencyMs = Math.max(metrics.p99LatencyMs, latencyMs * 0.99);

    // 更新成功率/错误率
    metrics.successRate = metrics.successfulRequests / metrics.totalRequests;
    metrics.errorRate = metrics.failedRequests / metrics.totalRequests;
  }

  private checkStageProgress(): void {
    if (!this.activeSession) {
      return;
    }

    const metrics = this.activeSession.stageMetrics;
    const elapsedMinutes = (Date.now() - this.activeSession.stageStartedAt) / 60000;

    // 检查是否达到阶段持续时间
    if (elapsedMinutes < this.config.stageDurationMinutes) {
      return;
    }

    // 检查指标是否达标
    if (metrics.successRate < this.config.successRateThreshold) {
      if (this.config.autoRollbackEnabled) {
        this.rollback(`Success rate ${metrics.successRate.toFixed(2)} below threshold ${this.config.successRateThreshold}`);
      } else {
        this.activeSession.status = 'failed';
      }
      return;
    }

    if (metrics.errorRate > this.config.errorRateThreshold) {
      if (this.config.autoRollbackEnabled) {
        this.rollback(`Error rate ${metrics.errorRate.toFixed(2)} above threshold ${this.config.errorRateThreshold}`);
      } else {
        this.activeSession.status = 'failed';
      }
      return;
    }

    // 指标正常，尝试推进阶段
    const currentIndex = this.config.stages.indexOf(this.activeSession.currentStage);
    if (currentIndex < this.config.stages.length - 1) {
      this.advanceStage();
    } else {
      this.completeDeploy();
    }
  }

  private hashClientId(clientId: string): number {
    let hash = 0;
    for (let i = 0; i < clientId.length; i++) {
      hash = ((hash << 5) - hash) + clientId.charCodeAt(i);
      hash = hash & hash;
    }
    return Math.abs(hash) % 100;
  }

  private async notifyDeployStart(session: DeploySession): Promise<void> {
    const message = this.mcpBus.createDeployRequest(
      `deploy:${session.version}`,
      session.currentStage,
      'canary-deployer',
      'governance-controller'
    );
    await this.mcpBus.send(message);
  }

  private async notifyStageAdvance(session: DeploySession): Promise<void> {
    console.log(`[Canary Deployer] 📊 Stage metrics: ${JSON.stringify(session.stageMetrics)}`);
  }

  private async notifyRollback(session: DeploySession, reason: string): Promise<void> {
    console.error(`[Canary Deployer] 🚨 Rollback: ${reason}`);
  }

  private async notifyDeployComplete(session: DeploySession): Promise<void> {
    console.log(`[Canary Deployer] 🎉 Deploy completed successfully`);
  }
}

// ============== 导出 ==============

export default CanaryDeployer;
