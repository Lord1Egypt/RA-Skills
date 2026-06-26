/**
 * session.mjs — Kernel Managed Auth session management
 * Checks auth status before browser creation, triggers re-auth when needed.
 *
 * Looks up auth connections by domain (not stored ID) so it stays in sync
 * even when connections are recreated.
 *
 * Flow:
 * 1. List connections for domain, find the one matching our profile
 * 2. If AUTHENTICATED → good to go
 * 3. If NEEDS_AUTH + can_reauth → trigger login(), poll until done
 * 4. If NEEDS_AUTH + !can_reauth → return false (caller should alert + skip)
 */
import { createRequire } from 'module';
import {
  KERNEL_SDK_PATH, SESSION_REFRESH_POLL_TIMEOUT, SESSION_REFRESH_POLL_WAIT,
} from './constants.mjs';
const require = createRequire(import.meta.url);

const PLATFORM_DOMAINS = {
  linkedin: 'linkedin.com',
  wellfound: 'wellfound.com',
};

function getKernel(apiKey) {
  const Kernel = require(KERNEL_SDK_PATH);
  return new Kernel({ apiKey });
}

/**
 * Find auth connection for a platform by domain lookup.
 * Returns the connection object or null.
 */
async function findConnection(kernel, platform) {
  const domain = PLATFORM_DOMAINS[platform];
  if (!domain) return null;

  const page = await kernel.auth.connections.list({ domain });
  const connections = [];
  for await (const conn of page) {
    connections.push(conn);
  }

  if (connections.length === 0) return null;
  // If multiple connections for same domain, prefer AUTHENTICATED
  return connections.find(c => c.status === 'AUTHENTICATED') || connections[0];
}

/**
 * Check auth connection status and re-auth if needed.
 * Returns { ok: true } or { ok: false, reason: string }
 */
export async function ensureAuth(platform, apiKey) {
  const kernel = getKernel(apiKey);

  const conn = await findConnection(kernel, platform);
  if (!conn) {
    return { ok: false, reason: `no auth connection found for ${platform} (domain: ${PLATFORM_DOMAINS[platform]})` };
  }

  if (conn.status === 'AUTHENTICATED') {
    return { ok: true, profileName: conn.profile_name };
  }

  // NEEDS_AUTH — can we auto re-auth?
  if (!conn.can_reauth) {
    return { ok: false, reason: `${platform} needs manual re-login (can_reauth=false). Run: kernel auth connections login ${conn.id}` };
  }

  // Trigger re-auth with stored credentials
  console.log(`  🔄 ${platform} session expired — re-authenticating...`);
  try {
    await kernel.auth.connections.login(conn.id);
  } catch (e) {
    return { ok: false, reason: `re-auth login() failed: ${e.message}` };
  }

  // Poll until complete
  const start = Date.now();
  while (Date.now() - start < SESSION_REFRESH_POLL_TIMEOUT) {
    await new Promise(r => setTimeout(r, SESSION_REFRESH_POLL_WAIT));
    let updated;
    try {
      updated = await kernel.auth.connections.retrieve(conn.id);
    } catch (e) {
      return { ok: false, reason: `polling failed: ${e.message}` };
    }

    if (updated.status === 'AUTHENTICATED') {
      console.log(`  ✅ ${platform} re-authenticated`);
      return { ok: true, profileName: updated.profile_name };
    }

    if (updated.flow_status === 'FAILED') {
      return { ok: false, reason: `re-auth failed: ${updated.error_message || updated.error_code || 'unknown'}` };
    }
    if (updated.flow_status === 'EXPIRED' || updated.flow_status === 'CANCELED') {
      return { ok: false, reason: `re-auth ${updated.flow_status.toLowerCase()}` };
    }
  }

  return { ok: false, reason: `re-auth timed out after ${SESSION_REFRESH_POLL_TIMEOUT / 1000}s` };
}
