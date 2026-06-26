#!/usr/bin/env node
/**
 * AI Earnings Tracker - 科技/AI财报追踪 v2.3
 *
 * 功能：
 * 1. 搜索财报日历
 * 2. 获取公司财报新闻
 * 3. 生成财报摘要
 * 4. 追踪公司列表管理
 * 5. 批量检查财报动态
 * 6. JSON输出支持
 * 7. 中文翻译输出
 *
 * 数据源: Tavily AI Search API
 * 翻译: GLM-4 API
 *
 * Usage:
 *   node fetch-earnings.js calendar    # 获取本周财报日历
 *   node fetch-earnings.js news NVDA   # 获取 NVDA 财报新闻
 *   node fetch-earnings.js summary NVDA # 生成 NVDA 财报摘要
 *   node fetch-earnings.js track NVDA,AAPL  # 追踪公司
 *   node fetch-earnings.js untrack NVDA     # 取消追踪
 *   node fetch-earnings.js list        # 显示追踪列表
 *   node fetch-earnings.js check       # 检查追踪公司财报动态
 */

const fs = require('fs');
const path = require('path');

const TRACK_FILE = path.join(__dirname, '.tracked-companies.json');

// 追踪的公司列表
const DEFAULT_COMPANIES = [
  { symbol: 'NVDA', name: 'NVIDIA', sector: 'AI/GPU' },
  { symbol: 'AAPL', name: 'Apple', sector: 'Consumer Tech' },
  { symbol: 'MSFT', name: 'Microsoft', sector: 'Cloud/AI' },
  { symbol: 'GOOGL', name: 'Google', sector: 'AI/Search' },
  { symbol: 'AMZN', name: 'Amazon', sector: 'Cloud/E-commerce' },
  { symbol: 'META', name: 'Meta', sector: 'Social/AI' },
  { symbol: 'TSLA', name: 'Tesla', sector: 'EV/AI' },
  { symbol: 'AMD', name: 'AMD', sector: 'AI/GPU' },
  { symbol: 'PLTR', name: 'Palantir', sector: 'AI/Data' },
  { symbol: 'CRM', name: 'Salesforce', sector: 'Enterprise AI' }
];

const action = process.argv[2] || 'help';
const symbolArg = process.argv[3]?.toUpperCase() || '';
const useJson = process.argv.includes('--json');
const verbose = process.argv.includes('-v') || process.argv.includes('--verbose');
const noTranslate = process.argv.includes('--no-translate');

// JSON输出辅助
let jsonOutput = { action, success: false, data: null, error: null };

function output(text) {
  if (!useJson) console.log(text);
}

function outputJson() {
  if (useJson) {
    console.log(JSON.stringify(jsonOutput, null, 2));
  }
}

// 加载追踪列表
function loadTracked() {
  if (fs.existsSync(TRACK_FILE)) {
    return JSON.parse(fs.readFileSync(TRACK_FILE, 'utf8'));
  }
  return [...DEFAULT_COMPANIES];
}

// 保存追踪列表
function saveTracked(companies) {
  fs.writeFileSync(TRACK_FILE, JSON.stringify(companies, null, 2));
}

// 添加公司到追踪列表
function trackCompanies(symbols) {
  const tracked = loadTracked();
  const newSymbols = symbols.split(',').map(s => s.trim().toUpperCase());
  const added = [];

  for (const symbol of newSymbols) {
    if (!tracked.find(c => c.symbol === symbol)) {
      tracked.push({ symbol, name: symbol, sector: 'Unknown', addedAt: new Date().toISOString() });
      added.push(symbol);
      output(`✅ 已添加 ${symbol} 到追踪列表`);
    } else {
      output(`ℹ️ ${symbol} 已在追踪列表中`);
    }
  }

  saveTracked(tracked);
  jsonOutput.success = true;
  jsonOutput.data = { added, total: tracked.length };
  return tracked;
}

