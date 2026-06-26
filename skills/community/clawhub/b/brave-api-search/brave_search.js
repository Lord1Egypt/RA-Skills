#!/usr/bin/env node
// Brave Web Search - uses Brave Search API web/search endpoint
// Requires: BRAVE_SEARCH_API_KEY env var

const BASE_URL = 'https://api.search.brave.com/res/v1';
const VALID_FRESHNESS = new Set(['pd', 'pw', 'pm', 'py']);
const VALID_SAFESEARCH = new Set(['off', 'moderate', 'strict']);
const VALID_UNITS = new Set(['metric', 'imperial']);
const VALID_RESULT_FILTERS = new Set([
  'web', 'news', 'videos', 'discussions', 'faq', 'infobox', 'locations', 'query', 'summarizer'
]);

const { parseArgs, fetchWithRetry } = require('./utils');

// ─── Geo header builder ────────────────────────────────────────────────────────

function buildGeoHeaders(args) {
  const headers = {};
  if (args.lat)          headers['x-loc-lat'] = args.lat;
  if (args.long)         headers['x-loc-long'] = args.long;
  if (args.timezone)     headers['x-loc-timezone'] = args.timezone;
  if (args.city)         headers['x-loc-city'] = args.city;
  if (args.state)        headers['x-loc-state'] = args.state;
  if (args.country)      headers['x-loc-country'] = args.country;
  if (args['postal-code']) headers['x-loc-postal-code'] = args['postal-code'];
  return headers;
}

// ─── API fetch ────────────────────────────────────────────────────────────────

async function braveGet(path, params, apiKey, extraHeaders) {
  if (!apiKey) {
    console.error('Error: BRAVE_SEARCH_API_KEY environment variable not set.');
    console.error('Get your key at: https://api-dashboard.search.brave.com');
    process.exit(1);
  }

  const url = new URL(`${BASE_URL}${path}`);
  for (const [k, v] of Object.entries(params)) {
    if (v !== '' && v !== undefined && v !== null) url.searchParams.set(k, v);
  }

  const headers = {
    'Accept': 'application/json',
    'Accept-Encoding': 'gzip',
    'X-Subscription-Token': apiKey,
    ...extraHeaders,
  };

  const res = await fetchWithRetry(url.toString(), { headers });
  if (!res.ok) {
    const body = await res.text();
    console.error(`Brave API error ${res.status}: ${body}`);
    process.exit(1);
  }
  return res.json();
}

// ─── HTML stripper ────────────────────────────────────────────────────────────

