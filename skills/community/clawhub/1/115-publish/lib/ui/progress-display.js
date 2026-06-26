/**
 * 进度显示组件
 * 
 * 功能：
 * - 实时进度条
 * - 速度显示
 * - 剩余时间估算
 * - 多任务进度
 */

class ProgressDisplay {
  constructor() {
    this.defaultWidth = 30;
  }

  /**
   * 创建进度条
   * @param {Object} options - 选项
   * @returns {string}
   */
  create(options) {
    const {
      current = 0,
      total = 100,
      width = this.defaultWidth,
      showPercent = true,
      showCount = true,
      filledChar = '█',
      emptyChar = '░'
    } = options;

    const percent = total > 0 ? (current / total) * 100 : 0;
    const filledWidth = Math.round((percent / 100) * width);
    const emptyWidth = width - filledWidth;

    // 进度条
    const bar = filledChar.repeat(filledWidth) + emptyChar.repeat(emptyWidth);
    
    let output = `[${bar}]`;
    
    if (showPercent) {
      output += ` ${percent.toFixed(1)}%`;
    }
    
    if (showCount) {
      output += ` (${this._formatNumber(current)}/${this._formatNumber(total)})`;
    }

    return output;
  }

  /**
   * 创建带动画效果的进度条
   * @param {Object} options - 选项
   * @returns {string}
   */
  createAnimated(options) {
    const {
      current = 0,
      total = 100,
      width = this.defaultWidth,
      spinner = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    } = options;

    const frame = spinner[Math.floor(Date.now() / 100) % spinner.length];
    const percent = total > 0 ? (current / total) * 100 : 0;
    const filledWidth = Math.round((percent / 100) * width);
    const emptyWidth = width - filledWidth;

    const bar = '█'.repeat(filledWidth) + '░'.repeat(emptyWidth);
    
    return `${frame} [${bar}] ${percent.toFixed(1)}%`;
  }

  /**
   * 创建下载进度
   * @param {Object} options - 选项
   * @returns {string}
   */
  createDownload(options) {
    const {
      downloaded = 0,
      total = 0,
      speed = 0
    } = options;

    const percent = total > 0 ? (downloaded / total) * 100 : 0;
    const filledWidth = Math.round((percent / 100) * this.defaultWidth);
    const emptyWidth = this.defaultWidth - filledWidth;

    const bar = '🟦'.repeat(filledWidth) + '⬜'.repeat(emptyWidth);
    
    let output = `[${bar}] ${percent.toFixed(1)}%\n`;
    output += `${this._formatSize(downloaded)} / ${this._formatSize(total)}`;
    
    if (speed > 0) {
      output += ` | ⚡ ${this._formatSize(speed)}/s`;
    }

    // 估算剩余时间
    if (speed > 0 && downloaded > 0) {
      const remaining = total - downloaded;
      const eta = Math.round(remaining / speed);
      output += ` | ⏱️ ${this._formatTime(eta)}`;
    }

    return output;
  }

  /**
   * 创建上传进度
   * @param {Object} options - 选项
   * @returns {string}
   */
  createUpload(options) {
    const {
      uploaded = 0,
      total = 0,
      speed = 0
    } = options;

    const percent = total > 0 ? (uploaded / total) * 100 : 0;
    const filledWidth = Math.round((percent / 100) * this.defaultWidth);
    const emptyWidth = this.defaultWidth - filledWidth;

    const bar = '🟩'.repeat(filledWidth) + '⬜'.repeat(emptyWidth);
    
    let output = `[${bar}] ${percent.toFixed(1)}%\n`;
    output += `${this._formatSize(uploaded)} / ${this._formatSize(total)}`;
    
    if (speed > 0) {
      output += ` | ⚡ ${this._formatSize(speed)}/s`;
    }

    return output;
  }

