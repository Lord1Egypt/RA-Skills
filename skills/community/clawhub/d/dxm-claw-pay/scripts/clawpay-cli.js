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

/**
 * 校验 zip 条目名解压后仍落在 destDir 内，防止路径穿越（Zip Slip）。
 * 拒绝绝对路径、盘符路径、含 .. 的路径以及解析后逃逸出 destDir 的路径。
 */
function safeResolveEntry(destRoot, fileName) {
  // 统一分隔符：zip 规范用 '/'，但恶意包可能塞入 '\'
  const normalized = fileName.replace(/\\/g, '/');
  if (normalized === '' || normalized.startsWith('/') || /^[a-zA-Z]:/.test(normalized)) {
    throw new Error(`非法的压缩包条目（绝对路径）: ${fileName}`);
  }
  if (normalized.split('/').some((seg) => seg === '..')) {
    throw new Error(`非法的压缩包条目（路径穿越）: ${fileName}`);
  }
  const resolved = path.resolve(destRoot, normalized);
  if (resolved !== destRoot && !resolved.startsWith(destRoot + path.sep)) {
    throw new Error(`非法的压缩包条目（越出解压目录）: ${fileName}`);
  }
  return resolved;
}

function extractZip(zipPath, destDir) {
  const destRoot = path.resolve(destDir);
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
    const destPath = safeResolveEntry(destRoot, fileName);
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

// ─── 下载包完整性校验（哈希 + 验签） ─────────────────────────────────────────

// 服务端签名公钥（RSA-2048），源码中以 XOR 混淆存放，使用时还原。
// 混淆仅为避免明文出现在仓库/静态扫描中，不构成机密性保护——公钥本身是公开信息，
// 安全性依赖于服务端私钥不泄漏。
const PUB_KEY_MASK = 'clawpay-skill-verify-2026';
const PUB_KEY_OBF = [
  'TkFMWl0jPGo6JUk8OW86LDFJLTx0Hx0fG05mLD45IzBHMiUrCwdcHg4bLl8OHXBxY3MlLSA4MyAo',
  'FTImICUubhEuMSg3PGwZY2RwCCpVIyoHKwYaHT4FAgIyEngdETZDRnpIfjIJCRI/ERFsAQEtADtJ',
  'IDAYGwgMewJkRmwkD1FFNCwMdz0DKBw5YEISIDxVCmlzWHpSMAoFJQAOcxUKRAFcFFgZIyYEVSt4',
  'A15WYCtDFyc8VgNLIzEhHx8GMQY/MxMVdV4ES1kxDiAkABczZB0EHgUlZl0nQDoPN2k4CUB+AhY2',
  'JREFAHQUMTwbDl00HEEbUBt7C2RXXQQdNRVINjFICy0ZHAUeWSMRBzc9YERofk8NFgciRjM6SkBb',
  'M2YkXzwyEDBNLXRxG2h5FiYXIzEjM2A0CDwvC2kiAREsXxhVAl9oBlo9NjIGDBdcWCMsAFhgJzQz',
  'HgIufX9xZngtZiUPKTtIGh8iETQ/HkQAESwPTkxDeWZnBTksFDsYPGQyXhMYA0MFKD5bPDRnAUN/',
  'WFEHEjkXFTJZQyQbNS9iWTV4HBEwaXNhc3RpQUxaXUw8YzdLOTkuYT8mUiIjIAAfHR8baQ==',
].join('');

/** 还原签名公钥 PEM */
function getVerifyPublicKeyPem() {
  const data = Buffer.from(PUB_KEY_OBF, 'base64');
  const mask = Buffer.from(PUB_KEY_MASK, 'utf8');
  const out = Buffer.alloc(data.length);
  for (let i = 0; i < data.length; i++) out[i] = data[i] ^ mask[i % mask.length];
  return out.toString('utf8');
}

/**
 * 校验下载内容：
 *   1) sha256(zip) 必须等于响应头 file_hash
 *   2) file_sign 必须能被服务端公钥验证通过
 *      签名算法对应 `openssl dgst -sha256 -sign priv.pem input | base64`
 *      （RSASSA-PKCS1-v1_5 + SHA256）。input 兼容两种服务端实现：
 *      file_hash 十六进制串，或 zip 原始字节。
 * 校验不通过时抛错；无论成功或失败都打印一行日志。
 */
function verifyDownload(buf, headers) {
  const expectHash = String(headers['file_hash'] || headers['x-file-hash'] || '').trim().toLowerCase();
  const signB64    = String(headers['file_sign'] || headers['x-file-sign'] || '').replace(/\s+/g, '');

  process.stderr.write(`签名: ${expectHash},sign:${signB64}\n`);

  if (!expectHash || !signB64) {
    process.stderr.write('❌ 签名校验失败: 响应头缺少 file_hash 或 file_sign\n');
    throw new Error('响应头缺少 file_hash 或 file_sign，拒绝安装');
  }

  const actualHash = crypto.createHash('sha256').update(buf).digest('hex');
  if (actualHash !== expectHash) {
    process.stderr.write(`❌ 签名校验失败: 文件哈希不匹配 (expect=${expectHash} actual=${actualHash})\n`);
    throw new Error('文件哈希不匹配，拒绝安装');
  }

  const pubKeyPem = getVerifyPublicKeyPem();
  let matched = null;
  for (const [label, payload] of [['file_hash', Buffer.from(expectHash, 'utf8')], ['zip_bytes', buf]]) {
    let ok = false;
    try {
      const verifier = crypto.createVerify('RSA-SHA256');
      verifier.update(payload);
      ok = verifier.verify(pubKeyPem, signB64, 'base64');
    } catch (_) {
      ok = false;
    }
    if (ok) { matched = label; break; }
  }

  if (!matched) {
    process.stderr.write('❌ 签名校验失败: file_sign 与服务端公钥不匹配\n');
    throw new Error('签名验证失败，拒绝安装');
  }

  process.stderr.write(`✅ 签名校验通过: sha256=${actualHash} payload=${matched}\n`);
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

  // 1.5 解压前做哈希 + 验签校验，失败立即删包退出
  try {
    verifyDownload(res.body, res.headers);
  } catch (e) {
    try { fs.unlinkSync(zipPath); } catch (_) {}
    output({ success: false, error: 'INTEGRITY_CHECK_FAILED', message: e.message });
    process.exit(1);
  }

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

const COMMANDS = {
  userConfig:           cmdUserConfig,
  queryPurchaseDetail:  cmdQueryPurchaseDetail,
  downloadSkill:        cmdDownloadSkill,
};

// 仅在作为 CLI 直接执行时运行；被 require 时只导出函数，便于测试
if (require.main === module) {
  const [, , command, ...args] = process.argv;
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
}

module.exports = {
  extractZip,
  safeResolveEntry,
  sortKeysRecursive,
  parseArgs,
  getVerifyPublicKeyPem,
  verifyDownload,
};
