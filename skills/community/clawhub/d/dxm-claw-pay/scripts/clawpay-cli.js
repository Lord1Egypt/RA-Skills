#!/usr/bin/env node
'use strict';

const crypto = require('crypto');
const fs     = require('fs');
const os     = require('os');
const path   = require('path');
const http   = require('http');
const https  = require('https');
const zlib = require('zlib');

const CONFIG_PATH = path.join(__dirname, 'clawpay.json');
const BASE_URL    = 'https://clawpay.dxmjuhe.com';
const SKILLS_DIR  = path.join(__dirname, '../..');

// ─── ZIP extractor (pure Node.js, no child_process) ──────────────────────────

function extractZip(zipPath, destDir) {
  const buf = fs.readFileSync(zipPath);
  // Find End of Central Directory record (signature 0x06054b50)
  let eocdOffset = -1;
  for (let i = buf.length - 22; i >= 0; i--) {
    if (buf.readUInt32LE(i) === 0x06054b50) { eocdOffset = i; break; }
  }
  if (eocdOffset === -1) throw new Error('Invalid ZIP file');
  const cdEntries = buf.readUInt16LE(eocdOffset + 10);
  let offset = buf.readUInt32LE(eocdOffset + 16);
  for (let i = 0; i < cdEntries; i++) {
    if (buf.readUInt32LE(offset) !== 0x02014b50) throw new Error('Invalid central directory');
    const compression     = buf.readUInt16LE(offset + 10);
    const compressedSize  = buf.readUInt32LE(offset + 20);
    const fileNameLen     = buf.readUInt16LE(offset + 28);
    const extraLen        = buf.readUInt16LE(offset + 30);
    const commentLen      = buf.readUInt16LE(offset + 32);
    const localHdrOffset  = buf.readUInt32LE(offset + 42);
    const fileName        = buf.slice(offset + 46, offset + 46 + fileNameLen).toString('utf8');
    offset += 46 + fileNameLen + extraLen + commentLen;
    const destPath = path.join(destDir, fileName);
    if (fileName.endsWith('/')) { fs.mkdirSync(destPath, { recursive: true }); continue; }
    const localFileNameLen = buf.readUInt16LE(localHdrOffset + 26);
    const localExtraLen    = buf.readUInt16LE(localHdrOffset + 28);
    const dataOffset       = localHdrOffset + 30 + localFileNameLen + localExtraLen;
    const compressed       = buf.slice(dataOffset, dataOffset + compressedSize);
    const fileData = compression === 0 ? compressed : zlib.inflateRawSync(compressed);
    fs.mkdirSync(path.dirname(destPath), { recursive: true });
    fs.writeFileSync(destPath, fileData);
  }
}

// ─── Crypto ───────────────────────────────────────────────────────────────────

function generateKeys() {
  const { privateKey, publicKey } = crypto.generateKeyPairSync('ec', { namedCurve: 'prime256v1' });
  const pubKeyDer = publicKey.export({ type: 'spki', format: 'der' });
  return {
    uid:           crypto.createHash('sha256').update(pubKeyDer).digest('hex').substring(0, 32),
    publicKeyB64:  pubKeyDer.toString('base64'),
    publicKeyPem:  publicKey.export({ type: 'spki', format: 'pem' }),
    privateKeyPem: privateKey.export({ type: 'pkcs8', format: 'pem' }),
  };
}

// ─── Config ───────────────────────────────────────────────────────────────────

function ensureConfig() {
  let config;
  try {
    config = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
  } catch (_) {
    output({ success: false, message: '用户未注册，请先运行: userConfig' });
    process.exit(1);
  }
  if (!config.uid || !config.registered) {
    output({ success: false, message: '用户未注册，请先运行: userConfig' });
    process.exit(1);
  }
  return config;
}

// ─── HTTP ─────────────────────────────────────────────────────────────────────

