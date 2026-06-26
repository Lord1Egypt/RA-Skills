const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const crypto = require('crypto');
const {
  ALGORITHM,
  KEY_BYTES,
  IV_BYTES,
  TAG_BYTES,
  generateKey,
  encrypt,
  decrypt,
  pack,
  unpack,
} = require('../src/gep/crypto');

describe('constants', () => {
  it('exposes AES-256-GCM algorithm', () => {
    assert.equal(ALGORITHM, 'aes-256-gcm');
  });

  it('defines 32-byte keys, 12-byte IVs, 16-byte tags', () => {
    assert.equal(KEY_BYTES, 32);
    assert.equal(IV_BYTES, 12);
    assert.equal(TAG_BYTES, 16);
  });
});

describe('generateKey', () => {
  it('returns a 32-byte Buffer', () => {
    const k = generateKey();
    assert.ok(Buffer.isBuffer(k));
    assert.equal(k.length, KEY_BYTES);
  });

  it('returns different keys on successive calls', () => {
    const a = generateKey();
    const b = generateKey();
    assert.notEqual(a.toString('hex'), b.toString('hex'));
  });
});

describe('encrypt / decrypt round-trip', () => {
  it('round-trips an ASCII string', () => {
    const key = generateKey();
    const plaintext = 'hello evolver';
    const parts = encrypt(plaintext, key);
    const recovered = decrypt(parts.ciphertext, key, parts.iv, parts.authTag);
    assert.equal(recovered.toString('utf8'), plaintext);
  });

  it('round-trips a multi-byte UTF-8 string', () => {
    const key = generateKey();
    const plaintext = 'evolver 演进 🧬 multi-byte';
    const parts = encrypt(plaintext, key);
    const recovered = decrypt(parts.ciphertext, key, parts.iv, parts.authTag);
    assert.equal(recovered.toString('utf8'), plaintext);
  });

  it('round-trips a binary Buffer', () => {
    const key = generateKey();
    const plaintext = crypto.randomBytes(1024);
    const parts = encrypt(plaintext, key);
    const recovered = decrypt(parts.ciphertext, key, parts.iv, parts.authTag);
    assert.equal(Buffer.compare(recovered, plaintext), 0);
  });

  it('round-trips an empty buffer', () => {
    const key = generateKey();
    const parts = encrypt(Buffer.alloc(0), key);
    const recovered = decrypt(parts.ciphertext, key, parts.iv, parts.authTag);
    assert.equal(recovered.length, 0);
  });

  it('produces a fresh IV per call (non-deterministic ciphertext)', () => {
    const key = generateKey();
    const a = encrypt('same input', key);
    const b = encrypt('same input', key);
    assert.notEqual(a.iv.toString('hex'), b.iv.toString('hex'));
    assert.notEqual(a.ciphertext.toString('hex'), b.ciphertext.toString('hex'));
  });

  it('returns components with expected lengths', () => {
    const key = generateKey();
    const { iv, authTag, ciphertext } = encrypt('abc', key);
    assert.equal(iv.length, IV_BYTES);
    assert.equal(authTag.length, TAG_BYTES);
    assert.equal(ciphertext.length, Buffer.byteLength('abc', 'utf8'));
  });
});

describe('encrypt key validation', () => {
  it('rejects missing key', () => {
    assert.throws(() => encrypt('x', null), /key must be exactly 32 bytes/);
  });

  it('rejects too-short key', () => {
    assert.throws(() => encrypt('x', Buffer.alloc(16)), /key must be exactly 32 bytes/);
  });

  it('rejects too-long key', () => {
    assert.throws(() => encrypt('x', Buffer.alloc(64)), /key must be exactly 32 bytes/);
  });
});

