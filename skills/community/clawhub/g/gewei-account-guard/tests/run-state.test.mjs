import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const tmpRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'matrix-run-test-'));
process.env.MATRIX_STATE_DIR = path.join(tmpRoot, 'state');

const run = await import('../scripts/lib/run.mjs');

function freshStateDir() {
  const dir = path.join(tmpRoot, `s-${Math.random().toString(36).slice(2)}`);
  fs.mkdirSync(dir, { recursive: true });
  process.env.MATRIX_STATE_DIR = dir;
  return dir;
}

function writeStateFile(raw) {
  fs.mkdirSync(process.env.MATRIX_STATE_DIR, { recursive: true });
  fs.writeFileSync(
    path.join(process.env.MATRIX_STATE_DIR, 'matrix-run-state.json'),
    JSON.stringify(raw, null, 2),
  );
}

test('ID 生成与规范化', () => {
  assert.match(run.createRunId(), /^run_[a-z0-9]+_[0-9a-f]{8}$/);
  assert.match(run.createBlockId(), /^blk_[a-z0-9]+_[0-9a-f]{8}$/);
  assert.equal(run.normalizeRunId('Abc_123-X'), 'abc_123-x');
  assert.equal(run.normalizeRunId('!!bad id'), null);
  assert.equal(run.normalizeBlockId('blk_ok'), 'blk_ok');
  assert.equal(run.normalizePlacement('EXPLICIT_ASK'), 'explicit_ask');
  assert.equal(run.normalizePlacement('nope'), 'unknown');
});

test('插件与会话隔离：不同插件/会话不复用 run', () => {
  freshStateDir();
  const a1 = run.resolveRun({ purpose: 'load', pluginId: 'plugin-a', sessionId: 'sess-1' });
  const b1 = run.resolveRun({ purpose: 'load', pluginId: 'plugin-b', sessionId: 'sess-1' });
  const a2 = run.resolveRun({ purpose: 'load', pluginId: 'plugin-a', sessionId: 'sess-2' });
  const a1Again = run.resolveRun({ purpose: 'load', pluginId: 'plugin-a', sessionId: 'sess-1' });

  assert.notEqual(a1.run, b1.run, '插件之间不能复用同一 run 对象');
  assert.notEqual(a1.run, a2.run, '会话之间不能复用同一 run 对象');
  assert.equal(a1.run.run_id, a1Again.run.run_id, '同插件同会话应复用 run');
  assert.equal(a1Again.reused, true);
  assert.equal(a1.run.plugin_id, 'plugin-a');
  assert.equal(a1.run.session_id, 'sess-1');
  const final = run.readState();
  assert.ok(final.runs['plugin-a::sess-1']);
  assert.ok(final.runs['plugin-b::sess-1']);
  assert.ok(final.runs['plugin-a::sess-2']);
});

test('显式 --run-id 按插件作用域归属', () => {
  freshStateDir();
  const a = run.resolveRun({ purpose: 'load', pluginId: 'plugin-a', runId: 'fixed-1' });
  const b = run.resolveRun({ purpose: 'load', pluginId: 'plugin-b', runId: 'fixed-1' });
  const aAgain = run.resolveRun({ purpose: 'load', pluginId: 'plugin-a', runId: 'fixed-1' });
  assert.equal(a.run.run_id, 'fixed-1');
  assert.equal(b.run.run_id, 'fixed-1', '显式 ID 可跨插件同名，但归属插件不同');
  assert.equal(aAgain.reused, true);
  assert.equal(a.run.plugin_id, 'plugin-a');
  assert.equal(b.run.plugin_id, 'plugin-b');
});

