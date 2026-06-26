#!/usr/bin/env node
// Query collection task status
//
// Usage:
//   node {baseDir}/scripts/get_task_status.mjs '{"task_id":"task_20260315_abc123"}'

import { callAPI, parseArgs, validateRequired } from './_api_client.mjs';

const params = parseArgs();
validateRequired(params, ['task_id']);

const result = await callAPI('/openapi/v1/collection/tasks/status', {
  task_id: params.task_id,
});
console.log(JSON.stringify(result, null, 2));