/** 普通 JSON 请求 */
async function httpRequest(url, options = {}) {
  return new Promise((resolve, reject) => {
    const urlObj = new URL(url);
    const lib = urlObj.protocol === 'https:' ? https : http;
    const reqOptions = {
      hostname: urlObj.hostname,
      port: urlObj.port || (urlObj.protocol === 'https:' ? 443 : 80),
      path: urlObj.pathname + urlObj.search,
      method: options.method || 'GET',
      headers: options.headers || {},
    };
    if (urlObj.protocol === 'https:') {
      try { reqOptions.secureOptions = crypto.constants.SSL_OP_LEGACY_SERVER_CONNECT; } catch (_) {}
    }
    const req = lib.request(reqOptions, (res) => {
      const chunks = [];
      res.on('data', (c) => chunks.push(c));
      res.on('end', () => resolve({ status: res.statusCode, headers: res.headers, body: Buffer.concat(chunks) }));
    });
    req.on('error', reject);
    if (options.body) req.write(options.body);
    req.end();
  });
}

// ─── Signing ──────────────────────────────────────────────────────────────────

function sortKeysRecursive(obj) {
  if (Array.isArray(obj)) return obj.map(sortKeysRecursive);
  if (obj !== null && typeof obj === 'object') {
    return Object.fromEntries(Object.keys(obj).sort().map((k) => [k, sortKeysRecursive(obj[k])]));
  }
  return obj;
}

function buildSignedGetUrl(baseUrl, params, privateKeyPem) {
  const timestamp = String(Date.now());
  const allParams = Object.assign({}, params, { timestamp });
  const sortedJson = JSON.stringify(sortKeysRecursive(allParams));
  const message = `${timestamp}\n${sortedJson}`;
  const signer = crypto.createSign('SHA256');
  signer.update(message, 'utf8');
  const sign = signer.sign(privateKeyPem, 'base64');
  const qs = new URLSearchParams(Object.assign({}, allParams, { sign })).toString();
  return `${baseUrl}?${qs}`;
}

// ─── Helpers ──────────────────────────────────────────────────────────────────

function output(data) {
  console.log(JSON.stringify(data, null, 2));
}

function parseArgs(args) {
  const result = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--')) {
      const key = args[i].slice(2).replace(/-([a-z])/g, (_, c) => c.toUpperCase());
      result[key] = args[i + 1] !== undefined && !args[i + 1].startsWith('--') ? args[++i] : true;
    }
  }
  return result;
}

// ─── userConfig ───────────────────────────────────────────────────────────────

