const { describe, it, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const os = require('os');
const path = require('path');

const envKeys = ['EVOLUTION_DIR', 'MEMORY_DIR', 'EVOLVER_REPO_ROOT'];

function freshRequire(modulePath) {
  const resolved = require.resolve(modulePath);
  delete require.cache[resolved];
  return require(resolved);
}

function loadMod(tmpDir) {
  process.env.EVOLUTION_DIR = tmpDir;
  delete require.cache[require.resolve('../src/gep/paths')];
  return freshRequire('../src/gep/curriculum');
}

function writeMemoryGraph(memoryGraphPath, events) {
  const lines = events.map((e) => JSON.stringify(e)).join('\n') + '\n';
  fs.writeFileSync(memoryGraphPath, lines, 'utf8');
}

function successEvent(key) {
  return { kind: 'outcome', signal_key: key, outcome: { status: 'success' } };
}
function failedEvent(key) {
  return { kind: 'outcome', signal_key: key, outcome: { status: 'failed' } };
}

describe('curriculum', () => {
  let tmpDir;
  let savedEnv;
  let mod;
  let memoryGraphPath;

  beforeEach(() => {
    tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'curriculum-test-'));
    savedEnv = {};
    for (const k of envKeys) {
      savedEnv[k] = process.env[k];
      delete process.env[k];
    }
    mod = loadMod(tmpDir);
    memoryGraphPath = path.join(tmpDir, 'memory_graph.jsonl');
  });

  afterEach(() => {
    for (const k of envKeys) {
      if (savedEnv[k] === undefined) delete process.env[k];
      else process.env[k] = savedEnv[k];
    }
    fs.rmSync(tmpDir, { recursive: true, force: true });
  });

  describe('loadCurriculumState', () => {
    it('returns a fresh default when state file is absent', () => {
      const s = mod.loadCurriculumState();
      assert.equal(s.level, 1);
      assert.deepEqual(s.current_targets, []);
      assert.deepEqual(s.completed, []);
      assert.equal(s.updated_at, null);
    });

    it('returns the default when file is empty or invalid JSON', () => {
      const statePath = path.join(tmpDir, 'curriculum_state.json');
      fs.writeFileSync(statePath, '', 'utf8');
      assert.equal(mod.loadCurriculumState().level, 1);
      fs.writeFileSync(statePath, '{not json', 'utf8');
      assert.equal(mod.loadCurriculumState().level, 1);
    });
  });

  describe('generateCurriculumSignals', () => {
    it('returns empty array when no capability gaps and no memory graph', () => {
      const signals = mod.generateCurriculumSignals({
        capabilityGaps: [],
        memoryGraphPath: '',
      });
      assert.deepEqual(signals, []);
    });

    it('emits a gap-target signal when capabilityGaps is provided', () => {
      const signals = mod.generateCurriculumSignals({
        capabilityGaps: ['skill_install'],
        memoryGraphPath,
      });
      assert.equal(signals.length, 1);
      assert.ok(signals[0].startsWith('curriculum_target:gap:'));
      assert.ok(signals[0].includes('skill_install'));
    });

    it('skips the gap when that capability is already mastered', () => {
      // 4 successes out of 4 total for 'skill_install' -> mastered.
      const events = [];
      for (let i = 0; i < 4; i++) events.push(successEvent('skill_install_ok'));
      writeMemoryGraph(memoryGraphPath, events);

      const signals = mod.generateCurriculumSignals({
        capabilityGaps: ['skill_install'],
        memoryGraphPath,
      });
      // No gap target since it's mastered; no frontier either (rate is 1.0).
      assert.ok(!signals.some((s) => s.startsWith('curriculum_target:gap:')));
    });

    it('emits a frontier signal for a mid-rate key', () => {
      const events = [
        successEvent('perf_tune'),
        failedEvent('perf_tune'),
        successEvent('perf_tune'),
        failedEvent('perf_tune'),
      ];
      writeMemoryGraph(memoryGraphPath, events);

      const signals = mod.generateCurriculumSignals({
        capabilityGaps: [],
        memoryGraphPath,
      });
      assert.ok(signals.some((s) => s.startsWith('curriculum_target:frontier:')));
      assert.ok(signals[0].includes('perf_tune'));
    });

    it('caps output at 2 signals', () => {
      const events = [];
      for (let i = 0; i < 3; i++) {
        events.push(successEvent('alpha'), failedEvent('alpha'));
        events.push(successEvent('beta'), failedEvent('beta'));
        events.push(successEvent('gamma'), failedEvent('gamma'));
      }
      writeMemoryGraph(memoryGraphPath, events);

      const signals = mod.generateCurriculumSignals({
        capabilityGaps: ['alpha'],
        memoryGraphPath,
      });
      assert.ok(signals.length <= 2);
    });

    it('persists state when signals are produced', () => {
      const signals = mod.generateCurriculumSignals({
        capabilityGaps: ['skill_install'],
        memoryGraphPath,
      });
      assert.ok(signals.length > 0);
      const state = mod.loadCurriculumState();
      assert.ok(Array.isArray(state.current_targets));
      assert.equal(state.current_targets.length, signals.length);
      assert.ok(state.updated_at);
    });

    it('does not persist state when no signals are produced', () => {
      const signals = mod.generateCurriculumSignals({
        capabilityGaps: [],
        memoryGraphPath: '',
      });
      assert.deepEqual(signals, []);
      assert.equal(fs.existsSync(path.join(tmpDir, 'curriculum_state.json')), false);
    });

    it('skips non-outcome events and corrupt lines', () => {
      fs.writeFileSync(
        memoryGraphPath,
        [
          JSON.stringify({ kind: 'heartbeat', signal_key: 'x' }),
          'not-json-at-all',
          JSON.stringify({ kind: 'outcome', outcome: { status: 'success' } }), // no key
          JSON.stringify(successEvent('legit')),
          JSON.stringify(failedEvent('legit')),
        ].join('\n') + '\n',
        'utf8'
      );
      const signals = mod.generateCurriculumSignals({
        capabilityGaps: [],
        memoryGraphPath,
      });
      // With only 2 events for 'legit' at 50% rate it is a valid frontier key.
      assert.ok(signals.some((s) => s.includes('legit')));
    });

    it('truncates very long capability gap names to 60 chars', () => {
      const longName = 'x'.repeat(200);
      const signals = mod.generateCurriculumSignals({
        capabilityGaps: [longName],
        memoryGraphPath,
      });
      assert.equal(signals.length, 1);
      const suffix = signals[0].slice('curriculum_target:gap:'.length);
      assert.ok(suffix.length <= 60);
    });
  });

  describe('markCurriculumProgress', () => {
    it('appends an entry with signal, outcome, and timestamp', () => {
      mod.markCurriculumProgress('curriculum_target:gap:xyz', 'success');
      const s = mod.loadCurriculumState();
      assert.equal(s.completed.length, 1);
      assert.equal(s.completed[0].signal, 'curriculum_target:gap:xyz');
      assert.equal(s.completed[0].outcome, 'success');
      assert.ok(s.completed[0].at);
    });

    it('levels up every 5 successes, capped at level 5', () => {
      for (let i = 0; i < 5; i++) {
        mod.markCurriculumProgress(`s${i}`, 'success');
      }
      assert.equal(mod.loadCurriculumState().level, 2);

      for (let i = 0; i < 20; i++) {
        mod.markCurriculumProgress(`more_${i}`, 'success');
      }
      assert.equal(mod.loadCurriculumState().level, 5);
    });

    it('does not level up on failed outcomes', () => {
      for (let i = 0; i < 10; i++) {
        mod.markCurriculumProgress(`f${i}`, 'failed');
      }
      assert.equal(mod.loadCurriculumState().level, 1);
    });

    it('caps completed history at 50 entries', () => {
      for (let i = 0; i < 75; i++) {
        mod.markCurriculumProgress(`entry_${i}`, 'success');
      }
      const s = mod.loadCurriculumState();
      assert.equal(s.completed.length, 50);
      assert.equal(s.completed[0].signal, 'entry_25');
      assert.equal(s.completed[49].signal, 'entry_74');
    });

    it('truncates very long signal/outcome strings', () => {
      const longSignal = 's'.repeat(500);
      const longOutcome = 'o'.repeat(100);
      mod.markCurriculumProgress(longSignal, longOutcome);
      const s = mod.loadCurriculumState();
      assert.ok(s.completed[0].signal.length <= 100);
      assert.ok(s.completed[0].outcome.length <= 20);
    });
  });
});
