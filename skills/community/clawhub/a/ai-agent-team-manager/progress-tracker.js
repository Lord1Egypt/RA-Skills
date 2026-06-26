/**
 * AI Agent Team Manager - Progress Tracker Module
 * 
 * 跟踪AI代理团队的工作进度，提供实时状态更新和性能指标
 */

class ProgressTracker {
  constructor() {
    this.tasks = new Map();
    this.agents = new Map();
    this.metrics = {
      completedTasks: 0,
      failedTasks: 0,
      avgCompletionTime: 0,
      successRate: 0
    };
  }

  /**
   * 初始化任务跟踪
   * @param {string} taskId - 任务ID
   * @param {Object} taskInfo - 任务信息
   */
  initializeTask(taskId, taskInfo) {
    this.tasks.set(taskId, {
      id: taskId,
      name: taskInfo.name,
      description: taskInfo.description,
      assignedAgent: taskInfo.assignedAgent,
      status: 'pending',
      startTime: null,
      endTime: null,
      progress: 0,
      milestones: taskInfo.milestones || [],
      currentMilestone: 0,
      logs: []
    });
  }

  /**
   * 更新任务状态
   * @param {string} taskId - 任务ID
   * @param {string} status - 状态 ('pending', 'in_progress', 'completed', 'failed')
   * @param {number} progress - 进度百分比 (0-100)
   */
  updateTaskStatus(taskId, status, progress = 0) {
    const task = this.tasks.get(taskId);
    if (!task) {
      console.warn(`Task ${taskId} not found`);
      return;
    }

    task.status = status;
    task.progress = progress;

    if (status === 'in_progress' && !task.startTime) {
      task.startTime = new Date().toISOString();
    }

    if (status === 'completed' || status === 'failed') {
      task.endTime = new Date().toISOString();
      this.updateMetrics(task);
    }

    this.logTaskActivity(taskId, `Status updated to: ${status}, Progress: ${progress}%`);
  }

  /**
   * 记录里程碑完成
   * @param {string} taskId - 任务ID
   * @param {number} milestoneIndex - 里程碑索引
   */
  completeMilestone(taskId, milestoneIndex) {
    const task = this.tasks.get(taskId);
    if (!task) return;

    if (milestoneIndex >= task.milestones.length) {
      console.warn(`Invalid milestone index ${milestoneIndex} for task ${taskId}`);
      return;
    }

    task.currentMilestone = milestoneIndex + 1;
    const milestone = task.milestones[milestoneIndex];
    this.logTaskActivity(taskId, `Milestone completed: ${milestone.name}`);
  }

  /**
   * 注册代理信息
   * @param {string} agentId - 代理ID
   * @param {Object} agentInfo - 代理信息
   */
  registerAgent(agentId, agentInfo) {
    this.agents.set(agentId, {
      id: agentId,
      name: agentInfo.name,
      role: agentInfo.role,
      capabilities: agentInfo.capabilities,
      currentTasks: [],
      performance: {
        completedTasks: 0,
        failedTasks: 0,
        avgResponseTime: 0
      }
    });
  }

  /**
   * 分配任务给代理
   * @param {string} taskId - 任务ID
   * @param {string} agentId - 代理ID
   */
  assignTaskToAgent(taskId, agentId) {
    const task = this.tasks.get(taskId);
    const agent = this.agents.get(agentId);

    if (!task || !agent) {
      console.warn(`Task ${taskId} or agent ${agentId} not found`);
      return;
    }

    task.assignedAgent = agentId;
    agent.currentTasks.push(taskId);
    this.logTaskActivity(taskId, `Assigned to agent: ${agent.name}`);
  }

  /**
   * 获取任务详细状态
   * @param {string} taskId - 任务ID
   * @returns {Object} 任务状态详情
   */
  getTaskStatus(taskId) {
    return this.tasks.get(taskId) || null;
  }

