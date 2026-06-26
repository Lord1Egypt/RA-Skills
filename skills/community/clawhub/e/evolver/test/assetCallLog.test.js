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

describe('assetCallLog', () => {
  let tmpDir;
  let savedEnv;
  let mod;

  beforeEach(() => {
    tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'asset-call-log-test-'));
    savedEnv = {};
    for (const k of envKeys) {
      savedEnv[k] = process.env[k];
      delete process.env[k];
    }
    process.env.EVOLUTION_DIR = tmpDir;

    delete require.cache[require.resolve('../src/gep/paths')];
    mod = freshRequire('../src/gep/assetCallLog');
  });

  afterEach(() => {
    for (const k of envKeys) {
      if (savedEnv[k] === undefined) delete process.env[k];
      else process.env[k] = savedEnv[k];
    }
    fs.rmSync(tmpDir, { recursive: true, force: true });
  });

  describe('getLogPath', () => {
    it('returns a path under EVOLUTION_DIR', () => {
      const logPath = mod.getLogPath();
      assert.ok(logPath.startsWith(tmpDir));
      assert.ok(logPath.endsWith('asset_call_log.jsonl'));
    });
  });

  describe('logAssetCall', () => {
    it('creates the log file on first write', () => {
      const logPath = mod.getLogPath();
      assert.ok(!fs.existsSync(logPath));
      mod.logAssetCall({ run_id: 'r1', action: 'asset_reuse', asset_id: 'a1' });
      assert.ok(fs.existsSync(logPath));
    });

    it('appends a newline-delimited JSON record with timestamp', () => {
      mod.logAssetCall({ run_id: 'r1', action: 'asset_publish', asset_id: 'a1' });
      const raw = fs.readFileSync(mod.getLogPath(), 'utf8');
      assert.ok(raw.endsWith('\n'));
      const parsed = JSON.parse(raw.trim());
      assert.equal(parsed.run_id, 'r1');
      assert.equal(parsed.action, 'asset_publish');
      assert.equal(parsed.asset_id, 'a1');
      assert.ok(typeof parsed.timestamp === 'string');
      assert.ok(!Number.isNaN(Date.parse(parsed.timestamp)));
    });

    it('appends subsequent records (does not overwrite)', () => {
      mod.logAssetCall({ run_id: 'r1', action: 'hub_search_hit' });
      mod.logAssetCall({ run_id: 'r1', action: 'asset_reuse' });
      mod.logAssetCall({ run_id: 'r2', action: 'asset_publish' });
      const lines = fs
        .readFileSync(mod.getLogPath(), 'utf8')
        .split('\n')
        .filter(Boolean);
      assert.equal(lines.length, 3);
    });

    it('silently ignores missing directory by creating it', () => {
      const nested = path.join(tmpDir, 'nested', 'deep');
      process.env.EVOLUTION_DIR = nested;
      delete require.cache[require.resolve('../src/gep/paths')];
      const nestedMod = freshRequire('../src/gep/assetCallLog');
      nestedMod.logAssetCall({ run_id: 'r1', action: 'hub_search_miss' });
      assert.ok(fs.existsSync(nestedMod.getLogPath()));
    });

    it('no-ops on invalid entry without throwing', () => {
      mod.logAssetCall(null);
      mod.logAssetCall(undefined);
      mod.logAssetCall('not-an-object');
      mod.logAssetCall(42);
      assert.ok(!fs.existsSync(mod.getLogPath()));
    });
  });

  describe('readCallLog', () => {
    it('returns empty array when log file does not exist', () => {
      assert.deepEqual(mod.readCallLog(), []);
    });

    it('parses all valid JSON lines', () => {
      mod.logAssetCall({ run_id: 'r1', action: 'a' });
      mod.logAssetCall({ run_id: 'r2', action: 'b' });
      const entries = mod.readCallLog();
      assert.equal(entries.length, 2);
    });

    it('skips corrupt lines instead of throwing', () => {
      mod.logAssetCall({ run_id: 'r1', action: 'a' });
      fs.appendFileSync(mod.getLogPath(), 'not-json-at-all\n', 'utf8');
      mod.logAssetCall({ run_id: 'r2', action: 'b' });
      const entries = mod.readCallLog();
      assert.equal(entries.length, 2);
      assert.equal(entries[0].run_id, 'r1');
      assert.equal(entries[1].run_id, 'r2');
    });

    it('filters by run_id', () => {
      mod.logAssetCall({ run_id: 'r1', action: 'a' });
      mod.logAssetCall({ run_id: 'r2', action: 'a' });
      mod.logAssetCall({ run_id: 'r1', action: 'b' });
      const entries = mod.readCallLog({ run_id: 'r1' });
      assert.equal(entries.length, 2);
      assert.ok(entries.every((e) => e.run_id === 'r1'));
    });

    it('filters by action', () => {
      mod.logAssetCall({ run_id: 'r1', action: 'asset_reuse' });
      mod.logAssetCall({ run_id: 'r1', action: 'asset_publish' });
      const entries = mod.readCallLog({ action: 'asset_reuse' });
      assert.equal(entries.length, 1);
      assert.equal(entries[0].action, 'asset_reuse');
    });

    it('filters by since (inclusive)', () => {
      const now = Date.now();
      const old = new Date(now - 60_000).toISOString();
      const recent = new Date(now).toISOString();
      fs.writeFileSync(
        mod.getLogPath(),
        JSON.stringify({ timestamp: old, run_id: 'r1', action: 'a' }) +
          '\n' +
          JSON.stringify({ timestamp: recent, run_id: 'r2', action: 'a' }) +
          '\n',
        'utf8'
      );
      const entries = mod.readCallLog({ since: new Date(now - 1000).toISOString() });
      assert.equal(entries.length, 1);
      assert.equal(entries[0].run_id, 'r2');
    });

    it('ignores invalid since value', () => {
      mod.logAssetCall({ run_id: 'r1', action: 'a' });
      mod.logAssetCall({ run_id: 'r2', action: 'b' });
      const entries = mod.readCallLog({ since: 'not-a-date' });
      assert.equal(entries.length, 2);
    });

    it('applies last N after filters', () => {
      for (let i = 0; i < 5; i++) {
        mod.logAssetCall({ run_id: 'r1', action: 'a', seq: i });
      }
      const entries = mod.readCallLog({ last: 2 });
      assert.equal(entries.length, 2);
      assert.equal(entries[0].seq, 3);
      assert.equal(entries[1].seq, 4);
    });

    it('combines run_id and action filters', () => {
      mod.logAssetCall({ run_id: 'r1', action: 'asset_reuse' });
      mod.logAssetCall({ run_id: 'r1', action: 'asset_publish' });
      mod.logAssetCall({ run_id: 'r2', action: 'asset_reuse' });
      const entries = mod.readCallLog({ run_id: 'r1', action: 'asset_reuse' });
      assert.equal(entries.length, 1);
      assert.equal(entries[0].run_id, 'r1');
      assert.equal(entries[0].action, 'asset_reuse');
    });
  });

  describe('summarizeCallLog', () => {
    it('returns zeroed summary on empty log', () => {
      const s = mod.summarizeCallLog();
      assert.equal(s.total_entries, 0);
      assert.equal(s.unique_assets, 0);
      assert.equal(s.unique_runs, 0);
      assert.deepEqual(s.by_action, {});
    });

    it('counts totals, unique assets/runs, and per-action buckets', () => {
      mod.logAssetCall({ run_id: 'r1', action: 'asset_reuse', asset_id: 'a1' });
      mod.logAssetCall({ run_id: 'r1', action: 'asset_reuse', asset_id: 'a2' });
      mod.logAssetCall({ run_id: 'r2', action: 'asset_publish', asset_id: 'a1' });
      const s = mod.summarizeCallLog();
      assert.equal(s.total_entries, 3);
      assert.equal(s.unique_assets, 2);
      assert.equal(s.unique_runs, 2);
      assert.equal(s.by_action.asset_reuse, 2);
      assert.equal(s.by_action.asset_publish, 1);
    });

    it('labels missing action as "unknown"', () => {
      mod.logAssetCall({ run_id: 'r1' });
      const s = mod.summarizeCallLog();
      assert.equal(s.by_action.unknown, 1);
    });

    it('passes filters through to readCallLog', () => {
      mod.logAssetCall({ run_id: 'r1', action: 'a' });
      mod.logAssetCall({ run_id: 'r2', action: 'a' });
      const s = mod.summarizeCallLog({ run_id: 'r1' });
      assert.equal(s.total_entries, 1);
      assert.equal(s.unique_runs, 1);
    });

    it('includes the entries array', () => {
      mod.logAssetCall({ run_id: 'r1', action: 'a' });
      const s = mod.summarizeCallLog();
      assert.ok(Array.isArray(s.entries));
      assert.equal(s.entries.length, 1);
    });
  });
});
