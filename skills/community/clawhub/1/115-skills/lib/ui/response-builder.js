/**
 * 115 响应构建器 - 卡片式 UI
 * 
 * 功能：
 * - 统一卡片格式
 * - 进度条生成
 * - 表格格式化
 * - 列表格式化
 * - 按钮/快捷操作
 */

class ResponseBuilder {
  constructor() {
    this.divider = '━━━━━━━━━━━━━━━━━━━━';
    this.smallDivider = '────────────────────';
  }

  /**
   * 构建基础卡片
   * @param {Object} options - 选项
   * @returns {string}
   */
  buildCard(options) {
    const {
      title = '',
      icon = '',
      subtitle = '',
      content = '',
      footer = '',
      actions = []
    } = options;

    let output = '';

    // 标题行
    if (title) {
      output += `${icon ? icon + ' ' : ''}${title}\n`;
      output += `${this.divider}\n`;
    }

    // 副标题
    if (subtitle) {
      output += `${subtitle}\n`;
    }

    // 内容
    if (content) {
      output += `${content}\n`;
    }

    // 操作按钮
    if (actions && actions.length > 0) {
      output += `\n${this.smallDivider}\n`;
      output += `💡 操作建议\n`;
      output += `${this.smallDivider}\n`;
      
      actions.forEach((action, index) => {
        const num = index + 1;
        const icon = action.icon || '•';
        output += `${num}. ${icon} ${action.label}`;
        if (action.hint) {
          output += ` - ${action.hint}`;
        }
        output += `\n`;
      });
    }

    // 页脚
    if (footer) {
      output += `\n${this.smallDivider}\n`;
      output += `${footer}\n`;
    }

    return output;
  }

  /**
   * 构建进度条
   * @param {number} current - 当前值
   * @param {number} total - 总值
   * @param {Object} options - 选项
   * @returns {string}
   */
  buildProgressBar(current, total, options = {}) {
    const {
      width = 20,
      showPercent = true,
      showCount = true,
      filledChar = '█',
      emptyChar = '░'
    } = options;

    const percent = total > 0 ? (current / total) * 100 : 0;
    const filledWidth = Math.round((percent / 100) * width);
    const emptyWidth = width - filledWidth;

    const bar = filledChar.repeat(filledWidth) + emptyChar.repeat(emptyWidth);
    
    let output = `[${bar}]`;
    
    if (showPercent) {
      output += ` ${percent.toFixed(1)}%`;
    }
    
    if (showCount) {
      output += ` (${current}/${total})`;
    }

    return output;
  }

  /**
   * 构建状态卡片
   * @param {Object} data - 状态数据
   * @returns {string}
   */
  buildStatusCard(data) {
    const {
      title = '状态',
      // icon = '📊', // 暂时未使用
      items = [],
      status = 'normal'
    } = data;

    const statusIcons = {
      success: '✅',
      error: '❌',
      warning: '⚠️',
      info: 'ℹ️',
      normal: '📊'
    };

    const statusIcon = statusIcons[status] || statusIcons.normal;

    let content = '';
    items.forEach(item => {
      const label = item.label || '';
      const value = item.value || '';
      const unit = item.unit || '';
      content += `${label}: ${value}${unit}\n`;
    });

    return this.buildCard({
      title,
      icon: statusIcon,
      content,
      style: status
    });
  }

  /**
   * 构建文件列表卡片
   * @param {Array} files - 文件列表
   * @param {Object} options - 选项
   * @returns {string}
   */
  buildFileList(files, options = {}) {
    const {
      title = '文件列表',
      showSize = true,
      showDate = false,
      limit = 10
    } = options;

    if (!files || files.length === 0) {
      return this.buildCard({
        title: '空列表',
        icon: '📁',
        content: '暂无文件',
        style: 'info'
      });
    }

    const displayFiles = files.slice(0, limit);
    
    let content = '';
    displayFiles.forEach((file, index) => {
      const icon = file.is_folder ? '📁' : '📄';
      const name = file.file_name || file.name || '未知';
      const size = showSize && file.file_size ? this._formatSize(file.file_size) : '';
      const date = showDate && file.file_time ? this._formatTime(file.file_time) : '';
      
      content += `${index + 1}. ${icon} ${name}`;
      if (size) content += ` (${size})`;
      if (date) content += ` [${date}]`;
      content += `\n`;
    });

    if (files.length > limit) {
      content += `\n... 还有 ${files.length - limit} 个文件\n`;
    }

    return this.buildCard({
      title,
      icon: '📁',
      content,
      footer: `共 ${files.length} 个文件`,
      actions: [
        { icon: '🔍', label: '搜索文件', hint: '快速查找' },
        { icon: '📥', label: '批量下载', hint: '下载选中' },
        { icon: '🗑️', label: '批量删除', hint: '删除选中' }
      ]
    });
  }

