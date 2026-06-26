#!/usr/bin/env node
const { globalProcessManager } = require('./global-process-manager.js');
/**
 * Agent 守护进程 v7.12
 * 
 * 核心功能:
 * 1. 每分钟检查 Agent 状态
 * 2. 自动重启停止的 Agent
 * 3. 发送告警通知
 */

const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

class AgentSupervisor {
  constructor(config = {}) {
    this.workspace = config.workspace || '/home/ubutu/.openclaw/workspace';
    this.agentsDir = path.join(this.workspace, '../agents');
    this.checkInterval = config.checkInterval || 60000;  // 1 分钟
    this.agents = ['novel_architect', 'novel_writer', 'novel_editor'];
    this.alerts = [];
  }

  /**
   * 启动守护
   */
  startSupervising() {
    console.log('🔒 Agent 守护进程已启动');
    console.log(`监控 Agent: ${this.agents.join(', ')}`);
    
    setInterval(() => {
      this.checkAllAgents();
    }, this.checkInterval);
    
    // 立即执行一次
    this.checkAllAgents();
  }

  /**
   * 检查所有 Agent
   */
  checkAllAgents() {
    for (const agentName of this.agents) {
      this.checkAgent(agentName);
    }
  }

  /**
   * 检查单个 Agent
   */
  checkAgent(agentName) {
    const isRunning = this.isAgentRunning(agentName);
    const hasTasks = this.hasPendingTasks(agentName);
    
    if (!isRunning && hasTasks) {
      console.log(`⚠️ ${agentName} 已停止但有待执行任务，正在重启...`);
      this.restartAgent(agentName);
    } else if (isRunning) {
      console.log(`✅ ${agentName} 运行正常`);
    }
  }

  /**
   * 检查 Agent 是否运行
   */
  isAgentRunning(agentName) {
    return new Promise((resolve) => {
      exec(`pgrep -f "openclaw.*${agentName}"`, (error, stdout) => {
        resolve(!error && stdout.trim().length > 0);
      });
    });
  }

  /**
   * 检查是否有待执行任务
   */
  hasPendingTasks(agentName) {
    const queueFile = path.join(this.agentsDir, agentName, 'tasks', 'QUEUE.md');
    
    if (!fs.existsSync(queueFile)) {
      return false;
    }
    
    const content = fs.readFileSync(queueFile, 'utf8');
    
    // 检查是否有"进行中"或"待执行"任务
    return content.includes('🚀 进行中') || 
           content.includes('⏳ 待执行') ||
           content.includes('🔴 待补全');
  }

  /**
   * 重启 Agent
   */
  restartAgent(agentName) {
    const queueFile = path.join(this.agentsDir, agentName, 'tasks', 'QUEUE.md');
    let project = '未知项目';
    
    if (fs.existsSync(queueFile)) {
      const content = fs.readFileSync(queueFile, 'utf8');
      const match = content.match(/\*\*项目\*\*: (.+)/);
      if (match) {
        project = match[1].trim();
      }
    }
    
    const command = `cd ${this.workspace} && /home/ubutu/.npm-global/bin/openclaw agent --local --agent ${agentName} --thinking minimal -m "检查任务队列并执行待办任务" >> ${this.workspace}/logs/agent-supervisor.log 2>&1 &`;
    
    // 🔒 全局进程数检查
    if (!globalProcessManager.canSpawnNewProcess()) {
      console.log('⚠️ 全局进程数已达上限，跳过重启');
      return;
    }
    
    exec(command, (error, stdout, stderr) => {
      if (error) {
        this.alert(`${agentName} 重启失败`, { error: error.message });
      } else {
        this.alert(`${agentName} 已重启`, { project: project });
        console.log(`✅ ${agentName} 重启成功`);
      }
    });
  }

  /**
   * 发送告警
   */
  alert(type, details) {
    const alert = {
      type,
      details,
      timestamp: new Date().toISOString()
    };
    
    this.alerts.push(alert);
    
    console.log(`⚠️ 告警：${type}`, details);
    
    // 记录到日志
    this.logAlert(alert);
  }

  /**
   * 记录告警日志
   */
  logAlert(alert) {
    const logFile = path.join(this.workspace, 'logs', 'agent-supervisor.log');
    const log = `[${alert.timestamp}] ${alert.type}: ${JSON.stringify(alert.details)}\n`;
    fs.appendFileSync(logFile, log);
  }

  /**
   * 获取告警历史
   */
  getAlerts(limit = 10) {
    return this.alerts.slice(-limit);
  }
}

module.exports = AgentSupervisor;

// CLI 入口
if (require.main === module) {
  const supervisor = new AgentSupervisor();
  supervisor.startSupervising();
  
  console.log('Agent 守护进程运行中... (Ctrl+C 停止)');
}
