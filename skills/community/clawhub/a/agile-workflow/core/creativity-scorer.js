#!/usr/bin/env node
/**
 * 通用创造性评分系统 v6.0-Phase1-Stage3
 * 
 * 核心功能:
 * 1. 新颖性检测（方案/思路/表达）
 * 2. 复杂性检测（系统/逻辑/关系）
 * 3. 深度检测（分析/思考/影响）
 * 4. 原创性检测（套路/陈词/创新）
 * 
 * 通用设计：适用于代码/文档/方案/分析/写作等所有任务
 */

const fs = require('fs');
const path = require('path');

// ============ 配置 ============

const CONFIG = {
  // 权重配置
  weights: {
    novelty: 0.25,      // 新颖性 25%
    complexity: 0.25,   // 复杂性 25%
    depth: 0.25,        // 深度 25%
    originality: 0.25   // 原创性 25%
  },
  
  // 质量等级
  levels: {
    S: 90,  // 卓越
    A: 80,  // 优秀
    B: 70,  // 良好
    C: 60,  // 合格
    D: 0    // 需改进
  },
  
  // 任务类型配置
  taskTypes: {
    'code': {
      noveltyKeywords: ['新', '创新', '优化', '改进', '重构', '升级'],
      complexityMetrics: ['modules', 'dependencies', 'layers'],
      depthKeywords: ['原理', '本质', '根因', '机制', '架构'],
      cliches: ['TODO', 'FIXME', 'placeholder', 'temp']
    },
    'document': {
      noveltyKeywords: ['新视角', '新方法', '新思路', '创新', '突破'],
      complexityMetrics: ['sections', 'subsections', 'references'],
      depthKeywords: ['深入', '本质', '核心', '关键', '根本'],
      cliches: ['总之', '综上所述', '显而易见', '毫无疑问']
    },
    'design': {
      noveltyKeywords: ['创新', '独特', '新颖', '首创', '突破'],
      complexityMetrics: ['components', 'interactions', 'constraints'],
      depthKeywords: ['考虑', '影响', '风险', '权衡', '取舍'],
      cliches: ['常规', '标准', '通用', '典型']
    },
    'analysis': {
      noveltyKeywords: ['发现', '洞察', '新发现', '意外', '出乎意料'],
      complexityMetrics: ['variables', 'correlations', 'factors'],
      depthKeywords: ['根因', '本质', '规律', '趋势', '模式'],
      cliches: ['数据表明', '可以看出', '综上所述']
    },
    'default': {
      noveltyKeywords: ['新', '创新', '独特', '新颖', '突破'],
      complexityMetrics: ['elements', 'relations', 'levels'],
      depthKeywords: ['深入', '本质', '核心', '根本', '关键'],
      cliches: ['总之', '综上所述', '显而易见', '毫无疑问']
    }
  }
};

// ============ 创造性评分器 ============

class CreativityScorer {
  constructor(taskType = 'default') {
    this.taskType = taskType;
    this.config = CONFIG.taskTypes[taskType] || CONFIG.taskTypes.default;
    this.weights = CONFIG.weights;
  }

  /**
   * 计算创造性总分
   */
  calculateCreativityScore(content, baseline = null) {
    console.log(`🎨 开始创造性评分：${this.taskType}`);

    const scores = {
      novelty: this.detectNovelty(content, baseline),
      complexity: this.detectComplexity(content),
      depth: this.detectDepth(content),
      originality: this.detectOriginality(content, baseline)
    };

    const totalScore = Math.round(
      scores.novelty * this.weights.novelty +
      scores.complexity * this.weights.complexity +
      scores.depth * this.weights.depth +
      scores.originality * this.weights.originality
    );

    const level = this.getCreativityLevel(totalScore);
    const suggestions = this.generateSuggestions(scores);

    const result = {
      total: totalScore,
      level,
      scores,
      suggestions,
      timestamp: Date.now()
    };

    console.log(`📊 创造性评分：${totalScore} 分 (${level}级)`);
    console.log(`   新颖性：${scores.novelty}`);
    console.log(`   复杂性：${scores.complexity}`);
    console.log(`   深度：${scores.depth}`);
    console.log(`   原创性：${scores.originality}`);

    if (suggestions.length > 0) {
      console.log(`\n💡 优化建议:`);
      suggestions.forEach((s, i) => console.log(`   ${i + 1}. ${s}`));
    }

    return result;
  }

  // ============ 新颖性检测 ============

