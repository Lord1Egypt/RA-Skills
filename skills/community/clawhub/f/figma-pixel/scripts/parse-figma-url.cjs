#!/usr/bin/env node

const { parseFigmaUrl } = require('../lib/parse-figma-url.cjs');

try {
  const result = parseFigmaUrl(process.argv[2]);
  console.log(JSON.stringify(result, null, 2));
  if (!result.fileKey) process.exit(2);
} catch (error) {
  console.error(error.message || String(error));
  process.exit(1);
}
