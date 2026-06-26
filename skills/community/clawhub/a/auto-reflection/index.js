/**
 * Auto Learning & Reflection - 自动学习与反思机制
 *
 * 功能：
 * 1. 每 5 轮自动深度反思
 * 2. 能力评估自动更新
 * 3. 学习计划自动调整
 * 4. 知识图谱自动优化
 */

const fs = require('fs');
const path = require('path');

const CONFIG = {
  workspace: 'D:\\OpenClaw\\workspace',
  memoryDir: 'D:\\OpenClaw\\workspace\\memory',
  logsDir: 'D:\\OpenClaw\\workspace\\logs',
  reflectionInterval: 5,  // 每 5 轮反思一次
};

function log(msg, level = 'INFO') {
  const ts = new Date().toISOString().replace('T', ' ').substring(0, 19);
  const emoji = {
    'INFO': '⚪',
    'SUCCESS': '🟢',
    'ERROR': '🔴',
    'WARN': '🟡',
    'REFLECT': '💭'
  }[level] || '⚪';
  console.log(`${emoji} ${msg}`);

  const logFile = path.join(CONFIG.logsDir, 'auto-reflection.log');
  fs.appendFileSync(logFile, `[${ts}] [${level}] ${msg}\n`);
}

function loadCapabilities() {
  const capPath = path.join(CONFIG.memoryDir, 'capabilities.json');
  if (fs.existsSync(capPath)) {
    return JSON.parse(fs.readFileSync(capPath, 'utf8'));
  }
  return null;
}

function saveCapabilities(capabilities) {
  const capPath = path.join(CONFIG.memoryDir, 'capabilities.json');
  fs.writeFileSync(capPath, JSON.stringify(capabilities, null, 2));
  log('✅ 能力评估已更新', 'SUCCESS');
}

function loadKnowledgeGraph() {
  const kgPath = path.join(CONFIG.memoryDir, 'knowledge-graph.json');
  if (fs.existsSync(kgPath)) {
    return JSON.parse(fs.readFileSync(kgPath, 'utf8'));
  }
  return null;
}

function saveKnowledgeGraph(kg) {
  const kgPath = path.join(CONFIG.memoryDir, 'knowledge-graph.json');
  fs.writeFileSync(kgPath, JSON.stringify(kg, null, 2));
  log('✅ 知识图谱已更新', 'SUCCESS');
}

function getLearningRoundCount() {
  if (!fs.existsSync(CONFIG.memoryDir)) return 0;

  return fs.readdirSync(CONFIG.memoryDir)
    .filter(f => f.startsWith('learning-round-') && f.endsWith('.json'))
    .length;
}

function shouldReflect() {
  const roundCount = getLearningRoundCount();
  return roundCount % CONFIG.reflectionInterval === 0;
}

