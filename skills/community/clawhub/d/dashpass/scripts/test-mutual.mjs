#!/usr/bin/env node
/**
 * test-mutual.mjs
 * End-to-end tests for DashPass Mutual Confirmation Protocol.
 * Runs entirely offline — no SDK or network access required.
 *
 * Usage: node test-mutual.mjs
 */

import {
  createHash,
  createECDH,
  hkdfSync,
  createCipheriv,
  randomBytes,
} from 'node:crypto';
import { existsSync, readFileSync, unlinkSync, mkdirSync, chmodSync, statSync } from 'node:fs';
import { homedir } from 'node:os';
import { join } from 'node:path';

import {
  gf256Mul,
  gf256Inv,
  L1_COEFF,
  L2_COEFF,
  splitKey,
  combineShares,
  storeShares,
  readShareA,
  readShareB,
  sharesExist,
  shareStatus,
  requestDecrypt,
  approveDecrypt,
  denyDecrypt,
  executeDecrypt,
  auditLog,
  DASHPASS_DIR,
  SHARE_A_PATH,
  SHARE_B_PATH,
  AUDIT_LOG_PATH,
} from './mutual-confirm.mjs';

// ── Test harness ─────────────────────────────────────────────────────────────

let passed = 0;
let failed = 0;
const failures = [];

function assert(condition, message) {
  if (condition) {
    passed++;
    console.log(`  PASS: ${message}`);
  } else {
    failed++;
    failures.push(message);
    console.log(`  FAIL: ${message}`);
  }
}

function assertEq(actual, expected, message) {
  const ok = actual === expected;
  if (!ok) {
    message += ` (got ${JSON.stringify(actual)}, expected ${JSON.stringify(expected)})`;
  }
  assert(ok, message);
}

function assertThrows(fn, message) {
  let threw = false;
  try { fn(); } catch { threw = true; }
  assert(threw, message);
}

// ── Helper: encrypt like Scheme C (for testing executeDecrypt) ───────────────

function testEncrypt(privKeyBytes, payload) {
  const salt  = randomBytes(32);
  const nonce = randomBytes(12);
  const ecdh  = createECDH('secp256k1');
  ecdh.setPrivateKey(privKeyBytes);
  const sharedSecret = ecdh.computeSecret(ecdh.getPublicKey());
  const aesKey = Buffer.from(hkdfSync('sha256', sharedSecret, salt, 'dashpass-v1', 32));
  const cipher = createCipheriv('aes-256-gcm', aesKey, nonce);
  const plain  = Buffer.from(JSON.stringify(payload), 'utf8');
  const ct     = Buffer.concat([cipher.update(plain), cipher.final()]);
  const tag    = cipher.getAuthTag();
  aesKey.fill(0);
  return { encryptedBlob: Buffer.concat([ct, tag]), salt, nonce };
}

// ── Cleanup helper ───────────────────────────────────────────────────────────

function cleanupShares() {
  for (const p of [SHARE_A_PATH, SHARE_B_PATH]) {
    try { unlinkSync(p); } catch { /* ok */ }
  }
}

function cleanupAuditLog() {
  try { unlinkSync(AUDIT_LOG_PATH); } catch { /* ok */ }
}

// ══════════════════════════════════════════════════════════════════════════════
//  TEST SUITES
// ══════════════════════════════════════════════════════════════════════════════

console.log('\n=== DashPass Mutual Confirmation Protocol — Tests ===\n');

// ── 1. GF(256) Math ─────────────────────────────────────────────────────────

console.log('1. GF(256) arithmetic');

// Identity
assertEq(gf256Mul(1, 1), 1, 'gf256Mul(1,1) = 1');
assertEq(gf256Mul(0, 42), 0, 'gf256Mul(0,x) = 0');
assertEq(gf256Mul(42, 0), 0, 'gf256Mul(x,0) = 0');
assertEq(gf256Mul(1, 0x53), 0x53, 'gf256Mul(1,x) = x');

