#!/usr/bin/env node
// chat-share-reader 主入口：把 AI 对话分享链接抓成 markdown。
//
// 用法：
//   node read.mjs <url> [url2 ...] [--out DIR] [--stdout] [--json] [--no-vendor]
//
// 通道优先级：
//   1. Convolvger（本机第三方 CLI，8 个 provider，直接读各站的数据接口）
//   2. 本 skill 自有实现（workbuddy / chatgpt / claude 这些 Convolvger 不支持或已失效的站）
//
// 站点模块声明 useVendor 表示允许先试 Convolvger，失败后回退到自己的 read()。
import { writeFile, mkdir, readFile, unlink } from 'node:fs/promises';
import { t } from './lib/i18n.mjs';
import { existsSync } from 'node:fs';
import path from 'node:path';
import * as workbuddy from './sites/workbuddy.mjs';
import * as chatgpt from './sites/chatgpt.mjs';
import * as claude from './sites/claude.mjs';
import * as gemini from './sites/gemini.mjs';
import * as grok from './sites/grok.mjs';
import * as perplexity from './sites/perplexity.mjs';
import * as biji from './sites/biji.mjs';
import * as vendorOnly from './sites/vendor-only.mjs';
import * as vendor from './lib/vendor.mjs';
import * as backend from './lib/backend/index.mjs';
import { buildDoc, normalizeMessages, safeName } from './lib/md.mjs';
import { createRedactor } from './lib/redact.mjs';

const SITES = [workbuddy, chatgpt, claude, gemini, grok, perplexity, biji, vendorOnly];

function parseArgs(argv) {
  const urls = [];
  const opts = { out: './chat-shares', stdout: false, json: false, noVendor: false, redact: 'home' };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--out') opts.out = argv[++i];
    else if (a === '--stdout') opts.stdout = true;
    else if (a === '--json') opts.json = true;
    else if (a === '--no-vendor') opts.noVendor = true;
    else if (a === '--redact') opts.redact = argv[++i] || 'home';
    else if (a === '--no-redact') opts.redact = 'off';
    else if (a.startsWith('--')) throw new Error('未知参数：' + a);
    else urls.push(a);
  }
  return { urls, opts };
}

function pickSite(url) {
  return SITES.find((s) => {
    try {
      return s.match(url);
    } catch {
      return false;
    }
  });
}

// 从 convolvger inspect 的输出里取标题
function parseInspectTitle(out) {
  const m = out.match(/^Title:\s*(.+)$/m);
  return m ? m[1].trim() : '';
}

// 目标文件路径。标题撞车时加 share id 后缀：
// DeepSeek 所有分享的标题都是 "Shared Conversation"，不处理会互相覆盖。
function targetFile(dir, title, url) {
  const base = safeName(title) || 'untitled';
  const first = path.resolve(dir, base + '.md');
  if (!existsSync(first)) return first;
  const id = (url.split('/').filter(Boolean).pop() || '').replace(/[^A-Za-z0-9_-]/g, '').slice(0, 8);
  return path.resolve(dir, `${base}-${id || Date.now()}.md`);
}

// vendor 通道产出的是别人拼好的 markdown，不经过 buildDoc，只能落盘后再过一遍脱敏。
// 就地重写，替换后内容不变时跳过写入，避免无谓改动 mtime。
async function redactFile(file, level) {
  if (level === 'off') return;
  const r = createRedactor(level);
  const before = await readFile(file, 'utf8');
  const after = r.apply(before);
  if (after !== before) await writeFile(file, after, 'utf8');
}

