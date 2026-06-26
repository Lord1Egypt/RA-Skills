#!/usr/bin/env node

import { execFile } from 'child_process';
import { promisify } from 'util';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';
import { readFile, writeFile } from 'fs/promises';
import { enrichFeedXQuotes, enrichPodcastEpisodeLinks } from './prepare-digest.js';

const execFileAsync = promisify(execFile);
const SCRIPT_DIR = dirname(fileURLToPath(import.meta.url));
const PREPARE_SCRIPT = join(SCRIPT_DIR, 'prepare-digest.js');
const SEND_SCRIPT = join(SCRIPT_DIR, 'send-feishu-card.js');
const PROMPT_PATH = join(SCRIPT_DIR, '..', 'prompts', 'feishu-card-digest.md');
const DEFAULT_MODEL = 'openai-codex/gpt-5.4';
const DEFAULT_PAYLOAD_PATH = '/tmp/follow-builders-card-payload.json';
const MODEL_TIMEOUT_MS = 120000;
const PREPARE_TIMEOUT_MS = 120000;
const SEND_TIMEOUT_MS = 120000;
const MAX_PODCAST_TRANSCRIPT_CHARS = 12000;
const MAX_BLOG_CONTENT_CHARS = 8000;
const MAX_MODEL_REPAIR_PASSES = 2;
const MAX_FALLBACK_HEADLINE_CHARS = 72;
const MAX_FALLBACK_DETAIL_CHARS = 160;
const MAX_SOURCE_LABEL_CHARS = 15;
const MIN_X_READABLE_CHARS = 40;
const MIN_X_READABLE_WORDS = 8;
const MIN_X_KEEP_LIKES = 500;
const MIN_X_SECONDARY_LIKES = 250;
const MIN_X_QUOTED_READABLE_CHARS = 60;
const MIN_X_QUOTED_READABLE_WORDS = 10;
const MIN_PODCAST_SIGNAL_CHARS = 1200;
const MIN_BLOG_SIGNAL_CHARS = 400;
const MIN_BLOG_DESCRIPTION_CHARS = 120;
const SIGNAL_KEYWORD_PATTERN = /\b(ai|agent|agentic|model|llm|inference|training|evals?|benchmark|token(?:s)?|compute|gpu|security|privacy|browser|sdk|api|mcp|cli|tool(?:ing|s)?|workflow|automation|enterprise|customer|product|design|figma|coding|code|developer|software|sandbox|runtime|infrastructure|infra|platform|memory|voice|search|payment|stablecoin|crypto|blockchain|open\s+source|oss)\b|模型|智能体|推理|训练|评测|代码|编程|工作流|自动化|企业|安全|隐私|浏览器|产品|设计|开发者|软件|基础设施|支付|稳定币/iu;
const PROMO_ONLY_PATTERN = /\b(subscribe|get the full episode|available on|newsletter|spotify|apple\s+podcasts?|youtube channel|follow the show|sign up for emails|dm if you want to be a part of it|limited seating)\b/i;
const LOW_SIGNAL_PATTERN = /\b(raw recording|cabaret|jet lag|good morning|good night|on vacation|weekend vibes|show tonight|live performance)\b/i;
const SUPPLEMENTAL_QUOTE_PATTERN = /^(and\b|also\b|exactly\b|agree\b|same\b|yep\b|yes\b|nope\b|lol\b|wow\b|indeed\b|\+1\b|this\b|that\b)/i;
const PRAISE_ONLY_PATTERN = /\b(well done|grow up so fast|congrats|congratulations|proud of|love this|so proud|huge win|big win|amazing work|nice work)\b/i;

function log(level, message, context = {}) {
  const payload = { level, message };
  if (Object.keys(context).length > 0) {
    payload.context = context;
  }
  console.error(JSON.stringify(payload));
}

function parseArgs(argv) {
  const args = argv.slice(2);
  const parsed = {
    accountId: null,
    inputJsonPath: null,
    model: DEFAULT_MODEL,
    mode: 'openclaw_account',
    payloadPath: DEFAULT_PAYLOAD_PATH,
    skipSend: false,
    to: null
  };

  for (let i = 0; i < args.length; i += 1) {
    const arg = args[i];
    switch (arg) {
      case '--account':
        parsed.accountId = args[++i];
        break;
      case '--input-json':
        parsed.inputJsonPath = args[++i];
        break;
      case '--model':
        parsed.model = args[++i];
        break;
      case '--mode':
        parsed.mode = args[++i];
        break;
      case '--payload-out':
        parsed.payloadPath = args[++i];
        break;
      case '--skip-send':
        parsed.skipSend = true;
        break;
      case '--to':
        parsed.to = args[++i];
        break;
      default:
        throw new Error(`Unknown argument: ${arg}`);
    }
  }

  if (!parsed.skipSend && !parsed.to) {
    throw new Error('Missing required argument: --to');
  }

  return parsed;
}

async function runPrepareDigest() {
  log('info', 'Running prepare-digest.js');
  const { stdout } = await execFileAsync('node', [PREPARE_SCRIPT], {
    cwd: SCRIPT_DIR,
    maxBuffer: 16 * 1024 * 1024,
    timeout: PREPARE_TIMEOUT_MS
  });
  const parsed = JSON.parse(stdout);
  log('info', 'prepare-digest.js completed', {
    xBuilders: parsed?.stats?.xBuilders || 0,
    totalTweets: parsed?.stats?.totalTweets || 0
  });
  return parsed;
}

async function loadPreparedDigestFromFile(filePath) {
  log('info', 'Loading prepared digest JSON from file', { filePath });
  const raw = await readFile(filePath, 'utf-8');
  const parsed = JSON.parse(raw);
  const errors = Array.isArray(parsed.errors) ? [...parsed.errors] : [];

  if (parsed?.x?.some((builder) => (builder?.tweets || []).some((tweet) => tweet?.quotedTweetId && !tweet?.quotedTweet))) {
    const enriched = await enrichFeedXQuotes({ x: parsed.x }, errors);
    parsed.x = enriched.feedX?.x || parsed.x;
  }

  if (parsed?.podcasts?.length > 0) {
    const enrichedPodcasts = await enrichPodcastEpisodeLinks({ podcasts: parsed.podcasts }, errors);
    parsed.podcasts = enrichedPodcasts.feedPodcasts?.podcasts || parsed.podcasts;
  }

  if (errors.length > 0) {
    parsed.errors = errors;
  }
  return parsed;
}

function tweetEngagement(tweet) {
  return (tweet?.likes || 0) + (tweet?.retweets || 0) * 2 + (tweet?.replies || 0);
}

