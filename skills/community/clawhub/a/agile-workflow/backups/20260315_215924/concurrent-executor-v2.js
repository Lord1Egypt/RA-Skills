#!/usr/bin/env node
/**
 * 并发执行器 v2.0 (安全版本)
 * 
 * 核心职责：安全地并发执行任务，零数据污染
 * 
 * 整合模块：
 * - WriteDomainIsolator: 写入域隔离
 * - DependencyGraphManager: 依赖管理
 * - MergeStrategyManager: 合并策略
 * 
 * 第一性原理：
 * - 并发安全 = 写入隔离 + 依赖显式 + 合并策略
 */

const fs = require('fs');
const path = require('path');
const EventEmitter = require('events');

const WriteDomainIsolator = require('./write-domain-isolator');
const DependencyGraphManager = require('./dependency-graph-manager');
const MergeStrategyManager = require('./merge-strategy-manager');

class ConcurrentExecutor extends EventEmitter {
  constructor(config = {}) {
    super();
    
    this.config = {
      workspace: config.workspace || '/tmp/concurrent-executor',
      maxConcurrency: config.maxConcurrency || 3,
      timeoutMs: config.timeoutMs || 300000,
      retryCount: config.retryCount || 0,
      cleanupOnComplete: config.cleanupOnComplete || false,
      ...config
    };
    
    // 初始化子模块
    this.isolator = new WriteDomainIsolator({
      baseDir: path.join(this.config.workspace, 'isolated')
    });
    
    this.depGraph = new DependencyGraphManager({
      maxDepth: config.maxDepth || 50,
      timeoutMs: this.config.timeoutMs
    });
    
    this.merger = new MergeStrategyManager({
      workspace: this.config.workspace
    });
    
    // 状态管理
    this.tasks = new Map(); // taskId → task definition
    this.results = new Map(); // taskId → execution result
    this.executionState = 'idle'; // idle, running, paused, completed
    this.startTime = null;
    this.endTime = null;
    
    // 确保工作目录
    this.ensureWorkspace();
  }

