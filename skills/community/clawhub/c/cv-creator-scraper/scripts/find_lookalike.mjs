#!/usr/bin/env node
// Find similar/lookalike creators — supports username, profile_url, or cross-platform search
// The API internally resolves username/URL to platform ID, no separate resolve step needed.
//
// Usage:
//   node {baseDir}/scripts/find_lookalike.mjs '{"username":"creator_demo","platform":"tiktok","limit":10}'
//   node {baseDir}/scripts/find_lookalike.mjs '{"profile_url":"https://www.tiktok.com/@creator_demo","limit":10}'
//   node {baseDir}/scripts/find_lookalike.mjs '{"username":"creator_demo","target_platform":"youtube","limit":10}'

import { callAPI, parseArgs } from './_api_client.mjs';

const params = parseArgs();

if (!params.username && !params.profile_url) {
  console.error(JSON.stringify({ error: 'Either username or profile_url is required' }));
  process.exit(1);
}

const result = await callAPI('/openapi/v1/creators/lookalike', params);
console.log(JSON.stringify(result, null, 2));
