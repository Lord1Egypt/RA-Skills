#!/usr/bin/env node
/**
 * Bumblebee — Talk Through Music 🐝🎵
 * 
 * An AI agent that communicates through Spotify song clips,
 * like Bumblebee from Transformers who speaks through radio snippets.
 * 
 * Usage:
 *   node bumblebee.js play <intent>           — Play a clip matching the intent
 *   node bumblebee.js say <intent1> <intent2> — Chain multiple clips into a sentence
 *   node bumblebee.js list                    — List available intents
 *   node bumblebee.js refresh                 — Refresh Spotify token
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

// Config
// Configurable paths — override with env vars or defaults to workspace layout
const WORKSPACE = process.env.BUMBLEBEE_WORKSPACE || path.join(__dirname, '..', '..', '..', 'projects');
const SPOTIFY_DIR = process.env.SPOTIFY_DIR || path.join(WORKSPACE, 'spotify');
const LYRICS_DB = path.join(__dirname, 'lyrics-db.json');
const TOKENS_FILE = path.join(SPOTIFY_DIR, 'tokens.json');
const ENV_FILE = path.join(SPOTIFY_DIR, '.env');
const CLIP_GAP_MS = 1500; // Pause between clips

// --- Spotify API helpers ---

function loadTokens() {
  return JSON.parse(fs.readFileSync(TOKENS_FILE, 'utf8'));
}

function saveTokens(tokens) {
  tokens.obtained_at = new Date().toISOString();
  fs.writeFileSync(TOKENS_FILE, JSON.stringify(tokens, null, 2));
}

function loadEnv() {
  const env = {};
  const lines = fs.readFileSync(ENV_FILE, 'utf8').split('\n');
  for (const line of lines) {
    const [key, ...val] = line.split('=');
    if (key && val.length) env[key.trim()] = val.join('=').trim();
  }
  return env;
}

function spotifyRequest(method, endpoint, body = null) {
  return new Promise((resolve, reject) => {
    const tokens = loadTokens();
    const options = {
      hostname: 'api.spotify.com',
      path: endpoint,
      method,
      headers: {
        'Authorization': `Bearer ${tokens.access_token}`,
        'Content-Type': 'application/json',
      },
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        if (res.statusCode === 401) {
          // Token expired — refresh
          refreshToken().then(() => {
            // Retry with new token
            spotifyRequest(method, endpoint, body).then(resolve).catch(reject);
          }).catch(reject);
          return;
        }
        try {
          resolve(data ? JSON.parse(data) : { status: res.statusCode });
        } catch {
          resolve({ raw: data, status: res.statusCode });
        }
      });
    });

    req.on('error', reject);
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

function refreshToken() {
  return new Promise((resolve, reject) => {
    const tokens = loadTokens();
    const env = loadEnv();
    const auth = Buffer.from(`${env.SPOTIFY_CLIENT_ID}:${env.SPOTIFY_CLIENT_SECRET}`).toString('base64');
    const postData = `grant_type=refresh_token&refresh_token=${tokens.refresh_token}`;

    const options = {
      hostname: 'accounts.spotify.com',
      path: '/api/token',
      method: 'POST',
      headers: {
        'Authorization': `Basic ${auth}`,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': Buffer.byteLength(postData),
      },
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        const newTokens = JSON.parse(data);
        if (newTokens.access_token) {
          // Keep the old refresh token if new one isn't provided
          if (!newTokens.refresh_token) newTokens.refresh_token = tokens.refresh_token;
          newTokens.scope = newTokens.scope || tokens.scope;
          saveTokens(newTokens);
          console.log('🔄 Token refreshed');
          resolve();
        } else {
          reject(new Error(`Token refresh failed: ${data}`));
        }
      });
    });

    req.on('error', reject);
    req.write(postData);
    req.end();
  });
}

// --- Lyrics DB ---

function loadLyricsDB() {
  return JSON.parse(fs.readFileSync(LYRICS_DB, 'utf8'));
}

function getClipsForIntent(intent) {
  const db = loadLyricsDB();
  const clips = db.clips[intent.toLowerCase()];
  if (!clips || clips.length === 0) return null;
  // Pick a random clip from the intent category
  return clips[Math.floor(Math.random() * clips.length)];
}

function getAllIntents() {
  const db = loadLyricsDB();
  return Object.keys(db.clips);
}

// --- Playback ---

async function playClip(clip) {
  console.log(`🎵 ${clip.track} — ${clip.artist}`);
  console.log(`   "${clip.lyric}"`);
  console.log(`   [${(clip.start_ms / 1000).toFixed(1)}s → ${(clip.end_ms / 1000).toFixed(1)}s]`);

  // Start playback at the clip start position
  const result = await spotifyRequest('PUT', '/v1/me/player/play', {
    uris: [clip.uri],
    position_ms: clip.start_ms,
  });

  if (result?.error) {
    if (result.error.reason === 'NO_ACTIVE_DEVICE') {
      console.log('❌ No active Spotify device. Open Spotify on your phone first.');
      return false;
    }
    console.log(`❌ Error: ${result.error.message}`);
    return false;
  }

  // Wait for the clip duration, then pause
  const duration = clip.end_ms - clip.start_ms;
  await sleep(duration);
  await spotifyRequest('PUT', '/v1/me/player/pause');
  return true;
}

async function sayWithMusic(intents) {
  console.log(`\n🐝 Bumblebee speaking: [${intents.join(' → ')}]\n`);

  for (let i = 0; i < intents.length; i++) {
    const clip = getClipsForIntent(intents[i]);
    if (!clip) {
      console.log(`⚠️  No clip for intent: "${intents[i]}"`);
      continue;
    }

    const success = await playClip(clip);
    if (!success) return;

    // Gap between clips (except after the last one)
    if (i < intents.length - 1) {
      await sleep(CLIP_GAP_MS);
    }
  }

  console.log('\n🐝 Message delivered.\n');
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// --- CLI ---

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  switch (command) {
    case 'list':
      const intents = getAllIntents();
      console.log('\n🐝 Available Bumblebee intents:\n');
      const db = loadLyricsDB();
      for (const intent of intents) {
        const clips = db.clips[intent];
        console.log(`  ${intent} (${clips.length} clips)`);
        for (const clip of clips) {
          console.log(`    → "${clip.lyric}" — ${clip.artist}`);
        }
      }
      console.log('\nUsage: node bumblebee.js play <intent>');
      console.log('       node bumblebee.js say <intent1> <intent2> ...');
      break;

    case 'play':
      if (!args[1]) {
        console.log('Usage: node bumblebee.js play <intent>');
        return;
      }
      const clip = getClipsForIntent(args[1]);
      if (!clip) {
        console.log(`No clip found for intent: "${args[1]}"`);
        return;
      }
      await playClip(clip);
      break;

    case 'say':
      if (args.length < 2) {
        console.log('Usage: node bumblebee.js say <intent1> <intent2> ...');
        return;
      }
      await sayWithMusic(args.slice(1));
      break;

    case 'refresh':
      await refreshToken();
      console.log('✅ Token refreshed');
      break;

    case 'now':
      // What's currently playing?
      const current = await spotifyRequest('GET', '/v1/me/player/currently-playing');
      if (current?.item) {
        const artists = current.item.artists.map(a => a.name).join(', ');
        console.log(`🎵 Now playing: ${current.item.name} — ${artists}`);
        console.log(`   Progress: ${(current.progress_ms / 1000).toFixed(0)}s / ${(current.item.duration_ms / 1000).toFixed(0)}s`);
      } else {
        console.log('Nothing playing');
      }
      break;

    case 'devices':
      const devices = await spotifyRequest('GET', '/v1/me/player/devices');
      console.log('\n📱 Devices:\n');
      for (const dev of devices.devices || []) {
        const active = dev.is_active ? '🟢' : '⚪';
        console.log(`  ${active} ${dev.name} (${dev.type}) — vol: ${dev.volume_percent}%`);
      }
      break;

    default:
      console.log(`
🐝 Bumblebee — Talk Through Music

Commands:
  list              List available intents and clips
  play <intent>     Play a single clip
  say <i1> <i2>...  Chain clips into a sentence
  now               What's currently playing
  devices           List Spotify devices
  refresh           Refresh access token

Example:
  node bumblebee.js say greeting motivation celebration
      `);
  }
}

main().catch(console.error);
