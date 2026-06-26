#!/usr/bin/env node
const { globalProcessManager } = require('./global-process-manager.js');
/**
 * 失败任务自动修复器 v1.0
 * 
 * 核心功能：
 * 1. 失败分析：识别细纲问题/正文问题/OOM/未知错误
 * 2. 智能路由：路由到 novel_architect 或 novel_writer
 * 3. 队列管理：空队列立即执行，否则插入队首
 * 4. 脏数据清理：清理残留 running 状态
 * 
 * 第一性原理：
 * - 失败是常态，自动修复是关键
 * - 不同失败类型需要不同修复策略
 * - 任务队列应该智能调度
 */

const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

class FailureHandler {
  constructor(projectDir) {
    this.projectDir = projectDir;
    this.stateFile = path.join(projectDir, '.task-state.json');
    this.depsFile = path.join(projectDir, '.task-dependencies.json');
    
    // 任务队列（内存中）
    this.taskQueue = [];
    this.isProcessing = false;
  }
  
  /**
   * 加载任务状态
   */
  loadState() {
    return JSON.parse(fs.readFileSync(this.stateFile, 'utf-8'));
  }
  
  /**
   * 保存任务状态
   */
  saveState(state) {
    fs.writeFileSync(this.stateFile, JSON.stringify(state, null, 2));
  }
  
  /**
   * 分析失败原因
   */
  analyzeFailure(taskId, taskInfo) {
    const errorCode = taskInfo.error?.match(/退出码：(\d+|null)/)?.[1];
    
    console.log(`🔍 分析失败：${taskId} (错误码：${errorCode})`);
    
    // 1. OOM 被杀（137）
    if (errorCode === '137') {
      console.log(`   类型：OOM 被杀 → 直接重试`);
      return { type: 'oom', action: 'retry', taskId };
    }
    
    // 2. 未知错误（null）
    if (errorCode === 'null' || !errorCode) {
      console.log(`   类型：未知错误 → 直接重试`);
      return { type: 'unknown', action: 'retry', taskId };
    }
    
    // 3. 审查失败（需要分析是细纲还是正文问题）
    if (taskId.includes('review')) {
      const chapterMatch = taskId.match(/chapter-(\d+)/);
      if (!chapterMatch) {
        console.log(`   类型：无法解析章节 → 直接重试`);
        return { type: 'unknown', action: 'retry', taskId };
      }
      
      const chapterNum = chapterMatch[1];
      const outlineTaskId = `chapter-${chapterNum}-outline`;
      const writingTaskId = `chapter-${chapterNum}-writing`;
      
      const state = this.loadState();
      
      // 检查细纲和正文状态
      const outlineStatus = state[outlineTaskId]?.status;
      const writingStatus = state[writingTaskId]?.status;
      
      console.log(`   细纲状态：${outlineStatus}`);
      console.log(`   正文状态：${writingStatus}`);
      
      // 如果细纲是 failed 或审查提到细纲问题 → 细纲修复
      if (outlineStatus === 'failed' || taskInfo.error?.includes('细纲')) {
        console.log(`   类型：细纲问题 → 路由到 novel_architect`);
        return { 
          type: 'outline', 
          action: 'fix', 
          agent: 'novel_architect',
          taskId: outlineTaskId,
          description: `修复第${chapterNum}章细纲（审查发现问题）`
        };
      }
      
      // 默认正文问题
      console.log(`   类型：正文问题 → 路由到 novel_writer`);
      return { 
        type: 'writing', 
        action: 'fix', 
        agent: 'novel_writer',
        taskId: writingTaskId,
        description: `修复第${chapterNum}章正文（审查发现问题）`
      };
    }
    
    // 4. 其他任务失败
    console.log(`   类型：其他失败 → 直接重试`);
    return { type: 'other', action: 'retry', taskId };
  }
  
  /**
   * 路由到 Agent
   */
  async routeToAgent(failure) {
    console.log(`📍 路由任务：${failure.taskId} → ${failure.agent || 'retry'}`);
    
    if (failure.action === 'retry') {
      // 直接重试：重置状态为 pending
      const state = this.loadState();
      if (state[failure.taskId]) {
        state[failure.taskId].status = 'pending';
        delete state[failure.taskId].error;
        state[failure.taskId].updatedAt = new Date().toISOString();
        this.saveState(state);
        console.log(`✅ 已重置 ${failure.taskId} 为 pending`);
      }
      return;
    }
    
    if (failure.action === 'fix') {
      // 修复任务：插入到 agent 队列
      this.insertToQueue(failure);
      return;
    }
  }
  
  /**
   * 插入任务到队列
   */
  insertToQueue(failure) {
    console.log(`📋 插入任务到队列：${failure.taskId}`);
    
    // 检查队列中是否已存在
    const exists = this.taskQueue.some(t => t.taskId === failure.taskId);
    if (exists) {
      console.log(`⚠️ 任务已在队列中，跳过`);
      return;
    }
    
    // 插入队首（高优先级）
    this.taskQueue.unshift({
      ...failure,
      priority: 'high',
      insertedAt: Date.now()
    });
    
    console.log(`✅ 已插入队首，当前队列长度：${this.taskQueue.length}`);
    
    // 如果当前没有处理任务，立即开始
    if (!this.isProcessing) {
      this.processQueue();
    }
  }
  
