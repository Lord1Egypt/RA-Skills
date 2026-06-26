/**
 * 02_extract_insights.js - Step 2: 从收集内容中提炼洞察
 * 
 * 功能：
 * 1. 读取 Step 1 收集的搜索结果和网页内容
 * 2. 使用 LLM 分析并提炼关键洞察
 * 3. 生成结构化的洞察报告
 * 
 * 使用方式：
 * node scripts/02_extract_insights.js --session-id "abc123"
 * 
 * 输入：
 * - collected/search_results.json
 * - collected/web_pages/*.md
 * 
 * 输出：
 * - insights/insights.json - 洞察清单
 * - insights/key_stats.json - 关键指标
 * - insights/evidence.json - 证据清单
 */
const fs = require('fs');
const path = require('path');

const config = require('../lib/config');
const loggerModule = require('../lib/logger');
const fileUtils = require('../lib/file_utils');

// ============================================================
// 命令行参数解析
// ============================================================
const args = process.argv.slice(2);
const params = {};

for (let i = 0; i < args.length; i++) {
  if (args[i].startsWith('--')) {
    const key = args[i].substring(2);
    if (args[i + 1] && !args[i + 1].startsWith('--')) {
      params[key] = args[i + 1];
      i++;
    } else {
      params[key] = true;
    }
  }
}

const SESSION_ID = params['session-id'];

// ============================================================
// 初始化
// ============================================================
if (!SESSION_ID) {
  console.error('❌ 请提供 --session-id 参数');
  process.exit(1);
}

const dirs = fileUtils.createSessionDirs(SESSION_ID);
const log = new loggerModule.Logger(SESSION_ID);
log.info(`会话目录: ${dirs.base}`);

// ============================================================
// 洞察数据结构
// ============================================================
const insightsData = {
  sessionId: SESSION_ID,
  timestamp: new Date().toISOString(),
  topic: null,
  insights: [],
  keyStats: [],
  evidence: [],
  sourceReferences: []
};

// ============================================================
// 洞察提炼引擎（由 Agent 调用 LLM 执行）
// ============================================================

/**
 * 从搜索结果中提炼洞察
 * 
 * Agent 需要：
 * 1. 读取 collected/search_results.json
 * 2. 读取 collected/web_pages/*.md 中的关键内容
 * 3. 调用 LLM 分析并提炼洞察
 * 4. 调用 addInsight() 添加洞察
 * 
 * @param {object} searchResults - 搜索结果数据
 * @returns {Promise<object>}
 */
async function extractInsights(searchResults) {
  log.info(`开始提炼洞察，共 ${searchResults.items?.length || 0} 条内容`);

  // ============================================================
  // 这里由 Agent 根据 SKILL.md 中的指南，调用 LLM 执行分析
  // Agent 应该：
  // 1. 分析搜索结果中的关键数据点
  // 2. 识别趋势、模式、异常
  // 3. 调用 addInsight() 添加洞察
  // ============================================================

  return {
    totalInsights: insightsData.insights.length,
    byType: getInsightsByType()
  };
}

/**
 * 添加洞察
 * @param {object} insight 
 */
function addInsight(insight) {
  const item = {
    id: insightsData.insights.length + 1,
    type: insight.type || 'fact',  // fact/trend/technical/comparison/causal/recommendation
    title: insight.title,
    statement: insight.statement,
    evidence: insight.evidence || [],
    data: insight.data || null,
    confidence: insight.confidence || 'medium',  // high/medium/low
    sources: insight.sources || [],
    timestamp: new Date().toISOString()
  };

  insightsData.insights.push(item);
  log.info(`   ✅ 添加洞察 [${item.type}]: ${item.title}`);

  // 同时记录证据
  if (insight.evidence) {
    for (const ev of insight.evidence) {
      if (typeof ev === 'string') {
        addEvidence({
          type: 'quote',
          content: ev,
          insightId: item.id
        });
      } else if (ev.url) {
        addEvidence({
          type: 'source',
          url: ev.url,
          title: ev.title || '',
          insightId: item.id
        });
      }
    }
  }

  return item;
}

/**
 * 添加证据
 * @param {object} evidence 
 */
function addEvidence(evidence) {
  const item = {
    id: insightsData.evidence.length + 1,
    type: evidence.type,  // quote/source/data/fact
    content: evidence.content || '',
    url: evidence.url || null,
    title: evidence.title || null,
    insightId: evidence.insightId || null,
    timestamp: new Date().toISOString()
  };

  insightsData.evidence.push(item);
  return item;
}

/**
 * 添加关键指标
 * @param {object} stat 
 */
function addKeyStat(stat) {
  const item = {
    id: insightsData.keyStats.length + 1,
    label: stat.label,
    value: stat.value,
    unit: stat.unit || '',
    trend: stat.trend || 'stable',  // up/down/stable
    change: stat.change || null,
    source: stat.source || '',
    description: stat.description || '',
    timestamp: new Date().toISOString()
  };

  insightsData.keyStats.push(item);
  log.info(`   📊 添加指标: ${item.label} = ${item.value} ${item.unit}`);
  return item;
}