function generateReflection() {
  log('生成深度反思报告...', 'REFLECT');

  const capabilities = loadCapabilities();
  const knowledgeGraph = loadKnowledgeGraph();
  const roundCount = getLearningRoundCount();

  if (!capabilities || !knowledgeGraph) {
    log('⚠️ 无法加载能力评估或知识图谱', 'WARN');
    return null;
  }

  const reflection = {
    round: roundCount,
    timestamp: new Date().toISOString(),
    type: 'deep-reflection',

    // 能力分析
    capabilityAnalysis: {
      overallLevel: capabilities.overallLevel,
      overallScore: capabilities.overallScore,
      changeFromPrevious: capabilities.overallChange || 'N/A',
      topStrengths: capabilities.strengths,
      criticalWeaknesses: capabilities.weaknesses,
      dimensionChanges: Object.entries(capabilities.dimensions)
        .map(([name, dim]) => ({
          name,
          level: dim.level,
          score: dim.score,
          change: dim.change || '0'
        }))
        .sort((a, b) => parseFloat(b.change) - parseFloat(a.change))
    },

    // 知识图谱分析
    knowledgeAnalysis: {
      totalNodes: knowledgeGraph.nodes ? knowledgeGraph.nodes.length : 0,
      totalEdges: knowledgeGraph.edges ? knowledgeGraph.edges.length : 0,
      domainMastery: knowledgeGraph.knowledgeDomains || {},
      masteredTopics: knowledgeGraph.masteredTopics || [],
      learningTopics: knowledgeGraph.learningTopics || []
    },

    // 成就与不足
    achievements: capabilities.recentAchievements || [],
    areasForImprovement: capabilities.weaknesses.map(w => ({
      area: w,
      priority: 'high',
      suggestedActions: []
    })),

    // 下一步计划
    nextSteps: {
      immediate: capabilities.nextLearningFocus,
      shortTerm: capabilities.learningPath.slice(0, 3),
      longTerm: capabilities.learningPath
    },

    // 元认知
    metaCognition: {
      learningEfficiency: calculateLearningEfficiency(capabilities),
      knowledgeGrowthRate: calculateKnowledgeGrowth(knowledgeGraph),
      reflectionQuality: 'good',
      suggestions: generateSuggestions(capabilities, knowledgeGraph)
    }
  };

  // 保存反思报告
  const reflectionPath = path.join(CONFIG.workspace, `reflection-round-${roundCount}-${new Date().toISOString().replace(/[:.]/g, '-')}.json`);
  fs.writeFileSync(reflectionPath, JSON.stringify(reflection, null, 2));

  log(`✅ 反思报告已保存：${reflectionPath}`, 'SUCCESS');

  // 更新 HEARTBEAT.md
  updateHeartbeatWithReflection(reflection);

  return reflection;
}

function calculateLearningEfficiency(capabilities) {
  // 计算学习效率：平均分变化 / 轮次
  const avgChange = Object.values(capabilities.dimensions)
    .map(d => parseFloat(d.change || '0'))
    .reduce((a, b) => a + b, 0) / Object.keys(capabilities.dimensions).length;

  return {
    averageChangePerDimension: parseFloat(avgChange.toFixed(2)),
    overallChange: parseFloat(capabilities.overallChange || '0'),
    efficiency: avgChange > 5 ? 'high' : avgChange > 2 ? 'medium' : 'low'
  };
}

function calculateKnowledgeGrowth(knowledgeGraph) {
  const domains = knowledgeGraph.knowledgeDomains || {};
  const avgMastery = Object.values(domains)
    .map(d => d.mastery || 0)
    .reduce((a, b) => a + b, 0) / (Object.keys(domains).length || 1);

  return {
    averageDomainMastery: parseFloat(avgMastery.toFixed(2)),
    totalTopics: (knowledgeGraph.masteredTopics || []).length + (knowledgeGraph.learningTopics || []).length,
    growthRate: avgMastery > 75 ? 'fast' : avgMastery > 50 ? 'medium' : 'slow'
  };
}

function generateSuggestions(capabilities, knowledgeGraph) {
  const suggestions = [];

  // 基于弱点生成建议
  capabilities.weaknesses.forEach(weakness => {
    if (weakness.includes('性能')) {
      suggestions.push('📊 建议：深入学习性能优化技术，包括缓存机制、并发控制、资源管理');
    }
    if (weakness.includes('知识')) {
      suggestions.push('📚 建议：加强知识整合，建立更系统的知识框架，定期复习和关联');
    }
  });

  // 基于优势生成建议
  capabilities.strengths.forEach(strength => {
    if (strength.includes('自动化')) {
      suggestions.push('⚡ 优势：继续保持自动化建设，考虑扩展到更多场景');
    }
    if (strength.includes('协作')) {
      suggestions.push('🤝 优势：优化 Agent 协作机制，探索更高效的并行模式');
    }
  });

  // 基于学习路径生成建议
  if (capabilities.learningPath && capabilities.learningPath.length > 0) {
    suggestions.push(`🎯 当前重点：${capabilities.learningPath[0]}`);
  }

  return suggestions;
}

