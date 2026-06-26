import crypto from 'crypto';
import fs from 'fs';

export function encryptPrivateKey(pk: string, passphrase: string): { iv: string; salt: string; tag: string; data: string } {
  const iv = crypto.randomBytes(12);
  const salt = crypto.randomBytes(16);
  const key = crypto.scryptSync(passphrase, salt, 32);
  const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);
  const data = Buffer.concat([cipher.update(pk, 'utf8'), cipher.final()]);
  const tag = cipher.getAuthTag();
  return { iv: iv.toString('hex'), salt: salt.toString('hex'), tag: tag.toString('hex'), data: data.toString('hex') };
}

export function decryptPrivateKey(file: string, passphrase: string): string {
  const p = JSON.parse(fs.readFileSync(file, 'utf8'));
  const key = crypto.scryptSync(passphrase, Buffer.from(p.salt, 'hex'), 32);
  const decipher = crypto.createDecipheriv('aes-256-gcm', key, Buffer.from(p.iv, 'hex'));
  decipher.setAuthTag(Buffer.from(p.tag, 'hex'));
  const out = Buffer.concat([decipher.update(Buffer.from(p.data, 'hex')), decipher.final()]);
  return out.toString('utf8');
}
