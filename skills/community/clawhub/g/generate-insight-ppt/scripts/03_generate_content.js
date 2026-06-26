/**
 * 03_generate_content.js - Step 3: 生成目录 + 结构化内容
 * 
 * 功能：
 * 1. 基于洞察生成 PPT 目录结构
 * 2. 为每个目录项生成详细的页面内容
 * 3. 识别并深度展开关键技术点
 * 
 * 使用方式：
 * node scripts/03_generate_content.js --session-id "abc123" --slides 10
 * 
 * 输入：
 * - insights/insights.json
 * - collected/web_pages/*.md
 * 
 * 输出：
 * - content/outline.json - 目录结构
 * - content/slides/*.json - 每页内容
 * - content/tech_points.json - 技术点清单
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
const TARGET_SLIDES = parseInt(params.slides) || 10;

// ============================================================
// 初始化
// ============================================================
if (!SESSION_ID) {
  console.error('❌ 请提供 --session-id 参数');
  process.exit(1);
}

const dirs = fileUtils.createSessionDirs(SESSION_ID);
const log = new loggerModule.Logger(SESSION_ID);

// ============================================================
// 数据结构
// ============================================================
let outlineData = {
  sessionId: SESSION_ID,
  topic: null,
  timestamp: new Date().toISOString(),
  totalSlides: 0,
  slides: [],
  techPoints: []
};

let currentSlide = null;

// ============================================================
// 目录生成引擎
// ============================================================

/**
 * 生成 PPT 目录结构
 * 
 * Agent 需要：
 * 1. 读取 insights/insights.json
 * 2. 根据洞察设计合理的 PPT 结构
 * 3. 调用 addSlide() 添加目录项
 * 4. 识别关键技术点并调用 addTechPoint()
 * 
 * @param {object} insights - 洞察数据
 * @param {number} targetSlides - 目标幻灯片数
 * @returns {Promise<object>}
 */
async function generateOutline(insights, targetSlides = TARGET_SLIDES) {
  log.info(`开始生成目录，目标 ${targetSlides} 页`);

  outlineData.topic = insights.topic;
  outlineData.totalSlides = targetSlides;

  // ============================================================
  // 这里由 Agent 根据 SKILL.md 中的指南设计目录结构
  // Agent 应该：
  // 1. 分析洞察数据，确定核心内容
  // 2. 设计页面顺序和结构
  // 3. 识别关键技术点
  // 4. 调用 addSlide() 添加页面
  // 5. 调用 addTechPoint() 标记技术点
  // ============================================================

  return {
    totalSlides: outlineData.slides.length,
    techPointsCount: outlineData.techPoints.length
  };
}

/**
 * 添加目录页
 * @param {object} options 
 */
function addSlide(options) {
  const slide = {
    id: outlineData.slides.length + 1,
    type: options.type || 'content',
    title: options.title,
    subtitle: options.subtitle || '',
    pageNumber: outlineData.slides.length + 1,
    techPointId: options.techPointId || null,  // 如果是技术点展开页
    content: {
      background: options.background || '',
      principles: options.principles || [],
      details: options.details || [],
      effects: options.effects || []
    },
    data: options.data || null,
    sources: options.sources || [],
    timestamp: new Date().toISOString()
  };

  outlineData.slides.push(slide);
  currentSlide = slide;
  
  log.info(`   📄 添加页面 [${slide.type}]: ${slide.title}`);
  return slide;
}

/**
 * 添加封面页
 * @param {string} title 
 * @param {string} subtitle 
 */
function addCoverSlide(title, subtitle) {
  return addSlide({
    type: 'cover',
    title,
    subtitle
  });
}

/**
 * 添加目录页
 * @param {array} items - 目录项 [{title, page}]
 */
function addTocSlide(items) {
  return addSlide({
    type: 'toc',
    title: '目录',
    content: { items }
  });
}

/**
 * 添加执行摘要页
 * @param {object} summary - {stats, findings}
 */
