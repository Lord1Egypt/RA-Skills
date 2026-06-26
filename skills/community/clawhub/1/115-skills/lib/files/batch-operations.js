/**
 * 115 批量操作增强模块
 * 
 * 功能：
 * - 批量选择管理
 * - 批量操作（移动/复制/删除/下载）
 * - 进度跟踪
 * - 错误恢复
 * - 操作历史
 */

const HttpClient = require('../client/http-client');
const ErrorHandler = require('../error/error-handler');

class BatchOperations {
  constructor(cookie) {
    this.http = new HttpClient(cookie);
    this.errorHandler = new ErrorHandler();
    this.selectedFiles = new Map(); // fuuid -> fileInfo
    this.operationHistory = [];
    this.maxHistory = 50;
  }

  /**
   * 选择文件
   * @param {string} fuuid - 文件 ID
   * @param {Object} fileInfo - 文件信息
   */
  selectFile(fuuid, fileInfo = {}) {
    this.selectedFiles.set(fuuid, {
      fuuid,
      isFolder: fileInfo.is_folder || fileInfo.isFolder || false,
      name: fileInfo.file_name || fileInfo.name || '未知文件',
      size: fileInfo.file_size || fileInfo.size || 0,
      selectedAt: Date.now()
    });
    return this.getSelectedCount();
  }

  /**
   * 取消选择文件
   * @param {string} fuuid - 文件 ID
   */
  deselectFile(fuuid) {
    this.selectedFiles.delete(fuuid);
    return this.getSelectedCount();
  }

  /**
   * 清空选择
   */
  clearSelection() {
    this.selectedFiles.clear();
    return 0;
  }

  /**
   * 获取选中的文件
   * @returns {Array} 选中的文件列表
   */
  getSelectedFiles() {
    return Array.from(this.selectedFiles.values());
  }

  /**
   * 获取选中数量
   * @returns {number}
   */
  getSelectedCount() {
    return this.selectedFiles.size;
  }

  /**
   * 批量移动文件
   * @param {Array} fileIds - 文件 ID 数组
   * @param {string} targetCid - 目标目录 ID
   * @param {Object} options - 选项
   * @returns {Object} 操作结果
   */
  async batchMove(fileIds, targetCid) {
    const progress = {
      total: fileIds.length,
      success: 0,
      failed: 0,
      current: 0,
      errors: []
    };

    try {
      const ids = fileIds.map(id => String(id));
      
      const response = await this.http.post('/files/move', {
        fid: ids.join(','),
        pid: targetCid
      });

      progress.current = fileIds.length;
      
      if (!response.state) {
        const error = this.errorHandler.fromApiResponse(response);
        if (error) {
          progress.errors.push({ error: error.message, count: fileIds.length });
        } else {
          progress.errors.push({ error: response.error || '移动失败', count: fileIds.length });
        }
        progress.failed = fileIds.length;
      } else {
        progress.success = fileIds.length;
      }

      this._recordOperation('move', fileIds, targetCid, progress);
      
      return {
        success: progress.success > 0,
        progress,
        message: `成功移动 ${progress.success}/${progress.total} 个文件`
      };
    } catch (error) {
      progress.errors.push({ error: error.message, count: fileIds.length });
      progress.failed = fileIds.length;
      
      const handlerError = this.errorHandler.fromHttpError(error);
      throw handlerError || error;
    }
  }

