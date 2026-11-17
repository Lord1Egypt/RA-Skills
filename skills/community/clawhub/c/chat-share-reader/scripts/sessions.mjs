#!/usr/bin/env node
// 本地会话入口：列出、搜索、导出本机各 AI 编码 agent 的会话记录。
//
// 用法：
//   node sessions.mjs sources
//   node sessions.mjs list [--source <名字>|all] [--limit 20] [--cwd <子串>] [--json]
//   node sessions.mjs search <关键词> [--source ...] [--limit 20] [--cwd <子串>] [--json]
//   node sessions.mjs export [<会话 id 或文件路径>] [--current] [--out DIR] [--stdout] [--full]
//                            [--json] [--redact off|home|strict] [--within 分钟]
//
// export 不给目标时导当前会话：先认宿主 agent 的会话标识环境变量，
// 认不出再按工作目录和最近活跃时间挑，挑中哪个会打印出来。
//
// 和 read.mjs 的分工：那个处理别人发来的分享链接，这个读你自己机器上的会话文件。
import { readdir, stat, writeFile, mkdir } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import * as claudeLocal from './lib/local/claude.mjs';
import * as codexLocal from './lib/local/codex.mjs';
import * as piLocal from './lib/local/pi.mjs';
import * as cursorLocal from './lib/local/cursor.mjs';
import * as zcodeLocal from './lib/local/zcode.mjs';
import * as geminiCliLocal from './lib/local/gemini-cli.mjs';
import * as qwenLocal from './lib/local/qwen.mjs';
import * as clineLocal from './lib/local/cline.mjs';
import * as opencodeLocal from './lib/local/opencode.mjs';
import * as hermesLocal from './lib/local/hermes.mjs';
import * as workbuddyLocal from './lib/local/workbuddy.mjs';
import { makeParser } from './lib/local/jsonl-generic.mjs';
import { lines as readLines, readText } from './lib/local/zst.mjs';
import { buildDoc, safeName, normalizeMessages } from './lib/md.mjs';
import { expandShards, stitchMessages } from './lib/merge.mjs';
import { createRedactor } from './lib/redact.mjs';
import { t, role as rn } from './lib/i18n.mjs';

const home = os.homedir();

// kind: jsonl 每个会话一个文件（或目录树），sqlite 用自带 list/parse 的实现
const SOURCES = {  claude: {
    kind: 'jsonl',
    label: 'Claude Code',
    root: path.join(home, '.claude', 'projects'),
    parser: claudeLocal,
  },
  // 归档会话在 archived_sessions，压缩成 .jsonl.zst，且 Codex 会把读过的会话
  // 解压搬回 sessions 下，两个目录都要扫，否则归档的历史对话搜不到。
  codex: {
    kind: 'jsonl',
    label: 'Codex CLI',
    roots: [path.join(home, '.codex', 'sessions'), path.join(home, '.codex', 'archived_sessions')],
    parser: codexLocal,
  },
  pi: {
    kind: 'jsonl',
    label: 'pi',
    root: path.join(home, '.pi', 'agent', 'sessions'),
    parser: piLocal,
  },
  omp: {
    kind: 'jsonl',
    label: 'Oh My Pi',
    root: path.join(home, '.omp', 'agent', 'sessions'),
    parser: piLocal,
  },
  cursor: { kind: 'sqlite', label: 'Cursor', parser: cursorLocal },
  zcode: { kind: 'sqlite', label: 'zcode', parser: zcodeLocal },
  opencode: { kind: 'sqlite', label: 'opencode', parser: opencodeLocal },
  hermes: { kind: 'sqlite', label: 'Hermes', parser: hermesLocal },

  // WorkBuddy 每条会话一个 jsonl，父目录名是工作区 slug；同级的 <sessionId>/
  // 子目录放工具输出，必须排除，否则会把 tool-results 当成会话。
  workbuddy: {
    kind: 'jsonl',
    label: 'WorkBuddy',
    root: path.join(home, '.workbuddy', 'projects'),
    filter: (f) => /\.jsonl$/.test(f) && !/[\\/]tool-results[\\/]/.test(f),
    parser: workbuddyLocal,
  },

  // 以下源的路径与格式取自 deja-vu 的 registry（社区观测记录），本机无可验证样本
  'gemini-cli': {
    kind: 'jsonl',
    label: 'Gemini CLI',
    root: path.join(home, '.gemini', 'tmp'),
    filter: (f) => /[\\/]chats[\\/][^\\/]+\.jsonl?$/.test(f),
    parser: geminiCliLocal,
  },
  qwen: {
    kind: 'jsonl',
    label: 'Qwen Code',
    root: path.join(home, '.qwen', 'projects'),
    filter: (f) => /[\\/]chats[\\/][^\\/]+\.jsonl$/.test(f),
    parser: qwenLocal,
  },
  cline: {
    kind: 'jsonl',
    label: 'Cline',
    root: path.join(home, '.cline', 'data', 'sessions'),
    filter: (f) => /\.messages\.json$/.test(f),
    refOf: (f) => ({ messagesFile: f, metaFile: f.replace(/\.messages\.json$/, '.json') }),
    parser: clineLocal,
  },
  copilot: {
    kind: 'jsonl',
    label: 'Copilot CLI',
    root: path.join(home, '.copilot', 'session-state'),
    filter: (f) => /events\.jsonl$/.test(f),
    parser: { parse: makeParser('Copilot') },
  },
  commandcode: {
    kind: 'jsonl',
    label: 'Command Code',
    root: path.join(home, '.commandcode', 'projects'),
    filter: (f) => /\.jsonl$/.test(f),
    parser: { parse: makeParser('Command Code') },
  },
  kimi: {
    kind: 'jsonl',
    label: 'Kimi Code',
    root: path.join(home, '.kimi-code', 'sessions'),
    filter: (f) => /wire\.jsonl$/.test(f),
    parser: { parse: makeParser('Kimi') },
  },
  antigravity: {
    kind: 'jsonl',
    label: 'Antigravity',
    root: path.join(home, '.gemini'),
    filter: (f) => /transcript\.jsonl$/.test(f),
    parser: { parse: makeParser('Antigravity') },
  },
};

