#!/usr/bin/env node
const { globalProcessManager } = require('./global-process-manager.js');
/**
 * 任务调度器 v7.17
 * 
 * 核心功能:
 * 1. 检测任务完成
   2. 自动触发后续任务
 * 3. 管理任务执行队列
 */

const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');
const TokenCounter = require('./token-counter');
const AutoChunker = require('./auto-chunker');
const AgentProcessPool = require('./agent-process-pool');
const SelfHealingMonitor = require('./self-healing-monitor');
const LogMonitor = require('./log-monitor'); // ✅ 实时日志监控器
const TaskReportMonitor = require('./task-report-monitor'); // ✅ 任务汇报监控器

class TaskScheduler {
  constructor(projectDir) {
    this.projectDir = projectDir;
    this.tracker = new (require('./task-state-tracker'))(projectDir);
    this.deps = new (require('./dependency-manager'))(this.tracker);
    this.runningTasks = new Set();
    this.counter = new TokenCounter();
    // ✅ 从 openclaw.json 读取模型配置（qwen3.5-plus maxTokens=65536）
    this.chunker = new AutoChunker({ maxTokenPerChunk: 60000 });
    this.maxTokens = 60000;  // ✅ 符合 qwen3.5-plus 输出限制（原 7000 过小）
    // 🚀 按 Agent 分组并发控制（非全局）
    // novel_architect: 串行, novel_writer: 串行, novel_editor: 并发=2
    this.maxConcurrency = 2;  // 用于审查任务的最大并发（实际由进程池控制）
    
    // 🚀 进程池：按 Agent 分组的并发控制器
    this.processPool = new AgentProcessPool({
      idleTimeout: 300000,  // 5 分钟空闲超时
      maxTasksPerProcess: 10,  // 单进程最多执行 10 个任务
      workspace: '/home/ubutu/.openclaw/workspace',
      projectDir: this.projectDir,  // 🔒 用于同步任务状态
      reviewConcurrency: 2  // 审查任务并发
    });
    
    // 🛡️ 自愈监控器：兜底检查（实时问题由 log-monitor.js 处理）
    this.selfHealing = new SelfHealingMonitor(this.projectDir, {
      checkInterval: 300000,        // 5 分钟检查（兜底）
      progressStuckThreshold: 600000, // 10 分钟无进展
      runningTaskThreshold: 1800000,  // 30 分钟运行中
      sessionLockThreshold: 300000    // 5 分钟锁文件（与 log-monitor 一致）
    });
    
    // 📊 实时日志监控器：秒级响应错误
    this.logMonitor = new LogMonitor({
      projectDir: this.projectDir,
      checkInterval: 5000  // 5 秒检查
    });
    
    // 📋 任务汇报监控器：定期发送进度报告
    this.taskReport = new TaskReportMonitor({
      projectDir: this.projectDir,
      reportInterval: 300000  // 5 分钟汇报
    });
    
    // 🚀 并发控制（仅用于串行任务的兜底保护）
    // novel_architect/novel_writer: 串行 (maxSerialTasks=1)
    // novel_editor: 并发=2 (由进程池控制)
    this.maxSerialTasks = 1;  // 串行任务最大并发（兜底保护）
  }

  /**
   * 检查并触发任务（按 Agent 分组并发控制）
   */
  async checkAndTrigger() {
    console.log('🔍 调度器检查中...');
    
    // ⚠️ 注意：不在这里清理会话锁，避免中断正在执行的任务
    // 会话锁由自愈监控器统一清理（带 Gateway 进程检查）
    
    const executable = this.deps.getExecutableTasks();
    const runningCount = this.runningTasks.size;
    
    if (executable.length === 0) {
      console.log('✅ 无待执行任务');
      return;
    }
    
    console.log(`🚀 发现 ${executable.length} 个可执行任务，当前运行 ${runningCount}/${this.maxSerialTasks} (串行兜底)`);
    
    // 🔒 并发限制：仅用于串行任务的兜底保护
    // 实际并发由进程池的按 Agent 分组控制（novel_editor=2，其他=1）
    let triggered = 0;
    for (const task of executable) {
      // 检查是否已在运行
      if (this.isRunning(task.id)) {
        console.log(`⏳ ${task.id} 已在运行`);
        continue;
      }
      
      // 检查串行任务兜底上限（novel_architect/novel_writer 串行）
      const isReviewTask = task.id.includes('review');
      const maxConcurrency = isReviewTask ? 2 : this.maxSerialTasks;
      
      if (runningCount >= maxConcurrency) {
        console.log(`⚠️ 已达 ${isReviewTask ? '审查' : '串行'} 并发上限 (${maxConcurrency})，等待下一轮`);
        break;
      }
      
      // 触发任务
      await this.triggerTask(task);
      triggered++;
    }
    
    console.log(`📊 本轮触发 ${triggered} 个任务`);
  }

