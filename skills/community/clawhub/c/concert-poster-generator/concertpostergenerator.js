#!/usr/bin/env node
import process from 'node:process';

const DEFAULT_PROMPT = 'bold concert poster design, dramatic stage lighting, vibrant typography composition, high contrast cinematic mood, music event flyer aesthetic, eye-catching gig poster art';

const SIZES = {
  square: { width: 1024, height: 1024 },
  portrait: { width: 832, height: 1216 },
  landscape: { width: 1216, height: 832 },
  tall: { width: 704, height: 1408 },
};

function parseArgs(argv) {
  const args = argv.slice(2);
  let prompt = null;
  let size = 'portrait';
  let tokenFlag = null;
  let ref = null;

  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if (a === '--size') {
      size = args[++i];
    } else if (a === '--token') {
      tokenFlag = args[++i];
    } else if (a === '--ref') {
      ref = args[++i];
    } else if (!a.startsWith('--') && prompt === null) {
      prompt = a;
    }
  }

  return { prompt, size, tokenFlag, ref };
}

async function main() {
  const { prompt, size, tokenFlag, ref } = parseArgs(process.argv);

  const TOKEN = tokenFlag;

  if (!TOKEN) {
    console.error('\n✗ Token required. Pass via: --token YOUR_TOKEN');
    console.error('  Get yours at: https://www.neta.art/open/');
    process.exit(1);
  }

  const PROMPT = prompt || DEFAULT_PROMPT;

  const dims = SIZES[size];
  if (!dims) {
    console.error(`\n✗ Invalid size: ${size}. Use one of: ${Object.keys(SIZES).join(', ')}`);
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

  console.error(`→ Generating: "${PROMPT}"`);
  console.error(`  Size: ${size} (${dims.width}×${dims.height})`);

  let createRes;
  try {
    createRes = await fetch('https://api.talesofai.com/v3/make_image', {
      method: 'POST',
      headers,
      body: JSON.stringify(body),
    });
  } catch (err) {
    console.error(`\n✗ Network error: ${err.message}`);
    process.exit(1);
  }

  if (!createRes.ok) {
    const text = await createRes.text();
    console.error(`\n✗ make_image failed (${createRes.status}): ${text}`);
    process.exit(1);
  }

  const rawText = await createRes.text();
  let taskUuid;
  try {
    const parsed = JSON.parse(rawText);
    if (typeof parsed === 'string') {
      taskUuid = parsed;
    } else if (parsed && parsed.task_uuid) {
      taskUuid = parsed.task_uuid;
    } else {
      taskUuid = rawText.replace(/^"|"$/g, '');
    }
  } catch {
    taskUuid = rawText.replace(/^"|"$/g, '').trim();
  }

  if (!taskUuid) {
    console.error(`\n✗ No task_uuid in response: ${rawText}`);
    process.exit(1);
  }

  console.error(`  Task: ${taskUuid}`);
  console.error('→ Polling for result...');

  for (let attempt = 0; attempt < 90; attempt++) {
    await new Promise((r) => setTimeout(r, 2000));

    let pollRes;
    try {
      pollRes = await fetch(`https://api.talesofai.com/v1/artifact/task/${taskUuid}`, {
        method: 'GET',
        headers,
      });
    } catch (err) {
      console.error(`  poll error: ${err.message}`);
      continue;
    }

    if (!pollRes.ok) {
      console.error(`  poll failed (${pollRes.status})`);
      continue;
    }

    const data = await pollRes.json();
    const status = data.task_status;

    if (status === 'PENDING' || status === 'MODERATION') {
      continue;
    }

    let url = null;
    if (Array.isArray(data.artifacts) && data.artifacts.length > 0) {
      url = data.artifacts[0].url;
    }
    if (!url && data.result_image_url) {
      url = data.result_image_url;
    }

    if (url) {
      console.log(url);
      process.exit(0);
    }

    console.error(`\n✗ Task finished (status=${status}) but no image URL found.`);
    console.error(JSON.stringify(data, null, 2));
    process.exit(1);
  }

  console.error('\n✗ Timed out after 90 attempts (180s).');
  process.exit(1);
}

main().catch((err) => {
  console.error(`\n✗ Unexpected error: ${err.message}`);
  process.exit(1);
});
