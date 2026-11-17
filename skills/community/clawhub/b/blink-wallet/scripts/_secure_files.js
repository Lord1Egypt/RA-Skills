'use strict';

/**
 * Secure filesystem primitives for ~/.blink state (security-audit fix).
 *
 * The audit found two standards of care in one codebase: l402-root-key was
 * written 0600 and the Spark state dir 0700-with-symlink-rejection, while
 * l402-tokens.json (macaroons + preimages — a REUSABLE BEARER CREDENTIAL
 * pair) was written umask-dependent (0644 in practice), and budget.json /
 * spending-log.json likewise. These helpers apply the strict pattern
 * everywhere and migrate pre-existing loose files on first touch.
 *
 * Rules:
 *   - ~/.blink is 0700, owned, and never a symlink.
 *   - Secret-bearing files are 0600, written atomically (temp + rename), and
 *     never through a symlink.
 *   - Pre-existing world/group-readable state files are tightened on load —
 *     a file that leaked under an old release stops leaking after upgrade.
 */

const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');

/** State files that must be 0600 whenever they exist. */
const SECURE_FILE_NAMES = ['l402-tokens.json', 'l402-root-key', 'budget.json', 'spending-log.json'];

/** State subdirectories that must be 0700 whenever they exist (FT6: the
 * pre-existing ~/.blink/spark — SDK wallet state keyed by seed hash — was
 * left 0775 by older installs while its parent was tightened). */
const SECURE_SUBDIR_NAMES = ['spark'];

const migratedDirs = new Set();

/**
 * Ensure a directory exists at mode 0700 and is not a symlink. Pre-existing
 * directories with looser modes are tightened (idempotent).
 *
 * @param {string} dir
 */
function ensureSecureDir(dir) {
  try {
    const st = fs.lstatSync(dir);
    if (st.isSymbolicLink()) {
      throw new Error(`Refusing to use '${dir}': it is a symlink.`);
    }
    if (!st.isDirectory()) {
      throw new Error(`Refusing to use '${dir}': not a directory.`);
    }
    fs.chmodSync(dir, 0o700);
  } catch (e) {
    if (e.code === 'ENOENT') {
      fs.mkdirSync(dir, { recursive: true, mode: 0o700 });
      // mkdir's mode is masked by umask — set it explicitly afterwards.
      fs.chmodSync(dir, 0o700);
    } else {
      throw e;
    }
  }
}

/**
 * Tighten the permissions of known state files inside a directory (one-time
 * per process per directory). Existing 0644-era files become 0600.
 *
 * @param {string} dir
 */
function migrateSecureFiles(dir) {
  if (migratedDirs.has(dir)) return;
  // NOTE: the dir is added to migratedDirs only AFTER both loops complete —
  // marking it up front would let one transient failure (e.g. EACCES on the
  // spark/ chmod) permanently disable hardening for the process, and the
  // read-path callers deliberately swallow best-effort hardening errors
  // (review round 2, PR #21).
  for (const name of SECURE_FILE_NAMES) {
    const file = path.join(dir, name);
    try {
      const st = fs.lstatSync(file);
      if (st.isSymbolicLink()) continue; // readers/writers must refuse it themselves
      if (st.isFile()) fs.chmodSync(file, 0o600);
    } catch (e) {
      if (e.code !== 'ENOENT') throw e;
    }
  }
  for (const name of SECURE_SUBDIR_NAMES) {
    const sub = path.join(dir, name);
    try {
      const st = fs.lstatSync(sub);
      if (st.isSymbolicLink()) continue;
      if (st.isDirectory()) fs.chmodSync(sub, 0o700);
    } catch (e) {
      if (e.code !== 'ENOENT') throw e;
    }
  }
  migratedDirs.add(dir);
}

/**
 * One-call security bootstrap for a state directory: 0700 dir + one-time
 * migration of known member files.
 *
 * @param {string} dir
 */
function ensureSecureStateDir(dir) {
  ensureSecureDir(dir);
  migrateSecureFiles(dir);
}

/**
 * Atomically write a file at mode 0600 (temp file + rename, never through a
 * symlink). The directory is ensured secure first.
 *
 * @param {string} file  absolute path to the target file
 * @param {string} content
 */
function writeSecureFileAtomic(file, content) {
  const dir = path.dirname(file);
  ensureSecureDir(dir);
  migrateSecureFiles(dir);
  try {
    const st = fs.lstatSync(file);
    if (st.isSymbolicLink()) {
      throw new Error(`Refusing to write through symlink '${file}'.`);
    }
  } catch (e) {
    if (e.code !== 'ENOENT') throw e;
  }
  // Unpredictable temp name, created EXCLUSIVELY (O_CREAT|O_EXCL via 'wx'),
  // which also refuses a pre-existing symlink (ClawHub 3.0.3 ClawScan note:
  // `<file>.<pid>.tmp` without exclusive creation let a planted symlink
  // redirect the write). A collision (EEXIST) just draws a new name.
  let tmp;
  for (let attempt = 0; ; attempt++) {
    tmp = `${file}.${crypto.randomBytes(12).toString('hex')}.tmp`;
    try {
      fs.writeFileSync(tmp, content, { mode: 0o600, flag: 'wx' });
      break;
    } catch (e) {
      if (e.code !== 'EEXIST' || attempt >= 4) throw e;
    }
  }
  // Belt for a pre-existing target created by an older release with looser
  // umask: rename preserves the OLD file's mode, so set it explicitly.
  try {
    fs.chmodSync(tmp, 0o600);
    fs.renameSync(tmp, file);
  } catch (e) {
    // Never leave a 0600 copy of the state behind (PR #27 review).
    try {
      fs.unlinkSync(tmp);
    } catch {
      /* already gone */
    }
    throw e;
  }
  fs.chmodSync(file, 0o600);
}

module.exports = {
  ensureSecureDir,
  migrateSecureFiles,
  ensureSecureStateDir,
  writeSecureFileAtomic,
  SECURE_FILE_NAMES,
  SECURE_SUBDIR_NAMES,
};