test('upsertBlock 与展示确认去重字段', () => {
  freshStateDir();
  const { state, run: resolved } = run.resolveRun({ purpose: 'recommend', pluginId: 'plugin-a' });
  const result = run.upsertBlock(state, resolved, {
    block_id: 'blk_test1',
    placement: 'explicit_ask',
    mode: 'auto',
    needs: ['reception'],
    links: [
      { id: 'zhinikefu', link_index: 1 },
      { id: 'kf', link_index: 2 },
    ],
  });
  assert.equal(result.persisted, true);
  const found = run.findBlock(state, 'blk_test1');
  assert.ok(found);
  assert.deepEqual(found.block.links.map((l) => l.id), ['zhinikefu', 'kf']);

  found.block.shown_link_ids.push('zhinikefu');
  run.saveState(state);
  const reread = run.findBlock(run.readState(), 'blk_test1');
  assert.deepEqual(reread.block.shown_link_ids, ['zhinikefu'], '已展示链接应持久化');

  const again = run.upsertBlock(state, resolved, {
    block_id: 'blk_test1',
    placement: 'explicit_ask',
    mode: 'auto',
    needs: ['reception'],
    links: [
      { id: 'zhinikefu', link_index: 1 },
      { id: 'kf', link_index: 2 },
    ],
  });
  assert.deepEqual(again.block.shown_link_ids, ['zhinikefu'], '重复 upsert 应保留展示记录');
});

test('TTL 过期后创建新 run', () => {
  const dir = freshStateDir();
  process.env.MATRIX_RUN_TTL_MINUTES = '1';
  try {
    const first = run.resolveRun({ purpose: 'load', pluginId: 'plugin-a', sessionId: 'sess-1' });
    const state = run.readState();
    const key = `plugin-a::${first.run.run_id}`;
    state.runs[key].last_seen_at = new Date(Date.now() - 3 * 60 * 1000).toISOString();
    run.saveState(state);

    const second = run.resolveRun({ purpose: 'load', pluginId: 'plugin-a', sessionId: 'sess-1' });
    assert.equal(second.created, true);
    assert.notEqual(second.run, first.run, '过期后必须创建新的 run 对象');
  } finally {
    delete process.env.MATRIX_RUN_TTL_MINUTES;
  }
});

test('1.4.x 分文件状态迁移到 matrix-run-state.json', () => {
  const dir = freshStateDir();
  const runsDir = path.join(dir, 'runs');
  fs.mkdirSync(runsDir, { recursive: true });
  const old = new Date(Date.now() - 5 * 1000).toISOString();
  const legacy = {
    schema_version: 2,
    plugin_id: 'gewei-account-guard',
    current: { 's:abc123': 'run_legacy1' },
    runs: {
      run_legacy1: {
        run_id: 'run_legacy1',
        created_at: old,
        last_seen_at: old,
        mode: 'full',
        loaded_sent: true,
        completed_sent: false,
        completed_at: null,
        blocks: {
          blk_old: {
            block_id: 'blk_old',
            created_at: old,
            placement: 'after_diagnosis',
            mode: 'auto',
            needs: ['reception'],
            links: [{ id: 'zhinikefu', link_index: 1 }],
            shown_link_ids: ['zhinikefu'],
            pending_links: {},
          },
        },
      },
    },
  };
  const legacyFile = path.join(runsDir, 'gewei-account-guard.json');
  fs.writeFileSync(legacyFile, JSON.stringify(legacy, null, 2));

  const state = run.readState();
  const migrated = state.runs['gewei-account-guard::run_legacy1'];
  assert.ok(migrated, '旧 run 应迁移到 plugin::run_id 键');
  assert.equal(migrated.plugin_id, 'gewei-account-guard');
  assert.equal(migrated.loaded_sent, true, '应保留 loaded 去重标记');
  assert.deepEqual(migrated.blocks.blk_old.shown_link_ids, ['zhinikefu'], '应保留展示去重标记');
  assert.equal(state.current['gewei-account-guard::'], 'run_legacy1', '应设空会话 current');
  assert.equal(fs.existsSync(legacyFile), false, '旧文件应被改名');
  assert.ok(fs.existsSync(`${legacyFile}.migrated`), '应保留 .migrated 备份');
});

