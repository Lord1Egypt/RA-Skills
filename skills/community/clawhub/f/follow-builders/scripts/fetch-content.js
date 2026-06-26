#!/usr/bin/env node

// ============================================================================
// Follow Builders — Content Fetcher
// ============================================================================
// This script fetches new content from YouTube podcasts (via Supadata API) and
// X/Twitter accounts (via Rettiwt-API). It tracks what's already been processed in a
// state file so you never get duplicate content in your digest.
//
// Usage: node fetch-content.js [--lookback-hours 24]
// Output: JSON to stdout with all new content, organized by source
// ============================================================================

import { readFile, writeFile, mkdir } from 'fs/promises';
import { existsSync } from 'fs';
import { join } from 'path';
import { homedir } from 'os';
import { config as loadEnv } from 'dotenv';
import lockfile from 'proper-lockfile';

// -- Constants ---------------------------------------------------------------

// Where user config and state live
const USER_DIR = join(homedir(), '.follow-builders');
const CONFIG_PATH = join(USER_DIR, 'config.json');
const STATE_PATH = join(USER_DIR, 'state.json');
const ENV_PATH = join(USER_DIR, '.env');

// How far back to look for new content (overridable via --lookback-hours flag)
const DEFAULT_LOOKBACK_HOURS = 24;

// How many days of state to keep before pruning old entries
const STATE_RETENTION_DAYS = 90;

// Supadata API base URL
const SUPADATA_BASE = 'https://api.supadata.ai/v1';

// URL to fetch the latest default sources from GitHub
// This ensures users always get the most up-to-date builder list
// without needing to git pull or reinstall the skill
const REMOTE_SOURCES_URL = 'https://raw.githubusercontent.com/zarazhangrui/follow-builders/main/config/default-sources.json';

// -- Config Loading ----------------------------------------------------------

// Loads the user's config.json and merges it with default sources.
// The merge logic: start with all defaults, then add user additions and
// remove user removals. This way users can customize without losing defaults.
//
// Default sources are fetched from GitHub so users automatically get
// the latest curated list. Falls back to the local file if offline.
async function loadConfig() {
  // Try to fetch the latest default sources from GitHub
  // If that fails (offline, rate-limited, etc.), fall back to the local copy
  let defaultSources;
  try {
    const res = await fetch(REMOTE_SOURCES_URL);
    if (res.ok) {
      defaultSources = await res.json();
      // Loaded latest sources from GitHub — no need to log this
    } else {
      throw new Error(`GitHub returned ${res.status}`);
    }
  } catch (err) {
    // Could not fetch remote sources, using local copy — not a problem
    const scriptDir = decodeURIComponent(new URL('.', import.meta.url).pathname);
    const defaultSourcesPath = join(scriptDir, '..', 'config', 'default-sources.json');
    defaultSources = JSON.parse(await readFile(defaultSourcesPath, 'utf-8'));
  }

  // Load user config (may not exist yet on first run)
  let userConfig = {};
  if (existsSync(CONFIG_PATH)) {
    userConfig = JSON.parse(await readFile(CONFIG_PATH, 'utf-8'));
  }

  // Merge sources: defaults + user additions - user removals
  const sources = userConfig.sources || {};
  const podcasts = [
    ...defaultSources.podcasts.filter(
      p => !(sources.removedPodcasts || []).includes(p.name)
    ),
    ...(sources.addedPodcasts || [])
  ];
  const xAccounts = [
    ...defaultSources.x_accounts.filter(
      a => !(sources.removedXAccounts || []).includes(a.handle)
    ),
    ...(sources.addedXAccounts || [])
  ];

  return {
    language: userConfig.language || 'en',
    timezone: userConfig.timezone || 'America/Los_Angeles',
    frequency: userConfig.frequency || 'daily',
    podcasts,
    xAccounts
  };
}

// -- State Management --------------------------------------------------------

// The state file tracks which videos and tweets we've already processed.
// It uses file locking to prevent corruption if two runs overlap
// (e.g., a manual /ai trigger while a cron job is running).