  /**
   * 批量复制文件
   * @param {Array} fileIds - 文件 ID 数组
   * @param {string} targetCid - 目标目录 ID
   * @returns {Object} 操作结果
   */
  async batchCopy(fileIds, targetCid) {
    const progress = {
      total: fileIds.length,
      success: 0,
      failed: 0,
      current: 0,
      errors: []
    };

    try {
      const ids = fileIds.map(id => String(id));
      
      const response = await this.http.post('/files/copy', {
        fid: ids.join(','),
        pid: targetCid
      });

      progress.current = fileIds.length;
      
      if (!response.state) {
        const error = this.errorHandler.fromApiResponse(response);
        if (error) {
          progress.errors.push({ error: error.message, count: fileIds.length });
        } else {
          progress.errors.push({ error: response.error || '复制失败', count: fileIds.length });
        }
        progress.failed = fileIds.length;
      } else {
        progress.success = fileIds.length;
      }

      this._recordOperation('copy', fileIds, targetCid, progress);
      
      return {
        success: progress.success > 0,
        progress,
        message: `成功复制 ${progress.success}/${progress.total} 个文件`
      };
    } catch (error) {
      progress.errors.push({ error: error.message, count: fileIds.length });
      progress.failed = fileIds.length;
      
      const handlerError = this.errorHandler.fromHttpError(error);
      throw handlerError || error;
    }
  }

  /**
   * 批量删除文件
   * @param {Array} fileIds - 文件 ID 数组
   * @returns {Object} 操作结果
   */
  async batchDelete(fileIds) {
    const progress = {
      total: fileIds.length,
      success: 0,
      failed: 0,
      current: 0,
      errors: []
    };

    try {
      const ids = fileIds.map(id => String(id));
      
      const response = await this.http.post('/rb/delete', {
        fid: ids.join(',')
      }, {
        headers: {
          'Origin': 'https://115.com',
          'X-Requested-With': 'XMLHttpRequest'
        }
      });

      progress.current = fileIds.length;
      
      if (!response.state) {
        const error = this.errorHandler.fromApiResponse(response);
        if (error) {
          progress.errors.push({ error: error.message, count: fileIds.length });
        } else {
          progress.errors.push({ error: response.error || '删除失败', count: fileIds.length });
        }
        progress.failed = fileIds.length;
      } else {
        progress.success = fileIds.length;
      }

      this._recordOperation('delete', fileIds, null, progress);
      
      return {
        success: progress.success > 0,
        progress,
        message: `成功删除 ${progress.success}/${progress.total} 个文件`
      };
    } catch (error) {
      progress.errors.push({ error: error.message, count: fileIds.length });
      progress.failed = fileIds.length;
      
      const handlerError = this.errorHandler.fromHttpError(error);
      throw handlerError || error;
    }
  }

  /**
   * 批量重命名文件
   * @param {Array} operations - 重命名操作数组 [{fuuid, newName}]
   * @returns {Object} 操作结果
   */
  async batchRename(operations) {
    const progress = {
      total: operations.length,
      success: 0,
      failed: 0,
      current: 0,
      errors: []
    };

    for (const op of operations) {
      progress.current++;
      
      try {
        const response = await this.http.post('/files/edit', {
          fid: op.fuuid,
          file_name: op.newName
        });

        if (!response.state) {
          progress.failed++;
          const error = this.errorHandler.fromApiResponse(response);
          progress.errors.push({
            fuuid: op.fuuid,
            error: error?.message || response.error || '重命名失败'
          });
        } else {
          progress.success++;
        }
      } catch (error) {
        progress.failed++;
        progress.errors.push({
          fuuid: op.fuuid,
          error: error.message
        });
      }
    }

    this._recordOperation('rename', operations.map(op => op.fuuid), null, progress);
    
    return {
      success: progress.success > 0,
      progress,
      message: `成功重命名 ${progress.success}/${progress.total} 个文件`
    };
  }

