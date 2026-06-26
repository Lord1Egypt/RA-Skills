/**
 * 历史记录管理模块
 * 
 * 功能：
 * - 操作历史记录
 * - 历史搜索
 * - 历史过滤
 * - 历史导出
 * - 历史统计
 */

class HistoryManager {
  constructor(options = {}) {
    this.maxRecords = options.maxRecords || 1000;
    this.records = [];
    this.searchIndex = new Map();
  }

  /**
   * 添加记录
   * @param {Object} record - 记录
   */
  addRecord(record) {
    const timestamp = Date.now();
    const id = this._generateId();
    
    const newRecord = {
      id,
      timestamp,
      type: record.type || 'unknown',
      action: record.action || '',
      details: record.details || {},
      status: record.status || 'success',
      userInput: record.userInput || '',
      assistantOutput: record.assistantOutput || '',
      context: record.context || {},
      duration: record.duration || 0
    };

    this.records.push(newRecord);
    
    // 更新搜索索引
    this._updateIndex(newRecord);

    // 限制记录数量
    if (this.records.length > this.maxRecords) {
      const removed = this.records.shift();
      this._removeFromIndex(removed);
    }

    return newRecord;
  }

  /**
   * 获取历史记录
   * @param {Object} options - 选项
   * @returns {Array}
   */
  getHistory(options = {}) {
    let result = [...this.records];

    // 按类型过滤
    if (options.type) {
      result = result.filter(r => r.type === options.type);
    }

    // 按状态过滤
    if (options.status) {
      result = result.filter(r => r.status === options.status);
    }

    // 按时间范围过滤
    if (options.startTime) {
      result = result.filter(r => r.timestamp >= options.startTime);
    }
    if (options.endTime) {
      result = result.filter(r => r.timestamp <= options.endTime);
    }

    // 搜索
    if (options.search) {
      result = this._search(result, options.search);
    }

    // 分页
    const page = parseInt(options.page) || 1;
    const limit = parseInt(options.limit) || 20;
    const start = (page - 1) * limit;
    
    const total = result.length;
    result = result.slice(start, start + limit);

    return {
      records: result,
      total,
      page,
      limit,
      hasMore: start + limit < total
    };
  }

  /**
   * 搜索历史
   * @param {string} keyword - 关键词
   * @returns {Array}
   */
  search(keyword) {
    if (!keyword) return [];

    const results = [];
    const kw = keyword.toLowerCase();

    for (const record of this.records) {
      let match = false;

      // 搜索类型
      if (record.type && record.type.toLowerCase().includes(kw)) {
        match = true;
      }

      // 搜索操作
      if (record.action && record.action.toLowerCase().includes(kw)) {
        match = true;
      }

      // 搜索用户输入
      if (record.userInput && record.userInput.toLowerCase().includes(kw)) {
        match = true;
      }

      // 搜索详情
      if (record.details) {
        const detailsStr = JSON.stringify(record.details).toLowerCase();
        if (detailsStr.includes(kw)) {
          match = true;
        }
      }

      if (match) {
        results.push(record);
      }
    }

    return results;
  }

  /**
   * 按类型统计
   * @returns {Object}
   */
  getStatsByType() {
    const stats = {};

    for (const record of this.records) {
      const type = record.type || 'unknown';
      if (!stats[type]) {
        stats[type] = {
          count: 0,
          success: 0,
          failed: 0,
          totalDuration: 0
        };
      }

      stats[type].count++;
      if (record.status === 'success') {
        stats[type].success++;
      } else {
        stats[type].failed++;
      }
      stats[type].totalDuration += record.duration || 0;
    }

    return stats;
  }