// 取消追踪公司
function untrackCompanies(symbols) {
  let tracked = loadTracked();
  const removeSymbols = symbols.split(',').map(s => s.trim().toUpperCase());
  const removed = [];

  for (const symbol of removeSymbols) {
    const idx = tracked.findIndex(c => c.symbol === symbol);
    if (idx !== -1) {
      tracked.splice(idx, 1);
      removed.push(symbol);
      output(`✅ 已移除 ${symbol}`);
    } else {
      output(`ℹ️ ${symbol} 不在追踪列表中`);
    }
  }

  saveTracked(tracked);
  jsonOutput.success = true;
  jsonOutput.data = { removed, total: tracked.length };
  return tracked;
}

// 显示帮助
function showHelp() {
  output(`
🦞 AI Earnings Tracker v2.3 - 科技/AI财报追踪

Usage:
  node fetch-earnings.js calendar       获取本周财报日历
  node fetch-earnings.js news NVDA      获取 NVDA 财报新闻
  node fetch-earnings.js summary NVDA   生成 NVDA 财报摘要
  node fetch-earnings.js track NVDA,AAPL   追踪多个公司
  node fetch-earnings.js untrack NVDA      取消追踪
  node fetch-earnings.js list           显示追踪列表
  node fetch-earnings.js check          检查追踪公司财报动态

Options:
  --json         输出 JSON 格式
  -v             详细输出
  --no-translate 不翻译（保持英文）
`);
}

// Tavily API 搜索
async function tavilySearch(query, options = {}) {
  const apiKey = (process.env.TAVILY_API_KEY ?? '').trim();
  if (!apiKey) {
    throw new Error('Missing TAVILY_API_KEY environment variable');
  }

  const body = {
    api_key: apiKey,
    query: query,
    search_depth: options.deep ? 'advanced' : 'basic',
    topic: options.topic || 'general',
    max_results: options.maxResults || 5,
    include_answer: true,
    include_raw_content: false,
  };

  if (options.topic === 'news' && options.days) {
    body.days = options.days;
  }

  const resp = await fetch('https://api.tavily.com/search', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });

  if (!resp.ok) {
    const text = await resp.text().catch(() => '');
    throw new Error(`Tavily Search failed (${resp.status}): ${text}`);
  }

  return await resp.json();
}

// GLM API 翻译
async function translateToChinese(text) {
  if (!text || noTranslate) return text;
  
  // 检测是否已经是中文
  if (/[\u4e00-\u9fa5]/.test(text) && !/[a-zA-Z]{10,}/.test(text)) {
    return text;
  }

  const apiKey = (process.env.ZAI_API_KEY ?? process.env.OPENAI_API_KEY ?? '').trim();
  if (!apiKey) {
    return text; // 无 API Key 则返回原文
  }

  try {
    const resp = await fetch('https://open.bigmodel.cn/api/paas/v4/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`
      },
      body: JSON.stringify({
        model: 'glm-4-flash',
        messages: [
          {
            role: 'system',
            content: '你是一个专业的财经翻译助手。将英文财经新闻翻译成简洁、专业的中文。保持专业术语的准确性，如 EPS、YoY、Revenue 等可保留英文或使用标准中文译法。翻译要简洁，不要添加额外解释。'
          },
          {
            role: 'user',
            content: `请将以下英文财经内容翻译成中文：\n\n${text}`
          }
        ],
        temperature: 0.3,
        max_tokens: 1000
      })
    });

    if (!resp.ok) {
      if (verbose) output(` ⚠️ 翻译失败: ${resp.status}`);
      return text;
    }

    const data = await resp.json();
    return data.choices?.[0]?.message?.content?.trim() || text;
  } catch (error) {
    if (verbose) output(` ⚠️ 翻译错误: ${error.message}`);
    return text;
  }
}

// 批量翻译（带缓存和节流）
const translateCache = new Map();
async function translateBatch(texts) {
  const results = [];
  for (const text of texts) {
    if (translateCache.has(text)) {
      results.push(translateCache.get(text));
    } else {
      const translated = await translateToChinese(text);
      translateCache.set(text, translated);
      results.push(translated);
      // 节流：避免 API 限流
      await new Promise(r => setTimeout(r, 100));
    }
  }
  return results;
}