function countMeaningfulWords(text) {
  return collapseWhitespace(text)
    .split(/\s+/)
    .map((token) => token.trim())
    .filter(Boolean)
    .length;
}

function hasBuilderSignal(text) {
  return SIGNAL_KEYWORD_PATTERN.test(stripUrls(text));
}

function isPromoOnlyText(text) {
  return PROMO_ONLY_PATTERN.test(stripUrls(text));
}

function isLowSignalText(text) {
  return LOW_SIGNAL_PATTERN.test(stripUrls(text));
}

function getQuotedTweetText(tweet) {
  return collapseWhitespace(tweet?.quotedTweet?.text || '');
}

function getTweetContextText(tweet) {
  return [
    collapseWhitespace(tweet?.text || ''),
    getQuotedTweetText(tweet)
  ].filter(Boolean).join('\n\n');
}

function hasReadableText(text) {
  return Boolean(stripUrls(text));
}

function pickTweetHeadlineText(tweet) {
  const quotedText = getQuotedTweetText(tweet);
  if (hasReadableText(quotedText)) {
    return quotedText;
  }
  return collapseWhitespace(tweet?.text || '');
}

function isSupplementalQuoteComment(text) {
  const cleaned = stripUrls(text);
  if (!cleaned) return true;
  return cleaned.length < MIN_X_READABLE_CHARS && SUPPLEMENTAL_QUOTE_PATTERN.test(cleaned);
}

function classifyTweet(tweet) {
  const cleanedText = stripUrls(tweet.text || '');
  const quotedText = getQuotedTweetText(tweet);
  const combinedText = getTweetContextText(tweet);
  const engagement = tweetEngagement(tweet);
  const wordCount = countMeaningfulWords(cleanedText);
  const quotedWordCount = countMeaningfulWords(quotedText);
  const readableComment = cleanedText.length >= MIN_X_READABLE_CHARS || wordCount >= MIN_X_READABLE_WORDS;
  const readableQuoted = quotedText.length >= MIN_X_QUOTED_READABLE_CHARS || quotedWordCount >= MIN_X_QUOTED_READABLE_WORDS;
  const readable = readableComment || readableQuoted;
  const promoOnly = isPromoOnlyText(cleanedText) && (!quotedText || isPromoOnlyText(quotedText));
  const lowSignal = isLowSignalText(combinedText);
  const supplementalQuote = Boolean(tweet.isQuote) && isSupplementalQuoteComment(cleanedText);
  const praiseOnlyQuote = Boolean(tweet.isQuote)
    && !hasBuilderSignal(combinedText)
    && PRAISE_ONLY_PATTERN.test(combinedText);
  const strongSignal = hasBuilderSignal(combinedText);
  const valuable = readable
    && !promoOnly
    && !lowSignal
    && !praiseOnlyQuote
    && (!supplementalQuote || readableQuoted)
    && (strongSignal || Boolean(tweet.isQuote && readableQuoted) || (tweet.likes || 0) >= MIN_X_KEEP_LIKES);
  const keepPrimary = valuable && (tweet.likes || 0) >= MIN_X_KEEP_LIKES;
  const keepSecondary = valuable && (tweet.likes || 0) >= MIN_X_SECONDARY_LIKES;

  return {
    ...tweet,
    cleanedText,
    quotedText,
    combinedText,
    engagement,
    readable,
    readableComment,
    readableQuoted,
    promoOnly,
    lowSignal,
    supplementalQuote,
    praiseOnlyQuote,
    strongSignal,
    valuable,
    keepPrimary,
    keepSecondary
  };
}

function pickBuilders(raw) {
  const builders = Array.isArray(raw?.x) ? raw.x : [];
  return builders
    .map((builder) => {
      const rankedTweets = Array.isArray(builder.tweets)
        ? [...builder.tweets]
          .sort((a, b) => tweetEngagement(b) - tweetEngagement(a))
          .map((tweet) => classifyTweet({
            text: tweet.text,
            url: tweet.url,
            createdAt: tweet.createdAt,
            likes: tweet.likes,
            retweets: tweet.retweets,
            replies: tweet.replies,
            isQuote: tweet.isQuote,
            quotedTweetId: tweet.quotedTweetId,
            quotedTweet: tweet.quotedTweet || null
          }))
        : [];

      const primaryTweets = rankedTweets.filter((tweet) => tweet.keepPrimary);
      const secondaryTweets = primaryTweets.length > 0
        ? rankedTweets.filter((tweet) => !tweet.keepPrimary && tweet.keepSecondary)
        : [];
      const keptTweets = [...primaryTweets, ...secondaryTweets].slice(0, 3);

      return {
        name: builder.name,
        handle: builder.handle,
        bio: builder.bio,
        tweets: keptTweets
          .slice(0, 3)
          .map((tweet) => ({
            text: tweet.text,
            url: tweet.url,
            createdAt: tweet.createdAt,
            likes: tweet.likes,
            retweets: tweet.retweets,
            replies: tweet.replies,
            isQuote: tweet.isQuote,
            quotedTweetId: tweet.quotedTweetId,
            quotedTweet: tweet.quotedTweet || null
          }))
      };
    })
    .filter((builder) => builder.tweets.length > 0)
    ;
}

function pickPodcasts(raw) {
  const podcasts = Array.isArray(raw?.podcasts) ? raw.podcasts : [];
  return podcasts
    .map((episode) => {
      const transcriptExcerpt = String(episode.transcript || '').slice(0, MAX_PODCAST_TRANSCRIPT_CHARS);
      const signalText = `${episode.title || ''}\n${transcriptExcerpt}`;
      const keep = transcriptExcerpt.length >= MIN_PODCAST_SIGNAL_CHARS && hasBuilderSignal(signalText);

      if (!keep) return null;

      return {
        name: episode.name,
        title: episode.title,
        url: episode.url,
        show_url: episode.showUrl || episode.show_url || undefined,
        publishedAt: episode.publishedAt,
        transcript_excerpt: transcriptExcerpt
      };
    })
    .filter(Boolean);
}

function pickBlogs(raw) {
  const blogs = Array.isArray(raw?.blogs) ? raw.blogs : [];
  return blogs
    .map((post) => {
      const contentExcerpt = String(post.content || '').slice(0, MAX_BLOG_CONTENT_CHARS);
      const description = String(post.description || '');
      const signalText = `${post.title || ''}\n${description}\n${contentExcerpt}`;
      const keep = hasBuilderSignal(signalText)
        && (
          contentExcerpt.length >= MIN_BLOG_SIGNAL_CHARS
          || description.length >= MIN_BLOG_DESCRIPTION_CHARS
        );

      if (!keep) return null;

      return {
        name: post.name,
        title: post.title,
        url: post.url,
        publishedAt: post.publishedAt,
        author: post.author,
        description,
        content_excerpt: contentExcerpt
      };
    })
    .filter(Boolean);
}

