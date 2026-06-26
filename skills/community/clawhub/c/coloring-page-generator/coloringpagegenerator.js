#!/usr/bin/env node
import https from 'https';

const args = process.argv.slice(2);

// Parse CLI arguments
let prompt = null;
let size = 'portrait';
let tokenFlag = null;
let refUuid = null;

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--token' && args[i + 1]) {
    tokenFlag = args[++i];
  } else if (args[i] === '--size' && args[i + 1]) {
    size = args[++i];
  } else if (args[i] === '--ref' && args[i + 1]) {
    refUuid = args[++i];
  } else if (!args[i].startsWith('--') && prompt === null) {
    prompt = args[i];
  }
}

const TOKEN = tokenFlag;

if (!TOKEN) {
  console.error('\n✗ Token required. Pass via: --token YOUR_TOKEN');
  console.error('  Get yours at: https://www.neta.art/open/');
  process.exit(1);
}

if (!prompt) {
  // Use default prompt if none provided
  prompt = 'black and white line art coloring page, clean outlines, no shading, no color fills, white background, detailed illustration suitable for coloring, bold clear lines, printable coloring book style';
}

const SIZES = {
  square:    { width: 1024, height: 1024 },
  portrait:  { width: 832,  height: 1216 },
  landscape: { width: 1216, height: 832  },
  tall:      { width: 704,  height: 1408 },
};

const { width, height } = SIZES[size] || SIZES.portrait;

const HEADERS = {
  'x-token': TOKEN,
  'x-platform': 'nieta-app/web',
  'content-type': 'application/json',
};

function request(method, url, body) {
  return new Promise((resolve, reject) => {
    const parsed = new URL(url);
    const options = {
      hostname: parsed.hostname,
      path: parsed.pathname + parsed.search,
      method,
      headers: {
        ...HEADERS,
        ...(body ? { 'content-length': Buffer.byteLength(JSON.stringify(body)) } : {}),
      },
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => (data += chunk));
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch {
          resolve(data);
        }
      });
    });

    req.on('error', reject);

    if (body) {
      req.write(JSON.stringify(body));
    }
    req.end();
  });
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function main() {
  const body = {
    storyId: 'DO_NOT_USE',
    jobType: 'universal',
    rawPrompt: [{ type: 'freetext', value: prompt, weight: 1 }],
    width,
    height,
    meta: { entrance: 'PICTURE,VERSE' },
    context_model_series: '8_image_edit',
  };

  if (refUuid) {
    body.inherit_params = {
      collection_uuid: refUuid,
      picture_uuid: refUuid,
    };
  }

  const makeRes = await request('POST', 'https://api.talesofai.com/v3/make_image', body);

  let taskUuid;
  if (typeof makeRes === 'string') {
    taskUuid = makeRes;
  } else {
    taskUuid = makeRes.task_uuid;
  }

  if (!taskUuid) {
    console.error('✗ Failed to get task UUID from API response:', JSON.stringify(makeRes));
    process.exit(1);
  }

  const pollUrl = `https://api.talesofai.com/v1/artifact/task/${taskUuid}`;
  const MAX_ATTEMPTS = 90;

  for (let i = 0; i < MAX_ATTEMPTS; i++) {
    await sleep(2000);

    const pollRes = await request('GET', pollUrl, null);

    const status = pollRes.task_status;
    if (status === 'PENDING' || status === 'MODERATION') {
      continue;
    }

    // Done
    const url =
      (pollRes.artifacts && pollRes.artifacts[0] && pollRes.artifacts[0].url) ||
      pollRes.result_image_url;

    if (!url) {
      console.error('✗ No image URL in response:', JSON.stringify(pollRes));
      process.exit(1);
    }

    console.log(url);
    process.exit(0);
  }

  console.error('✗ Timed out waiting for image generation.');
  process.exit(1);
}

main().catch((err) => {
  console.error('✗ Error:', err.message);
  process.exit(1);
});