async function walk(dir, out = [], filter) {
  let entries;
  try {
    entries = await readdir(dir, { withFileTypes: true });
  } catch {
    return out;
  }
  for (const e of entries) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) await walk(p, out, filter);
    else if (filter ? filter(p) : /\.jsonl(\.zst)?$/.test(e.name)) out.push(p);
  }
  return out;
}

// 文件名里最后一段 UUID 就是会话 id，列表和 export 都用它匹配。
// 归档/压缩后的会话是 `<id>.jsonl.zst`，后缀要一起剥掉。
function idOfFile(file) {
  const base = path.basename(file).replace(/\.jsonl(\.zst)?$/i, '');
  const m = base.match(/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/gi);
  return m && m.length ? m[m.length - 1] : base;
}

// Codex 的 fork 分片名形如 `<父线程>_<新线程>.jsonl`，父线程 id 是第一个 UUID。
// 合并一个会话的所有分片时要按它归组。
function familyOfFile(file) {
  const base = path.basename(file).replace(/\.jsonl(\.zst)?$/i, '');
  const m = base.match(/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/i);
  return m ? m[1] : base;
}

// 注入型消息：文件内容包裹、系统提示片段，不能当标题
function isInjected(text) {
  const t = String(text || '').trim();
  return t.startsWith('<') || t.length < 4;
}

