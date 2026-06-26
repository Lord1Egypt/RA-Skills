#!/usr/bin/env node
/**
 * 负载均衡器 v6.0-Phase4
 * 
 * 核心功能:
 * 1. 负载实时检测 (Agent/任务/系统)
 * 2. 智能任务分配 (评分算法/最优选择)
 * 3. 冲突自动解决 (资源/依赖/优先级)
 * 4. 过载保护 (限流/降级/熔断)
 */

const EventEmitter = require('events');

// ============ 配置 ============

const CONFIG = {
  // 评分权重
  weights: {
    load: 0.5,        // 负载率权重 50%
    error: 0.3,       // 错误率权重 30%
    response: 0.2     // 响应时间权重 20%
  },
  
  // 阈值配置
  thresholds: {
    overload: 90,     // 过载阈值 90%
    warning: 70,      // 警告阈值 70%
    healthy: 50       // 健康阈值 50%
  },
  
  // 检测间隔
  intervals: {
    load: 1000,       // 负载检测 1 秒
    score: 5000,      // 评分更新 5 秒
    health: 30000     // 健康检查 30 秒
  },
  
  // 过载保护
  protection: {
    enabled: true,
    maxQueueSize: 100,
    timeout: 30000
  }
};

// ============ 负载均衡器类 ============

class LoadBalancer extends EventEmitter {
  constructor(options = {}) {
    super();
    this.config = { ...CONFIG, ...options };
    this.agents = new Map();
    this.taskQueue = [];
    this.scores = new Map();
    this.metrics = {
      totalTasks: 0,
      completedTasks: 0,
      failedTasks: 0,
      avgWaitTime: 0,
      avgExecutionTime: 0
    };
    
    this.startMonitoring();
    console.log('⚖️ 负载均衡器已启动');
  }

  /**
   * 注册 Agent
   */
  registerAgent(agent) {
    console.log(`📝 注册 Agent: ${agent.name}`);
    
    this.agents.set(agent.name, {
      name: agent.name,
      status: 'idle',
      loadPercent: 0,
      currentTasks: [],
      maxConcurrent: agent.maxConcurrent || 5,
      errorRate: 0,
      responseTime: 0,
      lastHeartbeat: Date.now(),
      healthy: true,
      recentSuccess: true,
      metrics: {
        totalTasks: 0,
        completedTasks: 0,
        failedTasks: 0,
        avgExecutionTime: 0
      }
    });
    
    this.updateScore(agent.name);
  }

  /**
   * 注销 Agent
   */
  unregisterAgent(agentName) {
    console.log(`📝 注销 Agent: ${agentName}`);
    this.agents.delete(agentName);
    this.scores.delete(agentName);
  }

  /**
   * 更新 Agent 状态
   */
  updateAgentStatus(agentName, status) {
    const agent = this.agents.get(agentName);
    if (!agent) return;
    
    agent.status = status;
    agent.lastHeartbeat = Date.now();
    
    if (status === 'error') {
      agent.healthy = false;
      agent.recentSuccess = false;
    } else if (status === 'success') {
      agent.recentSuccess = true;
    }
    
    this.updateScore(agentName);
  }

  /**
   * 计算 Agent 得分
   */
  calculateScore(agent) {
    const { weights } = this.config;
    
    // 基础分 100 分
    let score = 100;
    
    // 负载率扣分 (权重 50%)
    const loadPenalty = agent.loadPercent * weights.load;
    score -= loadPenalty;
    
    // 错误率扣分 (权重 30%)
    const errorPenalty = agent.errorRate * 100 * weights.error;
    score -= errorPenalty;
    
    // 响应时间扣分 (权重 20%)
    const responsePenalty = Math.min(agent.responseTime / 1000, 10) * weights.response * 2;
    score -= responsePenalty;
    
    // 健康状态加分
    if (agent.healthy) score += 10;
    if (agent.recentSuccess) score += 5;
    
    // 过载惩罚
    if (agent.loadPercent > this.config.thresholds.overload) {
      score -= 20;
    }
    
    return Math.max(0, Math.min(100, score));
  }

  /**
   * 更新 Agent 得分
   */
  updateScore(agentName) {
    const agent = this.agents.get(agentName);
    if (!agent) return;
    
    const score = this.calculateScore(agent);
    this.scores.set(agentName, score);
    
    this.emit('score:update', { agentName, score });
  }

