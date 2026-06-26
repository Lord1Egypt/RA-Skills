#!/usr/bin/env node

// ============================================================================
// Follow GitHub — Prepare Digest
// ============================================================================
// Gathers everything the LLM needs to produce a GitHub digest:
// - Fetches events from users the reader follows (GitHub API)
// - Scrapes github.com/trending for trending repos
// - Fetches recently-created popular repos via GitHub Search API
// - Loads prompts with 3-tier priority (user > remote > local)
// - Deduplicates against ~/.follow-github/state.json
// - Outputs a single JSON blob to stdout
//
// Usage: node prepare-digest.js
// Output: JSON to stdout
// ============================================================================

import { readFile, writeFile, mkdir } from 'fs/promises';
import { existsSync } from 'fs';
import { join } from 'path';
import { homedir } from 'os';
import { config as loadEnv } from 'dotenv';
import * as cheerio from 'cheerio';

const USER_DIR = join(homedir(), '.follow-github');
const CONFIG_PATH = join(USER_DIR, 'config.json');
const ENV_PATH = join(USER_DIR, '.env');
const STATE_PATH = join(USER_DIR, 'state.json');

const GH_API = 'https://api.github.com';
const TRENDING_URL = 'https://github.com/trending';

const PROMPT_FILES = [
  'digest-intro.md',
  'summarize-following.md',
  'summarize-trending.md',
  'summarize-hot.md',
  'translate.md'
];

const RELEVANT_EVENT_TYPES = new Set([
  'WatchEvent',      // starred
  'CreateEvent',     // created (only ref_type=repository — filtered below)
  'PublicEvent',     // open-sourced
  'ReleaseEvent'     // published release
]);

// -- State (dedup) -----------------------------------------------------------

async function loadState() {
  if (!existsSync(STATE_PATH)) {
    return { seenEvents: {}, seenHotRepos: {} };
  }
  try {
    return JSON.parse(await readFile(STATE_PATH, 'utf-8'));
  } catch {
    return { seenEvents: {}, seenHotRepos: {} };
  }
}

async function saveState(state) {
  // Prune entries older than 30 days
  const cutoff = Date.now() - 30 * 24 * 60 * 60 * 1000;
  for (const [id, ts] of Object.entries(state.seenEvents)) {
    if (ts < cutoff) delete state.seenEvents[id];
  }
  for (const [id, ts] of Object.entries(state.seenHotRepos)) {
    if (ts < cutoff) delete state.seenHotRepos[id];
  }
  if (!existsSync(USER_DIR)) await mkdir(USER_DIR, { recursive: true });
  await writeFile(STATE_PATH, JSON.stringify(state, null, 2));
}

// -- Config ------------------------------------------------------------------

async function loadConfig() {
  const defaults = {
    github: { username: null },
    sources: { following: true, trending: true, hot: true },
    languages: [],
    frequency: 'weekly',
    digestLanguage: 'en',
    delivery: { method: 'stdout' },
    prompts: { remoteUrl: null }
  };
  if (!existsSync(CONFIG_PATH)) return defaults;
  try {
    return { ...defaults, ...JSON.parse(await readFile(CONFIG_PATH, 'utf-8')) };
  } catch {
    return defaults;
  }
}

// -- GitHub API helpers ------------------------------------------------------

function ghHeaders(token) {
  const h = {
    'Accept': 'application/vnd.github+json',
    'X-GitHub-Api-Version': '2022-11-28',
    'User-Agent': 'follow-github-skill'
  };
  if (token) h['Authorization'] = `Bearer ${token}`;
  return h;
}

async function ghGet(url, token) {
  const res = await fetch(url, { headers: ghHeaders(token) });
  if (!res.ok) {
    const body = await res.text().catch(() => '');
    throw new Error(`GitHub ${res.status}: ${body.slice(0, 200)}`);
  }
  return res.json();
}

// -- Following activity ------------------------------------------------------

