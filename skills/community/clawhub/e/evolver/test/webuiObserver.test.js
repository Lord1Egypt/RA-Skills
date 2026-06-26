'use strict';

const { describe, it, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');

const ENV_KEYS = [
  'EVOLUTION_DIR',
  'GEP_ASSETS_DIR',
  'EVOLVER_REPO_ROOT',
  'MEMORY_DIR',
  'SKILLS_DIR',
  'AGENT_SESSIONS_DIR',
  'EVOLVER_LOGS_DIR',
  'EVOLVER_SETTINGS_DIR',
  'EVOLVER_ATP_AUTOBUY',
  'ATP_AUTOBUY_DAILY_CAP_CREDITS',
  'ATP_AUTOBUY_PER_ORDER_CAP_CREDITS',
  'EVOLVER_AUTO_PUBLISH',
  'EVOLVER_VALIDATOR_ENABLED',
];

function freshObserver() {
  for (const key of Object.keys(require.cache)) {
    if (key.includes(`${path.sep}src${path.sep}webui${path.sep}`) || key.endsWith(`${path.sep}src${path.sep}gep${path.sep}paths.js`)) {
      delete require.cache[key];
    }
  }
  return require('../src/webui/observer');
}

function writeJson(filePath, value) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, JSON.stringify(value, null, 2) + '\n', 'utf8');
}

function appendJsonl(filePath, rows) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, rows.map((row) => JSON.stringify(row)).join('\n') + '\n', 'utf8');
}

