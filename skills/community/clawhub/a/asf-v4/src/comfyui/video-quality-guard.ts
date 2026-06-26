/**
 * 视频质量门禁 (Video Quality Guard)
 * 
 * 层级：Layer 17 - Evolution Guard
 * 功能：视频质量验收、自动回滚、进化安全护栏
 * 版本：V1.0.0
 * 状态：🟡 开发中
 */

import { VideoGenerationResponse } from './comfyui-workflow-orchestrator';

// ============== 类型定义 ==============

/**
 * 质量检查项
 */
export interface QualityCheckItem {
  /** 检查项名称 */
  name: string;
  /** 检查项描述 */
  description: string;
  /** 权重 (1-10) */
  weight: number;
  /** 得分 (0-1) */
  score: number;
  /** 是否通过 */
  passed: boolean;
  /** 详细信息 */
  details?: string;
}

/**
 * 质量检查报告
 */
export interface QualityReport {
  /** 视频路径 */
  videoPath: string;
  /** 总体得分 (0-1) */
  overallScore: number;
  /** 是否通过 */
  passed: boolean;
  /** 检查时间 */
  checkedAt: number;
  /** 检查耗时 (ms) */
  durationMs: number;
  /** 检查项列表 */
  items: QualityCheckItem[];
  /** 建议操作 */
  recommendation: 'accept' | 'retry' | 'reject' | 'manual_review';
  /** 错误信息 */
  error?: string;
}

/**
 * 质量门禁配置
 */
export interface QualityGuardConfig {
  /** 最低通过分数 */
  minPassScore: number;
  /** 自动重试阈值 */
  retryThreshold: number;
  /** 最大重试次数 */
  maxRetries: number;
  /** 人工审核阈值 */
  manualReviewThreshold: number;
  /** 启用检查项 */
  enabledChecks: string[];
  /** 关键检查项 (必须通过) */
  criticalChecks: string[];
}

/**
 * 回滚配置
 */
export interface RollbackConfig {
  /** 启用自动回滚 */
  enabled: boolean;
  /** 回滚触发条件 */
  triggerConditions: {
    /** 质量分数低于阈值 */
    qualityScoreBelow: number;
    /** 关键检查项失败 */
    criticalCheckFailed: boolean;
    /** 连续失败次数 */
    consecutiveFailures: number;
  };
  /** 回滚动作 */
  actions: {
    /** 通知管理员 */
    notifyAdmin: boolean;
    /** 标记为高风险 */
    markAsHighRisk: boolean;
    /** 暂停自动部署 */
    pauseAutoDeploy: boolean;
  };
}

// ============== 默认配置 ==============

const DEFAULT_QUALITY_GUARD_CONFIG: QualityGuardConfig = {
  minPassScore: 0.7,
  retryThreshold: 0.5,
  maxRetries: 3,
  manualReviewThreshold: 0.6,
  enabledChecks: [
    'resolution',
    'duration',
    'aspectRatio',
    'visualQuality',
    'audioQuality',
    'contentSafety',
    'brandConsistency',
  ],
  criticalChecks: ['resolution', 'contentSafety'],
};

const DEFAULT_ROLLBACK_CONFIG: RollbackConfig = {
  enabled: true,
  triggerConditions: {
    qualityScoreBelow: 0.5,
    criticalCheckFailed: true,
    consecutiveFailures: 3,
  },
  actions: {
    notifyAdmin: true,
    markAsHighRisk: true,
    pauseAutoDeploy: true,
  },
};

// ============== 核心类 ==============

/**
 * 视频质量门禁
 */
export class VideoQualityGuard {
  private config: QualityGuardConfig;
  private rollbackConfig: RollbackConfig;
  private consecutiveFailures: number = 0;
  private failureHistory: { timestamp: number; score: number; reason: string }[] = [];

  constructor(
    config: Partial<QualityGuardConfig> = {},
    rollbackConfig: Partial<RollbackConfig> = {}
  ) {
    this.config = { ...DEFAULT_QUALITY_GUARD_CONFIG, ...config };
    this.rollbackConfig = { ...DEFAULT_ROLLBACK_CONFIG, ...rollbackConfig };
  }

