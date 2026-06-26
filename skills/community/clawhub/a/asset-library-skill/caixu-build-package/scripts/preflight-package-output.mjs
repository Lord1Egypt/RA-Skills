#!/usr/bin/env node

import { existsSync } from "node:fs";
import { resolve } from "node:path";

function fail(message) {
  console.error(message);
  process.exit(1);
}

const outputDir = process.argv[2];
const assetPaths = process.argv.slice(3);

if (!outputDir) {
  fail("Usage: node preflight-package-output.mjs <outputDir> [assetPath...]");
}

if (!existsSync(resolve(outputDir))) {
  fail(`Output directory does not exist: ${outputDir}`);
}

for (const assetPath of assetPaths) {
  if (!existsSync(resolve(assetPath))) {
    fail(`Missing source asset: ${assetPath}`);
  }
}

console.log(JSON.stringify({ ok: true }));