// 搜索财报新闻
async function searchEarningsNews(symbol) {
  const query = `${symbol} earnings report 2026 Q1 Q2 financial results`;
  try {
    const data = await tavilySearch(query, {
      topic: 'news',
      days: 30,
      maxResults: 5,
      deep: false
    });

    const results = (data.results || []).map(r => ({
      title: r.title?.trim() || '',
      desc: r.content?.trim() || '',
      link: r.url || '',
      score: r.score
    }));

    return {
      answer: data.answer || null,
      results: results.filter(r => r.title)
    };
  } catch (error) {
    if (verbose) output(` ⚠️ ${symbol} 搜索失败: ${error.message}`);
    return { answer: null, results: [] };
  }
}

// 提取财报关键数据
function extractEarningsData(newsItems, symbol) {
  const allText = newsItems.map(n => `${n.title} ${n.desc}`).join(' ');

  const patterns = {
    revenue: /(?:营收|revenue|收入)[\s:]*\$?([\d.]+)\s*[BMK]?/i,
    profit: /(?:净利润|net income|profit)[\s:]*\$?([\d.]+)\s*[BMK]?/i,
    eps: /EPS[\s:]*\$?([\d.]+)/i,
    growth: /(?:同比|YoY|增长)[\s:+-]*([\d.]+)%/i
  };

  const data = {};
  for (const [key, pattern] of Object.entries(patterns)) {
    const match = allText.match(pattern);
    data[key] = match ? match[1] : null;
  }

  return data;
}

// 生成财报摘要
async function generateSummary(symbol, newsData) {
  const { answer, results } = newsData;
  const data = extractEarningsData(results, symbol);

  let summary = `# ${symbol} 财报摘要\n\n`;

  if (answer) {
    const translatedAnswer = await translateToChinese(answer);
    summary += `## 🤖 AI 摘要\n${translatedAnswer}\n\n`;
  }

  summary += `## 📈 核心数据\n`;
  if (data.revenue) summary += `- 营收: $${data.revenue}B\n`;
  if (data.profit) summary += `- 净利润: $${data.profit}B\n`;
  if (data.eps) summary += `- EPS: $${data.eps}\n`;
  if (data.growth) summary += `- 同比增长: ${data.growth}%\n`;
  if (!data.revenue && !data.profit && !data.eps) {
    summary += `- 暂无详细数据，请查看新闻摘要\n`;
  }

  summary += `\n## 📰 相关新闻\n`;
  for (let i = 0; i < Math.min(5, results.length); i++) {
    const item = results[i];
    const translatedTitle = await translateToChinese(item.title);
    summary += `${i+1}. ${translatedTitle}\n`;
    if (item.desc) {
      const translatedDesc = await translateToChinese(item.desc.substring(0, 150));
      summary += `   ${translatedDesc}...\n`;
    }
  }

  return summary;
}

