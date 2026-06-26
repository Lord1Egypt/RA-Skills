#!/usr/bin/env node

'use strict';

const https = require('https');
const fs = require('fs');
const path = require('path');
const os = require('os');

const BASE_URL = 'postmoo.re';
const BASE_PATH = '/api/v1';

// ---------------------------------------------------------------------------
// Config
// ---------------------------------------------------------------------------

function getConfigPaths() {
  return {
    local: path.join(process.cwd(), '.postmoore', 'config.json'),
    global: path.join(os.homedir(), '.config', 'postmoore', 'config.json'),
  };
}

function loadApiKey() {
  if (process.env.POSTMOORE_API_KEY) return process.env.POSTMOORE_API_KEY;

  const { local, global: globalPath } = getConfigPaths();
  for (const p of [local, globalPath]) {
    if (fs.existsSync(p)) {
      try {
        const cfg = JSON.parse(fs.readFileSync(p, 'utf8'));
        if (cfg.key) return cfg.key;
      } catch (_) {}
    }
  }
  return null;
}

function requireApiKey() {
  const key = loadApiKey();
  if (!key) {
    error(
      'No API key found. Run: postmoore setup --key pm_live_...\n' +
      '  Get your key at https://postmoo.re'
    );
  }
  return key;
}

// ---------------------------------------------------------------------------
// HTTP
// ---------------------------------------------------------------------------

function request(method, endpoint, body, key) {
  return new Promise((resolve, reject) => {
    const data = body ? JSON.stringify(body) : null;

    const options = {
      hostname: BASE_URL,
      path: BASE_PATH + endpoint,
      method,
      headers: {
        Authorization: `Bearer ${key}`,
        'Content-Type': 'application/json',
        ...(data ? { 'Content-Length': Buffer.byteLength(data) } : {}),
      },
    };

    const req = https.request(options, (res) => {
      let raw = '';
      res.on('data', (chunk) => (raw += chunk));
      res.on('end', () => {
        try {
          resolve({ status: res.statusCode, body: JSON.parse(raw) });
        } catch (_) {
          resolve({ status: res.statusCode, body: raw });
        }
      });
    });

    req.on('error', reject);
    if (data) req.write(data);
    req.end();
  });
}