/**
 * 添加来源引用
 * @param {object} ref 
 */
function addSourceReference(ref) {
  const item = {
    id: insightsData.sourceReferences.length + 1,
    source: ref.source,
    url: ref.url,
    title: ref.title,
    type: ref.type || 'web',  // web/paper/report
    relevance: ref.relevance || 'medium',  // high/medium/low
    timestamp: new Date().toISOString()
  };

  insightsData.sourceReferences.push(item);
  return item;
}

/**
 * 获取按类型分组的洞察
 */
function getInsightsByType() {
  const byType = {};
  for (const insight of insightsData.insights) {
    if (!byType[insight.type]) {
      byType[insight.type] = [];
    }
    byType[insight.type].push({
      id: insight.id,
      title: insight.title,
      confidence: insight.confidence
    });
  }
  return byType;
}

/**
 * 保存洞察结果
 */
function saveInsights() {
  // 确保目录存在
  fileUtils.ensureDir(dirs.insights);

  // 保存完整洞察
  const insightsFile = path.join(dirs.insights, 'insights.json');
  fileUtils.writeJson(insightsFile, insightsData);
  log.info(`\n💾 洞察结果已保存: ${insightsFile}`);

  // 保存关键指标
  const statsFile = path.join(dirs.insights, 'key_stats.json');
  fileUtils.writeJson(statsFile, {
    sessionId: SESSION_ID,
    timestamp: new Date().toISOString(),
    stats: insightsData.keyStats
  });

  // 保存证据清单
  const evidenceFile = path.join(dirs.insights, 'evidence.json');
  fileUtils.writeJson(evidenceFile, {
    sessionId: SESSION_ID,
    timestamp: new Date().toISOString(),
    evidence: insightsData.evidence
  });

  return {
    insightsFile,
    statsFile,
    evidenceFile
  };
}

/**
 * 获取统计数据
 */
function getStats() {
  const byType = getInsightsByType();
  
  return {
    totalInsights: insightsData.insights.length,
    byType: Object.fromEntries(
      Object.entries(byType).map(([k, v]) => [k, v.length])
    ),
    totalStats: insightsData.keyStats.length,
    totalEvidence: insightsData.evidence.length,
    totalSources: insightsData.sourceReferences.length,
    highConfidence: insightsData.insights.filter(i => i.confidence === 'high').length
  };
}

// ============================================================
// 主函数
// ============================================================

/**
 * 执行洞察提炼
 * @param {string} sessionId 
 * @returns {Promise<object>}
 */
async function run(sessionId = SESSION_ID) {
  log.stepStart(2, '洞察提炼', '从收集的内容中提炼关键观点');

  try {
    // 读取会话信息和搜索结果
    const sessionInfoPath = path.join(config.getSessionDir(sessionId), 'session_info.json');
    if (!fs.existsSync(sessionInfoPath)) {
      throw new Error(`找不到会话信息: ${sessionInfoPath}`);
    }
    
    const sessionInfo = fileUtils.readJson(sessionInfoPath);
    const searchResultsPath = path.join(sessionInfo.collectedDir, 'search_results.json');
    
    if (!fs.existsSync(searchResultsPath)) {
      throw new Error(`找不到搜索结果: ${searchResultsPath}`);
    }

    const searchResults = fileUtils.readJson(searchResultsPath);
    insightsData.topic = searchResults.topic;

    log.info(`已加载搜索结果: ${searchResults.items?.length || 0} 条`);

    // 读取收集的网页内容
    const webPages = fileUtils.listFiles(sessionInfo.webPagesDir, '.md');
    log.info(`已收集网页内容: ${webPages.length} 个文件`);

    // 执行洞察提炼（由 Agent 调用 LLM 完成）
    await extractInsights(searchResults);

    // 保存结果
    saveInsights();

    // 获取统计
    const stats = getStats();
    
    log.stepComplete(2, {
      '总洞察数': stats.totalInsights,
      '事实洞察': stats.byType.fact || 0,
      '趋势洞察': stats.byType.trend || 0,
      '技术洞察': stats.byType.technical || 0,
      '对比洞察': stats.byType.comparison || 0,
      '高置信度': stats.highConfidence,
      '关键指标': stats.totalStats,
      '证据数量': stats.totalEvidence
    });

    return {
      success: true,
      sessionId,
      baseDir: dirs.base,
      stats,
      insightsData
    };
  } catch (error) {
    log.stepFailed(2, error.message);
    throw error;
  }
}

// ============================================================
// 直接执行
// ============================================================
if (require.main === module) {
  run().then(result => {
    console.log('\n✅ 洞察提炼完成！');
    console.log(`📊 统计: 共 ${result.stats.totalInsights} 条洞察`);
  }).catch(err => {
    console.error('❌ 洞察提炼失败:', err.message);
    process.exit(1);
  });
}

// 导出
module.exports = { run, extractInsights, addInsight, addKeyStat, addEvidence, addSourceReference };
