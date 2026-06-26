/**
 * AES-256-GCM card details encryption.
 *
 * Storage format (details_encrypted column):
 *   [version: 1 byte] [iv: 12 bytes] [authTag: 16 bytes] [ciphertext: N bytes]
 *
 * version = 0x01 (allows future migration to different algo/KMS)
 */
import crypto from "node:crypto";
import type { CardDetails } from "../types/domain";

const CURRENT_VERSION = 0x01;
const IV_LENGTH = 12;
const AUTH_TAG_LENGTH = 16;
const KEY_LENGTH = 32; // AES-256

/**
 * Decode and validate CARD_DETAILS_KEY.
 * Expects base64-encoded 32 random bytes.
 * Fail-fast if key is invalid.
 */
export function parseEncryptionKey(base64Key: string): Buffer {
    const keyBuf = Buffer.from(base64Key, "base64");
    if (keyBuf.length !== KEY_LENGTH) {
        throw new Error(
            `CARD_DETAILS_KEY must be exactly ${KEY_LENGTH} bytes (got ${keyBuf.length}). ` +
            `Generate with: node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"`
        );
    }
    return keyBuf;
}

/**
 * Encrypt CardDetails to a versioned binary blob.
 */
export function encryptCardDetails(
    details: CardDetails,
    key: Buffer
): Buffer {
    const plaintext = Buffer.from(JSON.stringify(details), "utf-8");
    const iv = crypto.randomBytes(IV_LENGTH);

    const cipher = crypto.createCipheriv("aes-256-gcm", key, iv);
    const encrypted = Buffer.concat([cipher.update(plaintext), cipher.final()]);
    const authTag = cipher.getAuthTag();

    // [version(1)] [iv(12)] [authTag(16)] [ciphertext(N)]
    return Buffer.concat([
        Buffer.from([CURRENT_VERSION]),
        iv,
        authTag,
        encrypted
    ]);
}

/**
 * Decrypt a versioned binary blob back to CardDetails.
 */
export function decryptCardDetails(
    blob: Buffer,
    key: Buffer
): CardDetails {
    if (blob.length < 1 + IV_LENGTH + AUTH_TAG_LENGTH) {
        throw new Error("Encrypted blob too short");
    }

    const version = blob[0];
    if (version !== CURRENT_VERSION) {
        throw new Error(`Unsupported encryption version: ${version}`);
    }

    const iv = blob.subarray(1, 1 + IV_LENGTH);
    const authTag = blob.subarray(1 + IV_LENGTH, 1 + IV_LENGTH + AUTH_TAG_LENGTH);
    const ciphertext = blob.subarray(1 + IV_LENGTH + AUTH_TAG_LENGTH);

    const decipher = crypto.createDecipheriv("aes-256-gcm", key, iv);
    decipher.setAuthTag(authTag);

    const plaintext = Buffer.concat([
        decipher.update(ciphertext),
        decipher.final()
    ]);

    return JSON.parse(plaintext.toString("utf-8")) as CardDetails;
}
