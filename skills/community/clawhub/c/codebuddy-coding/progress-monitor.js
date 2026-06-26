/**
 * Progress Monitor
 * 监控 CodeBuddy CLI 的执行进度并报告
 */

const EventEmitter = require('events');

class ProgressMonitor extends EventEmitter {
  constructor(options = {}) {
    super();
    this.pollInterval = options.pollInterval || 30000; // 30秒
    this.lastProgress = null;
    this.startTime = null;
    this.taskId = null;
    this.status = 'idle';
  }

  /**
   * 开始监控任务
   */
  startMonitoring(taskId) {
    this.taskId = taskId;
    this.startTime = Date.now();
    this.status = 'running';
    this.lastProgress = {
      percentage: 0,
      currentTask: '启动中',
      elapsedTime: 0,
      filesModified: [],
      toolCalls: 0
    };

    this.emit('start', {
      taskId: this.taskId,
      startTime: new Date(this.startTime)
    });
  }

  /**
   * 更新进度
   */
  updateProgress(progressData) {
    this.lastProgress = {
      ...this.lastProgress,
      ...progressData,
      elapsedTime: (Date.now() - this.startTime) / 1000
    };

    this.emit('progress', this.lastProgress);
  }

  /**
   * 完成监控
   */
  completeMonitoring(result) {
    this.status = 'completed';
    const finalProgress = {
      ...this.lastProgress,
      percentage: 100,
      elapsedTime: (Date.now() - this.startTime) / 1000,
      status: result.status,
      filesModified: result.filesModified,
      toolCalls: result.toolCalls?.length || 0
    };

    this.emit('complete', {
      taskId: this.taskId,
      result: result,
      progress: finalProgress
    });

    return finalProgress;
  }

  /**
   * 失败监控
   */
  failMonitoring(error) {
    this.status = 'failed';
    const finalProgress = {
      ...this.lastProgress,
      elapsedTime: (Date.now() - this.startTime) / 1000,
      error: error.message || error
    };

    this.emit('failed', {
      taskId: this.taskId,
      error: error,
      progress: finalProgress
    });

    return finalProgress;
  }

  /**
   * 获取当前进度
   */
  getCurrentProgress() {
    if (!this.startTime) {
      return null;
    }

    return {
      ...this.lastProgress,
      elapsedTime: (Date.now() - this.startTime) / 1000,
      status: this.status
    };
  }

  /**
   * 获取任务状态
   */
  getTaskStatus() {
    return {
      taskId: this.taskId,
      status: this.status,
      startTime: this.startTime ? new Date(this.startTime) : null,
      progress: this.getCurrentProgress()
    };
  }

  /**
   * 重置监控器
   */
  reset() {
    this.taskId = null;
    this.startTime = null;
    this.status = 'idle';
    this.lastProgress = null;
  }

  /**
   * 订阅进度事件（便捷方法）
   */
  onProgress(callback) {
    this.on('progress', callback);
    return this;
  }

  /**
   * 订阅完成事件（便捷方法）
   */
  onComplete(callback) {
    this.on('complete', callback);
    return this;
  }

  /**
   * 订阅失败事件（便捷方法）
   */
  onFailed(callback) {
    this.on('failed', callback);
    return this;
  }

  /**
   * 格式化进度报告
   */
  formatProgressReport(progress) {
    const elapsed = Math.floor(progress.elapsedTime || 0);
    const percentage = Math.floor(progress.percentage || 0);

    let report = `📊 任务进度报告\n`;
    report += `━━━━━━━━━━━━━━━━━━\n`;
    report += `状态: ${this._getStatusEmoji(this.status)} ${this.status}\n`;
    report += `进度: ${percentage}%\n`;
    report += `当前任务: ${progress.currentTask || '处理中'}\n`;
    report += `已用时间: ${this._formatDuration(elapsed)}\n`;
    
    if (progress.filesModified && progress.filesModified.length > 0) {
      report += `已修改文件: ${progress.filesModified.length} 个\n`;
    }
    
    if (progress.toolCalls !== undefined) {
      report += `已执行操作: ${progress.toolCalls} 次\n`;
    }

    return report;
  }

  /**
   * 获取状态 Emoji
   */
  _getStatusEmoji(status) {
    const emojis = {
      'idle': '💤',
      'running': '⏳',
      'completed': '✅',
      'failed': '❌'
    };
    return emojis[status] || '❓';
  }

  /**
   * 格式化持续时间
   */
  _formatDuration(seconds) {
    if (seconds < 60) {
      return `${seconds}秒`;
    } else if (seconds < 3600) {
      const minutes = Math.floor(seconds / 60);
      const secs = Math.floor(seconds % 60);
      return `${minutes}分${secs}秒`;
    } else {
      const hours = Math.floor(seconds / 3600);
      const minutes = Math.floor((seconds % 3600) / 60);
      return `${hours}小时${minutes}分`;
    }
  }
}

module.exports = ProgressMonitor;
