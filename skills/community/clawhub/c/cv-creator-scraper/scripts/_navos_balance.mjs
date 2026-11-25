// Query Navos credit balance for the current Navos desktop user.
//
// Usage as a module:
//   import { checkNavosBalance } from './_navos_balance.mjs';
//   const { available_balance } = await checkNavosBalance({ uid });
//
// Configuration (resolution order, first hit wins):
//   - NAVOS_BASE_URL           explicit override (escape hatch).
//   - CV_API_BASE_URL          if it points at a *.tec-do.* host → use Navos prod;
//                              if it points at a *.tec-develop.* host → use Navos staging.
//   - default                  staging (dev01-...).
//   - NAVOS_BALANCE_TOKEN      X-Cm-Admin-Auth value; defaults to the shared
//                              external query token. Override via env if needed.
//
// Returns {total_balance, available_balance, raw} on success.
// Throws on network error / non-zero ret. Caller decides UX (block vs warn).

import { loadNavosIdentity } from './_navos_identity.mjs';
import { loadRuntimeProfile } from './_runtime_profile.mjs';

const NAVOS_CN_PROD_BASE_URL = 'https://navos-mind-server-vip-gz.tec-do.com';
const NAVOS_GLOBAL_PROD_BASE_URL = 'https://navos-mind-server-vip.tec-do.com';
const NAVOS_STAGING_BASE_URL = 'https://dev01-navos-mind-server-vip.tec-develop.cn';
const DEFAULT_BALANCE_TOKEN = 'ext_bq_2H9aLpQz6mKvR3sN';
const BALANCE_PATH = '/api/v1/balancebatch/external/query/balance';
const RUNTIME_PROFILE = loadRuntimeProfile();

const REQUEST_TIMEOUT_MS = 5_000;

/**
 * Resolve the effective Navos base URL.
 *
 * Priority:
 *   1. NAVOS_BASE_URL env override (escape hatch).
 *   2. Inferred from CV_API_BASE_URL host (prod / staging by suffix).
 *   3. Staging default.
 *
 * @returns {string} URL with no trailing slash.
 */
function resolveNavosBase() {
  const explicit = (process.env.NAVOS_BASE_URL || '').trim();
  if (explicit) return explicit.replace(/\/+$/, '');

  const profileBase = String(RUNTIME_PROFILE.navos_base_url || '').trim();
  if (profileBase) return profileBase.replace(/\/+$/, '');

  const region = String(process.env.NAVOS_REGION || RUNTIME_PROFILE.navos_region || '').trim().toLowerCase();
  if (region === 'cn' || region === 'china' || region === 'mainland') {
    return NAVOS_CN_PROD_BASE_URL;
  }
  if (region === 'global' || region === 'overseas' || region === 'intl' || region === 'international') {
    return NAVOS_GLOBAL_PROD_BASE_URL;
  }

  const cvBase = (process.env.CV_API_BASE_URL || '').trim();
  if (cvBase) {
    let host;
    try {
      host = new URL(cvBase).host.toLowerCase();
    } catch {
      host = '';
    }
    // CV prod hosts: *.tec-do.* or *.creativault.ai; staging: *.tec-develop.*
    if (host && host.endsWith('.tec-do.cn')) return NAVOS_GLOBAL_PROD_BASE_URL;
    if (host && host.endsWith('.tec-do.com')) return NAVOS_GLOBAL_PROD_BASE_URL;
    if (host && host.endsWith('.creativault.ai')) return NAVOS_GLOBAL_PROD_BASE_URL;
    if (host && host.endsWith('.tec-develop.cn')) return NAVOS_STAGING_BASE_URL;
    if (host && host.endsWith('.tec-develop.com')) return NAVOS_STAGING_BASE_URL;
  }

  return NAVOS_STAGING_BASE_URL;
}

/**
 * Resolve the X-Cm-Admin-Auth token (env > built-in default).
 */
function resolveBalanceToken() {
  return (process.env.NAVOS_BALANCE_TOKEN || '').trim() || DEFAULT_BALANCE_TOKEN;
}

/**
 * Query Navos credit balance for a uid.
 *
 * @param {{uid?: string}} [opts]  uid override; defaults to identity.uid.
 * @returns {Promise<{total_balance: number, available_balance: number, raw: object}>}
 */
export async function checkNavosBalance(opts = {}) {
  const uid = (opts.uid || '').trim() || loadNavosIdentity().uid;
  if (!uid) {
    throw new Error('checkNavosBalance: uid is required.');
  }

  const url = `${resolveNavosBase()}${BALANCE_PATH}`;
  const body = JSON.stringify({ common: { uid } });

  // Use AbortController to enforce a hard timeout independent of fetch defaults.
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

  let resp;
  try {
    resp = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Cm-Admin-Auth': resolveBalanceToken(),
      },
      body,
      signal: controller.signal,
    });
  } catch (err) {
    clearTimeout(timer);
    if (err.name === 'AbortError') {
      throw new Error(`Navos balance request timed out (${REQUEST_TIMEOUT_MS}ms)`);
    }
    const e = new Error(`Navos balance request failed: ${err.message}`);
    e.cause = err;
    throw e;
  }
  clearTimeout(timer);

  let payload;
  try {
    payload = await resp.json();
  } catch {
    throw new Error(`Navos balance returned non-JSON (HTTP ${resp.status})`);
  }

  const respCommon = payload?.resp_common || {};
  const ret = respCommon.ret;

  if (ret !== 0) {
    const err = new Error(
      `Navos balance returned ret=${ret} (${respCommon.msg || 'unknown error'})`,
    );
    err.ret = ret;
    err.requestId = respCommon.request_id;
    err.payload = payload;
    throw err;
  }

  const data = payload?.data || {};
  const total_balance = Number(data.total_balance);
  const available_balance = Number(data.available_balance);

  if (!Number.isFinite(total_balance) || !Number.isFinite(available_balance)) {
    throw new Error(
      `Navos balance response missing numeric fields. Got: ${JSON.stringify(data)}`,
    );
  }

  return { total_balance, available_balance, raw: payload };
}

/**
 * Convenience: throw if available_balance < required.
 *
 * @param {{required: number, uid?: string, label?: string}} params
 * @returns {Promise<{total_balance: number, available_balance: number}>}
 */
export async function assertNavosBalance({ required, uid, label = 'operation' }) {
  if (!Number.isFinite(required) || required < 0) {
    throw new Error(`assertNavosBalance: invalid required=${required}`);
  }
  const balance = await checkNavosBalance({ uid });
  if (balance.available_balance < required) {
    const err = new Error(
      `Navos balance insufficient for ${label}: `
      + `need ${required}, available ${balance.available_balance} (total ${balance.total_balance}).`,
    );
    err.code = 'NAVOS_INSUFFICIENT_BALANCE';
    err.balance = balance;
    err.required = required;
    throw err;
  }
  return balance;
}
