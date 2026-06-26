#!/usr/bin/env node
import process from 'node:process';

const DEFAULT_PROMPT = 'baroque oil painting masterpiece, dramatic chiaroscuro lighting, rich golden and deep crimson color palette, ornate renaissance composition, painterly brushstrokes, opulent fabric textures, museum-quality classical portrait in the style of Caravaggio and Rembrandt, dramatic shadow play, gilded details';

const SIZES = {
  square: { width: 1024, height: 1024 },
  portrait: { width: 832, height: 1216 },
  landscape: { width: 1216, height: 832 },
  tall: { width: 704, height: 1408 },
};

function parseArgs(argv) {
  const args = { size: 'portrait', token: null, ref: null, prompt: null };
  const rest = [];
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--size') args.size = argv[++i];
    else if (a === '--token') args.token = argv[++i];
    else if (a === '--ref') args.ref = argv[++i];
    else rest.push(a);
  }
  if (rest.length > 0) args.prompt = rest.join(' ');
  return args;
}

async function main() {
  const { size, token: tokenFlag, ref, prompt } = parseArgs(process.argv.slice(2));

  const TOKEN = tokenFlag;
  if (!TOKEN) {
    console.error('\n✗ Token required. Pass via: --token YOUR_TOKEN');
    console.error('  Get yours at: https://www.neta.art/open/');
    process.exit(1);
  }

  const PROMPT = prompt || DEFAULT_PROMPT;
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

  console.error(`→ Submitting: "${PROMPT.slice(0, 80)}${PROMPT.length > 80 ? '…' : ''}"`);
  console.error(`  Size: ${size} (${dims.width}×${dims.height})`);

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

  console.error(`  Task: ${taskUuid}`);
  console.error('→ Polling…');

  for (let attempt = 0; attempt < 90; attempt++) {
    await new Promise((r) => setTimeout(r, 2000));
    const pollRes = await fetch(`https://api.talesofai.com/v1/artifact/task/${taskUuid}`, { headers });
    if (!pollRes.ok) continue;
    const data = await pollRes.json();
    const status = data.task_status;
    if (status === 'PENDING' || status === 'MODERATION') continue;
    const url = data.artifacts?.[0]?.url || data.result_image_url;
    if (url) {
      console.log(url);
      process.exit(0);
    }
    console.error(`✗ Task finished with status ${status} but no URL`);
    process.exit(1);
  }

  console.error('✗ Timed out after 90 attempts');
  process.exit(1);
}

main().catch((err) => {
  console.error('✗ Error:', err.message);
  process.exit(1);
});
