// AI Agent Team Manager - Workflow Manager
// 管理复杂的多代理工作流和任务依赖关系

const fs = require('fs');
const path = require('path');

class WorkflowManager {
  constructor() {
    this.workflows = new Map();
    this.activeWorkflows = new Map();
  }

  // 创建新的工作流
  createWorkflow(workflowConfig) {
    const workflowId = `wf_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    
    const workflow = {
      id: workflowId,
      name: workflowConfig.name || 'Untitled Workflow',
      description: workflowConfig.description || '',
      createdAt: new Date().toISOString(),
      steps: workflowConfig.steps || [],
      dependencies: workflowConfig.dependencies || {},
      parallelTasks: workflowConfig.parallelTasks || false,
      maxRetries: workflowConfig.maxRetries || 3,
      timeout: workflowConfig.timeout || 3600000, // 1 hour default
      status: 'created',
      results: {},
      errors: []
    };
    
    this.workflows.set(workflowId, workflow);
    return workflowId;
  }

  // 验证工作流配置
  validateWorkflow(workflowConfig) {
    const issues = [];
    
    if (!workflowConfig.steps || !Array.isArray(workflowConfig.steps)) {
      issues.push('Workflow must have steps array');
    }
    
    if (workflowConfig.steps.length === 0) {
      issues.push('Workflow must have at least one step');
    }
    
    // 验证每个步骤
    workflowConfig.steps.forEach((step, index) => {
      if (!step.id) {
        issues.push(`Step ${index} missing id`);
      }
      if (!step.agentId) {
        issues.push(`Step ${index} (${step.id}) missing agentId`);
      }
      if (!step.task) {
        issues.push(`Step ${index} (${step.id}) missing task`);
      }
      
      // 验证依赖关系
      if (step.dependsOn) {
        if (!Array.isArray(step.dependsOn)) {
          issues.push(`Step ${index} (${step.id}) dependsOn must be array`);
        } else {
          step.dependsOn.forEach(dep => {
            const depExists = workflowConfig.steps.some(s => s.id === dep);
            if (!depExists) {
              issues.push(`Step ${index} (${step.id}) depends on non-existent step ${dep}`);
            }
          });
        }
      }
    });
    
    // 检测循环依赖
    const dependencyGraph = new Map();
    workflowConfig.steps.forEach(step => {
      dependencyGraph.set(step.id, step.dependsOn || []);
    });
    
    if (this.hasCircularDependency(dependencyGraph)) {
      issues.push('Workflow has circular dependencies');
    }
    
    return issues;
  }

  // 检测循环依赖
  hasCircularDependency(graph) {
    const visited = new Set();
    const recursionStack = new Set();
    
    for (const node of graph.keys()) {
      if (this.isCyclicUtil(node, visited, recursionStack, graph)) {
        return true;
      }
    }
    return false;
  }

  isCyclicUtil(node, visited, recursionStack, graph) {
    if (!visited.has(node)) {
      visited.add(node);
      recursionStack.add(node);
      
      const neighbors = graph.get(node) || [];
      for (const neighbor of neighbors) {
        if (!visited.has(neighbor) && this.isCyclicUtil(neighbor, visited, recursionStack, graph)) {
          return true;
        } else if (recursionStack.has(neighbor)) {
          return true;
        }
      }
    }
    recursionStack.delete(node);
    return false;
  }

  // 执行工作流
  async executeWorkflow(workflowId, context = {}) {
    const workflow = this.workflows.get(workflowId);
    if (!workflow) {
      throw new Error(`Workflow ${workflowId} not found`);
    }
    
    // 验证工作流状态
    if (workflow.status === 'running') {
      throw new Error(`Workflow ${workflowId} is already running`);
    }
    
    workflow.status = 'running';
    workflow.startedAt = new Date().toISOString();
    workflow.context = context;
    this.activeWorkflows.set(workflowId, workflow);
    
    try {
      const result = await this.executeWorkflowSteps(workflow);
      workflow.status = 'completed';
      workflow.completedAt = new Date().toISOString();
      workflow.results = result;
      return result;
    } catch (error) {
      workflow.status = 'failed';
      workflow.failedAt = new Date().toISOString();
      workflow.errors.push({
        timestamp: new Date().toISOString(),
        error: error.message,
        stack: error.stack
      });
      throw error;
    } finally {
      this.activeWorkflows.delete(workflowId);
    }
  }

  // 执行工作流步骤
  async executeWorkflowSteps(workflow) {
    const results = {};
    const completedSteps = new Set();
    
    // 找到所有没有依赖的步骤（入口点）
    const entrySteps = workflow.steps.filter(step => 
      !step.dependsOn || step.dependsOn.length === 0
    );
    
    // 并行执行入口步骤
    const entryPromises = entrySteps.map(step => 
      this.executeStep(step, workflow, results, completedSteps)
    );
    
    await Promise.all(entryPromises);
    
    // 继续执行剩余步骤
    let remainingSteps = workflow.steps.filter(step => !completedSteps.has(step.id));
    let iterations = 0;
    const maxIterations = workflow.steps.length * 2; // 防止无限循环
    
    while (remainingSteps.length > 0 && iterations < maxIterations) {
      iterations++;
      
      const readySteps = remainingSteps.filter(step => {
        if (!step.dependsOn) return true;
        return step.dependsOn.every(dep => completedSteps.has(dep));
      });
      
      if (readySteps.length === 0) {
        // 检查是否有死锁
        const allDependencies = new Set();
        remainingSteps.forEach(step => {
          if (step.dependsOn) {
            step.dependsOn.forEach(dep => allDependencies.add(dep));
          }
        });
        
        const unresolvedDeps = Array.from(allDependencies).filter(dep => 
          !completedSteps.has(dep) && !remainingSteps.some(s => s.id === dep)
        );
        
        if (unresolvedDeps.length > 0) {
          throw new Error(`Unresolved dependencies: ${unresolvedDeps.join(', ')}`);
        }
        
        // 可能是并行任务，继续等待
        await new Promise(resolve => setTimeout(resolve, 100));
        remainingSteps = workflow.steps.filter(step => !completedSteps.has(step.id));
        continue;
      }
      
      // 执行就绪的步骤
      const stepPromises = readySteps.map(step => 
        this.executeStep(step, workflow, results, completedSteps)
      );
      
      await Promise.all(stepPromises);
      remainingSteps = workflow.steps.filter(step => !completedSteps.has(step.id));
    }
    
    if (remainingSteps.length > 0) {
      throw new Error(`Workflow execution timed out or deadlocked. Remaining steps: ${remainingSteps.map(s => s.id).join(', ')}`);
    }
    
    return results;
  }

  // 执行单个步骤
  async executeStep(step, workflow, results, completedSteps) {
    const stepId = step.id;
    const maxRetries = step.maxRetries || workflow.maxRetries || 3;
    let lastError = null;
    
    for (let attempt = 1; attempt <= maxRetries; attempt++) {
      try {
        // 准备步骤上下文
        const stepContext = {
          ...workflow.context,
          stepId: stepId,
          stepName: step.name,
          attempt: attempt,
          previousResults: results,
          workflowId: workflow.id
        };
        
        // 调用代理执行任务
        const stepResult = await this.callAgent(step.agentId, step.task, stepContext);
        
        results[stepId] = {
          success: true,
          result: stepResult,
          attempt: attempt,
          timestamp: new Date().toISOString()
        };
        
        completedSteps.add(stepId);
        return stepResult;
        
      } catch (error) {
        lastError = error;
        console.warn(`Step ${stepId} attempt ${attempt} failed:`, error.message);
        
        if (attempt < maxRetries) {
          // 等待后重试
          const delay = Math.min(1000 * Math.pow(2, attempt - 1), 30000); // 指数退避
          await new Promise(resolve => setTimeout(resolve, delay));
        }
      }
    }
    
    // 所有重试都失败了
    results[stepId] = {
      success: false,
      error: lastError.message,
      stack: lastError.stack,
      attempts: maxRetries,
      timestamp: new Date().toISOString()
    };
    
    completedSteps.add(stepId);
    throw lastError;
  }

  // 调用代理执行任务（模拟）
  async callAgent(agentId, task, context) {
    // 这里应该集成实际的 OpenClaw 代理调用
    // 目前作为模拟实现
    console.log(`Calling agent ${agentId} with task:`, task);
    console.log(`Context:`, context);
    
    // 模拟成功结果
    return {
      status: 'success',
      output: `Task completed by agent ${agentId}`,
      metadata: {
        agentId: agentId,
        taskId: context.stepId,
        workflowId: context.workflowId,
        timestamp: new Date().toISOString()
      }
    };
  }

  // 获取工作流状态
  getWorkflowStatus(workflowId) {
    const workflow = this.workflows.get(workflowId);
    if (!workflow) {
      return null;
    }
    
    return {
      id: workflow.id,
      name: workflow.name,
      status: workflow.status,
      createdAt: workflow.createdAt,
      startedAt: workflow.startedAt,
      completedAt: workflow.completedAt,
      failedAt: workflow.failedAt,
      stepCount: workflow.steps.length,
      completedSteps: Object.keys(workflow.results || {}).length,
      errors: workflow.errors
    };
  }

  // 列出所有工作流
  listWorkflows() {
    return Array.from(this.workflows.values()).map(wf => ({
      id: wf.id,
      name: wf.name,
      status: wf.status,
      createdAt: wf.createdAt
    }));
  }

  // 删除工作流
  deleteWorkflow(workflowId) {
    if (this.activeWorkflows.has(workflowId)) {
      throw new Error(`Cannot delete active workflow ${workflowId}`);
    }
    return this.workflows.delete(workflowId);
  }

  // 导出工作流配置
  exportWorkflow(workflowId) {
    const workflow = this.workflows.get(workflowId);
    if (!workflow) {
      throw new Error(`Workflow ${workflowId} not found`);
    }
    
    return {
      name: workflow.name,
      description: workflow.description,
      steps: workflow.steps,
      dependencies: workflow.dependencies,
      parallelTasks: workflow.parallelTasks,
      maxRetries: workflow.maxRetries,
      timeout: workflow.timeout
    };
  }

  // 从配置导入工作流
  importWorkflow(workflowConfig) {
    const issues = this.validateWorkflow(workflowConfig);
    if (issues.length > 0) {
      throw new Error(`Invalid workflow configuration: ${issues.join('; ')}`);
    }
    
    return this.createWorkflow(workflowConfig);
  }
}

module.exports = WorkflowManager;