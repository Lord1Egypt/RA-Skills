#!/usr/bin/env node
// Submit a lightweight realtime brand keyword mention collection task.
//
// Usage:
//   node scripts/submit_brand_realtime_mentions.mjs \
//     '{"platform":"tiktok","brand_name":"Fenty Beauty"}'
//   node scripts/submit_brand_realtime_mentions.mjs \
//     '{"platform":"instagram","keywords":["Fenty Beauty","fentybeauty"]}'

import { callAPI, parseArgs, validateRequired } from './_api_client.mjs';

const params = parseArgs();

validateRequired(params, ['platform']);

const validPlatforms = ['tiktok', 'youtube', 'instagram', 'twitter'];
if (!validPlatforms.includes(params.platform)) {
  console.error(JSON.stringify({
    error: 'platform must be one of: tiktok, youtube, instagram, twitter',
    received: params.platform,
  }));
  process.exit(1);
}

const hasBrandName = typeof params.brand_name === 'string' && params.brand_name.trim();
const hasKeywords = Array.isArray(params.keywords)
  && params.keywords.some(keyword => typeof keyword === 'string' && keyword.trim());

if (!hasBrandName && !hasKeywords) {
  console.error(JSON.stringify({
    error: 'Either brand_name or a non-empty keywords array is required',
  }));
  process.exit(1);
}

if (params.keywords !== undefined) {
  if (!Array.isArray(params.keywords) || params.keywords.length === 0) {
    console.error(JSON.stringify({ error: 'keywords must be a non-empty array' }));
    process.exit(1);
  }

  if (params.keywords.length > 10) {
    console.error(JSON.stringify({ error: 'keywords supports at most 10 items' }));
    process.exit(1);
  }
}

const result = await callAPI(
  '/openapi/v1/brand-discovery/realtime-mentions',
  params,
  null,
);

console.log(JSON.stringify(result, null, 2));
