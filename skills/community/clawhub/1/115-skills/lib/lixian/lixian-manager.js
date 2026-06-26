/**
 * 115 离线下载管理增强模块
 * 
 * 功能：
 * - 任务列表管理
 * - 进度跟踪
 * - 任务控制（开始/暂停/删除）
 * - 完成清理
 * - 批量操作
 */

const HttpClient = require('../client/http-client');
const ErrorHandler = require('../error/error-handler');

class LixianManager {
  constructor(cookie) {
    this.http = new HttpClient(cookie);
    this.apiBase = 'https://lixian.115.com';
    this.errorHandler = new ErrorHandler();
    this.taskCache = new Map();
  }

  /**
   * 添加磁力链接任务
   * @param {string} magnetUrl - 磁力链接
   * @param {string} targetCid - 目标目录 ID
   * @returns {Object} 任务信息
   */
  async addMagnet(magnetUrl, targetCid = '0') {
    try {
      const response = await this.http.post('/lixian', {
        wa: '1',
        wp: '1',
        ac: 'add_task_url',
        url: magnetUrl,
        path: targetCid
      });

      if (!response.state) {
        const error = this.errorHandler.fromApiResponse(response);
        throw error || new Error(response.error || '添加磁力任务失败');
      }

      const taskInfo = {
        taskId: response.data?.task_id,
        fileName: response.data?.file_name,
        fileSize: response.data?.file_size,
        status: 'pending',
        addedAt: Date.now()
      };

      this.taskCache.set(taskInfo.taskId, taskInfo);

      return {
        success: true,
        ...taskInfo,
        message: '磁力任务添加成功'
      };
    } catch (error) {
      if (error.type) throw error;
      throw this.errorHandler.fromHttpError(error);
    }
  }

  /**
   * 添加 HTTP/HTTPS 下载任务
   * @param {string} url - 下载链接
   * @param {string} targetCid - 目标目录 ID
   * @returns {Object} 任务信息
   */
  async addHttp(url, targetCid = '0') {
    try {
      const response = await this.http.post('/lixian', {
        wa: '1',
        wp: '1',
        ac: 'add_task_url',
        url: url,
        path: targetCid
      });

      if (!response.state) {
        const error = this.errorHandler.fromApiResponse(response);
        throw error || new Error(response.error || '添加 HTTP 任务失败');
      }

      const taskInfo = {
        taskId: response.data?.task_id,
        fileName: response.data?.file_name,
        fileSize: response.data?.file_size,
        status: 'pending',
        addedAt: Date.now()
      };

      this.taskCache.set(taskInfo.taskId, taskInfo);

      return {
        success: true,
        ...taskInfo,
        message: 'HTTP 任务添加成功'
      };
    } catch (error) {
      if (error.type) throw error;
      throw this.errorHandler.fromHttpError(error);
    }
  }

  /**
   * 获取任务列表
   * @param {Object} options - 选项
   * @returns {Object} 任务列表
   */
  async getTaskList(options = {}) {
    try {
      const params = {
        wp: '1',
        ac: 'get_task_list',
        page: options.page || '1',
        limit: options.limit || '20'
      };

      const response = await this.http.post('/lixian', params);

      if (!response.state) {
        const error = this.errorHandler.fromApiResponse(response);
        throw error || new Error(response.error || '获取任务列表失败');
      }

      const tasks = response.data?.tasks || response.data || [];
      
      return {
        success: true,
        tasks,
        count: tasks.length,
        total: response.data?.total || tasks.length,
        page: parseInt(options.page || '1'),
        hasMore: tasks.length === parseInt(options.limit || '20')
      };
    } catch (error) {
      if (error.type) throw error;
      throw this.errorHandler.fromHttpError(error);
    }
  }

  /**
   * 获取任务详情
   * @param {string} taskId - 任务 ID
   * @returns {Object} 任务详情
   */
  async getTaskInfo(taskId) {
    try {
      const listResult = await this.getTaskList({ limit: '100' });
      const task = listResult.tasks.find(t => t.task_id === taskId || t.id === taskId);

      if (!task) {
        throw this.errorHandler.createError('NOT_FOUND', '任务不存在', {
          context: { taskId }
        });
      }

      return {
        success: true,
        task,
        progress: this._parseProgress(task)
      };
    } catch (error) {
      if (error.type) throw error;
      throw this.errorHandler.fromHttpError(error);
    }
  }