async function loadState() {
  if (!existsSync(STATE_PATH)) {
    return { processedVideos: {}, processedTweets: {}, lastUpdated: null };
  }
  return JSON.parse(await readFile(STATE_PATH, 'utf-8'));
}

async function saveState(state) {
  // Prune entries older than 90 days to prevent the file from growing forever
  const cutoff = Date.now() - (STATE_RETENTION_DAYS * 24 * 60 * 60 * 1000);

  for (const [id, timestamp] of Object.entries(state.processedVideos)) {
    if (timestamp < cutoff) delete state.processedVideos[id];
  }
  for (const [id, timestamp] of Object.entries(state.processedTweets)) {
    if (timestamp < cutoff) delete state.processedTweets[id];
  }

  state.lastUpdated = Date.now();
  await writeFile(STATE_PATH, JSON.stringify(state, null, 2));
}

// -- YouTube Fetching (Supadata API) -----------------------------------------

// Fetches recent videos from a YouTube channel or playlist, then grabs
// transcripts for any we haven't seen before. Supadata charges 1 credit
// per transcript, so we only fetch what's new.
//
// Supadata API endpoints:
//   GET /v1/youtube/channel/videos?id=<handle>&type=video — returns { video_ids: [] }
//   GET /v1/youtube/playlist/videos?id=<playlistId>       — returns { video_ids: [] }
//   GET /v1/youtube/transcript?url=<full youtube URL>&text=true — returns { content, lang, availableLangs }
//   GET /v1/youtube/video?id=<videoId>                     — returns video metadata (title, etc.)

