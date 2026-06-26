/**
 * 全局进程管理器 v1.0
 * 
 * 功能：
 * 1. 统一的最大进程数限制
 * 2. 全局 PID 追踪
 * 3. 堆栈记录（启动位置）
 * 4. 孤儿进程清理
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

class GlobalProcessManager {
  constructor() {
    this.MAX_TOTAL_AGENTS = 5;  // 全局最大 agent 进程数
    this.REGISTRY_FILE = '/tmp/openclaw-agent-registry.json';
    this.loadRegistry();
  }

  /**
   * 加载进程注册表
   */
  loadRegistry() {
    try {
      if (fs.existsSync(this.REGISTRY_FILE)) {
        const data = fs.readFileSync(this.REGISTRY_FILE, 'utf8');
        this.registry = JSON.parse(data);
      } else {
        this.registry = { processes: [] };
      }
    } catch (e) {
      this.registry = { processes: [] };
    }
  }

  /**
   * 保存进程注册表
   */
  saveRegistry() {
    try {
      fs.writeFileSync(this.REGISTRY_FILE, JSON.stringify(this.registry, null, 2));
    } catch (e) {
      console.error('保存进程注册表失败:', e.message);
    }
  }

  /**
   * 获取当前 openclaw-agent 进程数
   */
  getCurrentProcessCount() {
    try {
      const output = execSync('pgrep -f "openclaw-agent" || echo ""', { encoding: 'utf8' });
      const pids = output.trim().split('\n').filter(p => p);
      return pids.length;
    } catch (e) {
      return 0;
    }
  }

  /**
   * 检查是否可以启动新进程
   */
  canSpawnNewProcess() {
    const current = this.getCurrentProcessCount();
    if (current >= this.MAX_TOTAL_AGENTS) {
      console.log(`⚠️ 全局进程数已达上限 (${current}/${this.MAX_TOTAL_AGENTS})，拒绝启动新进程`);
      return false;
    }
    return true;
  }

  /**
   * 注册进程
   */
  registerProcess(pid, agentName, source) {
    const stack = new Error().stack;
    const stackLine = stack.split('\n')[2] || 'unknown';
    
    this.registry.processes.push({
      pid,
      agentName,
      source,
      stack: stackLine.trim(),
      startTime: new Date().toISOString()
    });
    
    this.saveRegistry();
    console.log(`📝 注册进程: PID=${pid}, Agent=${agentName}, 来源=${source}`);
  }

  /**
   * 注销进程
   */
  unregisterProcess(pid) {
    const index = this.registry.processes.findIndex(p => p.pid === pid);
    if (index > -1) {
      this.registry.processes.splice(index, 1);
      this.saveRegistry();
      console.log(`🗑️ 注销进程: PID=${pid}`);
    }
  }

  /**
   * 清理孤儿进程
   */
  cleanupOrphanProcesses() {
    const activePids = [];
    
    // 获取当前活跃的进程
    try {
      const output = execSync('pgrep -f "openclaw-agent" || echo ""', { encoding: 'utf8' });
      const pids = output.trim().split('\n').filter(p => p);
      activePids.push(...pids.map(p => parseInt(p)));
    } catch (e) {}

    // 清理注册表中不存在的进程
    const before = this.registry.processes.length;
    this.registry.processes = this.registry.processes.filter(p => {
      return activePids.includes(p.pid);
    });
    const after = this.registry.processes.length;
    
    if (before !== after) {
      console.log(`🧹 清理 ${before - after} 个孤儿进程记录`);
      this.saveRegistry();
    }

    // 如果实际进程数超过限制，杀死最老的
    if (activePids.length > this.MAX_TOTAL_AGENTS) {
      const toKill = activePids.length - this.MAX_TOTAL_AGENTS;
      console.log(`⚠️ 进程数超限 (${activePids.length}/${this.MAX_TOTAL_AGENTS})，杀死 ${toKill} 个最老的进程`);
      
      for (let i = 0; i < toKill; i++) {
        const oldestPid = this.registry.processes[0]?.pid || activePids[i];
        try {
          process.kill(oldestPid, 'SIGKILL');
          console.log(`🔪 杀死进程: PID=${oldestPid}`);
        } catch (e) {}
      }
    }

    return activePids.length;
  }

  /**
   * 获取状态报告
   */
  getStatus() {
    const current = this.getCurrentProcessCount();
    return {
      currentProcesses: current,
      maxAllowed: this.MAX_TOTAL_AGENTS,
      registered: this.registry.processes.length,
      canSpawn: current < this.MAX_TOTAL_AGENTS,
      processes: this.registry.processes
    };
  }
}

// 单例导出
const globalProcessManager = new GlobalProcessManager();

module.exports = { GlobalProcessManager, globalProcessManager };
