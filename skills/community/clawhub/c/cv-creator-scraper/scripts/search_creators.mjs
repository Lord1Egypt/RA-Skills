#!/usr/bin/env node
// Search creators — supports TikTok / YouTube / Instagram
//
// Usage:
//   node {baseDir}/scripts/search_creators.mjs '{"platform":"tiktok","keyword":"beauty","country_code":"US","followers_cnt_gte":10000}'
//
// Industry category examples:
//   - Chinese name: '{"platform":"tiktok","industry":"美妆"}'
//   - English name: '{"platform":"youtube","industry":"Skincare"}'
//   - Level-1 ID:   '{"platform":"tiktok","industry":"25"}'
//   - Level-3 ID:   '{"platform":"instagram","industry":"25009001"}'

import { callAPI, parseArgs, validatePlatform } from './_api_client.mjs';

const params = parseArgs();
const { platform, ...searchParams } = params;

validatePlatform(platform);

const result = await callAPI(`/openapi/v1/creators/${platform}/search`, searchParams, platform);
console.log(JSON.stringify(result, null, 2));