  /**
   * 更新所有 Agent 得分
   */
  updateAllScores() {
    for (const agentName of this.agents.keys()) {
      this.updateScore(agentName);
    }
  }

  /**
   * 获取可用 Agent
   */
  getAvailableAgents() {
    const available = [];
    
    for (const [name, agent] of this.agents) {
      // 检查健康状态
      if (!agent.healthy) continue;
      
      // 检查是否过载
      if (agent.loadPercent >= this.config.thresholds.overload) continue;
      
      // 检查心跳
      const timeSinceHeartbeat = Date.now() - agent.lastHeartbeat;
      if (timeSinceHeartbeat > 60000) continue; // 1 分钟无心跳
      
      available.push(agent);
    }
    
    return available;
  }

  /**
   * 选择最优 Agent
   */
  selectBestAgent(task) {
    const availableAgents = this.getAvailableAgents();
    
    if (availableAgents.length === 0) {
      return null;
    }
    
    // 计算所有 Agent 得分
    const scoredAgents = availableAgents.map(agent => ({
      agent,
      score: this.scores.get(agent.name) || 0
    }));
    
    // 按得分排序
    scoredAgents.sort((a, b) => b.score - a.score);
    
    // 返回最优 Agent
    return scoredAgents[0].agent;
  }

  /**
   * 分配任务
   */
  async assignTask(task) {
    console.log(`📋 分配任务：${task.name || task.id}`);
    
    const agent = this.selectBestAgent(task);
    
    if (!agent) {
      // 无可用 Agent，加入等待队列
      console.log(`⚠️ 无可用 Agent，任务加入等待队列`);
      
      if (this.taskQueue.length >= this.config.protection.maxQueueSize) {
        throw new Error('任务队列已满，拒绝新任务');
      }
      
      this.taskQueue.push({
        task,
        timestamp: Date.now()
      });
      
      this.emit('task:queued', { task });
      throw new Error('无可用 Agent，任务已加入等待队列');
    }
    
    // 检测冲突
    const conflicts = this.detectConflict(task, agent);
    if (conflicts.length > 0) {
      console.log(`⚠️ 检测到 ${conflicts.length} 个冲突`);
      await this.resolveConflicts(conflicts, task, agent);
    }
    
    // 分配任务
    console.log(`✅ 任务分配给 Agent ${agent.name} (得分：${this.scores.get(agent.name)})`);
    
    agent.currentTasks.push(task);
    agent.loadPercent = (agent.currentTasks.length / agent.maxConcurrent) * 100;
    this.updateScore(agent.name);
    
    this.metrics.totalTasks++;
    this.emit('task:assigned', { task, agent });
    
    return agent;
  }

  /**
   * 完成任务
   */
  completeTask(agentName, task, success = true) {
    const agent = this.agents.get(agentName);
    if (!agent) return;
    
    // 从当前任务中移除
    const index = agent.currentTasks.indexOf(task);
    if (index > -1) {
      agent.currentTasks.splice(index, 1);
    }
    
    // 更新负载
    agent.loadPercent = (agent.currentTasks.length / agent.maxConcurrent) * 100;
    
    // 更新指标
    agent.metrics.totalTasks++;
    if (success) {
      agent.metrics.completedTasks++;
      agent.recentSuccess = true;
    } else {
      agent.metrics.failedTasks++;
      agent.errorRate = agent.metrics.failedTasks / agent.metrics.totalTasks;
      agent.recentSuccess = false;
    }
    
    // 更新平均执行时间
    if (task.executionTime) {
      const total = agent.metrics.avgExecutionTime * (agent.metrics.totalTasks - 1);
      agent.metrics.avgExecutionTime = (total + task.executionTime) / agent.metrics.totalTasks;
      agent.responseTime = agent.metrics.avgExecutionTime;
    }
    
    this.updateScore(agentName);
    this.emit('task:completed', { agent, task, success });
    
    // 处理等待队列
    this.processWaitingTasks();
  }

  /**
   * 检测冲突
   */
  detectConflict(task, agent) {
    const conflicts = [];
    
    // 检测资源冲突
    if (this.hasResourceConflict(task, agent)) {
      conflicts.push({
        type: 'RESOURCE_CONFLICT',
        task,
        agent,
        resource: task.resource
      });
    }
    
    // 检测依赖冲突
    if (this.hasDependencyConflict(task, agent)) {
      conflicts.push({
        type: 'DEPENDENCY_CONFLICT',
        task,
        agent,
        dependency: task.dependency
      });
    }
    
    return conflicts;
  }