// Known vector: 0x53 * 0xCA = 0x01 in GF(256) with 0x11d
// (0x53 and 0xCA are multiplicative inverses under AES's polynomial)
// Let's verify with our polynomial 0x11d instead.
// Commutativity
assertEq(gf256Mul(7, 11), gf256Mul(11, 7), 'gf256Mul is commutative');

// Inverse
assertEq(gf256Mul(3, gf256Inv(3)), 1, 'gf256Mul(3, gf256Inv(3)) = 1');
assertEq(gf256Mul(0xff, gf256Inv(0xff)), 1, 'gf256Mul(255, gf256Inv(255)) = 1');
assertEq(gf256Mul(42, gf256Inv(42)), 1, 'gf256Mul(42, gf256Inv(42)) = 1');

// Inverse of 1
assertEq(gf256Inv(1), 1, 'gf256Inv(1) = 1');

// Zero inversion should throw
assertThrows(() => gf256Inv(0), 'gf256Inv(0) throws');

// Lagrange coefficients sanity: L1 + L2 should reconstruct identity
// For a constant polynomial f(x) = c: f(1) = c, f(2) = c
// Reconstruction: c*L1 XOR c*L2 should equal c
for (const c of [0, 1, 42, 0xff]) {
  const reconstructed = gf256Mul(c, L1_COEFF) ^ gf256Mul(c, L2_COEFF);
  assertEq(reconstructed, c, `Lagrange identity for constant ${c}`);
}

console.log('');

// ── 2. Shamir split/combine round-trip ──────────────────────────────────────

console.log('2. Shamir split/combine round-trip');

// 32-byte key (typical AES key / private key size)
const testKey32 = randomBytes(32);
const { shareA: sA32, shareB: sB32 } = splitKey(testKey32);
const recovered32 = combineShares(sA32, sB32);
assert(recovered32.equals(testKey32), '32-byte key round-trip');
recovered32.fill(0);

// 1-byte key
const testKey1 = Buffer.from([0x42]);
const { shareA: sA1, shareB: sB1 } = splitKey(testKey1);
const recovered1 = combineShares(sA1, sB1);
assert(recovered1.equals(testKey1), '1-byte key round-trip');

// All-zeros key
const testKey0s = Buffer.alloc(32, 0);
const { shareA: sA0, shareB: sB0 } = splitKey(testKey0s);
const recovered0s = combineShares(sA0, sB0);
assert(recovered0s.equals(testKey0s), 'All-zeros key round-trip');

// All-ones key
const testKeyFFs = Buffer.alloc(32, 0xff);
const { shareA: sAFF, shareB: sBFF } = splitKey(testKeyFFs);
const recoveredFF = combineShares(sAFF, sBFF);
assert(recoveredFF.equals(testKeyFFs), 'All-0xFF key round-trip');

// Different splits of same key produce different shares (randomness test)
const { shareA: sA32b } = splitKey(testKey32);
assert(sA32 !== sA32b, 'Different splits produce different shares (randomness)');

// Wrong share order should NOT reconstruct correctly (in general)
const wrongOrder = combineShares(sB32, sA32);
assert(!wrongOrder.equals(testKey32), 'Swapped shares do not reconstruct key');

// Shares are hex strings of expected length
assertEq(sA32.length, 64, 'Share A is 64 hex chars for 32-byte key');
assertEq(sB32.length, 64, 'Share B is 64 hex chars for 32-byte key');
assert(/^[0-9a-f]+$/.test(sA32), 'Share A is valid hex');
assert(/^[0-9a-f]+$/.test(sB32), 'Share B is valid hex');

// Error cases
assertThrows(() => splitKey(Buffer.alloc(0)), 'splitKey rejects empty buffer');
assertThrows(() => splitKey('not a buffer'), 'splitKey rejects non-buffer');
assertThrows(() => combineShares('aa', 'bbcc'), 'combineShares rejects mismatched lengths');
assertThrows(() => combineShares('', ''), 'combineShares rejects empty shares');

console.log('');

// ── 3. Share file I/O ───────────────────────────────────────────────────────

console.log('3. Share file I/O');

cleanupShares();

