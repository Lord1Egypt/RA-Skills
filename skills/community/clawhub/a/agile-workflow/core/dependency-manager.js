#!/usr/bin/env node
/**
 * 依赖关系管理器 v7.17
 * 
 * 核心功能:
 * 1. 定义任务依赖关系
 * 2. 检查依赖是否完成
 * 3. 获取可执行任务
 */

const fs = require('fs');
const path = require('path');

class DependencyManager {
  constructor(tracker) {
    this.tracker = tracker;
    this.dependencies = new Map();
    this.loadDependencies();
  }

  /**
   * 加载依赖配置
   */
  loadDependencies() {
    const configPath = path.join(this.tracker.projectDir, '.task-dependencies.json');
    
    if (fs.existsSync(configPath)) {
      const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
      
      for (const [taskId, deps] of Object.entries(config)) {
        this.addDependency(taskId, deps);
      }
      
      console.log(`✅ 加载 ${Object.keys(config).length} 个任务依赖`);
    } else {
      console.warn(`⚠️ 依赖配置文件不存在：${configPath}`);
    }
  }

  /**
   * 重新加载依赖配置（用于动态更新）
   */
  reloadDependencies() {
    this.dependencies.clear();
    this.loadDependencies();
    console.log('🔄 依赖配置已重新加载');
  }

  /**
   * 添加任务依赖
   */
  addDependency(taskId, dependsOn) {
    if (!this.dependencies.has(taskId)) {
      this.dependencies.set(taskId, []);
    }
    
    const deps = Array.isArray(dependsOn) ? dependsOn : [dependsOn];
    this.dependencies.get(taskId).push(...deps);
  }

  /**
   * 检查依赖是否完成
   */
  areDependenciesMet(taskId) {
    const deps = this.dependencies.get(taskId) || [];
    
    if (deps.length === 0) {
      return true;  // 无依赖，可直接执行
    }
    
    return deps.every(depId => {
      const state = this.tracker.getTaskStatus(depId);
      return state && state.status === 'completed';
    });
  }

  /**
   * 获取未完成的依赖
   */
  getUnmetDependencies(taskId) {
    const deps = this.dependencies.get(taskId) || [];
    const unmet = [];
    
    for (const depId of deps) {
      const state = this.tracker.getTaskStatus(depId);
      if (!state || state.status !== 'completed') {
        unmet.push({
          taskId: depId,
          status: state ? state.status : 'unknown'
        });
      }
    }
    
    return unmet;
  }

  /**
   * 获取可执行任务
   */
  getExecutableTasks() {
    const pending = this.tracker.getPendingTasks();
    
    return pending.filter(task => {
      const canExecute = this.areDependenciesMet(task.id);
      
      if (!canExecute) {
        const unmet = this.getUnmetDependencies(task.id);
        task.blockedBy = unmet;
      }
      
      return canExecute;
    });
  }

  /**
   * 获取任务依赖链
   */
  getDependencyChain(taskId, visited = new Set()) {
    if (visited.has(taskId)) {
      return [];
    }
    
    visited.add(taskId);
    const deps = this.dependencies.get(taskId) || [];
    const chain = [];
    
    for (const depId of deps) {
      chain.push(depId);
      chain.push(...this.getDependencyChain(depId, visited));
    }
    
    return chain;
  }

  /**
   * 保存依赖配置
   */
  saveDependencies(configPath) {
    const config = {};
    
    for (const [taskId, deps] of this.dependencies.entries()) {
      config[taskId] = deps;
    }
    
    fs.writeFileSync(configPath, JSON.stringify(config, null, 2), 'utf8');
  }
}

module.exports = DependencyManager;

// CLI 入口
if (require.main === module) {
  const args = process.argv.slice(2);
  const [projectDir, command, taskId] = args;
  
  if (!projectDir || !command) {
    console.log('用法：node dependency-manager.js <项目目录> <命令> [任务 ID]');
    console.log('命令：check, chain, executable');
    process.exit(1);
  }
  
  const TaskStateTracker = require('./task-state-tracker');
  const tracker = new TaskStateTracker(projectDir);
  const deps = new DependencyManager(tracker);
  
  switch (command) {
    case 'check':
      if (taskId) {
        const met = deps.areDependenciesMet(taskId);
        console.log(`任务 ${taskId} 依赖：${met ? '✅ 已满足' : '❌ 未满足'}`);
        
        if (!met) {
          const unmet = deps.getUnmetDependencies(taskId);
          console.log('未完成的依赖:');
          unmet.forEach(u => console.log(`  - ${u.taskId} (${u.status})`));
        }
      }
      break;
    
    case 'chain':
      if (taskId) {
        const chain = deps.getDependencyChain(taskId);
        console.log(`任务 ${taskId} 的依赖链:`);
        chain.forEach(t => console.log(`  - ${t}`));
      }
      break;
    
    case 'executable':
      const executable = deps.getExecutableTasks();
      console.log('可执行任务:');
      executable.forEach(t => console.log(`  - ${t.id}`));
      
      if (executable.length === 0) {
        console.log('（无）');
      }
      break;
    
    default:
      console.log(`未知命令：${command}`);
  }
}
