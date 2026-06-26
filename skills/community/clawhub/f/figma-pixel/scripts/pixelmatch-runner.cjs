#!/usr/bin/env node

const { runPixelmatch } = require('../lib/pixelmatch.cjs');

function main() {
  const [img1Path, img2Path, diffPath] = process.argv.slice(2);
  const result = runPixelmatch(img1Path, img2Path, diffPath);
  console.log(JSON.stringify(result, null, 2));
}

try {
  main();
} catch (error) {
  console.error(error.stack || String(error));
  process.exit(1);
}