assert(!sharesExist(), 'sharesExist() returns false when no files');

const testShareA = 'a'.repeat(64);
const testShareB = 'b'.repeat(64);
storeShares(testShareA, testShareB);

assert(sharesExist(), 'sharesExist() returns true after store');
assertEq(readShareA(), testShareA, 'readShareA() returns stored value');
assertEq(readShareB(), testShareB, 'readShareB() returns stored value');

// Check file permissions (0600)
const statA = statSync(SHARE_A_PATH);
const statB = statSync(SHARE_B_PATH);
assertEq((statA.mode & 0o777).toString(8), '600', 'evo.share has 0600 permissions');
assertEq((statB.mode & 0o777).toString(8), '600', 'cc.share has 0600 permissions');

// shareStatus health check
const status = shareStatus();
assert(status.evo.exists, 'shareStatus: evo exists');
assert(status.cc.exists, 'shareStatus: cc exists');
assert(status.evo.healthy, 'shareStatus: evo healthy');
assert(status.cc.healthy, 'shareStatus: cc healthy');
assertEq(status.evo.bytes, 32, 'shareStatus: evo reports 32 bytes');
assertEq(status.evo.permissions, '0600', 'shareStatus: evo permissions 0600');

cleanupShares();

console.log('');

// ── 4. Mutual decryption (executeDecrypt) ───────────────────────────────────

console.log('4. executeDecrypt with Scheme C data');

// Generate a test private key and encrypt some data
const testPrivKey = randomBytes(32);
const testPayload = { value: 'sk-test-mutual-secret-12345' };
const { encryptedBlob, salt, nonce } = testEncrypt(testPrivKey, testPayload);

// Split the private key
const { shareA: decShareA, shareB: decShareB } = splitKey(testPrivKey);
testPrivKey.fill(0); // Zero original

// Decrypt using shares
const decrypted = executeDecrypt(decShareA, decShareB, encryptedBlob, salt, nonce);
assertEq(decrypted.value, testPayload.value, 'executeDecrypt returns correct plaintext');

// Wrong shares should fail
const badShareA = 'ff'.repeat(32);
assertThrows(
  () => executeDecrypt(badShareA, decShareB, encryptedBlob, salt, nonce),
  'executeDecrypt fails with wrong share A',
);

console.log('');

// ── 5. Memory zeroing ───────────────────────────────────────────────────────

console.log('5. Memory zeroing verification');

// Test that combineShares output can be zeroed
const zeroTestKey = randomBytes(32);
const { shareA: zShareA, shareB: zShareB } = splitKey(zeroTestKey);
const reconstructed = combineShares(zShareA, zShareB);
assert(reconstructed.equals(zeroTestKey), 'Pre-zero: key matches');
reconstructed.fill(0);
assert(reconstructed.every(b => b === 0), 'Buffer.fill(0) zeroes all bytes');
assert(!reconstructed.equals(zeroTestKey), 'Zeroed buffer no longer matches key');

// Test that splitKey zeroes its internal coefficients
// (We can't directly observe internal state, but we verify the API contract:
//  the function returns and the output is valid, implying cleanup happened.)
const zKey2 = randomBytes(32);
const { shareA: zs2A, shareB: zs2B } = splitKey(zKey2);
const rec2 = combineShares(zs2A, zs2B);
assert(rec2.equals(zKey2), 'splitKey internal cleanup did not corrupt output');

console.log('');

// ── 6. Audit log ────────────────────────────────────────────────────────────

console.log('6. Audit log format');

cleanupAuditLog();

// Trigger protocol steps that write to audit log
const req = requestDecrypt('test-service', 'unit test', 'cc');
assertEq(req.status, 'pending', 'Request status is pending');
assertEq(req.credentialName, 'test-service', 'Request has credentialName');
assert(req.id.length === 32, 'Request id is 32 hex chars');

const approval = approveDecrypt(req, 'evo');
assertEq(approval.status, 'approved', 'Approval status is approved');
assertEq(approval.approver, 'evo', 'Approval has approver');

