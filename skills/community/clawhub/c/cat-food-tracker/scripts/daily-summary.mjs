#!/usr/bin/env node
import { readFile } from 'node:fs/promises';
import { stdin, argv, exit } from 'node:process';
import {
  assertDateFilter,
  buildDailySummaryRows,
  parseBackupText,
  parseCliArgs,
  toCSV,
  validateBackupData,
} from './cat-food-core.mjs';

const usage = `Usage:
  node scripts/daily-summary.mjs <backup.json|-> [--format json|csv] [--pretty]
  node scripts/daily-summary.mjs backup.json --pet-id pet-1 --from 2026-04-01 --to 2026-04-30 --format csv

Creates daily cat feeding, water, and weight summaries from a CatFoodCalculator-style JSON backup.`;

async function readInput(input) {
  if (!input || input === '-') {
    return new Promise((resolve, reject) => {
      let text = '';
      stdin.setEncoding('utf8');
      stdin.on('data', (chunk) => {
        text += chunk;
      });
      stdin.on('end', () => resolve(text));
      stdin.on('error', reject);
    });
  }
  return readFile(input, 'utf8');
}

try {
  const options = parseCliArgs(argv.slice(2));
  if (options.help) {
    console.log(usage);
    exit(0);
  }
  if (!['json', 'csv'].includes(options.format)) {
    throw new Error('--format must be json or csv');
  }
  assertDateFilter(options.from, '--from');
  assertDateFilter(options.to, '--to');

  const text = await readInput(options.input);
  const { backup, warnings } = validateBackupData(parseBackupText(text));
  const rows = buildDailySummaryRows(backup, options);

  if (options.format === 'csv') {
    if (warnings.length > 0) {
      console.error(JSON.stringify({ warnings }));
    }
    console.log(toCSV(rows));
  } else {
    console.log(JSON.stringify({ rows, warnings }, null, options.pretty ? 2 : 0));
  }
} catch (error) {
  console.error(JSON.stringify({ error: error.message }));
  exit(1);
}
