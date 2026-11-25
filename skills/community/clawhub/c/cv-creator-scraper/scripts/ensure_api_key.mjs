#!/usr/bin/env node
// Manually trigger CV ensure for the current Navos desktop user.
//
// Use cases:
//   - Smoke-test the integration after first-time login (`node ensure_api_key.mjs`).
//   - Force re-issue after a manual revoke (`node ensure_api_key.mjs --refresh`).
//
// Output (stdout): single-line JSON with non-sensitive fields.
//   {
//     "partner_code": "navos-cn",
//     "uid": "...",
//     "user_id": "<cv-uuid>",
//     "key_prefix": "cv_live_n",
//     "is_new": true,
//     "source": "ensure" | "cache" | "env",
//     "api_key_masked": "cv_live_navos_****abcd"
//   }
//
// Errors → JSON on stderr + exit 1.

import { resolveCvCredentials } from './_cv_credentials.mjs';
import { loadRuntimeProfile } from './_runtime_profile.mjs';

const RUNTIME_PROFILE = loadRuntimeProfile();

function maskKey(key) {
  if (!key || typeof key !== 'string') return '';
  if (key.length <= 12) return `${key.slice(0, 4)}****`;
  return `${key.slice(0, 14)}****${key.slice(-4)}`;
}

async function main() {
  const args = new Set(process.argv.slice(2));
  const forceRefresh = args.has('--refresh') || args.has('--force');

  const partnerCode = (process.env.CV_PARTNER_CODE || RUNTIME_PROFILE.partner_code || 'navos').trim();
  const cvBase = (process.env.CV_API_BASE_URL || '').replace(/\/+$/, '');
  if (!cvBase) {
    console.error(JSON.stringify({
      error: 'CV_API_BASE_URL is not configured',
      hint: 'export CV_API_BASE_URL=https://api.creativault.vip/skill/creativault',
    }));
    process.exit(1);
  }

  let creds;
  try {
    creds = await resolveCvCredentials({
      partnerCode,
      cvBase,
      forceRefresh,
      navosRegion: RUNTIME_PROFILE.navos_region || '',
      navosValidateBaseUrl: RUNTIME_PROFILE.navos_validate_base_url || '',
      navosCallbackBaseUrl: RUNTIME_PROFILE.navos_callback_base_url || '',
    });
  } catch (err) {
    console.error(JSON.stringify({
      error: 'Failed to resolve CV credentials',
      reason: err.message,
      hint: 'Make sure Navos desktop is logged in (NAVOS_UID/NAVOS_TOKEN env or '
          + '~/.navos/identity/navos-userinfo.json) and CV_API_BASE_URL is correct.',
    }, null, 2));
    process.exit(1);
  }

  const out = {
    partner_code: creds.partnerCode,
    profile: RUNTIME_PROFILE.profile,
    navos_region: RUNTIME_PROFILE.navos_region || null,
    uid: creds.uid,
    user_identity: creds.userIdentity,
    user_id: creds.userId,
    cache_env: creds.cacheEnv,
    is_new: creds.isNew,
    source: creds.source,
    api_key_masked: maskKey(creds.apiKey),
  };
  process.stdout.write(`${JSON.stringify(out, null, 2)}\n`);
}

main().catch(err => {
  console.error(JSON.stringify({
    error: 'Unexpected error in ensure_api_key',
    reason: err.message,
  }));
  process.exit(1);
});
