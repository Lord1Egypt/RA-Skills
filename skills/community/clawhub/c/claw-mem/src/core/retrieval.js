/**
 * ClawMem 核心模块 - 三层检索工作流
 * L0: 极简索引 → L1: 时间线 → L2: 完整详情
 */

import db from '../database/init.js';
import { v4 as uuidv4 } from 'uuid';
import config from '../../config/loader.js';

export class ClawMemCore {
  constructor(options = {}) {
    this.options = {
      maxL0SummaryLength: config.retrieval.l0MaxSummaryLength,
      maxL1SummaryLength: config.retrieval.l1MaxSummaryLength,
      l2StoreHighValueOnly: config.retrieval.l2StoreHighValueOnly,
      tokenEstimateRatio: config.retrieval.tokenEstimateRatio,
      maxRetrieveLimit: config.retrieval.maxRetrieveLimit,
      ...options
    };
  }

  /**
   * L0: 存储极简索引（Token 消耗 < 100）
   * @param {Object} record - 记录数据
   * @returns {string} record_id
   */
  storeL0(record) {
    const recordId = record.record_id || uuidv4();
    const summary = record.summary.substring(0, this.options.maxL0SummaryLength);
    
    const stmt = db.prepare(`
      INSERT OR REPLACE INTO l0_index 
      (record_id, category, timestamp, summary, token_cost)
      VALUES (?, ?, ?, ?, ?)
    `);
    
    stmt.run(
      recordId,
      record.category,
      record.timestamp || Math.floor(Date.now() / 1000),
      summary,
      record.token_cost || this._estimateTokenCost(summary)
    );
    
    console.log(`📌 L0 索引已存储：${recordId} (${summary.length} chars)`);
    return recordId;
  }

  /**
   * L1: 存储时间线索引（Token 消耗 < 500）
   * @param {Object} record - 记录数据
   * @returns {string} record_id
   */
  storeL1(record) {
    const recordId = record.record_id || uuidv4();
    const semanticSummary = record.semantic_summary.substring(0, this.options.maxL1SummaryLength);
    
    const stmt = db.prepare(`
      INSERT OR REPLACE INTO l1_timeline 
      (record_id, session_id, event_type, timestamp, semantic_summary, tags, token_cost)
      VALUES (?, ?, ?, ?, ?, ?, ?)
    `);
    
    stmt.run(
      recordId,
      record.session_id,
      record.event_type,
      record.timestamp || Math.floor(Date.now() / 1000),
      semanticSummary,
      JSON.stringify(record.tags || []),
      record.token_cost || this._estimateTokenCost(semanticSummary)
    );
    
    console.log(`📍 L1 时间线索引已存储：${recordId} (${semanticSummary.length} chars)`);
    return recordId;
  }

  /**
   * L2: 存储完整详情（按需加载）
   * @param {Object} record - 记录数据
   * @returns {string} record_id
   */
  storeL2(record) {
    const recordId = record.record_id || uuidv4();
    
    const stmt = db.prepare(`
      INSERT OR REPLACE INTO l2_details 
      (record_id, full_content, metadata, token_cost)
      VALUES (?, ?, ?, ?)
    `);
    
    stmt.run(
      recordId,
      record.full_content,
      JSON.stringify(record.metadata || {}),
      record.token_cost || this._estimateTokenCost(record.full_content)
    );
    
    console.log(`📦 L2 完整详情已存储：${recordId} (${record.full_content?.length || 0} chars)`);
    return recordId;
  }

  /**
   * 检索 L0 索引（极低 Token 消耗）
   * @param {Object} query - 查询条件
   * @returns {Array} 索引列表
   */
  searchL0(query = {}) {
    let sql = 'SELECT * FROM l0_index WHERE 1=1';
    const params = [];
    
    if (query.category) {
      sql += ' AND category = ?';
      params.push(query.category);
    }
    
    if (query.timeRange) {
      sql += ' AND timestamp BETWEEN ? AND ?';
      params.push(query.timeRange.start, query.timeRange.end);
    }
    
    if (query.limit) {
      sql += ' LIMIT ?';
      params.push(query.limit);
    }
    
    const stmt = db.prepare(sql);
    const results = stmt.all(...params);
    
    console.log(`🔍 L0 检索完成：${results.length} 条记录`);
    return results;
  }