// 主程序
(async () => {
  output('🦞 AI Earnings Tracker v2.3\n');

  // 不需要 API 的操作
  if (action === 'help' || action === '--help' || action === '-h') {
    showHelp();
    jsonOutput.success = true;
    outputJson();
    process.exit(0);
  }

  if (action === 'list') {
    const tracked = loadTracked();
    output('📋 追踪公司列表:\n');
    output('| 序号 | 股票代码 | 公司名称 | 行业 |');
    output('|------|---------|---------|------|');
    tracked.forEach((c, i) => {
      output(`| ${i+1} | ${c.symbol} | ${c.name} | ${c.sector} |`);
    });
    jsonOutput.success = true;
    jsonOutput.data = tracked;
    outputJson();
    process.exit(0);
  }

  if (action === 'track') {
    if (!symbolArg) {
      output('❌ 请提供股票代码，如: node fetch-earnings.js track NVDA,AAPL');
      jsonOutput.error = 'Missing symbol argument';
      outputJson();
      process.exit(1);
    }
    trackCompanies(symbolArg);
    outputJson();
    process.exit(0);
  }

  if (action === 'untrack') {
    if (!symbolArg) {
      output('❌ 请提供股票代码，如: node fetch-earnings.js untrack NVDA');
      jsonOutput.error = 'Missing symbol argument';
      outputJson();
      process.exit(1);
    }
    untrackCompanies(symbolArg);
    outputJson();
    process.exit(0);
  }

  // 需要 API 的操作
  try {
    if (action === 'calendar') {
      output('📅 获取本周财报日历...\n');

      const data = await tavilySearch('US tech earnings calendar February 2026 NVDA AAPL MSFT GOOGL', {
        topic: 'news',
        days: 7,
        maxResults: 10
      });

      output('📋 本周财报日历:\n');

      if (data.answer) {
        const translated = await translateToChinese(data.answer);
        output(`🤖 AI 摘要:\n${translated}\n`);
      }

      for (const item of (data.results || [])) {
        const translatedTitle = await translateToChinese(item.title);
        output(`• ${translatedTitle}`);
        if (item.content) {
          const translatedContent = await translateToChinese(item.content.substring(0, 100));
          output(`  ${translatedContent}...\n`);
        }
      }

      jsonOutput.success = true;
      jsonOutput.data = data;

    } else if (action === 'news') {
      if (!symbolArg) {
        output('❌ 请提供股票代码，如: node fetch-earnings.js news NVDA');
        jsonOutput.error = 'Missing symbol argument';
        process.exit(1);
      }

      output(`📰 获取 ${symbolArg} 财报新闻...\n`);

      const newsData = await searchEarningsNews(symbolArg);

      output(`📋 ${symbolArg} 财报新闻:\n`);

      if (newsData.answer) {
        const translated = await translateToChinese(newsData.answer);
        output(`🤖 AI 摘要:\n${translated}\n`);
      }

      for (const item of newsData.results) {
        const scoreStr = item.score ? ` (相关度: ${(item.score * 100).toFixed(0)}%)` : '';
        const translatedTitle = await translateToChinese(item.title);
        output(`${translatedTitle}${scoreStr}`);
        if (item.desc) {
          const translatedDesc = await translateToChinese(item.desc.substring(0, 150));
          output(`  ${translatedDesc}\n`);
        }
      }

      jsonOutput.success = true;
      jsonOutput.data = newsData;

    } else if (action === 'summary') {
      if (!symbolArg) {
        output('❌ 请提供股票代码，如: node fetch-earnings.js summary NVDA');
        jsonOutput.error = 'Missing symbol argument';
        process.exit(1);
      }

      output(`📊 生成 ${symbolArg} 财报摘要...\n`);

      const newsData = await searchEarningsNews(symbolArg);
      const summary = await generateSummary(symbolArg, newsData);

      output(summary);

      jsonOutput.success = true;
      jsonOutput.data = { summary, news: newsData.results.slice(0, 5) };

    } else if (action === 'check') {
      const tracked = loadTracked();
      const total = tracked.length;

      output(`🔍 检查 ${total} 家追踪公司的财报动态...\n`);
      output('进度: ');

      const allNews = [];

      for (let i = 0; i < total; i++) {
        const company = tracked[i];
        process.stdout.write(`\r[${i+1}/${total}] 检查 ${company.symbol}...`);

        const newsData = await searchEarningsNews(company.symbol);

        if (newsData.results.length > 0) {
          allNews.push({
            symbol: company.symbol,
            name: company.name,
            sector: company.sector,
            answer: newsData.answer,
            news: newsData.results.slice(0, 3)
          });
        }
      }

      output('\n\n📊 追踪公司财报动态:\n');

      for (const item of allNews) {
        output(`【${item.symbol} - ${item.name}】`);
        
        for (let i = 0; i < item.news.length; i++) {
          const n = item.news[i];
          const scoreStr = n.score ? ` (相关度: ${(n.score * 100).toFixed(0)}%)` : '';
          const translatedTitle = await translateToChinese(n.title);
          output(`  ${i+1}. ${translatedTitle}${scoreStr}`);
          if (n.desc) {
            const translatedDesc = await translateToChinese(n.desc.substring(0, 80));
            output(`     ${translatedDesc}...`);
          }
        }
        output('');
      }

      jsonOutput.success = true;
      jsonOutput.data = allNews;

    } else {
      showHelp();
    }

  } catch (error) {
    output(`\n❌ 错误: ${error.message}`);
    jsonOutput.error = error.message;
  }

  output('\n✅ 完成');
  outputJson();
})();
