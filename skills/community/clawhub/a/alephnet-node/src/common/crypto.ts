/**
 * Cryptographic Utilities
 * 
 * Centralized cryptographic operations for AlephNet.
 * Uses Node.js crypto module for consistent behavior.
 */

import * as crypto from 'crypto';
import { PRIMES_16, SMFVector, HexString, Base64 } from './types';
import { tanh, normalize } from './math';

// ═══════════════════════════════════════════════════════════════════════════
// KEY GENERATION
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Ed25519 Key Pair
 */
export interface Ed25519KeyPair {
  publicKey: Buffer;
  privateKey: Buffer;
  publicKeyBase64: Base64;
  privateKeyBase64: Base64;
}

/**
 * Generate an Ed25519 key pair
 */
export function generateEd25519KeyPair(): Ed25519KeyPair {
  const { publicKey, privateKey } = crypto.generateKeyPairSync('ed25519', {
    publicKeyEncoding: { type: 'spki', format: 'der' },
    privateKeyEncoding: { type: 'pkcs8', format: 'der' }
  });
  
  // Extract raw 32-byte public key from SPKI format
  // SPKI for Ed25519: 12-byte prefix + 32-byte key
  const pubKeyRaw = publicKey.slice(-32);
  
  return {
    publicKey: pubKeyRaw,
    privateKey,
    publicKeyBase64: pubKeyRaw.toString('base64'),
    privateKeyBase64: privateKey.toString('base64')
  };
}

/**
 * Generate random bytes
 */
export function randomBytes(length: number): Buffer {
  return crypto.randomBytes(length);
}

/**
 * Generate a random UUID
 */
export function randomUUID(): string {
  return crypto.randomUUID();
}

// ═══════════════════════════════════════════════════════════════════════════
// SIGNING & VERIFICATION
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Sign data with Ed25519 private key (PKCS8 format)
 */
export function signEd25519(
  data: Buffer,
  privateKeyPkcs8: Buffer
): Buffer {
  const privateKey = crypto.createPrivateKey({
    key: privateKeyPkcs8,
    format: 'der',
    type: 'pkcs8'
  });
  
  return crypto.sign(null, data, privateKey);
}

/**
 * Verify Ed25519 signature with raw 32-byte public key
 */
export function verifyEd25519(
  data: Buffer,
  signature: Buffer,
  publicKeyRaw: Buffer
): boolean {
  // Wrap raw key in SPKI format
  const spkiPrefix = Buffer.from([
    0x30, 0x2a, 0x30, 0x05, 0x06, 0x03, 0x2b, 0x65,
    0x70, 0x03, 0x21, 0x00
  ]);
  const spkiKey = Buffer.concat([spkiPrefix, publicKeyRaw]);
  
  const publicKey = crypto.createPublicKey({
    key: spkiKey,
    format: 'der',
    type: 'spki'
  });
  
  return crypto.verify(null, data, publicKey, signature);
}

/**
 * Sign data with Ed25519 private key and return base64
 */
export function signToBase64(data: string | Buffer, privateKeyPkcs8: Buffer): Base64 {
  const dataBuffer = Buffer.isBuffer(data) ? data : Buffer.from(data);
  const signature = signEd25519(dataBuffer, privateKeyPkcs8);
  return signature.toString('base64');
}

/**
 * Verify Ed25519 signature from base64
 */
export function verifyFromBase64(
  data: string | Buffer,
  signatureBase64: Base64,
  publicKeyRaw: Buffer
): boolean {
  const dataBuffer = Buffer.isBuffer(data) ? data : Buffer.from(data);
  const signature = Buffer.from(signatureBase64, 'base64');
  return verifyEd25519(dataBuffer, signature, publicKeyRaw);
}

// ═══════════════════════════════════════════════════════════════════════════
// ENCRYPTION
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Encrypted data container
 */
export interface EncryptedData {
  ciphertext: Base64;
  nonce: Base64;
  authTag: Base64;
  algorithm: 'AES-256-GCM';
}

/**
 * Encrypt data using AES-256-GCM
 */
export function encryptAES256GCM(
  plaintext: Buffer,
  key: Buffer
): EncryptedData {
  if (key.length !== 32) {
    throw new Error('AES-256 requires a 32-byte key');
  }
  
  const nonce = crypto.randomBytes(12); // 96-bit nonce for GCM
  const cipher = crypto.createCipheriv('aes-256-gcm', key, nonce);
  
  const encrypted = Buffer.concat([
    cipher.update(plaintext),
    cipher.final()
  ]);
  
  const authTag = cipher.getAuthTag();
  
  return {
    ciphertext: encrypted.toString('base64'),
    nonce: nonce.toString('base64'),
    authTag: authTag.toString('base64'),
    algorithm: 'AES-256-GCM'
  };
}

