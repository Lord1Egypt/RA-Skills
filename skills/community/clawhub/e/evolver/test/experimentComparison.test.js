// test/experimentComparison.test.js
//
// Deterministic unit tests for the comparative experiment executor
// (src/experiment/*). All agent/gene/sandbox dependencies are injected, so
// these run with zero network, zero subprocess, and zero LLM -- safe for the
// PR gate. NOTE: must live at the top level of test/ (not test/experiments/)
// because package.json's test script scans test/ non-recursively.
'use strict';

const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const os = require('os');
const fs = require('fs');
const path = require('path');

const { runComparison } = require('../src/experiment/comparison');
const { deriveMetric } = require('../src/experiment/metrics');
const { parseExperimentArgs, runExperiment } = require('../src/experiment/cli');

const VARIANT_MARK = 'Reuse the following proven strategy';

// A fake agent runner that returns distinct metrics per arm, keyed on whether
// the prompt carries the injected-strategy marker (variant) or not (baseline).
function fakeRunner(baselineMetrics, variantMetrics) {
  return async (prompt) => {
    const isVariant = String(prompt).includes(VARIANT_MARK);
    return Object.assign(
      { ok: true, isError: false, runnerName: 'injected-fake', agentCommand: 'fake' },
      isVariant ? variantMetrics : baselineMetrics,
    );
  };
}

const genesFix = () => [{ id: 'gene_x', strategy: ['Step A', 'Step B'] }];

// Fake sandbox: each arm gets a distinct workdir id; validation verdicts are a
// function of (command, cwd) so two arms can legitimately differ on pass-rate.
function fakeSandbox(verdict) {
  let n = 0;
  return {
    createSandboxDir: () => '/tmp/exp-arm-' + (n++),
    cleanupDir: () => {},
    runSingleCommand: async (cmd, opts) => ({ ok: !!verdict(cmd, opts && opts.cwd) }),
  };
}

describe('runComparison — metric collection & mapping', () => {
  it('collects per-arm metrics field-by-field', async () => {
    const r = await runComparison({
      task: 'T', metric: 'token', geneId: 'gene_x',
      agentRunner: fakeRunner(
        { durationMs: 12000, rounds: 8, tokensIn: 4000, tokensOut: 2000, costUsd: 0.03 },
        { durationMs: 9000, rounds: 5, tokensIn: 3000, tokensOut: 1000, costUsd: 0.02 }),
      geneLoader: genesFix,
    });
    assert.equal(r.arms.baseline.durationMs, 12000);
    assert.equal(r.arms.baseline.rounds, 8);
    assert.equal(r.arms.baseline.tokensTotal, 6000);
    assert.equal(r.arms.variant.tokensTotal, 4000);
    assert.equal(r.arms.variant.costUsd, 0.02);
    assert.equal(r.arms.baseline.ok, true);
    // token metric: lower is better -> variant (4000 < 6000) wins
    assert.equal(r.metricField, 'tokensTotal');
    assert.equal(r.lowerIsBetter, true);
    assert.equal(r.baselineScore, 6000);
    assert.equal(r.variantScore, 4000);
    assert.equal(r.winner, 'variant');
    assert.equal(r.improvement, 0.3333);
  });

  it('maps 完成耗时 (s) to durationSec (seconds), lower-is-better, variant faster', async () => {
    const r = await runComparison({
      task: 'T', metric: '完成耗时 (s)', geneId: 'gene_x',
      agentRunner: fakeRunner({ durationMs: 12800 }, { durationMs: 9500 }),
      geneLoader: genesFix,
    });
    assert.equal(r.metricField, 'durationSec');
    assert.equal(r.lowerIsBetter, true);
    assert.equal(r.baselineScore, 12.8);
    assert.equal(r.variantScore, 9.5);
    assert.equal(r.winner, 'variant');
    assert.equal(r.improvement, 0.2578);
  });

  it('rounds metric (higher rounds is worse)', async () => {
    const r = await runComparison({
      task: 'T', metric: '轮次', geneId: 'gene_x',
      agentRunner: fakeRunner({ rounds: 8 }, { rounds: 6 }),
      geneLoader: genesFix,
    });
    assert.equal(r.metricField, 'rounds');
    assert.equal(r.baselineScore, 8);
    assert.equal(r.variantScore, 6);
    assert.equal(r.winner, 'variant');
  });
});

