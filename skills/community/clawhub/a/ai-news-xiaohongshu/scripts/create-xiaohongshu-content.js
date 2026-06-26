#!/usr/bin/env node

/**
 * AI 资讯小红书内容创作脚本
 * 
 * 功能：
 * 1. 获取当前时间
 * 2. 接收传入的资讯数据（由 OpenClaw 主流程搜索后传入）
 * 3. 生成小红书文案
 * 4. 生成 3:4 比例 HTML 封面
 * 5. 输出到 output/日期 目录
 * 6. 打开输出目录
 * 
 * 使用方式：
 * node create-xiaohongshu-content.js --news-json '{"..."}'
 * 或直接运行使用默认演示数据
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// 配置
const SKILL_DIR = path.join(__dirname, '..');
const OUTPUT_BASE = path.join(SKILL_DIR, 'output');
const USER_CONFIG_PATH = path.join(SKILL_DIR, 'references', 'user-config.md');

// 默认配置
const DEFAULT_CONFIG = {
  callToAction: `📌 关注我，每日更新 AI 前沿资讯
👉 评论区留言"资料"获取 AI 工具包
💬 加入交流群：xxx`,
  coreNewsCount: 5,
  htmlPages: 2,
  focus: 'all'
};

// 演示数据（仅当没有传入真实数据时使用）
const DEMO_NEWS = [
  {
    title: "OpenAI 发布 GPT-4.5，推理速度提升 3 倍",
    content: "OpenAI 今日凌晨突然发布 GPT-4.5 模型，在推理速度和准确性上都有显著提升...",
    url: "https://openai.com/blog/gpt-4-5",
    time: "2 小时前",
    source: "OpenAI 官方博客"
  },
  {
    title: "阿里千问 Qwen3 开源，直接对标 Llama3",
    content: "阿里达摩院宣布开源 Qwen3 系列模型，包含 7B、72B 等多个版本...",
    url: "https://qwenlm.github.io/",
    time: "5 小时前",
    source: "阿里达摩院"
  },
  {
    title: "MiniMax 完成 5 亿美元融资，估值破百亿",
    content: "国内 AI 独角兽 MiniMax 宣布完成新一轮融资，投后估值超过 100 亿美元...",
    url: "https://www.minimax.io/",
    time: "8 小时前",
    source: "36 氪"
  },
  {
    title: "Anthropic 推出 Claude 3.5，安全性大幅提升",
    content: "Anthropic 发布 Claude 3.5 系列，在保持性能的同时显著提升了安全性...",
    url: "https://www.anthropic.com/",
    time: "12 小时前",
    source: "Anthropic"
  },
  {
    title: "Google Gemini 2.0 正式推送，多模态能力再升级",
    content: "Google 宣布 Gemini 2.0 正式向所有用户推送，图像理解和视频分析能力大幅提升...",
    url: "https://deepmind.google/",
    time: "18 小时前",
    source: "Google DeepMind"
  }
];

/**
 * 获取当前日期时间
 */
function getCurrentDateTime() {
  const now = new Date();
  const dateStr = now.toISOString().split('T')[0];
  const timeStr = now.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
  const dateDisplay = now.toLocaleDateString('zh-CN', { month: '2-digit', day: '2-digit' });
  const year = now.getFullYear();
  
  return { dateStr, timeStr, dateDisplay, year, full: now };
}

/**
 * 创建输出目录
 */
function createOutputDir(dateStr) {
  const outputDir = path.join(OUTPUT_BASE, dateStr);
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
  return outputDir;
}

/**
 * 加载用户配置
 */
function loadUserConfig() {
  try {
    if (fs.existsSync(USER_CONFIG_PATH)) {
      return { ...DEFAULT_CONFIG };
    }
  } catch (e) {
    console.log('未找到用户配置，使用默认配置');
  }
  return { ...DEFAULT_CONFIG };
}

/**
 * 解析命令行参数
 */
function parseArgs() {
  const args = process.argv.slice(2);
  const params = {};
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--news-json' && args[i + 1]) {
      try {
        params.newsData = JSON.parse(args[i + 1]);
      } catch (e) {
        console.log('⚠️ JSON 解析失败，使用演示数据');
      }
      i++;
    } else if (args[i] === '--use-demo') {
      params.useDemo = true;
    }
  }
  
  return params;
}

