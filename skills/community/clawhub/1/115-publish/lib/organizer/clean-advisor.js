/**
 * 115 智能清理模块
 * 
 * 功能：
 * - 回收站统计
 * - 重复文件检测
 * - 大文件查找
 * - 临时文件清理
 * - 清理建议
 */

const HttpClient = require('../client/http-client');
const ErrorHandler = require('../error/error-handler');

class CleanAdvisor {
  constructor(cookie) {
    this.http = new HttpClient(cookie);
    this.errorHandler = new ErrorHandler();
  }

  /**
   * 获取回收站统计
   * @returns {Object} 统计信息
   */
  async getRecycleStats() {
    try {
      // 注意：回收站 API 可能 404，需要错误处理
      const response = await this.http.get('/recycle/list', {
        offset: '0',
        limit: '1'
      });

      if (!response.state) {
        // 如果 API 不可用，返回提示信息
        return {
          success: false,
          available: false,
          message: '回收站 API 暂不可用',
          stats: null
        };
      }

      const files = response.data?.files || response.data || [];
      const totalSize = files.reduce((sum, f) => sum + parseInt(f.file_size || '0'), 0);

      return {
        success: true,
        available: true,
        stats: {
          count: files.length,
          totalSize,
          oldestFile: files[files.length - 1],
          newestFile: files[0]
        },
        message: `回收站有 ${files.length} 个文件，共 ${this._formatSize(totalSize)}`
      };
    } catch (error) {
      // API 可能 404
      return {
        success: false,
        available: false,
        message: '回收站功能暂不可用',
        stats: null
      };
    }
  }

  /**
   * 获取空间使用分析
   * @returns {Object} 分析结果
   */
  async getSpaceAnalysis() {
    try {
      const response = await this.http.get('/files/index_info', {
        count_space_nums: '1'
      });

      if (!response.state) {
        throw this.errorHandler.fromApiResponse(response) || new Error('获取空间信息失败');
      }

      const data = response.data || {};
      const total = parseInt(data.total || '0');
      const used = parseInt(data.used || '0');
      const remain = total - used;
      const percent = total > 0 ? (used / total * 100).toFixed(2) : 0;

      return {
        success: true,
        analysis: {
          total,
          used,
          remain,
          percent: parseFloat(percent),
          level: this._getSpaceLevel(percent)
        },
        message: `已用 ${this._formatSize(used)} / ${this._formatSize(total)} (${percent}%)`
      };
    } catch (error) {
      if (error.type) throw error;
      throw this.errorHandler.fromHttpError(error);
    }
  }

  /**
   * 查找大文件
   * @param {Object} options - 选项
   * @returns {Object} 大文件列表
   */
  async findLargeFiles(options = {}) {
    try {
      const minSize = options.minSize || 104857600; // 默认 100MB
      const limit = options.limit || 20;

      const response = await this.http.get('/files', {
        aid: '1',
        cid: options.cid || '0',
        o: 'file_size', // 按大小排序
        asc: '0', // 降序
        offset: '0',
        limit: String(limit),
        show_dir: '0', // 只显示文件
        format: 'json'
      });

      if (!response.state) {
        throw this.errorHandler.fromApiResponse(response) || new Error('获取文件列表失败');
      }

      const files = (response.data || []).filter(f => {
        const size = parseInt(f.file_size || '0');
        return size >= minSize && !f.is_folder;
      });

      return {
        success: true,
        files,
        count: files.length,
        totalSize: files.reduce((sum, f) => sum + parseInt(f.file_size || '0'), 0),
        message: `找到 ${files.length} 个大于 ${this._formatSize(minSize)} 的文件`
      };
    } catch (error) {
      if (error.type) throw error;
      throw this.errorHandler.fromHttpError(error);
    }
  }

