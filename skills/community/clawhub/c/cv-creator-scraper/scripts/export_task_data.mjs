#!/usr/bin/env node
// Export collection task data to file (xlsx / csv / html) and return download URL
//
// Usage:
//   node {baseDir}/scripts/export_task_data.mjs '{"task_id":"task_20260315_abc123","format":"xlsx"}'
//   node {baseDir}/scripts/export_task_data.mjs '{"task_id":"task_xxx","format":"csv"}'
//   node {baseDir}/scripts/export_task_data.mjs '{"task_id":"task_xxx","format":"html"}'
//
// Parameters:
//   task_id  — Required. Task ID
//   format   — Required. Export format: xlsx / csv / html

import { callAPI, parseArgs, validateRequired } from './_api_client.mjs';

const params = parseArgs();
validateRequired(params, ['task_id', 'format']);

const validFormats = ['xlsx', 'csv', 'html'];
if (!validFormats.includes(params.format)) {
  console.error(JSON.stringify({
    error: `format must be one of: ${validFormats.join(' / ')}`,
    received: params.format,
  }));
  process.exit(1);
}

const result = await callAPI('/openapi/v1/collection/tasks/export', {
  task_id: params.task_id,
  format: params.format,
});
console.log(JSON.stringify(result, null, 2));
