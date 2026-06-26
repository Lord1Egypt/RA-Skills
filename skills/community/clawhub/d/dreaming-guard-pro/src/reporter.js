/**
 * Dreaming Guard Pro - Reporter Module (Phase 5)
 * 
 * 健康报告：定期输出dreaming健康状态
 * 报告格式：text/json/markdown
 * 内容：当前状态、趋势预测、最近动作、建议
 * 
 * 纯Node.js实现，零外部依赖
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

// 报告格式
const REPORT_FORMATS = {
  TEXT: 'text',
  JSON: 'json',
  MARKDOWN: 'markdown'
};

// 默认配置
const DEFAULT_CONFIG = {
  outputDir: path.join(os.homedir(), '.openclaw', 'logs'),
  reportInterval: 3600000,  // 1小时
  maxReports: 24,           // 保留24份报告
  defaultFormat: REPORT_FORMATS.TEXT,
  includeHistory: true,
  historyLimit: 10
};

/**
 * Reporter类 - 健康报告生成器
 */
class Reporter {
  constructor(options = {}) {
    this.config = { ...DEFAULT_CONFIG, ...options };
    
    // 确保输出目录存在
    if (!fs.existsSync(this.config.outputDir)) {
      fs.mkdirSync(this.config.outputDir, { recursive: true });
    }
    
    // 绑定依赖模块
    this.monitor = options.monitor;
    this.analyzer = options.analyzer;
    this.decision = options.decision;
    this.protector = options.protector;
    this.healer = options.healer;
    this.stateManager = options.stateManager;
    
    // 绑定日志器
    this.logger = options.logger || {
      debug: (...args) => console.debug('[Reporter]', ...args),
      info: (...args) => console.info('[Reporter]', ...args),
      warn: (...args) => console.warn('[Reporter]', ...args),
      error: (...args) => console.error('[Reporter]', ...args)
    };
    
    // 报告历史
    this.reports = [];
  }

  /**
   * 生成健康报告
   * @param {string} format - 报告格式 (text/json/markdown)
   * @returns {object} 报告对象
   */
  generate(format = this.config.defaultFormat) {
    const timestamp = Date.now();
    
    // 收集数据
    const data = this._collectData();
    
    // 生成摘要
    const summary = this.getSummary(data);
    
    // 格式化报告
    const content = this.formatReport(data, format);
    
    // 构建报告对象
    const report = {
      timestamp,
      format,
      summary,
      data,
      content,
      generatedAt: new Date(timestamp).toISOString()
    };
    
    // 保存到历史
    this.reports.push(report);
    if (this.reports.length > this.config.maxReports) {
      this.reports.shift();
    }
    
    this.logger.info('Report generated', { format, timestamp });
    
    return report;
  }

  /**
   * 获取健康摘要
   * @param {object} data - 数据对象（可选）
   * @returns {object} 摘要对象
   */
  getSummary(data = null) {
    if (!data) {
      data = this._collectData();
    }
    
    return {
      status: this._determineStatus(data),
      score: this._calculateScore(data),
      riskLevel: data.analysis?.riskLevel || 'unknown',
      currentSize: data.current?.totalSize || 0,
      currentFiles: data.current?.totalFiles || 0,
      growthRate: data.analysis?.growthRateKB || 0,
      memoryUsage: data.memory?.usagePercent || 0,
      lastAction: data.actions?.length > 0 ? data.actions[0] : null,
      recommendation: data.analysis?.recommendation || 'continue_monitoring',
      timestamp: data.timestamp
    };
  }

  /**
   * 格式化报告
   * @param {object} data - 数据对象
   * @param {string} format - 报告格式
   * @returns {string} 格式化内容
   */
  formatReport(data, format) {
    switch (format) {
      case REPORT_FORMATS.JSON:
        return this._formatJson(data);
      case REPORT_FORMATS.MARKDOWN:
        return this._formatMarkdown(data);
      case REPORT_FORMATS.TEXT:
      default:
        return this._formatText(data);
    }
  }

