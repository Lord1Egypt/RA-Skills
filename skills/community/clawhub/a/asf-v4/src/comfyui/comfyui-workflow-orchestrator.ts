/**
 * ComfyUI 工作流编排器
 * 
 * 层级：Layer 6 - System Architecture Layer
 * 功能：ComfyUI 工作流编排、视频生成管道、多媒体资产管理
 * 版本：V1.0.0
 * 状态：🟡 开发中
 */

import { video_generate } from '@openclaw/core';

// ============== 类型定义 ==============

/**
 * 视频生成请求参数
 */
export interface VideoGenerationRequest {
  /** 生成提示词 */
  prompt: string;
  /** 参考图片路径 (可选) */
  image?: string;
  /** 参考图片数组 (可选，最多 5 张) */
  images?: string[];
  /** 参考视频路径 (可选) */
  video?: string;
  /** 参考视频数组 (可选，最多 4 个) */
  videos?: string[];
  /** 目标时长 (秒) */
  durationSeconds?: number;
  /** 分辨率 (480P|720P|1080P) */
  resolution?: '480P' | '720P' | '1080P';
  /** 宽高比 */
  aspectRatio?: '1:1' | '2:3' | '3:2' | '3:4' | '4:3' | '4:5' | '5:4' | '9:16' | '16:9' | '21:9';
  /** 尺寸 (如 1280x720) */
  size?: string;
  /** 模型 override */
  model?: string;
  /** 是否启用音频 */
  audio?: boolean;
  /** 是否添加水印 */
  watermark?: boolean;
  /** 输出文件名 */
  filename?: string;
}

/**
 * 视频生成响应
 */
export interface VideoGenerationResponse {
  /** 生成状态 */
  status: 'success' | 'failed' | 'pending';
  /** 视频路径 (成功时) */
  videoPath?: string;
  /** 错误信息 (失败时) */
  error?: string;
  /** 生成耗时 (ms) */
  durationMs?: number;
  /** 成本估算 (USD) */
  costEstimate?: number;
  /** 质量评分 (0-1) */
  qualityScore?: number;
  /** 元数据 */
  metadata?: {
    model: string;
    resolution: string;
    duration: number;
    aspectRatio: string;
  };
}

/**
 * 治理门禁配置
 */
export interface GovernanceConfig {
  /** 最大时长 (秒) */
  maxDurationSeconds: number;
  /** 最大分辨率 */
  maxResolution: '480P' | '720P' | '1080P';
  /** 最大生成时间 (秒) */
  maxGenerationTimeSeconds: number;
  /** 最小质量评分 */
  minQualityScore: number;
  /** 单次成本预算 (USD) */
  maxCostPerRequest: number;
  /** 每分钟请求限制 */
  requestsPerMinute: number;
  /** 每日配额 */
  dailyQuota: number;
}

/**
 * 沙箱配置
 */
export interface SandboxConfig {
  /** 内存限制 (MB) */
  memoryLimitMB: number;
  /** 超时时间 (秒) */
  timeoutSeconds: number;
  /** GPU 隔离 */
  gpuIsolated: boolean;
  /** 允许的 API */
  allowedApis: string[];
  /** 禁止的 API */
  deniedApis: string[];
}

// ============== 默认配置 ==============

const DEFAULT_GOVERNANCE_CONFIG: GovernanceConfig = {
  maxDurationSeconds: 10,
  maxResolution: '1080P',
  maxGenerationTimeSeconds: 60,
  minQualityScore: 0.7,
  maxCostPerRequest: 0.1,
  requestsPerMinute: 10,
  dailyQuota: 100,
};

const DEFAULT_SANDBOX_CONFIG: SandboxConfig = {
  memoryLimitMB: 512,
  timeoutSeconds: 60,
  gpuIsolated: true,
  allowedApis: ['video_generate'],
  deniedApis: ['external_upload'],
};

// ============== 核心类 ==============

/**
 * ComfyUI 工作流编排器
 */
export class ComfyUIWorkflowOrchestrator {
  private governanceConfig: GovernanceConfig;
  private sandboxConfig: SandboxConfig;
  private requestCount: Map<string, number> = new Map();
  private dailyQuotaUsed: number = 0;
  private lastResetTime: number = Date.now();

  constructor(
    governanceConfig: Partial<GovernanceConfig> = {},
    sandboxConfig: Partial<SandboxConfig> = {}
  ) {
    this.governanceConfig = { ...DEFAULT_GOVERNANCE_CONFIG, ...governanceConfig };
    this.sandboxConfig = { ...DEFAULT_SANDBOX_CONFIG, ...sandboxConfig };
  }

  /**
   * 验证生成请求
   */
  public validateRequest(request: VideoGenerationRequest): { valid: boolean; errors: string[] } {
    const errors: string[] = [];

    // 提示词验证
    if (!request.prompt || request.prompt.trim().length === 0) {
      errors.push('Prompt is required');
    }

    // 时长验证
    if (request.durationSeconds !== undefined) {
      if (request.durationSeconds > this.governanceConfig.maxDurationSeconds) {
        errors.push(`Duration exceeds maximum (${this.governanceConfig.maxDurationSeconds}s)`);
      }
      if (request.durationSeconds < 1) {
        errors.push('Duration must be at least 1 second');
      }
    }

    // 分辨率验证
    if (request.resolution !== undefined) {
      const resolutionOrder = { '480P': 1, '720P': 2, '1080P': 3 };
      const requestedLevel = resolutionOrder[request.resolution];
      const maxLevel = resolutionOrder[this.governanceConfig.maxResolution];
      if (requestedLevel > maxLevel) {
        errors.push(`Resolution exceeds maximum (${this.governanceConfig.maxResolution})`);
      }
    }

    // 图片数量验证
    if (request.images && request.images.length > 5) {
      errors.push('Maximum 5 images allowed');
    }

    // 视频数量验证
    if (request.videos && request.videos.length > 4) {
      errors.push('Maximum 4 videos allowed');
    }

    return {
      valid: errors.length === 0,
      errors,
    };
  }

