#!/usr/bin/env node
'use strict';

const crypto = require('crypto');
const fs   = require('fs');
const os   = require('os');
const path = require('path');
const http  = require('http');
const https = require('https');

const CONFIG_PATH = path.join(process.env.CLAUDE_SKILL_DIR || __dirname, 'sp-weather-config.json');
const BASE_URL = process.env.SP_WEATHER_BASE || 'https://www.dxmpay.com';
const SKILL_ID = '6143ff36-82e6-4d96-468a-e299dd478554';

// ─── 密码读取（终端不回显 / 环境变量两路） ────────────────────────────────

/**
 * 从终端读取密码（字符不回显）。
 * 若 SP_WEATHER_PASSWORD 环境变量已设置则直接返回，不弹提示。
 * @param {string} prompt
 * @returns {Promise<string>}
 */
function readPassword(prompt) {
  if (process.env.SP_WEATHER_PASSWORD) {
    return Promise.resolve(process.env.SP_WEATHER_PASSWORD);
  }
  return new Promise((resolve) => {
    process.stderr.write(prompt);
    let password = '';
    const onData = (buf) => {
      for (const ch of buf.toString()) {
        if (ch === '\n' || ch === '\r' || ch === '\u0004') {   // Enter / EOF
          process.stdin.setRawMode(false);
          process.stdin.removeListener('data', onData);
          process.stdin.pause();
          process.stderr.write('\n');
          resolve(password);
          return;
        } else if (ch === '\u0003') {                           // Ctrl-C
          process.stderr.write('\n');
          process.exit(0);
        } else if (ch === '\u007f' || ch === '\b') {            // Backspace
          password = password.slice(0, -1);
        } else {
          password += ch;
        }
      }
    };
    process.stdin.setRawMode(true);
    process.stdin.resume();
    process.stdin.on('data', onData);
  });
}

// 同一进程内只读一次密码
let _cachedPassword = null;
async function getPassword() {
  if (_cachedPassword !== null) return _cachedPassword;
  _cachedPassword = await readPassword('请输入私钥保护密码: ');
  return _cachedPassword;
}

// ─── PBKDF2 + AES-256-GCM 私钥加解密 ────────────────────────────────────────

const PBKDF2_ITERATIONS = 210000;

/**
 * 用密码加密私钥 PEM，返回可 JSON 序列化的对象。
 * @param {string} pem
 * @param {string} password
 */
function encryptPrivateKey(pem, password) {
  const salt       = crypto.randomBytes(32);
  const key        = crypto.pbkdf2Sync(password, salt, PBKDF2_ITERATIONS, 32, 'sha512');
  const iv         = crypto.randomBytes(12);
  const cipher     = crypto.createCipheriv('aes-256-gcm', key, iv);
  const ciphertext = Buffer.concat([cipher.update(pem, 'utf8'), cipher.final()]);
  const authTag    = cipher.getAuthTag();
  return {
    kdf:        'pbkdf2-sha512',
    iterations: PBKDF2_ITERATIONS,
    salt:       salt.toString('base64'),
    iv:         iv.toString('base64'),
    authTag:    authTag.toString('base64'),
    ciphertext: ciphertext.toString('base64'),
  };
}

/**
 * 用密码解密私钥，密码错误时抛出异常。
 * @param {{ salt, iv, authTag, ciphertext, iterations }} encrypted
 * @param {string} password
 * @returns {string} PEM
 */
function decryptPrivateKey(encrypted, password) {
  const salt       = Buffer.from(encrypted.salt,       'base64');
  const iv         = Buffer.from(encrypted.iv,         'base64');
  const authTag    = Buffer.from(encrypted.authTag,    'base64');
  const ciphertext = Buffer.from(encrypted.ciphertext, 'base64');
  const iterations = encrypted.iterations || PBKDF2_ITERATIONS;
  const key        = crypto.pbkdf2Sync(password, salt, iterations, 32, 'sha512');
  const decipher   = crypto.createDecipheriv('aes-256-gcm', key, iv);
  decipher.setAuthTag(authTag);
  try {
    return decipher.update(ciphertext) + decipher.final('utf8');
  } catch {
    throw new Error('密码错误，私钥解密失败');
  }
}

