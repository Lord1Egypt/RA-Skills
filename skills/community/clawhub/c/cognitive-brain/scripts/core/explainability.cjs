#!/usr/bin/env node
/**
 * Cognitive Brain - 可解释性模块
 * 解释 Agent 的决策和行为
 */

const { createLogger } = require('../../src/utils/logger.cjs');
const logger = createLogger('explainability');
const fs = require('fs');
const path = require('path');

const HOME = process.env.HOME || '/root';
const SKILL_DIR = path.join(HOME, '.openclaw/workspace/skills/cognitive-brain');
const EXPLANATION_LOG_PATH = path.join(SKILL_DIR, '.explanation-log.json');

// 解释日志
let explanationLog = [];

/**
 * 加载日志
 */
function load() {
  try {
    if (fs.existsSync(EXPLANATION_LOG_PATH)) {
      explanationLog = JSON.parse(fs.readFileSync(EXPLANATION_LOG_PATH, 'utf8'));
    }
  } catch (e) { console.error("[explainability] 错误:", e.message);
    explanationLog = [];
  }
}

/**
 * 保存日志
 */
function save() {
  try {
    fs.writeFileSync(EXPLANATION_LOG_PATH, JSON.stringify(explanationLog.slice(-500), null, 2));
  } catch (e) { console.error("[explainability] 错误:", e.message);
    // ignore
  }
}

/**
 * 解释决策
 */
function explainDecision(decision, context, factors) {
  const explanation = {
    id: `exp_${Date.now()}`,
    timestamp: Date.now(),
    decision: decision.name || decision,
    reasoning: [],
    factors: [],
    confidence: decision.score || 0,
    alternatives: []
  };

  // 解释决策因素
  if (factors) {
    for (const [name, factor] of Object.entries(factors)) {
      explanation.factors.push({
        name,
        value: factor.value,
        weight: factor.weight,
        contribution: factor.value * factor.weight
      });

      explanation.reasoning.push(
        `${name} 得分 ${factor.value.toFixed(2)}，权重 ${factor.weight}，贡献 ${(factor.value * factor.weight).toFixed(2)}`
      );
    }
  }

  // 添加上下文解释
  if (context) {
    if (context.userIntent) {
      explanation.reasoning.push(`用户意图: ${context.userIntent}`);
    }
    if (context.userPreference) {
      explanation.reasoning.push(`符合用户偏好`);
    }
  }

  // 记录
  load();
  explanationLog.push(explanation);
  save();

  return explanation;
}

/**
 * 解释记忆召回
 */
function explainRecall(query, results, method) {
  const explanation = {
    id: `exp_${Date.now()}`,
    timestamp: Date.now(),
    type: 'recall',
    query,
    method,
    resultsCount: results.length,
    reasoning: [],
    topResults: results.slice(0, 3).map(r => ({
      summary: r.summary,
      score: r.importance || r.score
    }))
  };

  // 解释搜索方法
  switch (method) {
    case 'keyword':
      explanation.reasoning.push('使用关键词匹配搜索');
      break;
    case 'vector':
      explanation.reasoning.push('使用向量相似度搜索');
      break;
    case 'hybrid':
      explanation.reasoning.push('使用混合搜索（关键词 + 向量）');
      break;
    case 'association':
      explanation.reasoning.push('通过联想网络激活');
      break;
    default:
      explanation.reasoning.push(`使用 ${method} 方法`);
  }

  // 解释结果排序
  if (results.length > 0) {
    explanation.reasoning.push(`返回 ${results.length} 条结果，按重要性排序`);
  }

  load();
  explanationLog.push(explanation);
  save();

  return explanation;
}

/**
 * 新增：详细解释记忆检索结果
 */
function explainRecallDetailed(query, memories, searchMethod = 'hybrid') {
  const explanation = {
    id: `exp_${Date.now()}`,
    timestamp: Date.now(),
    type: 'recall_detailed',
    query,
    method: searchMethod,
    results: [],
    reasoning: []
  };

  // 解释每条检索结果
  memories.forEach((memory, index) => {
    const resultExplanation = {
      rank: index + 1,
      memoryId: memory.id,
      summary: memory.summary?.slice(0, 50) + '...',
      relevanceScore: memory.relevance || 0,
      matchReasons: []
    };

    // 分析匹配原因
    if (query && memory.summary) {
      const queryWords = query.toLowerCase().split(/\s+/);
      const matchedWords = queryWords.filter(w => 
        memory.summary.toLowerCase().includes(w)
      );
      if (matchedWords.length > 0) {
        resultExplanation.matchReasons.push({
          type: 'keyword_match',
          detail: `关键词匹配: ${matchedWords.join(', ')}`
        });
      }
    }

    if (memory.semanticScore || memory.relevance) {
      resultExplanation.matchReasons.push({
        type: 'semantic_similarity',
        detail: `语义相似度: ${((memory.semanticScore || memory.relevance) * 100).toFixed(1)}%`
      });
    }

    if (memory.timestamp) {
      const tsObj = new Date(memory.timestamp);
      if (!isNaN(tsObj.getTime())) {
        const ageHours = (Date.now() - tsObj.getTime()) / 3600000;
        if (ageHours < 24 && ageHours >= 0) {
          resultExplanation.matchReasons.push({
            type: 'recency',
            detail: `最近记忆 (${Math.floor(ageHours)}小时前)`
          });
        }
      }
    }

    if (memory.importance > 0.8) {
      resultExplanation.matchReasons.push({
        type: 'importance',
        detail: `高重要性 (${(memory.importance * 100).toFixed(0)}%)`
      });
    }

    if (memory.emotions?.dominantEmotion) {
      resultExplanation.matchReasons.push({
        type: 'emotion',
        detail: `情感: ${memory.emotions.dominantEmotion}`
      });
    }

    explanation.results.push(resultExplanation);
  });

  explanation.reasoning.push(`检索方法: ${searchMethod}`);
  explanation.reasoning.push(`返回结果: ${memories.length} 条`);

  load();
  explanationLog.push(explanation);
  save();

  return explanation;
}

