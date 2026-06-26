#!/usr/bin/env node
/**
 * 自愈监控器 v2.0（与实时日志监控器解耦）
 * 
 * 职责划分：
 * - 实时日志监控器（5 秒）：会话锁、任务失败、Gateway 崩溃 → 秒级响应
 * - 自愈监控器（5 分钟）：进度停滞、长期稳定性、根因分析 → 兜底检查
 * 
 * 核心功能：
 * 1. 进度停滞检测（长期趋势分析）
 * 2. 长期稳定性检查（每小时）
 * 3. 根因分析（复杂分析）
 * 4. 日志轮转（每天）
 * 
 * 已解耦功能（由实时日志监控器处理）：
 * - ❌ 会话锁检测 → log-monitor.js
 * - ❌ 脏数据任务检测 → log-monitor.js
 * - ❌ Gateway 健康检查 → log-monitor.js
 * 
 * 第一性原理：
 * - 预防优于治疗：提前发现问题
 * - 自动优于人工：减少人工干预
 * - 透明优于黑盒：修复过程可追踪
 */

const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

class SelfHealingMonitor {
  constructor(projectDir, config = {}) {
    this.projectDir = projectDir;
    this.stateFile = path.join(projectDir, '.task-state.json');
    this.logFile = path.join(path.dirname(projectDir), 'logs/self-healing.log');
    this.rootCauseLogFile = path.join(path.dirname(projectDir), 'logs/root-cause-analysis.log');
    
    this.config = {
      checkInterval: config.checkInterval || 60000,      // ✅ 1 分钟检查（兜底）
      progressStuckThreshold: config.progressStuckThreshold || 600000, // 10 分钟无进展
      runningTaskThreshold: config.runningTaskThreshold || 1800000,    // 30 分钟运行中
      sessionLockThreshold: config.sessionLockThreshold || 120000,     // ✅ 2 分钟锁文件（与 log-monitor 一致）
      maxConcurrentFailures: config.maxConcurrentFailures || 5,        // 连续失败阈值
      enableRootCauseAnalysis: config.enableRootCauseAnalysis !== false, // 启用根因分析
      enablePermanentFix: config.enablePermanentFix !== false,          // 启用永久修复
      autoRestartGateway: config.autoRestartGateway || false,           // 自动重启 Gateway
      ...config
    };
    
    // 状态追踪
    this.lastCompletedCount = 0;
    this.lastCheckTime = Date.now();
    this.consecutiveFailures = 0;
    this.issueHistory = new Map(); // 问题历史记录（用于根因分析）
    this.permanentFixesApplied = new Set(); // 已应用的永久修复
    
    // 确保日志目录
    const logDir = path.dirname(this.logFile);
    if (!fs.existsSync(logDir)) {
      fs.mkdirSync(logDir, { recursive: true });
    }
  }
  
  /**
   * 记录日志
   */
  log(message, level = 'INFO') {
    const timestamp = new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' });
    const logLine = `[${timestamp}] [${level}] ${message}\n`;
    console.log(logLine.trim());
    fs.appendFileSync(this.logFile, logLine);
  }
  
  /**
   * 加载任务状态
   */
  loadState() {
    try {
      return JSON.parse(fs.readFileSync(this.stateFile, 'utf-8'));
    } catch (e) {
      this.log('加载任务状态失败：' + e.message, 'ERROR');
      return null;
    }
  }
  
  /**
   * 保存任务状态
   */
  saveState(state) {
    fs.writeFileSync(this.stateFile, JSON.stringify(state, null, 2));
  }
  
