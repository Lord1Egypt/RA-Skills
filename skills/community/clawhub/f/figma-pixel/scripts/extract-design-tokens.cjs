#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { extractDesignTokensFromFile } = require('../lib/design-tokens.cjs');

const figmaNodePath = process.argv[2];
const outputPath = process.argv[3];
const nodeId = process.argv[4];

if (!figmaNodePath) {
  console.error('Usage: node scripts/extract-design-tokens.cjs <figma-node.json> [output.json] [node-id]');
  process.exit(1);
}

try {
  const tokens = extractDesignTokensFromFile(path.resolve(figmaNodePath), nodeId);
  const json = JSON.stringify(tokens, null, 2);

  if (outputPath) {
    fs.mkdirSync(path.dirname(path.resolve(outputPath)), { recursive: true });
    fs.writeFileSync(path.resolve(outputPath), json);
    console.error(`Design tokens written to ${outputPath}`);
  }

  process.stdout.write(json + '\n');
  process.exit(0);
} catch (error) {
  console.error(error.message);
  process.exit(1);
}