function stripHtml(text) {
  if (!text) return '';
  return text
    .replace(/<[^>]+>/g, '')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&amp;/g, '&')
    .replace(/&#x27;/g, "'")
    .replace(/&#x2F;/g, '/')
    .replace(/&#39;/g, "'")
    .replace(/&quot;/g, '"')
    .trim();
}

// ─── Web results formatter ─────────────────────────────────────────────────────

function formatResults(data, extraSnippets, showDecorations, showSpellcheckInfo) {
  const results = data.web?.results || [];
  const q = data.query || {};
  const lines = [];

  if (showSpellcheckInfo && q.altered && q.altered !== q.original) {
    lines.push(`🔍 Query corrected: "${q.original}" → "${q.altered}"\n`);
  }

  if (results.length === 0) {
    lines.push('No web results found.');
    return lines.join('\n');
  }

  lines.push(`Found ${results.length} web result(s) for: ${q.original || ''}`);
  if (q.more_results_available) lines.push(` *(More results — use --offset)*`);
  lines.push('');

  for (let i = 0; i < results.length; i++) {
    const r = results[i];
    const title = showDecorations ? (r.title || '') : stripHtml(r.title);
    const desc  = showDecorations ? (r.description || '') : stripHtml(r.description);

    lines.push(`${i + 1}. **${title}**`);
    lines.push(`   URL: ${r.url}`);
    if (desc) lines.push(`   ${desc}`);
    if (extraSnippets && r.extra_snippets?.length) {
      lines.push('   Additional context:');
      for (const s of r.extra_snippets) {
        lines.push(`   - ${showDecorations ? s : stripHtml(s)}`);
      }
    }
    lines.push('');
  }

  return lines.join('\n');
}

// ─── Discussions formatter ────────────────────────────────────────────────────

function formatDiscussions(data) {
  const threads = data.discussions?.results || [];
  if (threads.length === 0) return null;

  const lines = ['## Discussions\n'];
  for (let i = 0; i < threads.length; i++) {
    const t = threads[i];
    lines.push(`${i + 1}. **${stripHtml(t.title || t.question || '')}**`);
    lines.push(`   URL: ${t.url}`);
    if (t.description) lines.push(`   ${stripHtml(t.description)}`);
    if (t.meta_url?.forum_name) lines.push(`   Source: ${t.meta_url.forum_name}`);
    lines.push('');
  }
  return lines.join('\n');
}

// ─── FAQ formatter ────────────────────────────────────────────────────────────

function formatFAQ(data) {
  const faqs = data.faq?.results || [];
  if (faqs.length === 0) return null;

  const lines = ['## FAQ\n'];
  for (let i = 0; i < faqs.length; i++) {
    const f = faqs[i];
    const title = stripHtml(f.title || f.question || '');
    lines.push(`${i + 1}. **${title}**`);
    if (f.url) lines.push(`   URL: ${f.url}`);
    const body = f.description || f.answer || '';
    if (body) lines.push(`   ${stripHtml(body)}`);
    lines.push('');
  }
  return lines.join('\n');
}

// ─── Infobox formatter ───────────────────────────────────────────────────────

function formatInfobox(data) {
  const entries = data.infobox?.results || [];
  if (entries.length === 0) return null;

  const lines = [];
  for (const entry of entries) {
    lines.push(`## ${stripHtml(entry.title || entry.name || 'Infobox')}\n`);
    if (entry.long_desc) {
      lines.push(`${stripHtml(entry.long_desc).slice(0, 500)}${entry.long_desc.length > 500 ? '…' : ''}\n`);
    } else if (entry.description) {
      lines.push(`${stripHtml(entry.description)}\n`);
    }
    if (entry.profiles?.length) {
      lines.push('**Profiles:**');
      for (const p of entry.profiles) lines.push(`- [${p.name}](${p.url})`);
    }
    if (entry.attributes?.length) {
      lines.push('**Attributes:**');
      for (const [key, val] of entry.attributes) {
        lines.push(`- **${stripHtml(key)}**: ${stripHtml(val)}`);
      }
    }
    lines.push('');
  }
  return lines.join('\n');
}

// ─── News formatter ───────────────────────────────────────────────────────────

function formatNews(data) {
  const articles = data.news?.results || [];
  if (articles.length === 0) return null;

  const lines = ['## News\n'];
  for (let i = 0; i < Math.min(articles.length, 5); i++) {
    const n = articles[i];
    lines.push(`${i + 1}. **${stripHtml(n.title || '')}**`);
    lines.push(`   URL: ${n.url}`);
    if (n.description) lines.push(`   ${stripHtml(n.description)}`);
    if (n.page_age) lines.push(`   Age: ${n.page_age}`);
    if (n.profile?.name) lines.push(`   Source: ${n.profile.name}`);
    lines.push('');
  }
  return lines.join('\n');
}

// ─── Video formatter ────────────────────────────────────────────────────────────

function formatVideos(data) {
  const videos = data.videos?.results || [];
  if (videos.length === 0) return null;

  const lines = ['## Videos\n'];
  for (let i = 0; i < Math.min(videos.length, 5); i++) {
    const v = videos[i];
    lines.push(`${i + 1}. **${stripHtml(v.title || '')}**`);
    lines.push(`   URL: ${v.url}`);
    if (v.video?.duration) lines.push(`   Duration: ${v.video.duration}`);
    if (v.publisher) lines.push(`   Publisher: ${v.publisher}`);
    if (v.meta_url?.netloc) lines.push(`   Source: ${v.meta_url.netloc}`);
    lines.push('');
  }
  return lines.join('\n');
}

// ─── Summary formatter ────────────────────────────────────────────────────────

function formatSummary(data) {
  if (!data || data.status === 'failed') return null;
  const lines = [];
  if (data.title) lines.push(`## ${data.title}\n`);
  if (data.summary?.length) {
    lines.push(data.summary.map(s => s.data || '').join(''));
  }
  if (data.followups?.length) {
    lines.push('\n**Related questions:**');
    for (const q of data.followups) lines.push(`- ${q}`);
  }
  return lines.join('\n');
}

// ─── Main ─────────────────────────────────────────────────────────────────────

async function main() {
  const args = parseArgs(process.argv);

  const query = args.query;
  if (!query) {
    console.error(
      'Usage: brave_search.js --query "search terms" [options]\n' +
      'Options:\n' +
      '  --count N          Results per page (1-20, default: 10)\n' +
      '  --country CC       2-letter country code (default: us)\n' +
      '  --offset N         Pagination offset, 0-9 (default: 0)\n' +
      '  --freshness pd|pw|pm|py|YYYY-MM-DDtoYYYY-MM-DD  Date filter\n' +
      '  --result-filter    Comma list: web,news,videos,discussions,faq,infobox\n' +
      '  --search-lang      Language code (e.g. en, da, de)\n' +
      '  --ui-lang          UI locale (e.g. en-US, da-DK)\n' +
      '  --safesearch off|moderate|strict  Adult filter (default: moderate)\n' +
      '  --spellcheck true|false  Enable spellcheck (default: true)\n' +
      '  --text-decorations true|false  Show HTML highlights (default: true)\n' +
      '  --extra-snippets   Include additional excerpts (default: false)\n' +
      '  --summary          Fetch AI summary (default: false)\n' +
      '  --units metric|imperial\n' +
      'Geo (for local results):\n' +
      '  --lat NUM --long NUM --city NAME --state CODE --country CODE\n'
    );
    process.exit(1);
  }

  const apiKey = process.env.BRAVE_SEARCH_API_KEY;
  if (!apiKey) {
    console.error('Error: BRAVE_SEARCH_API_KEY environment variable not set.');
    console.error('Get your key at: https://api-dashboard.search.brave.com');
    process.exit(1);
  }

  const count          = Math.min(20, Math.max(1, parseInt(args.count) || 10));
  const country        = args.country || 'us';
  const freshness      = args.freshness || undefined;
  const extraSnippets  = args['extra-snippets'] === 'true';
  const wantSummary   = args.summary === 'true';
  const showDecorations = args['text-decorations'] !== 'false';
  const showSpellcheckInfo = args['spellcheck-info'] === 'true';
  const units          = VALID_UNITS.has(args.units) ? args.units : undefined;
  const safesearch     = VALID_SAFESEARCH.has(args.safesearch) ? args.safesearch : 'moderate';
  const spellcheck     = args.spellcheck === 'false' ? 'false' : undefined;

  // Parse result_filter
  let resultFilter;
  if (args['result-filter']) {
    const filters = args['result-filter']
      .split(',')
      .map(f => f.trim())
      .filter(f => VALID_RESULT_FILTERS.has(f));
    resultFilter = filters.length > 0 ? filters.join(',') : undefined;
  }

  const searchParams = {
    q: query,
    count,
    country,
    safesearch,
    spellcheck,
    extra_snippets: extraSnippets ? '1' : undefined,
    result_filter: resultFilter,
    freshness,
    units,
    offset: args.offset ? String(Math.min(9, Math.max(0, parseInt(args.offset)))) : undefined,
  };

  if (args['search-lang'])    searchParams.search_lang = args['search-lang'];
  if (args['ui-lang'])        searchParams.ui_lang = args['ui-lang'];
  if (!showDecorations)      searchParams.text_decorations = 'false';
  if (wantSummary)           searchParams.summary = '1';

  const geoHeaders = buildGeoHeaders(args);
  const data = await braveGet('/web/search', searchParams, apiKey, geoHeaders);

  // ── Web results (always printed) ──
  console.log(formatResults(data, extraSnippets, showDecorations, showSpellcheckInfo));

  // ── Additional result types (only if not filtered to web-only) ──
  if (!resultFilter || !resultFilter.split(',').every(f => f === 'web' || f === 'query')) {
    if (data.summarizer?.key && wantSummary) {
      const summaryData = await braveGet('/summarizer/search', {
        key: data.summarizer.key,
        inline_references: 'true',
      }, apiKey, geoHeaders);
      const summary = formatSummary(summaryData);
      if (summary) console.log('\n---\n**AI Summary:**\n' + summary);
    }

    const discussions = formatDiscussions(data);
    if (discussions) console.log('\n' + discussions);

    const faq = formatFAQ(data);
    if (faq) console.log('\n' + faq);

    const infobox = formatInfobox(data);
    if (infobox) console.log('\n' + infobox);

    const news = formatNews(data);
    if (news) console.log('\n' + news);

    const videos = formatVideos(data);
    if (videos) console.log('\n' + videos);
  }

  if (data.query?.spellcheck_off) {
    console.log('\n*(Spellcheck was disabled for this query)*');
  }
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
