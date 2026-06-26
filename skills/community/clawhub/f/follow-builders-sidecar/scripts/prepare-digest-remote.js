#!/usr/bin/env node

const RSS_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36';

function collapseWhitespace(value) {
  return String(value || '').replace(/\s+/g, ' ').trim();
}

function normalizeXUrl(value) {
  const raw = collapseWhitespace(value);
  if (!raw) return null;
  try {
    const parsed = new URL(raw);
    if (parsed.hostname === 'twitter.com' || parsed.hostname === 'www.twitter.com') {
      parsed.hostname = 'x.com';
    }
    parsed.hash = '';
    return parsed.toString().replace(/\/$/, '');
  } catch {
    return raw.replace(/\/$/, '');
  }
}

function extractHandleFromUrl(value) {
  const normalized = normalizeXUrl(value);
  if (!normalized) return null;
  try {
    const parsed = new URL(normalized);
    const [handle] = parsed.pathname.split('/').filter(Boolean);
    if (!handle || handle === 'i') return null;
    return handle.replace(/^@/, '');
  } catch {
    return null;
  }
}

function decodeHtmlEntities(value) {
  return String(value || '')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, '\'')
    .replace(/&nbsp;/g, ' ')
    .replace(/&mdash;/g, '—')
    .replace(/&ndash;/g, '–');
}

function extractTweetTextFromOEmbedHtml(value) {
  const html = String(value || '');
  const paragraphMatch = html.match(/<p[^>]*>([\s\S]*?)<\/p>/i);
  const paragraph = paragraphMatch ? paragraphMatch[1] : html;
  const withLineBreaks = paragraph.replace(/<br\s*\/?>/gi, '\n');
  const anchorText = withLineBreaks.replace(/<a [^>]*>([\s\S]*?)<\/a>/gi, '$1');
  const withoutTags = anchorText.replace(/<[^>]+>/g, ' ');
  return collapseWhitespace(decodeHtmlEntities(withoutTags));
}

async function fetchJSON(url) {
  const res = await fetch(url);
  if (!res.ok) return null;
  return res.json();
}

async function fetchText(url) {
  const res = await fetch(url);
  if (!res.ok) return null;
  return res.text();
}

async function fetchPodcastRss(rssUrl) {
  const res = await fetch(rssUrl, {
    headers: {
      'User-Agent': RSS_USER_AGENT,
      'Accept': 'application/rss+xml, application/xml, text/xml, */*',
      'Accept-Language': 'en-US,en;q=0.9',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive'
    },
    signal: AbortSignal.timeout(45000)
  });

  if (!res.ok) {
    throw new Error(`HTTP ${res.status}`);
  }

  return res.text();
}

async function fetchQuotedTweetOEmbed(tweetId) {
  const url = new URL('https://publish.twitter.com/oembed');
  url.searchParams.set('omit_script', '1');
  url.searchParams.set('url', `https://x.com/i/status/${tweetId}`);

  const res = await fetch(url, {
    headers: {
      'User-Agent': 'follow-builders-prepare-digest/1.0'
    }
  });

  if (!res.ok) {
    throw new Error(`HTTP ${res.status}`);
  }

  const payload = await res.json();
  const authorHandle = extractHandleFromUrl(payload.author_url);
  const normalizedUrl = normalizeXUrl(payload.url) || `https://x.com/i/status/${tweetId}`;

  return {
    id: tweetId,
    text: extractTweetTextFromOEmbedHtml(payload.html),
    url: normalizedUrl,
    authorName: collapseWhitespace(payload.author_name),
    authorHandle,
    authorUrl: normalizeXUrl(payload.author_url) || (authorHandle ? `https://x.com/${authorHandle}` : null)
  };
}

export {
  fetchJSON,
  fetchPodcastRss,
  fetchQuotedTweetOEmbed,
  fetchText
};