  /**
   * 构建任务列表卡片
   * @param {Array} tasks - 任务列表
   * @param {Object} options - 选项
   * @returns {string}
   */
  buildTaskList(tasks, options = {}) {
    const {
      title = '任务列表',
      type = 'download'
    } = options;

    if (!tasks || tasks.length === 0) {
      return this.buildCard({
        title: '空列表',
        icon: type === 'download' ? '📥' : '📤',
        content: '暂无任务',
        style: 'info'
      });
    }

    const taskIcon = type === 'download' ? '📥' : '📤';
    
    let content = '';
    tasks.forEach((task, index) => {
      const name = task.file_name || task.name || '未知任务';
      const status = this._formatTaskStatus(task.status || task.state);
      const progress = task.percent || '0';
      const size = task.file_size ? this._formatSize(task.file_size) : '';
      
      content += `${index + 1}. ${name}\n`;
      content += `   ${status} | 进度：${progress}%`;
      if (size) content += ` | 大小：${size}`;
      content += `\n\n`;
    });

    return this.buildCard({
      title,
      icon: taskIcon,
      content,
      footer: `共 ${tasks.length} 个任务`,
      actions: [
        { icon: '⏸️', label: '暂停任务', hint: '暂停下载' },
        { icon: '▶️', label: '继续任务', hint: '继续下载' },
        { icon: '🗑️', label: '清理完成', hint: '删除已完成' }
      ]
    });
  }

  /**
   * 构建清理建议卡片
   * @param {Object} suggestions - 建议数据
   * @returns {string}
   */
  buildCleanSuggestions(suggestions) {
    if (!suggestions || !suggestions.suggestions || suggestions.suggestions.length === 0) {
      return this.buildCard({
        title: '存储空间',
        icon: '✅',
        content: '存储空间健康，无需清理',
        style: 'success'
      });
    }

    const urgentCount = suggestions.suggestions.filter(s => s.type === 'urgent').length;
    const warningCount = suggestions.suggestions.filter(s => s.type === 'warning').length;
    
    let content = '';
    suggestions.suggestions.slice(0, 5).forEach((suggestion, index) => {
      const icon = suggestion.type === 'urgent' ? '🚨' : 
                   suggestion.type === 'warning' ? '⚠️' : 'ℹ️';
      content += `${index + 1}. ${icon} ${suggestion.title}\n`;
      content += `   ${suggestion.description}\n\n`;
    });

    if (suggestions.suggestions.length > 5) {
      content += `... 还有 ${suggestions.suggestions.length - 5} 条建议\n`;
    }

    let status = 'normal';
    if (urgentCount > 0) status = 'error';
    else if (warningCount > 0) status = 'warning';

    return this.buildCard({
      title: '清理建议',
      icon: status === 'error' ? '🚨' : status === 'warning' ? '⚠️' : '🧹',
      content,
      footer: `共 ${suggestions.suggestions.length} 条建议`,
      style: status,
      actions: [
        { icon: '🗑️', label: '一键清理', hint: '清理推荐项' },
        { icon: '📊', label: '查看详情', hint: '分析详情' }
      ]
    });
  }

  /**
   * 构建分享卡片
   * @param {Object} share - 分享数据
   * @returns {string}
   */
  buildShareCard(share) {
    if (!share || !share.data) {
      return this.buildCard({
        title: '分享信息',
        icon: '❌',
        content: '分享信息不可用',
        style: 'error'
      });
    }

    const data = share.data;
    
    let content = '';
    content += `📝 标题：${data.share_title || '无标题'}\n`;
    content += `🔗 链接：${data.share_url || data.share_code || '无'}\n`;
    
    if (data.receive_code) {
      content += `🔑 提取码：${data.receive_code}\n`;
    }
    
    content += `📁 文件：${data.file_count || 0} 个\n`;
    content += `💾 大小：${data.total_size ? this._formatSize(data.total_size) : '未知'}\n`;
    
    if (data.share_duration) {
      content += `⏰ 有效期：${data.share_duration}\n`;
    }
    
    if (data.receive_count !== undefined) {
      content += `👁️ 访问：${data.receive_count} 次\n`;
    }

    return this.buildCard({
      title: '分享详情',
      icon: '📦',
      content,
      actions: [
        { icon: '⏰', label: '更新时长', hint: '修改有效期' },
        { icon: '👁️', label: '查看访问', hint: '访问列表' },
        { icon: '❌', label: '取消分享', hint: '删除分享' }
      ]
    });
  }

