/**
 * 记忆搜索模块
 * 支持关键词搜索、语义搜索、时间范围搜索
 */

import db from '../database/init.js';
import config from '../../config/loader.js';

export class MemorySearch {
  constructor() {
    this.maxResults = config.retrieval.maxRetrieveLimit;
  }

  /**
   * 关键词搜索（L0 索引）
   * @param {string} keyword - 关键词
   * @param {Object} options - 搜索选项
   * @returns {Array} 搜索结果
   */
  searchByKeyword(keyword, options = {}) {
    console.log(`🔍 关键词搜索：${keyword}`);
    
    const { category, timeRange, limit = this.maxResults } = options;
    
    let sql = `
      SELECT * FROM l0_index 
      WHERE summary LIKE ?
    `;
    const params = [`%${keyword}%`];
    
    if (category) {
      sql += ' AND category = ?';
      params.push(category);
    }
    
    if (timeRange) {
      sql += ' AND timestamp BETWEEN ? AND ?';
      params.push(timeRange.start, timeRange.end);
    }
    
    sql += ' ORDER BY timestamp DESC LIMIT ?';
    params.push(limit);
    
    const stmt = db.prepare(sql);
    const results = stmt.all(...params);
    
    console.log(`✅ 找到 ${results.length} 条记录`);
    return results;
  }

  /**
   * 时间范围搜索（L1 时间线）
   * @param {Object} timeRange - 时间范围 {start, end}
   * @param {Object} options - 搜索选项
   * @returns {Array} 搜索结果
   */
  searchByTimeRange(timeRange, options = {}) {
    console.log(`📅 时间范围搜索：${new Date(timeRange.start * 1000).toLocaleString()} - ${new Date(timeRange.end * 1000).toLocaleString()}`);
    
    const { session_id, event_type, limit = this.maxResults } = options;
    
    let sql = `
      SELECT * FROM l1_timeline 
      WHERE timestamp BETWEEN ? AND ?
    `;
    const params = [timeRange.start, timeRange.end];
    
    if (session_id) {
      sql += ' AND session_id = ?';
      params.push(session_id);
    }
    
    if (event_type) {
      sql += ' AND event_type = ?';
      params.push(event_type);
    }
    
    sql += ' ORDER BY timestamp DESC LIMIT ?';
    params.push(limit);
    
    const stmt = db.prepare(sql);
    const results = stmt.all(...params);
    
    console.log(`✅ 找到 ${results.length} 条记录`);
    return results;
  }

  /**
   * 标签搜索（L1 时间线）
   * @param {Array} tags - 标签列表
   * @param {Object} options - 搜索选项
   * @returns {Array} 搜索结果
   */
  searchByTags(tags, options = {}) {
    console.log(`🏷️  标签搜索：${tags.join(', ')}`);
    
    const { limit = this.maxResults } = options;
    
    // 搜索包含所有标签的记录
    const results = [];
    
    for (const tag of tags) {
      const stmt = db.prepare(`
        SELECT * FROM l1_timeline 
        WHERE tags LIKE ?
        ORDER BY timestamp DESC
        LIMIT ?
      `);
      
      const tagResults = stmt.all([`%${tag}%`], limit);
      results.push(...tagResults);
    }
    
    // 去重
    const uniqueResults = results.filter(
      (item, index, self) => index === self.findIndex(t => t.record_id === item.record_id)
    );
    
    console.log(`✅ 找到 ${uniqueResults.length} 条记录`);
    return uniqueResults;
  }

