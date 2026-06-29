#!/usr/bin/env node
/* eslint-disable no-console */
/**
 * baidu_img.js
 * =============
 * 百度图片下载器（Node.js 零依赖版）
 *
 * 底层：百度 acjson JSON 端点（image.baidu.com/search/acjson）
 * 不需要浏览器、登录、Cookie，不依赖任何 npm 包。
 *
 * 用法：
 *   node baidu_img.js -k openclaw
 *   node baidu_img.js -k 猫 -n 60
 *   node baidu_img.js -k 风景 -n 100 -s origin
 *   node baidu_img.js -k 猫 -n 20 -o D:/images/cat
 */
'use strict';

const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// ---- 常量 --------------------------------------------------------------------

const ENDPOINT = 'https://image.baidu.com/search/acjson';
const PER_PAGE = 60;          // 百度 acjson 单次最大返回数
const RETRY = 2;              // 下载失败重试次数
const TIMEOUT_MS = 15000;     // 单次请求超时（毫秒）
const MIN_DELAY_MS = 200;     // 两次请求间的最小间隔（礼貌爬取）
const TITLE_MAX = 50;         // 标题最大长度（清洗后）

const UA =
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
  'AppleWebKit/537.36 (KHTML, like Gecko) ' +
  'Chrome/120.0.0.0 Safari/537.36';

// ---- 命令行解析 --------------------------------------------------------------

function parseArgs(argv) {
  const args = {
    keyword: '',
    count: 30,
    source: 'thumb', // thumb | middle | origin
    output: null,
    delay: 0.3,
  };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    const next = () => argv[++i];
    if (a === '-k' || a === '--keyword') args.keyword = next();
    else if (a === '-n' || a === '--count') args.count = parseInt(next(), 10) || 30;
    else if (a === '-s' || a === '--source') args.source = next();
    else if (a === '-o' || a === '--output') args.output = next();
    else if (a === '--delay') args.delay = parseFloat(next()) || 0.3;
    else if (a === '-h' || a === '--help') {
      printHelp();
      process.exit(0);
    }
  }
  return args;
}

function printHelp() {
  console.log(
    '用法: node baidu_img.js -k <关键词> [选项]\n' +
      '\n' +
      '  -k, --keyword   搜索关键词（必填）\n' +
      '  -n, --count     下载数量，默认 30\n' +
      '  -s, --source    thumb=缩略图（默认，最稳） / middle=中等图 / origin=原图（需 Referer）\n' +
      '  -o, --output    输出目录，默认 <skill_dir>/download/<关键词>/\n' +
      '  --delay         下载间隔秒数，默认 0.3\n',
  );
}

// ---- HTTP 工具 ---------------------------------------------------------------

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

/** 跟随最多 5 次重定向 */
function httpRequest(rawUrl, headers) {
  return new Promise((resolve, reject) => {
    let redirected = 0;
    const visit = (u) => {
      const lib = u.startsWith('https') ? https : http;
      const req = lib.get(
        u,
        { headers, timeout: TIMEOUT_MS },
        (res) => {
          const status = res.statusCode || 0;
          if (status === 301 || status === 302) {
            res.resume();
            if (redirected++ > 5) return reject(new Error('重定向过多'));
            const loc = res.headers.location;
            if (!loc) return reject(new Error('重定向缺少 Location'));
            return visit(new URL(loc, u).toString());
          }
          resolve(res);
        },
      );
      req.on('error', reject);
      req.on('timeout', () => req.destroy(new Error('timeout')));
    };
    visit(rawUrl);
  });
}

function httpGetText(rawUrl, headers) {
  return new Promise((resolve, reject) => {
    httpRequest(rawUrl, headers)
      .then((res) => {
        let buf = '';
        res.setEncoding('utf8');
        res.on('data', (c) => (buf += c));
        res.on('end', () => resolve(buf));
        res.on('error', reject);
      })
      .catch(reject);
  });
}

