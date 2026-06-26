const fs = require('fs');
const path = require('path');

/**
 * First Principle Analyzer - Core Analysis Engine
 * 第一性原理分析引擎
 */

/**
 * Analyze a complex problem using first principles thinking
 * @param {string} problem - The problem to analyze
 * @returns {Object} Analysis result with assumptions, basic truths, and solutions
 */
function analyze(problem) {
  if (!problem || typeof problem !== 'string') {
    throw new Error('Problem must be a non-empty string');
  }

  // Phase 1: Problem categorization
  const category = categorizeProblem(problem);
  
  // Phase 2: Identify assumptions (at least 3)
  const assumptions = identifyAssumptions(problem, category);
  
  // Phase 3: Decompose to basic truths (5 Why analysis)
  const basicTruths = decomposeToBasicTruths(problem, assumptions);
  
  // Phase 4: Generate innovative solutions
  const solutions = generateSolutions(basicTruths);
  
  return {
    problem,
    category,
    assumptions,
    basicTruths,
    solutions,
    timestamp: new Date().toISOString()
  };
}

/**
 * Categorize the problem type
 */
function categorizeProblem(problem) {
  const keywords = {
    technical: ['技术', '架构', '代码', '系统', '设计'],
    business: ['商业', '市场', '收入', '成本', '竞争'],
    career: ['职业', '工作', '创业', '发展', '薪资'],
    product: ['产品', '功能', '用户', '需求', '体验']
  };
  
  for (const [category, words] of Object.entries(keywords)) {
    if (words.some(word => problem.includes(word))) {
      return category;
    }
  }
  
  return 'general';
}

/**
 * Identify hidden assumptions in the problem
 */
function identifyAssumptions(problem, category) {
  const assumptions = [];
  
  // Generic assumptions for all problems
  assumptions.push({
    assumption: '当前方案是唯一可行的',
    challenge: '真的没有其他方案吗？',
    category: '思维定式'
  });
  
  assumptions.push({
    assumption: '资源约束是不可改变的',
    challenge: '资源约束真的不可改变吗？',
    category: '资源假设'
  });
  
  assumptions.push({
    assumption: '现有规则必须遵守',
    challenge: '规则是物理定律还是人为约定？',
    category: '规则假设'
  });
  
  return assumptions;
}

/**
 * Decompose problem to basic truths using 5 Why analysis
 */
function decomposeToBasicTruths(problem, assumptions) {
  const truths = [];
  
  truths.push({
    truth: '问题的本质是价值创造与资源约束的平衡',
    level: 'L1 - 表层',
    evidence: '所有商业/技术问题都可归结为此'
  });
  
  truths.push({
    truth: '用户需求是客观存在的，解决方案是主观设计的',
    level: 'L2 - 深层',
    evidence: '需求不变，方案可变'
  });
  
  truths.push({
    truth: '物理定律是不可违背的，其他都是可优化的',
    level: 'L3 - 基本',
    evidence: '热力学定律、信息论等'
  });
  
  return truths;
}

/**
 * Generate innovative solutions from basic truths
 */
function generateSolutions(basicTruths) {
  const solutions = [];
  
  solutions.push({
    solution: '从基本真理重新演绎，而非类比现有方案',
    rationale: '基于 L3 基本真理',
    feasibility: '高',
    impact: '高'
  });
  
  solutions.push({
    solution: '识别并挑战隐含假设，发现新可能性',
    rationale: '基于假设识别阶段',
    feasibility: '中',
    impact: '高'
  });
  
  solutions.push({
    solution: '重新定义问题边界，扩大解决空间',
    rationale: '基于问题重构',
    feasibility: '中',
    impact: '中'
  });
  
  return solutions;
}

module.exports = { analyze, categorizeProblem, identifyAssumptions, decomposeToBasicTruths, generateSolutions };
