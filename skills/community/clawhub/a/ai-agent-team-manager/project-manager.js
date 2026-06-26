/**
 * AI Agent Team Manager - Project Manager Module
 * 
 * 负责AI代理团队的项目管理，包括任务分解、进度跟踪、资源分配等
 */

class ProjectManager {
  constructor() {
    this.projects = new Map();
    this.tasks = new Map();
    this.agents = new Map();
  }

  /**
   * 创建新项目
   * @param {Object} projectConfig - 项目配置
   * @param {string} projectConfig.name - 项目名称
   * @param {string} projectConfig.description - 项目描述
   * @param {Array} projectConfig.teamMembers - 团队成员列表
   * @param {Object} projectConfig.deadlines - 截止日期配置
   */
  createProject(projectConfig) {
    const projectId = this.generateProjectId();
    const project = {
      id: projectId,
      name: projectConfig.name,
      description: projectConfig.description,
      status: 'active',
      createdAt: new Date().toISOString(),
      teamMembers: projectConfig.teamMembers || [],
      deadlines: projectConfig.deadlines || {},
      milestones: [],
      tasks: [],
      metrics: {
        completionRate: 0,
        qualityScore: 0,
        efficiency: 0
      }
    };
    
    this.projects.set(projectId, project);
    return projectId;
  }

  /**
   * 分解项目为任务
   * @param {string} projectId - 项目ID
   * @param {Array} taskList - 任务列表
   */
  decomposeProject(projectId, taskList) {
    const project = this.projects.get(projectId);
    if (!project) {
      throw new Error(`Project ${projectId} not found`);
    }

    const tasks = taskList.map(task => {
      const taskId = this.generateTaskId();
      const taskObj = {
        id: taskId,
        projectId: projectId,
        title: task.title,
        description: task.description,
        status: 'pending',
        priority: task.priority || 'medium',
        assignee: task.assignee || null,
        dependencies: task.dependencies || [],
        estimatedTime: task.estimatedTime || 0,
        actualTime: 0,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      };
      
      this.tasks.set(taskId, taskObj);
      project.tasks.push(taskId);
      return taskId;
    });

    this.projects.set(projectId, project);
    return tasks;
  }

  /**
   * 分配任务给代理
   * @param {string} taskId - 任务ID
   * @param {string} agentId - 代理ID
   */
  assignTask(taskId, agentId) {
    const task = this.tasks.get(taskId);
    if (!task) {
      throw new Error(`Task ${taskId} not found`);
    }

    task.assignee = agentId;
    task.status = 'assigned';
    task.updatedAt = new Date().toISOString();
    this.tasks.set(taskId, task);

    // 更新代理的任务列表
    if (!this.agents.has(agentId)) {
      this.agents.set(agentId, {
        id: agentId,
        tasks: [],
        performance: {
          completedTasks: 0,
          averageQuality: 0,
          efficiency: 0
        }
      });
    }

    const agent = this.agents.get(agentId);
    agent.tasks.push(taskId);
    this.agents.set(agentId, agent);

    return true;
  }

  /**
   * 更新任务状态
   * @param {string} taskId - 任务ID
   * @param {string} status - 新状态
   * @param {Object} updates - 其他更新信息
   */
  updateTaskStatus(taskId, status, updates = {}) {
    const task = this.tasks.get(taskId);
    if (!task) {
      throw new Error(`Task ${taskId} not found`);
    }

    task.status = status;
    task.updatedAt = new Date().toISOString();
    
    // 应用其他更新
    Object.keys(updates).forEach(key => {
      task[key] = updates[key];
    });

    this.tasks.set(taskId, task);
    
    // 如果任务完成，更新项目进度
    if (status === 'completed') {
      this.updateProjectProgress(task.projectId);
    }

    return true;
  }

  /**
   * 更新项目进度
   * @param {string} projectId - 项目ID
   */
  updateProjectProgress(projectId) {
    const project = this.projects.get(projectId);
    if (!project) {
      throw new Error(`Project ${projectId} not found`);
    }

    const totalTasks = project.tasks.length;
    if (totalTasks === 0) {
      project.metrics.completionRate = 100;
    } else {
      const completedTasks = project.tasks.filter(taskId => {
        const task = this.tasks.get(taskId);
        return task && task.status === 'completed';
      }).length;
      
      project.metrics.completionRate = (completedTasks / totalTasks) * 100;
    }

    this.projects.set(projectId, project);
    return project.metrics.completionRate;
  }

  /**
   * 获取项目报告
   * @param {string} projectId - 项目ID
   */
  getProjectReport(projectId) {
    const project = this.projects.get(projectId);
    if (!project) {
      throw new Error(`Project ${projectId} not found`);
    }

    const report = {
      projectName: project.name,
      status: project.status,
      completionRate: project.metrics.completionRate,
      teamPerformance: [],
      taskBreakdown: [],
      recommendations: []
    };

    // 团队绩效
    project.teamMembers.forEach(agentId => {
      const agent = this.agents.get(agentId);
      if (agent) {
        report.teamPerformance.push({
          agentId: agentId,
          completedTasks: agent.performance.completedTasks,
          averageQuality: agent.performance.averageQuality,
          efficiency: agent.performance.efficiency
        });
      }
    });

    // 任务分解
    project.tasks.forEach(taskId => {
      const task = this.tasks.get(taskId);
      if (task) {
        report.taskBreakdown.push({
          taskId: taskId,
          title: task.title,
          status: task.status,
          assignee: task.assignee,
          priority: task.priority
        });
      }
    });

    // 建议
    if (project.metrics.completionRate < 50) {
      report.recommendations.push('项目进度较慢，建议增加资源或调整优先级');
    }
    if (project.metrics.completionRate > 90) {
      report.recommendations.push('项目接近完成，准备验收和交付');
    }

    return report;
  }

  /**
   * 生成项目ID
   */
  generateProjectId() {
    return `proj_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  /**
   * 生成任务ID
   */
  generateTaskId() {
    return `task_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  /**
   * 导出项目数据
   * @param {string} projectId - 项目ID
   */
  exportProjectData(projectId) {
    const project = this.projects.get(projectId);
    if (!project) {
      throw new Error(`Project ${projectId} not found`);
    }

    const exportData = {
      project: project,
      tasks: project.tasks.map(taskId => this.tasks.get(taskId)),
      agents: project.teamMembers.map(agentId => this.agents.get(agentId))
    };

    return JSON.stringify(exportData, null, 2);
  }
}

module.exports = ProjectManager;