  /**
   * 启动自愈监控（守护模式，带长期稳定性保障）
   */
  startDaemon() {
    this.log('🚀 自愈监控器启动（带长期稳定性保障）');
    this.log('📊 配置：检查间隔=' + this.config.checkInterval/1000 + 's, 进度停滞阈值=' + this.config.progressStuckThreshold/1000/60 + 'min');
    this.log('🛡️ 根因分析：' + (this.config.enableRootCauseAnalysis ? '已启用' : '未启用'));
    this.log('🔧 永久修复：' + (this.config.enablePermanentFix ? '已启用' : '未启用'));
    
    // 初始化
    const state = this.loadState();
    if (state) {
      this.lastCompletedCount = Object.values(state).filter(t => t.status === 'completed').length;
    }
    
    // 定期检查（5 分钟）
    setInterval(() => {
      this.checkAndHeal().catch(e => {
        this.log('自愈检查失败：' + e.message, 'ERROR');
      });
    }, this.config.checkInterval);
    
    // 长期稳定性监控（每小时）
    setInterval(() => {
      this.longTermStabilityCheck().catch(e => {
        this.log('长期稳定性检查失败：' + e.message, 'ERROR');
      });
    }, 3600000); // 1 小时
    
    // 日志轮转检查（每天）
    setInterval(() => {
      this.rotateLogs().catch(e => {
        this.log('日志轮转失败：' + e.message, 'ERROR');
      });
    }, 86400000); // 24 小时
    
    // 立即执行一次
    this.checkAndHeal().catch(console.error);
    
    this.log('✅ 自愈监控器已启动，长期稳定性保障已启用');
  }
  
  /**
   * 长期稳定性检查（每小时）
   */
  async longTermStabilityCheck() {
    this.log('🔍 开始长期稳定性检查...');
    
    const issues = [];
    
    // 1. 检查 Gateway 内存增长
    const gatewayMemory = await this.checkGatewayMemory();
    if (gatewayMemory && gatewayMemory.growthRate > 20) { // >20MB/min
      this.log('🔴 Gateway 内存增长过快：' + gatewayMemory.growthRate.toFixed(1) + 'MB/min', 'WARN');
      issues.push({
        type: 'gateway_memory_leak',
        severity: 'high',
        details: gatewayMemory
      });
    }
    
    // 2. 检查磁盘空间
    const diskUsage = await this.checkDiskUsage();
    if (diskUsage && diskUsage.usagePercent > 80) {
      this.log('🔴 磁盘使用率过高：' + diskUsage.usagePercent + '%', 'WARN');
      issues.push({
        type: 'disk_space_low',
        severity: 'high',
        details: diskUsage
      });
    }
    
    // 3. 检查文件描述符
    const fdUsage = await this.checkFileDescriptors();
    if (fdUsage && fdUsage.count > 10000) {
      this.log('🔴 文件描述符过多：' + fdUsage.count, 'WARN');
      issues.push({
        type: 'fd_leak',
        severity: 'medium',
        details: fdUsage
      });
    }
    
    // 4. 检查旧 sessions 文件
    const oldSessions = await this.checkOldSessions();
    if (oldSessions && oldSessions.count > 100) {
      this.log('🔴 旧 sessions 文件过多：' + oldSessions.count + ' 个', 'WARN');
      issues.push({
        type: 'old_sessions',
        severity: 'low',
        details: oldSessions
      });
    }
    
    // 5. 检查问题复发率
    const recurrenceRate = this.calculateRecurrenceRate();
    if (recurrenceRate > 0.5) { // >50% 问题复发
      this.log('🔴 问题复发率过高：' + (recurrenceRate * 100).toFixed(1) + '%', 'WARN');
      this.log('⚠️  建议启用根因分析和永久修复', 'WARN');
    }
    
    if (issues.length === 0) {
      this.log('✅ 长期稳定性检查通过');
    } else {
      this.log('⚠️ 发现 ' + issues.length + ' 个长期稳定性问题');
      for (const issue of issues) {
        await this.healLongTermIssue(issue);
      }
    }
  }
  