/**
 * Decrypt data using AES-256-GCM
 */
export function decryptAES256GCM(
  encrypted: EncryptedData,
  key: Buffer
): Buffer {
  if (key.length !== 32) {
    throw new Error('AES-256 requires a 32-byte key');
  }
  
  const ciphertext = Buffer.from(encrypted.ciphertext, 'base64');
  const nonce = Buffer.from(encrypted.nonce, 'base64');
  const authTag = Buffer.from(encrypted.authTag, 'base64');
  
  const decipher = crypto.createDecipheriv('aes-256-gcm', key, nonce);
  decipher.setAuthTag(authTag);
  
  return Buffer.concat([
    decipher.update(ciphertext),
    decipher.final()
  ]);
}

/**
 * Encrypt a string and return base64
 */
export function encryptString(plaintext: string, key: Buffer): EncryptedData {
  return encryptAES256GCM(Buffer.from(plaintext, 'utf8'), key);
}

/**
 * Decrypt to string
 */
export function decryptToString(encrypted: EncryptedData, key: Buffer): string {
  return decryptAES256GCM(encrypted, key).toString('utf8');
}

// ═══════════════════════════════════════════════════════════════════════════
// KEY DERIVATION
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Derive a key using HKDF
 */
export function deriveKeyHKDF(
  ikm: Buffer,
  salt: Buffer,
  info: Buffer,
  length: number = 32
): Buffer {
  return Buffer.from(crypto.hkdfSync('sha256', ikm, salt, info, length));
}

/**
 * Derive a key from password using scrypt
 */
export function deriveKeyFromPassword(
  password: string,
  salt: Buffer,
  keyLen: number = 32,
  options?: crypto.ScryptOptions
): Promise<Buffer> {
  return new Promise((resolve, reject) => {
    crypto.scrypt(
      password,
      salt,
      keyLen,
      options || { N: 16384, r: 8, p: 1 },
      (err, derivedKey) => {
        if (err) reject(err);
        else resolve(derivedKey);
      }
    );
  });
}

// ═══════════════════════════════════════════════════════════════════════════
// RESONANCE FIELD COMPUTATION
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Compute 16-dimensional resonance field from public key
 * This is the core AlephNet identity derivation
 */
export function computeResonanceField(publicKey: Buffer): SMFVector {
  const resonance: number[] = new Array(16);
  
  for (let i = 0; i < 16; i++) {
    let sum = 0;
    const prime = PRIMES_16[i];
    
    for (let j = 0; j < publicKey.length; j++) {
      // Prime-modulated sine wave transformation
      sum += publicKey[j] * Math.sin(prime * j / publicKey.length);
    }
    
    // Normalize to [-1, 1] using tanh
    resonance[i] = tanh(sum / publicKey.length);
  }
  
  // Return as normalized SMF vector
  return normalize(resonance) as SMFVector;
}

/**
 * Select body primes based on public key hash
 */
export function selectBodyPrimes(publicKey: Buffer, count: number = 5): number[] {
  const hash = sha256Buffer(publicKey);
  const primes: number[] = [];
  
  // Use hash bytes to select from extended prime list
  const extendedPrimes = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53,
    59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113
  ];
  
  for (let i = 0; i < count && i < hash.length; i++) {
    const index = hash[i] % extendedPrimes.length;
    const prime = extendedPrimes[index];
    if (!primes.includes(prime)) {
      primes.push(prime);
    }
  }
  
  // Ensure we have enough primes
  while (primes.length < count) {
    for (const p of extendedPrimes) {
      if (!primes.includes(p)) {
        primes.push(p);
        break;
      }
    }
  }
  
  return primes.slice(0, count);
}

/**
 * Generate fingerprint from public key and resonance
 */
export function generateFingerprint(publicKey: Buffer, resonance: SMFVector): string {
  // Create deterministic hash of key + resonance
  const resonanceStr = resonance.map(n => n.toFixed(6)).join(',');
  const combined = Buffer.concat([publicKey, Buffer.from(resonanceStr)]);
  const hash = sha256Buffer(combined);
  
  // Convert first 8 bytes to 16-char hex fingerprint
  return hash.slice(0, 8).toString('hex');
}

// ═══════════════════════════════════════════════════════════════════════════
// HASHING
// ═══════════════════════════════════════════════════════════════════════════

/**
 * SHA-256 hash returning Buffer
 */
export function sha256Buffer(data: Buffer | string): Buffer {
  const hash = crypto.createHash('sha256');
  hash.update(data);
  return hash.digest();
}

/**
 * SHA-256 hash returning hex string
 */
