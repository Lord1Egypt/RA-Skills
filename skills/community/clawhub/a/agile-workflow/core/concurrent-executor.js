#!/usr/bin/env node
/**
 * 并发执行器 v6.1-Phase6.1.2
 * 
 * 核心功能:
 * 1. 任务池管理 (最大并发数控制)
 * 2. 任务调度 (优先级/公平)
 * 3. 结果收集 (聚合/错误处理)
 * 4. 超时控制 (单个/总体)
 * 5. 批量处理 (分组/执行)
 */

const EventEmitter = require('events');

// ============ 并发执行器类 ============

class ConcurrentExecutor extends EventEmitter {
  constructor(options = {}) {
    super();
    this.maxConcurrent = options.maxConcurrent || 10;
    this.timeout = options.timeout || 30000;
    this.retryCount = options.retryCount || 3;
    this.retryDelay = options.retryDelay || 1000;
    
    this.running = 0;
    this.queue = [];
    this.results = [];
    this.errors = [];
    this.stats = {
      total: 0,
      completed: 0,
      failed: 0,
      retried: 0,
      startTime: null,
      endTime: null
    };
  }

  /**
   * 执行单个任务
   */
  async executeTask(task, index) {
    const startTime = Date.now();
    
    try {
      // 设置超时
      const timeoutPromise = new Promise((_, reject) => {
        setTimeout(() => reject(new Error(`任务超时 (${this.timeout}ms)`)), this.timeout);
      });
      
      // 执行任务
      const result = await Promise.race([
        Promise.resolve(task()),
        timeoutPromise
      ]);
      
      const endTime = Date.now();
      
      return {
        index,
        success: true,
        result,
        duration: endTime - startTime,
        timestamp: endTime
      };
    } catch (error) {
      const endTime = Date.now();
      
      return {
        index,
        success: false,
        error: error.message,
        duration: endTime - startTime,
        timestamp: endTime
      };
    }
  }

  /**
   * 执行任务（带重试）
   */
  async executeWithRetry(task, index, retryLeft = this.retryCount) {
    const result = await this.executeTask(task, index);
    
    if (!result.success && retryLeft > 0) {
      this.stats.retried++;
      this.emit('task:retry', { index, retryLeft, error: result.error });
      
      // 延迟后重试
      await new Promise(resolve => setTimeout(resolve, this.retryDelay));
      return this.executeWithRetry(task, index, retryLeft - 1);
    }
    
    return result;
  }

  /**
   * 执行所有任务
   */
  async execute(tasks, options = {}) {
    const {
      concurrent = this.maxConcurrent,
      ordered = false,
      stopOnError = false
    } = options;
    
    console.log(`🚀 开始执行 ${tasks.length} 个任务 (并发：${concurrent})`);
    
    this.stats.total = tasks.length;
    this.stats.startTime = Date.now();
    this.results = [];
    this.errors = [];
    this.running = 0;
    this.queue = [...tasks];
    
    const executing = new Set();
    const results = new Array(tasks.length);
    
    return new Promise((resolve, reject) => {
      const processNext = async () => {
        if (this.queue.length === 0 && executing.size === 0) {
          // 所有任务完成
          this.stats.endTime = Date.now();
          this.stats.completed = results.filter(r => r?.success).length;
          this.stats.failed = results.filter(r => r?.success === false).length;
          
          this.emit('complete', {
            results: ordered ? results : this.results,
            stats: this.getStats()
          });
          
          if (stopOnError && this.errors.length > 0) {
            reject(new Error(`有 ${this.errors.length} 个任务失败`));
          } else {
            resolve({
              results: ordered ? results : this.results,
              stats: this.getStats()
            });
          }
          return;
        }
        
        while (executing.size < concurrent && this.queue.length > 0) {
          const task = this.queue.shift();
          const index = tasks.length - this.queue.length - 1;
          
          const promise = this.executeWithRetry(task, index)
            .then(result => {
              executing.delete(promise);
              
              if (result.success) {
                this.results.push(result);
                if (ordered) {
                  results[index] = result;
                }
                this.stats.completed++;
                this.emit('task:success', result);
              } else {
                this.errors.push(result);
                if (ordered) {
                  results[index] = result;
                }
                this.stats.failed++;
                this.emit('task:error', result);
                
                if (stopOnError) {
                  // 清空队列
                  this.queue = [];
                  executing.forEach(p => p.cancel?.());
                }
              }
              
              this.emit('progress', {
                total: this.stats.total,
                completed: this.stats.completed,
                failed: this.stats.failed,
                percent: ((this.stats.completed + this.stats.failed) / this.stats.total * 100).toFixed(2) + '%'
              });
              
              processNext();
            })
            .catch(error => {
              executing.delete(promise);
              this.emit('task:error', { index, error: error.message });
              processNext();
            });
          
          promise.cancel = () => {}; // 占位符
          executing.add(promise);
          this.running = executing.size;
          
          this.emit('task:start', { index, running: this.running });
        }
      };
      
      processNext();
    });
  }

