/**
 * 04_optimize_content.js - Step 4: 反思优化内容
 * 
 * 功能：
 * 1. 检查内容质量（标题、内容深度、数据支撑）
 * 2. 优化空洞的表述
 * 3. 补充缺失的量化数据
 * 4. 确保逻辑连贯性
 * 
 * 使用方式：
 * node scripts/04_optimize_content.js --session-id "abc123"
 * 
 * 输入：
 * - content/outline.json
 * - content/slides/*.json
 * 
 * 输出：
 * - content/optimized_slides/*.json - 优化后的内容
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

// ============================================================
// 优化结果数据
// ============================================================
const optimizationReport = {
  sessionId: SESSION_ID,
  timestamp: new Date().toISOString(),
  totalSlides: 0,
  optimizedSlides: [],
  optimizations: {
    titles: [],
    content: [],
    depth: [],
    data: []
  },
  issues: []
};

// ============================================================
// 检查规则
// ============================================================
const CHECK_RULES = {
  // 标题检查
  titleIssues: [
    { pattern: /^(概述|背景|简介|介绍|什么是)/, suggestion: '改为有观点的标题' },
    { pattern: /^(技术概述|技术背景)/, suggestion: '改为具体技术点名称' }
  ],
  
  // 内容空洞检查
  emptyPhrases: [
    '非常重要',
    '非常优秀',
    '表现良好',
    '效果显著',
    '得到广泛认可',
    '市场前景广阔'
  ],
  
  // 缺少数据的检查
  needsQuantification: [
    '提升效率',
    '降低成本',
    '提高性能',
    '改善体验'
  ]
};

// ============================================================
// 优化引擎
// ============================================================

/**
 * 检查并优化单页内容
 * 
 * Agent 需要：
 * 1. 读取每页内容
 * 2. 根据检查清单进行审查
 * 3. 调用 optimizeSlide() 进行优化
 * 
 * @param {object} slide 
 * @returns {object} 优化后的幻灯片
 */
function optimizeSlide(slide) {
  const optimized = JSON.parse(JSON.stringify(slide));
  const slideIssues = [];
  const slideOptimizations = [];

  // ============================================================
  // 1. 标题检查
  // ============================================================
  if (optimized.title) {
    for (const rule of CHECK_RULES.titleIssues) {
      if (rule.pattern.test(optimized.title)) {
        slideIssues.push({
          type: 'title',
          original: optimized.title,
          issue: `标题过于空泛: "${optimized.title}"`,
          suggestion: rule.suggestion
        });
        slideOptimizations.push({
          type: 'title',
          before: optimized.title,
          after: null,  // Agent 应该提供优化后的标题
          status: 'pending'
        });
      }
    }
  }

  // ============================================================
  // 2. 内容空洞检查
  // ============================================================
  if (optimized.content) {
    const contentStr = JSON.stringify(optimized.content);
    
    for (const phrase of CHECK_RULES.emptyPhrases) {
      if (contentStr.includes(phrase)) {
        slideIssues.push({
          type: 'content',
          content: phrase,
          issue: `发现空洞表述: "${phrase}"`,
          suggestion: '用具体数据替代'
        });
      }
    }
  }

  // ============================================================
  // 3. 技术点深度检查（如果是技术点页）
  // ============================================================
  if (optimized.type === 'tech_point' || optimized.techPointId) {
    const depthChecks = [
      { field: 'background', desc: '背景说明' },
      { field: 'principles', desc: '原理说明' },
      { field: 'details', desc: '实现细节' },
      { field: 'effects', desc: '量化效果' }
    ];

    for (const check of depthChecks) {
      const content = optimized.content || {};
      if (!content[check.field] || content[check.field].length === 0) {
        slideIssues.push({
          type: 'depth',
          issue: `技术点页面缺少 ${check.desc}`,
          slideId: slide.id,
          slideTitle: slide.title
        });
      }
    }
  }

  // ============================================================
  // 4. 数据来源检查
  // ============================================================
  if (optimized.sources && optimized.sources.length === 0) {
    // 检查内容中是否有数据
    const contentStr = JSON.stringify(optimized.content);
    const hasNumbers = /\d+%|\d+x|\d+k|\d+\s*(倍|次|个|条)/.test(contentStr);
    
    if (hasNumbers && optimized.type !== 'cover') {
      slideIssues.push({
        type: 'source',
        issue: '内容包含数据但缺少来源标注',
        slideId: slide.id
      });
    }
  }

  // ============================================================
  // 5. 量化效果检查（如果是技术点页）
  // ============================================================
  if ((optimized.type === 'tech_point' || optimized.techPointId) && optimized.content) {
    const effects = optimized.content.effects || [];
    const hasQuantified = effects.some(e => 
      typeof e === 'string' && (/%|\d+x|\d+k/.test(e))
    );
    
    if (!hasQuantified && effects.length > 0) {
      slideIssues.push({
        type: 'data',
        issue: '效果描述缺少具体数字',
        slideId: slide.id,
        slideTitle: slide.title,
        suggestion: '添加量化指标，如：性能提升 40%、延迟降低 50ms'
      });
      slideOptimizations.push({
        type: 'data',
        field: 'effects',
        status: 'pending',
        suggestion: '添加量化数据'
      });
    }
  }

  // 记录
  if (slideIssues.length > 0) {
    optimizationReport.issues.push(...slideIssues);
    optimized._hasIssues = true;
    optimized._issueCount = slideIssues.length;
  }

  if (slideOptimizations.length > 0) {
    optimizationReport.optimizations.content.push(...slideOptimizations);
  }

  return optimized;
}