  /**
   * 检测新颖性（方案/思路/表达）
   */
  detectNovelty(content, baseline) {
    const subScores = {
      solution: this.detectSolutionNovelty(content, baseline),
      approach: this.detectApproachNovelty(content),
      expression: this.detectExpressionNovelty(content)
    };

    // 平均评分
    const score = Math.round(
      (subScores.solution + subScores.approach + subScores.expression) / 3
    );

    console.log(`   新颖性细分：方案${subScores.solution} 思路${subScores.approach} 表达${subScores.expression}`);
    return score;
  }

  /**
   * 方案创新检测
   */
  detectSolutionNovelty(content, baseline) {
    // 检测创新关键词
    const noveltyKeywords = this.config.noveltyKeywords;
    let noveltyCount = 0;

    for (const keyword of noveltyKeywords) {
      const regex = new RegExp(keyword, 'g');
      const matches = content.match(regex);
      if (matches) {
        noveltyCount += matches.length;
      }
    }

    // 与基准对比（如果有）
    if (baseline) {
      const uniqueElements = this.findUniqueElements(content, baseline);
      noveltyCount += uniqueElements.length * 2;
    }

    // 密度评分（每千字创新点数）
    const density = (noveltyCount / content.length) * 1000;
    return Math.min(100, Math.round(density * 10));
  }

  /**
   * 思路创新检测
   */
  detectApproachNovelty(content) {
    // 检测独特角度
    const uniqueAngles = this.detectUniqueAngles(content);
    
    // 检测逻辑创新
    const logicInnovations = this.detectLogicInnovations(content);
    
    // 检测框架创新
    const frameworkInnovations = this.detectFrameworkInnovations(content);

    // 综合评分
    const score = (uniqueAngles + logicInnovations + frameworkInnovations) / 3;
    return Math.min(100, Math.round(score));
  }

  /**
   * 表达创新检测
   */
  detectExpressionNovelty(content) {
    // 检测结构创新
    const structureVariety = this.detectStructureVariety(content);
    
    // 检测呈现方式
    const presentationVariety = this.detectPresentationVariety(content);
    
    // 检测交互创新（如果有）
    const interactionVariety = this.detectInteractionVariety(content);

    // 综合评分
    const score = (structureVariety + presentationVariety + interactionVariety) / 3;
    return Math.min(100, Math.round(score));
  }

  // ============ 复杂性检测 ============

  /**
   * 检测复杂性（系统/逻辑/关系）
   */
  detectComplexity(content) {
    const subScores = {
      system: this.detectSystemComplexity(content),
      logic: this.detectLogicComplexity(content),
      relations: this.detectRelationComplexity(content)
    };

    // 平均评分
    const score = Math.round(
      (subScores.system + subScores.logic + subScores.relations) / 3
    );

    console.log(`   复杂性细分：系统${subScores.system} 逻辑${subScores.logic} 关系${subScores.relations}`);
    return score;
  }

  /**
   * 系统复杂度检测
   */
  detectSystemComplexity(content) {
    // 检测模块/组件数量
    const modules = this.countModules(content);
    
    // 检测依赖关系
    const dependencies = this.countDependencies(content);
    
    // 检测层次结构
    const layers = this.countLayers(content);

    // 综合评分
    const score = modules * 5 + dependencies * 3 + layers * 10;
    return Math.min(100, Math.round(score));
  }

  /**
   * 逻辑复杂度检测
   */
  detectLogicComplexity(content) {
    // 检测条件分支
    const conditions = this.countConditions(content);
    
    // 检测因果链
    const causeEffectChains = this.countCauseEffectChains(content);
    
    // 检测递归/循环
    const recursions = this.countRecursions(content);

    // 综合评分
    const score = conditions * 2 + causeEffectChains * 5 + recursions * 10;
    return Math.min(100, Math.round(score));
  }

  /**
   * 关系复杂度检测
   */
  detectRelationComplexity(content) {
    // 检测实体数量
    const entities = this.countEntities(content);
    
    // 检测关系数量
    const relations = this.countRelations(content);
    
    // 检测影响范围
    const impacts = this.countImpacts(content);

    // 关系密度评分
    const maxRelations = entities * (entities - 1) / 2;
    const density = maxRelations > 0 ? relations / maxRelations : 0;
    
    // 综合评分
    const score = entities * 2 + relations * 3 + impacts * 5 + density * 50;
    return Math.min(100, Math.round(score));
  }

  // ============ 深度检测 ============

