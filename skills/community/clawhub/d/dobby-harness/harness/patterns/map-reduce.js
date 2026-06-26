/**
 * Map-Reduce Pattern - 映射归约模式
 * 
 * 适用场景：
 * - 先并行处理多个项目
 * - 再聚合所有结果
 * - 数据分析、批量转换
 * 
 * @example
 * const result = await orchestrator.execute({
 *   task: '分析 100 个文件的代码质量',
 *   pattern: 'map-reduce',
 *   map: {
 *     items: files,
 *     taskFn: (file) => `分析 ${file} 的质量`,
 *   },
 *   reduce: {
 *     task: '汇总所有分析结果，生成报告',
 *     agent: 'analyst',
 *   }
 * });
 */

export const mapReducePattern = {
  name: 'map-reduce',
  description: '先并行 Map 处理，再 Reduce 聚合',

  /**
   * 分解任务
   */
  decompose: async (task, context, options = {}) => {
    const { map, reduce } = options;
    const tasks = [];
    const timestamp = Date.now();

    // Map 阶段：并行处理
    if (map && map.items && map.items.length > 0) {
      const mapTasks = map.items.map((item, i) => ({
        id: `map-${timestamp}-${i}`,
        task: typeof map.taskFn === 'function' ? map.taskFn(item) : map.taskFn,
        dependencies: [],
        context: { ...context, item, index: i },
        priority: 1,
        agent: map.agent,
        phase: 'map',
      }));
      tasks.push(...mapTasks);

      // Reduce 阶段：聚合（依赖所有 Map 任务）
      if (reduce) {
        tasks.push({
          id: `reduce-${timestamp}`,
          task: reduce.task,
          dependencies: mapTasks.map(t => t.id),
          context: { ...context, mapResults: 'pending' },
          priority: 2,
          agent: reduce.agent,
          phase: 'reduce',
        });
      }
    } else {
      // 降级为普通并行
      tasks.push({
        id: `map-${timestamp}-0`,
        task,
        dependencies: [],
        context,
        priority: 1,
        phase: 'map',
      });
    }

    return tasks;
  },

  /**
   * 聚合结果
   */
  aggregate: async (results) => {
    const mapResults = results.filter(r => r.phase === 'map' && r.success);
    const reduceResults = results.filter(r => r.phase === 'reduce' && r.success);
    const failed = results.filter(r => !r.success);

    return {
      strategy: 'map-reduce',
      success: reduceResults.length > 0 || (mapResults.length > 0 && failed.length === 0),
      mapOutputs: mapResults.map(r => r.output),
      reduceOutput: reduceResults.length > 0 ? reduceResults[0].output : null,
      finalOutput: reduceResults.length > 0 ? reduceResults[0].output : mapResults.map(r => r.output),
      errors: failed.map(r => ({ task: r.task, error: r.error, phase: r.phase })),
      stats: {
        total: results.length,
        mapCompleted: mapResults.length,
        reduceCompleted: reduceResults.length,
        failed: failed.length,
      },
    };
  },

  /**
   * 验证结果
   */
  validate: async (aggregated, validators = []) => {
    const issues = [];

    // 内置验证：Map 阶段至少部分成功
    if (aggregated.stats.mapCompleted === 0) {
      issues.push({
        type: 'MAP_FAILED',
        message: 'Map 阶段所有任务都失败了',
        severity: 'error',
      });
    }

    // 内置验证：如果有 Reduce 阶段，必须成功
    const hasReduce = aggregated.stats.total > aggregated.stats.mapCompleted;
    if (hasReduce && aggregated.stats.reduceCompleted === 0) {
      issues.push({
        type: 'REDUCE_FAILED',
        message: 'Reduce 阶段失败',
        severity: 'error',
      });
    }

    // 自定义验证器
    for (const validator of validators) {
      const issue = validator(aggregated);
      if (issue) issues.push(issue);
    }

    return {
      valid: issues.length === 0,
      issues,
    };
  },
};

export default mapReducePattern;
