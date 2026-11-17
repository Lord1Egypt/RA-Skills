#!/usr/bin/env node
import { realpathSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { strategyValidationFiles } from './backtest.mjs';
import { BacktestError } from './engine.mjs';
function isMain() {
  try { return Boolean(process.argv[1]) && realpathSync(process.argv[1]) === fileURLToPath(import.meta.url); }
  catch { return false; }
}
if (isMain()) {
  const args = process.argv.slice(2);
  if (args.length === 1 && ['--help', '-h'].includes(args[0])) {
    process.stdout.write('Frozen-rule strategy validation (Node.js 20+)\nUsage: node scripts/validate-strategy.mjs --data <dataset.json> --spec <spec.json> [--split <first-held-out-index>] [--stress-fee-bps <bps>] [--stress-slippage-bps <bps>]\nSplit is a zero-based observation index; default floor(observations / 2). Both periods restart independently in declared cash with fresh warmup and period-specific contributions. Higher costs default to max(2 times baseline, baseline + 10 bps), capped at 1000 bps each. Local JSON only; no optimization, network or wallet access.\n');
  } else {
    let result;
    try {
      const values = new Map();
      for (let i = 0; i < args.length; i += 2) {
        if (!['--data', '--spec', '--split', '--stress-fee-bps', '--stress-slippage-bps'].includes(args[i]) || values.has(args[i]) || !args[i + 1] || args[i + 1].startsWith('--')) throw new BacktestError('invalid_arguments');
        values.set(args[i], args[i + 1]);
      }
      if (!values.has('--data') || !values.has('--spec')) throw new BacktestError('invalid_arguments');
      const options = {};
      for (const [flag, name] of [['--split', 'splitIndex'], ['--stress-fee-bps', 'stressFeeBps'], ['--stress-slippage-bps', 'stressSlippageBps']]) {
        if (values.has(flag)) {
          const raw = values.get(flag);
          if (!/^(0|[1-9]\d*)(\.\d+)?$/.test(raw) || (flag === '--split' && !/^(0|[1-9]\d*)$/.test(raw))) throw new BacktestError('invalid_arguments');
          options[name] = Number(raw);
        }
      }
      result = strategyValidationFiles(values.get('--data'), values.get('--spec'), options);
    } catch (error) { result = { ok: false, error: error instanceof BacktestError ? error.code : 'input_read_error' }; }
    process.stdout.write(JSON.stringify(result, null, 2) + '\n');
    if (!result.ok) process.exitCode = 1;
  }
}
