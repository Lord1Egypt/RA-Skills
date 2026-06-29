#!/usr/bin/env node
/**
 * smart-web-search search.js v2.0.0
 *
 * 路由策略：仅按 IP 归属判断
 *   - IP 国内 → Bing CN（Playwright 全流程：开首页拿 cookies → 搜索框提交）
 *   - IP 国外 → DDG（Playwright 全流程：开首页拿 cookies → 搜索框提交）
 *   - 任一引擎为空时互相兜底
 *
 * 不做 query 改写，不做城市/意图识别，不做低质量域名过滤。
 */
import process from 'process';
import querystring from 'querystring';
import path from 'path';
import { fileURLToPath } from 'url';
import { chromium } from 'playwright';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SKILL_ROOT = path.resolve(__dirname, '..');

const DEFAULT_MAX = 10;
const DEFAULT_FETCH = 3;
const PW_TIMEOUT = 25000;

const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36';

// ==================== 工具函数 ====================
function clean(s) { return String(s || '').replace(/\s+/g, ' ').trim(); }

function decodeBingUrl(url) {
  if (!url?.includes('bing.com/ck/')) return url;
  try {
    const u = new URL(url).searchParams.get('u');
    if (!u) return url;
    const stripped = u.replace(/^a[0-9]/, '');
    const b64 = stripped + '='.repeat((4 - stripped.length % 4) % 4);
    const dec = Buffer.from(b64, 'base64').toString('utf-8');
    return dec.startsWith('http') ? dec : url;
  } catch { return url; }
}

function normalizeUrl(raw) {
  let url = clean(raw);
  if (!url) return url;
  url = decodeBingUrl(url);
  try {
    const u = new URL(url);
    u.hash = '';
    for (const k of ['utm_source','utm_medium','utm_campaign','gclid','fbclid','msclkid','spm','from','ref','src']) {
      u.searchParams.delete(k);
    }
    return u.toString();
  } catch { return url; }
}

function dedupKey(url) {
  try {
    const u = new URL(url);
    const host = u.hostname.replace(/^(www|m|mobile)\./, '');
    const p = u.pathname.replace(/\/+$/, '').replace(/\.(html?|php|aspx?)$/, '');
    return `${host}${p}`.toLowerCase();
  } catch { return url.toLowerCase(); }
}

// ==================== 依赖检查 ====================
async function checkDeps() {
  const missing = [];
  for (const mod of ['cheerio', 'commander', 'playwright']) {
    try { await import(mod); } catch { missing.push(mod); }
  }
  if (missing.length === 0) return;

  console.error(`\n[X] smart-web-search 缺少依赖: ${missing.join(', ')}\n`);
  console.error('   一键安装（推荐）:');
  console.error(`     cd "${SKILL_ROOT}" && bash scripts/setup.sh`);
  console.error('   Windows:');
  console.error(`     cd "${SKILL_ROOT}"; powershell -File scripts/setup.ps1\n`);
  console.error('   手动安装:');
  console.error(`     cd "${SKILL_ROOT}" && npm install && npx playwright install chromium\n`);
  console.error('   详细文档: 见 SKILL.md「安装」章节\n');
  process.exit(2);
}