  /**
   * 获取所有任务摘要
   * @returns {Object} 任务摘要信息
   */
  getAllTasksSummary() {
    const summary = {
      totalTasks: this.tasks.size,
      pending: 0,
      inProgress: 0,
      completed: 0,
      failed: 0,
      tasks: []
    };

    for (const task of this.tasks.values()) {
      switch (task.status) {
        case 'pending':
          summary.pending++;
          break;
        case 'in_progress':
          summary.inProgress++;
          break;
        case 'completed':
          summary.completed++;
          break;
        case 'failed':
          summary.failed++;
          break;
      }

      summary.tasks.push({
        id: task.id,
        name: task.name,
        status: task.status,
        progress: task.progress,
        assignedAgent: task.assignedAgent,
        startTime: task.startTime,
        endTime: task.endTime
      });
    }

    return summary;
  }

  /**
   * 获取代理性能报告
   * @param {string} agentId - 代理ID
   * @returns {Object} 代理性能报告
   */
  getAgentPerformance(agentId) {
    const agent = this.agents.get(agentId);
    if (!agent) return null;

    return {
      id: agent.id,
      name: agent.name,
      role: agent.role,
      currentTasks: agent.currentTasks.length,
      completedTasks: agent.performance.completedTasks,
      failedTasks: agent.performance.failedTasks,
      successRate: agent.performance.completedTasks > 0 ? 
        (agent.performance.completedTasks / (agent.performance.completedTasks + agent.performance.failedTasks)) * 100 : 0,
      avgResponseTime: agent.performance.avgResponseTime
    };
  }

  /**
   * 获取团队整体性能
   * @returns {Object} 团队性能报告
   */
  getTeamPerformance() {
    let totalCompleted = 0;
    let totalFailed = 0;
    let totalResponseTime = 0;
    let activeAgents = 0;

    for (const agent of this.agents.values()) {
      totalCompleted += agent.performance.completedTasks;
      totalFailed += agent.performance.failedTasks;
      totalResponseTime += agent.performance.avgResponseTime;
      if (agent.currentTasks.length > 0) {
        activeAgents++;
      }
    }

    const totalTasks = totalCompleted + totalFailed;
    const successRate = totalTasks > 0 ? (totalCompleted / totalTasks) * 100 : 0;
    const avgResponseTime = this.agents.size > 0 ? totalResponseTime / this.agents.size : 0;

    return {
      totalAgents: this.agents.size,
      activeAgents: activeAgents,
      totalTasks: totalTasks,
      completedTasks: totalCompleted,
      failedTasks: totalFailed,
      successRate: successRate,
      avgResponseTime: avgResponseTime,
      teamEfficiency: this.calculateTeamEfficiency()
    };
  }

  /**
   * 计算团队效率评分
   * @returns {number} 效率评分 (0-100)
   */
  calculateTeamEfficiency() {
    const performance = this.getTeamPerformance();
    // 综合考虑成功率、响应时间和活跃度
    const successWeight = 0.5;
    const responseWeight = 0.3;
    const activityWeight = 0.2;

    const successScore = performance.successRate;
    const responseScore = Math.max(0, 100 - (performance.avgResponseTime / 1000)); // 假设响应时间以毫秒为单位
    const activityScore = (performance.activeAgents / performance.totalAgents) * 100;

    return (successScore * successWeight) + (responseScore * responseWeight) + (activityScore * activityWeight);
  }

  /**
   * 记录任务活动日志
   * @param {string} taskId - 任务ID
   * @param {string} activity - 活动描述
   */
  logTaskActivity(taskId, activity) {
    const task = this.tasks.get(taskId);
    if (!task) return;

    task.logs.push({
      timestamp: new Date().toISOString(),
      activity: activity
    });

    // 限制日志数量，避免内存溢出
    if (task.logs.length > 100) {
      task.logs = task.logs.slice(-100);
    }
  }

  /**
   * 生成进度报告
   * @param {string} format - 报告格式 ('json', 'markdown', 'html')
   * @returns {string} 格式化的进度报告
   */
  generateProgressReport(format = 'json') {
    const summary = this.getAllTasksSummary();
    const teamPerformance = this.getTeamPerformance();

    switch (format) {
      case 'json':
        return JSON.stringify({
          summary: summary,
          teamPerformance: teamPerformance,
          timestamp: new Date().toISOString()
        }, null, 2);

      case 'markdown':
        return this.generateMarkdownReport(summary, teamPerformance);

      case 'html':
        return this.generateHtmlReport(summary, teamPerformance);

      default:
        return JSON.stringify({ error: 'Unsupported format' });
    }
  }