  /**
   * 创建批量操作进度
   * @param {Object} options - 选项
   * @returns {string}
   */
  createBatch(options) {
    const {
      current = 0,
      total = 0,
      success = 0,
      failed = 0,
      operation = '操作'
    } = options;

    const percent = total > 0 ? (current / total) * 100 : 0;
    const filledWidth = Math.round((percent / 100) * this.defaultWidth);
    const emptyWidth = this.defaultWidth - filledWidth;

    const bar = '█'.repeat(filledWidth) + '░'.repeat(emptyWidth);
    
    let output = `📊 ${operation}进度\n`;
    output += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`;
    output += `[${bar}] ${percent.toFixed(1)}%\n\n`;
    output += `当前：${current}/${total}\n`;
    output += `成功：${success} ✅\n`;
    output += `失败：${failed} ❌\n`;

    return output;
  }

  /**
   * 创建多任务进度
   * @param {Array} tasks - 任务列表
   * @returns {string}
   */
  createMultiTask(tasks) {
    if (!tasks || tasks.length === 0) {
      return '暂无任务';
    }

    let output = `📋 多任务进度 (${tasks.length} 个)\n`;
    output += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n`;

    tasks.forEach((task, index) => {
      const name = task.name || `任务 ${index + 1}`;
      const current = task.current || 0;
      const total = task.total || 100;
      const status = task.status || 'pending';
      
      const percent = total > 0 ? (current / total) * 100 : 0;
      const filledWidth = Math.round((percent / 100) * 20);
      const emptyWidth = 20 - filledWidth;

      const statusIcon = this._getStatusIcon(status);
      const bar = '█'.repeat(filledWidth) + '░'.repeat(emptyWidth);

      output += `${index + 1}. ${statusIcon} ${name}\n`;
      output += `   [${bar}] ${percent.toFixed(0)}%\n`;
      
      if (task.speed) {
        output += `   ⚡ ${this._formatSize(task.speed)}/s`;
      }
      if (task.eta) {
        output += ` | ⏱️ ${this._formatTime(task.eta)}`;
      }
      output += `\n\n`;
    });

    // 总体进度
    const totalCurrent = tasks.reduce((sum, t) => sum + (t.current || 0), 0);
    const totalAll = tasks.reduce((sum, t) => sum + (t.total || 0), 0);
    const overallPercent = totalAll > 0 ? (totalCurrent / totalAll * 100) : 0;

    output += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`;
    output += `总进度：${overallPercent.toFixed(1)}%\n`;

    return output;
  }

  /**
   * 创建步骤进度
   * @param {Object} options - 选项
   * @returns {string}
   */
  createSteps(options) {
    const {
      current = 0,
      total = 0,
      steps = []
    } = options;

    let output = `📍 进度 (${current}/${total})\n`;
    output += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n`;

    steps.forEach((step, index) => {
      const num = index + 1;
      const isCompleted = num <= current;
      const isCurrent = num === current;
      // const isPending = num > current;

      const icon = isCompleted ? '✅' : isCurrent ? '🔵' : '⚪';
      const status = isCompleted ? '已完成' : isCurrent ? '进行中' : '待处理';

      output += `${icon} 步骤 ${num}: ${step.name || `步骤 ${num}`}\n`;
      output += `   ${status}`;
      
      if (step.description) {
        output += ` - ${step.description}`;
      }
      output += `\n\n`;
    });

    return output;
  }

  /**
   * 创建环形进度（文本模拟）
   * @param {Object} options - 选项
   * @returns {string}
   */
  createCircular(options) {
    const {
      percent = 0
    } = options;

    const normalizedPercent = Math.min(100, Math.max(0, percent));
    
    // 简化的文本环形进度
    const segments = 8;
    const filledSegments = Math.round((normalizedPercent / 100) * segments);
    
    const circle = '◐◓◑◒'.charAt(filledSegments % 4);
    
    return `${circle} ${normalizedPercent.toFixed(1)}%`;
  }

  /**
   * 创建迷你进度条
   * @param {Object} options - 选项
   * @returns {string}
   */
  createMini(options) {
    const {
      current = 0,
      total = 100,
      width = 10
    } = options;

    const percent = total > 0 ? (current / total) * 100 : 0;
    const filledWidth = Math.round((percent / 100) * width);
    const emptyWidth = width - filledWidth;

    const bar = '█'.repeat(filledWidth) + '░'.repeat(emptyWidth);
    
    return `[${bar}]`;
  }

  /**
   * 格式化文件大小
   * @private
   */
  _formatSize(bytes) {
    if (!bytes || bytes === 0) return '0 B';
    
    const units = ['B', 'KB', 'MB', 'GB', 'TB'];
    const k = 1024;
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return (bytes / Math.pow(k, i)).toFixed(2) + ' ' + units[i];
  }

  /**
   * 格式化时间
   * @private
   */
  _formatTime(seconds) {
    if (seconds < 60) {
      return `${seconds} 秒`;
    }
    if (seconds < 3600) {
      const mins = Math.floor(seconds / 60);
      const secs = seconds % 60;
      return `${mins} 分 ${secs} 秒`;
    }
    const hours = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    return `${hours} 小时 ${mins} 分`;
  }

  /**
   * 格式化数字
   * @private
   */
  _formatNumber(num) {
    if (num >= 1000000) {
      return (num / 1000000).toFixed(1) + 'M';
    }
    if (num >= 1000) {
      return (num / 1000).toFixed(1) + 'K';
    }
    return String(num);
  }

  /**
   * 获取状态图标
   * @private
   */
  _getStatusIcon(status) {
    const icons = {
      'pending': '⏳',
      'running': '⬇️',
      'completed': '✅',
      'failed': '❌',
      'paused': '⏸️',
      'error': '❌'
    };
    return icons[status] || '⚪';
  }
}

module.exports = ProgressDisplay;
