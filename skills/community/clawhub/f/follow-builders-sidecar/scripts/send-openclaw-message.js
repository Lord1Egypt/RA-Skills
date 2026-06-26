#!/usr/bin/env node

import { access, readFile } from 'fs/promises';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';
import { promisify } from 'util';
import { execFile } from 'child_process';

import { log } from './sidecar-common.js';
import { renderDigestText } from './render-openclaw-digest.js';

const execFileAsync = promisify(execFile);
const DEFAULT_CHUNK_SIZE = 3200;
const OPENCLAW_CANDIDATES = [...new Set([
  process.env.OPENCLAW_BIN,
  '/opt/homebrew/bin/openclaw',
  join(dirname(process.execPath), 'openclaw'),
  'openclaw'
].filter(Boolean))];

async function resolveOpenClawBin() {
  for (const candidate of OPENCLAW_CANDIDATES) {
    if (candidate === 'openclaw') {
      return candidate;
    }
    try {
      await access(candidate);
      return candidate;
    } catch {
      // try next candidate
    }
  }
  return 'openclaw';
}

function parseArgs(argv) {
  const args = argv.slice(2);
  const parsed = {
    file: null,
    channel: null,
    to: null,
    accountId: null,
    chunkSize: DEFAULT_CHUNK_SIZE
  };

  for (let index = 0; index < args.length; index += 1) {
    const arg = args[index];
    switch (arg) {
      case '--file':
        parsed.file = args[++index];
        break;
      case '--channel':
        parsed.channel = args[++index];
        break;
      case '--to':
        parsed.to = args[++index];
        break;
      case '--account':
        parsed.accountId = args[++index];
        break;
      case '--chunk-size':
        parsed.chunkSize = Number(args[++index]) || DEFAULT_CHUNK_SIZE;
        break;
      default:
        throw new Error(`Unknown argument: ${arg}`);
    }
  }

  if (!parsed.file) {
    throw new Error('Missing required argument: --file');
  }
  if (!parsed.channel || !parsed.to) {
    throw new Error('Missing required arguments: --channel and --to');
  }

  return parsed;
}

function splitMessage(text, maxChars = DEFAULT_CHUNK_SIZE) {
  const paragraphs = String(text || '').trim().split(/\n{2,}/).filter(Boolean);
  const chunks = [];
  let current = '';

  function pushCurrent() {
    if (current.trim()) {
      chunks.push(current.trim());
      current = '';
    }
  }

  for (const paragraph of paragraphs) {
    if (paragraph.length > maxChars) {
      pushCurrent();
      let remaining = paragraph;
      while (remaining.length > maxChars) {
        const splitAt = Math.max(remaining.lastIndexOf('\n', maxChars), remaining.lastIndexOf(' ', maxChars), maxChars);
        chunks.push(remaining.slice(0, splitAt).trim());
        remaining = remaining.slice(splitAt).trim();
      }
      if (remaining) {
        current = remaining;
      }
      continue;
    }

    const candidate = current ? `${current}\n\n${paragraph}` : paragraph;
    if (candidate.length > maxChars) {
      pushCurrent();
      current = paragraph;
    } else {
      current = candidate;
    }
  }

  pushCurrent();
  return chunks.length > 0 ? chunks : [''];
}

async function sendTextChunk(text, options) {
  const args = [
    'message',
    'send',
    '--channel',
    options.channel,
    '--target',
    options.to,
    '--message',
    text,
    '--json'
  ];

  if (options.accountId) {
    args.push('--account', options.accountId);
  }

  const openclawBin = await resolveOpenClawBin();
  const { stdout } = await execFileAsync(openclawBin, args, {
    maxBuffer: 16 * 1024 * 1024
  });

  return JSON.parse(stdout);
}

async function sendTextThroughOpenClaw(text, options) {
  const chunks = splitMessage(text, options.chunkSize);
  const results = [];

  for (let index = 0; index < chunks.length; index += 1) {
    const chunk = chunks.length === 1
      ? chunks[index]
      : `(${index + 1}/${chunks.length})\n\n${chunks[index]}`;
    results.push(await sendTextChunk(chunk, options));
  }

  return {
    status: 'ok',
    chunks: chunks.length,
    results
  };
}

async function sendDigestPayloadThroughOpenClaw(payload, options) {
  if (!options?.channel || !options?.to) {
    throw new Error('OpenClaw delivery is missing channel or target');
  }
  const text = renderDigestText(payload);
  log('info', 'Sending digest through OpenClaw channel', {
    channel: options.channel,
    to: options.to,
    accountId: options.accountId || null,
    chars: text.length
  });
  return sendTextThroughOpenClaw(text, options);
}

async function main() {
  const args = parseArgs(process.argv);
  const payload = JSON.parse(await readFile(args.file, 'utf-8'));
  const result = await sendDigestPayloadThroughOpenClaw(payload, {
    channel: args.channel,
    to: args.to,
    accountId: args.accountId,
    chunkSize: args.chunkSize
  });
  process.stdout.write(`${JSON.stringify(result)}\n`);
}

export {
  sendDigestPayloadThroughOpenClaw,
  sendTextThroughOpenClaw
};

const IS_ENTRYPOINT = process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1];

if (IS_ENTRYPOINT) {
  main().catch((error) => {
    log('error', 'OpenClaw message delivery failed', {
      error: error.message,
      stack: error.stack
    });
    process.exit(1);
  });
}
