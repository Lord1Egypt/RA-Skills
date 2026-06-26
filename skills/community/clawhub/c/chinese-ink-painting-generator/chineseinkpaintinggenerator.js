#!/usr/bin/env node
import { argv, exit, stdout, stderr } from 'node:process';

const DEFAULT_PROMPT = "traditional Chinese ink painting (shui-mo hua), sumi-e brushwork, flowing black ink on rice paper, misty mountains and bamboo, minimalist negative space composition, delicate calligraphic strokes, soft gradient washes, serene oriental aesthetic, classic shan shui landscape style";

const SIZES = {
  square: { width: 1024, height: 1024 },
  portrait: { width: 832, height: 1216 },
  landscape: { width: 1216, height: 832 },
  tall: { width: 704, height: 1408 },
};

function parseArgs(args) {
  let prompt = null;
  let size = 'landscape';
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

async function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function main() {
  const { prompt, size, tokenFlag, ref } = parseArgs(argv.slice(2));

  const TOKEN = tokenFlag;

  if (!TOKEN) {
    console.error('\n✗ Token required. Pass via: --token YOUR_TOKEN');
    console.error('  Get yours at: https://www.neta.art/open/');
    process.exit(1);
  }

  const PROMPT = prompt || DEFAULT_PROMPT;

  const dims = SIZES[size];
  if (!dims) {
    stderr.write(`\n✗ Invalid size: ${size}. Must be one of: ${Object.keys(SIZES).join(', ')}\n`);
    exit(1);
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

  stderr.write(`Generating: "${PROMPT}"\n`);
  stderr.write(`Size: ${size} (${dims.width}x${dims.height})\n`);

  let submitRes;
  try {
    submitRes = await fetch('https://api.talesofai.com/v3/make_image', {
      method: 'POST',
      headers,
      body: JSON.stringify(body),
    });
  } catch (err) {
    stderr.write(`\n✗ Request failed: ${err.message}\n`);
    exit(1);
  }

  if (!submitRes.ok) {
    const text = await submitRes.text();
    stderr.write(`\n✗ API error ${submitRes.status}: ${text}\n`);
    exit(1);
  }

  const submitText = await submitRes.text();
  let taskUuid;
  try {
    const parsed = JSON.parse(submitText);
    taskUuid = typeof parsed === 'string' ? parsed : parsed.task_uuid;
  } catch {
    taskUuid = submitText.trim().replace(/^"|"$/g, '');
  }

  if (!taskUuid) {
    stderr.write(`\n✗ No task_uuid returned: ${submitText}\n`);
    exit(1);
  }

  stderr.write(`Task: ${taskUuid}\nPolling...\n`);

  for (let attempt = 0; attempt < 90; attempt++) {
    await sleep(2000);
    let pollRes;
    try {
      pollRes = await fetch(`https://api.talesofai.com/v1/artifact/task/${taskUuid}`, {
        headers,
      });
    } catch (err) {
      stderr.write(`  poll error: ${err.message}\n`);
      continue;
    }

    if (!pollRes.ok) {
      stderr.write(`  poll ${pollRes.status}\n`);
      continue;
    }

    const data = await pollRes.json();
    const status = data.task_status;

    if (status === 'PENDING' || status === 'MODERATION') {
      stderr.write(`  ${status}... (${attempt + 1}/90)\n`);
      continue;
    }

    const url = (data.artifacts && data.artifacts[0] && data.artifacts[0].url) || data.result_image_url;
    if (url) {
      stdout.write(url + '\n');
      exit(0);
    }

    stderr.write(`\n✗ Task ended with status "${status}" but no image URL.\n`);
    stderr.write(JSON.stringify(data, null, 2) + '\n');
    exit(1);
  }

  stderr.write('\n✗ Timed out after 90 attempts (~3 minutes).\n');
  exit(1);
}

main().catch((err) => {
  stderr.write(`\n✗ ${err.message}\n`);
  exit(1);
});
