#!/usr/bin/env node

import { mkdir, readFile, writeFile } from "node:fs/promises";
import { homedir } from "node:os";
import path from "node:path";
import { pathToFileURL } from "node:url";

const DEFAULT_BASE_URL = "http://127.0.0.1:17777";
const SEARCH_BASE_URL = "https://www.douyin.com/jingxuan/search";
const SESSION_PREFIX = "douyin-live-hot-free";
const GROUP_TITLE = "抖音实时热点搜索";

const EXTRACT_SCRIPT = `(() => {
  const input = document.querySelector('[data-e2e="searchbar-input"]');
  if (!input) return { ok: false, reason: 'search-input-not-found', url: location.href };

  const items = [...document.querySelectorAll('.search-result-card')].map((card) => {
    const host = card.closest('[id^="waterfall_item_"]');
    const contentId = host?.id?.replace('waterfall_item_', '') || '';
    const lines = card.innerText.split(/\\n+/).map((line) => line.trim()).filter(Boolean);
    const authorIndex = lines.findLastIndex((line) => line.startsWith('@'));
    if (!contentId || lines.length < 5 || authorIndex < 3) return null;

    const contentType = lines[0] === '图文' ? 'image' : 'video';
    const publishedText = lines.slice(authorIndex + 1).find((line) => line.startsWith('·'))?.replace(/^·\\s*/, '') || null;
    return {
      contentId,
      contentType,
      duration: contentType === 'video' ? lines[0] : null,
      visibleLikesText: lines[1],
      title: lines.slice(2, authorIndex).join(' '),
      author: lines[authorIndex].replace(/^@/, ''),
      publishedText,
      coverUrl: card.querySelector('img[src]')?.src || null,
      url: 'https://www.douyin.com/' + (contentType === 'image' ? 'note/' : 'video/') + contentId,
    };
  }).filter(Boolean).map((item, index) => ({ position: index + 1, ...item }));

  return {
    ok: true,
    keyword: input.value.trim(),
    url: location.href,
    items,
  };
})()`;

function usage() {
  console.log(`Usage:
  douyin-live-hot-free list
  douyin-live-hot-free search --keyword <text> --browser <name> [--limit 20] [--output <dir>] [--keep-tab]
  douyin-live-hot-free search --keyword <text> --browser-id <id> [--limit 20] [--output <dir>] [--keep-tab]
  douyin-live-hot-free render --input <search-results.json> --output <dir>
`);
}

function parseArgs(argv) {
  const [verb = "help", ...rest] = argv;
  const options = {};
  for (let index = 0; index < rest.length; index += 1) {
    const arg = rest[index];
    if (arg === "--keep-tab") {
      options.keepTab = true;
      continue;
    }
    if (!arg.startsWith("--")) throw new Error(`Unexpected argument: ${arg}`);
    const key = arg.slice(2).replaceAll("-", "_");
    const value = rest[index + 1];
    if (!value || value.startsWith("--")) throw new Error(`Missing value for ${arg}`);
    options[key] = value;
    index += 1;
  }
  return { verb, options };
}

function parseCount(value) {
  const text = String(value || "").trim();
  const match = text.match(/^([0-9]+(?:\.[0-9]+)?)(万|亿)?$/);
  if (!match) return null;
  const multiplier = match[2] === "亿" ? 100_000_000 : match[2] === "万" ? 10_000 : 1;
  return Math.round(Number(match[1]) * multiplier);
}

