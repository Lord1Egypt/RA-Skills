import crypto from "crypto";
import fs from "fs";
import path from "path";

const ALGORITHM = "aes-256-gcm";
const KEY_BYTES = 32;
const SALT_BYTES = 16;
const NONCE_BYTES = 12;
const AUTH_TAG_BYTES = 16;
const PBKDF2_ITERATIONS = 100_000;

/**
 * Safe storage for bot identity (seed + address).
 * Encrypts data at rest using AES-256-GCM with a PBKDF2-derived key.
 *
 * File format: [salt 16B] [nonce 12B] [ciphertext] [authTag 16B]
 * Plaintext is JSON: { seed, address }
 */
export interface StoredIdentity {
  seed: string;
  address: string;
}

export class SafeStorage {
  private filePath: string;

  constructor(dataDir: string, fileName = "identity.enc") {
    fs.mkdirSync(dataDir, { recursive: true });
    this.filePath = path.join(dataDir, fileName);
  }

  /** Save seed and address encrypted with passphrase. */
  save(identity: StoredIdentity, passphrase: string): void {
    const plaintext = Buffer.from(JSON.stringify(identity), "utf-8");
    const salt = crypto.randomBytes(SALT_BYTES);
    const key = crypto.pbkdf2Sync(passphrase, salt, PBKDF2_ITERATIONS, KEY_BYTES, "sha256");
    const nonce = crypto.randomBytes(NONCE_BYTES);

    const cipher = crypto.createCipheriv(ALGORITHM, key, nonce);
    const encrypted = Buffer.concat([cipher.update(plaintext), cipher.final()]);
    const authTag = cipher.getAuthTag();

    // [salt][nonce][ciphertext][authTag]
    const output = Buffer.concat([salt, nonce, encrypted, authTag]);
    fs.writeFileSync(this.filePath, output, { mode: 0o600 });
  }

  /** Load and decrypt identity. Returns null if file doesn't exist. */
  load(passphrase: string): StoredIdentity | null {
    if (!fs.existsSync(this.filePath)) return null;

    const data = fs.readFileSync(this.filePath);
    const salt = data.subarray(0, SALT_BYTES);
    const nonce = data.subarray(SALT_BYTES, SALT_BYTES + NONCE_BYTES);
    const ciphertextWithTag = data.subarray(SALT_BYTES + NONCE_BYTES);
    const encrypted = ciphertextWithTag.subarray(0, ciphertextWithTag.length - AUTH_TAG_BYTES);
    const authTag = ciphertextWithTag.subarray(ciphertextWithTag.length - AUTH_TAG_BYTES);

    const key = crypto.pbkdf2Sync(passphrase, salt, PBKDF2_ITERATIONS, KEY_BYTES, "sha256");
    const decipher = crypto.createDecipheriv(ALGORITHM, key, nonce);
    decipher.setAuthTag(authTag);

    const plaintext = Buffer.concat([decipher.update(encrypted), decipher.final()]);
    return JSON.parse(plaintext.toString("utf-8")) as StoredIdentity;
  }

  /** Check if an identity file exists. */
  exists(): boolean {
    return fs.existsSync(this.filePath);
  }

  /** Delete the identity file. */
  delete(): void {
    if (fs.existsSync(this.filePath)) fs.unlinkSync(this.filePath);
  }

  getFilePath(): string {
    return this.filePath;
  }
}