  /**
   * 构建空间统计卡片
   * @param {Object} space - 空间数据
   * @returns {string}
   */
  buildSpaceCard(space) {
    if (!space || !space.analysis) {
      return this.buildCard({
        title: '存储空间',
        icon: '❌',
        content: '空间信息获取失败',
        style: 'error'
      });
    }

    const analysis = space.analysis;
    const percent = analysis.percent;
    
    const progressBar = this.buildProgressBar(percent, 100, {
      width: 30,
      filledChar: percent >= 90 ? '🔴' : percent >= 80 ? '🟡' : '🟢',
      emptyChar: '⚪'
    });

    let content = '';
    content += `${progressBar}\n\n`;
    content += `已用：${this._formatSize(analysis.used)}\n`;
    content += `总共：${this._formatSize(analysis.total)}\n`;
    content += `剩余：${this._formatSize(analysis.remain)}\n`;

    let status = 'normal';
    let title = '存储空间';
    let icon = '📊';
    
    if (percent >= 90) {
      status = 'error';
      title = '空间严重不足';
      icon = '🚨';
    } else if (percent >= 80) {
      status = 'warning';
      title = '空间紧张';
      icon = '⚠️';
    } else if (percent >= 60) {
      icon = '📊';
    } else {
      status = 'success';
      icon = '✅';
    }

    return this.buildCard({
      title,
      icon,
      content,
      style: status,
      actions: [
        { icon: '🧹', label: '清理空间', hint: '智能清理' },
        { icon: '📁', label: '查看文件', hint: '浏览文件' },
        { icon: '🤖', label: '智能整理', hint: '自动分类' }
      ]
    });
  }

  /**
   * 构建错误卡片
   * @param {Object} error - 错误对象
   * @returns {string}
   */
  buildErrorCard(error) {
    const message = error.message || '未知错误';
    const recoveries = error.recoveries || [];

    let content = `${message}\n`;
    
    if (recoveries.length > 0) {
      content += `\n${this.smallDivider}\n`;
      content += `💡 建议操作\n`;
      content += `${this.smallDivider}\n`;
      
      recoveries.forEach((rec, index) => {
        content += `${index + 1}. ${rec}\n`;
      });
    }

    return this.buildCard({
      title: '操作失败',
      icon: '❌',
      content,
      style: 'error'
    });
  }

  /**
   * 构建批量操作结果卡片
   * @param {Object} result - 操作结果
   * @returns {string}
   */
  buildBatchResultCard(result) {
    const progress = result.progress || {};
    const total = progress.total || 0;
    const success = progress.success || 0;
    const failed = progress.failed || 0;
    // const percent = total > 0 ? (success / total * 100) : 0; // 暂时未使用

    const progressBar = this.buildProgressBar(success, total, {
      width: 30
    });

    let content = `${progressBar}\n\n`;
    content += `成功：${success} 个 ✅\n`;
    content += `失败：${failed} 个 ❌\n`;

    if (progress.errors && progress.errors.length > 0) {
      content += `\n${this.smallDivider}\n`;
      content += `⚠️ 错误详情\n`;
      content += `${this.smallDivider}\n`;
      
      progress.errors.slice(0, 3).forEach((err, index) => {
        content += `${index + 1}. ${err.error}\n`;
      });
      
      if (progress.errors.length > 3) {
        content += `... 还有 ${progress.errors.length - 3} 个错误\n`;
      }
    }

    let status = 'success';
    if (failed > 0) status = failed === total ? 'error' : 'warning';

    return this.buildCard({
      title: result.message || '批量操作',
      icon: status === 'success' ? '✅' : status === 'error' ? '❌' : '⚠️',
      content,
      style: status
    });
  }

  /**
   * 构建快捷命令帮助卡片
   * @returns {string}
   */
  buildHelpCard() {
    const content = `
📝 斜杠命令
   /115 容量 - 查看存储空间
   /115 文件 - 浏览文件
   /115 搜索 关键词 - 搜索文件

💬 快捷词
   容量、文件、搜索
   下载、转存、分享
   整理、清理、返回

🔗 直接发送
   分享链接：115.com/s/abc123
   磁力链接：magnet:?xt=...
   HTTP 链接：https://...
`.trim();

    return this.buildCard({
      title: '使用帮助',
      icon: '❓',
      content,
      footer: '回复任意命令开始使用'
    });
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
  _formatTime(timestamp) {
    const date = new Date(timestamp * 1000);
    return date.toLocaleDateString('zh-CN');
  }

  /**
   * 格式化任务状态
   * @private
   */
  _formatTaskStatus(status) {
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
}

module.exports = ResponseBuilder;
