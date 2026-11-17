#!/usr/bin/env node
// cgartlab-search dispatcher — zero-dependency Node ESM (Node 18+ global fetch).
// Works in harnesses whose shell can reach the network (Claude Code, Codex, opencode, terminal).
// In DSH's sandboxed shell (no outbound network) use web_fetch instead — see references/backends.md.
//
// Usage:
//   node search.mjs <backends> "<query>" [--limit N] [--topic T] [--library ID] [--news]
//   backends: comma list from brave,exa,context7,tencent,zhihu,bing,qqnews,hupu,so,github,hn
//
// Keyed backends read env vars BRAVE_SEARCH_API_KEY EXA_API_KEY CONTEXT7_API_KEY
// TENCENT_NEWS_KEY ZHIHU_API_KEY (fallback: secrets.json next to SKILL.md).
// Key-less backends (bing,context7,qqnews,hupu,so,github,hn) need nothing.
// Output: one line of normalized JSON on stdout. Exit 0 if any backend returned results.
import { readFileSync } from 'node:fs';
import { execFile } from 'node:child_process';
import { homedir } from 'node:os';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const here = dirname(fileURLToPath(import.meta.url));
const argv = process.argv.slice(2);
const flag = (n) => { const i = argv.indexOf(n); return i >= 0 ? (argv.splice(i, 2)[1] ?? null) : null; };
const limit = +(flag('--limit') ?? 5);
const topic = flag('--topic');
const libOverride = flag('--library');
const wantNews = argv.includes('--news'); if (wantNews) argv.splice(argv.indexOf('--news'), 1);
const backends = (argv[0] || '').split(',').map(s => s.trim()).filter(Boolean);
const query = argv.slice(1).join(' ').trim();

