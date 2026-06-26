#!/usr/bin/env node
/**
 * Claw Search V7 - 智能语言适配版
 * 根据查询语言自动匹配最佳搜索引擎，综合所有结果智能排序
 */

const puppeteer = require('puppeteer-core');
const http = require('http');
const fs = require('fs');
const crypto = require('crypto');

const PORT = 8093;

// ============ 加载免费 API 数据库 ============
let freeAPIs = [];
try {
  const apiData = fs.readFileSync('/root/.openclaw/workspace/skills/claw-search/data/free-apis.json', 'utf8');
  freeAPIs = JSON.parse(apiData).apis || [];
  console.log(`[Data] Loaded ${freeAPIs.length} free APIs`);
} catch(e) {
  console.log('[Data] No free APIs loaded');
}

// 匹配免费 API
function matchFreeAPIs(query) {
  const queryLower = query.toLowerCase();
  const keywords = queryLower.split(/\s+/).filter(w => w.length > 1);
  
  // 计算匹配分数
  const scored = freeAPIs.map(api => {
    let score = 0;
    const apiText = `${api.name} ${api.description} ${(api.tags || []).join(' ')}`.toLowerCase();
    
    keywords.forEach(kw => {
      // 全词匹配（最优先）
      if (apiText.includes(` ${kw} `) || apiText.includes(` ${kw}`) || apiText.includes(`${kw} `)) {
        score += 100;
      }
      // 包含匹配
      if (apiText.includes(kw)) {
        score += 50;
      }
      // 标题匹配
      if (api.name.toLowerCase().includes(kw)) {
        score += 30;
      }
      // 描述匹配
      if (api.description.toLowerCase().includes(kw)) {
        score += 10;
      }
      // 标签匹配
      (api.tags || []).forEach(tag => {
        if (tag.toLowerCase().includes(kw)) score += 20;
      });
    });
    
    return { ...api, score };
  });
  
  // 按分数排序，返回前3个
  return scored.filter(a => a.score > 0).sort((a, b) => b.score - a.score).slice(0, 3).map(({ score, ...api }) => api);
}

// ============ 浏览器池 ============
class BrowserPool {
  constructor(size = 3) { this.size = size; this.browsers = []; this.queue = []; this.using = 0; }
  
  async acquire() {
    if (this.browsers.length > 0) { const browser = this.browsers.pop(); this.using++; return browser; }
    if (this.using < this.size) {
      this.using++;
      try {
        const browser = await puppeteer.launch({
          executablePath: '/usr/bin/chromium-browser',
          headless: 'new',
          args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--disable-gpu']
        });
        return browser;
      } catch(e) { this.using--; throw e; }
    }
    return new Promise(resolve => this.queue.push(resolve));
  }
  
  async release(browser) {
    this.using--;
    if (this.queue.length > 0) { const resolve = this.queue.shift(); this.using++; resolve(browser); }
    else if (this.browsers.length < this.size - 1) { this.browsers.push(browser); }
    else { try { await browser.close(); } catch(e) {} }
  }
  
  async closeAll() { for (const browser of this.browsers) { try { await browser.close(); } catch(e) {} } this.browsers = []; }
}

const browserPool = new BrowserPool(3);

// ============ 缓存 ============
class SearchCache {
  constructor() { this.cache = new Map(); this.stats = { hits: 0, misses: 0 }; this.TTL = 15 * 60 * 1000; }
  
  get(key) {
    const item = this.cache.get(key);
    if (item && Date.now() - item.ts < this.TTL) { this.stats.hits++; return item.data; }
    this.stats.misses++; return null;
  }
  
  set(key, data) {
    this.cache.set(key, { data, ts: Date.now() });
    if (this.cache.size > 2000) {
      const now = Date.now();
      for (const [k, v] of this.cache) { if (now - v.ts > this.TTL) this.cache.delete(k); }
    }
  }
  
  getStats() {
    const total = this.stats.hits + this.stats.misses;
    return { hits: this.stats.hits, misses: this.stats.misses, hitRate: total ? (this.stats.hits / total * 100).toFixed(1) + '%' : '0%', size: this.cache.size };
  }
}

const cache = new SearchCache();