describe('runComparison — gene strategy injection', () => {
  it('injects the numbered gene strategy into the variant prompt only', async () => {
    let variantPrompt = null;
    let baselinePrompt = null;
    const spy = async (prompt) => {
      if (String(prompt).includes(VARIANT_MARK)) variantPrompt = prompt;
      else baselinePrompt = prompt;
      return { ok: true, durationMs: 1 };
    };
    await runComparison({ task: 'Do X', metric: '轮次', geneId: 'gene_x', agentRunner: spy, geneLoader: genesFix });
    assert.equal(baselinePrompt, 'Do X');
    assert.ok(variantPrompt.startsWith('Do X'));
    assert.ok(variantPrompt.includes('1. Step A'));
    assert.ok(variantPrompt.includes('2. Step B'));
  });

  it('degrades variant to the plain task when the gene is not found', async () => {
    const prompts = [];
    const spy = async (prompt) => { prompts.push(prompt); return { ok: true, durationMs: 1 }; };
    const r = await runComparison({ task: 'Do X', metric: '轮次', geneId: 'missing', agentRunner: spy, geneLoader: genesFix });
    assert.equal(prompts[0], 'Do X');
    assert.equal(prompts[1], 'Do X');
    assert.ok(r.meta.warnings.some((w) => w.startsWith('gene_not_found')));
  });

  it('warns when no gene is given — both arms run identical prompts', async () => {
    const prompts = [];
    const spy = async (prompt) => { prompts.push(prompt); return { ok: true, durationMs: 1 }; };
    const r = await runComparison({ task: 'Do X', metric: '轮次', agentRunner: spy });
    assert.equal(prompts[0], prompts[1]); // no strategy injected -> identical
    assert.ok(r.meta.warnings.some((w) => w.startsWith('no_gene')));
  });
});

describe('runComparison — failed arms never fabricate a winner', () => {
  it('marks inconclusive + null improvement when an arm fails, baseline still scored', async () => {
    const runner = async (prompt) => (String(prompt).includes(VARIANT_MARK)
      ? { ok: false, isError: true, error: 'agent_cli_not_found: claude' }
      : { ok: true, durationMs: 12000 });
    const r = await runComparison({ task: 'T', metric: '完成耗时 (s)', geneId: 'gene_x', agentRunner: runner, geneLoader: genesFix });
    assert.equal(r.winner, 'inconclusive');
    assert.equal(r.improvement, null);
    assert.equal(r.arms.variant.ok, false);
    assert.equal(r.arms.variant.error, 'agent_cli_not_found: claude');
    assert.equal(r.arms.baseline.ok, true);
    assert.equal(r.baselineScore, 12); // partial metric still recorded
  });

  it('treats a thrown agent runner as a failed arm (no crash)', async () => {
    const runner = async () => { throw new Error('boom'); };
    const r = await runComparison({ task: 'T', metric: '轮次', agentRunner: runner });
    assert.equal(r.arms.baseline.ok, false);
    assert.ok(String(r.arms.baseline.error).includes('agent_runner_threw'));
    assert.equal(r.winner, 'inconclusive');
  });
});