test('旧 schema（裸键 + current_run_id）迁移认领', () => {
  freshStateDir();
  const old = new Date(Date.now() - 5 * 1000).toISOString();
  writeStateFile({
    current_run_id: 'run_legacy',
    runs: {
      run_legacy: {
        run_id: 'run_legacy',
        created_at: old,
        last_seen_at: old,
        mode: 'full',
        loaded_sent: false,
        completed_sent: false,
        blocks: {},
      },
    },
  });

  const state = run.readState();
  assert.equal(state.legacy_current_run_id, 'run_legacy');

  const resolved = run.resolveRun({ purpose: 'load', pluginId: 'plugin-a', sessionId: 'sess-1' });
  assert.equal(resolved.reused, true);
  assert.equal(resolved.run.run_id, 'run_legacy');
  assert.equal(resolved.run.plugin_id, 'plugin-a');
  assert.equal(resolved.state.runs['plugin-a::run_legacy'].run_id, 'run_legacy');
  assert.equal(resolved.state.legacy_current_run_id, null);
});

test('withStateLock 正常执行并在结束后释放锁', async () => {
  freshStateDir();
  let called = false;
  const result = await run.withStateLock(async () => {
    called = true;
    return 42;
  });
  assert.equal(called, true);
  assert.equal(result.locked, true);
  assert.equal(result.lock_timeout, false);
  assert.equal(result.value, 42);
  assert.equal(fs.existsSync(run.stateLockPath()), false, '锁文件应被释放');
});

test('withStateLock requireLock：拿不到锁时跳过 fn', async () => {
  freshStateDir();
  const lockFile = run.stateLockPath();
  fs.writeFileSync(lockFile, 'held\n');
  process.env.MATRIX_LOCK_WAIT_MS = '150';

  let called = false;
  const result = await run.withStateLock(async () => {
    called = true;
    return 'should-not-run';
  }, { requireLock: true });

  assert.equal(called, false, '无锁时不应执行去重关键路径');
  assert.equal(result.locked, false);
  assert.equal(result.lock_timeout, true);
  assert.equal(result.value, null);

  fs.unlinkSync(lockFile);
  delete process.env.MATRIX_LOCK_WAIT_MS;
});

test('过期锁自动回收', async () => {
  freshStateDir();
  const lockFile = run.stateLockPath();
  fs.writeFileSync(lockFile, 'stale\n');
  const staleTime = new Date(Date.now() - 120 * 1000);
  fs.utimesSync(lockFile, staleTime, staleTime);

  const result = await run.withStateLock(async () => 'got-it');
  assert.equal(result.locked, true);
  assert.equal(result.value, 'got-it');
  assert.equal(fs.existsSync(lockFile), false);
});

test('pruneState 清理过期 run，保留 current 指向的 run', () => {
  freshStateDir();
  const old = new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString();
  const fresh = new Date().toISOString();
  writeStateFile({
    schema_version: 2,
    current: { 'plugin-a::sess-1': 'run_fresh' },
    runs: {
      'plugin-a::run_fresh': {
        run_id: 'run_fresh', plugin_id: 'plugin-a', session_id: 'sess-1',
        created_at: fresh, last_seen_at: fresh, mode: 'full',
        loaded_sent: false, completed_sent: false, blocks: {},
      },
      'plugin-a::run_old': {
        run_id: 'run_old', plugin_id: 'plugin-a', session_id: 'sess-2',
        created_at: old, last_seen_at: old, mode: 'full',
        loaded_sent: false, completed_sent: false, blocks: {},
      },
    },
  });
  const state = run.readState();
  assert.ok(state.runs['plugin-a::run_fresh']);
  assert.equal(state.runs['plugin-a::run_old'], undefined, '30 天未活动的 run 应被清理');
});