const ENV_KEYS = { brave: 'BRAVE_SEARCH_API_KEY', exa: 'EXA_API_KEY', context7: 'CONTEXT7_API_KEY', tencent: 'TENCENT_NEWS_KEY', zhihu: 'ZHIHU_API_KEY' };
const FILE_KEYS = { brave: 'brave_api_key', exa: 'exa_api_key', context7: 'context7_api_key', tencent: 'tencent_news_key', zhihu: 'zhihu_api_key' };
const secrets = {};
for (const b of Object.keys(ENV_KEYS)) { const v = process.env[ENV_KEYS[b]]; if (v) secrets[b] = v; }
// secrets.json lives next to SKILL.md (skill root); a copy beside this script still works.
const SECRETS_CANDIDATES = [join(here, 'secrets.json'), join(here, '..', 'secrets.json')];
for (const p of SECRETS_CANDIDATES) {
  try {
    const f = JSON.parse(readFileSync(p, 'utf8'));
    for (const b of Object.keys(FILE_KEYS)) if (!secrets[b] && f[FILE_KEYS[b]]) secrets[b] = f[FILE_KEYS[b]];
    break;
  } catch { /* try next candidate; env-only mode when none parse */ }
}
const enc = s => encodeURIComponent(s);
const unent = s => s.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"')
  .replace(/&#39;/g, "'").replace(/&#x27;/g, "'").replace(/&#x2F;/g, '/').replace(/&amp;/g, '&');

// --- A. key-less backends ---

async function bing() {
  const r = await fetch(`https://cn.bing.com/search?q=${enc(query)}&format=rss`);
  if (!r.ok) return { error: `HTTP ${r.status}` };
  const xml = await r.text();
  const out = [];
  const re = /<item>([\s\S]*?)<\/item>/g; let m;
  const field = (src, tag) => {
    const mm = src.match(new RegExp(`<${tag}[^>]*>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/${tag}>`));
    return mm ? unent(mm[1].trim()) : '';
  };
  while ((m = re.exec(xml)) && out.length < limit) {
    const t = field(m[1], 'title'), u = field(m[1], 'link');
    if (!t || !u) continue;
    out.push({ backend: 'bing', type: wantNews ? 'news' : 'web', title: t, url: u,
      snippet: field(m[1], 'description'), published: field(m[1], 'pubDate') || null });
  }
  return { results: out };
}

async function qqnews() {
  const r = await fetch(`https://r.inews.qq.com/gw/event/hot_ranking_list?page_size=${Math.max(limit, 10)}`);
  if (!r.ok) return { error: `HTTP ${r.status}` };
  const j = await r.json();
  const list = (j.idlist?.[0]?.newslist) || [];
  const out = list.filter(x => x.url && x.title).slice(0, limit).map(x => ({
    backend: 'qqnews', type: 'news', title: x.title, url: x.url,
    snippet: String(x.abstract || '').slice(0, 300), published: x.time || null,
    source: x.card?.chlname || null, score: x.readCount ?? null,
  }));
  return { results: out, note: '腾讯新闻热榜（全站热门，未按 query 过滤）' };
}

async function hupu() {
  const r = await fetch('https://soccer.hupu.com/');
  if (!r.ok) return { error: `HTTP ${r.status}` };
  const html = await r.text();
  const re = /<a[^>]+href=["'](https:\/\/bbs\.hupu\.com\/\d+\.html)["'][^>]*>([\s\S]*?)<\/a>/g;
  const seen = new Set(); const out = []; let m;
  while ((m = re.exec(html))) {
    const title = unent(m[2].replace(/<[^>]+>/g, '')).trim();
    if (title.length < 8 || seen.has(m[1])) continue;
    seen.add(m[1]);
    out.push({ backend: 'hupu', type: 'news', title, url: m[1], snippet: '' });
    if (out.length >= limit) break;
  }
  return out.length ? { results: out } : { error: 'no items parsed (page layout changed?)' };
}

async function so() {
  const r = await fetch(`https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=relevance&q=${enc(query)}&site=stackoverflow&pagesize=${limit}`);
  if (!r.ok) return { error: `HTTP ${r.status}` };
  const j = await r.json();
  return { results: (j.items || []).map(x => ({
    backend: 'so', type: 'qa', title: unent(x.title || ''), url: x.link,
    snippet: `[${(x.tags || []).slice(0, 5).join(', ')}] ${x.is_answered ? 'answered' : 'unanswered'} · ${x.view_count} views`,
    score: x.score ?? null,
    published: x.creation_date ? new Date(x.creation_date * 1000).toISOString() : null,
  })) };
}

async function github() {
  const r = await fetch(`https://api.github.com/search/repositories?q=${enc(query)}&sort=stars&per_page=${limit}`,
    { headers: { Accept: 'application/vnd.github+json' } });
  if (r.status === 403) return { error: 'rate-limited (unauthenticated: ~10 search req/min)' };
  if (!r.ok) return { error: `HTTP ${r.status}` };
  const j = await r.json();
  return { results: (j.items || []).map(x => ({
    backend: 'github', type: 'repo', title: x.full_name, url: x.html_url,
    snippet: String(x.description || '').slice(0, 300), score: x.stargazers_count ?? null,
    published: x.pushed_at || null,
  })) };
}

async function hn() {
  const r = await fetch(`https://hn.algolia.com/api/v1/search?query=${enc(query)}&hitsPerPage=${limit}`);
  if (!r.ok) return { error: `HTTP ${r.status}` };
  const j = await r.json();
  return { results: (j.hits || []).filter(x => x.title).map(x => ({
    backend: 'hn', type: 'community', title: x.title,
    url: x.url || `https://news.ycombinator.com/item?id=${x.objectID}`,
    snippet: `${x.points || 0} points · ${x.num_comments || 0} comments`,
    published: x.created_at || null,
  })) };
}

async function context7() {
  let id = libOverride;
  let title = id;
  if (!id) {
    const r = await fetch(`https://context7.com/api/v1/search?query=${enc(query)}`);
    if (!r.ok) return { error: `search HTTP ${r.status}` };
    const j = await r.json();
    const top = (j.results || []).find(x => x.verified) || (j.results || [])[0];
    if (!top) return { error: 'no library found' };
    id = top.id; title = top.title || id;
  }
  const idEnc = enc(id.replace(/^\//, ''));
  const url = `https://context7.com/api/v1/${idEnc}?tokens=4000` + (topic ? `&topic=${enc(topic)}` : '');
  const r2 = await fetch(url);
  if (!r2.ok) return { error: `fetch HTTP ${r2.status}` };
  const content = await r2.text();
  return { results: [{ backend: 'context7', type: 'docs', library: id, title, url: `https://context7.com/${id}`, content }] };
}

// --- B. keyed backends ---

async function brave() {
  if (!secrets.brave) return { error: 'missing key' };
  const path = wantNews ? 'news/search' : 'web/search';
  const r = await fetch(`https://api.search.brave.com/res/v1/${path}?q=${enc(query)}&count=${limit}`,
    { headers: { 'X-Subscription-Token': secrets.brave, Accept: 'application/json' } });
  if (!r.ok) return { error: `HTTP ${r.status}` };
  const j = await r.json();
  const arr = (wantNews ? j.news?.results : j.web?.results) || [];
  return { results: arr.map(x => ({ backend: 'brave', type: wantNews ? 'news' : 'web', title: x.title, url: x.url, snippet: x.description || x.text || '', published: x.age || x.publish_date || null })) };
}

async function exa() {
  if (!secrets.exa) return { error: 'missing key' };
  const r = await fetch('https://api.exa.ai/search', {
    method: 'POST',
    headers: { 'x-api-key': secrets.exa, 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, numResults: limit, type: 'auto', contents: { text: true, maxCharacters: 1000 } }),
  });
  if (!r.ok) return { error: `HTTP ${r.status}` };
  const j = await r.json();
  return { results: (j.results || []).map(x => ({ backend: 'exa', type: 'web', title: x.title, url: x.url, snippet: (x.text || '').slice(0, 300), score: x.score ?? null, published: x.publishedDate || null })) };
}

async function tencent() {
  // tencent-news-cli is a Go binary that prints human-readable text, not JSON, and
  // has no --json/--format flag (verified v1.0.17). Its key lives in the CLI's own
  // config (HKCU\Environment on Windows), NOT here — so we never read a secret for
  // it and instead detect an auth failure from the CLI's own message.
  const n = Math.max(1, Math.min(50, limit));
  // `hot` takes no query, so it is only used when there is no keyword. `--news` does
  // NOT force the hot list: every tencent result is already type=news, and ignoring a
  // real keyword would return unrelated headlines.
  const args = query ? ['search', query, '--limit', String(n)]
    : ['hot', '--limit', String(n)];
  const run = (cmd, argv) => new Promise((resolve) => {
    execFile(cmd, argv, { timeout: 30000, maxBuffer: 4 * 1024 * 1024, windowsHide: true },
      (err, stdout, stderr) => resolve({ err, stdout: stdout || '', stderr: stderr || '' }));
  });
  // Resolution order: explicit override → PATH → the installer's own directory.
  // The installer drops the binary in ~/.tencent-news-cli/bin/ without touching PATH,
  // so a PATH-only lookup reports "not found" on a perfectly working install.
  const exeName = process.platform === 'win32' ? 'tencent-news-cli.exe' : 'tencent-news-cli';
  const candidates = [
    process.env.TENCENT_NEWS_CLI_PATH,
    'tencent-news-cli',
    join(homedir(), '.tencent-news-cli', 'bin', exeName),
  ].filter(Boolean);
  let err, stdout = '', stderr = '', used = candidates[0];
  for (const cmd of candidates) {
    ({ err, stdout, stderr } = await run(cmd, args));
    used = cmd;
    if (err && (err.code === 'ENOENT' || err.code === 'EACCES')) continue; // try next candidate
    break;
  }
  if (err && (err.code === 'ENOENT' || err.code === 'EACCES')) {
    return { error: `tencent-news-cli not found (tried: ${candidates.join(', ')}) — install from https://mat1.gtimg.com/qqcdn/qqnews/cli/hub/tencent-news/setup.ps1` };
  }
  const text = `${stdout}\n${stderr}`;
  if (/未设置 API Key|not set/i.test(text)) {
    return { error: `API key not configured — run: ${used} apikey-set <KEY>` };
  }
  if (/API Key 无效|invalid api key|unauthorized|401|403/i.test(text)) {
    return { error: 'API key invalid or unauthorized' };
  }
  if (err && !stdout.trim()) return { error: `CLI failed: ${String(err.message || err).slice(0, 120)}` };
  if (/未找到与/.test(stdout)) return { results: [] };

  // Parse blocks: "N. 标题：...\n   摘要: ...\n   来源: ...\n   发布时间: ...\n   链接: ..."
  const out = [];
  const blocks = stdout.split(/\n(?=\d+\.\s*标题：)/);
  for (const b of blocks) {
    const grab = (label) => {
      const m = b.match(new RegExp(`^\\s*${label}[:：]\\s*(.+)$`, 'm'));
      return m ? m[1].trim() : '';
    };
    // The title line is prefixed with "N. " ("1. 标题：..."), unlike the other fields.
    const titleMatch = b.match(/^\s*\d+\.\s*标题[:：]\s*(.+)$/m);
    const title = titleMatch ? titleMatch[1].trim() : '';
    const url = grab('链接');
    if (!title || !url) continue;
    out.push({
      backend: 'tencent',
      type: 'news',
      title,
      url,
      snippet: grab('摘要').replace(/\.\.\.$/, ''),
      published: grab('发布时间') || null,
      source: grab('来源') || null,
    });
    if (out.length >= n) break;
  }
  return { results: out };
}
async function zhihu() {
  if (!secrets.zhihu) return { error: 'missing key' };
  // Zhihu OpenAPI global search — searches the whole public web, not just zhihu.com.
  // Auth is Bearer + a request timestamp; params are PascalCase (Query/Count/Filter/SearchDB).
  // Count is clamped to 1-20 server-side; we clamp locally too so --limit stays honest.
  const n = Math.max(1, Math.min(20, limit));
  const params = new URLSearchParams({ Query: query, Count: String(n) });
  if (wantNews) params.set('SearchDB', 'realtime');
  const r = await fetch(`https://developer.zhihu.com/api/v1/content/global_search?${params}`, {
    headers: {
      Authorization: `Bearer ${secrets.zhihu}`,
      'X-Request-Timestamp': String(Math.floor(Date.now() / 1000)),
    },
  });
  if (!r.ok) return { error: `HTTP ${r.status}` };
  const j = await r.json();
  if (j.Code !== 0) return { error: `API Code ${j.Code}: ${j.Message || 'unknown'}` };
  const items = j.Data?.Items || [];
  return { results: items.map(x => ({
    backend: 'zhihu',
    type: wantNews ? 'news' : 'web',
    title: x.Title || '',
    url: x.Url || '',
    snippet: (x.ContentText || '').slice(0, 300),
    published: x.EditTime ? new Date(x.EditTime * 1000).toISOString() : null,
    author: x.AuthorName || null,
    score: x.RankingScore ?? null,
  })) };
}

const ADAPTERS = { bing, qqnews, hupu, so, github, hn, context7, brave, exa, tencent, zhihu };
const out = { query, backends, results: [], errors: [], notes: [] };
for (const b of backends) {
  if (!ADAPTERS[b]) out.errors.push({ backend: b, error: `unknown backend (choose: ${Object.keys(ADAPTERS).join(',')})` });
}
await Promise.all(backends.filter(b => ADAPTERS[b]).map(async (b) => {
  try {
    const res = await ADAPTERS[b]();
    if (res.results) out.results.push(...res.results);
    if (res.error) out.errors.push({ backend: b, error: res.error });
    if (res.note) out.notes.push({ backend: b, note: res.note });
  } catch (e) {
    out.errors.push({ backend: b, error: String(e?.message || e) });
  }
}));
process.stdout.write(JSON.stringify(out));
process.exit(out.results.length ? 0 : 1);