const denial = denyDecrypt(req, 'evo', 'test denial');
assertEq(denial.status, 'denied', 'Denial status is denied');

// Read and validate audit log entries
assert(existsSync(AUDIT_LOG_PATH), 'Audit log file exists');
const logLines = readFileSync(AUDIT_LOG_PATH, 'utf8').trim().split('\n');
assert(logLines.length >= 3, `Audit log has >= 3 entries (got ${logLines.length})`);

for (const line of logLines) {
  const entry = JSON.parse(line);
  assert(typeof entry.timestamp === 'string', `Audit entry has timestamp`);
  assert(typeof entry.action === 'string', `Audit entry has action`);
  // Verify no key/share material in log
  assert(!line.includes(testShareA), 'Audit log does not contain share A');
  assert(!line.includes(testShareB), 'Audit log does not contain share B');
}

// Verify specific actions were logged
const actions = logLines.map(l => JSON.parse(l).action);
assert(actions.includes('request'), 'Audit log has request action');
assert(actions.includes('approve'), 'Audit log has approve action');
assert(actions.includes('deny'), 'Audit log has deny action');

cleanupAuditLog();

console.log('');

// ── 7. Backward compatibility ───────────────────────────────────────────────

console.log('7. Backward compatibility');

// Without shares, sharesExist returns false
cleanupShares();
assert(!sharesExist(), 'No shares after cleanup — Scheme C path available');

// shareStatus gracefully reports missing
const missingStatus = shareStatus();
assert(!missingStatus.evo.exists, 'shareStatus: evo missing after cleanup');
assert(!missingStatus.cc.exists, 'shareStatus: cc missing after cleanup');

console.log('');

// ── 8. GF(256) known test vectors ──────────────────────────────────────────

console.log('8. GF(256) known test vectors');

// Verify multiplication against manually computed values:
// In GF(2^8) with polynomial 0x11d:
//   2 * 2 = 4 (no reduction needed, 0x04 < 0x100)
assertEq(gf256Mul(2, 2), 4, '2*2 = 4');
//   2 * 128 = 256, but 256 >= 256 so XOR with 0x11d:
//   256 ^ 0x11d = 0x100 ^ 0x11d = 0x01d = 29
assertEq(gf256Mul(2, 128), 0x100 ^ 0x11d, '2*128 reduces mod 0x11d');
//   Associativity: (a*b)*c = a*(b*c)
const a = 0x57, b = 0x83, c = 0x1b;
assertEq(gf256Mul(gf256Mul(a, b), c), gf256Mul(a, gf256Mul(b, c)), 'Associativity');
//   Distributivity: a*(b^c) = (a*b)^(a*c)
assertEq(gf256Mul(a, b ^ c), gf256Mul(a, b) ^ gf256Mul(a, c), 'Distributivity');

// All non-zero elements should have inverses
let allInverses = true;
for (let i = 1; i <= 255; i++) {
  if (gf256Mul(i, gf256Inv(i)) !== 1) {
    allInverses = false;
    break;
  }
}
assert(allInverses, 'All 255 non-zero elements have valid inverses');

console.log('');

// ── 9. Stress: many round-trips ─────────────────────────────────────────────

console.log('9. Stress test: 100 random key round-trips');

let stressOk = true;
for (let i = 0; i < 100; i++) {
  const key = randomBytes(32);
  const { shareA, shareB } = splitKey(key);
  const rec = combineShares(shareA, shareB);
  if (!rec.equals(key)) {
    stressOk = false;
    break;
  }
}
assert(stressOk, '100 random 32-byte key round-trips all pass');

console.log('');

// ══════════════════════════════════════════════════════════════════════════════
//  SUMMARY
// ══════════════════════════════════════════════════════════════════════════════

// Final cleanup
cleanupShares();
cleanupAuditLog();

console.log('═'.repeat(60));
console.log(`  Results: ${passed} passed, ${failed} failed`);
if (failures.length > 0) {
  console.log('  Failures:');
  for (const f of failures) console.log(`    - ${f}`);
}
console.log('═'.repeat(60));

process.exit(failed > 0 ? 1 : 0);