// ─── Config ──────────────────────────────────────────────────────────────────

function readConfig() {
  try {
    if (fs.existsSync(CONFIG_PATH)) {
      return JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
    }
  } catch (e) {}
  return null;
}

function generateKeys() {
  const { privateKey, publicKey } = crypto.generateKeyPairSync('ec', {
    namedCurve: 'prime256v1', // secp256r1
  });
  const pubKeyDer = publicKey.export({ type: 'spki', format: 'der' });
  // uid = hex(SHA-256(publicKey.getEncoded())).substring(0, 32)
  const uid = crypto.createHash('sha256').update(pubKeyDer).digest('hex').substring(0, 32);
  return {
    uid,
    publicKeyB64: pubKeyDer.toString('base64'),
    publicKeyPem: publicKey.export({ type: 'spki', format: 'pem' }),
    privateKeyPem: privateKey.export({ type: 'pkcs8', format: 'pem' }),
  };
}

/**
 * 读取并校验配置，用密码解密私钥后返回完整 config 对象。
 * 自动检测旧格式（uid 推导密钥），提示用户重新注册。
 */
async function ensureConfig() {
  const config = readConfig();
  if (!config || !config.uid || !config.registered) {
    output({ success: false, message: '用户未注册，请先运行: userConfig' });
    process.exit(1);
  }
  // 旧格式检测：privateKey 字段不存在或不是 object，说明是旧的 uid 推导加密方案
  if (!config.privateKey || typeof config.privateKey !== 'object') {
    output({
      success: false,
      message: '配置格式已更新，请重新运行 userConfig 完成迁移（原配置将被覆盖）',
    });
    process.exit(1);
  }
  const password = await getPassword();
  try {
    config.privateKeyPem = decryptPrivateKey(config.privateKey, password);
  } catch (e) {
    output({ success: false, message: e.message });
    process.exit(1);
  }
  return config;
}

// ─── HTTP ─────────────────────────────────────────────────────────────────────

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

    // Fix for Node.js 22+ OpenSSL 3.x TLS renegotiation issue
    if (urlObj.protocol === 'https:') {
      try {
        reqOptions.secureOptions = crypto.constants.SSL_OP_LEGACY_SERVER_CONNECT;
      } catch (e) {
        console.error('Warning: could not set secureOptions:', e.message);
      }
    }

    const req = lib.request(reqOptions, (res) => {
      let data = '';
      res.on('data', (chunk) => (data += chunk));
      res.on('end', () => {
        resolve({ status: res.statusCode, body: data });
      });
    });
    req.on('error', reject);
    if (options.body) req.write(options.body);
    req.end();
  });
}

// ─── Signing ──────────────────────────────────────────────────────────────────

// 递归按 key 排序对象
function sortKeysRecursive(obj) {
  if (Array.isArray(obj)) return obj.map(sortKeysRecursive);
  if (obj !== null && typeof obj === 'object') {
    return Object.fromEntries(
      Object.keys(obj).sort().map((k) => [k, sortKeysRecursive(obj[k])])
    );
  }
  return obj;
}

// 注册签名: timestamp + "\n" + public_key_b64
function signRegistration(timestamp, publicKeyB64, privateKeyPem) {
  const message = `${timestamp}\n${publicKeyB64}`;
  const signer = crypto.createSign('SHA256');
  signer.update(message, 'utf8');
  return signer.sign(privateKeyPem, 'base64');
}

// API 请求签名: timestamp + "\n" + sortedJson(bodyWithoutSign)
function signApiBody(timestamp, bodyObj, privateKeyPem) {
  const bodyWithoutSign = Object.assign({}, bodyObj);
  delete bodyWithoutSign.sign;
  const sortedJson = JSON.stringify(sortKeysRecursive(bodyWithoutSign));
  const message = `${timestamp}\n${sortedJson}`;
  const signer = crypto.createSign('SHA256');
  signer.update(message, 'utf8');
  return signer.sign(privateKeyPem, 'base64');
}

// 构造带签名的 POST body（timestamp 为毫秒字符串）
function buildSignedPostBody(params, privateKeyPem) {
  const timestamp = String(Date.now());
  const bodyObj = Object.assign({}, params, { timestamp });
  const sign = signApiBody(timestamp, bodyObj, privateKeyPem);
  return JSON.stringify(Object.assign({}, bodyObj, { sign }));
}

