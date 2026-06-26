/**
 * Fan-Out Pattern - 扇出模式
 * 
 * 适用场景：
 * - 一个任务分解为多个独立子任务
 * - 探索多种方案/答案
 * - A/B 测试、多方案对比
 * 
 * @example
 * const result = await orchestrator.execute({
 *   task: '设计用户登录方案',
 *   pattern: 'fan-out',
 *   fanOut: 5,  // 生成 5 种不同方案
 *   subTasks: [
 *     { task: '方案 1: 传统密码登录', agent: 'designer', variation: 'traditional' },
 *     { task: '方案 2: 手机验证码登录', agent: 'designer', variation: 'sms' },
 *     { task: '方案 3: 第三方 OAuth 登录', agent: 'designer', variation: 'oauth' },
 *     { task: '方案 4: 生物识别登录', agent: 'designer', variation: 'biometric' },
 *     { task: '方案 5: 无密码魔法链接', agent: 'designer', variation: 'magic-link' },
 *   ],
 *   fanIn: {
 *     task: '对比所有方案，推荐最佳选择',
 *     agent: 'architect',
 *   }
 * });
 */

export const fanOutPattern = {
  name: 'fan-out',
  description: '一个任务扇出为多个独立探索，可选扇入聚合',

  /**
   * 分解任务
   */
  decompose: async (task, context, options = {}) => {
    const { fanOut = 3, subTasks = [], fanIn = null } = options;
    const tasks = [];
    const timestamp = Date.now();

    // Fan-Out 阶段：生成多个变体
    const outTasks = subTasks.length > 0 
      ? subTasks 
      : Array.from({ length: fanOut }, (_, i) => ({
          task: `${task} (方案 ${i + 1}/${fanOut})`,
          variation: `variant-${i + 1}`,
        }));

    for (let i = 0; i < outTasks.length; i++) {
      const st = outTasks[i];
      tasks.push({
        id: `fanout-${timestamp}-${i}`,
        task: st.task,
        dependencies: [],
        context: { ...context, variation: st.variation, index: i },
        priority: 1,
        agent: st.agent,
        phase: 'fan-out',
      });
    }

    // Fan-In 阶段：聚合（可选）
    if (fanIn) {
      tasks.push({
        id: `fanin-${timestamp}`,
        task: fanIn.task,
        dependencies: tasks.map(t => t.id),
        context: { ...context, fanIn: true },
        priority: 2,
        agent: fanIn.agent,
        phase: 'fan-in',
      });
    }

    return tasks;
  },

  /**
   * 聚合结果
   */
  aggregate: async (results) => {
    const fanOutResults = results.filter(r => r.phase === 'fan-out' && r.success);
    const fanInResults = results.filter(r => r.phase === 'fan-in' && r.success);
    const failed = results.filter(r => !r.success);

    // 提取变体结果
    const variations = fanOutResults.map(r => ({
      variation: r.context?.variation || r.taskId,
      output: r.output,
      metadata: r.metadata,
    }));

    return {
      strategy: 'fan-out',
      success: fanInResults.length > 0 || (fanOutResults.length > 0 && failed.length === 0),
      variations,
      fanInOutput: fanInResults.length > 0 ? fanInResults[0].output : null,
      finalOutput: fanInResults.length > 0 ? fanInResults[0].output : variations,
      errors: failed.map(r => ({ task: r.task, error: r.error, phase: r.phase })),
      stats: {
        total: results.length,
        fanOutCompleted: fanOutResults.length,
        fanInCompleted: fanInResults.length,
        failed: failed.length,
        variationCount: variations.length,
      },
    };
  },

  /**
   * 验证结果
   */
  validate: async (aggregated, validators = []) => {
    const issues = [];

    // 内置验证：至少有一个变体成功
    if (aggregated.stats.fanOutCompleted === 0) {
      issues.push({
        type: 'NO_VARIATIONS',
        message: '所有变体方案都失败了',
        severity: 'error',
      });
    }

    // 内置验证：变体数量不足时警告
    const expectedVariations = aggregated.stats.total - (aggregated.stats.fanInCompleted > 0 ? 1 : 0);
    if (aggregated.stats.fanOutCompleted < expectedVariations && expectedVariations > 1) {
      issues.push({
        type: 'FEW_VARIATIONS',
        message: `只有 ${aggregated.stats.fanOutCompleted}/${expectedVariations} 个变体成功`,
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

  /**
   * 选择最佳变体（辅助函数）
   */
  selectBest: async (variations, criteria) => {
    if (!variations || variations.length === 0) {
      return null;
    }

    // 简单评分：根据 criteria 函数打分
    const scored = variations.map((v, i) => ({
      ...v,
      score: typeof criteria === 'function' ? criteria(v, i) : 0,
    }));

    scored.sort((a, b) => b.score - a.score);
    return scored[0];
  },
};

export default fanOutPattern;
