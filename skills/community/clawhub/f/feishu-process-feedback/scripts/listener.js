#!/usr/bin/env node

/**
 * 飞书消息监听器 - 增强版
 * 后台运行，监听飞书消息并创建处理进程
 * 
 * 功能：
 * - 自动重试机制
 * - 错误容错处理
 * - 状态持久化
 * - 进程管理
 * 
 * 用法：node listener.js
 */

const { exec, spawn } = require('child_process');
const { promisify } = require('util');
const execAsync = promisify(exec);
const path = require('path');
const fs = require('fs');

// ============ 配置 ============
const CONFIG = {
  // 轮询间隔（毫秒）
  pollInterval: parseInt(process.env.FEISHU_POLL_INTERVAL) || 5000,
  
  // 最大重试次数
  maxRetries: parseInt(process.env.FEISHU_MAX_RETRIES) || 3,
  
  // 重试延迟（毫秒）
  retryDelay: parseInt(process.env.FEISHU_RETRY_DELAY) || 1000,
  
  // 是否启用详细日志
  verbose: process.env.FEISHU_VERBOSE === 'true',
  
  // 状态文件路径
  stateFile: path.join(__dirname, '..', '.listener_state.json'),
  
  // 日志文件路径
  logFile: path.join(__dirname, '..', '.listener.log'),
  
  // 进程超时时间（毫秒）
  processTimeout: parseInt(process.env.FEISHU_PROCESS_TIMEOUT) || 300000, // 5 分钟
  
  // 最大并发进程数
  maxConcurrent: parseInt(process.env.FEISHU_MAX_CONCURRENT) || 5
};

const SCRIPT_DIR = __dirname;

class FeishuListener {
  constructor() {
    this.activeProcesses = new Map();
    this.taskCounter = 0;
    this.lastMessageId = null;
    this.retryCount = 0;
    this.isRunning = true;
    this.startTime = Date.now();
  }

  /**
   * 日志记录
   */
  log(level, message, data = null) {
    const timestamp = new Date().toISOString();
    const logEntry = {
      timestamp,
      level,
      message,
      ...(data && { data })
    };
    
    const logLine = `[${timestamp}] [${level.toUpperCase()}] ${message}${data ? ' ' + JSON.stringify(data) : ''}\n`;
    
    // 控制台输出
    if (CONFIG.verbose || level !== 'debug') {
      console.log(logLine.trim());
    }
    
    // 写入日志文件
    try {
      fs.appendFileSync(CONFIG.logFile, logLine);
    } catch (error) {
      // 忽略日志写入错误
    }
  }

  /**
   * 加载状态
   */
  loadState() {
    try {
      if (fs.existsSync(CONFIG.stateFile)) {
        const state = JSON.parse(fs.readFileSync(CONFIG.stateFile, 'utf8'));
        this.lastMessageId = state.lastMessageId;
        this.taskCounter = state.taskCounter || 0;
        this.log('info', '加载状态成功', { lastMessageId: this.lastMessageId, taskCounter: this.taskCounter });
        return true;
      }
    } catch (error) {
      this.log('warn', '加载状态失败', { error: error.message });
    }
    this.log('info', '无历史状态，从头开始');
    return false;
  }

  /**
   * 保存状态
   */
  saveState() {
    try {
      const state = {
        lastMessageId: this.lastMessageId,
        taskCounter: this.taskCounter,
        updatedAt: Date.now(),
        uptime: Date.now() - this.startTime
      };
      fs.writeFileSync(CONFIG.stateFile, JSON.stringify(state, null, 2));
      this.log('debug', '状态已保存');
      return true;
    } catch (error) {
      this.log('error', '保存状态失败', { error: error.message });
      return false;
    }
  }