export function sha256Hex(data: Buffer | string): HexString {
  const hash = crypto.createHash('sha256');
  hash.update(data);
  return hash.digest('hex');
}

/**
 * SHA-256 hash returning base64
 */
export function sha256Base64(data: Buffer | string): Base64 {
  const hash = crypto.createHash('sha256');
  hash.update(data);
  return hash.digest('base64');
}

/**
 * HMAC-SHA256
 */
export function hmacSha256(key: Buffer, data: Buffer | string): Buffer {
  const hmac = crypto.createHmac('sha256', key);
  hmac.update(data);
  return hmac.digest();
}

/**
 * Content-addressable hash for semantic content
 */
export function contentHash(content: string, modelName: string): string {
  return sha256Hex(`${modelName}:${content}`);
}

// ═══════════════════════════════════════════════════════════════════════════
// ENCODING UTILITIES
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Convert Buffer to Base64
 */
export function bufferToBase64(buf: Buffer): Base64 {
  return buf.toString('base64');
}

/**
 * Convert Base64 to Buffer
 */
export function base64ToBuffer(base64: Base64): Buffer {
  return Buffer.from(base64, 'base64');
}

/**
 * Convert Buffer to hex string
 */
export function bufferToHex(buf: Buffer): HexString {
  return buf.toString('hex');
}

/**
 * Convert hex string to Buffer
 */
export function hexToBuffer(hex: HexString): Buffer {
  return Buffer.from(hex, 'hex');
}

/**
 * Convert string to Buffer (UTF-8)
 */
export function stringToBuffer(str: string): Buffer {
  return Buffer.from(str, 'utf8');
}

/**
 * Convert Buffer to string (UTF-8)
 */
export function bufferToString(buf: Buffer): string {
  return buf.toString('utf8');
}

// ═══════════════════════════════════════════════════════════════════════════
// PRIME UTILITIES
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Check if a number is prime
 */
export function isPrime(n: number): boolean {
  if (n < 2) return false;
  if (n === 2) return true;
  if (n % 2 === 0) return false;
  
  const sqrt = Math.sqrt(n);
  for (let i = 3; i <= sqrt; i += 2) {
    if (n % i === 0) return false;
  }
  return true;
}

/**
 * Get prime factors of a number
 */
export function primeFactors(n: number): number[] {
  const factors: number[] = [];
  let divisor = 2;
  let remaining = n;
  
  while (remaining >= 2) {
    if (remaining % divisor === 0) {
      if (!factors.includes(divisor)) {
        factors.push(divisor);
      }
      remaining = remaining / divisor;
    } else {
      divisor++;
    }
  }
  
  return factors;
}

/**
 * Calculate prime domain overlap (Jaccard index)
 */
export function primeDomainOverlap(a: number[], b: number[]): number {
  if (a.length === 0 && b.length === 0) return 1;
  if (a.length === 0 || b.length === 0) return 0;
  
  const setA = new Set(a);
  const setB = new Set(b);
  
  let intersection = 0;
  for (const p of setA) {
    if (setB.has(p)) intersection++;
  }
  
  const union = new Set([...a, ...b]).size;
  return intersection / union;
}

// ═══════════════════════════════════════════════════════════════════════════
// KEYTRIPLET GENERATION
// ═══════════════════════════════════════════════════════════════════════════

/**
 * KeyTriplet: Complete AlephNet identity
 */
export interface KeyTriplet {
  pub: Base64;
  priv: Base64;
  resonance: SMFVector;
  fingerprint: string;
  bodyPrimes: number[];
}

/**
 * Generate a complete KeyTriplet identity
 */
export function generateKeyTriplet(): KeyTriplet {
  const keyPair = generateEd25519KeyPair();
  const resonance = computeResonanceField(keyPair.publicKey);
  const fingerprint = generateFingerprint(keyPair.publicKey, resonance);
  const bodyPrimes = selectBodyPrimes(keyPair.publicKey);
  
  return {
    pub: keyPair.publicKeyBase64,
    priv: keyPair.privateKeyBase64,
    resonance,
    fingerprint,
    bodyPrimes
  };
}

/**
 * Reconstruct a KeyTriplet from stored keys (without private key)
 */
export function reconstructKeyTriplet(publicKeyBase64: Base64): Omit<KeyTriplet, 'priv'> {
  const publicKey = base64ToBuffer(publicKeyBase64);
  const resonance = computeResonanceField(publicKey);
  const fingerprint = generateFingerprint(publicKey, resonance);
  const bodyPrimes = selectBodyPrimes(publicKey);
  
  return {
    pub: publicKeyBase64,
    resonance,
    fingerprint,
    bodyPrimes
  };
}
