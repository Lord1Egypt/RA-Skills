#!/usr/bin/env node
import process from 'node:process';

const DEFAULT_PROMPT = '1990s anime art style, retro OVA aesthetic, flat cel-shaded colors, vintage analog film grain, hand-drawn line art, soft pastel palette, nostalgic shoujo/seinen composition, expressive eyes, dramatic lighting, classic Japanese animation';

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
    else args._.push(a);
  }
  return args;
}

const argv = parseArgs(process.argv.slice(2));
const userPrompt = argv._[0];
const sizeKey = argv.size || 'portrait';
const tokenFlag = argv.token;
const refUuid = argv.ref;

const TOKEN = tokenFlag;

if (!TOKEN) {
  console.error('\n✗ Token required. Pass via: --token YOUR_TOKEN');
  console.error('  Get yours at: https://www.neta.art/open/');
  process.exit(1);
}

const size = SIZES[sizeKey];
if (!size) {
  console.error(`\n✗ Invalid size: ${sizeKey}. Use one of: ${Object.keys(SIZES).join(', ')}`);
  process.exit(1);
}

const PROMPT = userPrompt
  ? `${DEFAULT_PROMPT}, ${userPrompt}`
  : DEFAULT_PROMPT;

const HEADERS = {
  'x-token': TOKEN,
  'x-platform': 'nieta-app/web',
  'content-type': 'application/json',
};

async function createTask() {
  const body = {
    storyId: 'DO_NOT_USE',
    jobType: 'universal',
    rawPrompt: [{ type: 'freetext', value: PROMPT, weight: 1 }],
    width: size.width,
    height: size.height,
    meta: { entrance: 'PICTURE,VERSE' },
    context_model_series: '8_image_edit',
  };

  if (refUuid) {
    body.inherit_params = {
      collection_uuid: refUuid,
      picture_uuid: refUuid,
    };
  }

  const res = await fetch('https://api.talesofai.com/v3/make_image', {
    method: 'POST',
    headers: HEADERS,
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`make_image failed: ${res.status} ${res.statusText} — ${text}`);
  }

  const text = await res.text();
  let taskUuid;
  try {
    const json = JSON.parse(text);
    taskUuid = typeof json === 'string' ? json : json.task_uuid;
  } catch {
    taskUuid = text.replace(/^"|"$/g, '').trim();
  }

  if (!taskUuid) {
    throw new Error(`No task_uuid in response: ${text}`);
  }

  return taskUuid;
}

async function pollTask(taskUuid) {
  const url = `https://api.talesofai.com/v1/artifact/task/${taskUuid}`;
  for (let attempt = 0; attempt < 90; attempt++) {
    await new Promise((r) => setTimeout(r, 2000));
    const res = await fetch(url, { headers: HEADERS });
    if (!res.ok) continue;
    const data = await res.json();
    const status = data.task_status;
    if (status === 'PENDING' || status === 'MODERATION') continue;

    const imageUrl =
      (data.artifacts && data.artifacts[0] && data.artifacts[0].url) ||
      data.result_image_url;
    if (imageUrl) return imageUrl;

    throw new Error(`Task finished without image URL: ${JSON.stringify(data)}`);
  }
  throw new Error('Timed out waiting for image generation.');
}

(async () => {
  try {
    const taskUuid = await createTask();
    const imageUrl = await pollTask(taskUuid);
    console.log(imageUrl);
    process.exit(0);
  } catch (err) {
    console.error(`\n✗ ${err.message}`);
    process.exit(1);
  }
})();