describe('decrypt key validation', () => {
  it('rejects missing key', () => {
    const key = generateKey();
    const parts = encrypt('x', key);
    assert.throws(
      () => decrypt(parts.ciphertext, null, parts.iv, parts.authTag),
      /key must be exactly 32 bytes/
    );
  });

  it('rejects wrong-size key', () => {
    const key = generateKey();
    const parts = encrypt('x', key);
    assert.throws(
      () => decrypt(parts.ciphertext, Buffer.alloc(16), parts.iv, parts.authTag),
      /key must be exactly 32 bytes/
    );
  });
});

describe('decrypt authentication', () => {
  it('fails when ciphertext is tampered', () => {
    const key = generateKey();
    const parts = encrypt('trusted payload', key);
    const tampered = Buffer.from(parts.ciphertext);
    tampered[0] ^= 0xff;
    assert.throws(() => decrypt(tampered, key, parts.iv, parts.authTag));
  });

  it('fails when auth tag is tampered', () => {
    const key = generateKey();
    const parts = encrypt('trusted payload', key);
    const tag = Buffer.from(parts.authTag);
    tag[0] ^= 0xff;
    assert.throws(() => decrypt(parts.ciphertext, key, parts.iv, tag));
  });

  it('fails when decrypted with a different key', () => {
    const keyA = generateKey();
    const keyB = generateKey();
    const parts = encrypt('secret', keyA);
    assert.throws(() => decrypt(parts.ciphertext, keyB, parts.iv, parts.authTag));
  });

  it('fails when IV is wrong', () => {
    const key = generateKey();
    const parts = encrypt('secret', key);
    const badIv = crypto.randomBytes(IV_BYTES);
    assert.throws(() => decrypt(parts.ciphertext, key, badIv, parts.authTag));
  });
});

describe('pack / unpack', () => {
  it('pack produces iv || authTag || ciphertext layout', () => {
    const key = generateKey();
    const parts = encrypt('payload', key);
    const packed = pack(parts);
    assert.ok(Buffer.isBuffer(packed));
    assert.equal(packed.length, IV_BYTES + TAG_BYTES + parts.ciphertext.length);
    assert.equal(
      packed.subarray(0, IV_BYTES).toString('hex'),
      parts.iv.toString('hex')
    );
    assert.equal(
      packed.subarray(IV_BYTES, IV_BYTES + TAG_BYTES).toString('hex'),
      parts.authTag.toString('hex')
    );
  });

  it('unpack reverses pack', () => {
    const key = generateKey();
    const parts = encrypt('payload', key);
    const roundTripped = unpack(pack(parts));
    assert.equal(roundTripped.iv.toString('hex'), parts.iv.toString('hex'));
    assert.equal(roundTripped.authTag.toString('hex'), parts.authTag.toString('hex'));
    assert.equal(
      roundTripped.ciphertext.toString('hex'),
      parts.ciphertext.toString('hex')
    );
  });

  it('pack + unpack + decrypt composes with encrypt', () => {
    const key = generateKey();
    const plaintext = 'end-to-end transport test';
    const packed = pack(encrypt(plaintext, key));
    const parts = unpack(packed);
    const recovered = decrypt(parts.ciphertext, key, parts.iv, parts.authTag);
    assert.equal(recovered.toString('utf8'), plaintext);
  });

  it('unpack rejects non-Buffer input', () => {
    assert.throws(() => unpack('not a buffer'), /packed buffer too short/);
    assert.throws(() => unpack(null), /packed buffer too short/);
  });

  it('unpack rejects buffer smaller than iv + tag + 1', () => {
    assert.throws(
      () => unpack(Buffer.alloc(IV_BYTES + TAG_BYTES)),
      /packed buffer too short/
    );
  });

  it('unpack accepts minimal-size buffer (1 ciphertext byte)', () => {
    const buf = Buffer.alloc(IV_BYTES + TAG_BYTES + 1);
    const parts = unpack(buf);
    assert.equal(parts.iv.length, IV_BYTES);
    assert.equal(parts.authTag.length, TAG_BYTES);
    assert.equal(parts.ciphertext.length, 1);
  });
});
