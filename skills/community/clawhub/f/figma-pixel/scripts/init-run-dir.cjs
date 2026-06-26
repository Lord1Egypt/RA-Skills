#!/usr/bin/env node

const path = require('path');
const { createRunManifest } = require('../lib/run-manifest.cjs');

const result = createRunManifest(
  process.argv[2] || 'project',
  process.argv[3] || new Date().toISOString().replace(/[:.]/g, '-'),
  process.argv[4] || path.resolve(process.cwd(), 'figma-pixel-runs')
);

console.log(JSON.stringify(result, null, 2));
