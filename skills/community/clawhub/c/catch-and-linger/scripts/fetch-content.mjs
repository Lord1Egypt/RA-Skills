#!/usr/bin/env node
/**
 * fetch-content.mjs — 抓取网页正文，输出结构化 JSON 供 AI 解读。
 *
 * 用法：node fetch-content.mjs <url> [更多 url…]
 *
 * 零依赖，只用 Node 内置 fetch。GitHub 仓库链接改走 GitHub API（信息更结构化）。
 * 抓取失败不抛栈，返回 extraction:'none' 并带上 HTTP 状态码。
 */

const UA =
  'Mozilla/5.0 (compatible; CatchLingerCapture/1.0)';
const TIMEOUT_MS = 15_000;
const MAX_TEXT = 8_000;

/** HTML 实体解码（&amp; 最后解，避免二次解码）。 */
function decodeEntities(input) {
  return String(input)
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&apos;/g, "'")
    .replace(/&#0?39;/g, "'")
    .replace(/&nbsp;/g, ' ')
    .replace(/&#x([0-9a-f]+);/gi, (_, h) => String.fromCharCode(parseInt(h, 16)))
    .replace(/&#(\d+);/g, (_, d) => String.fromCharCode(Number(d)))
    .replace(/&amp;/g, '&');
}

function stripTags(html) {
  return decodeEntities(
    String(html)
      .replace(/<!--[\s\S]*?-->/g, ' ')
      .replace(/<script[\s\S]*?<\/script>/gi, ' ')
      .replace(/<style[\s\S]*?<\/style>/gi, ' ')
      .replace(/<noscript[\s\S]*?<\/noscript>/gi, ' ')
      .replace(/<svg[\s\S]*?<\/svg>/gi, ' ')
      .replace(/<br\s*\/?>/gi, '\n')
      .replace(/<\/(p|div|li|h[1-6]|tr|section|article|blockquote|pre)>/gi, '\n')
      .replace(/<[^>]+>/g, ' ')
      .replace(/[ \t ]+/g, ' ')
      .replace(/ *\n */g, '\n')
      .replace(/\n{3,}/g, '\n\n')
      .trim(),
  );
}

function metaContent(html, ...names) {
  for (const name of names) {
    const re = new RegExp(
      `<meta[^>]+(?:property|name)=["']${name}["'][^>]*>`,
      'i',
    );
    const m = html.match(re);
    if (!m) continue;
    const c = m[0].match(/content=["']([^"']*)["']/i);
    if (c && c[1]) return decodeEntities(c[1]).trim();
  }
  return null;
}

function extractMain(html) {
  const article = html.match(/<article[\s\S]*?<\/article>/i);
  if (article) return article[0];
  const main = html.match(/<main[\s\S]*?<\/main>/i);
  if (main) return main[0];
  const body = html.match(/<body[\s\S]*?<\/body>/i);
  return body ? body[0] : html;
}

async function fetchWithTimeout(url, headers = {}) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), TIMEOUT_MS);
  try {
    const res = await fetch(url, {
      headers: { 'user-agent': UA, accept: '*/*', ...headers },
      signal: controller.signal,
      redirect: 'follow',
    });
    return { res, error: null };
  } catch (e) {
    return { res: null, error: e?.message ?? String(e) };
  } finally {
    clearTimeout(timer);
  }
}