// ============ 统计 ============
const stats = { total_calls: 0, today_calls: 0, last_date: new Date().toDateString(), countries: {}, sources: {}, latency_sum: 0, latency_count: 0 };

function saveStats() { try { fs.writeFileSync('/tmp/claw-search-stats.json', JSON.stringify(stats)); } catch(e) {} }

function loadStats() {
  try { Object.assign(stats, JSON.parse(fs.readFileSync('/tmp/claw-search-stats.json', 'utf8'))); if (stats.last_date !== new Date().toDateString()) { stats.today_calls = 0; stats.last_date = new Date().toDateString(); } } catch(e) {}
}
loadStats();

// ============ 搜索历史 ============
const searchHistory = { data: [], maxSize: 100, add(query) { const idx = this.data.indexOf(query); if (idx > -1) this.data.splice(idx, 1); this.data.unshift(query); if (this.data.length > this.maxSize) this.data.pop(); }, getRecent(count = 10) { return this.data.slice(0, count); }, getSuggestions(prefix) { if (!prefix || prefix.length < 2) return []; return this.data.filter(q => q.toLowerCase().includes(prefix.toLowerCase())).slice(0, 5); } };

// ============ 语言检测 ============
function detectLanguage(query) {
  const patterns = { 
    zh: /[\u4e00-\u9fa5]/, 
    ko: /[\uac00-\ud7af]/, 
    ja: /[\u3040-\u309f\u30a0-\u30ff]/,
    ru: /[\u0400-\u04ff]/,
    ar: /[\u0600-\u06ff]/
  };
  for (const [lang, re] of Object.entries(patterns)) { if (re.test(query)) return lang; }
  return 'en';
}

// 意图检测
function detectIntent(query) {
  const lower = query.toLowerCase();
  const intents = [
    { name: 'tutorial', keywords: ['怎么', '如何', 'what is', 'how to', 'tutorial', '教程', '学习', '入门', 'guide', 'learn'] },
    { name: 'news', keywords: ['最新', 'news', '2024', '2025', '2026', '今日', '今天', 'breaking'] },
    { name: 'official', keywords: ['官网', 'official', 'homepage', '官方网站', '官网首页'] },
    { name: 'download', keywords: ['下载', 'download', 'free', '安装'] },
    { name: 'price', keywords: ['价格', 'price', '多少钱', 'cost', '价格表'] }
  ];
  for (const intent of intents) {
    for (const kw of intent.keywords) { if (lower.includes(kw)) return intent.name; }
  }
  return 'general';
}

// ============ 搜索 Bing - 根据语言选择版本 ============
async function searchBing(query, count = 10) {
  const lang = detectLanguage(query);
  const intent = detectIntent(query);
  const langMap = { zh: 'zh-CN', en: 'en-US', ja: 'ja-JP', ko: 'ko-KR', ru: 'ru-RU', ar: 'ar-SA' };
  
  let browser; 
  const startTime = Date.now();
  
  try {
    browser = await browserPool.acquire();
    const page = await browser.newPage();
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36');
    
    // 根据意图增强搜索词
    let searchQuery = query;
    if (intent === 'tutorial' && lang !== 'zh') searchQuery += ' tutorial';
    if (intent === 'news') searchQuery += ' latest news';
    
    // 根据语言选择搜索引擎
    // 中文 -> cn.bing.com (国内版)
    // 其他 -> www.bing.com (国际版)
    const langCode = langMap[lang] || 'en-US';
    const isChinese = lang === 'zh';
    const bingDomain = isChinese ? 'https://cn.bing.com' : 'https://www.bing.com';
    const domainName = isChinese ? 'Bing CN' : 'Bing';
    
    console.log(`[${domainName}] Query: "${query}", Lang: ${langCode}`);
    
    const url = `${bingDomain}/search?q=${encodeURIComponent(searchQuery)}&count=${count}&setlang=${langCode}`;
    await page.goto(url, { waitUntil: 'networkidle2', timeout: 20000 });

    const results = await page.evaluate((max, isCN) => {
      const items = document.querySelectorAll('li.b_algo');
      const data = [];
      items.forEach((item) => {
        if (data.length >= max) return;
        const titleEl = item.querySelector('h2 a');
        const descEl = item.querySelector('p');
        const dateEl = item.querySelector('span.news_dt');
        if (titleEl && titleEl.href) {
          data.push({ 
            title: titleEl.textContent?.trim() || '', 
            url: titleEl.href || '', 
            description: descEl?.textContent?.trim() || '', 
            published_date: dateEl?.textContent?.trim() || '', 
            source: isCN ? 'Bing CN' : 'Bing' 
          });
        }
      });
      return data;
    }, count, isChinese);
    
    return { results, latency: Date.now() - startTime };
  } catch (e) { 
    console.error('[Bing] Error:', e.message);
    return { results: [], latency: Date.now() - startTime }; 
  }
  finally { if (browser) await browserPool.release(browser); }
}

