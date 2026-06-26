#!/usr/bin/env node
import { argv, exit, stdout } from 'node:process';

const DEFAULT_PROMPT = 'dark academia aesthetic, candlelit antique library, leather-bound books stacked on oak desk, vintage tweed and wool coat, autumn golden hour light through tall arched windows, classical marble bust, parchment papers, ink quill, moody chiaroscuro lighting, film grain, muted earth tones of brown burgundy and forest green, scholarly atmosphere, painterly cinematic composition';

const SIZES = {
  square: { width: 1024, height: 1024 },
  portrait: { width: 832, height: 1216 },
  landscape: { width: 1216, height: 832 },
  tall: { width: 704, height: 1408 },
};

function parseArgs(args) {
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

async function makeImage({ token, prompt, width, height, ref }) {
  const body = {
    storyId: 'DO_NOT_USE',
    jobType: 'universal',
    rawPrompt: [{ type: 'freetext', value: prompt, weight: 1 }],
    width,
    height,
    meta: { entrance: 'PICTURE,VERSE' },
    context_model_series: '8_image_edit',
  };

  if (ref) {
    body.inherit_params = { collection_uuid: ref, picture_uuid: ref };
  }

  const res = await fetch('https://api.talesofai.com/v3/make_image', {
    method: 'POST',
    headers: {
      'x-token': token,
      'x-platform': 'nieta-app/web',
      'content-type': 'application/json',
    },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`make_image failed: ${res.status} ${text}`);
  }

  const text = await res.text();
  let task_uuid;
  try {
    const json = JSON.parse(text);
    task_uuid = typeof json === 'string' ? json : json.task_uuid;
  } catch {
    task_uuid = text.replace(/^"|"$/g, '').trim();
  }

  if (!task_uuid) throw new Error(`No task_uuid in response: ${text}`);
  return task_uuid;
}

async function pollTask({ token, task_uuid }) {
  for (let attempt = 0; attempt < 90; attempt++) {
    await new Promise((r) => setTimeout(r, 2000));

    const res = await fetch(`https://api.talesofai.com/v1/artifact/task/${task_uuid}`, {
      headers: {
        'x-token': token,
        'x-platform': 'nieta-app/web',
        'content-type': 'application/json',
      },
    });

    if (!res.ok) continue;

    const data = await res.json();
    const status = data.task_status;

    if (status === 'PENDING' || status === 'MODERATION') continue;

    const url = data.artifacts?.[0]?.url || data.result_image_url;
    if (!url) throw new Error(`Task finished but no image URL: ${JSON.stringify(data)}`);
    return url;
  }
  throw new Error('Polling timed out after 90 attempts');
}

async function main() {
  const args = parseArgs(argv.slice(2));
  const PROMPT = args.prompt || DEFAULT_PROMPT;
  const TOKEN = args.tokenFlag;

  if (!TOKEN) {
    console.error('\n✗ Token required. Pass via: --token YOUR_TOKEN');
    console.error('  Get yours at: https://www.neta.art/open/');
    process.exit(1);
  }

  const dims = SIZES[args.size] || SIZES.portrait;

  const task_uuid = await makeImage({
    token: TOKEN,
    prompt: PROMPT,
    width: dims.width,
    height: dims.height,
    ref: args.ref,
  });

  const url = await pollTask({ token: TOKEN, task_uuid });
  stdout.write(url + '\n');
  exit(0);
}

main().catch((err) => {
  console.error(`\n✗ ${err.message}`);
  exit(1);
});
