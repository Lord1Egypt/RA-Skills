#!/usr/bin/env node
import process from 'node:process';

const DEFAULT_PROMPT = "dark fantasy art, ominous moody atmosphere, volumetric fog, dramatic chiaroscuro lighting, intricate gothic detail, ancient ruins and eldritch creatures, painterly oil texture, desaturated palette with deep crimson and cold blue accents, grimdark epic cinematic composition";

const SIZES = {
  square:    { width: 1024, height: 1024 },
  portrait:  { width: 832,  height: 1216 },
  landscape: { width: 1216, height: 832  },
  tall:      { width: 704,  height: 1408 },
};

function parseArgs(argv) {
  const args = { size: 'portrait', token: null, ref: null, prompt: null };
  const positional = [];
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--size') args.size = argv[++i];
    else if (a === '--token') args.token = argv[++i];
    else if (a === '--ref') args.ref = argv[++i];
    else positional.push(a);
  }
  if (positional.length > 0) args.prompt = positional.join(' ');
  return args;
}

async function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

async function main() {
  const argv = process.argv.slice(2);
  const { size, token: tokenFlag, ref, prompt: promptArg } = parseArgs(argv);

  const PROMPT = promptArg && promptArg.trim().length > 0 ? promptArg : DEFAULT_PROMPT;
  const TOKEN = tokenFlag;

  if (!TOKEN) {
    console.error('\n✗ Token required. Pass via: --token YOUR_TOKEN');
    console.error('  Get yours at: https://www.neta.art/open/');
    process.exit(1);
  }

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

  const createRes = await fetch('https://api.talesofai.com/v3/make_image', {
    method: 'POST',
    headers,
    body: JSON.stringify(body),
  });

  if (!createRes.ok) {
    const text = await createRes.text();
    console.error(`\n✗ Failed to create task: ${createRes.status} ${createRes.statusText}`);
    console.error(text);
    process.exit(1);
  }

  const createText = await createRes.text();
  let taskUuid;
  try {
    const parsed = JSON.parse(createText);
    taskUuid = typeof parsed === 'string' ? parsed : parsed.task_uuid;
  } catch {
    taskUuid = createText.replace(/^"|"$/g, '').trim();
  }

  if (!taskUuid) {
    console.error('\n✗ No task_uuid returned from server.');
    console.error(createText);
    process.exit(1);
  }

  for (let attempt = 0; attempt < 90; attempt++) {
    await sleep(2000);
    const pollRes = await fetch(`https://api.talesofai.com/v1/artifact/task/${taskUuid}`, {
      method: 'GET',
      headers,
    });
    if (!pollRes.ok) continue;
    const data = await pollRes.json();
    const status = data.task_status;
    if (status === 'PENDING' || status === 'MODERATION') continue;

    let url = null;
    if (Array.isArray(data.artifacts) && data.artifacts[0]?.url) {
      url = data.artifacts[0].url;
    } else if (data.result_image_url) {
      url = data.result_image_url;
    }

    if (url) {
      console.log(url);
      process.exit(0);
    }

    console.error(`\n✗ Task finished with status "${status}" but no image URL.`);
    console.error(JSON.stringify(data, null, 2));
    process.exit(1);
  }

  console.error('\n✗ Timed out waiting for image generation.');
  process.exit(1);
}

main().catch((err) => {
  console.error(`\n✗ ${err.message || err}`);
  process.exit(1);
});