function resolveFeedDate(raw) {
  return (
    toDateOnly(raw?.stats?.feedGeneratedAt)
    || toDateOnly(raw?.generatedAt)
    || new Date().toISOString().slice(0, 10)
  );
}

function buildCondensedFeed(raw) {
  const x = pickBuilders(raw);
  const podcasts = pickPodcasts(raw);
  const blogs = pickBlogs(raw);
  const originalX = Array.isArray(raw?.x) ? raw.x.length : 0;
  const originalPodcasts = Array.isArray(raw?.podcasts) ? raw.podcasts.length : 0;
  const originalBlogs = Array.isArray(raw?.blogs) ? raw.blogs.length : 0;

  return {
    date: resolveFeedDate(raw),
    language: raw?.config?.language || 'zh',
    generatedAt: raw?.generatedAt || null,
    stats: {
      ...(raw?.stats || {}),
      xBuilders: x.length,
      totalTweets: x.reduce((sum, builder) => sum + (builder.tweets?.length || 0), 0),
      podcastEpisodes: podcasts.length,
      blogPosts: blogs.length
    },
    filter_stats: {
      xFilteredOut: Math.max(0, originalX - x.length),
      podcastFilteredOut: Math.max(0, originalPodcasts - podcasts.length),
      blogFilteredOut: Math.max(0, originalBlogs - blogs.length)
    },
    x,
    podcasts,
    blogs
  };
}

function buildPrompt(template, condensedFeed, options = {}) {
  const hardRequirements = [
    'Create exactly one item for every source object present in the feed JSON.',
    'Do not omit any builder, podcast episode, or blog post that appears in the feed.',
    'If a source has weaker signal, make the item shorter instead of dropping it.',
    'When an item is based on multiple posts from the same person, preserve all relevant original links in source_links.',
    'If one person has multiple unrelated posts, keep them inside one item but split them into separate sections.',
    'For quote tweets, use the quoted original post content when it carries the main information and keep both the quote tweet URL and the original URL when both materially contribute.'
  ];

  if (typeof options.expectedItemCount === 'number') {
    hardRequirements.unshift(
      `The feed below contains exactly ${options.expectedItemCount} sources with new content, so the final JSON must contain exactly ${options.expectedItemCount} items.`
    );
  }

  if (options.repairContext) {
    hardRequirements.push(options.repairContext);
  }

  return [
    'You are generating a Feishu card payload for a daily AI builders digest.',
    'Return pure JSON only.',
    'Do not wrap the result in markdown fences.',
    '',
    'Hard requirements:',
    ...hardRequirements,
    '',
    'Follow these instructions exactly:',
    template.trim(),
    '',
    'Condensed source feed JSON:',
    JSON.stringify(condensedFeed, null, 2)
  ].join('\n');
}

function extractTrailingJson(rawText) {
  const match = rawText.match(/\{[\s\S]*\}\s*$/);
  if (!match) {
    throw new Error('Could not find JSON payload in model output');
  }
  return JSON.parse(match[0]);
}

async function runModel(prompt, model) {
  log('info', 'Calling model to generate structured card payload', { model });
  const { stdout } = await execFileAsync('openclaw', [
    'infer',
    'model',
    'run',
    '--model',
    model,
    '--json',
    '--prompt',
    prompt
  ], {
    cwd: SCRIPT_DIR,
    maxBuffer: 16 * 1024 * 1024,
    timeout: MODEL_TIMEOUT_MS
  });

  const response = extractTrailingJson(stdout);
  const text = response?.outputs?.[0]?.text;
  if (!text) {
    throw new Error('Model returned no text output');
  }

  log('info', 'Model response received', { model });
  return JSON.parse(text);
}

function collapseWhitespace(value) {
  return String(value || '').replace(/\s+/g, ' ').trim();
}

function truncateText(value, maxChars) {
  const collapsed = collapseWhitespace(value);
  if (!collapsed) return '';
  if (collapsed.length <= maxChars) return collapsed;
  return `${collapsed.slice(0, Math.max(1, maxChars - 1)).trimEnd()}…`;
}

function normalizeHandle(value) {
  return collapseWhitespace(value).replace(/^@/, '').toLowerCase();
}

function normalizeName(value) {
  return collapseWhitespace(value).toLowerCase();
}

function normalizeUrl(value) {
  if (!value) return '';
  try {
    const parsed = new URL(value);
    parsed.hash = '';
    if ((parsed.protocol === 'https:' && parsed.port === '443') || (parsed.protocol === 'http:' && parsed.port === '80')) {
      parsed.port = '';
    }
    return parsed.toString().replace(/\/$/, '');
  } catch {
    return String(value).trim().replace(/\/$/, '');
  }
}

function toDateOnly(value) {
  const text = collapseWhitespace(value);
  if (!text) return undefined;
  if (/^\d{4}-\d{2}-\d{2}/.test(text)) {
    return text.slice(0, 10);
  }
  const parsed = new Date(text);
  if (!Number.isNaN(parsed.getTime())) {
    return parsed.toISOString().slice(0, 10);
  }
  return text.slice(0, 10);
}

function latestDate(records, field) {
  return records
    .map((record) => toDateOnly(record?.[field]))
    .filter(Boolean)
    .sort()
    .at(-1);
}

function truncateLabel(value, maxChars = MAX_SOURCE_LABEL_CHARS) {
  const collapsed = collapseWhitespace(value);
  if (!collapsed) return '';
  if (collapsed.length <= maxChars) return collapsed;
  return `${collapsed.slice(0, Math.max(1, maxChars - 1)).trimEnd()}…`;
}

function stripUrls(value) {
  return collapseWhitespace(value).replace(/https?:\/\/\S+/gi, '').trim();
}

function normalizeSourceLinkLabel(label) {
  return collapseWhitespace(label).toLowerCase();
}

function isGenericSourceLinkLabel(label) {
  return /^(查看原文(?:\s*\d+)?)$/i.test(collapseWhitespace(label));
}

function pickEnglishKeywords(text, maxWords = 3) {
  const stopwords = new Set([
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'how',
    'i', 'if', 'in', 'into', 'is', 'it', 'its', 'just', 'more', 'most', 'new',
    'of', 'on', 'or', 'our', 'so', 'that', 'the', 'their', 'there', 'these',
    'this', 'to', 'up', 'we', 'with', 'you', 'your'
  ]);

  const tokens = stripUrls(text)
    .replace(/[^a-zA-Z0-9\s\-]/g, ' ')
    .split(/\s+/)
    .map((token) => token.trim())
    .filter(Boolean)
    .map((token) => token.replace(/^[^a-zA-Z0-9]+|[^a-zA-Z0-9]+$/g, ''))
    .filter((token) => token.length >= 3 && !stopwords.has(token.toLowerCase()));

  return tokens.slice(0, maxWords).map((token) => {
    const lower = token.toLowerCase();
    return lower === 'ai' ? 'AI' : lower.charAt(0).toUpperCase() + lower.slice(1);
  });
}

