#!/usr/bin/env node
// Usage: node scripts/feishu-send-image.mjs <target> <image_path>
// target: "user:open_id_xxx" or "oc_xxx" (chat_id)

import { readFileSync, writeFileSync, existsSync } from 'fs';
import { resolve } from 'path';
import { homedir } from 'os';

const API = 'https://open.feishu.cn/open-apis';
// Secure token cache: user-private directory instead of world-readable /tmp
const CACHE_DIR = resolve(homedir(), '.cache/agent-memes');
const TOKEN_CACHE = resolve(CACHE_DIR, 'feishu-token.json');

const [target, imagePath] = process.argv.slice(2);
if (!target || !imagePath) {
  console.error('Usage: node scripts/feishu-send-image.mjs <target> <image_path>');
  process.exit(1);
}

// --- credentials via centralized helper ---
import { execSync } from 'child_process';
import { mkdirSync } from 'fs';

let appId = process.env.FEISHU_APP_ID;
let appSecret = process.env.FEISHU_APP_SECRET;

if (!appId || !appSecret) {
  try {
    const helperPath = resolve(import.meta.dirname || new URL('.', import.meta.url).pathname, 'get-credential.sh');
    const creds = execSync(`bash "${helperPath}" feishu`, { encoding: 'utf8' }).trim();
    const parts = creds.split(' ');
    appId = parts[0];
    appSecret = parts[1];
  } catch {}
}
if (!appId || !appSecret) {
  console.error('Missing credentials. Set FEISHU_APP_ID + FEISHU_APP_SECRET env vars, or configure ~/.openclaw/openclaw.json');
  process.exit(1);
}

// Ensure secure cache directory exists (0700)
try { mkdirSync(CACHE_DIR, { recursive: true, mode: 0o700 }); } catch {}

// --- tenant_access_token (cached) ---
async function getToken() {
  if (existsSync(TOKEN_CACHE)) {
    try {
      const cached = JSON.parse(readFileSync(TOKEN_CACHE, 'utf8'));
      if (cached.token && cached.expiresAt > Date.now() + 60_000) return cached.token;
    } catch {}
  }
  const res = await fetch(`${API}/auth/v3/tenant_access_token/internal`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ app_id: appId, app_secret: appSecret }),
  });
  const data = await res.json();
  if (data.code !== 0) throw new Error(`token error: ${data.msg}`);
  const token = data.tenant_access_token;
  writeFileSync(TOKEN_CACHE, JSON.stringify({ token, expiresAt: Date.now() + data.expire * 1000 }));
  return token;
}

// --- upload image ---
async function uploadImage(token, filePath) {
  const absPath = resolve(filePath);
  const bytes = readFileSync(absPath);
  const blob = new Blob([bytes]);
  const form = new FormData();
  form.append('image_type', 'message');
  form.append('image', blob, absPath.split('/').pop());
  const res = await fetch(`${API}/im/v1/images`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}` },
    body: form,
  });
  const data = await res.json();
  if (data.code !== 0) throw new Error(`upload error: ${data.code} ${data.msg}`);
  return data.data.image_key;
}

// --- send message ---
async function sendImage(token, target, imageKey) {
  let receiveIdType, receiveId;
  if (target.startsWith('user:')) {
    receiveIdType = 'open_id';
    receiveId = target.slice(5);
  } else {
    receiveIdType = 'chat_id';
    receiveId = target;
  }
  const res = await fetch(`${API}/im/v1/messages?receive_id_type=${receiveIdType}`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ receive_id: receiveId, msg_type: 'image', content: JSON.stringify({ image_key: imageKey }) }),
  });
  const data = await res.json();
  if (data.code !== 0) throw new Error(`send error: ${data.code} ${data.msg}`);
  return data.data.message_id;
}

// --- main ---
try {
  const token = await getToken();
  console.log('token ok');
  const imageKey = await uploadImage(token, imagePath);
  console.log('uploaded:', imageKey);
  const msgId = await sendImage(token, target, imageKey);
  console.log('sent:', msgId);
} catch (e) {
  console.error(e.message);
  process.exit(1);
}
