/**
 * CodeBuddy Coding Skill
 * 主入口文件
 */

const CodeBuddyCLIWrapper = require('./cli-wrapper');
const ProgressMonitor = require('./progress-monitor');

class CodeBuddyCodingSkill {
  constructor(options = {}) {
    this.cli = new CodeBuddyCLIWrapper(options);
    this.monitor = new ProgressMonitor(options);
    this.debug = options.debug || false;
    this.currentTask = null;
    this.executionLogs = [];
  }

  /**
   * 执行编程任务
   */
  async execute(options) {
    const task = typeof options === 'string' ? { task: options } : options;
    const taskId = this._generateTaskId();
    
    // 记录日志
    this._log('TASK_START', { taskId, task: task.task || task });

    // 开始监控
    this.monitor.startMonitoring(taskId);
    this.currentTask = taskId;

    // 订阅进度事件
    const progressCallback = (progress) => {
      this._log('PROGRESS_UPDATE', progress);
      if (task.onProgress) {
        task.onProgress(progress);
      }
    };
    this.monitor.on('progress', progressCallback);

    try {
      // 检查 CLI 是否可用
      const available = await this.cli.checkAvailable();
      if (!available.available) {
        throw {
          type: 'CLI_NOT_FOUND',
          message: 'CodeBuddy CLI not found. Please install it first.',
          version: null
        };
      }

      if (this.debug) {
        console.log('[CodeBuddy Skill] CLI version:', available.version);
      }

      // 执行任务
      const result = await this.cli.execute(task, {
        outputFormat: task.outputFormat || 'json',
        permissionMode: task.permissionMode || 'bypassPermissions',
        timeout: task.timeout,
        workspace: task.workspace,
        cwd: task.cwd,
        onProgress: (progress) => {
          this.monitor.updateProgress(progress);
        }
      });

      // 完成监控
      const finalProgress = this.monitor.completeMonitoring(result);
      this._log('TASK_COMPLETE', { taskId, result, progress: finalProgress });

      return {
        status: result.status,
        filesModified: result.filesModified,
        toolCalls: result.toolCalls,
        reasoning: result.reasoning,
        duration: result.duration,
        progress: finalProgress
      };

    } catch (error) {
      // 失败监控
      const finalProgress = this.monitor.failMonitoring(error);
      this._log('TASK_FAILED', { taskId, error, progress: finalProgress });

      throw {
        type: error.type || 'EXECUTION_ERROR',
        message: error.message || error,
        progress: finalProgress
      };
    } finally {
      // 清理
      this.monitor.removeListener('progress', progressCallback);
      this.currentTask = null;
    }
  }

  /**
   * 订阅进度事件
   */
  onProgress(callback) {
    this.monitor.onProgress(callback);
    return this;
  }

  /**
   * 订阅完成事件
   */
  onComplete(callback) {
    this.monitor.onComplete(callback);
    return this;
  }

  /**
   * 订阅失败事件
   */
  onFailed(callback) {
    this.monitor.onFailed(callback);
    return this;
  }

  /**
   * 获取当前任务状态
   */
  getStatus() {
    return this.monitor.getTaskStatus();
  }

  /**
   * 获取当前进度
   */
  getCurrentProgress() {
    return this.monitor.getCurrentProgress();
  }

  /**
   * 设置调试模式
   */
  setDebugMode(enabled) {
    this.debug = enabled;
    this.cli.debug = enabled;
  }

  /**
   * 获取执行日志
   */
  getExecutionLogs() {
    return this.executionLogs;
  }

  /**
   * 生成任务 ID
   */
  _generateTaskId() {
    return `task_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  /**
   * 记录日志
   */
  _log(event, data) {
    const logEntry = {
      time: new Date().toISOString(),
      event: event,
      data: data
    };
    this.executionLogs.push(logEntry);

    if (this.debug) {
      console.log(`[CodeBuddy Skill] ${event}:`, data);
    }
  }

  /**
   * 格式化进度报告
   */
  formatProgressReport(progress) {
    return this.monitor.formatProgressReport(progress);
  }

  /**
   * 重置 Skill 状态
   */
  reset() {
    this.monitor.reset();
    this.currentTask = null;
    this.executionLogs = [];
  }
}

// 导出单例和类
const skill = new CodeBuddyCodingSkill();

module.exports = skill;
module.exports.CodeBuddyCodingSkill = CodeBuddyCodingSkill;
module.exports.default = skill;