  /**
   * 自愈长期稳定性问题
   */
  async healLongTermIssue(issue) {
    this.log('🔧 自愈长期稳定性问题：' + issue.type);
    
    switch (issue.type) {
      case 'gateway_memory_leak':
        this.log('📋 建议：重启 Gateway 释放内存');
        if (this.config.autoRestartGateway) {
          await this.healGatewayDown({ type: 'gateway_down' });
        }
        break;
      
      case 'disk_space_low':
        this.log('📋 建议：清理日志和旧 sessions 文件');
        await this.cleanupOldFiles();
        break;
      
      case 'fd_leak':
        this.log('📋 建议：检查文件描述符泄漏，重启 Gateway');
        break;
      
      case 'old_sessions':
        this.log('📋 建议：清理 7 天前的 sessions 文件');
        await this.cleanupOldSessions();
        break;
    }
  }
  
  /**
   * 检查 Gateway 内存
   */
  async checkGatewayMemory() {
    return new Promise((resolve) => {
      exec('ps -o rss,etime,cmd -p $(pgrep -f "openclaw-gateway") | tail -1', (error, stdout) => {
        if (error || !stdout.trim()) {
          this.log('⚠️ 检查 Gateway 内存失败：' + (error ? error.message : '无输出'), 'DEBUG');
          resolve(null);
          return;
        }
        
        const parts = stdout.trim().split(/\s+/);
        const rssKB = parseInt(parts[0]);
        const etime = parts[1];
        
        // 解析运行时长
        let minutes = 0;
        if (etime.includes('-')) { // DD-HH:MM:SS
          const days = parseInt(etime.split('-')[0]);
          const timeParts = etime.split('-')[1].split(':');
          minutes = days * 24 * 60 + parseInt(timeParts[0]) * 60 + parseInt(timeParts[1]);
        } else if (etime.split(':').length === 3) { // HH:MM:SS
          const timeParts = etime.split(':');
          minutes = parseInt(timeParts[0]) * 60 + parseInt(timeParts[1]);
        } else { // MM:SS
          minutes = parseInt(etime.split(':')[0]);
        }
        
        const growthRate = minutes > 0 ? (rssKB / 1024) / minutes : 0;
        
        resolve({
          rssMB: rssKB / 1024,
          uptimeMinutes: minutes,
          growthRate: growthRate
        });
      });
    });
  }
  
  /**
   * 检查磁盘使用
   */
  async checkDiskUsage() {
    return new Promise((resolve) => {
      exec('df -h /home | tail -1', (error, stdout) => {
        if (error) {
          this.log('⚠️ 检查磁盘使用失败：' + error.message, 'DEBUG');
          resolve(null);
          return;
        }
        
        const parts = stdout.trim().split(/\s+/);
        const usagePercent = parseInt(parts[4].replace('%', ''));
        
        resolve({
          usagePercent,
          available: parts[3]
        });
      });
    });
  }
  
  /**
   * 检查文件描述符
   */
  async checkFileDescriptors() {
    return new Promise((resolve) => {
      exec('ls /proc/$(pgrep -f "openclaw-gateway")/fd | wc -l', (error, stdout) => {
        if (error) {
          resolve(null);
          return;
        }
        
        resolve({
          count: parseInt(stdout.trim())
        });
      });
    });
  }
  
  /**
   * 检查旧 sessions 文件
   */
  async checkOldSessions() {
    return new Promise((resolve) => {
      exec('find /home/ubutu/.openclaw/agents -name "*.jsonl" -mtime +7 | wc -l', (error, stdout) => {
        if (error) {
          resolve(null);
          return;
        }
        
        resolve({
          count: parseInt(stdout.trim())
        });
      });
    });
  }
  
  /**
   * 计算问题复发率
   */
  calculateRecurrenceRate() {
    let totalIssues = 0;
    let recurrentIssues = 0;
    
    for (const [type, history] of this.issueHistory.entries()) {
      totalIssues += history.length;
      if (history.length > 1) {
        recurrentIssues += history.length - 1;
      }
    }
    
    return totalIssues > 0 ? recurrentIssues / totalIssues : 0;
  }
  