function addExecutiveSummarySlide(summary) {
  return addSlide({
    type: 'executive_summary',
    title: '执行摘要',
    content: {
      stats: summary.stats || [],
      findings: summary.findings || []
    }
  });
}

/**
 * 添加技术全景图页
 * @param {object} overview - {layers, components}
 */
function addTechOverviewSlide(overview) {
  return addSlide({
    type: 'tech_overview',
    title: overview.title || '技术全景图',
    subtitle: overview.subtitle || '',
    content: {
      layers: overview.layers || [],
      components: overview.components || [],
      description: overview.description || ''
    }
  });
}

/**
 * 添加核心技术点展开页
 * @param {object} techPoint - 技术点详情
 */
function addTechPointSlide(techPoint) {
  // 先添加技术点到清单
  const tp = addTechPoint(techPoint);
  
  return addSlide({
    type: 'tech_point',
    title: techPoint.title,
    subtitle: techPoint.subtitle || '',
    techPointId: tp.id,
    content: {
      background: techPoint.background || '',
      principles: techPoint.principles || [],
      details: techPoint.details || [],
      effects: techPoint.effects || [],
      keyParams: techPoint.keyParams || []
    },
    sources: techPoint.sources || []
  });
}

/**
 * 添加技术原理页
 * @param {object} detail 
 */
function addTechDetailSlide(detail) {
  return addSlide({
    type: 'tech_detail',
    title: detail.title,
    subtitle: detail.subtitle || '',
    content: {
      description: detail.description || '',
      mechanism: detail.mechanism || '',
      steps: detail.steps || [],
      beforeAfter: detail.beforeAfter || null
    },
    sources: detail.sources || []
  });
}

/**
 * 添加对比分析页
 * @param {object} comparison - {items, insight}
 */
function addComparisonSlide(comparison) {
  return addSlide({
    type: 'comparison',
    title: comparison.title || '对比分析',
    subtitle: comparison.subtitle || '',
    content: {
      items: comparison.items || [],
      insight: comparison.insight || ''
    }
  });
}

/**
 * 添加总结页
 * @param {object} summary - {points, recommendations}
 */
function addSummarySlide(summary) {
  return addSlide({
    type: 'summary',
    title: '总结',
    content: {
      points: summary.points || [],
      recommendations: summary.recommendations || [],
      callToAction: summary.callToAction || ''
    }
  });
}

/**
 * 添加技术点到清单
 * @param {object} techPoint 
 */
function addTechPoint(techPoint) {
  const item = {
    id: outlineData.techPoints.length + 1,
    title: techPoint.title,
    subtitle: techPoint.subtitle || '',
    category: techPoint.category || 'general',  // architecture/algorithm/api/implementation/security/ecosystem
    coreValue: techPoint.coreValue || '',
    background: techPoint.background || '',
    principles: techPoint.principles || [],
    details: techPoint.details || [],
    effects: techPoint.effects || [],
    keyParams: techPoint.keyParams || [],
    slideId: null,  // 稍后关联
    sources: techPoint.sources || [],
    timestamp: new Date().toISOString()
  };

  outlineData.techPoints.push(item);
  log.info(`   🔬 识别技术点 [${item.category}]: ${item.title}`);
  return item;
}

/**
 * 保存目录
 */
function saveOutline() {
  // 确保目录存在
  fileUtils.ensureDir(dirs.content);
  fileUtils.ensureDir(dirs.slides);

  // 保存完整目录
  const outlineFile = path.join(dirs.content, 'outline.json');
  fileUtils.writeJson(outlineFile, outlineData);
  log.info(`\n💾 目录已保存: ${outlineFile}`);

  // 保存技术点清单
  const techPointsFile = path.join(dirs.content, 'tech_points.json');
  fileUtils.writeJson(techPointsFile, {
    sessionId: SESSION_ID,
    timestamp: new Date().toISOString(),
    totalTechPoints: outlineData.techPoints.length,
    techPoints: outlineData.techPoints
  });
  log.info(`💾 技术点清单已保存: ${techPointsFile}`);

  // 逐页保存内容文件
  for (const slide of outlineData.slides) {
    const slideFile = path.join(dirs.slides, `slide_${String(slide.id).padStart(2, '0')}_${fileUtils.safeFileName(slide.title)}.json`);
    fileUtils.writeJson(slideFile, slide);
  }
  log.info(`💾 ${outlineData.slides.length} 个页面内容已保存到 ${dirs.slides}`);

  return {
    outlineFile,
    techPointsFile,
    slidesCount: outlineData.slides.length
  };
}

