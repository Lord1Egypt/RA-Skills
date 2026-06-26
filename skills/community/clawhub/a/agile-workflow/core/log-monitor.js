#!/usr/bin/env node
/**
 * 实时日志监控器 v1.0
 * 
 * 核心功能：
 * 1. 实时监控 Gateway/Agent 日志
 * 2. 检测错误模式（Token 超限、会话锁、Gateway 崩溃等）
 * 3. 针对性自动修复（清理 session、重置任务等）
 * 
 * 第一性原理：
 * - 主动监控优于被动检查
 * - 精准修复优于批量清理
 * - 秒级响应优于 5 分钟延迟
 */

const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

class LogMonitor {
  constructor(config = {}) {
    this.config = {
      logDir: config.logDir || '/home/ubutu/.openclaw/workspace/logs',
      projectDir: config.projectDir,
      checkInterval: config.checkInterval || 5000, // 5 秒检查
      ...config
    };
    
    this.lastPosition = new Map(); // 文件上次读取位置
    this.errorHistory = new Map(); // 错误历史记录（防重复处理）
    this.taskStateFile = this.config.projectDir 
      ? path.join(this.config.projectDir, '.task-state.json')
      : null;
  }
  
  /**
   * 记录日志
   */
  log(message, level = 'INFO') {
    const timestamp = new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' });
    console.log(`[${timestamp}] [${level}] ${message}`);
  }
  
  /**
   * 启动实时监控（守护模式）
   */
  startDaemon() {
    this.log('🚀 实时日志监控器启动');
    this.log('📊 监控目录：' + this.config.logDir);
    this.log('📊 检查间隔：' + this.config.checkInterval + 'ms');
    
    // 定期检查日志文件
    setInterval(() => {
      this.checkLogs().catch(e => {
        this.log('日志检查失败：' + e.message, 'ERROR');
      });
    }, this.config.checkInterval);
    
    // 立即执行一次
    this.checkLogs().catch(console.error);
    
    this.log('✅ 实时日志监控器已启动');
  }
  
  /**
   * 检查所有日志文件
   */
  async checkLogs() {
    // ✅ 扩展日志文件列表（覆盖更多错误场景）
    const logFiles = [
      path.join(this.config.logDir, 'agent-daemon.log.1'),
      path.join(this.config.logDir, 'agent-coordinator.log'),
      path.join(this.config.logDir, 'gateway.log'),      // ✅ Gateway 错误
      path.join(this.config.logDir, 'task-scheduler.log'), // ✅ 调度器日志
      path.join(this.config.logDir, 'agent-daemon.log'), // ✅ 主日志
    ];
    
    for (const logFile of logFiles) {
      if (!fs.existsSync(logFile)) {
        console.log(`ℹ️ 跳过不存在的日志：${logFile}`);
        continue;
      }
      
      console.log(`🔍 监控日志：${logFile}`);
      const newLines = await this.readNewLines(logFile);
      for (const line of newLines) {
        await this.analyzeLine(line, logFile);
      }
    }
  }
  
  /**
   * 读取文件新增行
   */
  async readNewLines(filePath) {
    const lastPos = this.lastPosition.get(filePath) || 0;
    
    try {
      const stats = fs.statSync(filePath);
      if (stats.size < lastPos) {
        // 文件被轮转，从头开始
        this.lastPosition.set(filePath, 0);
        return [];
      }
      
      const buffer = Buffer.alloc(stats.size - lastPos);
      const fd = fs.openSync(filePath, 'r');
      fs.readSync(fd, buffer, 0, stats.size - lastPos, lastPos);
      fs.closeSync(fd);
      
      const content = buffer.toString('utf8');
      const lines = content.split('\n').filter(l => l.trim());
      
      this.lastPosition.set(filePath, stats.size);
      
      return lines;
    } catch (e) {
      return [];
    }
  }
  
  /**
   * 分析日志行
   */
  async analyzeLine(line, logFile) {
    // 1. Token 超限检测
    if (line.includes('400 Total tokens of image and text exceed max message tokens')) {
      const requestId = this.extractRequestId(line);
      this.log('🔴 检测到 Token 超限 (Request ID: ' + requestId + ')', 'WARN');
      await this.handleTokenExceed(requestId);
    }
    
    // 2. 会话锁超时检测
    if (line.includes('session file locked (timeout')) {
      const lockInfo = this.extractLockInfo(line);
      this.log('🔴 检测到会话锁超时：' + lockInfo.file, 'WARN');
      await this.handleSessionLock(lockInfo);
    }
    
    // 3. Gateway 崩溃检测
    if (line.includes('Gateway target:') && line.includes('error')) {
      this.log('🔴 检测到 Gateway 连接失败', 'ERROR');
      await this.handleGatewayDown();
    }
    
    // 4. 任务失败检测
    if (line.includes('任务失败，退出码：')) {
      const taskId = this.extractTaskId(line);
      if (taskId) {
        this.log('🔴 检测到任务失败：' + taskId, 'WARN');
        await this.handleTaskFailure(taskId);
      }
    }
  }
  