  /**
   * 检测深度（分析/思考/影响）
   */
  detectDepth(content) {
    const subScores = {
      analysis: this.detectAnalysisDepth(content),
      thinking: this.detectThinkingDepth(content),
      impact: this.detectImpactDepth(content)
    };

    // 平均评分
    const score = Math.round(
      (subScores.analysis + subScores.thinking + subScores.impact) / 3
    );

    console.log(`   深度细分：分析${subScores.analysis} 思考${subScores.thinking} 影响${subScores.impact}`);
    return score;
  }

  /**
   * 分析深度检测
   */
  detectAnalysisDepth(content) {
    // 检测深度分析关键词
    const depthKeywords = this.config.depthKeywords;
    let depthCount = 0;

    for (const keyword of depthKeywords) {
      const regex = new RegExp(keyword, 'g');
      const matches = content.match(regex);
      if (matches) {
        depthCount += matches.length;
      }
    }

    // 检测根因分析
    const rootCauseAnalysis = this.detectRootCauseAnalysis(content);
    
    // 检测本质探讨
    const essenceDiscussion = this.detectEssenceDiscussion(content);

    // 综合评分
    const score = depthCount * 5 + rootCauseAnalysis * 20 + essenceDiscussion * 30;
    return Math.min(100, Math.round(score));
  }

  /**
   * 思考深度检测
   */
  detectThinkingDepth(content) {
    // 检测抽象层次
    const abstractionLevels = this.detectAbstractionLevels(content);
    
    // 检测概括能力
    const generalization = this.detectGeneralization(content);
    
    // 检测哲学思考
    const philosophicalThinking = this.detectPhilosophicalThinking(content);

    // 综合评分
    const score = abstractionLevels * 10 + generalization * 20 + philosophicalThinking * 30;
    return Math.min(100, Math.round(score));
  }

  /**
   * 影响深度检测
   */
  detectImpactDepth(content) {
    // 检测短期影响
    const shortTermImpacts = this.countShortTermImpacts(content);
    
    // 检测长期影响
    const longTermImpacts = this.countLongTermImpacts(content);
    
    // 检测全局影响
    const globalImpacts = this.countGlobalImpacts(content);

    // 综合评分（长期和全局影响权重更高）
    const score = shortTermImpacts * 5 + longTermImpacts * 15 + globalImpacts * 25;
    return Math.min(100, Math.round(score));
  }

  // ============ 原创性检测 ============

  /**
   * 检测原创性（套路/陈词/创新）
   */
  detectOriginality(content, baseline) {
    const subScores = {
      cliches: this.detectCliches(content),
      overused: this.detectOverusedPhrases(content),
      innovations: this.detectInnovations(content, baseline)
    };

    // 综合评分（创新加分，套路减分）
    const score = subScores.innovations - (100 - subScores.cliches) * 0.5 - (100 - subScores.overused) * 0.3;
    
    const finalScore = Math.max(0, Math.min(100, Math.round(score)));

    console.log(`   原创性细分：反套路${subScores.cliches} 反陈词${subScores.overused} 创新${subScores.innovations}`);
    return finalScore;
  }

  /**
   * 套路识别
   */
  detectCliches(content) {
    const cliches = this.config.cliches;
    let detectedCount = 0;

    for (const cliche of cliches) {
      if (content.includes(cliche)) {
        detectedCount++;
      }
    }

    // 每出现一个套路减 20 分，从 100 分开始
    const score = Math.max(0, 100 - detectedCount * 20);
    return score;
  }

  /**
   * 陈词滥调检测
   */
  detectOverusedPhrases(content) {
    const overusedPhrases = [
      '总之', '综上所述', '显而易见', '毫无疑问',
      '非常', '十分', '特别', '极其',
      '好的', '优秀的', '出色的', '卓越的'
    ];

    let frequency = 0;
    for (const phrase of overusedPhrases) {
      const regex = new RegExp(phrase, 'g');
      const matches = content.match(regex);
      if (matches) {
        frequency += matches.length;
      }
    }

    // 频率越高分数越低
    const score = Math.max(0, 100 - frequency * 5);
    return score;
  }

  /**
   * 创新点检测
   */
  detectInnovations(content, baseline) {
    // 找出创新点
    const innovations = this.findInnovations(content, baseline);
    
    // 评估创新点质量
    const qualityScore = this.evaluateInnovationQuality(innovations);

    // 综合评分
    const score = innovations.length * 10 + qualityScore;
    return Math.min(100, Math.round(score));
  }

  // ============ 工具方法 ============

  /**
   * 获取创造性等级
   */
  getCreativityLevel(score) {
    for (const [level, threshold] of Object.entries(CONFIG.levels)) {
      if (score >= threshold) {
        return level;
      }
    }
    return 'D';
  }

