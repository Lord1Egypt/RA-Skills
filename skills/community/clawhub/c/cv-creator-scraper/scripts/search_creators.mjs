#!/usr/bin/env node
// Search creators — supports TikTok / YouTube / Instagram
//
// Usage:
//   node {baseDir}/scripts/search_creators.mjs '{"platform":"tiktok","keyword":"beauty","country_code":"US","followers_cnt_gte":10000}'
//   node {baseDir}/scripts/search_creators.mjs '{"platform":"tiktok","profile_urls":["https://www.tiktok.com/@creator_a"],"union_user_ids":["creator_b"]}'
//
// Industry category examples:
//   - Chinese name: '{"platform":"tiktok","industry":"美妆"}'
//   - English name: '{"platform":"youtube","industry":"Skincare"}'
//   - Level-1 ID:   '{"platform":"tiktok","industry":"25"}'
//   - Level-3 ID:   '{"platform":"instagram","industry":"25009001"}'

import {
  attachCreatorResultSetUrl,
  callAPI,
  parseArgs,
  validatePlatform,
} from './_api_client.mjs';

const params = parseArgs();
const { platform, ...searchParams } = params;

validatePlatform(platform);
validateBatchIdentityParams(searchParams);

const result = await callAPI(`/openapi/v1/creators/${platform}/search`, searchParams, platform);
await attachCreatorResultSetUrl(result, platform, searchParams);
console.log(JSON.stringify(result, null, 2));

function validateBatchIdentityParams(params) {
  for (const field of ['union_user_ids', 'profile_urls']) {
    const value = params[field];
    if (value === undefined) continue;
    if (!Array.isArray(value) || value.length === 0 || value.length > 200) {
      throw new Error(`${field} must be a non-empty array with at most 200 items`);
    }
    if (value.some((item) => typeof item !== 'string' || !item.trim())) {
      throw new Error(`${field} must contain only non-empty strings`);
    }
  }
}
