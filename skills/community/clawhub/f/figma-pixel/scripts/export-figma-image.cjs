#!/usr/bin/env node

const { exportFigmaImage } = require('../lib/figma-export.cjs');

async function main() {
  const fileKey = process.argv[2];
  const nodeId = process.argv[3];
  const outputPath = process.argv[4] || 'reference-image.png';
  const result = await exportFigmaImage(fileKey, nodeId, outputPath, null);
  console.log(JSON.stringify(result, null, 2));
}

main().catch((error) => {
  console.error(error.stack || String(error));
  process.exit(1);
});