function inferShortLabelFromText(text) {
  const cleaned = stripUrls(text);
  if (!cleaned) return '查看原文';

  const lines = cleaned
    .split('\n')
    .map((line) => line.replace(/^[*\-•\s]+/, '').trim())
    .filter(Boolean);
  const candidate = lines.find((line) => /(agent|security|memory|payment|stablecoin|renderer|flicker|software|architect|pirate|compute|token|headless|atom|material)/i.test(line))
    || lines.find((line) => line.length >= 12)
    || lines[0]
    || cleaned;
  const lower = candidate.toLowerCase();

  if (/security|jevons|exploit/.test(lower)) return '安全 Jevons';
  if (/agent deployer|agent manager/.test(lower)) return 'Agent 新岗位';
  if (/chat era|agent transformation|enterprise.*agent|agents in the enterprise/.test(lower)) return '企业 Agent 化';
  if (/renderer|flicker/.test(lower)) return '新渲染器';
  if (/software factory/.test(lower)) return '软件工厂';
  if (/payment|stablecoin|usdc/.test(lower)) return '支付协议';
  if (/memory/.test(lower)) return '记忆架构';
  if (/pirate|architect/.test(lower)) return '海盗与建筑师';
  if (/open[- ]sourc|open agents|coding agent/.test(lower)) return '开源平台';
  if (/productive without producing|setup can feel productive/.test(lower)) return '伪进展提醒';
  if (/atoms|materials/.test(lower)) return 'AI for Atoms';
  if (/headless software/.test(lower)) return 'Headless 软件';
  if (/token|maxxing|compute budget/.test(lower)) return 'Token 预算';

  if (/[\u4e00-\u9fff]/.test(candidate)) {
    return truncateLabel(candidate);
  }

  const keywords = pickEnglishKeywords(candidate);
  if (keywords.length > 0) {
    return truncateLabel(keywords.join(' '));
  }

  return truncateLabel(candidate);
}

function inferShortLabelFromTitle(title) {
  const cleaned = stripUrls(title)
    .replace(/[|·•:]+/g, ' ')
    .trim();
  if (!cleaned) return '查看原文';
  if (/[\u4e00-\u9fff]/.test(cleaned)) return truncateLabel(cleaned);
  const keywords = pickEnglishKeywords(cleaned, 4);
  return truncateLabel((keywords.length > 0 ? keywords.join(' ') : cleaned));
}

function buildSourceLinks(entries, kind = 'generic') {
  const normalizedEntries = entries
    .map((entry) => {
      if (!entry) return null;
      if (typeof entry === 'string') {
        return { url: collapseWhitespace(entry) };
      }
      return {
        url: collapseWhitespace(entry.url),
        label: collapseWhitespace(entry.label),
        text: entry.text,
        title: entry.title
      };
    })
    .filter((entry) => entry?.url);

  return normalizedEntries.map((entry, index) => {
    let label = entry.label;
    if (!label || isGenericSourceLinkLabel(label)) {
      if (kind === 'x') {
        label = inferShortLabelFromText(entry.text || entry.title || '');
      } else {
        label = inferShortLabelFromTitle(entry.title || entry.text || '');
      }
    }

    return {
      label: label || (normalizedEntries.length === 1 ? '查看原文' : `查看原文 ${index + 1}`),
      url: entry.url
    };
  });
}

function mergeSourceLinks(primary = [], secondary = []) {
  const merged = [];
  const seen = new Set();

  for (const entry of [...primary, ...secondary]) {
    if (!entry?.url) continue;
    const normalized = normalizeUrl(entry.url);
    if (!normalized || seen.has(normalized)) continue;
    seen.add(normalized);
    merged.push({
      label: entry.label || (merged.length === 0 ? '查看原文' : `查看原文 ${merged.length + 1}`),
      url: entry.url
    });
  }

  for (const entry of secondary) {
    if (!entry?.url) continue;
    const normalized = normalizeUrl(entry.url);
    const existing = merged.find((item) => normalizeUrl(item.url) === normalized);
    if (!existing) continue;
    if (isGenericSourceLinkLabel(existing.label) && entry.label && !isGenericSourceLinkLabel(entry.label)) {
      existing.label = truncateLabel(entry.label);
    }
  }

  return merged;
}

function deriveIdentityFromBio(bio, fallback) {
  const collapsed = collapseWhitespace(bio);
  if (!collapsed) return fallback;
  const [head] = collapsed.split(/[|·•]/).map((part) => part.trim()).filter(Boolean);
  return truncateText(head || collapsed, 80) || fallback;
}

function buildSourceCatalog(condensedFeed) {
  const sources = [];

  for (const builder of Array.isArray(condensedFeed?.x) ? condensedFeed.x : []) {
    const handle = normalizeHandle(builder.handle);
    const sourceLinks = buildSourceLinks((builder.tweets || []).flatMap((tweet) => ([
      {
        url: tweet?.url,
        text: tweet?.text
      },
      ...(tweet?.quotedTweet?.url ? [{
        url: tweet.quotedTweet.url,
        text: tweet.quotedTweet.text
      }] : [])
    ])), 'x');
    if (sourceLinks.length === 0) continue;

    sources.push({
      key: `x:${handle || normalizeName(builder.name)}`,
      kind: 'x',
      feedItem: builder,
      person_name: builder.name || handle || 'Unknown Builder',
      person_handle: handle || undefined,
      person_identity: deriveIdentityFromBio(builder.bio, 'AI Builder'),
      profile_url: handle ? `https://x.com/${handle}` : sourceLinks[0].url,
      posted_at: latestDate(builder.tweets || [], 'createdAt'),
      source_label: 'X / Twitter',
      source_links: sourceLinks,
      source_url: sourceLinks[0].url
    });
  }

  for (const episode of Array.isArray(condensedFeed?.podcasts) ? condensedFeed.podcasts : []) {
    const sourceLinks = buildSourceLinks([{
      url: episode.url,
      title: episode.title
    }], 'podcast');
    if (sourceLinks.length === 0) continue;

    sources.push({
      key: `podcast:${normalizeUrl(episode.url) || normalizeName(episode.name)}`,
      kind: 'podcast',
      feedItem: episode,
      person_name: episode.name || 'Podcast',
      person_handle: undefined,
      person_identity: 'Podcast',
      profile_url: episode.show_url || episode.showUrl || episode.url,
      posted_at: toDateOnly(episode.publishedAt),
      source_label: 'Podcast',
      source_links: sourceLinks,
      source_url: sourceLinks[0].url
    });
  }

  for (const post of Array.isArray(condensedFeed?.blogs) ? condensedFeed.blogs : []) {
    const sourceLinks = buildSourceLinks([{
      url: post.url,
      title: post.title
    }], 'blog');
    if (sourceLinks.length === 0) continue;

    sources.push({
      key: `blog:${normalizeUrl(post.url) || normalizeName(post.name)}`,
      kind: 'blog',
      feedItem: post,
      person_name: post.name || post.author || 'Blog',
      person_handle: undefined,
      person_identity: post.author ? `${post.author} · Blog` : 'Blog',
      profile_url: post.url,
      posted_at: toDateOnly(post.publishedAt),
      source_label: 'Blog',
      source_links: sourceLinks,
      source_url: sourceLinks[0].url
    });
  }

  return sources;
}

