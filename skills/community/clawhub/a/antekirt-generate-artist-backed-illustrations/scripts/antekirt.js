#!/usr/bin/env node

const readline = require('node:readline/promises');
const { stdin: input, stdout: output } = require('node:process');

const API_KEY = process.env.ANTEKIRT_API_KEY;
const BASE_URL = (process.env.ANTEKIRT_BASE_URL || 'https://antekirt.com').replace(/\/$/, '');

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith('--')) {
      const [k, inline] = a.slice(2).split('=');
      if (inline !== undefined) {
        args[k] = inline;
      } else if (argv[i + 1] && !argv[i + 1].startsWith('--')) {
        args[k] = argv[++i];
      } else {
        args[k] = true;
      }
    } else {
      args._.push(a);
    }
  }
  return args;
}

function requireApiKey() {
  if (!API_KEY) {
    console.error('Missing ANTEKIRT_API_KEY env variable.');
    process.exit(1);
  }
}

function generationIdFrom(payload) {
  return payload?.id || payload?.generationId || payload?.data?.id || payload?.data?.generationId || null;
}

function cleanString(v) {
  return String(v || '').trim().toLowerCase();
}

function imageUrlFrom(value) {
  if (!value) return null;
  if (typeof value === 'string') return value;
  return value?.url || value?.src || value?.imageUrl || null;
}

async function api(path, options = {}) {
  const res = await fetch(`${BASE_URL}${path}`, {
    ...options,
    headers: {
      'x-api-key': API_KEY,
      'content-type': 'application/json',
      ...(options.headers || {}),
    },
  });

  const text = await res.text();
  let data;
  try {
    data = text ? JSON.parse(text) : {};
  } catch {
    data = { raw: text };
  }

  if (!res.ok) {
    const msg = data?.messages?.join('; ') || data?.message || res.statusText;
    throw new Error(`${res.status} ${msg}`);
  }

  return data;
}

function pickThumb(a) {
  const direct = [
    a?.thumbnail,
    a?.thumbnailUrl,
    a?.avatar,
    a?.avatarUrl,
    a?.image,
    a?.imageUrl,
    a?.profileImage,
    a?.profileImageUrl,
    a?.photo,
    a?.photoUrl,
  ].find(Boolean);
  if (direct) return direct;

  const nested = [
    a?.assets?.thumbnail,
    a?.assets?.avatar,
    a?.assets?.image,
    a?.media?.thumbnail,
    a?.media?.avatar,
    a?.media?.image,
  ].find(Boolean);
  return nested || null;
}

function rowsFromList(payload) {
  const items = payload?.items || payload?.data || payload?.results || payload;
  if (Array.isArray(items)) return items;
  return [];
}

function artistLabel(a) {
  return a?.name || a?.displayName || '(unnamed)';
}

async function fetchArtists(args = {}) {
  const search = args.search ? `&search=${encodeURIComponent(args.search)}` : '';
  const limit = Number(args.limit || 25);
  const page = Number(args.page || 1);
  const data = await api(`/api/v1/artists?page=${page}&limit=${limit}${search}`);
  return { data, rows: rowsFromList(data) };
}

async function listArtists(args) {
  requireApiKey();
  const { data, rows } = await fetchArtists(args);

  if (args.json) {
    console.log(JSON.stringify(data, null, 2));
    return;
  }

  if (!rows.length) {
    console.log('No artists found.');
    return;
  }

  rows.forEach((a, idx) => {
    const name = artistLabel(a);
    const thumb = pickThumb(a) || 'No thumbnail';
    console.log(`${idx + 1}. ${name}`);
    console.log(`   id: ${a.id}`);
    console.log(`   thumbnail: ${thumb}`);
  });
}

function findArtist(rows, value) {
  const v = cleanString(value);
  if (!v) return null;

  if (/^\d+$/.test(v)) {
    const idx = Number(v);
    if (idx >= 1 && idx <= rows.length) return rows[idx - 1];
  }

  return rows.find((a) => {
    const name = cleanString(artistLabel(a));
    const id = cleanString(a?.id);
    return id === v || name === v || name.includes(v);
  }) || null;
}

async function chooseArtistInteractively(seedArgs = {}) {
  const { rows } = await fetchArtists(seedArgs);
  if (!rows.length) throw new Error('No artists available to pick.');

  console.log('Pick an artist:');
  rows.forEach((a, idx) => {
    const name = artistLabel(a);
    const thumb = pickThumb(a) || 'No thumbnail';
    console.log(`${idx + 1}) ${name}`);
    console.log(`   id: ${a.id}`);
    console.log(`   ${thumb}`);
  });

  const rl = readline.createInterface({ input, output });
  const ans = await rl.question('Enter number, name, or id: ');
  rl.close();

  const found = findArtist(rows, ans);
  if (!found) throw new Error('Invalid selection.');
  return found;
}

async function resolveArtist(args) {
  if (args['artist-id']) return { id: args['artist-id'], name: null };

  if (args.artist) {
    const { rows } = await fetchArtists(args);
    const found = findArtist(rows, args.artist);
    if (!found) throw new Error(`Artist not found for --artist "${args.artist}"`);
    return { id: found.id, name: artistLabel(found) };
  }

  if (args.pick) {
    const artist = await chooseArtistInteractively(args);
    return { id: artist.id, name: artistLabel(artist) };
  }

  throw new Error('Provide --artist-id <uuid>, --artist <name|id|index>, or --pick');
}