async function fetchFollowingActivity(username, token, state, lookbackHours, errors) {
  if (!username) {
    errors.push('following: no github.username in config');
    return [];
  }

  let events = [];
  try {
    // received_events returns the public event feed for users this user follows
    events = await ghGet(
      `${GH_API}/users/${username}/received_events/public?per_page=100`,
      token
    );
  } catch (err) {
    errors.push(`following: ${err.message}`);
    return [];
  }

  const cutoff = Date.now() - lookbackHours * 60 * 60 * 1000;

  const relevant = events.filter(e => {
    if (!RELEVANT_EVENT_TYPES.has(e.type)) return false;
    if (new Date(e.created_at).getTime() < cutoff) return false;
    if (state.seenEvents[e.id]) return false;
    // CreateEvent: only new repos, not branches/tags
    if (e.type === 'CreateEvent' && e.payload?.ref_type !== 'repository') return false;
    return true;
  });

  // Collect unique repo full_names, fetch details once each
  const uniqueRepos = [...new Set(relevant.map(e => e.repo?.name).filter(Boolean))];
  const repoDetails = {};
  await Promise.all(uniqueRepos.slice(0, 30).map(async (fullName) => {
    try {
      const info = await ghGet(`${GH_API}/repos/${fullName}`, token);
      repoDetails[fullName] = {
        description: info.description || '',
        language: info.language || '',
        stars: info.stargazers_count || 0,
        fork: info.fork || false
      };
    } catch {
      // If repo fetch fails (deleted, private, etc), skip enrichment
    }
  }));

  // Build event records
  const results = [];
  for (const e of relevant) {
    const repoName = e.repo?.name;
    const detail = repoDetails[repoName] || {};

    // Skip forks for CreateEvent (usually noise)
    if (e.type === 'CreateEvent' && detail.fork) continue;

    const record = {
      id: e.id,
      type: e.type,
      actor: e.actor?.login,
      repo: repoName,
      url: repoName ? `https://github.com/${repoName}` : null,
      repo_desc: detail.description || '',
      repo_language: detail.language || '',
      repo_stars: detail.stars || 0,
      createdAt: e.created_at
    };

    if (e.type === 'ReleaseEvent') {
      const rel = e.payload?.release || {};
      record.release_tag = rel.tag_name || '';
      record.release_name = rel.name || '';
      record.release_body = (rel.body || '').slice(0, 500);
      record.url = rel.html_url || record.url;
    }

    results.push(record);
    state.seenEvents[e.id] = Date.now();
  }

  return results;
}

// -- Trending scraper --------------------------------------------------------

