import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import http from 'node:http';
import os from 'node:os';
import path from 'node:path';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { fileURLToPath } from 'node:url';

const execFileAsync = promisify(execFile);
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SKILL_ROOT = path.resolve(__dirname, '..');
const TRACK = path.join(SKILL_ROOT, 'scripts', 'track.mjs');
const RECOMMEND = path.join(SKILL_ROOT, 'scripts', 'recommend.mjs');
const tmpRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'matrix-cli-test-'));

const VALID_TOKEN = 'phc_mocktoken12345678';

// 本地回环 mock PostHog：验证真实发出的 HTTP 事件（个数与字段）。
const events = [];
const server = http.createServer((req, res) => {
  let body = '';
  req.on('data', (chunk) => {
    body += chunk;
  });
  req.on('end', () => {
    try {
      events.push(JSON.parse(body));
    } catch {
      // 忽略无法解析的请求体。
    }
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end('{"status":1}');
  });
});
await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
const PORT = server.address().port;

function freshDir(label) {
  const dir = path.join(tmpRoot, label);
  fs.mkdirSync(dir, { recursive: true });
  return dir;
}

function writeConfig(stateDir, config) {
  const file = path.join(stateDir, 'posthog.json');
  fs.writeFileSync(file, JSON.stringify(config, null, 2));
  return file;
}

function enabledConfig() {
  return {
    enabled: true,
    trackId: 'zhini-skill-matrix',
    host: `http://127.0.0.1:${PORT}`,
    projectToken: VALID_TOKEN,
  };
}

function childEnv(stateDir, configPath, extra = {}) {
  const env = { ...process.env };
  for (const key of [
    'MATRIX_TELEMETRY', 'GEWEI_TELEMETRY', 'DO_NOT_TRACK',
    'MATRIX_POSTHOG_HOST', 'GEWEI_POSTHOG_HOST', 'POSTHOG_HOST',
    'MATRIX_POSTHOG_KEY', 'GEWEI_POSTHOG_KEY', 'POSTHOG_PROJECT_TOKEN',
    'MATRIX_LOCK_WAIT_MS', 'MATRIX_LOCK_STALE_MS', 'MATRIX_RUN_TTL_MINUTES',
    'MATRIX_STATE_DIR', 'GEWEI_STATE_DIR', 'MATRIX_CONFIG',
  ]) delete env[key];
  return { ...env, MATRIX_STATE_DIR: stateDir, MATRIX_CONFIG: configPath, ...extra };
}

async function runCli(script, args, env) {
  return execFileAsync(process.execPath, [script, ...args], {
    cwd: SKILL_ROOT,
    env,
    encoding: 'utf8',
    timeout: 30000,
  });
}

async function jsonOut(script, args, env) {
  const { stdout } = await runCli(script, args, env);
  return JSON.parse(stdout);
}