  /**
   * 确保工作目录存在
   */
  ensureWorkspace() {
    const dirs = [
      this.config.workspace,
      path.join(this.config.workspace, 'isolated'),
      path.join(this.config.workspace, 'merged'),
      path.join(this.config.workspace, 'logs')
    ];
    
    dirs.forEach(dir => {
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }
    });
  }

  /**
   * 提交任务
   * @param {string} taskId - 任务 ID
   * @param {Function} taskFn - 任务执行函数 (async function(domainPath, context))
   * @param {string[]} dependencies - 依赖的任务 ID 列表
   * @param {object} options - 任务选项
   * @returns {object} 任务定义
   */
  submitTask(taskId, taskFn, dependencies = [], options = {}) {
    if (this.executionState === 'running') {
      throw new Error('执行中不能添加新任务');
    }

    const task = {
      taskId,
      taskFn,
      dependencies,
      options: {
        priority: options.priority || 0,
        timeout: options.timeout || this.config.timeoutMs,
        retryCount: options.retryCount || this.config.retryCount,
        mergeStrategy: options.mergeStrategy || 'append',
        metadata: options.metadata || {},
        ...options
      },
      status: 'queued',
      submittedAt: Date.now()
    };

    // 添加到依赖图
    this.depGraph.addTask(taskId, dependencies, {
      priority: task.options.priority,
      timeout: task.options.timeout,
      retryCount: task.options.retryCount
    });

    this.tasks.set(taskId, task);
    
    this.emit('task:submitted', { taskId, dependencies });
    
    return task;
  }

  /**
   * 批量提交任务
   * @param {Array} taskDefinitions - 任务定义数组
   * @returns {Array} 任务列表
   */
  submitTasks(taskDefinitions) {
    return taskDefinitions.map(def => {
      const { taskId, taskFn, dependencies = [], options = {} } = def;
      return this.submitTask(taskId, taskFn, dependencies, options);
    });
  }

  /**
   * 执行所有任务
   * @returns {Promise<object>} 执行结果
   */
  async executeAll() {
    if (this.executionState === 'running') {
      throw new Error('已在执行中');
    }

    this.executionState = 'running';
    this.startTime = Date.now();
    
    this.emit('execution:start', {
      taskCount: this.tasks.size,
      maxConcurrency: this.config.maxConcurrency
    });

    try {
      // 获取分层执行计划
      const layers = this.depGraph.getLayeredExecutionPlan();
      
      console.log(`[ConcurrentExecutor] 执行计划：${layers.length} 层，共 ${this.tasks.size} 个任务`);
      
      // 逐层执行
      for (let i = 0; i < layers.length; i++) {
        const layer = layers[i];
        console.log(`[ConcurrentExecutor] 执行第 ${i + 1}/${layers.length} 层，${layer.length} 个任务`);
        
        this.emit('layer:start', {
          layerIndex: i,
          totalLayers: layers.length,
          taskCount: layer.length
        });

        // 并发执行当前层
        const layerResults = await this.executeLayer(layer);
        
        this.emit('layer:complete', {
          layerIndex: i,
          results: layerResults
        });
      }

      this.executionState = 'completed';
      this.endTime = Date.now();
      
      const summary = this.getExecutionSummary();
      
      this.emit('execution:complete', summary);
      
      // 清理
      if (this.config.cleanupOnComplete) {
        this.cleanup();
      }
      
      return summary;
      
    } catch (error) {
      this.executionState = 'failed';
      this.endTime = Date.now();
      
      this.emit('execution:error', {
        error: error.message,
        timestamp: Date.now()
      });
      
      throw error;
    }
  }

  /**
   * 执行一层任务（可并行）
   * @param {string[]} taskIds - 任务 ID 列表
   * @returns {Promise<Array>} 执行结果
   */
  async executeLayer(taskIds) {
    // 控制并发数
    const chunks = this.chunk(taskIds, this.config.maxConcurrency);
    const allResults = [];

    for (const chunk of chunks) {
      const promises = chunk.map(async (taskId) => {
        return this.executeTask(taskId);
      });

      const results = await Promise.allSettled(promises);
      allResults.push(...results);
    }

    return allResults;
  }

  /**
   * 执行单个任务
   * @param {string} taskId - 任务 ID
   * @returns {Promise<object>} 执行结果
   */
  async executeTask(taskId) {
    const task = this.tasks.get(taskId);
    
    if (!task) {
      throw new Error(`任务不存在：${taskId}`);
    }

    this.depGraph.markStarted(taskId);
    this.emit('task:start', { taskId });

    const startTime = Date.now();
    let domainPath = null;

    try {
      // 创建隔离域
      domainPath = this.isolator.createDomain(taskId, {
        ttl: task.options.timeout,
        quota: task.options.quota
      });

      // 准备执行上下文
      const context = {
        taskId,
        domainPath,
        workspace: this.config.workspace,
        dependencies: this.getDependencyResults(task.dependencies),
        startTime,
        options: task.options
      };

      // 执行任务（带超时）
      const result = await this.withTimeout(
        task.taskFn(domainPath, context),
        task.options.timeout,
        `任务 ${taskId} 超时`
      );

      const duration = Date.now() - startTime;
      
      this.depGraph.markCompleted(taskId, result);
      
      const taskResult = {
        taskId,
        status: 'completed',
        result,
        domainPath,
        duration,
        files: this.isolator.getDomainFiles(taskId)
      };
      
      this.results.set(taskId, taskResult);
      this.emit('task:complete', taskResult);
      
      console.log(`[ConcurrentExecutor] 任务 ${taskId} 完成 (${duration}ms)`);
      
      return { status: 'fulfilled', value: taskResult };
      
    } catch (error) {
      const duration = Date.now() - startTime;
      
      // 判断是否重试
      const node = this.depGraph.graph.get(taskId);
      const shouldRetry = error.message.includes('timeout') && 
                          node && 
                          node.attempt <= task.options.retryCount;
      
      this.depGraph.markFailed(taskId, error, shouldRetry);
      
      const taskResult = {
        taskId,
        status: 'failed',
        error: error.message,
        domainPath,
        duration
      };
      
      this.results.set(taskId, taskResult);
      this.emit('task:error', taskResult);
      
      console.error(`[ConcurrentExecutor] 任务 ${taskId} 失败：${error.message}`);
      
      return { status: 'rejected', reason: error };
    }
  }

  /**
   * 获取依赖任务的结果
   * @param {string[]} dependencyIds - 依赖任务 ID 列表
   * @returns {object} 依赖结果映射
   */
  getDependencyResults(dependencyIds) {
    const results = {};
    
    dependencyIds.forEach(depId => {
      const depResult = this.results.get(depId);
      if (depResult) {
        results[depId] = depResult.result;
      }
    });
    
    return results;
  }

  /**
   * 带超时执行
   */
  async withTimeout(promise, timeoutMs, errorMessage) {
    const timeout = new Promise((_, reject) => {
      setTimeout(() => reject(new Error(errorMessage || '超时')), timeoutMs);
    });
    
    return Promise.race([promise, timeout]);
  }

  /**
   * 合并任务结果
   * @param {string[]} taskIds - 任务 ID 列表
   * @param {string} strategyName - 合并策略名称
   * @param {object} options - 合并选项
   * @returns {object} 合并结果
   */
  mergeResults(taskIds, strategyName = 'append', options = {}) {
    const results = taskIds
      .map(id => this.results.get(id))
      .filter(r => r && r.status === 'completed')
      .map(r => r.result);

    const mergeResult = this.merger.applyStrategy(strategyName, results, options);
    
    // 保存合并结果
    const outputPath = path.join(
      this.config.workspace,
      'merged',
      `merged_${Date.now()}.json`
    );
    
    fs.writeFileSync(outputPath, JSON.stringify(mergeResult, null, 2));
    
    this.emit('results:merged', {
      taskIds,
      strategy: strategyName,
      outputPath,
      conflictCount: mergeResult.conflicts?.length || 0
    });
    
    return mergeResult;
  }

  /**
   * 获取执行摘要
   */
  getExecutionSummary() {
    const progress = this.depGraph.getProgress();
    
    const failedTasks = [];
    const completedTasks = [];
    
    for (const [taskId, result] of this.results) {
      if (result.status === 'completed') {
        completedTasks.push(taskId);
      } else if (result.status === 'failed') {
        failedTasks.push({ taskId, error: result.error });
      }
    }
    
    return {
      status: this.executionState,
      startTime: this.startTime,
      endTime: this.endTime,
      duration: this.endTime - this.startTime,
      progress,
      completedTasks,
      failedTasks,
      totalTasks: this.tasks.size,
      conflictLog: this.merger.getConflictLog()
    };
  }

  /**
   * 获取任务状态
   * @param {string} taskId - 任务 ID
   * @returns {object} 任务状态
   */
  getTaskStatus(taskId) {
    const result = this.results.get(taskId);
    const depStatus = this.depGraph.getTaskStatus(taskId);
    
    return {
      ...depStatus,
      result: result ? {
        status: result.status,
        duration: result.duration,
        error: result.error
      } : null
    };
  }

  /**
   * 获取所有任务状态
   */
  getAllTaskStatus() {
    const status = {};
    for (const taskId of this.tasks.keys()) {
      status[taskId] = this.getTaskStatus(taskId);
    }
    return status;
  }

  /**
   * 获取依赖图可视化
   */
  getDependencyGraphviz() {
    return this.depGraph.toDot();
  }

  /**
   * 清理资源
   */
  cleanup() {
    console.log('[ConcurrentExecutor] 清理资源...');
    
    // 清理隔离域
    for (const [taskId, result] of this.results) {
      if (result.domainPath && result.status !== 'running') {
        try {
          this.isolator.closeDomain(taskId);
          // 可选：删除文件
          // this.isolator.cleanupDomain(taskId, true);
        } catch (error) {
          console.error(`清理域 ${taskId} 失败：${error.message}`);
        }
      }
    }
    
    this.emit('cleanup:complete');
  }

  /**
   * 重置执行器
   */
  reset() {
    this.tasks.clear();
    this.results.clear();
    this.depGraph.clear();
    this.executionState = 'idle';
    this.startTime = null;
    this.endTime = null;
    
    this.emit('reset');
  }

  /**
   * 暂停执行（用于未来扩展）
   */
  pause() {
    if (this.executionState === 'running') {
      this.executionState = 'paused';
      this.emit('execution:pause');
    }
  }

  /**
   * 恢复执行（用于未来扩展）
   */
  resume() {
    if (this.executionState === 'paused') {
      this.executionState = 'running';
      this.emit('execution:resume');
    }
  }

  /**
   * 分块辅助函数
   */
  chunk(array, size) {
    const chunks = [];
    for (let i = 0; i < array.length; i += size) {
      chunks.push(array.slice(i, i + size));
    }
    return chunks;
  }

  /**
   * 导出执行报告
   */
  exportReport(outputPath) {
    const report = {
      generatedAt: Date.now(),
      config: this.config,
      summary: this.getExecutionSummary(),
      taskStatus: this.getAllTaskStatus(),
      strategies: this.merger.getAvailableStrategies(),
      dependencyGraph: this.getDependencyGraphviz()
    };
    
    fs.writeFileSync(outputPath, JSON.stringify(report, null, 2));
    return outputPath;
  }
}