// ==================== IP 归属探测 ====================
let _inChinaCache = null;
async function detectInChina() {
  if (_inChinaCache !== null) return _inChinaCache;
  const probes = [
    (async () => {
      for (const url of ['https://myip.ipip.net', 'https://cip.cc']) {
        try {
          const r = await fetch(url, { headers: { 'User-Agent': UA }, signal: AbortSignal.timeout(3000) });
          if (!r.ok) continue;
          const text = await r.text();
          if (/中国|CN/i.test(text)) {
            const ip = text.match(/(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/)?.[1] ?? '?';
            return { inChina: true, label: `${ip} → CN` };
          }
        } catch {}
      }
      throw new Error('cn probe failed');
    })(),
    (async () => {
      for (const url of ['https://ipinfo.io/json', 'https://ipapi.co/json/']) {
        try {
          const r = await fetch(url, { headers: { 'User-Agent': UA }, signal: AbortSignal.timeout(3000) });
          if (!r.ok) continue;
          const d = await r.json();
          const cc = String(d.country || d.country_code || '').toUpperCase();
          if (!cc) continue;
          return { inChina: cc === 'CN', label: `${d.ip ?? '?'} → ${cc}` };
        } catch {}
      }
      throw new Error('intl probe failed');
    })(),
    (async () => {
      const r = await fetch('https://cn.bing.com', { headers: { 'User-Agent': UA }, signal: AbortSignal.timeout(3000), redirect: 'manual' });
      return { inChina: r.status === 200 || r.status === 302, label: `cn.bing.com → ${r.status}` };
    })(),
  ];
  try {
    const winner = await Promise.any(probes);
    console.error(`[地理] ${winner.label} → ${winner.inChina ? '国内' : '国外'}`);
    _inChinaCache = winner.inChina;
    return winner.inChina;
  } catch {
    console.error('[地理] 检测失败，默认国外');
    _inChinaCache = false;
    return false;
  }
}

// ==================== 浏览器管理 ====================
let _browser = null;
async function getBrowser() {
  if (_browser) return _browser;
  _browser = await chromium.launch({ headless: true });
  return _browser;
}
async function closeBrowser() {
  if (_browser) {
    try { await _browser.close(); } catch {}
    _browser = null;
  }
}

// ==================== Bing CN (Playwright 全流程：先访问首页拿 cookies → 搜索框提交) ====================
async function searchBingPW(query, max) {
  console.error(`[Bing:pw] ${query}`);
  const out = [], seen = new Set();
  const base = 'https://cn.bing.com';
  let context;
  try {
    const browser = await getBrowser();
    context = await browser.newContext({
      userAgent: UA,
      locale: 'zh-CN',
      viewport: { width: 1920, height: 1080 },
      extraHTTPHeaders: { 'Accept-Language': 'zh-CN,zh;q=0.9' },
    });

    const page = await context.newPage();

    // 1) 先访问首页建立 session 并拿 cookies
    await page.goto(base + '/', { waitUntil: 'domcontentloaded', timeout: 15000 });
    await page.waitForTimeout(1500);

// __APPEND_MARKER_1__
    // 2) 通过搜索框提交（携带首页 cookies）
    try {
      const searchBox = await page.$('#sb_form_q');
      if (searchBox) {
        await searchBox.click();
        await searchBox.fill(query);
        await page.waitForTimeout(300);
        await Promise.all([
          page.waitForLoadState('domcontentloaded', { timeout: PW_TIMEOUT }),
          page.keyboard.press('Enter'),
        ]);
        await page.waitForTimeout(2000);
      } else {
        await page.goto(base + '/search?' + querystring.stringify({ q: query }), {
          waitUntil: 'domcontentloaded', timeout: PW_TIMEOUT,
        });
        await page.waitForTimeout(1500);
      }
    } catch {
      await page.goto(base + '/search?' + querystring.stringify({ q: query }), {
        waitUntil: 'domcontentloaded', timeout: PW_TIMEOUT,
      });
      await page.waitForTimeout(1500);
    }

    const results = await page.evaluate(() => {
      const items = [];
      const seen = new Set();
      const add = (title, url, snippet) => {
        if (title && url && url.startsWith('http') && !seen.has(url)) {
          seen.add(url);
          items.push({ title, url, snippet });
        }
      };
      document.querySelectorAll('li.b_algo').forEach(el => {
        const a = el.querySelector('h2 a');
        if (!a) return;
        add(a.textContent.trim(), a.href, el.querySelector('.b_caption p')?.textContent?.trim() || '');
      });
      if (items.length === 0) {
        document.querySelectorAll('li.b_ans, li.b_vList, li.b_entityTP, li.b_mop').forEach(el => {
          el.querySelectorAll('a[href]').forEach(a => {
            const href = a.href;
            if (!href || href.includes('bing.com') || href.includes('microsoft.com') || href.startsWith('javascript:')) return;
            add(a.textContent.trim().slice(0, 120), href, '');
          });
        });
      }
      return items;
    });
// __APPEND_MARKER_2__

    for (const item of results) {
      const url = normalizeUrl(item.url);
      const title = clean(item.title);
      const snippet = clean(item.snippet);
      if (title && url?.startsWith('http') && !seen.has(url.toLowerCase())) {
        seen.add(url.toLowerCase());
        out.push({ title, url, snippet });
      }
    }
    console.error(`[Bing:pw] ${out.length} 条`);
  } catch (e) {
    console.error(`[Bing:pw] 错误: ${e.message.split('\n')[0]}`);
  } finally {
    if (context) await context.close().catch(() => {});
  }
  return out.slice(0, max);
}

// ==================== DDG (Playwright 全流程：先访问首页拿 cookies → 搜索框提交) ====================
async function searchDDGPW(query, max) {
  console.error(`[DDG:pw] ${query}`);
  const out = [], seen = new Set();
  const base = 'https://duckduckgo.com';
  let context;
  try {
    const browser = await getBrowser();
    context = await browser.newContext({
      userAgent: UA,
      locale: 'en-US',
      viewport: { width: 1920, height: 1080 },
      extraHTTPHeaders: { 'Accept-Language': 'en-US,en;q=0.9' },
    });

    const page = await context.newPage();

    // 1) 先访问首页建立 session 并拿 cookies
    await page.goto(base + '/', { waitUntil: 'domcontentloaded', timeout: 15000 });
    await page.waitForTimeout(1500);
// __APPEND_MARKER_3__

    // 2) 搜索框提交（携带首页 cookies）
    try {
      const searchBox = await page.$('input[name="q"]');
      if (searchBox) {
        await searchBox.click();
        await searchBox.fill(query);
        await page.waitForTimeout(300);
        await Promise.all([
          page.waitForLoadState('domcontentloaded', { timeout: PW_TIMEOUT }),
          page.keyboard.press('Enter'),
        ]);
        await page.waitForTimeout(2500);
      } else {
        await page.goto(base + '/?q=' + encodeURIComponent(query), {
          waitUntil: 'domcontentloaded', timeout: PW_TIMEOUT,
        });
        await page.waitForTimeout(2000);
      }
    } catch {
      await page.goto(base + '/?q=' + encodeURIComponent(query), {
        waitUntil: 'domcontentloaded', timeout: PW_TIMEOUT,
      });
      await page.waitForTimeout(2000);
    }

    const results = await page.evaluate(() => {
      const items = [];
      const seen = new Set();
      const add = (title, url, snippet) => {
        if (title && url && url.startsWith('http') && !seen.has(url)) {
          seen.add(url);
          items.push({ title, url, snippet });
        }
      };
      const selectors = [
        'article[data-testid="result"]',
        'li[data-layout="organic"]',
        '.result',
        '.web-result',
      ];
      for (const sel of selectors) {
        document.querySelectorAll(sel).forEach(el => {
          const a = el.querySelector('a[href^="http"]');
          const t = el.querySelector('h2, [data-testid="result-title-a"], .result__a, .result__title');
          const s = el.querySelector('[data-testid="result-snippet"], .result__snippet, .result__body');
          if (a && t) add((t.innerText || t.textContent || '').trim(), a.href, s ? (s.innerText || s.textContent || '').trim() : '');
        });
        if (items.length > 0) break;
      }
      return items;
    });
// __APPEND_MARKER_4__

    for (const item of results) {
      const url = normalizeUrl(item.url);
      const title = clean(item.title);
      const snippet = clean(item.snippet);
      if (title && url?.startsWith('http') && !seen.has(url.toLowerCase())) {
        seen.add(url.toLowerCase());
        out.push({ title, url, snippet });
      }
    }
    console.error(`[DDG:pw] ${out.length} 条`);
  } catch (e) {
    console.error(`[DDG:pw] 错误: ${e.message.split('\n')[0]}`);
  } finally {
    if (context) await context.close().catch(() => {});
  }
  return out.slice(0, max);
}

// ==================== 自动抓取正文 ====================
// 直接 import 同语言 fetch.js 函数，不再 spawn 子进程。
async function autoFetch(results, fetchCount, maxLen) {
  if (fetchCount <= 0 || results.length === 0) return;
  const safeUrls = results
    .slice(0, Math.min(fetchCount, results.length))
    .map(r => r.url)
    .filter(u => /^https?:\/\//i.test(u));
  if (safeUrls.length === 0) return;
  console.error(`[fetch] 抓取 ${safeUrls.length} 条正文...`);
  try {
    const { fetchUrl } = await import('./fetch.js');
    const tasks = safeUrls.map(async (url) => {
      try {
        const r = await fetchUrl(url, maxLen);
        return r && r.content ? r.content.slice(0, maxLen) : '';
      } catch (e) {
        console.error(`[fetch] ${url} 失败: ${e.message.split('\n')[0]}`);
        return '';
      }
    });
    const contents = await Promise.all(tasks);
    for (let i = 0; i < contents.length; i++) {
      if (contents[i]) results[i].content = contents[i];
    }
    console.error('[fetch] 完成');
  } catch (e) {
    console.error(`[fetch] 失败: ${e.message.split('\n')[0]}`);
  }
}
// __APPEND_MARKER_5__

// ==================== main ====================
async function main() {
  const startTime = Date.now();
  await checkDeps();
  const { program } = await import('commander');
  program
    .argument('[query...]', '搜索关键词')
    .option('--max <n>', '最大结果数 (1-30)', v => parseInt(v, 10), DEFAULT_MAX)
    .option('--fetch <n>', '自动抓取前N条正文 (0=不抓)', v => parseInt(v, 10), DEFAULT_FETCH)
    .option('--max-len <n>', '单页最大字符数', v => parseInt(v, 10), 6000)
    .option('--no-fetch', '禁用正文抓取')
    .option('--region <r>', '区域覆盖: auto/cn/intl（auto = IP 探测）', 'auto')
    .parse(process.argv);

  const opts = program.opts();
  const query = clean(program.args.join(' '));
  if (!query) { console.log(JSON.stringify({ error: '未传入搜索关键词' })); process.exit(1); }

  const max = Math.max(1, Math.min(30, opts.max));
  const fetchCount = opts.noFetch ? 0 : (typeof opts.fetch === 'number' ? opts.fetch : DEFAULT_FETCH);
  const maxLen = opts.maxLen || 6000;

  // 仅按 IP 归属判断（--region 仅为代理用户的手动覆盖）
  let inChina;
  if (opts.region === 'cn') inChina = true;
  else if (opts.region === 'intl') inChina = false;
  else inChina = await detectInChina();

  const out = [], seen = new Set();
  const add = (items) => {
    for (const item of items) {
      const key = dedupKey(item.url);
      if (!seen.has(key)) { seen.add(key); out.push(item); }
    }
  };
// __APPEND_MARKER_6__

  if (inChina) {
    console.error('[策略] IP 国内 → Bing CN');
    add(await searchBingPW(query, max));
    if (out.length === 0) {
      console.error('[策略] Bing 为空，兜底 → DDG');
      add(await searchDDGPW(query, max));
    }
  } else {
    console.error('[策略] IP 国外 → DDG');
    add(await searchDDGPW(query, max));
    if (out.length === 0) {
      console.error('[策略] DDG 为空，兜底 → Bing CN');
      add(await searchBingPW(query, max));
    }
  }

  const results = out.slice(0, max);
  await autoFetch(results, fetchCount, maxLen);

  console.log(JSON.stringify(results, null, 2));
  console.error(`[完成] ${((Date.now() - startTime) / 1000).toFixed(1)}s | ${results.length} 条结果`);
  await closeBrowser();
}

main().then(() => process.exit(0)).catch(e => {
  console.error('[ERROR]', e.message);
  closeBrowser().finally(() => process.exit(1));
});
