import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

// MATRIX_CONFIG 必须在 import analytics.mjs 之前设置（模块加载时读一次）。
const tmpRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'matrix-analytics-test-'));
process.env.MATRIX_STATE_DIR = path.join(tmpRoot, 'state');
process.env.MATRIX_CONFIG = path.join(tmpRoot, 'posthog.json');

const analytics = await import('../scripts/lib/analytics.mjs');
const { EVENT_NAMES } = await import('../scripts/lib/identity.mjs');

const VALID_TOKEN = 'phc_mocktoken12345678';

function writeConfig(config) {
  fs.writeFileSync(process.env.MATRIX_CONFIG, JSON.stringify(config, null, 2));
}

function resetEnv() {
  for (const key of [
    'MATRIX_TELEMETRY', 'GEWEI_TELEMETRY', 'DO_NOT_TRACK',
    'MATRIX_POSTHOG_HOST', 'GEWEI_POSTHOG_HOST', 'POSTHOG_HOST',
    'MATRIX_POSTHOG_KEY', 'GEWEI_POSTHOG_KEY', 'POSTHOG_PROJECT_TOKEN',
  ]) delete process.env[key];
}

test('默认配置：无 Token、enabled:false → not_configured，不发送', () => {
  resetEnv();
  writeConfig({ enabled: false, projectToken: '', trackId: 'zhini-skill-matrix' });
  const status = analytics.getAnalyticsStatus();
  assert.equal(status.enabled, false);
  assert.equal(status.disabled_reason, 'not_configured');
  assert.equal(status.token_configured, false);
});

test('enabled:true + 有效 Token → 开启（https 主机）', () => {
  resetEnv();
  writeConfig({ enabled: true, projectToken: VALID_TOKEN, trackId: 'zhini-skill-matrix' });
  const status = analytics.getAnalyticsStatus();
  assert.equal(status.enabled, true);
  assert.equal(status.disabled_reason, null);
  assert.equal(status.host, 'https://us.i.posthog.com');
});

test('占位 Token（phc_replace_ 前缀）视为未配置', () => {
  resetEnv();
  writeConfig({ enabled: true, projectToken: 'phc_replace_me_please' });
  const status = analytics.getAnalyticsStatus();
  assert.equal(status.enabled, false);
  assert.equal(status.disabled_reason, 'not_configured');
});

test('http:// 非回环主机 → insecure_host，禁止明文外发', () => {
  resetEnv();
  writeConfig({ enabled: true, projectToken: VALID_TOKEN });
  process.env.MATRIX_POSTHOG_HOST = 'http://evil.example.com';
  const status = analytics.getAnalyticsStatus();
  assert.equal(status.enabled, false);
  assert.equal(status.disabled_reason, 'insecure_host');
});

test('http:// 回环地址（本地测试）允许', () => {
  resetEnv();
  writeConfig({ enabled: true, projectToken: VALID_TOKEN });
  process.env.MATRIX_POSTHOG_HOST = 'http://127.0.0.1:8123';
  const status = analytics.getAnalyticsStatus();
  assert.equal(status.enabled, true);
  assert.equal(status.host, 'http://127.0.0.1:8123');
});

test('MATRIX_TELEMETRY=1 显式同意可覆盖 enabled:false', () => {
  resetEnv();
  writeConfig({ enabled: false, projectToken: VALID_TOKEN });
  process.env.MATRIX_TELEMETRY = '1';
  const status = analytics.getAnalyticsStatus();
  assert.equal(status.enabled, true);
});

test('MATRIX_TELEMETRY=0 强制关闭优先于配置开启', () => {
  resetEnv();
  writeConfig({ enabled: true, projectToken: VALID_TOKEN });
  process.env.MATRIX_TELEMETRY = '0';
  const status = analytics.getAnalyticsStatus();
  assert.equal(status.enabled, false);
  assert.equal(status.disabled_reason, 'opted_out');
});

test('DO_NOT_TRACK=1 永远优先于显式同意', () => {
  resetEnv();
  writeConfig({ enabled: true, projectToken: VALID_TOKEN });
  process.env.MATRIX_TELEMETRY = '1';
  process.env.DO_NOT_TRACK = '1';
  const status = analytics.getAnalyticsStatus();
  assert.equal(status.enabled, false);
  assert.equal(status.disabled_reason, 'opted_out');
});

test('stableEventUuid：同一事件身份稳定，不同事件不碰撞', () => {
  const a = analytics.stableEventUuid('plugin-a', 'matrix_skill_loaded', 'run_1');
  const b = analytics.stableEventUuid('plugin-a', 'matrix_skill_loaded', 'run_1');
  const c = analytics.stableEventUuid('plugin-a', 'matrix_skill_loaded', 'run_2');
  assert.equal(a, b, '同参数重试必须复用同一 uuid');
  assert.notEqual(a, c);
  assert.match(a, /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/);
});

test('trackEvent：未开启时跳过且带原因', async () => {
  resetEnv();
  writeConfig({ enabled: false, projectToken: '' });
  const result = await analytics.trackEvent(EVENT_NAMES.loaded, {}, { agent: 'test' });
  assert.equal(result.ok, false);
  assert.equal(result.skipped, true);
  assert.equal(result.reason, 'not_configured');
});

test('trackEvent：未知事件拒绝发送', async () => {
  resetEnv();
  writeConfig({ enabled: true, projectToken: VALID_TOKEN });
  const result = await analytics.trackEvent('matrix_fake_event', {});
  assert.equal(result.ok, false);
  assert.equal(result.skipped, true);
  assert.equal(result.reason, 'invalid_event');
});

test('channel/surface/agent 非法值回落 unknown', () => {
  assert.equal(analytics.normalizeChannel('非法!!!'), 'unknown');
  assert.equal(analytics.normalizeChannel('official'), 'official');
  assert.equal(analytics.normalizeSurface(''), 'agent-skill');
  assert.equal(analytics.normalizeAgent(undefined), 'unknown');
});