  /**
   * 收集报告数据
   * @returns {object} 数据对象
   */
  _collectData() {
    const timestamp = Date.now();
    const data = {
      timestamp,
      generatedAt: new Date(timestamp).toISOString(),
      current: null,
      analysis: null,
      memory: null,
      actions: [],
      healer: null,
      protector: null,
      trend: null
    };
    
    // 从Monitor获取当前状态
    if (this.monitor) {
      const status = this.monitor.getStatus();
      const snapshot = this.monitor.getLatestSnapshot();
      data.current = {
        totalSize: status.currentSize,
        totalFiles: status.currentFiles,
        growthRate: status.growthRate,
        running: status.running,
        path: status.path
      };
      
      // 获取趋势
      if (this.config.includeHistory) {
        data.trend = this.monitor.getTrend(30);
      }
    }
    
    // 从Analyzer获取分析结果
    if (this.analyzer && this.monitor) {
      const history = this.monitor.getHistory(60);
      data.analysis = this.analyzer.analyze(history);
    }
    
    // 获取内存状态
    const memUsage = process.memoryUsage();
    const totalMem = os.totalmem();
    const freeMem = os.freemem();
    data.memory = {
      process: {
        rssMB: Math.round(memUsage.rss / 1024 / 1024),
        heapUsedMB: Math.round(memUsage.heapUsed / 1024 / 1024),
        heapTotalMB: Math.round(memUsage.heapTotal / 1024 / 1024)
      },
      system: {
        totalMB: Math.round(totalMem / 1024 / 1024),
        freeMB: Math.round(freeMem / 1024 / 1024),
        usedMB: Math.round((totalMem - freeMem) / 1024 / 1024),
        usagePercent: Math.round((totalMem - freeMem) / totalMem * 100)
      },
      usagePercent: Math.round(memUsage.rss / (512 * 1024 * 1024) * 100) // 相对512MB阈值
    };
    
    // 从Decision获取最近动作
    if (this.decision) {
      data.actions = this.decision.getHistory(this.config.historyLimit);
    }
    
    // 从Protector获取保护状态
    if (this.protector) {
      data.protector = this.protector.getStatus();
    }
    
    // 从Healer获取自愈状态
    if (this.healer) {
      data.healer = this.healer.getStatus();
    }
    
    // 从StateManager获取历史动作
    if (this.stateManager) {
      const actionHistory = this.stateManager.getActionHistory(5);
      if (actionHistory.length > 0) {
        data.actions = [...actionHistory, ...data.actions].slice(-this.config.historyLimit);
      }
    }
    
    return data;
  }

  /**
   * 确定整体状态
   * @param {object} data - 数据对象
   * @returns {string} 状态 (healthy/warning/critical/emergency)
   */
  _determineStatus(data) {
    const riskLevel = data.analysis?.riskLevel;
    
    if (riskLevel === 'red') return 'critical';
    if (riskLevel === 'yellow') return 'warning';
    
    // 检查内存
    if (data.memory?.usagePercent > 85) return 'warning';
    if (data.memory?.usagePercent > 95) return 'critical';
    
    // 检查Healer状态
    if (data.healer?.status === 'recovering' || data.healer?.status === 'failed') {
      return 'emergency';
    }
    
    return 'healthy';
  }