  /**
   * 生成优化建议
   */
  generateSuggestions(scores) {
    const suggestions = [];

    if (scores.novelty < 70) {
      suggestions.push('增加创新点，提升新颖性');
      suggestions.push('尝试新的方案、思路或表达方式');
    }

    if (scores.complexity < 70) {
      suggestions.push('增加系统/逻辑/关系的复杂性');
      suggestions.push('考虑更多维度、层次和关联');
    }

    if (scores.depth < 70) {
      suggestions.push('深化分析和思考');
      suggestions.push('探讨本质、根因和长远影响');
    }

    if (scores.originality < 70) {
      suggestions.push('避免使用套路和陈词滥调');
      suggestions.push('寻找独特的创新点和突破');
    }

    return suggestions;
  }

  // ============ 占位实现（需要具体任务类型实现） ============

  findUniqueElements(content, baseline) { return []; }
  detectUniqueAngles(content) { return 0; }
  detectLogicInnovations(content) { return 0; }
  detectFrameworkInnovations(content) { return 0; }
  detectStructureVariety(content) { return 0; }
  detectPresentationVariety(content) { return 0; }
  detectInteractionVariety(content) { return 0; }
  countModules(content) { return 0; }
  countDependencies(content) { return 0; }
  countLayers(content) { return 0; }
  countConditions(content) { return 0; }
  countCauseEffectChains(content) { return 0; }
  countRecursions(content) { return 0; }
  countEntities(content) { return 0; }
  countRelations(content) { return 0; }
  countImpacts(content) { return 0; }
  detectRootCauseAnalysis(content) { return 0; }
  detectEssenceDiscussion(content) { return 0; }
  detectAbstractionLevels(content) { return 0; }
  detectGeneralization(content) { return 0; }
  detectPhilosophicalThinking(content) { return 0; }
  countShortTermImpacts(content) { return 0; }
  countLongTermImpacts(content) { return 0; }
  countGlobalImpacts(content) { return 0; }
  findInnovations(content, baseline) { return []; }
  evaluateInnovationQuality(innovations) { return 0; }
}

// ============ CLI 接口 ============

function printHelp() {
  console.log(`
创造性评分系统 v6.0-Phase1-Stage3

用法：node creativity-scorer.js <命令> [选项]

命令:
  test                测试评分系统
  score <文件>        评分文件
  compare <文件 1> <文件 2>  对比评分

示例:
  node creativity-scorer.js test
  node creativity-scorer.js score document.md
  node creativity-scorer.js compare v1.md v2.md
`);
}

// ============ 主程序 ============

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  if (!command || command === '--help') {
    printHelp();
    return;
  }

  const scorer = new CreativityScorer('default');

  switch (command) {
    case 'test':
      console.log('🧪 测试创造性评分系统...\n');
      
      const testContent = '这是一个创新方案，采用了新的方法和思路。深入分析了问题的本质和根因，考虑了短期和长期影响。';
      const result = scorer.calculateCreativityScore(testContent);
      
      console.log('\n✅ 测试完成');
      break;

    case 'score':
      const file = args[1];
      if (!file) {
        console.log('❌ 请指定文件路径');
        return;
      }

      try {
        const content = fs.readFileSync(file, 'utf-8');
        const result = scorer.calculateCreativityScore(content);
        console.log('\n✅ 评分完成');
      } catch (error) {
        console.error('❌ 评分失败:', error.message);
      }
      break;

    case 'compare':
      const file1 = args[1];
      const file2 = args[2];
      if (!file1 || !file2) {
        console.log('❌ 请指定两个文件路径');
        return;
      }

      try {
        const content1 = fs.readFileSync(file1, 'utf-8');
        const content2 = fs.readFileSync(file2, 'utf-8');
        
        const result1 = scorer.calculateCreativityScore(content1);
        const result2 = scorer.calculateCreativityScore(content2);
        
        console.log('\n📊 对比结果:');
        console.log(`文件 1: ${result1.total} 分 (${result1.level}级)`);
        console.log(`文件 2: ${result2.total} 分 (${result2.level}级)`);
        console.log(`差异：${result2.total - result1.total} 分`);
      } catch (error) {
        console.error('❌ 对比失败:', error.message);
      }
      break;

    default:
      console.log(`未知命令：${command}`);
      printHelp();
  }
}

// 导出 API
module.exports = { CreativityScorer, CONFIG };

// 运行 CLI
if (require.main === module) {
  main().catch(console.error);
}
