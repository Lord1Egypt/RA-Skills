#!/usr/bin/env node

// ============================================================================
// Follow Builders — Prepare Digest
// ============================================================================
// Gathers everything the LLM needs to produce a digest:
// - Fetches the central feeds (tweets + podcasts)
// - Fetches the latest prompts from GitHub
// - Reads the user's config (language, delivery method)
// - Outputs a single JSON blob to stdout
//
// The LLM's ONLY job is to read this JSON, remix the content, and output
// the digest text. Everything else is handled here deterministically.
//
// Usage: node prepare-digest.js
// Output: JSON to stdout
// ============================================================================

import { join, dirname } from 'path';
import { homedir } from 'os';
import { fileURLToPath } from 'url';
import {
  loadConfig,
  loadDefaultSources,
  loadPrompts
} from './prepare-digest-local.js';
import {
  fetchJSON,
  fetchPodcastRss,
  fetchQuotedTweetOEmbed,
  fetchText
} from './prepare-digest-remote.js';

const USER_DIR = join(homedir(), '.follow-builders');
const CONFIG_PATH = join(USER_DIR, 'config.json');
const SCRIPT_DIR = dirname(fileURLToPath(import.meta.url));
const SOURCES_PATH = join(SCRIPT_DIR, '..', 'config', 'default-sources.json');
const FEED_X_URL = 'https://raw.githubusercontent.com/zarazhangrui/follow-builders/main/feed-x.json';
const FEED_PODCASTS_URL = 'https://raw.githubusercontent.com/zarazhangrui/follow-builders/main/feed-podcasts.json';
const FEED_BLOGS_URL = 'https://raw.githubusercontent.com/zarazhangrui/follow-builders/main/feed-blogs.json';

const PROMPTS_BASE = 'https://raw.githubusercontent.com/zarazhangrui/follow-builders/main/prompts';
const PROMPT_FILES = [
  'summarize-podcast.md',
  'summarize-tweets.md',
  'summarize-blogs.md',
  'digest-intro.md',
  'translate.md'
];

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