  /**
   * 检查任务是否在运行
   */
  isRunning(taskId) {
    return this.runningTasks.has(taskId);
  }

  // ⚠️ 注意：会话锁清理由自愈监控器统一处理
  // 调度器不主动清理，避免中断正在执行的任务造成数据污染

  /**
   * 触发任务（使用进程池，带超时保护）
   */
  async triggerTask(task) {
    console.log(`🚀 触发任务：${task.id}`);
    
    // 更新状态为运行中
    this.tracker.updateTask(task.id, 'running');
    this.runningTasks.add(task.id);
    
    // 🔒 容错机制：任务超时保护（10 分钟）
    const timeoutId = setTimeout(() => {
      console.log(`⚠️ 任务 ${task.id} 执行超时（>10 分钟），强制重置...`);
      // 🔒 清理进程池 slot
      this.processPool.runningTasks.delete(task.id);
      this.tracker.updateTask(task.id, 'pending', { error: '任务执行超时' });
      this.runningTasks.delete(task.id);
    }, 600000); // 10 分钟超时
    
    // 启动 Agent 执行（使用进程池）
    try {
      await this.startAgentWithPool(task);
      clearTimeout(timeoutId); // 任务完成，清除超时
    } catch (error) {
      clearTimeout(timeoutId);
      console.error(`❌ 任务 ${task.id} 执行失败:`, error.message);
      // 🔒 清理进程池 slot
      this.processPool.runningTasks.delete(task.id);
      this.tracker.updateTask(task.id, 'failed', { error: error.message });
    } finally {
      this.runningTasks.delete(task.id);
    }
  }

  /**
   * 启动 Agent（使用进程池，带唯一 ID 追踪）
   */
  async startAgentWithPool(task) {
    const description = task.description || `执行 ${task.id}`;
    
    // ✅ 添加项目上下文 (修复输出路径问题)
    const projectContext = `\n\n【项目上下文】
- 项目目录：${this.projectDir}
- 任务 ID: ${task.id}
- 请根据任务类型将输出保存到正确目录：
  - 章节细纲：${this.projectDir}/04_章节细纲/第 N 章_标题.md
  - 正文创作：${this.projectDir}/05_正文创作/第 N 章_标题.md`;
    
    const fullDescription = description + projectContext;
    
    // 使用进程池执行
    const result = await this.processPool.executeTask({
      agent: task.agent || 'novel_architect',
      description: fullDescription,
      taskId: task.id
    });
    
    console.log(`📊 进程 ID: ${result.processId}`);
    return result;
  }
  
  /**
   * 启动 Agent（带 Token 管理）- 保留向后兼容
   */
  async startAgent(task) {
    const description = task.description || `执行 ${task.id}`;
    const messages = [{ role: 'user', content: description }];
    
    // ✅ 检查 token 数
    const status = this.counter.isExceedLimit(messages, 100000);
    
    if (status.exceed) {
      console.error(`⚠️ Token 超限 ${status.usage}%，启用自动分片`);
      return await this.startAgentChunked(task);
    }
    
    // 正常执行
    return await this.startAgentNormal(task);
  }

  /**
   * 启动 Agent（正常模式，带输出限制）
   */
  startAgentNormal(task) {
    return new Promise((resolve, reject) => {
      const agent = task.agent || 'novel_architect';
      const description = task.description || `执行 ${task.id}`;
      
      console.log(`🤖 启动 Agent: ${agent}`);
      console.log(`📝 任务：${description}`);
      
      // ✅ 添加输出长度限制（通过系统提示）
      const cmd = `cd /home/ubutu/.openclaw/workspace && /home/ubutu/.npm-global/bin/openclaw agent --local \
        --agent ${agent} \
        --thinking minimal \
        -m "${description}（请简洁回答，不超过 4000 tokens）"`;
      
      // 🔒 全局进程数检查
      if (!globalProcessManager.canSpawnNewProcess()) {
        console.log('⚠️ 全局进程数已达上限，跳过本次执行');
        return;
      }
      
      const child = exec(cmd, {
        timeout: 30 * 60 * 1000  // 30 分钟超时
      });
      
      child.stdout.on('data', (data) => {
        console.log(`[${task.id}] ${data}`);
      });
      
      child.stderr.on('data', (data) => {
        console.error(`[${task.id}] ${data}`);
      });
      
      child.on('close', (code) => {
        if (code === 0) {
          console.log(`✅ ${task.id} 完成`);
          this.tracker.updateTask(task.id, 'completed');
          resolve();
        } else {
          console.error(`❌ ${task.id} 失败 (退出码：${code})`);
          reject(new Error(`任务失败，退出码：${code}`));
        }
      });
      
      child.on('error', (error) => {
        reject(error);
      });
    });
  }

