#!/usr/bin/env node
/**
 * 依赖图管理器 v7.0
 * 
 * 核心职责：管理任务依赖关系，确保正确执行顺序
 * 
 * 第一性原理：
 * - 任务依赖 = 有向无环图 (DAG)
 * - 执行条件 = 所有前置依赖已完成
 * - 并发优化 = 拓扑排序 + 分层并行
 */

class DependencyGraphManager {
  constructor(config = {}) {
    this.graph = new Map(); // taskId → node
    this.config = {
      allowCycles: false,
      maxDepth: config.maxDepth || 100,
      timeoutMs: config.timeoutMs || 300000
    };
    this.executionHistory = [];
  }

  /**
   * 添加任务及依赖
   * @param {string} taskId - 任务 ID
   * @param {string[]} dependencies - 依赖的任务 ID 列表
   * @param {object} metadata - 任务元数据
   */
  addTask(taskId, dependencies = [], metadata = {}) {
    if (this.graph.has(taskId)) {
      throw new Error(`任务 ${taskId} 已存在`);
    }

    // 验证依赖是否存在
    const missingDeps = dependencies.filter(depId => !this.graph.has(depId));
    if (missingDeps.length > 0 && !metadata.allowMissingDeps) {
      throw new Error(
        `任务 ${taskId} 的依赖不存在：${missingDeps.join(', ')}`
      );
    }

    const node = {
      taskId,
      dependencies,
      dependents: [],
      status: 'pending', // pending, running, completed, failed, skipped
      result: null,
      error: null,
      metadata: {
        priority: metadata.priority || 0,
        estimatedDuration: metadata.estimatedDuration || null,
        retryCount: metadata.retryCount || 0,
        timeout: metadata.timeout || this.config.timeoutMs,
        ...metadata
      },
      timing: {
        createdAt: Date.now(),
        startedAt: null,
        completedAt: null,
        duration: null
      },
      attempt: 0
    };

    this.graph.set(taskId, node);

    // 更新依赖者的 dependents
    dependencies.forEach(depId => {
      const depNode = this.graph.get(depId);
      if (depNode) {
        depNode.dependents.push(taskId);
      }
    });

    // 检测环路
    if (!this.config.allowCycles && this.hasCycle()) {
      this.graph.delete(taskId);
      throw new Error(`检测到依赖环路，涉及任务：${this.findCyclePath(taskId)}`);
    }

    return node;
  }

  /**
   * 检查任务是否可执行（所有依赖已完成）
   * @param {string} taskId - 任务 ID
   * @returns {boolean} 是否可执行
   */
  canExecute(taskId) {
    const node = this.graph.get(taskId);
    if (!node) return false;
    if (node.status !== 'pending') return false;

    // 检查所有依赖是否完成
    return node.dependencies.every(depId => {
      const depNode = this.graph.get(depId);
      return depNode && depNode.status === 'completed';
    });
  }

  /**
   * 获取可并行执行的任务集合
   * @param {object} options - 选项
   * @returns {string[]} 可执行任务 ID 列表
   */
  getExecutableTasks(options = {}) {
    const executable = [];
    const maxCount = options.maxCount || Infinity;
    const minPriority = options.minPriority || -Infinity;

    for (const [taskId, node] of this.graph) {
      if (
        node.status === 'pending' &&
        this.canExecute(taskId) &&
        node.metadata.priority >= minPriority
      ) {
        executable.push(taskId);
        if (executable.length >= maxCount) break;
      }
    }

    // 按优先级排序
    executable.sort((a, b) => {
      const nodeA = this.graph.get(a);
      const nodeB = this.graph.get(b);
      return nodeB.metadata.priority - nodeA.metadata.priority;
    });

    return executable;
  }

  /**
   * 标记任务开始执行
   * @param {string} taskId - 任务 ID
   */
  markStarted(taskId) {
    const node = this.graph.get(taskId);
    if (node) {
      node.status = 'running';
      node.timing.startedAt = Date.now();
      node.attempt++;
      
      this.executionHistory.push({
        taskId,
        event: 'started',
        timestamp: Date.now(),
        attempt: node.attempt
      });
    }
  }

  /**
   * 标记任务完成
   * @param {string} taskId - 任务 ID
   * @param {any} result - 执行结果
   */
  markCompleted(taskId, result = null) {
    const node = this.graph.get(taskId);
    if (node) {
      node.status = 'completed';
      node.result = result;
      node.timing.completedAt = Date.now();
      node.timing.duration = node.timing.completedAt - node.timing.startedAt;
      
      this.executionHistory.push({
        taskId,
        event: 'completed',
        timestamp: Date.now(),
        duration: node.timing.duration
      });
    }
  }