describe('webui observer', () => {
  let tmpDir;
  let savedEnv;

  beforeEach(() => {
    tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'webui-observer-'));
    savedEnv = {};
    for (const key of ENV_KEYS) {
      savedEnv[key] = process.env[key];
      delete process.env[key];
    }
    process.env.EVOLUTION_DIR = path.join(tmpDir, 'evolution');
    process.env.GEP_ASSETS_DIR = path.join(tmpDir, 'assets', 'gep');
    process.env.EVOLVER_REPO_ROOT = tmpDir;
    process.env.MEMORY_DIR = path.join(tmpDir, 'memory');
    process.env.SKILLS_DIR = path.join(tmpDir, 'skills');
    process.env.AGENT_SESSIONS_DIR = path.join(tmpDir, 'sessions');
    process.env.EVOLVER_LOGS_DIR = path.join(tmpDir, 'logs');
    // Isolate the proxy settings file from sibling test workers writing to
    // the shared ~/.evolver/settings.json. Without this, a parallel proxy
    // server test causes getStatus() to return mode='proxy_only' instead of
    // 'idle' for the "files are missing" case.
    process.env.EVOLVER_SETTINGS_DIR = path.join(tmpDir, 'settings');
  });

  afterEach(() => {
    for (const key of ENV_KEYS) {
      if (savedEnv[key] === undefined) delete process.env[key];
      else process.env[key] = savedEnv[key];
    }
    fs.rmSync(tmpDir, { recursive: true, force: true });
  });

  it('reports safe default status when files are missing', () => {
    const observer = freshObserver();
    const status = observer.getStatus();

    assert.equal(status.mode, 'idle');
    assert.equal(status.safety.safeMode, true);
    assert.equal(status.filesPresent.events, false);
  });

  it('normalizes runs from cycle state, events, and asset calls', () => {
    const evoDir = process.env.EVOLUTION_DIR;
    const gepDir = process.env.GEP_ASSETS_DIR;
    writeJson(path.join(evoDir, 'cycle_progress.json'), {
      run_id: 'run-1',
      outer_cycle: 7,
      phase: 'evolve.run',
      started_at: Date.now() - 1000,
      updated_at: Date.now(),
    });
    writeJson(path.join(evoDir, 'evolution_solidify_state.json'), {
      pending: true,
      last_run: { run_id: 'run-1', selected_gene_id: 'gene_a', validation: { ok: true } },
    });
    appendJsonl(path.join(gepDir, 'events.jsonl'), [
      { id: 'evt-1', run_id: 'run-1', genes_used: ['gene_a'], outcome: { status: 'success' } },
    ]);
    appendJsonl(path.join(evoDir, 'asset_call_log.jsonl'), [
      { run_id: 'run-1', action: 'hub_search_hit', asset_id: 'asset-1', timestamp: new Date().toISOString() },
    ]);

    const observer = freshObserver();
    const runs = observer.listRuns().data;
    const detail = observer.getRun('run-1');

    assert.equal(runs.length, 1);
    assert.equal(runs[0].selectedGeneId, 'gene_a');
    assert.equal(runs[0].requiresConfirmation, true);
    // Regression: asset_call_log entries used to overwrite a successful event
    // outcome with a hardcoded "running" status, so any run with asset calls
    // appeared perpetually running. Ensure the event-derived terminal status
    // wins instead.
    assert.equal(runs[0].status, 'completed');
    assert.ok(detail.phases.some((phase) => phase.phase === 'asset_search' && phase.status === 'success'));
  });

  it('reclassifies stale "running" runs as abandoned', () => {
    const evoDir = process.env.EVOLUTION_DIR;
    const oldTs = new Date(Date.now() - 8 * 60 * 60 * 1000).toISOString(); // 8h ago
    const freshTs = new Date(Date.now() - 60 * 1000).toISOString();        // 1m ago
    appendJsonl(path.join(evoDir, 'pipeline_events.jsonl'), [
      { run_id: 'run-old',   phase: 'evolve.run', status: 'running', started_at: oldTs,   timestamp: oldTs },
      { run_id: 'run-fresh', phase: 'evolve.run', status: 'running', started_at: freshTs, timestamp: freshTs },
    ]);

    const observer = freshObserver();
    const runs = observer.listRuns().data;
    const oldRun = runs.find((r) => r.runId === 'run-old');
    const freshRun = runs.find((r) => r.runId === 'run-fresh');

    assert.equal(oldRun.status, 'abandoned', '8h-old running run with no finishedAt should be abandoned');
    assert.equal(freshRun.status, 'running', 'recent running run should still show running');
  });

  it('respects EVOLVER_RUN_STUCK_THRESHOLD_MS override', () => {
    const evoDir = process.env.EVOLUTION_DIR;
    const ts = new Date(Date.now() - 5 * 60 * 1000).toISOString(); // 5m ago
    appendJsonl(path.join(evoDir, 'pipeline_events.jsonl'), [
      { run_id: 'run-x', phase: 'evolve.run', status: 'running', started_at: ts, timestamp: ts },
    ]);

    process.env.EVOLVER_RUN_STUCK_THRESHOLD_MS = '60000'; // 1 minute
    try {
      const observer = freshObserver();
      const run = observer.listRuns().data.find((r) => r.runId === 'run-x');
      assert.equal(run.status, 'abandoned', '5m-old running run should exceed 1m threshold');
    } finally {
      delete process.env.EVOLVER_RUN_STUCK_THRESHOLD_MS;
    }
  });

  it('lists assets and lineage without leaking secrets', () => {
    const gepDir = process.env.GEP_ASSETS_DIR;
    writeJson(path.join(gepDir, 'genes.json'), {
      genes: [{ type: 'Gene', id: 'gene_secret', category: 'repair', node_secret: 'secret-value' }],
    });
    writeJson(path.join(gepDir, 'capsules.json'), {
      capsules: [{ type: 'Capsule', id: 'cap-1', gene: 'gene_secret', outcome: { status: 'success' } }],
    });
    appendJsonl(path.join(gepDir, 'events.jsonl'), [
      { id: 'evt-1', genes_used: ['gene_secret'], capsule_id: 'cap-1' },
    ]);

    const observer = freshObserver();
    const genes = observer.listGenes().data;
    const lineage = observer.getLineage('gene_secret');

    assert.equal(genes[0].node_secret, '[REDACTED]');
    assert.equal(lineage.capsules.length, 1);
    assert.equal(lineage.events.length, 1);
  });

  it('getStatus redacts solidify.last_run before returning it', () => {
    // Cursor agentic security review (MEDIUM): /webui/status used to
    // surface solidify.last_run verbatim, while every other observer
    // endpoint routes its payload through redactValue. last_run carries
    // prompt + task context that often embeds API keys; without the
    // filter the unauthenticated local endpoint became the easy
    // exfiltration path.
    const evoDir = process.env.EVOLUTION_DIR;
    writeJson(path.join(evoDir, 'evolution_solidify_state.json'), {
      pending: false,
      last_run: {
        run_id: 'run-secret',
        api_key: 'sk-leakage-1234',
        initial_user_prompt: 'plain prose, do not redact',
      },
    });

    const observer = freshObserver();
    const status = observer.getStatus();

    assert.ok(status.lastRun, 'lastRun should be populated');
    assert.equal(status.lastRun.run_id, 'run-secret');
    assert.equal(status.lastRun.api_key, '[REDACTED]', 'object-key redaction must apply');
    assert.equal(status.lastRun.initial_user_prompt, 'plain prose, do not redact');
  });

  it('redactText covers env-style credentials beyond SECRET / TOKEN', () => {
    // Cursor agentic security review (HIGH): the original SECRET_TEXT_RE
    // only masked Bearer / *SECRET* / *TOKEN* shapes, so plaintext
    // credentials like OPENAI_API_KEY=sk-... and DB_PASSWORD=... slipped
    // through and were exposed via /webui/logs/evolver.
    const observer = freshObserver();
    const { redactText } = require('../src/webui/observer/redact');

    const cases = [
      ['Bearer abc.def.ghi', /Bearer \[REDACTED\]/],
      ['MY_SECRET=hunter2', /MY_SECRET=\[REDACTED\]/],
      ['OPENAI_API_KEY=sk-abcdef0123456789abcdef', /OPENAI_API_KEY=\[REDACTED\]/],
      ['ANTHROPIC_API_KEY=sk-ant-abcdef0123456789abc', /ANTHROPIC_API_KEY=\[REDACTED\]/],
      ['DB_PASSWORD=hunter2pls', /DB_PASSWORD=\[REDACTED\]/],
      ['Standalone sk-ant-abcdef0123456789xyzqwertyuiop12345', /Standalone \[REDACTED\]/],
    ];
    for (const [input, expected] of cases) {
      assert.match(redactText(input), expected, `redactText should mask: ${input}`);
    }

    assert.equal(
      redactText('the monkey jumped over the fence'),
      'the monkey jumped over the fence',
      'plain prose without credential shapes must pass through unchanged',
    );
  });
});
