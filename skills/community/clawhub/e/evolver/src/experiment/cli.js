// src/experiment/cli.js
//
// CLI surface for the `experiment` subcommand. Mirrors src/atp/cli.js:
//   parseExperimentArgs(args) -> { ok, opts? , error? }
//   runExperiment(opts, deps) -> { ok, data?, error?, exitCode }
// Dependency-injected (comparison / agentRunner / geneLoader / sandbox)
// so the runner is unit-testable without a real agent CLI.
'use strict';

const fs = require('fs');
const path = require('path');

const MAX_REQUEST_FILE_BYTES = 1024 * 1024; // 1 MB — a request JSON is tiny

// Minimal `--key=value` / `--flag` parser (no shell, no globbing).
function parseFlags(args) {
  const out = {};
  for (const a of args || []) {
    if (typeof a !== 'string') continue;
    const eq = a.indexOf('=');
    if (a.startsWith('--') && eq > 2) {
      out[a.slice(2, eq)] = a.slice(eq + 1);
    } else if (a.startsWith('--')) {
      out[a.slice(2)] = true;
    }
  }
  return out;
}

/**
 * Parse experiment subcommand args.
 *
 * Flags: --task= --metric= [--baseline=] [--variant=] [--gene=]
 *        [--validation="cmd1;;cmd2"] [--timeout=ms] [--request-file=<json>]
 *
 * --request-file supplies a JSON base ({task,baseline,variant,metric,geneId,
 * validationCommands,timeoutMs}); explicit flags override it. This is the only
 * filesystem read here and lets the desktop pass complex params without argv
 * escaping headaches.
 *
 * @returns {{ ok: true, opts: object } | { ok: false, error: string }}
 */
function parseExperimentArgs(args) {
  const f = parseFlags(args);

  let base = {};
  if (f['request-file']) {
    try {
      // Resolve + stat the path and bound its size before reading: don't open
      // an arbitrary non-file (device/FIFO) or slurp an unbounded file.
      const rfPath = path.resolve(String(f['request-file']));
      const st = fs.statSync(rfPath);
      if (!st.isFile()) return { ok: false, error: '--request-file must be a regular file' };
      if (st.size > MAX_REQUEST_FILE_BYTES) return { ok: false, error: '--request-file too large (> 1 MB)' };
      base = JSON.parse(fs.readFileSync(rfPath, 'utf8'));
    } catch (e) {
      return { ok: false, error: 'failed to read --request-file: ' + (e && e.message ? e.message : String(e)) };
    }
    if (!base || typeof base !== 'object') {
      return { ok: false, error: '--request-file must contain a JSON object' };
    }
  }

  const pick = (flagVal, baseVal, dflt) => {
    if (flagVal !== undefined && flagVal !== true) return String(flagVal);
    if (baseVal !== undefined && baseVal !== null) return String(baseVal);
    return dflt;
  };

  const opts = {
    // trim() so a whitespace-only value fails the required-field check below
    // (parse-time exit 2 + usage) instead of crashing later in runComparison
    // (exit 1 with no JSON on stdout for the Go caller).
    task: pick(f.task, base.task, '').trim(),
    baseline: pick(f.baseline, base.baseline, 'baseline'),
    variant: pick(f.variant, base.variant, 'variant'),
    metric: pick(f.metric, base.metric, '').trim(),
    geneId: pick(f.gene, base.geneId !== undefined ? base.geneId : base.gene, '') || null,
    validationCommands: null,
    timeoutMs: undefined,
  };

  if (f.validation !== undefined && f.validation !== true) {
    opts.validationCommands = String(f.validation).split(';;').map((s) => s.trim()).filter(Boolean);
  } else if (Array.isArray(base.validationCommands)) {
    opts.validationCommands = base.validationCommands.map(String);
  }

  const timeoutRaw = f.timeout !== undefined && f.timeout !== true ? Number(f.timeout)
    : (Number.isFinite(Number(base.timeoutMs)) ? Number(base.timeoutMs) : NaN);
  if (Number.isFinite(timeoutRaw)) opts.timeoutMs = timeoutRaw;

  if (!opts.task) return { ok: false, error: 'missing required --task (or "task" in --request-file)' };
  if (!opts.metric) return { ok: false, error: 'missing required --metric (or "metric" in --request-file)' };

  return { ok: true, opts };
}

/**
 * Run the comparison. Returns the result object (also written to stdout by the
 * index.js wrapper) plus an exit code. exitCode 3 == inconclusive (a real,
 * structured outcome, not a crash).
 *
 * @param {object} opts  from parseExperimentArgs
 * @param {object} [deps] { comparison, agentRunner, geneLoader, sandbox, err }
 */
async function runExperiment(opts, deps) {
  deps = deps || {};
  const comparison = deps.comparison || require('./comparison');
  const err = typeof deps.err === 'function' ? deps.err : ((...a) => console.error(...a));

  const params = Object.assign({}, opts);
  if (deps.agentRunner) params.agentRunner = deps.agentRunner;
  if (deps.geneLoader) params.geneLoader = deps.geneLoader;
  if (deps.sandbox) params.sandbox = deps.sandbox;

  try {
    const raw = await comparison.runComparison(params);
    // Redact any secrets / API keys an agent's resultText (or a parse-failure
    // snippet) may carry before the result crosses the process boundary into
    // the desktop consumer / is persisted to disk.
    const data = require('../gep/sanitize').sanitizePayload(raw);
    let exitCode = 0;
    if (data && data.winner === 'inconclusive') {
      exitCode = 3;
      // Two distinct causes share the inconclusive verdict; say which one
      // happened so operators don't go debugging arm failures that never
      // occurred (both arms can be ok when pass-rate was simply unmeasured).
      const bothArmsOk = !!(data.arms && data.arms.baseline && data.arms.baseline.ok
        && data.arms.variant && data.arms.variant.ok);
      err(bothArmsOk
        ? '[Experiment] inconclusive: metric resolved to pass-rate but no validation commands were given, so pass-rate was never measured — pass --validation (or pick another --metric)'
        : '[Experiment] inconclusive: one or both arms failed — see arms.*.error');
    }
    return { ok: true, data, exitCode };
  } catch (e) {
    err('[Experiment] error: ' + (e && e.message ? e.message : String(e)));
    return { ok: false, error: e && e.message ? e.message : String(e), exitCode: 1 };
  }
}

function printExperimentUsage() {
  return [
    'Usage: node index.js experiment --task="..." --metric="..." [flags]',
    '  --baseline="..."          对照臂标签 (default: baseline)',
    '  --variant="..."           实验臂标签 (default: variant)',
    '  --gene=<geneId>           变体臂复用的基因 id (注入其 strategy)',
    '  --validation="c1;;c2"     自包含 node 校验命令 (通过率评分; ;; 分隔)',
    '  --timeout=<ms>            单臂超时',
    '  --request-file=<path>     JSON 基底 (显式 flag 覆盖之)',
    '',
    'Runs the same task twice (baseline vs variant-with-gene) via a headless',
    'agent CLI and prints a comparison JSON to stdout. Logs go to stderr.',
    'Env: EVOLVER_EXPERIMENT_AGENT_CMD (default claude),',
    '     EVOLVER_EXPERIMENT_AGENT_ARGS, EVOLVER_EXPERIMENT_TIMEOUT_MS (300000).',
  ].join('\n');
}

module.exports = { parseExperimentArgs, runExperiment, printExperimentUsage, parseFlags };