// ============ 内容提取 ============
async function extractContent(url) {
  let browser;
  try {
    browser = await browserPool.acquire();
    const page = await browser.newPage();
    await page.setUserAgent('Mozilla/5.0');
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 10000 });
    
    const content = await page.evaluate(() => {
      const remove = ['script', 'style', 'nav', 'footer', 'header', 'aside', 'iframe', 'noscript', '.ad', '.comment'];
      remove.forEach(sel => { try { document.querySelectorAll(sel).forEach(el => el.remove()); } catch(e) {} });
      
      const article = document.querySelector('article') || document.querySelector('main') || document.querySelector('.content') || document.body;
      const title = document.querySelector('h1')?.textContent?.trim() || document.title;
      
      const paragraphs = article?.querySelectorAll('p') || [];
      const text = Array.from(paragraphs).map(p => p.textContent?.trim()).filter(t => t && t.length > 30).slice(0, 15).join('\n\n');
      
      return { title, content: text };
    });
    
    return content;
  } catch (e) { return { error: e.message }; }
  finally { if (browser) await browserPool.release(browser); }
}

// ============ 智能排序 ============
function smartRank(results, query, lang, intent) {
  const keywords = query.toLowerCase().split(/\s+/).filter(w => w.length > 1);
  const seen = new Set();
  
  // 简单去重 - 只基于完整URL
  const uniqueResults = results.filter(r => {
    if (!r.url || !r.url.startsWith('http')) return false;
    if (seen.has(r.url)) return false;
    seen.add(r.url);
    return true;
  });
  
  // 评分
  return uniqueResults.map(r => {
    let score = 0;
    const text = `${r.title || ''} ${r.description || ''} ${r.url || ''}`.toLowerCase();
    
    // 关键词匹配
    keywords.forEach(kw => {
      if (r.title?.toLowerCase().includes(kw)) score += 20;
      else if (text.includes(kw)) score += 8;
    });
    
    // 来源权重
    score += { Bing: 15, Yahoo: 10, DuckDuckGo: 8 }[r.source] || 5;
    
    // 意图匹配
    if (intent === 'tutorial') {
      if (r.title.includes('教程') || r.title.includes('tutorial') || r.title.includes('入门') || r.title.includes('Guide')) score += 15;
    }
    if (intent === 'news' && r.published_date) score += 12;
    if (intent === 'official' && r.url.includes('official')) score += 10;
    
    // 语言匹配
    if (lang === 'zh' && /[\u4e00-\u9fa5]/.test(r.title)) score += 10;
    if (lang === 'ja' && /[\u3040-\u309f\u30a0-\u30ff]/.test(r.title)) score += 10;
    if (lang === 'ko' && /[\uac00-\ud7af]/.test(r.title)) score += 10;
    
    if (r.published_date) score += 5;
    
    return { ...r, score: Math.min(score, 150), intent, language: lang };
  }).sort((a, b) => b.score - a.score);
}

