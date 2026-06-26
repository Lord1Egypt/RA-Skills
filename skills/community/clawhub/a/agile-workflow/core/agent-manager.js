#!/usr/bin/env node
/**
 * Agent 动态伸缩管理器 v5.1
 * 
 * 核心功能:
 * 1. Agent 状态管理（活跃/空闲/休眠/离线）
 * 2. 按需启动（分配任务时检查并启动）
 * 3. 空闲释放（10 分钟无任务自动释放）
 * 4. 健康监控（心跳/日志/进程）
 */

const fs = require('fs');
const path = require('path');
const { execSync, spawn } = require('child_process');

// ============ 配置 ============

const CONFIG = {
  workspace: '/home/ubutu/.openclaw/workspace',
  logsDir: '/home/ubutu/.openclaw/workspace/logs/agent-manager',
  stateFile: '/home/ubutu/.openclaw/workspace/logs/agent-manager/agent-states.json',
  agentsDir: '/home/ubutu/.openclaw/workspace/agents',
  
  // 超时配置
  idleToSleep: 5 * 60 * 1000,       // 5 分钟空闲→休眠
  idleToOffline: 10 * 60 * 1000,    // 10 分钟空闲→离线
  heartbeatInterval: 30000,          // 30 秒心跳检测
  startupTimeout: 30000,             // 启动超时 30 秒
  
  // 资源限制
  maxConcurrentAgents: 5,            // 最大同时运行 Agent 数
  minIdleAgents: 1,                  // 最小空闲 Agent 数
  
  // Agent 配置
  agents: {
    'chapter_writer': {
      command: 'node agents/chapter-writer.js',
      port: 3001,
      autoStart: false
    },
    'world_builder': {
      command: 'node agents/world-builder.js',
      port: 3002,
      autoStart: false
    },
    'character_designer': {
      command: 'node agents/character-designer.js',
      port: 3003,
      autoStart: false
    },
    'outline_generator': {
      command: 'node agents/outline-generator.js',
      port: 3004,
      autoStart: false
    },
    'novel_architect': {
      command: 'node agents/novel-architect.js',
      port: 3005,
      autoStart: false
    }
  }
};

// ============ Agent 状态管理器 ============

class AgentStateManager {
  constructor(config = {}) {
    this.states = this.loadStates();
    this.ensureDirs();
    
    // 只在守护进程模式下启动定时器
    if (config.daemonMode) {
      this.startMonitoring();
    }
  }

  ensureDirs() {
    fs.mkdirSync(CONFIG.logsDir, { recursive: true });
  }

  loadStates() {
    if (fs.existsSync(CONFIG.stateFile)) {
      return JSON.parse(fs.readFileSync(CONFIG.stateFile, 'utf-8'));
    }
    
    // 初始化所有 Agent 状态
    const states = {};
    for (const [name, config] of Object.entries(CONFIG.agents)) {
      states[name] = {
        name,
        status: 'offline',  // offline/sleeping/idle/active
        pid: null,
        port: config.port,
        currentTask: null,
        lastTaskTime: null,
        startedAt: null,
        idleTime: 0,
        health: {
          heartbeat: null,
          memory: 0,
          cpu: 0,
          errors: 0
        },
        stats: {
          totalTasks: 0,
          successRate: 100,
          avgDuration: 0,
          totalUptime: 0
        }
      };
    }
    
    return states;
  }

  saveStates() {
    fs.writeFileSync(CONFIG.stateFile, JSON.stringify(this.states, null, 2));
  }

  // ============ 状态查询 ============

  getAgentState(agentName) {
    return this.states[agentName] || null;
  }

  getAllStates() {
    return this.states;
  }

  getActiveAgents() {
    return Object.values(this.states).filter(s => s.status === 'active');
  }

  getIdleAgents() {
    return Object.values(this.states).filter(s => s.status === 'idle' || s.status === 'sleeping');
  }

  getOfflineAgents() {
    return Object.values(this.states).filter(s => s.status === 'offline');
  }

  // ============ 状态转换 ============

  updateAgentState(agentName, updates) {
    if (!this.states[agentName]) {
      console.error(`❌ Agent ${agentName} 不存在`);
      return false;
    }

    const oldStatus = this.states[agentName].status;
    Object.assign(this.states[agentName], updates);
    
    // 状态变化时记录日志
    if (updates.status && updates.status !== oldStatus) {
      console.log(`📊 Agent ${agentName} 状态变化：${oldStatus} → ${updates.status}`);
      this.logStateChange(agentName, oldStatus, updates.status);
    }

    this.saveStates();
    return true;
  }

