#!/usr/bin/env node

/**
 * 柯南周报技能 - 主脚本
 * 
 * 功能：搜索并整理名侦探柯南最新剧情进展
 * 执行时间：每周六 21:00 (Asia/Shanghai)
 * 
 * 运行方式：
 * 1. 通过 OpenClaw 定时任务自动执行（推荐）
 * 2. 手动运行：node index.js
 */

const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');

// 配置
const CONFIG = {
  searchQueries: [
    '名侦探柯南 动画 最新集数 剧情 2026',
    '名侦探柯南 主线剧情 黑衣组织 更新',
    '名侦探柯南 特别篇 剧场版 2026',
    '名侦探柯南 声优 角色 登场'
  ],
  outputDir: path.join(__dirname, 'reports'),
  timezone: 'Asia/Shanghai',
  // 搜索超时时间（毫秒）
  requestTimeout: 10000,
  // 请求间隔（毫秒）
  requestDelay: 1500
};

/**
 * 确保输出目录存在
 */
function ensureOutputDir() {
  if (!fs.existsSync(CONFIG.outputDir)) {
    fs.mkdirSync(CONFIG.outputDir, { recursive: true });
  }
}

/**
 * HTTP GET 请求（支持超时）
 */
function httpGet(url) {
  return new Promise((resolve, reject) => {
    const protocol = url.startsWith('https') ? https : http;
    const req = protocol.get(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
      },
      timeout: CONFIG.requestTimeout
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(data);
        } else {
          reject(new Error(`HTTP ${res.statusCode}: ${res.statusMessage}`));
        }
      });
    });
    req.on('error', reject);
    req.on('timeout', () => {
      req.destroy();
      reject(new Error('Request timeout'));
    });
  });
}

/**
 * 搜索柯南剧情（使用 DuckDuckGo HTML 接口）
 */
async function searchConanNews() {
  console.log('🔍 开始搜索柯南最新剧情...');
  
  const results = [];
  
  for (const query of CONFIG.searchQueries) {
    console.log(`  搜索：${query}`);
    
    try {
      // 使用 DuckDuckGo HTML 接口（无需 API 密钥）
      const encodedQuery = encodeURIComponent(query);
      const searchUrl = `https://html.duckduckgo.com/html/?q=${encodedQuery}`;
      
      const html = await httpGet(searchUrl);
      
      // 解析搜索结果
      const snippets = parseDuckDuckGoResults(html, query);
      
      results.push({
        query,
        snippets,
        timestamp: new Date().toISOString()
      });
      
      console.log(`    找到 ${snippets.length} 条结果`);
    } catch (error) {
      console.log(`    搜索失败：${error.message}`);
      results.push({
        query,
        snippets: [],
        error: error.message,
        timestamp: new Date().toISOString()
      });
    }
    
    // 避免请求过快
    await sleep(CONFIG.requestDelay);
  }
  
  return results;
}

/**
 * 解析 DuckDuckGo 搜索结果
 */
function parseDuckDuckGoResults(html, query) {
  const snippets = [];
  
  // 提取结果标题和链接
  const resultRegex = /<a[^>]*class="result__a"[^>]*href="([^"]*)"[^>]*>([^<]+)<\/a>/g;
  
  let match;
  let count = 0;
  
  while ((match = resultRegex.exec(html)) !== null && count < 5) {
    let url = match[1];
    const title = match[2].replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>');
    
    // 提取 DuckDuckGo 重定向链接中的真实 URL
    if (url.includes('uddg=')) {
      try {
        const urlMatch = url.match(/uddg=([^&]+)/);
        if (urlMatch && urlMatch[1]) {
          url = decodeURIComponent(urlMatch[1]);
        }
      } catch (e) {
        // 解析失败，保留原链接
      }
    }
    
    snippets.push({
      title: title.trim(),
      url: url,
      query
    });
    count++;
  }
  
  return snippets;
}

/**
 * 辅助函数：延迟
 */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * 根据搜索查询获取分类名称
 */
function getCategoryFromQuery(query) {
  if (query.includes('最新集数')) return '新播出集数';
  if (query.includes('主线剧情')) return '主线剧情进展';
  if (query.includes('特别篇') || query.includes('剧场版')) return '特别篇/剧场版';
  if (query.includes('声优') || query.includes('角色')) return '角色/声优动态';
  return '其他资讯';
}

