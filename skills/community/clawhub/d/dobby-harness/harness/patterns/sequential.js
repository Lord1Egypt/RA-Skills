/**
 * Sequential Pattern - 顺序执行模式
 * 
 * 适用场景：
 * - 任务间有严格依赖关系
 * - 后一任务需要前一任务的输出
 * - 流水线处理
 * 
 * @example
 * const result = await orchestrator.execute({
 *   task: '构建并发布应用',
 *   pattern: 'sequential',
 *   subTasks: [
 *     { task: '安装依赖', agent: 'builder' },
 *     { task: '编译代码', agent: 'builder', dependencies: ['task-1'] },
 *     { task: '运行测试', agent: 'tester', dependencies: ['task-2'] },
 *     { task: '部署上线', agent: 'deployer', dependencies: ['task-3'] },
 *   ]
 * });
 */

export const sequentialPattern = {
  name: 'sequential',
  description: '顺序执行，每个任务依赖前一个任务的完成',

  /**
   * 分解任务
   */
  decompose: async (task, context, subTasks = []) => {
    if (subTasks.length > 0) {
      const tasks = [];
      for (let i = 0; i < subTasks.length; i++) {
        const st = subTasks[i];
        tasks.push({
          id: `sequential-${Date.now()}-${i}`,
          task: st.task,
          dependencies: i > 0 ? [tasks[i - 1].id] : [],
          context: { ...context, ...st.context },
          priority: subTasks.length - i, // 前面的优先级更高
          agent: st.agent,
        });
      }
      return tasks;
    }

    // 默认分解为 3 个顺序任务
    const tasks = [];
    for (let i = 0; i < 3; i++) {
      tasks.push({
        id: `sequential-${Date.now()}-${i}`,
        task: `${task} (步骤 ${i + 1}/3)`,
        dependencies: i > 0 ? [tasks[i - 1].id] : [],
        context,
        priority: 3 - i,
      });
    }
    return tasks;
  },

  /**
   * 聚合结果
   */
  aggregate: async (results) => {
    const completed = results.filter(r => r.success);
    const failed = results.filter(r => !r.success);

    // 顺序模式下，找到第一个失败点
    let failurePoint = -1;
    for (let i = 0; i < results.length; i++) {
      if (!results[i].success) {
        failurePoint = i;
        break;
      }
    }

    return {
      strategy: 'sequential',
      success: failed.length === 0,
      outputs: completed.map(r => r.output),
      errors: failed.map(r => ({ task: r.task, error: r.error })),
      failurePoint,
      stats: {
        total: results.length,
        completed: completed.length,
        failed: failed.length,
        chainBroken: failurePoint >= 0,
      },
    };
  },

  /**
   * 验证结果
   */
  validate: async (aggregated, validators = []) => {
    const issues = [];

    // 内置验证：链条不能断
    if (aggregated.stats.chainBroken) {
      issues.push({
        type: 'CHAIN_BROKEN',
        message: `执行链在步骤 ${aggregated.failurePoint + 1} 处中断`,
        severity: 'error',
      });
    }

    // 内置验证：所有任务必须完成
    if (aggregated.stats.completed < aggregated.stats.total) {
      issues.push({
        type: 'INCOMPLETE',
        message: '顺序链未完整执行',
        severity: 'warning',
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

export default sequentialPattern;