/**
 * 获取目录统计
 */
function getStats() {
  const byType = {};
  for (const slide of outlineData.slides) {
    if (!byType[slide.type]) {
      byType[slide.type] = 0;
    }
    byType[slide.type]++;
  }

  return {
    totalSlides: outlineData.slides.length,
    byType,
    totalTechPoints: outlineData.techPoints.length,
    techPointCategories: outlineData.techPoints.reduce((acc, tp) => {
      acc[tp.category] = (acc[tp.category] || 0) + 1;
      return acc;
    }, {})
  };
}

// ============================================================
// 主函数
// ============================================================

/**
 * 执行内容生成
 * @param {string} sessionId 
 * @param {number} targetSlides 
 * @returns {Promise<object>}
 */
async function run(sessionId = SESSION_ID, targetSlides = TARGET_SLIDES) {
  log.stepStart(3, '目录+内容生成', '基于洞察生成 PPT 结构并撰写每页详细内容');

  try {
    // 读取会话信息和洞察数据
    const sessionInfoPath = path.join(config.getSessionDir(sessionId), 'session_info.json');
    const insightsPath = path.join(dirs.insights, 'insights.json');
    
    if (!fs.existsSync(sessionInfoPath)) {
      throw new Error(`找不到会话信息: ${sessionInfoPath}`);
    }
    if (!fs.existsSync(insightsPath)) {
      throw new Error(`找不到洞察数据: ${insightsPath}`);
    }

    const sessionInfo = fileUtils.readJson(sessionInfoPath);
    const insights = fileUtils.readJson(insightsPath);

    log.info(`已加载洞察: ${insights.insights.length} 条`);

    // 生成目录结构（由 Agent 完成）
    await generateOutline(insights, targetSlides);

    // 保存结果
    const files = saveOutline();

    // 获取统计
    const stats = getStats();
    
    log.stepComplete(3, {
      '总页面数': stats.totalSlides,
      '封面/目录': (stats.byType.cover || 0) + (stats.byType.toc || 0),
      '执行摘要': stats.byType.executive_summary || 0,
      '技术全景': stats.byType.tech_overview || 0,
      '技术点展开': stats.byType.tech_point || 0,
      '技术原理': stats.byType.tech_detail || 0,
      '对比分析': stats.byType.comparison || 0,
      '总结页': stats.byType.summary || 0,
      '识别技术点': stats.totalTechPoints
    });

    return {
      success: true,
      sessionId,
      baseDir: dirs.base,
      stats,
      files,
      outline: outlineData
    };
  } catch (error) {
    log.stepFailed(3, error.message);
    throw error;
  }
}

// ============================================================
// 直接执行
// ============================================================
if (require.main === module) {
  run().then(result => {
    console.log('\n✅ 目录生成完成！');
    console.log(`📊 统计: 共 ${result.stats.totalSlides} 页，${result.stats.totalTechPoints} 个技术点`);
  }).catch(err => {
    console.error('❌ 目录生成失败:', err.message);
    process.exit(1);
  });
}

// 导出
module.exports = {
  run,
  generateOutline,
  addSlide,
  addCoverSlide,
  addTocSlide,
  addExecutiveSummarySlide,
  addTechOverviewSlide,
  addTechPointSlide,
  addTechDetailSlide,
  addComparisonSlide,
  addSummarySlide,
  addTechPoint
};