  /**
   * 生成Markdown格式报告
   */
  generateMarkdownReport(summary, teamPerformance) {
    return `
# AI Agent Team Progress Report

**Generated:** ${new Date().toISOString()}

## Team Performance
- **Total Agents:** ${teamPerformance.totalAgents}
- **Active Agents:** ${teamPerformance.activeAgents}
- **Success Rate:** ${teamPerformance.successRate.toFixed(2)}%
- **Team Efficiency:** ${teamPerformance.teamEfficiency.toFixed(2)}%
- **Average Response Time:** ${teamPerformance.avgResponseTime.toFixed(2)}ms

## Task Summary
- **Total Tasks:** ${summary.totalTasks}
- **Completed:** ${summary.completed}
- **In Progress:** ${summary.inProgress}
- **Pending:** ${summary.pending}
- **Failed:** ${summary.failed}

## Current Tasks
${summary.tasks.map(task => `- **${task.name}**: ${task.status} (${task.progress}%) - Assigned to: ${task.assignedAgent}`).join('\n')}

---
*Report generated by AI Agent Team Manager*
`;
  }

  /**
   * 生成HTML格式报告
   */
  generateHtmlReport(summary, teamPerformance) {
    return `
<!DOCTYPE html>
<html>
<head>
    <title>AI Agent Team Progress Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .section { margin-bottom: 20px; }
        .metric { display: inline-block; margin-right: 20px; }
        .task-item { margin: 5px 0; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <h1>AI Agent Team Progress Report</h1>
    <p><strong>Generated:</strong> ${new Date().toISOString()}</p>

    <div class="section">
        <h2>Team Performance</h2>
        <div class="metric"><strong>Total Agents:</strong> ${teamPerformance.totalAgents}</div>
        <div class="metric"><strong>Active Agents:</strong> ${teamPerformance.activeAgents}</div>
        <div class="metric"><strong>Success Rate:</strong> ${teamPerformance.successRate.toFixed(2)}%</div>
        <div class="metric"><strong>Team Efficiency:</strong> ${teamPerformance.teamEfficiency.toFixed(2)}%</div>
        <div class="metric"><strong>Avg Response Time:</strong> ${teamPerformance.avgResponseTime.toFixed(2)}ms</div>
    </div>

    <div class="section">
        <h2>Task Summary</h2>
        <div class="metric"><strong>Total Tasks:</strong> ${summary.totalTasks}</div>
        <div class="metric"><strong>Completed:</strong> ${summary.completed}</div>
        <div class="metric"><strong>In Progress:</strong> ${summary.inProgress}</div>
        <div class="metric"><strong>Pending:</strong> ${summary.pending}</div>
        <div class="metric"><strong>Failed:</strong> ${summary.failed}</div>
    </div>

    <div class="section">
        <h2>Current Tasks</h2>
        <table>
            <thead>
                <tr>
                    <th>Task Name</th>
                    <th>Status</th>
                    <th>Progress</th>
                    <th>Assigned Agent</th>
                </tr>
            </thead>
            <tbody>
                ${summary.tasks.map(task => `
                <tr>
                    <td>${task.name}</td>
                    <td>${task.status}</td>
                    <td>${task.progress}%</td>
                    <td>${task.assignedAgent}</td>
                </tr>
                `).join('')}
            </tbody>
        </table>
    </div>
</body>
</html>
`;
  }

  /**
   * 导出进度数据
   * @param {string} filePath - 导出文件路径
   * @param {string} format - 导出格式
   */
  async exportProgressData(filePath, format = 'json') {
    const report = this.generateProgressReport(format);
    // 这里需要集成文件系统操作
    console.log(`Exporting progress data to ${filePath} in ${format} format`);
    return report;
  }
}

module.exports = ProgressTracker;