// vendor 通道：先 inspect 拿标题与消息数，再 export 到最终文件名
async function viaVendor(url, opts, siteName) {
  const info = await vendor.inspect(url);
  const title = parseInspectTitle(info) || url.split('/').pop() || 'untitled';
  const countMatch = info.match(/^Messages:\s*(\d+)/m);
  const count = countMatch ? Number(countMatch[1]) : 0;

  if (opts.stdout) {
    const tmp = path.resolve(opts.out, `.tmp-${Date.now()}.md`);
    await mkdir(opts.out, { recursive: true });
    await vendor.exportMarkdown(url, tmp);
    const md = await readFile(tmp, 'utf8');
    await unlink(tmp).catch(() => {});
    return { site: siteName, channel: 'vendor', title, messages: count, md: createRedactor(opts.redact).apply(md) };
  }

  await mkdir(opts.out, { recursive: true });
  const file = targetFile(opts.out, title, url);
  await vendor.exportMarkdown(url, file);
  await redactFile(file, opts.redact);
  return { site: siteName, channel: 'vendor', title, messages: count, file };
}

async function runOne(url, opts) {
  const site = pickSite(url);
  if (!site) {
    throw new Error(
      '不支持的站点：' + url + '\n已支持：' + SITES.map((s) => s.name).join('、') +
      '\n新增站点见 references/sites.md 的接入说明'
    );
  }

  let vendorError = '';
  if (!opts.noVendor && site.useVendor && vendor.supports(url)) {
    if (vendor.findConvolvger()) {
      try {
        return await viaVendor(url, opts, site.name);
      } catch (e) {
        vendorError = String(e.message || e).slice(0, 200);
      }
    } else {
      vendorError = '本机没装 convolvger';
    }
  }

  let result;
  let session = null;
  try {
    if (site.channel === 'browser') {
      // 只有真要开浏览器的站点才创建 session，纯 HTTP 站点不受后端影响
      session = await backend.createSession({ name: 'csr-' + site.name.replace(/[^a-z0-9]+/gi, '') });
    }
    result = await site.read(url, { session });
  } catch (e) {
    const msg = String(e.message || e);
    throw new Error(vendorError ? `${msg}；Convolvger 通道也失败：${vendorError}` : msg);
  } finally {
    if (session) await session.close().catch(() => {});
  }
  const messages = normalizeMessages(result.messages || []);
  if (!messages.length) {
    const hint = vendorError ? `（Convolvger 通道也失败：${vendorError}）` : '';
    throw new Error('抓到 0 条消息，页面结构可能改版了' + hint);
  }

  const md = buildDoc({
    title: result.title,
    url,
    source: result.source,
    channel: site.channel,
    messages,
    note: result.note,
    demote: result.demote,
    redact: opts.redact,
  });

  if (opts.stdout) return { site: site.name, title: result.title, messages: messages.length, md };

  await mkdir(opts.out, { recursive: true });
  const file = targetFile(opts.out, result.title, url);
  await writeFile(file, md, 'utf8');
  return {
    site: site.name,
    channel: site.channel,
    title: result.title,
    messages: messages.length,
    chars: md.length,
    file,
    vendorFallback: vendorError || undefined,
  };
}

const { urls, opts } = parseArgs(process.argv.slice(2));
if (!urls.length) {
  console.error(t(
    '用法：node read.mjs <url> [url2 ...] [--out DIR] [--stdout] [--json] [--no-vendor]\n' +
      '      [--redact off|home|strict]   脱敏档位，默认 home',
    'Usage: node read.mjs <url> [url2 ...] [--out DIR] [--stdout] [--json] [--no-vendor]\n' +
      '       [--redact off|home|strict]   redaction level, default home'
  ));
  process.exit(2);
}

const results = [];
let failed = 0;
for (const url of urls) {
  try {
    results.push(await runOne(url, opts));
  } catch (e) {
    failed++;
    results.push({ url, error: String(e.message || e).slice(0, 500) });
  }
}

if (opts.json) {
  console.log(JSON.stringify(results, null, 2));
} else {
  for (const r of results) {
    if (r.error) console.log('FAIL ' + (r.url || '') + ' :: ' + r.error);
    else if (r.md) console.log(r.md);
    else {
      const fb = r.vendorFallback ? `（vendor 失败后回退：${r.vendorFallback}）` : '';
      console.log(`OK ${r.site} [${r.channel}] ${r.messages} ${t('条', 'msgs')} -> ${r.file}${fb}`);
    }
  }
}
process.exit(failed ? 1 : 0);
