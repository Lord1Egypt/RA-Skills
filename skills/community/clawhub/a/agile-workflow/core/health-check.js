#!/usr/bin/env node
/**
 * 敏捷工作流健康检查器 v1.0
 * 
 * 基于第一性原理 + 思维链 + MECE 拆解 + 自我校验
 * 
 * 第一性原理：
 * - 健康检查的本质 = 确保工作流系统按预期运行
 * - 预期运行 = 任务正确分配 + 任务正确执行 + 状态正确同步 + 异常自动修复
 * 
 * MECE 拆解（相互独立，完全穷尽）：
 * 1. 任务列表检查 - 任务是否存在、配置是否正确
 * 2. 任务分配检查 - Agent 是否正确分配、负载是否均衡
 * 3. 任务执行检查 - 任务是否在执行、是否超时、是否失败
 * 4. Agent 状态检查 - Agent 是否可用、会话是否正常
 * 5. 数据一致性检查 - 状态文件与实际情况是否一致
 * 6. 自动修复 - 发现问题自动修复
 * 
 * ADD 实现：
 * - Analysis: 分析系统状态
 * - Design: 设计检查逻辑和修复策略
 * - Development: 实现检查和修复代码
 */

const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

// ============================================================================
// 配置
// ============================================================================

const CONFIG = {
  workspace: '/home/ubutu/.openclaw/workspace',
  agentsDir: '/home/ubutu/.openclaw/agents',
  skillDir: '/home/ubutu/.openclaw/workspace/skills/agile-workflow',
  logsDir: '/home/ubutu/.openclaw/workspace/logs/agile-workflow',
  
  // 阈值配置
  thresholds: {
    taskTimeout: 1800000,        // 30 分钟任务超时
    sessionLockTimeout: 300000,  // 5 分钟会话锁超时
    progressStuckThreshold: 600000, // 10 分钟进度停滞
    maxConcurrentFailures: 5,    // 最大连续失败数
    gatewayMemoryThreshold: 500, // MB，Gateway 内存阈值
  },
  
  // Agent 列表
  agents: ['novel_architect', 'novel_writer', 'novel_editor', 'main'],
  
  // 检查项权重（用于健康评分）
  weights: {
    taskList: 0.15,
    taskAssignment: 0.15,
    taskExecution: 0.25,
    agentStatus: 0.20,
    dataConsistency: 0.25,
  }
};

// ============================================================================
// 工具函数
// ============================================================================

function log(message, level = 'INFO') {
  const timestamp = new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' });
  const prefix = {
    'INFO': '📊',
    'WARN': '⚠️',
    'ERROR': '❌',
    'SUCCESS': '✅',
    'FIX': '🔧'
  }[level] || '📊';
  
  console.log(`[${timestamp}] ${prefix} ${message}`);
}

function execAsync(cmd) {
  return new Promise((resolve, reject) => {
    exec(cmd, { timeout: 30000 }, (error, stdout, stderr) => {
      if (error) {
        reject(error);
      } else {
        resolve(stdout.trim());
      }
    });
  });
}

function safeReadJSON(filePath) {
  try {
    if (!fs.existsSync(filePath)) return null;
    return JSON.parse(fs.readFileSync(filePath, 'utf8'));
  } catch (e) {
    return null;
  }
}

