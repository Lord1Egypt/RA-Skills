#!/usr/bin/env node
// 得到大脑 / Get 笔记（biji.com）登录态批量导出：把你自己账号下的录音笔记拉成本地 markdown。
//
// 与 sites/biji.mjs 的分工：那个处理别人发来的公开分享链接，走免认证的 /share/<id>；
// 这个处理你自己账号里的全部历史，走登录后才放行的 /notes/* 接口。
//
// 为什么不在页面里发请求（bulk.mjs 的做法）：get-notes.luojilab.com 与 www.biji.com
// 跨域，页面上下文的 fetch 直接被 CORS 拦成 TypeError: Failed to fetch，iframe 与 XHR
// 都一样。所以只从页面取一次 token，之后所有请求走 Node 侧的 curl。
//
// 用法：
//   node scripts/biji-notes.mjs list [--limit 20]
//   node scripts/biji-notes.mjs export --since 2026-11-11 --until 2026-11-12 --out DIR
//   node scripts/biji-notes.mjs export --since 2026-11-01 --transcript --type class_audio
import { mkdir, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { httpGetJson } from './lib/http.mjs';
import { available, createSession } from './lib/backend/index.mjs';
import { buildDoc, safeName } from './lib/md.mjs';
import { stripSeek, transcriptFrom } from './sites/biji.mjs';
import { t } from './lib/i18n.mjs';

const API = 'https://get-notes.luojilab.com/voicenotes/web';
const HOME = 'https://www.biji.com/';

function parseArgs(argv) {
  const cmd = argv[0] || 'list';
  const opts = {
    out: './biji-notes',
    limit: 0,
    since: '',
    until: '',
    type: '',
    transcript: false,
    force: false,
  };
  for (let i = 1; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--out') opts.out = argv[++i];
    else if (a === '--limit') opts.limit = Number(argv[++i]) || 0;
    else if (a === '--since') opts.since = argv[++i];
    else if (a === '--until') opts.until = argv[++i];
    else if (a === '--type') opts.type = argv[++i];
    else if (a === '--transcript') opts.transcript = true;
    else if (a === '--force') opts.force = true;
    else throw new Error(t('未知参数：', 'Unknown argument: ') + a);
  }
  return { cmd, opts };
}

// token 在页面 localStorage 里，是 360 字符的 JWT。裸 token 当 Authorization 用会
// 返回 ParseTokenFailed，必须是 "Bearer <token>"。
async function getToken() {
  if (process.env.BIJI_TOKEN) return process.env.BIJI_TOKEN;
  if (!available()) {
    throw new Error(t('需要浏览器通道取登录态（装 Chrome/Edge 或 opencli），或设置环境变量 BIJI_TOKEN', 'Needs a browser backend for the session (Chrome/Edge or opencli), or set BIJI_TOKEN'));
  }
  const sess = await createSession({ name: 'csr-biji' });
  try {
    await sess.open(HOME, { window: 'background' });
    for (let i = 0; i < 12; i++) {
      const out = String(await sess.eval('localStorage.getItem("token")')).trim();
      const m = out.match(/ey[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+/);
      if (m) return m[0];
      await new Promise((r) => setTimeout(r, 2000));
    }
  } finally {
    await sess.close();
  }
  throw new Error(t('页面里没找到 token，先在浏览器打开 ' + HOME + ' 登录一次', 'No token found on the page. Open ' + HOME + ' in a browser and sign in once.'));
}

async function call(url, tk) {
  const body = await httpGetJson(url, { headers: ['Authorization: Bearer ' + tk] });
  if (body && body.h && body.h.c === 0) return body.c;
  if (body && body.message) {
    throw new Error(t(`鉴权失败（${body.message}），token 已过期，重新登录 ${HOME} 再跑`, `Auth failed (${body.message}). Token expired; sign in at ${HOME} and rerun.`));
  }
  const h = (body && body.h) || {};
  throw new Error(t(`接口返回错误 ${h.c || '?'}：${h.e || '未知'}（${url}）`, `API error ${h.c || '?'}: ${h.e || 'unknown'} (${url})`));
}

// limit 服务端会截断到 20，翻页靠 has_more + next_cursor，不能靠加大 limit。
// 实测 cursor 分页首尾相接，没有丢条。
async function listAll(tk) {
  const out = [];
  let cursor = '';
  for (let page = 0; page < 200; page++) {
    const url =
      `${API}/notes/list?limit=20&category=recording&sort=create_desc` +
      (cursor ? '&cursor=' + encodeURIComponent(cursor) : '');
    const c = await call(url, tk);
    const arr = c.list || [];
    out.push(...arr);
    if (!c.has_more || !arr.length || !c.next_cursor) break;
    cursor = c.next_cursor;
    await new Promise((r) => setTimeout(r, 300));
  }
  return out;
}

// created_at 是本地时间字符串 "YYYY-MM-DD HH:mm:ss"，按日期前缀比较即可，不要过 Date()。
// timestamps.created_at 是 ISO 字符串，对它用 new Date() 没问题，但那是另一个字段。
function pick(list, opts) {
  return list
    .filter((n) => {
      const d = String(n.created_at || '').slice(0, 10);
      if (opts.since && d < opts.since) return false;
      if (opts.until && d > opts.until) return false;
      if (opts.type && n.note_type !== opts.type) return false;
      return true;
    })
    .sort((a, b) => String(a.created_at).localeCompare(String(b.created_at)));
}

function fileName(n, i) {
  const d = String(n.created_at || '').replace(/[-: ]/g, '');
  const stamp = d.slice(0, 8) + '-' + d.slice(8, 12);
  return `${String(i + 1).padStart(2, '0')}-${stamp}-${safeName(n.title || '未命名')}.md`;
}

async function cmdList(opts) {
  const tk = await getToken();
  const all = await listAll(tk);
  const todo = pick(all, opts);
  console.log(t(`账号下录音笔记 ${all.length} 条，命中筛选 ${todo.length} 条`, `${all.length} voice notes on the account, ${todo.length} match the filter`));
  for (const n of todo.slice(0, opts.limit || 50)) {
    const len = String(n.content || '').length;
    console.log(`${n.created_at}  ${n.note_type || '-'}  ${String(len).padStart(6)} ${t('字', 'ch')}  ${n.title || t('(无标题)', '(untitled)')}`);
  }
}

async function cmdExport(opts) {
  const tk = await getToken();
  const all = await listAll(tk);
  const todo = pick(all, opts);
  if (!todo.length) throw new Error(t('筛选结果为空，检查 --since / --until / --type', 'Filter matched nothing. Check --since / --until / --type'));

  const out = path.resolve(opts.out);
  await mkdir(out, { recursive: true });
  const trDir = path.join(out, 'transcripts');
  if (opts.transcript) await mkdir(trDir, { recursive: true });

  console.log(t(`账号下录音笔记 ${all.length} 条，导出 ${todo.length} 条 → ${out}`, `${all.length} voice notes, exporting ${todo.length} -> ${out}`));
  let ok = 0;
  let bad = 0;

  for (let i = 0; i < todo.length; i++) {
    const n = todo[i];
    const name = fileName(n, i);
    try {
      // notes/list 返回的 content 已是完整正文（与 /notes/<id> 逐行比对只差图片的
      // 签名串），所以列表这一趟就能拿到全文，不必再逐条打详情。
      const md = stripSeek(n.content || '');
      if (!md.trim()) throw new Error(t('正文为空', 'Body is empty'));
      const doc = buildDoc({
        title: n.title || '得到大脑笔记',
        url: HOME + 'note/' + (n.note_id || n.id),
        source: API + '/notes/' + (n.note_id || n.id),
        channel: 'http',
        messages: [{ role: '课堂笔记', body: md }],
        note: '内容由「得到大脑」自动整理，AI 生成部分请核实',
        demote: false,
      });
      await writeFile(path.join(out, name), doc, 'utf8');

      let tr = '';
      if (opts.transcript && n.note_type === 'class_audio') {
        try {
          const orig = await call(`${API}/notes/${n.note_id || n.id}/original`, tk);
          tr = transcriptFrom(orig);
        } catch {
          /* 纯手写或纯图片笔记没有 original，静默跳过 */
        }
        if (tr) await writeFile(path.join(trDir, name), `# ${n.title} 逐字稿\n\n${tr}\n`, 'utf8');
      }

      ok += 1;
      console.log(`${name}  ${t('正文', 'body')} ${md.length}${tr ? ' / ' + t('逐字稿', 'transcript') + ' ' + tr.length : ''}`);
    } catch (e) {
      bad += 1;
      console.log(`${name}  ${t('失败：', 'failed: ')}${String(e.message || e)}`);
    }
    await new Promise((r) => setTimeout(r, 300));
  }
  console.log(`完成 ${ok} 条，失败 ${bad} 条`);
  if (bad) process.exitCode = 1;
}

const { cmd, opts } = parseArgs(process.argv.slice(2));
if (cmd === 'list') await cmdList(opts);
else if (cmd === 'export') await cmdExport(opts);
else {
  console.log(t('用法：', 'Usage:'));
  console.log('  node scripts/biji-notes.mjs list [--limit 20] [--since 2026-11-01] [--type class_audio]');
  console.log('  node scripts/biji-notes.mjs export --since 2026-11-11 --until 2026-11-12 [--out DIR] [--transcript]');
  process.exitCode = cmd === 'help' ? 0 : 2;
}
