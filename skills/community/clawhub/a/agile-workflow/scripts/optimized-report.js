#!/usr/bin/env node
/**
 * 优化任务汇报生成器 v1.0
 * 
 * 核心原则:
 * 1. 增量汇报：只报告新完成的任务
 * 2. 已完成静默：不重复展示历史完成任务
 * 3. 聚焦执行：运行中 + 待执行 + 新增完成
 * 4. 执行者透明：每个任务标注 Agent
 */

const fs = require('fs');
const path = require('path');

class OptimizedReporter {
  constructor(projectDir) {
    this.projectDir = projectDir;
    this.stateFile = path.join(projectDir, '.task-state.json');
    this.lastReportFile = path.join(projectDir, '.last-report-state.json');
  }

  loadState() {
    return JSON.parse(fs.readFileSync(this.stateFile, 'utf-8'));
  }

  loadLastReport() {
    if (!fs.existsSync(this.lastReportFile)) {
      return { completed: [], timestamp: null };
    }
    return JSON.parse(fs.readFileSync(this.lastReportFile, 'utf-8'));
  }

  saveLastReport(state) {
    fs.writeFileSync(this.lastReportFile, JSON.stringify(state, null, 2));
  }

  generateReport() {
    const state = this.loadState();
    const lastReport = this.loadLastReport();

    // 分类任务
    const tasks = Object.entries(state);
    const running = tasks.filter(([k, v]) => v.status === 'running');
    const pending = tasks.filter(([k, v]) => v.status === 'pending');
    const completed = tasks.filter(([k, v]) => v.status === 'completed');
    const failed = tasks.filter(([k, v]) => v.status === 'failed');

    // 计算新增完成（增量）
    const lastCompletedSet = new Set(lastReport.completed);
    const newCompleted = completed.filter(([k, v]) => !lastCompletedSet.has(k));

    // 生成汇报
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

    // 保存状态用于下次对比
    this.saveLastReport({
      completed: completed.map(([k]) => k),
      timestamp: new Date().toISOString()
    });

    return lines.join('\n');
  }

  getTaskType(taskId) {
    if (taskId.includes('outline')) return '细纲';
    if (taskId.includes('writing')) return '正文';
    if (taskId.includes('review')) return '审查';
    return '其他';
  }
}

// 主执行
const projectDir = process.argv[2] || process.env.OPENCLAW_PROJECT_DIR || '.';
const reporter = new OptimizedReporter(projectDir);
console.log(reporter.generateReport());