function buildSourceIndex(sourceCatalog) {
  const byHandle = new Map();
  const byName = new Map();
  const byNameAndLabel = new Map();
  const byProfileUrl = new Map();
  const bySourceUrl = new Map();
  const byKey = new Map();

  for (const source of sourceCatalog) {
    byKey.set(source.key, source);

    if (source.person_handle) {
      byHandle.set(normalizeHandle(source.person_handle), source);
    }

    const normalizedName = normalizeName(source.person_name);
    if (normalizedName) {
      const existing = byName.get(normalizedName) || [];
      existing.push(source);
      byName.set(normalizedName, existing);
    }

    const nameAndLabelKey = `${normalizedName}::${normalizeName(source.source_label)}`;
    if (normalizedName) {
      byNameAndLabel.set(nameAndLabelKey, source);
    }

    const normalizedProfileUrl = normalizeUrl(source.profile_url);
    if (normalizedProfileUrl) {
      byProfileUrl.set(normalizedProfileUrl, source);
    }

    for (const link of source.source_links) {
      const normalizedLinkUrl = normalizeUrl(link.url);
      if (normalizedLinkUrl) {
        bySourceUrl.set(normalizedLinkUrl, source);
      }
    }
  }

  return {
    byHandle,
    byKey,
    byName,
    byNameAndLabel,
    byProfileUrl,
    bySourceUrl,
    sourceCatalog
  };
}

function matchSource(item, sourceIndex) {
  const handleCandidates = [item.person_handle, item.handle];
  for (const handleCandidate of handleCandidates) {
    const normalizedHandle = normalizeHandle(handleCandidate);
    if (normalizedHandle && sourceIndex.byHandle.has(normalizedHandle)) {
      return sourceIndex.byHandle.get(normalizedHandle);
    }
  }

  const urlCandidates = [
    item.profile_url,
    item.source_url,
    item.url,
    ...(Array.isArray(item.source_links) ? item.source_links.map((entry) => entry?.url) : []),
    ...flattenSectionSourceLinks(extractSections(item)).map((entry) => entry?.url)
  ];

  for (const urlCandidate of urlCandidates) {
    const normalizedUrlValue = normalizeUrl(urlCandidate);
    if (!normalizedUrlValue) continue;
    if (sourceIndex.bySourceUrl.has(normalizedUrlValue)) {
      return sourceIndex.bySourceUrl.get(normalizedUrlValue);
    }
    if (sourceIndex.byProfileUrl.has(normalizedUrlValue)) {
      return sourceIndex.byProfileUrl.get(normalizedUrlValue);
    }
  }

  const normalizedName = normalizeName(item.person_name || item.name);
  const normalizedLabel = normalizeName(item.source_label);
  if (normalizedName && normalizedLabel) {
    const keyed = sourceIndex.byNameAndLabel.get(`${normalizedName}::${normalizedLabel}`);
    if (keyed) return keyed;
  }

  if (normalizedName && sourceIndex.byName.has(normalizedName)) {
    const candidates = sourceIndex.byName.get(normalizedName);
    if (candidates.length === 1) {
      return candidates[0];
    }
  }

  return null;
}

function pickNonEmpty(...values) {
  for (const value of values) {
    if (Array.isArray(value) && value.length > 0) return value;
    if (typeof value === 'string' && collapseWhitespace(value)) return value;
    if (value && typeof value === 'object') return value;
  }
  return values.at(-1);
}

function extractHighlightDetails(highlights) {
  return (Array.isArray(highlights) ? highlights : [])
    .map((highlight) => {
      if (!highlight) return '';
      if (typeof highlight === 'string') return collapseWhitespace(highlight);
      return collapseWhitespace(highlight.detail || highlight.text || '');
    })
    .filter(Boolean);
}

function isInterpretiveSentence(text) {
  return /^(这意味着|意味着|值得注意的是|可以看出|说明了|背后的意思是|潜台词是|本质上|换句话说)/.test(collapseWhitespace(text));
}

function deriveBodyFromItem(item) {
  const directBody = collapseWhitespace(
    item?.body
    || item?.detail
    || item?.summary_text
  );
  if (directBody) {
    return directBody;
  }

  const parts = [
    collapseWhitespace(item?.translation || item?.subtitle || item?.title_translation || ''),
    ...extractHighlightDetails(item?.highlights).filter((detail) => !isInterpretiveSentence(detail))
  ].filter(Boolean);

  if (parts.length === 0) return '';
  return truncateText(parts.join(' '), 360);
}

function normalizeSourceLinkEntries(entries = [], fallbackUrl = null) {
  const normalized = [];

  for (const entry of Array.isArray(entries) ? entries : []) {
    if (!entry) continue;
    if (typeof entry === 'string') {
      normalized.push({ label: '查看原文', url: entry });
      continue;
    }
    if (entry.url) {
      normalized.push({
        label: truncateLabel(entry.label || '查看原文'),
        url: entry.url
      });
    }
  }

  if (normalized.length === 0 && fallbackUrl) {
    normalized.push({
      label: '查看原文',
      url: fallbackUrl
    });
  }

  return normalized;
}

function normalizeSection(section) {
  if (!section || typeof section !== 'object') return null;

  const sourceLinks = normalizeSourceLinkEntries(section.source_links, section.source_url || section.url);
  const body = deriveBodyFromItem(section) || undefined;
  const headline = collapseWhitespace(section.headline || section.title || '')
    || truncateText(body || sourceLinks[0]?.label || '原文', MAX_FALLBACK_HEADLINE_CHARS);

  if (!headline && !body && sourceLinks.length === 0) {
    return null;
  }

  return {
    headline,
    body,
    source_links: sourceLinks
  };
}