async function cmdUserConfig() {
  let config;
  try { config = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8')); } catch (_) { config = null; }
  if (config && config.uid && config.registered) {
    output({ success: true, action: 'exists', uid: config.uid });
    return;
  }

  const keys = generateKeys();

  // 注册
  const timestamp = String(Date.now());
  const message   = `${timestamp}\n${keys.publicKeyB64}`;
  const signer    = crypto.createSign('SHA256');
  signer.update(message, 'utf8');
  const sign = signer.sign(keys.privateKeyPem, 'base64');

  const body = JSON.stringify({ public_key_b64: keys.publicKeyB64, timestamp, sign });
  let res;
  try {
    res = await httpRequest(`${BASE_URL}/api/skill/client/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(body) },
      body,
    });
  } catch (e) {
    output({ success: false, message: `注册请求失败: ${e.message}` }); process.exit(1); return;
  }

  let data;
  try { data = JSON.parse(res.body.toString('utf8')); } catch (_) { data = res.body.toString('utf8'); }
  if (res.status !== 200) {
    output({ success: false, message: '注册失败', status: res.status, data }); process.exit(1); return;
  }

  const configToSave = {
    uid:           keys.uid,
    publicKeyB64:  keys.publicKeyB64,
    publicKeyPem:  keys.publicKeyPem,
    privateKeyPem: keys.privateKeyPem,
    registered:    true,
    registeredAt:  new Date().toISOString(),
  };
  fs.mkdirSync(path.dirname(CONFIG_PATH), { recursive: true });
  fs.writeFileSync(CONFIG_PATH, JSON.stringify(configToSave, null, 2));
  output({ success: true, action: 'created', uid: keys.uid, configPath: CONFIG_PATH, serverResponse: data });
}

// ─── queryPurchaseDetail ──────────────────────────────────────────────────────

async function cmdQueryPurchaseDetail(args) {
  const { skillId } = parseArgs(args);
  if (!skillId) {
    output({ success: false, message: '请提供 skill ID（--skill-id <id>）' });
    process.exit(1);
  }
  const config = ensureConfig();
  const url = buildSignedGetUrl(
    `${BASE_URL}/api/skill/purchase/detail`,
    { uid: config.uid, skill_id: skillId },
    config.privateKeyPem
  );
  let res;
  try { res = await httpRequest(url); } catch (e) {
    output({ success: false, message: `请求失败: ${e.message}` }); process.exit(1);
  }
  let data;
  try { data = JSON.parse(res.body.toString('utf8')); } catch (_) { data = res.body.toString('utf8'); }
  output({ success: res.status === 200, data });
}

// ─── downloadSkill ────────────────────────────────────────────────────────────

async function cmdDownloadSkill(args) {
  const { skillId } = parseArgs(args);
  if (!skillId) {
    output({ success: false, message: '请提供 skill ID（--skill-id <id>）' });
    process.exit(1);
  }

  const config = ensureConfig();

  // request_id = sha256(publicKeyB64 + random)
  const random     = crypto.randomBytes(16).toString('hex');
  const requestId  = crypto.createHash('sha256')
    .update(config.publicKeyB64 + random)
    .digest('hex');

  const url = buildSignedGetUrl(
    `${BASE_URL}/api/skill/download`,
    { uid: config.uid, skill_id: skillId, request_id: requestId },
    config.privateKeyPem
  );

  let res;
  try {
    res = await httpRequest(url);
  } catch (e) {
    output({ success: false, message: `请求失败: ${e.message}` });
    process.exit(1);
  }

  const contentType = (res.headers['content-type'] || '').toLowerCase();

  // 服务端用 HTTP 200 包裹逻辑 403（未支付）
  if (contentType.includes('application/json')) {
    let data;
    try { data = JSON.parse(res.body.toString('utf8')); } catch (_) { data = {}; }
    if (res.status === 403 || (data && data.ret === 403)) {
      const content = (data && data.content) || {};
      const purchaseParams = typeof content.data === 'string'
        ? Object.fromEntries(new URLSearchParams(content.data))
        : content.data || {};
      output({
        success:  false,
        error:    'PAYMENT_REQUIRED',
        message:  (data && data.msg) || '用户尚未支付',
        purchase: purchaseParams,
        raw:      data,
      });
      process.exit(1);
    }
    output({ success: false, status: res.status, data });
    process.exit(1);
  }

  if (res.status !== 200) {
    let data;
    try { data = JSON.parse(res.body.toString('utf8')); } catch (_) { data = res.body.toString('utf8'); }
    output({ success: false, status: res.status, data });
    process.exit(1);
  }

  // 1. 保存 zip 到当前目录
  const zipName = `${skillId}.zip`;
  const zipPath = path.join(process.cwd(), zipName);
  fs.writeFileSync(zipPath, res.body);
  process.stderr.write(`✅ 已下载: ${zipPath}\n`);

  // 2. 解压到临时目录
  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'skill-'));
  try {
    extractZip(zipPath, tmpDir);
  } catch (e) {
    output({ success: false, message: `解压失败: ${e.message}`, zipPath });
    process.exit(1);
  }
  process.stderr.write(`✅ 已解压到: ${tmpDir}\n`);

  // 3. 拷贝到 ~/.openclaw/workspace/skills/
  fs.mkdirSync(SKILLS_DIR, { recursive: true });
  try {
    fs.cpSync(tmpDir, SKILLS_DIR, { recursive: true });
  } catch (e) {
    output({ success: false, message: `安装失败: ${e.message}`, tmpDir });
    process.exit(1);
  }

  // 清理临时目录和 zip 包
  try {
    fs.rmSync(tmpDir, { recursive: true, force: true });
  } catch (_) {}
  try {
    fs.unlinkSync(zipPath);
  } catch (_) {}

  output({
    success: true,
    skillId,
    installedTo: SKILLS_DIR,
    message: `Skill ${skillId} 已成功安装到 ${SKILLS_DIR}`,
  });
}

// ─── Main ─────────────────────────────────────────────────────────────────────

const [, , command, ...args] = process.argv;

const COMMANDS = {
  userConfig:           cmdUserConfig,
  queryPurchaseDetail:  cmdQueryPurchaseDetail,
  downloadSkill:        cmdDownloadSkill,
};

(async () => {
  if (!command || !COMMANDS[command]) {
    output({
      success:   false,
      message:   `未知命令: ${command || '(无)'}`,
      available: Object.keys(COMMANDS),
    });
    process.exit(1);
  }
  await COMMANDS[command](args);
})().catch((err) => {
  output({ success: false, error: err.message });
  process.exit(1);
});
