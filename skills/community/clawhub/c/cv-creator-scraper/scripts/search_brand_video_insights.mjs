#!/usr/bin/env node
// Search existing videos for brand insights using CreatiVault hashtag expansion.
//
// Usage:
//   node scripts/search_brand_video_insights.mjs \
//     '{"brand_name":"Fenty Beauty","platforms":["tiktok"],"limit":20}'

import { callAPI, parseArgs, validateRequired } from './_api_client.mjs';

const params = parseArgs();

validateRequired(params, ['brand_name']);

if (params.platform && !params.platforms) {
  params.platforms = [params.platform];
  delete params.platform;
}

if (params.platforms !== undefined) {
  if (!Array.isArray(params.platforms) || params.platforms.length === 0) {
    console.error(JSON.stringify({ error: 'platforms must be a non-empty array' }));
    process.exit(1);
  }
  const validPlatforms = new Set(['tiktok', 'youtube', 'instagram']);
  const invalid = params.platforms.filter(platform => !validPlatforms.has(platform));
  if (invalid.length > 0) {
    console.error(JSON.stringify({
      error: 'platforms must contain only: tiktok, youtube, instagram',
      received: invalid,
    }));
    process.exit(1);
  }
}

if (params.hashtags !== undefined) {
  if (!Array.isArray(params.hashtags) || params.hashtags.length === 0) {
    console.error(JSON.stringify({ error: 'hashtags must be a non-empty array' }));
    process.exit(1);
  }
  if (params.hashtags.length > 5) {
    console.error(JSON.stringify({ error: 'hashtags supports at most 5 items' }));
    process.exit(1);
  }
}

const result = await callAPI(
  '/openapi/v1/brand-discovery/video-insights/search',
  params,
  null,
);

console.log(JSON.stringify(result, null, 2));
