/**
 * 用户流程可视化器
 * 
 * 层级：Layer 6 - System Architecture Layer
 * 功能：将用户操作流程转换为可视化视频
 * 版本：V1.0.0
 * 状态：🟡 开发中
 */

import { VideoGenerationRequest } from './comfyui-workflow-orchestrator';
import { VideoGenerationSkill } from './video-generation-skill';
import { MCPVideoBus } from './mcp-video-bus';

// ============== 类型定义 ==============

/**
 * 用户流程步骤
 */
export interface UserFlowStep {
  /** 步骤序号 */
  sequence: number;
  /** 步骤名称 */
  name: string;
  /** 步骤描述 */
  description: string;
  /** 用户操作 */
  userAction: string;
  /** 系统响应 */
  systemResponse: string;
  /** UI 截图路径 (可选) */
  screenshotPath?: string;
  /** 预计时长 (秒) */
  durationSeconds: number;
}

/**
 * 用户流程
 */
export interface UserFlow {
  /** 流程 ID */
  flowId: string;
  /** 流程名称 */
  flowName: string;
  /** 流程描述 */
  description: string;
  /** 目标用户 */
  targetUser: string;
  /** 流程步骤 */
  steps: UserFlowStep[];
  /** 预期结果 */
  expectedOutcome: string;
}

/**
 * 可视化配置
 */
export interface FlowVisualizationConfig {
  /** 视频风格 */
  style: 'tutorial' | 'demo' | 'animation' | 'screencast';
  /** 显示鼠标点击 */
  showClicks: boolean;
  /** 显示键盘输入 */
  showTyping: boolean;
  /** 高亮 UI 元素 */
  highlightUI: boolean;
  /** 添加标注 */
  addAnnotations: boolean;
  /** 旁白语速 */
  narrationSpeed: 'slow' | 'normal' | 'fast';
  /** 分辨率 */
  resolution: '480P' | '720P' | '1080P';
  /** 宽高比 */
  aspectRatio: '16:9' | '9:16';
}

/**
 * 可视化结果
 */
export interface FlowVisualizationResult {
  /** 流程 ID */
  flowId: string;
  /** 状态 */
  status: 'success' | 'failed' | 'partial';
  /** 生成的视频路径 */
  videoPath?: string;
  /** 步骤视频路径 */
  stepVideoPaths: string[];
  /** 生成耗时 (秒) */
  durationSeconds: number;
  /** 错误信息 */
  errors?: string[];
  /** 元数据 */
  metadata: {
    totalSteps: number;
    visualizedSteps: number;
    totalDuration: number;
  };
}

// ============== 默认配置 ==============

const DEFAULT_VISUALIZATION_CONFIG: FlowVisualizationConfig = {
  style: 'tutorial',
  showClicks: true,
  showTyping: true,
  highlightUI: true,
  addAnnotations: true,
  narrationSpeed: 'normal',
  resolution: '1080P',
  aspectRatio: '16:9',
};

const STYLE_PROMPTS: Record<FlowVisualizationConfig['style'], string> = {
  tutorial: 'step-by-step tutorial, clear instructions, educational, beginner-friendly',
  demo: 'product demo, smooth transitions, professional presentation',
  animation: 'animated walkthrough, motion graphics, engaging visuals',
  screencast: 'screen recording, real UI, authentic user experience',
};

// ============== 核心类 ==============

/**
 * 用户流程可视化器
 */
export class UserFlowVisualizer {
  private videoSkill: VideoGenerationSkill;
  private mcpBus: MCPVideoBus;

  constructor(videoSkill: VideoGenerationSkill, mcpBus: MCPVideoBus) {
    this.videoSkill = videoSkill;
    this.mcpBus = mcpBus;
  }

  /**
   * 将用户流程转换为可视化视频
   */
  async visualizeFlow(
    flow: UserFlow,
    config: Partial<FlowVisualizationConfig> = {}
  ): Promise<FlowVisualizationResult> {
    const startTime = Date.now();

    const fullConfig: FlowVisualizationConfig = {
      ...DEFAULT_VISUALIZATION_CONFIG,
      ...config,
    };

    try {
      // 1. 为每个步骤生成视觉提示
      const stepPrompts = flow.steps.map(step =>
        this.createStepVisualPrompt(step, flow, fullConfig)
      );

      // 2. 生成步骤视频
      const stepResults = await this.generateStepVideos(
        flow.flowId,
        stepPrompts,
        flow.steps,
        fullConfig
      );

      // 3. 合并步骤视频
      const successfulSteps = stepResults.filter(r => r.status === 'success');
      const mergedVideoPath =
        successfulSteps.length > 0
          ? `/videos/flow_${flow.flowId}_merged.mp4`
          : undefined;

      // 4. 返回结果
      const result: FlowVisualizationResult = {
        flowId: flow.flowId,
        status:
          successfulSteps.length === flow.steps.length
            ? 'success'
            : successfulSteps.length > 0
            ? 'partial'
            : 'failed',
        videoPath: mergedVideoPath,
        stepVideoPaths: successfulSteps.map(r => r.videoPath),
        durationSeconds: (Date.now() - startTime) / 1000,
        errors: stepResults
          .filter(r => r.status === 'failed')
          .map(r => r.error!)
          .filter(Boolean),
        metadata: {
          totalSteps: flow.steps.length,
          visualizedSteps: successfulSteps.length,
          totalDuration: successfulSteps.reduce((sum, r) => sum + r.duration, 0),
        },
      };

      // 5. 发送完成通知
      await this.notifyVisualizationComplete(result);

      return result;
    } catch (error) {
      return {
        flowId: flow.flowId,
        status: 'failed',
        stepVideoPaths: [],
        durationSeconds: (Date.now() - startTime) / 1000,
        errors: [error instanceof Error ? error.message : 'Unknown error'],
        metadata: {
          totalSteps: flow.steps.length,
          visualizedSteps: 0,
          totalDuration: 0,
        },
      };
    }
  }

