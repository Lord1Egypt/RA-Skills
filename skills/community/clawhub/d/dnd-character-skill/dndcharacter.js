#!/usr/bin/env node

const args = process.argv.slice(2);

function getFlag(name) {
  const idx = args.indexOf(name);
  if (idx !== -1 && idx + 1 < args.length) return args[idx + 1];
  return null;
}

const prompt = args.find(a => !a.startsWith('--') && (args.indexOf(a) === 0 || !['--size', '--token', '--ref'].includes(args[args.indexOf(a) - 1])));
const sizeFlag = getFlag('--size') || 'portrait';
const tokenFlag = getFlag('--token');
const refFlag = getFlag('--ref');

const TOKEN = tokenFlag;

if (!TOKEN) {
  console.error('\n\u2717 Token required. Pass via: --token YOUR_TOKEN');
  console.error('  Get yours at: https://www.neta.art/open/');
  process.exit(1);
}

if (!prompt) {
  console.error('\n\u2717 Prompt required. Usage: node dndcharacter.js "your prompt" --token YOUR_TOKEN');
  process.exit(1);
}

const SIZES = {
  square: { width: 1024, height: 1024 },
  portrait: { width: 832, height: 1216 },
  landscape: { width: 1216, height: 832 },
  tall: { width: 704, height: 1408 },
};

const size = SIZES[sizeFlag];
if (!size) {
  console.error(`\n\u2717 Invalid size "${sizeFlag}". Choose: square, portrait, landscape, tall`);
  process.exit(1);
}

const HEADERS = {
  "x-token": TOKEN,
  "x-platform": "nieta-app/web",
  "content-type": "application/json",
};

async function createImage() {
  const body = {
    storyId: "DO_NOT_USE",
    jobType: "universal",
    rawPrompt: [{ type: "freetext", value: prompt, weight: 1 }],
    width: size.width,
    height: size.height,
    meta: { entrance: "PICTURE,VERSE" },
    context_model_series: "8_image_edit",
  };

  if (refFlag) {
    body.inherit_params = {
      collection_uuid: refFlag,
      picture_uuid: refFlag,
    };
  }

  const res = await fetch("https://api.talesofai.com/v3/make_image", {
    method: "POST",
    headers: HEADERS,
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const text = await res.text();
    console.error(`\n\u2717 Image creation failed (${res.status}): ${text}`);
    process.exit(1);
  }

  const data = await res.json().catch(() => null);
  let taskUuid;
  if (typeof data === 'string') {
    taskUuid = data;
  } else if (data && data.task_uuid) {
    taskUuid = data.task_uuid;
  } else {
    const text = await res.text().catch(() => '');
    taskUuid = text || data;
  }

  if (!taskUuid) {
    console.error('\n\u2717 No task UUID returned from API');
    process.exit(1);
  }

  return taskUuid;
}

async function pollResult(taskUuid) {
  const url = `https://api.talesofai.com/v1/artifact/task/${taskUuid}`;
  const MAX_ATTEMPTS = 90;
  const INTERVAL = 2000;

  for (let i = 0; i < MAX_ATTEMPTS; i++) {
    await new Promise(r => setTimeout(r, INTERVAL));

    const res = await fetch(url, { headers: HEADERS });
    if (!res.ok) continue;

    const data = await res.json();
    const status = data.task_status;

    if (status === 'PENDING' || status === 'MODERATION') continue;

    const imageUrl =
      (data.artifacts && data.artifacts[0] && data.artifacts[0].url) ||
      data.result_image_url;

    if (imageUrl) {
      console.log(imageUrl);
      process.exit(0);
    }

    console.error('\n\u2717 Task completed but no image URL found in response');
    process.exit(1);
  }

  console.error('\n\u2717 Timed out waiting for image generation');
  process.exit(1);
}

const taskUuid = await createImage();
await pollResult(taskUuid);
