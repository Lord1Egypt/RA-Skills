// AgentAlarm end-to-end encryption, v1. Node stdlib only.
// The gateway seals an alarm to the iPhone's X25519 public key; only the phone can open it.
//   shared = X25519(ephemeralPrivate, devicePublic)
//   key    = HKDF-SHA256(shared, salt = ephemeralPublic || devicePublic, info = "agentalarm-v1", 32 bytes)
//   ct     = AES-256-GCM(key, nonce 12B, utf8 JSON) with the 16-byte tag appended
// The iOS side mirrors this with CryptoKit (Curve25519.KeyAgreement, HKDF<SHA256>, AES.GCM).
import { createCipheriv, createDecipheriv, createPublicKey, diffieHellman, generateKeyPairSync, hkdfSync, randomBytes } from 'node:crypto';

const INFO = Buffer.from('agentalarm-v1');
const b64url = (buf) => Buffer.from(buf).toString('base64url');
const rawPublic = (keyObject) => Buffer.from(keyObject.export({ format: 'jwk' }).x, 'base64url');
const publicFromRaw = (raw) => createPublicKey({ key: { kty: 'OKP', crv: 'X25519', x: b64url(raw) }, format: 'jwk' });

function deriveKey(shared, ephemeralPublic, devicePublic) {
  return Buffer.from(hkdfSync('sha256', shared, Buffer.concat([ephemeralPublic, devicePublic]), INFO, 32));
}

/** Seals `message` (any JSON value) for the device whose raw X25519 public key is `devicePublicB64` (standard base64). */
export function seal(devicePublicB64, message) {
  const devicePublic = Buffer.from(devicePublicB64, 'base64');
  if (devicePublic.length !== 32) throw new Error('device public key must be 32 bytes');
  const eph = generateKeyPairSync('x25519');
  const ephPublic = rawPublic(eph.publicKey);
  const shared = diffieHellman({ privateKey: eph.privateKey, publicKey: publicFromRaw(devicePublic) });
  const key = deriveKey(shared, ephPublic, devicePublic);
  const nonce = randomBytes(12);
  const cipher = createCipheriv('aes-256-gcm', key, nonce);
  const ct = Buffer.concat([cipher.update(JSON.stringify(message), 'utf8'), cipher.final(), cipher.getAuthTag()]);
  return { v: 1, epk: ephPublic.toString('base64'), n: nonce.toString('base64'), ct: ct.toString('base64') };
}

/** Opens a sealed box with the device's private KeyObject. Used by tests; the phone does this in Swift. */
export function open(devicePrivateKey, devicePublicB64, box) {
  const ephPublic = Buffer.from(box.epk, 'base64');
  const shared = diffieHellman({ privateKey: devicePrivateKey, publicKey: publicFromRaw(ephPublic) });
  const key = deriveKey(shared, ephPublic, Buffer.from(devicePublicB64, 'base64'));
  const data = Buffer.from(box.ct, 'base64');
  const decipher = createDecipheriv('aes-256-gcm', key, Buffer.from(box.n, 'base64'));
  decipher.setAuthTag(data.subarray(data.length - 16));
  return JSON.parse(Buffer.concat([decipher.update(data.subarray(0, data.length - 16)), decipher.final()]).toString('utf8'));
}

/** A fresh device key pair (tests and tooling): { privateKey: KeyObject, publicB64 }. */
export function deviceKeyPair() {
  const kp = generateKeyPairSync('x25519');
  return { privateKey: kp.privateKey, publicB64: rawPublic(kp.publicKey).toString('base64') };
}