  /**
   * 发送飞书消息（带重试）
   */
  async sendFeedback(message, retryCount = 0) {
    try {
      const escaped = message.replace(/"/g, '\\"').replace(/\n/g, '\\n');
      const cmd = `openclaw message send --channel feishu --message "${escaped}"`;
      await execAsync(cmd);
      this.log('info', '发送反馈', { message: message.substring(0, 50) });
      return true;
    } catch (error) {
      if (retryCount < CONFIG.maxRetries) {
        this.log('warn', `发送失败，重试 ${retryCount + 1}/${CONFIG.maxRetries}`, { error: error.message });
        await this.sleep(CONFIG.retryDelay * (retryCount + 1));
        return this.sendFeedback(message, retryCount + 1);
      }
      this.log('error', '发送反馈失败（已达最大重试次数）', { error: error.message });
      return false;
    }
  }

  /**
   * 延迟函数
   */
  sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  /**
   * 获取最新飞书消息
   * TODO: 集成飞书 API 或 webhook
   */
  async getLatestMessage() {
    try {
      // 简化实现：实际应调用飞书 API
      // const response = await fetch('https://open.feishu.cn/open-apis/im/v1/messages', {...});
      this.log('debug', '检查新消息');
      return null;
    } catch (error) {
      this.log('error', '获取消息失败', { error: error.message });
      return null;
    }
  }

  /**
   * 解析任务消息
   */
  parseTaskMessage(content) {
    // 简单的任务识别逻辑
    const keywords = ['帮我', '处理', '创建', '生成', '分析', '计算', '查询'];
    const isTask = keywords.some(keyword => content.includes(keyword));
    
    if (!isTask) {
      this.log('debug', '消息不是任务', { content: content.substring(0, 50) });
      return null;
    }
    
    return {
      type: 'task',
      content: content.trim(),
      timestamp: Date.now()
    };
  }

  /**
   * 创建任务处理进程
   */
  async createTaskProcess(taskText, messageId) {
    // 检查并发限制
    if (this.activeProcesses.size >= CONFIG.maxConcurrent) {
      this.log('warn', '达到最大并发进程数，等待中', { 
        active: this.activeProcesses.size, 
        max: CONFIG.maxConcurrent 
      });
      await this.sendFeedback('⚠️ 当前任务较多，正在排队处理...');
      
      // 等待有空闲进程
      while (this.activeProcesses.size >= CONFIG.maxConcurrent) {
        await this.sleep(1000);
      }
    }
    
    const taskId = ++this.taskCounter;
    
    this.log('info', '创建任务进程', { 
      taskId, 
      messageId, 
      taskPreview: taskText.substring(0, 80) 
    });
    
    const scriptPath = path.join(SCRIPT_DIR, 'process_task.js');
    const args = [scriptPath, taskText, taskId.toString(), messageId || 'unknown'];
    
    // 创建独立进程
    const child = spawn('node', args, {
      detached: true,
      stdio: ['ignore', 'inherit', 'inherit'],
      env: { ...process.env, FEISHU_TASK_ID: taskId.toString() }
    });
    
    const processInfo = {
      pid: child.pid,
      createdAt: Date.now(),
      messageId,
      taskText,
      status: 'running',
      timeout: null
    };
    
    // 设置超时
    processInfo.timeout = setTimeout(() => {
      this.log('warn', '任务超时，强制终止', { taskId, pid: child.pid });
      child.kill('SIGTERM');
      this.sendFeedback(`⚠️ 任务 #${taskId} 处理超时，已终止`);
    }, CONFIG.processTimeout);
    
    this.activeProcesses.set(taskId, processInfo);
    
    child.on('exit', (code, signal) => {
      clearTimeout(processInfo.timeout);
      this.log('info', '任务进程退出', { taskId, code, signal });
      this.activeProcesses.delete(taskId);
      this.saveState();
    });
    
    child.on('error', (error) => {
      this.log('error', '任务进程错误', { taskId, error: error.message });
      clearTimeout(processInfo.timeout);
      this.activeProcesses.delete(taskId);
    });
    
    // 发送开始反馈
    await this.sendFeedback(`📋 任务收到，开始处理...\n任务 ID: #${taskId}\n当前队列：${this.activeProcesses.size} 个任务`);
    
    return taskId;
  }

  /**
   * 检查并处理新消息
   */
  async checkNewMessages() {
    if (!this.isRunning) return;
    
    try {
      const message = await this.getLatestMessage();
      
      if (!message || message.id === this.lastMessageId) {
        return; // 无新消息
      }
      
      this.lastMessageId = message.id;
      
      const task = this.parseTaskMessage(message.content);
      if (task) {
        await this.createTaskProcess(task.content, message.id);
      }
      
      this.saveState();
    } catch (error) {
      this.log('error', '检查消息失败', { error: error.message });
      this.retryCount++;
      
      if (this.retryCount >= CONFIG.maxRetries) {
        this.log('error', '达到最大重试次数，暂停检查');
        await this.sleep(30000); // 暂停 30 秒
        this.retryCount = 0;
      }
    }
  }

  /**
   * 清理超时进程
   */
  cleanupStaleProcesses() {
    const now = Date.now();
    for (const [taskId, info] of this.activeProcesses.entries()) {
      const age = now - info.createdAt;
      if (age > CONFIG.processTimeout) {
        this.log('warn', '检测到超时进程', { taskId, age });
        // 进程应该已经由超时处理器终止
      }
    }
  }

  /**
   * 显示状态
   */
  showStatus() {
    const uptime = Math.floor((Date.now() - this.startTime) / 1000);
    const hours = Math.floor(uptime / 3600);
    const minutes = Math.floor((uptime % 3600) / 60);
    const seconds = uptime % 60;
    
    console.log('\n' + '='.repeat(50));
    console.log('📊 FeishuListener 状态');
    console.log('='.repeat(50));
    console.log(`运行时间：${hours}h ${minutes}m ${seconds}s`);
    console.log(`活跃进程：${this.activeProcesses.size}/${CONFIG.maxConcurrent}`);
    console.log(`总任务数：${this.taskCounter}`);
    console.log(`最后消息：${this.lastMessageId || '无'}`);
    console.log(`轮询间隔：${CONFIG.pollInterval}ms`);
    console.log('='.repeat(50) + '\n');
  }

  /**
   * 优雅关闭
   */
  async shutdown() {
    this.log('info', '正在关闭监听器...');
    this.isRunning = false;
    
    // 等待所有进程完成
    if (this.activeProcesses.size > 0) {
      this.log('info', '等待活跃进程完成', { count: this.activeProcesses.size });
      await this.sendFeedback('⚠️ 服务正在关闭，等待当前任务完成...');
      
      const maxWait = 30000;
      const startTime = Date.now();
      while (this.activeProcesses.size > 0 && (Date.now() - startTime) < maxWait) {
        await this.sleep(1000);
      }
    }
    
    this.saveState();
    this.log('info', '监听器已关闭');
    process.exit(0);
  }

  /**
   * 启动监听服务
   */
  async start() {
    console.log('\n🎧 [FeishuListener] 启动飞书消息监听服务...\n');
    console.log(`配置:`);
    console.log(`  轮询间隔：${CONFIG.pollInterval}ms`);
    console.log(`  最大重试：${CONFIG.maxRetries}`);
    console.log(`  并发限制：${CONFIG.maxConcurrent}`);
    console.log(`  进程超时：${CONFIG.processTimeout}ms`);
    console.log(`  详细日志：${CONFIG.verbose}`);
    console.log();
    
    this.loadState();
    
    // 定时轮询
    const pollTimer = setInterval(async () => {
      await this.checkNewMessages();
    }, CONFIG.pollInterval);
    
    // 定期保存状态
    const saveTimer = setInterval(() => {
      this.saveState();
    }, 30000);
    
    // 定期清理超时进程
    const cleanupTimer = setInterval(() => {
      this.cleanupStaleProcesses();
    }, 60000);
    
    // 定期显示状态（每 5 分钟）
    const statusTimer = setInterval(() => {
      this.showStatus();
    }, 300000);
    
    // 优雅关闭处理
    process.on('SIGINT', () => this.shutdown());
    process.on('SIGTERM', () => this.shutdown());
    process.on('uncaughtException', (error) => {
      this.log('error', '未捕获异常', { error: error.message, stack: error.stack });
    });
    
    console.log('✅ 监听服务已启动，等待飞书消息...\n');
    this.showStatus();
  }
}

// 启动服务
const listener = new FeishuListener();
listener.start().catch(error => {
  console.error('❌ 启动失败:', error.message);
  process.exit(1);
});
