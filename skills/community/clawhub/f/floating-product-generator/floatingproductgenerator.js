#!/usr/bin/env node
// Floating Product Generator — cinematic floating product photography via Neta AI
// Usage: node floatingproductgenerator.js "your prompt" --token YOUR_TOKEN [--size square] [--ref UUID]

const API_BASE = 'https://api.talesofai.com';

const DEFAULT_PROMPT_SUFFIX =
  'professional product photography, product floating and hovering in mid-air, dramatic cinematic lighting, studio backdrop with soft gradient, crisp shadows, commercial advertising shot, ultra detailed, high-end e-commerce photography, sharp focus, premium brand aesthetic';

const SIZES = {
  square: { width: 1024, height: 1024 },
  portrait: { width: 832, height: 1216 },
  landscape: { width: 1216, height: 832 },
  tall: { width: 704, height: 1408 },
};

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--size') args.size = argv[++i];
    else if (a === '--token') args.token = argv[++i];
    else if (a === '--ref') args.ref = argv[++i];
    else if (a === '--help' || a === '-h') args.help = true;
    else args._.push(a);
  }
  return args;
}

function printHelp() {
  console.log(`Floating Product Generator

Usage:
  node floatingproductgenerator.js "your prompt" --token YOUR_TOKEN [options]

Options:
  --token <token>   Neta API token (required) — get one at https://www.neta.art/open/
  --size <size>     portrait | landscape | square | tall  (default: square)
  --ref <uuid>      Reference image UUID for style inheritance
  -h, --help        Show this help

Example:
  node floatingproductgenerator.js "luxury perfume bottle" --token "$NETA_TOKEN"
`);
}

async function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function createTask({ token, prompt, width, height, ref }) {
  const body = {
    storyId: 'DO_NOT_USE',
    jobType: 'universal',
    rawPrompt: [{ type: 'freetext', value: prompt, weight: 1 }],
    width,
    height,
    meta: { entrance: 'PICTURE,VERSE' },
    context_model_series: '8_image_edit',
  };

  if (ref) {
    body.inherit_params = {
      collection_uuid: ref,
      picture_uuid: ref,
    };
  }

  const res = await fetch(`https://api.talesofai.com/v3/make_image`, {
    method: 'POST',
    headers: {
      'x-token': token,
      'x-platform': 'nieta-app/web',
      'content-type': 'application/json',
    },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`make_image failed: ${res.status} ${res.statusText} — ${text}`);
  }

  const text = await res.text();
  let taskUuid;
  try {
    const parsed = JSON.parse(text);
    taskUuid = typeof parsed === 'string' ? parsed : parsed.task_uuid;
  } catch {
    taskUuid = text.trim().replace(/^"|"$/g, '');
  }

  if (!taskUuid) {
    throw new Error(`No task_uuid in response: ${text}`);
  }
  return taskUuid;
}

async function pollTask({ token, taskUuid }) {
  const maxAttempts = 90;
  for (let attempt = 0; attempt < maxAttempts; attempt++) {
    const res = await fetch(`https://api.talesofai.com/v1/artifact/task/${taskUuid}`, {
      headers: {
        'x-token': token,
        'x-platform': 'nieta-app/web',
        'content-type': 'application/json',
      },
    });

    if (!res.ok) {
      const text = await res.text();
      throw new Error(`poll failed: ${res.status} ${res.statusText} — ${text}`);
    }

    const data = await res.json();
    const status = data.task_status;

    if (status && status !== 'PENDING' && status !== 'MODERATION') {
      const url =
        (Array.isArray(data.artifacts) && data.artifacts[0] && data.artifacts[0].url) ||
        data.result_image_url;
      if (!url) {
        throw new Error(`Task finished with status ${status} but no image URL found`);
      }
      return url;
    }

    await sleep(2000);
  }
  throw new Error('Timed out waiting for image generation');
}

async function main() {
  const args = parseArgs(process.argv.slice(2));

  if (args.help) {
    printHelp();
    process.exit(0);
  }

  const tokenFlag = args.token;
  const TOKEN = tokenFlag;

  if (!TOKEN) {
    console.error('\n✗ Token required. Pass via: --token YOUR_TOKEN');
    console.error('  Get yours at: https://www.neta.art/open/');
    process.exit(1);
  }

  const userPrompt = args._[0];
  if (!userPrompt) {
    console.error('\n✗ Prompt required. Usage: node floatingproductgenerator.js "your prompt" --token YOUR_TOKEN');
    process.exit(1);
  }

  const sizeKey = (args.size || 'square').toLowerCase();
  const size = SIZES[sizeKey];
  if (!size) {
    console.error(`\n✗ Invalid size: ${sizeKey}. Must be one of: ${Object.keys(SIZES).join(', ')}`);
    process.exit(1);
  }

  const fullPrompt = `${userPrompt}, ${DEFAULT_PROMPT_SUFFIX}`;

  try {
    console.error(`→ Generating floating product image (${size.width}×${size.height})...`);
    const taskUuid = await createTask({
      token: TOKEN,
      prompt: fullPrompt,
      width: size.width,
      height: size.height,
      ref: args.ref,
    });
    console.error(`→ Task created: ${taskUuid}`);
    console.error(`→ Polling for result...`);
    const imageUrl = await pollTask({ token: TOKEN, taskUuid });
    console.log(imageUrl);
    process.exit(0);
  } catch (err) {
    console.error(`\n✗ ${err.message}`);
    process.exit(1);
  }
}

main();
