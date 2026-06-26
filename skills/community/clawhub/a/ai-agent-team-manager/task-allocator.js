/**
 * AI Agent Team Manager - Task Allocator
 * 智能任务分配系统，基于代理能力和工作负载进行优化分配
 */

class TaskAllocator {
  constructor() {
    this.agents = new Map();
    this.taskQueue = [];
    this.performanceMetrics = new Map();
  }

  /**
   * 注册AI代理
   * @param {string} agentId - 代理ID
   * @param {Object} capabilities - 代理能力描述
   * @param {number} maxConcurrentTasks - 最大并发任务数
   */
  registerAgent(agentId, capabilities, maxConcurrentTasks = 3) {
    this.agents.set(agentId, {
      id: agentId,
      capabilities: capabilities,
      maxConcurrentTasks: maxConcurrentTasks,
      currentTasks: 0,
      successRate: 1.0,
      avgResponseTime: 0,
      lastActive: Date.now()
    });
  }

  /**
   * 分配任务给最适合的代理
   * @param {Object} task - 任务对象
   * @returns {string|null} 分配的代理ID
   */
  allocateTask(task) {
    const suitableAgents = this.findSuitableAgents(task);
    if (suitableAgents.length === 0) {
      return null;
    }

    // 基于多因素选择最佳代理
    const bestAgent = this.selectBestAgent(suitableAgents, task);
    
    if (bestAgent) {
      this.assignTaskToAgent(bestAgent.id, task);
      return bestAgent.id;
    }
    
    return null;
  }

  /**
   * 查找适合任务的代理
   * @param {Object} task - 任务对象
   * @returns {Array} 适合的代理列表
   */
  findSuitableAgents(task) {
    const suitable = [];
    
    for (const [agentId, agent] of this.agents) {
      // 检查能力匹配
      if (this.canHandleTask(agent, task)) {
        // 检查负载
        if (agent.currentTasks < agent.maxConcurrentTasks) {
          suitable.push(agent);
        }
      }
    }
    
    return suitable;
  }

  /**
   * 检查代理是否能处理任务
   * @param {Object} agent - 代理对象
   * @param {Object} task - 任务对象
   * @returns {boolean}
   */
  canHandleTask(agent, task) {
    const requiredSkills = task.requiredSkills || [];
    const agentSkills = agent.capabilities.skills || [];
    
    // 检查是否具备所有必需技能
    return requiredSkills.every(skill => 
      agentSkills.includes(skill) || 
      this.isSkillCompatible(skill, agentSkills)
    );
  }

  /**
   * 检查技能兼容性
   * @param {string} requiredSkill - 需要的技能
   * @param {Array} availableSkills - 可用技能列表
   * @returns {boolean}
   */
  isSkillCompatible(requiredSkill, availableSkills) {
    // 技能兼容性映射
    const compatibilityMap = {
      'content-writing': ['blog-writing', 'copywriting', 'seo-content'],
      'data-analysis': ['financial-analysis', 'market-research'],
      'web-development': ['frontend', 'backend', 'fullstack'],
      'security-audit': ['vulnerability-scanning', 'compliance-check']
    };
    
    if (compatibilityMap[requiredSkill]) {
      return compatibilityMap[requiredSkill].some(skill => 
        availableSkills.includes(skill)
      );
    }
    
    return false;
  }

  /**
   * 选择最佳代理（基于性能、负载、响应时间）
   * @param {Array} agents - 代理列表
   * @param {Object} task - 任务对象
   * @returns {Object} 最佳代理
   */
  selectBestAgent(agents, task) {
    return agents.reduce((best, agent) => {
      const score = this.calculateAgentScore(agent, task);
      const bestScore = best ? this.calculateAgentScore(best, task) : -Infinity;
      
      return score > bestScore ? agent : best;
    }, null);
  }

  /**
   * 计算代理评分
   * @param {Object} agent - 代理对象
   * @param {Object} task - 任务对象
   * @returns {number} 评分
   */
  calculateAgentScore(agent, task) {
    const loadFactor = 1 - (agent.currentTasks / agent.maxConcurrentTasks);
    const performanceFactor = agent.successRate;
    const responseTimeFactor = Math.max(0, 1 - (agent.avgResponseTime / 10000)); // 10秒为基准
    
    // 任务紧急度影响
    const urgencyFactor = task.urgency === 'high' ? 1.2 : 
                         task.urgency === 'medium' ? 1.0 : 0.8;
    
    return (loadFactor * 0.4 + performanceFactor * 0.3 + responseTimeFactor * 0.3) * urgencyFactor;
  }

  /**
   * 分配任务给代理
   * @param {string} agentId - 代理ID
   * @param {Object} task - 任务对象
   */
  assignTaskToAgent(agentId, task) {
    const agent = this.agents.get(agentId);
    if (agent) {
      agent.currentTasks++;
      agent.lastActive = Date.now();
      
      // 记录任务分配
      console.log(`Task ${task.id} assigned to agent ${agentId}`);
    }
  }

  /**
   * 任务完成回调
   * @param {string} agentId - 代理ID
   * @param {Object} task - 任务对象
   * @param {boolean} success - 是否成功
   * @param {number} responseTime - 响应时间（毫秒）
   */
  onTaskComplete(agentId, task, success, responseTime) {
    const agent = this.agents.get(agentId);
    if (agent) {
      agent.currentTasks = Math.max(0, agent.currentTasks - 1);
      
      // 更新性能指标
      this.updatePerformanceMetrics(agent, success, responseTime);
    }
  }

  /**
   * 更新性能指标
   * @param {Object} agent - 代理对象
   * @param {boolean} success - 是否成功
   * @param {number} responseTime - 响应时间
   */
  updatePerformanceMetrics(agent, success, responseTime) {
    // 更新成功率（滑动平均）
    agent.successRate = agent.successRate * 0.9 + (success ? 1 : 0) * 0.1;
    
    // 更新平均响应时间（滑动平均）
    agent.avgResponseTime = agent.avgResponseTime * 0.9 + responseTime * 0.1;
  }

  /**
   * 获取团队状态报告
   * @returns {Object} 团队状态
   */
  getTeamStatus() {
    const totalAgents = this.agents.size;
    const activeAgents = Array.from(this.agents.values())
      .filter(agent => agent.currentTasks > 0).length;
    const totalTasks = Array.from(this.agents.values())
      .reduce((sum, agent) => sum + agent.currentTasks, 0);
    
    return {
      totalAgents,
      activeAgents,
      totalTasks,
      averageSuccessRate: this.getAverageSuccessRate(),
      averageResponseTime: this.getAverageResponseTime()
    };
  }

  /**
   * 获取平均成功率
   * @returns {number}
   */
  getAverageSuccessRate() {
    if (this.agents.size === 0) return 0;
    const total = Array.from(this.agents.values())
      .reduce((sum, agent) => sum + agent.successRate, 0);
    return total / this.agents.size;
  }

  /**
   * 获取平均响应时间
   * @returns {number}
   */
  getAverageResponseTime() {
    if (this.agents.size === 0) return 0;
    const total = Array.from(this.agents.values())
      .reduce((sum, agent) => sum + agent.avgResponseTime, 0);
    return total / this.agents.size;
  }
}

module.exports = TaskAllocator;