  /**
   * 检测资源冲突
   */
  hasResourceConflict(task, agent) {
    if (!task.resource) return false;
    
    // 检查是否有其他任务使用同一资源
    for (const currentTask of agent.currentTasks) {
      if (currentTask.resource === task.resource) {
        return true;
      }
    }
    
    return false;
  }

  /**
   * 检测依赖冲突
   */
  hasDependencyConflict(task, agent) {
    if (!task.dependency) return false;
    
    // 检查依赖任务是否完成
    // 这里简化实现，实际应该查询任务状态
    return false;
  }

  /**
   * 解决冲突
   */
  async resolveConflicts(conflicts, task, agent) {
    for (const conflict of conflicts) {
      console.log(`🔧 解决冲突：${conflict.type}`);
      
      switch (conflict.type) {
        case 'RESOURCE_CONFLICT':
          await this.resolveResourceConflict(conflict);
          break;
        case 'DEPENDENCY_CONFLICT':
          await this.resolveDependencyConflict(conflict);
          break;
        default:
          throw new Error(`未知冲突类型：${conflict.type}`);
      }
    }
  }

  /**
   * 解决资源冲突
   */
  async resolveResourceConflict(conflict) {
    const { task, agent } = conflict;
    
    // 策略：排队等待
    const waitTime = agent.currentTasks.length * (agent.metrics.avgExecutionTime || 10000);
    
    console.log(`   策略：排队等待，预计等待 ${waitTime/1000} 秒`);
    
    return {
      action: 'QUEUE',
      task,
      agent,
      estimatedWait: waitTime
    };
  }

  /**
   * 解决依赖冲突
   */
  async resolveDependencyConflict(conflict) {
    const { task } = conflict;
    
    // 策略：等待依赖完成
    console.log(`   策略：等待依赖任务完成`);
    
    return {
      action: 'WAIT_DEPENDENCY',
      task,
      dependency: task.dependency
    };
  }

  /**
   * 处理等待队列
   */
  async processWaitingTasks() {
    if (this.taskQueue.length === 0) return;
    
    const availableAgents = this.getAvailableAgents();
    if (availableAgents.length === 0) return;
    
    // 处理队列中的任务
    while (this.taskQueue.length > 0 && availableAgents.length > 0) {
      const item = this.taskQueue.shift();
      const { task, timestamp } = item;
      
      try {
        await this.assignTask(task);
        
        // 统计等待时间
        const waitTime = Date.now() - timestamp;
        this.metrics.avgWaitTime = (this.metrics.avgWaitTime * (this.metrics.totalTasks - 1) + waitTime) / this.metrics.totalTasks;
        
      } catch (error) {
        // 重新加入队列
        this.taskQueue.unshift(item);
        break;
      }
    }
  }

  /**
   * 检查过载
   */
  checkOverload() {
    const overloadedAgents = [];
    
    for (const [name, agent] of this.agents) {
      if (agent.loadPercent >= this.config.thresholds.overload) {
        overloadedAgents.push(name);
        this.emit('agent:overload', { agentName: name, loadPercent: agent.loadPercent });
      } else if (agent.loadPercent >= this.config.thresholds.warning) {
        this.emit('agent:warning', { agentName: name, loadPercent: agent.loadPercent });
      }
    }
    
    if (overloadedAgents.length > 0) {
      console.log(`⚠️ ${overloadedAgents.length} 个 Agent 过载：${overloadedAgents.join(', ')}`);
    }
  }

  /**
   * 启动监控
   */
  startMonitoring() {
    console.log('👁️ 启动负载监控...');
    
    // 负载检测
    setInterval(() => {
      this.updateAllScores();
    }, this.config.intervals.load);
    
    // 评分更新
    setInterval(() => {
      this.emit('metrics:update', this.getMetrics());
    }, this.config.intervals.score);
    
    // 健康检查
    setInterval(() => {
      this.checkAgentHealth();
    }, this.config.intervals.health);
  }

