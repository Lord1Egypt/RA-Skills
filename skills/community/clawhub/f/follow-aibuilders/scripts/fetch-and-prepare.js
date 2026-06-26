#!/usr/bin/env node

// ============================================================================
// Follow Builders — Fetch and Prepare Digest
// ============================================================================
// Fetches content locally using free tools and prepares digest data:
// - Fetches from Twitter/X via Rettiwt-API (free, guest or user auth)
// - Fetches from YouTube via yt-dlp (free, no API key)
// - Scrapes blogs directly via HTTP
// - Manages user-customizable sources
// - Handles deduplication with per-user state
// - Loads prompts with priority (user > remote > local)
// - Outputs JSON for LLM processing
//
// Usage: node fetch-and-prepare.js
// Env vars (optional): RETTIWT_API_KEY (for Twitter user auth if guest is rate limited)
// System deps: yt-dlp (for YouTube video listing and transcripts)
// ============================================================================

import { readFile, writeFile, mkdir } from 'fs/promises';
import { existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';
import { Rettiwt } from 'rettiwt-api';
import { listChannelVideos, fetchTranscript, checkYtDlpAvailable } from './yt-dlp-helpers.js';

const SCRIPT_DIR = dirname(fileURLToPath(import.meta.url));
const PROJECT_DIR = join(SCRIPT_DIR, '..');

// Load environment variables from project root .env
const envPath = join(PROJECT_DIR, '.env');
if (existsSync(envPath)) {
  dotenv.config({ path: envPath });
}

// -- Constants ---------------------------------------------------------------

const CONFIG_PATH = join(PROJECT_DIR, 'config', 'config.json');
const STATE_PATH = join(PROJECT_DIR, 'state-feed.json');

const DEFAULT_LOOKBACK_HOURS = 24;
const MAX_TWEETS_PER_USER = 3;
const MAX_ARTICLES_PER_BLOG = 3;

const PROMPT_FILES = [
  'summarize-podcast.md',
  'summarize-tweets.md',
  'summarize-blogs.md',
  'digest-intro.md',
  'translate.md'
];

// -- Config Loading ----------------------------------------------------------

async function loadConfig() {
  const config = JSON.parse(await readFile(CONFIG_PATH, 'utf-8'));
  return config;
}

// -- Dependency Validation ---------------------------------------------------

async function validateDependencies() {
  const errors = [];

  // Check yt-dlp
  const ytDlp = await checkYtDlpAvailable();
  if (!ytDlp.available) {
    errors.push(
      'yt-dlp 未安装。请安装后重试：\n' +
      '  macOS: brew install yt-dlp\n' +
      '  Linux/Windows: pip install yt-dlp\n' +
      '  或从 https://github.com/yt-dlp/yt-dlp/releases 下载'
    );
  } else {
    console.error(`  yt-dlp ${ytDlp.version} found`);
  }

  // Check Twitter connectivity via Rettiwt
  const rettiwtOptions = { delay: 1000 };
  if (process.env.RETTIWT_API_KEY) {
    rettiwtOptions.apiKey = process.env.RETTIWT_API_KEY;
    console.error('  Using Twitter user auth (RETTIWT_API_KEY)');
  } else {
    console.error('  Using Twitter guest auth (no API key)');
  }
  const proxyUrl = process.env.FB_PROXY;
  if (proxyUrl) {
    rettiwtOptions.proxyUrl = proxyUrl;
    console.error(`  Using proxy: ${proxyUrl}`);
  }

  try {
    const rettiwt = new Rettiwt(rettiwtOptions);
    await rettiwt.user.details('twitter');
    console.error('  Twitter API connectivity OK');
  } catch (err) {
    const msg = err.message || String(err);
    if (msg.includes('429') || msg.includes('rate') || msg.includes('Rate')) {
      errors.push(
        'Twitter API 速率限制中。Guest 认证配额已用完。\n' +
        '建议配置 user 认证：\n' +
        '  1. 安装 Chrome 扩展 X Auth Helper\n' +
        '  2. 在隐身模式登录 Twitter/X\n' +
        '  3. 点击扩展获取 API_KEY\n' +
        '  4. 在 .env 中添加 RETTIWT_API_KEY=<api_key>'
      );
    } else {
      errors.push(`Twitter API 连接失败: ${msg}`);
    }
  }

  return errors;
}

// -- State Management --------------------------------------------------------

async function loadState() {
  if (!existsSync(STATE_PATH)) {
    return { seenTweets: {}, seenVideos: {}, seenArticles: {} };
  }

  try {
    const state = JSON.parse(await readFile(STATE_PATH, 'utf-8'));
    if (!state.seenArticles) state.seenArticles = {};
    return state;
  } catch {
    return { seenTweets: {}, seenVideos: {}, seenArticles: {} };
  }
}

async function saveState(state) {
  // Prune entries older than 7 days
  const cutoff = Date.now() - 7 * 24 * 60 * 60 * 1000;
  for (const [id, ts] of Object.entries(state.seenTweets)) {
    if (ts < cutoff) delete state.seenTweets[id];
  }
  for (const [id, ts] of Object.entries(state.seenVideos)) {
    if (ts < cutoff) delete state.seenVideos[id];
  }
  for (const [id, ts] of Object.entries(state.seenArticles || {})) {
    if (ts < cutoff) delete state.seenArticles[id];
  }

  await writeFile(STATE_PATH, JSON.stringify(state, null, 2));
}

// -- X/Twitter Fetching (Rettiwt-API) ----------------------------------------

// Parse Twitter date format: "Mon Nov 18 06:35:11 +0000 2024"
function parseTwitterDate(dateStr) {
  return new Date(dateStr);
}

async function fetchXContent(xAccounts, state, lookbackHours, errors) {
  const results = [];
  const cutoff = new Date(Date.now() - lookbackHours * 60 * 60 * 1000);

  // Initialize Rettiwt with delay between requests
  const rettiwtOptions = { delay: 1000 };
  if (process.env.RETTIWT_API_KEY) {
    rettiwtOptions.apiKey = process.env.RETTIWT_API_KEY;
  }
  const proxyUrl = process.env.FB_PROXY;
  if (proxyUrl) {
    rettiwtOptions.proxyUrl = proxyUrl;
  }
  const rettiwt = new Rettiwt(rettiwtOptions);

  for (const account of xAccounts) {
    try {
      // 1. Fetch user details (accepts username)
      const userDetails = await rettiwt.user.details(account.handle);

      if (!userDetails) {
        errors.push(`X API: User @${account.handle} not found`);
        continue;
      }

      const userId = userDetails.id;
      const userName = userDetails.fullName || account.name;
      const userBio = userDetails.description || '';

      // 2. Fetch user timeline (requires user ID, not username)
      const timelineData = await rettiwt.user.timeline(userId);
      const tweets = timelineData?.list || [];

      // Filter tweets within time window, exclude retweets, limit to MAX_TWEETS_PER_USER
      const newTweets = [];

      for (const tweet of tweets) {
        // Skip retweets
        if (tweet.retweetedTweet) continue;

        // Parse and check time
        const createdAt = parseTwitterDate(tweet.createdAt);
        if (createdAt < cutoff) continue;

        // Limit to MAX_TWEETS_PER_USER
        if (newTweets.length >= MAX_TWEETS_PER_USER) break;

        // Extract tweet data
        newTweets.push({
          id: tweet.id,
          text: tweet.fullText || '',
          createdAt: tweet.createdAt,
          url: `https://x.com/${account.handle}/status/${tweet.id}`,
          likes: tweet.likeCount || 0,
          retweets: tweet.retweetCount || 0,
          replies: tweet.replyCount || 0,
          isQuote: !!tweet.quoted,
          quotedTweetId: tweet.quoted || null
        });
      }

      if (newTweets.length === 0) continue;

      results.push({
        source: 'x',
        name: userName,
        handle: account.handle,
        bio: userBio,
        tweets: newTweets
      });
    } catch (err) {
      const msg = err.message || String(err);
      if (msg.includes('429') || msg.includes('rate') || msg.includes('Rate')) {
        errors.push(`X API: Rate limited at @${account.handle}, skipping remaining accounts`);
        break;
      }
      errors.push(`X API: Error fetching @${account.handle}: ${msg}`);
    }
  }

  return results;
}

// -- YouTube Fetching (yt-dlp) -----------------------------------------------

async function fetchYouTubeContent(podcasts, state, lookbackHours, errors) {
  const cutoff = new Date(Date.now() - lookbackHours * 60 * 60 * 1000);
  const allCandidates = [];

  for (const podcast of podcasts) {
    console.error(`  Processing podcast: ${podcast.name}...`);
    const videos = await listChannelVideos(podcast, lookbackHours, errors);

    for (const video of videos) {
      // Filter by cutoff
      if (video.publishedAt && new Date(video.publishedAt) < cutoff) continue;

      allCandidates.push({
        podcast,
        videoId: video.videoId,
        title: video.title,
        publishedAt: video.publishedAt || new Date().toISOString()
      });
    }
  }

  // If no new videos within time window, return early
  if (allCandidates.length === 0) {
    console.error('  No new podcast episodes found');
    return [];
  }

  // Pick 1 unseen video (oldest first for chronological order)
  const selected = allCandidates.sort((a, b) => new Date(a.publishedAt) - new Date(b.publishedAt))[0];

  console.error(`  Fetching transcript for: ${selected.title}`);

  // Fetch transcript
  const transcript = await fetchTranscript(selected.videoId, errors);

  return [{
    source: 'podcast',
    name: selected.podcast.name,
    title: selected.title,
    videoId: selected.videoId,
    url: `https://youtube.com/watch?v=${selected.videoId}`,
    publishedAt: selected.publishedAt,
    transcript
  }];
}

// -- Blog Fetching (HTML scraping) -------------------------------------------

function parseAnthropicEngineeringIndex(html) {
  const articles = [];

  // Strategy 1: Look for article data in Next.js __NEXT_DATA__ script tag
  const nextDataMatch = html.match(/<script[^>]*id="__NEXT_DATA__"[^>]*>([\s\S]*?)<\/script>/i);
  if (nextDataMatch) {
    try {
      const data = JSON.parse(nextDataMatch[1]);
      const pageProps = data?.props?.pageProps;
      const posts = pageProps?.posts || pageProps?.articles || pageProps?.entries || [];
      for (const post of posts) {
        const slug = post.slug?.current || post.slug || '';
        articles.push({
          title: post.title || 'Untitled',
          url: `https://www.anthropic.com/engineering/${slug}`,
          publishedAt: post.publishedOn || post.publishedAt || post.date || null,
          description: post.summary || post.description || ''
        });
      }
      if (articles.length > 0) return articles;
    } catch {
      // Fall through to regex approach
    }
  }

  // Strategy 2: Regex-based extraction
  const linkRegex = /href="\/engineering\/([a-z0-9-]+)"/gi;
  const seenSlugs = new Set();
  let linkMatch;
  while ((linkMatch = linkRegex.exec(html)) !== null) {
    const slug = linkMatch[1];
    if (seenSlugs.has(slug)) continue;
    seenSlugs.add(slug);
    articles.push({
      title: '',
      url: `https://www.anthropic.com/engineering/${slug}`,
      publishedAt: null,
      description: ''
    });
  }
  return articles;
}

function parseClaudeBlogIndex(html) {
  const articles = [];
  const seenSlugs = new Set();

  const linkRegex = /href="\/blog\/([a-z0-9-]+)"/gi;
  let linkMatch;
  while ((linkMatch = linkRegex.exec(html)) !== null) {
    const slug = linkMatch[1];
    if (seenSlugs.has(slug)) continue;
    seenSlugs.add(slug);
    articles.push({
      title: '',
      url: `https://claude.com/blog/${slug}`,
      publishedAt: null,
      description: ''
    });
  }
  return articles;
}

function extractAnthropicArticleContent(html) {
  let title = '';
  let author = '';
  let publishedAt = null;
  let content = '';

  const nextDataMatch = html.match(/<script[^>]*id="__NEXT_DATA__"[^>]*>([\s\S]*?)<\/script>/i);
  if (nextDataMatch) {
    try {
      const data = JSON.parse(nextDataMatch[1]);
      const pageProps = data?.props?.pageProps;
      const post = pageProps?.post || pageProps?.article || pageProps?.entry || pageProps;
      title = post?.title || '';
      author = post?.author?.name || post?.authors?.[0]?.name || '';
      publishedAt = post?.publishedOn || post?.publishedAt || post?.date || null;

      const body = post?.body || post?.content || [];
      if (Array.isArray(body)) {
        const textParts = [];
        for (const block of body) {
          if (block._type === 'block' && block.children) {
            const text = block.children.map(c => c.text || '').join('');
            if (text.trim()) textParts.push(text.trim());
          }
        }
        content = textParts.join('\n\n');
      }
      if (content) return { title, author, publishedAt, content };
    } catch {
      // Fall through
    }
  }

  const h1Match = html.match(/<h1[^>]*>([\s\S]*?)<\/h1>/i);
  if (h1Match) title = h1Match[1].replace(/<[^>]+>/g, '').trim();

  const articleMatch = html.match(/<article[^>]*>([\s\S]*?)<\/article>/i);
  const bodyHtml = articleMatch ? articleMatch[1] : html;

  content = bodyHtml
    .replace(/<script[\s\S]*?<\/script>/gi, '')
    .replace(/<style[\s\S]*?<\/style>/gi, '')
    .replace(/<[^>]+>/g, ' ')
    .replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&nbsp;/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();

  return { title, author, publishedAt, content };
}

function extractClaudeBlogArticleContent(html) {
  let title = '';
  let author = '';
  let publishedAt = null;
  let content = '';

  const jsonLdRegex = /<script[^>]*type="application\/ld\+json"[^>]*>([\s\S]*?)<\/script>/gi;
  let jsonLdMatch;
  while ((jsonLdMatch = jsonLdRegex.exec(html)) !== null) {
    try {
      const ld = JSON.parse(jsonLdMatch[1]);
      if (ld['@type'] === 'BlogPosting' || ld['@type'] === 'Article') {
        title = ld.headline || ld.name || '';
        author = ld.author?.name || '';
        publishedAt = ld.datePublished || null;
        break;
      }
    } catch {
      // Skip
    }
  }

  const richTextMatch = html.match(/<div[^>]*class="[^"]*u-rich-text-blog[^"]*"[^>]*>([\s\S]*?)<\/div>\s*<\/div>/i)
    || html.match(/<div[^>]*class="[^"]*w-richtext[^"]*"[^>]*>([\s\S]*?)<\/div>/i);

  if (richTextMatch) {
    content = richTextMatch[1]
      .replace(/<script[\s\S]*?<\/script>/gi, '')
      .replace(/<style[\s\S]*?<\/style>/gi, '')
      .replace(/<[^>]+>/g, ' ')
      .replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>')
      .replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&nbsp;/g, ' ')
      .replace(/\s+/g, ' ')
      .trim();
  }

  if (!content) {
    if (!title) {
      const h1Match = html.match(/<h1[^>]*>([\s\S]*?)<\/h1>/i);
      if (h1Match) title = h1Match[1].replace(/<[^>]+>/g, '').trim();
    }

    content = html
      .replace(/<script[\s\S]*?<\/script>/gi, '')
      .replace(/<style[\s\S]*?<\/style>/gi, '')
      .replace(/<nav[\s\S]*?<\/nav>/gi, '')
      .replace(/<footer[\s\S]*?<\/footer>/gi, '')
      .replace(/<header[\s\S]*?<\/header>/gi, '')
      .replace(/<[^>]+>/g, ' ')
      .replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>')
      .replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&nbsp;/g, ' ')
      .replace(/\s+/g, ' ')
      .trim();
  }

  return { title, author, publishedAt, content };
}

