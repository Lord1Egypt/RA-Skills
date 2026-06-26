#!/usr/bin/env node
import process from 'node:process';

const DEFAULT_PROMPT = "professional food photography, overhead shot of a gourmet dish on rustic ceramic plate, natural soft window light, shallow depth of field, vibrant fresh ingredients, garnishes and herbs, steam rising, warm golden hour tones, restaurant-quality plating, magazine editorial style, 50mm lens look, appetizing color grading";

const SIZES = {
  square: { width: 1024, height: 1024 },
  portrait: { width: 832, height: 1216 },
  landscape: { width: 1216, height: 832 },
  tall: { width: 704, height: 1408 },
};

function parseArgs(argv) {
  const args = { prompt: null, size: 'square', token: null, ref: null };
  const rest = [];
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--size') {
      args.size = argv[++i];
    } else if (a === '--token') {
      args.token = argv[++i];
    } else if (a === '--ref') {
      args.ref = argv[++i];
    } else if (a.startsWith('--size=')) {
      args.size = a.slice(7);
    } else if (a.startsWith('--token=')) {
      args.token = a.slice(8);
    } else if (a.startsWith('--ref=')) {
      args.ref = a.slice(6);
    } else {
      rest.push(a);
    }
  }
  if (rest.length > 0) args.prompt = rest.join(' ');
  return args;
}

async function main() {
  const { prompt: promptArg, size, token: tokenFlag, ref } = parseArgs(process.argv.slice(2));

  const TOKEN = tokenFlag;

  if (!TOKEN) {
    console.error('\n✗ Token required. Pass via: --token YOUR_TOKEN');
    console.error('  Get yours at: https://www.neta.art/open/');
    process.exit(1);
  }

  const PROMPT = promptArg || DEFAULT_PROMPT;
  const dims = SIZES[size] || SIZES.square;

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

  console.error(`→ Submitting prompt (${dims.width}×${dims.height})...`);

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
  let taskUuid;
  try {
    const parsed = JSON.parse(submitText);
    taskUuid = typeof parsed === 'string' ? parsed : parsed.task_uuid;
  } catch {
    taskUuid = submitText.replace(/^"|"$/g, '').trim();
  }

  if (!taskUuid) {
    console.error('✗ No task_uuid returned');
    process.exit(1);
  }

  console.error(`→ Task: ${taskUuid}`);
  console.error('→ Polling...');

  for (let attempt = 0; attempt < 90; attempt++) {
    await new Promise((r) => setTimeout(r, 2000));
    const pollRes = await fetch(`https://api.talesofai.com/v1/artifact/task/${taskUuid}`, {
      method: 'GET',
      headers,
    });

    if (!pollRes.ok) {
      console.error(`  poll ${attempt + 1}: HTTP ${pollRes.status}`);
      continue;
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

    console.error(`✗ Task ended with status "${status}" but no image URL`);
    console.error(JSON.stringify(data, null, 2));
    process.exit(1);
  }

  console.error('✗ Timed out waiting for image');
  process.exit(1);
}

main().catch((err) => {
  console.error(`✗ ${err.message}`);
  process.exit(1);
});