async function fetchYouTubeContent(podcasts, state, apiKey, isFirstRun, errors, lookbackHours) {
  const results = [];
  const videoCutoff = new Date(Date.now() - lookbackHours * 60 * 60 * 1000);

  // Phase 1: Collect the most recent unprocessed video from each channel
  // We get metadata (title, date) but NOT transcripts yet — transcripts are expensive
  const allCandidates = [];

  for (const podcast of podcasts) {
    try {
      let videosUrl;
      if (podcast.type === 'youtube_playlist') {
        videosUrl = `${SUPADATA_BASE}/youtube/playlist/videos?id=${podcast.playlistId}`;
      } else {
        videosUrl = `${SUPADATA_BASE}/youtube/channel/videos?id=${podcast.channelHandle}&type=video`;
      }

      const videosRes = await fetch(videosUrl, {
        headers: { 'x-api-key': apiKey }
      });

      if (!videosRes.ok) {
        errors.push(`Failed to fetch videos for ${podcast.name}: HTTP ${videosRes.status}`);
        continue;
      }

      const videosData = await videosRes.json();
      const videoIds = videosData.videoIds || videosData.video_ids || [];
      const newVideoIds = videoIds.filter(id => !state.processedVideos[id]);

      if (newVideoIds.length === 0) continue;

      // Only check the first 3 videos per channel for metadata
      for (const videoId of newVideoIds.slice(0, 3)) {
        try {
          const metaRes = await fetch(
            `${SUPADATA_BASE}/youtube/video?id=${videoId}`,
            { headers: { 'x-api-key': apiKey } }
          );
          let title = 'Untitled';
          let publishedAt = null;
          if (metaRes.ok) {
            const metaData = await metaRes.json();
            title = metaData.title || 'Untitled';
            publishedAt = metaData.uploadDate || metaData.publishedAt || metaData.date || null;
          }
          allCandidates.push({ podcast, videoId, title, publishedAt });
          await new Promise(r => setTimeout(r, 300));
        } catch (err) {
          errors.push(`Error fetching metadata for video ${videoId}: ${err.message}`);
        }
      }
    } catch (err) {
      errors.push(`Error processing podcast ${podcast.name}: ${err.message}`);
    }
  }

  // Phase 2: Select which videos to fetch transcripts for
  let selectedVideos;

  if (isFirstRun) {
    // FIRST RUN: Return candidate list with titles (no transcripts) so the
    // agent can pick the most AI-relevant one. Saves tokens by not fetching
    // transcripts for all 5+ videos.
    const sorted = allCandidates
      .filter(v => v.publishedAt)
      .sort((a, b) => new Date(b.publishedAt) - new Date(a.publishedAt));

    // Store candidates on the results array as a special property
    // The main output will include these as "firstRunCandidates"
    results.firstRunCandidates = sorted.map(v => ({
      name: v.podcast.name,
      title: v.title,
      videoId: v.videoId,
      url: `https://youtube.com/watch?v=${v.videoId}`,
      publishedAt: v.publishedAt
    }));

    selectedVideos = [];
  } else {
    // REGULAR RUN: include all videos within the lookback window, up to 3 per channel
    const byChannel = {};
    selectedVideos = [];
    for (const v of allCandidates) {
      // Skip videos older than the lookback window
      if (v.publishedAt && new Date(v.publishedAt) < videoCutoff) continue;
      // Cap at 3 per channel
      const key = v.podcast.name;
      byChannel[key] = (byChannel[key] || 0) + 1;
      if (byChannel[key] > 3) continue;
      selectedVideos.push(v);
    }
  }

  // Phase 3: Fetch transcripts only for selected videos
  for (const video of selectedVideos) {
    try {
      const videoUrl = `https://www.youtube.com/watch?v=${video.videoId}`;
      const transcriptRes = await fetch(
        `${SUPADATA_BASE}/youtube/transcript?url=${encodeURIComponent(videoUrl)}&text=true`,
        { headers: { 'x-api-key': apiKey } }
      );

      if (!transcriptRes.ok) {
        errors.push(`Failed to fetch transcript for video ${video.videoId}: HTTP ${transcriptRes.status}`);
        continue;
      }

      const transcriptData = await transcriptRes.json();

      results.push({
        source: 'podcast',
        name: video.podcast.name,
        title: video.title,
        videoId: video.videoId,
        url: `https://youtube.com/watch?v=${video.videoId}`,
        publishedAt: video.publishedAt,
        transcript: transcriptData.content || '',
        language: transcriptData.lang || 'en'
      });

      state.processedVideos[video.videoId] = Date.now();
      await new Promise(r => setTimeout(r, 500));
    } catch (err) {
      errors.push(`Error fetching transcript for video ${video.videoId}: ${err.message}`);
    }
  }

  // Mark all checked candidates as processed so we don't re-check them
  for (const v of allCandidates) {
    if (!state.processedVideos[v.videoId]) {
      state.processedVideos[v.videoId] = Date.now();
    }
  }

  return results;
}

// -- X/Twitter ---------------------------------------------------------------
// X/Twitter content is NOT fetched by this script.
// Instead, the agent uses its own web search tools to find recent tweets.
// This avoids all X API/scraping issues: no login, no API key, no account risk.
// The script just passes the list of X accounts to the agent in the output.

// -- Main --------------------------------------------------------------------