/**
 * 应用优化（由 Agent 手动完成）
 * 
 * Agent 应该根据检查结果：
 * 1. 优化空泛的标题为有观点的标题
 * 2. 将空洞表述替换为具体数据
 * 3. 补充缺失的内容
 * 4. 添加数据来源标注
 * 
 * @param {object} slide 
 * @param {object} optimizations 
 */
function applyOptimizations(slide, optimizations) {
  const optimized = { ...slide };

  for (const opt of optimizations) {
    switch (opt.type) {
      case 'title':
        if (opt.after) {
          optimized.title = opt.after;
          optimizationReport.optimizations.titles.push({
            before: opt.before,
            after: opt.after,
            slideId: slide.id
          });
        }
        break;
      case 'content':
        if (opt.after) {
          // 替换空洞内容
          if (opt.field && optimized.content) {
            optimized.content[opt.field] = opt.after;
          }
          optimizationReport.optimizations.content.push({
            type: 'content',
            before: opt.before,
            after: opt.after,
            slideId: slide.id,
            status: 'applied'
          });
        }
        break;
      case 'data':
        if (opt.after && optimized.content) {
          optimized.content.effects = opt.after;
          optimizationReport.optimizations.data.push({
            before: opt.before,
            after: opt.after,
            slideId: slide.id,
            status: 'applied'
          });
        }
        break;
      case 'depth':
        if (opt.after && optimized.content) {
          optimized.content[opt.field] = opt.after;
          optimizationReport.optimizations.depth.push({
            field: opt.field,
            slideId: slide.id,
            status: 'applied'
          });
        }
        break;
    }
  }

  optimized._optimized = true;
  optimized._optimizationCount = optimizations.length;
  return optimized;
}

/**
 * 保存优化报告
 */
function saveOptimizationReport() {
  // 确保目录存在
  fileUtils.ensureDir(dirs.content);
  fileUtils.ensureDir(dirs.optimizedSlides);

  // 保存报告
  const reportFile = path.join(dirs.content, 'optimization_report.json');
  fileUtils.writeJson(reportFile, optimizationReport);
  log.info(`\n💾 优化报告已保存: ${reportFile}`);

  // 保存优化后的幻灯片
  for (const slide of optimizationReport.optimizedSlides) {
    const slideFile = path.join(dirs.optimizedSlides, `slide_${String(slide.id).padStart(2, '0')}_${fileUtils.safeFileName(slide.title)}.json`);
    fileUtils.writeJson(slideFile, slide);
  }
  log.info(`💾 ${optimizationReport.optimizedSlides.length} 个优化后的页面已保存到 ${dirs.optimizedSlides}`);

  return {
    reportFile,
    slidesCount: optimizationReport.optimizedSlides.length
  };
}

