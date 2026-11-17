#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i += 1) {
    if (argv[i] === '--help' || argv[i] === '-h') args.help = true;
    else if (argv[i] === '--fail-on-hard-fail') args.failOnHardFail = true;
    else if (argv[i].startsWith('--')) args[argv[i].slice(2)] = argv[++i];
  }
  return args;
}

function usage() {
  console.log('Usage: node summarize-evals.js --input eval-results.json [--output summary.md] [--fail-on-hard-fail]');
}

function pct(value, total) {
  return total === 0 ? '0.0%' : `${((value / total) * 100).toFixed(1)}%`;
}

function esc(value) {
  return String(value ?? '').replace(/\|/g, '\\|').replace(/\r?\n/g, ' ');
}

const args = parseArgs(process.argv.slice(2));
if (args.help || !args.input) {
  usage();
  process.exit(args.help ? 0 : 2);
}

const source = JSON.parse(fs.readFileSync(path.resolve(args.input), 'utf8'));
const records = Array.isArray(source) ? source : source.records;
if (!Array.isArray(records) || records.length === 0) {
  console.error('Input must be a non-empty array, or contain a records array.');
  process.exit(2);
}

const runs = new Map();
for (const record of records) {
  const runId = record.runId || 'UNSPECIFIED-RUN';
  if (!runs.has(runId)) runs.set(runId, []);
  runs.get(runId).push(record);
}

const lines = ['#POC review summary', '', `- Original record:${records.length}`, `- Running batch:${runs.size}`, ''];
let totalHardFailures = 0;

for (const [runId, rows] of runs) {
  const passed = rows.filter((row) => row.passed === true).length;
  const hardFailures = rows.filter((row) => row.hardFail === true && row.passed !== true);
  totalHardFailures += hardFailures.length;
  const scores = rows.map((row) => Number(row.score)).filter(Number.isFinite);
  const latencies = rows.map((row) => Number(row.latencyMs)).filter(Number.isFinite);
  const costs = rows.map((row) => Number(row.costCny)).filter(Number.isFinite);
  const avg = (values) => values.length === 0 ? 'No data' : (values.reduce((a, b) => a + b, 0) / values.length).toFixed(2);

  lines.push(`## ${runId}`, '');
  lines.push(`- Passed:${passed}/${rows.length}(${pct(passed, rows.length)})`);
  lines.push(`- Hard failure:${hardFailures.length}`);
  lines.push(`- Average rating:${avg(scores)}`);
  lines.push(`- Average latency:${avg(latencies)}ms`);
  lines.push(`- Average cost:${avg(costs)}yuan`, '');
  lines.push('| Category | Sample | Pass | Pass Rate | Hard Fail |', '|---|---:|---:|---:|---:|');
  const categories = new Map();
  for (const row of rows) {
    const key = row.category || 'Uncategorized';
    if (!categories.has(key)) categories.set(key, []);
    categories.get(key).push(row);
  }
  for (const [category, categoryRows] of categories) {
    const categoryPassed = categoryRows.filter((row) => row.passed === true).length;
    const categoryHard = categoryRows.filter((row) => row.hardFail === true && row.passed !== true).length;
    lines.push(`| ${esc(category)} | ${categoryRows.length} | ${categoryPassed} | ${pct(categoryPassed, categoryRows.length)} | ${categoryHard} |`);
  }
  if (hardFailures.length > 0) {
    lines.push('', '### Hard failure index', '', '| Case | Category | Question |', '|---|---|---|');
    for (const row of hardFailures) lines.push(`| ${esc(row.caseId)} | ${esc(row.category)} | ${esc(row.issue || 'Reason not recorded')} |`);
  }
  lines.push('');
}

lines.push('## Interpret discipline', '', '- This summary only provides deterministic statistics and does not replace business confirmation and root cause analysis;', '- Do not merge results across versions and do not delete failed records;', '- In the event of a hard failure, the POC shall not be declared passed based solely on the average score;', '- Adoption and business value must be judged separately in Ring 7 using real behavioral and business data.', '');
const output = `${lines.join('\n')}\n`;
if (args.output) {
  fs.writeFileSync(path.resolve(args.output), output, 'utf8');
  console.log(`Generated: ${path.resolve(args.output)}`);
} else process.stdout.write(output);

process.exit(args.failOnHardFail && totalHardFailures > 0 ? 1 : 0);