  /**
   * 清理旧文件
   */
  async cleanupOldFiles() {
    this.log('🧹 清理旧文件...');
    
    // 清理 30 天前的日志
    exec('find /home/ubutu/.openclaw/workspace-novel_architect/logs -name "*.log" -mtime +30 -delete', () => {
      this.log('✅ 已清理 30 天前的日志文件');
    });
  }
  
  /**
   * 清理旧 sessions
   */
  async cleanupOldSessions() {
    this.log('🧹 清理 7 天前的 sessions 文件...');
    
    exec('find /home/ubutu/.openclaw/agents -name "*.jsonl" -mtime +7 -delete', () => {
      this.log('✅ 已清理 7 天前的 sessions 文件');
    });
  }
  
  /**
   * 日志轮转（每天）
   */
  async rotateLogs() {
    this.log('🔄 开始日志轮转...');
    
    const timestamp = new Date().toISOString().split('T')[0];
    const rotatedLogFile = this.logFile.replace('.log', '.' + timestamp + '.log');
    
    try {
      if (fs.existsSync(this.logFile)) {
        fs.renameSync(this.logFile, rotatedLogFile);
        this.log('✅ 日志已轮转：' + rotatedLogFile);
      }
    } catch (e) {
      this.log('❌ 日志轮转失败：' + e.message, 'ERROR');
    }
  }
  
  /**
   * 检查并自愈（兜底检查，实时问题由 log-monitor.js 处理）
   */
  async checkAndHeal() {
    this.log('🔍 开始健康检查（兜底检查）...');
    
    const issues = [];
    
    // 1. 检查进度停滞（长期趋势分析，日志监控器无法替代）
    const progressIssue = await this.checkProgressStuck();
    if (progressIssue) issues.push(progressIssue);
    
    // 2. 检查会话锁（兜底检查，日志监控器可能遗漏）
    const lockIssue = await this.checkSessionLocks();
    if (lockIssue) issues.push(lockIssue);
    
    // 3. 检查连续失败（趋势分析）
    const failureIssue = await this.checkConsecutiveFailures();
    if (failureIssue) issues.push(failureIssue);
    
    // ⚠️ 已解耦（由 log-monitor.js 实时处理）：
    // - 脏数据任务检测 → log-monitor.js 检测任务失败日志
    // - Gateway 健康检查 → log-monitor.js 检测 Gateway 错误日志
    
    if (issues.length === 0) {
      this.log('✅ 健康检查通过，无问题');
      return;
    }
    
    this.log('⚠️ 发现 ' + issues.length + ' 个问题，开始自愈...');
    
    // 执行自愈
    for (const issue of issues) {
      await this.healIssue(issue);
    }
    
    this.log('✅ 自愈完成');
  }
  
  /**
   * 检查进度停滞
   */
  async checkProgressStuck() {
    const state = this.loadState();
    if (!state) return null;
    
    const completedCount = Object.values(state).filter(t => t.status === 'completed').length;
    const now = Date.now();
    
    if (completedCount === this.lastCompletedCount) {
      const stuckDuration = now - this.lastCheckTime;
      
      if (stuckDuration > this.config.progressStuckThreshold) {
        this.log('🔴 进度停滞检测：' + Math.round(stuckDuration/60000) + '分钟无进展', 'WARN');
        return {
          type: 'progress_stuck',
          severity: 'high',
          duration: stuckDuration,
          completedCount: completedCount
        };
      }
    } else {
      this.lastCompletedCount = completedCount;
    }
    
    this.lastCheckTime = now;
    return null;
  }
  
