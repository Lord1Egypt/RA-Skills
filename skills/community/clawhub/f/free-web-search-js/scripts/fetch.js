#!/usr/bin/env node
/**
 * free-web-search-js fetch.js v23.0
 *
 * 两层兜底 + 增强：
 *   1. 轻量 HTTP + cheerio（快，不启动浏览器）
 *      - 支持 JSON API 响应
 *      - 提取 JSON-LD / __NEXT_DATA__ 等嵌入数据
 *      - meta 标签兜底（og:description 等）
 *   2. Playwright headed（完整浏览器，支持 JS 渲染）
 * 多 URL 并行，打不开跳过
 */
import process from 'process';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { findBrowserExecutable, launchBrowser } from './playwright-support.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ENDPOINT_FILE = path.resolve(__dirname, '..', '.browser-endpoint');

const TIMEOUT = 35000;
const DEFAULT_MAX_LEN = 12000;

const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36';

// ==================== 浏览器复用 ====================
const HEARTBEAT_FILE = path.resolve(__dirname, '..', '.browser-heartbeat');
function touchHeartbeat() {
  try { fs.writeFileSync(HEARTBEAT_FILE, String(Date.now())); } catch {}
}

async function getBrowser() {
  try {
    const { chromium } = await import('playwright');
    const info = JSON.parse(fs.readFileSync(ENDPOINT_FILE, 'utf-8'));
    process.kill(info.pid, 0);
    touchHeartbeat();
    const browser = await chromium.connectOverCDP(info.wsEndpoint);
    return { browser, shared: true };
  } catch (e) {
    if (e.code === 'MODULE_NOT_FOUND') throw e;
  }
  const browser = await launchBrowser({ headless: true });
  return { browser, shared: false };
}

function releaseBrowser(browser, shared) {
  return shared ? browser.disconnect() : browser.close();
}

// 兼容性补丁：headless 下让 navigator.permissions.query('notifications') 与 Notification.permission 返回一致结果，避免页面脚本抛异常。
const PAGE_COMPAT_INIT = () => {
  const origQuery = window.navigator.permissions?.query;
  if (origQuery) {
    window.navigator.permissions.query = (params) => (
      params.name === 'notifications'
        ? Promise.resolve({ state: Notification.permission })
        : origQuery(params)
    );
  }
};

async function ensureDeps() {
  const missing = [];
  for (const m of ['cheerio', 'commander', 'iconv-lite', 'playwright']) {
    try { await import(m); } catch { missing.push(m); }
  }
  if (missing.length === 0) return;

  const skillRoot = path.resolve(__dirname, '..');
  console.error(`\n[X] free-web-search-js 缺少依赖: ${missing.join(', ')}\n`);
  console.error('   一键安装（推荐）:');
  console.error(`     cd "${skillRoot}" && bash scripts/setup.sh`);
  console.error('     # Windows: powershell -File scripts/setup.ps1\n');
  console.error('   手动安装:');
  console.error(`     cd "${skillRoot}" && npm install`);
  console.error('     npx playwright install chromium\n');
  console.error('   已有 Chrome（跳过 150MB 下载）:');
  console.error('     export CHROMIUM_EXECUTABLE_PATH=/path/to/chrome\n');
  console.error('   验证:');
  console.error('     node scripts/check-env.js\n');
  process.exit(1);
}

// ==================== 编码处理 ====================
async function decodeBuffer(buf, contentTypeHeader) {
  // 优先从 Content-Type 检测编码
  let charset = 'utf-8';
  if (contentTypeHeader) {
    const m = contentTypeHeader.match(/charset=([^\s;]+)/i);
    if (m) charset = m[1].toLowerCase();
  }

  if (charset === 'utf-8' || charset === 'utf8') {
    return buf.toString('utf-8');
  }
  if (charset === 'gbk' || charset === 'gb2312' || charset === 'gb18030') {
    try {
      const iconv = await import('iconv-lite');
      return iconv.default.decode(buf, 'gbk');
    } catch {
      try { return new TextDecoder('gbk').decode(buf); } catch {}
    }
  }
  // fallback: 尝试 utf-8，乱码多则试 gbk
  let text = buf.toString('utf-8');
  if ((text.match(/\ufffd/g) || []).length > 20) {
    try {
      const iconv = await import('iconv-lite');
      text = iconv.default.decode(buf, 'gbk');
    } catch {
      try { text = new TextDecoder('gbk').decode(buf); } catch {}
    }
  }
  return text;
}

