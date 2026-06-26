#!/usr/bin/env node

const { fetchFigmaApi } = require('../lib/figma-api.cjs');

async function main() {
  const figmaUrl = process.argv[2];
  const outputDir = process.argv[3] || 'figma-pixel-runs/project/run-id/figma';
  const result = await fetchFigmaApi(figmaUrl, outputDir);
  console.log(JSON.stringify(result, null, 2));
}

main().catch((error) => {
  console.error(error.stack || String(error));
  process.exit(1);
});