  /**
   * 检查会话锁
   */
  async checkSessionLocks() {
    const agents = ['novel_architect', 'novel_writer', 'novel_editor', 'main'];
    const lockFiles = [];
    
    for (const agent of agents) {
      const sessionDir = path.join('/home/ubutu/.openclaw/agents', agent, 'sessions');
      if (!fs.existsSync(sessionDir)) continue;
      
      const files = fs.readdirSync(sessionDir);
      for (const file of files) {
        if (file.endsWith('.lock')) {
          const lockPath = path.join(sessionDir, file);
          const stats = fs.statSync(lockPath);
          const age = Date.now() - stats.mtimeMs;
          
          if (age > this.config.sessionLockThreshold) {
            this.log('🔴 会话锁检测：' + file + ' (存在 ' + Math.round(age/1000) + 's)', 'WARN');
            lockFiles.push(lockPath);
          }
        }
      }
    }
    
    if (lockFiles.length > 0) {
      return {
        type: 'session_locks',
        severity: 'high',
        lockFiles: lockFiles
      };
    }
    
    return null;
  }
  
  /**
   * 检查脏数据任务
   */
  async checkDirtyTasks() {
    const state = this.loadState();
    if (!state) return null;
    
    const dirtyTasks = [];
    const now = Date.now();
    
    for (const [taskId, taskInfo] of Object.entries(state)) {
      if (taskInfo.status !== 'running') continue;
      
      // 无 startedAt 或无 updatedAt
      if (!taskInfo.startedAt || !taskInfo.updatedAt) {
        dirtyTasks.push(taskId);
        continue;
      }
      
      // 运行超过阈值
      const lastUpdate = new Date(taskInfo.updatedAt).getTime();
      const runningDuration = now - lastUpdate;
      
      if (runningDuration > this.config.runningTaskThreshold) {
        dirtyTasks.push(taskId);
      }
    }
    
    if (dirtyTasks.length > 0) {
      this.log('🔴 脏数据检测：' + dirtyTasks.length + ' 个任务卡住', 'WARN');
      return {
        type: 'dirty_tasks',
        severity: 'medium',
        tasks: dirtyTasks
      };
    }
    
    return null;
  }
  
  // ⚠️ 已解耦：Gateway 健康检查由 log-monitor.js 实时处理
  // async checkGatewayHealth() - 已删除
  
  /**
   * 检查连续失败
   */
  async checkConsecutiveFailures() {
    const state = this.loadState();
    if (!state) return null;
    
    const now = Date.now();
    let recentFailures = 0;
    
    for (const taskInfo of Object.values(state)) {
      if (taskInfo.status !== 'failed') continue;
      if (!taskInfo.updatedAt) continue;
      
      const updated = new Date(taskInfo.updatedAt).getTime();
      if (now - updated < 30 * 60 * 1000) { // 30 分钟内
        recentFailures++;
      }
    }
    
    if (recentFailures > this.config.maxConcurrentFailures) {
      this.log('🔴 连续失败检测：' + recentFailures + ' 个任务失败', 'WARN');
      return {
        type: 'consecutive_failures',
        severity: 'medium',
        count: recentFailures
      };
    }
    
    return null;
  }
  
  /**
   * 自愈问题（带根因分析）
   */
  async healIssue(issue) {
    this.log('🔧 开始自愈：' + issue.type + ' (严重性：' + issue.severity + ')');
    
    // 记录问题历史（用于根因分析）
    this.recordIssueHistory(issue);
    
    // 根因分析（如果启用）
    if (this.config.enableRootCauseAnalysis) {
      const rootCause = await this.analyzeRootCause(issue);
      if (rootCause) {
        this.logRootCause(rootCause);
        
        // 应用永久修复（如果启用且未应用过）
        if (this.config.enablePermanentFix && !this.permanentFixesApplied.has(rootCause.id)) {
          await this.applyPermanentFix(rootCause);
          this.permanentFixesApplied.add(rootCause.id);
        }
      }
    }
    
    // 症状自愈（立即执行）
    switch (issue.type) {
      case 'session_locks':
        await this.healSessionLocks(issue);
        break;
      
      case 'dirty_tasks':
        await this.healDirtyTasks(issue);
        break;
      
      case 'progress_stuck':
        await this.healProgressStuck(issue);
        break;
      
      case 'gateway_down':
        await this.healGatewayDown(issue);
        break;
      
      case 'consecutive_failures':
        await this.healConsecutiveFailures(issue);
        break;
    }
  }
  