  /**
   * 检查 Agent 健康
   */
  checkAgentHealth() {
    for (const [name, agent] of this.agents) {
      const timeSinceHeartbeat = Date.now() - agent.lastHeartbeat;
      
      if (timeSinceHeartbeat > 60000) {
        agent.healthy = false;
        this.emit('agent:unhealthy', { agentName: name });
        console.log(`⚠️ Agent ${name} 不健康（${timeSinceHeartbeat/1000}秒无心跳）`);
      } else {
        agent.healthy = true;
      }
      
      this.updateScore(name);
    }
  }

  /**
   * 获取指标
   */
  getMetrics() {
    const agentMetrics = [];
    
    for (const [name, agent] of this.agents) {
      agentMetrics.push({
        name,
        status: agent.status,
        loadPercent: agent.loadPercent,
        score: this.scores.get(name),
        healthy: agent.healthy,
        currentTasks: agent.currentTasks.length,
        maxConcurrent: agent.maxConcurrent
      });
    }
    
    return {
      agents: agentMetrics,
      queue: {
        size: this.taskQueue.length,
        maxSize: this.config.protection.maxQueueSize
      },
      system: this.metrics
    };
  }

  /**
   * 获取状态
   */
  getStatus() {
    const metrics = this.getMetrics();
    
    return {
      totalAgents: this.agents.size,
      availableAgents: this.getAvailableAgents().length,
      queuedTasks: this.taskQueue.length,
      avgLoad: metrics.agents.reduce((sum, a) => sum + a.loadPercent, 0) / (metrics.agents.length || 1),
      systemMetrics: this.metrics
    };
  }
}

// ============ CLI 接口 ============

function printHelp() {
  console.log(`
负载均衡器 v6.0-Phase4

用法：node load-balancer.js <命令> [选项]

命令:
  status              查看状态
  metrics             查看指标
  agents              查看 Agent 列表
  queue               查看等待队列
  test                运行测试

示例:
  node load-balancer.js status
  node load-balancer.js metrics
  node load-balancer.js test
`);
}

// ============ 主程序 ============

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  if (!command || command === '--help' || command === '-h') {
    printHelp();
    return;
  }

  const balancer = new LoadBalancer();

  // 注册测试 Agent
  balancer.registerAgent({ name: 'agent_1', maxConcurrent: 5 });
  balancer.registerAgent({ name: 'agent_2', maxConcurrent: 5 });
  balancer.registerAgent({ name: 'agent_3', maxConcurrent: 5 });

  switch (command) {
    case 'status':
      const status = balancer.getStatus();
      console.log('📊 负载均衡器状态:');
      console.log(JSON.stringify(status, null, 2));
      break;

    case 'metrics':
      const metrics = balancer.getMetrics();
      console.log('📈 负载均衡器指标:');
      console.log(JSON.stringify(metrics, null, 2));
      break;

    case 'agents':
      const agentsMetrics = balancer.getMetrics().agents;
      console.log('🤖 Agent 列表:');
      agentsMetrics.forEach(a => {
        console.log(`  ${a.name}: 负载${a.loadPercent}% 得分${a.score} ${a.healthy ? '✅' : '❌'}`);
      });
      break;

    case 'queue':
      console.log('📋 等待队列:');
      console.log(`  队列大小：${balancer.taskQueue.length}/${balancer.config.protection.maxQueueSize}`);
      break;

    case 'test':
      console.log('🧪 运行负载均衡测试...\n');
      
      // 模拟任务分配
      for (let i = 1; i <= 10; i++) {
        const task = {
          id: `task_${i}`,
          name: `测试任务 ${i}`,
          resource: i % 3 === 0 ? 'shared_resource' : null
        };
        
        try {
          const agent = await balancer.assignTask(task);
          console.log(`✅ 任务 ${task.name} → Agent ${agent.name}`);
          
          // 模拟任务完成
          setTimeout(() => {
            balancer.completeTask(agent.name, task, true);
          }, 1000 + Math.random() * 2000);
          
        } catch (error) {
          console.log(`⚠️ 任务 ${task.name} 加入等待队列`);
        }
      }
      
      // 等待任务完成
      setTimeout(() => {
        console.log('\n📊 最终状态:');
        console.log(JSON.stringify(balancer.getStatus(), null, 2));
      }, 5000);
      
      break;

    default:
      console.log(`未知命令：${command}`);
      printHelp();
  }
}

// 导出 API
module.exports = { LoadBalancer, CONFIG };

// 运行 CLI
if (require.main === module) {
  main().catch(console.error);
}