  /**
   * 标记任务失败
   * @param {string} taskId - 任务 ID
   * @param {Error} error - 错误信息
   * @param {boolean} shouldRetry - 是否重试
   */
  markFailed(taskId, error, shouldRetry = false) {
    const node = this.graph.get(taskId);
    if (node) {
      if (shouldRetry && node.attempt <= node.metadata.retryCount) {
        node.status = 'pending'; // 重置为待执行
        node.error = null;
        node.timing.startedAt = null;
        
        this.executionHistory.push({
          taskId,
          event: 'retry',
          timestamp: Date.now(),
          attempt: node.attempt,
          error: error.message
        });
      } else {
        node.status = 'failed';
        node.error = error.message || String(error);
        node.timing.completedAt = Date.now();
        node.timing.duration = node.timing.completedAt - node.timing.startedAt;
        
        // 标记所有依赖此任务的任务为跳过
        this.markDependentsSkipped(taskId);
        
        this.executionHistory.push({
          taskId,
          event: 'failed',
          timestamp: Date.now(),
          error: error.message
        });
      }
    }
  }

  /**
   * 标记依赖者跳过
   * @param {string} taskId - 失败任务 ID
   */
  markDependentsSkipped(taskId) {
    const node = this.graph.get(taskId);
    if (!node) return;

    const markSkipped = (tid) => {
      const n = this.graph.get(tid);
      if (n && n.status === 'pending') {
        n.status = 'skipped';
        n.error = `依赖任务 ${taskId} 失败`;
        n.dependents.forEach(markSkipped);
      }
    };

    node.dependents.forEach(markSkipped);
  }

  /**
   * 获取拓扑排序
   * @returns {string[]} 拓扑排序后的任务 ID 列表
   */
  getTopologicalOrder() {
    const visited = new Set();
    const order = [];
    const visiting = new Set(); // 用于检测环路

    const visit = (taskId, depth = 0) => {
      if (depth > this.config.maxDepth) {
        throw new Error(`依赖深度超过限制 (${this.config.maxDepth})`);
      }

      if (visited.has(taskId)) return;
      if (visiting.has(taskId)) {
        throw new Error(`检测到环路：${taskId}`);
      }

      visiting.add(taskId);

      const node = this.graph.get(taskId);
      if (node) {
        node.dependencies.forEach(depId => visit(depId, depth + 1));
        order.push(taskId);
      }

      visiting.delete(taskId);
      visited.add(taskId);
    };

    for (const taskId of this.graph.keys()) {
      visit(taskId);
    }

    return order;
  }

  /**
   * 获取分层执行计划（用于并行优化）
   * @returns {string[][]} 分层任务列表，每层可并行执行
   */
  getLayeredExecutionPlan() {
    const layers = [];
    const completed = new Set();
    const remaining = new Set(this.graph.keys());

    while (remaining.size > 0) {
      const layer = [];
      
      for (const taskId of remaining) {
        const node = this.graph.get(taskId);
        const allDepsCompleted = node.dependencies.every(depId => 
          completed.has(depId)
        );
        
        if (allDepsCompleted) {
          layer.push(taskId);
        }
      }

      if (layer.length === 0) {
        // 剩余任务都有未完成的依赖，可能是环路
        throw new Error(
          `无法生成执行计划，剩余任务：${Array.from(remaining).join(', ')}`
        );
      }

      layers.push(layer);
      layer.forEach(id => {
        remaining.delete(id);
        completed.add(id);
      });
    }

    return layers;
  }

  /**
   * 检测是否有环路
   * @returns {boolean} 是否有环路
   */
  hasCycle() {
    const visited = new Set();
    const visiting = new Set();

    const dfs = (taskId) => {
      if (visiting.has(taskId)) return true;
      if (visited.has(taskId)) return false;

      visiting.add(taskId);
      
      const node = this.graph.get(taskId);
      if (node) {
        for (const depId of node.dependencies) {
          if (dfs(depId)) return true;
        }
      }

      visiting.delete(taskId);
      visited.add(taskId);
      return false;
    };

    for (const taskId of this.graph.keys()) {
      if (dfs(taskId)) return true;
    }

    return false;
  }