describe('runComparison — passRate is linked to each arm workspace', () => {
  it('variant can win on 通过率 — pass-rate reflects each arm\'s own workdir (not always tie)', async () => {
    // baseline workdir = exp-arm-0 (commands fail), variant = exp-arm-1 (pass)
    const sandbox = fakeSandbox((_cmd, cwd) => cwd === '/tmp/exp-arm-1');
    const r = await runComparison({
      task: 'T', metric: '通过率', geneId: 'gene_x', geneLoader: genesFix,
      validationCommands: ['node check.js'],
      agentRunner: fakeRunner({}, {}), sandbox,
    });
    assert.equal(r.metricField, 'passRate');
    assert.equal(r.lowerIsBetter, false);
    assert.equal(r.arms.baseline.passRate, 0);
    assert.equal(r.arms.variant.passRate, 1);
    assert.equal(r.winner, 'variant'); // higher pass-rate wins; arms no longer always tie
  });

  it('pass-rate = 0.5 when half of an arm\'s validation commands fail', async () => {
    const sandbox = fakeSandbox((cmd) => cmd === 'node a.js');
    const r = await runComparison({
      task: 'T', metric: '通过率', geneId: 'gene_x', geneLoader: genesFix,
      validationCommands: ['node a.js', 'node b.js'],
      agentRunner: fakeRunner({}, {}), sandbox,
    });
    assert.equal(r.arms.baseline.passRate, 0.5);
  });

  it('reports inconclusive (not a fake tie) when pass-rate is unmeasured', async () => {
    const r = await runComparison({
      task: 'T', metric: '通过率', geneId: 'gene_x', geneLoader: genesFix,
      agentRunner: fakeRunner({}, {}), sandbox: fakeSandbox(() => true),
    });
    assert.ok(r.meta.warnings.includes('passrate_degraded_no_validation'));
    assert.equal(r.winner, 'inconclusive'); // synthetic 1.0/1.0 must not read as a tie
    assert.equal(r.improvement, null);
  });
});

describe('deriveMetric', () => {
  it('轮次 -> rounds, lower-is-better', () => {
    const m = deriveMetric('Bugbot 轮次');
    assert.equal(m.metricField, 'rounds');
    assert.equal(m.lowerIsBetter, true);
  });
  it('token -> tokensTotal', () => {
    assert.equal(deriveMetric('token 用量').metricField, 'tokensTotal');
  });
  it('成本 -> costUsd', () => {
    assert.equal(deriveMetric('成本 (USD)').metricField, 'costUsd');
  });
  it('通过率 -> passRate, higher-is-better', () => {
    const m = deriveMetric('通过率');
    assert.equal(m.metricField, 'passRate');
    assert.equal(m.lowerIsBetter, false);
  });
  it('seconds-flavoured duration -> durationSec', () => {
    assert.equal(deriveMetric('构建耗时 (s)').metricField, 'durationSec');
  });
  it('plain duration -> durationMs', () => {
    assert.equal(deriveMetric('latency').metricField, 'durationMs');
  });
  it('unrecognized -> fallback passRate + recognized:false', () => {
    const m = deriveMetric('吞吐 (task/h)');
    assert.equal(m.recognized, false);
    assert.equal(m.metricField, 'passRate');
  });
});

