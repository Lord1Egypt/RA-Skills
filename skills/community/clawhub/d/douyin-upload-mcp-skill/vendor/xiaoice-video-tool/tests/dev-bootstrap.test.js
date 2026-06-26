const test = require('node:test');
const assert = require('node:assert/strict');
const path = require('node:path');

const { resolveStateDir, selectNgrokTunnel } = require('../scripts/dev-utils');
const { syncCallbackPublicBaseUrl } = require('../scripts/dev-callback-sync');
const { runDevUp } = require('../scripts/dev-up');
const { runDoctor } = require('../scripts/dev-doctor');

test('resolveStateDir resolves relative path against repo root', () => {
  const repoRoot = path.join(path.sep, 'tmp', 'xvt-repo');

  assert.equal(
    resolveStateDir('./data', repoRoot),
    path.join(repoRoot, 'data')
  );
  assert.equal(
    resolveStateDir('nested/state', repoRoot),
    path.join(repoRoot, 'nested', 'state')
  );
  assert.equal(
    resolveStateDir(path.join(path.sep, 'var', 'tmp', 'state'), repoRoot),
    path.join(path.sep, 'var', 'tmp', 'state')
  );
});

test('selectNgrokTunnel prefers exact-port https tunnel when multiple tunnels exist', () => {
  const tunnels = [
    {
      public_url: 'https://wrong-port.ngrok.app',
      proto: 'https',
      config: { addr: 'http://127.0.0.1:3999' },
    },
    {
      public_url: 'http://correct-port-http.ngrok.app',
      proto: 'http',
      config: { addr: 'http://127.0.0.1:3105' },
    },
    {
      public_url: 'https://correct-port.ngrok.app',
      proto: 'https',
      config: { addr: 'http://localhost:3105' },
    },
  ];

  const selected = selectNgrokTunnel(tunnels, 3105);

  assert.ok(selected);
  assert.equal(selected.publicUrl, 'https://correct-port.ngrok.app');
  assert.equal(selected.addrPort, 3105);
  assert.equal(selected.localAddr, 'http://localhost:3105');
});

test('syncCallbackPublicBaseUrl sends minimal PUT payload with admin token', async () => {
  const calls = [];
  const callbackPublicBaseUrl = 'https://demo.ngrok.app';

  await syncCallbackPublicBaseUrl({
    serviceBaseUrl: 'http://127.0.0.1:3105',
    adminToken: 'admin-token-123',
    callbackPublicBaseUrl,
    fetchImpl: async (url, init) => {
      calls.push({ url, init });
      return {
        ok: true,
        status: 200,
        async text() {
          return JSON.stringify({ data: { callbackPublicBaseUrl } });
        },
      };
    },
  });

  assert.equal(calls.length, 1);
  assert.equal(calls[0].url, 'http://127.0.0.1:3105/v1/admin/config');
  assert.equal(calls[0].init.method, 'PUT');
  assert.equal(calls[0].init.headers['X-Admin-Token'], 'admin-token-123');
  assert.deepEqual(JSON.parse(calls[0].init.body), {
    callbackPublicBaseUrl,
  });
});

test('runDevUp fails fast when required tokens are missing in ngrok mode', async () => {
  await assert.rejects(
    runDevUp({
      env: {
        VIDEO_USE_NGROK: 'true',
        VIDEO_SERVICE_CALLBACK_TOKEN: 'callback-token',
      },
      deps: {
        async ensureService() {},
        async ensureNgrok() {},
        async syncCallback() {},
      },
    }),
    (error) => error && error.code === 'MISSING_ADMIN_TOKEN'
  );

  await assert.rejects(
    runDevUp({
      env: {
        VIDEO_USE_NGROK: 'true',
        VIDEO_SERVICE_ADMIN_TOKEN: 'admin-token',
      },
      deps: {
        async ensureService() {},
        async ensureNgrok() {},
        async syncCallback() {},
      },
    }),
    (error) => error && error.code === 'MISSING_CALLBACK_TOKEN'
  );
});

test('runDevUp fails when ngrok bootstrap step fails', async () => {
  await assert.rejects(
    runDevUp({
      env: {
        VIDEO_USE_NGROK: 'true',
        VIDEO_SERVICE_ADMIN_TOKEN: 'admin-token',
        VIDEO_SERVICE_CALLBACK_TOKEN: 'callback-token',
      },
      deps: {
        async ensureService() {
          return { healthUrl: 'http://127.0.0.1:3105/health' };
        },
        async ensureNgrok() {
          throw Object.assign(new Error('ngrok startup failed'), { code: 'NGROK_START_FAILED' });
        },
        async syncCallback() {},
      },
    }),
    (error) => error && error.code === 'NGROK_START_FAILED'
  );
});

test('runDoctor fails when callback base URL does not match ngrok URL', async () => {
  await assert.rejects(
    runDoctor({
      env: {
        VIDEO_TASK_SERVICE_HOST: '127.0.0.1',
        VIDEO_TASK_SERVICE_PORT: '3105',
        VIDEO_USE_NGROK: 'true',
      },
      deps: {
        async checkHealth() {
          return { ok: true, healthUrl: 'http://127.0.0.1:3105/health' };
        },
        async getNgrokStatus() {
          return { publicUrl: 'https://from-ngrok.ngrok.app' };
        },
        async getSyncedCallbackBaseUrl() {
          return 'https://from-runtime-config.ngrok.app';
        },
        async checkCallbackEndpoint() {
          return { ok: true };
        },
      },
    }),
    (error) => error && error.code === 'CALLBACK_URL_MISMATCH'
  );
});