  /**
   * 检查速率限制
   */
  public checkRateLimit(clientId: string): { allowed: boolean; reason?: string } {
    const now = Date.now();
    
    // 重置每日配额 (每 24 小时)
    if (now - this.lastResetTime > 24 * 60 * 60 * 1000) {
      this.dailyQuotaUsed = 0;
      this.requestCount.clear();
      this.lastResetTime = now;
    }

    // 检查每日配额
    if (this.dailyQuotaUsed >= this.governanceConfig.dailyQuota) {
      return { allowed: false, reason: 'Daily quota exceeded' };
    }

    // 检查每分钟请求限制
    const minuteKey = `${clientId}-${Math.floor(now / 60000)}`;
    const count = this.requestCount.get(minuteKey) || 0;
    if (count >= this.governanceConfig.requestsPerMinute) {
      return { allowed: false, reason: 'Rate limit exceeded (requests per minute)' };
    }

    return { allowed: true };
  }

  /**
   * 估算成本
   */
  public estimateCost(request: VideoGenerationRequest): number {
    // 基础成本
    let cost = 0.02;

    // 分辨率系数
    const resolutionMultipliers = { '480P': 1.0, '720P': 1.5, '1080P': 2.0 };
    if (request.resolution) {
      cost *= resolutionMultipliers[request.resolution];
    }

    // 时长系数
    if (request.durationSeconds) {
      cost *= (request.durationSeconds / 5); // 基准 5 秒
    }

    // 音频系数
    if (request.audio) {
      cost *= 1.3;
    }

    return Math.round(cost * 100) / 100;
  }

  /**
   * 执行视频生成
   */
  async generateVideo(request: VideoGenerationRequest, clientId: string = 'default'): Promise<VideoGenerationResponse> {
    const startTime = Date.now();

    try {
      // 1. 验证请求
      const validation = this.validateRequest(request);
      if (!validation.valid) {
        return {
          status: 'failed',
          error: `Validation failed: ${validation.errors.join(', ')}`,
          durationMs: Date.now() - startTime,
        };
      }

      // 2. 检查速率限制
      const rateLimit = this.checkRateLimit(clientId);
      if (!rateLimit.allowed) {
        return {
          status: 'failed',
          error: `Rate limit: ${rateLimit.reason}`,
          durationMs: Date.now() - startTime,
        };
      }

      // 3. 估算成本
      const costEstimate = this.estimateCost(request);
      if (costEstimate > this.governanceConfig.maxCostPerRequest) {
        return {
          status: 'failed',
          error: `Cost exceeds budget ($${costEstimate} > $${this.governanceConfig.maxCostPerRequest})`,
          durationMs: Date.now() - startTime,
        };
      }

      // 4. 调用 video_generate 工具
      const result = await video_generate({
        action: 'generate',
        prompt: request.prompt,
        image: request.image,
        images: request.images,
        video: request.video,
        videos: request.videos,
        durationSeconds: request.durationSeconds,
        resolution: request.resolution,
        aspectRatio: request.aspectRatio,
        size: request.size,
        model: request.model,
        audio: request.audio,
        watermark: request.watermark,
        filename: request.filename,
      });

      // 5. 更新配额
      const minuteKey = `${clientId}-${Math.floor(Date.now() / 60000)}`;
      this.requestCount.set(minuteKey, (this.requestCount.get(minuteKey) || 0) + 1);
      this.dailyQuotaUsed++;

      // 6. 返回成功响应
      return {
        status: 'success',
        videoPath: result.videoPath,
        durationMs: Date.now() - startTime,
        costEstimate,
        qualityScore: 0.85, // TODO: 实际质量评分
        metadata: {
          model: request.model || 'wan2.6-t2v',
          resolution: request.resolution || '1080P',
          duration: request.durationSeconds || 5,
          aspectRatio: request.aspectRatio || '16:9',
        },
      };
    } catch (error) {
      return {
        status: 'failed',
        error: error instanceof Error ? error.message : 'Unknown error',
        durationMs: Date.now() - startTime,
      };
    }
  }

  /**
   * 获取使用统计
   */
  getUsageStats(): {
    dailyQuotaUsed: number;
    dailyQuotaRemaining: number;
    requestCount: number;
  } {
    return {
      dailyQuotaUsed: this.dailyQuotaUsed,
      dailyQuotaRemaining: this.governanceConfig.dailyQuota - this.dailyQuotaUsed,
      requestCount: Array.from(this.requestCount.values()).reduce((a, b) => a + b, 0),
    };
  }

  /**
   * 重置配额 (管理员操作)
   */
  resetQuota(): void {
    this.dailyQuotaUsed = 0;
    this.requestCount.clear();
    this.lastResetTime = Date.now();
  }
}

// ============== 导出 ==============

export default ComfyUIWorkflowOrchestrator;
