// src/experiment/comparison.js
//
// Thin orchestrator for a comparative experiment: run the SAME task twice --
// a baseline arm (plain task) and a variant arm (task + the reused gene's
// strategy injected) -- through a pluggable agent runner, collect real
// metrics (duration / rounds / tokens / pass-rate), and emit a versioned
// comparison result.
//
// Design notes:
//  - This module NEVER requires child_process. The agent runner, gene loader,
//    and sandbox runner are all injectable, so unit tests stay deterministic
//    (no LLM, no network, no subprocess). Production defaults are lazy-loaded.
//  - A failed arm never fabricates a score: if either arm is !ok the winner is
//    'inconclusive' and improvement is null, while still recording whatever
//    partial metrics were captured.
'use strict';

const { deriveMetric, scoreArm, num, round } = require('./metrics');

const SCHEMA = 'evolver.experiment.comparison.v1';
const RESULT_TEXT_CAP = 2000;
const EPS = 1e-9;

// Build the variant prompt by appending the reused gene's strategy, mirroring
// the numbered-list format used in src/gep/prompt.js (`${i+1}. ${s}`).
function buildVariantPrompt(task, gene) {
  if (!gene || !Array.isArray(gene.strategy) || gene.strategy.length === 0) return task;
  const steps = gene.strategy.map((s, i) => `${i + 1}. ${s}`).join('\n');
  return (
    task +
    '\n\n## Reuse the following proven strategy\n' +
    steps +
    '\n\nApply the strategy above while completing the task.'
  );
}

// Coerce whatever the agent runner returned into the canonical arm shape.
function normalizeArm(label, raw) {
  raw = raw || {};
  const tokensIn = num(raw.tokensIn);
  const tokensOut = num(raw.tokensOut);
  const tokensTotal = Number.isFinite(Number(raw.tokensTotal)) ? num(raw.tokensTotal) : tokensIn + tokensOut;
  return {
    label: String(label == null ? '' : label),
    ok: !!raw.ok,
    error: raw.error != null ? String(raw.error) : null,
    durationMs: num(raw.durationMs),
    rounds: num(raw.rounds),
    tokensIn,
    tokensOut,
    tokensTotal,
    costUsd: num(raw.costUsd),
    passRate: Number.isFinite(Number(raw.passRate)) ? num(raw.passRate) : (raw.ok ? 1 : 0),
    resultText: typeof raw.resultText === 'string' ? raw.resultText.slice(0, RESULT_TEXT_CAP) : '',
    exitCode: Number.isFinite(Number(raw.exitCode)) ? num(raw.exitCode) : null,
    timedOut: !!raw.timedOut,
  };
}

// Pass-rate for ONE arm: run its `node <script>` validation commands INSIDE that
// arm's own workspace (where its agent just ran), so two arms whose agents
// produced different output get different pass-rates -- the metric is linked to
// the arm, not to a shared empty sandbox. Each command is a `node <script>`
// vetted by sandboxExecutor's allowlist (runSingleCommand rejects anything else).
async function passRateInDir(commands, cwd, runSingleCommand, timeoutMs, warnings) {
  let passed = 0;
  let total = 0;
  for (const cmd of commands) {
    total += 1;
    try {
      const r = await runSingleCommand(cmd, { cwd, timeoutMs });
      if (r && r.ok) passed += 1;
    } catch (e) {
      warnings.push('passrate_command_error: ' + (e && e.message ? e.message : String(e)));
    }
  }
  return total > 0 ? round(passed / total, 4) : 0;
}

/**
 * Run a two-arm comparison.
 *
 * @param {object}   params
 * @param {string}   params.task                自然语言任务(必填)
 * @param {string}  [params.baseline='baseline'] 对照臂标签
 * @param {string}  [params.variant='variant']   实验臂标签
 * @param {string}   params.metric               评估指标(必填)
 * @param {string}  [params.geneId]              变体臂复用的基因 id
 * @param {string[]}[params.validationCommands]  自包含 `node <script>` 校验命令
 * @param {number}  [params.timeoutMs]           单臂超时
 * @param {function}[params.agentRunner]   (prompt, opts) => Promise<AgentResult>
 * @param {function}[params.geneLoader]    () => Gene[]
 * @param {object}  [params.sandbox]    { createSandboxDir, cleanupDir, runSingleCommand } (default: sandboxExecutor)
 * @returns {Promise<object>} versioned ComparisonResult (see SCHEMA)
 */
