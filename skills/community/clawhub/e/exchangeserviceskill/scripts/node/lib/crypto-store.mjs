import crypto from 'node:crypto';

export function encryptSecret(plaintext, masterKey) {
  if (!plaintext) {
    throw new Error('plaintext is required for encryption');
  }
  if (!masterKey) {
    throw new Error('masterKey is required for encryption');
  }

  const salt = crypto.randomBytes(16);
  const iv = crypto.randomBytes(12);
  const key = crypto.scryptSync(masterKey, salt, 32);
  const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);

  const encrypted = Buffer.concat([
    cipher.update(String(plaintext), 'utf8'),
    cipher.final(),
  ]);

  const tag = cipher.getAuthTag();

  return {
    version: 1,
    algorithm: 'aes-256-gcm',
    kdf: 'scrypt',
    salt_b64: salt.toString('base64'),
    iv_b64: iv.toString('base64'),
    tag_b64: tag.toString('base64'),
    ciphertext_b64: encrypted.toString('base64'),
  };
}

export function decryptSecret(store, masterKey) {
  if (!store) {
    throw new Error('secret_store is missing');
  }
  if (!masterKey) {
    throw new Error('masterKey is required for decryption');
  }

  if (store.algorithm !== 'aes-256-gcm' || store.kdf !== 'scrypt') {
    throw new Error('Unsupported secret_store format');
  }

  const salt = Buffer.from(store.salt_b64, 'base64');
  const iv = Buffer.from(store.iv_b64, 'base64');
  const tag = Buffer.from(store.tag_b64, 'base64');
  const ciphertext = Buffer.from(store.ciphertext_b64, 'base64');

  const key = crypto.scryptSync(masterKey, salt, 32);
  const decipher = crypto.createDecipheriv('aes-256-gcm', key, iv);
  decipher.setAuthTag(tag);

  const decrypted = Buffer.concat([
    decipher.update(ciphertext),
    decipher.final(),
  ]);

  return decrypted.toString('utf8');
}
