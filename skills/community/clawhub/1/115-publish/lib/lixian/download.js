const HttpClient = require('../client/http-client');

/**
 * 115 离线下载模块
 * 
 * 功能：
 * - 磁力链接下载
 * - 种子文件下载
 * - HTTP 下载
 * - 任务管理
 */
class LixianDownload {
  constructor(cookie) {
    this.http = new HttpClient(cookie);
    this.apiBase = 'https://lixian.115.com';
  }

  /**
   * 添加磁力链接下载任务
   * @param {string} magnetUrl - 磁力链接
   * @param {string} targetCid - 目标目录 ID
   * @returns {Promise<Object>} 任务信息
   */
  async addMagnet(magnetUrl, targetCid = '0') {
    const response = await this.http.post('/lixian', {
      wa: '1',
      wp: '1',
      ac: 'add_task_url',
      url: magnetUrl,
      path: targetCid
    });

    if (!response.state) {
      throw new Error(response.error || '添加磁力任务失败');
    }

    return {
      success: true,
      taskId: response.data?.task_id,
      fileName: response.data?.file_name,
      fileSize: response.data?.file_size,
      status: 'pending'
    };
  }

  /**
   * 添加 HTTP/HTTPS 下载任务
   * @param {string} url - 下载链接
   * @param {string} targetCid - 目标目录 ID
   * @returns {Promise<Object>} 任务信息
   */
  async addHttp(url, targetCid = '0') {
    const response = await this.http.post('/lixian', {
      wa: '1',
      wp: '1',
      ac: 'add_task_url',
      url: url,
      path: targetCid
    });

    if (!response.state) {
      throw new Error(response.error || '添加 HTTP 任务失败');
    }

    return {
      success: true,
      taskId: response.data?.task_id
    };
  }

  /**
   * 获取任务列表
   * @param {Object} options - 选项
   * @returns {Promise<Object>} 任务列表
   */
  async getTaskList(options = {}) {
    const { page = 1, size = 20 } = options;

    const response = await this.http.get('/lixian/tasks', {
      page,
      size,
      ac: 'task_list',
      _: Date.now()
    });

    if (!response.state) {
      return { success: false, message: response.error || '获取任务列表失败', tasks: [] };
    }

    return {
      success: true,
      tasks: response.data?.tasks || [],
      totalCount: response.data?.count || 0,
      hasMore: response.data?.has_more || false
    };
  }

  /**
   * 获取任务详情
   * @param {string} taskId - 任务 ID
   * @returns {Promise<Object>} 任务详情
   */
  async getTaskDetail(taskId) {
    const response = await this.http.get('/lixian/task', {
      task_id: taskId,
      ac: 'task_info',
      _: Date.now()
    });

    if (!response.state) {
      throw new Error(response.error || '获取任务详情失败');
    }

    return {
      success: true,
      task: response.data || {}
    };
  }

  /**
   * 删除任务
   * @param {string|array} taskIds - 任务 ID 或 ID 数组
   * @returns {Promise<Object>} 删除结果
   */
  async deleteTask(taskIds) {
    const ids = Array.isArray(taskIds) ? taskIds : [taskIds];

    const response = await this.http.post('/lixian', {
      wa: '1',
      wp: '1',
      ac: 'del_task',
      hash: ids.join(',')
    });

    if (!response.state) {
      throw new Error(response.error || '删除任务失败');
    }

    return {
      success: true,
      deletedCount: ids.length,
      taskIds: ids
    };
  }

  /**
   * 清空已完成任务
   * @returns {Promise<Object>} 清空结果
   */
  async clearCompleted() {
    const taskList = await this.getTaskList({ size: 1000 });
    const completedTasks = taskList.tasks
      .filter(t => t.status === 2 || t.status === 'completed')
      .map(t => t.task_id);

    if (completedTasks.length > 0) {
      return this.deleteTask(completedTasks);
    }

    return { success: true, deletedCount: 0 };
  }

  /**
   * 获取任务统计
   * @returns {Promise<Object>} 统计信息
   */
  async getTaskStats() {
    const taskList = await this.getTaskList({ size: 1000 });
    
    const stats = {
      total: taskList.totalCount,
      pending: 0,
      downloading: 0,
      completed: 0,
      failed: 0
    };

    for (const task of taskList.tasks) {
      if (task.status === 0 || task.status === 'pending') stats.pending++;
      else if (task.status === 1 || task.status === 'downloading') stats.downloading++;
      else if (task.status === 2 || task.status === 'completed') stats.completed++;
      else if (task.status === -1 || task.status === 'failed') stats.failed++;
    }

    return stats;
  }

  /**
   * 等待任务完成
   * @param {string} taskId - 任务 ID
   * @param {Object} options - 选项
   * @returns {Promise<Object>} 任务结果
   */
  async waitForCompletion(taskId, options = {}) {
    const { timeout = 3600000, interval = 5000, onProgress = null } = options;
    const startTime = Date.now();

    while (Date.now() - startTime < timeout) {
      const detail = await this.getTaskDetail(taskId);
      const task = detail.task;

      onProgress?.(task);

      if (task.status === 2 || task.status === 'completed') {
        return {
          success: true,
          status: 'completed',
          task
        };
      }

      if (task.status === -1 || task.status === 'failed') {
        return {
          success: false,
          status: 'failed',
          task,
          error: task.error_msg || '下载失败'
        };
      }

      await this.http.sleep(interval);
    }

    return {
      success: false,
      status: 'timeout',
      error: '等待超时'
    };
  }

  /**
   * 批量添加磁力任务
   * @param {Array<string>} magnetUrls - 磁力链接数组
   * @param {string} targetCid - 目标目录 ID
   * @param {Object} options - 选项
   * @returns {Promise<Object>} 添加结果
   */
  async batchAddMagnet(magnetUrls, targetCid = '0', options = {}) {
    const { onProgress = null } = options;
    const results = {
      total: magnetUrls.length,
      success: 0,
      failed: 0,
      details: []
    };

    for (let i = 0; i < magnetUrls.length; i++) {
      try {
        const result = await this.addMagnet(magnetUrls[i], targetCid);
        results.success++;
        results.details.push({ success: true, url: magnetUrls[i], ...result });
      } catch (error) {
        results.failed++;
        results.details.push({ success: false, url: magnetUrls[i], error: error.message });
      }

      onProgress?.({
        processed: i + 1,
        total: magnetUrls.length,
        success: results.success,
        failed: results.failed
      });

      // 避免速率限制
      if (i < magnetUrls.length - 1) {
        await this.http.sleep(1000);
      }
    }

    return results;
  }
}

module.exports = LixianDownload;