  /**
   * 查找重复文件（基于文件名和大小）
   * @param {Object} options - 选项
   * @returns {Object} 重复文件列表
   */
  async findDuplicateFiles(options = {}) {
    try {
      const limit = options.limit || 100;
      
      // 获取文件列表
      const response = await this.http.get('/files', {
        aid: '1',
        cid: options.cid || '0',
        offset: '0',
        limit: String(limit),
        show_dir: '0',
        format: 'json'
      });

      if (!response.state) {
        throw this.errorHandler.fromApiResponse(response) || new Error('获取文件列表失败');
      }

      const files = response.data || [];
      const fileMap = new Map();
      const duplicates = [];

      // 按文件名 + 大小分组
      files.forEach(file => {
        if (file.is_folder) return;
        
        const key = `${file.file_name}_${file.file_size}`;
        if (fileMap.has(key)) {
          const group = fileMap.get(key);
          if (!duplicates.find(d => d.key === key)) {
            duplicates.push({
              key,
              fileName: file.file_name,
              fileSize: file.file_size,
              files: [...group]
            });
          }
          duplicates.find(d => d.key === key).files.push(file);
        } else {
          fileMap.set(key, [file]);
        }
      });

      // 计算可清理空间
      const cleanableSize = duplicates.reduce((sum, d) => {
        return sum + parseInt(d.fileSize || '0') * (d.files.length - 1);
      }, 0);

      return {
        success: true,
        duplicates,
        count: duplicates.length,
        totalDuplicateFiles: duplicates.reduce((sum, d) => sum + d.files.length, 0),
        cleanableSize,
        message: `找到 ${duplicates.length} 组重复文件，可释放 ${this._formatSize(cleanableSize)}`
      };
    } catch (error) {
      if (error.type) throw error;
      throw this.errorHandler.fromHttpError(error);
    }
  }

  /**
   * 查找临时文件
   * @param {Object} options - 选项
   * @returns {Object} 临时文件列表
   */
  async findTempFiles(options = {}) {
    try {
      const limit = options.limit || 50;
      const tempPatterns = [
        /\.tmp$/i,
        /\.temp$/i,
        /\.cache$/i,
        /^~\$/,
        /\.bak$/i,
        /\.swp$/i
      ];

      const response = await this.http.get('/files', {
        aid: '1',
        cid: options.cid || '0',
        offset: '0',
        limit: String(limit),
        format: 'json'
      });

      if (!response.state) {
        throw this.errorHandler.fromApiResponse(response) || new Error('获取文件列表失败');
      }

      const files = response.data || [];
      const tempFiles = files.filter(file => {
        if (file.is_folder) return false;
        const name = file.file_name || '';
        return tempPatterns.some(pattern => pattern.test(name));
      });

      return {
        success: true,
        tempFiles,
        count: tempFiles.length,
        totalSize: tempFiles.reduce((sum, f) => sum + parseInt(f.file_size || '0'), 0),
        message: `找到 ${tempFiles.length} 个临时文件`
      };
    } catch (error) {
      if (error.type) throw error;
      throw this.errorHandler.fromHttpError(error);
    }
  }

  /**
   * 获取清理建议
   * @returns {Object} 清理建议
   */
  async getCleanSuggestions() {
    try {
      const suggestions = [];
      
      // 获取空间分析
      const spaceAnalysis = await this.getSpaceAnalysis();
      const spacePercent = spaceAnalysis.analysis?.percent || 0;

      if (spacePercent > 90) {
        suggestions.push({
          type: 'urgent',
          title: '🚨 空间严重不足',
          description: `存储空间已使用 ${spacePercent}%，建议立即清理`,
          priority: 1,
          actions: ['清理回收站', '删除大文件', '清理重复文件']
        });
      } else if (spacePercent > 80) {
        suggestions.push({
          type: 'warning',
          title: '⚠️ 空间紧张',
          description: `存储空间已使用 ${spacePercent}%，建议清理`,
          priority: 2,
          actions: ['清理回收站', '整理文件']
        });
      }

      // 查找大文件
      try {
        const largeFiles = await this.findLargeFiles({ limit: 10 });
        if (largeFiles.count > 0) {
          suggestions.push({
            type: 'info',
            title: '📦 大文件清理',
            description: `找到 ${largeFiles.count} 个大文件，共 ${this._formatSize(largeFiles.totalSize)}`,
            priority: 3,
            actions: ['查看大文件', '选择性删除']
          });
        }
      } catch (e) {
        // 忽略错误
      }

      // 查找重复文件
      try {
        const duplicates = await this.findDuplicateFiles({ limit: 50 });
        if (duplicates.count > 0) {
          suggestions.push({
            type: 'info',
            title: '🔄 重复文件',
            description: `找到 ${duplicates.count} 组重复文件，可释放 ${this._formatSize(duplicates.cleanableSize)}`,
            priority: 4,
            actions: ['查看重复文件', '清理重复']
          });
        }
      } catch (e) {
        // 忽略错误
      }

      // 查找临时文件
      try {
        const tempFiles = await this.findTempFiles({ limit: 50 });
        if (tempFiles.count > 0) {
          suggestions.push({
            type: 'info',
            title: '🗑️ 临时文件',
            description: `找到 ${tempFiles.count} 个临时文件`,
            priority: 5,
            actions: ['查看临时文件', '清理临时文件']
          });
        }
      } catch (e) {
        // 忽略错误
      }

      // 回收站
      try {
        const recycleStats = await this.getRecycleStats();
        if (recycleStats.available && recycleStats.stats?.count > 0) {
          suggestions.push({
            type: 'info',
            title: '♻️ 回收站',
            description: `回收站有 ${recycleStats.stats.count} 个文件`,
            priority: 6,
            actions: ['清空回收站']
          });
        }
      } catch (e) {
        // 忽略错误
      }

      // 按优先级排序
      suggestions.sort((a, b) => a.priority - b.priority);

      return {
        success: true,
        suggestions,
        count: suggestions.length,
        message: suggestions.length > 0 
          ? `找到 ${suggestions.length} 条清理建议`
          : '存储空间健康，无需清理'
      };
    } catch (error) {
      if (error.type) throw error;
      throw this.errorHandler.fromHttpError(error);
    }
  }