// 构造带签名的 GET URL（query params 转为 JSON 对象签名）
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

// ─── QR Code ─────────────────────────────────────────────────────────────────

const { showQRCode } = require('./qrcode.min');

// ─── Arg parser ───────────────────────────────────────────────────────────────

function parseArgs(args) {
  const result = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--')) {
      const key = args[i].slice(2).replace(/-([a-z])/g, (_, c) => c.toUpperCase());
      result[key] = args[i + 1] !== undefined && !args[i + 1].startsWith('--')
        ? args[++i]
        : true;
    }
  }
  return result;
}

function output(data) {
  console.log(JSON.stringify(data, null, 2));
}

// ─── Commands ─────────────────────────────────────────────────────────────────

async function cmdUserConfig() {
  const config = readConfig();
  if (config && config.uid && config.registered) {
    output({ success: true, action: 'exists', uid: config.uid });
    return;
  }

  // 生成 EC 密钥对
  const keys = generateKeys();

  // 提示用户设置密码（两次确认），不从环境变量读（这是首次设置）
  let password, confirm;
  do {
    password = await readPassword('设置私钥保护密码（不可为空）: ');
    if (!password) {
      process.stderr.write('密码不能为空，请重新输入\n');
      continue;
    }
    confirm = await readPassword('再次输入密码确认: ');
    if (password !== confirm) {
      process.stderr.write('两次密码不一致，请重新输入\n');
      password = '';
    }
  } while (!password);

  const timestamp = String(Date.now());
  const sign = signRegistration(timestamp, keys.publicKeyB64, keys.privateKeyPem);

  const body = JSON.stringify({
    public_key_b64: keys.publicKeyB64,
    timestamp,
    sign,
  });

  let res;
  try {
    res = await httpRequest(`${BASE_URL}/api/skill/client/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(body),
      },
      body,
    });
  } catch (e) {
    output({ success: false, message: `注册请求失败: ${e.message}` });
    process.exit(1);
    return;
  }

  let data;
  try { data = JSON.parse(res.body); } catch (_) { data = res.body; }

  if (res.status !== 200) {
    output({ success: false, message: '注册失败', status: res.status, data });
    process.exit(1);
    return;
  }

  // 公钥明文保存，私钥用密码 + PBKDF2 加密
  const configToSave = {
    uid:          keys.uid,
    publicKeyB64: keys.publicKeyB64,
    publicKeyPem: keys.publicKeyPem,
    privateKey:   encryptPrivateKey(keys.privateKeyPem, password),
    registered:   true,
    registeredAt: new Date().toISOString(),
  };
  fs.writeFileSync(CONFIG_PATH, JSON.stringify(configToSave, null, 2));
  output({
    success:        true,
    action:         'registered',
    uid:            keys.uid,
    configPath:     CONFIG_PATH,
    serverResponse: data,
  });
}

async function cmdQueryWeather(args) {
  const config = await ensureConfig();
  const { date, city } = parseArgs(args);

  if (!city) {
    output({ success: false, needCity: true, message: '请提供城市名称（--city 北京）' });
    process.exit(1);
    return;
  }

  const queryDate = date || new Date().toISOString().split('T')[0];
  const payload = { date: queryDate, city };

  const params = {
    skill_id: SKILL_ID,
    uid: config.uid,
    payload,
  };
  const body = buildSignedPostBody(params, config.privateKeyPem);

  let res;
  try {
    res = await httpRequest(`${BASE_URL}/api/skill/invoke`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(body),
      },
      body,
    });
  } catch (e) {
    output({ success: false, message: `连接天气服务失败: ${e.message}` });
    process.exit(1);
    return;
  }

  let data;
  try { data = JSON.parse(res.body); } catch (_) { data = res.body; }
   // data.payUrl = "https://www.baidu.com"
  if (data && data.payUrl) {
    process.stderr.write('\n⚠️  余额不足，请使用微信扫码付费：\n');
     showQRCode(data.payUrl);
    output({ success: false, payRequired: true, payUrl: data.payUrl, message: '余额不足，请扫码充值后重试' });
    process.exit(1);
    return;
  }

  if (res.status !== 200) {
    output({ success: false, status: res.status, data });
    process.exit(1);
    return;
  }

  output({ success: true, date: queryDate, city, data });
}

async function cmdQueryOrders(args) {
  const config = await ensureConfig();
  const { page = '1', pageSize = '20' } = parseArgs(args);
  const url = buildSignedGetUrl(
    `${BASE_URL}/api/skill/orders`,
    { uid: config.uid, page, page_size: pageSize },
    config.privateKeyPem
  );

  let res;
  try { res = await httpRequest(url); } catch (e) {
    output({ success: false, message: `请求失败: ${e.message}` }); process.exit(1); return;
  }
  let data;
  try { data = JSON.parse(res.body); } catch (_) { data = res.body; }
  output({ success: res.status === 200, data });
}

async function cmdQueryOrder(args) {
  const config = await ensureConfig();
  const { orderId } = parseArgs(args);
  if (!orderId) {
    output({ success: false, message: '请提供订单ID（--orderId SP202603192029449B6A4893）' });
    process.exit(1); return;
  }
  const url = buildSignedGetUrl(
    `${BASE_URL}/api/skill/orders/${encodeURIComponent(orderId)}`,
    { uid: config.uid },
    config.privateKeyPem
  );

  let res;
  try { res = await httpRequest(url); } catch (e) {
    output({ success: false, message: `请求失败: ${e.message}` }); process.exit(1); return;
  }
  let data;
  try { data = JSON.parse(res.body); } catch (_) { data = res.body; }
  output({ success: res.status === 200, data });
}

async function cmdQueryQuota() {
  const config = await ensureConfig();
  const url = buildSignedGetUrl(
    `${BASE_URL}/api/skill/quota`,
    { uid: config.uid, skill_id: SKILL_ID },
    config.privateKeyPem
  );

  let res;
  try { res = await httpRequest(url); } catch (e) {
    output({ success: false, message: `请求失败: ${e.message}` }); process.exit(1); return;
  }
  let data;
  try { data = JSON.parse(res.body); } catch (_) { data = res.body; }
  output({ success: res.status === 200, data });
}

async function cmdQueryPurchaseDetail() {
  const config = await ensureConfig();
  const url = buildSignedGetUrl(
    `${BASE_URL}/api/skill/purchase/detail`,
    { uid: config.uid, skill_id: SKILL_ID },
    config.privateKeyPem
  );

  let res;
  try { res = await httpRequest(url); } catch (e) {
    output({ success: false, message: `请求失败: ${e.message}` }); process.exit(1); return;
  }
  let data;
  try { data = JSON.parse(res.body); } catch (_) { data = res.body; }
  output({ success: res.status === 200, data });
}

async function cmdQueryCallLogs(args) {
  const config = await ensureConfig();
  const { page = '1', pageSize = '20' } = parseArgs(args);
  const url = buildSignedGetUrl(
    `${BASE_URL}/api/skill/call-logs`,
    { uid: config.uid, skill_id: SKILL_ID, page, page_size: pageSize },
    config.privateKeyPem
  );

  let res;
  try { res = await httpRequest(url); } catch (e) {
    output({ success: false, message: `请求失败: ${e.message}` }); process.exit(1); return;
  }
  let data;
  try { data = JSON.parse(res.body); } catch (_) { data = res.body; }
  output({ success: res.status === 200, data });
}

// ─── Main ─────────────────────────────────────────────────────────────────────

const [, , command, ...args] = process.argv;

const COMMANDS = {
  userConfig: cmdUserConfig,
  queryWeather: cmdQueryWeather,
  queryOrders: cmdQueryOrders,
  queryOrder: cmdQueryOrder,
  queryQuota: cmdQueryQuota,
  queryPurchaseDetail: cmdQueryPurchaseDetail,
  queryCallLogs: cmdQueryCallLogs,
};

(async () => {
  if (!command || !COMMANDS[command]) {
    output({
      success: false,
      message: `未知命令: ${command || '(无)'}`,
      available: Object.keys(COMMANDS),
    });
    process.exit(1);
  }
  await COMMANDS[command](args);
})().catch((err) => {
  output({ success: false, error: err.message });
  process.exit(1);
});
