#!/usr/bin/env node
import { readFile } from 'node:fs/promises';
import { stdin, argv, exit } from 'node:process';
import { parseBackupText, parseCliArgs, validateBackupData } from './cat-food-core.mjs';

const usage = `Usage:
  node scripts/validate-backup.mjs <backup.json|-> [--pretty]

Validates a CatFoodCalculator-style JSON backup and prints a JSON report.`;

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

  const text = await readInput(options.input);
  const report = validateBackupData(parseBackupText(text));
  const { backup: _backup, ...publicReport } = report;
  console.log(JSON.stringify(publicReport, null, options.pretty ? 2 : 0));
} catch (error) {
  console.error(JSON.stringify({ valid: false, error: error.message }));
  exit(1);
}
