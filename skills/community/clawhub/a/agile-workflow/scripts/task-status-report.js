#!/usr/bin/env node
/**
 * 任务状态报告生成器 v2.0
 * 
 * 核心原则:
 * 1. 聚焦最小单位任务
 * 2. 显示执行人、任务、状态、进度
 * 3. 不聚合章节范围
 */

const fs = require('fs');
const path = require('path');

class TaskStatusReporter {
  constructor(projectDir) {
    this.projectDir = projectDir;
    this.stateFile = path.join(projectDir, '.task-state.json');
  }

  loadState() {
    return JSON.parse(fs.readFileSync(this.stateFile, 'utf-8'));
  }

  generateReport() {
    const state = this.loadState();
    const tasks = Object.entries(state);
    
    const running = tasks.filter(([k, v]) => v.status === 'running');
    const pending = tasks.filter(([k, v]) => v.status === 'pending');
    const completedToday = tasks.filter(([k, v]) => {
      if (v.status !== 'completed' || !v.completedAt) return false;
      const today = new Date().toDateString();
      return new Date(v.completedAt).toDateString() === today;
    });
    const failed = tasks.filter(([k, v]) => v.status === 'failed');

    const lines = [];
    
    // 标题
    lines.push('=== 任务执行状态 ===');
    lines.push(`更新时间：${new Date().toLocaleString('zh-CN')}`);
    lines.push('');

    // 运行中任务（按执行人分组）
    lines.push('【执行中】');
    if (running.length === 0) {
      lines.push('  无');
    } else {
      const byAgent = {};
      running.forEach(([k, v]) => {
        const agent = v.agent || '未分配';
        if (!byAgent[agent]) byAgent[agent] = [];
        byAgent[agent].push({ id: k, type: this.getTaskType(k), updatedAt: v.updatedAt });
      });
      
      Object.entries(byAgent).forEach(([agent, taskList]) => {
        lines.push(`  ${agent} (${taskList.length}个):`);
        taskList.forEach(task => {
          const progress = this.getProgress(task.id);
          lines.push(`    - ${task.id} | ${task.type} | ${progress}`);
        });
      });
    }
    lines.push('');

    // 待执行任务（前 15 个，按执行人分组）
    lines.push(`【待执行】(显示前 15 个)`);
    if (pending.length === 0) {
      lines.push('  无');
    } else {
      const topPending = pending.slice(0, 15);
      const byAgent = {};
      topPending.forEach(([k, v]) => {
        const agent = v.agent || '未分配';
        if (!byAgent[agent]) byAgent[agent] = [];
        byAgent[agent].push({ id: k, type: this.getTaskType(k) });
      });
      
      Object.entries(byAgent).forEach(([agent, taskList]) => {
        lines.push(`  ${agent} (${taskList.length}个):`);
        taskList.forEach(task => {
          lines.push(`    - ${task.id} | ${task.type} | 等待依赖`);
        });
      });
      
      if (pending.length > 15) {
        lines.push(`  ... 还有 ${pending.length - 15} 个待执行任务`);
      }
    }
    lines.push('');

    // 今日完成
    lines.push(`【今日完成】(${completedToday.length}个)`);
    if (completedToday.length === 0) {
      lines.push('  无');
    } else {
      completedToday.slice(0, 20).forEach(([k, v]) => {
        const agent = v.agent || '未分配';
        const type = this.getTaskType(k);
        const time = new Date(v.completedAt).toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
        lines.push(`  - ${k} | ${agent} | ${type} | ${time}`);
      });
      if (completedToday.length > 20) {
        lines.push(`  ... 还有 ${completedToday.length - 20} 个`);
      }
    }
    lines.push('');

    // 失败任务
    if (failed.length > 0) {
      lines.push(`【失败】(${failed.length}个，需处理)`);
      failed.forEach(([k, v]) => {
        const agent = v.agent || '未分配';
        const type = this.getTaskType(k);
        lines.push(`  - ${k} | ${agent} | ${type}`);
      });
      lines.push('');
    }

    // 统计
    const total = tasks.length;
    const completed = tasks.filter(([k, v]) => v.status === 'completed').length;
    const progress = ((completed / total) * 100).toFixed(1);
    
    lines.push('=== 统计 ===');
    lines.push(`总任务：${total} | 完成：${completed} (${progress}%) | 执行中：${running.length} | 待执行：${pending.length} | 失败：${failed.length}`);

    return lines.join('\n');
  }

  getTaskType(taskId) {
    if (taskId.includes('outline')) return '细纲';
    if (taskId.includes('writing')) return '正文';
    if (taskId.includes('review')) return '审查';
    return '其他';
  }

  getProgress(taskId) {
    // 简单进度估算
    if (taskId.includes('outline')) return '生成中...';
    if (taskId.includes('writing')) return '创作中...';
    if (taskId.includes('review')) return '审查中...';
    return '执行中...';
  }
}

// CLI 入口
const projectDir = process.argv[2] || process.env.OPENCLAW_PROJECT_DIR || '.';
const reporter = new TaskStatusReporter(projectDir);
console.log(reporter.generateReport());
