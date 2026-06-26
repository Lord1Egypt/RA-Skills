#!/usr/bin/env node
import process from 'node:process';

const DEFAULT_PROMPT = 'full body cosplay character reference sheet, T-pose front view, detailed costume design, vibrant colors, clean white background, professional reference art, full outfit visible, multiple costume details';
const STYLE_SUFFIX = 'anime';

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
    if (a === '--size') {
      args.size = argv[++i];
    } else if (a === '--token') {
      args.token = argv[++i];
    } else if (a === '--ref') {
      args.ref = argv[++i];
    } else if (a.startsWith('--size=')) {
      args.size = a.slice('--size='.length);
    } else if (a.startsWith('--token=')) {
      args.token = a.slice('--token='.length);
    } else if (a.startsWith('--ref=')) {
      args.ref = a.slice('--ref='.length);
    } else {
      args.positional.push(a);
    }
  }
  return args;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const tokenFlag = args.token;
  const TOKEN = tokenFlag;

  if (!TOKEN) {
    console.error('\n✗ Token required. Pass via: --token YOUR_TOKEN');
    console.error('  Get yours at: https://www.neta.art/open/');
    process.exit(1);
  }

  const userPrompt = args.positional[0];
  const PROMPT = userPrompt
    ? `${DEFAULT_PROMPT}, ${userPrompt}, ${STYLE_SUFFIX}`
    : `${DEFAULT_PROMPT}, ${STYLE_SUFFIX}`;

  const sizeKey = SIZES[args.size] ? args.size : 'portrait';
  const { width, height } = SIZES[sizeKey];

  const headers = {
    'x-token': TOKEN,
    'x-platform': 'nieta-app/web',
    'content-type': 'application/json',
  };

  const body = {
    storyId: 'DO_NOT_USE',
    jobType: 'universal',
    rawPrompt: [{ type: 'freetext', value: PROMPT, weight: 1 }],
    width,
    height,
    meta: { entrance: 'PICTURE,VERSE' },
    context_model_series: '8_image_edit',
  };

  if (args.ref) {
    body.inherit_params = {
      collection_uuid: args.ref,
      picture_uuid: args.ref,
    };
  }

  const submitRes = await fetch('https://api.talesofai.com/v3/make_image', {
    method: 'POST',
    headers,
    body: JSON.stringify(body),
  });

  if (!submitRes.ok) {
    const text = await submitRes.text();
    console.error(`\n✗ Submit failed (${submitRes.status}): ${text}`);
    process.exit(1);
  }

  const submitText = await submitRes.text();
  let task_uuid;
  try {
    const parsed = JSON.parse(submitText);
    task_uuid = typeof parsed === 'string' ? parsed : parsed.task_uuid;
  } catch {
    task_uuid = submitText.replace(/^"|"$/g, '').trim();
  }

  if (!task_uuid) {
    console.error('\n✗ No task_uuid returned');
    process.exit(1);
  }

  for (let attempt = 0; attempt < 90; attempt++) {
    await new Promise((r) => setTimeout(r, 2000));
    const pollRes = await fetch(
      `https://api.talesofai.com/v1/artifact/task/${task_uuid}`,
      { headers },
    );
    if (!pollRes.ok) continue;
    const data = await pollRes.json();
    const status = data.task_status;
    if (status === 'PENDING' || status === 'MODERATION') continue;

    const url =
      (data.artifacts && data.artifacts[0] && data.artifacts[0].url) ||
      data.result_image_url;
    if (url) {
      console.log(url);
      process.exit(0);
    }
    console.error(`\n✗ Task finished without image. Status: ${status}`);
    process.exit(1);
  }

  console.error('\n✗ Timed out waiting for image');
  process.exit(1);
}

main().catch((err) => {
  console.error(`\n✗ ${err.message}`);
  process.exit(1);
});
