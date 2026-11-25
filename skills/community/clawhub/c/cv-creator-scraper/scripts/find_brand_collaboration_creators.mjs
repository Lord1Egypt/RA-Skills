#!/usr/bin/env node
// Find creators who collaborated with a competitor/brand from offline tables.
//
// Usage:
//   node scripts/find_brand_collaboration_creators.mjs \
//     '{"brand_name":"Fenty Beauty","platforms":["tiktok","instagram"],"limit":20}'

import { callAPI, parseArgs, validateRequired } from './_api_client.mjs';

const params = parseArgs();

validateRequired(params, ['brand_name']);

if (params.platforms !== undefined) {
  if (!Array.isArray(params.platforms) || params.platforms.length === 0) {
    console.error(JSON.stringify({ error: 'platforms must be a non-empty array' }));
    process.exit(1);
  }
  const invalid = params.platforms.filter(platform => !['tiktok', 'instagram'].includes(platform));
  if (invalid.length > 0) {
    console.error(JSON.stringify({
      error: 'offline brand collaboration discovery supports only tiktok / instagram',
      invalid,
    }));
    process.exit(1);
  }
}

const result = await callAPI(
  '/openapi/v1/brand-discovery/collaboration-creators',
  params,
  null,
);
console.log(JSON.stringify(result, null, 2));