async function fetchBlogContent(blogs, state, lookbackHours, errors) {
  const results = [];
  const cutoff = new Date(Date.now() - lookbackHours * 60 * 60 * 1000);

  for (const blog of blogs) {
    console.error(`  Processing blog: ${blog.name}...`);
    let candidates = [];

    try {
      const indexRes = await fetch(blog.indexUrl, {
        headers: { 'User-Agent': 'FollowBuilders/1.0 (feed aggregator)' }
      });
      if (!indexRes.ok) {
        errors.push(`Blog: Failed to fetch index for ${blog.name}: HTTP ${indexRes.status}`);
        continue;
      }
      const indexHtml = await indexRes.text();

      if (blog.indexUrl.includes('anthropic.com')) {
        candidates = parseAnthropicEngineeringIndex(indexHtml);
      } else if (blog.indexUrl.includes('claude.com')) {
        candidates = parseClaudeBlogIndex(indexHtml);
      }

      const MAX_INDEX_SCAN = MAX_ARTICLES_PER_BLOG;
      const toFetch = candidates.slice(0, MAX_INDEX_SCAN);

      if (toFetch.length === 0) {
        console.error(`    No articles found on index page`);
        continue;
      }

      console.error(`    Scanning ${toFetch.length} article(s) from index...`);

      for (const article of toFetch) {
        if (results.length >= MAX_ARTICLES_PER_BLOG) break;

        try {
          const articleRes = await fetch(article.url, {
            headers: { 'User-Agent': 'FollowBuilders/1.0 (feed aggregator)' }
          });
          if (!articleRes.ok) {
            errors.push(`Blog: Failed to fetch article ${article.url}: HTTP ${articleRes.status}`);
            continue;
          }
          const articleHtml = await articleRes.text();

          let extracted;
          if (article.url.includes('anthropic.com/engineering')) {
            extracted = extractAnthropicArticleContent(articleHtml);
          } else if (article.url.includes('claude.com/blog')) {
            extracted = extractClaudeBlogArticleContent(articleHtml);
          }

          if (!extracted || !extracted.content) {
            errors.push(`Blog: No content extracted from ${article.url}`);
            continue;
          }

          // Time filter: now we have the real publishedAt from article content
          const pubDate = extracted.publishedAt || article.publishedAt || null;
          if (pubDate && new Date(pubDate) < cutoff) continue;

          results.push({
            source: 'blog',
            name: blog.name,
            title: extracted.title || article.title || 'Untitled',
            url: article.url,
            publishedAt: pubDate,
            author: extracted.author || '',
            description: article.description || '',
            content: extracted.content
          });

          await new Promise(r => setTimeout(r, 500));
        } catch (err) {
          errors.push(`Blog: Error fetching article ${article.url}: ${err.message}`);
        }
      }
    } catch (err) {
      errors.push(`Blog: Error processing ${blog.name}: ${err.message}`);
    }
  }

  return results;
}