  /**
   * 提取 Request ID
   */
  extractRequestId(line) {
    const match = line.match(/Request id: ([a-f0-9]+)/);
    return match ? match[1] : 'unknown';
  }
  
  /**
   * 提取锁文件信息
   */
  extractLockInfo(line) {
    const match = line.match(/pid=(\d+)\s+(.+?\.lock)/);
    if (match) {
      return {
        pid: parseInt(match[1]),
        file: match[2]
      };
    }
    return { pid: 0, file: 'unknown' };
  }
  
  /**
   * 提取任务 ID
   */
  extractTaskId(line) {
    const match = line.match(/任务 ([a-z0-9_-]+) 执行失败/);
    return match ? match[1] : null;
  }
  
  /**
   * 处理 Token 超限（清理 session + 重置任务）
   */
  async handleTokenExceed(requestId) {
    const key = 'token_' + requestId;
    if (this.errorHistory.has(key) && Date.now() - this.errorHistory.get(key) < 60000) {
      return; // 1 分钟内不重复处理
    }
    this.errorHistory.set(key, Date.now());
    
    this.log('🔧 处理 Token 超限：清理 Agent 上下文 + 重置任务', 'INFO');
    
    // 清理所有 Agent 的 session 文件（释放上下文）
    const agents = ['novel_architect', 'novel_writer', 'novel_editor'];
    for (const agent of agents) {
      const sessionDir = path.join('/home/ubutu/.openclaw/agents', agent, 'sessions');
      if (!fs.existsSync(sessionDir)) continue;
      
      const files = fs.readdirSync(sessionDir);
      for (const file of files) {
        if (file.endsWith('.jsonl') && !file.includes('.lock')) {
          try {
            const filePath = path.join(sessionDir, file);
            const stats = fs.statSync(filePath);
            // 清理 1 小时内的 session（可能是卡住的）
            if (Date.now() - stats.mtimeMs < 3600000) {
              fs.unlinkSync(filePath);
              this.log('🧹 清理 session 文件：' + file);
            }
          } catch (e) {
            // 忽略
          }
        }
      }
    }
    
    // 重置最近的失败任务
    await this.resetRecentFailedTasks();
    
    this.log('✅ Token 超限处理完成');
  }
  
  /**
   * 重置最近的失败任务
   */
  async resetRecentFailedTasks() {
    if (!this.taskStateFile || !fs.existsSync(this.taskStateFile)) {
      return;
    }
    
    try {
      const state = JSON.parse(fs.readFileSync(this.taskStateFile, 'utf-8'));
      let resetCount = 0;
      
      for (const [tid, tstate] of Object.entries(state)) {
        if (tstate.status === 'failed' && tstate.error && tstate.error.includes('Token')) {
          // 确保 agent 字段存在
          if (!tstate.agent) {
            if (tid.includes('writing')) tstate.agent = 'novel_writer';
            else if (tid.includes('outline')) tstate.agent = 'novel_architect';
            else tstate.agent = 'novel_architect';
          }
          
          tstate.status = 'pending';
          tstate.updatedAt = new Date().toISOString();
          delete tstate.completedAt;
          delete tstate.startedAt;
          delete tstate.error;
          resetCount++;
        }
      }
      
      if (resetCount > 0) {
        fs.writeFileSync(this.taskStateFile, JSON.stringify(state, null, 2));
        this.log('✅ 已重置 ' + resetCount + ' 个 Token 超限失败任务');
      }
    } catch (e) {
      this.log('❌ 重置任务失败：' + e.message, 'ERROR');
    }
  }
  
