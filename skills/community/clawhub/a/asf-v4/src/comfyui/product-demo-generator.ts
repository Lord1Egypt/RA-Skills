/**
 * 产品演示视频生成器
 * 
 * 层级：Layer 6 - System Architecture Layer
 * 功能：从 PRD/产品描述自动生成产品演示视频
 * 版本：V1.0.0
 * 状态：🟡 开发中
 */

import { VideoGenerationRequest } from './comfyui-workflow-orchestrator';
import { VideoGenerationSkill } from './video-generation-skill';
import { MCPVideoBus } from './mcp-video-bus';

// ============== 类型定义 ==============

/**
 * 产品信息
 */
export interface ProductInfo {
  /** 产品名称 */
  name: string;
  /** 产品描述 */
  description: string;
  /** 核心功能 */
  features: string[];
  /** 目标用户 */
  targetAudience?: string;
  /** 使用场景 */
  useCases?: string[];
  /** 品牌色调 */
  brandColor?: string;
  /** Logo 路径 */
  logoPath?: string;
}

/**
 * 演示视频配置
 */
export interface DemoVideoConfig {
  /** 视频时长 (秒) */
  durationSeconds: number;
  /** 视频风格 */
  style: 'professional' | 'casual' | 'energetic' | 'minimalist';
  /** 旁白语言 */
  language: 'zh-CN' | 'en-US' | 'ja-JP';
  /** 背景音乐 */
  backgroundMusic: boolean;
  /** 显示字幕 */
  showSubtitles: boolean;
  /** 宽高比 */
  aspectRatio: '16:9' | '9:16' | '1:1';
  /** 分辨率 */
  resolution: '480P' | '720P' | '1080P';
}

/**
 * 演示视频场景
 */
export interface DemoScene {
  /** 场景序号 */
  sequence: number;
  /** 场景描述 */
  description: string;
  /** 展示功能 */
  feature?: string;
  /** 视觉提示 */
  visualPrompt: string;
  /** 预计时长 (秒) */
  durationSeconds: number;
}

/**
 * 生成任务
 */
export interface DemoGenerationTask {
  /** 任务 ID */
  taskId: string;
  /** 产品信息 */
  product: ProductInfo;
  /** 视频配置 */
  config: DemoVideoConfig;
  /** 生成场景 */
  scenes: DemoScene[];
  /** 创建时间 */
  createdAt: number;
  /** 状态 */
  status: 'pending' | 'generating' | 'completed' | 'failed';
}

/**
 * 生成结果
 */
export interface DemoGenerationResult {
  /** 任务 ID */
  taskId: string;
  /** 状态 */
  status: 'success' | 'failed' | 'partial';
  /** 生成的视频路径 */
  videoPaths: string[];
  /** 合并后的视频路径 */
  mergedVideoPath?: string;
  /** 生成耗时 (秒) */
  durationSeconds: number;
  /** 错误信息 */
  errors?: string[];
  /** 元数据 */
  metadata: {
    totalScenes: number;
    successfulScenes: number;
    failedScenes: number;
    totalDuration: number;
  };
}

// ============== 默认配置 ==============

const DEFAULT_VIDEO_CONFIG: DemoVideoConfig = {
  durationSeconds: 30,
  style: 'professional',
  language: 'zh-CN',
  backgroundMusic: true,
  showSubtitles: true,
  aspectRatio: '16:9',
  resolution: '1080P',
};

const STYLE_PROMPTS: Record<DemoVideoConfig['style'], string> = {
  professional: 'professional, clean, corporate style, high quality, polished',
  casual: 'casual, friendly, approachable, warm colors, relaxed',
  energetic: 'energetic, dynamic, vibrant, fast-paced, exciting',
  minimalist: 'minimalist, simple, elegant, clean lines, subtle',
};

// ============== 核心类 ==============

/**
 * 产品演示视频生成器
 */