function httpGetBinary(rawUrl, headers) {
  return new Promise((resolve, reject) => {
    httpRequest(rawUrl, headers)
      .then((res) => {
        const chunks = [];
        res.on('data', (c) => chunks.push(c));
        res.on('end', () => resolve(Buffer.concat(chunks)));
        res.on('error', reject);
      })
      .catch(reject);
  });
}

// ---- 抓取 & URL 抽取 ----------------------------------------------------------

async function fetchPage(keyword, pn) {
  const qs = new URLSearchParams({
    tn: 'resultjson_com',
    ipn: 'rj',
    word: keyword,
    pn: String(pn),
    rn: String(PER_PAGE),
    ie: 'utf-8',
  }).toString();
  const url = ENDPOINT + '?' + qs;
  const raw = await httpGetText(url, {
    'User-Agent': UA,
    Accept: 'application/json,text/plain,*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    Referer: 'https://image.baidu.com/search/index?word=' + encodeURIComponent(keyword),
  });
  // 找到 JSON 边界
  const s = raw.indexOf('{');
  const e = raw.lastIndexOf('}');
  if (s < 0 || e <= s) throw new Error('返回内容不包含 JSON');
  return JSON.parse(raw.slice(s, e + 1));
}

function pickUrl(item, source) {
  const thumb = item.thumbURL || item.middleURL || item.hoverURL || '';
  const middle = item.middleURL || item.hoverURL || item.thumbURL || '';
  if (source === 'thumb') return thumb;
  if (source === 'middle') return middle;
  if (source === 'origin') {
    const ru = item.replaceUrl;
    if (Array.isArray(ru)) {
      for (const r of ru) {
        if (r && typeof r === 'object') {
          const u = r.ObjURL || r.ObjUrl;
          if (u) return u;
        }
      }
    }
    return middle;
  }
  return thumb;
}

async function collectUrls(keyword, count, source) {
  const collected = [];
  const seen = new Set();
  let pn = 0;
  let page = 0;
  while (collected.length < count) {
    page++;
    let data;
    try {
      data = await fetchPage(keyword, pn);
    } catch (e) {
      console.error(`[warn] 第 ${page} 页请求失败: ${e.message}`);
      break;
    }
    const items = Array.isArray(data.data)
      ? data.data.filter((it) => it && typeof it === 'object')
      : [];
    if (items.length === 0) break;
    for (const it of items) {
      const u = pickUrl(it, source);
      if (!u) continue;
      const host = (it.fromURLHost || '').trim();
      const key = host + '|' + u;
      if (seen.has(key)) continue;
      seen.add(key);
      collected.push({
        url: u,
        title: (it.fromPageTitle || '').trim(),
        host,
        width: it.width || 0,
        height: it.height || 0,
        type: (it.type || 'jpg').toLowerCase(),
        date: (it.bdImgnewsDate || '').trim(),
      });
      if (collected.length >= count) break;
    }
    if (items.length < PER_PAGE) break; // 末页
    pn += PER_PAGE;
    await sleep(MIN_DELAY_MS);
  }
  return collected.slice(0, count);
}

// ---- 下载 --------------------------------------------------------------------

async function downloadOne(url, outPath, referer) {
  const headers = {
    'User-Agent': UA,
    Accept: 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
  };
  if (referer) headers.Referer = referer;
  let lastErr = null;
  for (let i = 0; i <= RETRY; i++) {
    try {
      const buf = await httpGetBinary(url, headers);
      if (buf.length < 256) throw new Error(`返回数据过小 (${buf.length}B)`);
      fs.writeFileSync(outPath, buf);
      return buf.length;
    } catch (e) {
      lastErr = e;
      await sleep(500 * (i + 1));
    }
  }
  throw new Error('下载失败: ' + (lastErr ? lastErr.message : 'unknown'));
}

// ---- 文件名清洗 --------------------------------------------------------------