  /**
   * 检索 L1 时间线（中等 Token 消耗）
   * @param {string} recordId - 记录 ID
   * @returns {Object|null} 时间线索引
   */
  getL1(recordId) {
    const stmt = db.prepare('SELECT * FROM l1_timeline WHERE record_id = ?');
    const result = stmt.get(recordId);
    
    if (result) {
      console.log(`📍 L1 检索完成：${recordId}`);
    }
    
    return result || null;
  }

  /**
   * 检索 L2 完整详情（高 Token 消耗，按需加载）
   * @param {string} recordId - 记录 ID
   * @returns {Object|null} 完整记录
   */
  getL2(recordId) {
    const stmt = db.prepare('SELECT * FROM l2_details WHERE record_id = ?');
    const result = stmt.get(recordId);
    
    if (result) {
      console.log(`📦 L2 检索完成：${recordId} (${result.full_content?.length || 0} chars)`);
      // 解析元数据
      result.metadata = JSON.parse(result.metadata || '{}');
    }
    
    return result || null;
  }

  /**
   * 三层检索工作流
   * 1. L0 搜索相关记录
   * 2. L1 获取时间线索引
   * 3. L2 按需加载完整详情
   * @param {Object} query - 查询条件
   * @returns {Object} 检索结果
   */
  async retrieve(query = {}) {
    console.log(`🚀 开始三层检索工作流...`);
    
    // Step 1: L0 极简索引搜索
    const l0Results = this.searchL0(query);
    console.log(`✅ L0 找到 ${l0Results.length} 条相关记录`);
    
    if (l0Results.length === 0) {
      return {
        success: true,
        count: 0,
        records: [],
        tokenCost: 0
      };
    }
    
    // Step 2: L1 获取时间线索引（仅当需要时）
    const l1Results = [];
    if (query.includeTimeline !== false) {
      for (const record of l0Results) {
        const l1 = this.getL1(record.record_id);
        if (l1) {
          l1Results.push(l1);
        }
      }
      console.log(`✅ L1 获取 ${l1Results.length} 条时间线索引`);
    }
    
    // Step 3: L2 按需加载完整详情（仅当明确需要时）
    const l2Results = [];
    if (query.includeDetails === true) {
      for (const record of l0Results) {
        const l2 = this.getL2(record.record_id);
        if (l2) {
          l2Results.push(l2);
        }
      }
      console.log(`✅ L2 加载 ${l2Results.length} 条完整详情`);
    }
    
    // 计算总 Token 消耗
    const totalTokenCost = l0Results.reduce((sum, r) => sum + (r.token_cost || 0), 0) +
                          l1Results.reduce((sum, r) => sum + (r.token_cost || 0), 0) +
                          l2Results.reduce((sum, r) => sum + (r.token_cost || 0), 0);
    
    return {
      success: true,
      count: l0Results.length,
      l0: l0Results,
      l1: l1Results,
      l2: l2Results,
      tokenCost: totalTokenCost,
      message: `检索完成：L0(${l0Results.length}) → L1(${l1Results.length}) → L2(${l2Results.length})`
    };
  }

  /**
   * 估算 Token 消耗（简单估算：1 token ≈ 4 chars）
   * @param {string} text - 文本内容
   * @returns {number} 估算的 token 数
   */
  _estimateTokenCost(text) {
    return Math.ceil((text?.length || 0) / 4);
  }

  /**
   * 获取统计信息
   * @returns {Object} 统计信息
   */
  getStats() {
    const l0Count = db.prepare('SELECT COUNT(*) as count FROM l0_index').get().count;
    const l1Count = db.prepare('SELECT COUNT(*) as count FROM l1_timeline').get().count;
    const l2Count = db.prepare('SELECT COUNT(*) as count FROM l2_details').get().count;
    const totalTokenCost = db.prepare(`
      SELECT COALESCE(SUM(token_cost), 0) as total FROM (
        SELECT token_cost FROM l0_index
        UNION ALL SELECT token_cost FROM l1_timeline
        UNION ALL SELECT token_cost FROM l2_details
      )
    `).get().total;
    
    return {
      l0_count: l0Count,
      l1_count: l1Count,
      l2_count: l2Count,
      total_records: l0Count + l1Count + l2Count,
      total_token_cost: totalTokenCost,
      estimated_savings: '60-80%' // 相比直接存储完整内容
    };
  }
}

// 导出单例
export const clawMem = new ClawMemCore();
export default clawMem;
