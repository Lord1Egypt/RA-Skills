#!/usr/bin/env node
'use strict';

/**
 * clip — Extract media from social media URLs
 * Uses yt-dlp to download images, videos, and GIFs from 1000+ sites
 * Handles large files via cloud storage fallback
 */

const { execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// ── Config ────────────────────────────────────────────────────────────────────

const MAX_DIRECT_SEND = 50 * 1024 * 1024; // 50MB — Telegram bot API limit

// ── Args ──────────────────────────────────────────────────────────────────────

const args = process.argv.slice(2);
const url = args.find(a => !a.startsWith('--'));
const outputDir = args.find(a => a.startsWith('--output-dir='))?.split('=')[1] || '/tmp/media-share';
const showTitle = args.includes('--title');
const showInfo = args.includes('--info');
const listSites = args.includes('--list-sites');
const listTypes = args.includes('--list-types') && url;
const testMode = args.includes('--test');
const uploadToCloud = args.includes('--upload');
const noUpload = args.includes('--no-upload');
const confirmUpload = args.includes('--confirm-upload');
const cloudProvider = args.find(a => a.startsWith('--cloud='))?.split('=')[1] || null;
const directSend = !args.includes('--no-direct-send');

if (!url && !listSites && !listTypes) {
  console.error('Usage: extract.js <url> [--output-dir <dir>] [--title] [--info] [--test]');
  console.error('       extract.js --list-sites');
  console.error('       extract.js --list-types <url>');
  process.exit(1);
}

if (listSites) {
  try {
    const output = execFileSync('yt-dlp', ['--list-extractors'], { encoding: 'utf8' });
    const sites = output.trim().split('\n').filter(s => s.trim());
    const total = sites.length;

    // Known platform categories for organized display
    const categories = {
      '🎬 Video Platforms': [
        'youtube', 'tiktok', 'twitch', 'vimeo', 'dailymotion', 'facebook',
        'instagram', 'twitter', 'reddit', 'rumble', 'odysee', 'lbry',
        'peertube', 'bilibili', 'niconico', 'dlive', 'kick', 'trovo',
        'caffeine', 'mixch', 'showroom', 'openrec', 'chaturbate', 'cam4',
        'camsoda', 'bongacams', 'fux', 'stripchat', 'teevio', 'goodgame',
        'livestream', 'youtube', 'tiktok', 'twitch', 'vimeo', 'dailymotion',
        'facebook', 'instagram', 'twitter', 'reddit', 'rumble', 'odysee',
        'peertube', 'bilibili', 'niconico', 'dlive', 'kick', 'trovo',
        'caffeine', 'mixch', 'showroom', 'openrec', 'chaturbate', 'cam4',
        'camsoda', 'bongacams', 'fux', 'stripchat', 'teevio', 'goodgame',
        'livestream'
      ],
      '📸 Photo & Image': [
        'imgur', 'pinterest', 'flickr', 'tumblr', '9gag', 'deviantart',
        'unsplash', 'pexels', 'pixabay', 'giphy', 'redgifs', 'scrolller',
        'instagram', 'twitter', 'reddit', 'tumblr', 'imgur', 'pinterest',
        'flickr', 'deviantart', 'unsplash', 'pexels', 'pixabay', 'giphy',
        'redgifs', 'scrolller'
      ],
      '🎵 Music & Audio': [
        'soundcloud', 'spotify', 'bandcamp', 'soundgasm', 'vocaroo', 'audius',
        'audiomack', 'mixcloud', 'jamendo', 'idagio', 'qqmusic', 'jiosaavn',
        'zingmp3', 'yandexmusic', 'lastfm', 'soundcloud', 'bandcamp',
        'soundgasm', 'vocaroo', 'audius', 'audiomack', 'mixcloud', 'jamendo',
        'idagio', 'qqmusic', 'jiosaavn', 'zingmp3', 'yandexmusic'
      ],
      '💬 Social Media': [
        'facebook', 'instagram', 'twitter', 'reddit', 'tumblr', 'linkedin',
        'tiktok', 'bluesky', 'mastodon', 'gab', 'gettr', 'parler',
        'truthsocial', 'weibo', 'telegram', 'facebook', 'instagram',
        'twitter', 'reddit', 'tumblr', 'linkedin', 'tiktok', 'bluesky',
        'mastodon', 'gab', 'gettr', 'parler', 'truthsocial', 'weibo',
        'telegram'
      ],
      '📺 Streaming & VOD': [
        'netflix', 'hulu', 'hbomax', 'disney', 'amazon', 'appletv',
        'paramount', 'peacock', 'crunchyroll', 'hidive', 'funimation',
        'crave', 'pluto', 'tubi', 'crackle', 'freevee', 'rakuten',
        'mbc', 'sbs', 'tving', 'wavve', 'tver', 'niconico', 'abematv',
        'dmm', 'globo', 'globoplay', 'canalplus', 'canal13', 'caracol',
        'rti', 'telefe', 'eltrece'
      ],
      '📰 News & Broadcasting': [
        'cnn', 'bbc', 'aljazeera', 'rt', 'cgtn', 'nhk', 'arte', 'dw',
        'francetv', 'raiprime', 'rtve', 'nrk', 'svt', 'yle', 'cbcgem',
        'itv', 'skynews', 'foxnews', 'cbsnews', 'nbcnews', 'espn',
        'nbcsports', 'foxsports', 'discoveryplus', 'history', 'natgeo',
        'sciencechannel'
      ],
      '🎓 Education': [
        'khanacademy', 'coursera', 'udemy', 'frontendmasters', 'pluralsight',
        'lynda', 'linkedinlearning', 'egghead', 'laracasts', 'skillshare',
        'edx', 'safari', 'teachable', 'mitocw', 'ted', 'bigthink',
        'digitalconcerthall'
      ],
      '🎙️ Podcasts': [
        'applemusic', 'applepodcasts', 'spotify', 'googlepodcasts', 'stitcher',
        'simplecast', 'art19', 'megaphone', 'podomatic', 'podbay', 'podchaser',
        'radiofrance', 'npr', 'bbcradio', 'iheartradio', 'tunein', 'radiko',
        'polskieradio'
      ],
      '🌍 Regional': [
        'bilibili', 'douyin', 'xiaohongshu', 'kuaishou', 'youku', 'iqiyi',
        'tencentvideo', 'sohu', 'tudou', 'niconico', 'abematv', 'tver',
        'dmm', 'giao', 'mangotv', 'iqcom', 'viu', 'viki', 'ondemandkorea',
        'trueid', 'zee5', 'sonyliv', 'jiosaavn', 'hungama', 'tarangplus',
        'mxplayer', 'arirang', 'sbs', 'tving', 'wavve', 'chzzk', 'naver',
        'nrk', 'dr', 'svt', 'yle', 'tv2', 'prosieben', 'rtl', 'zdf',
        'arte', 'francetv', 'tf1', 'rai', 'mediaset', 'rtp', 'globo',
        'canalplus', 'canal13', 'caracol', 'rti', 'telefe', 'eltrece'
      ],
      '🔗 Cloud & File Sharing': [
        'googledrive', 'dropbox', 'onedrive', 'sharepoint', 'gofile',
        'streamable', 'vidyard', 'wistia', 'sproutvideo', 'vimeo',
        'cloudflarestream', 'mux', 'piksel', 'brightcove', 'jwplatform',
        'uplynk', 'nexx', 'glomex', 'bunnycdn', 'filemoon', 'vidflex'
      ],
      '👤 Personal & User Content': [
        'youtube', 'instagram', 'twitter', 'tiktok', 'reddit', 'tumblr',
        'flickr', 'deviantart', 'soundcloud', 'bandcamp', 'mixcloud',
        'patreon', 'onlyfans', 'fanvue', 'fansly'
      ],
      '🎲 Niche & Alternative': [
        'bitchute', 'gab', 'gettr', 'parler', 'truthsocial', 'rumble',
        'odysee', 'peertube', 'voicy', 'freesound', 'freespeech',
        'newgrounds', 'gamespot', 'gamejolt', 'rokfin', 'minds',
        'worldstarhiphop', 'tmz', 'dailymail', 'buzzfeed', 'voxmedia',
        'insider', 'businessinsider', 'thesun', 'dailywire', 'theintercept',
        'democracynow', 'theguardian', 'nytimes', 'washingtonpost',
        'lemonde', 'elpais', 'ilpost', 'internazionale', 'expressen',
        'dagbladet', 'huffpost', 'inc', 'weatherchannel'
      ],
      '🏛️ Government & Public': [
        'cspan', 'senategov', 'europarl', 'parliamentlive', 'sangiin',
        'folketinget', 'bundesliga', 'wimbledon', 'pgatour', 'nrlltv',
        'mlb', 'mlbtv', 'espnsports', 'nbcsports', 'foxsports',
        'tennistv', 'masters'
      ],
      '🧩 Other': [
        'generic', 'html5', 'archive', 'internetarchive', 'webarchive',
        'slideshare', 'slidelive'
      ]
    };

    // Build lookup: extractor name → category
    const nameToCategory = {};
    for (const [cat, names] of Object.entries(categories)) {
      for (const name of names) {
        nameToCategory[name] = cat;
      }
    }

    // Group sites by category
    const byCategory = {};
    for (const cat of Object.keys(categories)) {
      byCategory[cat] = [];
    }

    const uncategorized = [];
    for (const site of sites) {
      const cleanName = site.replace(/\s*\(CURRENTLY BROKEN\)/g, '').trim().toLowerCase();
      const matchName = cleanName.split(':')[0].toLowerCase();
      if (nameToCategory[matchName] || nameToCategory[cleanName]) {
        const cat = nameToCategory[matchName] || nameToCategory[cleanName];
        byCategory[cat].push(site);
      } else {
        uncategorized.push(site);
      }
    }

    console.log(`yt-dlp supports ${total} extractors (\u2705 working + broken marked)`);
    console.log('');

    let shown = 0;
    for (const [cat, sitesInCat] of Object.entries(byCategory)) {
      if (sitesInCat.length === 0) continue;
      const sorted = sitesInCat.sort();
      console.log(`${cat} (${sorted.length}):`);
      const maxShow = Math.min(sorted.length, 30);
      for (let i = 0; i < maxShow; i++) {
        console.log(`  • ${sorted[i]}`);
      }
      if (sorted.length > maxShow) {
        console.log(`  ... and ${sorted.length - maxShow} more`);
      }
      console.log('');
      shown += sorted.length;
    }

    if (uncategorized.length > 0) {
      console.log(`📦 Other / Uncategorized (${uncategorized.length}):`);
      const maxShow = Math.min(uncategorized.length, 30);
      for (let i = 0; i < maxShow; i++) {
        console.log(`  • ${uncategorized[i]}`);
      }
      if (uncategorized.length > maxShow) {
        console.log(`  ... and ${uncategorized.length - maxShow} more`);
      }
      console.log('');
      shown += uncategorized.length;
    }

    console.log(`Total categorized: ${shown} / ${total}`);
    console.log('');
    console.log('💡 Tip: To test if a specific URL is supported, run:');
    console.log('   node extract.js --list-types <url>');
    console.log('');
    console.log('📋 Top 50 most commonly used:');
    console.log('   YouTube, TikTok, Instagram, X/Twitter, Facebook, Reddit,');
    console.log('   Twitch, Vimeo, Dailymotion, Rumble, SoundCloud, Bandcamp,');
    console.log('   Pinterest, Imgur, Tumblr, Flickr, LinkedIn, Bluesky, Telegram,');
    console.log('   Kick, Odysee, PeerTube, Bilibili, Niconico, Weibo, CNN, BBC,');
    console.log('   Al Jazeera, TED, Khan Academy, Udemy, Coursera, Netflix,');
    console.log('   HBO Max, Disney+, Amazon Prime, Apple TV+, Crunchyroll,');
    console.log('   HiDive, Tubi, Google Drive, Dropbox, Streamable, Wistia,');
    console.log('   Giphy, RedGifs, 9GAG, DeviantArt');

  } catch (e) {
    console.error('yt-dlp not found. Install with: pip install yt-dlp');
  }
  process.exit(0);
}

// ── Helpers ───────────────────────────────────────────────────────────────────

function run(cmd, args, opts = {}) {
  // Safe: calls execFileSync with array args to prevent command injection.
  // Usage: run('yt-dlp', ['--dump-json', '--flat-playlist', url])
  // Never pass user-controlled strings as the command argument.
  return execFileSync(cmd, args || [], { encoding: 'utf8', timeout: 120000, ...opts });
}

function ensureDir(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

// ── Cloud Upload ──────────────────────────────────────────────────────────────

function uploadToTmpfiles(filePath) {
  return new Promise((resolve, reject) => {
    const stat = fs.statSync(filePath);
    const fileSize = stat.size;
    const fileName = path.basename(filePath);

    console.log(`\n📦 File size: ${(fileSize / 1048576).toFixed(1)} MB`);

    // Compress if over 50MB
    if (fileSize > 50 * 1024 * 1024) {
      console.log('File > 50MB, compressing with tar.gz...');
      const compressedPath = filePath + '.tar.gz';
      try {
        run('tar', ['-czf', compressedPath, '-C', path.dirname(filePath), path.basename(filePath)]);
        const compSize = fs.statSync(compressedPath).size;
        if (compSize < fileSize && compSize <= 50 * 1024 * 1024) {
          console.log(`Compressed: ${(compSize / 1048576).toFixed(1)} MB (${((1 - compSize / fileSize) * 100).toFixed(0)}% reduction)`);
          filePath = compressedPath;
        } else {
          console.log('Compression not effective enough, uploading as-is');
          fs.unlinkSync(compressedPath);
        }
      } catch (e) {
        console.error('Compression failed, uploading original');
      }
    }

    try {
      const output = run('curl', ['-s', '-F', `file=@${filePath}`, 'https://tmpfiles.org/api/v1/upload']);
      const result = JSON.parse(output);
      if (result.status === 'success') {
        console.log(`✅ Uploaded: ${result.data.url}`);
        resolve(result.data.url);
      } else {
        reject(new Error('Upload failed: ' + output));
      }
    } catch (e) {
      reject(new Error('Upload failed: ' + e.message));
    }
  });
}

function uploadToTransferSh(filePath) {
  return new Promise((resolve, reject) => {
    const stat = fs.statSync(filePath);
    const fileName = path.basename(filePath);

    console.log(`\n📦 File size: ${(stat.size / 1048576).toFixed(1)} MB`);

    try {
      const output = run('curl', ['-s', '-T', filePath, `https://transfer.sh/${fileName}`, '-H', 'Max-Days: 30']);
      const url = output.trim();
      if (url && url.startsWith('http')) {
        console.log(`✅ Uploaded: ${url}`);
        resolve(url);
      } else {
        reject(new Error(`transfer.sh error: ${output}`));
      }
    } catch (e) {
      reject(new Error('Upload failed: ' + e.message));
    }
  });
}

function smartUpload(filePath, provider) {
  const stat = fs.statSync(filePath);
  const fileSize = stat.size;

  if (fileSize <= 50 * 1024 * 1024) {
    try {
      return uploadToTmpfiles(filePath);
    } catch (e) {
      console.log('tmpfiles.org failed, trying transfer.sh...');
    }
  }

  // Over 50MB or tmpfiles failed — try transfer.sh
  try {
    return uploadToTransferSh(filePath);
  } catch (e) {
    console.error('All upload services failed:', e.message);
    return Promise.reject(e);
  }
}

function needsCloudUpload(filePath) {
  if (noUpload) return false;
  const stat = fs.statSync(filePath);
  const sizeExceeds = stat.size > MAX_DIRECT_SEND;
  const uploadFlag = uploadToCloud;
  
  if (sizeExceeds || uploadFlag) {
    if (!confirmUpload) {
      console.error(`\n⛔ UPLOAD BLOCKED — --confirm-upload required`);
      console.error(`   File is ${(stat.size / 1048576).toFixed(1)} MB.`);
      console.error(`   To upload to public cloud, run with: --confirm-upload`);
      console.error(`   To save locally only: --no-upload`);
      return 'needs_confirm';
    }
    return true;
  }
  return false;
}

// ── List types for a URL ──────────────────────────────────────────────────────

if (listTypes) {
  try {
    const output = run('yt-dlp', ['--dump-json', '--no-download', '--flat-playlist', url]);
    if (!output || !output.trim()) {
      console.error('❌ Platform returned no data — may require authentication cookies.');
      process.exit(1);
    }
    const info = JSON.parse(output);

    if (info._type === 'playlist' && (!info.entries || info.entries.length === 0)) {
      console.log(`URL type: ${info.extractor_key || 'unknown'} (playlist with no entries)`);
      console.log('Hint: This platform may require authentication for full access.');
    } else if (info._type === 'url' || info._type === 'url_matched') {
      console.log(`URL type: ${info.extractor_key || 'unknown'}`);
      console.log(`Title: ${info.title || 'unknown'}`);
      console.log(`Format: ${info.ext || 'unknown'}`);
      if (info.duration) {
        const dur = `${Math.floor(info.duration / 60)}:${String(info.duration % 60).padStart(2, '0')}`;
        console.log(`Duration: ${dur}`);
      }
      if (info.filesize) {
        console.log(`Estimated size: ${(info.filesize / 1048576).toFixed(1)} MB`);
      }
    } else {
      console.log(`URL type: ${info._type} (${info.extractor_key || 'unknown'})`);
      if (info.title) console.log(`Title: ${info.title}`);
    }
  } catch (e) {
    console.error(`Error analyzing URL: ${e.message}`);
  }
  process.exit(0);
}

// ── Extract media ─────────────────────────────────────────────────────────────

if (!url) {
  console.error('URL required for extraction.');
  process.exit(1);
}

ensureDir(outputDir);

// Record files in output dir before download (to detect new files)
const preFiles = new Set(fs.readdirSync(outputDir));

let info;
try {
  info = JSON.parse(run('yt-dlp', ['--no-download', '-J', '--no-warnings', '--flat-playlist', url]));
} catch (e) {
  // Parse stderr for the actual error message
  const stderr = e.stderr ? e.stderr.toString() : '';
  const match = stderr.match(/ERROR:\s*\[([^\]]+)\]\s*(.+)$/m);
  if (match) {
    const platform = match[1];
    const msg = match[2].trim();
    console.error(`❌ ${platform} error: ${msg}`);
  } else {
    console.error(`❌ Failed to analyze URL: ${e.message}`);
  }
  process.exit(1);
}

if (!info || !info._type) {
  console.error('❌ Could not determine URL type. Is the URL valid?');
  process.exit(1);
}

// Check for empty playlists (common with Instagram/X without cookies)
if (info._type === 'playlist' && (!info.entries || info.entries.length === 0)) {
  console.error(`❌ ${info.extractor_key || 'Platform'} returned empty playlist.`);
  console.error('   This platform may require authentication cookies.');
  process.exit(1);
}

const title = info.title || info.get('fulltitle') || info.id || 'unknown';
const duration = info.duration ? `${Math.floor(info.duration / 60)}:${String(info.duration % 60).padStart(2, '0')}` : null;
const ext = info.ext || 'mp4';
const filesize = info.filesize ? `${(info.filesize / 1048576).toFixed(1)} MB` : null;

if (showInfo) {
  console.log(JSON.stringify(info, null, 2));
  process.exit(0);
}

if (showTitle) {
  let summary = `Title: ${title}`;
  if (duration) summary += `\nDuration: ${duration}`;
  if (filesize) summary += `\nSize: ${filesize}`;
  if (info.description) summary += `\nDescription: ${info.description.substring(0, 200)}`;
  console.log(summary);
  process.exit(0);
}

// Download the media
const outPath = path.join(outputDir, `${info.id || 'media'}.${ext}`);

(async function () {
  try {
    if (testMode) {
      console.log(`Would download: ${outPath}`);
      console.log(`Title: ${title}`);
      if (duration) console.log(`Duration: ${duration}`);
      if (filesize) console.log(`Size: ${filesize}`);
      process.exit(0);
    }

    // download command built safely below
    console.log(`Downloading: ${title}`);

    run('yt-dlp', ['-o', outPath, '--no-warnings', '--prefer-free-formats', url]);

    // Find the actual file that was created (yt-dlp may use a different name)
    const postFiles = fs.readdirSync(outputDir).filter(f => !preFiles.has(f));
    const newFile = postFiles.length > 0 ? postFiles.sort().pop() : null;

    if (newFile) {
      const newPath = path.join(outputDir, newFile);
      const stat = fs.statSync(newPath);
      console.log(`\n✅ Downloaded: ${newPath}`);
      console.log(`   Size: ${(stat.size / 1048576).toFixed(1)} MB`);
      if (duration) console.log(`   Duration: ${duration}`);
      console.log(`   Title: ${title}`);

      const uploadResult = needsCloudUpload(newPath);
      if (uploadResult === true) {
        const provider = cloudProvider || 'tmpfiles';
        console.log(`\n⚠️ Uploading to public cloud (${provider})...`);
        console.log(`   ${provider} is a public temp host. Anyone with the link can access this file.`);
        const cloudUrl = await smartUpload(newPath, provider);
        if (cloudUrl) {
          console.log(`🔗 Link: ${cloudUrl}`);
        }
      } else if (uploadResult === 'needs_confirm') {
        console.log(`\n✅ Downloaded: ${newPath}`);
        console.log(`   Size: ${(stat.size / 1048576).toFixed(1)} MB`);
        console.log(`   Title: ${title}`);
        console.log(`\n⛔ Not uploaded — public cloud upload requires --confirm-upload flag.`);
        console.log(`   Use --no-upload to save locally without prompts.`);
      } else if (directSend) {
        console.log(`\n✅ File is small enough to send directly via chat.`);
        console.log(`   Path: ${newPath}`);
        console.log(`   Size: ${(stat.size / 1048576).toFixed(1)} MB`);
      }
    } else {
      // Check if yt-dlp saved with expected name anyway
      if (fs.existsSync(outPath)) {
        const stat = fs.statSync(outPath);
        console.log(`\n✅ Downloaded: ${outPath}`);
        console.log(`   Size: ${(stat.size / 1048576).toFixed(1)} MB`);
        if (duration) console.log(`   Duration: ${duration}`);
        console.log(`   Title: ${title}`);

        const uploadResult2 = needsCloudUpload(outPath);
        if (uploadResult2 === true) {
          const provider = cloudProvider || 'tmpfiles';
          console.log(`\n⚠️ Uploading to public cloud (${provider})...`);
          console.log(`   ${provider} is a public temp host. Anyone with the link can access this file.`);
          const cloudUrl = await smartUpload(outPath, provider);
          if (cloudUrl) {
            console.log(`🔗 Link: ${cloudUrl}`);
          }
        } else if (uploadResult2 === 'needs_confirm') {
          console.log(`\n✅ Downloaded: ${outPath}`);
          console.log(`   Size: ${(stat.size / 1048576).toFixed(1)} MB`);
          console.log(`   Title: ${title}`);
          console.log(`\n⛔ Not uploaded — public cloud upload requires --confirm-upload flag.`);
          console.log(`   Use --no-upload to save locally without prompts.`);
        } else if (directSend) {
          console.log(`\n✅ File is small enough to send directly via chat.`);
          console.log(`   Path: ${outPath}`);
          console.log(`   Size: ${(stat.size / 1048576).toFixed(1)} MB`);
        }
      } else {
        console.error('❌ Download failed — no file found in output directory.');
        console.error('   Hint: Some platforms (Instagram, X) may require authentication cookies.');
      }
    }
  } catch (e) {
    const stderr = e.stderr ? e.stderr.toString() : '';
    const match = stderr.match(/ERROR:\s*\[([^\]]+)\]\s*(.+)$/m);
    if (match) {
      console.error(`❌ ${match[1]} error: ${match[2].trim()}`);
    } else {
      console.error(`❌ Download failed: ${e.message}`);
    }
    process.exit(1);
  }
})();
