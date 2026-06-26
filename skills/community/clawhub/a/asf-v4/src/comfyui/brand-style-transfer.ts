/**
 * 品牌风格迁移引擎
 * 
 * 层级：Layer 6 - System Architecture Layer
 * 功能：将品牌视觉风格应用到生成的视频
 * 版本：V1.0.0
 * 状态：🟡 开发中
 */

import { VideoGenerationRequest } from './comfyui-workflow-orchestrator';
import { VideoGenerationSkill } from './video-generation-skill';

// ============== 类型定义 ==============

/**
 * 品牌风格定义
 */
export interface BrandStyle {
  /** 品牌 ID */
  brandId: string;
  /** 品牌名称 */
  brandName: string;
  /** 主色调 */
  primaryColor: string;
  /** 辅助色调 */
  secondaryColors: string[];
  /** 品牌字体 */
  fonts: {
    heading?: string;
    body?: string;
  };
  /** Logo 路径 */
  logoPath?: string;
  /** 风格关键词 */
  styleKeywords: string[];
  /** 视觉规范 */
  visualGuidelines: {
    /** 最小留白 */
    minWhitespace: string;
    /** 圆角大小 */
    cornerRadius: string;
    /** 阴影强度 */
    shadowIntensity: 'none' | 'light' | 'medium' | 'heavy';
    /** 动画风格 */
    animationStyle: 'subtle' | 'moderate' | 'bold';
  };
  /** 禁用元素 */
  forbiddenElements: string[];
}

/**
 * 风格迁移配置
 */
export interface StyleTransferConfig {
  /** 源视频路径 */
  sourceVideoPath: string;
  /** 目标品牌风格 */
  targetBrand: BrandStyle;
  /** 迁移强度 (0-1) */
  transferStrength: number;
  /** 保持内容完整性 */
  preserveContent: boolean;
  /** 添加品牌水印 */
  addWatermark: boolean;
  /** 添加 Logo */
  addLogo: boolean;
  /** 颜色校正 */
  colorCorrection: boolean;
  /** 输出分辨率 */
  outputResolution: '480P' | '720P' | '1080P';
}

/**
 * 风格迁移结果
 */
export interface StyleTransferResult {
  /** 任务 ID */
  taskId: string;
  /** 状态 */
  status: 'success' | 'failed';
  /** 输出视频路径 */
  outputVideoPath?: string;
  /** 预览图路径 */
  thumbnailPath?: string;
  /** 生成耗时 (秒) */
  durationSeconds: number;
  /** 错误信息 */
  error?: string;
  /** 应用的风格 */
  appliedStyle: {
    colorGrading: boolean;
    logoAdded: boolean;
    watermarkAdded: boolean;
    fontApplied: boolean;
  };
}

// ============== 默认配置 ==============

const DEFAULT_BRAND_STYLES: Record<string, BrandStyle> = {
  tech: {
    brandId: 'tech',
    brandName: '科技感',
    primaryColor: '#0066FF',
    secondaryColors: ['#00D4FF', '#7B61FF', '#1A1A2E'],
    fonts: {
      heading: 'Inter',
      body: 'Roboto',
    },
    styleKeywords: ['modern', 'sleek', 'futuristic', 'clean', 'minimal'],
    visualGuidelines: {
      minWhitespace: '24px',
      cornerRadius: '8px',
      shadowIntensity: 'light',
      animationStyle: 'moderate',
    },
    forbiddenElements: ['comic sans', 'neon colors', 'excessive gradients'],
  },
  luxury: {
    brandId: 'luxury',
    brandName: '奢华感',
    primaryColor: '#D4AF37',
    secondaryColors: ['#1A1A1A', '#FFFFFF', '#8B7355'],
    fonts: {
      heading: 'Playfair Display',
      body: 'Lato',
    },
    styleKeywords: ['elegant', 'sophisticated', 'premium', 'refined', 'timeless'],
    visualGuidelines: {
      minWhitespace: '48px',
      cornerRadius: '4px',
      shadowIntensity: 'medium',
      animationStyle: 'subtle',
    },
    forbiddenElements: ['bright colors', 'cartoon effects', 'casual fonts'],
  },
  playful: {
    brandId: 'playful',
    brandName: '活泼感',
    primaryColor: '#FF6B6B',
    secondaryColors: ['#4ECDC4', '#FFE66D', '#95E1D3'],
    fonts: {
      heading: 'Fredoka One',
      body: 'Open Sans',
    },
    styleKeywords: ['fun', 'colorful', 'energetic', 'friendly', 'vibrant'],
    visualGuidelines: {
      minWhitespace: '16px',
      cornerRadius: '16px',
      shadowIntensity: 'medium',
      animationStyle: 'bold',
    },
    forbiddenElements: ['dark themes', 'serious tone', 'rigid layouts'],
  },
};