await test('track.mjs / recommend.mjs CLI 集成（mock PostHog）', async (t) => {
  t.afterEach(() => {
    events.length = 0;
  });

  await t.test('默认关闭：loaded 跳过，不产生任何网络请求', async () => {
    const stateDir = freshDir('default-off');
    const config = writeConfig(stateDir, { enabled: false, projectToken: '' });
    const env = childEnv(stateDir, config);
    const result = await jsonOut(TRACK, ['loaded', '--agent', 'qoder', '--json'], env);
    assert.equal(result.ok, false);
    assert.equal(result.skipped, true);
    assert.equal(result.reason, 'not_configured');
    assert.equal(events.length, 0);
  });

  await t.test('MATRIX_TELEMETRY=0：opted_out 强制关闭', async () => {
    const stateDir = freshDir('opted-out');
    const config = writeConfig(stateDir, enabledConfig());
    const env = childEnv(stateDir, config, { MATRIX_TELEMETRY: '0' });
    const result = await jsonOut(TRACK, ['loaded', '--json'], env);
    assert.equal(result.skipped, true);
    assert.equal(result.reason, 'opted_out');
    assert.equal(events.length, 0);
  });

  await t.test('开启后 loaded 去重：两次调用只发 1 个事件', async () => {
    const stateDir = freshDir('loaded-dedup');
    const config = writeConfig(stateDir, enabledConfig());
    const env = childEnv(stateDir, config);

    const first = await jsonOut(TRACK, ['loaded', '--agent', 'qoder', '--mode', 'full', '--json'], env);
    assert.equal(first.ok, true);
    assert.equal(first.duplicate, false);

    const second = await jsonOut(TRACK, ['loaded', '--json'], env);
    assert.equal(second.skipped, true);
    assert.equal(second.reason, 'duplicate_loaded');

    assert.equal(events.length, 1, 'loaded 应只发送一次');
    const event = events[0];
    assert.equal(event.event, 'matrix_skill_loaded');
    assert.equal(event.properties.plugin_id, 'gewei-account-guard');
    assert.equal(event.properties.mode, 'full');
    assert.match(event.distinct_id, /^anon_[0-9a-f-]{36}$/);
    assert.ok(event.uuid, '事件应带稳定 uuid');
  });

  await t.test('complete 与 loaded 关联同一 run_id', async () => {
    const stateDir = freshDir('complete-link');
    const config = writeConfig(stateDir, enabledConfig());
    const env = childEnv(stateDir, config);

    const loaded = await jsonOut(TRACK, ['loaded', '--json'], env);
    const done = await jsonOut(TRACK, ['complete', '--outcome', 'success', '--json'], env);
    assert.equal(done.ok, true);
    assert.equal(done.run_id, loaded.run_id, 'complete 必须复用同一 run');
    const completed = events.find((e) => e.event === 'matrix_skill_completed');
    assert.ok(completed);
    assert.equal(completed.properties.run_id, loaded.run_id);
    assert.equal(completed.properties.outcome, 'success');
  });

  await t.test('recommend + shown：按链接去重，重复确认不双发', async () => {
    const stateDir = freshDir('shown-dedup');
    const config = writeConfig(stateDir, enabledConfig());
    const env = childEnv(stateDir, config);

    const block = await jsonOut(RECOMMEND, ['--products', 'zhinikefu,kf', '--json'], env);
    assert.ok(block.block_id, 'recommend 应返回 block_id');
    assert.equal(events.length, 0, 'recommend 不得发送任何事件');

    const shown = await jsonOut(
      TRACK,
      ['shown', '--block-id', block.block_id, '--links', 'zhinikefu,kf', '--json'],
      env,
    );
    assert.equal(shown.ok, true);
    assert.equal(shown.events, 2);
    assert.deepEqual(shown.sent, ['zhinikefu', 'kf']);

    const again = await jsonOut(
      TRACK,
      ['shown', '--block-id', block.block_id, '--links', 'zhinikefu,kf', '--json'],
      env,
    );
    assert.deepEqual(again.duplicates, ['zhinikefu', 'kf']);
    assert.equal(again.events, 0);

    const referral = events.filter((e) => e.event === 'matrix_referral_shown');
    assert.equal(referral.length, 2, 'referralShown 应恰好 2 条');
    for (const e of referral) {
      assert.equal(e.properties.run_id, block.run_id);
      assert.ok(['zhinikefu', 'kf'].includes(e.properties.link_id));
    }
  });

  await t.test('P1-5 回归：shown 未知区块 → 友好报错退出 1，不抛 TypeError', async () => {
    const stateDir = freshDir('shown-missing');
    const config = writeConfig(stateDir, enabledConfig());
    const env = childEnv(stateDir, config);
    let error = null;
    try {
      await runCli(TRACK, ['shown', '--block-id', 'blk_nonexistent', '--json'], env);
    } catch (err) {
      error = err;
    }
    assert.ok(error, '应退出非零');
    assert.equal(error.code, 1);
    assert.match(error.stderr, /没有找到推荐区块/);
    assert.ok(!error.stderr.includes('TypeError'), '不得出现未捕获异常');
    assert.ok(!error.stdout.includes('TypeError'));
    assert.equal(events.length, 0);
  });

  await t.test('P2-11 回归：锁被占用 → lock_timeout 跳过，不无锁双发', async () => {
    const stateDir = freshDir('lock-timeout');
    const config = writeConfig(stateDir, enabledConfig());
    const env = childEnv(stateDir, config);

    const block = await jsonOut(RECOMMEND, ['--products', 'zhinikefu', '--json'], env);
    fs.writeFileSync(path.join(stateDir, 'matrix-run-state.lock'), 'held\n');

    const result = await jsonOut(
      TRACK,
      ['shown', '--block-id', block.block_id, '--json'],
      { ...env, MATRIX_LOCK_WAIT_MS: '150' },
    );
    assert.equal(result.ok, false);
    assert.equal(result.skipped, true);
    assert.equal(result.reason, 'lock_timeout');
    assert.equal(result.lock_timeout, true);
    assert.equal(result.state_lock, false);
    assert.equal(events.length, 0, '无锁时不得发送');
  });

  await t.test('dry-run：--no-track 不发事件、不写去重状态', async () => {
    const stateDir = freshDir('dry-run');
    const config = writeConfig(stateDir, enabledConfig());
    const env = childEnv(stateDir, config);

    const block = await jsonOut(RECOMMEND, ['--products', 'zhinikefu', '--json'], env);
    const dry = await jsonOut(
      TRACK,
      ['shown', '--block-id', block.block_id, '--no-track', '--json'],
      env,
    );
    assert.equal(dry.dry_run, true);
    assert.deepEqual(dry.would_send, ['zhinikefu']);
    assert.equal(events.length, 0);

    const real = await jsonOut(
      TRACK,
      ['shown', '--block-id', block.block_id, '--json'],
      env,
    );
    assert.equal(real.events, 1, 'dry-run 不写去重状态，正式确认仍应上报');
  });
});

server.close();
