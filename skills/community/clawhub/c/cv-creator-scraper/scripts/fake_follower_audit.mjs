#!/usr/bin/env node
// Detect fake-follower and engagement-quality risk for one creator.
//
// Usage:
//   node scripts/fake_follower_audit.mjs '{"profile_url":"https://www.tiktok.com/@creator","lang":"cn"}'
//   node scripts/fake_follower_audit.mjs '{"platform":"instagram","platform_user_id":"creator","lang":"en"}'

import { callAPI, parseArgs } from './_api_client.mjs';
import { loadRuntimeProfile } from './_runtime_profile.mjs';

const PLATFORM_ALIASES = new Map([
  ['tiktok', 'tiktok'],
  ['tt', 'tiktok'],
  ['tk', 'tiktok'],
  ['instagram', 'instagram'],
  ['ins', 'instagram'],
  ['ig', 'instagram'],
  ['youtube', 'youtube'],
  ['yt', 'youtube'],
  ['ytb', 'youtube'],
]);
const ALLOWED_FIELDS = new Set([
  'profile_url',
  'platform',
  'platform_user_id',
  'service_level',
  'lang',
]);
const VALID_LANGS = new Set(['cn', 'en']);
const VALID_SERVICE_LEVELS = new Set(['S1', 'S2', 'S3']);

function fail(error, details = {}) {
  console.error(JSON.stringify({ error, ...details }));
  process.exit(1);
}

const params = parseArgs();
const unknownFields = Object.keys(params).filter((key) => !ALLOWED_FIELDS.has(key));
if (unknownFields.length > 0) {
  fail('Unsupported parameters for fake follower audit', {
    unsupported: unknownFields,
    allowed: [...ALLOWED_FIELDS],
  });
}

const profileUrl = typeof params.profile_url === 'string'
  ? params.profile_url.trim()
  : '';
const platformUserId = typeof params.platform_user_id === 'string'
  ? params.platform_user_id.trim()
  : '';
const hasProfileTarget = Boolean(profileUrl);
const hasPlatformTarget = Boolean(params.platform || platformUserId);

if (hasProfileTarget === hasPlatformTarget) {
  fail('Provide exactly one creator target', {
    hint: 'Use profile_url, or use platform together with platform_user_id.',
  });
}

let platform;
if (hasProfileTarget) {
  let parsedUrl;
  try {
    parsedUrl = new URL(profileUrl);
  } catch {
    fail('profile_url must be a valid HTTP/HTTPS URL', { received: params.profile_url });
  }
  if (!['http:', 'https:'].includes(parsedUrl.protocol)) {
    fail('profile_url must use HTTP or HTTPS', { received: params.profile_url });
  }
} else {
  const platformInput = String(params.platform || '').trim().toLowerCase();
  platform = PLATFORM_ALIASES.get(platformInput);
  if (!platform) {
    fail('platform must be one of: tiktok / instagram / youtube', {
      received: params.platform,
    });
  }
  if (!platformUserId) {
    fail('platform_user_id must be a non-empty string when platform is provided');
  }
}

const runtimeProfile = loadRuntimeProfile();
const lang = String(params.lang || runtimeProfile.default_lang || 'en').trim().toLowerCase();
if (!VALID_LANGS.has(lang)) {
  fail('lang must be one of: cn / en', { received: params.lang });
}

let serviceLevel;
if (params.service_level !== undefined && params.service_level !== null) {
  serviceLevel = String(params.service_level).trim().toUpperCase();
  if (!VALID_SERVICE_LEVELS.has(serviceLevel)) {
    fail('service_level must be one of: S1 / S2 / S3', {
      received: params.service_level,
    });
  }
}

const body = {
  ...(profileUrl && { profile_url: profileUrl }),
  ...(platform && { platform }),
  ...(platformUserId && { platform_user_id: platformUserId }),
  ...(serviceLevel && { service_level: serviceLevel }),
  lang,
};

const result = await callAPI(
  '/openapi/v1/fake-follower-audit/run',
  body,
  null,
  {
    // This API defaults to S1. Avoid Navos' creator-search S3 body injection.
    skipProfileBodyDefaults: true,
  },
);
console.log(JSON.stringify(result, null, 2));