// -- Prompts Loading ---------------------------------------------------------

async function loadPrompts() {
  const prompts = {};
  const localPromptsDir = join(PROJECT_DIR, 'prompts');
  const errors = [];

  for (const filename of PROMPT_FILES) {
    const key = filename.replace('.md', '').replace(/-/g, '_');
    const localPath = join(localPromptsDir, filename);

    if (existsSync(localPath)) {
      prompts[key] = await readFile(localPath, 'utf-8');
    } else {
      errors.push(`Could not load prompt: ${filename}`);
    }
  }

  return { prompts, errors };
}

// -- Main --------------------------------------------------------------------

async function main() {
  const errors = [];

  // 1. Validate dependencies (non-fatal: only yt-dlp is required)
  console.error('Validating dependencies...');
  const depErrors = await validateDependencies();

  // yt-dlp is the only hard dependency
  const ytDlpMissing = depErrors.find(e => e.includes('yt-dlp 未安装'));
  if (ytDlpMissing) {
    console.error(JSON.stringify({
      status: 'error',
      message: '依赖检查失败',
      errors: depErrors
    }, null, 2));
    process.exit(1);
  }

  // Twitter errors are warnings, not fatal
  const warnings = depErrors.filter(e => !e.includes('yt-dlp 未安装'));
  for (const w of warnings) {
    console.error(`  WARNING: ${w}`);
    errors.push(w);
  }

  // 2. Load config
  const config = await loadConfig();
  const lookbackHours = config.lookbackHours || DEFAULT_LOOKBACK_HOURS;
  console.error(`Time window: ${lookbackHours} hours`);

  // 3. Load sources from config, filter out disabled items
  const rawSources = config.sources || {};
  const sources = {
    x_accounts: (rawSources.x_accounts || []).filter(s => s.enabled !== false),
    podcasts: (rawSources.podcasts || []).filter(s => s.enabled !== false),
    blogs: (rawSources.blogs || []).filter(s => s.enabled !== false)
  };
  const state = await loadState();

  // 4. Fetch content
  console.error('Fetching X/Twitter content...');
  const xContent = await fetchXContent(sources.x_accounts, state, lookbackHours, errors);
  console.error(`  Found ${xContent.length} builders with new tweets`);

  console.error('Fetching YouTube content...');
  const podcasts = await fetchYouTubeContent(sources.podcasts, state, lookbackHours, errors);
  console.error(`  Found ${podcasts.length} new episodes`);

  console.error('Fetching blog content...');
  const blogContent = await fetchBlogContent(sources.blogs, state, lookbackHours, errors);
  console.error(`  Found ${blogContent.length} new blog post(s)`);

  // 5. Save dedup state
  await saveState(state);

  // 6. Load prompts
  const { prompts, errors: promptErrors } = await loadPrompts();
  errors.push(...promptErrors);

  // 7. Build output
  const output = {
    status: 'ok',
    generatedAt: new Date().toISOString(),

    config: {
      language: config.language || 'en'
    },

    podcasts,
    x: xContent,
    blogs: blogContent,

    stats: {
      podcastEpisodes: podcasts.length,
      xBuilders: xContent.length,
      totalTweets: xContent.reduce((sum, a) => sum + a.tweets.length, 0),
      blogPosts: blogContent.length
    },

    prompts,

    errors: errors.length > 0 ? errors : undefined
  };

  // Save to file
  const OUTPUT_PATH = join(PROJECT_DIR, 'digest-data.json');
  await writeFile(OUTPUT_PATH, JSON.stringify(output, null, 2));

  // Print to stdout
  console.log(JSON.stringify(output, null, 2));
}

main().catch(err => {
  console.error(JSON.stringify({
    status: 'error',
    message: err.message
  }, null, 2));
  process.exit(1);
});
