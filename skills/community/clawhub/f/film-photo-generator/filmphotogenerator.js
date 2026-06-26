#!/usr/bin/env node
import process from 'node:process';

const DEFAULT_PROMPT = 'analog film photograph, 35mm film grain, soft light leaks, faded color palette, muted contrast, nostalgic 1970s 1980s aesthetic, vintage kodak portra film stock, subtle vignette, authentic imperfect photography, shot on film camera, cinematic warm tones';

const SIZES = {
  square: { width: 1024, height: 1024 },
  portrait: { width: 832, height: 1216 },
  landscape: { width: 1216, height: 832 },
  tall: { width: 704, height: 1408 },
};

function parseArgs(argv) {
  const args = { positional: [], size: 'portrait', token: null, ref: null };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--size') args.size = argv[++i];
    else if (a === '--token') args.token = argv[++i];
    else if (a === '--ref') args.ref = argv[++i];
    else if (a === '--help' || a === '-h') {
      console.log('Usage: node filmphotogenerator.js "prompt" --token YOUR_TOKEN [--size portrait|landscape|square|tall] [--ref picture_uuid]');
      process.exit(0);
    } else args.positional.push(a);
  }
  return args;
}

const args = parseArgs(process.argv.slice(2));
const PROMPT = args.positional[0] || DEFAULT_PROMPT;
const tokenFlag = args.token;
const TOKEN = tokenFlag;

if (!TOKEN) {
  console.error('\n✗ Token required. Pass via: --token YOUR_TOKEN');
  console.error('  Get yours at: https://www.neta.art/open/');
  process.exit(1);
}

const sizeKey = (args.size || 'portrait').toLowerCase();
const size = SIZES[sizeKey];
if (!size) {
  console.error(`✗ Invalid size "${args.size}". Use: square, portrait, landscape, tall`);
  process.exit(1);
}

const HEADERS = {
  'x-token': TOKEN,
  'x-platform': 'nieta-app/web',
  'content-type': 'application/json',
};

async function submitJob() {
  const body = {
    storyId: 'DO_NOT_USE',
    jobType: 'universal',
    rawPrompt: [{ type: 'freetext', value: PROMPT, weight: 1 }],
    width: size.width,
    height: size.height,
    meta: { entrance: 'PICTURE,VERSE' },
    context_model_series: '8_image_edit',
  };

  if (args.ref) {
    body.inherit_params = {
      collection_uuid: args.ref,
      picture_uuid: args.ref,
    };
  }

  const res = await fetch('https://api.talesofai.com/v3/make_image', {
    method: 'POST',
    headers: HEADERS,
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Submit failed (${res.status}): ${text}`);
  }

  const ct = res.headers.get('content-type') || '';
  if (ct.includes('application/json')) {
    const data = await res.json();
    if (typeof data === 'string') return data;
    if (data && data.task_uuid) return data.task_uuid;
    return String(data).replace(/"/g, '').trim();
  }

  const text = await res.text();
  return text.replace(/"/g, '').trim();
}

async function pollTask(taskUuid) {
  const maxAttempts = 90;
  for (let i = 0; i < maxAttempts; i++) {
    await new Promise((r) => setTimeout(r, 2000));
    const res = await fetch(`https://api.talesofai.com/v1/artifact/task/${taskUuid}`, {
      headers: HEADERS,
    });
    if (!res.ok) continue;
    const data = await res.json();
    const status = data.task_status;
    if (status === 'PENDING' || status === 'MODERATION') continue;
    const url = (data.artifacts && data.artifacts[0] && data.artifacts[0].url) || data.result_image_url;
    if (url) return url;
    throw new Error(`Task ended without image. Status: ${status}`);
  }
  throw new Error('Timed out waiting for image');
}

(async () => {
  try {
    console.error(`→ Submitting (${size.width}×${size.height})...`);
    const taskUuid = await submitJob();
    console.error(`→ Task: ${taskUuid}`);
    console.error('→ Polling...');
    const url = await pollTask(taskUuid);
    console.log(url);
    process.exit(0);
  } catch (err) {
    console.error(`✗ ${err.message}`);
    process.exit(1);
  }
})();
