#!/usr/bin/env node
// Submit collection task (link batch / username batch)
//
// Usage:
//   node {baseDir}/scripts/submit_collection_task.mjs '{"task_type":"LINK_BATCH","platform":"tiktok","values":["https://www.tiktok.com/@creator1"]}'
//   node {baseDir}/scripts/submit_collection_task.mjs '{"task_type":"FILE_UPLOAD","platform":"youtube","values":["creator1","creator2"]}'

import { callAPI, parseArgs, validateRequired, validatePlatform } from './_api_client.mjs';

const params = parseArgs();

validateRequired(params, ['task_type', 'platform', 'values']);
validatePlatform(params.platform);

const validTypes = ['LINK_BATCH', 'FILE_UPLOAD'];
if (!validTypes.includes(params.task_type)) {
  console.error(JSON.stringify({
    error: `task_type must be one of: ${validTypes.join(' / ')}`,
    received: params.task_type,
  }));
  process.exit(1);
}

if (!Array.isArray(params.values) || params.values.length === 0) {
  console.error(JSON.stringify({ error: 'values must be a non-empty array' }));
  process.exit(1);
}

if (params.values.length > 500) {
  console.error(JSON.stringify({ error: 'values cannot exceed 500 items' }));
  process.exit(1);
}

const result = await callAPI('/openapi/v1/collection/tasks/submit', params);
console.log(JSON.stringify(result, null, 2));
