#!/usr/bin/env node

const { analyzeDiff } = require('../lib/opencv-diff.cjs');

async function main() {
  const [referencePath, screenshotPath, diffPath, outputReportPath, figmaNodePath] = process.argv.slice(2);
  const result = await analyzeDiff(referencePath, screenshotPath, diffPath, outputReportPath, figmaNodePath);
  process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
  process.exit(result?.ok === false && String(result.error || '').startsWith('Usage:') ? 1 : 0);
}

main().catch((error) => {
  process.stdout.write(`${JSON.stringify({ ok: false, error: error?.message || String(error) }, null, 2)}\n`);
  process.exit(0);
});