function normalizeUrl(value) {
  const raw = collapseWhitespace(value);
  if (!raw) return null;
  try {
    const parsed = new URL(raw);
    parsed.hash = '';
    return parsed.toString().replace(/\/$/, '');
  } catch {
    return raw.replace(/\/$/, '');
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

function normalizeComparableText(value) {
  return decodeHtmlEntities(value)
    .toLowerCase()
    .replace(/[^a-z0-9\u4e00-\u9fff]+/gi, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function parseRssFeed(xml) {
  const episodes = [];
  const itemRegex = /<item>([\s\S]*?)<\/item>/gi;
  let itemMatch;
  while ((itemMatch = itemRegex.exec(xml)) !== null) {
    const block = itemMatch[1];
    const titleMatch = block.match(/<title><!\[CDATA\[([\s\S]*?)\]\]><\/title>/)
      || block.match(/<title>([\s\S]*?)<\/title>/);
    const guidMatch = block.match(/<guid[^>]*><!\[CDATA\[([\s\S]*?)\]\]><\/guid>/)
      || block.match(/<guid[^>]*>([\s\S]*?)<\/guid>/);
    const pubDateMatch = block.match(/<pubDate>([\s\S]*?)<\/pubDate>/);
    const linkMatch = block.match(/<link>([\s\S]*?)<\/link>/);

    episodes.push({
      title: decodeHtmlEntities(titleMatch ? titleMatch[1].trim() : ''),
      guid: guidMatch ? guidMatch[1].trim() : null,
      publishedAt: pubDateMatch ? new Date(pubDateMatch[1].trim()).toISOString() : null,
      link: linkMatch ? linkMatch[1].trim() : null
    });
  }
  return episodes;
}

function isConcretePodcastEpisodeUrl(value) {
  const url = normalizeUrl(value);
  if (!url) return false;

  try {
    const parsed = new URL(url);
    const host = parsed.hostname.replace(/^www\./i, '').toLowerCase();
    const path = parsed.pathname || '';

    if (host === 'youtube.com' || host === 'm.youtube.com') {
      if (path === '/watch' && parsed.searchParams.get('v')) return true;
      return false;
    }

    if (host === 'youtu.be') {
      return Boolean(path.replace(/^\//, ''));
    }

    if (/youtube\.com$/i.test(host)) {
      return false;
    }

    return true;
  } catch {
    return false;
  }
}

function needsPodcastLinkRepair(episode, source) {
  const url = normalizeUrl(episode?.url);
  const showUrl = normalizeUrl(episode?.showUrl || episode?.show_url || source?.url);
  if (!isConcretePodcastEpisodeUrl(url)) return true;
  if (showUrl && url === showUrl) return true;
  return false;
}

function findMatchingEpisodeLink(episode, rssEpisodes) {
  const guid = collapseWhitespace(episode?.guid);
  if (guid) {
    const exactGuid = rssEpisodes.find((entry) => collapseWhitespace(entry.guid) === guid && entry.link);
    if (exactGuid) return exactGuid.link;
  }

  const normalizedTitle = normalizeComparableText(episode?.title);
  if (!normalizedTitle) return null;

  const exactTitle = rssEpisodes.find((entry) => normalizeComparableText(entry.title) === normalizedTitle && entry.link);
  if (exactTitle) return exactTitle.link;

  const fuzzyTitle = rssEpisodes.find((entry) => {
    const candidate = normalizeComparableText(entry.title);
    return candidate && (candidate.includes(normalizedTitle) || normalizedTitle.includes(candidate));
  });
  return fuzzyTitle?.link || null;
}

async function enrichFeedXQuotes(feedX, errors = []) {
  if (!feedX?.x || !Array.isArray(feedX.x)) {
    return { feedX, enrichedCount: 0 };
  }

  const quoteIds = [...new Set(
    feedX.x
      .flatMap((builder) => Array.isArray(builder?.tweets) ? builder.tweets : [])
      .map((tweet) => tweet?.quotedTweetId)
      .filter((tweetId, index, all) => (
        tweetId
        && !all.slice(0, index).includes(tweetId)
      ))
  )];

  if (quoteIds.length === 0) {
    return { feedX, enrichedCount: 0 };
  }

  const quoteMap = new Map();

  for (const tweetId of quoteIds) {
    try {
      const quotedTweet = await fetchQuotedTweetOEmbed(tweetId);
      if (quotedTweet?.text || quotedTweet?.url) {
        quoteMap.set(tweetId, quotedTweet);
      }
    } catch (error) {
      errors.push(`Could not enrich quoted tweet ${tweetId}: ${error.message}`);
    }
  }

  let enrichedCount = 0;
  const enrichedFeedX = {
    ...feedX,
    x: feedX.x.map((builder) => ({
      ...builder,
      tweets: (Array.isArray(builder?.tweets) ? builder.tweets : []).map((tweet) => {
        if (!tweet?.quotedTweetId || tweet?.quotedTweet) {
          return tweet;
        }

        const quotedTweet = quoteMap.get(tweet.quotedTweetId);
        if (!quotedTweet) {
          return tweet;
        }

        enrichedCount += 1;
        return {
          ...tweet,
          quotedTweet
        };
      })
    }))
  };

  return { feedX: enrichedFeedX, enrichedCount };
}

async function enrichPodcastEpisodeLinks(feedPodcasts, errors = []) {
  if (!feedPodcasts?.podcasts || !Array.isArray(feedPodcasts.podcasts)) {
    return { feedPodcasts, enrichedCount: 0 };
  }

  const sources = await loadDefaultSources(errors);
  const sourceByName = new Map(
    (Array.isArray(sources?.podcasts) ? sources.podcasts : [])
      .map((source) => [normalizeComparableText(source.name), source])
  );
  const rssCache = new Map();
  let enrichedCount = 0;

  const podcasts = [];
  for (const episode of feedPodcasts.podcasts) {
    const source = sourceByName.get(normalizeComparableText(episode?.name));
    const showUrl = episode?.showUrl || episode?.show_url || source?.url || undefined;
    const originalUrl = normalizeUrl(episode?.url);

    if (!source?.rssUrl || !needsPodcastLinkRepair(episode, source)) {
      if (isConcretePodcastEpisodeUrl(originalUrl)) {
        podcasts.push({
          ...episode,
          ...(showUrl ? { showUrl } : {})
        });
      } else {
        errors.push(`Filtered podcast without concrete episode URL: ${episode?.name || 'podcast'} - ${episode?.title || 'untitled'}`);
      }
      continue;
    }

    try {
      if (!rssCache.has(source.rssUrl)) {
        const rssXml = await fetchPodcastRss(source.rssUrl);
        rssCache.set(source.rssUrl, parseRssFeed(rssXml));
      }

      const rssEpisodes = rssCache.get(source.rssUrl) || [];
      const episodeLink = findMatchingEpisodeLink(episode, rssEpisodes);
      if (isConcretePodcastEpisodeUrl(episodeLink)) {
        enrichedCount += 1;
        podcasts.push({
          ...episode,
          url: episodeLink,
          ...(showUrl ? { showUrl } : {})
        });
        continue;
      }
    } catch (error) {
      errors.push(`Could not enrich podcast link for ${episode?.name || 'podcast'}: ${error.message}`);
    }

    errors.push(`Filtered podcast without concrete episode URL: ${episode?.name || 'podcast'} - ${episode?.title || 'untitled'}`);
  }

  return {
    feedPodcasts: {
      ...feedPodcasts,
      podcasts
    },
    enrichedCount
  };
}

function resolveFeedGeneratedAt(feedX, feedPodcasts, feedBlogs) {
  return feedX?.generatedAt || feedPodcasts?.generatedAt || feedBlogs?.generatedAt || null;
}

function buildPreparedDigest({ config, feedX, feedPodcasts, feedBlogs, prompts, errors = [] }) {
  return {
    status: 'ok',
    generatedAt: new Date().toISOString(),
    config: {
      language: config.language || 'en',
      frequency: config.frequency || 'daily',
      delivery: config.delivery || { method: 'stdout' },
      timezone: config.timezone || 'UTC',
      deliveryTime: config.deliveryTime || '08:00',
      deliveryCheckHours: Array.isArray(config.deliveryCheckHours) ? config.deliveryCheckHours : undefined
    },
    podcasts: feedPodcasts?.podcasts || [],
    x: feedX?.x || [],
    blogs: feedBlogs?.blogs || [],
    stats: {
      podcastEpisodes: feedPodcasts?.podcasts?.length || 0,
      xBuilders: feedX?.x?.length || 0,
      totalTweets: (feedX?.x || []).reduce((sum, author) => sum + (author?.tweets?.length || 0), 0),
      blogPosts: feedBlogs?.blogs?.length || 0,
      feedGeneratedAt: resolveFeedGeneratedAt(feedX, feedPodcasts, feedBlogs),
      quotedTweetsEnriched: (feedX?.x || []).reduce((sum, author) => (
        sum + (author?.tweets || []).filter((tweet) => Boolean(tweet?.quotedTweet)).length
      ), 0)
    },
    prompts,
    errors: errors.length > 0 ? errors : undefined
  };
}

async function main() {
  const errors = [];
  const config = await loadConfig(CONFIG_PATH, errors);
  const [feedX, feedPodcasts, feedBlogs, prompts] = await Promise.all([
    fetchJSON(FEED_X_URL),
    fetchJSON(FEED_PODCASTS_URL),
    fetchJSON(FEED_BLOGS_URL),
    loadPrompts({
      promptFiles: PROMPT_FILES,
      userDir: USER_DIR,
      scriptDir: SCRIPT_DIR,
      promptsBase: PROMPTS_BASE,
      fetchText,
      errors
    })
  ]);

  if (!feedX) errors.push('Could not fetch tweet feed');
  if (!feedPodcasts) errors.push('Could not fetch podcast feed');
  if (!feedBlogs) errors.push('Could not fetch blog feed');

  const { feedX: enrichedFeedX } = feedX
    ? await enrichFeedXQuotes(feedX, errors)
    : { feedX };
  const { feedPodcasts: enrichedFeedPodcasts } = feedPodcasts
    ? await enrichPodcastEpisodeLinks(feedPodcasts, errors)
    : { feedPodcasts };

  const output = buildPreparedDigest({
    config,
    feedX: enrichedFeedX,
    feedPodcasts: enrichedFeedPodcasts,
    feedBlogs,
    prompts,
    errors
  });

  console.log(JSON.stringify(output, null, 2));
}

export {
  buildPreparedDigest,
  enrichFeedXQuotes,
  enrichPodcastEpisodeLinks,
  isConcretePodcastEpisodeUrl,
  loadConfig,
  loadPrompts
};

const IS_ENTRYPOINT = process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1];

if (IS_ENTRYPOINT) {
  main().catch((error) => {
    console.error(JSON.stringify({
      status: 'error',
      message: error.message
    }));
    process.exit(1);
  });
}
