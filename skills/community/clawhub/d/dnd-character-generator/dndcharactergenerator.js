#!/usr/bin/env node
import https from 'https';

const args = process.argv.slice(2);

const PROMPT = args.find(a => !a.startsWith('--')) ||
  'DnD fantasy character portrait, detailed armor and weapons, dramatic lighting, epic fantasy art style, highly detailed character design, tabletop RPG hero';

const tokenIndex = args.indexOf('--token');
const tokenFlag = tokenIndex !== -1 ? args[tokenIndex + 1] : null;

const sizeIndex = args.indexOf('--size');
const sizeArg = sizeIndex !== -1 ? args[sizeIndex + 1] : 'portrait';

const refIndex = args.indexOf('--ref');
const refArg = refIndex !== -1 ? args[refIndex + 1] : null;

const TOKEN = tokenFlag;

if (!TOKEN) {
  console.error('\n✗ Token required. Pass via: --token YOUR_TOKEN');
  console.error('  Get yours at: https://www.neta.art/open/');
  process.exit(1);
}

const SIZES = {
  square: { width: 1024, height: 1024 },
  portrait: { width: 832, height: 1216 },
  landscape: { width: 1216, height: 832 },
  tall: { width: 704, height: 1408 },
};

const { width, height } = SIZES[sizeArg] || SIZES.portrait;

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
      headers: { ...HEADERS },
    };
    if (body) {
      const data = JSON.stringify(body);
      options.headers['content-length'] = Buffer.byteLength(data);
      const req = https.request(options, res => {
        let raw = '';
        res.on('data', c => raw += c);
        res.on('end', () => {
          try { resolve(JSON.parse(raw)); } catch { resolve(raw); }
        });
      });
      req.on('error', reject);
      req.write(data);
      req.end();
    } else {
      const req = https.request(options, res => {
        let raw = '';
        res.on('data', c => raw += c);
        res.on('end', () => {
          try { resolve(JSON.parse(raw)); } catch { resolve(raw); }
        });
      });
      req.on('error', reject);
      req.end();
    }
  });
}

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function main() {
  const body = {
    storyId: 'DO_NOT_USE',
    jobType: 'universal',
    rawPrompt: [{ type: 'freetext', value: PROMPT, weight: 1 }],
    width,
    height,
    meta: { entrance: 'PICTURE,VERSE' },
    context_model_series: '8_image_edit',
  };

  if (refArg) {
    body.inherit_params = { collection_uuid: refArg, picture_uuid: refArg };
  }

  let taskUuid;
  const makeRes = await request('POST', 'https://api.talesofai.com/v3/make_image', body);

  if (typeof makeRes === 'string') {
    taskUuid = makeRes.trim();
  } else if (makeRes && makeRes.task_uuid) {
    taskUuid = makeRes.task_uuid;
  } else {
    console.error('✗ Unexpected response from make_image:', JSON.stringify(makeRes));
    process.exit(1);
  }

  console.error(`Generating... (task: ${taskUuid})`);

  for (let i = 0; i < 90; i++) {
    await sleep(2000);
    const poll = await request('GET', `https://api.talesofai.com/v1/artifact/task/${taskUuid}`);
    const status = poll && poll.task_status;

    if (status === 'PENDING' || status === 'MODERATION') {
      continue;
    }

    const url =
      (poll.artifacts && poll.artifacts[0] && poll.artifacts[0].url) ||
      poll.result_image_url;

    if (url) {
      console.log(url);
      process.exit(0);
    } else {
      console.error('✗ Task finished but no image URL found:', JSON.stringify(poll));
      process.exit(1);
    }
  }

  console.error('✗ Timed out waiting for image generation.');
  process.exit(1);
}

main().catch(err => {
  console.error('✗ Error:', err.message || err);
  process.exit(1);
});