// ============== 核心类 ==============

/**
 * 品牌风格迁移引擎
 */
export class BrandStyleTransferEngine {
  private videoSkill: VideoGenerationSkill;
  private brandStyles: Map<string, BrandStyle>;

  constructor(videoSkill: VideoGenerationSkill) {
    this.videoSkill = videoSkill;
    this.brandStyles = new Map(Object.entries(DEFAULT_BRAND_STYLES));
  }

  /**
   * 注册品牌风格
   */
  registerBrand(brand: BrandStyle): void {
    this.brandStyles.set(brand.brandId, brand);
  }

  /**
   * 获取品牌风格
   */
  getBrand(brandId: string): BrandStyle | undefined {
    return this.brandStyles.get(brandId);
  }

  /**
   * 执行风格迁移
   */
  async transferStyle(
    config: StyleTransferConfig
  ): Promise<StyleTransferResult> {
    const startTime = Date.now();
    const taskId = `style_transfer_${config.sourceVideoPath.split('/').pop()}_${Date.now()}`;

    try {
      // 1. 验证品牌风格
      if (!this.brandStyles.has(config.targetBrand.brandId)) {
        throw new Error(`Unknown brand: ${config.targetBrand.brandId}`);
      }

      // 2. 验证迁移强度
      if (config.transferStrength < 0 || config.transferStrength > 1) {
        throw new Error('Transfer strength must be between 0 and 1');
      }

      // 3. 生成风格迁移提示
      const transferPrompt = this.createTransferPrompt(config);

      // 4. 创建视频生成请求 (使用参考视频)
      const request: VideoGenerationRequest = {
        prompt: transferPrompt,
        video: config.sourceVideoPath, // 使用源视频作为参考
        durationSeconds: 30, // 实际应从源视频获取
        resolution: config.outputResolution,
        aspectRatio: '16:9',
      };

      // 5. 提交生成任务
      const task = {
        id: taskId,
        description: `Apply ${config.targetBrand.brandName} style`,
        priority: 7,
        request,
        clientId: 'brand-style-transfer',
        createdAt: Date.now(),
        retryCount: 0,
        maxRetries: 2,
      };

      const submitResult = this.videoSkill.submitTask(task);

      if (!submitResult.success) {
        throw new Error(submitResult.message);
      }

      // 6. 模拟等待生成完成
      await new Promise(resolve => setTimeout(resolve, 3000));

      // 7. 构建结果
      const result: StyleTransferResult = {
        taskId,
        status: 'success',
        outputVideoPath: `/videos/styled_${taskId}.mp4`,
        thumbnailPath: `/thumbnails/styled_${taskId}.jpg`,
        durationSeconds: (Date.now() - startTime) / 1000,
        appliedStyle: {
          colorGrading: config.colorCorrection,
          logoAdded: config.addLogo,
          watermarkAdded: config.addWatermark,
          fontApplied: true,
        },
      };

      return result;
    } catch (error) {
      return {
        taskId,
        status: 'failed',
        outputVideoPath: undefined,
        durationSeconds: (Date.now() - startTime) / 1000,
        error: error instanceof Error ? error.message : 'Unknown error',
        appliedStyle: {
          colorGrading: false,
          logoAdded: false,
          watermarkAdded: false,
          fontApplied: false,
        },
      };
    }
  }