  /**
   * 查找环路路径
   * @param {string} startId - 起始任务 ID
   * @returns {string} 环路路径描述
   */
  findCyclePath(startId) {
    const visited = new Set();
    const path = [];

    const dfs = (taskId) => {
      if (path.includes(taskId)) {
        const cycleStart = path.indexOf(taskId);
        return path.slice(cycleStart).concat(taskId).join(' → ');
      }

      if (visited.has(taskId)) return null;
      visited.add(taskId);
      path.push(taskId);

      const node = this.graph.get(taskId);
      if (node) {
        for (const depId of node.dependencies) {
          const result = dfs(depId);
          if (result) return result;
        }
      }

      path.pop();
      return null;
    };

    return dfs(startId) || '未知';
  }

  /**
   * 获取任务状态
   * @param {string} taskId - 任务 ID
   * @returns {object} 任务状态
   */
  getTaskStatus(taskId) {
    const node = this.graph.get(taskId);
    if (!node) return null;

    return {
      taskId,
      status: node.status,
      dependencies: node.dependencies,
      dependents: node.dependents,
      attempt: node.attempt,
      timing: node.timing,
      error: node.error
    };
  }

  /**
   * 获取整体进度
   * @returns {object} 进度信息
   */
  getProgress() {
    const total = this.graph.size;
    const status = {
      pending: 0,
      running: 0,
      completed: 0,
      failed: 0,
      skipped: 0
    };

    for (const node of this.graph.values()) {
      status[node.status]++;
    }

    return {
      total,
      ...status,
      percentComplete: total > 0 ? ((status.completed / total) * 100).toFixed(2) : 0,
      percentFailed: total > 0 ? ((status.failed / total) * 100).toFixed(2) : 0
    };
  }

  /**
   * 获取关键路径（最长路径）
   * @returns {string[]} 关键路径任务 ID 列表
   */
  getCriticalPath() {
    const memo = new Map();

    const longestPath = (taskId) => {
      if (memo.has(taskId)) return memo.get(taskId);

      const node = this.graph.get(taskId);
      if (!node || node.dependents.length === 0) {
        memo.set(taskId, [taskId]);
        return [taskId];
      }

      let maxPath = [];
      for (const dependentId of node.dependents) {
        const path = longestPath(dependentId);
        if (path.length > maxPath.length) {
          maxPath = path;
        }
      }

      const result = [taskId, ...maxPath];
      memo.set(taskId, result);
      return result;
    };

    // 从所有无依赖的任务开始
    let criticalPath = [];
    for (const [taskId, node] of this.graph) {
      if (node.dependencies.length === 0) {
        const path = longestPath(taskId);
        if (path.length > criticalPath.length) {
          criticalPath = path;
        }
      }
    }

    return criticalPath;
  }

  /**
   * 导出图为 DOT 格式（用于可视化）
   * @returns {string} DOT 格式字符串
   */
  toDot() {
    let dot = 'digraph DependencyGraph {\n';
    dot += '  rankdir=TB;\n';
    dot += '  node [shape=box];\n\n';

    for (const [taskId, node] of this.graph) {
      const color = {
        pending: 'gray',
        running: 'yellow',
        completed: 'green',
        failed: 'red',
        skipped: 'lightgray'
      }[node.status];

      dot += `  "${taskId}" [style=filled, fillcolor=${color}];\n`;
      
      node.dependencies.forEach(depId => {
        dot += `  "${depId}" -> "${taskId}";\n`;
      });
    }

    dot += '}';
    return dot;
  }

  /**
   * 重置图
   */
  reset() {
    for (const node of this.graph.values()) {
      node.status = 'pending';
      node.result = null;
      node.error = null;
      node.timing = {
        createdAt: Date.now(),
        startedAt: null,
        completedAt: null,
        duration: null
      };
      node.attempt = 0;
    }
    this.executionHistory = [];
  }

  /**
   * 清空图
   */
  clear() {
    this.graph.clear();
    this.executionHistory = [];
  }

  /**
   * 获取执行历史
   * @returns {Array} 执行历史
   */
  getExecutionHistory() {
    return this.executionHistory;
  }
}

module.exports = DependencyGraphManager;

// CLI 测试
if (require.main === module) {
  const graph = new DependencyGraphManager();

  // 构建测试图
  graph.addTask('A', [], { priority: 1 });
  graph.addTask('B', [], { priority: 1 });
  graph.addTask('C', ['A'], { priority: 2 });
  graph.addTask('D', ['A', 'B'], { priority: 2 });
  graph.addTask('E', ['C', 'D'], { priority: 3 });

  console.log('拓扑排序:', graph.getTopologicalOrder());
  console.log('分层执行:', JSON.stringify(graph.getLayeredExecutionPlan(), null, 2));
  console.log('关键路径:', graph.getCriticalPath());
  console.log('可执行任务:', graph.getExecutableTasks());
  console.log('DOT 图:\n', graph.toDot());
}
