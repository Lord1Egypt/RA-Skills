#!/usr/bin/env node

const path = require('path');
const { renderPage } = require('../lib/page-render.cjs');

async function main() {
  const url = process.argv[2];
  const outputPath = process.argv[3] || path.resolve(process.cwd(), 'figma-pixel-runs/project/run-id/capture/captured-page.png');
  const width = Number(process.argv[4] || 1600);
  const height = Number(process.argv[5] || 900);
  const result = await renderPage(url, outputPath, width, height);
  console.log(JSON.stringify(result, null, 2));
}

main().catch((error) => {
  console.error(error.stack || String(error));
  process.exit(1);
});