  /**
   * 计算健康分数 (0-100)
   * @param {object} data - 数据对象
   * @returns {number} 健康分数
   */
  _calculateScore(data) {
    let score = 100;
    
    // 扣分项
    const riskLevel = data.analysis?.riskLevel;
    if (riskLevel === 'red') score -= 40;
    if (riskLevel === 'yellow') score -= 20;
    
    // 内存扣分
    const memUsage = data.memory?.usagePercent || 0;
    if (memUsage > 70) score -= 10;
    if (memUsage > 85) score -= 20;
    if (memUsage > 95) score -= 30;
    
    // 增长率扣分
    const growthRateKB = data.analysis?.growthRateKB || 0;
    if (growthRateKB > 100) score -= 10;
    if (growthRateKB > 500) score -= 20;
    
    // 恢复状态扣分
    if (data.healer?.status === 'failed') score -= 50;
    if (data.healer?.stats?.crashesDetected > 0) score -= 10;
    
    return Math.max(0, Math.min(100, score));
  }

  /**
   * JSON格式报告
   * @param {object} data - 数据对象
   * @returns {string} JSON字符串
   */
  _formatJson(data) {
    return JSON.stringify(data, null, 2);
  }

  /**
   * 文本格式报告
   * @param {object} data - 数据对象
   * @returns {string} 文本内容
   */
  _formatText(data) {
    const lines = [];
    const status = this._determineStatus(data);
    const score = this._calculateScore(data);
    
    lines.push('='.repeat(50));
    lines.push('Dreaming Guard Pro - Health Report');
    lines.push('Generated: ' + data.generatedAt);
    lines.push('='.repeat(50));
    lines.push('');
    
    // 整体状态
    lines.push('[Overall Status]');
    lines.push(`  Status: ${status.toUpperCase()}`);
    lines.push(`  Health Score: ${score}/100`);
    lines.push(`  Risk Level: ${data.analysis?.riskLevel || 'unknown'}`);
    lines.push('');
    
    // 当前状态
    lines.push('[Current State]');
    const sizeKB = Math.round((data.current?.totalSize || 0) / 1024);
    const sizeMB = Math.round(sizeKB / 1024);
    lines.push(`  Total Size: ${sizeMB}MB (${sizeKB}KB)`);
    lines.push(`  Total Files: ${data.current?.totalFiles || 0}`);
    lines.push(`  Growth Rate: ${Math.round(data.analysis?.growthRateKB || 0)} KB/min`);
    lines.push('');
    
    // 内存状态
    lines.push('[Memory Usage]');
    lines.push(`  Process RSS: ${data.memory?.process?.rssMB || 0}MB`);
    lines.push(`  Process Heap: ${data.memory?.process?.heapUsedMB || 0}/${data.memory?.process?.heapTotalMB || 0}MB`);
    lines.push(`  System: ${data.memory?.system?.usedMB || 0}/${data.memory?.system?.totalMB || 0}MB (${data.memory?.system?.usagePercent || 0}%)`);
    lines.push('');
    
    // 趋势分析
    if (data.analysis) {
      lines.push('[Trend Analysis]');
      lines.push(`  Direction: ${data.analysis.trend || 'stable'}`);
      if (data.analysis.prediction?.timeToFullHours) {
        const hours = data.analysis.prediction.timeToFullHours;
        if (hours < Infinity) {
          lines.push(`  Time to Full: ${hours < 1 ? Math.round(hours * 60) + 'min' : Math.round(hours) + 'h'}`);
        } else {
          lines.push('  Time to Full: N/A (no growth)');
        }
      }
      lines.push(`  Confidence: ${Math.round((data.analysis.prediction?.confidence || 0) * 100)}%`);
      lines.push('');
    }
    
    // 最近动作
    if (data.actions && data.actions.length > 0) {
      lines.push('[Recent Actions]');
      for (const action of data.actions.slice(0, 5)) {
        const time = new Date(action.timestamp || 0).toLocaleTimeString();
        lines.push(`  ${time}: ${action.action || 'unknown'} - ${action.reason || ''}`);
      }
      lines.push('');
    }
    
    // 保护状态
    if (data.protector) {
      lines.push('[Protector Status]');
      lines.push(`  Running: ${data.protector.running ? 'Yes' : 'No'}`);
      lines.push(`  Interventions: ${data.protector.stats?.interventions || 0}`);
      lines.push(`  Last Intervention: ${data.protector.lastIntervention || 'None'}`);
      lines.push('');
    }
    
    // 自愈状态
    if (data.healer) {
      lines.push('[Healer Status]');
      lines.push(`  Running: ${data.healer.running ? 'Yes' : 'No'}`);
      lines.push(`  Status: ${data.healer.status || 'idle'}`);
      lines.push(`  Crashes Detected: ${data.healer.stats?.crashesDetected || 0}`);
      lines.push(`  Recoveries: ${data.healer.stats?.recoveriesSucceeded || 0}/${data.healer.stats?.recoveriesAttempted || 0}`);
      lines.push('');
    }
    
    // 建议
    lines.push('[Recommendations]');
    const recommendations = this._generateRecommendations(data);
    for (const rec of recommendations) {
      lines.push(`  - ${rec}`);
    }
    
    lines.push('');
    lines.push('='.repeat(50));
    
    return lines.join('\n');
  }

