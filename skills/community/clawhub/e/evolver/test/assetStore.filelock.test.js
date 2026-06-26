'use strict';

// Regression tests for the v1.69.8 file-lock hardening of assetStore.
// See GH issue #451 (H3 — race condition in concurrent upsertGene /
// appendCapsule / upsertCapsule / appendFailedCapsule).

const test = require('node:test');
const assert = require('node:assert');
const os = require('node:os');
const fs = require('node:fs');
const path = require('node:path');

const { withFileLock } = require('../src/gep/assetStore');

test('withFileLock serializes critical sections on the same target', async () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'evolver-lock-'));
  const target = path.join(dir, 'target.json');
  let active = 0;
  let maxActive = 0;
  const enter = () => {
    active += 1;
    if (active > maxActive) maxActive = active;
  };
  const leave = () => {
    active -= 1;
  };
  const jobs = Array.from({ length: 20 }).map(() => new Promise((resolve, reject) => {
    setTimeout(() => {
      try {
        withFileLock(target, () => {
          enter();
          const start = Date.now();
          while (Date.now() - start < 15) { /* hold the lock briefly */ }
          leave();
        });
        resolve();
      } catch (e) {
        reject(e);
      }
    }, 0);
  }));
  await Promise.all(jobs);
  assert.strictEqual(maxActive, 1, 'critical section must never overlap');
});

test('withFileLock releases the lock even when the callback throws', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'evolver-lock-'));
  const target = path.join(dir, 'target.json');
  assert.throws(() => {
    withFileLock(target, () => {
      throw new Error('boom');
    });
  }, /boom/);
  let entered = false;
  withFileLock(target, () => {
    entered = true;
  });
  assert.ok(entered, 'must be able to re-acquire after a throwing callback');
});
