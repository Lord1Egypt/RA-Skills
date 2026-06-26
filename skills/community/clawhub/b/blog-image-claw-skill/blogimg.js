#!/usr/bin/env node
/**
 * blogimg.js — Blog Image API helper (zero dependencies)
 *
 * The agent reads blog content, builds visual prompts, then calls this script.
 *
 * Commands:
 *   node blogimg.js gen <prompt> [--size header|inline]
 *       → {status, url, task_uuid, width, height}
 *
 * Sizes:
 *   header  1024×576  (16:9) — hero / OG image
 *   inline  1024×576  (16:9) — in-article image (same ratio, agent may vary)
 *
 */

import { homedir }      from 'node:os';
import { resolve }      from 'node:path';

const BASE = 'https://api.talesofai.com';

function getToken() {
  const idx = process.argv.indexOf('--token');
  if (idx !== -1 && process.argv[idx + 1]) return process.argv[idx + 1];
  throw new Error('Token required. Pass via: --token YOUR_TOKEN');
}

const HEADERS = {
  'x-token': getToken(),
  'x-platform': 'nieta-app/web',
  'content-type': 'application/json',
};

async function api(method, path, body) {
  const res = await fetch(BASE + path, { method, headers: HEADERS, ...(body ? { body: JSON.stringify(body) } : {}) });
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
  return res.json();
}

const log = msg => process.stderr.write(msg + '\n');
const out = data => console.log(JSON.stringify(data));

function parseFlags(args) {
  const flags = { _: [] };
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--')) {
      const key = args[i].slice(2);
      const val = args[i + 1] && !args[i + 1].startsWith('--') ? args[++i] : true;
      flags[key] = val;
    } else { flags._.push(args[i]); }
  }
  return flags;
}

const SIZES = {
  header: { width: 1024, height: 576  },
  inline: { width: 1024, height: 576  },
};

const [,, cmd, ...rawArgs] = process.argv;

if (cmd === 'gen') {
  const flags  = parseFlags(rawArgs);
  const prompt = flags._.join(' ');
  const size   = SIZES[flags.size] ?? SIZES.header;

  if (!prompt) throw new Error('Usage: blogimg.js gen <prompt> [--size header|inline]');

  log(`🖼️  Generating ${flags.size ?? 'header'} image...`);

  const taskUuid = await api('POST', '/v3/make_image', {
    storyId: 'DO_NOT_USE',
    jobType: 'universal',
    rawPrompt: [{ type: 'freetext', value: prompt, weight: 1 }],
    width: size.width,
    height: size.height,
    meta: { entrance: 'PICTURE' },
  });

  const task_uuid = typeof taskUuid === 'string' ? taskUuid : taskUuid?.task_uuid;
  log(`⏳ Task: ${task_uuid}`);

  let warnedSlow = false;
  for (let i = 0; i < 90; i++) {
    await new Promise(r => setTimeout(r, 2000));
    if (!warnedSlow && i >= 14) { log('⏳ Still rendering...'); warnedSlow = true; }
    const result = await api('GET', `/v1/artifact/task/${task_uuid}`);
    if (result.task_status !== 'PENDING' && result.task_status !== 'MODERATION') {
      out({ status: result.task_status, url: result.artifacts?.[0]?.url ?? null, task_uuid, ...size });
      process.exit(0);
    }
  }
  out({ status: 'TIMEOUT', url: null, task_uuid, ...size });
}

else {
  process.stderr.write('Usage: node blogimg.js gen <prompt> [--size header|inline]\n');
  process.exit(1);
}