  /**
   * 启动 Agent（分片模式，用于 Token 超限）
   */
  async startAgentChunked(task) {
    const description = task.description || `执行 ${task.id}`;
    const messages = [{ role: 'user', content: description }];
    
    // 自动分片
    const chunks = this.chunker.chunkMessages(messages);
    const results = [];
    
    for (let i = 0; i < chunks.length; i++) {
      console.log(`📦 处理分片 ${i + 1}/${chunks.length}`);
      const chunkDesc = chunks[i][0].content;
      
      const result = await this.startAgentNormal({
        ...task,
        description: chunkDesc
      });
      results.push(result);
    }
    
    return this.chunker.mergeResults(results);
  }

  /**
   * 启动持续调度（守护模式，带自愈监控 + 实时日志监控 + 任务汇报）
   */
  startDaemon(checkInterval = 60000) {
    console.log(`🔒 调度器守护模式启动（检查间隔：${checkInterval}ms）`);
    console.log(`📊 进程池配置：所有任务串行执行（并发=1）`);
    console.log(`🛡️ 自愈监控：已启用（5 分钟检查，10 分钟进度停滞阈值）`);
    console.log(`📊 实时日志监控：已启用（5 秒检查，秒级响应）`);
    console.log(`📋 任务汇报：已启用（5 分钟汇报）`);
    
    // 启动自愈监控器
    this.selfHealing.startDaemon();
    
    // 启动实时日志监控器
    this.logMonitor.startDaemon();
    
    // 启动任务汇报监控器
    this.taskReport.startDaemon();
    
    // 立即检查一次
    this.checkAndTrigger().catch(console.error);
    
    // 定期检查
    const intervalId = setInterval(() => {
      this.checkAndTrigger().catch(console.error);
    }, checkInterval);
    
    // 进程池状态监控（每 30 秒）
    const monitorId = setInterval(() => {
      const status = this.processPool.getStatus();
      console.log(`📊 进程池状态：活跃=${status.stats.currentActive}, 已创建=${status.stats.totalSpawned}, 已完成=${status.stats.totalCompleted}`);
    }, 30000);
    
    // 优雅关闭处理
    process.on('SIGINT', async () => {
      console.log('\n🛑 收到退出信号，清理进程池...');
      clearInterval(intervalId);
      clearInterval(monitorId);
      await this.processPool.cleanup();
      process.exit(0);
    });
    
    process.on('SIGTERM', async () => {
      console.log('\n🛑 收到终止信号，清理进程池...');
      clearInterval(intervalId);
      clearInterval(monitorId);
      await this.processPool.cleanup();
      process.exit(0);
    });
  }

  /**
   * 获取调度状态
   */
  getStatus() {
    const summary = this.tracker.getProgressSummary();
    
    return {
      ...summary,
      running: Array.from(this.runningTasks),
      executable: this.deps.getExecutableTasks().map(t => t.id)
    };
  }
}

module.exports = TaskScheduler;

// CLI 入口
if (require.main === module) {
  const args = process.argv.slice(2);
  const [projectDir, command] = args;
  
  if (!projectDir || !command) {
    console.log('用法：node task-scheduler.js <项目目录> <命令>');
    console.log('命令：check, daemon, status');
    process.exit(1);
  }
  
  // 🔒 单实例锁机制（防止多实例竞争）
  const pidFile = path.join(projectDir, '.scheduler.pid');
  const fs = require('fs');
  
  if (command === 'daemon') {
    if (fs.existsSync(pidFile)) {
      const oldPid = parseInt(fs.readFileSync(pidFile, 'utf8'));
      try {
        process.kill(oldPid, 0);  // 检查进程是否存在
        console.log(`❌ 调度器已在运行 (PID: ${oldPid})，退出当前实例`);
        process.exit(1);
      } catch (e) {
        console.log(`🧹 清理旧 PID 文件 (进程 ${oldPid} 已不存在)`);
        fs.unlinkSync(pidFile);
      }
    }
    
    // 写入当前 PID
    fs.writeFileSync(pidFile, process.pid.toString());
    console.log(`🔒 单实例锁已获取 (PID: ${process.pid})`);
    
    // 退出时清理 PID 文件
    process.on('exit', () => {
      try { fs.unlinkSync(pidFile); } catch (e) {}
    });
    process.on('SIGINT', () => {
      try { fs.unlinkSync(pidFile); } catch (e) {}
      process.exit(0);
    });
    process.on('SIGTERM', () => {
      try { fs.unlinkSync(pidFile); } catch (e) {}
      process.exit(0);
    });
  }
  
  const scheduler = new TaskScheduler(projectDir);
  
  switch (command) {
    case 'check':
      scheduler.checkAndTrigger().catch(console.error);
      break;
    
    case 'daemon':
      scheduler.startDaemon();
      console.log('守护模式运行中... (Ctrl+C 停止)');
      break;
    
    case 'status':
      const status = scheduler.getStatus();
      console.log(JSON.stringify(status, null, 2));
      break;
    
    default:
      console.log(`未知命令：${command}`);
  }
}