  /**
   * Markdown格式报告
   * @param {object} data - 数据对象
   * @returns {string} Markdown内容
   */
  _formatMarkdown(data) {
    const status = this._determineStatus(data);
    const score = this._calculateScore(data);
    const statusEmoji = {
      healthy: '🟢',
      warning: '🟡',
      critical: '🔴',
      emergency: '🚨'
    };
    
    const lines = [];
    
    lines.push(`# Dreaming Guard Pro - Health Report`);
    lines.push('');
    lines.push(`**Generated:** ${data.generatedAt}`);
    lines.push('');
    
    lines.push(`## Overall Status`);
    lines.push('');
    lines.push(`| Metric | Value |`);
    lines.push(`|--------|-------|`);
    lines.push(`| Status | ${statusEmoji[status] || '⚪'} ${status.toUpperCase()} |`);
    lines.push(`| Health Score | ${score}/100 |`);
    lines.push(`| Risk Level | ${data.analysis?.riskLevel || 'unknown'} |`);
    lines.push('');
    
    lines.push(`## Current State`);
    lines.push('');
    const sizeMB = Math.round((data.current?.totalSize || 0) / 1024 / 1024);
    lines.push(`| Metric | Value |`);
    lines.push(`|--------|-------|`);
    lines.push(`| Total Size | ${sizeMB}MB |`);
    lines.push(`| Total Files | ${data.current?.totalFiles || 0} |`);
    lines.push(`| Growth Rate | ${Math.round(data.analysis?.growthRateKB || 0)} KB/min |`);
    lines.push('');
    
    lines.push(`## Memory Usage`);
    lines.push('');
    lines.push(`| Metric | Value |`);
    lines.push(`|--------|-------|`);
    lines.push(`| Process RSS | ${data.memory?.process?.rssMB || 0}MB |`);
    lines.push(`| Process Heap | ${data.memory?.process?.heapUsedMB || 0}/${data.memory?.process?.heapTotalMB || 0}MB |`);
    lines.push(`| System Usage | ${data.memory?.system?.usagePercent || 0}% |`);
    lines.push('');
    
    if (data.analysis) {
      lines.push(`## Trend Analysis`);
      lines.push('');
      lines.push(`- **Direction:** ${data.analysis.trend || 'stable'}`);
      if (data.analysis.prediction?.timeToFullHours && data.analysis.prediction.timeToFullHours < Infinity) {
        lines.push(`- **Time to Full:** ${data.analysis.prediction.timeToFullHours < 1 ? Math.round(data.analysis.prediction.timeToFullHours * 60) + ' minutes' : Math.round(data.analysis.prediction.timeToFullHours) + ' hours'}`);
      }
      lines.push(`- **Confidence:** ${Math.round((data.analysis.prediction?.confidence || 0) * 100)}%`);
      lines.push('');
    }
    
    if (data.actions && data.actions.length > 0) {
      lines.push(`## Recent Actions`);
      lines.push('');
      for (const action of data.actions.slice(0, 5)) {
        const time = new Date(action.timestamp || 0).toLocaleTimeString();
        lines.push(`- **${time}:** ${action.action || 'unknown'} - ${action.reason || ''}`);
      }
      lines.push('');
    }
    
    lines.push(`## Recommendations`);
    lines.push('');
    const recommendations = this._generateRecommendations(data);
    for (const rec of recommendations) {
      lines.push(`- ${rec}`);
    }
    
    return lines.join('\n');
  }

