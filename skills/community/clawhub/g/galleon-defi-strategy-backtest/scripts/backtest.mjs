#!/usr/bin/env node
import { createHash } from 'node:crypto';
import { readFileSync, statSync, realpathSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { runBacktest, runStrategyValidation, BacktestError } from './engine.mjs';
const MAX_BYTES = 4000000;
const digest = bytes => createHash('sha256').update(bytes).digest('hex');
function readJson(path) {
  if (!statSync(path).isFile() || statSync(path).size > MAX_BYTES) throw new BacktestError('invalid_input_file');
  const bytes = readFileSync(path);
  if (bytes.length > MAX_BYTES) throw new BacktestError('invalid_input_file');
  let value;
  try { value = JSON.parse(new TextDecoder('utf-8', { fatal: true }).decode(bytes)); }
  catch { throw new BacktestError('invalid_json'); }
  return { value, hash: digest(bytes) };
}
export function backtestFiles(datasetPath, specPath) {
  const dataset = readJson(datasetPath), spec = readJson(specPath);
  const input = dataset.value?.ok === true && dataset.value?.dataset ? dataset.value.dataset : dataset.value;
  return { ...runBacktest(input, spec.value), integrity: { datasetSha256: dataset.hash, specSha256: spec.hash, algorithm: 'sha256' } };
}
export function strategyValidationFiles(datasetPath, specPath, options = {}) {
  const dataset = readJson(datasetPath), spec = readJson(specPath);
  const input = dataset.value?.ok === true && dataset.value?.dataset ? dataset.value.dataset : dataset.value;
  return { ...runStrategyValidation(input, spec.value, options), integrity: { datasetSha256: dataset.hash, specSha256: spec.hash, algorithm: 'sha256' } };
}
function isMain() {
  try { return Boolean(process.argv[1]) && realpathSync(process.argv[1]) === fileURLToPath(import.meta.url); }
  catch { return false; }
}
if (isMain()) {
  const args = process.argv.slice(2);
  if (args.length === 1 && ['--help', '-h'].includes(args[0])) {
    process.stdout.write('Daily strategy backtest (Node.js 20+)\nUsage: node scripts/backtest.mjs --data <dataset.json> --spec <spec.json>\nLocal files only; JSON report with trades, equity curve, flow-neutral drawdown and same-cost buy-and-hold benchmark. No network or wallet access.\n');
  } else {
    let result;
    try {
      if (args.length !== 4 || args[0] !== '--data' || args[2] !== '--spec' || !args[1] || !args[3]) throw new BacktestError('invalid_arguments');
      result = backtestFiles(args[1], args[3]);
    } catch (error) { result = { ok: false, error: error instanceof BacktestError ? error.code : 'input_read_error' }; }
    process.stdout.write(JSON.stringify(result, null, 2) + '\n');
    if (!result.ok) process.exitCode = 1;
  }
}
