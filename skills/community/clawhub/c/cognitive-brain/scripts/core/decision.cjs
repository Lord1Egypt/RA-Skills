#!/usr/bin/env node
/**
 * Cognitive Brain - 决策引擎模块
 * 基于上下文和记忆做出决策
 */

const { createLogger } = require('../../src/utils/logger.cjs');
const logger = createLogger('decision');
const fs = require('fs');
const path = require('path');

const HOME = process.env.HOME || '/root';
const SKILL_DIR = path.join(HOME, '.openclaw/workspace/skills/cognitive-brain');
const DECISION_HISTORY_PATH = path.join(SKILL_DIR, '.decision-history.json');

// 决策历史
let decisionHistory = [];

/**
 * 加载决策历史
 */
function loadHistory() {
  try {
    if (fs.existsSync(DECISION_HISTORY_PATH)) {
      decisionHistory = JSON.parse(fs.readFileSync(DECISION_HISTORY_PATH, 'utf8'));
    }
  } catch (e) { console.error("[decision] 错误:", e.message);
    decisionHistory = [];
  }
}

/**
 * 保存决策历史
 */
function saveHistory() {
  try {
    fs.writeFileSync(DECISION_HISTORY_PATH, JSON.stringify(decisionHistory.slice(-1000), null, 2));
  } catch (e) { console.error("[decision] 错误:", e.message);
    // ignore
  }
}

/**
 * 决策选项
 */
class DecisionOption {
  constructor(name, description, score = 0) {
    this.name = name;
    this.description = description;
    this.score = score;
    this.factors = {};
    this.metadata = {};
  }

  addFactor(name, value, weight = 1) {
    this.factors[name] = { value, weight };
    this.score += value * weight;
  }
}

/**
 * 决策上下文
 */
class DecisionContext {
  constructor() {
    this.userIntent = null;
    this.userPreference = null;
    this.memoryContext = [];
    this.workingMemory = null;
    this.constraints = [];
    this.resources = {};
    this.timeAvailable = null;
  }

  setIntent(intent) {
    this.userIntent = intent;
    return this;
  }

  setPreference(preference) {
    this.userPreference = preference;
    return this;
  }

  setMemory(memories) {
    this.memoryContext = memories;
    return this;
  }

  addConstraint(constraint) {
    this.constraints.push(constraint);
    return this;
  }

  setResource(name, available) {
    this.resources[name] = available;
    return this;
  }
}

/**
 * 决策引擎
 */
class DecisionEngine {
  constructor() {
    this.rules = [];
    this.strategies = new Map();
  }

  /**
   * 添加决策规则
   */
  addRule(name, condition, action, priority = 0) {
    this.rules.push({ name, condition, action, priority });
    this.rules.sort((a, b) => b.priority - a.priority);
  }

  /**
   * 添加策略
   */
  addStrategy(name, fn) {
    this.strategies.set(name, fn);
  }

  /**
   * 评估选项
   */
  evaluateOption(option, context) {
    // 用户意图匹配
    if (context.userIntent) {
      const intentMatch = this.matchIntent(option, context.userIntent);
      option.addFactor('intent_match', intentMatch ? 1 : 0, 0.3);
    }

    // 用户偏好匹配
    if (context.userPreference) {
      const prefMatch = this.matchPreference(option, context.userPreference);
      option.addFactor('preference_match', prefMatch, 0.2);
    }

    // 资源可用性
    const resourceScore = this.checkResources(option, context.resources);
    option.addFactor('resource_availability', resourceScore, 0.15);

    // 约束满足
    const constraintScore = this.checkConstraints(option, context.constraints);
    option.addFactor('constraint_satisfaction', constraintScore, 0.2);

    // 历史成功率
    const historyScore = this.getHistoryScore(option.name);
    option.addFactor('historical_success', historyScore, 0.15);

    return option;
  }

  /**
   * 匹配意图
   */
  matchIntent(option, intent) {
    // 简单匹配：选项名称或描述包含意图关键词
    const keywords = intent.split(/\s+/);
    const text = `${option.name} ${option.description}`.toLowerCase();
    return keywords.some(k => text.includes(k.toLowerCase()));
  }

  /**
   * 匹配偏好
   */
  matchPreference(option, preference) {
    if (!preference) return 0.5;

    let score = 0.5;

    // 沟通风格
    if (preference.communicationStyle === 'technical' &&
        option.description.includes('技术')) {
      score += 0.2;
    }

    // 详细程度
    if (preference.levelOfDetail === 'detailed' &&
        option.description.includes('详细')) {
      score += 0.1;
    }

    return Math.min(1, score);
  }