  /**
   * 批量应用品牌风格到多个视频
   */
  async batchTransferStyle(
    videoPaths: string[],
    brand: BrandStyle,
    config: Partial<StyleTransferConfig> = {}
  ): Promise<StyleTransferResult[]> {
    const results: StyleTransferResult[] = [];

    for (const videoPath of videoPaths) {
      const result = await this.transferStyle({
        sourceVideoPath: videoPath,
        targetBrand: brand,
        transferStrength: 0.8,
        preserveContent: true,
        addWatermark: true,
        addLogo: true,
        colorCorrection: true,
        outputResolution: '1080P',
        ...config,
      });
      results.push(result);
    }

    return results;
  }

  /**
   * 验证视频是否符合品牌规范
   */
  validateBrandCompliance(
    videoPath: string,
    brand: BrandStyle
  ): { compliant: boolean; issues: string[] } {
    const issues: string[] = [];

    // 模拟品牌合规检查
    // 实际应使用计算机视觉 API 检测

    // 检查禁用元素
    brand.forbiddenElements.forEach(element => {
      // 模拟检查
      if (Math.random() < 0.1) {
        issues.push(`Detected forbidden element: ${element}`);
      }
    });

    // 检查主色调使用
    // 模拟：假设检查通过
    const primaryColorUsage = Math.random();
    if (primaryColorUsage < 0.3) {
      issues.push('Primary color usage below recommended threshold');
    }

    return {
      compliant: issues.length === 0,
      issues,
    };
  }

  /**
   * 生成品牌风格指南
   */
  generateStyleGuide(brand: BrandStyle): string {
    let guide = `# ${brand.brandName} 品牌风格指南\n\n`;

    guide += `## 品牌色彩\n\n`;
    guide += `- **主色调**: ${brand.primaryColor}\n`;
    guide += `- **辅助色**: ${brand.secondaryColors.join(', ')}\n\n`;

    guide += `## 品牌字体\n\n`;
    guide += `- **标题**: ${brand.fonts.heading || 'N/A'}\n`;
    guide += `- **正文**: ${brand.fonts.body || 'N/A'}\n\n`;

    guide += `## 风格关键词\n\n`;
    guide += brand.styleKeywords.map(k => `- ${k}`).join('\n');
    guide += '\n\n';

    guide += `## 视觉规范\n\n`;
    guide += `- **最小留白**: ${brand.visualGuidelines.minWhitespace}\n`;
    guide += `- **圆角大小**: ${brand.visualGuidelines.cornerRadius}\n`;
    guide += `- **阴影强度**: ${brand.visualGuidelines.shadowIntensity}\n`;
    guide += `- **动画风格**: ${brand.visualGuidelines.animationStyle}\n\n`;

    guide += `## 禁用元素\n\n`;
    guide += brand.forbiddenElements.map(e => `- ❌ ${e}`).join('\n');

    return guide;
  }

  /**
   * 创建风格迁移提示
   */
  private createTransferPrompt(config: StyleTransferConfig): string {
    const brand = config.targetBrand;
    const styleKeywords = brand.styleKeywords.join(', ');

    let prompt = `Apply ${brand.brandName} brand style to video. `;
    prompt += `Style: ${styleKeywords}. `;
    prompt += `Primary color: ${brand.primaryColor}. `;

    if (config.addLogo && brand.logoPath) {
      prompt += `Add logo overlay. `;
    }

    if (config.addWatermark) {
      prompt += `Add subtle watermark. `;
    }

    if (config.colorCorrection) {
      prompt += `Color grade to match brand palette. `;
    }

    if (config.preserveContent) {
      prompt += `Preserve original content and composition. `;
    }

    prompt += `Transfer strength: ${config.transferStrength * 100}%. `;
    prompt += `Professional quality, high fidelity.`;

    return prompt;
  }
}

// ============== 导出 ==============

export default BrandStyleTransferEngine;
