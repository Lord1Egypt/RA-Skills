#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const root = path.join(__dirname, '..');
const files = [];

function walk(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name === 'node_modules' || entry.name === '.git') continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(full);
    else if (entry.isFile() && entry.name.endsWith('.js')) {
      files.push(full);
    }
  }
}

walk(root);

let failed = 0;
for (const file of files) {
  const res = spawnSync(process.execPath, ['--check', file], { encoding: 'utf8' });
  const rel = path.relative(root, file);
  if (res.status === 0) {
    console.log(`OK   ${rel}`);
  } else {
    failed++;
    console.error(`FAIL ${rel}`);
    if (res.stderr) console.error(res.stderr.trim());
  }
}

process.exit(failed ? 1 : 0);
