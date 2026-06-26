/**
 * 生命周期监听器 - 无感知全自动监控
 * 拦截 OpenClaw 5 个关键生命周期事件
 */

import db from '../database/init.js';
import { clawMem } from './retrieval.js';
import config from '../../config/loader.js';

export class LifecycleMonitor {
  constructor() {
    this.events = config.lifecycle.events;
    this.workerQueue = [];
    this.isProcessing = false;
    this.workerIntervalMs = config.lifecycle.workerIntervalMs;
  }

  /**
   * 启动监听器
   */
  start() {
    console.log('👁️  生命周期监听器已启动');
    console.log(`📍 监听事件：${this.events.join(', ')}`);
    
    // 启动后台 Worker
    this._startWorker();
  }

  /**
   * 拦截事件（由 OpenClaw 调用）
   * @param {string} eventName - 事件名称
   * @param {Object} payload - 事件数据
   */
  intercept(eventName, payload) {
    if (!this.events.includes(eventName)) {
      return;
    }
    
    console.log(`📡 拦截事件：${eventName}`);
    
    // 存储原始事件
    const stmt = db.prepare(`
      INSERT INTO lifecycle_events (event_name, session_id, timestamp)
      VALUES (?, ?, ?)
    `);
    
    stmt.run(
      eventName,
      payload.session_id || 'unknown',
      Math.floor(Date.now() / 1000)
    );
    
    // 加入 Worker 队列
    this.workerQueue.push({
      event: eventName,
      payload: payload,
      timestamp: Date.now()
    });
  }

  /**
   * 后台 Worker - 静默处理事件
   */
  async _startWorker() {
    console.log('🔧 后台 Worker 已启动');
    
    while (true) {
      try {
        await this._processQueue();
      } catch (error) {
        console.error('❌ Worker 处理错误:', error.message);
      }
      
      // 等待配置的时间间隔
      await new Promise(resolve => setTimeout(resolve, this.workerIntervalMs));
    }
  }

  /**
   * 处理队列中的事件
   */
  async _processQueue() {
    if (this.workerQueue.length === 0 || this.isProcessing) {
      return;
    }
    
    this.isProcessing = true;
    
    while (this.workerQueue.length > 0) {
      const item = this.workerQueue.shift();
      await this._processEvent(item);
    }
    
    this.isProcessing = false;
  }

  /**
   * 处理单个事件
   * @param {Object} item - 事件项
   */
  async _processEvent(item) {
    const { event, payload } = item;
    
    console.log(`🔧 处理事件：${event}`);
    
    try {
      // 调用 LLM 提炼语义摘要（简化版，实际应调用 LLM）
      const semanticSummary = this._generateSemanticSummary(event, payload);
      
      // 存储到 L0 索引
      const recordId = clawMem.storeL0({
        category: event.split('.')[0],
        timestamp: Math.floor(Date.now() / 1000),
        summary: semanticSummary.substring(0, 100),
        token_cost: semanticSummary.length / 4
      });
      
      // 存储到 L1 时间线
      clawMem.storeL1({
        record_id: recordId,
        session_id: payload.session_id,
        event_type: event,
        timestamp: Math.floor(Date.now() / 1000),
        semantic_summary: semanticSummary,
        tags: this._extractTags(event, payload),
        token_cost: semanticSummary.length / 4
      });
      
      // 存储到 L2 详情（仅当内容有价值时）
      if (this._shouldStoreL2(event, payload)) {
        clawMem.storeL2({
          record_id: recordId,
          full_content: JSON.stringify(payload, null, 2),
          metadata: {
            event_type: event,
            session_id: payload.session_id,
            importance: this._calculateImportance(event, payload)
          },
          token_cost: JSON.stringify(payload).length / 4
        });
      }
      
      console.log(`✅ 事件处理完成：${event} → ${recordId}`);
      
    } catch (error) {
      console.error(`❌ 事件处理失败：${event}`, error.message);
    }
  }

  /**
   * 生成语义摘要（简化版，实际应用应调用 LLM）
   * @param {string} event - 事件名称
   * @param {Object} payload - 事件数据
   * @returns {string} 语义摘要
   */
  _generateSemanticSummary(event, payload) {
    const summaries = {
      'session.start': `会话开始：${payload.session_id || 'unknown'}`,
      'session.end': `会话结束：${payload.session_id || 'unknown'}，持续 ${payload.duration || 0}s`,
      'tool.call': `工具调用：${payload.tool_name || 'unknown'}，参数 ${JSON.stringify(payload.args || {}).length} chars`,
      'memory.read': `记忆读取：${payload.memory_type || 'unknown'}，${payload.count || 0} 条记录`,
      'memory.write': `记忆写入：${payload.memory_type || 'unknown'}，${payload.content?.length || 0} chars`
    };
    
    return summaries[event] || `事件：${event}`;
  }

  /**
   * 提取标签
   * @param {string} event - 事件名称
   * @param {Object} payload - 事件数据
   * @returns {Array} 标签列表
   */
  _extractTags(event, payload) {
    const tags = [event];
    
    if (payload.tool_name) {
      tags.push(`tool:${payload.tool_name}`);
    }
    
    if (payload.session_id) {
      tags.push(`session:${payload.session_id}`);
    }
    
    return tags;
  }

  /**
   * 判断是否需要存储 L2 详情
   * @param {string} event - 事件名称
   * @param {Object} payload - 事件数据
   * @returns {boolean} 是否存储
   */
  _shouldStoreL2(event, payload) {
    // 仅存储高价值事件
    const highValueEvents = ['memory.write', 'tool.call'];
    return highValueEvents.includes(event);
  }

  /**
   * 计算重要性分数
   * @param {string} event - 事件名称
   * @param {Object} payload - 事件数据
   * @returns {number} 重要性分数 (0-1)
   */
  _calculateImportance(event, payload) {
    const baseScores = {
      'session.start': 0.1,
      'session.end': 0.2,
      'tool.call': 0.5,
      'memory.read': 0.3,
      'memory.write': 0.7
    };
    
    return baseScores[event] || 0.5;
  }

  /**
   * 获取监听统计
   * @returns {Object} 统计信息
   */
  getStats() {
    const totalEvents = db.prepare('SELECT COUNT(*) as count FROM lifecycle_events').get().count;
    const processedEvents = db.prepare('SELECT COUNT(*) as count FROM lifecycle_events WHERE processed = 1').get().count;
    
    const eventCounts = db.prepare(`
      SELECT event_name, COUNT(*) as count 
      FROM lifecycle_events 
      GROUP BY event_name
    `).all();
    
    return {
      total_events: totalEvents,
      processed_events: processedEvents,
      pending_events: totalEvents - processedEvents,
      event_breakdown: eventCounts
    };
  }
}

// 导出单例
export const lifecycleMonitor = new LifecycleMonitor();
export default lifecycleMonitor;
