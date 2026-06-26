#!/usr/bin/env node
const sodium = require('libsodium-wrappers');
const fs = require('fs');
const path = require('path');

const VAULT_PATH = path.join(process.cwd(), 'data/keystore');

module.exports = {
  // --- 身份与签名 (Phase 1) ---
  getOrGenerateIdentity: async (localAgentId) => {
    await sodium.ready;
    if (!fs.existsSync(VAULT_PATH)) fs.mkdirSync(VAULT_PATH, { recursive: true });
    const keyPath = path.join(VAULT_PATH, `${localAgentId}.keys.json`);
    if (fs.existsSync(keyPath)) {
      const keys = JSON.parse(fs.readFileSync(keyPath));
      return { publicKey: Buffer.from(keys.publicKey, 'hex'), privateKey: Buffer.from(keys.privateKey, 'hex') };
    }
    const keypair = sodium.crypto_sign_keypair();
    fs.writeFileSync(keyPath, JSON.stringify({
      publicKey: sodium.to_hex(keypair.publicKey),
      privateKey: sodium.to_hex(keypair.privateKey)
    }), { mode: 0o600 });
    return { publicKey: keypair.publicKey, privateKey: keypair.privateKey };
  },

  signPayload: async (localAgentId, payloadString) => {
    await sodium.ready;
    const keyPath = path.join(VAULT_PATH, `${localAgentId}.keys.json`);
    const keys = JSON.parse(fs.readFileSync(keyPath));
    const signature = sodium.crypto_sign_detached(payloadString, Buffer.from(keys.privateKey, 'hex'));
    return sodium.to_hex(signature);
  },

  verifySignature: async (publicKeyHex, payloadString, signatureHex) => {
    await sodium.ready;
    return sodium.crypto_sign_verify_detached(Buffer.from(signatureHex, 'hex'), payloadString, Buffer.from(publicKeyHex, 'hex'));
  },

  // --- 端到端对称加密 (Phase 3: E2EE) ---
  
  // 生成会话共享密钥 (32字节)
  generateSessionKey: async () => {
    await sodium.ready;
    return sodium.to_hex(sodium.randombytes_buf(sodium.crypto_secretbox_KEYBYTES));
  },

  encryptSecret: async (payloadString, sessionKeyHex) => {
    await sodium.ready;
    const key = Buffer.from(sessionKeyHex, 'hex');
    const nonce = sodium.randombytes_buf(sodium.crypto_secretbox_NONCEBYTES);
    const ciphertext = sodium.crypto_secretbox_easy(payloadString, nonce, key);
    return {
      ciphertext: sodium.to_hex(ciphertext),
      nonce: sodium.to_hex(nonce)
    };
  },

  decryptSecret: async (ciphertextHex, nonceHex, sessionKeyHex) => {
    await sodium.ready;
    try {
      const key = Buffer.from(sessionKeyHex, 'hex');
      const ciphertext = Buffer.from(ciphertextHex, 'hex');
      const nonce = Buffer.from(nonceHex, 'hex');
      const decrypted = sodium.crypto_secretbox_open_easy(ciphertext, nonce, key);
      return decrypted ? Buffer.from(decrypted).toString('utf-8') : null;
    } catch (e) {
      return null;
    }
  }
};