function updateHeartbeatWithReflection(reflection) {
  const heartbeatPath = path.join(CONFIG.workspace, 'HEARTBEAT.md');

  if (!fs.existsSync(heartbeatPath)) {
    log('⚠️ HEARTBEAT.md 不存在', 'WARN');
    return;
  }

  let content = fs.readFileSync(heartbeatPath, 'utf8');

  // 更新反思部分
  const反思Section = `
## 💭 最新反思（第 ${reflection.round} 轮）

**反思时间**: ${new Date(reflection.timestamp).toLocaleString('zh-CN')}

### 能力变化
- **整体等级**: ${reflection.capabilityAnalysis.overallLevel}
- **整体分数**: ${reflection.capabilityAnalysis.overallScore} (${reflection.capabilityAnalysis.changeFromPrevious})
- **最大提升**: ${reflection.capabilityAnalysis.dimensionChanges[0]?.name} (+${reflection.capabilityAnalysis.dimensionChanges[0]?.change})

### 关键成就
${reflection.achievements.map(a => `- ✅ ${a}`).join('\n')}

### 改进建议
${reflection.metaCognition.suggestions.map(s => `${s}`).join('\n')}

---
`;

  // 插入反思内容
  const marker = '## 💭 最新反思';
  const markerIndex = content.indexOf(marker);

  if (markerIndex >= 0) {
    // 找到下一个章节标记
    const nextSectionIndex = content.indexOf('##', markerIndex + 1);
    if (nextSectionIndex >= 0) {
      content = content.substring(0, markerIndex) + 反思 Section + content.substring(nextSectionIndex);
    }
  } else {
    // 在开头插入
    content = 反思 Section + content;
  }

  fs.writeFileSync(heartbeatPath, content);
  log('✅ HEARTBEAT.md 已更新', 'SUCCESS');
}

function updateCapabilitiesAfterLearning() {
  log('更新能力评估...', 'REFLECT');

  const capabilities = loadCapabilities();
  if (!capabilities) {
    log('⚠️ 无法加载能力评估', 'WARN');
    return;
  }

  // 更新时间戳
  capabilities.lastAssessment = new Date().toISOString();

  // 如果有新版本，更新
  capabilities.version = (capabilities.version || 1) + 1;

  saveCapabilities(capabilities);
}

function run() {
  log('=========================================', 'REFLECT');
  log('💭 自动学习与反思机制启动', 'REFLECT');
  log('=========================================', 'REFLECT');

  const roundCount = getLearningRoundCount();
  log(`📊 当前学习轮次：${roundCount}`, 'INFO');

  if (shouldReflect()) {
    log(`✨ 达到反思条件（每${CONFIG.reflectionInterval}轮）`, 'REFLECT');
    const reflection = generateReflection();

    if (reflection) {
      log('=========================================', 'REFLECT');
      log('📊 反思摘要', 'INFO');
      log('=========================================', 'INFO');
      log(`等级：${reflection.capabilityAnalysis.overallLevel} (${reflection.capabilityAnalysis.overallScore})`, 'INFO');
      log(`变化：${reflection.capabilityAnalysis.changeFromPrevious}`, 'INFO');
      log(`成就：${reflection.achievements.length} 项`, 'INFO');
      log(`建议：${reflection.metaCognition.suggestions.length} 条`, 'INFO');
      log('=========================================', 'REFLECT');
    }
  } else {
    const nextReflectIn = CONFIG.reflectionInterval - (roundCount % CONFIG.reflectionInterval);
    log(`⏭️  跳过反思（${nextReflectIn} 轮后进行）`, 'INFO');
  }

  // 更新能力评估
  updateCapabilitiesAfterLearning();

  log('=========================================', 'REFLECT');
  log('✅ 自动学习与反思完成', 'SUCCESS');
  log('=========================================', 'REFLECT');
}

// 如果直接运行
if (require.main === module) {
  run();
}

module.exports = { run, generateReflection, shouldReflect, getLearningRoundCount };