async function main() {
  // Parse command-line args
  const args = process.argv.slice(2);
  const lookbackIdx = args.indexOf('--lookback-hours');
  const lookbackHours = lookbackIdx !== -1
    ? parseInt(args[lookbackIdx + 1], 10)
    : DEFAULT_LOOKBACK_HOURS;

  // --video-id flag: fetch a single transcript and output it
  // Used by the agent after picking the most AI-relevant video from firstRunCandidates
  const videoIdIdx = args.indexOf('--video-id');
  if (videoIdIdx !== -1 && args[videoIdIdx + 1]) {
    // Load env for the API key
    if (!existsSync(USER_DIR)) await mkdir(USER_DIR, { recursive: true });
    loadEnv({ path: ENV_PATH });
    const apiKey = process.env.SUPADATA_API_KEY;
    if (!apiKey) {
      console.log(JSON.stringify({ error: 'SUPADATA_API_KEY not found' }));
      process.exit(1);
    }
    const videoId = args[videoIdIdx + 1];
    try {
      const videoUrl = `https://www.youtube.com/watch?v=${videoId}`;
      const res = await fetch(
        `${SUPADATA_BASE}/youtube/transcript?url=${encodeURIComponent(videoUrl)}&text=true`,
        { headers: { 'x-api-key': apiKey } }
      );
      if (!res.ok) {
        console.log(JSON.stringify({ error: `HTTP ${res.status}` }));
        process.exit(1);
      }
      const data = await res.json();
      console.log(JSON.stringify({ status: 'ok', videoId, transcript: data.content || '' }));
    } catch (err) {
      console.log(JSON.stringify({ error: err.message }));
      process.exit(1);
    }
    return;
  }

  // Ensure user directory exists
  if (!existsSync(USER_DIR)) {
    await mkdir(USER_DIR, { recursive: true });
  }

  // Load environment variables from user's .env file
  loadEnv({ path: ENV_PATH });

  const supadataKey = process.env.SUPADATA_API_KEY;

  if (!supadataKey) {
    console.error(JSON.stringify({
      error: 'SUPADATA_API_KEY not found',
      message: 'Please add your Supadata API key to ~/.follow-builders/.env'
    }));
    process.exit(1);
  }

  // Load config and state
  const config = await loadConfig();

  // Acquire lock on state file to prevent concurrent corruption
  let releaseLock;
  try {
    // Create state file if it doesn't exist (lockfile needs the file to exist)
    if (!existsSync(STATE_PATH)) {
      await writeFile(STATE_PATH, JSON.stringify({
        processedVideos: {},
        processedTweets: {},
        lastUpdated: null
      }, null, 2));
    }
    // stale: 300000 (5 min) — default 10s is too short, API calls take longer
    // update: 60000 (1 min) — how often the lock refreshes itself
    releaseLock = await lockfile.lock(STATE_PATH, { retries: 3, stale: 300000, update: 60000 });
  } catch (err) {
    console.error(JSON.stringify({
      error: 'STATE_LOCKED',
      message: 'Another fetch is already running. Try again in a few minutes.'
    }));
    process.exit(1);
  }

  try {
    const state = await loadState();

    // Detect first run (welcome digest) — if we've never processed anything
    const isFirstRun = !state.lastUpdated;

    // Collect all errors in an array so they appear in the JSON output
    // instead of stderr — this makes the output much easier for any model
    // to parse, since they only need to read one clean JSON blob
    const errors = [];

    // Fetch YouTube podcast content
    const podcastContent = await fetchYouTubeContent(
      config.podcasts, state, supadataKey, isFirstRun, errors, lookbackHours
    );

    // Save updated state (with new processed IDs)
    await saveState(state);

    // Output results as JSON to stdout
    // - Podcast content is fully fetched (transcripts included)
    // - X/Twitter accounts are listed but NOT fetched — the agent handles
    //   X content itself using web search (no login, no API, no account risk)
    const output = {
      status: 'ok',
      fetchedAt: new Date().toISOString(),
      lookbackHours,
      isFirstRun,
      podcasts: podcastContent,
      // On first run: list of candidate videos with titles (no transcripts)
      // so the agent can pick the most AI-relevant one to fetch
      firstRunCandidates: podcastContent.firstRunCandidates || undefined,
      // List of X accounts for the agent to search — NOT pre-fetched
      xAccountsToSearch: config.xAccounts,
      stats: {
        newPodcastEpisodes: podcastContent.length,
        xAccountCount: config.xAccounts.length
      },
      // Any errors that occurred during fetching — these are non-fatal,
      // the digest should still be generated from whatever content was fetched
      errors: errors.length > 0 ? errors : undefined
    };

    console.log(JSON.stringify(output, null, 2));
  } finally {
    // Always release the lock, even if something went wrong
    if (releaseLock) await releaseLock();
  }
}

main().catch(err => {
  console.error(JSON.stringify({
    error: 'FETCH_FAILED',
    message: err.message
  }));
  process.exit(1);
});
