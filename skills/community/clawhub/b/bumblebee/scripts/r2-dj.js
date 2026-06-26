#!/usr/bin/env node
/**
 * R2-DJ — Contextual Music Curation 🎧🤖
 * 
 * An AI DJ that reads the moment — time of day, recent listening,
 * mood, activity — and builds the perfect queue on Spotify.
 * 
 * Part of the Bumblebee skill. Bumblebee speaks through lyrics,
 * R2-DJ curates the vibe.
 * 
 * Usage:
 *   node r2-dj.js vibe                          — Auto-detect and play the right music NOW
 *   node r2-dj.js vibe --frequency <name>       — Force a specific frequency
 *   node r2-dj.js vibe --mood <description>     — Play for a mood/activity
 *   node r2-dj.js queue <uri1> <uri2> ...       — Queue specific tracks on active device
 *   node r2-dj.js context                       — Show current context (time, recent, device)
 *   node r2-dj.js frequencies                   — List all frequency profiles
 *   node r2-dj.js history                       — Show recent listening history
 *   node r2-dj.js devices                       — List Spotify devices
 *   node r2-dj.js search <query>                — Search Spotify tracks
 *   node r2-dj.js play <query|uri> [--device <name>] — Play a track/album/playlist
 *   node r2-dj.js pause                         — Pause playback
 *   node r2-dj.js skip                          — Skip to next track
 *   node r2-dj.js now                           — What's currently playing
 *   node r2-dj.js volume <0-100> [--device <name>] — Set volume
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

// --- Config ---
const WORKSPACE = process.env.BUMBLEBEE_WORKSPACE || path.join(__dirname, '..', '..', '..', 'projects');
const SPOTIFY_DIR = process.env.SPOTIFY_DIR || path.join(WORKSPACE, 'spotify');
const TOKENS_FILE = path.join(SPOTIFY_DIR, 'tokens.json');
const ENV_FILE = path.join(SPOTIFY_DIR, '.env');

// --- Frequency Profiles ---
// These define musical archetypes — the agent picks the right one based on context
const FREQUENCIES = {
  architect: {
    name: 'Architect',
    description: 'Solo builder energy. Focus, creation, flow state.',
    timeWindows: ['09:00-17:00', '22:00-02:00'],
    seeds: {
      artists: ['C418', 'Jean-Michel Jarre', 'Tangerine Dream', 'Vangelis'],
      genres: ['ambient', 'electronic', 'synthwave'],
      tracks: [] // populated by search
    },
    searchQueries: [
      'C418 minecraft volume alpha',
      'Jean-Michel Jarre Oxygène',
      'Tangerine Dream Phaedra',
      'Vangelis Blade Runner',
      'Boards of Canada Music Has the Right to Children',
      'Brian Eno Music for Airports',
    ],
    energy: { min: 0.0, max: 0.5 },
    valence: { min: 0.2, max: 0.7 },
  },
  dreamer: {
    name: 'Dreamer',
    description: 'Synthwave, retro-futurism. Driving, night cruising, imagination.',
    timeWindows: ['20:00-03:00'],
    seeds: {
      artists: ['Kavinsky', 'M83', 'Com Truise', 'Perturbator'],
      genres: ['synthwave', 'retrowave', 'electronic'],
      tracks: [],
    },
    searchQueries: [
      'Kavinsky Nightcall',
      'M83 Midnight City',
      'Com Truise Brokendate',
      'Perturbator Dangerous Days',
      'The Midnight Days of Thunder',
      'FM-84 Running in the Night',
      'Gunship Tech Noir',
    ],
    energy: { min: 0.3, max: 0.8 },
    valence: { min: 0.3, max: 0.8 },
  },
  mexican_soul: {
    name: 'Mexican Soul',
    description: 'Heritage, roots, identity. José José, Vicente, Natalia, Café Tacvba.',
    timeWindows: ['*'], // anytime
    seeds: {
      artists: ['José José', 'Vicente Fernández', 'Natalia Lafourcade', 'Café Tacvba'],
      genres: ['latin', 'ranchera', 'latin rock'],
      tracks: [],
    },
    searchQueries: [
      'José José El Triste',
      'Vicente Fernández Volver Volver',
      'Natalia Lafourcade Hasta la Raíz',
      'Café Tacvba Eres',
      'Carla Morrison Disfruto',
      'Mon Laferte Tu Falta De Querer',
      'Gustavo Cerati Crimen',
      'Soda Stereo De Música Ligera',
      'Zoé Soñé',
      'Caifanes La Negra Tomasa',
    ],
    energy: { min: 0.2, max: 0.8 },
    valence: { min: 0.2, max: 0.9 },
  },
  seeker: {
    name: 'Seeker',
    description: 'Post-midnight processing. Solfeggio, 528Hz, 639Hz, healing frequencies, deep ambient.',
    timeWindows: ['23:00-06:00'],
    seeds: {
      artists: [],
      genres: ['ambient', 'meditation', 'new age'],
      tracks: [],
    },
    searchQueries: [
      'solfeggio 528Hz meditation',
      '639Hz healing frequency',
      'deep ambient sleep meditation',
      'tibetan singing bowls meditation',
      'binaural beats focus',
      '432Hz healing',
    ],
    energy: { min: 0.0, max: 0.2 },
    valence: { min: 0.1, max: 0.5 },
  },
  cinephile: {
    name: 'Cinephile',
    description: 'Film scores, orchestral. Jóhannsson, Zimmer, Richter, Greenwood. Thinking, reflecting.',
    timeWindows: ['19:00-02:00'],
    seeds: {
      artists: ['Jóhann Jóhannsson', 'Hans Zimmer', 'Max Richter', 'Jonny Greenwood'],
      genres: ['soundtrack', 'classical', 'post-classical'],
      tracks: [],
    },
    searchQueries: [
      'Jóhann Jóhannsson Arrival',
      'Hans Zimmer Interstellar',
      'Max Richter Sleep',
      'Jonny Greenwood Phantom Thread',
      'Nils Frahm Says',
      'Ólafur Arnalds Near Light',
      'Brian Eno An Ending Ascent',
      'Clint Mansell Together We Will Live Forever',
      'Gustavo Santaolalla Babel',
    ],
    energy: { min: 0.0, max: 0.4 },
    valence: { min: 0.1, max: 0.6 },
  },
};

// --- Spotify API ---

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

function spotifyAPI(method, endpoint, body = null, retried = false) {
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
        if (res.statusCode === 401 && !retried) {
          refreshToken().then(() => {
            spotifyAPI(method, endpoint, body, true).then(resolve).catch(reject);
          }).catch(reject);
          return;
        }
        if (res.statusCode === 204 || res.statusCode === 202) {
          resolve({ ok: true, status: res.statusCode });
          return;
        }
        try { resolve(JSON.parse(data)); }
        catch { resolve({ raw: data, status: res.statusCode }); }
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
          if (!newTokens.refresh_token) newTokens.refresh_token = tokens.refresh_token;
          newTokens.scope = newTokens.scope || tokens.scope;
          saveTokens(newTokens);
          resolve();
        } else reject(new Error(`Token refresh failed: ${data}`));
      });
    });
    req.on('error', reject);
    req.write(postData);
    req.end();
  });
}

// --- Context Detection ---

function getCurrentHour() {
  // CST/CDT (America/Chicago)
  const now = new Date();
  const cst = new Date(now.toLocaleString('en-US', { timeZone: 'America/Chicago' }));
  return { hour: cst.getHours(), minute: cst.getMinutes(), day: cst.getDay(), date: cst };
}

function isInTimeWindow(hour, window) {
  if (window === '*') return true;
  const [startStr, endStr] = window.split('-');
  const start = parseInt(startStr.split(':')[0]);
  const end = parseInt(endStr.split(':')[0]);
  
  if (start <= end) {
    return hour >= start && hour < end;
  } else {
    // Wraps midnight (e.g., 22:00-02:00)
    return hour >= start || hour < end;
  }
}

function detectFrequency(hour, recentTracks = []) {
  // Score each frequency based on time match and recent listening
  const scores = {};
  
  for (const [key, freq] of Object.entries(FREQUENCIES)) {
    let score = 0;
    
    // Time match
    for (const window of freq.timeWindows) {
      if (isInTimeWindow(hour, window)) {
        score += 50;
        break;
      }
    }
    
    // Recent listening affinity — if they've been listening to similar artists
    const recentArtists = recentTracks.map(t => t.artist?.toLowerCase() || '');
    for (const seedArtist of freq.seeds.artists) {
      if (recentArtists.some(a => a.includes(seedArtist.toLowerCase()))) {
        score += 30;
      }
    }
    
    scores[key] = score;
  }
  
  // Special rules
  if (hour >= 23 || hour < 4) {
    scores.seeker += 20;
    scores.cinephile += 15;
  }
  if (hour >= 9 && hour < 17) {
    scores.architect += 20;
  }
  if (hour >= 20 && hour < 2) {
    scores.dreamer += 10;
  }
  
  // Sort by score
  const ranked = Object.entries(scores).sort((a, b) => b[1] - a[1]);
  return ranked[0][0]; // Return top frequency key
}

// --- Playback ---

async function getDevices() {
  const result = await spotifyAPI('GET', '/v1/me/player/devices');
  return result?.devices || [];
}

async function getActiveDevice(preferredName = null) {
  const devices = await getDevices();
  if (!devices.length) return null;
  
  // If preferred device name given, find it
  if (preferredName) {
    const preferred = devices.find(d => 
      d.name.toLowerCase().includes(preferredName.toLowerCase())
    );
    if (preferred) return preferred;
  }
  
  // Return active device, or first available
  return devices.find(d => d.is_active) || devices[0];
}

async function getRecentlyPlayed(limit = 20) {
  const result = await spotifyAPI('GET', `/v1/me/player/recently-played?limit=${limit}`);
  return (result?.items || []).map(item => ({
    track: item.track.name,
    artist: item.track.artists[0]?.name,
    uri: item.track.uri,
    played_at: item.played_at,
  }));
}

async function getCurrentlyPlaying() {
  const result = await spotifyAPI('GET', '/v1/me/player/currently-playing');
  if (!result?.item) return null;
  return {
    track: result.item.name,
    artist: result.item.artists.map(a => a.name).join(', '),
    album: result.item.album.name,
    uri: result.item.uri,
    progress_ms: result.progress_ms,
    duration_ms: result.item.duration_ms,
    is_playing: result.is_playing,
  };
}

async function searchTracks(query, limit = 10) {
  const q = encodeURIComponent(query);
  const result = await spotifyAPI('GET', `/v1/search?q=${q}&type=track&limit=${limit}&market=US`);
  return (result?.tracks?.items || []).map(t => ({
    name: t.name,
    artist: t.artists.map(a => a.name).join(', '),
    album: t.album.name,
    uri: t.uri,
    duration_ms: t.duration_ms,
  }));
}

async function buildQueue(frequency, count = 12) {
  const freq = FREQUENCIES[frequency];
  if (!freq) throw new Error(`Unknown frequency: ${frequency}`);
  
  const uris = [];
  const seen = new Set();
  
  // Search each query, collect unique tracks
  for (const query of freq.searchQueries) {
    const tracks = await searchTracks(query, 3);
    for (const t of tracks) {
      if (!seen.has(t.uri)) {
        seen.add(t.uri);
        uris.push(t);
        if (uris.length >= count) break;
      }
    }
    if (uris.length >= count) break;
  }
  
  // Shuffle for variety (Fisher-Yates)
  for (let i = uris.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [uris[i], uris[j]] = [uris[j], uris[i]];
  }
  
  return uris.slice(0, count);
}

async function playTracks(uris, deviceId = null) {
  const body = { uris: uris.map(u => typeof u === 'string' ? u : u.uri) };
  const endpoint = deviceId 
    ? `/v1/me/player/play?device_id=${deviceId}`
    : '/v1/me/player/play';
  
  return spotifyAPI('PUT', endpoint, body);
}

// --- CLI Commands ---

async function cmdVibe(args) {
  const { hour, minute, day, date } = getCurrentHour();
  const timeStr = `${String(hour).padStart(2, '0')}:${String(minute).padStart(2, '0')}`;
  const dayNames = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  
  console.log(`\n🎧 R2-DJ — Reading the room...`);
  console.log(`   ${dayNames[day]} ${timeStr} CST\n`);
  
  // Get recent listening for context
  const recent = await getRecentlyPlayed(10);
  if (recent.length) {
    console.log('📻 Recent:');
    recent.slice(0, 5).forEach(t => console.log(`   ${t.track} — ${t.artist}`));
    console.log('');
  }
  
  // Detect or force frequency
  let freqKey = null;
  const freqArg = args.find((_, i) => args[i - 1] === '--frequency');
  const moodArg = args.find((_, i) => args[i - 1] === '--mood');
  
  if (freqArg) {
    freqKey = freqArg.toLowerCase().replace(/\s+/g, '_');
    if (!FREQUENCIES[freqKey]) {
      console.log(`❌ Unknown frequency: ${freqArg}`);
      console.log(`   Available: ${Object.keys(FREQUENCIES).join(', ')}`);
      return;
    }
  } else {
    freqKey = detectFrequency(hour, recent);
  }
  
  const freq = FREQUENCIES[freqKey];
  console.log(`🔊 Frequency: ${freq.name}`);
  console.log(`   ${freq.description}\n`);
  
  // Build queue
  console.log('🎵 Building queue...\n');
  const queue = await buildQueue(freqKey);
  
  if (!queue.length) {
    console.log('❌ Could not find tracks. Try a different frequency.');
    return;
  }
  
  // Find device
  const deviceArg = args.find((_, i) => args[i - 1] === '--device');
  const device = await getActiveDevice(deviceArg);
  
  if (!device) {
    console.log('❌ No Spotify devices found. Open Spotify first.');
    return;
  }
  
  console.log(`📱 Device: ${device.name} (${device.type})\n`);
  
  // Play
  const result = await playTracks(queue, device.id);
  
  if (result?.error) {
    console.log(`❌ ${result.error.message}`);
    return;
  }
  
  console.log('▶️  Now playing:\n');
  queue.forEach((t, i) => {
    const marker = i === 0 ? '►' : ' ';
    console.log(`  ${marker} ${i + 1}. ${t.name} — ${t.artist}`);
  });
  
  console.log(`\n🎧 ${queue.length} tracks queued. Enjoy. 🤖`);
  
  // Output JSON summary for the agent to use in its reply
  console.log('\n---JSON_SUMMARY---');
  console.log(JSON.stringify({
    frequency: freqKey,
    frequencyName: freq.name,
    description: freq.description,
    device: device.name,
    trackCount: queue.length,
    tracks: queue.map(t => ({ name: t.name, artist: t.artist, uri: t.uri })),
    time: timeStr,
    day: dayNames[day],
  }));
}

async function cmdContext() {
  const { hour, minute, day, date } = getCurrentHour();
  const timeStr = `${String(hour).padStart(2, '0')}:${String(minute).padStart(2, '0')}`;
  const dayNames = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  
  console.log(`\n🎧 R2-DJ Context\n`);
  console.log(`⏰ Time: ${dayNames[day]} ${timeStr} CST`);
  
  // Recent
  const recent = await getRecentlyPlayed(10);
  console.log(`\n📻 Recently Played:`);
  recent.forEach(t => console.log(`   ${t.track} — ${t.artist}`));
  
  // Current
  const current = await getCurrentlyPlaying();
  if (current) {
    console.log(`\n▶️  Now Playing: ${current.track} — ${current.artist}`);
    console.log(`   ${Math.round(current.progress_ms / 1000)}s / ${Math.round(current.duration_ms / 1000)}s`);
  }
  
  // Auto-detected frequency
  const freqKey = detectFrequency(hour, recent);
  const freq = FREQUENCIES[freqKey];
  console.log(`\n🔊 Detected Frequency: ${freq.name}`);
  console.log(`   ${freq.description}`);
  
  // Devices
  const devices = await getDevices();
  console.log(`\n📱 Devices:`);
  devices.forEach(d => {
    const icon = d.is_active ? '🟢' : '⚪';
    console.log(`   ${icon} ${d.name} (${d.type}) — vol ${d.volume_percent}%`);
  });
}

async function cmdFrequencies() {
  console.log('\n🎧 R2-DJ Frequency Profiles\n');
  for (const [key, freq] of Object.entries(FREQUENCIES)) {
    console.log(`  🔊 ${freq.name} (${key})`);
    console.log(`     ${freq.description}`);
    console.log(`     Time: ${freq.timeWindows.join(', ')}`);
    console.log(`     Artists: ${freq.seeds.artists.slice(0, 4).join(', ') || 'genre-based'}`);
    console.log('');
  }
}

async function cmdHistory() {
  const recent = await getRecentlyPlayed(20);
  console.log('\n📻 Recently Played:\n');
  recent.forEach((t, i) => {
    const time = new Date(t.played_at).toLocaleString('en-US', { timeZone: 'America/Chicago', hour: '2-digit', minute: '2-digit' });
    console.log(`  ${String(i + 1).padStart(2)}. ${t.track} — ${t.artist}  (${time})`);
  });
}

async function cmdDevices() {
  const devices = await getDevices();
  console.log('\n📱 Spotify Devices:\n');
  if (!devices.length) {
    console.log('  No devices found. Open Spotify on a device.');
    return;
  }
  devices.forEach(d => {
    const icon = d.is_active ? '🟢' : '⚪';
    console.log(`  ${icon} ${d.name} (${d.type}) — vol ${d.volume_percent}%  [${d.id}]`);
  });
}

async function cmdSearch(args) {
  const query = args.join(' ');
  if (!query) {
    console.log('Usage: r2-dj.js search <query>');
    return;
  }
  const tracks = await searchTracks(query);
  console.log(`\n🔍 Results for "${query}":\n`);
  tracks.forEach((t, i) => {
    const dur = `${Math.floor(t.duration_ms / 60000)}:${String(Math.round((t.duration_ms % 60000) / 1000)).padStart(2, '0')}`;
    console.log(`  ${i + 1}. ${t.name} — ${t.artist} (${dur})  ${t.uri}`);
  });
}

async function cmdPlay(args) {
  const deviceArg = args.find((_, i) => args[i - 1] === '--device');
  const cleanArgs = args.filter((a, i) => a !== '--device' && args[i - 1] !== '--device');
  const query = cleanArgs.join(' ');
  
  if (!query) {
    console.log('Usage: r2-dj.js play <query or spotify:uri> [--device <name>]');
    return;
  }
  
  const device = await getActiveDevice(deviceArg);
  if (!device) {
    console.log('❌ No Spotify devices found.');
    return;
  }
  
  // If it's already a URI, play directly
  if (query.startsWith('spotify:')) {
    const isTrack = query.startsWith('spotify:track:');
    const isAlbum = query.startsWith('spotify:album:');
    const isPlaylist = query.startsWith('spotify:playlist:');
    
    const body = isTrack ? { uris: [query] } : { context_uri: query };
    const result = await spotifyAPI('PUT', `/v1/me/player/play?device_id=${device.id}`, body);
    
    if (result?.error) {
      console.log(`❌ ${result.error.message}`);
    } else {
      console.log(`▶️  Playing on ${device.name}`);
    }
    return;
  }
  
  // Search and play first result
  const tracks = await searchTracks(query, 1);
  if (!tracks.length) {
    console.log(`❌ No results for "${query}"`);
    return;
  }
  
  const track = tracks[0];
  const result = await playTracks([track], device.id);
  
  if (result?.error) {
    console.log(`❌ ${result.error.message}`);
  } else {
    console.log(`▶️  ${track.name} — ${track.artist} on ${device.name}`);
  }
}

async function cmdNow() {
  const current = await getCurrentlyPlaying();
  if (!current) {
    console.log('Nothing playing.');
    return;
  }
  const progress = `${Math.floor(current.progress_ms / 60000)}:${String(Math.round((current.progress_ms % 60000) / 1000)).padStart(2, '0')}`;
  const duration = `${Math.floor(current.duration_ms / 60000)}:${String(Math.round((current.duration_ms % 60000) / 1000)).padStart(2, '0')}`;
  const status = current.is_playing ? '▶️' : '⏸️';
  
  console.log(`${status} ${current.track} — ${current.artist}`);
  console.log(`   Album: ${current.album}`);
  console.log(`   ${progress} / ${duration}`);
  console.log(`   URI: ${current.uri}`);
}

async function cmdPause() {
  const result = await spotifyAPI('PUT', '/v1/me/player/pause');
  if (result?.error) console.log(`❌ ${result.error.message}`);
  else console.log('⏸️  Paused.');
}

async function cmdSkip() {
  const result = await spotifyAPI('POST', '/v1/me/player/next');
  if (result?.error) console.log(`❌ ${result.error.message}`);
  else {
    // Wait a moment and show what's now playing
    await new Promise(r => setTimeout(r, 500));
    await cmdNow();
  }
}

async function cmdVolume(args) {
  const vol = parseInt(args[0]);
  if (isNaN(vol) || vol < 0 || vol > 100) {
    console.log('Usage: r2-dj.js volume <0-100>');
    return;
  }
  const deviceArg = args.find((_, i) => args[i - 1] === '--device');
  const device = await getActiveDevice(deviceArg);
  
  let endpoint = `/v1/me/player/volume?volume_percent=${vol}`;
  if (device) endpoint += `&device_id=${device.id}`;
  
  const result = await spotifyAPI('PUT', endpoint);
  if (result?.error) console.log(`❌ ${result.error.message}`);
  else console.log(`🔊 Volume: ${vol}%`);
}

async function cmdQueue(args) {
  // Add tracks to queue (Spotify queue = single-track add)
  for (const uri of args) {
    if (!uri.startsWith('spotify:')) {
      console.log(`⚠️  Skipping non-URI: ${uri}`);
      continue;
    }
    const result = await spotifyAPI('POST', `/v1/me/player/queue?uri=${encodeURIComponent(uri)}`);
    if (result?.error) {
      console.log(`❌ ${result.error.message}`);
    } else {
      console.log(`✅ Queued: ${uri}`);
    }
  }
}

// --- Main ---

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  try {
    switch (command) {
      case 'vibe':     await cmdVibe(args.slice(1)); break;
      case 'context':  await cmdContext(); break;
      case 'frequencies': await cmdFrequencies(); break;
      case 'history':  await cmdHistory(); break;
      case 'devices':  await cmdDevices(); break;
      case 'search':   await cmdSearch(args.slice(1)); break;
      case 'play':     await cmdPlay(args.slice(1)); break;
      case 'now':      await cmdNow(); break;
      case 'pause':    await cmdPause(); break;
      case 'skip':     await cmdSkip(); break;
      case 'volume':   await cmdVolume(args.slice(1)); break;
      case 'queue':    await cmdQueue(args.slice(1)); break;
      default:
        console.log(`
🎧 R2-DJ — Contextual Music Curation

Commands:
  vibe [--frequency <name>] [--device <name>]  Auto-curate and play the right music
  context                                       Show current context (time, recent, device)
  frequencies                                   List frequency profiles
  history                                       Recent listening history
  devices                                       List Spotify devices
  search <query>                                Search tracks
  play <query|uri> [--device <name>]            Play a track
  now                                           Currently playing
  pause                                         Pause playback
  skip                                          Skip track
  volume <0-100>                                Set volume
  queue <uri1> [uri2...]                        Add to queue

Frequencies: architect, dreamer, mexican_soul, seeker, cinephile
        `);
    }
  } catch (err) {
    console.error(`❌ Error: ${err.message}`);
  }
}

main();