/**
 * 新增：生成用户可读的解释
 */
function generateUserFriendlyExplanation(explanation) {
  const lines = [];

  if (explanation.type === 'recall_detailed') {
    lines.push(`📌 检索 "${explanation.query}" 的结果:`);
    
    explanation.results.slice(0, 3).forEach(result => {
      lines.push(`\n${result.rank}. ${result.summary}`);
      result.matchReasons.forEach(reason => {
        lines.push(`   • ${reason.detail}`);
      });
    });
  } else {
    lines.push(`🤔 决策 "${explanation.decision || explanation.type}":`);
    (explanation.reasoning || []).forEach(r => lines.push(`  • ${r}`));
  }

  return lines.join('\n');
}

/**
 * 解释行动选择
 */
function explainAction(action, alternatives, context) {
  const explanation = {
    id: `exp_${Date.now()}`,
    timestamp: Date.now(),
    type: 'action',
    selectedAction: action,
    alternatives: alternatives || [],
    context: {},
    reasoning: []
  };

  // 解释为什么选择这个行动
  if (context) {
    if (context.required) {
      explanation.reasoning.push(`此行动是必需的: ${context.required}`);
    }
    if (context.safety) {
      explanation.reasoning.push(`安全考虑: ${context.safety}`);
    }
    if (context.efficiency) {
      explanation.reasoning.push(`效率考虑: ${context.efficiency}`);
    }
  }

  // 解释为什么没有选择替代方案
  if (alternatives && alternatives.length > 0) {
    for (const alt of alternatives) {
      if (alt.rejected) {
        explanation.reasoning.push(`未选择 ${alt.name}: ${alt.reason}`);
      }
    }
  }

  load();
  explanationLog.push(explanation);
  save();

  return explanation;
}

/**
 * 生成自然语言解释
 */
function generateNaturalLanguage(explanation) {
  const parts = [];

  switch (explanation.type || 'decision') {
    case 'decision':
      parts.push(`我选择 "${explanation.decision}" 是因为：`);
      for (const reason of explanation.reasoning) {
        parts.push(`  - ${reason}`);
      }
      if (explanation.confidence) {
        parts.push(`置信度: ${(explanation.confidence * 100).toFixed(0)}%`);
      }
      break;

    case 'recall':
      parts.push(`我搜索了 "${explanation.query}"：`);
      for (const reason of explanation.reasoning) {
        parts.push(`  - ${reason}`);
      }
      if (explanation.topResults && explanation.topResults.length > 0) {
        parts.push(`找到的相关记忆:`);
        for (const r of explanation.topResults) {
          parts.push(`  - ${r.summary}`);
        }
      }
      break;

    case 'action':
      parts.push(`我执行了 "${explanation.selectedAction}"：`);
      for (const reason of explanation.reasoning) {
        parts.push(`  - ${reason}`);
      }
      break;
  }

  return parts.join('\n');
}

/**
 * 获取决策历史解释
 */
function getDecisionHistory(limit = 10) {
  load();

  const decisions = explanationLog
    .filter(e => e.type === 'decision' || !e.type)
    .slice(-limit);

  return decisions.map(d => ({
    decision: d.decision,
    timestamp: d.timestamp,
    confidence: d.confidence,
    summary: d.reasoning.slice(0, 2).join('; ')
  }));
}

/**
 * 追踪溯源
 */
function traceBack(decisionId) {
  load();

  const decision = explanationLog.find(e => e.id === decisionId);
  if (!decision) {
    return null;
  }

  // 找到相关的记忆召回
  const relatedRecalls = explanationLog.filter(
    e => e.type === 'recall' && e.timestamp < decision.timestamp
  ).slice(-3);

  // 找到相关的上下文
  const context = {
    recalls: relatedRecalls.map(r => ({
      query: r.query,
      results: r.topResults
    }))
  };

  return {
    decision,
    context,
    fullExplanation: generateNaturalLanguage(decision)
  };
}

/**
 * 导出解释报告
 */
function exportReport(format = 'text') {
  load();

  const recent = explanationLog.slice(-50);

  if (format === 'json') {
    return JSON.stringify(recent, null, 2);
  }

  // 文本格式
  const lines = ['📊 解释报告', '=' .repeat(50), ''];

  for (const exp of recent) {
    lines.push(`[${new Date(exp.timestamp).toISOString()}]`);
    lines.push(generateNaturalLanguage(exp));
    lines.push('');
  }

  return lines.join('\n');
}

// ===== 主函数 =====
async function main() {
  const action = process.argv[2];
  const args = process.argv.slice(3);

  load();

  switch (action) {
    case 'test': {
      const exp = explainDecision(
        { name: 'use_tools', score: 0.85 },
        { userIntent: '搜索信息' },
        {
          intent_match: { value: 0.9, weight: 0.3 },
          resource_availability: { value: 1.0, weight: 0.2 }
        }
      );

      console.log('📝 解释:');
      console.log(generateNaturalLanguage(exp));
      break;
    }

    case 'history':
      console.log('📋 决策历史:');
      console.log(JSON.stringify(getDecisionHistory(), null, 2));
      break;

    case 'report':
      console.log(exportReport('text'));
      break;

    default:
      console.log(`
可解释性模块

用法:
  node explainability.cjs test     # 测试解释生成
  node explainability.cjs history  # 查看决策历史
  node explainability.cjs report   # 导出解释报告
      `);
  }
}

main();

