/**
 * 策略选择器 (Strategy Selector) v1.0.0
 *
 * 根据任务特征选择最合适的规划策略
 */

class StrategySelector {
  constructor() {
    this.strategies = this._registerDefaultStrategies();
  }

  /**
   * 注册默认策略
   */
  _registerDefaultStrategies() {
    return {
      sequential: {
        name: 'sequential',
        description: '顺序执行策略',
       适用于: ['简单任务', '单一步骤任务', '线性依赖任务'],
        weight: 1.0,
        confidence: 0.9
      },
      parallel: {
        name: 'parallel',
        description: '并行执行策略',
        适用于: ['独立任务', '多文件操作', '批量处理'],
        weight: 1.0,
        confidence: 0.85
      },
      exploratory: {
        name: 'exploratory',
        description: '探索式执行策略',
        适用于: ['调查任务', '问题定位', '代码分析'],
        weight: 1.0,
        confidence: 0.8
      },
      conservative: {
        name: 'conservative',
        description: '保守执行策略',
        适用于: ['危险操作', '生产环境', '未测试代码'],
        weight: 1.0,
        confidence: 0.75
      },
      aggressive: {
        name: 'aggressive',
        description: '激进执行策略',
        适用于: ['快速原型', '开发环境', '明确需求'],
        weight: 1.0,
        confidence: 0.7
      }
    };
  }

  /**
   * 选择策略
   */
  selectStrategy(task, context = {}, options = {}) {
    const taskType = this._classifyTask(task);
    const environment = context.environment || 'development';
    const hasFailures = options.failureAnalysis != null;

    let strategyName;

    if (hasFailures) {
      // 基于失败分析选择策略
      strategyName = this._selectBasedOnFailure(options.failureAnalysis, options.previousStrategy);
    } else {
      // 基于任务特征选择策略
      strategyName = this._selectBasedOnTask(taskType, environment, context);
    }

    const strategy = this.strategies[strategyName] || this.strategies.sequential;

    return {
      ...strategy,
      taskType,
      environment
    };
  }

  /**
   * 基于任务特征选择
   */
  _selectBasedOnTask(taskType, environment, context) {
    // 危险操作使用保守策略
    if (this._isDangerousOperation(task, context)) {
      return 'conservative';
    }

    // 生产环境使用保守策略
    if (environment === 'production') {
      return 'conservative';
    }

    // 调查任务使用探索式
    if (taskType === 'investigation' || taskType === 'debugging') {
      return 'exploratory';
    }

    // 并行任务
    if (context.parallelizable) {
      return 'parallel';
    }

    // 简单任务
    if (taskType === 'simple') {
      return 'sequential';
    }

    // 默认根据任务类型
    const typeToStrategy = {
      implementation: 'aggressive',
      investigation: 'exploratory',
      refactoring: 'conservative',
      debugging: 'exploratory',
      generic: 'sequential'
    };

    return typeToStrategy[taskType] || 'sequential';
  }

  /**
   * 基于失败选择
   */
  _selectBasedOnFailure(failureAnalysis, previousStrategy) {
    const { primaryError, errorPatterns } = failureAnalysis;

    // 语法错误 - 保守策略
    if (errorPatterns.syntax) {
      return 'conservative';
    }

    // 超时错误 - 增加超时时间，使用顺序策略
    if (errorPatterns.timeout) {
      return 'conservative';
    }

    // 依赖错误 - 先解决依赖
    if (errorPatterns.dependency) {
      return 'conservative';
    }

    // 权限错误 - 检查权限
    if (errorPatterns.permission) {
      return 'conservative';
    }

    // 如果之前是激进策略，改为保守
    if (previousStrategy === 'aggressive') {
      return 'conservative';
    }

    // 如果之前是探索策略，保持或改为顺序
    if (previousStrategy === 'exploratory') {
      return 'sequential';
    }

    // 默认保持当前策略但降低信心
    return previousStrategy || 'sequential';
  }

  /**
   * 分类任务
   */
  _classifyTask(task) {
    const taskStr = typeof task === 'string' ? task : task.description || '';

    // 简单任务特征
    if (/^(ls|cd|pwd|echo|date|whoami)$/i.test(taskStr.trim())) {
      return 'simple';
    }

    // 复杂任务特征
    if (/实现|创建|开发|添加.*功能|构建/.test(taskStr)) return 'implementation';
    if (/调查|分析|研究|检查|查找|搜索/.test(taskStr)) return 'investigation';
    if (/重构|重写|优化|整理|清理/.test(taskStr)) return 'refactoring';
    if (/调试|修复|解决|排查|错误|bug/.test(taskStr)) return 'debugging';

    return 'generic';
  }

  /**
   * 判断是否危险操作
   */
  _isDangerousOperation(task, context = {}) {
    const taskStr = typeof task === 'string' ? task : task.description || '';
    const dangerousPatterns = [
      /rm\s+-rf|rm\s+-r\s+\/|del\s+\/s\/q/i,  // 删除系统文件
      /DROP\s+TABLE|DELETE\s+FROM.*WHERE/i,    // 数据库删除
      /format\s+|mkfs/i,                        // 格式化
      /chmod\s+777|chmod\s+-R\s+777/i,         // 过度权限
      /shutdown|reboot|init\s+0/i,              // 系统关机
      /\|\s*sh|\|\s*bash|eval\s+/i,            // 管道到shell
      /curl.*\|.*sh|wget.*\|.*sh/i              // 下载并执行
    ];

    return dangerousPatterns.some(p => p.test(taskStr));
  }

  /**
   * 注册自定义策略
   */
  registerStrategy(name, strategy) {
    this.strategies[name] = {
      name,
      ...strategy
    };
  }

  /**
   * 获取所有策略
   */
  getStrategies() {
    return { ...this.strategies };
  }
}

module.exports = { StrategySelector };
