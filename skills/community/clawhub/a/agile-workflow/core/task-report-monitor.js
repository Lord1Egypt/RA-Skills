#!/usr/bin/env node
/**
 * 任务汇报监控器 v2.0（优化版）
 * 
 * 核心原则:
 * 1. 增量汇报：只报告新完成的任务
 * 2. 已完成静默：不重复展示历史完成任务
 * 3. 聚焦执行：运行中 + 待执行 + 新增完成
 * 4. 执行者透明：每个任务标注 Agent
 */

const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

class TaskReportMonitor {
  constructor(config = {}) {
    this.config = {
      reportInterval: config.reportInterval || 300000, // 5 分钟汇报一次
      projectDir: config.projectDir,
      logFile: path.join(path.dirname(config.projectDir), 'logs/task-report-monitor.log'),
      ...config
    };
    
    this.lastReportedCompletedList = []; // 上次汇报的已完成任务列表
    this.lastReportedFailed = new Set(); // 上次汇报的失败任务
    
    // 确保日志目录
    const logDir = path.dirname(this.config.logFile);
    if (!fs.existsSync(logDir)) {
      fs.mkdirSync(logDir, { recursive: true });
    }
  }
  
  /**
   * 记录日志
   */
  log(message) {
    const timestamp = new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' });
    const logLine = `[${timestamp}] ${message}\n`;
    console.log(logLine.trim());
    fs.appendFileSync(this.config.logFile, logLine);
  }
  
  /**
   * 加载任务状态
   */
  loadState() {
    const stateFile = path.join(this.config.projectDir, '.task-state.json');
    try {
      return JSON.parse(fs.readFileSync(stateFile, 'utf-8'));
    } catch (e) {
      this.log('❌ 加载任务状态失败：' + e.message);
      return null;
    }
  }
  
  /**
   * 启动任务汇报（守护模式）
   */
  startDaemon() {
    this.log('🚀 任务汇报监控器启动（优化版）');
    this.log('📊 汇报间隔：' + this.config.reportInterval/1000 + 's');
    
    // 定期汇报
    setInterval(() => {
      this.sendReport().catch(e => {
        this.log('❌ 汇报失败：' + e.message);
      });
    }, this.config.reportInterval);
    
    // 立即汇报一次
    this.sendReport().catch(console.error);
    
    this.log('✅ 任务汇报监控器已启动');
  }
  
  /**
   * 获取任务类型
   */
  getTaskType(taskId) {
    if (taskId.includes('outline')) return '细纲';
    if (taskId.includes('writing')) return '正文';
    if (taskId.includes('review')) return '审查';
    return '其他';
  }
  
  /**
   * 发送任务进度报告（优化版）
   */
  async sendReport() {
    const state = this.loadState();
    if (!state) return;
    
    const tasks = Object.entries(state);
    const completed = tasks.filter(([k, v]) => v.status === 'completed');
    const running = tasks.filter(([k, v]) => v.status === 'running');
    const pending = tasks.filter(([k, v]) => v.status === 'pending');
    const failed = tasks.filter(([k, v]) => v.status === 'failed');
    
    // 计算新增完成（增量）
    const lastCompletedSet = new Set(this.lastReportedCompletedList);
    const newCompleted = completed.filter(([k, v]) => !lastCompletedSet.has(k));
    
    // 如果没有变化且无运行中任务，跳过汇报
    if (newCompleted.length === 0 && running.length === 0 && failed.length === this.lastReportedFailed.size) {
      this.log('📊 进度无变化，跳过汇报');
      return;
    }
    
    // 更新上次状态
    this.lastReportedCompletedList = completed.map(([k]) => k);
    this.lastReportedFailed = new Set(failed.map(([k]) => k));
    
    // 生成优化报告
    const lines = [];
    lines.push('=== 任务执行快照 ===');
    lines.push('');
    
    // 1. 运行中任务
    lines.push(`【运行中】(${running.length}个)`);
    if (running.length === 0) {
      lines.push('- 无');
    } else {
      running.forEach(([k, v]) => {
        const agent = v.agent || '未分配';
        const type = this.getTaskType(k);
        lines.push(`- ${k} | ${agent} | ${type}`);
      });
    }
    lines.push('');
    
    // 2. 待执行任务（前 10 个）
    const topPending = pending.slice(0, 10);
    lines.push(`【待执行】(${pending.length}个，显示前 10 个)`);
    if (topPending.length === 0) {
      lines.push('- 无');
    } else {
      topPending.forEach(([k, v]) => {
        const agent = v.agent || '未分配';
        const type = this.getTaskType(k);
        lines.push(`- ${k} | ${agent} | ${type}`);
      });
    }
    lines.push('');
    
    // 3. 新增完成任务（增量）
    lines.push(`【本次新增完成】(${newCompleted.length}个)`);
    if (newCompleted.length === 0) {
      lines.push('- 无新增');
    } else {
      newCompleted.forEach(([k, v]) => {
        const agent = v.agent || '未分配';
        const completedAt = v.completedAt ? new Date(v.completedAt).toLocaleTimeString('zh-CN') : '未知';
        lines.push(`- ${k} | ${agent} | ${completedAt}`);
      });
    }
    lines.push('');
    
    // 4. 失败任务（需要关注）
    if (failed.length > 0) {
      lines.push(`【失败任务】(${failed.length}个，需处理)`);
      failed.forEach(([k, v]) => {
        const agent = v.agent || '未分配';
        lines.push(`- ${k} | ${agent}`);
      });
      lines.push('');
    }
    
    // 5. 统计信息
    const total = tasks.length;
    const completedCount = completed.length;
    const progress = ((completedCount / total) * 100).toFixed(1);
    lines.push('=== 统计 ===');
    lines.push(`总进度：${completedCount}/${total} (${progress}%)`);
    lines.push(`运行中：${running.length} | 待执行：${pending.length} | 失败：${failed.length}`);
    
    // 输出报告
    lines.forEach(line => this.log(line));
  }
}

module.exports = TaskReportMonitor;

// CLI 入口
if (require.main === module) {
  const args = process.argv.slice(2);
  const projectDir = args[0];
  
  if (!projectDir) {
    console.log('用法：node task-report-monitor.js <项目目录>');
    process.exit(1);
  }
  
  const monitor = new TaskReportMonitor({ projectDir });
  monitor.startDaemon();
  console.log('任务汇报监控器运行中... (Ctrl+C 停止)');
}