function buildLegacySectionFromItem(item) {
  return normalizeSection({
    headline: item.headline || item.title,
    body: item.body,
    detail: item.detail,
    summary_text: item.summary_text,
    translation: item.translation,
    subtitle: item.subtitle,
    title_translation: item.title_translation,
    highlights: item.highlights,
    source_links: item.source_links,
    source_url: item.source_url,
    url: item.url
  });
}

function extractSections(item) {
  const sections = (Array.isArray(item?.sections) ? item.sections : [])
    .map(normalizeSection)
    .filter(Boolean);

  if (sections.length > 0) {
    return sections;
  }

  const legacySection = buildLegacySectionFromItem(item);
  return legacySection ? [legacySection] : [];
}

function flattenSectionSourceLinks(sections) {
  return (Array.isArray(sections) ? sections : [])
    .flatMap((section) => Array.isArray(section?.source_links) ? section.source_links : []);
}

function buildSectionKey(section) {
  const urls = (Array.isArray(section?.source_links) ? section.source_links : [])
    .map((entry) => normalizeUrl(entry?.url))
    .filter(Boolean)
    .sort();

  if (urls.length > 0) {
    return urls.join('|');
  }

  return `${normalizeName(section?.headline)}::${normalizeName(section?.body)}`;
}

function mergeSections(primary = [], secondary = []) {
  const merged = [];
  const indexByKey = new Map();

  for (const section of [...primary, ...secondary]) {
    const normalized = normalizeSection(section);
    if (!normalized) continue;

    const key = buildSectionKey(normalized);
    if (!indexByKey.has(key)) {
      indexByKey.set(key, merged.length);
      merged.push(normalized);
      continue;
    }

    const existingIndex = indexByKey.get(key);
    const existing = merged[existingIndex];
    merged[existingIndex] = {
      headline: pickNonEmpty(existing.headline, normalized.headline),
      body: pickPreferredParagraph(existing.body, normalized.body),
      source_links: mergeSourceLinks(existing.source_links, normalized.source_links)
    };
  }

  return merged;
}

function pickPreferredParagraph(...values) {
  const normalized = values
    .map((value) => collapseWhitespace(value))
    .filter(Boolean);

  if (normalized.length === 0) return '';
  return normalized.sort((a, b) => b.length - a.length)[0];
}

function hydrateItemFromSource(item, source) {
  const allowedUrls = new Set((source.source_links || []).map((entry) => normalizeUrl(entry.url)).filter(Boolean));
  const sections = extractSections(item)
    .map((section) => ({
      ...section,
      source_links: (Array.isArray(section.source_links) ? section.source_links : [])
        .filter((entry) => entry?.url && allowedUrls.has(normalizeUrl(entry.url)))
    }))
    .filter((section) => section.headline || section.body || section.source_links.length > 0);

  const itemLinks = normalizeSourceLinkEntries(item.source_links, item.source_url || item.url)
    .filter((entry) => entry?.url && allowedUrls.has(normalizeUrl(entry.url)));
  const sectionLinks = flattenSectionSourceLinks(sections);
  const sourceLinks = mergeSourceLinks(mergeSourceLinks(itemLinks, sectionLinks), source.source_links);
  const hydratedSections = sections.length > 0
    ? sections
    : [{
      headline: pickNonEmpty(item.headline, item.title, source.person_name),
      body: deriveBodyFromItem(item) || undefined,
      source_links: sourceLinks
    }];
  const primarySection = hydratedSections[0];

  return {
    ...item,
    _sourceKey: source.key,
    person_name: pickNonEmpty(item.person_name, item.name, source.person_name),
    person_handle: pickNonEmpty(item.person_handle, item.handle, source.person_handle),
    person_identity: pickNonEmpty(item.person_identity, item.identity, item.role, source.person_identity),
    profile_url: pickNonEmpty(item.profile_url, item.author_url, item.source_profile_url, source.profile_url, source.source_url),
    posted_at: pickNonEmpty(item.posted_at, item.published_at, source.posted_at),
    source_label: pickNonEmpty(item.source_label, source.source_label),
    headline: pickNonEmpty(item.headline, item.title, primarySection?.headline),
    title: pickNonEmpty(item.title, item.headline, primarySection?.headline),
    body: pickPreferredParagraph(item.body, primarySection?.body, deriveBodyFromItem(item)),
    sections: hydratedSections,
    source_links: sourceLinks,
    source_url: pickNonEmpty(itemLinks[0]?.url, item.source_url, item.url, sourceLinks[0]?.url, source.source_url),
    url: pickNonEmpty(itemLinks[0]?.url, item.url, item.source_url, sourceLinks[0]?.url, source.source_url)
  };
}

function mergeDuplicateItems(existing, incoming) {
  const mergedSections = mergeSections(existing.sections, incoming.sections);
  const mergedSourceLinks = mergeSourceLinks(
    mergeSourceLinks(existing.source_links, incoming.source_links),
    flattenSectionSourceLinks(mergedSections)
  );
  const primarySection = mergedSections[0];
  return {
    ...existing,
    _sourceKey: existing._sourceKey,
    person_name: pickNonEmpty(existing.person_name, incoming.person_name),
    person_handle: pickNonEmpty(existing.person_handle, incoming.person_handle),
    person_identity: pickNonEmpty(existing.person_identity, incoming.person_identity),
    profile_url: pickNonEmpty(existing.profile_url, incoming.profile_url),
    posted_at: pickNonEmpty(existing.posted_at, incoming.posted_at),
    source_label: pickNonEmpty(existing.source_label, incoming.source_label),
    headline: pickNonEmpty(existing.headline, incoming.headline, primarySection?.headline),
    title: pickNonEmpty(existing.title, incoming.title, primarySection?.headline),
    body: pickPreferredParagraph(
      existing.body,
      incoming.body,
      primarySection?.body,
      deriveBodyFromItem(existing),
      deriveBodyFromItem(incoming)
    ),
    summary: pickNonEmpty(existing.summary, incoming.summary),
    sections: mergedSections,
    source_links: mergedSourceLinks,
    source_url: pickNonEmpty(existing.source_url, incoming.source_url, mergedSourceLinks[0]?.url),
    url: pickNonEmpty(existing.url, incoming.url, mergedSourceLinks[0]?.url)
  };
}

function stripInternalFields(item) {
  const { _sourceKey, ...rest } = item;
  return rest;
}