/**
 * 获取周数
 */
function getWeekNumber(date) {
  const d = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()));
  const dayNum = d.getUTCDay() || 7;
  d.setUTCDate(d.getUTCDate() + 4 - dayNum);
  const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
  return Math.ceil((((d - yearStart) / 86400000) + 1) / 7);
}

/**
 * 整理周报内容
 */
function compileReport(searchResults) {
  const now = new Date();
  const dateStr = now.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    weekday: 'long'
  });
  
  const weekNum = getWeekNumber(now);
  
  let report = `📺 柯南周报 | 2026 年第${weekNum}周 (${dateStr})
═══════════════════════════════════════\n\n`;

  let hasContent = false;

  // 整理搜索结果
  for (const result of searchResults) {
    if (result.snippets && result.snippets.length > 0) {
      hasContent = true;
      const category = getCategoryFromQuery(result.query);
      report += `【${category}】\n`;
      result.snippets.forEach((snippet, idx) => {
        report += `  ${idx + 1}. ${snippet.title}\n`;
        if (snippet.url) {
          report += `     🔗 ${snippet.url}\n`;
        }
      });
      report += '\n';
    }
  }

  if (!hasContent) {
    report += `⚠️ 本次搜索未获取到有效结果，可能是网络问题或搜索源暂时不可用。\n`;
    report += `建议手动查阅以下渠道获取最新柯南资讯：\n`;
    report += `  • 哔哩哔哩动画：https://www.bilibili.com/bangumi/media/md2819\n`;
    report += `  • 百度百科：https://baike.baidu.com/item/名侦探柯南/3469662\n`;
    report += `  • 维基百科：https://zh.wikipedia.org/wiki/名侦探柯南\n\n`;
  }

  report += `═══════════════════════════════════════
📌 数据来源：网络公开搜索结果
🔗 详细剧情请查阅官方渠道或动漫资讯站
⏰ 下期周报：下周六晚 9 点
`;

  return report;
}

/**
 * 发送/保存报告
 */
async function sendReport(report) {
  ensureOutputDir();
  
  const filename = `conan-report-${new Date().toISOString().split('T')[0]}.md`;
  const filepath = path.join(CONFIG.outputDir, filename);
  
  fs.writeFileSync(filepath, report, 'utf8');
  console.log(`📄 报告已保存：${filepath}`);
  
  // 输出到控制台
  console.log('\n' + report);
  
  // 如果配置了 OpenClaw 消息接口，可以通过环境变量发送
  const webhookUrl = process.env.REPORT_WEBHOOK_URL;
  if (webhookUrl) {
    await sendViaWebhook(webhookUrl, report);
  }
}

/**
 * 通过 Webhook 发送报告
 */
async function sendViaWebhook(url, report) {
  try {
    const postData = JSON.stringify({ text: report });
    const parsedUrl = new URL(url);
    
    await new Promise((resolve, reject) => {
      const protocol = parsedUrl.protocol === 'https:' ? https : http;
      const req = protocol.request(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(postData)
        }
      }, (res) => {
        if (res.statusCode === 200) {
          console.log('📤 报告已发送');
          resolve();
        } else {
          reject(new Error(`HTTP ${res.statusCode}`));
        }
      });
      req.on('error', reject);
      req.write(postData);
      req.end();
    });
  } catch (error) {
    console.log('⚠️ Webhook 发送失败:', error.message);
  }
}

/**
 * 主函数
 */
async function main() {
  console.log('🎬 柯南周报技能启动...');
  console.log(`📁 报告目录：${CONFIG.outputDir}`);
  console.log(`🌐 搜索源：DuckDuckGo HTML`);
  console.log(`⏱️  请求超时：${CONFIG.requestTimeout}ms`);
  console.log(`⏸️  请求间隔：${CONFIG.requestDelay}ms\n`);
  
  try {
    // 1. 搜索
    const searchResults = await searchConanNews();
    
    // 2. 整理
    const report = compileReport(searchResults);
    
    // 3. 发送/保存
    await sendReport(report);
    
    console.log('✅ 柯南周报生成完成！');
    process.exit(0);
  } catch (error) {
    console.error('❌ 错误:', error.message);
    console.error(error.stack);
    process.exit(1);
  }
}

// 执行
if (require.main === module) {
  main();
}

module.exports = { main, searchConanNews, compileReport, sendReport };
