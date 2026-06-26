/**
 * 视频生成技能 (Video Generation Skill)
 * 
 * 层级：Layer 9 - Agent Operating System
 * 功能：视频生成执行、多 Agent 协同、任务编排
 * 版本：V1.0.0
 * 状态：🟡 开发中
 */

import ComfyUIWorkflowOrchestrator, {
  VideoGenerationRequest,
  VideoGenerationResponse,
  GovernanceConfig,
  SandboxConfig,
} from './comfyui-workflow-orchestrator';

// ============== 类型定义 ==============

/**
 * 视频生成任务
 */
export interface VideoGenerationTask {
  /** 任务 ID */
  id: string;
  /** 任务描述 */
  description: string;
  /** 优先级 (1-5, 5 最高) */
  priority: number;
  /** 生成请求 */
  request: VideoGenerationRequest;
  /** 客户端 ID */
  clientId: string;
  /** 创建时间 */
  createdAt: number;
  /** 截止时间 (可选) */
  deadline?: number;
  /** 重试次数 */
  retryCount: number;
  /** 最大重试次数 */
  maxRetries: number;
}

/**
 * 任务状态
 */
export type TaskStatus = 'pending' | 'running' | 'completed' | 'failed' | 'cancelled';

/**
 * 任务执行结果
 */
export interface TaskExecutionResult {
  /** 任务 ID */
  taskId: string;
  /** 执行状态 */
  status: TaskStatus;
  /** 生成响应 */
  response?: VideoGenerationResponse;
  /** 错误信息 */
  error?: string;
  /** 执行耗时 (ms) */
  durationMs: number;
  /** 执行时间戳 */
  executedAt: number;
}

/**
 * Agent 通信消息
 */
export interface AgentMessage {
  /** 消息类型 */
  type: 'request' | 'response' | 'status' | 'error';
  /** 发送方 Agent */
  from: string;
  /** 接收方 Agent */
  to: string;
  /** 消息内容 */
  payload: any;
  /** 时间戳 */
  timestamp: number;
  /** 追踪 ID */
  traceId?: string;
}

// ============== 队列管理 ==============

/**
 * 任务队列
 */
class TaskQueue {
  private tasks: VideoGenerationTask[] = [];

  /**
   * 添加任务
   */
  enqueue(task: VideoGenerationTask): void {
    this.tasks.push(task);
    // 按优先级排序
    this.tasks.sort((a, b) => b.priority - a.priority || a.createdAt - b.createdAt);
  }

  /**
   * 获取下一个任务
   */
  dequeue(): VideoGenerationTask | undefined {
    return this.tasks.shift();
  }

  /**
   * 查看队列长度
   */
  length(): number {
    return this.tasks.length;
  }

  /**
   * 获取所有待处理任务
   */
  getAll(): VideoGenerationTask[] {
    return [...this.tasks];
  }

  /**
   * 取消任务
   */
  cancel(taskId: string): boolean {
    const index = this.tasks.findIndex(t => t.id === taskId);
    if (index !== -1) {
      this.tasks.splice(index, 1);
      return true;
    }
    return false;
  }
}

// ============== 核心类 ==============

/**
 * 视频生成技能 (Video Production Agent)
 */
export class VideoGenerationSkill {
  private orchestrator: ComfyUIWorkflowOrchestrator;
  private taskQueue: TaskQueue = new TaskQueue();
  private runningTasks: Map<string, NodeJS.Timeout> = new Map();
  private taskHistory: TaskExecutionResult[] = [];
  private maxConcurrentTasks: number = 3;
  private currentRunningTasks: number = 0;

  constructor(
    governanceConfig: Partial<GovernanceConfig> = {},
    sandboxConfig: Partial<SandboxConfig> = {}
  ) {
    this.orchestrator = new ComfyUIWorkflowOrchestrator(governanceConfig, sandboxConfig);
  }

  /**
   * 提交视频生成任务
   */
  submitTask(task: VideoGenerationTask): { success: boolean; taskId: string; message?: string } {
    // 验证任务
    if (!task.id || !task.description || !task.request) {
      return { success: false, taskId: task.id, message: 'Invalid task definition' };
    }

    // 检查截止时间
    if (task.deadline && task.deadline < Date.now()) {
      return { success: false, taskId: task.id, message: 'Task deadline has passed' };
    }

    // 添加到队列
    this.taskQueue.enqueue(task);

    // 触发执行
    this.processQueue();

    return { success: true, taskId: task.id, message: 'Task submitted successfully' };
  }

  /**
   * 处理任务队列
   */
  private async processQueue(): Promise<void> {
    while (this.currentRunningTasks < this.maxConcurrentTasks && this.taskQueue.length() > 0) {
      const task = this.taskQueue.dequeue();
      if (task) {
        this.executeTask(task);
      }
    }
  }