async function getGeneration(id) {
  return api(`/api/v1/generations/${encodeURIComponent(id)}`);
}

async function pollGeneration(id, timeoutSec = 120, intervalMs = 3000) {
  const start = Date.now();
  while (true) {
    const response = await fetch(`${BASE_URL}/api/v1/generations/${encodeURIComponent(id)}`, {
      headers: {
        'x-api-key': API_KEY,
        'content-type': 'application/json',
      },
    });

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    const status = data.status || data.data?.status;

    if (status === 'completed') return data.data ? data.data : data;
    if (status === 'failed') throw new Error(`Generation failed: ${data?.messages?.join('; ') || 'unknown reason'}`);

    const elapsed = (Date.now() - start) / 1000;
    if (elapsed > timeoutSec) throw new Error(`Timed out after ${timeoutSec}s while waiting for generation ${id}`);

    process.stdout.write(`Waiting... status=${status}\n`);
    await new Promise((r) => setTimeout(r, intervalMs));
  }
}

function printGenerationOutputs(done) {
  const outputs = done?.outputs || {};
  const images = Array.isArray(outputs.images) ? outputs.images : [];

  console.log('Completed ✅');
  console.log(`status: ${done.status}`);
  console.log(`generationId: ${done.id || done.generationId || '(unknown)'}`);

  if (images.length) {
    images.forEach((img, idx) => {
      const url = imageUrlFrom(img) || JSON.stringify(img);
      console.log(`image[${idx}]: ${url}`);
    });
  } else {
    console.log('images: none');
  }

  if (outputs.svg) {
    const svgUrl = imageUrlFrom(outputs.svg) || outputs.svg?.svgUrl || JSON.stringify(outputs.svg);
    console.log(`svg: ${svgUrl}`);
  }

  if (outputs.video) {
    const videoUrl = outputs.video?.url || outputs.video?.src || outputs.video?.videoUrl || JSON.stringify(outputs.video);
    console.log(`video: ${videoUrl}`);
  }
}

async function startAndWait(path, body, timeoutSec) {
  const created = await api(path, {
    method: 'POST',
    body: JSON.stringify(body),
  });

  const id = generationIdFrom(created);
  if (!id) {
    console.log(JSON.stringify(created, null, 2));
    throw new Error('Generation ID not found in response.');
  }

  console.log(`Generation started: ${id}`);
  const done = await pollGeneration(id, timeoutSec);
  printGenerationOutputs(done);
}

async function generateImage(args) {
  requireApiKey();
  const prompt = args.prompt;
  if (!prompt) throw new Error('Missing --prompt');

  const artist = await resolveArtist(args);
  if (artist.name) {
    console.log(`Selected artist: ${artist.name} (${artist.id})`);
  }

  await startAndWait('/api/v1/generations/image', {
    artistId: artist.id,
    prompt,
  }, Number(args.timeout || 180));
}

async function generateSvg(args) {
  requireApiKey();
  const generationId = args['generation-id'];
  if (!generationId) throw new Error('Missing --generation-id <uuid>');

  await startAndWait('/api/v1/generations/svg', {
    generationId,
    imageIndex: Number(args['image-index'] || 0),
  }, Number(args.timeout || 180));
}

async function generateVideo(args) {
  requireApiKey();
  const generationId = args['generation-id'];
  const prompt = args.prompt;
  if (!generationId) throw new Error('Missing --generation-id <uuid>');
  if (!prompt) throw new Error('Missing --prompt');

  await startAndWait('/api/v1/generations/video', {
    generationId,
    imageIndex: Number(args['image-index'] || 0),
    prompt,
    duration: Number(args.duration || 4),
    fps: Number(args.fps || 24),
    resolution: args.resolution || '480p',
    aspectRatio: args['aspect-ratio'] || '16:9',
    cameraFixed: Boolean(args['camera-fixed']),
  }, Number(args.timeout || 300));
}

function printHelp() {
  console.log(`Antekirt CLI

Usage:
  antekirt.js artists [--search <text>] [--limit <n>] [--json]
  antekirt.js image --prompt <text> [--artist-id <uuid> | --artist <name|id|index> | --pick] [--timeout <sec>]
  antekirt.js svg --generation-id <uuid> [--image-index <n>] [--timeout <sec>]
  antekirt.js video --generation-id <uuid> --prompt <text> [--image-index <n>] [--duration <2-10>] [--fps <12-60>] [--resolution <480p|720p>] [--aspect-ratio <16:9|9:16|1:1>] [--camera-fixed] [--timeout <sec>]

Env:
  ANTEKIRT_API_KEY   required
  ANTEKIRT_BASE_URL  optional (default: https://antekirt.com)
`);
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const cmd = args._[0];
  try {
    if (!cmd || cmd === 'help' || cmd === '--help') {
      printHelp();
      return;
    }
    if (cmd === 'artists') return await listArtists(args);
    if (cmd === 'image') return await generateImage(args);
    if (cmd === 'svg') return await generateSvg(args);
    if (cmd === 'video') return await generateVideo(args);

    printHelp();
    process.exitCode = 1;
  } catch (e) {
    console.error(`Error: ${e.message}`);
    process.exit(1);
  }
}

main();
