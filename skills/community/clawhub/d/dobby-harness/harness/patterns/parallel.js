/**
 * Parallel Pattern - 并行执行模式
 * 
 * 适用场景：
 * - 任务间无依赖关系
 * - 可完全并行执行
 * - 批量处理独立项目
 * 
 * @example
 * const result = await orchestrator.execute({
 *   task: '审查 5 个文件的代码质量',
 *   pattern: 'parallel',
 *   subTasks: [
 *     { task: '审查 file1.js', agent: 'linter' },
 *     { task: '审查 file2.js', agent: 'linter' },
 *     { task: '审查 file3.js', agent: 'linter' },
 *   ]
 * });
 */

export const parallelPattern = {
  name: 'parallel',
  description: '完全并行执行，所有子任务同时开始',

  /**
   * 分解任务
   */
  decompose: async (task, context, subTasks = []) => {
    if (subTasks.length > 0) {
      return subTasks.map((st, i) => ({
        id: `parallel-${Date.now()}-${i}`,
        task: st.task,
        dependencies: [],
        context: { ...context, ...st.context },
        priority: st.priority || 0,
        agent: st.agent,
      }));
    }

    // 默认分解为 3 个并行任务
    return [0, 1, 2].map(i => ({
      id: `parallel-${Date.now()}-${i}`,
      task: `${task} (部分 ${i + 1}/3)`,
      dependencies: [],
      context,
      priority: 0,
    }));
  },

  /**
   * 聚合结果
   */
  aggregate: async (results) => {
    const completed = results.filter(r => r.success);
    const failed = results.filter(r => !r.success);

    return {
      strategy: 'parallel',
      success: failed.length === 0,
      outputs: completed.map(r => r.output),
      errors: failed.map(r => ({ task: r.task, error: r.error })),
      stats: {
        total: results.length,
        completed: completed.length,
        failed: failed.length,
        parallelism: results.length, // 理论并行度
      },
    };
  },

  /**
   * 验证结果
   */
  validate: async (aggregated, validators = []) => {
    const issues = [];

    // 内置验证：至少有一个成功
    if (aggregated.stats.completed === 0) {
      issues.push({
        type: 'NO_SUCCESS',
        message: '所有子任务都失败了',
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

export default parallelPattern;
