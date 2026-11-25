// Read Navos desktop identity (uid, token, email) from local files / env vars.
//
// Resolution order (first hit wins):
//   1. Env vars: NAVOS_UID + NAVOS_TOKEN (+ NAVOS_EMAIL / NAVOS_APP_ID optional)
//      Override mechanism for tests / non-standard installs.
//   2. Identity file: NAVOS_IDENTITY_FILE env var, or ~/.navos/identity/navos-userinfo.json
//      The same path used by the navos-mcp skill, so we stay consistent with whatever
//      the desktop client writes there.
//
// File schema (best effort - the Navos client may evolve):
//   {
//     "uid":   "...",        // required
//     "token": "...",        // required
//     "email": "user@...",   // optional, falls back to "<uid>@navos.local"
//     "app_id": "navos-global" | "navos-cn" // optional, defaults downstream to navos-global
//     ...
//   }
//
// We DO NOT print token to stdout/stderr. Errors carry a high-level reason only.

import { existsSync, readFileSync } from 'node:fs';
import { homedir } from 'node:os';
import { join } from 'node:path';

const FALLBACK_EMAIL_DOMAIN = 'navos.local';

/**
 * Resolve the identity file path (override > default).
 * @returns {string}
 */
function resolveIdentityPath() {
  const override = process.env.NAVOS_IDENTITY_FILE;
  if (override && override.trim()) {
    return override.trim();
  }
  return join(homedir(), '.navos', 'identity', 'navos-userinfo.json');
}

/**
 * Load Navos identity for the currently logged-in desktop user.
 *
 * @returns {{uid: string, token: string, email: string, appId: string, source: 'env' | 'file', filePath?: string}}
 * @throws {Error} when neither env vars nor identity file provide a complete record.
 */
export function loadNavosIdentity() {
  // 1) Env-var override path
  const envUid = (process.env.NAVOS_UID || '').trim();
  const envToken = (process.env.NAVOS_TOKEN || '').trim();
  if (envUid && envToken) {
    const envEmail = (process.env.NAVOS_EMAIL || '').trim()
      || `${envUid}@${FALLBACK_EMAIL_DOMAIN}`;
    return {
      uid: envUid,
      token: envToken,
      email: envEmail,
      appId: (process.env.NAVOS_APP_ID || '').trim(),
      source: 'env',
    };
  }

  // 2) Identity file path
  const path = resolveIdentityPath();
  if (!existsSync(path)) {
    throw new Error(
      `Navos identity not found. Expected env vars NAVOS_UID + NAVOS_TOKEN, `
      + `or identity file at: ${path}. Please log in to Navos first.`,
    );
  }

  let raw;
  try {
    raw = readFileSync(path, 'utf8');
  } catch (err) {
    throw new Error(`Failed to read Navos identity file: ${err.code || err.name}`);
  }

  let data;
  try {
    data = JSON.parse(raw.replace(/^\uFEFF/, ''));
  } catch {
    throw new Error('Navos identity file is not valid JSON. Please re-login to Navos.');
  }

  const uid = typeof data?.uid === 'string' ? data.uid.trim() : '';
  const token = typeof data?.token === 'string' ? data.token.trim() : '';
  if (!uid || !token) {
    throw new Error(
      'Navos identity file is missing uid or token. Please re-login to Navos.',
    );
  }

  const fileEmail = typeof data?.email === 'string' ? data.email.trim() : '';
  const email = fileEmail || `${uid}@${FALLBACK_EMAIL_DOMAIN}`;
  const appId = typeof data?.app_id === 'string' ? data.app_id.trim() : '';

  return {
    uid,
    token,
    email,
    appId,
    source: 'file',
    filePath: path,
  };
}
