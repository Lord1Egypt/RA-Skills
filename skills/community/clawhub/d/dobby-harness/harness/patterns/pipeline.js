/**
 * Pipeline Pattern - 流水线模式
 * 
 * 适用场景：
 * - 多阶段处理
 * - 每阶段内部可并行
 * - 阶段间顺序执行
 * 
 * @example
 * const result = await orchestrator.execute({
 *   task: '发布新版本',
 *   pattern: 'pipeline',
 *   stages: [
 *     {
 *       name: 'build',
 *       tasks: [
 *         { task: '编译 TypeScript', agent: 'builder' },
 *         { task: '打包资源', agent: 'builder' },
 *       ]
 *     },
 *     {
 *       name: 'test',
 *       tasks: [
 *         { task: '单元测试', agent: 'tester' },
 *         { task: '集成测试', agent: 'tester' },
 *       ]
 *     },
 *     {
 *       name: 'deploy',
 *       tasks: [
 *         { task: '部署到生产环境', agent: 'deployer' },
 *       ]
 *     }
 *   ]
 * });
 */

export const pipelinePattern = {
  name: 'pipeline',
  description: '多阶段流水线，阶段内并行，阶段间顺序',

  /**
   * 分解任务
   */
  decompose: async (task, context, options = {}) => {
    const { stages = [] } = options;
    const tasks = [];
    const timestamp = Date.now();

    let previousStageTaskIds = [];

    for (let s = 0; s < stages.length; s++) {
      const stage = stages[s];
      const stageTaskIds = [];

      for (let t = 0; t < (stage.tasks || []).length; t++) {
        const st = stage.tasks[t];
        const taskId = `pipeline-${timestamp}-stage${s}-task${t}`;
        
        tasks.push({
          id: taskId,
          task: st.task,
          dependencies: stage.parallel === false && t > 0 
            ? [stageTaskIds[t - 1]] 
            : previousStageTaskIds,
          context: { ...context, stage: stage.name, stageIndex: s },
          priority: (stages.length - s) * 10 + (stage.tasks.length - t),
          agent: st.agent,
          stage: stage.name,
          stageIndex: s,
        });

        stageTaskIds.push(taskId);
      }

      previousStageTaskIds = stageTaskIds;
    }

    // 如果没有预定义 stages，降级为 3 阶段流水线
    if (stages.length === 0) {
      const stageNames = ['prepare', 'process', 'finalize'];
      for (let s = 0; s < 3; s++) {
        tasks.push({
          id: `pipeline-${timestamp}-stage${s}`,
          task: `${task} (${stageNames[s]})`,
          dependencies: s > 0 ? [tasks[tasks.length - 1].id] : [],
          context: { ...context, stage: stageNames[s], stageIndex: s },
          priority: 3 - s,
          stage: stageNames[s],
          stageIndex: s,
        });
      }
    }

    return tasks;
  },

  /**
   * 聚合结果
   */
  aggregate: async (results) => {
    const byStage = {};
    const failed = [];

    // 按阶段分组
    for (const result of results) {
      const stage = result.stage || 'unknown';
      if (!byStage[stage]) {
        byStage[stage] = { completed: [], failed: [] };
      }
      if (result.success) {
        byStage[stage].completed.push(result);
      } else {
        byStage[stage].failed.push(result);
        failed.push(result);
      }
    }

    // 计算阶段状态
    const stageStats = {};
    let brokenStage = null;
    for (const [stage, data] of Object.entries(byStage)) {
      stageStats[stage] = {
        completed: data.completed.length,
        failed: data.failed.length,
        success: data.failed.length === 0,
      };
      if (data.failed.length > 0 && !brokenStage) {
        brokenStage = stage;
      }
    }

    // 提取最终输出
    const finalStage = Object.keys(byStage).pop();
    const finalOutputs = byStage[finalStage]?.completed.map(r => r.output) || [];

    return {
      strategy: 'pipeline',
      success: failed.length === 0,
      byStage,
      stageStats,
      brokenStage,
      finalOutputs,
      errors: failed.map(r => ({ task: r.task, error: r.error, stage: r.stage })),
      stats: {
        total: results.length,
        completed: results.filter(r => r.success).length,
        failed: failed.length,
        stages: Object.keys(byStage).length,
      },
    };
  },

  /**
   * 验证结果
   */
  validate: async (aggregated, validators = []) => {
    const issues = [];

    // 内置验证：流水线不能中断
    if (aggregated.brokenStage) {
      issues.push({
        type: 'PIPELINE_BROKEN',
        message: `流水线在阶段 "${aggregated.brokenStage}" 处中断`,
        severity: 'error',
      });
    }

    // 内置验证：所有阶段必须成功
    for (const [stage, stats] of Object.entries(aggregated.stageStats)) {
      if (!stats.success) {
        issues.push({
          type: 'STAGE_FAILED',
          message: `阶段 "${stage}" 有 ${stats.failed} 个任务失败`,
          severity: 'error',
        });
      }
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

export default pipelinePattern;
