#!/usr/bin/env node
/**
 * 敏捷工作流健康检查器 v2.0
 * 
 * 基于第一性原理 + 思维链 + MECE 拆解 + 自我校验
 * 
 * ============================================================================
 * 第一性原理分析
 * ============================================================================
 * 
 * 问题本质：如何确保工作流系统按预期运行？
 * 
 * 预期运行的定义：
 * 1. 任务正确创建和配置
 * 2. 任务正确分配给合适的 Agent
 * 3. 任务正确执行并产生产出物
 * 4. 状态正确同步和更新
 * 5. 异常自动检测和修复
 * 
 * 健康检查 = 验证上述 5 点是否成立
 * 自动修复 = 当某点不成立时，恢复到成立状态
 * 
 * ============================================================================
 * 思维链推理
 * ============================================================================
 * 
 * 推理链 1: 任务状态验证
 * 任务标记为 completed → 应该有产出物 → 检查产出物是否存在 → 不存在则重置为 pending
 * 
 * 推理链 2: 任务配置验证
 * 任务存在 → 应该有完整配置 (agent, description, status) → 检查字段 → 缺失则补充
 * 
 * 推理链 3: 执行进度验证
 * 任务标记为 running → 应该有进展 → 检查 updatedAt → 长时间未更新则判定为停滞 → 重启或失败
 * 
 * 推理链 4: Agent 负载验证
 * 所有任务 → 按 Agent 分组 → 计算分布 → 检查是否均衡 → 不均衡则重新分配
 * 
 * 推理链 5: 数据一致性验证
 * 状态文件 → 实际文件系统 → 对比 → 不一致则同步
 * 
 * ============================================================================
 * MECE 拆解（相互独立，完全穷尽）
 * ============================================================================
 * 
 * 1. 任务列表检查 (Task List Check)
 *    1.1 任务存在性 - 任务状态文件是否存在
 *    1.2 任务数量 - 是否有任务
 *    1.3 配置完整性 - 每个任务是否有必需字段 (status, agent, description)
 *    1.4 依赖关系 - 依赖配置是否正确
 * 
 * 2. 任务分配检查 (Task Assignment Check)
 *    2.1 Agent 有效性 - 分配的 Agent 是否存在
 *    2.2 负载均衡 - 任务在各 Agent 间是否均衡
 *    2.3 类型匹配 - 任务类型与 Agent 专长是否匹配
 * 
 * 3. 任务执行检查 (Task Execution Check)
 *    3.1 状态分布 - pending/running/completed/failed 比例是否合理
 *    3.2 超时检测 - running 任务是否超时
 *    3.3 停滞检测 - running 任务是否长时间无进展
 *    3.4 失败分析 - failed 任务的失败原因
 * 
 * 4. Agent 状态检查 (Agent Status Check)
 *    4.1 进程状态 - Agent 进程是否运行
 *    4.2 会话状态 - Agent 会话是否活跃
 *    4.3 资源使用 - Agent 资源使用是否正常
 * 
 * 5. 数据一致性检查 (Data Consistency Check)
 *    5.1 产出物验证 - completed 任务是否有产出物
 *    5.2 状态同步 - 状态文件与文件系统是否一致
 *    5.3 时间戳验证 - updatedAt 字段是否合理
 * 
 * 6. 自动修复 (Auto Healing)
 *    6.1 配置修复 - 补充缺失字段
 *    6.2 状态修复 - 重置假完成任务
 *    6.3 执行修复 - 重启停滞任务
 *    6.4 分配修复 - 重新分配不平衡任务
 * 
 * ============================================================================
 * ADD 实现 (Analysis-Design-Development)
 * ============================================================================
 * 
 * Analysis: 分析当前系统状态，识别问题
 * Design: 设计检查逻辑和修复策略
 * Development: 实现检查和修复代码
 */

const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

// ============================================================================
// 配置
// ============================================================================

const CONFIG = {
  workspace: '/home/ubutu/.openclaw/workspace',
  skillDir: '/home/ubutu/.openclaw/workspace/skills/agile-workflow',
  logsDir: '/home/ubutu/.openclaw/workspace/logs/agile-workflow',
  
  // 阈值配置
  thresholds: {
    taskTimeout: 1800000,        // 30 分钟任务超时
    progressStuckThreshold: 600000, // 10 分钟进度停滞
    maxConcurrentTasks: 10,      // 最大并发任务数
    loadImbalanceThreshold: 2.0, // 负载不均衡阈值（最大/最小）
  },
  
  // 检查项权重（用于健康评分）
  weights: {
    taskList: 0.15,
    taskAssignment: 0.15,
    taskExecution: 0.25,
    agentStatus: 0.20,
    dataConsistency: 0.25,
  },
  
  // Agent 专长映射
  agentSpecialties: {
    novel_architect: ['outline', 'world_building', 'character_design', 'plot'],
    novel_writer: ['writing', 'chapter'],
    novel_editor: ['review', 'edit'],
    editor_in_chief: ['review-l3', 'final_review'],
    main: ['general', 'coordination'],
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
    'FIX': '🔧',
    'CHECK': '🔍'
  }[level] || '📊';
  
  console.log(`[${timestamp}] ${prefix} ${message}`);
}