async function runComparison(params) {
  const p = params || {};
  const task = String(p.task == null ? '' : p.task).trim();
  const baseline = p.baseline ? String(p.baseline) : 'baseline';
  const variant = p.variant ? String(p.variant) : 'variant';
  const metric = String(p.metric == null ? '' : p.metric);
  const geneId = p.geneId ? String(p.geneId) : null;
  const validationCommands = Array.isArray(p.validationCommands)
    ? p.validationCommands.filter((c) => typeof c === 'string' && c.trim())
    : null;
  const timeoutMs = Number.isFinite(Number(p.timeoutMs)) ? Number(p.timeoutMs) : undefined;

  if (!task) throw new Error('task is required');
  if (!metric) throw new Error('metric is required');

  const agentRunner = typeof p.agentRunner === 'function'
    ? p.agentRunner
    : require('./agentRunner').runAgentTask;
  const geneLoader = typeof p.geneLoader === 'function'
    ? p.geneLoader
    : require('../gep/assetStore').loadGenes;
  const sandbox = p.sandbox && typeof p.sandbox === 'object'
    ? p.sandbox
    : require('../gep/validator/sandboxExecutor');

  const startedAt = new Date().toISOString();
  const t0 = Date.now();
  const warnings = [];

  const metricInfo = deriveMetric(metric);
  if (!metricInfo.recognized) warnings.push('metric_unrecognized: ' + metric);

  // Look up the reused gene (variant arm). Without a resolved gene the variant
  // prompt is identical to the baseline task, so the two arms are NOT a strategy
  // comparison -- record an explicit warning so identical arms aren't mistaken
  // for one.
  let gene = null;
  if (geneId) {
    let genes = [];
    try {
      genes = geneLoader() || [];
    } catch (e) {
      warnings.push('gene_load_error: ' + (e && e.message ? e.message : String(e)));
    }
    gene = genes.find((g) => g && String(g.id) === geneId) || null;
    if (!gene) warnings.push('gene_not_found: ' + geneId + ' (variant arm equals baseline)');
  } else {
    warnings.push('no_gene: variant arm equals baseline (no strategy injected)');
  }

  const hasValidation = !!(validationCommands && validationCommands.length);
  if (!hasValidation) warnings.push('passrate_degraded_no_validation');

  let metaRunner = null;
  let metaCommand = null;

  const runArm = async (label, prompt) => {
    // Each arm runs in its OWN fresh sandbox dir, so the agent works in
    // isolation (never the evolver repo / process.cwd()) and its pass-rate
    // validation reads that arm's own output, not a shared empty directory.
    const workdir = sandbox.createSandboxDir();
    let raw;
    try {
      raw = await agentRunner(prompt, { timeoutMs, cwd: workdir });
    } catch (e) {
      raw = { ok: false, error: 'agent_runner_threw: ' + (e && e.message ? e.message : String(e)) };
    }
    if (raw) {
      if (metaRunner == null && raw.runnerName) metaRunner = String(raw.runnerName);
      if (metaCommand == null && raw.agentCommand) metaCommand = String(raw.agentCommand);
    }
    const arm = normalizeArm(label, raw);
    if (hasValidation) {
      arm.passRate = await passRateInDir(validationCommands, workdir, sandbox.runSingleCommand, timeoutMs, warnings);
    }
    try { sandbox.cleanupDir(workdir); } catch (_) { /* best-effort cleanup */ }
    return arm;
  };

  // Arms run sequentially: two real agent CLIs in parallel would contend for
  // local resources / provider rate limits and muddy the duration metric.
  const armBaseline = await runArm(baseline, task);
  const armVariant = await runArm(variant, buildVariantPrompt(task, gene));

  const baselineScore = scoreArm(armBaseline, metricInfo.metricField);
  const variantScore = scoreArm(armVariant, metricInfo.metricField);

  // Pass-rate is only a real measurement when validation commands ran. Without
  // them it's a synthetic ok?1:0, so a pass-rate comparison would falsely tie
  // (both arms 1.0) — report it as inconclusive instead of a fake tie.
  const passRateNotMeasured = metricInfo.metricField === 'passRate' && !hasValidation;
  let winner;
  let improvement;
  if (!armBaseline.ok || !armVariant.ok || passRateNotMeasured) {
    winner = 'inconclusive';
    improvement = null;
  } else if (Math.abs(baselineScore - variantScore) <= EPS) {
    winner = 'tie';
    improvement = 0;
  } else {
    const variantBetter = metricInfo.lowerIsBetter
      ? variantScore < baselineScore
      : variantScore > baselineScore;
    winner = variantBetter ? 'variant' : 'baseline';
    if (baselineScore === 0) {
      improvement = null;
    } else {
      const ratio = metricInfo.lowerIsBetter
        ? (baselineScore - variantScore) / Math.abs(baselineScore)
        : (variantScore - baselineScore) / Math.abs(baselineScore);
      improvement = round(ratio, 4);
    }
  }

  return {
    schema: SCHEMA,
    task,
    metric,
    metricField: metricInfo.metricField,
    lowerIsBetter: metricInfo.lowerIsBetter,
    scoreUnit: metricInfo.scoreUnit,
    geneId,
    baselineScore,
    variantScore,
    winner,
    improvement,
    arms: { baseline: armBaseline, variant: armVariant },
    meta: {
      runner: metaRunner || 'unknown',
      agentCommand: metaCommand || null,
      startedAt,
      durationMs: Date.now() - t0,
      warnings,
    },
  };
}

module.exports = { runComparison, buildVariantPrompt, normalizeArm, SCHEMA };