  /**
   * 执行单个任务
   */
  private async executeTask(task: VideoGenerationTask): Promise<void> {
    this.currentRunningTasks++;
    const startTime = Date.now();

    try {
      // 执行视频生成
      const response = await this.orchestrator.generateVideo(task.request, task.clientId);

      // 创建执行结果
      const result: TaskExecutionResult = {
        taskId: task.id,
        status: response.status === 'success' ? 'completed' : 'failed',
        response,
        durationMs: Date.now() - startTime,
        executedAt: Date.now(),
      };

      // 处理失败重试
      if (response.status === 'failed' && task.retryCount < task.maxRetries) {
        task.retryCount++;
        // 重新加入队列
        this.taskQueue.enqueue(task);
        result.status = 'pending';
        result.error = `Retrying (${task.retryCount}/${task.maxRetries})`;
      }

      // 记录历史
      this.taskHistory.push(result);

      // 通知相关 Agent (TODO: 实现 MCP 通信)
      await this.notifyAgents(result);
    } catch (error) {
      const result: TaskExecutionResult = {
        taskId: task.id,
        status: 'failed',
        error: error instanceof Error ? error.message : 'Unknown error',
        durationMs: Date.now() - startTime,
        executedAt: Date.now(),
      };
      this.taskHistory.push(result);
      await this.notifyAgents(result);
    } finally {
      this.currentRunningTasks--;
      // 继续处理队列
      this.processQueue();
    }
  }

  /**
   * 通知相关 Agent
   */
  private async notifyAgents(result: TaskExecutionResult): Promise<void> {
    // TODO: 通过 MCP Bus 发送消息给 Interaction Agent、UI Synthesis 等
    const message: AgentMessage = {
      type: result.status === 'completed' ? 'response' : 'error',
      from: 'video-production-agent',
      to: 'interaction-agent',
      payload: result,
      timestamp: Date.now(),
      traceId: result.taskId,
    };

    console.log(`[Agent Message] ${JSON.stringify(message)}`);
  }

  /**
   * 获取任务状态
   */
  getTaskStatus(taskId: string): TaskExecutionResult | undefined {
    return this.taskHistory.find(t => t.taskId === taskId);
  }

  /**
   * 获取队列状态
   */
  getQueueStatus(): {
    pendingTasks: number;
    runningTasks: number;
    maxConcurrentTasks: number;
  } {
    return {
      pendingTasks: this.taskQueue.length(),
      runningTasks: this.currentRunningTasks,
      maxConcurrentTasks: this.maxConcurrentTasks,
    };
  }

  /**
   * 取消任务
   */
  cancelTask(taskId: string): { success: boolean; message: string } {
    // 尝试从队列中取消
    const cancelled = this.taskQueue.cancel(taskId);
    if (cancelled) {
      return { success: true, message: 'Task cancelled from queue' };
    }

    // 检查是否正在运行 (TODO: 实现运行中任务取消)
    const runningTask = this.runningTasks.get(taskId);
    if (runningTask) {
      clearTimeout(runningTask);
      this.runningTasks.delete(taskId);
      this.currentRunningTasks--;
      return { success: true, message: 'Running task cancelled' };
    }

    return { success: false, message: 'Task not found' };
  }

  /**
   * 获取使用统计
   */
  getUsageStats(): {
    totalTasks: number;
    completedTasks: number;
    failedTasks: number;
    pendingTasks: number;
    averageDurationMs: number;
    successRate: number;
  } {
    const total = this.taskHistory.length;
    const completed = this.taskHistory.filter(t => t.status === 'completed').length;
    const failed = this.taskHistory.filter(t => t.status === 'failed').length;
    const pending = this.taskHistory.filter(t => t.status === 'pending').length;

    const avgDuration = total > 0
      ? this.taskHistory.reduce((sum, t) => sum + t.durationMs, 0) / total
      : 0;

    const successRate = total > 0 ? completed / total : 0;

    return {
      totalTasks: total,
      completedTasks: completed,
      failedTasks: failed,
      pendingTasks: pending,
      averageDurationMs: Math.round(avgDuration),
      successRate: Math.round(successRate * 100) / 100,
    };
  }

  /**
   * 获取 Orchestrator 使用统计
   */
  getOrchestratorStats(): {
    dailyQuotaUsed: number;
    dailyQuotaRemaining: number;
    requestCount: number;
  } {
    return this.orchestrator.getUsageStats();
  }

  /**
   * 清空历史记录 (保留最近 N 条)
   */
  clearHistory(keepLast: number = 100): void {
    if (this.taskHistory.length > keepLast) {
      this.taskHistory = this.taskHistory.slice(-keepLast);
    }
  }
}

// ============== 导出 ==============

export default VideoGenerationSkill;