  /**
   * 处理会话锁超时（带日志去重 + 年龄检查）
   */
  async handleSessionLock(lockInfo) {
    const key = 'lock_' + lockInfo.file;
    const now = Date.now();
    
    // 5 分钟内只记录一次日志
    if (this.errorHistory.has(key) && now - this.errorHistory.get(key) < 300000) {
      return;
    }
    this.errorHistory.set(key, now);
    
    // 检查锁文件年龄
    let lockAge = 0;
    try {
      const stats = fs.statSync(lockInfo.file);
      lockAge = now - stats.mtimeMs;
    } catch (e) {
      this.log('⚠️ 锁文件不存在：' + lockInfo.file, 'WARN');
      return;
    }
    
    this.log('🔴 检测到会话锁超时：' + lockInfo.file + ' (PID: ' + lockInfo.pid + ', 年龄：' + Math.round(lockAge/1000) + 's)', 'WARN');
    
    // 🔒 容错机制：锁文件年龄 >2 分钟直接清理（无论进程状态）
    // 因为正常任务执行不会超过 2 分钟，超过说明卡住了
    if (lockAge > 120000) {
      this.log('🔧 锁文件年龄超过 2 分钟，强制清理...', 'INFO');
      try {
        fs.unlinkSync(lockInfo.file);
        this.log('🧹 已清理锁文件：' + lockInfo.file, 'INFO');
      } catch (e) {
        this.log('❌ 清理失败：' + e.message, 'ERROR');
      }
      return;
    }
    
    // 锁文件年龄 <2 分钟，检查进程状态
    const gatewayRunning = await this.checkGatewayRunning();
    const agentProcesses = await this.checkAgentProcesses();
    
    if (!gatewayRunning && agentProcesses === 0) {
      // Gateway 和 Agent 都不在运行，安全清理
      try {
        fs.unlinkSync(lockInfo.file);
        this.log('🧹 清理会话锁：' + lockInfo.file, 'INFO');
      } catch (e) {
        this.log('❌ 清理失败：' + e.message, 'ERROR');
      }
    } else {
      this.log('⚠️ Gateway/Agent 仍在运行，锁文件年龄 <2 分钟，暂时保留', 'WARN');
    }
  }
  
  /**
   * 处理 Gateway 崩溃
   */
  async handleGatewayDown() {
    const key = 'gateway_down';
    if (this.errorHistory.has(key) && Date.now() - this.errorHistory.get(key) < 300000) {
      return; // 5 分钟内不重复处理
    }
    this.errorHistory.set(key, Date.now());
    
    this.log('🔧 检测 Gateway 状态...', 'INFO');
    
    const gatewayRunning = await this.checkGatewayRunning();
    
    if (!gatewayRunning) {
      this.log('🔴 Gateway 确实未运行，建议手动重启', 'ERROR');
    } else {
      this.log('✅ Gateway 仍在运行，可能是临时连接问题', 'INFO');
    }
  }
  
  /**
   * 处理任务失败
   */
  async handleTaskFailure(taskId) {
    const key = 'task_' + taskId;
    if (this.errorHistory.has(key) && Date.now() - this.errorHistory.get(key) < 60000) {
      return; // 1 分钟内不重复处理
    }
    this.errorHistory.set(key, Date.now());
    
    this.log('🔧 处理任务失败：重置任务状态', 'INFO');
    
    if (!this.taskStateFile || !fs.existsSync(this.taskStateFile)) {
      this.log('⚠️ 任务状态文件不存在，跳过', 'WARN');
      return;
    }
    
    try {
      const state = JSON.parse(fs.readFileSync(this.taskStateFile, 'utf-8'));
      
      if (state[taskId] && state[taskId].status === 'failed') {
        // 确保 agent 字段存在
        if (!state[taskId].agent) {
          if (taskId.includes('writing')) state[taskId].agent = 'novel_writer';
          else if (taskId.includes('outline')) state[taskId].agent = 'novel_architect';
          else state[taskId].agent = 'novel_architect';
        }
        
        state[taskId].status = 'pending';
        state[taskId].updatedAt = new Date().toISOString();
        delete state[taskId].completedAt;
        delete state[taskId].startedAt;
        delete state[taskId].error;
        
        fs.writeFileSync(this.taskStateFile, JSON.stringify(state, null, 2));
        this.log('✅ 已重置任务 ' + taskId + ' 为 pending');
      }
    } catch (e) {
      this.log('❌ 重置任务失败：' + e.message, 'ERROR');
    }
  }
  
  /**
   * 检查 Gateway 是否运行
   */
  async checkGatewayRunning() {
    return new Promise((resolve) => {
      exec('pgrep -f "openclaw.*gateway"', (error, stdout) => {
        resolve(!error && stdout.trim().length > 0);
      });
    });
  }
  
  /**
   * 检查 Agent 进程数
   */
  async checkAgentProcesses() {
    return new Promise((resolve) => {
      exec('pgrep -f "novel_writer|novel_architect|novel_editor" | wc -l', (error, stdout) => {
        if (error) {
          resolve(0);
          return;
        }
        resolve(parseInt(stdout.trim()));
      });
    });
  }
}

module.exports = LogMonitor;

// CLI 入口
if (require.main === module) {
  const args = process.argv.slice(2);
  const [projectDir] = args;
  
  if (!projectDir) {
    console.log('用法：node log-monitor.js <项目目录>');
    process.exit(1);
  }
  
  const monitor = new LogMonitor({
    projectDir: projectDir,
    checkInterval: 5000 // 5 秒检查
  });
  
  monitor.startDaemon();
}