/** 清洗字符串用作文件名片段。去除非法字符、规整空白、去首尾点划线、截断长度。 */
function safeName(s, n) {
  if (!s) return '';
  const limit = n || TITLE_MAX;
  let out = String(s)
    .replace(/[\\/:*?"<>|\r\n\t]+/g, '_')   // 非法文件名字符 → _
    .replace(/\s+/g, ' ')                    // 多空白 → 单空格
    .trim()
    .replace(/^[._\- ]+|[._\- ]+$/g, '');    // 去首尾 . _ - 空格
  if (out.length > limit) out = out.slice(0, limit).trim();
  return out;
}

function extFrom(type) {
  const t = (type || '').toLowerCase();
  if (t === 'jpg' || t === 'jpeg') return 'jpg';
  if (t === 'png' || t === 'gif' || t === 'webp' || t === 'bmp') return t;
  return 'jpg';
}

function shortHash(text) {
  return crypto.createHash('md5').update(text, 'utf8').digest('hex').slice(0, 10);
}

// ---- 主流程 ------------------------------------------------------------------

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (!args.keyword) {
    console.error('[error] 缺少关键词，请用 -k 指定');
    printHelp();
    process.exit(1);
  }

  // 输出目录：脚本同级 ../download/<关键词>/
  const skillDir = path.resolve(__dirname, '..');
  const defaultOut = path.join(
    skillDir,
    'download',
    safeName(args.keyword, 80) || 'output',
  );
  const outDir = args.output ? path.resolve(args.output) : defaultOut;
  fs.mkdirSync(outDir, { recursive: true });

  console.log(`[info] 关键词    : ${args.keyword}`);
  console.log(`[info] 目标数量  : ${args.count}`);
  console.log(`[info] 来源      : ${args.source}`);
  console.log(`[info] 输出目录  : ${outDir}`);

  const items = await collectUrls(args.keyword, args.count, args.source);
  console.log(`[info] 收集到 ${items.length} 条候选`);
  if (items.length === 0) {
    console.error('[error] 没有可用的图片，请检查关键词或网络');
    process.exit(1);
  }

  let ok = 0;
  let fail = 0;
  let skip = 0;
  const seenHash = new Set();

  for (let i = 0; i < items.length; i++) {
    const it = items[i];
    const idx = i + 1;
    const uHash = shortHash(it.url);
    if (seenHash.has(uHash)) {
      skip++;
      continue;
    }
    seenHash.add(uHash);

    const ext = extFrom(it.type);

    // 优先用 fromPageTitle；空则 fallback 到 host；都空用 untitled
    let titlePart = safeName(it.title, TITLE_MAX);
    if (!titlePart) {
      titlePart = safeName((it.host || '').replace(/^www\./, ''), 30) || 'untitled';
    }

    const filename = `${String(idx).padStart(4, '0')}_${titlePart}_${uHash}.${ext}`;
    const outPath = path.join(outDir, filename);

    const referer = it.host ? `https://${it.host}/` : 'https://image.baidu.com/';
    try {
      const size = await downloadOne(it.url, outPath, referer);
      const kb = (size / 1024) | 0;
      console.log(
        `[${String(idx).padStart(4)}/${items.length}] OK    ${String(kb).padStart(5)}KB  ${filename}`,
      );
      ok++;
    } catch (e) {
      console.error(
        `[${String(idx).padStart(4)}/${items.length}] FAIL  ${filename}  (${e.message})`,
      );
      // 清理半成品
      try {
        if (fs.existsSync(outPath) && fs.statSync(outPath).size < 1024) {
          fs.unlinkSync(outPath);
        }
      } catch (_) {
        /* ignore */
      }
      fail++;
    }
    await sleep(Math.max(args.delay * 1000, MIN_DELAY_MS));
  }

  console.log(
    `\n[done] 成功 ${ok}，失败 ${fail}，去重跳过 ${skip}，目录 ${outDir}`,
  );
  process.exit(fail === 0 ? 0 : 2);
}

main().catch((e) => {
  console.error('[fatal]', e && e.stack ? e.stack : e);
  process.exit(1);
});
