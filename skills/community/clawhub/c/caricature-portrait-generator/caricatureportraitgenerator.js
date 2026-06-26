#!/usr/bin/env node
import https from 'https';

const args = process.argv.slice(2);

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
  prompt = 'caricature portrait with exaggerated facial features, comically enlarged eyes and expression, bold linework, professional caricature art style, vibrant colors, humorous likeness';
}

const sizes = {
  square: [1024, 1024],
  portrait: [832, 1216],
  landscape: [1216, 832],
  tall: [704, 1408],
};

const [width, height] = sizes[size] || sizes.portrait;

const headers = {
  'x-token': TOKEN,
  'x-platform': 'nieta-app/web',
  'content-type': 'application/json',
};

function request(method, hostname, path, body) {
  return new Promise((resolve, reject) => {
    const data = body ? JSON.stringify(body) : null;
    const options = {
      hostname,
      path,
      method,
      headers: {
        ...headers,
        ...(data ? { 'content-length': Buffer.byteLength(data) } : {}),
      },
    };
    const req = https.request(options, (res) => {
      let raw = '';
      res.on('data', (chunk) => (raw += chunk));
      res.on('end', () => {
        try {
          resolve(JSON.parse(raw));
        } catch {
          resolve(raw.trim());
        }
      });
    });
    req.on('error', reject);
    if (data) req.write(data);
    req.end();
  });
}

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
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
    body.inherit_params = { collection_uuid: refUuid, picture_uuid: refUuid };
  }

  const createRes = await request('POST', 'api.talesofai.com', '/v3/make_image', body);

  let taskUuid;
  if (typeof createRes === 'string') {
    taskUuid = createRes;
  } else if (createRes && createRes.task_uuid) {
    taskUuid = createRes.task_uuid;
  } else {
    console.error('✗ Unexpected response from image creation:', JSON.stringify(createRes));
    process.exit(1);
  }

  const maxAttempts = 90;
  for (let i = 0; i < maxAttempts; i++) {
    await sleep(2000);
    const pollRes = await request('GET', 'api.talesofai.com', `/v1/artifact/task/${taskUuid}`, null);

    const status = pollRes && pollRes.task_status;
    if (status === 'PENDING' || status === 'MODERATION') {
      continue;
    }

    const url =
      (pollRes.artifacts && pollRes.artifacts[0] && pollRes.artifacts[0].url) ||
      pollRes.result_image_url;

    if (url) {
      console.log(url);
      process.exit(0);
    } else {
      console.error('✗ Generation finished but no image URL found:', JSON.stringify(pollRes));
      process.exit(1);
    }
  }

  console.error('✗ Timed out waiting for image generation.');
  process.exit(1);
}

main().catch((err) => {
  console.error('✗ Error:', err.message || err);
  process.exit(1);
});
