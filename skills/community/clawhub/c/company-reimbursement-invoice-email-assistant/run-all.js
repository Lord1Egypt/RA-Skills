#!/usr/bin/env node
const { spawnSync } = require('child_process');
const path = require('path');
const fs = require('fs');
const { loadDotEnv } = require('./lib/env');

loadDotEnv();

const args = process.argv.slice(2);
const startDate = args[0] || '2026-01-01';
const endDate = args[1] || new Date().toISOString().split('T')[0];
const dateTag = startDate.replace(/-/g, '') + '-' + endDate.replace(/-/g, '');
const root = __dirname;

function runStep(label, script, scriptArgs) {
  console.log(`\n[${label}] node ${script} ${scriptArgs.join(' ')}`);
  const result = spawnSync(process.execPath, [path.join(root, script), ...scriptArgs], {
    cwd: root,
    stdio: 'inherit',
    env: process.env,
    timeout: Number(process.env.PIPELINE_STEP_TIMEOUT_MS || 300000),
  });
  if (result.error) {
    console.error(`${label} failed: ${result.error.message}`);
    return false;
  }
  if (result.status !== 0) {
    console.error(`${label} exited with code ${result.status}`);
    return false;
  }
  return true;
}

console.log('Email invoice pipeline');
console.log(`Date range: ${startDate} ~ ${endDate}`);
console.log(`Date tag: ${dateTag}`);

const emailFile = path.join(root, 'scan-results', 'emails', `emails-${dateTag}.json`);
const classifiedFile = path.join(root, 'scan-results', 'classified', `classified-${dateTag}.json`);
const steps = [
  ['Step 1/7 scan invoice emails', 'step1-email-scan.js', [startDate, endDate]],
  ['Step 2/7 classify invoice candidates', 'step2-classify-invoices.js', [emailFile, dateTag]],
  ['Step 3/7 download source files to staging', 'step2-download-pdf.js', [classifiedFile, dateTag]],
  ['Step 4/7 extract PDF text from staging', 'step3-extract-pdf.js', [dateTag]],
  ['Step 5/7 merge invoice data by UID', 'step4-merge-data.js', [dateTag]],
  ['Step 6/7 generate Excel ledger', 'step5-generate-ledger.js', [dateTag]],
  ['Step 7/7 archive PDFs and generate index', 'archive-invoices.js', [dateTag]],
];

let completed = 0;
for (const [label, script, scriptArgs] of steps) {
  if (!runStep(label, script, scriptArgs)) break;
  completed++;
}

if (completed !== steps.length) {
  console.error(`\nPipeline stopped after ${completed}/${steps.length} completed step(s).`);
  process.exit(1);
}

const scanDir = path.join(root, 'scan-results');
const expected = [
  ['Email scan', path.join(scanDir, 'emails', `emails-${dateTag}.json`)],
  ['Classification', path.join(scanDir, 'classified', `classified-${dateTag}.json`)],
  ['Staging PDFs', path.join(scanDir, 'staging', dateTag, 'pdfs')],
  ['Download report', path.join(scanDir, 'downloads', `download-results-${dateTag}.json`)],
  ['PDF extraction', path.join(scanDir, `pdf-text-${dateTag}.json`)],
  ['Merged invoices', path.join(scanDir, `invoice-final-${dateTag}.json`)],
  ['Manual tasks', path.join(scanDir, `manual-tasks-${dateTag}.csv`)],
  ['Excel ledger', path.join(scanDir, `发票台账-${dateTag}.xlsx`)],
  ['Archive index', path.join(root, 'archive', 'index.html')],
];

console.log('\nPipeline completed. Output check:');
for (const [label, file] of expected) {
  console.log(`${fs.existsSync(file) ? 'OK  ' : 'MISS'} ${label}: ${path.relative(root, file)}`);
}