/**
 * 生成小红书文案
 */
function generateXiaohongshuCopy(newsItems, config, dateTime) {
  const topNews = newsItems.slice(0, config.coreNewsCount);
  
  const title = `🔥 AI 圈炸了！今日${newsItems.length}大重磅消息，第 3 个太意外！`;
  
  let body = `家人们谁懂啊！今天 AI 圈又是大动作不断😱\n`;
  body += `早上刚醒就看到一堆重磅消息，赶紧给大家整理好了！\n\n`;
  
  body += `📌 今日核心资讯：\n`;
  topNews.forEach((news, i) => {
    const emojis = ['🚀', '💪', '💰', '🔥', '⚡', '🎯', '💡', '🌟'];
    const emoji = emojis[i % emojis.length];
    body += `• ${news.title} ${emoji}\n`;
  });
  
  body += `\n💡 个人解读：\n`;
  body += `这次几家大厂都在疯狂内卷，看来 2026 年 AI 竞争要白热化了...\n`;
  body += `个人最看好阿里开源这步棋，生态才是王道啊！\n\n`;
  
  body += `👇 互动时间：\n`;
  body += `最期待哪个模型？评论区聊聊～\n\n`;
  
  body += `${config.callToAction}\n\n`;
  
  body += `#AI #大模型 #人工智能 #科技资讯 #AIGC #OpenAI #阿里 #MiniMax #Claude #Gemini`;
  
  return { title, body };
}

/**
 * 生成 HTML 封面
 */