async function fetchTrending(languages, frequency, errors) {
  const since = frequency === 'daily' ? 'daily' : 'weekly';
  const queries = languages.length > 0
    ? languages.map(lang => ({ lang, url: `${TRENDING_URL}/${lang}?since=${since}` }))
    : [{ lang: '', url: `${TRENDING_URL}?since=${since}` }];

  const allResults = [];

  await Promise.all(queries.map(async ({ lang, url }) => {
    try {
      const res = await fetch(url, {
        headers: { 'User-Agent': 'follow-github-skill' }
      });
      if (!res.ok) {
        errors.push(`trending (${lang || 'all'}): HTTP ${res.status}`);
        return;
      }
      const html = await res.text();
      const $ = cheerio.load(html);

      $('article.Box-row').each((_, el) => {
        const $el = $(el);
        const href = $el.find('h2 a').attr('href') || '';
        const fullName = href.replace(/^\//, '').trim();
        if (!fullName) return;

        const description = $el.find('p').text().trim();
        const language = $el.find('[itemprop=programmingLanguage]').text().trim();
        const totalStarsText = $el.find('a[href$="/stargazers"]').first().text().trim();
        const periodText = $el.find('span.d-inline-block.float-sm-right').text().trim();

        allResults.push({
          full_name: fullName,
          url: `https://github.com${href}`,
          description,
          language,
          stars: parseIntLoose(totalStarsText),
          stars_period: parseIntLoose(periodText),
          period: since,
          query_language: lang || null
        });
      });
    } catch (err) {
      errors.push(`trending (${lang || 'all'}): ${err.message}`);
    }
  }));

  // Cap at 20 total
  return allResults.slice(0, 20);
}

function parseIntLoose(s) {
  if (!s) return 0;
  const m = s.replace(/[^0-9.]/g, '');
  return parseInt(m || '0', 10) || 0;
}

// -- Hot new projects --------------------------------------------------------

async function fetchHotProjects(frequency, languages, token, state, errors) {
  const daysBack = frequency === 'daily' ? 3 : 14;
  const minStars = frequency === 'daily' ? 30 : 100;
  const since = new Date(Date.now() - daysBack * 24 * 60 * 60 * 1000)
    .toISOString().slice(0, 10);

  const langFilters = languages.length > 0
    ? languages.map(l => ` language:${l}`).join('')
    : '';
  const q = `created:>${since} stars:>${minStars}${langFilters}`;

  try {
    const data = await ghGet(
      `${GH_API}/search/repositories?q=${encodeURIComponent(q)}&sort=stars&order=desc&per_page=15`,
      token
    );
    const items = (data.items || []).filter(r => !state.seenHotRepos[r.full_name]);

    const results = items.slice(0, 10).map(r => {
      state.seenHotRepos[r.full_name] = Date.now();
      return {
        full_name: r.full_name,
        url: r.html_url,
        description: r.description || '',
        language: r.language || '',
        stars: r.stargazers_count,
        created_at: r.created_at
      };
    });
    return results;
  } catch (err) {
    errors.push(`hot: ${err.message}`);
    return [];
  }
}

// -- Prompt loading (3-tier: user > remote > local) --------------------------

async function loadPrompts(remoteUrl, errors) {
  const scriptDir = decodeURIComponent(new URL('.', import.meta.url).pathname);
  const localPromptsDir = join(scriptDir, '..', 'prompts');
  const userPromptsDir = join(USER_DIR, 'prompts');

  const prompts = {};
  for (const filename of PROMPT_FILES) {
    const key = filename.replace('.md', '').replace(/-/g, '_');
    const userPath = join(userPromptsDir, filename);
    const localPath = join(localPromptsDir, filename);

    // Priority 1: user custom
    if (existsSync(userPath)) {
      prompts[key] = await readFile(userPath, 'utf-8');
      continue;
    }

    // Priority 2: remote (only if remoteUrl configured)
    if (remoteUrl) {
      try {
        const res = await fetch(`${remoteUrl}/${filename}`);
        if (res.ok) {
          prompts[key] = await res.text();
          continue;
        }
      } catch { /* fall through to local */ }
    }

    // Priority 3: local shipped
    if (existsSync(localPath)) {
      prompts[key] = await readFile(localPath, 'utf-8');
    } else {
      errors.push(`prompt missing: ${filename}`);
    }
  }
  return prompts;
}

// -- Main --------------------------------------------------------------------

async function main() {
  loadEnv({ path: ENV_PATH });

  const errors = [];
  const config = await loadConfig();
  const state = await loadState();
  const token = process.env.GITHUB_TOKEN || null;

  const username = config.github?.username;
  const sources = config.sources || {};
  const languages = config.languages || [];
  const frequency = config.frequency || 'weekly';
  const lookbackHours = frequency === 'daily' ? 24 : 24 * 7;

  // Parallel fetches
  const [following, trending, hot] = await Promise.all([
    sources.following !== false
      ? fetchFollowingActivity(username, token, state, lookbackHours, errors)
      : Promise.resolve([]),
    sources.trending !== false
      ? fetchTrending(languages, frequency, errors)
      : Promise.resolve([]),
    sources.hot !== false
      ? fetchHotProjects(frequency, languages, token, state, errors)
      : Promise.resolve([])
  ]);

  const prompts = await loadPrompts(config.prompts?.remoteUrl, errors);

  await saveState(state);

  const output = {
    status: 'ok',
    generatedAt: new Date().toISOString(),
    config: {
      digestLanguage: config.digestLanguage || 'en',
      frequency,
      languages,
      delivery: config.delivery || { method: 'stdout' }
    },
    following,
    trending,
    hot,
    stats: {
      followingEvents: following.length,
      trendingRepos: trending.length,
      hotRepos: hot.length,
      lookbackHours
    },
    prompts,
    errors: errors.length > 0 ? errors : undefined
  };

  console.log(JSON.stringify(output, null, 2));
}

main().catch(err => {
  console.error(JSON.stringify({ status: 'error', message: err.message }));
  process.exit(1);
});
