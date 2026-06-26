#!/usr/bin/env node
/**
 * Message Bus v1.0 - 消息总线
 * 
 * 核心职责：Agent 间解耦通信，统一消息传递
 * 
 * 第一性原理：
 * - Agent 不应直接调用彼此 → 通过消息总线通信
 * - 解耦 = 可扩展 + 可测试 + 可监控
 * - 消息持久化 = 可恢复 + 可审计
 * 
 * 架构：
 * Agent A → publish(channel, msg) → Message Bus → subscribe(channel, handler) → Agent B
 */

const EventEmitter = require('events');
const fs = require('fs');
const path = require('path');

class MessageBus extends EventEmitter {
  constructor(options = {}) {
    super();
    
    this.history = [];
    this.maxHistory = options.maxHistory || 10000;
    this.historyFile = options.historyFile || '/home/ubutu/.openclaw/workspace/logs/message-bus/history.json';
    this.subscriptions = new Map(); // channel → handlers[]
    this.pendingRequests = new Map(); // requestId → {resolve, reject, timer}
    this.requestTimeout = options.requestTimeout || 30000;
    
    // 统计
    this.stats = {
      published: 0,
      delivered: 0,
      requests: 0,
      responses: 0,
      timeouts: 0
    };
    
    this.ensureHistoryDir();
    this.loadHistory();
  }

  /**
   * 确保历史目录存在
   */
  ensureHistoryDir() {
    const dir = path.dirname(this.historyFile);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
  }

  /**
   * 加载历史记录
   */
  loadHistory() {
    if (fs.existsSync(this.historyFile)) {
      try {
        this.history = JSON.parse(fs.readFileSync(this.historyFile, 'utf-8'));
        console.log(`[MessageBus] 加载历史: ${this.history.length} 条`);
      } catch {
        this.history = [];
      }
    }
  }

  /**
   * 保存历史记录
   */
  saveHistory() {
    // 仅保留最近的记录
    if (this.history.length > this.maxHistory) {
      this.history = this.history.slice(-this.maxHistory);
    }
    fs.writeFileSync(this.historyFile, JSON.stringify(this.history, null, 2));
  }

  /**
   * 发布消息（核心方法）
   * @param {string} channel - 频道名
   * @param {object} message - 消息内容
   * @returns {string} 消息 ID
   */
  publish(channel, message) {
    const msgId = this.generateId();
    
    const msg = {
      id: msgId,
      channel,
      payload: message,
      timestamp: Date.now(),
      source: message._source || 'unknown',
      traceId: message._traceId || msgId
    };
    
    // 1. 记录历史
    this.history.push(msg);
    this.stats.published++;
    
    // 2. 发送事件（本地）
    this.emit(channel, msg);
    this.emit('*', msg); // 全局监听
    
    // 3. 检查是否有订阅者
    const handlers = this.subscriptions.get(channel) || [];
    this.stats.delivered += handlers.length;
    
    console.log(`[MessageBus] 发布: ${channel} → ${handlers.length} 订阅者 (id: ${msgId.substring(0, 8)}...)`);
    
    return msgId;
  }

  /**
   * 订阅频道（核心方法）
   * @param {string} channel - 频道名
   * @param {function} handler - 处理函数
   * @returns {function} 取消订阅函数
   */
  subscribe(channel, handler) {
    if (!this.subscriptions.has(channel)) {
      this.subscriptions.set(channel, []);
    }
    
    this.subscriptions.get(channel).push(handler);
    
    // 同时注册 EventEmitter
    this.on(channel, handler);
    
    console.log(`[MessageBus] 订阅: ${channel} (共 ${this.subscriptions.get(channel).length} 个订阅者)`);
    
    // 返回取消订阅函数
    return () => {
      const handlers = this.subscriptions.get(channel) || [];
      const index = handlers.indexOf(handler);
      if (index > -1) {
        handlers.splice(index, 1);
        this.off(channel, handler);
        console.log(`[MessageBus] 取消订阅: ${channel}`);
      }
    };
  }