function execAsync(cmd, options = {}) {
  return new Promise((resolve, reject) => {
    exec(cmd, { timeout: options.timeout || 30000, ...options }, (error, stdout, stderr) => {
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
    const content = fs.readFileSync(filePath, 'utf8');
    return JSON.parse(content);
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
// 健康检查器类
// ============================================================================

class HealthCheckerV2 {
  constructor(projectDir) {
    this.projectDir = projectDir;
    this.stateFile = path.join(projectDir, '.task-state.json');
    this.depsFile = path.join(projectDir, '.task-dependencies.json');
    this.reportFile = path.join(CONFIG.logsDir, 'health-check-report-v2.json');
    this.summaryFile = path.join(CONFIG.logsDir, 'health-check-summary-v2.json');
    
    this.issues = [];
    this.fixes = [];
    this.metrics = {
      taskList: { score: 100, issues: [], details: {} },
      taskAssignment: { score: 100, issues: [], details: {} },
      taskExecution: { score: 100, issues: [], details: {} },
      agentStatus: { score: 100, issues: [], details: {} },
      dataConsistency: { score: 100, issues: [], details: {} },
    };
    
    this.state = null;
    this.dependencies = null;
  }

  // ============================================================================
  // 主入口：执行完整健康检查
  // ============================================================================

  async runFullCheck() {
    const startTime = Date.now();
    log('='.repeat(80), 'INFO');
    log('开始敏捷工作流健康检查 v2.0', 'INFO');
    log('项目目录：' + this.projectDir, 'INFO');
    log('='.repeat(80), 'INFO');
    
    // 加载状态
    this.state = safeReadJSON(this.stateFile);
    this.dependencies = safeReadJSON(this.depsFile);
    
    if (!this.state) {
      log('任务状态文件不存在，无法进行检查', 'ERROR');
      return this.generateReport(startTime);
    }
    
    // 执行所有检查
    log('开始检查任务列表...', 'CHECK');
    await this.checkTaskList();
    
    log('开始检查任务分配...', 'CHECK');
    await this.checkTaskAssignment();
    
    log('开始检查任务执行...', 'CHECK');
    await this.checkTaskExecution();
    
    log('开始检查 Agent 状态...', 'CHECK');
    await this.checkAgentStatus();
    
    log('开始检查数据一致性...', 'CHECK');
    await this.checkDataConsistency();
    
    // 执行自动修复
    log('开始自动修复...', 'FIX');
    const fixesApplied = await this.applyAutoFixes();
    
    // 生成报告
    return this.generateReport(startTime, fixesApplied);
  }

  // ============================================================================
  // 1. 任务列表检查
  // ============================================================================

  async checkTaskList() {
    const tasks = Object.entries(this.state);
    const totalTasks = tasks.length;
    
    // 1.1 任务存在性
    if (totalTasks === 0) {
      this.metrics.taskList.score = 0;
      this.metrics.taskList.issues.push('任务列表为空');
      this.issues.push({
        type: 'task_list_empty',
        severity: 'high',
        category: 'taskList',
        description: '任务列表为空，无任务可执行',
        fix: '初始化工作流任务'
      });
      return;
    }
    
    // 1.2 配置完整性检查
    let incompleteTasks = 0;
    const missingFields = { agent: [], description: [], status: [] };
    
    for (const [taskId, taskInfo] of tasks) {
      if (!taskInfo.agent) {
        missingFields.agent.push(taskId);
        incompleteTasks++;
      }
      if (!taskInfo.description) {
        missingFields.description.push(taskId);
        incompleteTasks++;
      }
      if (!taskInfo.status) {
        missingFields.status.push(taskId);
        incompleteTasks++;
      }
    }
    
    this.metrics.taskList.details = {
      total: totalTasks,
      incomplete: incompleteTasks,
      missingFields: {
        agent: missingFields.agent.length,
        description: missingFields.description.length,
        status: missingFields.status.length
      }
    };
    
    if (incompleteTasks > 0) {
      const penalty = (incompleteTasks / totalTasks) * 30;
      this.metrics.taskList.score -= penalty;
      
      this.metrics.taskList.issues.push(`${incompleteTasks} 个任务配置不完整`);
      if (missingFields.agent.length > 0 && missingFields.agent.length <= 20) {
        this.metrics.taskList.issues.push(`缺少 agent: ${missingFields.agent.slice(0, 10).join(', ')}${missingFields.agent.length > 10 ? '...' : ''}`);
      }
      if (missingFields.description.length > 0 && missingFields.description.length <= 20) {
        this.metrics.taskList.issues.push(`缺少 description: ${missingFields.description.slice(0, 10).join(', ')}${missingFields.description.length > 10 ? '...' : ''}`);
      }
      
      this.issues.push({
        type: 'task_config_incomplete',
        severity: 'medium',
        category: 'taskList',
        count: incompleteTasks,
        description: `${incompleteTasks} 个任务配置不完整`,
        fix: '补充缺失的任务字段',
        details: missingFields
      });
      
      // 添加修复任务
      for (const taskId of missingFields.agent) {
        this.fixes.push({
          type: 'fix_missing_agent',
          taskId: taskId,
          priority: 'high'
        });
      }
      for (const taskId of missingFields.description) {
        this.fixes.push({
          type: 'fix_missing_description',
          taskId: taskId,
          priority: 'medium'
        });
      }
    }
    
    // 1.3 依赖关系检查
    if (this.dependencies) {
      let invalidDeps = 0;
      for (const [taskId, deps] of Object.entries(this.dependencies)) {
        if (!Array.isArray(deps)) {
          invalidDeps++;
          continue;
        }
        for (const dep of deps) {
          if (!this.state[dep]) {
            invalidDeps++;
            this.metrics.taskList.issues.push(`任务 ${taskId} 依赖不存在的任务：${dep}`);
          }
        }
      }
      
      if (invalidDeps > 0) {
        this.metrics.taskList.score -= Math.min(invalidDeps * 2, 20);
        this.issues.push({
          type: 'invalid_dependencies',
          severity: 'medium',
          category: 'taskList',
          count: invalidDeps,
          description: `${invalidDeps} 个依赖关系无效`,
          fix: '修复或移除无效依赖'
        });
      }
    }
    
    log(`任务列表检查完成：${totalTasks} 个任务，${incompleteTasks} 个配置不完整`, 
        incompleteTasks > 0 ? 'WARN' : 'SUCCESS');
  }

  // ============================================================================
  // 2. 任务分配检查
  // ============================================================================

  async checkTaskAssignment() {
    const tasks = Object.entries(this.state);
    
    // 2.1 Agent 有效性检查
    const agentDistribution = {};
    const unknownAgents = [];
    
    for (const [taskId, taskInfo] of tasks) {
      const agent = taskInfo.agent;
      if (!agent) continue;
      
      if (!agentDistribution[agent]) {
        agentDistribution[agent] = [];
      }
      agentDistribution[agent].push(taskId);
      
      // 检查是否为已知 Agent
      if (!CONFIG.agentSpecialties[agent]) {
        unknownAgents.push({ taskId, agent });
      }
    }
    
    this.metrics.taskAssignment.details = {
      agentDistribution: Object.fromEntries(
        Object.entries(agentDistribution).map(([k, v]) => [k, v.length])
      ),
      unknownAgents: unknownAgents.length
    };
    
    if (unknownAgents.length > 0) {
      const penalty = Math.min(unknownAgents.length * 3, 20);
      this.metrics.taskAssignment.score -= penalty;
      
      this.metrics.taskAssignment.issues.push(`${unknownAgents.length} 个任务分配给未知 Agent`);
      unknownAgents.slice(0, 5).forEach(({ taskId, agent }) => {
        this.metrics.taskAssignment.issues.push(`  - ${taskId} → ${agent}`);
      });
      
      this.issues.push({
        type: 'unknown_agent',
        severity: 'medium',
        category: 'taskAssignment',
        count: unknownAgents.length,
        description: `${unknownAgents.length} 个任务分配给未知 Agent`,
        fix: '更正 Agent 分配',
        details: unknownAgents
      });
      
      // 添加修复任务
      for (const { taskId, agent } of unknownAgents.slice(0, 10)) {
        this.fixes.push({
          type: 'fix_unknown_agent',
          taskId: taskId,
          currentAgent: agent,
          priority: 'high'
        });
      }
    }
    
    // 2.2 负载均衡检查
    const counts = Object.values(agentDistribution).map(v => v.length);
    if (counts.length > 1) {
      const maxLoad = Math.max(...counts);
      const minLoad = Math.min(...counts);
      const ratio = maxLoad / (minLoad || 1);
      
      this.metrics.taskAssignment.details.loadBalance = {
        max: maxLoad,
        min: minLoad,
        ratio: ratio.toFixed(2)
      };
      
      if (ratio > CONFIG.thresholds.loadImbalanceThreshold) {
        const penalty = Math.min((ratio - 1) * 10, 20);
        this.metrics.taskAssignment.score -= penalty;
        
        this.metrics.taskAssignment.issues.push(`负载不均衡：最大 ${maxLoad}, 最小 ${minLoad}, 比率 ${ratio.toFixed(2)}`);
        
        this.issues.push({
          type: 'load_imbalance',
          severity: 'low',
          category: 'taskAssignment',
          distribution: Object.fromEntries(
            Object.entries(agentDistribution).map(([k, v]) => [k, v.length])
          ),
          description: `Agent 负载不均衡（比率 ${ratio.toFixed(2)}）`,
          fix: '重新分配任务以平衡负载'
        });
      }
    }
    
    // 2.3 类型匹配检查
    const typeMismatches = [];
    for (const [taskId, taskInfo] of tasks) {
      const agent = taskInfo.agent;
      if (!agent || !CONFIG.agentSpecialties[agent]) continue;
      
      const specialties = CONFIG.agentSpecialties[agent];
      const taskType = taskId.toLowerCase();
      
      // 简单匹配：检查任务 ID 是否包含 Agent 专长的关键词
      const matches = specialties.some(spec => taskType.includes(spec));
      if (!matches && taskInfo.status === 'pending') {
        typeMismatches.push({ taskId, agent, taskType });
      }
    }
    
    if (typeMismatches.length > 10) {
      this.metrics.taskAssignment.score -= Math.min(typeMismatches.length, 15);
      this.issues.push({
        type: 'agent_type_mismatch',
        severity: 'low',
        category: 'taskAssignment',
        count: typeMismatches.length,
        description: `${typeMismatches.length} 个任务可能分配给了不匹配的 Agent`,
        fix: '根据任务类型重新分配 Agent'
      });
    }
    
    log(`任务分配检查完成：${Object.keys(agentDistribution).length} 个 Agent, ${unknownAgents.length} 个未知 Agent`, 
        unknownAgents.length > 0 ? 'WARN' : 'SUCCESS');
  }

  // ============================================================================
  // 3. 任务执行检查
  // ============================================================================

  async checkTaskExecution() {
    const tasks = Object.entries(this.state);
    
    // 3.1 状态分布
    const statusDistribution = {
      pending: 0,
      ready: 0,
      running: 0,
      completed: 0,
      failed: 0
    };
    
    for (const [, taskInfo] of tasks) {
      const status = taskInfo.status || 'pending';
      if (statusDistribution[status] !== undefined) {
        statusDistribution[status]++;
      } else {
        statusDistribution.pending++;
      }
    }
    
    this.metrics.taskExecution.details = {
      statusDistribution,
      total: tasks.length,
      completionRate: ((statusDistribution.completed / tasks.length) * 100).toFixed(1) + '%'
    };
    
    // 3.2 超时检测
    const now = Date.now();
    const timeoutTasks = [];
    const stuckTasks = [];
    
    for (const [taskId, taskInfo] of tasks) {
      if (taskInfo.status === 'running') {
        const updatedAt = taskInfo.updatedAt || taskInfo.startedAt || 0;
        const runningTime = now - updatedAt;
        
        if (runningTime > CONFIG.thresholds.taskTimeout) {
          timeoutTasks.push({
            taskId,
            runningTime,
            updatedAt: new Date(updatedAt).toISOString()
          });
        } else if (runningTime > CONFIG.thresholds.progressStuckThreshold) {
          stuckTasks.push({
            taskId,
            runningTime,
            updatedAt: new Date(updatedAt).toISOString()
          });
        }
      }
    }
    
    if (timeoutTasks.length > 0) {
      this.metrics.taskExecution.score -= Math.min(timeoutTasks.length * 5, 25);
      this.metrics.taskExecution.issues.push(`${timeoutTasks.length} 个任务超时（>30 分钟）`);
      
      this.issues.push({
        type: 'task_timeout',
        severity: 'high',
        category: 'taskExecution',
        count: timeoutTasks.length,
        description: `${timeoutTasks.length} 个任务执行超时`,
        fix: '重启或标记失败',
        details: timeoutTasks.slice(0, 10)
      });
      
      // 添加修复任务
      for (const { taskId } of timeoutTasks.slice(0, 10)) {
        this.fixes.push({
          type: 'fix_timeout_task',
          taskId: taskId,
          priority: 'high'
        });
      }
    }
    
    if (stuckTasks.length > 0) {
      this.metrics.taskExecution.score -= Math.min(stuckTasks.length * 3, 15);
      this.metrics.taskExecution.issues.push(`${stuckTasks.length} 个任务停滞（>10 分钟无进展）`);
      
      this.issues.push({
        type: 'task_stuck',
        severity: 'medium',
        category: 'taskExecution',
        count: stuckTasks.length,
        description: `${stuckTasks.length} 个任务执行停滞`,
        fix: '检查 Agent 状态或重启任务',
        details: stuckTasks.slice(0, 10)
      });
    }
    
    // 3.3 失败任务分析
    const failedTasks = tasks.filter(([, t]) => t.status === 'failed');
    if (failedTasks.length > 0) {
      this.metrics.taskExecution.issues.push(`${failedTasks.length} 个任务失败`);
      
      this.issues.push({
        type: 'task_failures',
        severity: 'high',
        category: 'taskExecution',
        count: failedTasks.length,
        description: `${failedTasks.length} 个任务执行失败`,
        fix: '分析失败原因并重试',
        details: failedTasks.slice(0, 10).map(([tid, t]) => ({
          taskId: tid,
          error: t.error || '未知错误'
        }))
      });
    }
    
    // 3.4 并发数检查
    if (statusDistribution.running > CONFIG.thresholds.maxConcurrentTasks) {
      this.metrics.taskExecution.score -= 10;
      this.issues.push({
        type: 'too_many_concurrent',
        severity: 'medium',
        category: 'taskExecution',
        count: statusDistribution.running,
        description: `并发任务数过多 (${statusDistribution.running} > ${CONFIG.thresholds.maxConcurrentTasks})`,
        fix: '等待部分任务完成或增加资源'
      });
    }
    
    log(`任务执行检查完成：${statusDistribution.completed} 完成, ${statusDistribution.running} 运行中, ${statusDistribution.failed} 失败`, 
        statusDistribution.failed > 0 || timeoutTasks.length > 0 ? 'WARN' : 'SUCCESS');
  }

  // ============================================================================
  // 4. Agent 状态检查
  // ============================================================================

  async checkAgentStatus() {
    // 4.1 检查 Agent 进程
    const agentProcesses = {};
    
    for (const agent of Object.keys(CONFIG.agentSpecialties)) {
      try {
        const result = await execAsync(`ps aux | grep -E "${agent}" | grep -v grep | wc -l`);
        const count = parseInt(result) || 0;
        agentProcesses[agent] = count;
      } catch (e) {
        agentProcesses[agent] = 0;
      }
    }
    
    this.metrics.agentStatus.details = { agentProcesses };
    
    // 4.2 检查 Gateway 状态
    try {
      const gatewayStatus = await execAsync('openclaw gateway status 2>/dev/null || echo "unknown"');
      this.metrics.agentStatus.details.gatewayStatus = gatewayStatus;
      
      if (gatewayStatus.includes('unknown') || gatewayStatus.includes('stopped')) {
        this.metrics.agentStatus.score -= 30;
        this.issues.push({
          type: 'gateway_down',
          severity: 'critical',
          category: 'agentStatus',
          description: 'Gateway 未运行',
          fix: '启动 Gateway: openclaw gateway start'
        });
      }
    } catch (e) {
      this.metrics.agentStatus.details.gatewayStatus = 'error: ' + e.message;
    }
    
    // 4.3 检查活跃会话
    try {
      const sessionsResult = await execAsync('openclaw sessions list --limit 100 2>/dev/null | head -20 || echo "unknown"');
      this.metrics.agentStatus.details.activeSessions = sessionsResult.split('\n').filter(l => l.trim()).length;
    } catch (e) {
      this.metrics.agentStatus.details.activeSessions = 'error';
    }
    
    log(`Agent 状态检查完成：Gateway ${this.metrics.agentStatus.details.gatewayStatus?.includes('running') ? '运行中' : '未知'}`, 
        'SUCCESS');
  }

  // ============================================================================
  // 5. 数据一致性检查
  // ============================================================================

  async checkDataConsistency() {
    const tasks = Object.entries(this.state);
    
    // 5.1 产出物验证
    const falseCompletes = [];
    const outputDirs = {
      'outline': '04_章节细纲',
      'writing': '05_正文创作',
      'review': '06_审查报告'
    };
    
    for (const [taskId, taskInfo] of tasks) {
      if (taskInfo.status !== 'completed') continue;
      
      // 检查是否有产出物
      let hasOutput = false;
      
      // 检查 output 字段
      if (taskInfo.output) {
        hasOutput = true;
      }
      
      // 检查实际文件
      if (!hasOutput) {
        for (const [type, dir] of Object.entries(outputDirs)) {
          if (taskId.toLowerCase().includes(type)) {
            const chapterMatch = taskId.match(/chapter-(\d+)/);
            if (chapterMatch) {
              const chapterNum = chapterMatch[1];
              const possibleFiles = [
                path.join(this.projectDir, dir, `第${chapterNum}章*.md`),
                path.join(this.projectDir, dir, `chapter-${chapterNum}*.md`)
              ];
              
              for (const pattern of possibleFiles) {
                try {
                  const files = await execAsync(`ls "${path.join(this.projectDir, dir)}" 2>/dev/null | grep -E "第${chapterNum}章|chapter-${chapterNum}" | wc -l`);
                  if (parseInt(files) > 0) {
                    hasOutput = true;
                    break;
                  }
                } catch (e) {
                  // 忽略
                }
              }
            }
            break;
          }
        }
      }
      
      if (!hasOutput) {
        falseCompletes.push(taskId);
      }
    }
    
    this.metrics.dataConsistency.details = {
      totalCompleted: tasks.filter(([, t]) => t.status === 'completed').length,
      falseCompletes: falseCompletes.length,
      falseCompleteRate: ((falseCompletes.length / tasks.filter(([, t]) => t.status === 'completed').length) * 100).toFixed(1) + '%'
    };
    
    if (falseCompletes.length > 0) {
      const penalty = Math.min((falseCompletes.length / tasks.length) * 100, 30);
      this.metrics.dataConsistency.score -= penalty;
      
      this.metrics.dataConsistency.issues.push(`${falseCompletes.length} 个任务标记为完成但无产出物`);
      if (falseCompletes.length <= 30) {
        this.metrics.dataConsistency.issues.push(`  ${falseCompletes.slice(0, 10).join(', ')}${falseCompletes.length > 10 ? '...' : ''}`);
      }
      
      this.issues.push({
        type: 'false_completion',
        severity: 'high',
        category: 'dataConsistency',
        count: falseCompletes.length,
        description: `${falseCompletes.length} 个任务假完成（标记为 completed 但无产出物）`,
        fix: '重置为 pending 状态',
        details: falseCompletes
      });
      
      // 添加修复任务
      for (const taskId of falseCompletes) {
        this.fixes.push({
          type: 'fix_false_complete',
          taskId: taskId,
          priority: 'high'
        });
      }
    }
    
    // 5.2 时间戳验证
    const missingTimestamps = [];
    for (const [taskId, taskInfo] of tasks) {
      if (!taskInfo.updatedAt && taskInfo.status !== 'pending') {
        missingTimestamps.push(taskId);
      }
    }
    
    if (missingTimestamps.length > 0) {
      this.metrics.dataConsistency.score -= Math.min(missingTimestamps.length, 10);
      this.issues.push({
        type: 'missing_timestamps',
        severity: 'low',
        category: 'dataConsistency',
        count: missingTimestamps.length,
        description: `${missingTimestamps.length} 个任务缺少 updatedAt 字段`,
        fix: '补充时间戳'
      });
    }
    
    log(`数据一致性检查完成：${falseCompletes.length} 个假完成任务`, 
        falseCompletes.length > 0 ? 'WARN' : 'SUCCESS');
  }

  // ============================================================================
  // 6. 自动修复
  // ============================================================================

  async applyAutoFixes() {
    const fixesApplied = {
      taskConfig: 0,
      agentAssignment: 0,
      falseCompletion: 0,
      timeout: 0,
      total: 0
    };
    
    let stateModified = false;
    
    for (const fix of this.fixes) {
      try {
        switch (fix.type) {
          case 'fix_missing_agent': {
            const taskInfo = this.state[fix.taskId];
            if (taskInfo && !taskInfo.agent) {
              // 根据任务类型推断 Agent
              const taskType = fix.taskId.toLowerCase();
              if (taskType.includes('outline') || taskType.includes('world') || taskType.includes('character')) {
                taskInfo.agent = 'novel_architect';
              } else if (taskType.includes('writing') || taskType.includes('chapter')) {
                taskInfo.agent = 'novel_writer';
              } else if (taskType.includes('review')) {
                taskInfo.agent = 'novel_editor';
              } else {
                taskInfo.agent = 'main';
              }
              taskInfo.updatedAt = Date.now();
              fixesApplied.taskConfig++;
              stateModified = true;
              log(`修复 ${fix.taskId}: 补充 agent=${taskInfo.agent}`, 'FIX');
            }
            break;
          }
          
          case 'fix_missing_description': {
            const taskInfo = this.state[fix.taskId];
            if (taskInfo && !taskInfo.description) {
              // 生成默认描述
              taskInfo.description = `执行任务：${fix.taskId}`;
              taskInfo.updatedAt = Date.now();
              fixesApplied.taskConfig++;
              stateModified = true;
              log(`修复 ${fix.taskId}: 补充 description`, 'FIX');
            }
            break;
          }
          
          case 'fix_false_complete': {
            const taskInfo = this.state[fix.taskId];
            if (taskInfo && taskInfo.status === 'completed') {
              // 重置为 pending
              taskInfo.status = 'pending';
              taskInfo.updatedAt = Date.now();
              delete taskInfo.output;
              delete taskInfo.completedAt;
              fixesApplied.falseCompletion++;
              stateModified = true;
              log(`修复 ${fix.taskId}: 重置为 pending (假完成)`, 'FIX');
            }
            break;
          }
          
          case 'fix_timeout_task': {
            const taskInfo = this.state[fix.taskId];
            if (taskInfo && taskInfo.status === 'running') {
              // 标记为失败，等待重试
              taskInfo.status = 'failed';
              taskInfo.error = '任务超时';
              taskInfo.updatedAt = Date.now();
              fixesApplied.timeout++;
              stateModified = true;
              log(`修复 ${fix.taskId}: 标记为失败 (超时)`, 'FIX');
            }
            break;
          }
          
          case 'fix_unknown_agent': {
            const taskInfo = this.state[fix.taskId];
            if (taskInfo) {
              // 重置为 main Agent
              taskInfo.agent = 'main';
              taskInfo.updatedAt = Date.now();
              fixesApplied.agentAssignment++;
              stateModified = true;
              log(`修复 ${fix.taskId}: 更正 agent=main`, 'FIX');
            }
            break;
          }
        }
      } catch (e) {
        log(`修复失败 ${fix.taskId}: ${e.message}`, 'ERROR');
      }
    }
    
    // 保存修改
    if (stateModified) {
      safeWriteJSON(this.stateFile, this.state);
      log('已保存任务状态修改', 'SUCCESS');
    }
    
    fixesApplied.total = fixesApplied.taskConfig + fixesApplied.agentAssignment + 
                         fixesApplied.falseCompletion + fixesApplied.timeout;
    
    log(`自动修复完成：应用 ${fixesApplied.total} 个修复`, 'SUCCESS');
    
    return fixesApplied;
  }

  // ============================================================================
  // 生成报告
  // ============================================================================

  generateReport(startTime, fixesApplied = null) {
    const duration = Date.now() - startTime;
    const timestamp = new Date().toISOString();
    const timestampLocal = new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' });
    
    // 计算总体健康分数
    const healthScore = Math.round(
      this.metrics.taskList.score * CONFIG.weights.taskList +
      this.metrics.taskAssignment.score * CONFIG.weights.taskAssignment +
      this.metrics.taskExecution.score * CONFIG.weights.taskExecution +
      this.metrics.agentStatus.score * CONFIG.weights.agentStatus +
      this.metrics.dataConsistency.score * CONFIG.weights.dataConsistency
    );
    
    // 分类统计问题
    const criticalIssues = this.issues.filter(i => i.severity === 'critical').length;
    const highIssues = this.issues.filter(i => i.severity === 'high').length;
    const mediumIssues = this.issues.filter(i => i.severity === 'medium').length;
    const lowIssues = this.issues.filter(i => i.severity === 'low').length;
    
    const report = {
      timestamp,
      timestampLocal,
      projectDir: this.projectDir,
      healthScore,
      duration,
      
      summary: {
        totalIssues: this.issues.length,
        criticalIssues,
        highIssues,
        mediumIssues,
        lowIssues,
        fixesApplied: fixesApplied?.total || 0
      },
      
      metrics: this.metrics,
      
      issues: this.issues,
      
      fixesApplied: fixesApplied || { total: 0 },
      
      recommendations: this.generateRecommendations()
    };
    
    // 保存报告
    safeWriteJSON(this.reportFile, report);
    
    // 生成摘要
    const summary = {
      timestamp,
      timestampLocal,
      projectDir: this.projectDir,
      healthScore,
      duration,
      summary: report.summary,
      taskStatus: this.metrics.taskExecution.details.statusDistribution || {},
      metrics: {
        taskList: {
          score: Math.round(this.metrics.taskList.score),
          status: this.metrics.taskList.score >= 90 ? 'ok' : this.metrics.taskList.score >= 70 ? 'warning' : 'critical',
          issues: this.metrics.taskList.issues.slice(0, 3).join('; ')
        },
        taskAssignment: {
          score: Math.round(this.metrics.taskAssignment.score),
          status: this.metrics.taskAssignment.score >= 90 ? 'ok' : this.metrics.taskAssignment.score >= 70 ? 'warning' : 'critical',
          issues: this.metrics.taskAssignment.issues.slice(0, 3).join('; ')
        },
        taskExecution: {
          score: Math.round(this.metrics.taskExecution.score),
          status: this.metrics.taskExecution.score >= 90 ? 'ok' : this.metrics.taskExecution.score >= 70 ? 'warning' : 'critical',
          issues: this.metrics.taskExecution.issues.slice(0, 3).join('; ')
        },
        agentStatus: {
          score: Math.round(this.metrics.agentStatus.score),
          status: this.metrics.agentStatus.score >= 90 ? 'ok' : this.metrics.agentStatus.score >= 70 ? 'warning' : 'critical',
          issues: this.metrics.agentStatus.issues.slice(0, 3).join('; ')
        },
        dataConsistency: {
          score: Math.round(this.metrics.dataConsistency.score),
          status: this.metrics.dataConsistency.score >= 90 ? 'ok' : this.metrics.dataConsistency.score >= 70 ? 'warning' : 'critical',
          issues: this.metrics.dataConsistency.issues.slice(0, 3).join('; ')
        }
      },
      criticalFindings: this.issues.filter(i => ['critical', 'high'].includes(i.severity)).slice(0, 5),
      nextCheck: new Date(Date.now() + 300000).toISOString(),
      nextCheckLocal: new Date(Date.now() + 300000).toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })
    };
    
    safeWriteJSON(this.summaryFile, summary);
    
    // 输出摘要
    log('='.repeat(80), 'INFO');
    log('健康检查完成', 'SUCCESS');
    log(`健康分数：${healthScore}/100`, healthScore >= 90 ? 'SUCCESS' : healthScore >= 70 ? 'WARN' : 'ERROR');
    log(`发现问题：${this.issues.length} 个 (严重:${criticalIssues}, 高:${highIssues}, 中:${mediumIssues}, 低:${lowIssues})`);
    log(`自动修复：${fixesApplied?.total || 0} 个`);
    log(`耗时：${duration}ms`);
    log('='.repeat(80), 'INFO');
    
    return { report, summary };
  }

  // ============================================================================
  // 生成建议
  // ============================================================================

  generateRecommendations() {
    const recommendations = [];
    
    // 根据问题生成建议
    const hasFalseCompletes = this.issues.some(i => i.type === 'false_completion');
    const hasTimeoutTasks = this.issues.some(i => i.type === 'task_timeout');
    const hasIncompleteConfig = this.issues.some(i => i.type === 'task_config_incomplete');
    const hasUnknownAgents = this.issues.some(i => i.type === 'unknown_agent');
    
    if (hasFalseCompletes) {
      recommendations.push({
        priority: 'high',
        action: '批量重置假完成任务',
        details: '将标记为 completed 但无产出物的任务重置为 pending'
      });
    }
    
    if (hasTimeoutTasks) {
      recommendations.push({
        priority: 'high',
        action: '处理超时任务',
        details: '检查超时任务的 Agent 状态，必要时重启'
      });
    }
    
    if (hasIncompleteConfig) {
      recommendations.push({
        priority: 'medium',
        action: '补充任务配置',
        details: '批量补充缺失的 agent 和 description 字段'
      });
    }
    
    if (hasUnknownAgents) {
      recommendations.push({
        priority: 'medium',
        action: '更正 Agent 分配',
        details: '将分配给未知 Agent 的任务重新分配'
      });
    }
    
    // 如果没有问题
    if (recommendations.length === 0) {
      recommendations.push({
        priority: 'low',
        action: '保持监控',
        details: '系统运行正常，继续定期健康检查'
      });
    }
    
    return recommendations;
  }
}

// ============================================================================
// CLI 入口
// ============================================================================

async function main() {
  const args = process.argv.slice(2);
  
  // 解析参数
  let projectDir = null;
  let quiet = false;
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--project' && args[i + 1]) {
      projectDir = args[++i];
    } else if (args[i] === '--quiet' || args[i] === '-q') {
      quiet = true;
    } else if (args[i] === '--help' || args[i] === '-h') {
      console.log(`
敏捷工作流健康检查器 v2.0

用法：node health-check-v2.js [选项]

选项:
  --project, -p <目录>  项目目录（必需）
  --quiet, -q          安静模式（仅输出摘要）
  --help, -h           显示帮助

示例:
  node health-check-v2.js --project /path/to/project
  node health-check-v2.js -p /path/to/project -q
`);
      process.exit(0);
    }
  }
  
  if (!projectDir) {
    console.error('错误：必须指定项目目录 (--project)');
    process.exit(1);
  }
  
  if (!fs.existsSync(projectDir)) {
    console.error(`错误：项目目录不存在：${projectDir}`);
    process.exit(1);
  }
  
  // 运行检查
  const checker = new HealthCheckerV2(projectDir);
  
  if (quiet) {
    console.log = () => {}; // 禁用日志
  }
  
  try {
    const result = await checker.runFullCheck();
    
    if (quiet) {
      console.log = console.log; // 恢复日志
      console.log(JSON.stringify(result.summary, null, 2));
    }
    
    process.exit(result.summary.healthScore >= 70 ? 0 : 1);
  } catch (e) {
    console.error('健康检查失败:', e.message);
    process.exit(1);
  }
}

// 导出类
module.exports = { HealthCheckerV2, CONFIG };

// 运行 CLI
if (require.main === module) {
  main();
}
