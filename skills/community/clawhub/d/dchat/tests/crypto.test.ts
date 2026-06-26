import { describe, it, expect } from "vitest";
import { encrypt, decrypt } from "../src/crypto.js";

describe("AES-128-GCM crypto", () => {
  it("encrypts and decrypts a buffer", () => {
    const plaintext = Buffer.from("hello decentralized world");
    const { ciphertext, key } = encrypt(plaintext);

    // Ciphertext should be nonce(12) + encrypted + authTag(16)
    expect(ciphertext.length).toBeGreaterThan(12 + 16);

    const decrypted = decrypt(ciphertext, key);
    expect(decrypted.toString()).toBe("hello decentralized world");
  });

  it("rejects tampered ciphertext", () => {
    const plaintext = Buffer.from("sensitive data");
    const { ciphertext, key } = encrypt(plaintext);

    // Tamper with a byte in the encrypted data
    ciphertext[15] ^= 0xff;

    expect(() => decrypt(ciphertext, key)).toThrow();
  });

  it("rejects wrong key", () => {
    const plaintext = Buffer.from("secret");
    const { ciphertext } = encrypt(plaintext);
    const wrongKey = Buffer.alloc(16, 0);

    expect(() => decrypt(ciphertext, wrongKey)).toThrow();
  });

  it("produces different ciphertext for same plaintext", () => {
    const plaintext = Buffer.from("determinism test");
    const r1 = encrypt(plaintext);
    const r2 = encrypt(plaintext);

    expect(r1.ciphertext).not.toEqual(r2.ciphertext);
    expect(r1.key).not.toEqual(r2.key);
  });

  it("handles empty buffer", () => {
    const plaintext = Buffer.alloc(0);
    const { ciphertext, key } = encrypt(plaintext);
    const decrypted = decrypt(ciphertext, key);
    expect(decrypted.length).toBe(0);
  });

  it("handles large buffer", () => {
    const plaintext = Buffer.alloc(1024 * 1024, 0xab); // 1MB
    const { ciphertext, key } = encrypt(plaintext);
    const decrypted = decrypt(ciphertext, key);
    expect(decrypted).toEqual(plaintext);
  });

  it("key bytes roundtrip through number array (nMobile format)", () => {
    const plaintext = Buffer.from("nMobile compatibility test");
    const { ciphertext, key } = encrypt(plaintext);

    // Simulate nMobile wire format: key as number[]
    const keyBytes: number[] = Array.from(key);
    const restoredKey = Buffer.from(keyBytes);

    const decrypted = decrypt(ciphertext, restoredKey);
    expect(decrypted.toString()).toBe("nMobile compatibility test");
  });
});
