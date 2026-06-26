#!/usr/bin/env node

// ============================================================================
// yt-dlp Helper Functions
// ============================================================================
// Wraps yt-dlp CLI for listing channel/playlist videos and fetching transcripts.
// All calls use child_process.execFile (no shell, no injection risk).
// ============================================================================

import { execFile as execFileCb } from 'child_process';
import { readFile, readdir, mkdir, rm } from 'fs/promises';
import { existsSync } from 'fs';
import { join } from 'path';
import { tmpdir } from 'os';

// Promisified execFile wrapper
function execFile(cmd, args, options = {}) {
  return new Promise((resolve, reject) => {
    execFileCb(cmd, args, options, (err, stdout, stderr) => {
      if (err) {
        err.stderr = stderr;
        reject(err);
      } else {
        resolve({ stdout, stderr });
      }
    });
  });
}

// ============================================================================
// yt-dlp Availability
// ============================================================================

export async function checkYtDlpAvailable() {
  try {
    const { stdout } = await execFile('yt-dlp', ['--version'], { timeout: 10000 });
    const version = stdout.trim();
    return { available: true, version };
  } catch (err) {
    return { available: false };
  }
}

// ============================================================================
// Cookies Support
// ============================================================================

// Get yt-dlp cookie args if YT_DLP_COOKIES is set in env
// Supports: "chrome", "firefox", "edge", or path to cookies.txt file
function getCookieArgs() {
  const cookieSource = process.env.YT_DLP_COOKIES;
  if (!cookieSource) return [];

  // If it's a browser name, use --cookies-from-browser
  const browsers = ['chrome', 'firefox', 'edge', 'brave', 'opera', 'vivaldi', 'safari'];
  if (browsers.includes(cookieSource.toLowerCase())) {
    return ['--cookies-from-browser', cookieSource.toLowerCase()];
  }

  // Otherwise treat as path to cookies file
  return ['--cookies', cookieSource];
}

// Get yt-dlp proxy args if HTTPS_PROXY or HTTP_PROXY is set
function getProxyArgs() {
  const proxy = process.env.FB_PROXY;
  if (!proxy) return [];
  return ['--proxy', proxy];
}

// ============================================================================
// List Channel/Playlist Videos
// ============================================================================

export async function listChannelVideos(podcast, lookbackHours, errors) {
  const url = podcast.url;
  const candidates = [];

  try {
    const args = [
      '--dump-json',
      '--skip-download',
      '--playlist-end', '5',
      '--no-warnings',
      '--quiet',
      ...getProxyArgs(),
      ...getCookieArgs()
    ];

    const { stdout } = await execFile('yt-dlp', args.concat(url), {
      maxBuffer: 20 * 1024 * 1024,
      timeout: 120000
    });

    // yt-dlp outputs one JSON object per line (NDJSON)
    const lines = stdout.trim().split('\n').filter(l => l.trim());

    for (const line of lines) {
      try {
        const video = JSON.parse(line);
        const uploadDate = video.upload_date || video.release_date || null;

        candidates.push({
          videoId: video.id,
          title: video.title || 'Untitled',
          publishedAt: uploadDate ? parseYtDlpDate(uploadDate) : null,
          rawDate: uploadDate
        });
      } catch {
        // Skip malformed lines
      }
    }
  } catch (err) {
    const msg = err.stderr || err.message || String(err);
    if (msg.includes('Sign in to confirm') || msg.includes('not a bot')) {
      errors.push(
        `YouTube: yt-dlp 被要求验证身份。请配置 cookies：\n` +
        `  在 data/.env 中添加 YT_DLP_COOKIES=chrome（或 firefox/edge）\n` +
        `  或指定 cookies 文件路径：YT_DLP_COOKIES=/path/to/cookies.txt`
      );
    } else {
      errors.push(`YouTube: Failed to list videos for ${podcast.name}: ${msg}`);
    }
  }

  return candidates;
}

// ============================================================================
// Fetch Transcript
// ============================================================================

export async function fetchTranscript(videoId, errors) {
  const tempDir = join(tmpdir(), `follow-builders-subs-${videoId}-${Date.now()}`);
  const videoUrl = `https://www.youtube.com/watch?v=${videoId}`;

  try {
    await mkdir(tempDir, { recursive: true });

    const args = [
      '--write-subs',
      '--write-auto-subs',
      '--skip-download',
      '--sub-lang', 'en',
      '--output', join(tempDir, 'subs'),
      ...getProxyArgs(),
      ...getCookieArgs(),
      videoUrl
    ];

    await execFile('yt-dlp', args, {
      timeout: 60000,
      maxBuffer: 5 * 1024 * 1024
    });

    // Find the VTT file
    const files = await readdir(tempDir);
    const vttFile = files.find(f => f.endsWith('.vtt'));

    if (!vttFile) {
      errors.push(`YouTube: No subtitles found for video ${videoId}`);
      return '';
    }

    const vttContent = await readFile(join(tempDir, vttFile), 'utf-8');
    return cleanVtt(vttContent);
  } catch (err) {
    const msg = err.stderr || err.message || String(err);
    errors.push(`YouTube: Failed to get transcript for ${videoId}: ${msg}`);
    return '';
  } finally {
    // Clean up temp directory
    try {
      if (existsSync(tempDir)) {
        await rm(tempDir, { recursive: true, force: true });
      }
    } catch {
      // Ignore cleanup errors
    }
  }
}

// ============================================================================
// VTT Parser
// ============================================================================

function cleanVtt(content) {
  const lines = content.split('\n');
  const textLines = [];

  const timestampPattern = /^\d{2}:\d{2}:\d{2}\.\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}\.\d{3}/;
  const shortTimestampPattern = /^\d{2}:\d{2}\.\d{3}\s*-->\s*\d{2}:\d{2}\.\d{3}/;

  for (const rawLine of lines) {
    const line = rawLine.trim();

    if (!line) continue;
    if (line === 'WEBVTT') continue;
    if (/^\d+$/.test(line)) continue; // cue identifiers
    if (timestampPattern.test(line) || shortTimestampPattern.test(line)) continue;
    if (line.startsWith('NOTE') || line.startsWith('STYLE')) continue;

    // Strip HTML tags
    const clean = line.replace(/<[^>]+>/g, '');

    // Skip consecutive duplicates
    if (textLines.length > 0 && textLines[textLines.length - 1] === clean) continue;

    textLines.push(clean);
  }

  return textLines.join('\n');
}

// ============================================================================
// Utilities
// ============================================================================

function parseYtDlpDate(dateStr) {
  // yt-dlp returns upload_date as "YYYYMMDD"
  if (!dateStr || dateStr.length !== 8) return null;
  const year = parseInt(dateStr.slice(0, 4), 10);
  const month = parseInt(dateStr.slice(4, 6), 10) - 1;
  const day = parseInt(dateStr.slice(6, 8), 10);
  return new Date(Date.UTC(year, month, day)).toISOString();
}
