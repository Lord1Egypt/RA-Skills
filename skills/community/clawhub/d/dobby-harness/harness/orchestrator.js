/**
 * Harness Orchestrator - 多 Agent 编排核心
 * 
 * 负责：
 * - 任务分解
 * - 子 Agent 会话管理
 * - 任务调度与并行执行
 * - 结果聚合与验证
 * 
 * @author 多比 🧦
 * @version 1.0.0
 */

import { EventEmitter } from 'events';
import { createHash } from 'crypto';

// ============================================================================
// 配置
// ============================================================================

const DEFAULT_CONFIG = {
  maxParallel: 5,           // 最大并行任务数
  timeoutSeconds: 300,      // 单个任务超时 (秒)
  retryAttempts: 2,         // 失败重试次数
  retryDelay: 1000,         // 重试延迟 (ms)
  enableLogging: true,      // 启用日志
};

// ============================================================================
// 任务状态枚举
// ============================================================================

const TaskStatus = {
  PENDING: 'pending',
  RUNNING: 'running',
  COMPLETED: 'completed',
  FAILED: 'failed',
  TIMEOUT: 'timeout',
  CANCELLED: 'cancelled',
};

// ============================================================================
// 消息类型枚举
// ============================================================================

const MessageType = {
  TASK_REQUEST: 'task-request',
  TASK_RESPONSE: 'task-response',
  STATUS_UPDATE: 'status-update',
  ERROR: 'error',
};

// ============================================================================
// 工具函数
// ============================================================================

/**
 * 生成唯一任务 ID
 */
function generateTaskId(task, timestamp) {
  const content = `${task}-${timestamp}-${Math.random()}`;
  return `task-${createHash('sha256').update(content).digest('hex').slice(0, 12)}`;
}

/**
 * 生成唯一消息 ID
 */