  /**
   * 请求-响应模式（核心方法）
   * @param {string} channel - 频道名
   * @param {object} message - 请求消息
   * @param {number} timeout - 超时时间（毫秒）
   * @returns {Promise<object>} 响应
   */
  async request(channel, message, timeout = this.requestTimeout) {
    return new Promise((resolve, reject) => {
      const requestId = this.generateId();
      const replyChannel = `${channel}.response.${requestId}`;
      
      // 设置超时
      const timer = setTimeout(() => {
        this.pendingRequests.delete(requestId);
        this.stats.timeouts++;
        reject(new Error(`MessageBus request timeout: ${channel} (requestId: ${requestId.substring(0, 8)}...)`));
      }, timeout);
      
      // 存储请求
      this.pendingRequests.set(requestId, { resolve, reject, timer });
      
      // 订阅响应频道
      const unsubscribe = this.subscribe(replyChannel, (msg) => {
        clearTimeout(timer);
        this.pendingRequests.delete(requestId);
        this.stats.responses++;
        resolve(msg.payload);
      });
      
      // 发送请求（带回复频道）
      this.stats.requests++;
      this.publish(channel, {
        ...message,
        _requestId: requestId,
        _replyTo: replyChannel
      });
      
      console.log(`[MessageBus] 请求: ${channel} (requestId: ${requestId.substring(0, 8)}..., timeout: ${timeout}ms)`);
    });
  }

  /**
   * 响应请求
   * @param {string} replyTo - 回复频道
   * @param {object} response - 响应内容
   */
  reply(replyTo, response) {
    this.publish(replyTo, response);
  }

  /**
   * 广播消息（所有订阅者）
   * @param {object} message - 消息内容
   */
  broadcast(message) {
    return this.publish('*', message);
  }

  /**
   * 发布任务完成事件
   */
  taskCompleted(taskId, result, agentId) {
    return this.publish('task.completed', {
      taskId,
      result,
      agentId,
      timestamp: Date.now()
    });
  }

  /**
   * 发布任务失败事件
   */
  taskFailed(taskId, error, agentId) {
    return this.publish('task.failed', {
      taskId,
      error: error.message || error,
      agentId,
      timestamp: Date.now()
    });
  }

  /**
   * 发布 Agent 状态变化事件
   */
  agentStatusChanged(agentId, status, details = {}) {
    return this.publish('agent.status', {
      agentId,
      status,
      details,
      timestamp: Date.now()
    });
  }

  /**
   * 获取频道订阅者数量
   */
  getSubscriberCount(channel) {
    return (this.subscriptions.get(channel) || []).length;
  }

  /**
   * 获取历史消息
   */
  getHistory(channel = null, limit = 100) {
    let messages = this.history;
    
    if (channel) {
      messages = messages.filter(m => m.channel === channel);
    }
    
    return messages.slice(-limit);
  }

  /**
   * 获取统计信息
   */
  getStats() {
    return {
      ...this.stats,
      subscriptions: this.subscriptions.size,
      historySize: this.history.length,
      pendingRequests: this.pendingRequests.size
    };
  }

  /**
   * 清理历史
   */
  cleanup(keepLast = 1000) {
    if (this.history.length > keepLast) {
      this.history = this.history.slice(-keepLast);
      this.saveHistory();
      console.log(`[MessageBus] 清理历史，保留 ${keepLast} 条`);
    }
  }

  /**
   * 生成唯一 ID
   */
  generateId() {
    return Date.now().toString(36) + Math.random().toString(36).substring(2, 10);
  }
}

// 单例导出
let instance = null;

function getMessageBus(options = {}) {
  if (!instance) {
    instance = new MessageBus(options);
  }
  return instance;
}

module.exports = {
  MessageBus,
  getMessageBus
};