  /**
   * 暂停任务
   * @param {string} taskId - 任务 ID
   * @returns {Object} 操作结果
   */
  async pauseTask(taskId) {
    try {
      const response = await this.http.post('/lixian', {
        wp: '1',
        ac: 'stop_task',
        task_id: taskId
      });

      if (!response.state) {
        const error = this.errorHandler.fromApiResponse(response);
        throw error || new Error(response.error || '暂停任务失败');
      }

      return {
        success: true,
        taskId,
        message: '任务已暂停'
      };
    } catch (error) {
      if (error.type) throw error;
      throw this.errorHandler.fromHttpError(error);
    }
  }

  /**
   * 开始/继续任务
   * @param {string} taskId - 任务 ID
   * @returns {Object} 操作结果
   */
  async startTask(taskId) {
    try {
      const response = await this.http.post('/lixian', {
        wp: '1',
        ac: 'start_task',
        task_id: taskId
      });

      if (!response.state) {
        const error = this.errorHandler.fromApiResponse(response);
        throw error || new Error(response.error || '开始任务失败');
      }

      return {
        success: true,
        taskId,
        message: '任务已开始'
      };
    } catch (error) {
      if (error.type) throw error;
      throw this.errorHandler.fromHttpError(error);
    }
  }

  /**
   * 删除任务
   * @param {string} taskId - 任务 ID
   * @returns {Object} 操作结果
   */
  async deleteTask(taskId) {
    try {
      const response = await this.http.post('/lixian', {
        wp: '1',
        ac: 'del_task',
        task_id: taskId
      });

      if (!response.state) {
        const error = this.errorHandler.fromApiResponse(response);
        throw error || new Error(response.error || '删除任务失败');
      }

      this.taskCache.delete(taskId);

      return {
        success: true,
        taskId,
        message: '任务已删除'
      };
    } catch (error) {
      if (error.type) throw error;
      throw this.errorHandler.fromHttpError(error);
    }
  }

  /**
   * 批量删除任务
   * @param {Array} taskIds - 任务 ID 数组
   * @returns {Object} 操作结果
   */
  async batchDeleteTasks(taskIds) {
    const progress = {
      total: taskIds.length,
      success: 0,
      failed: 0,
      errors: []
    };

    for (const taskId of taskIds) {
      try {
        await this.deleteTask(taskId);
        progress.success++;
      } catch (error) {
        progress.failed++;
        progress.errors.push({
          taskId,
          error: error.message
        });
      }
    }

    return {
      success: progress.success > 0,
      progress,
      message: `成功删除 ${progress.success}/${progress.total} 个任务`
    };
  }

  /**
   * 删除已完成任务
   * @returns {Object} 操作结果
   */
  async clearCompleted() {
    try {
      const listResult = await this.getTaskList({ limit: '100' });
      const completedTasks = listResult.tasks.filter(t => {
        const status = t.status || t.state || '';
        return status === '2' || status === 'completed' || status === 'finished';
      });

      if (completedTasks.length === 0) {
        return {
          success: true,
          count: 0,
          message: '没有已完成的任务'
        };
      }

      const taskIds = completedTasks.map(t => t.task_id || t.id);
      const deleteResult = await this.batchDeleteTasks(taskIds);

      return {
        success: true,
        count: deleteResult.progress.success,
        message: `已清理 ${deleteResult.progress.success} 个已完成任务`
      };
    } catch (error) {
      if (error.type) throw error;
      throw this.errorHandler.fromHttpError(error);
    }
  }

  /**
   * 获取任务统计
   * @returns {Object} 统计信息
   */
  async getStats() {
    try {
      const listResult = await this.getTaskList({ limit: '100' });
      const tasks = listResult.tasks;

      const stats = {
        total: tasks.length,
        downloading: 0,
        pending: 0,
        completed: 0,
        failed: 0,
        paused: 0,
        totalSize: 0,
        completedSize: 0
      };

      tasks.forEach(task => {
        const status = task.status || task.state || '';
        const size = parseInt(task.file_size || task.size || '0');

        stats.totalSize += size;

        switch (status) {
          case '0':
          case 'pending':
            stats.pending++;
            break;
          case '1':
          case 'downloading':
            stats.downloading++;
            stats.completedSize += parseInt(task.percent || '0') * size / 100;
            break;
          case '2':
          case 'completed':
          case 'finished':
            stats.completed++;
            stats.completedSize += size;
            break;
          case '3':
          case 'failed':
            stats.failed++;
            break;
          case '4':
          case 'paused':
            stats.paused++;
            break;
        }
      });

      return {
        success: true,
        stats,
        message: `共 ${stats.total} 个任务，${stats.downloading} 个下载中，${stats.completed} 个已完成`
      };
    } catch (error) {
      if (error.type) throw error;
      throw this.errorHandler.fromHttpError(error);
    }
  }

