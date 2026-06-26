/**
 * 01_search_and_collect.js - Step 1: 搜索 + 内容抽取 + 文档下载
 * 
 * 功能：
 * 1. 围绕主题在多个渠道搜索内容
 * 2. 抽取网页关键内容并保存为 Markdown
 * 3. 下载 PDF 论文到本地
 * 
 * 使用方式：
 * node scripts/01_search_and_collect.js --topic "Claude Code" --session-id "abc123"
 * 
 * 输出：
 * - collected/search_results.json    - 搜索结果汇总
 * - collected/web_pages/*.md         - 抽取的网页内容
 * - collected/papers/*.pdf            - 下载的 PDF 文件
 */
const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');
const { URL } = require('url');

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

const TOPIC = params.topic || 'AI 技术趋势';
const SESSION_ID = params['session-id'] || Date.now().toString();
const DEPTH = params.depth || 'normal';

// ============================================================
// 初始化
// ============================================================
fileUtils.ensureDir(config.REPORTS_ROOT);
const dirs = fileUtils.createSessionDirs(SESSION_ID);
const log = new loggerModule.Logger(SESSION_ID);
log.info(`会话目录: ${dirs.base}`);

// ============================================================
// 搜索结果数据结构
// ============================================================
const searchResults = {
  sessionId: SESSION_ID,
  topic: TOPIC,
  timestamp: new Date().toISOString(),
  searchDepth: DEPTH,
  totalResults: 0,
  bySource: {},
  items: []
};

// ============================================================
// 下载工具
// ============================================================

/**
 * 下载文件到本地
 * @param {string} url 
 * @param {string} destPath 
 * @returns {Promise<boolean>}
 */
function downloadFile(url, destPath) {
  return new Promise((resolve, reject) => {
    const file = fs.createWriteStream(destPath);
    const protocol = url.startsWith('https') ? https : http;
    
    protocol.get(url, (response) => {
      if (response.statusCode === 301 || response.statusCode === 302) {
        // 重定向处理
        const redirectUrl = response.headers.location;
        file.close();
        downloadFile(redirectUrl, destPath).then(resolve).catch(reject);
        return;
      }
      
      if (response.statusCode !== 200) {
        file.close();
        reject(new Error(`HTTP ${response.statusCode}`));
        return;
      }
      
      response.pipe(file);
      file.on('finish', () => {
        file.close();
        resolve(true);
      });
    }).on('error', (err) => {
      file.close();
      fs.unlink(destPath, () => {});
      reject(err);
    });
  });
}

/**
 * 生成搜索关键词
 * @param {string} topic 
 * @param {string} suffix 
 * @returns {string}
 */
function buildSearchQuery(topic, suffix) {
  return suffix ? `${topic} ${suffix}` : topic;
}

// ============================================================
// 内容抽取器基类
// ============================================================

/**
 * 从 URL 下载并提取纯文本内容
 * @param {string} url 
 * @returns {Promise<string>}
 */
async function extractTextFromUrl(url) {
  return new Promise((resolve, reject) => {
    const protocol = url.startsWith('https') ? https : http;
    
    protocol.get(url, (response) => {
      if (response.statusCode === 301 || response.statusCode === 302) {
        extractTextFromUrl(response.headers.location).then(resolve).catch(reject);
        return;
      }
      
      let data = '';
      response.on('data', chunk => data += chunk);
      response.on('end', () => resolve(data));
    }).on('error', reject);
  });
}

// ============================================================
// 主要搜索函数（由 Agent 调用 browser_use/news/research skill）
// ============================================================

/**
 * 执行主题搜索
 * 此函数由 Agent 在执行 SKILL.md 中的指南时调用
 * Agent 需要使用 browser_use、news、research 等 skill 来执行实际搜索
 * 
 * 本脚本提供：
 * 1. 搜索结果的数据结构定义
 * 2. 搜索结果的保存逻辑
 * 3. 网页内容抽取和文档下载的框架
 * 
 * @param {string} topic 
 * @param {object} options 
 * @returns {Promise<object>}
 */
async function performSearch(topic, options = {}) {
  const {
    sources = ['GitHub', 'Hacker News', '知乎'],
    depth = 'normal'
  } = options;

  log.info(`开始搜索: "${topic}"`);
  log.info(`搜索来源: ${sources.join(', ')}`);
  log.info(`搜索深度: ${depth}`);

  const results = [];

  // ============================================================
  // 这里由 Agent 根据 SKILL.md 中的指南，实际调用搜索 skill
  // Agent 应该：
  // 1. 使用 browser_use skill 访问各网站搜索
  // 2. 使用 news skill 获取新闻
  // 3. 使用 research skill 获取学术论文
  // 4. 对每个搜索结果，调用 addSearchResult() 记录
  // ============================================================

  // 示例：添加搜索结果（Agent 实际搜索后替换）
  // await addSearchResult({
  //   source: 'GitHub',
  //   url: 'https://github.com/xxx/yyy',
  //   title: '项目名称',
  //   snippet: '项目描述...',
  //   stars: 10000,
  //   extractedContent: '抽取的正文内容...'
  // });

  return {
    topic,
    results,
    totalCount: results.length
  };
}

/**
 * 添加单条搜索结果
 * @param {object} result 
 */