function materializeGeneratedItems(items, sourceIndex) {
  const normalizedItems = [];
  const matchedSourceKeys = new Set();
  const unmatchedItems = [];

  for (const item of Array.isArray(items) ? items.map(normalizeItem) : []) {
    const source = matchSource(item, sourceIndex);
    if (!source) {
      unmatchedItems.push(item);
      continue;
    }

    const hydrated = hydrateItemFromSource(item, source);
    const existingIndex = normalizedItems.findIndex((entry) => entry._sourceKey === source.key);
    if (existingIndex >= 0) {
      normalizedItems[existingIndex] = mergeDuplicateItems(normalizedItems[existingIndex], hydrated);
    } else {
      normalizedItems.push(hydrated);
    }
    matchedSourceKeys.add(source.key);
  }

  return {
    items: normalizedItems,
    matchedSourceKeys,
    unmatchedItems
  };
}

function buildSubsetFeed(condensedFeed, missingSources) {
  return {
    date: condensedFeed.date,
    language: condensedFeed.language,
    generatedAt: condensedFeed.generatedAt,
    stats: {
      xBuilders: missingSources.filter((source) => source.kind === 'x').length,
      podcastEpisodes: missingSources.filter((source) => source.kind === 'podcast').length,
      blogPosts: missingSources.filter((source) => source.kind === 'blog').length,
      totalTweets: missingSources
        .filter((source) => source.kind === 'x')
        .reduce((sum, source) => sum + ((source.feedItem?.tweets || []).length), 0),
      feedGeneratedAt: condensedFeed.stats?.feedGeneratedAt || null
    },
    x: missingSources.filter((source) => source.kind === 'x').map((source) => source.feedItem),
    podcasts: missingSources.filter((source) => source.kind === 'podcast').map((source) => source.feedItem),
    blogs: missingSources.filter((source) => source.kind === 'blog').map((source) => source.feedItem)
  };
}

function buildFallbackItem(source) {
  if (source.kind === 'x') {
    const sections = (source.feedItem?.tweets || []).map((tweet) => {
      const sectionLinks = buildSourceLinks([
        {
          url: tweet?.url,
          text: tweet?.text
        },
        ...(tweet?.quotedTweet?.url ? [{
          url: tweet.quotedTweet.url,
          text: tweet.quotedTweet.text
        }] : [])
      ], 'x');
      const bodyParts = [
        hasReadableText(tweet?.quotedTweet?.text || '') ? collapseWhitespace(tweet?.quotedTweet?.text || '') : '',
        collapseWhitespace(tweet?.text || '')
      ].filter(Boolean);

      return {
        headline: truncateText(
          pickTweetHeadlineText(tweet)
          || `${source.person_name} 今日更新`,
          MAX_FALLBACK_HEADLINE_CHARS
        ),
        body: truncateText(bodyParts.join(' '), 360) || undefined,
        source_links: sectionLinks
      };
    }).filter((section) => section.headline || section.body || (section.source_links || []).length > 0);
    const primarySection = sections[0];

    return {
      _sourceKey: source.key,
      person_name: source.person_name,
      person_handle: source.person_handle,
      person_identity: source.person_identity,
      profile_url: source.profile_url,
      source_label: source.source_label,
      posted_at: source.posted_at,
      headline: primarySection?.headline || `${source.person_name} 今日更新`,
      body: primarySection?.body || `今天共抓到 ${source.source_links.length} 条更新，原文链接已全部保留。`,
      sections,
      source_links: mergeSourceLinks(flattenSectionSourceLinks(sections), source.source_links),
      source_url: source.source_url
    };
  }

  if (source.kind === 'podcast') {
    const transcriptExcerpt = source.feedItem?.transcript_excerpt || source.feedItem?.title;
    const sections = [{
      headline: truncateText(source.feedItem?.title || `${source.person_name} Podcast 更新`, MAX_FALLBACK_HEADLINE_CHARS),
      body: truncateText(transcriptExcerpt, 360) || '这期播客已纳入本次卡片，若模型摘要缺失，请直接查看原文。',
      source_links: source.source_links
    }];
    return {
      _sourceKey: source.key,
      person_name: source.person_name,
      person_identity: source.person_identity,
      profile_url: source.profile_url,
      source_label: source.source_label,
      posted_at: source.posted_at,
      headline: sections[0].headline,
      body: sections[0].body,
      sections,
      source_links: source.source_links,
      source_url: source.source_url
    };
  }

  const blogText = source.feedItem?.description || source.feedItem?.content_excerpt || source.feedItem?.title;
  const sections = [{
    headline: truncateText(source.feedItem?.title || `${source.person_name} Blog 更新`, MAX_FALLBACK_HEADLINE_CHARS),
    body: truncateText(blogText, 360) || '这篇博客已纳入本次卡片，若模型摘要缺失，请直接查看原文。',
    source_links: source.source_links
  }];
  return {
    _sourceKey: source.key,
    person_name: source.person_name,
    person_identity: source.person_identity,
    profile_url: source.profile_url,
    source_label: source.source_label,
    posted_at: source.posted_at,
    headline: sections[0].headline,
    body: sections[0].body,
    sections,
    source_links: source.source_links,
    source_url: source.source_url
  };
}

function normalizeItem(item) {
  const handle = item.person_handle || item.handle || '';
  const cleanHandle = handle.replace(/^@/, '');
  const profileUrl = item.profile_url || (cleanHandle ? `https://x.com/${cleanHandle}` : null);
  const sections = extractSections(item);
  const sourceLinks = mergeSourceLinks(
    normalizeSourceLinkEntries(item.source_links, item.source_url || item.url),
    flattenSectionSourceLinks(sections)
  );
  const primarySection = sections[0];
  return {
    ...item,
    headline: collapseWhitespace(item.headline || item.title || '') || primarySection?.headline,
    title: collapseWhitespace(item.title || item.headline || '') || primarySection?.headline,
    body: pickPreferredParagraph(item.body, primarySection?.body, deriveBodyFromItem(item)) || undefined,
    person_handle: cleanHandle || undefined,
    profile_url: profileUrl || item.source_url || item.url,
    sections,
    source_links: sourceLinks
      .filter((entry) => entry && entry.url)
      .map((entry) => ({
        label: truncateLabel(entry.label || '查看原文'),
        url: entry.url
      }))
  };
}

