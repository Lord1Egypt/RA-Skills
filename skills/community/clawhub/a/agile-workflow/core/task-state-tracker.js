#!/usr/bin/env node
/**
 * 任务状态追踪器 v7.17
 * 
 * 核心功能:
 * 1. 追踪任务状态（pending/running/completed/failed）
 * 2. 任务完成时自动触发调度器
 * 3. 持久化状态到文件
 */

const fs = require('fs');
const path = require('path');

class TaskStateTracker {
  constructor(projectDir) {
    this.projectDir = projectDir;
    this.stateFile = path.join(projectDir, '.task-state.json');
    this.states = this.loadStates();
  }

  /**
   * 加载状态
   */
  loadStates() {
    if (fs.existsSync(this.stateFile)) {
      return JSON.parse(fs.readFileSync(this.stateFile, 'utf8'));
    }
    return {};
  }

  /**
   * 保存状态
   */
  saveStates() {
    fs.writeFileSync(this.stateFile, JSON.stringify(this.states, null, 2), 'utf8');
  }

  /**
   * 更新任务状态
   */
  updateTask(taskId, status, metadata = {}) {
    console.log(`📊 更新任务状态：${taskId} → ${status}`);
    
    this.states[taskId] = {
      status,
      updatedAt: new Date().toISOString(),
      ...metadata
    };
    
    this.saveStates();
    
    // ✅ 触发调度器检查
    if (status === 'completed') {
      this.triggerScheduler();
    }
  }

  /**
   * 获取任务状态
   */
  getTaskStatus(taskId) {
    return this.states[taskId];
  }

  /**
   * 获取所有待执行任务
   */
  getPendingTasks() {
    return Object.entries(this.states)
      .filter(([_, state]) => state.status === 'pending')
      .map(([id, state]) => ({ id, ...state }));
  }

  /**
   * 获取已完成任务
   */
  getCompletedTasks() {
    return Object.entries(this.states)
      .filter(([_, state]) => state.status === 'completed')
      .map(([id, state]) => ({ id, ...state }));
  }

  /**
   * 触发调度器
   */
  triggerScheduler() {
    try {
      const TaskScheduler = require('./task-scheduler');
      const scheduler = new TaskScheduler(this.projectDir);
      scheduler.checkAndTrigger().catch(console.error);
    } catch (error) {
      console.error('触发调度器失败:', error.message);
    }
  }

  /**
   * 初始化任务
   */
  initTasks(tasks) {
    for (const [taskId, taskConfig] of Object.entries(tasks)) {
      if (!this.states[taskId]) {
        this.states[taskId] = {
          status: 'pending',
          agent: taskConfig.agent,
          description: taskConfig.description,
          dependsOn: taskConfig.dependsOn || [],
          createdAt: new Date().toISOString()
        };
      }
    }
    this.saveStates();
  }

  /**
   * 获取进度摘要
   */
  getProgressSummary() {
    const total = Object.keys(this.states).length;
    const completed = Object.values(this.states).filter(s => s.status === 'completed').length;
    const running = Object.values(this.states).filter(s => s.status === 'running').length;
    const pending = Object.values(this.states).filter(s => s.status === 'pending').length;
    
    return {
      total,
      completed,
      running,
      pending,
      percent: total > 0 ? Math.round((completed / total) * 100) : 0
    };
  }
}

module.exports = TaskStateTracker;

// CLI 入口
if (require.main === module) {
  const args = process.argv.slice(2);
  const [projectDir, command, taskId, status] = args;
  
  if (!projectDir || !command) {
    console.log('用法：node task-state-tracker.js <项目目录> <命令> [任务 ID] [状态]');
    console.log('命令：status, update, list, summary');
    process.exit(1);
  }
  
  const tracker = new TaskStateTracker(projectDir);
  
  switch (command) {
    case 'status':
      if (taskId) {
        console.log(JSON.stringify(tracker.getTaskStatus(taskId), null, 2));
      }
      break;
    
    case 'update':
      if (taskId && status) {
        tracker.updateTask(taskId, status);
        console.log(`✅ 已更新 ${taskId} → ${status}`);
      }
      break;
    
    case 'list':
      console.log('待执行任务:');
      tracker.getPendingTasks().forEach(t => console.log(`  - ${t.id}`));
      console.log('已完成任务:');
      tracker.getCompletedTasks().forEach(t => console.log(`  - ${t.id}`));
      break;
    
    case 'summary':
      const summary = tracker.getProgressSummary();
      console.log(`总任务：${summary.total}`);
      console.log(`已完成：${summary.completed}`);
      console.log(`进行中：${summary.running}`);
      console.log(`待执行：${summary.pending}`);
      console.log(`进度：${summary.percent}%`);
      break;
    
    default:
      console.log(`未知命令：${command}`);
  }
}