/**
 * 获取优化统计
 */
function getStats() {
  return {
    totalSlides: optimizationReport.totalSlides,
    issuesFound: optimizationReport.issues.length,
    issuesByType: optimizationReport.issues.reduce((acc, issue) => {
      acc[issue.type] = (acc[issue.type] || 0) + 1;
      return acc;
    }, {}),
    titlesOptimized: optimizationReport.optimizations.titles.length,
    contentOptimized: optimizationReport.optimizations.content.length,
    dataOptimized: optimizationReport.optimizations.data.length,
    depthOptimized: optimizationReport.optimizations.depth.length,
    slidesWithIssues: optimizationReport.issues.reduce((acc, issue) => {
      acc[issue.slideId] = (acc[issue.slideId] || 0) + 1;
      return acc;
    }, {})
  };
}

// ============================================================
// 主函数
// ============================================================

/**
 * 执行内容优化
 * @param {string} sessionId 
 * @returns {Promise<object>}
 */
async function run(sessionId = SESSION_ID) {
  log.stepStart(4, '反思优化', '检查内容质量并优化空洞表述');

  try {
    // 读取目录
    const outlineFile = path.join(dirs.content, 'outline.json');
    if (!fs.existsSync(outlineFile)) {
      throw new Error(`找不到目录文件: ${outlineFile}`);
    }

    const outline = fileUtils.readJson(outlineFile);
    optimizationReport.totalSlides = outline.slides.length;
    optimizationReport.topic = outline.topic;

    log.info(`已加载 ${outline.slides.length} 页内容`);

    // 读取各页面内容
    for (const slideSummary of outline.slides) {
      const slideFile = path.join(dirs.slides, `slide_${String(slideSummary.id).padStart(2, '0')}_${fileUtils.safeFileName(slideSummary.title)}.json`);
      
      if (fs.existsSync(slideFile)) {
        const slide = fileUtils.readJson(slideFile);
        
        // 检查并优化
        const optimized = optimizeSlide(slide);
        optimizationReport.optimizedSlides.push(optimized);
      } else {
        // 使用摘要创建简化版本
        optimizationReport.optimizedSlides.push({
          ...slideSummary,
          content: slideSummary.content || {}
        });
      }
    }

    // ============================================================
    // 这里由 Agent 根据检查结果进行手动优化
    // Agent 应该：
    // 1. 查看 optimizationReport.issues
    // 2. 对每个问题进行优化
    // 3. 调用 applyOptimizations() 应用优化
    // ============================================================

    // 保存结果
    const files = saveOptimizationReport();

    // 获取统计
    const stats = getStats();
    
    log.stepComplete(4, {
      '总页面数': stats.totalSlides,
      '发现问题': stats.issuesFound,
      '标题优化': stats.titlesOptimized,
      '内容优化': stats.contentOptimized,
      '数据优化': stats.dataOptimized,
      '深度优化': stats.depthOptimized
    });

    // 输出问题摘要
    if (stats.issuesFound > 0) {
      log.warn(`\n⚠️ 发现 ${stats.issuesFound} 个问题待优化`);
      for (const [type, count] of Object.entries(stats.issuesByType)) {
        log.warn(`   - ${type}: ${count} 个`);
      }
    }

    return {
      success: true,
      sessionId,
      baseDir: dirs.base,
      stats,
      files,
      issues: optimizationReport.issues,
      optimizedSlides: optimizationReport.optimizedSlides
    };
  } catch (error) {
    log.stepFailed(4, error.message);
    throw error;
  }
}

// ============================================================
// 直接执行
// ============================================================
if (require.main === module) {
  run().then(result => {
    console.log('\n✅ 优化检查完成！');
    console.log(`📊 统计: 发现 ${result.stats.issuesFound} 个问题，进行了 ${result.stats.titlesOptimized + result.stats.contentOptimized} 处优化`);
  }).catch(err => {
    console.error('❌ 优化失败:', err.message);
    process.exit(1);
  });
}

// 导出
module.exports = {
  run,
  optimizeSlide,
  applyOptimizations,
  CHECK_RULES
};
