/**
 * AI Agent Team Coordinator
 * 负责协调多个AI代理之间的协作和通信
 */

class AIAgentTeamCoordinator {
  constructor() {
    this.agents = new Map();
    this.activeTasks = new Map();
    this.communicationChannels = new Map();
  }

  /**
   * 注册新代理到团队
   * @param {string} agentId - 代理ID
   * @param {Object} agentConfig - 代理配置
   */
  registerAgent(agentId, agentConfig) {
    this.agents.set(agentId, {
      id: agentId,
      config: agentConfig,
      status: 'active',
      lastActive: Date.now(),
      performance: { tasksCompleted: 0, successRate: 1.0 }
    });
    
    console.log(`✅ 代理 ${agentId} 已注册到团队`);
    return true;
  }

  /**
   * 分配任务给合适的代理
   * @param {Object} task - 任务对象
   * @returns {string} 分配的代理ID
   */
  assignTask(task) {
    const suitableAgents = this.findSuitableAgents(task);
    if (suitableAgents.length === 0) {
      throw new Error('没有合适的代理可以处理此任务');
    }

    // 基于负载均衡选择最佳代理
    const bestAgent = this.selectBestAgent(suitableAgents);
    this.activeTasks.set(task.id, {
      taskId: task.id,
      assignedTo: bestAgent.id,
      startTime: Date.now(),
      status: 'assigned'
    });

    console.log(`📋 任务 ${task.id} 已分配给代理 ${bestAgent.id}`);
    return bestAgent.id;
  }

  /**
   * 查找适合处理任务的代理
   * @param {Object} task - 任务对象
   * @returns {Array} 适合的代理列表
   */
  findSuitableAgents(task) {
    const suitable = [];
    for (const [agentId, agent] of this.agents) {
      if (this.isAgentSuitable(agent, task)) {
        suitable.push(agent);
      }
    }
    return suitable;
  }

  /**
   * 检查代理是否适合处理任务
   * @param {Object} agent - 代理对象
   * @param {Object} task - 任务对象
   * @returns {boolean}
   */
  isAgentSuitable(agent, task) {
    // 检查代理状态
    if (agent.status !== 'active') {
      return false;
    }

    // 检查技能匹配
    const requiredSkills = task.requiredSkills || [];
    const agentSkills = agent.config.skills || [];
    
    for (const skill of requiredSkills) {
      if (!agentSkills.includes(skill)) {
        return false;
      }
    }

    return true;
  }

  /**
   * 基于性能和负载选择最佳代理
   * @param {Array} agents - 代理列表
   * @returns {Object} 最佳代理
   */
  selectBestAgent(agents) {
    return agents.reduce((best, current) => {
      // 优先选择成功率高的代理
      if (current.performance.successRate > best.performance.successRate) {
        return current;
      }
      // 如果成功率相同，选择任务完成数少的（负载更轻）
      if (current.performance.successRate === best.performance.successRate &&
          current.performance.tasksCompleted < best.performance.tasksCompleted) {
        return current;
      }
      return best;
    });
  }

  /**
   * 更新任务状态
   * @param {string} taskId - 任务ID
   * @param {string} status - 新状态
   * @param {Object} result - 任务结果（可选）
   */
  updateTaskStatus(taskId, status, result = null) {
    const task = this.activeTasks.get(taskId);
    if (!task) {
      console.warn(`⚠️ 任务 ${taskId} 未找到`);
      return false;
    }

    task.status = status;
    task.endTime = Date.now();
    task.result = result;

    // 更新代理性能统计
    if (status === 'completed' || status === 'failed') {
      const agent = this.agents.get(task.assignedTo);
      if (agent) {
        agent.performance.tasksCompleted++;
        if (status === 'completed') {
          agent.performance.successRate = 
            (agent.performance.successRate * (agent.performance.tasksCompleted - 1) + 1) / 
            agent.performance.tasksCompleted;
        } else {
          agent.performance.successRate = 
            (agent.performance.successRate * (agent.performance.tasksCompleted - 1)) / 
            agent.performance.tasksCompleted;
        }
        agent.lastActive = Date.now();
      }
    }

    console.log(`🔄 任务 ${taskId} 状态更新为: ${status}`);
    return true;
  }

  /**
   * 获取团队状态报告
   * @returns {Object} 团队状态
   */
  getTeamStatus() {
    const activeAgents = Array.from(this.agents.values())
      .filter(agent => agent.status === 'active');
    
    const totalTasks = this.activeTasks.size;
    const completedTasks = Array.from(this.activeTasks.values())
      .filter(task => task.status === 'completed').length;
    
    const avgSuccessRate = activeAgents.length > 0 
      ? activeAgents.reduce((sum, agent) => sum + agent.performance.successRate, 0) / activeAgents.length
      : 0;

    return {
      totalAgents: this.agents.size,
      activeAgents: activeAgents.length,
      totalTasks: totalTasks,
      completedTasks: completedTasks,
      averageSuccessRate: avgSuccessRate,
      agents: activeAgents.map(agent => ({
        id: agent.id,
        status: agent.status,
        tasksCompleted: agent.performance.tasksCompleted,
        successRate: agent.performance.successRate
      }))
    };
  }

  /**
   * 创建新的通信频道
   * @param {string} channelId - 频道ID
   * @param {Array} participants - 参与者列表
   */
  createCommunicationChannel(channelId, participants) {
    this.communicationChannels.set(channelId, {
      id: channelId,
      participants: participants,
      messages: [],
      createdAt: Date.now()
    });
    console.log(`📡 通信频道 ${channelId} 已创建`);
  }

  /**
   * 发送消息到频道
   * @param {string} channelId - 频道ID
   * @param {string} sender - 发送者
   * @param {string} message - 消息内容
   */
  sendMessageToChannel(channelId, sender, message) {
    const channel = this.communicationChannels.get(channelId);
    if (!channel) {
      throw new Error(`频道 ${channelId} 不存在`);
    }

    channel.messages.push({
      sender: sender,
      content: message,
      timestamp: Date.now()
    });

    // 通知所有参与者
    for (const participant of channel.participants) {
      if (participant !== sender) {
        this.notifyAgent(participant, `来自 ${sender} 的消息: ${message}`);
      }
    }
  }

  /**
   * 通知代理
   * @param {string} agentId - 代理ID
   * @param {string} message - 通知消息
   */
  notifyAgent(agentId, message) {
    const agent = this.agents.get(agentId);
    if (agent) {
      console.log(`🔔 通知 ${agentId}: ${message}`);
      // 这里可以集成实际的通知机制
    }
  }

  /**
   * 移除代理
   * @param {string} agentId - 代理ID
   */
  removeAgent(agentId) {
    if (this.agents.has(agentId)) {
      this.agents.delete(agentId);
      console.log(`❌ 代理 ${agentId} 已从团队移除`);
      return true;
    }
    return false;
  }
}

module.exports = AIAgentTeamCoordinator;