async function fetchGithub(rawUrl) {
  const m = rawUrl.match(/^https?:\/\/github\.com\/([^/]+)\/([^/?#]+)/i);
  if (!m) return null;

  const owner = m[1];
  const repo = m[2].replace(/\.git$/, '');
  const apiUrl = `https://api.github.com/repos/${owner}/${repo}`;

  const headers = { accept: 'application/vnd.github+json' };
  if (process.env.GITHUB_TOKEN) {
    headers.authorization = `Bearer ${process.env.GITHUB_TOKEN}`;
  }

  const { res, error } = await fetchWithTimeout(apiUrl, headers);
  if (!res) {
    return {
      url: rawUrl,
      status: 0,
      title: `${owner}/${repo}`,
      meta_description: null,
      og_title: null,
      og_description: null,
      site_name: 'GitHub',
      text: `无法访问 GitHub API：${error}`,
      extraction: 'none',
      lang: null,
    };
  }

  if (!res.ok) {
    return {
      url: rawUrl,
      status: res.status,
      title: `${owner}/${repo}`,
      meta_description: null,
      og_title: null,
      og_description: null,
      site_name: 'GitHub',
      text: `GitHub API 返回 ${res.status} ${res.statusText}`,
      extraction: 'none',
      lang: null,
    };
  }

  const data = await res.json();
  const topics = Array.isArray(data.topics) ? data.topics : [];
  const text = [
    `仓库：${data.full_name ?? `${owner}/${repo}`}`,
    `描述：${data.description ?? '（无）'}`,
    `语言：${data.language ?? '（未标注）'}`,
    `Stars：${data.stargazers_count ?? 0}`,
    `Forks：${data.forks_count ?? 0}`,
    `许可证：${data.license?.spdx_id ?? '（未标注）'}`,
    topics.length ? `Topics：${topics.join(', ')}` : null,
    `主页：${data.homepage ?? '（无）'}`,
    `最近推送：${data.pushed_at ?? '未知'}`,
    data.description ? `README 摘要：${data.description}` : null,
  ]
    .filter(Boolean)
    .join('\n');

  return {
    url: rawUrl,
    status: res.status,
    title: data.full_name ?? `${owner}/${repo}`,
    meta_description: data.description ?? null,
    og_title: data.full_name ?? null,
    og_description: data.description ?? null,
    site_name: 'GitHub',
    text: text.slice(0, MAX_TEXT),
    extraction: 'full',
    lang: null,
  };
}

async function fetchHtml(rawUrl) {
  const { res, error } = await fetchWithTimeout(rawUrl);

  if (!res) {
    return {
      url: rawUrl,
      status: 0,
      title: null,
      meta_description: null,
      og_title: null,
      og_description: null,
      site_name: null,
      text: `请求失败：${error}`,
      extraction: 'none',
      lang: null,
    };
  }

  if (!res.ok) {
    return {
      url: rawUrl,
      status: res.status,
      title: null,
      meta_description: null,
      og_title: null,
      og_description: null,
      site_name: null,
      text: `HTTP ${res.status} ${res.statusText}`,
      extraction: 'none',
      lang: null,
    };
  }

  const contentType = res.headers.get('content-type') ?? '';
  if (!contentType.includes('html')) {
    const body = (await res.text()).slice(0, MAX_TEXT);
    return {
      url: rawUrl,
      status: res.status,
      title: null,
      meta_description: null,
      og_title: null,
      og_description: null,
      site_name: null,
      text: body,
      extraction: 'full',
      lang: null,
    };
  }

  const html = await res.text();

  const titleMatch = html.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
  const title = titleMatch ? decodeEntities(titleMatch[1]).trim() : null;

  const metaDescription = metaContent(html, 'description');
  const ogTitle = metaContent(html, 'og:title');
  const ogDescription = metaContent(html, 'og:description');
  const siteName = metaContent(html, 'og:site_name');
  const langMatch = html.match(/<html[^>]+lang=["']([^"']+)["']/i);

  const text = stripTags(extractMain(html)).slice(0, MAX_TEXT);

  // 正文太短通常是 JS 渲染站或反爬 —— 标记为 partial，让调用方退化为 og 描述
  const extraction = text.length >= 200 ? 'full' : text.length > 0 ? 'partial' : 'none';

  return {
    url: rawUrl,
    status: res.status,
    title,
    meta_description: metaDescription,
    og_title: ogTitle,
    og_description: ogDescription,
    site_name: siteName,
    text,
    extraction,
    lang: langMatch ? langMatch[1] : null,
  };
}

const urls = process.argv.slice(2).filter((a) => !a.startsWith('--'));
if (urls.length === 0) {
  console.error('用法：node fetch-content.mjs <url> [更多 url…]');
  process.exit(1);
}

const results = [];
for (const raw of urls) {
  const gh = await fetchGithub(raw);
  results.push(gh ?? (await fetchHtml(raw)));
}

console.log(JSON.stringify(results.length === 1 ? results[0] : results, null, 2));
