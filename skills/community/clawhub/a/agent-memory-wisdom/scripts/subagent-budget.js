#!/usr/bin/env node
/**
 * 子agent预算分配器
 * 按任务复杂度动态分配迭代预算
 *
 * 用法: node subagent-budget.js <任务描述>
 * 输出: budget值 + 建议模型
 *
 * 注意：修改 COMPLEXITY 中的 model 字段为你实际使用的模型名称
 */

const args = process.argv.slice(2).join(' ').toLowerCase();

// 任务复杂度定义
// ⚙️ 按需修改 model 字段为你实际配置的模型
const COMPLEXITY = {
  simple: {
    keywords: ['搜索', '查天气', '查日历', '查时间', '查汇率', '天气', '时间'],
    budget: 10,
    model: '[YOUR_SIMPLE_MODEL]',       // 替换为轻量模型
    description: '简单查询类任务'
  },
  medium: {
    keywords: ['调研', '分析', '总结', '对比', '整理', '报告', '文案', '写作'],
    budget: 30,
    model: '[YOUR_MEDIUM_MODEL]',       // 替换为中等模型
    description: '中等复杂度任务'
  },
  complex: {
    keywords: ['代码', '编程', '开发', '实现', '架构', '深度研究', '算法'],
    budget: null, // 无上限
    model: '[YOUR_CODE_MODEL]',         // 替换为代码专用模型
    description: '复杂技术任务'
  }
};

function analyzeComplexity(task) {
  let scores = { simple: 0, medium: 0, complex: 0 };

  COMPLEXITY.simple.keywords.forEach(k => { if (task.includes(k)) scores.simple++; });
  COMPLEXITY.medium.keywords.forEach(k => { if (task.includes(k)) scores.medium++; });
  COMPLEXITY.complex.keywords.forEach(k => { if (task.includes(k)) scores.complex++; });

  // 优先级: complex > medium > simple
  if (scores.complex > 0) return COMPLEXITY.complex;
  if (scores.medium > 0) return COMPLEXITY.medium;
  return COMPLEXITY.simple;
}

const result = analyzeComplexity(args);

console.log(JSON.stringify({
  budget: result.budget,
  budgetText: result.budget === null ? 'unlimited' : result.budget,
  model: result.model,
  complexity: result.description,
  task: args
}, null, 2));