export class ProductDemoGenerator {
  private videoSkill: VideoGenerationSkill;
  private mcpBus: MCPVideoBus;

  constructor(videoSkill: VideoGenerationSkill, mcpBus: MCPVideoBus) {
    this.videoSkill = videoSkill;
    this.mcpBus = mcpBus;
  }

  /**
   * 从产品信息生成演示视频
   */
  async generateDemo(
    product: ProductInfo,
    config: Partial<DemoVideoConfig> = {}
  ): Promise<DemoGenerationResult> {
    const startTime = Date.now();
    const taskId = `demo_${product.name.replace(/\s+/g, '_')}_${Date.now()}`;

    const fullConfig: DemoVideoConfig = {
      ...DEFAULT_VIDEO_CONFIG,
      ...config,
    };

    try {
      // 1. 分析产品并生成场景
      const scenes = this.analyzeProductAndGenerateScenes(product, fullConfig);

      // 2. 创建生成任务
      const task: DemoGenerationTask = {
        taskId,
        product,
        config: fullConfig,
        scenes,
        createdAt: Date.now(),
        status: 'generating',
      };

      // 3. 发送任务开始通知
      await this.notifyTaskStart(task);

      // 4. 并行生成所有场景视频
      const sceneResults = await this.generateScenes(task);

      // 5. 合并场景视频 (模拟)
      const mergedPath = await this.mergeSceneVideos(sceneResults);

      // 6. 计算结果
      const successfulScenes = sceneResults.filter(r => r.status === 'success');
      const failedScenes = sceneResults.filter(r => r.status === 'failed');

      const result: DemoGenerationResult = {
        taskId,
        status: failedScenes.length === 0 ? 'success' : 'partial',
        videoPaths: successfulScenes.map(r => r.videoPath),
        mergedVideoPath: mergedPath,
        durationSeconds: (Date.now() - startTime) / 1000,
        errors: failedScenes.map(r => r.error!).filter(Boolean),
        metadata: {
          totalScenes: scenes.length,
          successfulScenes: successfulScenes.length,
          failedScenes: failedScenes.length,
          totalDuration: successfulScenes.reduce((sum, r) => sum + r.duration, 0),
        },
      };

      // 7. 发送完成通知
      await this.notifyTaskComplete(result);

      return result;
    } catch (error) {
      return {
        taskId,
        status: 'failed',
        videoPaths: [],
        durationSeconds: (Date.now() - startTime) / 1000,
        errors: [error instanceof Error ? error.message : 'Unknown error'],
        metadata: {
          totalScenes: 0,
          successfulScenes: 0,
          failedScenes: 0,
          totalDuration: 0,
        },
      };
    }
  }

  /**
   * 分析产品并生成场景
   */
  private analyzeProductAndGenerateScenes(
    product: ProductInfo,
    config: DemoVideoConfig
  ): DemoScene[] {
    const scenes: DemoScene[] = [];
    const totalDuration = config.durationSeconds;
    const featureCount = product.features.length;
    const durationPerFeature = Math.floor(totalDuration / (featureCount + 2)); // +2 for intro/outro

    // 场景 1: 开场介绍
    scenes.push({
      sequence: 1,
      description: `介绍${product.name}，${product.description.substring(0, 50)}...`,
      visualPrompt: this.createVisualPrompt(
        `Product introduction: ${product.name}, ${product.description}`,
        config.style,
        'intro'
      ),
      durationSeconds: durationPerFeature,
    });

    // 场景 2-N: 功能展示
    product.features.forEach((feature, index) => {
      scenes.push({
        sequence: index + 2,
        description: `展示功能：${feature}`,
        feature,
        visualPrompt: this.createVisualPrompt(
          `Feature demonstration: ${feature} for ${product.name}`,
          config.style,
          'feature'
        ),
        durationSeconds: durationPerFeature,
      });
    });

    // 场景 N+1: 结尾呼吁
    scenes.push({
      sequence: product.features.length + 2,
      description: '结尾：呼吁行动',
      visualPrompt: this.createVisualPrompt(
        `Call to action: Try ${product.name} today`,
        config.style,
        'outro'
      ),
      durationSeconds: durationPerFeature,
    });

    return scenes;
  }