  /**
   * 生成建议
   * @param {object} data - 数据对象
   * @returns {array} 建议列表
   */
  _generateRecommendations(data) {
    const recommendations = [];
    const status = this._determineStatus(data);
    
    if (status === 'healthy') {
      recommendations.push('Continue monitoring - system is healthy');
      recommendations.push('No immediate action required');
    } else if (status === 'warning') {
      recommendations.push('Monitor closely - warning conditions detected');
      if (data.analysis?.growthRateKB > 100) {
        recommendations.push('Consider triggering archive to reduce growth');
      }
      if (data.memory?.usagePercent > 70) {
        recommendations.push('Memory usage elevated - check for leaks');
      }
    } else if (status === 'critical') {
      recommendations.push('IMMEDIATE ACTION REQUIRED');
      recommendations.push('Trigger emergency archive or compression');
      if (data.analysis?.prediction?.timeToFullHours < 1) {
        recommendations.push('Critical: capacity filling rapidly');
      }
    } else if (status === 'emergency') {
      recommendations.push('EMERGENCY: recovery in progress or failed');
      recommendations.push('Check healer logs for details');
      recommendations.push('Manual intervention may be needed');
    }
    
    // 通用建议
    if (data.healer?.stats?.crashesDetected > 0) {
      recommendations.push('Recent crashes detected - investigate root cause');
    }
    
    if (data.protector?.stats?.emergencies > 0) {
      recommendations.push('Memory emergencies occurred - consider increasing limits');
    }
    
    return recommendations;
  }

  /**
   * 保存报告到文件
   * @param {object} report - 报告对象
   * @returns {string} 文件路径
   */
  saveReport(report) {
    const filename = `health-report-${new Date(report.timestamp).toISOString().slice(0, 10)}-${report.timestamp}.log`;
    const filepath = path.join(this.config.outputDir, filename);
    
    fs.writeFileSync(filepath, report.content);
    
    this.logger.info('Report saved', { filepath });
    
    // 清理旧报告
    this._cleanupOldReports();
    
    return filepath;
  }

  /**
   * 清理旧报告
   */
  _cleanupOldReports() {
    const files = fs.readdirSync(this.config.outputDir)
      .filter(f => f.startsWith('health-report-'))
      .sort()
      .reverse();
    
    // 删除超出限制的报告
    while (files.length > this.config.maxReports) {
      const oldFile = files.pop();
      const oldPath = path.join(this.config.outputDir, oldFile);
      fs.unlinkSync(oldPath);
      this.logger.debug('Old report removed', { file: oldFile });
    }
  }

  /**
   * 获取报告历史
   * @param {number} limit - 限制数量
   * @returns {array} 报告历史
   */
  getReportHistory(limit = 10) {
    return this.reports.slice(-limit);
  }

  /**
   * 获取最近报告
   * @returns {object|null} 最近报告
   */
  getLastReport() {
    return this.reports.length > 0 ? this.reports[this.reports.length - 1] : null;
  }

  /**
   * 获取配置
   * @returns {object} 配置对象
   */
  getConfig() {
    return { ...this.config };
  }

  /**
   * 更新配置
   * @param {object} newConfig - 新配置
   */
  updateConfig(newConfig) {
    this.config = { ...this.config, ...newConfig };
  }
}

module.exports = Reporter;
module.exports.REPORT_FORMATS = REPORT_FORMATS;