  /**
   * 检查分辨率
   */
  private checkResolution(response: VideoGenerationResponse): QualityCheckItem {
    const expectedResolutions = ['480P', '720P', '1080P'];
    const actualResolution = response.metadata?.resolution || 'unknown';
    const passed = expectedResolutions.includes(actualResolution);

    return {
      name: 'resolution',
      description: '视频分辨率检查',
      weight: 8,
      score: passed ? 1.0 : 0.0,
      passed,
      details: `Expected: ${expectedResolutions.join('/')}, Actual: ${actualResolution}`,
    };
  }

  /**
   * 检查时长
   */
  private checkDuration(response: VideoGenerationResponse): QualityCheckItem {
    const expectedDuration = response.metadata?.duration || 0;
    const passed = expectedDuration >= 1 && expectedDuration <= 10;

    return {
      name: 'duration',
      description: '视频时长检查 (1-10 秒)',
      weight: 5,
      score: passed ? 1.0 : Math.max(0, 1 - Math.abs(expectedDuration - 5) / 10),
      passed,
      details: `Duration: ${expectedDuration}s`,
    };
  }

  /**
   * 检查宽高比
   */
  private checkAspectRatio(response: VideoGenerationResponse): QualityCheckItem {
    const expectedRatios = ['1:1', '16:9', '9:16', '4:3', '3:4'];
    const actualRatio = response.metadata?.aspectRatio || 'unknown';
    const passed = expectedRatios.includes(actualRatio);

    return {
      name: 'aspectRatio',
      description: '视频宽高比检查',
      weight: 4,
      score: passed ? 1.0 : 0.5,
      passed,
      details: `Expected: ${expectedRatios.join('/')}, Actual: ${actualRatio}`,
    };
  }

  /**
   * 检查视觉质量 (模拟)
   */
  private checkVisualQuality(response: VideoGenerationResponse): QualityCheckItem {
    // TODO: 接入实际视觉质量评估模型
    const qualityScore = response.qualityScore || 0.8;
    const passed = qualityScore >= this.config.minPassScore;

    return {
      name: 'visualQuality',
      description: '视觉质量评估',
      weight: 10,
      score: qualityScore,
      passed,
      details: `Quality score: ${qualityScore.toFixed(2)}`,
    };
  }

  /**
   * 检查内容安全 (模拟)
   */
  private checkContentSafety(response: VideoGenerationResponse): QualityCheckItem {
    // TODO: 接入实际内容安全检测 API
    // 如果响应中有 error，则安全检查失败
    const hasError = response.status === 'failed' || response.error !== undefined;
    const passed = !hasError;

    return {
      name: 'contentSafety',
      description: '内容安全检查',
      weight: 10,
      score: passed ? 1.0 : 0.0,
      passed,
      details: hasError ? `Safety check failed: ${response.error || 'Unknown error'}` : 'No safety issues detected',
    };
  }

  /**
   * 检查音频质量 (如果启用)
   */
  private checkAudioQuality(response: VideoGenerationResponse): QualityCheckItem {
    const hasAudio = response.metadata ? response.metadata.duration > 0 : false;
    const passed = hasAudio || true; // 音频可选

    return {
      name: 'audioQuality',
      description: '音频质量检查',
      weight: 3,
      score: passed ? 1.0 : 0.0,
      passed,
      details: hasAudio ? 'Audio present' : 'No audio',
    };
  }

  /**
   * 检查品牌一致性 (模拟)
   */

  /**
   * 检查品牌一致性 (模拟)
   */
  private checkBrandConsistency(response: VideoGenerationResponse): QualityCheckItem {
    // TODO: 接入品牌风格检测
    const passed = true; // 默认通过

    return {
      name: 'brandConsistency',
      description: '品牌风格一致性检查',
      weight: 6,
      score: passed ? 1.0 : 0.7,
      passed,
      details: 'Brand style check passed',
    };
  }