  logStateChange(agentName, oldStatus, newStatus) {
    const logFile = path.join(CONFIG.logsDir, 'state-changes.log');
    const log = `[${new Date().toISOString()}] ${agentName}: ${oldStatus} → ${newStatus}\n`;
    fs.appendFileSync(logFile, log);
  }

  // ============ Agent 生命周期管理 ============

  /**
   * 启动 Agent
   */
  async startAgent(agentName) {
    const state = this.states[agentName];
    if (!state) {
      throw new Error(`Agent ${agentName} 不存在`);
    }

    if (state.status !== 'offline' && state.status !== 'sleeping') {
      console.log(`⚠️ Agent ${agentName} 已在运行 (${state.status})`);
      return state;
    }

    console.log(`🚀 启动 Agent ${agentName}...`);

    const config = CONFIG.agents[agentName];
    if (!config) {
      throw new Error(`Agent ${agentName} 配置不存在`);
    }

    try {
      // 启动进程
      const [cmd, ...args] = config.command.split(' ');
      const child = spawn(cmd, args, {
        cwd: CONFIG.workspace,
        stdio: ['ignore', 'pipe', 'pipe'],
        detached: false
      });

      state.pid = child.pid;
      state.status = 'starting';
      state.startedAt = Date.now();
      this.saveStates();

      // 等待启动完成
      await this.waitForStartup(agentName);

      // 验证健康
      const healthy = await this.verifyHealth(agentName);
      if (!healthy) {
        throw new Error(`Agent ${agentName} 启动后健康检查失败`);
      }

      state.status = 'idle';
      this.saveStates();

      console.log(`✅ Agent ${agentName} 启动成功 (PID: ${child.pid})`);
      return state;

    } catch (error) {
      console.error(`❌ Agent ${agentName} 启动失败：${error.message}`);
      state.status = 'offline';
      state.pid = null;
      this.saveStates();
      throw error;
    }
  }

  /**
   * 停止 Agent
   */
  async stopAgent(agentName, graceful = true) {
    const state = this.states[agentName];
    if (!state || state.status === 'offline') {
      console.log(`⚠️ Agent ${agentName} 已离线`);
      return;
    }

    console.log(`🛑 停止 Agent ${agentName}...`);

    if (graceful) {
      // 优雅关闭：等待当前任务完成
      if (state.status === 'active') {
        console.log(`⏳ 等待 Agent ${agentName} 完成当前任务...`);
        await this.waitForTaskComplete(agentName, 10000);
      }

      // 备份状态
      await this.backupState(agentName);
    }

    // 发送终止信号
    if (state.pid) {
      try {
        process.kill(state.pid, 'SIGTERM');
        console.log(`✅ Agent ${agentName} 已停止 (PID: ${state.pid})`);
      } catch (error) {
        console.warn(`⚠️ 停止 Agent ${agentName} 失败：${error.message}`);
      }
    }

    state.status = 'offline';
    state.pid = null;
    state.currentTask = null;
    this.saveStates();
  }

  /**
   * 休眠 Agent（保留状态，快速恢复）
   */
  async sleepAgent(agentName) {
    const state = this.states[agentName];
    if (!state || state.status === 'offline') {
      return;
    }

    console.log(`💤 Agent ${agentName} 进入休眠...`);

    // 保存状态到文件
    await this.backupState(agentName);

    // 暂停进程（SIGSTOP）
    if (state.pid) {
      try {
        process.kill(state.pid, 'SIGSTOP');
      } catch (error) {
        console.warn(`⚠️ 休眠 Agent ${agentName} 失败：${error.message}`);
      }
    }

    state.status = 'sleeping';
    this.saveStates();
  }

  /**
   * 唤醒 Agent
   */
  async wakeupAgent(agentName) {
    const state = this.states[agentName];
    if (!state || state.status !== 'sleeping') {
      return;
    }

    console.log(`☀️ 唤醒 Agent ${agentName}...`);

    // 恢复进程（SIGCONT）
    if (state.pid) {
      try {
        process.kill(state.pid, 'SIGCONT');
      } catch (error) {
        console.warn(`⚠️ 唤醒 Agent ${agentName} 失败：${error.message}`);
      }
    }

    state.status = 'idle';
    this.saveStates();
  }