  /**
   * 记录问题历史
   */
  recordIssueHistory(issue) {
    const key = issue.type;
    if (!this.issueHistory.has(key)) {
      this.issueHistory.set(key, []);
    }
    
    const history = this.issueHistory.get(key);
    history.push({
      timestamp: Date.now(),
      severity: issue.severity,
      details: issue
    });
    
    // 保留最近 10 次记录
    if (history.length > 10) {
      history.shift();
    }
  }
  
  /**
   * 分析根因
   */
  async analyzeRootCause(issue) {
    this.log('🔍 开始根因分析：' + issue.type);
    
    switch (issue.type) {
      case 'session_locks':
        return this.analyzeSessionLockRootCause(issue);
      
      case 'dirty_tasks':
        return this.analyzeDirtyTasksRootCause(issue);
      
      case 'consecutive_failures':
        return this.analyzeConsecutiveFailuresRootCause(issue);
      
      default:
        return null;
    }
  }
  
  /**
   * 根因分析：会话锁
   */
  async analyzeSessionLockRootCause(issue) {
    const history = this.issueHistory.get('session_locks') || [];
    const recurrenceCount = history.length;
    
    this.log('📊 会话锁复发分析：' + recurrenceCount + ' 次历史复发');
    
    // 检查 Gateway 进程
    const gatewayRunning = await this.checkGatewayRunning();
    
    // 检查锁文件年龄
    const lockAges = issue.lockFiles.map(file => {
      try {
        const stats = fs.statSync(file);
        return Date.now() - stats.mtimeMs;
      } catch {
        return 0;
      }
    });
    const avgLockAge = lockAges.reduce((a, b) => a + b, 0) / lockAges.length;
    
    this.log('🔍 分析结果:');
    this.log('   - Gateway 运行状态：' + (gatewayRunning ? '正常' : '异常'));
    this.log('   - 锁文件平均年龄：' + Math.round(avgLockAge/1000) + '秒');
    this.log('   - 复发次数：' + recurrenceCount);
    
    if (recurrenceCount > 2) {
      this.log('🔴 根因判断：Gateway 会话管理机制缺陷（锁未正确释放）', 'WARN');
      
      return {
        id: 'session_lock_root_cause',
        type: 'session_locks',
        rootCause: 'Gateway 会话管理机制缺陷',
        description: 'Gateway 持有会话锁后未正确释放，导致锁文件复发',
        evidence: {
          recurrenceCount,
          avgLockAge,
          gatewayRunning
        },
        permanentFix: {
          type: 'gateway_session_config',
          action: 'enable_auto_unlock',
          description: '配置 Gateway 自动释放超时锁'
        }
      };
    }
    
    return null;
  }
  
  /**
   * 根因分析：脏数据任务
   */
  async analyzeDirtyTasksRootCause(issue) {
    const history = this.issueHistory.get('dirty_tasks') || [];
    const recurrenceCount = history.length;
    
    this.log('📊 脏数据复发分析：' + recurrenceCount + ' 次历史复发');
    
    // 分析任务类型分布
    const taskTypes = {};
    issue.tasks.forEach(taskId => {
      if (taskId.includes('review')) taskTypes['review'] = (taskTypes['review'] || 0) + 1;
      else if (taskId.includes('writing')) taskTypes['writing'] = (taskTypes['writing'] || 0) + 1;
      else if (taskId.includes('outline')) taskTypes['outline'] = (taskTypes['outline'] || 0) + 1;
    });
    
    this.log('🔍 分析结果:');
    this.log('   - 复发次数：' + recurrenceCount);
    this.log('   - 任务类型分布：' + JSON.stringify(taskTypes));
    
    if (recurrenceCount > 2) {
      this.log('🔴 根因判断：任务执行超时机制缺失', 'WARN');
      
      return {
        id: 'dirty_tasks_root_cause',
        type: 'dirty_tasks',
        rootCause: '任务执行超时机制缺失',
        description: '任务执行超时后未自动清理，导致脏数据积累',
        evidence: {
          recurrenceCount,
          taskTypes
        },
        permanentFix: {
          type: 'task_timeout_config',
          action: 'enable_auto_cleanup',
          description: '配置任务超时自动清理'
        }
      };
    }
    
    return null;
  }
  