  /**
   * 格式化清理建议
   * @param {Object} result - 建议结果
   * @returns {string}
   */
  formatSuggestions(result) {
    if (!result.suggestions || result.suggestions.length === 0) {
      return '✅ 存储空间健康，无需清理';
    }

    let output = `🧹 清理建议 (${result.suggestions.length}条)\n`;
    output += `━━━━━━━━━━━━━━━━━━━━\n`;

    result.suggestions.forEach((suggestion, index) => {
      const icon = suggestion.type === 'urgent' ? '🚨' : 
                   suggestion.type === 'warning' ? '⚠️' : 'ℹ️';
      
      output += `${index + 1}. ${icon} ${suggestion.title}\n`;
      output += `   ${suggestion.description}\n`;
      
      if (suggestion.actions && suggestion.actions.length > 0) {
        output += `   操作：${suggestion.actions.join(' → ')}\n`;
      }
      output += `\n`;
    });

    return output;
  }

  /**
   * 格式化大文件列表
   * @param {Object} result - 大文件结果
   * @returns {string}
   */
  formatLargeFiles(result) {
    if (!result.files || result.files.length === 0) {
      return '没有找到大文件';
    }

    let output = `📦 大文件列表 (${result.files.length}个)\n`;
    output += `━━━━━━━━━━━━━━━━━━━━\n`;
    output += `总计：${this._formatSize(result.totalSize)}\n\n`;

    result.files.slice(0, 10).forEach((file, index) => {
      const size = this._formatSize(parseInt(file.file_size || '0'));
      output += `${index + 1}. ${file.file_name}\n`;
      output += `   大小：${size}\n`;
      output += `   ID: ${file.fuuid || file.file_id}\n\n`;
    });

    if (result.files.length > 10) {
      output += `... 还有 ${result.files.length - 10} 个文件\n`;
    }

    return output;
  }

  /**
   * 格式化重复文件列表
   * @param {Object} result - 重复文件结果
   * @returns {string}
   */
  formatDuplicates(result) {
    if (!result.duplicates || result.duplicates.length === 0) {
      return '没有找到重复文件';
    }

    let output = `🔄 重复文件 (${result.duplicates.length}组)\n`;
    output += `━━━━━━━━━━━━━━━━━━━━\n`;
    output += `可释放：${this._formatSize(result.cleanableSize)}\n\n`;

    result.duplicates.slice(0, 5).forEach((group, index) => {
      const size = this._formatSize(parseInt(group.fileSize || '0'));
      output += `${index + 1}. ${group.fileName} (${size})\n`;
      output += `   重复：${group.files.length} 份\n`;
      output += `   位置：${group.files.map(f => f.category_name || '根目录').join(', ')}\n\n`;
    });

    if (result.duplicates.length > 5) {
      output += `... 还有 ${result.duplicates.length - 5} 组重复文件\n`;
    }

    return output;
  }

  /**
   * 获取空间等级
   * @private
   */
  _getSpaceLevel(percent) {
    if (percent >= 90) return 'critical';
    if (percent >= 80) return 'warning';
    if (percent >= 60) return 'normal';
    return 'healthy';
  }

  /**
   * 格式化文件大小
   * @private
   */
  _formatSize(bytes) {
    if (bytes === 0) return '0 B';
    
    const units = ['B', 'KB', 'MB', 'GB', 'TB'];
    const k = 1024;
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return (bytes / Math.pow(k, i)).toFixed(2) + ' ' + units[i];
  }
}

module.exports = CleanAdvisor;