  /**
   * 检查资源
   */
  checkResources(option, resources) {
    if (!resources || Object.keys(resources).length === 0) return 1;

    // 假设所有资源可用
    return Object.values(resources).every(v => v) ? 1 : 0.5;
  }

  /**
   * 检查约束
   */
  checkConstraints(option, constraints) {
    if (!constraints || constraints.length === 0) return 1;

    let satisfied = 0;
    for (const constraint of constraints) {
      if (constraint(option)) {
        satisfied++;
      }
    }
    return satisfied / constraints.length;
  }

  /**
   * 获取历史得分
   */
  getHistoryScore(optionName) {
    const related = decisionHistory.filter(d => d.option === optionName);
    if (related.length === 0) return 0.5;

    const successCount = related.filter(d => d.outcome === 'success').length;
    return successCount / related.length;
  }

  /**
   * 做出决策
   */
  decide(options, context) {
    // 评估所有选项
    const evaluated = options.map(opt => this.evaluateOption(opt, context));

    // 按得分排序
    evaluated.sort((a, b) => b.score - a.score);

    // 应用规则
    for (const rule of this.rules) {
      if (rule.condition(evaluated[0], context)) {
        const result = rule.action(evaluated[0], context);
        if (result) {
          return {
            decision: result,
            reasoning: `Rule applied: ${rule.name}`,
            alternatives: evaluated.slice(1, 3),
            timestamp: Date.now()
          };
        }
      }
    }

    // 返回最佳选项
    return {
      decision: evaluated[0],
      reasoning: 'Score-based selection',
      alternatives: evaluated.slice(1, 3),
      timestamp: Date.now()
    };
  }

  /**
   * 记录决策结果
   */
  recordOutcome(decisionId, outcome, feedback = null) {
    const record = decisionHistory.find(d => d.id === decisionId);
    if (record) {
      record.outcome = outcome;
      record.feedback = feedback;
      record.resolvedAt = Date.now();
      saveHistory();
    }
  }
}

/**
 * 创建常用决策
 */
function createDefaultOptions(intent) {
  const options = [];

  switch (intent) {
    case 'question':
      options.push(
        new DecisionOption('direct_answer', '直接回答问题'),
        new DecisionOption('search_then_answer', '搜索后回答'),
        new DecisionOption('clarify_first', '先澄清问题再回答')
      );
      break;

    case 'request':
      options.push(
        new DecisionOption('do_directly', '直接执行'),
        new DecisionOption('use_tools', '使用工具执行'),
        new DecisionOption('delegate_subagent', '委派给子代理'),
        new DecisionOption('ask_clarification', '请求澄清')
      );
      break;

    case 'search':
      options.push(
        new DecisionOption('web_search', '网络搜索'),
        new DecisionOption('memory_search', '记忆搜索'),
        new DecisionOption('hybrid_search', '混合搜索')
      );
      break;

    default:
      options.push(
        new DecisionOption('respond_directly', '直接响应'),
        new DecisionOption('ask_clarification', '请求澄清')
      );
  }

  return options;
}

// ===== 主函数 =====
async function main() {
  const action = process.argv[2];
  const args = process.argv.slice(3);

  loadHistory();

  const engine = new DecisionEngine();

  // 添加默认规则
  engine.addRule(
    'safety_check',
    (option, ctx) => option.description.includes('危险'),
    () => new DecisionOption('reject', '拒绝危险操作', 0)
  );

  engine.addRule(
    'resource_constraint',
    (option, ctx) => ctx.resources && !ctx.resources.time,
    (option) => {
      option.addFactor('time_constraint', 0.5, 0.1);
      return null; // 不覆盖，只调整
    }
  );

  switch (action) {
    case 'decide': {
      const intent = args[0] || 'unknown';
      const context = new DecisionContext();
      context.setIntent(intent);

      const options = createDefaultOptions(intent);
      const result = engine.decide(options, context);

      console.log('🎯 决策结果:');
      console.log(JSON.stringify(result, null, 2));
      break;
    }

    case 'history': {
      console.log('📋 决策历史:');
      console.log(`   总计: ${decisionHistory.length} 条`);
      const recent = decisionHistory.slice(-10);
      recent.forEach((d, i) => {
        console.log(`   ${i + 1}. ${d.option} - ${d.outcome || 'pending'}`);
      });
      break;
    }

    default:
      console.log(`
决策引擎模块

用法:
  node decision.cjs decide [intent]   # 根据意图做决策
  node decision.cjs history           # 查看决策历史

示例:
  node decision.cjs decide question
  node decision.cjs decide request
      `);
  }
}

main();

