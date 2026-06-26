#!/usr/bin/env node
import process from 'node:process';

const DEFAULT_PROMPT = 'A haunting ghost portrait featuring a translucent spectral figure with ethereal mist, dark atmospheric shadows, dim moonlight, wispy smoke curling around the figure, pale glowing skin, empty hollow eyes, vintage gothic attire with tattered fabric, eerie fog rolling in the background, cinematic horror lighting, supernatural paranormal aesthetic, dramatic chiaroscuro, high contrast dark moody atmosphere, photorealistic spooky ghostly apparition';

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
    } else if (a.startsWith('--size=')) {
      size = a.slice('--size='.length);
    } else if (a.startsWith('--token=')) {
      tokenFlag = a.slice('--token='.length);
    } else if (a.startsWith('--ref=')) {
      ref = a.slice('--ref='.length);
    } else if (!prompt && !a.startsWith('--')) {
      prompt = a;
    }
  }

  return { prompt, size, tokenFlag, ref };
}

async function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function main() {
  const { prompt: promptArg, size, tokenFlag, ref } = parseArgs(process.argv);

  const TOKEN = tokenFlag;

  if (!TOKEN) {
    console.error('\n✗ Token required. Pass via: --token YOUR_TOKEN');
    console.error('  Get yours at: https://www.neta.art/open/');
    process.exit(1);
  }

  const PROMPT = promptArg || DEFAULT_PROMPT;
  const dims = SIZES[size] || SIZES.portrait;

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

  const submitBody = await submitRes.text();
  let taskUuid;
  try {
    const parsed = JSON.parse(submitBody);
    taskUuid = typeof parsed === 'string' ? parsed : parsed.task_uuid;
  } catch {
    taskUuid = submitBody.replace(/^"|"$/g, '').trim();
  }

  if (!taskUuid) {
    console.error('\n✗ No task_uuid in response');
    process.exit(1);
  }

  for (let i = 0; i < 90; i++) {
    await sleep(2000);
    const pollRes = await fetch(`https://api.talesofai.com/v1/artifact/task/${taskUuid}`, {
      method: 'GET',
      headers,
    });

    if (!pollRes.ok) {
      continue;
    }

    const data = await pollRes.json();
    const status = data.task_status;

    if (status === 'PENDING' || status === 'MODERATION') {
      continue;
    }

    const url =
      (Array.isArray(data.artifacts) && data.artifacts[0] && data.artifacts[0].url) ||
      data.result_image_url;

    if (url) {
      console.log(url);
      process.exit(0);
    }

    console.error(`\n✗ Task finished with status ${status} but no image URL`);
    process.exit(1);
  }

  console.error('\n✗ Timed out waiting for image');
  process.exit(1);
}

main().catch((err) => {
  console.error(`\n✗ ${err.message || err}`);
  process.exit(1);
});