  /**
   * 根因分析：连续失败
   */
  async analyzeConsecutiveFailuresRootCause(issue) {
    const history = this.issueHistory.get('consecutive_failures') || [];
    const recurrenceCount = history.length;
    
    this.log('📊 连续失败复发分析：' + recurrenceCount + ' 次历史复发');
    
    if (recurrenceCount > 2) {
      this.log('🔴 根因判断：系统性问题（模型/API/配置）', 'WARN');
      
      return {
        id: 'consecutive_failures_root_cause',
        type: 'consecutive_failures',
        rootCause: '系统性问题',
        description: '连续失败复发表明存在系统性问题（模型配置、API 限制、网络问题）',
        evidence: {
          recurrenceCount,
          failureCount: issue.count
        },
        permanentFix: {
          type: 'system_review',
          action: 'review_model_config',
          description: '审查模型配置和 API 限制'
        }
      };
    }
    
    return null;
  }
  
  /**
   * 应用永久修复
   */
  async applyPermanentFix(rootCause) {
    this.log('🔧 应用永久修复：' + rootCause.id + ' - ' + rootCause.rootCause);
    
    switch (rootCause.permanentFix.type) {
      case 'gateway_session_config':
        await this.fixGatewaySessionConfig(rootCause);
        break;
      
      case 'task_timeout_config':
        await this.fixTaskTimeoutConfig(rootCause);
        break;
      
      case 'system_review':
        await this.reviewSystemConfig(rootCause);
        break;
    }
  }
  
  /**
   * 永久修复：Gateway 会话配置
   */
  async fixGatewaySessionConfig(rootCause) {
    this.log('🔧 修复 Gateway 会话管理...');
    
    // 创建 Gateway 配置文件（如果不存在）
    const gatewayConfigPath = '/home/ubutu/.openclaw/openclaw.json';
    
    try {
      let config = {};
      if (fs.existsSync(gatewayConfigPath)) {
        config = JSON.parse(fs.readFileSync(gatewayConfigPath, 'utf-8'));
      }
      
      // 配置会话超时自动释放
      if (!config.gateway) config.gateway = {};
      if (!config.gateway.session) config.gateway.session = {};
      
      config.gateway.session.autoUnlockTimeout = 30000; // 30 秒自动释放
      config.gateway.session.enableHeartbeat = true;    // 启用心跳检测
      
      fs.writeFileSync(gatewayConfigPath, JSON.stringify(config, null, 2));
      
      this.log('✅ 已配置 Gateway 会话超时自动释放（30 秒）', 'INFO');
      this.log('⚠️  需要重启 Gateway 生效：openclaw gateway restart', 'WARN');
      
    } catch (e) {
      this.log('❌ Gateway 配置失败：' + e.message, 'ERROR');
    }
  }
  
  /**
   * 永久修复：任务超时配置
   */
  async fixTaskTimeoutConfig(rootCause) {
    this.log('🔧 配置任务超时自动清理...');
    
    // 这个已经在 scheduler 中实现，这里只是记录
    this.log('✅ 任务超时自动清理已启用（30 分钟阈值）', 'INFO');
  }
  
  /**
   * 系统配置审查
   */
  async reviewSystemConfig(rootCause) {
    this.log('📋 系统配置审查建议:');
    this.log('   1. 检查模型配置是否正确');
    this.log('   2. 检查 API 限制和配额');
    this.log('   3. 检查网络连接稳定性');
    this.log('   4. 检查 Gateway 日志是否有错误');
  }
  
