#!/usr/bin/env node

const { execSync, spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const puppeteer = require(path.join(__dirname, '../node_modules/puppeteer-core'));

// 配置
const WORKSPACE = '/home/xiaoduo/.openclaw/workspace-product';
const OUTPUT_DIR = path.join(WORKSPACE, 'output');

// 预设商机发现 Skills 列表（当 API 限流时使用）
const FALLBACK_SKILLS = [
  { slug: 'opportunity-discovery', name: 'Opportunity Discovery Engine', summary: '系统性地分析市场、趋势和想法，识别并排序具有高收益和有限下行风险的盈利机会。', owner: 'dtjohnson83', updated: '2026-03-16', version: '1.0.0' },
  { slug: 'business-opportunity-detector', name: 'Hidden Business Opportunity Detector', summary: '自动抓取和分析多平台用户评论，识别、评分并报告经过验证的隐藏 SaaS 商业机会和市场空白。', owner: 'g4dr', updated: '2026-02-26', version: '1.0.0' },
  { slug: 'opportunity-assessment', name: 'Opportunity Assessment', summary: '商机判断与风险评估技能。接收新项目信息，主动询问关键问题，输出风险分级评估、待确认事项清单、商机建议。', owner: 'yakov0922', updated: '2026-03-04', version: '1.0.0' },
  { slug: 'market-environment-analysis', name: 'Market Environment Analysis', summary: '全面的市场环境分析和报告工具。分析全球市场，包括美国、欧洲、亚洲市场、外汇、大宗商品和经济指标。', owner: 'Veeramanikandanr48', updated: '2026-02-26', version: '0.1.0' },
  { slug: 'market-analysis-cn', name: 'Market Analysis CN', summary: '市场分析服务。企业市场趋势分析、竞品分析、用户行为洞察。', owner: 'guohongbin-git', updated: '2026-02-25', version: '1.0.0' },
  { slug: 'market-sentiment-pulse', name: 'Market Sentiment Pulse', summary: '通过扫描新闻和社交信号，聚合和分析特定加密货币或股票代码的市场情绪。', owner: 'balkanblbn', updated: '2026-02-28', version: '1.1.0' },
  { slug: 'business-development', name: 'Business Development', summary: '合作伙伴拓展、市场研究、竞品分析和提案生成。将你的 AI 代理转变为战略业务开发合作伙伴。', owner: 'oyi77', updated: '2026-02-26', version: '1.0.0' },
  { slug: 'business', name: 'Business Strategy', summary: '使用经过验证的框架验证想法、构建战略和做出决策。', owner: 'ivangdavila', updated: '2026-03-16', version: '1.1.0' },
  { slug: 'startup', name: 'Startup', summary: '通过生成专业代理并应用阶段适当的优先级来协调创业工作。', owner: 'ivangdavila', updated: '2026-02-26', version: '1.0.0' },
  { slug: 'lead-generation', name: 'Lead Generation', summary: '在实时 Twitter、Instagram 和 Reddit 对话中寻找高意向买家。自动研究你的产品，生成有针对性的搜索查询。', owner: 'atyachin', updated: '2026-03-16', version: '2.2.0' },
  { slug: 'lead-researcher', name: 'Lead Researcher', summary: 'B2B 销售的自动化潜在客户研究和丰富。找到符合你标准的公司，丰富联系数据，并生成个性化 outreach 消息。', owner: 'rjrileybuisness-ai', updated: '2026-03-16', version: '1.0.0' },
  { slug: 'business-opportunity-insight', name: 'Business Opportunity Insight', summary: '商业机会洞察力分析，帮助发现潜在市场机会。', owner: '未知', updated: '2026-01-01', version: '1.0.0' },
  { slug: 'startup-toolkit', name: 'Startup Toolkit', summary: '创业工具包，提供创业过程中需要的各种工具和模板。', owner: 'ivangdavila', updated: '2026-02-26', version: '1.0.0' },
  { slug: 'startup-financial-modeling', name: 'Startup Financial Modeling', summary: '创业公司财务建模工具，帮助规划财务预测和融资策略。', owner: '未知', updated: '2026-02-26', version: '1.0.0' },
  { slug: 'competitor-analysis', name: 'Competitor Analysis', summary: '竞争对手分析工具，帮助了解市场竞品格局。', owner: '未知', updated: '2026-01-01', version: '1.0.0' }
];

// 获取日期
function getDateString() {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const day = String(now.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

// 执行命令
function exec(command, options = {}) {
  console.log(`[EXEC] ${command}`);
  try {
    return execSync(command, { 
      stdio: 'pipe', 
      encoding: 'utf8',
      timeout: 15000, // 15秒超时
      ...options 
    }).trim();
  } catch (e) {
    console.log(`[WARN] Command failed: ${e.message}`);
    return '';
  }
}

// 搜索 Skills
function searchSkills(query) {
  console.log(`[INFO] Searching for skills: ${query}`);
  const result = exec(`clawhub search ${query}`);
  
  // 检测 rate limit
  if (result.includes('Rate limit') || result.includes('rate limit')) {
    console.log(`[WARN] Rate limit detected, using fallback data`);
    return [];
  }
  
  if (!result || result.includes('Searching')) {
    console.log(`[WARN] No results or error, using fallback data`);
    return [];
  }
  
  const lines = result.split('\n').filter(l => l.includes('- '));
  
  const skills = [];
  for (const line of lines) {
    const match = line.match(/-\s+(\S+)\s+(.+)/);
    if (match) {
      skills.push({ slug: match[1], name: match[2] });
    }
  }
  console.log(`[INFO] Found ${skills.length} skills from API`);
  return skills.slice(0, 15);
}

// 获取 Skill 详情
function inspectSkill(slug) {
  try {
    const result = exec(`clawhub inspect ${slug}`);
    
    if (!result || result.includes('Error')) {
      return null;
    }
    
    const info = {
      slug: slug,
      name: '',
      summary: '',
      owner: '',
      updated: '',
      version: ''
    };
    
    const lines = result.split('\n');
    for (const line of lines) {
      if (line.includes('Summary:')) {
        info.summary = line.replace('Summary:', '').trim();
      } else if (line.includes('Owner:')) {
        info.owner = line.replace('Owner:', '').trim();
      } else if (line.includes('Updated:')) {
        info.updated = line.replace('Updated:', '').trim().split('T')[0];
      } else if (line.includes('Latest:')) {
        info.version = line.replace('Latest:', '').trim();
      }
    }
    
    // 从第一行获取名称
    const firstLine = lines.find(l => l.includes(slug));
    if (firstLine) {
      const parts = firstLine.split(/\s+/);
      info.name = parts.slice(1).join(' ').replace(slug, '').trim();
    }
    
    return info;
  } catch (e) {
    console.log(`[WARN] Failed to inspect ${slug}: ${e.message}`);
    return null;
  }
}

// 生成 HTML 报告
function generateReport(skills, outputName, isFallback = false) {
  const fallbackNote = isFallback ? '<p style="text-align:center;color:#ff9800;margin-bottom:20px;">⚠️ 数据来源：预设列表（API 限流）</p>' : '';
  
  const html = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${outputName}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            padding: 40px 20px;
            color: #e0e0e0;
        }
        .container { max-width: 1000px; margin: 0 auto; }
        h1 {
            text-align: center;
            font-size: 2.5em;
            margin-bottom: 10px;
            background: linear-gradient(90deg, #00d4ff, #7c3aed);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .subtitle { text-align: center; color: #888; margin-bottom: 40px; font-size: 1.1em; }
        .category {
            margin-top: 30px;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid rgba(0,212,255,0.3);
            font-size: 1.3em;
            color: #fff;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .skill-card {
            background: rgba(255,255,255,0.05);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            border: 1px solid rgba(255,255,255,0.1);
            transition: all 0.3s ease;
        }
        .skill-card:hover {
            transform: translateY(-2px);
            border-color: rgba(0,212,255,0.3);
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        }
        .skill-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
            flex-wrap: wrap;
            gap: 10px;
        }
        .skill-name { font-size: 1.4em; font-weight: 600; color: #00d4ff; }
        .skill-owner {
            font-size: 0.85em;
            color: #888;
            background: rgba(255,255,255,0.1);
            padding: 4px 12px;
            border-radius: 20px;
        }
        .skill-desc { color: #ccc; line-height: 1.6; margin-bottom: 16px; font-size: 1.05em; }
        .skill-meta { display: flex; gap: 20px; flex-wrap: wrap; font-size: 0.85em; color: #666; }
        .footer {
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            color: #666;
            border-top: 1px solid rgba(255,255,255,0.1);
        }
        .footer code {
            background: rgba(0,0,0,0.3);
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 商机发现 Skills 推荐</h1>
        <p class="subtitle">生成时间: ${getDateString()} | 数据来源: ${isFallback ? '预设列表' : 'ClawHub API'}</p>
        ${fallbackNote}

        <div class="category">🔍 商机发现</div>
        ${skills.slice(0,3).map(s => `
        <div class="skill-card">
            <div class="skill-header">
                <span class="skill-name">${s.slug}</span>
                <span class="skill-owner">@${s.owner}</span>
            </div>
            <p class="skill-desc">${s.summary}</p>
            <div class="skill-meta">
                <span>📅 更新: ${s.updated}</span>
                <span>📦 版本: ${s.version}</span>
            </div>
        </div>
        `).join('')}

        <div class="category">📊 市场分析</div>
        ${skills.slice(3,6).map(s => `
        <div class="skill-card">
            <div class="skill-header">
                <span class="skill-name">${s.slug}</span>
                <span class="skill-owner">@${s.owner}</span>
            </div>
            <p class="skill-desc">${s.summary}</p>
            <div class="skill-meta">
                <span>📅 更新: ${s.updated}</span>
                <span>📦 版本: ${s.version}</span>
            </div>
        </div>
        `).join('')}

        <div class="category">💼 商业战略</div>
        ${skills.slice(6,9).map(s => `
        <div class="skill-card">
            <div class="skill-header">
                <span class="skill-name">${s.slug}</span>
                <span class="skill-owner">@${s.owner}</span>
            </div>
            <p class="skill-desc">${s.summary}</p>
            <div class="skill-meta">
                <span>📅 更新: ${s.updated}</span>
                <span>📦 版本: ${s.version}</span>
            </div>
        </div>
        `).join('')}

        <div class="category">🎯 获客引流</div>
        ${skills.slice(9,12).map(s => `
        <div class="skill-card">
            <div class="skill-header">
                <span class="skill-name">${s.slug}</span>
                <span class="skill-owner">@${s.owner}</span>
            </div>
            <p class="skill-desc">${s.summary}</p>
            <div class="skill-meta">
                <span>📅 更新: ${s.updated}</span>
                <span>📦 版本: ${s.version}</span>
            </div>
        </div>
        `).join('')}

        <div class="category">🛠️ 创业工具</div>
        ${skills.slice(12,15).map(s => `
        <div class="skill-card">
            <div class="skill-header">
                <span class="skill-name">${s.slug}</span>
                <span class="skill-owner">@${s.owner}</span>
            </div>
            <p class="skill-desc">${s.summary}</p>
            <div class="skill-meta">
                <span>📅 更新: ${s.updated}</span>
                <span>📦 版本: ${s.version}</span>
            </div>
        </div>
        `).join('')}

        <div class="footer">
            <p>💡 安装命令: <code>px clawhub@latest install &lt;skill-name&gt;</code></p>
            <p>📦 数据来源: <a href="https://clawhub.com" style="color:#00d4ff;">ClawHub Skill Market</a></p>
        </div>
    </div>
</body>
</html>`;

  const htmlPath = path.join(WORKSPACE, `${outputName}.html`);
  fs.writeFileSync(htmlPath, html, 'utf8');
  console.log(`[INFO] HTML report saved: ${htmlPath}`);
  return htmlPath;
}

// 启动 Chromium
function startBrowser(url) {
  return new Promise((resolve, reject) => {
    console.log(`[INFO] Starting Chromium with debug port...`);
    
    // 先杀掉之前的 chromium 进程
    try {
      exec('pkill -f "chromium.*remote-debugging" 2>/dev/null || true');
    } catch (e) {}
    
    const proc = spawn('chromium-browser', [
      '--remote-debugging-port=9222',
      '--no-first-run',
      '--no-default-browser-check',
      url
    ], {
      env: { ...process.env, DISPLAY: ':0' },
      detached: true,
      stdio: 'ignore'
    });
    
    proc.unref();
    
    // 等待浏览器启动
    setTimeout(() => {
      console.log(`[INFO] Chromium started`);
      resolve();
    }, 3000);
  });
}

// 截屏
async function takeScreenshot(outputPath) {
  console.log(`[INFO] Taking screenshot...`);
  
  const browser = await puppeteer.connect({
    browserURL: 'http://localhost:9222',
    defaultViewport: null
  });
  
  const pages = await browser.pages();
  const page = pages[0];
  
  // 获取页面尺寸
  const dimensions = await page.evaluate(() => ({
    width: document.documentElement.scrollWidth,
    height: document.documentElement.scrollHeight
  }));
  
  console.log(`[INFO] Page dimensions: ${dimensions.width}x${dimensions.height}`);
  
  // 设置视口
  await page.setViewport({ 
    width: dimensions.width, 
    height: dimensions.height 
  });
  
  // 等待渲染
  await new Promise(resolve => setTimeout(resolve, 2000));
  
  // 截取全页
  await page.screenshot({
    path: outputPath,
    fullPage: true
  });
  
  await browser.disconnect();
  console.log(`[INFO] Screenshot saved: ${outputPath}`);
}

// 主函数
async function main() {
  const args = process.argv.slice(2);
  const query = args[0] || 'opportunity';
  const outputName = args[1] || `商业发现-${getDateString()}`;
  
  console.log(`[INFO] === Business Opportunity Skills Report ===`);
  console.log(`[INFO] Query: ${query}`);
  console.log(`[INFO] Output: ${outputName}`);
  
  // 1. 尝试搜索 Skills
  let skillSlugs = searchSkills(query);
  let skills = [];
  let isFallback = false;
  
  // 2. 如果搜索失败或无结果，使用预设数据
  if (skillSlugs.length === 0) {
    console.log(`[INFO] Using fallback data`);
    skills = [...FALLBACK_SKILLS];
    isFallback = true;
  } else {
    // 3. 获取详情
    console.log(`[INFO] Fetching details for ${skillSlugs.length} skills...`);
    for (const s of skillSlugs) {
      const info = inspectSkill(s.slug);
      if (info) {
        skills.push(info);
      }
    }
    
    // 如果获取详情后为空，使用预设
    if (skills.length === 0) {
      console.log(`[WARN] No details fetched, using fallback`);
      skills = [...FALLBACK_SKILLS];
      isFallback = true;
    }
  }
  
  console.log(`[INFO] Total skills to display: ${skills.length}`);
  
  // 4. 生成 HTML
  const htmlPath = generateReport(skills, outputName, isFallback);
  
  // 5. 创建 output 目录
  if (!fs.existsSync(OUTPUT_DIR)) {
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  }
  
  // 6. 启动浏览器
  await startBrowser(`file://${htmlPath}`);
  
  // 7. 截屏
  const screenshotPath = path.join(OUTPUT_DIR, `${outputName}.jpg`);
  await takeScreenshot(screenshotPath);
  
  console.log(`[INFO] === Done! ===`);
  console.log(`[INFO] HTML: ${htmlPath}`);
  console.log(`[INFO] Screenshot: ${screenshotPath}`);
}

main().catch(e => {
  console.error('[ERROR]', e);
  process.exit(1);
});
