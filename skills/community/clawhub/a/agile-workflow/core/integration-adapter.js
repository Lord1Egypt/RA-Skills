#!/usr/bin/env node
/**
 * 多 Agent 架构集成适配器 v1.0
 * 
 * 核心职责：将新模块（Context Router、Prompt Cache、Message Bus、Memory Manager、LLM Gateway）
 * 集成到现有 agile-workflow 系统中
 * 
 * 架构：
 * ┌─────────────────────────────────────────────────────────────┐
 * │                 AgentProcessPool (现有)                      │
 * │                                                              │
 * │  executeTask() ──→ [IntegrationAdapter] ──→ openclaw agent  │
 * │                           │                                  │
 * │                           ├─→ Context Router (上下文精简)    │
 * │                           ├─→ Message Bus (事件发布)         │
 * │                           ├─→ Memory Manager (记忆管理)      │
 * │                           └─→ LLM Gateway (统一入口)         │
 * └─────────────────────────────────────────────────────────────┘
 */

const { getContextRouter } = require('./context-router');
const { getPromptCache } = require('./prompt-cache');
const { getMessageBus } = require('./message-bus');
const { getMemoryManager } = require('./memory-manager');
const { getLLMGateway } = require('./llm-gateway');

class IntegrationAdapter {
  constructor(options = {}) {
    this.projectDir = options.projectDir;
    this.workspace = options.workspace || '/home/ubutu/.openclaw/workspace';
    
    // 初始化所有模块
    this.contextRouter = getContextRouter({
      taskStore: options.taskStore
    });
    
    this.promptCache = getPromptCache({
      cacheDir: require('path').join(this.workspace, 'data/cache/prompts')
    });
    
    this.messageBus = getMessageBus({
      historyFile: require('path').join(this.workspace, 'logs/message-bus/history.json')
    });
    
    this.memoryManager = getMemoryManager({
      longMemoryFile: require('path').join(this.workspace, 'memory/long-term.json')
    });
    
    this.llmGateway = getLLMGateway({
      cache: { cacheDir: require('path').join(this.workspace, 'data/cache/prompts') }
    });
    
    // 会话 ID（用于记忆管理）
    this.sessionId = `session-${Date.now()}`;
    
    // 统计
    this.stats = {
      contextRouted: 0,
      cacheHits: 0,
      messagesPublished: 0,
      memoriesPersisted: 0
    };
    
    console.log('🔌 IntegrationAdapter 初始化完成');
  }

  /**
   * 准备任务上下文（集成 Context Router）
   * @param {object} task - 任务对象
   * @param {string} agentType - Agent 类型
   * @returns {object} 精简上下文
   */
  prepareContext(task, agentType) {
    this.stats.contextRouted++;
    
    // 通过 Context Router 获取精简上下文
    const context = this.contextRouter.getContext(task.id, agentType);
    
    // 添加依赖上下文
    if (task.dependencies && task.dependencies.length > 0) {
      context.dependencies = this.contextRouter.buildDependencyContext(task.id);
    }
    
    // 记录到短期记忆
    this.memoryManager.setShort(this.sessionId, `context:${task.id}`, {
      agentType,
      contextSize: JSON.stringify(context).length
    });
    
    console.log(`📌 上下文准备: ${task.id} → ${agentType} (${JSON.stringify(context).length} bytes)`);
    
    return context;
  }

  /**
   * 发布任务事件（集成 Message Bus）
   * @param {string} event - 事件类型
   * @param {object} data - 事件数据
   */
  publishEvent(event, data) {
    this.stats.messagesPublished++;
    
    switch (event) {
      case 'task.started':
        this.messageBus.publish('task.started', {
          taskId: data.taskId,
          agent: data.agent,
          timestamp: Date.now()
        });
        break;
        
      case 'task.completed':
        this.messageBus.taskCompleted(data.taskId, data.result, data.agent);
        
        // 记录到记忆
        this.memoryManager.setShort(this.sessionId, `result:${data.taskId}`, data.result);
        break;
        
      case 'task.failed':
        this.messageBus.taskFailed(data.taskId, data.error, data.agent);
        
        // 记录错误到记忆
        this.memoryManager.setShort(this.sessionId, `error:${data.taskId}`, data.error);
        break;
        
      case 'agent.status':
        this.messageBus.agentStatusChanged(data.agentId, data.status, data.details);
        break;
        
      default:
        this.messageBus.publish(event, data);
    }
  }

  /**
   * 调用 LLM（集成 LLM Gateway + Prompt Cache）
   * @param {string} prompt - 提示词
   * @param {object} options - 选项
   * @returns {Promise<object>} 响应
   */
  async callLLM(prompt, options = {}) {
    // 检查缓存
    const cached = this.promptCache.get(prompt, { model: options.model });
    if (cached) {
      this.stats.cacheHits++;
      console.log('🎯 缓存命中，跳过 LLM 调用');
      return cached;
    }
    
    // 通过 Gateway 调用
    try {
      const result = await this.llmGateway.call(prompt, options);
      return result;
    } catch (error) {
      console.error('❌ LLM 调用失败:', error.message);
      throw error;
    }
  }

  /**
   * 保存决策到记忆（集成 Memory Manager）
   * @param {string} key - 决策键
   * @param {any} value - 决策值
   */
  recordDecision(key, value) {
    this.memoryManager.setShort(this.sessionId, `decision:${key}`, value);
    console.log(`📝 决策记录: ${key}`);
  }

  /**
   * 获取历史决策
   * @param {number} limit - 限制数量
   * @returns {array} 决策列表
   */
  getRecentDecisions(limit = 10) {
    return this.memoryManager.getDecisions(limit);
  }

  /**
   * 结束会话（持久化记忆）
   * @param {string} summary - 会话摘要
   */
  endSession(summary) {
    this.stats.memoriesPersisted++;
    this.memoryManager.persistSession(this.sessionId, summary);
    console.log(`💾 会话已持久化: ${this.sessionId}`);
  }

  /**
   * 获取综合统计
   * @returns {object} 统计信息
   */
  getStats() {
    return {
      adapter: this.stats,
      contextRouter: this.contextRouter.getStats(),
      promptCache: this.promptCache.getStats(),
      messageBus: this.messageBus.getStats(),
      memoryManager: this.memoryManager.getStats(),
      llmGateway: this.llmGateway.getStats()
    };
  }

  /**
   * 健康检查
   * @returns {object} 健康状态
   */
  healthCheck() {
    const issues = [];
    
    // 检查缓存命中率
    const cacheStats = this.promptCache.getStats();
    const hitRate = parseFloat(cacheStats.hitRate);
    if (cacheStats.total > 10 && hitRate < 20) {
      issues.push('缓存命中率过低（<20%）');
    }
    
    // 检查熔断器状态
    const gatewayHealth = this.llmGateway.healthCheck();
    if (!gatewayHealth.healthy) {
      issues.push(...gatewayHealth.issues);
    }
    
    return {
      healthy: issues.length === 0,
      issues,
      stats: this.getStats()
    };
  }

  /**
   * 清理资源
   */
  cleanup() {
    this.promptCache.cleanup();
    this.memoryManager.cleanup();
    this.messageBus.cleanup(1000);
    console.log('🧹 资源清理完成');
  }
}

// 单例导出
let instance = null;

function getIntegrationAdapter(options = {}) {
  if (!instance) {
    instance = new IntegrationAdapter(options);
  }
  return instance;
}

module.exports = {
  IntegrationAdapter,
  getIntegrationAdapter
};