  /**
   * 会话搜索
   * @param {string} sessionId - 会话 ID
   * @param {Object} options - 搜索选项
   * @returns {Object} 会话完整记录
   */
  searchBySession(sessionId, options = {}) {
    console.log(`💬 会话搜索：${sessionId}`);
    
    const { includeDetails = false } = options;
    
    // 搜索 L0 索引
    const l0Stmt = db.prepare(`
      SELECT * FROM l0_index 
      WHERE record_id IN (
        SELECT record_id FROM l1_timeline WHERE session_id = ?
      )
      ORDER BY timestamp DESC
    `);
    const l0Results = l0Stmt.all(sessionId);
    
    // 搜索 L1 时间线
    const l1Stmt = db.prepare(`
      SELECT * FROM l1_timeline 
      WHERE session_id = ?
      ORDER BY timestamp DESC
    `);
    const l1Results = l1Stmt.all(sessionId);
    
    // 可选：加载 L2 详情
    let l2Results = [];
    if (includeDetails) {
      for (const record of l1Results) {
        const l2Stmt = db.prepare('SELECT * FROM l2_details WHERE record_id = ?');
        const l2 = l2Stmt.get(record.record_id);
        if (l2) {
          l2Results.push({
            ...l2,
            metadata: JSON.parse(l2.metadata || '{}')
          });
        }
      }
    }
    
    console.log(`✅ 会话记录：L0(${l0Results.length}) L1(${l1Results.length}) L2(${l2Results.length})`);
    
    return {
      session_id: sessionId,
      l0: l0Results,
      l1: l1Results,
      l2: l2Results,
      total: l0Results.length
    };
  }

  /**
   * 高级搜索（组合搜索）
   * @param {Object} query - 搜索查询
   * @returns {Object} 搜索结果
   */
  advancedSearch(query = {}) {
    console.log(`🔬 高级搜索：${JSON.stringify(query)}`);
    
    const {
      keyword,
      category,
      tags,
      session_id,
      timeRange,
      event_type,
      includeDetails = false,
      limit = this.maxResults
    } = query;
    
    let results = [];
    
    // 根据查询类型选择搜索策略
    if (keyword) {
      results = this.searchByKeyword(keyword, { category, timeRange, limit });
    } else if (session_id) {
      return this.searchBySession(session_id, { includeDetails });
    } else if (tags && tags.length > 0) {
      results = this.searchByTags(tags, { limit });
    } else if (timeRange) {
      results = this.searchByTimeRange(timeRange, { session_id, event_type, limit });
    } else {
      // 默认：返回最近的记录
      const stmt = db.prepare(`
        SELECT * FROM l0_index 
        ORDER BY timestamp DESC 
        LIMIT ?
      `);
      results = stmt.all(limit);
    }
    
    // 可选：加载 L2 详情
    if (includeDetails && results.length > 0) {
      const resultsWithDetails = [];
      
      for (const record of results) {
        const l2Stmt = db.prepare('SELECT * FROM l2_details WHERE record_id = ?');
        const l2 = l2Stmt.get(record.record_id);
        
        resultsWithDetails.push({
          ...record,
          l2: l2 ? {
            ...l2,
            metadata: JSON.parse(l2.metadata || '{}')
          } : null
        });
      }
      
      results = resultsWithDetails;
    }
    
    return {
      success: true,
      count: results.length,
      results: results,
      query: query
    };
  }

  /**
   * 获取搜索统计
   * @returns {Object} 统计信息
   */
  getStats() {
    const l0Count = db.prepare('SELECT COUNT(*) as count FROM l0_index').get().count;
    const l1Count = db.prepare('SELECT COUNT(*) as count FROM l1_timeline').get().count;
    const l2Count = db.prepare('SELECT COUNT(*) as count FROM l2_details').get().count;
    
    // 按分类统计
    const categoryStats = db.prepare(`
      SELECT category, COUNT(*) as count 
      FROM l0_index 
      GROUP BY category
    `).all();
    
    // 按事件类型统计
    const eventStats = db.prepare(`
      SELECT event_type, COUNT(*) as count 
      FROM l1_timeline 
      GROUP BY event_type
    `).all();
    
    // 最近活动时间线
    const recentActivity = db.prepare(`
      SELECT event_type, timestamp 
      FROM l1_timeline 
      ORDER BY timestamp DESC 
      LIMIT 10
    `).all();
    
    return {
      total_records: {
        l0: l0Count,
        l1: l1Count,
        l2: l2Count
      },
      categories: categoryStats,
      event_types: eventStats,
      recent_activity: recentActivity
    };
  }
}

// 导出单例
export const memorySearch = new MemorySearch();
export default memorySearch;