// ==================== JSON 内容提取 ====================
function extractJsonContent(data, maxLen) {
  /** 从 JSON API 响应中提取有意义的文本 */
  const texts = [];

  function walk(obj, depth = 0) {
    if (depth > 8 || texts.join(' ').length > maxLen) return;
    if (typeof obj === 'string' && obj.length > 20) {
      texts.push(obj);
    } else if (Array.isArray(obj)) {
      for (const item of obj) walk(item, depth + 1);
    } else if (obj && typeof obj === 'object') {
      // 优先提取常见内容字段
      for (const key of ['content', 'text', 'body', 'description', 'summary',
        'message', 'value', 'title', 'name', 'answer', 'result']) {
        if (obj[key] && typeof obj[key] === 'string' && obj[key].length > 20) {
          texts.push(obj[key]);
        }
      }
      for (const [k, v] of Object.entries(obj)) {
        if (typeof v === 'object' && v !== null) walk(v, depth + 1);
      }
    }
  }

  walk(data);
  return texts.join(' ').replace(/\s+/g, ' ').trim().slice(0, maxLen);
}

// ==================== 嵌入数据提取 ====================
function extractEmbeddedData($, maxLen) {
  /** 提取 HTML 中嵌入的结构化数据：JSON-LD, __NEXT_DATA__, meta 等 */
  const parts = [];

  // JSON-LD
  $('script[type="application/ld+json"]').each((_, el) => {
    try {
      const data = JSON.parse($(el).text());
      if (data.description) parts.push(String(data.description));
      if (data.articleBody) parts.push(String(data.articleBody));
      if (data.text) parts.push(String(data.text));
      // 遍历 @graph
      if (Array.isArray(data['@graph'])) {
        for (const item of data['@graph']) {
          if (item.description) parts.push(String(item.description));
          if (item.articleBody) parts.push(String(item.articleBody));
        }
      }
    } catch {}
  });

  // __NEXT_DATA__ (Next.js)
  $('script#__NEXT_DATA__').each((_, el) => {
    try {
      const data = JSON.parse($(el).text());
      const text = extractJsonContent(data, maxLen);
      if (text.length > 100) parts.push(text);
    } catch {}
  });

  // meta 标签兜底
  const metaSelectors = [
    'meta[property="og:description"]',
    'meta[name="description"]',
    'meta[property="og:title"]',
    'meta[name="twitter:description"]',
  ];
  for (const sel of metaSelectors) {
    const content = $(sel).attr('content');
    if (content && content.length > 20) parts.push(content);
  }

  return parts.join(' ').replace(/\s+/g, ' ').trim().slice(0, maxLen);
}

