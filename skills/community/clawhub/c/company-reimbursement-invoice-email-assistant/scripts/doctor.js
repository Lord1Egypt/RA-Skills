#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { loadDotEnv } = require('../lib/env');

loadDotEnv();

const root = path.join(__dirname, '..');
const checks = [];

function add(name, ok, detail) {
  checks.push({ name, ok, detail });
}

add('Node.js >= 18', Number(process.versions.node.split('.')[0]) >= 18, process.version);
add('package.json exists', fs.existsSync(path.join(root, 'package.json')), 'package.json');
add('.env exists', fs.existsSync(path.join(root, '.env')), '.env');
add('IMAP_USER configured', Boolean(process.env.IMAP_USER), 'required for live mailbox runs');
add('IMAP_PASSWORD configured', Boolean(process.env.IMAP_PASSWORD), 'required for live mailbox runs');

for (const dep of ['imap', 'mailparser', 'pdf2json', 'exceljs', 'iconv-lite']) {
  try {
    require.resolve(dep, { paths: [root] });
    add(`dependency ${dep}`, true, dep);
  } catch {
    add(`dependency ${dep}`, false, 'run npm install');
  }
}

let failed = 0;
for (const c of checks) {
  if (!c.ok) failed++;
  console.log(`${c.ok ? 'OK  ' : 'FAIL'} ${c.name} - ${c.detail}`);
}

if (failed) {
  console.error(`\nDoctor found ${failed} issue(s). Fix them before running live mailbox processing.`);
  process.exit(1);
}

console.log('\nDoctor passed. You can run the invoice pipeline.');