  /**
   * 按时间统计
   * @param {string} period - 周期 (day/week/month)
   * @returns {Object}
   */
  getStatsByTime(period = 'day') {
    const stats = {};
    // const now = Date.now();

    for (const record of this.records) {
      let key;
      const date = new Date(record.timestamp);

      switch (period) {
        case 'hour':
          key = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:00`;
          break;
        case 'day':
          key = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
          break;
        case 'week': {
          const weekNum = Math.ceil((date - new Date(date.getFullYear(), 0, 1)) / (7 * 24 * 60 * 60 * 1000));
          key = `${date.getFullYear()}-W${String(weekNum).padStart(2, '0')}`;
          break;
        }
        case 'month':
          key = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
          break;
        default:
          key = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
      }

      if (!stats[key]) {
        stats[key] = 0;
      }
      stats[key]++;
    }

    return stats;
  }

  /**
   * 获取最近记录
   * @param {number} limit - 数量
   * @returns {Array}
   */
  getRecent(limit = 10) {
    return this.records.slice(-limit).reverse();
  }

  /**
   * 获取指定记录
   * @param {string} id - 记录 ID
   * @returns {Object}
   */
  getById(id) {
    return this.records.find(r => r.id === id);
  }

  /**
   * 删除记录
   * @param {string} id - 记录 ID
   * @returns {boolean}
   */
  deleteRecord(id) {
    const index = this.records.findIndex(r => r.id === id);
    if (index !== -1) {
      const removed = this.records.splice(index, 1)[0];
      this._removeFromIndex(removed);
      return true;
    }
    return false;
  }

  /**
   * 清空历史
   * @returns {number} 删除数量
   */
  clearHistory() {
    const count = this.records.length;
    this.records = [];
    this.searchIndex.clear();
    return count;
  }

  /**
   * 导出历史
   * @param {Object} options - 选项
   * @returns {string}
   */
  export(options = {}) {
    const { format = 'json', filter = {} } = options;
    const data = this.getHistory(filter);

    switch (format) {
      case 'json':
        return JSON.stringify(data.records, null, 2);
      
      case 'csv':
        return this._exportCSV(data.records);
      
      case 'markdown':
        return this._exportMarkdown(data.records);
      
      default:
        return JSON.stringify(data.records);
    }
  }

  /**
   * 格式化历史为文本
   * @param {Object} options - 选项
   * @returns {string}
   */
  formatHistory(options = {}) {
    const result = this.getHistory(options);
    const records = result.records;

    if (records.length === 0) {
      return '暂无历史记录';
    }

    let output = `📋 历史记录 (${result.total}条)\n`;
    output += `━━━━━━━━━━━━━━━━━━━━\n`;

    records.forEach((record, index) => {
      const time = this._formatTime(record.timestamp);
      const icon = record.status === 'success' ? '✅' : '❌';
      const typeIcon = this._getTypeIcon(record.type);
      
      output += `${index + 1}. ${typeIcon} ${record.action || record.type}\n`;
      output += `   ${icon} ${time}`;
      
      if (record.duration > 0) {
        output += ` | ⏱️ ${record.duration}ms`;
      }
      output += '\n';

      if (record.userInput) {
        const input = record.userInput.length > 30 
          ? record.userInput.substring(0, 30) + '...' 
          : record.userInput;
        output += `   👤 ${input}\n`;
      }
    });

    if (result.hasMore) {
      output += `\n... 还有 ${result.total - records.length} 条记录\n`;
    }

    return output;
  }

  /**
   * 格式化统计
   * @returns {string}
   */
  formatStats() {
    const typeStats = this.getStatsByType();
    const total = this.records.length;
    const success = this.records.filter(r => r.status === 'success').length;
    const failed = total - success;

    let output = `📊 历史统计\n`;
    output += `━━━━━━━━━━━━━━━━━━━━\n`;
    output += `总记录：${total} 条\n`;
    output += `成功：${success} ✅\n`;
    output += `失败：${failed} ❌\n\n`;

    output += `📈 按类型统计：\n`;
    for (const [type, stats] of Object.entries(typeStats)) {
      output += `\n${this._getTypeIcon(type)} ${type}\n`;
      output += `   总计：${stats.count} | 成功：${stats.success} | 失败：${stats.failed}\n`;
      if (stats.totalDuration > 0) {
        output += `   平均耗时：${Math.round(stats.totalDuration / stats.count)}ms\n`;
      }
    }

    return output;
  }

  /**
   * 生成 ID
   * @private
   */
  _generateId() {
    return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }

  /**
   * 更新搜索索引
   * @private
   */
  _updateIndex(record) {
    const keywords = [];
    
    if (record.type) keywords.push(record.type.toLowerCase());
    if (record.action) keywords.push(record.action.toLowerCase());
    if (record.userInput) {
      const words = record.userInput.toLowerCase().split(/\s+/);
      keywords.push(...words);
    }

    for (const kw of keywords) {
      if (!this.searchIndex.has(kw)) {
        this.searchIndex.set(kw, []);
      }
      this.searchIndex.get(kw).push(record.id);
    }
  }

  /**
   * 从索引中移除
   * @private
   */
  _removeFromIndex(_record) {
    // 简化实现：清空并重建索引
    this.searchIndex.clear();
    for (const r of this.records) {
      this._updateIndex(r);
    }
  }

  /**
   * 搜索
   * @private
   */
  _search(records, keyword) {
    if (!keyword) return records;

    const kw = keyword.toLowerCase();
    return records.filter(r => {
      if (r.type && r.type.toLowerCase().includes(kw)) return true;
      if (r.action && r.action.toLowerCase().includes(kw)) return true;
      if (r.userInput && r.userInput.toLowerCase().includes(kw)) return true;
      return false;
    });
  }

  /**
   * 导出 CSV
   * @private
   */
  _exportCSV(records) {
    const headers = ['ID', '时间', '类型', '操作', '状态', '耗时'];
    const rows = [headers.join(',')];

    for (const r of records) {
      const row = [
        r.id,
        new Date(r.timestamp).toISOString(),
        r.type || '',
        `"${(r.action || '').replace(/"/g, '""')}"`,
        r.status,
        r.duration || 0
      ];
      rows.push(row.join(','));
    }

    return rows.join('\n');
  }

  /**
   * 导出 Markdown
   * @private
   */
  _exportMarkdown(records) {
    let md = `# 历史记录\n\n`;
    md += `导出时间：${new Date().toLocaleString()}\n\n`;
    md += `| ID | 时间 | 类型 | 操作 | 状态 | 耗时 |\n`;
    md += `|---|---|---|---|---|---|\n`;

    for (const r of records) {
      const time = new Date(r.timestamp).toLocaleString();
      md += `| ${r.id} | ${time} | ${r.type || ''} | ${r.action || ''} | ${r.status} | ${r.duration || 0}ms |\n`;
    }

    return md;
  }

  /**
   * 格式化时间
   * @private
   */
  _formatTime(timestamp) {
    const date = new Date(timestamp);
    const now = new Date();
    const diff = now - date;

    // 小于 1 分钟
    if (diff < 60000) {
      return '刚刚';
    }

    // 小于 1 小时
    if (diff < 3600000) {
      const mins = Math.floor(diff / 60000);
      return `${mins} 分钟前`;
    }

    // 小于 1 天
    if (diff < 86400000) {
      const hours = Math.floor(diff / 3600000);
      return `${hours} 小时前`;
    }

    // 小于 7 天
    if (diff < 604800000) {
      const days = Math.floor(diff / 86400000);
      return `${days} 天前`;
    }

    // 超过 7 天，显示具体日期
    return `${date.getMonth() + 1}/${date.getDate()} ${date.getHours()}:${String(date.getMinutes()).padStart(2, '0')}`;
  }

  /**
   * 获取类型图标
   * @private
   */
  _getTypeIcon(type) {
    const icons = {
      'files': '📁',
      'download': '📥',
      'upload': '📤',
      'share': '📦',
      'transfer': '🔄',
      'delete': '🗑️',
      'search': '🔍',
      'organize': '📂',
      'cleanup': '🧹',
      'lixian': '⚡',
      'auth': '🔐',
      'error': '❌',
      'unknown': '❓'
    };
    return icons[type] || '📝';
  }
}

module.exports = HistoryManager;
