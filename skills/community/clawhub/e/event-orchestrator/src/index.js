/**
 * event-orchestrator - 主入口文件
 * 
 * 基于事件驱动架构 (EDA) 的技能编排器
 * 应用设计模式：EDA、Middleware 链、状态机
 */

const { EventBus } = require('./event-bus');
const {
  LoggingMiddleware,
  ValidationMiddleware,
  RetryMiddleware,
  RateLimitMiddleware,
  MiddlewareChainExecutor
} = require('./middleware-chain');
const {
  OrchestrationState,
  StateMachine,
  OrchestrationTask
} = require('./state-machine');

/**
 * 事件编排器主类
 */
class EventOrchestrator {
  constructor(options = {}) {
    this.eventBus = new EventBus({
      maxHistorySize: options.maxHistorySize || 1000
    });
    
    this.tasks = new Map();
    this.options = options;
    
    // 注册默认中间件
    this._registerDefaultMiddleware();
  }

  /**
   * 注册默认中间件
   */
  _registerDefaultMiddleware() {
    // 日志中间件
    this.eventBus.use(new LoggingMiddleware({ logLevel: 'info' }));
    
    // 速率限制中间件
    this.eventBus.use(new RateLimitMiddleware({
      maxEvents: 100,
      windowMs: 60000
    }));
  }

  /**
   * 注册事件 Schema
   */
  registerSchema(eventName, schema) {
    this.eventBus.registerSchema(eventName, schema);
  }

  /**
   * 订阅事件
   */
  subscribe(eventName, handler, options = {}) {
    return this.eventBus.subscribe(eventName, handler, options);
  }

  /**
   * 取消订阅
   */
  unsubscribe(eventName, subscriberId) {
    return this.eventBus.unsubscribe(eventName, subscriberId);
  }

  /**
   * 发布事件
   */
  async publish(eventName, payload = {}, metadata = {}) {
    return await this.eventBus.publish(eventName, payload, metadata);
  }

  /**
   * 创建编排任务
   */
  createTask(taskId, definition) {
    const task = new OrchestrationTask(taskId, definition);
    this.tasks.set(taskId, task);
    return task;
  }

  /**
   * 获取任务状态
   */
  getTaskStatus(taskId) {
    const task = this.tasks.get(taskId);
    if (!task) {
      return { error: 'Task not found', taskId };
    }
    return task.getStatus();
  }

  /**
   * 获取所有任务状态
   */
  getAllTasksStatus() {
    const status = {};
    for (const [taskId, task] of this.tasks.entries()) {
      status[taskId] = task.getStatus();
    }
    return status;
  }

  /**
   * 获取事件历史
   */
  getEventHistory(limit = 100, eventName = null) {
    return this.eventBus.getHistory(limit, eventName);
  }

  /**
   * 获取订阅者统计
   */
  getSubscriberStats() {
    return this.eventBus.getSubscriberStats();
  }

  /**
   * 添加自定义中间件
   */
  useMiddleware(middleware) {
    this.eventBus.use(middleware);
  }

  /**
   * 清空所有数据
   */
  clear() {
    this.eventBus.clearHistory();
    this.tasks.clear();
  }

  /**
   * 导出状态
   */
  exportState() {
    return {
      tasks: Array.from(this.tasks.entries()).map(([id, task]) => ({
        id,
        status: task.getStatus()
      })),
      eventHistory: this.eventBus.getHistory(1000),
      subscriberStats: this.eventBus.getSubscriberStats(),
      exportedAt: Date.now()
    };
  }
}

/**
 * 预定义事件 Schema
 */
const EventSchemas = {
  // 技能执行事件
  'skill.started': {
    skillId: 'string',
    taskId: 'string',
    parameters: 'object'
  },
  'skill.completed': {
    skillId: 'string',
    taskId: 'string',
    result: 'object',
    duration: 'number'
  },
  'skill.failed': {
    skillId: 'string',
    taskId: 'string',
    error: 'string',
    retryCount: 'number'
  },
  
  // 任务编排事件
  'task.created': {
    taskId: 'string',
    definition: 'object',
    priority: 'number'
  },
  'task.started': {
    taskId: 'string',
    startedAt: 'number'
  },
  'task.completed': {
    taskId: 'string',
    completedAt: 'number',
    result: 'object'
  },
  'task.failed': {
    taskId: 'string',
    failedAt: 'number',
    error: 'string'
  },
  
  // 系统事件
  'system.ready': {
    version: 'string',
    timestamp: 'number'
  },
  'system.shutdown': {
    reason: 'string',
    timestamp: 'number'
  }
};

module.exports = {
  EventOrchestrator,
  EventBus,
  EventSchemas,
  OrchestrationState,
  StateMachine,
  OrchestrationTask,
  LoggingMiddleware,
  ValidationMiddleware,
  RetryMiddleware,
  RateLimitMiddleware
};