// ==================== 第1层：轻量 HTTP ====================
async function fetchLightweight(url, maxLen) {
  console.error(`[fetch:http] ${url}`);
  const ac = new AbortController();
  const t = setTimeout(() => ac.abort(), 15000);
  try {
    const r = await fetch(url, {
      headers: {
        'User-Agent': UA,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,application/json;q=0.8,*/*;q=0.5',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US,en;q=0.8',
      },
      redirect: 'follow', signal: ac.signal,
    });
    clearTimeout(t);
    if (!r.ok) return { status: r.status, content: '', error: `HTTP ${r.status}` };

    const contentType = r.headers.get('content-type') || '';
    const buf = Buffer.from(await r.arrayBuffer());

    // JSON 响应：直接解析
    if (/application\/json/i.test(contentType) || (/^[\[{]/.test(buf.toString('utf-8', 0, 100)))) {
      try {
        const data = JSON.parse(buf.toString('utf-8'));
        const text = extractJsonContent(data, maxLen);
        if (text.length > 50) return { status: 200, content: text };
      } catch {}
    }

    // HTML 响应
    const html = await decodeBuffer(buf, contentType);
    const { load } = await import('cheerio');
    const $ = load(html);

    // 先提取嵌入数据（JSON-LD 等），作为补充
    const embedded = extractEmbeddedData($, maxLen);

    // 去噪音
    $('script,style,nav,header,footer,aside,iframe,noscript,.ad,.sidebar,.comment,.social,.share,.related,.breadcrumb,.pagination,.cookie,.popup').remove();

    // 正文容器
    for (const sel of ['article','.article-content','.post-content','.entry-content',
      '#article_content','.markdown-body','.news-content','.detail-body',
      '.content','.main-content','main','#content','table']) {
      const el = $(sel).first();
      if (el.length) {
        const text = el.text().replace(/\s+/g, ' ').trim();
        if (text.length > 200) {
          // 如果嵌入数据有额外信息，拼上
          let result = text;
          if (embedded && !text.includes(embedded.slice(0, 50))) {
            result = text + '\n\n[结构化数据] ' + embedded;
          }
          return { status: 200, content: result.slice(0, maxLen) };
        }
      }
    }

    // 启发式：找文本密度最高的块
    const candidates = [];
    for (const el of $('div, section, main, article').toArray()) {
      const $el = $(el);
      if ($el.children().length > 50) continue;
      const text = $el.text().replace(/\s+/g, ' ').trim();
      if (text.length > 300) {
        const linkRatio = $el.find('a').length / (text.length / 100);
        if (linkRatio < 5) candidates.push({ text, len: text.length });
      }
    }
    candidates.sort((a, b) => b.len - a.len);
    if (candidates.length > 0 && candidates[0].len > 200) {
      let result = candidates[0].text;
      if (embedded && !result.includes(embedded.slice(0, 50))) {
        result = result + '\n\n[结构化数据] ' + embedded;
      }
      return { status: 200, content: result.slice(0, maxLen) };
    }

    // 嵌入数据兜底（正文提取失败但有 JSON-LD 等）
    if (embedded.length > 100) return { status: 200, content: embedded.slice(0, maxLen) };

    const body = $('body').text().replace(/\s+/g, ' ').trim();
    if (body.length > 200) return { status: 200, content: body.slice(0, maxLen) };

    return { status: r.status, content: '', error: `内容太短(${body.length}字)` };
  } catch (e) {
    clearTimeout(t);
    return { status: 0, content: '', error: e.message.split('\n')[0] };
  }
}

// ==================== 第2层：Playwright headed ====================
async function fetchHeaded(url, maxLen) {
  console.error(`[fetch:headed] ${url}`);

  let browser, shared;
  try {
    ({ browser, shared } = await getBrowser());
    const page = await browser.newPage();
    await page.addInitScript(PAGE_COMPAT_INIT);
    await page.setExtraHTTPHeaders({ 'Accept-Language': 'zh-CN,zh;q=0.9,en-US,en;q=0.8' });

    const resp = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: TIMEOUT });
    const httpStatus = resp?.status() || 0;
    await page.waitForTimeout(4000);
    try { await page.evaluate(() => window.scrollTo(0, 300)); await page.waitForTimeout(800); } catch {}

    let content = '';
    try {
      content = await page.evaluate((max) => {
        // 提取 JSON-LD
        const ldParts = [];
        document.querySelectorAll('script[type="application/ld+json"]').forEach(el => {
          try {
            const d = JSON.parse(el.textContent);
            if (d.description) ldParts.push(String(d.description));
            if (d.articleBody) ldParts.push(String(d.articleBody));
          } catch {}
        });

        // 去噪音
        for (const sel of ['script','style','nav','header','footer','aside','iframe','noscript',
          '.ad','.ads','.sidebar','.comment','.social','.share','.related',
          '.breadcrumb','.pagination','.cookie','.popup','[role="navigation"]','[role="banner"]']) {
          document.querySelectorAll(sel).forEach(el => el.remove());
        }

        // 正文提取
        for (const sel of ['article','.article-content','.post-content','.entry-content',
          '#article_content','.markdown-body','.news-content','.detail-body',
          '.content','.main-content','main','#content','table']) {
          const el = document.querySelector(sel);
          if (el) { const text = el.innerText.replace(/\s+/g, ' ').trim(); if (text.length > 200) return text.slice(0, max); }
        }
        const candidates = [];
        for (const el of document.querySelectorAll('div, section, main, article')) {
          if (el.children.length > 50) continue;
          const text = el.innerText?.replace(/\s+/g, ' ').trim() || '';
          if (text.length > 300) { const links = el.querySelectorAll('a'); if (links.length / (text.length / 100) < 5) candidates.push({ el, len: text.length }); }
        }
        candidates.sort((a, b) => b.len - a.len);
        if (candidates.length > 0) { const text = candidates[0].el.innerText.replace(/\s+/g, ' ').trim(); if (text.length > 200) return text.slice(0, max); }
        return document.body?.innerText?.replace(/\s+/g, ' ').trim().slice(0, max) || '';
      }, maxLen);
    } catch {
      try { await page.waitForTimeout(2000); content = await page.evaluate((max) => document.body?.innerText?.replace(/\s+/g, ' ').trim().slice(0, max) || '', maxLen); } catch {}
    }

    await page.close();
    if (content.length < 50) return { status: httpStatus, content: '', error: content ? `内容太短(${content.length}字)` : `HTTP ${httpStatus}` };
    return { status: httpStatus, content };
  } catch (e) {
    return { status: 0, content: '', error: e.message.split('\n')[0] };
  } finally {
    if (browser) await releaseBrowser(browser, shared).catch(() => {});
  }
}

// ==================== 单 URL：两层兜底 ====================
export async function fetchUrl(url, maxLen) {
  // 第1层：轻量 HTTP
  let result = await fetchLightweight(url, maxLen);
  if (result.content) return { url, ...result };
  console.error(`[fetch:http] 失败: ${result.error}`);

  // 第2层：Playwright headed
  result = await fetchHeaded(url, maxLen);
  return { url, ...result };
}

// ==================== main ====================
async function main() {
  await ensureDeps();
  const { program } = await import('commander');
  program
    .argument('<urls...>', '要抓取的 URL，多个并行')
    .option('--max-len <n>', '单页最大字符数', v => parseInt(v, 10), DEFAULT_MAX_LEN)
    .option('--http-only', '只用轻量 HTTP，不启动浏览器')
    .option('--headed', '跳过 HTTP，直接 headed')
    .parse(process.argv);

  const opts = program.opts();
  const maxLen = Math.max(1000, Math.min(50000, opts.maxLen || DEFAULT_MAX_LEN));
  const urls = program.args.filter(a => a.startsWith('http'));
  if (!urls.length) { console.log(JSON.stringify({ error: '未传入有效 URL' })); process.exit(1); }

  const tasks = urls.map(async (url) => {
    if (opts.httpOnly) {
      const r = await fetchLightweight(url, maxLen);
      if (r.error) console.error(`[fetch] 跳过: ${r.error}`);
      return { url, ...r };
    }
    if (opts.headed) {
      const r = await fetchHeaded(url, maxLen);
      if (r.error) console.error(`[fetch] 跳过: ${r.error}`);
      return { url, ...r };
    }
    const r = await fetchUrl(url, maxLen);
    if (r.error) console.error(`[fetch] 跳过: ${r.error}`);
    return r;
  });

  const settled = await Promise.allSettled(tasks);
  const results = settled.map(r => r.status === 'fulfilled' ? r.value : { url: '?', status: 0, content: '', error: String(r.reason) });
  console.log(JSON.stringify(results, null, 2));
}

// 仅在直接 CLI 运行时调用 main，作为模块被 import 时不自动执行
const isMain = import.meta.url === `file://${process.argv[1]?.replace(/\\/g, '/')}` ||
               import.meta.url === `file:///${process.argv[1]?.replace(/\\/g, '/')}`;
if (isMain) {
  main().catch(e => { console.error('[ERROR]', e.message); process.exit(1); });
}
