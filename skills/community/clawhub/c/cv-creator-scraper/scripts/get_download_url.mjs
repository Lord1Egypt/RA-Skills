#!/usr/bin/env node
// Get file download URL
//
// Usage:
//   node {baseDir}/scripts/get_download_url.mjs '{"file_id":"a1b2c3d4e5f6"}'
//   node {baseDir}/scripts/get_download_url.mjs '{"file_name":"upload-youtube-20.xls"}'

import { callAPI, parseArgs } from './_api_client.mjs';

const params = parseArgs();

if (!params.file_id && !params.file_name) {
  console.error(JSON.stringify({
    error: 'Either file_id or file_name is required',
  }));
  process.exit(1);
}

const result = await callAPI('/openapi/v1/files/download-url', params, null, { skipUserIdentity: true });
console.log(JSON.stringify(result, null, 2));