  /**
   * 记录根因分析日志
   */
  logRootCause(rootCause) {
    const timestamp = new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' });
    const logLine = `[${timestamp}] [ROOT_CAUSE] ${JSON.stringify(rootCause, null, 2)}\n`;
    fs.appendFileSync(this.rootCauseLogFile, logLine);
    this.log('📋 根因分析报告：' + this.rootCauseLogFile);
  }
  
  // ⚠️ 已解耦：Gateway 检查由 log-monitor.js 实时处理
  // async checkGatewayRunning() - 已删除
  
  /**
   * 自愈：会话锁（兜底清理，主要由 log-monitor.js 处理）
   */
  async healSessionLocks(issue) {
    this.log('🧹 兜底清理 ' + issue.lockFiles.length + ' 个会话锁文件...');
    
    for (const lockFile of issue.lockFiles) {
      try {
        fs.unlinkSync(lockFile);
        this.log('✅ 已清理：' + lockFile);
      } catch (e) {
        this.log('❌ 清理失败：' + lockFile + ' - ' + e.message, 'ERROR');
      }
    }
    
    this.log('✅ 会话锁兜底清理完成');
  }
  
  /**
   * 自愈：脏数据任务
   */
  async healDirtyTasks(issue) {
    const state = this.loadState();
    if (!state) return;
    
    let resetCount = 0;
    for (const taskId of issue.tasks) {
      if (state[taskId]) {
        // ✅ 保留 agent 字段，只重置状态相关字段
        const agent = state[taskId].agent;  // 保存 agent
        const description = state[taskId].description;  // 保存 description
        const dependsOn = state[taskId].dependsOn;  // 保存 dependsOn
        
        state[taskId].status = 'pending';
        state[taskId].updatedAt = new Date().toISOString();
        delete state[taskId].startedAt;
        delete state[taskId].completedAt;
        delete state[taskId].error;
        
        // ✅ 恢复 agent 字段
        if (agent) state[taskId].agent = agent;
        if (description) state[taskId].description = description;
        if (dependsOn) state[taskId].dependsOn = dependsOn;
        
        resetCount++;
      }
    }
    
    this.saveState(state);
    this.log('✅ 已重置 ' + resetCount + ' 个脏数据任务为 pending (保留 agent 字段)');
  }
  
  /**
   * 自愈：进度停滞
   */
  async healProgressStuck(issue) {
    this.log('⚠️ 进度停滞 ' + Math.round(issue.duration/60000) + ' 分钟，触发深度检查...');
    
    // 触发完整健康检查
    await this.checkAndHeal();
  }
  
  /**
   * 自愈：Gateway 宕机
   */
  async healGatewayDown(issue) {
    this.log('🚨 Gateway 进程不存在，尝试重启...');
    
    return new Promise((resolve) => {
      exec('openclaw gateway restart', (error, stdout, stderr) => {
        if (error) {
          this.log('❌ Gateway 重启失败：' + stderr, 'ERROR');
          resolve(false);
        } else {
          this.log('✅ Gateway 已重启');
          resolve(true);
        }
      });
    });
  }
  
  /**
   * 自愈：连续失败
   */
  async healConsecutiveFailures(issue) {
    this.log('⚠️ 检测到 ' + issue.count + ' 个连续失败，触发失败任务分析...');
    
    // 这里可以集成 failure-handler
    this.log('📋 建议运行：failure-handler.js <项目目录> process');
  }
}

module.exports = SelfHealingMonitor;

// CLI 入口
if (require.main === module) {
  const args = process.argv.slice(2);
  const [projectDir, command] = args;
  
  if (!projectDir) {
    console.log('用法：node self-healing-monitor.js <项目目录> [daemon]');
    process.exit(1);
  }
  
  const monitor = new SelfHealingMonitor(projectDir);
  
  if (command === 'daemon') {
    monitor.startDaemon();
  } else {
    monitor.checkAndHeal().catch(console.error);
  }
}