function generateMessageId() {
  return `msg-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
}

/**
 * 延迟函数
 */
function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * 日志工具
 */
class Logger {
  constructor(enabled = true) {
    this.enabled = enabled;
    this.prefix = '[Harness]';
  }

  info(...args) {
    if (this.enabled) {
      console.log(`${this.prefix} [INFO]`, ...args);
    }
  }

  warn(...args) {
    if (this.enabled) {
      console.warn(`${this.prefix} [WARN]`, ...args);
    }
  }

  error(...args) {
    if (this.enabled) {
      console.error(`${this.prefix} [ERROR]`, ...args);
    }
  }

  debug(...args) {
    if (this.enabled) {
      console.debug(`${this.prefix} [DEBUG]`, ...args);
    }
  }
}

// ============================================================================
// 任务类
// ============================================================================

class Task {
  constructor({ id, task, dependencies = [], context = {}, priority = 0 }) {
    this.id = id;
    this.task = task;
    this.dependencies = dependencies;
    this.context = context;
    this.priority = priority;
    this.status = TaskStatus.PENDING;
    this.result = null;
    this.error = null;
    this.startTime = null;
    this.endTime = null;
    this.retryCount = 0;
    this.agentId = null;
  }

  get duration() {
    if (!this.startTime) return 0;
    const end = this.endTime || Date.now();
    return end - this.startTime;
  }

  toJSON() {
    return {
      id: this.id,
      task: this.task,
      dependencies: this.dependencies,
      status: this.status,
      result: this.result,
      error: this.error,
      duration: this.duration,
      retryCount: this.retryCount,
      agentId: this.agentId,
    };
  }
}

// ============================================================================
// 任务队列
// ============================================================================

class TaskQueue {
  constructor(maxParallel) {
    this.maxParallel = maxParallel;
    this.pending = [];
    this.running = new Map();
    this.completed = [];
    this.failed = [];
  }

  /**
   * 添加任务到队列
   */
  enqueue(task) {
    this.pending.push(task);
    this.pending.sort((a, b) => b.priority - a.priority);
  }

  /**
   * 获取可执行的任务（依赖已满足）
   */
  getReadyTasks(completedTaskIds) {
    const ready = [];
    const remaining = [];

    for (const task of this.pending) {
      const depsMet = task.dependencies.every(dep => completedTaskIds.includes(dep));
      if (depsMet) {
        ready.push(task);
      } else {
        remaining.push(task);
      }
    }

    this.pending = remaining;
    return ready;
  }

  /**
   * 开始执行任务
   */
  startTask(task, agentId) {
    task.status = TaskStatus.RUNNING;
    task.startTime = Date.now();
    task.agentId = agentId;
    this.running.set(task.id, task);
  }

  /**
   * 标记任务完成
   */
  completeTask(taskId, result) {
    const task = this.running.get(taskId);
    if (task) {
      task.status = TaskStatus.COMPLETED;
      task.endTime = Date.now();
      task.result = result;
      this.running.delete(taskId);
      this.completed.push(task);
    }
  }

  /**
   * 标记任务失败
   */
  failTask(taskId, error) {
    const task = this.running.get(taskId);
    if (task) {
      task.status = TaskStatus.FAILED;
      task.endTime = Date.now();
      task.error = error;
      this.running.delete(taskId);
      this.failed.push(task);
    }
  }

  /**
   * 获取队列状态
   */
  getStatus() {
    return {
      pending: this.pending.length,
      running: this.running.size,
      completed: this.completed.length,
      failed: this.failed.length,
    };
  }
}

// ============================================================================
// 结果聚合器
// ============================================================================

class ResultAggregator {
  /**
   * 聚合所有任务结果
   */
  aggregate(tasks, strategy = 'merge') {
    const completed = tasks.filter(t => t.status === TaskStatus.COMPLETED);
    const failed = tasks.filter(t => t.status === TaskStatus.FAILED);

    const result = {
      success: failed.length === 0,
      completed: completed.length,
      failed: failed.length,
      total: tasks.length,
      outputs: [],
      errors: [],
      metadata: {
        totalTime: Math.max(...tasks.map(t => t.duration), 0),
        avgTime: completed.length > 0 
          ? completed.reduce((sum, t) => sum + t.duration, 0) / completed.length 
          : 0,
      },
    };

    // 根据策略合并输出
    switch (strategy) {
      case 'merge':
        result.outputs = completed.map(t => t.result);
        break;
      case 'first':
        result.outputs = completed.length > 0 ? [completed[0].result] : [];
        break;
      case 'concat':
        result.outputs = completed.flatMap(t => Array.isArray(t.result) ? t.result : [t.result]);
        break;
      default:
        result.outputs = completed.map(t => ({ taskId: t.id, output: t.result }));
    }

    // 收集错误
    result.errors = failed.map(t => ({
      taskId: t.id,
      task: t.task,
      error: t.error,
    }));

    return result;
  }

  /**
   * 验证结果质量
   */
  validate(result, validators = []) {
    const issues = [];

    for (const validator of validators) {
      const issue = validator(result);
      if (issue) {
        issues.push(issue);
      }
    }

    return {
      valid: issues.length === 0,
      issues,
    };
  }
}

// ============================================================================
// 重试工具
// ============================================================================

async function withRetry(fn, config) {
  const { maxAttempts, retryDelay, retryableErrors } = config;

  for (let attempt = 1; attempt <= maxAttempts + 1; attempt++) {
    try {
      return await fn();
    } catch (error) {
      const isRetryable = !retryableErrors || retryableErrors.includes(error.code);
      
      if (attempt <= maxAttempts && isRetryable) {
        const backoffDelay = retryDelay * Math.pow(2, attempt - 1);
        console.log(`[Retry] Attempt ${attempt} failed, retrying in ${backoffDelay}ms...`);
        await delay(backoffDelay);
      } else {
        throw error;
      }
    }
  }
}

// ============================================================================
// 主编排器类
// ============================================================================

export class HarnessOrchestrator extends EventEmitter {
  constructor(config = {}) {
    super();
    this.config = { ...DEFAULT_CONFIG, ...config };
    this.logger = new Logger(this.config.enableLogging);
    this.queue = new TaskQueue(this.config.maxParallel);
    this.aggregator = new ResultAggregator();
    this.tasks = new Map();
    this.isRunning = false;
  }

  /**
   * 执行任务
   * 
   * @param {Object} options
   * @param {string} options.task - 任务描述
   * @param {Object} options.context - 上下文数据
   * @param {string} options.pattern - 分解模式 (sequential|parallel|hybrid)
   * @param {Array} options.subTasks - 预定义的子任务列表（可选）
   * @returns {Promise<Object>} 聚合结果
   */
  async execute(options) {
    const { task, context = {}, pattern = 'parallel', subTasks = [] } = options;

    this.logger.info(`Starting execution: "${task}" (pattern: ${pattern})`);
    this.emit('start', { task, context, pattern });

    this.isRunning = true;
    const startTime = Date.now();

    try {
      // 1. 任务分解
      const tasks = await this.decomposeTask(task, context, pattern, subTasks);
      this.logger.info(`Decomposed into ${tasks.length} sub-tasks`);

      // 2. 初始化队列
      tasks.forEach(t => this.queue.enqueue(t));

      // 3. 执行任务
      const results = await this.runTasks(context);

      // 4. 聚合结果
      const aggregated = this.aggregator.aggregate(results);

      // 5. 质量验证
      const validation = this.aggregator.validate(aggregated);

      const finalResult = {
        ...aggregated,
        validation,
        totalDuration: Date.now() - startTime,
      };

      this.logger.info(`Execution completed: ${aggregated.completed}/${aggregated.total} successful`);
      this.emit('complete', finalResult);

      return finalResult;

    } catch (error) {
      this.logger.error(`Execution failed: ${error.message}`);
      this.emit('error', error);
      throw error;
    } finally {
      this.isRunning = false;
    }
  }

  /**
   * 任务分解
   */
  async decomposeTask(task, context, pattern, subTasks) {
    const timestamp = Date.now();
    const tasks = [];

    if (subTasks.length > 0) {
      // 使用预定义的子任务
      for (let i = 0; i < subTasks.length; i++) {
        const subTask = subTasks[i];
        tasks.push(new Task({
          id: generateTaskId(subTask.task, timestamp + i),
          task: subTask.task,
          dependencies: subTask.dependencies || [],
          context: { ...context, ...subTask.context },
          priority: subTask.priority || 0,
        }));
      }
    } else {
      // 根据模式自动分解（简化版，实际应该调用 AI 进行智能分解）
      switch (pattern) {
        case 'sequential':
          // 顺序执行：每个任务依赖前一个
          for (let i = 0; i < 3; i++) {
            tasks.push(new Task({
              id: generateTaskId(`${task}-step${i}`, timestamp + i),
              task: `${task} (步骤 ${i + 1}/3)`,
              dependencies: i > 0 ? [tasks[i - 1].id] : [],
              context,
              priority: 3 - i,
            }));
          }
          break;

        case 'parallel':
          // 并行执行：无依赖
          for (let i = 0; i < 3; i++) {
            tasks.push(new Task({
              id: generateTaskId(`${task}-part${i}`, timestamp + i),
              task: `${task} (部分 ${i + 1}/3)`,
              dependencies: [],
              context,
              priority: 0,
            }));
          }
          break;

        case 'hybrid':
        default:
          // 混合模式：先并行后串行
          for (let i = 0; i < 2; i++) {
            tasks.push(new Task({
              id: generateTaskId(`${task}-parallel${i}`, timestamp + i),
              task: `${task} (并行 ${i + 1}/2)`,
              dependencies: [],
              context,
              priority: 1,
            }));
          }
          tasks.push(new Task({
            id: generateTaskId(`${task}-final`, timestamp + 2),
            task: `${task} (汇总)`,
            dependencies: [tasks[0].id, tasks[1].id],
            context,
            priority: 2,
          }));
          break;
      }
    }

    // 存储任务
    tasks.forEach(t => this.tasks.set(t.id, t));

    return tasks;
  }

  /**
   * 运行所有任务
   */
  async runTasks(context) {
    const completedTaskIds = [];
    const agentSessions = new Map();

    while (true) {
      // 获取可执行的任务
      const readyTasks = this.queue.getReadyTasks(completedTaskIds);
      
      // 检查是否还有任务要执行
      const status = this.queue.getStatus();
      if (readyTasks.length === 0 && status.running === 0) {
        break;
      }

      // 启动新任务（不超过最大并行数）
      const slotsAvailable = this.config.maxParallel - status.running;
      const toStart = readyTasks.slice(0, slotsAvailable);

      const executionPromises = toStart.map(async (task) => {
        this.queue.startTask(task, `agent-${task.id.slice(-6)}`);
        this.emit('task-start', task);

        try {
          // 执行任务（这里简化为直接执行，实际应该调用子 Agent）
          const result = await this.executeTask(task, context);
          this.queue.completeTask(task.id, result);
          completedTaskIds.push(task.id);
          this.emit('task-complete', task);
        } catch (error) {
          // 重试逻辑
          if (task.retryCount < this.config.retryAttempts) {
            task.retryCount++;
            this.queue.pending.push(task);
            this.logger.warn(`Task ${task.id} failed, retrying (${task.retryCount}/${this.config.retryAttempts})`);
          } else {
            this.queue.failTask(task.id, error.message);
            this.emit('task-failed', { task, error });
          }
        }
      });

      // 等待当前批次完成
      await Promise.all(executionPromises);

      // 短暂延迟，避免忙等
      if (status.running > 0) {
        await delay(100);
      }
    }

    return Array.from(this.tasks.values());
  }

  /**
   * 执行单个任务
   * 
   * 这里是核心：实际应该调用 sessions_spawn 创建子 Agent
   * 当前简化版本直接返回模拟结果
   */
  async executeTask(task, context) {
    this.logger.debug(`Executing task: ${task.id}`);

    // TODO: 实际实现应该调用 sessions_spawn
    // const session = await sessions_spawn({
    //   task: task.task,
    //   mode: 'run',
    //   runtime: 'subagent',
    //   timeoutSeconds: this.config.timeoutSeconds,
    // });

    // 模拟执行（占位符）
    await delay(100 + Math.random() * 200);
    
    return {
      taskId: task.id,
      output: `Result for: ${task.task}`,
      metadata: {
        duration: task.duration,
        agentId: task.agentId,
      },
    };
  }

  /**
   * 取消执行
   */
  async cancel() {
    this.logger.info('Cancelling execution...');
    this.isRunning = false;
    
    for (const task of this.tasks.values()) {
      if (task.status === TaskStatus.PENDING || task.status === TaskStatus.RUNNING) {
        task.status = TaskStatus.CANCELLED;
      }
    }

    this.emit('cancelled');
  }

  /**
   * 获取执行状态
   */
  getStatus() {
    return {
      isRunning: this.isRunning,
      queue: this.queue.getStatus(),
      tasks: Array.from(this.tasks.values()).map(t => t.toJSON()),
    };
  }
}

// ============================================================================
// 导出
// ============================================================================

export { TaskStatus, MessageType, TaskQueue, ResultAggregator, withRetry };
export default HarnessOrchestrator;