  /**
   * 批量执行
   */
  async executeInBatches(tasks, batchSize = 100, options = {}) {
    console.log(`📦 批量执行 ${tasks.length} 个任务 (批次大小：${batchSize})`);
    
    const batches = this.chunk(tasks, batchSize);
    const allResults = [];
    let completedBatches = 0;
    
    for (const batch of batches) {
      completedBatches++;
      console.log(`📋 执行批次 ${completedBatches}/${batches.length}`);
      
      const batchResults = await this.execute(batch, options);
      allResults.push(...batchResults.results);
      
      this.emit('batch:complete', {
        batch: completedBatches,
        total: batches.length,
        results: batchResults
      });
    }
    
    return {
      results: allResults,
      stats: this.getStats(),
      batches: batches.length
    };
  }

  /**
   * 分组执行
   */
  async executeByGroups(groupedTasks, options = {}) {
    const { sequential = true } = options;
    
    console.log(`📊 分组执行 ${Object.keys(groupedTasks).length} 组`);
    
    const allResults = {};
    
    if (sequential) {
      // 顺序执行每组
      for (const [groupName, tasks] of Object.entries(groupedTasks)) {
        console.log(`📋 执行组：${groupName} (${tasks.length} 个任务)`);
        
        const results = await this.execute(tasks, options);
        allResults[groupName] = results;
        
        this.emit('group:complete', {
          group: groupName,
          results
        });
      }
    } else {
      // 并行执行所有组
      const groupPromises = Object.entries(groupedTasks).map(async ([groupName, tasks]) => {
        console.log(`📋 执行组：${groupName} (${tasks.length} 个任务)`);
        
        const results = await this.execute(tasks, options);
        allResults[groupName] = results;
        
        this.emit('group:complete', {
          group: groupName,
          results
        });
        
        return [groupName, results];
      });
      
      await Promise.all(groupPromises);
    }
    
    return {
      results: allResults,
      stats: this.getStats()
    };
  }

  /**
   * 分块数组
   */
  chunk(array, size) {
    const chunks = [];
    for (let i = 0; i < array.length; i += size) {
      chunks.push(array.slice(i, i + size));
    }
    return chunks;
  }

  /**
   * 获取统计信息
   */
  getStats() {
    const duration = this.stats.endTime ? this.stats.endTime - this.stats.startTime : Date.now() - this.stats.startTime;
    const avgDuration = this.results.length > 0
      ? this.results.reduce((sum, r) => sum + r.duration, 0) / this.results.length
      : 0;
    
    return {
      ...this.stats,
      duration,
      avgDuration: avgDuration.toFixed(2),
      qps: this.stats.completed > 0 ? (this.stats.completed / (duration / 1000)).toFixed(2) : 0,
      running: this.running,
      queued: this.queue.length
    };
  }

  /**
   * 取消所有任务
   */
  cancel() {
    console.log('🛑 取消所有任务');
    this.queue = [];
    this.running = 0;
    this.emit('cancelled');
  }

  /**
   * 暂停执行
   */
  pause() {
    console.log('⏸️  暂停执行');
    this.paused = true;
  }

  /**
   * 恢复执行
   */
  resume() {
    console.log('▶️  恢复执行');
    this.paused = false;
  }
}

// ============ 批量处理器类 ============

class BatchProcessor extends EventEmitter {
  constructor(options = {}) {
    super();
    this.batchSize = options.batchSize || 100;
    this.processFn = options.processFn;
    this.executor = new ConcurrentExecutor(options);
    
    this.stats = {
      totalItems: 0,
      processedItems: 0,
      failedItems: 0,
      batches: 0
    };
  }

  /**
   * 处理项目
   */
  async process(items, processFn = this.processFn) {
    if (!processFn) {
      throw new Error('请提供处理函数');
    }
    
    this.stats.totalItems = items.length;
    this.stats.batches = Math.ceil(items.length / this.batchSize);
    
    console.log(`🔄 开始处理 ${items.length} 个项目 (批次大小：${this.batchSize})`);
    
    const batches = this.chunk(items, this.batchSize);
    const allResults = [];
    
    for (let i = 0; i < batches.length; i++) {
      const batch = batches[i];
      console.log(`📋 处理批次 ${i + 1}/${batches.length}`);
      
      const batchResults = await this.executor.execute(
        batch.map((item, index) => () => processFn(item, i * this.batchSize + index)),
        { concurrent: 1 } // 批次内串行
      );
      
      allResults.push(...batchResults.results);
      this.stats.processedItems += batchResults.stats.completed;
      this.stats.failedItems += batchResults.stats.failed;
      
      this.emit('batch:complete', {
        batch: i + 1,
        total: batches.length,
        processed: this.stats.processedItems,
        failed: this.stats.failedItems,
        percent: (this.stats.processedItems / this.stats.totalItems * 100).toFixed(2) + '%'
      });
    }
    
    return {
      results: allResults,
      stats: this.getStats()
    };
  }