async function addSearchResult(result) {
  const item = {
    id: searchResults.items.length + 1,
    source: result.source,
    url: result.url,
    title: result.title,
    snippet: result.snippet || '',
    stars: result.stars || null,
    forks: result.forks || null,
    publishedAt: result.publishedAt || new Date().toISOString(),
    extractedContent: result.extractedContent || '',
    contentFile: null,
    isPaper: result.isPaper || false,
    paperFile: null,
    timestamp: new Date().toISOString()
  };

  // 保存抽取的内容到文件
  if (item.extractedContent) {
    const domain = fileUtils.extractDomain(item.url);
    const safeTitle = fileUtils.safeFileName(item.title).substring(0, 50);
    const fileName = `${String(item.id).padStart(3, '0')}_${domain}_${safeTitle}.md`;
    const filePath = path.join(dirs.webPages, fileName);
    
    // 写入 Markdown 文件
    const mdContent = `# ${item.title}\n\n` +
      `**来源**: ${item.source} | ${item.url}\n\n` +
      `---\n\n` +
      `${item.extractedContent}`;
    
    fileUtils.writeMd(filePath, mdContent);
    item.contentFile = filePath;
    log.info(`   📄 已保存: ${fileName}`);
  }

  // 下载 PDF 论文
  if (item.isPaper && result.pdfUrl) {
    const fileName = `${String(item.id).padStart(3, '0')}_${fileUtils.safeFileName(item.title)}.pdf`;
    const filePath = path.join(dirs.papers, fileName);
    
    try {
      await downloadFile(result.pdfUrl, filePath);
      item.paperFile = filePath;
      item.paperSize = fileUtils.getFileSize(filePath);
      log.info(`   📚 已下载论文: ${fileName} (${fileUtils.formatFileSize(item.paperSize)})`);
    } catch (err) {
      log.warn(`   ⚠️ 论文下载失败: ${err.message}`);
    }
  }

  searchResults.items.push(item);
  searchResults.totalResults++;

  // 更新来源统计
  if (!searchResults.bySource[item.source]) {
    searchResults.bySource[item.source] = { count: 0, items: [] };
  }
  searchResults.bySource[item.source].count++;
  searchResults.bySource[item.source].items.push(item.id);

  return item;
}

/**
 * 保存搜索结果汇总
 */
function saveSearchResults() {
  const filePath = path.join(dirs.collected, 'search_results.json');
  fileUtils.writeJson(filePath, searchResults);
  log.info(`\n💾 搜索结果已保存: ${filePath}`);
}

/**
 * 获取统计数据
 */
function getStats() {
  const stats = {
    total: searchResults.totalResults,
    bySource: {},
    withContent: 0,
    papers: 0,
    totalContentSize: 0
  };

  for (const [source, data] of Object.entries(searchResults.bySource)) {
    stats.bySource[source] = data.count;
  }

  for (const item of searchResults.items) {
    if (item.contentFile) {
      stats.withContent++;
      stats.totalContentSize += fileUtils.getFileSize(item.contentFile);
    }
    if (item.isPaper && item.paperFile) {
      stats.papers++;
    }
  }

  stats.totalContentSizeFormatted = fileUtils.formatFileSize(stats.totalContentSize);
  return stats;
}

// ============================================================
// 主函数（可被外部调用）
// ============================================================

/**
 * 执行搜索和收集
 * @param {string} topic 
 * @param {object} options 
 * @returns {Promise<object>}
 */
async function run(topic = TOPIC, options = {}) {
  log.stepStart(1, '内容搜索', '围绕主题搜索大量相关内容，构建知识基础');
  
  try {
    // 执行搜索
    const searchData = await performSearch(topic, {
      sources: options.sources || ['GitHub', 'Hacker News', '知乎'],
      depth: options.depth || DEPTH
    });

    // 保存结果
    saveSearchResults();

    // 获取统计
    const stats = getStats();
    
    log.stepComplete(1, {
      '搜索主题': topic,
      '总结果数': stats.total,
      '抽取内容': stats.withContent,
      '下载论文': stats.papers,
      '内容总大小': stats.totalContentSizeFormatted,
      '会话目录': dirs.base
    });

    // 保存会话信息供后续步骤使用
    const sessionInfo = {
      sessionId: SESSION_ID,
      topic: TOPIC,
      baseDir: dirs.base,
      collectedDir: dirs.collected,
      webPagesDir: dirs.webPages,
      papersDir: dirs.papers,
      searchResultsFile: path.join(dirs.collected, 'search_results.json')
    };
    fileUtils.writeJson(path.join(dirs.base, 'session_info.json'), sessionInfo);

    return {
      success: true,
      sessionId: SESSION_ID,
      baseDir: dirs.base,
      stats,
      searchResults
    };
  } catch (error) {
    log.stepFailed(1, error.message);
    throw error;
  }
}

// ============================================================
// 直接执行
// ============================================================
if (require.main === module) {
  run().then(result => {
    console.log('\n✅ 搜索完成！');
    console.log(`📁 会话目录: ${result.baseDir}`);
    console.log(`📊 统计: 共 ${result.stats.total} 条结果`);
  }).catch(err => {
    console.error('❌ 搜索失败:', err.message);
    process.exit(1);
  });
}

// 导出
module.exports = { run, performSearch, addSearchResult, SESSION_ID, dirs };
