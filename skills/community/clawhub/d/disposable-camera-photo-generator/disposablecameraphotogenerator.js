#!/usr/bin/env node
import process from 'node:process';

const SIZES = {
  square: { width: 1024, height: 1024 },
  portrait: { width: 832, height: 1216 },
  landscape: { width: 1216, height: 832 },
  tall: { width: 704, height: 1408 },
};

const DEFAULT_PROMPT = 'candid disposable camera photograph, harsh on-camera flash, slight overexposure, soft motion blur, grainy 35mm film texture, washed colors with magenta-green color cast, red-eye effect, fingerprint smudge on lens, light leak in corner, low contrast highlights, authentic 2000s point-and-shoot snapshot, lo-fi imperfect aesthetic, date stamp in orange in corner';

function parseArgs(argv) {
  const args = { size: 'square', prompt: null, token: null, ref: null };
  const rest = [];
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--size') args.size = argv[++i];
    else if (a === '--token') args.token = argv[++i];
    else if (a === '--ref') args.ref = argv[++i];
    else if (a === '--help' || a === '-h') {
      console.log('Usage: node disposablecameraphotogenerator.js "prompt" [--size square|portrait|landscape|tall] [--token TOKEN] [--ref PICTURE_UUID]');
      process.exit(0);
    } else rest.push(a);
  }
  if (rest.length > 0) args.prompt = rest.join(' ');
  return args;
}

async function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

async function main() {
  const { size, prompt, token: tokenFlag, ref } = parseArgs(process.argv.slice(2));

  const TOKEN = tokenFlag;

  if (!TOKEN) {
    console.error('\n✗ Token required. Pass via: --token YOUR_TOKEN');
    console.error('  Get yours at: https://www.neta.art/open/');
    process.exit(1);
  }

  const PROMPT = prompt || DEFAULT_PROMPT;
  const dims = SIZES[size];
  if (!dims) {
    console.error(`✗ Invalid --size: ${size}. Use one of: ${Object.keys(SIZES).join(', ')}`);
    process.exit(1);
  }

  const headers = {
    'x-token': TOKEN,
    'x-platform': 'nieta-app/web',
    'content-type': 'application/json',
  };

  const body = {
    storyId: 'DO_NOT_USE',
    jobType: 'universal',
    rawPrompt: [{ type: 'freetext', value: PROMPT, weight: 1 }],
    width: dims.width,
    height: dims.height,
    meta: { entrance: 'PICTURE,VERSE' },
    context_model_series: '8_image_edit',
  };

  if (ref) {
    body.inherit_params = { collection_uuid: ref, picture_uuid: ref };
  }

  console.error(`→ Submitting (${dims.width}×${dims.height})...`);

  const submitRes = await fetch('https://api.talesofai.com/v3/make_image', {
    method: 'POST',
    headers,
    body: JSON.stringify(body),
  });

  if (!submitRes.ok) {
    const text = await submitRes.text();
    console.error(`✗ Submit failed (${submitRes.status}): ${text}`);
    process.exit(1);
  }

  const submitText = await submitRes.text();
  let task_uuid;
  try {
    const parsed = JSON.parse(submitText);
    task_uuid = typeof parsed === 'string' ? parsed : parsed.task_uuid;
  } catch {
    task_uuid = submitText.trim().replace(/^"|"$/g, '');
  }

  if (!task_uuid) {
    console.error(`✗ No task_uuid in response: ${submitText}`);
    process.exit(1);
  }

  console.error(`→ Task: ${task_uuid}`);
  console.error('→ Polling...');

  for (let attempt = 0; attempt < 90; attempt++) {
    await sleep(2000);
    const pollRes = await fetch(`https://api.talesofai.com/v1/artifact/task/${task_uuid}`, {
      method: 'GET',
      headers,
    });

    if (!pollRes.ok) {
      const text = await pollRes.text();
      console.error(`✗ Poll failed (${pollRes.status}): ${text}`);
      process.exit(1);
    }

    const data = await pollRes.json();
    const status = data.task_status;

    if (status === 'PENDING' || status === 'MODERATION') {
      continue;
    }

    const url = (data.artifacts && data.artifacts[0] && data.artifacts[0].url) || data.result_image_url;
    if (url) {
      console.log(url);
      process.exit(0);
    }

    console.error(`✗ Task finished (status=${status}) but no image URL found.`);
    console.error(JSON.stringify(data, null, 2));
    process.exit(1);
  }

  console.error('✗ Timed out after 90 polls (~3 minutes).');
  process.exit(1);
}

main().catch((err) => {
  console.error(`✗ Error: ${err.message}`);
  process.exit(1);
});