  /**
   * 批量下载文件
   * @param {Array} fileIds - 文件 ID 数组
   * @returns {Object} 操作结果
   */
  async batchDownload(fileIds) {
    const progress = {
      total: fileIds.length,
      success: 0,
      failed: 0,
      current: 0,
      errors: [],
      downloadUrls: []
    };

    for (const fileId of fileIds) {
      progress.current++;
      
      try {
        // 获取下载链接
        const response = await this.http.get('/files/download', {
          fid: fileId
        });

        if (!response.state) {
          progress.failed++;
          const error = this.errorHandler.fromApiResponse(response);
          progress.errors.push({
            fileId,
            error: error?.message || response.error || '获取下载链接失败'
          });
        } else {
          progress.success++;
          if (response.data?.url) {
            progress.downloadUrls.push({
              fileId,
              url: response.data.url
            });
          }
        }
      } catch (error) {
        progress.failed++;
        progress.errors.push({
          fileId,
          error: error.message
        });
      }
    }

    this._recordOperation('download', fileIds, null, progress);
    
    return {
      success: progress.success > 0,
      progress,
      downloadUrls: progress.downloadUrls,
      message: `成功获取 ${progress.success}/${progress.total} 个下载链接`
    };
  }

  /**
   * 全选当前目录文件
   * @param {Array} files - 文件列表
   */
  selectAll(files) {
    files.forEach(file => {
      this.selectFile(file.fuuid || file.file_id, {
        is_folder: file.is_folder || file.isFolder,
        file_name: file.file_name || file.name,
        file_size: file.file_size || file.size
      });
    });
    return this.getSelectedCount();
  }

  /**
   * 反选文件
   * @param {Array} files - 文件列表
   */
  invertSelection(files) {
    const selectedFuuids = new Set(this.getSelectedFiles().map(f => f.fuuid));
    
    files.forEach(file => {
      const fuuid = file.fuuid || file.file_id;
      if (selectedFuuids.has(fuuid)) {
        this.deselectFile(fuuid);
      } else {
        this.selectFile(fuuid, {
          is_folder: file.is_folder || file.isFolder,
          file_name: file.file_name || file.name,
          file_size: file.file_size || file.size
        });
      }
    });
    
    return this.getSelectedCount();
  }

  /**
   * 按条件选择文件
   * @param {Array} files - 文件列表
   * @param {Function} predicate - 选择条件
   */
  selectByCondition(files, predicate) {
    files.forEach(file => {
      if (predicate(file)) {
        this.selectFile(file.fuuid || file.file_id, {
          is_folder: file.is_folder || file.isFolder,
          file_name: file.file_name || file.name,
          file_size: file.file_size || file.size
        });
      }
    });
    return this.getSelectedCount();
  }

  /**
   * 获取操作历史
   * @param {number} limit - 限制数量
   * @returns {Array}
   */
  getHistory(limit = 10) {
    return this.operationHistory.slice(-limit);
  }

  /**
   * 清空操作历史
   */
  clearHistory() {
    this.operationHistory = [];
  }

  /**
   * 格式化进度信息
   * @param {Object} progress - 进度对象
   * @returns {string}
   */
  formatProgress(progress) {
    const percentage = Math.round((progress.success / progress.total) * 100);
    
    let output = `📊 操作进度\n`;
    output += `━━━━━━━━━━━━━━━━━━━━\n`;
    output += `总计：${progress.total} 个文件\n`;
    output += `成功：${progress.success} 个 ✅\n`;
    output += `失败：${progress.failed} 个 ❌\n`;
    output += `进度：${percentage}%\n`;
    
    if (progress.errors && progress.errors.length > 0) {
      output += `\n⚠️ 错误详情：\n`;
      progress.errors.slice(0, 5).forEach((err, i) => {
        output += `   ${i + 1}. ${err.error}\n`;
      });
      if (progress.errors.length > 5) {
        output += `   ... 还有 ${progress.errors.length - 5} 个错误\n`;
      }
    }
    
    return output;
  }

  /**
   * 记录操作
   * @private
   */
  _recordOperation(type, fileIds, target, progress) {
    const record = {
      type,
      fileCount: fileIds.length,
      target,
      progress: { ...progress },
      timestamp: Date.now()
    };
    
    this.operationHistory.push(record);
    
    if (this.operationHistory.length > this.maxHistory) {
      this.operationHistory.shift();
    }
  }
}

module.exports = BatchOperations;
