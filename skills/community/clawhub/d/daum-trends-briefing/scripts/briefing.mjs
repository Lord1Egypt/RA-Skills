#!/usr/bin/env node
/**
 * Daum real-time trends briefing
 * - Node.js built-ins only
 * - Prints exactly 12 lines: title + 10 items + updatedAt
 */

import https from 'node:https';
import { URL } from 'node:url';

function fetchText(url, { timeoutMs = 15000 } = {}) {
  return new Promise((resolve, reject) => {
    const u = new URL(url);
    const req = https.request(
      {
        method: 'GET',
        hostname: u.hostname,
        path: u.pathname + u.search,
        headers: {
          'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123 Safari/537.36',
          accept: 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.7,en;q=0.6'
        }
      },
      (res) => {
        if (res.statusCode && res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
          // follow redirect (handle relative Location)
          const nextUrl = new URL(res.headers.location, url).toString();
          resolve(fetchText(nextUrl, { timeoutMs }));
          res.resume();
          return;
        }
        if (!res.statusCode || res.statusCode < 200 || res.statusCode >= 300) {
          const code = res.statusCode;
          res.resume();
          reject(new Error(`HTTP ${code} for ${url}`));
          return;
        }
        res.setEncoding('utf8');
        let data = '';
        res.on('data', (c) => (data += c));
        res.on('end', () => resolve(data));
      }
    );

    req.on('error', reject);
    req.setTimeout(timeoutMs, () => {
      req.destroy(new Error(`Timeout after ${timeoutMs}ms for ${url}`));
    });
    req.end();
  });
}

function decodeHtmlEntities(str) {
  return str
    .replace(/&quot;/g, '"')
    .replace(/&apos;/g, "'")
    .replace(/&#39;/g, "'")
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&nbsp;/g, ' ')
    .replace(/&#(\d+);/g, (_, n) => {
      const code = Number(n);
      if (!Number.isFinite(code)) return _;
      try {
        return String.fromCodePoint(code);
      } catch {
        return _;
      }
    });
}

function stripTags(html) {
  return html.replace(/<[^>]*>/g, '');
}

function extractBracketedArray(text, startIndexOfBracket) {
  if (text[startIndexOfBracket] !== '[') throw new Error('extractBracketedArray: not at [');
  let depth = 0;
  let inString = false;
  let escape = false;

  for (let i = startIndexOfBracket; i < text.length; i++) {
    const ch = text[i];

    if (inString) {
      if (escape) {
        escape = false;
      } else if (ch === '\\') {
        escape = true;
      } else if (ch === '"') {
        inString = false;
      }
      continue;
    }

    if (ch === '"') {
      inString = true;
      continue;
    }

    if (ch === '[') depth++;
    if (ch === ']') {
      depth--;
      if (depth === 0) return text.slice(startIndexOfBracket, i + 1);
    }
  }

  throw new Error('extractBracketedArray: unterminated array');
}

function parseRealtimeTrendTop(html) {
  const anchor = '"uiType":"REALTIME_TREND_TOP"';
  const idx = html.indexOf(anchor);
  if (idx === -1) throw new Error('REALTIME_TREND_TOP not found');

  const slice = html.slice(idx);

  const updatedAtMatch = slice.match(/"updatedAt"\s*:\s*"([^"]+)"/);
  const updatedAt = updatedAtMatch?.[1];
  if (!updatedAt) throw new Error('updatedAt not found near REALTIME_TREND_TOP');

  const keywordsKey = '"keywords":[';
  const kidx = slice.indexOf(keywordsKey);
  if (kidx === -1) throw new Error('keywords array not found near REALTIME_TREND_TOP');

  const arrStart = kidx + '"keywords":'.length;
  const arrText = extractBracketedArray(slice, arrStart);

  const keywordsRaw = JSON.parse(arrText);
  const keywords = keywordsRaw
    .map((k) => k?.keyword)
    .filter((k) => typeof k === 'string' && k.trim().length > 0)
    .slice(0, 10);

  if (keywords.length < 10) throw new Error(`Expected 10 keywords, got ${keywords.length}`);

  return { updatedAt, keywords };
}

function extractFirstTitleAndLinkFromSearch(html) {
  // Prefer first <strong class="tit-g ..."><a href="...">TITLE</a>
  const re = /<strong\s+class="tit-g[^\"]*"[^>]*>\s*<a[^>]*href="([^"]+)"[^>]*>([\s\S]*?)<\/a>\s*<\/strong>/i;
  const m = html.match(re);
  if (m) {
    const url = decodeHtmlEntities(m[1]);
    const title = decodeHtmlEntities(stripTags(m[2])).replace(/\s+/g, ' ').trim();
    if (title) return { title, url };
  }

  // Fallback: page <title>
  const t = html.match(/<title>([\s\S]*?)<\/title>/i)?.[1];
  if (t) {
    const title = decodeHtmlEntities(stripTags(t)).replace(/\s+/g, ' ').trim();
    if (title) return { title, url: null };
  }

  return { title: null, url: null };
}

function buildSearchUrl(keyword) {
  const base = 'https://search.daum.net/search';
  const q = encodeURIComponent(keyword);
  return `${base}?w=tot&DA=RT1&rtmaxcoll=AIO,NNS,DNS&q=${q}`;
}

async function main() {
  const daumHtml = await fetchText('https://www.daum.net/');
  const { updatedAt, keywords } = parseRealtimeTrendTop(daumHtml);

  const lines = [];
  lines.push('Daum 실시간 트렌드 TOP10');

  for (let i = 0; i < keywords.length; i++) {
    const kw = keywords[i];
    const searchUrl = buildSearchUrl(kw);

    let title = 'Daum 검색 결과';

    try {
      const searchHtml = await fetchText(searchUrl);
      const extracted = extractFirstTitleAndLinkFromSearch(searchHtml);
      if (extracted.title) title = extracted.title;
    } catch {
      // keep fallback
    }

    // Keep the link stable (search link), because result URLs can vary.
    lines.push(`${i + 1}. ${kw}: “${title}” ${searchUrl}`);
  }

  lines.push(`updatedAt: ${updatedAt}`);

  // Ensure exactly 12 lines
  process.stdout.write(lines.slice(0, 12).join('\n') + '\n');
}

main().catch((err) => {
  // Still keep a stable 12-line output, but mark failure.
  const now = new Date().toISOString();
  const lines = ['Daum 실시간 트렌드 TOP10'];
  for (let i = 1; i <= 10; i++) lines.push(`${i}. (수집 실패) — ${err?.message ?? 'unknown error'} https://www.daum.net/`);
  lines.push(`updatedAt: ${now}`);
  process.stdout.write(lines.join('\n') + '\n');
  process.exitCode = 1;
});