function tidy(t) {
  return String(t || '')
    .replace(/[#*`>\n]/g, ' ')
    .replace(/[，。、？！；："'（）《》…—\s]+/g, ' ')
    .trim()
    .slice(0, 40)
    .trim();
}

// 只读文件前部找标题，避免为了列表把所有会话全解析一遍。
// 走 zst.mjs 的行迭代，压缩会话也能取到标题，且不会把整个大文件读进内存。
async function* headLines(file, max = 500) {
  let n = 0;
  for await (const line of readLines(file)) {
    yield line;
    if (++n >= max) return;
  }
}

// 会话真正的线程 id 在文件里，不在文件名上。Codex 的 fork 分片会用新 id 命名，
// 但 session_meta 仍然复制父线程的 id，所以合并分片只能靠它。
async function sessionIdOf(file) {
  try {
    for await (const line of headLines(file, 5)) {
      const s = line.trim();
      if (!s) continue;
      let j;
      try {
        j = JSON.parse(s);
      } catch {
        continue;
      }
      if (j.type === 'session_meta' && j.payload) return j.payload.session_id || j.payload.id || '';
      if (j.type === 'session-meta' && j.sessionId) return j.sessionId;
    }
  } catch {
    /* 读不动就当没有 id */
  }
  return '';
}

async function peekJsonl(file, name) {
  let fallback = '';
  try {
    for await (const line of headLines(file)) {
      const s = line.trim();
      if (!s) continue;
      let j;
      try {
        j = JSON.parse(s);
      } catch {
        continue;
      }
      if (name === 'claude') {
        if (j.type !== 'user' || j.isSidechain) continue;
        const c = j.message && j.message.content;
        const text =
          typeof c === 'string'
            ? c
            : Array.isArray(c)
              ? c.map((x) => (x && x.text) || '').join(' ')
              : '';
        if (text.trim()) return tidy(text);
      } else if (name === 'codex') {
        if (j.type !== 'event_msg' || !j.payload || j.payload.type !== 'item_completed') continue;
        const it = j.payload.item || {};
        if (it.type !== 'UserMessage') continue;
        const text = (it.content || []).map((c) => (c && (c.text || c.Text)) || '').join(' ');
        if (text.trim()) return tidy(text);
      } else if (name === 'workbuddy') {
        if (j.type !== 'message' || j.role !== 'user') continue;
        const text = (Array.isArray(j.content) ? j.content : [])
          .map((c) => (c && typeof c.text === 'string' ? c.text : ''))
          .join(' ')
          .replace(/<system-reminder[\s\S]*?<\/system-reminder>/g, '')
          .replace(/<\/?user_query>/g, '');
        if (isInjected(text)) {
          if (!fallback && text.trim()) fallback = tidy(text);
          continue;
        }
        if (text.trim()) return tidy(text);
      } else {
        // pi / omp
        if (j.type === 'title' && (j.title || j.text)) return tidy(j.title || j.text);
        if (j.type !== 'message') continue;
        const m = j.message || {};
        if (m.role !== 'user') continue;
        const text = Array.isArray(m.content)
          ? m.content.map((c) => (c && c.text) || '').join(' ')
          : String(m.content || '');
        // 首条常是 <file name=...> 这类注入，不是真实提问，跳过；全被跳过时回退到它
        if (isInjected(text)) {
          if (!fallback && text.trim()) fallback = tidy(text);
          continue;
        }
        if (text.trim()) return tidy(text);
      }
    }
  } catch {
    /* 读不动就当没标题 */
  }
  return fallback;
}

async function discover(names, limit = 200) {
  const items = [];

  for (const name of names) {
    const cfg = SOURCES[name];
    if (!cfg) continue;

    if (cfg.kind === 'sqlite') {
      try {
        const rows = await cfg.parser.list({ limit });
        for (const r of rows) items.push({ ...r, name });
      } catch {
        /* 这个源不可用就跳过 */
      }
      continue;
    }

    if (!existsSync(cfg.root) && !(cfg.roots || []).some((r) => existsSync(r))) continue;
    const roots = cfg.roots || [cfg.root];
    for (const root of roots) {
      if (!existsSync(root)) continue;
      for (const f of await walk(root, [], cfg.filter)) {
        let st;
        try {
          st = await stat(f);
        } catch {
          continue;
        }
        items.push({
          source: name,
          name,
          id: idOfFile(f),
          family: familyOfFile(f),
          time: timeFromName(f) || st.mtimeMs,
          size: Math.round(st.size / 1024) + 'K',
          bytes: st.size,
          ref: cfg.refOf ? cfg.refOf(f) : f,
          file: f,
        });
      }
    }
  }

  // 标题要读文件，几千个会话逐个读太贵，交给 list 截断后再取
  return items.sort((a, b) => b.time - a.time);
}

function fmtTime(value) {
  if (!value) return '';
  const ms = typeof value === 'number' ? value : new Date(value).getTime();
  if (!Number.isFinite(ms)) return '';
  const d = new Date(ms);
  const p = (n) => String(n).padStart(2, '0');
  return `${d.getFullYear()}/${p(d.getMonth() + 1)}/${p(d.getDate())} ${p(d.getHours())}:${p(d.getMinutes())}`;
}

function parseArgs(argv) {
  const [cmd, ...rest] = argv;
  const opts = {
    source: 'all',
    limit: 20,
    cwd: '',
    out: './sessions',
    stdout: false,
    full: false,
    json: false,
    current: false,
    redact: 'home',
    within: 60,
  };
  const positional = [];
  for (let i = 0; i < rest.length; i++) {
    const a = rest[i];
    if (a === '--source') opts.source = rest[++i];
    else if (a === '--limit') opts.limit = Number(rest[++i]);
    else if (a === '--cwd') opts.cwd = rest[++i] || '';
    else if (a === '--out') opts.out = rest[++i];
    else if (a === '--stdout') opts.stdout = true;
    else if (a === '--full') opts.full = true;
    else if (a === '--json') opts.json = true;
    else if (a === '--current') opts.current = true;
    else if (a === '--redact') opts.redact = rest[++i] || 'home';
    else if (a === '--no-redact') opts.redact = 'off';
    else if (a === '--within') opts.within = Number(rest[++i]) || 60;
    else positional.push(a);
  }
  const names = opts.source === 'all' ? Object.keys(SOURCES) : [opts.source];
  return { cmd, positional, opts, names };
}

async function cmdList(opts, names) {
  let items = await discover(names, opts.limit);
  if (opts.cwd) {
    const kept = [];
    for (const it of items) {
      if (await matchCwd(it, opts.cwd)) kept.push(it);
    }
    items = kept;
  }
  items = items.slice(0, opts.limit);
  for (const it of items) {
    it.title = await peekJsonl(it.ref, it.name).catch(() => '');
  }
  if (opts.json) {
    return console.log(
      JSON.stringify(
        items.map((x) => ({
          source: x.name,
          id: x.id || idOfFile(x.ref),
          time: fmtTime(x.time),
          title: x.title || t('(无标题)', '(untitled)'),
          count: x.count,
          ref: x.file || x.ref,
        })),
        null,
        2
      )
    );
  }
  if (!items.length) return console.log(t('没有找到任何会话', 'No sessions found'));
  // 按时间混排时同源不连续，分组标题会重复出现，改成每行带来源
  for (const x of items) {
    const id = x.id ? String(x.id) : idOfFile(x.ref);
    const size = x.size || (x.count ? x.count + t('条', '') : '');
    const src = String(SOURCES[x.name].label || x.name).padEnd(11);
    console.log(`${fmtTime(x.time)}  ${src} ${String(size).padStart(7)}  ${id}  ${x.title || t('(无标题)', '(untitled)')}`);
  }
}

// 关键词只匹配对话正文，不匹配文件原文。
//
// 原来的实现直接对 jsonl 原文 indexOf，会把 role=developer 的系统提示和记忆注入
// 当成命中：记忆里写过一次项目路径，就能让几十个无关会话全部命中。所以这里先
// parse 出 messages，再在 body 里找。
//
// 代价是要读文件。普通文件先用原文预筛一次压掉大部分无关会话；压缩会话跳过
// 预筛直接 parse，避免解压两遍。
function snippet(text, keyword, span = 60) {
  const i = text.indexOf(keyword);
  if (i < 0) return '';
  return text
    .slice(Math.max(0, i - span), i + keyword.length + span)
    .replace(/\s+/g, ' ')
    .trim();
}

// 文件名里带 ISO 时间的源（codex 的 rollout-2026-10-05T22-24-13、pi 的 2026-11-01T13-34-07）
// 优先用它，因为归档 .zst 的 mtime 是解压时间，按 mtime 排会把旧会话顶到最前。
function timeFromName(file) {
  const m = path.basename(file).match(/(\d{4})-(\d{2})-(\d{2})T(\d{2})-(\d{2})-(\d{2})/);
  if (!m) return 0;
  const t = new Date(`${m[1]}-${m[2]}-${m[3]}T${m[4]}:${m[5]}:${m[6]}`).getTime();
  return Number.isFinite(t) ? t : 0;
}

// Windows 上 cwd 存的是反斜杠，用户敲的可能是正斜杠，两边都归一化再比
function normPath(p) {
  return String(p || '').replace(/\\/g, '/').toLowerCase();
}

async function matchCwd(item, needle) {
  const lower = normPath(needle);
  if (item.meta && normPath(item.meta.cwd).includes(lower)) return true;
  if (normPath(item.file).includes(lower)) return true;
  // 有些源（WorkBuddy）把会话按工作区 slug 分目录，目录名是 cwd 转写来的，
  // 路径里没有可读的工作目录，只能按 slug 比。
  if (item.file && path.basename(path.dirname(item.file)) === slugOfCwd(needle)) return true;
  // 路径里没写工作目录的源（codex/claude），读头几行的 cwd
  try {
    for await (const line of headLines(item.file, 5)) {
      const s = line.trim();
      if (!s) continue;
      let j;
      try {
        j = JSON.parse(s);
      } catch {
        continue;
      }
      const cwd = (j.payload && j.payload.cwd) || j.cwd;
      if (cwd) return normPath(cwd).includes(lower);
    }
  } catch {
    /* 读不动就按不匹配处理 */
  }
  return false;
}

// E:\01-project\00-workspace -> e-01-project-00-workspace
function slugOfCwd(p) {
  return String(p || '')
    .toLowerCase()
    .replace(/[\\/:]+/g, '-')
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '');
}

// 认当前会话。两条依据，先准确后兜底：
//   1. 宿主 agent 把自己的会话 id 传进环境变量，最准
//   2. 没有环境变量时，按工作目录匹配 + 最近活跃时间挑一个
// 第二条是启发式的：同一个目录同时开着两个 agent 会话时可能挑错，所以挑中哪个要报出来。
const CURRENT_ENV = [
  ['workbuddy', ['CODEBUDDY_SESSION_ID', 'WORKBUDDY_SESSION_ID']],
  ['claude', ['CLAUDE_SESSION_ID', 'CLAUDE_CODE_SESSION_ID']],
  ['codex', ['CODEX_THREAD_ID', 'CODEX_SESSION_ID']],
  ['qwen', ['QWEN_SESSION_ID']],
  ['kimi', ['KIMI_SESSION_ID']],
  ['gemini-cli', ['GEMINI_SESSION_ID']],
  ['cursor', ['CURSOR_SESSION_ID']],
];

async function findCurrent(opts, names) {
  const available = SESSION_ENV_SCAN(names);

  for (const [name, vars] of available) {
    for (const v of vars) {
      const id = String(process.env[v] || '').trim();
      if (!id || id.length < 6) continue;
      const items = await discover([name]);
      const hit = items.filter(
        (x) => String(x.id || '').includes(id) || String(x.file || x.ref || '').includes(id)
      );
      if (hit.length) return { picked: hit, items, how: `${name} ${id} · ${v}` };
    }
  }

  const items = await discover(names);
  const windowMs = Math.max(1, opts.within || 60) * 60000;
  const now = Date.now();
  const recent = items.filter((x) => now - x.time <= windowMs);
  if (!recent.length) {
    throw new Error(
      t(
        `最近 ${opts.within} 分钟内没有活跃会话，用 list 找一个再指定 id`,
        `No session active within ${opts.within} min; run list and pass an id`
      )
    );
  }

  const cwd = opts.cwd || process.cwd();
  const matched = [];
  for (const it of recent.slice(0, 20)) {
    if (await matchCwd(it, cwd)) matched.push(it);
  }
  const pool = matched.length ? matched : recent;
  const seed = pool[0];
  return {
    picked: [seed],
    items,
    how: `${seed.source} ${seed.id} · ${cwd} · ${matched.length ? 'cwd' : 'recent'}`,
  };
}

function SESSION_ENV_SCAN(names) {
  return CURRENT_ENV.filter(([name]) => names.includes(name));
}

async function cmdSearch(keyword, opts, names) {
  if (!keyword) throw new Error(t('要给一个关键词', 'A keyword is required'));
  const items = await discover(names);
  const hits = [];
  const failed = [];

  for (const it of items) {
    if (hits.length >= opts.limit) break;
    if (opts.cwd && !(await matchCwd(it, opts.cwd))) continue;

    const compressed = /\.zst$/i.test(it.file || '');
    if (!compressed) {
      const raw = await readText(it.file).catch(() => '');
      if (!raw.includes(keyword)) continue;
    }

    const cfg = SOURCES[it.name];
    let parsed;
    try {
      parsed = await cfg.parser.parse(it.ref);
    } catch (e) {
      failed.push({ file: it.file, error: String(e.message || e) });
      continue;
    }
    const matched = parsed.messages.filter((m) => m.body.includes(keyword));
    if (!matched.length) continue;
    // 文件 mtime 会被压缩、重写改掉，展示用会话内第一条消息的时间
    const startedAt = parsed.messages.find((m) => m.at)?.at || '';
    hits.push({ ...it, title: parsed.title, meta: parsed.meta, matched, startedAt });
  }

  if (opts.json) {
    return console.log(
      JSON.stringify(
        hits.map((h) => ({
          source: h.source,
          id: h.id,
          title: h.title,
          time: fmtTime(h.startedAt || h.time),
          cwd: (h.meta && h.meta.cwd) || '',
          ref: h.file || h.ref,
          matched: h.matched.map((m) => ({ role: rn(m.role), time: m.time, snippet: snippet(m.body, keyword) })),
        })),
        null,
        2
      )
    );
  }

  if (!hits.length) {
    console.log(t('没有命中', 'no matches'));
    if (failed.length) console.log(t(`（${failed.length} 个会话解析失败，可用 --source 缩小范围重试）`, `(${failed.length} sessions failed to parse; narrow with --source and retry)`));
    return;
  }
  for (const h of hits) {
    console.log(
      `${fmtTime(h.startedAt || h.time)}  ${String(h.source).padEnd(9)} ${t('命中', 'hits')} ${h.matched.length}  「${h.title || t('(无标题)', '(untitled)')}」`
    );
    for (const m of h.matched.slice(0, 3)) {
      console.log(`  ${rn(m.role)}: ${snippet(m.body, keyword)}`);
    }
    if (h.matched.length > 3) console.log(`  …另有 ${h.matched.length - 3} 条`);
    console.log(`  ${h.file || h.ref}`);
  }
  if (failed.length) console.log(`\n${failed.length} 个会话解析失败：${failed.map((f) => path.basename(f.file)).join(', ')}`);
}

// 直接给文件路径时，先按目录名认源；认不出再看内容特征。
// 目录判断要做分隔符归一化，Windows 上传进来的路径常是正斜杠。
async function guessSource(file) {
  const norm = String(file).replace(/\\/g, '/');
  for (const n of ['codex', 'claude', 'omp', 'pi', 'workbuddy']) {
    if (norm.includes(`/.${n}/`)) return n;
  }
  try {
    for await (const line of headLines(file, 3)) {
      const s = line.trim();
      if (!s) continue;
      if (s.includes('"type":"session-meta"')) return 'workbuddy';
      if (s.includes('"type":"session_meta"')) return 'codex';
      if (/"type":"(user|assistant)"/.test(s)) return 'claude';
    }
  } catch {
    /* 读不动就按默认 */
  }
  return 'claude';
}

async function cmdExport(target, opts, names) {
  // 不给目标就是导当前会话。零参数是 agent 在会话里最自然的用法：
  // 「把这段对话存下来」，不应该要求它先去 list 查一个 id。
  const wantCurrent = opts.current || !target;
  let picked = [];

  if (wantCurrent) {
    const cur = await findCurrent(opts, names);
    console.error(t(`当前会话：${cur.how}`, `current session: ${cur.how}`));
    picked = await expandShards(cur.picked, cur.items, sessionIdOf);
  } else if (existsSync(target)) {
    const name = await guessSource(target);
    picked = [{ name, ref: target, file: target, time: 0 }];
  } else {
    const items = await discover(names);
    picked = items.filter(
      (x) =>
        (x.id && String(x.id).includes(target)) ||
        (x.family && String(x.family).includes(target)) ||
        (x.ref && typeof x.ref === 'string' && path.basename(x.ref).includes(target))
    );
    if (!picked.length) throw new Error(t('找不到匹配的会话：', 'No matching session: ') + target);
    picked = await expandShards(picked, items, sessionIdOf);
  }

  const cfg = SOURCES[picked[0].name];
  if (!cfg) throw new Error(t('未知来源：', 'Unknown source: ') + picked[0].name);

  const parts = [];
  for (const p of picked) parts.push(await cfg.parser.parse(p.ref, { full: opts.full }));

  const merged = stitchMessages(parts);
  const messages = normalizeMessages(merged.messages);
  const note = merged.note;
  if (!messages.length) throw new Error(t('这个会话里没有可导出的对话', 'This session has no exportable messages'));

  const first = messages.find((m) => m.role === '用户');
  const title = (first ? first.body : messages[0].body)
    .replace(/[#*`>\n]/g, ' ')
    .replace(/[，。、？！；："'（）《》…—\s]+/g, ' ')
    .trim()
    .slice(0, 24)
    .trim();

  // 标题里常带路径（第一句就是「帮我看看 C:\Users\x\... 报错」），
  // 落成文件名前也要过一遍脱敏，否则用户名会留在文件名上。
  const r = createRedactor(opts.redact);
  const safeTitle = r.apply(title);

  if (opts.json) {
    return console.log(
      JSON.stringify(
        {
          source: picked[0].name,
          title: safeTitle,
          // segments 是给下游继续读文件的句柄，保持原样不脱敏；
          // 脱敏只作用于会被展示、复制、分享的内容字段。
          segments: picked.map((p) => p.file || String(p.ref)),
          redact: r.level,
          messages: messages.map((m) => ({ role: m.role, time: m.at || m.time, body: r.apply(m.body) })),
        },
        null,
        2
      )
    );
  }

  const md = buildDoc({
    title,
    url: picked.map((p) => p.file || String(p.ref)).join('\n  '),
    source: picked.length > 1 ? `合并 ${picked.length} 个分片` : '',
    channel: 'local/' + picked[0].name,
    messages,
    note,
    redact: opts.redact,
  });

  if (opts.stdout) return console.log(md);
  await mkdir(opts.out, { recursive: true });
  const out = path.resolve(opts.out, safeName(safeTitle) + '.md');
  await writeFile(out, md, 'utf8');
  console.log(
    `OK ${picked[0].name} ${messages.length} 条${picked.length > 1 ? `（合并 ${picked.length} 个分片）` : ''}${opts.redact === 'off' ? '' : t(` · 脱敏 ${opts.redact}`, ` · redacted ${opts.redact}`)} -> ${out}`
  );
}

function cmdSources() {
  for (const [name, cfg] of Object.entries(SOURCES)) {
    const roots = cfg.roots || (cfg.root ? [cfg.root] : []);
    let where = roots.join('  +  ');
    let state = '';
    if (cfg.kind === 'sqlite') {
      where = (cfg.parser.dbPath && cfg.parser.dbPath()) || '(未找到数据库)';
      state = where.startsWith('(') ? t('未安装', 'absent') : t('可用', 'usable');
    } else {
      state = roots.some((r) => existsSync(r)) ? t('有目录', 'found') : t('无目录', 'missing');
    }
    console.log(`${name.padEnd(7)} ${cfg.label.padEnd(12)} ${state.padEnd(6)} ${where}`);
  }
}

const { cmd, positional, opts, names } = parseArgs(process.argv.slice(2));

try {
  if (cmd === 'list') await cmdList(opts, names);
  else if (cmd === 'search') await cmdSearch(positional[0], opts, names);
  else if (cmd === 'export') await cmdExport(positional[0], opts, names);
  else if (cmd === 'sources') cmdSources();
  else {
    console.error(
      '用法：\n' +
        '  node sessions.mjs sources\n' +
        '  node sessions.mjs list [--source <名字>|all] [--limit 20] [--cwd <子串>] [--json]\n' +
        '  node sessions.mjs search <关键词> [--source ...] [--limit 20] [--cwd <子串>] [--json]\n' +
        '  node sessions.mjs export [<id 或路径>] [--current] [--out DIR] [--stdout] [--full] [--json]\n' +
        '                          [--redact off|home|strict] [--within 60]\n' +
        '\n' +
        'export 不给目标时导当前会话（认宿主 agent 的会话标识，认不出按工作目录 + 最近活跃挑）。\n' +
        '脱敏默认 home：家目录换成 ~，strict 再遮邮箱、令牌、内网 IP，off 导出原文。'
    );
    process.exit(2);
  }
} catch (e) {
  console.error('FAIL :: ' + String(e.message || e));
  process.exit(1);
}