async function finalizePayload(payload, context) {
  const {
    condensedFeed,
    model,
    repairRunner = runModel,
    raw,
    skipRepair = false,
    sourceCatalog,
    sourceIndex,
    template
  } = context;

  if (!payload || typeof payload !== 'object') {
    throw new Error('Generated payload is not a JSON object');
  }
  if (!Array.isArray(payload.items) || payload.items.length === 0) {
    throw new Error('Generated payload has no items');
  }

  const itemMap = new Map();
  const sourceOrder = sourceCatalog.map((source) => source.key);
  const registerItems = (items) => {
    for (const item of items) {
      const existing = itemMap.get(item._sourceKey);
      itemMap.set(item._sourceKey, existing ? mergeDuplicateItems(existing, item) : item);
    }
  };

  const firstPass = materializeGeneratedItems(payload.items, sourceIndex);
  registerItems(firstPass.items);

  log('info', 'Initial card payload coverage analyzed', {
    expectedSources: sourceCatalog.length,
    matchedSources: itemMap.size,
    unmatchedItems: firstPass.unmatchedItems.length
  });

  let missingSources = sourceCatalog.filter((source) => !itemMap.has(source.key));

  for (let attempt = 1; !skipRepair && attempt <= MAX_MODEL_REPAIR_PASSES && missingSources.length > 0; attempt += 1) {
    try {
      const subsetFeed = buildSubsetFeed(condensedFeed, missingSources);
      const repairPrompt = buildPrompt(template, subsetFeed, {
        expectedItemCount: missingSources.length,
        repairContext: `A previous pass omitted ${missingSources.length} sources. This repair pass must cover every source in the subset feed below.`
      });
      const repairedPayload = await repairRunner(repairPrompt, model);
      const repairedItems = materializeGeneratedItems(repairedPayload.items, sourceIndex);
      registerItems(repairedItems.items);

      log('info', 'Repair pass completed', {
        attempt,
        requestedSources: missingSources.length,
        repairedMatches: repairedItems.items.length,
        unmatchedItems: repairedItems.unmatchedItems.length
      });

      missingSources = sourceCatalog.filter((source) => !itemMap.has(source.key));
    } catch (error) {
      log('warning', 'Repair pass failed, switching to deterministic fallback', {
        attempt,
        error: error.message
      });
      break;
    }
  }

  if (missingSources.length > 0) {
    log('warning', 'Using deterministic fallback items for missing sources', {
      missingSources: missingSources.length,
      missingKeys: missingSources.map((source) => source.key)
    });
    registerItems(missingSources.map(buildFallbackItem));
  }

  const orderedItems = sourceOrder
    .map((sourceKey) => itemMap.get(sourceKey))
    .filter(Boolean)
    .map(stripInternalFields);

  return {
    date: payload.date || condensedFeed.date,
    title: payload.title || `AI Builders Daily · ${condensedFeed.date}`,
    summary: payload.summary || payload.top_takeaway || '',
    items: orderedItems,
    source_count: sourceCatalog.length,
    source_stats: raw?.stats || {}
  };
}

async function sendCard(payloadPath, to, accountId, mode) {
  log('info', 'Sending generated payload via send-feishu-card.js', {
    payloadPath,
    accountId,
    mode
  });

  const sendArgs = [
    SEND_SCRIPT,
    '--file',
    payloadPath,
    '--to',
    to,
    '--mode',
    mode || 'openclaw_account'
  ];

  if (accountId) {
    sendArgs.push('--account', accountId);
  }

  const { stdout } = await execFileAsync('node', sendArgs, {
    cwd: SCRIPT_DIR,
    maxBuffer: 16 * 1024 * 1024,
    timeout: SEND_TIMEOUT_MS
  });

  return stdout.trim();
}

async function main() {
  const args = parseArgs(process.argv);
  log('info', 'Feishu digest pipeline started', {
    model: args.model,
    accountId: args.accountId,
    mode: args.mode
  });

  const raw = args.inputJsonPath
    ? await loadPreparedDigestFromFile(args.inputJsonPath)
    : await runPrepareDigest();
  const template = await readFile(PROMPT_PATH, 'utf-8');
  const condensedFeed = buildCondensedFeed(raw);
  const sourceCatalog = buildSourceCatalog(condensedFeed);
  const sourceIndex = buildSourceIndex(sourceCatalog);

  log('info', 'Applied source quality filters', {
    keptXBuilders: condensedFeed.x.length,
    keptTweets: condensedFeed.stats?.totalTweets || 0,
    keptPodcasts: condensedFeed.podcasts.length,
    keptBlogs: condensedFeed.blogs.length,
    xFilteredOut: condensedFeed.filter_stats?.xFilteredOut || 0,
    podcastFilteredOut: condensedFeed.filter_stats?.podcastFilteredOut || 0,
    blogFilteredOut: condensedFeed.filter_stats?.blogFilteredOut || 0
  });

  if (sourceCatalog.length === 0) {
    const skipped = {
      status: 'skipped',
      reason: 'no_relevant_sources',
      date: condensedFeed.date,
      filter_stats: condensedFeed.filter_stats
    };
    log('info', 'No sources passed quality filters, skipping card generation', skipped);
    process.stdout.write(`${JSON.stringify(skipped)}\n`);
    return;
  }

  const prompt = buildPrompt(template, condensedFeed, {
    expectedItemCount: sourceCatalog.length
  });

  let normalized;
  try {
    const generated = await runModel(prompt, args.model);
    normalized = await finalizePayload(generated, {
      condensedFeed,
      model: args.model,
      raw,
      sourceCatalog,
      sourceIndex,
      template
    });
  } catch (error) {
    log('warning', 'Model generation failed, falling back to deterministic payload', {
      error: error.message
    });
    normalized = await finalizePayload({
      date: condensedFeed.date,
      title: `AI Builders Daily · ${condensedFeed.date}`,
      summary: '',
      items: []
    }, {
      condensedFeed,
      model: args.model,
      raw,
      sourceCatalog,
      sourceIndex,
      template,
      skipRepair: true
    });
  }

  await writeFile(args.payloadPath, JSON.stringify(normalized, null, 2));
  log('info', 'Structured payload written', {
    payloadPath: args.payloadPath,
    items: normalized.items.length,
    expectedSources: sourceCatalog.length
  });

  if (args.skipSend) {
    log('info', 'Feishu digest pipeline completed without sending', {
      payloadPath: args.payloadPath
    });
    process.stdout.write(`${JSON.stringify({ status: 'ok', skippedSend: true, payloadPath: args.payloadPath })}\n`);
    return;
  }

  const sendResult = await sendCard(args.payloadPath, args.to, args.accountId, args.mode);
  log('info', 'Feishu digest pipeline completed');
  process.stdout.write(`${sendResult}\n`);
}

export {
  buildCondensedFeed,
  buildSourceCatalog,
  buildSourceIndex,
  finalizePayload
};

const IS_ENTRYPOINT = process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1];

if (IS_ENTRYPOINT) {
  main().catch((error) => {
    log('error', 'Feishu digest pipeline failed', {
      error: error.message,
      stack: error.stack
    });
    process.exit(1);
  });
}