  /**
   * 并行批量处理
   */
  async processParallel(items, processFn = this.processFn, options = {}) {
    const { concurrent = 10 } = options;
    
    this.stats.totalItems = items.length;
    
    console.log(`🚀 并行处理 ${items.length} 个项目 (并发：${concurrent})`);
    
    const results = await this.executor.execute(
      items.map((item, index) => () => processFn(item, index)),
      { concurrent }
    );
    
    this.stats.processedItems = results.stats.completed;
    this.stats.failedItems = results.stats.failed;
    this.stats.batches = Math.ceil(items.length / this.batchSize);
    
    return {
      results: results.results,
      stats: this.getStats()
    };
  }

  /**
   * 分块数组
   */
  chunk(array, size) {
    const chunks = [];
    for (let i = 0; i < array.length; i += size) {
      chunks.push(array.slice(i, i + size));
    }
    return chunks;
  }

  /**
   * 获取统计信息
   */
  getStats() {
    return {
      ...this.stats,
      executorStats: this.executor.getStats()
    };
  }
}

// ============ CLI 接口 ============

function printHelp() {
  console.log(`
并发执行器 v6.1

用法：node concurrent-executor.js <命令> [选项]

命令:
  test                运行功能测试
  benchmark           性能基准测试
  demo                演示示例

示例:
  node concurrent-executor.js test
  node concurrent-executor.js benchmark
  node concurrent-executor.js demo
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

  switch (command) {
    case 'test':
      console.log('🧪 运行并发执行器测试...\n');
      
      const executor = new ConcurrentExecutor({
        maxConcurrent: 5,
        timeout: 5000,
        retryCount: 2
      });
      
      // 监听事件
      executor.on('progress', (progress) => {
        console.log(`📊 进度：${progress.percent} (${progress.completed}/${progress.total})`);
      });
      
      executor.on('complete', (result) => {
        console.log(`✅ 完成：${result.stats.completed} 成功，${result.stats.failed} 失败`);
      });
      
      // 创建测试任务
      const tasks = [];
      for (let i = 0; i < 20; i++) {
        tasks.push(() => {
          return new Promise(resolve => {
            setTimeout(() => {
              resolve(`任务${i}完成`);
            }, Math.random() * 1000);
          });
        });
      }
      
      const result = await executor.execute(tasks);
      console.log('\n📊 执行统计:');
      console.log(JSON.stringify(result.stats, null, 2));
      break;

    case 'benchmark':
      console.log('⚡ 运行性能基准测试...\n');
      
      // 测试不同并发度
      for (const concurrent of [1, 5, 10, 20]) {
        const benchExecutor = new ConcurrentExecutor({ maxConcurrent: concurrent });
        
        const tasks = [];
        for (let i = 0; i < 100; i++) {
          tasks.push(() => {
            return new Promise(resolve => {
              setTimeout(() => resolve(i), 10);
            });
          });
        }
        
        const start = Date.now();
        await benchExecutor.execute(tasks);
        const duration = Date.now() - start;
        
        console.log(`并发 ${concurrent}: ${duration}ms (${(100/duration*1000).toFixed(0)} ops/s)`);
      }
      break;

    case 'demo':
      console.log('📖 演示示例...\n');
      
      const demoExecutor = new ConcurrentExecutor({ maxConcurrent: 3 });
      
      // 演示进度监听
      demoExecutor.on('progress', (progress) => {
        const bar = '█'.repeat(Math.floor(progress.completed / progress.total * 20));
        const empty = '░'.repeat(20 - Math.floor(progress.completed / progress.total * 20));
        console.log(`\r[${bar}${empty}] ${progress.percent}`);
      });
      
      const demoTasks = [];
      for (let i = 0; i < 10; i++) {
        demoTasks.push(() => {
          return new Promise(resolve => {
            setTimeout(() => resolve(`结果${i}`), 500);
          });
        });
      }
      
      await demoExecutor.execute(demoTasks);
      console.log('\n✅ 演示完成');
      break;

    default:
      console.log(`未知命令：${command}`);
      printHelp();
  }
}

// 导出 API
module.exports = { ConcurrentExecutor, BatchProcessor };

// 运行 CLI
if (require.main === module) {
  main().catch(console.error);
}