  /**
   * 格式化任务列表
   * @param {Array} tasks - 任务列表
   * @returns {string} 格式化文本
   */
  formatTaskList(tasks) {
    if (!tasks || tasks.length === 0) {
      return '暂无离线下载任务';
    }

    let output = `📥 离线下载任务 (${tasks.length}个)\n`;
    output += `━━━━━━━━━━━━━━━━━━━━\n`;

    tasks.forEach((task, index) => {
      const status = this._formatStatus(task.status || task.state);
      const size = this._formatSize(parseInt(task.file_size || task.size || '0'));
      const name = task.file_name || task.name || '未知文件';
      const progress = task.percent || '0';

      output += `${index + 1}. ${name}\n`;
      output += `   状态：${status} | 进度：${progress}% | 大小：${size}\n`;
      
      if (task.task_id || task.id) {
        output += `   ID：${task.task_id || task.id}\n`;
      }
      output += `\n`;
    });

    return output;
  }

  /**
   * 格式化任务详情
   * @param {Object} task - 任务对象
   * @returns {string}
   */
  formatTaskInfo(task) {
    if (!task) {
      return '任务信息不可用';
    }

    let output = `📥 任务详情\n`;
    output += `━━━━━━━━━━━━━━━━━━━━\n`;
    output += `📝 名称：${task.file_name || task.name || '未知'}\n`;
    output += `🔗 ID：${task.task_id || task.id}\n`;
    output += `📊 状态：${this._formatStatus(task.status || task.state)}\n`;
    output += `📈 进度：${task.percent || '0'}%\n`;
    output += `💾 大小：${this._formatSize(parseInt(task.file_size || task.size || '0'))}\n`;
    
    if (task.speed) {
      output += `⚡ 速度：${task.speed}/s\n`;
    }
    
    if (task.peers !== undefined) {
      output += `👥  peers：${task.peers}\n`;
    }

    return output;
  }

  /**
   * 格式化统计信息
   * @param {Object} stats - 统计对象
   * @returns {string}
   */
  formatStats(stats) {
    let output = `📊 离线下载统计\n`;
    output += `━━━━━━━━━━━━━━━━━━━━\n`;
    output += `📋 总任务：${stats.total} 个\n`;
    output += `⬇️ 下载中：${stats.downloading} 个\n`;
    output += `⏳ 等待中：${stats.pending} 个\n`;
    output += `✅ 已完成：${stats.completed} 个\n`;
    output += `❌ 失败：${stats.failed} 个\n`;
    output += `⏸️ 已暂停：${stats.paused} 个\n`;
    output += `💾 总大小：${this._formatSize(stats.totalSize)}\n`;
    output += `📥 已完成：${this._formatSize(stats.completedSize)}\n`;

    return output;
  }

  /**
   * 解析进度信息
   * @private
   */
  _parseProgress(task) {
    const percent = parseFloat(task.percent || '0');
    const size = parseInt(task.file_size || task.size || '0');
    const downloaded = Math.round(size * percent / 100);

    return {
      percent,
      total: size,
      downloaded,
      remaining: size - downloaded
    };
  }

  /**
   * 格式化状态
   * @private
   */
  _formatStatus(status) {
    const statusMap = {
      '0': '⏳ 等待中',
      '1': '⬇️ 下载中',
      '2': '✅ 已完成',
      '3': '❌ 失败',
      '4': '⏸️ 已暂停',
      'pending': '⏳ 等待中',
      'downloading': '⬇️ 下载中',
      'completed': '✅ 已完成',
      'failed': '❌ 失败',
      'paused': '⏸️ 已暂停'
    };
    return statusMap[status] || `未知 (${status})`;
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

module.exports = LixianManager;