function uploadFile(filePath, key) {
  return new Promise((resolve, reject) => {
    if (!fs.existsSync(filePath)) {
      return reject(new Error(`File not found: ${filePath}`));
    }

    const fileData = fs.readFileSync(filePath);
    const fileName = path.basename(filePath);
    const boundary = `----PostmooreBoundary${Date.now()}`;

    const header = Buffer.from(
      `--${boundary}\r\n` +
      `Content-Disposition: form-data; name="file"; filename="${fileName}"\r\n` +
      `Content-Type: application/octet-stream\r\n\r\n`
    );
    const footer = Buffer.from(`\r\n--${boundary}--\r\n`);
    const body = Buffer.concat([header, fileData, footer]);

    const options = {
      hostname: BASE_URL,
      path: `${BASE_PATH}/media`,
      method: 'POST',
      headers: {
        Authorization: `Bearer ${key}`,
        'Content-Type': `multipart/form-data; boundary=${boundary}`,
        'Content-Length': body.length,
      },
    };

    const req = https.request(options, (res) => {
      let raw = '';
      res.on('data', (chunk) => (raw += chunk));
      res.on('end', () => {
        try {
          resolve({ status: res.statusCode, body: JSON.parse(raw) });
        } catch (_) {
          resolve({ status: res.statusCode, body: raw });
        }
      });
    });

    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

// ---------------------------------------------------------------------------
// Output
// ---------------------------------------------------------------------------

function out(data) {
  console.log(JSON.stringify(data, null, 2));
}

function error(msg) {
  console.error(`\x1b[31mError: ${msg}\x1b[0m`);
  process.exit(1);
}

// ---------------------------------------------------------------------------
// Arg parsing
// ---------------------------------------------------------------------------

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    if (argv[i].startsWith('--')) {
      const key = argv[i].slice(2);
      const next = argv[i + 1];
      if (next !== undefined && !next.startsWith('--')) {
        args[key] = next;
        i++;
      } else {
        args[key] = true;
      }
    } else {
      args._.push(argv[i]);
    }
  }
  return args;
}

// ---------------------------------------------------------------------------
// Commands
// ---------------------------------------------------------------------------

async function cmdSetup(args) {
  const key = args.key;
  if (!key || typeof key !== 'string' || !key.startsWith('pm_live_')) {
    error('--key must be a valid pm_live_... API key');
  }

  const { local, global: globalPath } = getConfigPaths();
  const targetPath = args.local ? local : globalPath;
  const dir = path.dirname(targetPath);

  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(targetPath, JSON.stringify({ key }, null, 2));

  out({ ok: true, stored: targetPath });
}

async function cmdAccounts() {
  const key = requireApiKey();
  const res = await request('GET', '/accounts', null, key);
  out(res.body);
}

async function cmdPost(args) {
  const key = requireApiKey();

  if (!args.accounts) error('--accounts is required (comma-separated IDs)');

  const accounts = String(args.accounts).split(',').map((s) => s.trim());
  const hasMedia = !!args.media;
  const contentType = hasMedia ? 'media' : 'text';

  if (contentType === 'text' && !args.text) {
    error('--text is required for text posts');
  }

  const body = {
    contentType,
    accounts,
    ...(args.text ? { text: args.text } : {}),
    ...(hasMedia
      ? { media: String(args.media).split(',').map((s) => s.trim()) }
      : {}),
    ...(args.schedule ? { schedule: args.schedule } : {}),
    ...(args.draft ? { draft: true } : {}),
  };

  const res = await request('POST', '/posts', body, key);
  out(res.body);
}

async function cmdPosts(args) {
  const key = requireApiKey();
  const qs = args.status ? `?status=${encodeURIComponent(args.status)}` : '';
  const res = await request('GET', `/posts${qs}`, null, key);
  out(res.body);
}

async function cmdPostsGet(args) {
  const key = requireApiKey();
  if (!args.id) error('--id is required');
  const res = await request('GET', `/posts/${encodeURIComponent(args.id)}`, null, key);
  out(res.body);
}

async function cmdPostsDelete(args) {
  const key = requireApiKey();
  if (!args.id) error('--id is required');
  const res = await request('DELETE', `/posts/${encodeURIComponent(args.id)}`, null, key);
  out(res.body);
}

async function cmdUpload(args) {
  const key = requireApiKey();
  if (!args.file) error('--file is required');
  const res = await uploadFile(args.file, key);
  out(res.body);
}

function cmdHelp() {
  out({
    usage: 'postmoore <command> [options]',
    commands: {
      'setup --key pm_live_... [--local]':
        'Store API key globally (~/.config/postmoore/config.json) or locally (.postmoore/config.json)',
      'accounts':
        'List all connected social accounts',
      'post --text "..." --accounts 1,2 [--schedule ISO8601] [--draft] [--media id1,id2]':
        'Create a post (text or media)',
      'posts [--status pending|scheduled|published|draft]':
        'List posts, optionally filtered by status',
      'posts:get --id X':
        'Get a single post by ID',
      'posts:delete --id X':
        'Delete a post by ID',
      'upload --file ./path':
        'Upload a media file, returns media ID',
      'help':
        'Show this help',
    },
    env: 'POSTMOORE_API_KEY — alternative to running setup',
    signup: 'https://postmoo.re',
  });
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

const COMMANDS = {
  setup: cmdSetup,
  accounts: cmdAccounts,
  post: cmdPost,
  posts: cmdPosts,
  'posts:get': cmdPostsGet,
  'posts:delete': cmdPostsDelete,
  upload: cmdUpload,
  help: cmdHelp,
};

async function main() {
  const [, , cmd, ...rest] = process.argv;
  const args = parseArgs(rest);

  if (!cmd || cmd === 'help') {
    cmdHelp();
    return;
  }

  const fn = COMMANDS[cmd];
  if (!fn) {
    error(`Unknown command: "${cmd}". Run 'postmoore help' for usage.`);
  }

  try {
    await fn(args);
  } catch (err) {
    error(err.message);
  }
}

main();