  /**
   * 创建视觉提示
   */
  private createVisualPrompt(
    basePrompt: string,
    style: DemoVideoConfig['style'],
    sceneType: 'intro' | 'feature' | 'outro'
  ): string {
    const stylePrompt = STYLE_PROMPTS[style];
    const typePrompts = {
      intro: 'opening scene, title card, professional introduction',
      feature: 'screen recording, UI demonstration, feature highlight',
      outro: 'closing scene, contact information, call to action',
    };

    return `${basePrompt}, ${stylePrompt}, ${typePrompts[sceneType]}, high quality, 4k`;
  }

  /**
   * 生成所有场景
   */
  private async generateScenes(
    task: DemoGenerationTask
  ): Promise<Array<{ status: 'success' | 'failed'; videoPath: string; duration: number; error?: string }>> {
    const results: Array<{ status: 'success' | 'failed'; videoPath: string; duration: number; error?: string }> = [];

    for (const scene of task.scenes) {
      try {
        // 创建视频生成请求
        const request: VideoGenerationRequest = {
          prompt: scene.visualPrompt,
          durationSeconds: scene.durationSeconds,
          resolution: task.config.resolution,
          aspectRatio: task.config.aspectRatio,
        };

        // 提交任务到视频生成技能
        const skillTask = {
          id: `${task.taskId}_scene_${scene.sequence}`,
          description: scene.description,
          priority: 5,
          request,
          clientId: 'product-demo-generator',
          createdAt: Date.now(),
          retryCount: 0,
          maxRetries: 2,
        };

        const submitResult = this.videoSkill.submitTask(skillTask);

        if (submitResult.success) {
          // 模拟等待生成完成
          await new Promise(resolve => setTimeout(resolve, 2000));

          results.push({
            status: 'success',
            videoPath: `/videos/${task.taskId}_scene_${scene.sequence}.mp4`,
            duration: scene.durationSeconds,
          });
        } else {
          results.push({
            status: 'failed',
            videoPath: '',
            duration: 0,
            error: submitResult.message,
          });
        }
      } catch (error) {
        results.push({
          status: 'failed',
          videoPath: '',
          duration: 0,
          error: error instanceof Error ? error.message : 'Unknown error',
        });
      }
    }

    return results;
  }

  /**
   * 合并场景视频 (模拟)
   */
  private async mergeSceneVideos(
    sceneResults: Array<{ status: string; videoPath: string; duration: number }>
  ): Promise<string | undefined> {
    const successfulPaths = sceneResults
      .filter(r => r.status === 'success')
      .map(r => r.videoPath);

    if (successfulPaths.length === 0) {
      return undefined;
    }

    // 模拟视频合并 (实际应调用视频处理服务)
    return `/videos/merged_${Date.now()}.mp4`;
  }

  /**
   * 发送任务开始通知
   */
  private async notifyTaskStart(task: DemoGenerationTask): Promise<void> {
    const message = this.mcpBus.createGenerateRequest(
      {
        prompt: `Generate product demo for ${task.product.name}`,
        durationSeconds: task.config.durationSeconds,
      },
      'product-demo-generator',
      'video-production-agent'
    );
    await this.mcpBus.send(message);
  }

  /**
   * 发送任务完成通知
   */
  private async notifyTaskComplete(result: DemoGenerationResult): Promise<void> {
    console.log(
      `[Product Demo Generator] ✅ Task completed: ${result.taskId}, ` +
        `${result.metadata.successfulScenes}/${result.metadata.totalScenes} scenes successful`
    );
  }
}

// ============== 导出 ==============

export default ProductDemoGenerator;