function buildSearchUrl(keyword) {
  const value = String(keyword || "").trim();
  if (!value) throw new Error("--keyword is required for search.");
  return `${SEARCH_BASE_URL}/${encodeURIComponent(value)}?type=general`;
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function escapeMarkdown(value) {
  return String(value ?? "").replaceAll("|", "\\|").replaceAll("\n", " ");
}

function timestampSlug(date = new Date()) {
  return date.toISOString().replace(/[:.]/g, "-");
}

function localTime(date = new Date()) {
  return new Intl.DateTimeFormat("zh-CN", {
    timeZone: "Asia/Shanghai",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  }).format(date);
}

function delay(milliseconds) {
  return new Promise((resolve) => setTimeout(resolve, milliseconds));
}

async function readToken() {
  if (process.env.EASY_WEBBRIDGE_TOKEN) return process.env.EASY_WEBBRIDGE_TOKEN;
  const tokenPath = path.join(homedir(), ".easy-webbridge", "bridge-token");
  try {
    return (await readFile(tokenPath, "utf8")).trim();
  } catch {
    throw new Error("Easy WebBridge token not found. Install and start Easy WebBridge first.");
  }
}

async function apiRequest(endpoint, init = {}) {
  const baseUrl = process.env.EASY_WEBBRIDGE_URL || DEFAULT_BASE_URL;
  const response = await fetch(`${baseUrl}${endpoint}`, {
    ...init,
    headers: {
      Authorization: `Bearer ${await readToken()}`,
      "Content-Type": "application/json",
      ...(init.headers || {}),
    },
  });
  let body;
  try {
    body = await response.json();
  } catch {
    body = {};
  }
  if (!response.ok) throw new Error(body.error || `Easy WebBridge HTTP ${response.status}`);
  return body;
}

async function command(browserId, action, args = {}, timeoutMs = 20_000) {
  const response = await apiRequest(`/v1/browsers/${encodeURIComponent(browserId)}/commands`, {
    method: "POST",
    body: JSON.stringify({ action, args, timeoutMs }),
  });
  return response.result;
}

async function onlineBrowsers() {
  const result = await apiRequest("/v1/browsers");
  return (result.browsers || []).filter((browser) => browser.online);
}

async function selectBrowser(options) {
  const browsers = await onlineBrowsers();
  if (browsers.length === 0) throw new Error("No online Easy WebBridge browser found.");
  if (options.browser_id) {
    const match = browsers.find((browser) => browser.browserId === options.browser_id);
    if (!match) throw new Error(`Browser is not online: ${options.browser_id}`);
    return match;
  }
  if (options.browser) {
    const matches = browsers.filter((browser) => browser.displayName === options.browser);
    if (matches.length !== 1) throw new Error(`Expected one online browser named '${options.browser}', found ${matches.length}.`);
    return matches[0];
  }
  if (browsers.length === 1) return browsers[0];
  const choices = browsers.map((browser) => `${browser.displayName} (${browser.browserId})`).join(", ");
  throw new Error(`Multiple browsers are online. Pass --browser or --browser-id. Available: ${choices}`);
}

async function waitForSearchResults(browserId, tabId, keyword) {
  for (let attempt = 0; attempt < 40; attempt += 1) {
    const state = await command(browserId, "evaluate", {
      tabId,
      code: `(() => {
        const input = document.querySelector('[data-e2e="searchbar-input"]');
        const text = document.body?.innerText || '';
        return {
          url: location.href,
          keyword: input?.value?.trim() || '',
          cards: document.querySelectorAll('.search-result-card').length,
          blocked: /验证码|安全验证|访问过于频繁|登录后即可/.test(text.slice(0, 8000)),
        };
      })()`,
    });
    if (state?.blocked) throw new Error("Douyin requires login or security verification. Complete it manually and retry.");
    if (state?.cards > 0 && state.keyword.toLowerCase() === keyword.toLowerCase()) return state;
    await delay(500);
  }
  throw new Error("Timed out waiting for Douyin search results.");
}

async function loadVisibleResults(browserId, tabId, limit) {
  let previous = 0;
  let stalled = 0;
  while (previous < limit && stalled < 3) {
    const state = await command(browserId, "evaluate", {
      tabId,
      code: `(() => {
        const count = document.querySelectorAll('.search-result-card').length;
        window.scrollTo({ top: document.documentElement.scrollHeight, behavior: 'instant' });
        return { count, height: document.documentElement.scrollHeight };
      })()`,
    });
    if (state.count >= limit) return state.count;
    await delay(1_000);
    const after = await command(browserId, "evaluate", {
      tabId,
      code: `document.querySelectorAll('.search-result-card').length`,
    });
    stalled = after > previous ? 0 : stalled + 1;
    previous = after;
  }
  return previous;
}

function normalizeSnapshot(extracted, browser, keyword, limit) {
  const captured = new Date();
  const items = extracted.items.slice(0, limit).map((item) => ({
    ...item,
    visibleLikesValue: parseCount(item.visibleLikesText),
  }));
  return {
    schemaVersion: "2.0",
    source: {
      platform: "抖音精选",
      pageType: "web-search-results",
      url: buildSearchUrl(keyword),
      method: "Easy WebBridge authorized browser page",
      scope: "抖音精选网页关键词搜索当前快照",
    },
    query: {
      keyword,
      type: "general",
    },
    capturedAt: captured.toISOString(),
    capturedAtLocal: localTime(captured),
    browser: {
      displayName: browser.displayName,
      browser: browser.browser,
      extensionVersion: browser.extensionVersion,
    },
    resultCount: items.length,
    items,
    notice: "结果顺序和页面数据会随账号、地区与时间变化；这不是官方 API、全站排名或历史趋势。",
  };
}

function renderMarkdown(data) {
  const lines = [
    "# 抖音实时热点免费版",
    "",
    `- 搜索关键词：${escapeMarkdown(data.query.keyword)}`,
    `- 搜索时间：${data.capturedAtLocal}`,
    `- 数据范围：${data.source.scope}`,
    `- 结果数量：${data.resultCount}`,
    "",
    "| 顺序 | 作品 | 类型 | 可见点赞 | 作者 | 发布时间 |",
    "| ---: | --- | :---: | ---: | --- | --- |",
  ];
  for (const item of data.items) {
    const type = item.contentType === "image" ? "图文" : "视频";
    lines.push(`| ${item.position} | [${escapeMarkdown(item.title)}](${item.url}) | ${type} | ${escapeMarkdown(item.visibleLikesText)} | ${escapeMarkdown(item.author)} | ${escapeMarkdown(item.publishedText || "-")} |`);
  }
  lines.push("", `> ${data.notice}`, "");
  return lines.join("\n");
}

function renderHtml(data) {
  const imageCount = data.items.filter((item) => item.contentType === "image").length;
  const videoCount = data.resultCount - imageCount;
  const cards = data.items.map((item) => {
    const type = item.contentType === "image" ? "图文" : "视频";
    const mediaMeta = item.contentType === "image" ? "图文" : escapeHtml(item.duration || "视频");
    const cover = item.coverUrl
      ? `<img src="${escapeHtml(item.coverUrl)}" alt="" loading="lazy" referrerpolicy="no-referrer">`
      : '<div class="cover-empty">无封面</div>';
    return `<article class="result" data-title="${escapeHtml(`${item.title} ${item.author}`.toLowerCase())}" data-type="${item.contentType}">
      <a class="cover" href="${escapeHtml(item.url)}" target="_blank" rel="noopener noreferrer">${cover}<span class="media-meta">${mediaMeta}</span></a>
      <div class="result-body">
        <div class="eyebrow"><span>${type}</span><span>第 ${item.position} 条</span></div>
        <h2><a href="${escapeHtml(item.url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(item.title)}</a></h2>
        <div class="meta"><strong>${escapeHtml(item.visibleLikesText)}</strong> 可见点赞 · ${escapeHtml(item.author)} · ${escapeHtml(item.publishedText || "时间未显示")}</div>
      </div>
    </article>`;
  }).join("\n");

  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="icon" href="data:,">
<title>${escapeHtml(data.query.keyword)} · 抖音实时热点免费版</title>
<style>
:root{--bg:#f3f4f5;--surface:#fff;--ink:#17181b;--muted:#6b7078;--line:#dfe2e6;--dark:#202226;--coral:#ee4055;--cyan:#008f95}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;letter-spacing:0}a{color:inherit}.shell{max-width:1220px;margin:0 auto;padding:28px 24px 52px}.header{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:24px;align-items:end;padding:26px 28px;background:var(--dark);color:#fff;border-radius:6px}.kicker{color:#8fe0df;font-size:12px;font-weight:700}.header h1{margin:5px 0 7px;font-size:30px;line-height:1.2}.header p{margin:0;color:#c1c4ca}.stamp{text-align:right;color:#aeb2ba}.stamp strong{display:block;color:#fff}.stats{display:grid;grid-template-columns:1.5fr 1fr 1fr 1fr;background:#fff;border:1px solid var(--line);margin:18px 0}.stat{min-width:0;padding:17px 20px;border-right:1px solid var(--line)}.stat:last-child{border-right:0}.stat label{display:block;color:var(--muted);font-size:12px}.stat strong{display:block;margin-top:4px;font-size:20px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.stat:first-child{border-left:4px solid var(--coral)}.controls{display:grid;grid-template-columns:minmax(0,1fr) 170px;gap:10px;margin:18px 0}.controls input,.controls select{width:100%;height:42px;border:1px solid var(--line);border-radius:4px;background:#fff;padding:0 13px;font:inherit}.results{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.result{display:grid;grid-template-columns:190px minmax(0,1fr);min-height:160px;background:#fff;border:1px solid var(--line);border-radius:6px;overflow:hidden}.cover{position:relative;display:block;background:#e5e7e9;min-height:160px;overflow:hidden}.cover img{width:100%;height:100%;object-fit:cover;display:block}.cover-empty{display:grid;place-items:center;height:100%;color:var(--muted)}.media-meta{position:absolute;right:8px;bottom:8px;padding:3px 7px;border-radius:4px;background:rgba(20,21,24,.86);color:#fff;font-size:12px}.result-body{display:flex;flex-direction:column;padding:15px 16px;min-width:0}.eyebrow{display:flex;justify-content:space-between;color:var(--cyan);font-size:12px;font-weight:700}.eyebrow span:last-child{color:var(--muted);font-weight:500}.result h2{margin:10px 0 12px;font-size:16px;line-height:1.48;display:-webkit-box;-webkit-box-orient:vertical;-webkit-line-clamp:3;overflow:hidden}.result h2 a{text-decoration:none}.result h2 a:hover{text-decoration:underline}.meta{margin-top:auto;color:var(--muted);font-size:12px}.meta strong{color:var(--coral)}.empty{display:none;padding:54px;text-align:center;color:var(--muted);background:#fff;border:1px solid var(--line)}.foot{display:flex;justify-content:space-between;gap:20px;margin-top:18px;color:var(--muted);font-size:12px}.hidden{display:none}.results.none+.empty{display:block}@media(max-width:900px){.results{grid-template-columns:1fr}}@media(max-width:620px){.shell{padding:12px 10px 36px}.header{display:block;padding:22px 18px}.header h1{font-size:25px}.stamp{text-align:left;margin-top:14px}.stats{grid-template-columns:1fr 1fr}.stat:nth-child(2){border-right:0}.stat:nth-child(-n+2){border-bottom:1px solid var(--line)}.controls{grid-template-columns:1fr}.result{grid-template-columns:128px minmax(0,1fr);min-height:150px}.cover{min-height:150px}.result-body{padding:12px}.foot{display:block}.foot span{display:block;margin-top:6px}}
</style>
</head>
<body>
<main class="shell">
  <header class="header"><div><div class="kicker">抖音实时热点免费版</div><h1>${escapeHtml(data.query.keyword)}</h1><p>抖音精选关键词搜索 · 当前页面快照</p></div><div class="stamp"><strong>${escapeHtml(data.capturedAtLocal)}</strong>${escapeHtml(data.source.scope)}</div></header>
  <section class="stats" aria-label="搜索摘要"><div class="stat"><label>搜索关键词</label><strong>${escapeHtml(data.query.keyword)}</strong></div><div class="stat"><label>当前结果</label><strong>${data.resultCount}</strong></div><div class="stat"><label>视频</label><strong>${videoCount}</strong></div><div class="stat"><label>图文</label><strong>${imageCount}</strong></div></section>
  <section class="controls" aria-label="结果筛选"><input id="search" type="search" placeholder="在结果中筛选标题或作者"><select id="type"><option value="">全部类型</option><option value="video">视频</option><option value="image">图文</option></select></section>
  <section id="results" class="results">${cards}</section><div id="empty" class="empty">没有匹配的结果</div>
  <footer class="foot"><span>来源：<a href="${escapeHtml(data.source.url)}" target="_blank" rel="noopener noreferrer">抖音精选搜索页</a></span><span>${escapeHtml(data.notice)}</span></footer>
</main>
<script>
const input=document.querySelector('#search');const type=document.querySelector('#type');const results=document.querySelector('#results');const cards=[...document.querySelectorAll('.result')];function apply(){const q=input.value.trim().toLowerCase();const t=type.value;let shown=0;for(const card of cards){const visible=(!q||card.dataset.title.includes(q))&&(!t||card.dataset.type===t);card.classList.toggle('hidden',!visible);if(visible)shown++}results.classList.toggle('none',shown===0)}input.addEventListener('input',apply);type.addEventListener('change',apply);
</script>
</body>
</html>`;
}

async function writeArtifacts(data, outputDir) {
  const absolute = path.resolve(outputDir);
  await mkdir(absolute, { recursive: true });
  const jsonPath = path.join(absolute, "search-results.json");
  const markdownPath = path.join(absolute, "search-results.md");
  const htmlPath = path.join(absolute, "index.html");
  await Promise.all([
    writeFile(jsonPath, `${JSON.stringify(data, null, 2)}\n`, "utf8"),
    writeFile(markdownPath, renderMarkdown(data), "utf8"),
    writeFile(htmlPath, renderHtml(data), "utf8"),
  ]);
  return { outputDir: absolute, jsonPath, markdownPath, htmlPath };
}

async function searchDouyin(options) {
  const keyword = String(options.keyword || "").trim();
  const searchUrl = buildSearchUrl(keyword);
  const browser = await selectBrowser(options);
  const limit = Number(options.limit || 20);
  if (!Number.isInteger(limit) || limit < 1 || limit > 100) throw new Error("--limit must be an integer between 1 and 100.");
  const output = options.output || path.join(process.cwd(), "output", `douyin-search-${timestampSlug()}`);
  const session = `${SESSION_PREFIX}-${process.pid}`;
  let opened = false;
  try {
    const navigation = await command(browser.browserId, "navigate", {
      url: searchUrl,
      newTab: true,
      active: false,
      session,
      groupTitle: GROUP_TITLE,
    });
    opened = true;
    await waitForSearchResults(browser.browserId, navigation.tabId, keyword);
    await loadVisibleResults(browser.browserId, navigation.tabId, limit);
    const extracted = await command(browser.browserId, "evaluate", { tabId: navigation.tabId, code: EXTRACT_SCRIPT });
    if (!extracted?.ok) throw new Error(`Douyin search extraction failed: ${extracted?.reason || "unknown error"}`);
    if (extracted.items.length === 0) throw new Error("Douyin returned no readable search-result cards.");
    const data = normalizeSnapshot(extracted, browser, keyword, limit);
    return { data, artifacts: await writeArtifacts(data, output) };
  } finally {
    if (opened && !options.keepTab) {
      try {
        await command(browser.browserId, "close_session", { session });
      } catch {
        // Collection remains valid if cleanup fails; report files contain no session state.
      }
    }
  }
}

async function main() {
  const { verb, options } = parseArgs(process.argv.slice(2));
  if (["help", "--help", "-h"].includes(verb)) return usage();
  if (verb === "list") {
    const browsers = await onlineBrowsers();
    console.log(JSON.stringify({ ok: true, browsers: browsers.map(({ browserId, displayName, browser, extensionVersion }) => ({ browserId, displayName, browser, extensionVersion })) }, null, 2));
    return;
  }
  if (verb === "search") {
    const result = await searchDouyin(options);
    console.log(JSON.stringify({ ok: true, keyword: result.data.query.keyword, resultCount: result.data.resultCount, capturedAt: result.data.capturedAt, ...result.artifacts }, null, 2));
    return;
  }
  if (verb === "render") {
    if (!options.input) throw new Error("--input is required for render.");
    const data = JSON.parse(await readFile(path.resolve(options.input), "utf8"));
    if (data.schemaVersion !== "2.0") throw new Error("render expects search-results.json schema version 2.0.");
    const output = options.output || path.dirname(path.resolve(options.input));
    console.log(JSON.stringify({ ok: true, ...(await writeArtifacts(data, output)) }, null, 2));
    return;
  }
  usage();
  process.exitCode = 2;
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  main().catch((error) => {
    console.error(JSON.stringify({ ok: false, error: error.message }, null, 2));
    process.exit(1);
  });
}

export { EXTRACT_SCRIPT, buildSearchUrl, escapeHtml, parseArgs, parseCount, renderHtml, renderMarkdown };