  // ============ 任务管理 ============

  /**
   * 分配任务给 Agent
   */
  async assignTask(agentName, task) {
    const state = this.states[agentName];
    if (!state) {
      throw new Error(`Agent ${agentName} 不存在`);
    }

    console.log(`📋 分配任务给 Agent ${agentName}: ${task.name}`);

    // 1. 检查状态，必要时启动
    if (state.status === 'offline') {
      await this.startAgent(agentName);
    } else if (state.status === 'sleeping') {
      await this.wakeupAgent(agentName);
    }

    // 2. 分配任务
    state.status = 'active';
    state.currentTask = task;
    state.lastTaskTime = Date.now();
    state.stats.totalTasks++;
    this.saveStates();

    console.log(`✅ 任务已分配给 Agent ${agentName}`);
    return state;
  }

  /**
   * 完成任务
   */
  completeTask(agentName, success = true) {
    const state = this.states[agentName];
    if (!state) return;

    console.log(`✅ Agent ${agentName} 完成任务`);

    state.status = 'idle';
    state.currentTask = null;
    state.lastTaskTime = Date.now();

    if (!success) {
      state.health.errors++;
    }

    this.saveStates();
  }

  // ============ 健康监控 ============

  /**
   * 验证 Agent 健康
   */
  async verifyHealth(agentName) {
    const state = this.states[agentName];
    if (!state) return false;

    // 1. 检查进程
    if (state.pid) {
      try {
        process.kill(state.pid, 0); // 检查进程是否存在
      } catch {
        return false;
      }
    }

    // 2. 检查心跳
    if (state.health.heartbeat) {
      const now = Date.now();
      const diff = now - state.health.heartbeat;
      if (diff > CONFIG.heartbeatInterval * 2) {
        return false;
      }
    }

    return true;
  }

  /**
   * 更新心跳
   */
  updateHeartbeat(agentName) {
    const state = this.states[agentName];
    if (!state) return;

    state.health.heartbeat = Date.now();
    this.saveStates();
  }

  // ============ 空闲检测 ============

  /**
   * 检测并处理空闲 Agent
   */
  async detectIdleAgents() {
    const now = Date.now();
    let changes = 0;

    for (const [agentName, state] of Object.entries(this.states)) {
      if (state.status !== 'idle' || !state.lastTaskTime) continue;

      const idleTime = now - state.lastTaskTime;

      if (idleTime >= CONFIG.idleToOffline) {
        // 1 小时空闲→释放
        console.log(`⏰ Agent ${agentName} 空闲 1 小时，释放资源...`);
        await this.stopAgent(agentName, true);
        changes++;
      } else if (idleTime >= CONFIG.idleToSleep) {
        // 30 分钟空闲→休眠
        console.log(`⏰ Agent ${agentName} 空闲 30 分钟，进入休眠...`);
        await this.sleepAgent(agentName);
        changes++;
      }
    }

    if (changes > 0) {
      console.log(`✅ 处理了 ${changes} 个空闲 Agent`);
    }

    return changes;
  }

  // ============ 辅助方法 ============

  async waitForStartup(agentName, timeout = CONFIG.startupTimeout) {
    const start = Date.now();
    while (Date.now() - start < timeout) {
      const healthy = await this.verifyHealth(agentName);
      if (healthy) return true;
      await new Promise(r => setTimeout(r, 1000));
    }
    throw new Error(`Agent ${agentName} 启动超时`);
  }

  async waitForTaskComplete(agentName, timeout = 10000) {
    const start = Date.now();
    while (Date.now() - start < timeout) {
      const state = this.states[agentName];
      if (!state || state.status !== 'active') return;
      await new Promise(r => setTimeout(r, 1000));
    }
  }

  async backupState(agentName) {
    const state = this.states[agentName];
    if (!state) return;

    const backupFile = path.join(
      CONFIG.logsDir,
      `backup-${agentName}-${Date.now()}.json`
    );
    fs.writeFileSync(backupFile, JSON.stringify(state, null, 2));
    console.log(`💾 Agent ${agentName} 状态已备份：${backupFile}`);
  }

  startMonitoring() {
    // 每分钟检测一次空闲 Agent
    setInterval(() => {
      this.detectIdleAgents();
    }, 60000);

    // 每 30 秒检查一次心跳
    setInterval(() => {
      this.checkHeartbeats();
    }, CONFIG.heartbeatInterval);

    console.log('✅ Agent 监控已启动');
  }

