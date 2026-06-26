#!/usr/bin/env node
// Get collection task data
//
// Usage:
//   node {baseDir}/scripts/get_task_data.mjs '{"task_id":"task_20260315_abc123","page":1,"size":20}'

import { callAPI, parseArgs, validateRequired } from './_api_client.mjs';

const params = parseArgs();
validateRequired(params, ['task_id']);

const result = await callAPI('/openapi/v1/collection/tasks/data', {
  task_id: params.task_id,
  page: params.page || 1,
  size: params.size || 20,
});
console.log(JSON.stringify(result, null, 2));