describe('parseExperimentArgs', () => {
  it('requires both --task and --metric', () => {
    assert.equal(parseExperimentArgs(['--task=T']).ok, false);
    assert.equal(parseExperimentArgs(['--metric=M']).ok, false);
    assert.equal(parseExperimentArgs(['--task=T', '--metric=M']).ok, true);
  });
  it('rejects whitespace-only --task / --metric at parse time (not as a late runComparison crash)', () => {
    assert.equal(parseExperimentArgs(['--task=   ', '--metric=M']).ok, false);
    assert.equal(parseExperimentArgs(['--task=T', '--metric= \t ']).ok, false);
  });
  it('maps --gene to geneId and defaults baseline/variant', () => {
    const p = parseExperimentArgs(['--task=T', '--metric=M', '--gene=gene_x']);
    assert.equal(p.opts.geneId, 'gene_x');
    assert.equal(p.opts.baseline, 'baseline');
    assert.equal(p.opts.variant, 'variant');
  });
  it('splits --validation on ;;', () => {
    const p = parseExperimentArgs(['--task=T', '--metric=M', '--validation=node a.js;;node b.js']);
    assert.deepEqual(p.opts.validationCommands, ['node a.js', 'node b.js']);
  });
  it('merges --request-file with explicit flags overriding', () => {
    const f = path.join(os.tmpdir(), 'exp_req_test_' + process.pid + '.json');
    fs.writeFileSync(f, JSON.stringify({ task: 'FromFile', metric: '轮次', baseline: 'B0', geneId: 'g0' }));
    try {
      const p = parseExperimentArgs(['--request-file=' + f, '--variant=V1']);
      assert.equal(p.ok, true);
      assert.equal(p.opts.task, 'FromFile');
      assert.equal(p.opts.baseline, 'B0');
      assert.equal(p.opts.variant, 'V1');
      assert.equal(p.opts.geneId, 'g0');
    } finally {
      fs.unlinkSync(f);
    }
  });

  it('rejects a --request-file that is not a regular file', () => {
    const p = parseExperimentArgs(['--request-file=' + os.tmpdir(), '--task=T', '--metric=M']);
    assert.equal(p.ok, false);
  });
});

describe('runExperiment — DI + secret redaction', () => {
  it('redacts secrets in arm resultText before returning data', async () => {
    const leaky = 'sk-ant-' + 'A'.repeat(30);
    const runner = async () => ({ ok: true, durationMs: 1, rounds: 1, resultText: 'output ' + leaky });
    const res = await runExperiment(
      { task: 'T', metric: '轮次' },
      { agentRunner: runner, geneLoader: () => [] },
    );
    assert.equal(res.ok, true);
    assert.ok(!JSON.stringify(res.data).includes(leaky), 'secret must not survive in output');
    assert.ok(res.data.arms.baseline.resultText.includes('[REDACTED]'));
  });

  it('passes deps.sandbox through to runComparison (key not dropped)', async () => {
    let sawCwd = null;
    const sandbox = {
      createSandboxDir: () => '/tmp/exp-di',
      cleanupDir: () => {},
      runSingleCommand: async (_cmd, opts) => { sawCwd = opts && opts.cwd; return { ok: true }; },
    };
    const res = await runExperiment(
      { task: 'T', metric: '通过率', geneId: 'gene_x', validationCommands: ['node check.js'] },
      { agentRunner: fakeRunner({}, {}), geneLoader: genesFix, sandbox },
    );
    assert.equal(res.ok, true);
    assert.equal(sawCwd, '/tmp/exp-di'); // proves the injected sandbox was actually used
    assert.equal(res.data.arms.baseline.passRate, 1);
  });

  it('inconclusive stderr names the actual cause: unmeasured pass-rate vs failed arms', async () => {
    const messages = [];
    const err = (...a) => messages.push(a.join(' '));

    // Cause 1: both arms ok, metric is pass-rate, no validation commands.
    messages.length = 0;
    let res = await runExperiment(
      { task: 'T', metric: '通过率', geneId: 'gene_x' },
      { agentRunner: fakeRunner({}, {}), geneLoader: genesFix, err },
    );
    assert.equal(res.data.winner, 'inconclusive');
    assert.equal(res.exitCode, 3);
    assert.match(messages.join('\n'), /never measured/);
    assert.doesNotMatch(messages.join('\n'), /arms failed/);

    // Cause 2: an arm actually failed.
    messages.length = 0;
    const failingRunner = async (prompt) => (
      String(prompt).includes(VARIANT_MARK)
        ? { ok: false, isError: true, error: 'agent_exit_1' }
        : { ok: true, isError: false, durationMs: 10 }
    );
    res = await runExperiment(
      { task: 'T', metric: '完成耗时', geneId: 'gene_x' },
      { agentRunner: failingRunner, geneLoader: genesFix, err },
    );
    assert.equal(res.data.winner, 'inconclusive');
    assert.match(messages.join('\n'), /one or both arms failed/);
  });
});