  checkHeartbeats() {
    const now = Date.now();
    for (const [agentName, state] of Object.entries(this.states)) {
      if (state.status === 'offline') continue;

      if (state.health.heartbeat) {
        const diff = now - state.health.heartbeat;
        if (diff > CONFIG.heartbeatInterval * 3) {
          console.warn(`⚠️ Agent ${agentName} 心跳丢失 (${Math.round(diff/1000)}秒)`);
          this.recoverAgent(agentName);
        }
      }
    }
  }

  async recoverAgent(agentName) {
    const state = this.states[agentName];
    if (!state) return;

    console.log(`🔄 尝试恢复 Agent ${agentName}...`);

    // 停止旧进程
    if (state.pid) {
      try {
        process.kill(state.pid, 'SIGKILL');
      } catch {}
    }

    // 重启
    state.status = 'offline';
    state.pid = null;
    this.saveStates();

    try {
      await this.startAgent(agentName);
      console.log(`✅ Agent ${agentName} 恢复成功`);
    } catch (error) {
      console.error(`❌ Agent ${agentName} 恢复失败：${error.message}`);
    }
  }

  // ============ 统计信息 ============

  getStats() {
    const stats = {
      total: Object.keys(this.states).length,
      active: 0,
      idle: 0,
      sleeping: 0,
      offline: 0,
      totalMemory: 0,
      totalCpu: 0
    };

    for (const state of Object.values(this.states)) {
      stats[state.status]++;
      stats.totalMemory += state.health.memory;
      stats.totalCpu += state.health.cpu;
    }

    return stats;
  }

  printStatus() {
    const stats = this.getStats();
    console.log('\n📊 Agent 状态统计:');
    console.log(`总计：${stats.total}`);
    console.log(`活跃：${stats.active}`);
    console.log(`空闲：${stats.idle}`);
    console.log(`休眠：${stats.sleeping}`);
    console.log(`离线：${stats.offline}`);
    console.log(`内存：${(stats.totalMemory / 1024).toFixed(1)} MB`);
    console.log(`CPU: ${stats.totalCpu}%\n`);
  }
}

// ============ CLI 接口 ============

function printHelp() {
  console.log(`
Agent 动态伸缩管理器 v5.1

用法：node agent-manager.js <命令> [选项]

命令:
  start <Agent>       启动指定 Agent
  stop <Agent>        停止指定 Agent
  status              查看所有 Agent 状态
  stats               查看统计信息
  assign <Agent> <任务> 分配任务
  idle-check          手动检测空闲 Agent

示例:
  node agent-manager.js start chapter_writer
  node agent-manager.js status
  node agent-manager.js assign chapter_writer "第 1 章创作"
`);
}

// ============ 主程序 ============

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  if (!command || command === '--help') {
    printHelp();
    return;
  }

  const manager = new AgentStateManager();

  switch (command) {
    case 'start':
      const agentName = args[1];
      if (!agentName) {
        console.log('❌ 请指定 Agent 名称');
        return;
      }
      await manager.startAgent(agentName);
      break;

    case 'stop':
      const stopAgent = args[1];
      if (!stopAgent) {
        console.log('❌ 请指定 Agent 名称');
        return;
      }
      await manager.stopAgent(stopAgent);
      break;

    case 'status':
      manager.printStatus();
      console.log('详细状态:');
      for (const [name, state] of Object.entries(manager.states)) {
        console.log(`  ${name}: ${state.status} (PID: ${state.pid || '-'})`);
      }
      process.exit(0);
      break;

    case 'stats':
      const stats = manager.getStats();
      console.log(JSON.stringify(stats, null, 2));
      process.exit(0);
      break;

    case 'assign':
      const assignAgent = args[1];
      const taskName = args[2] || '测试任务';
      if (!assignAgent) {
        console.log('❌ 请指定 Agent 名称');
        process.exit(1);
      }
      await manager.assignTask(assignAgent, { name: taskName });
      process.exit(0);
      break;

    case 'idle-check':
      await manager.detectIdleAgents();
      process.exit(0);
      break;

    default:
      console.log(`未知命令：${command}`);
      printHelp();
      process.exit(1);
  }
}

// 导出 API
module.exports = { AgentStateManager, CONFIG };

// 运行 CLI
if (require.main === module) {
  main().catch(console.error);
}