module.exports = ConcurrentExecutor;

// CLI 测试
if (require.main === module) {
  const executor = new ConcurrentExecutor({
    workspace: '/tmp/test-executor',
    maxConcurrency: 3
  });

  // 事件监听
  executor.on('task:submitted', (e) => console.log('任务提交:', e.taskId));
  executor.on('task:start', (e) => console.log('任务开始:', e.taskId));
  executor.on('task:complete', (e) => console.log('任务完成:', e.taskId, e.duration + 'ms'));
  executor.on('task:error', (e) => console.error('任务失败:', e.taskId, e.error));
  executor.on('execution:complete', (summary) => {
    console.log('\n执行完成摘要:');
    console.log(`  总任务：${summary.totalTasks}`);
    console.log(`  完成：${summary.completedTasks.length}`);
    console.log(`  失败：${summary.failedTasks.length}`);
    console.log(`  耗时：${summary.duration}ms`);
  });

  // 提交测试任务
  executor.submitTask('task-A', async (domainPath) => {
    console.log('执行 A，域路径:', domainPath);
    fs.writeFileSync(path.join(domainPath, 'output.txt'), 'Result A');
    await new Promise(r => setTimeout(r, 100));
    return { name: 'A', value: 1 };
  });

  executor.submitTask('task-B', async (domainPath) => {
    console.log('执行 B，域路径:', domainPath);
    fs.writeFileSync(path.join(domainPath, 'output.txt'), 'Result B');
    await new Promise(r => setTimeout(r, 150));
    return { name: 'B', value: 2 };
  });

  executor.submitTask('task-C', async (domainPath, context) => {
    console.log('执行 C，依赖结果:', context.dependencies);
    fs.writeFileSync(path.join(domainPath, 'output.txt'), 'Result C');
    await new Promise(r => setTimeout(r, 100));
    return { name: 'C', value: 3 };
  }, ['task-A']); // 依赖 A

  executor.submitTask('task-D', async (domainPath, context) => {
    console.log('执行 D，依赖结果:', context.dependencies);
    fs.writeFileSync(path.join(domainPath, 'output.txt'), 'Result D');
    await new Promise(r => setTimeout(r, 200));
    return { name: 'D', value: 4 };
  }, ['task-A', 'task-B']); // 依赖 A 和 B

  executor.submitTask('task-E', async (domainPath, context) => {
    console.log('执行 E，依赖结果:', context.dependencies);
    return { name: 'E', merged: Object.values(context.dependencies) };
  }, ['task-C', 'task-D']); // 依赖 C 和 D

  // 执行并合并结果
  (async () => {
    try {
      await executor.executeAll();
      
      // 合并最终结果
      const merged = executor.mergeResults(
        ['task-A', 'task-B', 'task-C', 'task-D', 'task-E'],
        'deep'
      );
      
      console.log('\n合并结果:', JSON.stringify(merged.merged, null, 2));
      
      // 导出报告
      executor.exportReport('/tmp/test-executor/report.json');
      
    } catch (error) {
      console.error('执行失败:', error.message);
    }
  })();
}
