#!/usr/bin/env node
/**
 * FadNote CLI - Create secure self-destructing notes
 * Usage: fadnote [options] [text] or pipe content via stdin
 * Run with --help for full usage information
 */

import crypto from 'crypto';

const FADNOTE_URL = process.env.FADNOTE_URL || 'https://fadnote.com';
const MAX_SIZE = 1024 * 1024; // 1MB

function showHelp() {
  console.log(`
Usage: fadnote [options] [text]
       echo "text" | fadnote [options]

Create secure self-destructing notes that can only be viewed once.

Options:
  -h, --help          Show this help message and exit
      --ttl <secs>    Time until note expires (default: 86400 = 24h)
      --json          Output JSON with noteId, expiresIn, and decryptionUrl

Examples:
  fadnote "My secret message"
  echo "My secret" | fadnote
  fadnote --ttl 3600 "Expires in 1 hour"
  fadnote --json --ttl 7200 "JSON output"
  cat file.txt | fadnote --ttl 86400

Environment:
  FADNOTE_URL         API endpoint (default: https://fadnote.com)
`);
  process.exit(0);
}

function parseArgs() {
  const args = process.argv.slice(2);
  const options = { ttl: 86400, json: false, content: '', help: false };
  const contentArgs = [];

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '-h' || args[i] === '--help') {
      options.help = true;
    } else if (args[i] === '--ttl' && i + 1 < args.length) {
      const ttl = parseInt(args[i + 1], 10);
      if (isNaN(ttl) || ttl <= 0) {
        throw new Error('Invalid TTL: must be a positive number');
      }
      options.ttl = ttl;
      i++;
    } else if (args[i] === '--json') {
      options.json = true;
    } else {
      contentArgs.push(args[i]);
    }
  }

  options.content = contentArgs.join(' ');
  return options;
}

async function readInput() {
  const args = parseArgs();

  if (args.help) {
    showHelp();
  }

  if (args.content) {
    return args;
  }

  const content = await new Promise((resolve, reject) => {
    let data = '';
    process.stdin.setEncoding('utf8');
    process.stdin.on('data', chunk => data += chunk);
    process.stdin.on('end', () => resolve(data.trim()));
    process.stdin.on('error', reject);
  });

  return { ...args, content };
}

function encrypt(content) {
  const key = crypto.randomBytes(32).toString('base64url');
  const salt = crypto.randomBytes(16);
  const iv = crypto.randomBytes(12);

  const derived = crypto.pbkdf2Sync(Buffer.from(key), salt, 600000, 32, 'sha256');
  const cipher = crypto.createCipheriv('aes-256-gcm', derived, iv);

  const encrypted = Buffer.concat([cipher.update(content, 'utf8'), cipher.final()]);
  const authTag = cipher.getAuthTag();

  return {
    blob: Buffer.from(JSON.stringify({
      ciphertext: Buffer.concat([encrypted, authTag]).toString('base64'),
      iv: iv.toString('base64'),
      salt: salt.toString('base64')
    })),
    key
  };
}

async function post(blob, ttl) {
  const res = await fetch(`${FADNOTE_URL}/n`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/octet-stream',
      'X-Note-TTL': String(ttl),
      'Content-Length': String(blob.length)
    },
    body: blob
  });
  const data = await res.text();
  if (res.status === 201) return JSON.parse(data);
  throw new Error(`HTTP ${res.status}: ${data}`);
}

async function main() {
  try {
    const { content, ttl, json } = await readInput();
    if (!content) throw new Error('Content is empty');
    if (Buffer.byteLength(content, 'utf8') > MAX_SIZE) throw new Error('Content exceeds 1MB limit');

    const { blob, key } = encrypt(content);
    const result = await post(blob, ttl);
    const decryptionUrl = `${FADNOTE_URL}/n/${result.id}#${key}`;

    if (json) {
      console.log(JSON.stringify({
        noteId: result.id,
        expiresIn: result.expiresIn,
        decryptionUrl
      }));
    } else {
      console.log(decryptionUrl);
    }
  } catch (err) {
    console.error(`Error: ${err.message}`);
    process.exit(1);
  }
}

main();
