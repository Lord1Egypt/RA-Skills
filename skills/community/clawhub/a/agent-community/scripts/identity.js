#!/usr/bin/env node
/**
 * OpenClaw 接入 Agent 聚落：身份管理（生成/加载 Ed25519，持久化到 identity/）
 * 身份 = 公钥 hex；私钥永不离开本机。
 */
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const ID_DIR = path.join(__dirname, 'identity');
const ID_FILE = path.join(ID_DIR, 'identity.json');

function loadOrCreateIdentity(name) {
  if (fs.existsSync(ID_FILE)) {
    const saved = JSON.parse(fs.readFileSync(ID_FILE, 'utf8'));
    const priv = crypto.createPrivateKey({ key: Buffer.from(saved.privkey, 'hex'), format: 'der', type: 'pkcs8' });
    return { name: saved.name, priv, privHex: saved.privkey, pubHex: saved.pubkey, agentId: saved.agentId };
  }
  const { publicKey, privateKey } = crypto.generateKeyPairSync('ed25519');
  const pubHex = publicKey.export({ format: 'der', type: 'spki' }).toString('hex');
  const privHex = privateKey.export({ format: 'der', type: 'pkcs8' }).toString('hex');
  fs.mkdirSync(ID_DIR, { recursive: true });
  fs.writeFileSync(ID_FILE, JSON.stringify({ name, pubkey: pubHex, privkey: privHex, created: new Date().toISOString() }, null, 2), { mode: 0o600 });
  return { name, priv: crypto.createPrivateKey({ key: Buffer.from(privHex, 'hex'), format: 'der', type: 'pkcs8' }), privHex, pubHex, agentId: pubHex.toLowerCase() };
}

function sign(priv, s) {
  return crypto.sign(null, Buffer.from(s, 'utf8'), priv).toString('hex');
}

module.exports = { loadOrCreateIdentity, sign, ID_FILE, ID_DIR };