// ============ HTTP 服务器 ============
const server = http.createServer(async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  
  if (req.method === 'OPTIONS') { res.writeHead(200); res.end(); return; }

  const url = req.url.split('?')[0];
  const queryParams = new URLSearchParams(req.url.split('?')[1] || '');
  
  if (url === '/health') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ status: 'ok', service: 'Claw Search V7', version: '7.0.0', cache: cache.getStats() }));
    return;
  }
  
  if (url === '/api/stats') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      total_calls: stats.total_calls, today_calls: stats.today_calls,
      avg_latency: stats.latency_count ? Math.round(stats.latency_sum / stats.latency_count) + 'ms' : 'N/A',
      countries: Object.entries(stats.countries).map(([c, n]) => ({ code: c, count: n })).sort((a, b) => b.count - a.count).slice(0, 10),
      sources: Object.entries(stats.sources).map(([s, n]) => ({ source: s, count: n })).sort((a, b) => b.count - a.count),
      cache: cache.getStats()
    }));
    return;
  }
  
  // 免费 API 列表
  if (url === '/api/free-apis') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      count: freeAPIs.length,
      apis: freeAPIs
    }));
    return;
  }
  
  // 搜索免费 API
  if (url === '/api/search-apis' && req.method === 'POST') {
    let body = ''; req.on('data', chunk => body += chunk);
    req.on('end', () => {
      try {
        const data = JSON.parse(body);
        const query = data.query || '';
        const matched = matchFreeAPIs(query);
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ query, count: matched.length, apis: matched }));
      } catch(e) {
        res.writeHead(500, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: e.message }));
      }
    });
    return;
  }
  
  if (url === '/api/suggest' && req.method === 'GET') {
    const prefix = queryParams.get('q') || queryParams.get('prefix') || '';
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ suggestions: searchHistory.getSuggestions(prefix) }));
    return;
  }
  
  if (url === '/api/history' && req.method === 'GET') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ history: searchHistory.getRecent(20) }));
    return;
  }
  
  if (url === '/api/extract' && req.method === 'POST') {
    let body = ''; req.on('data', chunk => body += chunk);
    req.on('end', async () => {
      try {
        const data = JSON.parse(body);
        if (!data.url) throw new Error('url is required');
        const content = await extractContent(data.url);
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ url: data.url, ...content }));
      } catch (e) { res.writeHead(500, { 'Content-Type': 'application/json' }); res.end(JSON.stringify({ error: e.message })); }
    });
    return;
  }
  
  if ((url === '/api/search' || url === '/search') && req.method === 'POST') {
    let body = ''; req.on('data', chunk => body += chunk);
    req.on('end', async () => {
      try {
        const data = JSON.parse(body);
        const query = data.query || '';
        const count = Math.min(parseInt(data.count) || 10, 20);
        
        if (!query) throw new Error('query is required');
        
        // 记录历史
        searchHistory.add(query);
        
        // 更新统计
        stats.total_calls++; stats.today_calls++; stats.countries['CN'] = (stats.countries['CN'] || 0) + 1;
        saveStats();
        
        // 检查缓存
        const cacheKey = crypto.createHash('md5').update(`${query}-${count}`).digest('hex');
        const cached = cache.get(cacheKey);
        if (cached) { 
          res.writeHead(200, { 'Content-Type': 'application/json' }); 
          res.end(JSON.stringify({ ...cached, cached: true })); 
          return; 
        }
        
        // 检测语言和意图
        const lang = detectLanguage(query);
        const intent = detectIntent(query);
        
        console.log(`[Search] "${query}" [${lang}] intent:${intent}`);
        
        // 单引擎搜索 - 更稳定
        const { results, latency } = await searchBing(query, count);
        
        stats.sources['Bing'] = (stats.sources['Bing'] || 0) + 1;
        stats.latency_sum += latency;
        stats.latency_count++;
        
        // 智能排序
        const rankedResults = smartRank(results, query, lang, intent);
        
        // 匹配免费 API
        const matchedAPIs = matchFreeAPIs(query);
        
        const response = { 
          query, 
          count: rankedResults.length, 
          language: lang, 
          intent, 
          latency: latency + 'ms', 
          results: rankedResults,
          freeApis: matchedAPIs,
          cached: false 
        };
        
        cache.set(cacheKey, response);
        
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(response));
      } catch (e) { 
        console.error('[Error]', e.message); 
        res.writeHead(500, { 'Content-Type': 'application/json' }); 
        res.end(JSON.stringify({ error: e.message })); 
      }
    });
    return;
  }
  
  res.writeHead(404); res.end();
});

process.on('SIGINT', async () => { await browserPool.closeAll(); process.exit(0); });

server.listen(PORT, '0.0.0.0', () => {
  console.log(`🦔 Claw Search V7 已启动: http://0.0.0.0:${PORT}`);
  console.log(`📡 智能语言适配 + 单引擎稳定搜索 + 意图识别`);
});