  /**
   * 创建步骤视觉提示
   */
  private createStepVisualPrompt(
    step: UserFlowStep,
    flow: UserFlow,
    config: FlowVisualizationConfig
  ): string {
    const stylePrompt = STYLE_PROMPTS[config.style];
    const actionPrompt = this.describeAction(step.userAction, config);

    let prompt = `User flow: ${flow.flowName}, Step ${step.sequence}: ${step.name}. `;
    prompt += `${step.description} `;
    prompt += `${actionPrompt}. `;
    prompt += `${stylePrompt}. `;

    if (config.highlightUI) {
      prompt += 'Highlight UI elements, clear visual focus. ';
    }

    if (config.addAnnotations) {
      prompt += 'Add text annotations, arrows, and callouts. ';
    }

    return prompt;
  }

  /**
   * 描述用户操作
   */
  private describeAction(
    action: string,
    config: FlowVisualizationConfig
  ): string {
    const actionLower = action.toLowerCase();

    if (actionLower.includes('click')) {
      return config.showClicks
        ? 'Show mouse cursor clicking on button, visual click effect'
        : 'User clicks on element';
    }

    if (actionLower.includes('type') || actionLower.includes('input')) {
      return config.showTyping
        ? 'Show keyboard typing animation, text appearing character by character'
        : 'User types input';
    }

    if (actionLower.includes('scroll')) {
      return 'Smooth scroll animation, content moving vertically';
    }

    if (actionLower.includes('swipe')) {
      return 'Swipe gesture animation, horizontal movement';
    }

    return `User action: ${action}`;
  }

  /**
   * 生成步骤视频
   */
  private async generateStepVideos(
    flowId: string,
    prompts: string[],
    steps: UserFlowStep[],
    config: FlowVisualizationConfig
  ): Promise<
    Array<{ status: 'success' | 'failed'; videoPath: string; duration: number; error?: string }>
  > {
    const results: Array<{
      status: 'success' | 'failed';
      videoPath: string;
      duration: number;
      error?: string;
    }> = [];

    for (let i = 0; i < prompts.length; i++) {
      try {
        const request: VideoGenerationRequest = {
          prompt: prompts[i],
          durationSeconds: steps[i].durationSeconds,
          resolution: config.resolution,
          aspectRatio: config.aspectRatio,
        };

        const task = {
          id: `flow_${flowId}_step_${i + 1}`,
          description: steps[i].name,
          priority: 5,
          request,
          clientId: 'user-flow-visualizer',
          createdAt: Date.now(),
          retryCount: 0,
          maxRetries: 2,
        };

        const submitResult = this.videoSkill.submitTask(task);

        if (submitResult.success) {
          await new Promise(resolve => setTimeout(resolve, 1500));

          results.push({
            status: 'success',
            videoPath: `/videos/flow_${flowId}_step_${i + 1}.mp4`,
            duration: steps[i].durationSeconds,
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
   * 发送完成通知
   */
  private async notifyVisualizationComplete(
    result: FlowVisualizationResult
  ): Promise<void> {
    console.log(
      `[User Flow Visualizer] ✅ Visualization completed: ${result.flowId}, ` +
        `${result.metadata.visualizedSteps}/${result.metadata.totalSteps} steps visualized`
    );

    // 通过 MCP 总线发送通知
    const message = this.mcpBus.createGenerateResponse(
      {
        status: result.status === 'success' ? 'success' : 'failed',
        videoPath: result.videoPath,
        durationMs: result.durationSeconds * 1000,
      },
      `flow_${result.flowId}`,
      'user-flow-visualizer',
      'interaction-agent'
    );
    await this.mcpBus.send(message);
  }

  /**
   * 从流程定义生成流程图 (静态)
   */
  generateFlowDiagram(flow: UserFlow): string {
    let diagram = `flowchart TD\n`;
    diagram += `    Start([开始])\n`;

    flow.steps.forEach((step, index) => {
      const nodeId = `Step${index + 1}`;
      diagram += `    ${nodeId}[${step.sequence}. ${step.name}]\n`;

      if (index === 0) {
        diagram += `    Start --> ${nodeId}\n`;
      } else {
        const prevNodeId = `Step${index}`;
        diagram += `    ${prevNodeId} --> ${nodeId}\n`;
      }
    });

    const endNodeId = `End${flow.steps.length}`;
    diagram += `    ${endNodeId} --> End([${flow.expectedOutcome}])\n`;

    return diagram;
  }
}

// ============== 导出 ==============

export default UserFlowVisualizer;