function safeWriteJSON(filePath, data) {
  try {
    const dir = path.dirname(filePath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
    return true;
  } catch (e) {
    log('写入文件失败：' + e.message, 'ERROR');
    return false;
  }
}

// ============================================================================
// 检查器类
// ============================================================================

class HealthChecker {
  constructor(projectDir) {
    this.projectDir = projectDir;
    this.stateFile = path.join(projectDir, '.task-state.json');
    this.reportFile = path.join(CONFIG.logsDir, 'health-check-report.json');
    
    this.issues = [];
    this.fixes = [];
    this.metrics = {
      taskList: { score: 100, issues: [] },
      taskAssignment: { score: 100, issues: [] },
      taskExecution: { score: 100, issues: [] },
      agentStatus: { score: 100, issues: [] },
      dataConsistency: { score: 100, issues: [] },
    };
  }

  // ============================================================================
  // 1. 任务列表检查
  // ============================================================================

  async checkTaskList() {
    log('开始检查任务列表...', 'INFO');
    
    const state = safeReadJSON(this.stateFile);
    
    if (!state) {
      this.metrics.taskList.score = 0;
      this.metrics.taskList.issues.push('任务状态文件不存在');
      this.issues.push({
        type: 'task_list_missing',
        severity: 'high',
        description: '任务状态文件不存在',
        fix: '创建工作流任务配置'
      });
      return;
    }
    
    const tasks = Object.entries(state);
    
    // 检查 1.1: 任务数量
    if (tasks.length === 0) {
      this.metrics.taskList.score -= 50;
      this.metrics.taskList.issues.push('任务列表为空');
      this.issues.push({
        type: 'task_list_empty',
        severity: 'medium',
        description: '任务列表为空，无任务可执行',
        fix: '添加任务到工作流'
      });
    }
    
    // 检查 1.2: 任务配置完整性
    let incompleteTasks = 0;
    const incompleteTaskIds = [];
    
    for (const [taskId, taskInfo] of tasks) {
      const requiredFields = ['status', 'agent', 'description'];
      const missingFields = requiredFields.filter(f => !taskInfo[f]);
      
      if (missingFields.length > 0) {
        incompleteTasks++;
        incompleteTaskIds.push(taskId);
        this.metrics.taskList.issues.push(`任务 ${taskId} 缺少字段：${missingFields.join(', ')}`);
      }
    }
    
    if (incompleteTasks > 0) {
      this.metrics.taskList.score -= (incompleteTasks / tasks.length) * 50;
      this.issues.push({
        type: 'task_config_incomplete',
        severity: 'medium',
        count: incompleteTasks,
        description: `${incompleteTasks} 个任务配置不完整`,
        fix: '补充缺失的任务字段'
      });
      
      // 添加修复任务（仅前 10 个，避免过多）
      for (const taskId of incompleteTaskIds.slice(0, 10)) {
        this.fixes.push({
          type: 'fix_task_config',
          taskId: taskId,
          action: '补充缺失的 agent 和 description 字段'
        });
      }
    }
    
    // 检查 1.3: 依赖关系有效性
    const taskIds = new Set(Object.keys(state));
    let invalidDeps = 0;
    
    for (const [taskId, taskInfo] of tasks) {
      if (taskInfo.dependsOn) {
        for (const dep of taskInfo.dependsOn) {
          if (!taskIds.has(dep)) {
            invalidDeps++;
            this.metrics.taskList.issues.push(`任务 ${taskId} 依赖不存在的任务：${dep}`);
          }
        }
      }
    }
    
    if (invalidDeps > 0) {
      this.metrics.taskList.score -= (invalidDeps / tasks.length) * 30;
      this.issues.push({
        type: 'invalid_dependencies',
        severity: 'high',
        count: invalidDeps,
        description: `${invalidDeps} 个任务依赖不存在`,
        fix: '修复依赖关系或删除无效依赖'
      });
    }
    
    log(`任务列表检查完成：${tasks.length} 个任务，${incompleteTasks} 个配置不完整，${invalidDeps} 个无效依赖`, 'INFO');
  }

  // ============================================================================
  // 2. 任务分配检查
  // ============================================================================

  async checkTaskAssignment() {
    log('开始检查任务分配...', 'INFO');
    
    const state = safeReadJSON(this.stateFile);
    if (!state) return;
    
    const tasks = Object.entries(state);
    
    // 检查 2.1: Agent 分配合理性
    const agentDistribution = {};
    for (const agent of CONFIG.agents) {
      agentDistribution[agent] = 0;
    }
    
    let unknownAgentTasks = 0;
    const unknownAgentTaskIds = [];
    
    for (const [taskId, taskInfo] of tasks) {
      const agent = taskInfo.agent;
      if (CONFIG.agents.includes(agent)) {
        agentDistribution[agent]++;
      } else {
        unknownAgentTasks++;
        unknownAgentTaskIds.push(taskId);
        this.metrics.taskAssignment.issues.push(`任务 ${taskId} 分配给未知 Agent: ${agent}`);
      }
    }
    
    if (unknownAgentTasks > 0) {
      this.metrics.taskAssignment.score -= (unknownAgentTasks / tasks.length) * 40;
      this.issues.push({
        type: 'unknown_agent',
        severity: 'medium',
        count: unknownAgentTasks,
        description: `${unknownAgentTasks} 个任务分配给未知 Agent`,
        fix: '更正 Agent 分配'
      });
      
      // 添加修复任务（仅前 10 个）
      for (const taskId of unknownAgentTaskIds.slice(0, 10)) {
        this.fixes.push({
          type: 'fix_agent_assignment',
          taskId: taskId,
          action: '根据任务类型重新分配正确的 Agent'
        });
      }
    }
    
    // 检查 2.2: 负载均衡
    const pendingTasks = tasks.filter(([_, t]) => t.status === 'pending');
    const pendingByAgent = {};
    
    for (const agent of CONFIG.agents) {
      pendingByAgent[agent] = pendingTasks.filter(([_, t]) => t.agent === agent).length;
    }
    
    const maxPending = Math.max(...Object.values(pendingByAgent));
    const minPending = Math.min(...Object.values(pendingByAgent));
    
    if (maxPending > 0 && (maxPending - minPending) > 3) {
      this.metrics.taskAssignment.score -= 20;
      this.metrics.taskAssignment.issues.push(`负载不均衡：最大 ${maxPending}, 最小 ${minPending}`);
      this.issues.push({
        type: 'load_imbalance',
        severity: 'low',
        distribution: pendingByAgent,
        description: 'Agent 负载不均衡',
        fix: '重新分配待执行任务'
      });
    }
    
    // 检查 2.3: 检查 Agent 进程是否运行
    for (const agent of CONFIG.agents) {
      const isRunning = await this.checkAgentProcess(agent);
      if (!isRunning && pendingByAgent[agent] > 0) {
        this.metrics.taskAssignment.score -= 30;
        this.issues.push({
          type: 'agent_not_running',
          severity: 'high',
          agent: agent,
          pendingTasks: pendingByAgent[agent],
          description: `Agent ${agent} 未运行但有 ${pendingByAgent[agent]} 个待执行任务`,
          fix: '启动 Agent 或重新分配任务'
        });
      }
    }
    
    log(`任务分配检查完成：Agent 分布=${JSON.stringify(agentDistribution)}`, 'INFO');
  }

  async checkAgentProcess(agentName) {
    try {
      const output = await execAsync(`pgrep -f "${agentName}" | wc -l`);
      return parseInt(output) > 0;
    } catch {
      return false;
    }
  }

  // ============================================================================
  // 3. 任务执行检查
  // ============================================================================

  async checkTaskExecution() {
    log('开始检查任务执行...', 'INFO');
    
    const state = safeReadJSON(this.stateFile);
    if (!state) return;
    
    const tasks = Object.entries(state);
    const now = Date.now();
    
    // 检查 3.1: 运行中任务超时
    let timeoutTasks = 0;
    for (const [taskId, taskInfo] of tasks) {
      if (taskInfo.status === 'running') {
        const lastUpdate = taskInfo.updatedAt ? new Date(taskInfo.updatedAt).getTime() : 0;
        const runningDuration = now - lastUpdate;
        
        if (runningDuration > CONFIG.thresholds.taskTimeout) {
          timeoutTasks++;
          this.metrics.taskExecution.issues.push(`任务 ${taskId} 运行超时 ${Math.round(runningDuration/60000)} 分钟`);
          this.issues.push({
            type: 'task_timeout',
            severity: 'high',
            taskId: taskId,
            duration: runningDuration,
            description: `任务 ${taskId} 运行超时`,
            fix: '重置任务状态并重新执行'
          });
          this.fixes.push({
            type: 'reset_task',
            taskId: taskId,
            action: '将状态重置为 pending'
          });
        }
      }
    }
    
    // 检查 3.2: 失败任务分析
    let failedTasks = 0;
    let recentFailures = 0;
    
    for (const [taskId, taskInfo] of tasks) {
      if (taskInfo.status === 'failed') {
        failedTasks++;
        
        const lastUpdate = taskInfo.updatedAt ? new Date(taskInfo.updatedAt).getTime() : 0;
        if (now - lastUpdate < 30 * 60 * 1000) { // 30 分钟内
          recentFailures++;
        }
      }
    }
    
    if (recentFailures > CONFIG.thresholds.maxConcurrentFailures) {
      this.metrics.taskExecution.score -= 40;
      this.issues.push({
        type: 'consecutive_failures',
        severity: 'high',
        count: recentFailures,
        description: `${recentFailures} 个任务在 30 分钟内失败`,
        fix: '分析失败原因并修复'
      });
    }
    
    // 检查 3.3: 进度停滞
    const completedCount = Object.values(state).filter(t => t.status === 'completed').length;
    const pendingCount = Object.values(state).filter(t => t.status === 'pending').length;
    
    if (completedCount === 0 && pendingCount > 0) {
      // 检查是否有任务应该执行但未执行
      const executableTasks = this.getExecutableTasks(state);
      if (executableTasks.length > 0) {
        this.metrics.taskExecution.score -= 30;
        this.issues.push({
          type: 'progress_stuck',
          severity: 'medium',
          executableCount: executableTasks.length,
          description: `${executableTasks.length} 个可执行任务未启动`,
          fix: '触发任务调度器'
        });
        this.fixes.push({
          type: 'trigger_scheduler',
          action: '启动任务调度器'
        });
      }
    }
    
    log(`任务执行检查完成：${timeoutTasks} 个超时，${failedTasks} 个失败，${recentFailures} 个近期失败`, 'INFO');
  }

  getExecutableTasks(state) {
    const completedTasks = new Set(
      Object.entries(state)
        .filter(([_, t]) => t.status === 'completed')
        .map(([id, _]) => id)
    );
    
    return Object.entries(state)
      .filter(([_, t]) => t.status === 'pending')
      .filter(([_, t]) => {
        if (!t.dependsOn || t.dependsOn.length === 0) return true;
        return t.dependsOn.every(dep => completedTasks.has(dep));
      })
      .map(([id, _]) => id);
  }

  // ============================================================================
  // 4. Agent 状态检查
  // ============================================================================

  async checkAgentStatus() {
    log('开始检查 Agent 状态...', 'INFO');
    
    for (const agent of CONFIG.agents) {
      const agentDir = path.join(CONFIG.agentsDir, agent);
      
      // 检查 4.1: Agent 目录存在性
      if (!fs.existsSync(agentDir)) {
        this.metrics.agentStatus.score -= 25;
        this.issues.push({
          type: 'agent_dir_missing',
          severity: 'high',
          agent: agent,
          description: `Agent ${agent} 目录不存在`,
          fix: '检查 Agent 配置'
        });
        continue;
      }
      
      // 检查 4.2: 会话锁
      const sessionDir = path.join(agentDir, 'sessions');
      if (fs.existsSync(sessionDir)) {
        const lockFiles = fs.readdirSync(sessionDir)
          .filter(f => f.endsWith('.lock'));
        
        for (const lockFile of lockFiles) {
          const lockPath = path.join(sessionDir, lockFile);
          const stats = fs.statSync(lockPath);
          const age = Date.now() - stats.mtimeMs;
          
          if (age > CONFIG.thresholds.sessionLockTimeout) {
            this.metrics.agentStatus.score -= 10;
            this.issues.push({
              type: 'session_lock_stale',
              severity: 'medium',
              agent: agent,
              lockFile: lockFile,
              age: Math.round(age / 1000),
              description: `Agent ${agent} 会话锁 ${lockFile} 超时 ${Math.round(age/1000)}s`,
              fix: '清理过期锁文件'
            });
            this.fixes.push({
              type: 'cleanup_lock',
              lockFile: lockPath,
              action: '删除过期锁文件'
            });
          }
        }
      }
      
      // 检查 4.3: Gateway 进程
      const gatewayRunning = await this.checkGatewayRunning();
      if (!gatewayRunning) {
        this.metrics.agentStatus.score -= 50;
        this.issues.push({
          type: 'gateway_down',
          severity: 'critical',
          description: 'Gateway 进程未运行',
          fix: '重启 Gateway'
        });
        this.fixes.push({
          type: 'restart_gateway',
          action: '重启 OpenClaw Gateway'
        });
      }
    }
    
    log('Agent 状态检查完成', 'INFO');
  }

  async checkGatewayRunning() {
    try {
      const output = await execAsync('pgrep -f "openclaw.*gateway" | wc -l');
      return parseInt(output) > 0;
    } catch {
      return false;
    }
  }

  // ============================================================================
  // 5. 数据一致性检查
  // ============================================================================

  async checkDataConsistency() {
    log('开始检查数据一致性...', 'INFO');
    
    const state = safeReadJSON(this.stateFile);
    if (!state) return;
    
    // 检查 5.1: 状态文件与文件系统一致性
    const tasks = Object.entries(state);
    let inconsistencies = 0;
    const falseCompletionTaskIds = [];
    
    for (const [taskId, taskInfo] of tasks) {
      if (taskInfo.status === 'completed') {
        // 检查是否有对应的产出物
        const hasOutput = await this.checkTaskOutput(taskId, taskInfo);
        if (!hasOutput) {
          inconsistencies++;
          falseCompletionTaskIds.push(taskId);
          this.metrics.dataConsistency.issues.push(`任务 ${taskId} 标记为完成但无产出物`);
          this.issues.push({
            type: 'false_completion',
            severity: 'high',
            taskId: taskId,
            description: `任务 ${taskId} 标记为完成但无产出物`,
            fix: '重新执行任务或修正状态'
          });
        }
      }
    }
    
    if (inconsistencies > 0) {
      this.metrics.dataConsistency.score -= (inconsistencies / tasks.length) * 50;
      
      // 添加修复任务（仅前 10 个，避免过多）
      for (const taskId of falseCompletionTaskIds.slice(0, 10)) {
        this.fixes.push({
          type: 'fix_false_completion',
          taskId: taskId,
          action: '将任务状态重置为 pending 以重新执行'
        });
      }
    }
    
    // 检查 5.2: 状态字段完整性
    let missingFields = 0;
    for (const [taskId, taskInfo] of tasks) {
      if (!taskInfo.updatedAt && taskInfo.status !== 'pending') {
        missingFields++;
        this.metrics.dataConsistency.issues.push(`任务 ${taskId} 缺少 updatedAt 字段`);
      }
    }
    
    if (missingFields > 0) {
      this.metrics.dataConsistency.score -= (missingFields / tasks.length) * 20;
    }
    
    log(`数据一致性检查完成：${inconsistencies} 个不一致，${missingFields} 个缺失字段`, 'INFO');
  }

  async checkTaskOutput(taskId, taskInfo) {
    // 根据任务类型检查产出物
    if (taskId.includes('outline')) {
      // 细纲任务：检查是否有细纲文件
      const outlineDir = path.join(this.projectDir, '04_章节细纲');
      if (fs.existsSync(outlineDir)) {
        const chapterMatch = taskId.match(/chapter-(\d+)/);
        if (chapterMatch) {
          const chapterNum = chapterMatch[1];
          const outlineFile = path.join(outlineDir, `第${chapterNum}章*.md`);
          const files = fs.readdirSync(outlineDir).filter(f => f.includes(`第${chapterNum}章`));
          return files.length > 0;
        }
      }
      return false;
    } else if (taskId.includes('writing')) {
      // 写作任务：检查是否有正文文件
      const writingDir = path.join(this.projectDir, '05_正文创作');
      if (fs.existsSync(writingDir)) {
        const chapterMatch = taskId.match(/chapter-(\d+)/);
        if (chapterMatch) {
          const chapterNum = chapterMatch[1];
          const files = fs.readdirSync(writingDir).filter(f => f.includes(`第${chapterNum}章`));
          return files.length > 0;
        }
      }
      return false;
    }
    
    // 默认返回 true（非文件产出任务）
    return true;
  }

  // ============================================================================
  // 6. 自动修复
  // ============================================================================

  async applyFixes() {
    if (this.fixes.length === 0) {
      log('无需修复', 'INFO');
      return;
    }
    
    log(`开始应用 ${this.fixes.length} 个修复...`, 'INFO');
    
    for (const fix of this.fixes) {
      try {
        await this.applyFix(fix);
      } catch (e) {
        log(`修复失败：${fix.type} - ${e.message}`, 'ERROR');
      }
    }
    
    log('修复完成', 'SUCCESS');
  }

  async applyFix(fix) {
    switch (fix.type) {
      case 'reset_task':
        await this.resetTask(fix.taskId);
        break;
      
      case 'cleanup_lock':
        await this.cleanupLock(fix.lockFile);
        break;
      
      case 'trigger_scheduler':
        await this.triggerScheduler();
        break;
      
      case 'restart_gateway':
        await this.restartGateway();
        break;
      
      case 'fix_task_config':
        await this.fixTaskConfig(fix.taskId);
        break;
      
      case 'fix_false_completion':
        await this.fixFalseCompletion(fix.taskId);
        break;
      
      case 'fix_agent_assignment':
        await this.fixAgentAssignment(fix.taskId);
        break;
    }
  }

  async resetTask(taskId) {
    const state = safeReadJSON(this.stateFile);
    if (!state || !state[taskId]) return;
    
    const agent = state[taskId].agent;
    const description = state[taskId].description;
    const dependsOn = state[taskId].dependsOn;
    
    state[taskId] = {
      status: 'pending',
      agent: agent,
      description: description,
      dependsOn: dependsOn || [],
      updatedAt: new Date().toISOString(),
      resetReason: '健康检查自动重置（超时）'
    };
    
    safeWriteJSON(this.stateFile, state);
    log(`已重置任务 ${taskId} 为 pending`, 'FIX');
  }

  async cleanupLock(lockFile) {
    if (fs.existsSync(lockFile)) {
      fs.unlinkSync(lockFile);
      log(`已清理锁文件：${lockFile}`, 'FIX');
    }
  }

  async triggerScheduler() {
    try {
      await execAsync(`node ${CONFIG.skillDir}/core/task-scheduler.js ${this.projectDir} check`);
      log('已触发任务调度器', 'FIX');
    } catch (e) {
      log('触发调度器失败：' + e.message, 'ERROR');
    }
  }

  async restartGateway() {
    try {
      await execAsync('openclaw gateway restart');
      log('已重启 Gateway', 'FIX');
    } catch (e) {
      log('重启 Gateway 失败：' + e.message, 'ERROR');
    }
  }

  async fixTaskConfig(taskId) {
    const state = safeReadJSON(this.stateFile);
    if (!state || !state[taskId]) return;
    
    const task = state[taskId];
    let fixed = false;
    
    // 补充缺失的 agent 字段
    if (!task.agent) {
      if (taskId.includes('writing')) {
        task.agent = 'novel_writer';
      } else if (taskId.includes('review')) {
        task.agent = 'novel_editor';
      } else if (taskId.includes('outline')) {
        task.agent = 'novel_architect';
      } else {
        task.agent = 'novel_architect';
      }
      fixed = true;
    }
    
    // 补充缺失的 description 字段
    if (!task.description) {
      const chapterMatch = taskId.match(/chapter-(\d+)/);
      const reviewMatch = taskId.match(/chapter-(\d+)-review/);
      
      if (reviewMatch) {
        task.description = `审查第${reviewMatch[1]}章`;
      } else if (chapterMatch) {
        const chapterNum = chapterMatch[1];
        if (taskId.includes('outline')) {
          task.description = `创作第${chapterNum}章细纲`;
        } else if (taskId.includes('writing')) {
          task.description = `创作第${chapterNum}章正文`;
        } else if (taskId.includes('review')) {
          task.description = `审查第${chapterNum}章`;
        }
      }
      fixed = true;
    }
    
    if (fixed) {
      task.updatedAt = new Date().toISOString();
      safeWriteJSON(this.stateFile, state);
      log(`已修复任务配置：${taskId}`, 'FIX');
    }
  }

  async fixFalseCompletion(taskId) {
    const state = safeReadJSON(this.stateFile);
    if (!state || !state[taskId]) return;
    
    // 将假完成的任务重置为 pending
    const task = state[taskId];
    const oldStatus = task.status;
    
    task.status = 'pending';
    task.updatedAt = new Date().toISOString();
    task.resetReason = '健康检查自动重置（假完成 - 无产出物）';
    delete task.completedAt;
    
    safeWriteJSON(this.stateFile, state);
    log(`已重置假完成任务 ${taskId} (${oldStatus} → pending)`, 'FIX');
  }

  async fixAgentAssignment(taskId) {
    const state = safeReadJSON(this.stateFile);
    if (!state || !state[taskId]) return;
    
    const task = state[taskId];
    const oldAgent = task.agent;
    
    // 根据任务类型重新分配 Agent
    if (taskId.includes('writing')) {
      task.agent = 'novel_writer';
    } else if (taskId.includes('review')) {
      task.agent = 'novel_editor';
    } else if (taskId.includes('outline')) {
      task.agent = 'novel_architect';
    } else {
      task.agent = 'novel_architect';
    }
    
    if (oldAgent !== task.agent) {
      task.updatedAt = new Date().toISOString();
      safeWriteJSON(this.stateFile, state);
      log(`已更正任务 Agent 分配：${taskId} (${oldAgent} → ${task.agent})`, 'FIX');
    }
  }

  // ============================================================================
  // 主检查流程
  // ============================================================================

  async runFullCheck() {
    log('=' .repeat(60), 'INFO');
    log('开始敏捷工作流健康检查', 'INFO');
    log('=' .repeat(60), 'INFO');
    
    const startTime = Date.now();
    
    // 执行所有检查
    await this.checkTaskList();
    await this.checkTaskAssignment();
    await this.checkTaskExecution();
    await this.checkAgentStatus();
    await this.checkDataConsistency();
    
    // 计算健康评分
    const healthScore = this.calculateHealthScore();
    
    // 应用自动修复
    if (this.fixes.length > 0) {
      await this.applyFixes();
    }
    
    // 生成报告
    const duration = Date.now() - startTime;
    const report = this.generateReport(healthScore, duration);
    
    // 保存报告
    safeWriteJSON(this.reportFile, report);
    
    log('=' .repeat(60), 'INFO');
    log(`健康检查完成：评分 ${healthScore}/100, 发现 ${this.issues.length} 个问题，应用 ${this.fixes.length} 个修复, 耗时 ${duration}ms`, 'SUCCESS');
    log('=' .repeat(60), 'INFO');
    
    return report;
  }

  calculateHealthScore() {
    let score = 0;
    
    for (const [category, data] of Object.entries(this.metrics)) {
      const weight = CONFIG.weights[category] || 0.2;
      score += data.score * weight;
    }
    
    return Math.round(score);
  }

  generateReport(healthScore, duration) {
    return {
      timestamp: new Date().toISOString(),
      projectDir: this.projectDir,
      healthScore: healthScore,
      duration: duration,
      summary: {
        totalIssues: this.issues.length,
        criticalIssues: this.issues.filter(i => i.severity === 'critical').length,
        highIssues: this.issues.filter(i => i.severity === 'high').length,
        mediumIssues: this.issues.filter(i => i.severity === 'medium').length,
        lowIssues: this.issues.filter(i => i.severity === 'low').length,
        fixesApplied: this.fixes.length
      },
      metrics: this.metrics,
      issues: this.issues,
      fixes: this.fixes,
      recommendations: this.generateRecommendations()
    };
  }

  generateRecommendations() {
    const recommendations = [];
    
    if (this.metrics.taskExecution.score < 70) {
      recommendations.push('任务执行问题较多，建议检查 Agent 配置和资源');
    }
    
    if (this.metrics.agentStatus.score < 70) {
      recommendations.push('Agent 状态异常，建议检查 Gateway 和会话管理');
    }
    
    if (this.metrics.dataConsistency.score < 70) {
      recommendations.push('数据一致性问题，建议运行完整验证');
    }
    
    if (this.issues.filter(i => i.severity === 'critical').length > 0) {
      recommendations.push('存在严重问题，建议立即处理');
    }
    
    return recommendations;
  }
}

// ============================================================================
// CLI 入口
// ============================================================================

async function main() {
  const args = process.argv.slice(2);
  const [projectDir, ...options] = args;
  
  const autoFix = options.includes('--auto-fix') || options.includes('-f');
  const jsonOutput = options.includes('--json') || options.includes('-j');
  const verbose = options.includes('--verbose') || options.includes('-v');
  
  if (!projectDir) {
    console.log('用法：node health-check.js <项目目录> [选项]');
    console.log('选项:');
    console.log('  --auto-fix, -f    自动修复发现的问题');
    console.log('  --json, -j        输出 JSON 格式报告');
    console.log('  --verbose, -v     详细输出');
    process.exit(1);
  }
  
  const checker = new HealthChecker(projectDir);
  
  try {
    const report = await checker.runFullCheck();
    
    if (jsonOutput) {
      console.log(JSON.stringify(report, null, 2));
    } else {
      // 输出摘要
      console.log('\n📊 健康检查报告摘要:');
      console.log(`   健康评分：${report.healthScore}/100`);
      console.log(`   问题总数：${report.summary.totalIssues}`);
      console.log(`     - 严重：${report.summary.criticalIssues}`);
      console.log(`     - 高：${report.summary.highIssues}`);
      console.log(`     - 中：${report.summary.mediumIssues}`);
      console.log(`     - 低：${report.summary.lowIssues}`);
      console.log(`   已应用修复：${report.summary.fixesApplied}`);
      console.log(`   耗时：${report.duration}ms`);
      
      if (report.recommendations.length > 0) {
        console.log('\n💡 建议:');
        for (const rec of report.recommendations) {
          console.log(`   - ${rec}`);
        }
      }
      
      if (report.issues.length > 0 && verbose) {
        console.log('\n⚠️ 问题列表:');
        for (const issue of report.issues) {
          console.log(`   [${issue.severity.toUpperCase()}] ${issue.type}: ${issue.description}`);
        }
      }
    }
    
    // 根据健康评分设置退出码
    if (report.healthScore < 50) {
      process.exit(2); // 严重问题
    } else if (report.healthScore < 70) {
      process.exit(1); // 警告
    } else {
      process.exit(0); // 健康
    }
  } catch (e) {
    console.error('健康检查失败:', e.message);
    process.exit(3);
  }
}

// 导出模块
module.exports = HealthChecker;

// 运行 CLI
if (require.main === module) {
  main();
}
