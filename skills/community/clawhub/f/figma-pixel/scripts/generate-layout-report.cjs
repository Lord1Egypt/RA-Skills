#!/usr/bin/env node

const { generateLayoutReport } = require('../lib/layout-report.cjs');

const args = process.argv.slice(2);
const options = {};
for (let i = 0; i < args.length; i += 1) {
  const key = args[i];
  if (!key.startsWith('--')) continue;
  const value = args[i + 1];
  options[key.slice(2)] = value;
  i += 1;
}

console.log(JSON.stringify(generateLayoutReport(options), null, 2));
