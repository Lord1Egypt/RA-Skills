#!/usr/bin/env node
// Search creators with one natural-language query.
//
// Usage:
//   node {baseDir}/scripts/search_creators_nl.mjs '{"platform":"instagram","query":"Find US running creators with authentic training content","limit":20}'

import {
  attachCreatorResultSetUrl,
  callAPI,
  parseArgs,
} from './_api_client.mjs';

const PLATFORM_ALIASES = new Map([
  ['instagram', 'instagram'],
  ['ins', 'instagram'],
  ['ig', 'instagram'],
  ['tiktok', 'tiktok'],
  ['tt', 'tiktok'],
  ['tk', 'tiktok'],
  ['youtube', 'youtube'],
  ['ytb', 'youtube'],
  ['yt', 'youtube'],
]);
const ALLOWED_FIELDS = new Set(['query', 'platform', 'limit']);
const ESTIMATED_CREDITS = 15;

function fail(error, details = {}) {
  console.error(JSON.stringify({ error, ...details }));
  process.exit(1);
}

const params = parseArgs();
const unknownFields = Object.keys(params).filter((key) => !ALLOWED_FIELDS.has(key));
if (unknownFields.length > 0) {
  fail('Unsupported parameters for natural-language creator search', {
    unsupported: unknownFields,
    allowed: [...ALLOWED_FIELDS],
  });
}

const query = typeof params.query === 'string' ? params.query.trim() : '';
if (!query) {
  fail('query must be a non-empty string');
}
if (query.length > 1000) {
  fail('query must not exceed 1000 characters', { length: query.length });
}

const platformInput = String(params.platform ?? 'instagram').trim().toLowerCase();
const platform = PLATFORM_ALIASES.get(platformInput);
if (!platform) {
  fail('platform must be one of: instagram / tiktok / youtube', {
    received: params.platform,
  });
}

const limit = params.limit ?? 20;
if (!Number.isInteger(limit) || limit < 1 || limit > 100) {
  fail('limit must be an integer between 1 and 100', { received: limit });
}

const result = await callAPI(
  '/openapi/v1/creators/nl-search',
  { query, platform, limit },
  null,
  {
    skipProfileBodyDefaults: true,
    estimatedCredits: ESTIMATED_CREDITS,
  },
);
await attachCreatorResultSetUrl(result, platform, { query, platform, limit });
console.log(JSON.stringify(result, null, 2));
