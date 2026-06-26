#!/usr/bin/env node
/**
 * activate-queued-tasks.js - 依赖激活器
 * 检查所有 queued 状态的任务，激活依赖已完成的任务
 * 
 * 用法：node activate-queued-tasks.js
 */

const fs = require('fs');
const path = require('path');

const TASKS_DIR = path.join(__dirname, '..', 'tasks');
const LOGS_DIR = path.join(__dirname, '..', 'logs');
const EVENTS_LOG = path.join(LOGS_DIR, 'events.log');

// 确保日志目录存在
if (!fs.existsSync(LOGS_DIR)) {
  fs.mkdirSync(LOGS_DIR, { recursive: true });
}

/**
 * 写入事件日志
 */
function logEvent(event, data = {}) {
  const entry = {
    timestamp: new Date().toISOString(),
    event,
    ...data
  };
  fs.appendFileSync(EVENTS_LOG, JSON.stringify(entry) + '\n');
  return entry;
}

/**
 * 读取任务文件
 */
function readTask(taskId) {
  const taskFile = path.join(TASKS_DIR, `${taskId}.json`);
  if (!fs.existsSync(taskFile)) {
    return null;
  }
  return JSON.parse(fs.readFileSync(taskFile, 'utf8'));
}

/**
 * 写入任务文件
 */
function writeTask(task) {
  const taskFile = path.join(TASKS_DIR, `${task.task_id}.json`);
  fs.writeFileSync(taskFile, JSON.stringify(task, null, 2));
}

/**
 * 检查依赖是否全部完成
 */
function areDependenciesCompleted(dependsOn) {
  if (!dependsOn || dependsOn.length === 0) {
    return true;
  }
  
  return dependsOn.every(depId => {
    const depTask = readTask(depId);
    return depTask && (depTask.status === 'completed' || depTask.status === 'packaged');
  });
}

/**
 * 激活任务
 */
function activateTask(task) {
  const oldStatus = task.status;
  task.status = 'pending';
  task.activated_at = new Date().toISOString();
  task.history = task.history || [];
  task.history.push({
    timestamp: task.activated_at,
    action: 'activated',
    previous_status: oldStatus,
    note: `依赖已完成：${(task.depends_on || []).join(', ')}`,
    activated_by: 'auto-dependency-check'
  });
  
  writeTask(task);
  
  logEvent('task_activated', {
    task_id: task.task_id,
    dependencies: task.depends_on,
    previous_status: oldStatus
  });
  
  console.log(`✅ ${task.task_id} 已激活（依赖完成）`);
}

/**
 * 主程序
 */
function main() {
  console.log('🔍 检查 queued 任务...');
  
  // 列出所有任务文件
  const taskFiles = fs.readdirSync(TASKS_DIR)
    .filter(f => f.endsWith('.json'))
    .map(f => f.replace('.json', ''));
  
  let activatedCount = 0;
  
  for (const taskId of taskFiles) {
    const task = readTask(taskId);
    if (!task) continue;
    
    // 只处理 queued 状态的任务
    if (task.status !== 'queued') {
      continue;
    }
    
    // 检查依赖
    const dependsOn = task.depends_on || [];
    if (dependsOn.length === 0) {
      // 没有依赖，直接激活
      activateTask(task);
      activatedCount++;
      continue;
    }
    
    // 检查所有依赖是否完成
    if (areDependenciesCompleted(dependsOn)) {
      activateTask(task);
      activatedCount++;
    } else {
      const pendingDeps = dependsOn.filter(depId => {
        const depTask = readTask(depId);
        return !depTask || (depTask.status !== 'completed' && depTask.status !== 'packaged');
      });
      console.log(`⏳ ${task.task_id} 等待依赖：${pendingDeps.join(', ')}`);
    }
  }
  
  console.log('');
  console.log(`📊 检查完成：${activatedCount} 个任务已激活`);
  
  if (activatedCount === 0) {
    console.log('✅ 没有需要激活的任务');
  }
}

main();
