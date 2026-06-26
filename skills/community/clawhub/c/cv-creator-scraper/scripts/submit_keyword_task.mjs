#!/usr/bin/env node
// Submit keyword collection task
//
// Usage:
//   node {baseDir}/scripts/submit_keyword_task.mjs '{"platform":"tiktok","keywords":["beauty tips","skincare"]}'

import { callAPI, parseArgs, validateRequired, validatePlatform } from './_api_client.mjs';

const params = parseArgs();

validateRequired(params, ['platform', 'keywords']);
validatePlatform(params.platform);

if (!Array.isArray(params.keywords) || params.keywords.length === 0) {
  console.error(JSON.stringify({ error: 'keywords must be a non-empty array' }));
  process.exit(1);
}

if (params.keywords.length > 10) {
  console.error(JSON.stringify({ error: 'keywords cannot exceed 10 items' }));
  process.exit(1);
}

const result = await callAPI('/openapi/v1/collection/tasks/keyword-submit', params);
console.log(JSON.stringify(result, null, 2));
