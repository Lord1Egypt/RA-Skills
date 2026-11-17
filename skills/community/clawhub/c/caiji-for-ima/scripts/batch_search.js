/**
 * 批量搜狗微信文章检索
 * 用法: node batch_search.js <keywords.txt> <outdir>
 */
const https = require('https');
const zlib = require('zlib');
const fs = require('fs');
const path = require('path');
const cheerio = require('cheerio');

// 使用单一标准浏览器 UA（固定，不做随机轮换），符合正常 HTTP 客户端行为
const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36';
const ua = () => UA;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
// 搜狗限流页特征串：命中即视为本次请求被限流，转入冷却退避
const THROTTLE_MARKER = 'antispider';

function get(url, headers, timeoutMs = 12000) {
  return new Promise((resolve, reject) => {
    const u = new URL(url);
    const req = https.request(
      { hostname: u.hostname, path: u.pathname + u.search, method: 'GET', headers },
      (resp) => {
        const chunks = [];
        resp.on('data', (d) => chunks.push(d));
        resp.on('end', () => {
          let b = Buffer.concat(chunks);
          const ce = resp.headers['content-encoding'];
          if (ce) {
            try {
              if (ce.includes('gzip')) b = zlib.gunzipSync(b);
              else if (ce.includes('deflate')) b = zlib.inflateSync(b);
              else if (ce.includes('br')) b = zlib.brotliDecompressSync(b);
            } catch (e) {}
          }
          resolve({ status: resp.statusCode, headers: resp.headers, text: b.toString('utf-8') });
        });
      }
    );
    req.on('error', reject);
    req.setTimeout(timeoutMs, () => {
      req.destroy();
      reject(new Error('timeout'));
    });
    req.end();
  });
}

async function getCookie() {
  try {
    const r = await get('https://v.sogou.com/v?ie=utf8&query=&p=40030600', {
      'User-Agent': ua(),
      'Accept-Encoding': 'gzip',
      Accept: 'text/html,application/xhtml+xml,*/*;q=0.8',
    });
    if (r.headers['set-cookie']) return r.headers['set-cookie'].map((x) => x.split(';')[0]).join('; ');
  } catch (e) {}
  return '';
}

async function searchPage(query, page, cookie) {
  const q = encodeURIComponent(query);
  const url = `https://weixin.sogou.com/weixin?query=${q}&s_from=input&_sug_=n&type=2&page=${page}&ie=utf8`;
  const r = await get(url, {
    'User-Agent': ua(),
    Accept: 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Accept-Encoding': 'gzip',
    Host: 'weixin.sogou.com',
    Referer: 'https://weixin.sogou.com/',
    Cookie: cookie,
  });
  if (r.status !== 200) return { articles: [], blocked: r.text.includes(THROTTLE_MARKER) };
  const html = r.text;
  if (html.includes(THROTTLE_MARKER)) return { articles: [], blocked: true };
  const $ = cheerio.load(html);
  const out = [];
  $('ul.news-list li').each((_, el) => {
    const $e = $(el);
    const $a = $e.find('h3 a');
    if (!$a.length) return;
    let href = $a.attr('href') || '';
    if (!href) return;
    if (href.startsWith('/')) href = 'https://weixin.sogou.com' + href;
    const title = $a.text().trim();
    const summary = $e.find('p.txt-info').text().trim();
    const $s = $e.find('.s-p');
    let source = $s.find('.all-time-y2').text().trim() || $s.find('a.account').text().trim();
    let ts = '';
    const scriptText = $s.find('.s2 script').text();
    const m = scriptText.match(/(\d{10})/);
    if (m) ts = new Date(parseInt(m[1]) * 1000).toISOString().slice(0, 10);
    out.push({ title, url: href, summary, source, date: ts, query });
  });
  return { articles: out, blocked: false };
}

// 每个关键词：每次请求刷新一次会话 cookie，遇限流则冷却后重试
function saveState(outDir) {
  fs.mkdirSync(outDir, { recursive: true });
  fs.writeFileSync(path.join(outDir, 'all_articles.json'), JSON.stringify(Object.values(all), null, 2), 'utf-8');
  fs.writeFileSync(path.join(outDir, 'progress.txt'), `done=${doneKw} total=${total} unique=${Object.keys(all).length}\n` + log.join('\n'), 'utf-8');
}

async function searchKeyword(kw, pages, outDir) {
  let count = 0;
  let blocked = false;
  for (let p = 1; p <= pages; p++) {
    let ok = false;
    for (let attempt = 0; attempt < 2; attempt++) {
      const cookie = await getCookie();
      try {
        const res = await searchPage(kw, p, cookie);
        if (res.blocked) {
          blocked = true;
          await sleep(5000 + Math.random() * 4000);
          continue;
        }
        for (const a of res.articles) {
          if (!all[a.url]) {
            all[a.url] = a;
            count++;
          }
        }
        ok = true;
        if (res.articles.length === 0) return { count, blocked };
        break;
      } catch (e) {
        await sleep(2000);
      }
    }
    if (!ok) return { count, blocked };
    await sleep(1000 + Math.random() * 900);
  }
  return { count, blocked };
}

const all = {};
const log = [];
let doneKw = 0;
let total = 0;

async function main() {
  const kwFile = process.argv[2];
  const outDir = process.argv[3];
  const pages = parseInt(process.argv[4] || '2', 10);
  fs.mkdirSync(outDir, { recursive: true });
  const kws = fs
    .readFileSync(kwFile, 'utf-8')
    .split('\n')
    .map((x) => x.trim())
    .filter(Boolean);
  total = kws.length;

  for (let i = 0; i < kws.length; i++) {
    const kw = kws[i];
    const got = await searchKeyword(kw, pages, outDir);
    doneKw = i + 1;
    log.push(`${kw} -> new ${got.count}${got.blocked ? ' [BLOCKED]' : ''}`);
    console.error(`[${i + 1}/${kws.length}] ${kw} new=${got.count}${got.blocked ? ' BLOCKED' : ''} (uniq ${Object.keys(all).length})`);
    saveState(outDir); // 每个关键词增量落盘
    await sleep(600 + Math.random() * 700);
  }
  console.error(`\nTOTAL UNIQUE: ${Object.keys(all).length}`);
}

main();