function generateHTML(newsItems, config, dateTime) {
  const pages = [];
  
  // 根据资讯数量自动计算页数（每页最多 5 条卡片）
  const ITEMS_PER_PAGE = 5;
  const detailPagesNeeded = Math.ceil(newsItems.length / ITEMS_PER_PAGE);
  const numPages = 1 + detailPagesNeeded + 1; // 封面 + 详细页 + 观点页
  
  // 第 1 屏：标题 + 核心资讯
  pages.push(`
    <div class="page page-1">
      <div class="header">
        <h1>🔥 AI 日报</h1>
        <div class="date">${dateTime.year}.${dateTime.dateDisplay}</div>
      </div>
      
      <div class="highlight-box">
        <div class="highlight-title">今日重磅</div>
        <div class="highlight-content">${newsItems[0]?.title || '暂无重磅'}</div>
      </div>
      
      <div class="news-preview">
        ${newsItems.slice(0, 3).map(news => `
          <div class="news-item">
            <span class="news-emoji">📌</span>
            <span class="news-text">${news.title}</span>
          </div>
        `).join('')}
      </div>
      
      <div class="footer">
        <span>共 ${newsItems.length} 条资讯</span>
        <span>滑动查看更多 →</span>
      </div>
    </div>
  `);
  
  // 第 2~N 屏：详细列表（自动分页，每页 5 条）
  for (let pageNum = 0; pageNum < detailPagesNeeded; pageNum++) {
    const startIdx = pageNum * ITEMS_PER_PAGE;
    const endIdx = Math.min(startIdx + ITEMS_PER_PAGE, newsItems.length);
    const pageNews = newsItems.slice(startIdx, endIdx);
    const isLastDetailPage = pageNum === detailPagesNeeded - 1;
    
    pages.push(`
      <div class="page page-${pageNum + 2} page-detail">
        <div class="section-title">📊 详细资讯 ${startIdx + 1}-${endIdx} / ${newsItems.length}</div>
        
        <div class="news-list">
          ${pageNews.map((news, i) => `
            <div class="news-card">
              <div class="news-card-header">
                <span class="news-number">${startIdx + i + 1}</span>
                <span class="news-time">${news.time}</span>
              </div>
              <div class="news-card-title">${news.title}</div>
              <div class="news-card-source">${news.source}</div>
            </div>
          `).join('')}
        </div>
        
        ${isLastDetailPage ? '' : '<div class="page-hint">↓ 继续滑动查看更多 ↓</div>'}
      </div>
    `);
  }
  
  // 最后一屏：观点 + 互动
  pages.push(`
    <div class="page page-${numPages} page-last">
      <div class="section-title">💡 我的观点</div>
      
      <div class="opinion-box">
        <p>2026 年 AI 竞争进入白热化阶段</p>
        <p>开源 vs 闭源，谁能笑到最后？</p>
        <p>你觉得哪个模型最强？</p>
      </div>
      
      <div class="cta-box">
        <div class="cta-text">👇 评论区聊聊</div>
        <div class="cta-sub">关注我，每日更新 AI 前沿</div>
      </div>
      
      <div class="tags">
        <span>#AI</span>
        <span>#大模型</span>
        <span>#人工智能</span>
        <span>#科技资讯</span>
      </div>
    </div>
  `);
  
  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI 日报 - ${dateTime.dateDisplay}</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
      background: #0a0a0f;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
    }
    
    .container { width: 1080px; margin: 0 auto; }
    
    .page {
      width: 1080px;
      height: 1440px;
      position: relative;
      overflow: hidden;
      page-break-after: always;
    }
    
    /* ========== 第 1 页：封面 ========== */
    .page-1 {
      background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 35%, #d946ef 100%);
      padding: 80px 60px;
    }
    
    .header { text-align: center; margin-bottom: 60px; }
    .header h1 {
      font-size: 96px;
      color: #fff;
      font-weight: 900;
      text-shadow: 0 4px 30px rgba(99, 102, 241, 0.4);
      margin-bottom: 20px;
      letter-spacing: -2px;
    }
    .date {
      font-size: 48px;
      color: rgba(255,255,255,0.95);
      font-weight: 500;
      letter-spacing: 1px;
    }
    
    .highlight-box {
      background: rgba(255,255,255,0.15);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border-radius: 30px;
      padding: 50px;
      margin-bottom: 50px;
      border: 2px solid rgba(255,255,255,0.3);
      box-shadow: 0 8px 32px rgba(0,0,0,0.2);
    }
    .highlight-title { font-size: 36px; color: rgba(255,255,255,0.85); margin-bottom: 20px; font-weight: 600; }
    .highlight-content { font-size: 44px; color: #fff; font-weight: 700; line-height: 1.4; }
    
    .news-preview { background: rgba(255,255,255,0.12); border-radius: 25px; padding: 40px; }
    .news-item { display: flex; align-items: center; padding: 25px 0; border-bottom: 1px solid rgba(255,255,255,0.2); }
    .news-item:last-child { border-bottom: none; }
    .news-emoji { font-size: 36px; margin-right: 25px; }
    .news-text { font-size: 32px; color: #fff; flex: 1; font-weight: 500; }
    
    .footer {
      position: absolute;
      bottom: 60px;
      left: 60px;
      right: 60px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .footer span { font-size: 28px; color: rgba(255,255,255,0.9); font-weight: 500; }
    
    /* ========== 详细资讯页 ========== */
    .page-detail {
      background: linear-gradient(180deg, #f1f5f9 0%, #e2e8f0 100%);
      padding: 80px 60px;
    }
    
    .section-title {
      font-size: 64px;
      color: #1e293b;
      font-weight: 800;
      margin-bottom: 50px;
      text-align: center;
      letter-spacing: -1px;
    }
    
    .news-list { display: flex; flex-direction: column; gap: 25px; }
    
    .news-card {
      background: #ffffff;
      border-radius: 20px;
      padding: 32px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.08), 0 2px 8px rgba(0,0,0,0.04);
      border-left: 6px solid #6366f1;
      break-inside: avoid;
      transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .news-card:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 30px rgba(99, 102, 241, 0.15);
    }
    
    .news-card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; }
    .news-number {
      background: linear-gradient(135deg, #6366f1, #8b5cf6);
      color: #fff;
      width: 48px;
      height: 48px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 22px;
      font-weight: 700;
      flex-shrink: 0;
      box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    }
    .news-time { font-size: 22px; color: #64748b; font-weight: 500; }
    
    .news-card-title {
      font-size: 32px;
      color: #0f172a;
      font-weight: 700;
      margin-bottom: 12px;
      line-height: 1.35;
    }
    .news-card-source {
      font-size: 22px;
      color: #6366f1;
      font-weight: 600;
      letter-spacing: 0.3px;
    }
    
    .page-hint {
      text-align: center;
      font-size: 24px;
      color: #64748b;
      margin-top: 35px;
      opacity: 0.8;
      font-weight: 500;
      letter-spacing: 1px;
    }
    
    /* ========== 最后一页：观点 ========== */
    .page-last {
      background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
      padding: 80px 60px;
    }
    .page-last .section-title { color: #f1f5f9; }
    
    .opinion-box {
      background: rgba(255,255,255,0.08);
      backdrop-filter: blur(10px);
      -webkit-backdrop-filter: blur(10px);
      border-radius: 25px;
      padding: 50px;
      margin-bottom: 50px;
      border: 1px solid rgba(255,255,255,0.15);
    }
    .opinion-box p { font-size: 36px; color: #f1f5f9; margin-bottom: 25px; line-height: 1.5; font-weight: 400; }
    
    .cta-box {
      background: linear-gradient(135deg, #6366f1, #8b5cf6);
      border-radius: 25px;
      padding: 50px;
      text-align: center;
      margin-bottom: 50px;
      box-shadow: 0 8px 30px rgba(99, 102, 241, 0.3);
    }
    .cta-text { font-size: 48px; color: #fff; font-weight: 700; margin-bottom: 15px; }
    .cta-sub { font-size: 32px; color: rgba(255,255,255,0.95); font-weight: 500; }
    
    .tags { display: flex; flex-wrap: wrap; gap: 15px; justify-content: center; }
    .tags span {
      background: rgba(99, 102, 241, 0.2);
      color: #e0e7ff;
      padding: 15px 30px;
      border-radius: 50px;
      font-size: 24px;
      font-weight: 600;
      border: 1px solid rgba(99, 102, 241, 0.3);
    }
    
    /* ========== 分页分隔线 ========== */
    .page-break {
      height: 12px;
      background: repeating-linear-gradient(
        45deg,
        #6366f1,
        #6366f1 15px,
        #8b5cf6 15px,
        #8b5cf6 30px
      );
      flex-shrink: 0;
      box-shadow: 0 2px 8px rgba(99, 102, 241, 0.4);
    }
  </style>
</head>
<body>
  <div class="container">
    ${pages.join('<div class="page-break"></div>')}
  </div>
</body>
</html>`;
}

/**
 * 生成资讯汇总表格
 */
function generateNewsSummary(newsItems, dateTime) {
  let md = `# AI 资讯汇总 - ${dateTime.dateDisplay}\n\n`;
  md += `| 时间 | 公司/项目 | 核心内容 | 来源 |\n`;
  md += `|------|----------|---------|------|\n`;
  
  newsItems.forEach(news => {
    const company = news.title.split(/[，,]/)[0];
    md += `| ${news.time} | ${company} | ${news.content.substring(0, 50)}... | [链接](${news.url}) |\n`;
  });
  
  return md;
}

/**
 * 生成来源链接列表
 */
function generateSources(newsItems) {
  let md = `# 原始来源链接 - ${new Date().toLocaleDateString('zh-CN')}\n\n`;
  newsItems.forEach((news, i) => {
    md += `${i + 1}. [${news.title}](${news.url}) - ${news.source}\n`;
  });
  return md;
}

/**
 * 打开目录
 */
function openDirectory(dirPath) {
  try {
    if (process.platform === 'darwin') {
      execSync(`open "${dirPath}"`);
    } else if (process.platform === 'win32') {
      execSync(`explorer "${dirPath}"`);
    } else {
      execSync(`xdg-open "${dirPath}"`);
    }
    console.log(`✅ 已打开目录：${dirPath}`);
  } catch (e) {
    console.log(`⚠️ 无法自动打开目录，请手动前往：${dirPath}`);
  }
}

/**
 * 在浏览器中打开 HTML 文件
 */
function openHTML(filePath) {
  try {
    if (process.platform === 'darwin') {
      execSync(`open "${filePath}"`);
    } else if (process.platform === 'win32') {
      execSync(`start "" "${filePath}"`);
    } else {
      execSync(`xdg-open "${filePath}"`);
    }
    console.log(`✅ HTML 封面已在浏览器中打开`);
  } catch (e) {
    console.log(`⚠️ 无法自动打开浏览器，请手动打开：${filePath}`);
  }
}

/**
 * 主函数
 */
async function main() {
  console.log('🚀 AI 资讯小红书内容创作开始...\n');
  
  // 1. 获取当前时间
  const dateTime = getCurrentDateTime();
  console.log(`📅 当前时间：${dateTime.dateStr} ${dateTime.timeStr}`);
  
  // 2. 创建输出目录
  const outputDir = createOutputDir(dateTime.dateStr);
  console.log(`📁 输出目录：${outputDir}\n`);
  
  // 3. 加载用户配置
  const config = loadUserConfig();
  console.log(`⚙️ 配置：核心资讯${config.coreNewsCount}条，HTML${config.htmlPages}屏\n`);
  
  // 4. 获取资讯数据
  const params = parseArgs();
  let newsItems = [];
  
  if (params.newsData && Array.isArray(params.newsData)) {
    console.log('🔍 使用传入的真实搜索数据...');
    newsItems = params.newsData;
  } else {
    console.log('⚠️ 未传入数据，使用演示数据（请使用 --news-json 传入真实搜索结果）');
    newsItems = DEMO_NEWS;
  }
  
  console.log(`✅ 共 ${newsItems.length} 条资讯\n`);
  
  // 5. 生成小红书文案
  console.log('✍️ 正在创作小红书文案...');
  const { title, body } = generateXiaohongshuCopy(newsItems, config, dateTime);
  const copyContent = `【标题】${title}\n\n【正文】\n${body}`;
  fs.writeFileSync(path.join(outputDir, 'xiaohongshu-copy.md'), copyContent);
  console.log(`✅ 文案已保存\n`);
  
  // 6. 生成 HTML 封面
  console.log('🎨 正在设计 HTML 封面...');
  const htmlContent = generateHTML(newsItems, config, dateTime);
  fs.writeFileSync(path.join(outputDir, 'cover.html'), htmlContent);
  console.log(`✅ HTML 封面已保存\n`);
  
  // 7. 生成资讯汇总
  console.log('📊 正在生成资讯汇总...');
  const summaryContent = generateNewsSummary(newsItems, dateTime);
  fs.writeFileSync(path.join(outputDir, 'news-summary.md'), summaryContent);
  console.log(`✅ 资讯汇总已保存\n`);
  
  // 8. 生成来源链接
  console.log('🔗 正在整理来源链接...');
  const sourcesContent = generateSources(newsItems);
  fs.writeFileSync(path.join(outputDir, 'sources.md'), sourcesContent);
  console.log(`✅ 来源链接已保存\n`);
  
  // 9. 打开 HTML 预览
  console.log('🌐 正在打开 HTML 预览...');
  openHTML(path.join(outputDir, 'cover.html'));
  
  // 10. 打开输出目录
  setTimeout(() => {
    console.log('\n📂 正在打开输出目录...');
    openDirectory(outputDir);
  }, 1000);
  
  console.log('\n✅ 创作完成！\n');
  console.log('═══════════════════════════════════════');
  console.log('📱 小红书文案：xiaohongshu-copy.md');
  console.log('🎨 HTML 封面：cover.html（可截图使用）');
  console.log('📊 资讯汇总：news-summary.md');
  console.log('🔗 来源链接：sources.md');
  console.log('═══════════════════════════════════════\n');
  
  // 输出 JSON 供调用方使用
  console.log('📤 输出数据摘要:');
  console.log(JSON.stringify({
    date: dateTime.dateStr,
    outputDir,
    newsCount: newsItems.length,
    files: ['xiaohongshu-copy.md', 'cover.html', 'news-summary.md', 'sources.md']
  }, null, 2));
}

// 运行
main().catch(console.error);