  /**
   * 处理任务队列
   */
  async processQueue() {
    if (this.isProcessing || this.taskQueue.length === 0) {
      return;
    }
    
    this.isProcessing = true;
    
    while (this.taskQueue.length > 0) {
      const task = this.taskQueue.shift();
      
      console.log(`🚀 执行队列任务：${task.taskId}`);
      
      try {
        await this.executeTask(task);
      } catch (error) {
        console.error(`❌ 任务失败：${task.taskId}`, error.message);
        // 失败后重新插入队尾（最多重试 3 次）
        if (!task.retryCount) task.retryCount = 0;
        task.retryCount++;
        
        if (task.retryCount < 3) {
          this.taskQueue.push(task);
          console.log(`🔄 已重新插入队尾，重试次数：${task.retryCount}`);
        }
      }
    }
    
    this.isProcessing = false;
  }
  
  /**
   * 执行单个任务
   */
  executeTask(task) {
    return new Promise((resolve, reject) => {
      const cmd = `cd /home/ubutu/.openclaw/workspace && /home/ubutu/.npm-global/bin/openclaw agent --local \
        --agent ${task.agent} \
        --thinking minimal \
        -m "${task.description}（请简洁回答，不超过 4000 tokens）"`;
      
      console.log(`📝 执行命令：${task.agent} - ${task.description}`);
      
      // 🔒 全局进程数检查
      if (!globalProcessManager.canSpawnNewProcess()) {
        console.log('⚠️ 全局进程数已达上限，跳过本次修复');
        return;
      }
      
      const child = exec(cmd, {
        timeout: 30 * 60 * 1000
      });
      
      child.stdout.on('data', (data) => {
        console.log(`[${task.taskId}] ${data.toString().trim()}`);
      });
      
      child.stderr.on('data', (data) => {
        console.error(`[${task.taskId}] ${data.toString().trim()}`);
      });
      
      child.on('close', (code) => {
        if (code === 0) {
          console.log(`✅ 任务完成：${task.taskId}`);
          resolve();
        } else {
          reject(new Error(`退出码：${code}`));
        }
      });
    });
  }
  
  /**
   * 清理脏数据
   */
  cleanupDirtyData() {
    console.log('🧹 清理脏数据...');
    
    const state = this.loadState();
    let cleaned = 0;
    
    for (const [taskId, taskInfo] of Object.entries(state)) {
      // 清理 running 但无 startedAt 的任务
      if (taskInfo.status === 'running' && !taskInfo.startedAt) {
        console.log(`  清理脏数据：${taskId} (running 但无 startedAt)`);
        state[taskId].status = 'pending';
        state[taskId].updatedAt = new Date().toISOString();
        cleaned++;
      }
      
      // 清理 running 超过 1 小时的任务（可能是卡住）
      if (taskInfo.status === 'running' && taskInfo.startedAt) {
        const startTime = new Date(taskInfo.startedAt).getTime();
        const now = Date.now();
        const runningTime = now - startTime;
        
        if (runningTime > 60 * 60 * 1000) { // 1 小时
          console.log(`  清理超时任务：${taskId} (运行 ${Math.round(runningTime/60000)} 分钟)`);
          state[taskId].status = 'pending';
          state[taskId].updatedAt = new Date().toISOString();
          cleaned++;
        }
      }
    }
    
    this.saveState(state);
    console.log(`✅ 清理完成，共清理 ${cleaned} 个任务`);
    
    return cleaned;
  }
  
  /**
   * 处理所有失败任务
   */
  async processAllFailures() {
    console.log('🔍 扫描失败任务...');
    
    const state = this.loadState();
    const failures = [];
    
    for (const [taskId, taskInfo] of Object.entries(state)) {
      if (taskInfo.status === 'failed') {
        console.log(`发现失败任务：${taskId}`);
        const analysis = this.analyzeFailure(taskId, taskInfo);
        failures.push(analysis);
      }
    }
    
    console.log(`共发现 ${failures.length} 个失败任务`);
    
    // 处理每个失败
    for (const failure of failures) {
      await this.routeToAgent(failure);
    }
    
    // 处理队列
    if (this.taskQueue.length > 0) {
      await this.processQueue();
    }
  }
}

module.exports = FailureHandler;

// CLI 入口
if (require.main === module) {
  const args = process.argv.slice(2);
  const [projectDir, command] = args;
  
  if (!projectDir || !command) {
    console.log('用法：node failure-handler.js <项目目录> <命令>');
    console.log('命令：cleanup, process, scan');
    process.exit(1);
  }
  
  const handler = new FailureHandler(projectDir);
  
  switch (command) {
    case 'cleanup':
      handler.cleanupDirtyData();
      break;
    
    case 'process':
      handler.processAllFailures().catch(console.error);
      break;
    
    case 'scan':
      const state = handler.loadState();
      const failures = Object.entries(state).filter(([k, v]) => v.status === 'failed');
      console.log(`发现 ${failures.length} 个失败任务:`);
      failures.forEach(([k, v]) => console.log(`  - ${k}: ${v.error || '未知'}`));
      break;
    
    default:
      console.log(`未知命令：${command}`);
  }
}