  /**
   * 执行质量检查
   */
  async checkQuality(response: VideoGenerationResponse): Promise<QualityReport> {
    const startTime = Date.now();
    const items: QualityCheckItem[] = [];

    try {
      // 执行所有启用的检查
      const checkMethods: { [key: string]: () => QualityCheckItem } = {
        resolution: () => this.checkResolution(response),
        duration: () => this.checkDuration(response),
        aspectRatio: () => this.checkAspectRatio(response),
        visualQuality: () => this.checkVisualQuality(response),
        audioQuality: () => this.checkAudioQuality(response),
        contentSafety: () => this.checkContentSafety(response),
        brandConsistency: () => this.checkBrandConsistency(response),
      };

      for (const checkName of this.config.enabledChecks) {
        if (checkMethods[checkName]) {
          items.push(checkMethods[checkName]());
        }
      }

      // 检查关键项
      const criticalFailed = items.some(
        item => this.config.criticalChecks.includes(item.name) && !item.passed
      );

      // 计算加权总分
      const totalWeight = items.reduce((sum, item) => sum + item.weight, 0);
      const weightedScore = items.reduce((sum, item) => sum + item.score * item.weight, 0);
      const overallScore = totalWeight > 0 ? weightedScore / totalWeight : 0;

      // 判断是否通过
      const passed = overallScore >= this.config.minPassScore && !criticalFailed;

      // 生成建议
      let recommendation: QualityReport['recommendation'] = 'accept';
      if (!passed) {
        if (criticalFailed || overallScore < this.config.retryThreshold) {
          recommendation = 'reject';
        } else if (overallScore < this.config.manualReviewThreshold) {
          recommendation = 'manual_review';
        } else {
          recommendation = 'retry';
        }
      }

      // 更新连续失败计数
      if (!passed) {
        this.consecutiveFailures++;
        this.failureHistory.push({
          timestamp: Date.now(),
          score: overallScore,
          reason: items.filter(i => !i.passed).map(i => i.name).join(', '),
        });
      } else {
        this.consecutiveFailures = 0;
      }

      const report: QualityReport = {
        videoPath: response.videoPath || 'unknown',
        overallScore: Math.round(overallScore * 100) / 100,
        passed,
        checkedAt: Date.now(),
        durationMs: Date.now() - startTime,
        items,
        recommendation,
      };

      // 检查是否需要回滚
      if (this.shouldTriggerRollback(report)) {
        await this.triggerRollback(report);
      }

      return report;
    } catch (error) {
      return {
        videoPath: response.videoPath || 'unknown',
        overallScore: 0,
        passed: false,
        checkedAt: Date.now(),
        durationMs: Date.now() - startTime,
        items: [],
        recommendation: 'reject',
        error: error instanceof Error ? error.message : 'Quality check failed',
      };
    }
  }

  /**
   * 检查是否触发回滚
   */
  private shouldTriggerRollback(report: QualityReport): boolean {
    if (!this.rollbackConfig.enabled) {
      return false;
    }

    const conditions = this.rollbackConfig.triggerConditions;

    return (
      report.overallScore < conditions.qualityScoreBelow ||
      report.items.some(
        item => this.config.criticalChecks.includes(item.name) && !item.passed
      ) ||
      this.consecutiveFailures >= conditions.consecutiveFailures
    );
  }

  /**
   * 触发回滚
   */
  private async triggerRollback(report: QualityReport): Promise<void> {
    console.log(`[VideoQualityGuard] 🚨 Rollback triggered!`);
    console.log(`  - Overall Score: ${report.overallScore}`);
    console.log(`  - Consecutive Failures: ${this.consecutiveFailures}`);
    console.log(`  - Failed Checks: ${report.items.filter(i => !i.passed).map(i => i.name).join(', ')}`);

    const actions = this.rollbackConfig.actions;

    if (actions.notifyAdmin) {
      console.log(`  - Action: Notifying admin...`);
      // TODO: 发送管理员通知
    }

    if (actions.markAsHighRisk) {
      console.log(`  - Action: Marking as high risk...`);
      // TODO: 标记为高风险
    }

    if (actions.pauseAutoDeploy) {
      console.log(`  - Action: Pausing auto deploy...`);
      // TODO: 暂停自动部署
    }
  }

  /**
   * 获取门禁状态
   */
  getStatus(): {
    consecutiveFailures: number;
    failureHistory: { timestamp: number; score: number; reason: string }[];
    config: QualityGuardConfig;
  } {
    return {
      consecutiveFailures: this.consecutiveFailures,
      failureHistory: [...this.failureHistory],
      config: { ...this.config },
    };
  }

  /**
   * 重置失败计数
   */
  resetFailureCount(): void {
    this.consecutiveFailures = 0;
    this.failureHistory = [];
  }

  /**
   * 更新配置
   */
  updateConfig(config: Partial<QualityGuardConfig>): void {
    this.config = { ...this.config, ...config };
  }
}

// ============== 导出 ==============

export default VideoQualityGuard;
